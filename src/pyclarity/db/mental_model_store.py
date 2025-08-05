"""Base store for Mental Models tool session management."""

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from pyclarity.tools.mental_models.models import MentalModelType


class MentalModelData(BaseModel):
    """Data model for mental model application storage."""
    
    id: Optional[int] = Field(None, description="Database ID")
    session_id: str = Field(..., description="Session this application belongs to")
    model_type: MentalModelType = Field(..., description="Type of mental model applied")
    problem_statement: str = Field(..., description="Problem being analyzed")
    context: Optional[str] = Field(None, description="Additional context provided")
    
    # Model outputs
    insights: List[Dict[str, Any]] = Field(default_factory=list, description="Key insights generated")
    recommendations: List[str] = Field(default_factory=list, description="Action recommendations")
    assumptions: List[Dict[str, Any]] = Field(default_factory=list, description="Assumptions identified")
    fundamental_elements: Optional[List[str]] = Field(None, description="For first principles")
    trade_offs: Optional[List[Dict[str, Any]]] = Field(None, description="For opportunity cost")
    error_impacts: Optional[List[Dict[str, Any]]] = Field(None, description="For error propagation")
    
    # Metadata
    confidence_score: float = Field(0.85, description="Overall confidence in analysis")
    limitations: Optional[str] = Field(None, description="Model limitations identified")
    next_steps: List[str] = Field(default_factory=list, description="Suggested next steps")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)


class BaseMentalModelStore(ABC):
    """Abstract base class for mental model storage operations."""
    
    @abstractmethod
    async def save_model_application(self, model_data: MentalModelData) -> MentalModelData:
        """Save a new mental model application."""
        pass
    
    @abstractmethod
    async def get_model_application(self, application_id: int) -> Optional[MentalModelData]:
        """Get a specific model application by ID."""
        pass
    
    @abstractmethod
    async def get_session_models(self, session_id: str) -> List[MentalModelData]:
        """Get all model applications for a session."""
        pass
    
    @abstractmethod
    async def get_models_by_type(
        self, 
        session_id: str, 
        model_type: MentalModelType
    ) -> List[MentalModelData]:
        """Get all applications of a specific model type in a session."""
        pass
    
    @abstractmethod
    async def update_model_insights(
        self, 
        application_id: int, 
        insights: List[Dict[str, Any]]
    ) -> Optional[MentalModelData]:
        """Update insights for a model application."""
        pass
    
    @abstractmethod
    async def update_model_confidence(
        self, 
        application_id: int, 
        confidence: float
    ) -> Optional[MentalModelData]:
        """Update confidence score for a model application."""
        pass
    
    @abstractmethod
    async def search_models(
        self,
        session_id: Optional[str] = None,
        problem_query: Optional[str] = None,
        model_type: Optional[MentalModelType] = None,
        min_confidence: Optional[float] = None,
        limit: int = 100
    ) -> List[MentalModelData]:
        """Search model applications with various filters."""
        pass
    
    @abstractmethod
    async def get_model_sequence(self, session_id: str) -> List[MentalModelData]:
        """Get model applications in chronological order for a session."""
        pass
    
    @abstractmethod
    async def count_session_models(self, session_id: str) -> Dict[str, int]:
        """Count model applications by type in a session."""
        pass