# Clear Thinking FastMCP Server - Collaborative Reasoning Models

"""
Pydantic models for the Collaborative Reasoning cognitive tool.

This tool supports multi-perspective reasoning through:
- Persona-based reasoning simulation
- Stakeholder perspective analysis
- Consensus building and conflict resolution
- Role-based decision making
- Team dynamics modeling

Agent: AGENT C - Collaborative Reasoning Implementation
Status: ACTIVE - Phase 2C Parallel Expansion
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union, Literal
from enum import Enum
from datetime import datetime
import uuid

from .base import CognitiveInputBase, CognitiveOutputBase, ComplexityLevel


class PersonaType(str, Enum):
    """Types of personas for collaborative reasoning"""
    
    STAKEHOLDER = "stakeholder"
    EXPERT = "expert"
    USER = "user"
    DECISION_MAKER = "decision_maker"
    IMPLEMENTER = "implementer"
    CRITIC = "critic"
    ADVOCATE = "advocate"
    MODERATOR = "moderator"
    
    @property
    def description(self) -> str:
        """Get description of the persona type"""
        descriptions = {
            self.STAKEHOLDER: "Someone with vested interest in the outcome",
            self.EXPERT: "Domain expert with specialized knowledge",
            self.USER: "End user who will be affected by the decision",
            self.DECISION_MAKER: "Person with authority to make final decisions",
            self.IMPLEMENTER: "Person responsible for executing the solution",
            self.CRITIC: "Someone who challenges assumptions and finds flaws",
            self.ADVOCATE: "Someone who supports and promotes specific solutions",
            self.MODERATOR: "Neutral party facilitating discussion"
        }
        return descriptions.get(self, "Unknown persona type")


class ReasoningStyle(str, Enum):
    """Different reasoning styles for personas"""
    
    ANALYTICAL = "analytical"
    CREATIVE = "creative"
    PRACTICAL = "practical"
    CAUTIOUS = "cautious"
    OPTIMISTIC = "optimistic"
    PESSIMISTIC = "pessimistic"
    SYSTEMATIC = "systematic"
    INTUITIVE = "intuitive"
    CRITICAL = "critical"


class ConsensusStrategy(str, Enum):
    """Strategies for reaching consensus"""
    
    MAJORITY_VOTE = "majority_vote"
    UNANIMOUS_AGREEMENT = "unanimous_agreement"
    WEIGHTED_CONSENSUS = "weighted_consensus"
    COMPROMISE_SOLUTION = "compromise_solution"
    EXPERT_JUDGMENT = "expert_judgment"
    HIERARCHICAL_DECISION = "hierarchical_decision"


class Persona(BaseModel):
    """Individual persona with perspective and reasoning style"""
    
    name: str = Field(..., description="Name or role identifier for the persona")
    persona_type: PersonaType = Field(..., description="Type of persona")
    reasoning_style: ReasoningStyle = Field(..., description="How this persona approaches reasoning")
    background: str = Field(..., description="Background and context for this persona")
    priorities: List[str] = Field(default_factory=list, description="Key priorities and concerns")
    constraints: List[str] = Field(default_factory=list, description="Constraints or limitations")
    expertise_areas: List[str] = Field(default_factory=list, description="Areas of expertise")
    influence_weight: float = Field(default=1.0, ge=0.0, le=10.0, description="Influence weight in decisions")
    
    class Config:
        json_encoders = {
            PersonaType: lambda v: v.value,
            ReasoningStyle: lambda v: v.value
        }


class PersonaPerspective(BaseModel):
    """A persona's perspective on the problem"""
    
    persona_name: str = Field(..., description="Name of the persona providing this perspective")
    viewpoint: str = Field(..., description="This persona's view of the problem")
    concerns: List[str] = Field(default_factory=list, description="Concerns raised by this persona")
    suggestions: List[str] = Field(default_factory=list, description="Suggestions from this persona")
    supporting_arguments: List[str] = Field(default_factory=list, description="Arguments supporting their position")
    objections: List[str] = Field(default_factory=list, description="Objections to other perspectives")
    confidence_level: float = Field(default=0.5, ge=0.0, le=1.0, description="Confidence in their perspective")
    reasoning_path: List[str] = Field(default_factory=list, description="How they arrived at this perspective")
    timestamp: datetime = Field(default_factory=datetime.now, description="When this perspective was formed")


class CollaborativeDialogue(BaseModel):
    """Record of collaborative dialogue between personas"""
    
    dialogue_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique dialogue identifier")
    participants: List[str] = Field(..., description="Names of participating personas")
    topic: str = Field(..., description="Topic of discussion")
    exchanges: List[Dict[str, Any]] = Field(default_factory=list, description="Dialogue exchanges")
    consensus_points: List[str] = Field(default_factory=list, description="Points of consensus reached")
    disagreements: List[str] = Field(default_factory=list, description="Remaining disagreements")
    resolution_attempts: List[str] = Field(default_factory=list, description="Attempts to resolve conflicts")
    outcome: Optional[str] = Field(None, description="Final outcome of dialogue")
    duration_minutes: float = Field(default=0.0, ge=0.0, description="Duration of dialogue in minutes")


class ConsensusResult(BaseModel):
    """Result of consensus-building process"""
    
    strategy_used: ConsensusStrategy = Field(..., description="Strategy used to reach consensus")
    consensus_reached: bool = Field(..., description="Whether consensus was reached")
    agreement_level: float = Field(..., ge=0.0, le=1.0, description="Level of agreement (0.0-1.0)")
    agreed_solution: Optional[str] = Field(None, description="Solution agreed upon")
    dissenting_opinions: List[str] = Field(default_factory=list, description="Dissenting opinions")
    compromise_elements: List[str] = Field(default_factory=list, description="Compromise elements included")
    unresolved_issues: List[str] = Field(default_factory=list, description="Issues that remain unresolved")
    confidence_in_consensus: float = Field(default=0.5, ge=0.0, le=1.0, description="Confidence in the consensus")


class CollaborativeReasoningInput(CognitiveInputBase):
    """Input model for Collaborative Reasoning tool"""
    
    personas: List[Persona] = Field(..., min_items=2, description="Personas to simulate in the reasoning process")
    reasoning_focus: str = Field(..., description="Specific aspect to focus collaborative reasoning on")
    consensus_strategy: ConsensusStrategy = Field(default=ConsensusStrategy.WEIGHTED_CONSENSUS, description="Strategy for reaching consensus")
    max_dialogue_rounds: int = Field(default=3, ge=1, le=10, description="Maximum rounds of dialogue")
    include_devil_advocate: bool = Field(default=True, description="Include a devil's advocate perspective")
    weight_by_expertise: bool = Field(default=True, description="Weight opinions by expertise level")
    allow_persona_evolution: bool = Field(default=True, description="Allow personas to change their views")
    conflict_resolution_enabled: bool = Field(default=True, description="Enable conflict resolution mechanisms")
    dialogue_style: Literal["formal", "informal", "structured"] = Field(default="structured", description="Style of dialogue")
    time_limit_minutes: Optional[float] = Field(None, ge=1.0, le=60.0, description="Time limit for collaborative process")
    
    class Config:
        json_encoders = {
            ConsensusStrategy: lambda v: v.value
        }


class CollaborativeReasoningOutput(CognitiveOutputBase):
    """Output model for Collaborative Reasoning tool"""
    
    persona_perspectives: List[PersonaPerspective] = Field(..., description="Individual perspectives from each persona")
    dialogue_records: List[CollaborativeDialogue] = Field(default_factory=list, description="Records of collaborative dialogues")
    consensus_result: ConsensusResult = Field(..., description="Result of consensus-building process")
    key_insights: List[str] = Field(default_factory=list, description="Key insights from collaborative process")
    perspective_diversity_score: float = Field(..., ge=0.0, le=1.0, description="How diverse the perspectives were")
    collaboration_quality_score: float = Field(..., ge=0.0, le=1.0, description="Quality of collaborative process")
    unresolved_tensions: List[str] = Field(default_factory=list, description="Tensions that remain unresolved")
    recommended_next_steps: List[str] = Field(default_factory=list, description="Recommended next steps")
    stakeholder_buy_in_assessment: Dict[str, float] = Field(default_factory=dict, description="Assessment of stakeholder buy-in")
    implementation_considerations: List[str] = Field(default_factory=list, description="Considerations for implementation")
    
    # Additional fields for FastMCP Context integration
    dialogue_duration_minutes: float = Field(default=0.0, ge=0.0, description="Total duration of collaborative process")
    personas_engaged: int = Field(..., ge=0, description="Number of personas that actively engaged")
    consensus_confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence in the consensus reached")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
