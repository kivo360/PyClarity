"""Base classes for database-agnostic session state management."""

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, TypeVar

from pydantic import BaseModel, Field


class SessionData(BaseModel):
    """Data model for session storage."""
    
    session_id: str = Field(..., description="Unique session identifier")
    tool_name: str = Field(..., description="Name of the cognitive tool")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)
    active: bool = Field(default=True)


class ThoughtData(BaseModel):
    """Data model for sequential thinking thought storage."""
    
    id: Optional[int] = Field(None, description="Database ID")
    session_id: str = Field(..., description="Session this thought belongs to")
    thought_number: int = Field(..., description="Sequential number of the thought")
    total_thoughts: int = Field(..., description="Expected total thoughts in sequence")
    content: str = Field(..., description="The thought content")
    thought_type: Optional[str] = Field(None, description="Type of reasoning step")
    confidence: float = Field(0.85, description="Confidence score")
    branch_id: Optional[str] = Field(None, description="Branch identifier if branching")
    branch_from_thought: Optional[int] = Field(None, description="Parent thought for branches")
    revises_thought: Optional[int] = Field(None, description="ID of thought being revised")
    is_revision: bool = Field(default=False)
    needs_more_thoughts: bool = Field(default=False)
    next_thought_needed: bool = Field(default=True)
    supporting_evidence: List[str] = Field(default_factory=list)
    assumptions_made: List[str] = Field(default_factory=list)
    potential_errors: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)


T = TypeVar('T', bound=BaseModel)


class BaseSessionStore(ABC):
    """Abstract base class for session storage operations."""
    
    @abstractmethod
    async def create_session(self, session_data: SessionData) -> SessionData:
        """Create a new session."""
        pass
    
    @abstractmethod
    async def get_session(self, session_id: str) -> Optional[SessionData]:
        """Get session by ID."""
        pass
    
    @abstractmethod
    async def update_session(self, session_id: str, updates: Dict[str, Any]) -> Optional[SessionData]:
        """Update session data."""
        pass
    
    @abstractmethod
    async def delete_session(self, session_id: str) -> bool:
        """Delete a session."""
        pass
    
    @abstractmethod
    async def list_sessions(
        self, 
        tool_name: Optional[str] = None,
        active_only: bool = True,
        limit: int = 100,
        offset: int = 0
    ) -> List[SessionData]:
        """List sessions with optional filtering."""
        pass
    
    @abstractmethod
    async def cleanup_old_sessions(self, days_old: int = 7) -> int:
        """Clean up sessions older than specified days."""
        pass


class BaseThoughtStore(ABC):
    """Abstract base class for thought storage operations."""
    
    @abstractmethod
    async def save_thought(self, thought: ThoughtData) -> ThoughtData:
        """Save a new thought."""
        pass
    
    @abstractmethod
    async def get_thought(self, thought_id: int) -> Optional[ThoughtData]:
        """Get a thought by ID."""
        pass
    
    @abstractmethod
    async def get_session_thoughts(
        self, 
        session_id: str,
        branch_id: Optional[str] = None
    ) -> List[ThoughtData]:
        """Get all thoughts for a session, optionally filtered by branch."""
        pass
    
    @abstractmethod
    async def get_latest_thought(
        self,
        session_id: str,
        branch_id: Optional[str] = None
    ) -> Optional[ThoughtData]:
        """Get the most recent thought for a session/branch."""
        pass
    
    @abstractmethod
    async def update_thought(self, thought_id: int, updates: Dict[str, Any]) -> Optional[ThoughtData]:
        """Update an existing thought."""
        pass
    
    @abstractmethod
    async def delete_thought(self, thought_id: int) -> bool:
        """Delete a thought."""
        pass
    
    @abstractmethod
    async def count_session_thoughts(self, session_id: str) -> int:
        """Count thoughts in a session."""
        pass
    
    @abstractmethod
    async def get_branch_thoughts(self, session_id: str, branch_id: str) -> List[ThoughtData]:
        """Get all thoughts for a specific branch."""
        pass
    
    @abstractmethod
    async def search_thoughts(
        self,
        session_id: Optional[str] = None,
        content_query: Optional[str] = None,
        thought_type: Optional[str] = None,
        min_confidence: Optional[float] = None,
        limit: int = 100
    ) -> List[ThoughtData]:
        """Search thoughts with various filters."""
        pass