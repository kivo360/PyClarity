"""
Collaborative Reasoning Models

Data structures for multi-perspective reasoning through persona simulation,
stakeholder perspective analysis, consensus building, conflict resolution,
role-based decision making, and team dynamics modeling.
"""

import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


class ComplexityLevel(str, Enum):
    """Problem complexity levels"""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    VERY_COMPLEX = "very_complex"


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


class DialogueStyle(str, Enum):
    """Style of dialogue between personas"""
    FORMAL = "formal"
    INFORMAL = "informal"
    STRUCTURED = "structured"


class Persona(BaseModel):
    """Individual persona with perspective and reasoning style"""

    name: str = Field(
        ...,
        description="Name or role identifier for the persona",
        min_length=1,
        max_length=100
    )

    persona_type: PersonaType = Field(
        ...,
        description="Type of persona"
    )

    reasoning_style: ReasoningStyle = Field(
        ...,
        description="How this persona approaches reasoning"
    )

    background: str = Field(
        ...,
        description="Background and context for this persona",
        min_length=10,
        max_length=500
    )

    priorities: list[str] = Field(
        default_factory=list,
        description="Key priorities and concerns",
        max_items=10
    )

    constraints: list[str] = Field(
        default_factory=list,
        description="Constraints or limitations",
        max_items=10
    )

    expertise_areas: list[str] = Field(
        default_factory=list,
        description="Areas of expertise",
        max_items=10
    )

    influence_weight: float = Field(
        default=1.0,
        ge=0.0,
        le=10.0,
        description="Influence weight in decisions"
    )

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        """Validate persona name"""
        if not v or v.strip() == "":
            raise ValueError("Persona name cannot be empty")
        return v.strip()

    @field_validator('priorities', 'constraints', 'expertise_areas')
    @classmethod
    def validate_string_lists(cls, v):
        """Validate string lists are non-empty when provided"""
        if v is not None:
            cleaned = [item.strip() for item in v if item.strip()]
            return cleaned if cleaned else []
        return v


class PersonaPerspective(BaseModel):
    """A persona's perspective on the problem"""

    persona_name: str = Field(
        ...,
        description="Name of the persona providing this perspective",
        min_length=1,
        max_length=100
    )

    viewpoint: str = Field(
        ...,
        description="This persona's view of the problem",
        min_length=10,
        max_length=1000
    )

    concerns: list[str] = Field(
        default_factory=list,
        description="Concerns raised by this persona",
        max_items=10
    )

    suggestions: list[str] = Field(
        default_factory=list,
        description="Suggestions from this persona",
        max_items=10
    )

    supporting_arguments: list[str] = Field(
        default_factory=list,
        description="Arguments supporting their position",
        max_items=10
    )

    objections: list[str] = Field(
        default_factory=list,
        description="Objections to other perspectives",
        max_items=10
    )

    confidence_level: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Confidence in their perspective"
    )

    reasoning_path: list[str] = Field(
        default_factory=list,
        description="How they arrived at this perspective",
        max_items=10
    )

    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="When this perspective was formed"
    )


class CollaborativeDialogue(BaseModel):
    """Record of collaborative dialogue between personas"""

    dialogue_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique dialogue identifier"
    )

    participants: list[str] = Field(
        ...,
        description="Names of participating personas",
        min_items=2,
        max_items=20
    )

    topic: str = Field(
        ...,
        description="Topic of discussion",
        min_length=5,
        max_length=200
    )

    exchanges: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Dialogue exchanges",
        max_items=50
    )

    consensus_points: list[str] = Field(
        default_factory=list,
        description="Points of consensus reached",
        max_items=20
    )

    disagreements: list[str] = Field(
        default_factory=list,
        description="Remaining disagreements",
        max_items=20
    )

    resolution_attempts: list[str] = Field(
        default_factory=list,
        description="Attempts to resolve conflicts",
        max_items=10
    )

    outcome: str | None = Field(
        None,
        description="Final outcome of dialogue",
        max_length=500
    )

    duration_minutes: float = Field(
        default=0.0,
        ge=0.0,
        description="Duration of dialogue in minutes"
    )


class ConsensusResult(BaseModel):
    """Result of consensus-building process"""

    strategy_used: ConsensusStrategy = Field(
        ...,
        description="Strategy used to reach consensus"
    )

    consensus_reached: bool = Field(
        ...,
        description="Whether consensus was reached"
    )

    agreement_level: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Level of agreement (0.0-1.0)"
    )

    agreed_solution: str | None = Field(
        None,
        description="Solution agreed upon",
        max_length=1000
    )

    dissenting_opinions: list[str] = Field(
        default_factory=list,
        description="Dissenting opinions",
        max_items=10
    )

    compromise_elements: list[str] = Field(
        default_factory=list,
        description="Compromise elements included",
        max_items=10
    )

    unresolved_issues: list[str] = Field(
        default_factory=list,
        description="Issues that remain unresolved",
        max_items=10
    )

    confidence_in_consensus: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Confidence in the consensus"
    )


class CollaborativeReasoningContext(BaseModel):
    """Context for collaborative reasoning analysis"""

    problem: str = Field(
        ...,
        description="The problem or question to analyze",
        min_length=20,
        max_length=2000
    )

    personas: list[Persona] = Field(
        ...,
        min_items=2,
        max_items=10,
        description="Personas to simulate in the reasoning process"
    )

    reasoning_focus: str = Field(
        ...,
        description="Specific aspect to focus collaborative reasoning on",
        min_length=5,
        max_length=200
    )

    consensus_strategy: ConsensusStrategy = Field(
        default=ConsensusStrategy.WEIGHTED_CONSENSUS,
        description="Strategy for reaching consensus"
    )

    complexity_level: ComplexityLevel = Field(
        ComplexityLevel.MODERATE,
        description="Complexity level of the problem"
    )

    max_dialogue_rounds: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Maximum rounds of dialogue"
    )

    include_devil_advocate: bool = Field(
        default=True,
        description="Include a devil's advocate perspective"
    )

    weight_by_expertise: bool = Field(
        default=True,
        description="Weight opinions by expertise level"
    )

    allow_persona_evolution: bool = Field(
        default=True,
        description="Allow personas to change their views"
    )

    conflict_resolution_enabled: bool = Field(
        default=True,
        description="Enable conflict resolution mechanisms"
    )

    dialogue_style: DialogueStyle = Field(
        default=DialogueStyle.STRUCTURED,
        description="Style of dialogue"
    )

    time_limit_minutes: float | None = Field(
        None,
        ge=1.0,
        le=60.0,
        description="Time limit for collaborative process"
    )

    @field_validator('problem')
    @classmethod
    def validate_problem(cls, v):
        """Validate problem description"""
        v = v.strip()
        if len(v) < 20:
            raise ValueError("Problem description must be at least 20 characters")
        return v

    @model_validator(mode='after')
    def validate_personas_diversity(self):
        """Ensure personas have diverse types"""
        if len(self.personas) >= 3:
            persona_types = [p.persona_type for p in self.personas]
            unique_types = set(persona_types)
            if len(unique_types) < 2:
                raise ValueError("Multiple personas should have diverse types")
        return self


class CollaborativeReasoningResult(BaseModel):
    """Result of collaborative reasoning analysis"""

    persona_perspectives: list[PersonaPerspective] = Field(
        ...,
        description="Individual perspectives from each persona",
        min_items=2
    )

    dialogue_records: list[CollaborativeDialogue] = Field(
        default_factory=list,
        description="Records of collaborative dialogues",
        max_items=10
    )

    consensus_result: ConsensusResult = Field(
        ...,
        description="Result of consensus-building process"
    )

    key_insights: list[str] = Field(
        default_factory=list,
        description="Key insights from collaborative process",
        max_items=10
    )

    perspective_diversity_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="How diverse the perspectives were"
    )

    collaboration_quality_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Quality of collaborative process"
    )

    unresolved_tensions: list[str] = Field(
        default_factory=list,
        description="Tensions that remain unresolved",
        max_items=10
    )

    recommended_next_steps: list[str] = Field(
        default_factory=list,
        description="Recommended next steps",
        max_items=10
    )

    stakeholder_buy_in_assessment: dict[str, float] = Field(
        default_factory=dict,
        description="Assessment of stakeholder buy-in"
    )

    implementation_considerations: list[str] = Field(
        default_factory=list,
        description="Considerations for implementation",
        max_items=10
    )

    dialogue_duration_minutes: float = Field(
        default=0.0,
        ge=0.0,
        description="Total duration of collaborative process"
    )

    personas_engaged: int = Field(
        ...,
        ge=0,
        description="Number of personas that actively engaged"
    )

    consensus_confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence in the consensus reached"
    )

    processing_time_ms: int = Field(
        0,
        description="Time taken to process in milliseconds"
    )

    def get_summary(self) -> str:
        """Get a summary of the collaborative reasoning results"""
        return (
            f"Collaborative reasoning with {self.personas_engaged} personas "
            f"achieved {self.consensus_result.agreement_level:.1%} consensus. "
            f"Diversity score: {self.perspective_diversity_score:.2f}, "
            f"Quality score: {self.collaboration_quality_score:.2f}"
        )

    def get_top_insights(self, n: int = 3) -> list[str]:
        """Get top N insights from the collaborative process"""
        return self.key_insights[:n]
