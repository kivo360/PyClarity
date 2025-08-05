"""Base store for Debugging Approaches tool session management."""

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class DebuggingHypothesis(BaseModel):
    """Model for a debugging hypothesis."""
    
    hypothesis_id: Optional[int] = Field(None, description="Unique hypothesis ID")
    statement: str = Field(..., description="Hypothesis statement")
    evidence_for: List[str] = Field(default_factory=list, description="Supporting evidence")
    evidence_against: List[str] = Field(default_factory=list, description="Contradicting evidence")
    test_method: Optional[str] = Field(None, description="How to test this hypothesis")
    status: str = Field("proposed", description="Status: proposed, testing, validated, refuted")
    confidence: float = Field(0.5, description="Confidence level")


class DebuggingData(BaseModel):
    """Data model for debugging session storage."""
    
    id: Optional[int] = Field(None, description="Database ID")
    session_id: str = Field(..., description="Session this step belongs to")
    step_number: int = Field(..., description="Sequential step number")
    debugging_type: str = Field(..., description="Type: systematic, rubber_duck, bisection, pattern_matching")
    
    # Problem description
    issue_description: str = Field(..., description="Description of the issue")
    error_message: Optional[str] = Field(None, description="Error message if applicable")
    stack_trace: Optional[str] = Field(None, description="Stack trace if available")
    
    # Debugging process
    hypothesis: Optional[DebuggingHypothesis] = Field(None, description="Current hypothesis")
    evidence_gathered: List[str] = Field(default_factory=list, description="Evidence collected")
    tests_performed: List[Dict[str, Any]] = Field(default_factory=list, description="Tests run")
    validation_result: Optional[Dict[str, Any]] = Field(None, description="Validation outcome")
    
    # Insights and next steps
    insights: List[str] = Field(default_factory=list, description="Insights discovered")
    next_steps: List[str] = Field(default_factory=list, description="Recommended next actions")
    root_cause: Optional[str] = Field(None, description="Identified root cause")
    solution: Optional[str] = Field(None, description="Solution if found")
    
    # Metadata
    confidence: float = Field(0.5, description="Confidence in current direction")
    time_spent_minutes: Optional[float] = Field(None, description="Time spent on this step")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)


class BaseDebuggingStore(ABC):
    """Abstract base class for debugging session storage operations."""
    
    @abstractmethod
    async def save_debugging_step(self, debug_data: DebuggingData) -> DebuggingData:
        """Save a new debugging step."""
        pass
    
    @abstractmethod
    async def get_debugging_step(self, step_id: int) -> Optional[DebuggingData]:
        """Get a specific debugging step by ID."""
        pass
    
    @abstractmethod
    async def get_session_steps(self, session_id: str) -> List[DebuggingData]:
        """Get all debugging steps for a session."""
        pass
    
    @abstractmethod
    async def get_hypotheses(
        self, 
        session_id: str, 
        status: Optional[str] = None
    ) -> List[DebuggingHypothesis]:
        """Get all hypotheses for a session, optionally filtered by status."""
        pass
    
    @abstractmethod
    async def update_hypothesis_status(
        self, 
        step_id: int, 
        hypothesis_id: int,
        status: str, 
        evidence: Dict[str, Any]
    ) -> Optional[DebuggingData]:
        """Update the status of a hypothesis with new evidence."""
        pass
    
    @abstractmethod
    async def add_test_result(
        self,
        step_id: int,
        test_name: str,
        test_result: Dict[str, Any]
    ) -> Optional[DebuggingData]:
        """Add a test result to a debugging step."""
        pass
    
    @abstractmethod
    async def mark_solution_found(
        self,
        session_id: str,
        root_cause: str,
        solution: str,
        confidence: float
    ) -> Optional[DebuggingData]:
        """Mark that a solution has been found for the session."""
        pass
    
    @abstractmethod
    async def get_debugging_patterns(
        self,
        session_id: Optional[str] = None,
        debugging_type: Optional[str] = None,
        min_confidence: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """Analyze debugging patterns across sessions."""
        pass
    
    @abstractmethod
    async def search_debugging_sessions(
        self,
        issue_query: Optional[str] = None,
        error_type: Optional[str] = None,
        solved_only: bool = False,
        limit: int = 100
    ) -> List[DebuggingData]:
        """Search debugging sessions with various filters."""
        pass