"""Base store for Decision Framework tool session management."""

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class DecisionOption(BaseModel):
    """Model for a decision option."""
    
    option_id: str = Field(..., description="Unique identifier for the option")
    name: str = Field(..., description="Name of the option")
    description: str = Field(..., description="Detailed description")
    pros: List[str] = Field(default_factory=list, description="Advantages")
    cons: List[str] = Field(default_factory=list, description="Disadvantages")
    feasibility: float = Field(0.5, description="Feasibility score (0-1)")
    risk_level: float = Field(0.5, description="Risk level (0-1)")


class DecisionCriterion(BaseModel):
    """Model for a decision criterion."""
    
    criterion_id: str = Field(..., description="Unique identifier")
    name: str = Field(..., description="Criterion name")
    description: str = Field(..., description="What this criterion measures")
    weight: float = Field(1.0, description="Importance weight")
    optimization_direction: str = Field("maximize", description="maximize or minimize")


class DecisionRecommendation(BaseModel):
    """Model for the final recommendation."""
    
    recommended_option_id: str = Field(..., description="ID of recommended option")
    confidence: float = Field(..., description="Confidence in recommendation (0-1)")
    rationale: str = Field(..., description="Explanation of recommendation")
    alternative_option_id: Optional[str] = Field(None, description="Second best option")
    conditions: List[str] = Field(default_factory=list, description="Conditions for recommendation")


class DecisionData(BaseModel):
    """Data model for decision framework storage."""
    
    id: Optional[int] = Field(None, description="Database ID")
    session_id: str = Field(..., description="Session this decision belongs to")
    
    # Decision context
    decision_statement: str = Field(..., description="What decision is being made")
    context: Optional[str] = Field(None, description="Additional context")
    constraints: List[str] = Field(default_factory=list, description="Constraints to consider")
    analysis_type: str = Field(..., description="Type: pros_cons, multi_criteria, cost_benefit, risk_reward")
    
    # Decision components
    options: List[DecisionOption] = Field(default_factory=list, description="Available options")
    criteria: List[DecisionCriterion] = Field(default_factory=list, description="Evaluation criteria")
    
    # Evaluation data
    scores: Dict[str, Dict[str, float]] = Field(
        default_factory=dict, 
        description="Scores: option_id -> criterion_id -> score"
    )
    normalized_scores: Dict[str, Dict[str, float]] = Field(
        default_factory=dict,
        description="Normalized scores for comparison"
    )
    weighted_totals: Dict[str, float] = Field(
        default_factory=dict,
        description="Total weighted score per option"
    )
    
    # Analysis results
    recommendation: Optional[DecisionRecommendation] = Field(None, description="Final recommendation")
    sensitivity_analysis: Optional[Dict[str, Any]] = Field(None, description="Sensitivity to weight changes")
    trade_off_analysis: Optional[Dict[str, Any]] = Field(None, description="Trade-off insights")
    
    # Metadata
    confidence: float = Field(0.5, description="Overall confidence in analysis")
    completeness: float = Field(0.0, description="How complete the analysis is (0-1)")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)


class BaseDecisionStore(ABC):
    """Abstract base class for decision framework storage operations."""
    
    @abstractmethod
    async def save_decision(self, decision_data: DecisionData) -> DecisionData:
        """Save a new decision analysis."""
        pass
    
    @abstractmethod
    async def get_decision(self, decision_id: int) -> Optional[DecisionData]:
        """Get a specific decision by ID."""
        pass
    
    @abstractmethod
    async def get_session_decisions(self, session_id: str) -> List[DecisionData]:
        """Get all decisions for a session."""
        pass
    
    @abstractmethod
    async def add_option(
        self, 
        decision_id: int, 
        option: DecisionOption
    ) -> Optional[DecisionData]:
        """Add an option to a decision."""
        pass
    
    @abstractmethod
    async def add_criterion(
        self, 
        decision_id: int, 
        criterion: DecisionCriterion
    ) -> Optional[DecisionData]:
        """Add a criterion to a decision."""
        pass
    
    @abstractmethod
    async def update_scores(
        self, 
        decision_id: int, 
        option_id: str, 
        criterion_scores: Dict[str, float]
    ) -> Optional[DecisionData]:
        """Update scores for an option."""
        pass
    
    @abstractmethod
    async def save_recommendation(
        self,
        decision_id: int,
        recommendation: DecisionRecommendation
    ) -> Optional[DecisionData]:
        """Save the final recommendation."""
        pass
    
    @abstractmethod
    async def get_decision_quality(self, decision_id: int) -> Dict[str, Any]:
        """Calculate quality metrics for a decision."""
        pass
    
    @abstractmethod
    async def search_decisions(
        self,
        keywords: Optional[str] = None,
        analysis_type: Optional[str] = None,
        min_confidence: Optional[float] = None,
        has_recommendation: Optional[bool] = None,
        limit: int = 100
    ) -> List[DecisionData]:
        """Search decisions with various filters."""
        pass
    
    @abstractmethod
    async def get_decision_patterns(
        self,
        analysis_type: Optional[str] = None,
        min_decisions: int = 5
    ) -> Dict[str, Any]:
        """Analyze patterns across decisions."""
        pass