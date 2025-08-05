"""Base store for Creative Thinking tool session management."""

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel, Field


class CreativeIdea(BaseModel):
    """Model for a creative idea."""
    
    idea_id: Optional[int] = Field(None, description="Unique idea ID")
    title: str = Field(..., description="Idea title")
    description: str = Field(..., description="Detailed description")
    category: str = Field(..., description="Category: novel, adaptation, combination, transformation")
    originality_score: float = Field(0.5, description="How original (0-1)")
    feasibility_score: float = Field(0.5, description="How feasible (0-1)")
    impact_score: float = Field(0.5, description="Potential impact (0-1)")
    tags: List[str] = Field(default_factory=list, description="Idea tags")


class InspirationSource(BaseModel):
    """Model for sources of inspiration."""
    
    source_type: str = Field(..., description="Type: analogy, metaphor, constraint, random, cross_domain")
    source_content: str = Field(..., description="The inspiring element")
    how_it_inspired: str = Field(..., description="How it led to ideas")
    ideas_generated: List[int] = Field(default_factory=list, description="IDs of ideas from this source")


class CombinedIdea(BaseModel):
    """Model for ideas created by combining others."""
    
    combined_id: Optional[int] = Field(None, description="Combined idea ID")
    source_idea_ids: List[int] = Field(..., description="IDs of source ideas")
    combination_method: str = Field(..., description="How ideas were combined")
    emergent_properties: List[str] = Field(default_factory=list, description="New properties from combination")
    synergy_score: float = Field(0.5, description="How well ideas combine (0-1)")


class CreativityScore(BaseModel):
    """Model for creativity evaluation."""
    
    idea_id: int = Field(..., description="Evaluated idea ID")
    novelty: float = Field(..., description="How novel (0-1)")
    usefulness: float = Field(..., description="How useful (0-1)")
    surprise: float = Field(..., description="How surprising (0-1)")
    elegance: float = Field(..., description="How elegant (0-1)")
    overall_creativity: float = Field(..., description="Overall score (0-1)")
    evaluation_criteria: Dict[str, float] = Field(default_factory=dict, description="Detailed criteria scores")


class CreativeData(BaseModel):
    """Data model for creative thinking session storage."""
    
    id: Optional[int] = Field(None, description="Database ID")
    session_id: str = Field(..., description="Session this creative process belongs to")
    
    # Creative context
    challenge: str = Field(..., description="The creative challenge or problem")
    constraints: List[str] = Field(default_factory=list, description="Constraints to work within")
    goals: List[str] = Field(default_factory=list, description="Creative goals")
    
    # Creative techniques used
    techniques_used: List[str] = Field(default_factory=list, description="Techniques: brainstorming, SCAMPER, etc.")
    thinking_modes: List[str] = Field(default_factory=list, description="Modes: divergent, convergent, lateral")
    
    # Ideas generated
    ideas: List[CreativeIdea] = Field(default_factory=list, description="All ideas generated")
    inspiration_sources: List[InspirationSource] = Field(default_factory=list, description="Sources of inspiration")
    combined_ideas: List[CombinedIdea] = Field(default_factory=list, description="Ideas from combinations")
    
    # Evaluation
    creativity_scores: List[CreativityScore] = Field(default_factory=list, description="Creativity evaluations")
    selected_ideas: List[int] = Field(default_factory=list, description="IDs of selected ideas")
    
    # Process metrics
    ideation_flow_state: float = Field(0.5, description="Flow state achieved (0-1)")
    divergence_level: float = Field(0.5, description="How divergent thinking was (0-1)")
    convergence_effectiveness: float = Field(0.5, description="How well ideas converged (0-1)")
    
    # Outcomes
    breakthrough_ideas: List[int] = Field(default_factory=list, description="IDs of breakthrough ideas")
    implementation_plan: Optional[Dict[str, Any]] = Field(None, description="Plan for top ideas")
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)


class BaseCreativeStore(ABC):
    """Abstract base class for creative thinking storage operations."""
    
    @abstractmethod
    async def save_creative_session(self, creative_data: CreativeData) -> CreativeData:
        """Save a new creative thinking session."""
        pass
    
    @abstractmethod
    async def get_creative_session(self, session_id: str) -> Optional[CreativeData]:
        """Get a creative session by ID."""
        pass
    
    @abstractmethod
    async def add_idea(
        self,
        session_id: str,
        idea: CreativeIdea
    ) -> CreativeIdea:
        """Add a new idea to a session."""
        pass
    
    @abstractmethod
    async def get_session_ideas(
        self,
        session_id: str,
        min_score: Optional[float] = None
    ) -> List[CreativeIdea]:
        """Get all ideas for a session."""
        pass
    
    @abstractmethod
    async def combine_ideas(
        self,
        session_id: str,
        idea_ids: List[int],
        combination_method: str
    ) -> CombinedIdea:
        """Combine multiple ideas into a new one."""
        pass
    
    @abstractmethod
    async def evaluate_creativity(
        self,
        idea_id: int,
        evaluation: CreativityScore
    ) -> CreativityScore:
        """Evaluate creativity of an idea."""
        pass
    
    @abstractmethod
    async def add_inspiration_source(
        self,
        session_id: str,
        source: InspirationSource
    ) -> InspirationSource:
        """Add an inspiration source."""
        pass
    
    @abstractmethod
    async def get_top_ideas(
        self,
        session_id: str,
        top_n: int = 10,
        criteria: str = "overall_creativity"
    ) -> List[Tuple[CreativeIdea, CreativityScore]]:
        """Get top ideas by creativity score."""
        pass
    
    @abstractmethod
    async def search_ideas(
        self,
        keywords: Optional[str] = None,
        category: Optional[str] = None,
        min_originality: Optional[float] = None,
        tags: Optional[List[str]] = None,
        limit: int = 100
    ) -> List[CreativeIdea]:
        """Search ideas across sessions."""
        pass
    
    @abstractmethod
    async def get_creativity_patterns(
        self,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Analyze creativity patterns."""
        pass
    
    @abstractmethod
    async def find_similar_ideas(
        self,
        idea_id: int,
        threshold: float = 0.7
    ) -> List[CreativeIdea]:
        """Find ideas similar to a given one."""
        pass