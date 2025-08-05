"""Base store for Collaborative Reasoning tool session management."""

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class PerspectiveData(BaseModel):
    """Data model for individual perspective storage."""
    
    id: Optional[int] = Field(None, description="Database ID")
    session_id: str = Field(..., description="Session this perspective belongs to")
    persona_name: str = Field(..., description="Name of the persona/stakeholder")
    perspective_type: str = Field(..., description="Type: technical, business, user, regulatory, etc.")
    
    # Perspective content
    viewpoint: str = Field(..., description="Main viewpoint or position")
    supporting_arguments: List[str] = Field(default_factory=list, description="Supporting points")
    concerns: List[str] = Field(default_factory=list, description="Concerns or objections")
    priorities: List[str] = Field(default_factory=list, description="Key priorities from this perspective")
    
    # Relationships
    conflicts_with: List[int] = Field(default_factory=list, description="IDs of conflicting perspectives")
    aligns_with: List[int] = Field(default_factory=list, description="IDs of aligned perspectives")
    
    # Metadata
    confidence: float = Field(0.85, description="Confidence in this perspective")
    influence_weight: float = Field(1.0, description="Weight of this perspective in synthesis")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ConflictData(BaseModel):
    """Data model for perspective conflicts."""
    
    id: Optional[int] = Field(None, description="Database ID")
    session_id: str = Field(..., description="Session this conflict belongs to")
    perspective_a_id: int = Field(..., description="First perspective ID")
    perspective_b_id: int = Field(..., description="Second perspective ID")
    
    # Conflict details
    conflict_type: str = Field(..., description="Type: priority, approach, resource, timeline")
    description: str = Field(..., description="Description of the conflict")
    severity: float = Field(0.5, description="Severity of conflict (0-1)")
    
    # Resolution
    resolved: bool = Field(False, description="Whether conflict is resolved")
    resolution: Optional[str] = Field(None, description="How the conflict was resolved")
    compromise_needed: bool = Field(False, description="Whether compromise was required")
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class CollaborativeSynthesis(BaseModel):
    """Data model for synthesized collaborative outcome."""
    
    id: Optional[int] = Field(None, description="Database ID")
    session_id: str = Field(..., description="Session this synthesis belongs to")
    
    # Synthesis content
    consensus_points: List[str] = Field(default_factory=list, description="Points of agreement")
    divergence_points: List[str] = Field(default_factory=list, description="Points of disagreement")
    integrated_solution: str = Field(..., description="Integrated solution or approach")
    
    # Perspective integration
    perspectives_included: List[int] = Field(default_factory=list, description="IDs of perspectives included")
    weighting_rationale: str = Field(..., description="How perspectives were weighted")
    
    # Quality metrics
    consensus_level: float = Field(0.0, description="Overall consensus level (0-1)")
    completeness: float = Field(0.0, description="How complete the synthesis is (0-1)")
    feasibility_score: float = Field(0.0, description="Feasibility of integrated solution (0-1)")
    
    # Recommendations
    implementation_plan: List[str] = Field(default_factory=list, description="Steps to implement")
    risk_mitigation: List[str] = Field(default_factory=list, description="Risks and mitigations")
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)


class BaseCollaborativeStore(ABC):
    """Abstract base class for collaborative reasoning storage operations."""
    
    @abstractmethod
    async def save_perspective(self, perspective_data: PerspectiveData) -> PerspectiveData:
        """Save a new perspective."""
        pass
    
    @abstractmethod
    async def get_perspective(self, perspective_id: int) -> Optional[PerspectiveData]:
        """Get a specific perspective by ID."""
        pass
    
    @abstractmethod
    async def get_session_perspectives(self, session_id: str) -> List[PerspectiveData]:
        """Get all perspectives for a session."""
        pass
    
    @abstractmethod
    async def get_perspectives_by_type(
        self, 
        session_id: str, 
        perspective_type: str
    ) -> List[PerspectiveData]:
        """Get perspectives of a specific type."""
        pass
    
    @abstractmethod
    async def save_conflict(self, conflict_data: ConflictData) -> ConflictData:
        """Save a new conflict between perspectives."""
        pass
    
    @abstractmethod
    async def get_conflicts(
        self, 
        session_id: str, 
        resolved: Optional[bool] = None
    ) -> List[ConflictData]:
        """Get conflicts for a session, optionally filtered by resolution status."""
        pass
    
    @abstractmethod
    async def resolve_conflict(
        self,
        conflict_id: int,
        resolution: str,
        compromise_needed: bool
    ) -> Optional[ConflictData]:
        """Mark a conflict as resolved."""
        pass
    
    @abstractmethod
    async def save_synthesis(self, synthesis: CollaborativeSynthesis) -> CollaborativeSynthesis:
        """Save a collaborative synthesis."""
        pass
    
    @abstractmethod
    async def get_synthesis(self, session_id: str) -> Optional[CollaborativeSynthesis]:
        """Get the synthesis for a session."""
        pass
    
    @abstractmethod
    async def update_consensus_level(
        self,
        session_id: str,
        consensus_level: float
    ) -> Optional[CollaborativeSynthesis]:
        """Update the consensus level for a synthesis."""
        pass
    
    @abstractmethod
    async def find_similar_perspectives(
        self,
        perspective_id: int,
        threshold: float = 0.7
    ) -> List[PerspectiveData]:
        """Find perspectives similar to a given one."""
        pass
    
    @abstractmethod
    async def get_collaboration_metrics(self, session_id: str) -> Dict[str, Any]:
        """Get collaboration metrics for a session."""
        pass