"""
Authentication middleware for PyClarity MCP Server
"""

import logging
import time
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import jwt
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class User(BaseModel):
    """User model for authentication"""

    id: str
    username: str
    role: str = "user"
    permissions: list = []


class AuthMiddleware:
    """Authentication middleware for JWT and API key authentication"""

    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.security = HTTPBearer(auto_error=False)

    def create_token(
        self, user_data: dict[str, Any], expires_delta: timedelta | None = None
    ) -> str:
        """Create a JWT token"""
        to_encode = user_data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(hours=1)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_token(self, token: str) -> dict[str, Any]:
        """Verify a JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def verify_api_key(self, api_key: str) -> dict[str, Any] | None:
        """Verify an API key (placeholder for now)"""
        # In a real implementation, you would check against a database
        # For now, we'll use a simple check
        if api_key.startswith("pyclarity_"):
            return {
                "id": "api_user",
                "username": "api_user",
                "role": "user",
                "permissions": ["read", "execute"],
            }
        return None

    async def get_current_user(self, request: Request) -> User | None:
        """Get the current authenticated user"""
        # Check for API key in headers
        api_key = request.headers.get("X-API-Key")
        if api_key:
            user_data = self.verify_api_key(api_key)
            if user_data:
                return User(**user_data)

        # Check for JWT token
        credentials: HTTPAuthorizationCredentials = await self.security(request)
        if credentials:
            token = credentials.credentials
            payload = self.verify_token(token)
            return User(**payload)

        return None

    async def require_auth(self, request: Request) -> User:
        """Require authentication - raises 401 if not authenticated"""
        user = await self.get_current_user(request)
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Authentication required",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    async def require_role(self, role: str):
        """Require a specific role"""

        async def role_checker(request: Request) -> User:
            user = await self.require_auth(request)
            if user.role != role and user.role != "admin":
                raise HTTPException(status_code=403, detail=f"Role '{role}' required")
            return user

        return role_checker

    def rate_limit_check(self, user_id: str, endpoint: str) -> bool:
        """Check rate limiting for a user and endpoint"""
        # This is a simple in-memory rate limiter
        # In production, you'd use Redis or similar
        current_time = time.time()
        key = f"{user_id}:{endpoint}"

        # Simple rate limiting logic
        # In a real implementation, you'd track requests per time window
        return True


class RateLimiter:
    """Simple rate limiter for API endpoints"""

    def __init__(self):
        self.requests = {}

    def is_allowed(self, user_id: str, endpoint: str, limit: int, window: int) -> bool:
        """Check if request is allowed based on rate limits"""
        current_time = time.time()
        key = f"{user_id}:{endpoint}"

        if key not in self.requests:
            self.requests[key] = []

        # Remove old requests outside the window
        self.requests[key] = [
            req_time for req_time in self.requests[key] if current_time - req_time < window
        ]

        # Check if we're under the limit
        if len(self.requests[key]) < limit:
            self.requests[key].append(current_time)
            return True

        return False


# Global rate limiter instance
rate_limiter = RateLimiter()
