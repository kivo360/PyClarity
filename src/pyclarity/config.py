"""
Configuration management for PyClarity MCP Server
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class AuthConfig(BaseModel):
    """Authentication configuration"""

    enabled: bool = Field(default=True, description="Enable authentication")
    jwt_secret: str = Field(default="your-secret-key", description="JWT secret key")
    jwt_expiry: int = Field(default=3600, description="JWT token expiry in seconds")
    api_key_rotation_days: int = Field(default=30, description="API key rotation period")
    rate_limit_requests: int = Field(default=100, description="Rate limit requests per window")
    rate_limit_window: int = Field(default=3600, description="Rate limit window in seconds")


class ServerConfig(BaseModel):
    """Server configuration"""

    host: str = Field(default="localhost", description="Server host")
    port: int = Field(default=8000, description="Server port")
    debug: bool = Field(default=False, description="Enable debug mode")


class ToolConfig(BaseModel):
    """Tool configuration"""

    enabled: bool = Field(default=True, description="Enable the tool")
    rate_limit: int = Field(default=10, description="Rate limit for this tool")
    requires_auth: bool = Field(default=True, description="Whether tool requires authentication")


class MCPConfig(BaseSettings):
    """Main configuration for PyClarity MCP Server"""

    # Server configuration
    server: ServerConfig = Field(default_factory=ServerConfig)

    # Authentication configuration
    auth: AuthConfig = Field(default_factory=AuthConfig)

    # Tool configurations
    tools: dict[str, ToolConfig] = Field(default_factory=dict)

    # Database configuration
    database_url: str = Field(
        default="postgresql://pyclarity:pyclarity@postgres:5432/pyclarity",
        description="Database connection URL",
    )

    # Logging configuration
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s", description="Log format"
    )

    model_config = {
        "env_prefix": "MCP_",
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",  # Ignore extra fields from environment
    }

    @classmethod
    def from_file(cls, config_path: str) -> "MCPConfig":
        """Load configuration from file"""
        config_file = Path(config_path)
        if not config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        # Load environment variables from file
        with open(config_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[f"MCP_{key.upper()}"] = value

        return cls()

    def get_tool_config(self, tool_name: str) -> ToolConfig:
        """Get configuration for a specific tool"""
        return self.tools.get(tool_name, ToolConfig())

    def is_tool_enabled(self, tool_name: str) -> bool:
        """Check if a tool is enabled"""
        tool_config = self.get_tool_config(tool_name)
        return tool_config.enabled


# Default configuration
default_config = MCPConfig()
