"""Base store for Metacognitive Monitoring tool session management."""

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class BiasIdentification(BaseModel):
    """Model for identified cognitive bias."""
    
    bias_type: str = Field(..., description="Type of bias: confirmation, anchoring, availability, etc.")
    description: str = Field(..., description="How the bias manifests")
    severity: float = Field(0.5, description="Severity of the bias (0-1)")
    evidence: List[str] = Field(default_factory=list, description="Evidence of the bias")
    mitigation_strategy: str = Field(..., description="How to counter this bias")


class QualityIndicator(BaseModel):
    """Model for thinking quality indicators."""
    
    indicator_name: str = Field(..., description="Name of quality indicator")
    score: float = Field(..., description="Score (0-1)")
    assessment: str = Field(..., description="Qualitative assessment")
    improvement_suggestions: List[str] = Field(default_factory=list)


class ImprovementSuggestion(BaseModel):
    """Model for cognitive improvement suggestions."""
    
    area: str = Field(..., description="Area for improvement")
    current_state: str = Field(..., description="Current approach")
    suggested_approach: str = Field(..., description="Better approach")
    expected_benefit: str = Field(..., description="Expected improvement")
    priority: float = Field(0.5, description="Priority level (0-1)")


class MetacognitiveData(BaseModel):
    """Data model for metacognitive monitoring storage."""
    
    id: Optional[int] = Field(None, description="Database ID")
    session_id: str = Field(..., description="Session this monitoring belongs to")
    
    # Monitoring context
    monitoring_type: str = Field(..., description="Type: self_assessment, bias_check, quality_review, progress_tracking")
    thinking_context: str = Field(..., description="What thinking process is being monitored")
    monitoring_depth: str = Field("standard", description="Depth: surface, standard, deep")
    
    # Observations
    thinking_pattern_observed: str = Field(..., description="Pattern of thinking observed")
    cognitive_strategies_used: List[str] = Field(default_factory=list, description="Strategies employed")
    decision_points: List[Dict[str, Any]] = Field(default_factory=list, description="Key decision points")
    
    # Analysis
    biases_identified: List[BiasIdentification] = Field(default_factory=list, description="Cognitive biases found")
    quality_indicators: List[QualityIndicator] = Field(default_factory=list, description="Quality metrics")
    strengths_observed: List[str] = Field(default_factory=list, description="Thinking strengths")
    weaknesses_observed: List[str] = Field(default_factory=list, description="Thinking weaknesses")
    
    # Improvements
    improvement_areas: List[ImprovementSuggestion] = Field(default_factory=list, description="Areas to improve")
    alternative_approaches: List[str] = Field(default_factory=list, description="Alternative thinking methods")
    
    # Self-assessment
    self_awareness_level: float = Field(0.5, description="Level of self-awareness (0-1)")
    adaptability_score: float = Field(0.5, description="How well thinking adapted (0-1)")
    confidence_in_assessment: float = Field(0.85, description="Confidence in this assessment")
    
    # Progress tracking
    improvement_from_last: Optional[float] = Field(None, description="Improvement from last assessment")
    goals_met: List[str] = Field(default_factory=list, description="Cognitive goals achieved")
    new_goals: List[str] = Field(default_factory=list, description="New cognitive goals set")
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)


class MetacognitiveProgress(BaseModel):
    """Model for tracking metacognitive progress over time."""
    
    session_id: str = Field(..., description="Session being tracked")
    assessments_count: int = Field(0, description="Number of assessments")
    
    # Progress metrics
    self_awareness_trend: List[float] = Field(default_factory=list, description="Self-awareness over time")
    bias_reduction_trend: List[float] = Field(default_factory=list, description="Bias reduction over time")
    quality_improvement_trend: List[float] = Field(default_factory=list, description="Quality improvement")
    
    # Patterns
    persistent_biases: List[str] = Field(default_factory=list, description="Biases that persist")
    resolved_issues: List[str] = Field(default_factory=list, description="Issues that were resolved")
    emerging_strengths: List[str] = Field(default_factory=list, description="New strengths developed")
    
    overall_progress_score: float = Field(0.0, description="Overall progress (0-1)")


class BaseMetacognitiveStore(ABC):
    """Abstract base class for metacognitive monitoring storage operations."""
    
    @abstractmethod
    async def save_monitoring_data(self, monitor_data: MetacognitiveData) -> MetacognitiveData:
        """Save new metacognitive monitoring data."""
        pass
    
    @abstractmethod
    async def get_monitoring_data(self, monitoring_id: int) -> Optional[MetacognitiveData]:
        """Get specific monitoring data by ID."""
        pass
    
    @abstractmethod
    async def get_session_monitoring(self, session_id: str) -> List[MetacognitiveData]:
        """Get all monitoring data for a session."""
        pass
    
    @abstractmethod
    async def get_monitoring_by_type(
        self, 
        session_id: str, 
        monitoring_type: str
    ) -> List[MetacognitiveData]:
        """Get monitoring data of a specific type."""
        pass
    
    @abstractmethod
    async def get_biases_identified(
        self, 
        session_id: str,
        bias_type: Optional[str] = None
    ) -> List[BiasIdentification]:
        """Get all biases identified in a session."""
        pass
    
    @abstractmethod
    async def add_improvement_suggestion(
        self,
        monitoring_id: int,
        suggestion: ImprovementSuggestion
    ) -> Optional[MetacognitiveData]:
        """Add an improvement suggestion to monitoring data."""
        pass
    
    @abstractmethod
    async def track_progress(self, session_id: str) -> MetacognitiveProgress:
        """Track metacognitive progress over a session."""
        pass
    
    @abstractmethod
    async def get_quality_trends(
        self,
        session_id: str,
        indicator_name: Optional[str] = None
    ) -> Dict[str, List[float]]:
        """Get quality indicator trends over time."""
        pass
    
    @abstractmethod
    async def find_similar_patterns(
        self,
        thinking_pattern: str,
        min_similarity: float = 0.7
    ) -> List[MetacognitiveData]:
        """Find similar thinking patterns across sessions."""
        pass
    
    @abstractmethod
    async def get_improvement_metrics(
        self,
        session_id: Optional[str] = None,
        time_period_days: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get improvement metrics over time."""
        pass