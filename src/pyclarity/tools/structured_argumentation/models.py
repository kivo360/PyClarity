"""
Structured Argumentation Models

Data structures for logic chain construction, argument validity assessment,
evidence evaluation frameworks, and reasoning quality validation.
"""

import uuid
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

from pydantic import BaseModel, Field, field_validator


class ArgumentType(str, Enum):
    """Types of arguments"""
    DEDUCTIVE = "deductive"
    INDUCTIVE = "inductive"
    ABDUCTIVE = "abductive"
    ANALOGICAL = "analogical"
    CAUSAL = "causal"
    STATISTICAL = "statistical"
    AUTHORITATIVE = "authoritative"
    MORAL = "moral"
    PRAGMATIC = "pragmatic"


class LogicalFallacy(str, Enum):
    """Common logical fallacies"""
    AD_HOMINEM = "ad_hominem"
    STRAW_MAN = "straw_man"
    FALSE_DICHOTOMY = "false_dichotomy"
    SLIPPERY_SLOPE = "slippery_slope"
    CIRCULAR_REASONING = "circular_reasoning"
    APPEAL_TO_AUTHORITY = "appeal_to_authority"
    APPEAL_TO_EMOTION = "appeal_to_emotion"
    HASTY_GENERALIZATION = "hasty_generalization"
    FALSE_CAUSE = "false_cause"
    BANDWAGON = "bandwagon"
    RED_HERRING = "red_herring"
    BEGGING_THE_QUESTION = "begging_the_question"


class EvidenceType(str, Enum):
    """Types of evidence"""
    EMPIRICAL = "empirical"
    STATISTICAL = "statistical"
    ANECDOTAL = "anecdotal"
    EXPERT_TESTIMONY = "expert_testimony"
    DOCUMENTARY = "documentary"
    EXPERIMENTAL = "experimental"
    OBSERVATIONAL = "observational"
    THEORETICAL = "theoretical"
    HISTORICAL = "historical"
    COMPARATIVE = "comparative"


class StrengthLevel(str, Enum):
    """Strength levels for arguments and evidence"""
    VERY_STRONG = "very_strong"
    STRONG = "strong"
    MODERATE = "moderate"
    WEAK = "weak"
    VERY_WEAK = "very_weak"


class Premise(BaseModel):
    """A premise in an argument"""

    premise_id: str = Field(
        default_factory=lambda: f"premise_{str(uuid.uuid4())[:8]}",
        description="Unique premise identifier"
    )

    statement: str = Field(
        ...,
        description="The premise statement",
        min_length=5,
        max_length=1000
    )

    premise_type: str = Field(
        ...,
        description="Type of premise (major, minor, supporting, assumption)",
        pattern="^(major|minor|supporting|assumption)$"
    )

    truth_value: bool | None = Field(
        None,
        description="Truth value of the premise if known"
    )

    certainty_level: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Certainty level of the premise (0.0 to 1.0)"
    )

    supporting_evidence: list[str] = Field(
        default_factory=list,
        description="Evidence supporting this premise",
        max_items=10
    )

    source: str | None = Field(
        None,
        description="Source of the premise",
        max_length=500
    )

    is_implicit: bool = Field(
        False,
        description="Whether this premise is implicit/unstated"
    )


class Evidence(BaseModel):
    """Evidence supporting a premise or conclusion"""

    evidence_id: str = Field(
        default_factory=lambda: f"evidence_{str(uuid.uuid4())[:8]}",
        description="Unique evidence identifier"
    )

    description: str = Field(
        ...,
        description="Description of the evidence",
        min_length=10,
        max_length=2000
    )

    evidence_type: EvidenceType = Field(
        ...,
        description="Type of evidence"
    )

    source: str = Field(
        ...,
        description="Source of the evidence",
        min_length=5,
        max_length=500
    )

    quality_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Quality score of the evidence (0.0 to 1.0)"
    )

    relevance_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Relevance score to the argument (0.0 to 1.0)"
    )

    reliability_assessment: str = Field(
        ...,
        description="Assessment of evidence reliability",
        pattern="^(high|moderate|low|unknown)$"
    )

    supporting_premises: list[str] = Field(
        default_factory=list,
        description="Premises this evidence supports",
        max_items=20
    )

    contradicting_evidence: list[str] = Field(
        default_factory=list,
        description="Evidence that contradicts this evidence",
        max_items=10
    )

    context: str = Field(
        default_factory=str,
        description="Context in which evidence was obtained",
        max_length=1000
    )

    limitations: list[str] = Field(
        default_factory=list,
        description="Limitations of this evidence",
        max_items=8
    )


class LogicChain(BaseModel):
    """A chain of logical reasoning"""

    chain_id: str = Field(
        default_factory=lambda: f"chain_{str(uuid.uuid4())[:8]}",
        description="Unique logic chain identifier"
    )

    premises: list[Premise] = Field(
        ...,
        description="Premises in the logic chain",
        min_items=1,
        max_items=20
    )

    inference_rules: list[str] = Field(
        default_factory=list,
        description="Inference rules applied",
        max_items=10
    )

    intermediate_conclusions: list[str] = Field(
        default_factory=list,
        description="Intermediate conclusions in the chain",
        max_items=15
    )

    final_conclusion: str = Field(
        ...,
        description="Final conclusion of the logic chain",
        min_length=10,
        max_length=1000
    )

    argument_type: ArgumentType = Field(
        ...,
        description="Type of argument used"
    )

    validity_assessment: str = Field(
        ...,
        description="Assessment of logical validity",
        pattern="^(valid|invalid|strong|weak|plausible|insufficient_premises)$"
    )

    soundness_assessment: str = Field(
        ...,
        description="Assessment of argument soundness",
        pattern="^(sound|unsound|partially_sound)$"
    )

    logical_gaps: list[str] = Field(
        default_factory=list,
        description="Identified gaps in logical reasoning",
        max_items=10
    )

    strength_rating: StrengthLevel = Field(
        ...,
        description="Overall strength rating of the logic chain"
    )


class ArgumentStructure(BaseModel):
    """Complete structure of an argument"""

    argument_id: str = Field(
        default_factory=lambda: f"argument_{str(uuid.uuid4())[:8]}",
        description="Unique argument identifier"
    )

    claim: str = Field(
        ...,
        description="Main claim or thesis of the argument",
        min_length=10,
        max_length=1000
    )

    logic_chains: list[LogicChain] = Field(
        ...,
        description="Logic chains supporting the claim",
        min_items=1,
        max_items=10
    )

    supporting_evidence: list[Evidence] = Field(
        default_factory=list,
        description="Evidence supporting the argument",
        max_items=20
    )

    counterarguments: list[str] = Field(
        default_factory=list,
        description="Known counterarguments",
        max_items=15
    )

    rebuttals: list[str] = Field(
        default_factory=list,
        description="Rebuttals to counterarguments",
        max_items=15
    )

    assumptions: list[str] = Field(
        default_factory=list,
        description="Underlying assumptions",
        max_items=10
    )

    context: str = Field(
        default_factory=str,
        description="Context in which argument is made",
        max_length=1000
    )

    argument_strength: StrengthLevel = Field(
        ...,
        description="Overall strength of the argument"
    )

    confidence_level: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence in the argument (0.0 to 1.0)"
    )


class FallacyDetection(BaseModel):
    """Detection of logical fallacies"""

    detection_id: str = Field(
        default_factory=lambda: f"fallacy_{str(uuid.uuid4())[:8]}",
        description="Unique detection identifier"
    )

    fallacy_type: LogicalFallacy = Field(
        ...,
        description="Type of fallacy detected"
    )

    location: str = Field(
        ...,
        description="Location of fallacy in the argument",
        min_length=5,
        max_length=200
    )

    description: str = Field(
        ...,
        description="Description of the fallacy",
        min_length=10,
        max_length=500
    )

    severity: StrengthLevel = Field(
        ...,
        description="Severity of the fallacy"
    )

    correction_suggestion: str = Field(
        ...,
        description="Suggestion for correcting the fallacy",
        min_length=10,
        max_length=500
    )

    impact_on_argument: str = Field(
        ...,
        description="Impact of fallacy on argument strength",
        min_length=10,
        max_length=300
    )

    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence in fallacy detection (0.0 to 1.0)"
    )


class ArgumentAnalysis(BaseModel):
    """Analysis of argument quality and structure"""

    analysis_id: str = Field(
        default_factory=lambda: f"analysis_{str(uuid.uuid4())[:8]}",
        description="Unique analysis identifier"
    )

    argument: ArgumentStructure = Field(
        ...,
        description="Argument being analyzed"
    )

    validity_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Logical validity score (0.0 to 1.0)"
    )

    soundness_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Argument soundness score (0.0 to 1.0)"
    )

    persuasiveness_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Persuasiveness score (0.0 to 1.0)"
    )

    logical_consistency: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Logical consistency score (0.0 to 1.0)"
    )

    evidence_quality: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Quality of supporting evidence (0.0 to 1.0)"
    )

    detected_fallacies: list[FallacyDetection] = Field(
        default_factory=list,
        description="Logical fallacies detected",
        max_items=20
    )

    strengths: list[str] = Field(
        default_factory=list,
        description="Argument strengths identified",
        max_items=15
    )

    weaknesses: list[str] = Field(
        default_factory=list,
        description="Argument weaknesses identified",
        max_items=15
    )

    improvement_suggestions: list[str] = Field(
        default_factory=list,
        description="Suggestions for improving the argument",
        max_items=20
    )

    overall_quality: StrengthLevel = Field(
        ...,
        description="Overall quality assessment"
    )


class CounterargumentAnalysis(BaseModel):
    """Analysis of counterarguments and responses"""

    analysis_id: str = Field(
        default_factory=lambda: f"counter_{str(uuid.uuid4())[:8]}",
        description="Unique counterargument analysis identifier"
    )

    original_argument: str = Field(
        ...,
        description="Original argument being countered",
        min_length=10,
        max_length=1000
    )

    counterarguments: list[str] = Field(
        default_factory=list,
        description="Generated counterarguments",
        max_items=20
    )

    counterargument_strength: dict[str, str] = Field(
        default_factory=dict,
        description="Strength assessment of each counterargument"
    )

    potential_rebuttals: dict[str, list[str]] = Field(
        default_factory=dict,
        description="Potential rebuttals for each counterargument"
    )

    argument_vulnerability: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Overall vulnerability of the argument (0.0 to 1.0)"
    )

    defensive_strategies: list[str] = Field(
        default_factory=list,
        description="Strategies to defend against counterarguments",
        max_items=15
    )

    strengthening_recommendations: list[str] = Field(
        default_factory=list,
        description="Recommendations to strengthen the argument",
        max_items=15
    )


class DebateStructure(BaseModel):
    """Structure for analyzing debates and discussions"""

    debate_id: str = Field(
        default_factory=lambda: f"debate_{str(uuid.uuid4())[:8]}",
        description="Unique debate identifier"
    )

    topic: str = Field(
        ...,
        description="Topic of the debate",
        min_length=5,
        max_length=500
    )

    positions: list[str] = Field(
        ...,
        description="Different positions in the debate",
        min_items=2,
        max_items=10
    )

    arguments_by_position: dict[str, list[str]] = Field(
        default_factory=dict,
        description="Arguments organized by position"
    )

    cross_references: dict[str, list[str]] = Field(
        default_factory=dict,
        description="Cross-references between related arguments"
    )

    consensus_points: list[str] = Field(
        default_factory=list,
        description="Points of agreement across positions",
        max_items=20
    )

    contentious_points: list[str] = Field(
        default_factory=list,
        description="Highly disputed points",
        max_items=20
    )

    resolution_pathways: list[str] = Field(
        default_factory=list,
        description="Potential paths to resolution",
        max_items=15
    )

    quality_assessment: dict[str, float] = Field(
        default_factory=dict,
        description="Quality assessment of each position's arguments"
    )


class StructuredArgumentationContext(BaseModel):
    """Context for structured argumentation analysis"""

    argument_text: str = Field(
        ...,
        description="Text of the argument to analyze",
        min_length=20,
        max_length=10000
    )

    analysis_type: str = Field(
        "comprehensive",
        description="Type of analysis to perform",
        pattern="^(basic|comprehensive|fallacy_only|structure_only|counterargument)$"
    )

    argument_type: ArgumentType = Field(
        ArgumentType.DEDUCTIVE,
        description="Expected type of argument"
    )

    include_fallacy_detection: bool = Field(
        True,
        description="Whether to include fallacy detection"
    )

    include_counterargument_analysis: bool = Field(
        True,
        description="Whether to include counterargument analysis"
    )

    include_evidence_evaluation: bool = Field(
        True,
        description="Whether to evaluate evidence quality"
    )

    domain_context: str | None = Field(
        None,
        description="Domain context for the argument (e.g., legal, scientific)",
        max_length=200
    )

    target_audience: str | None = Field(
        None,
        description="Target audience for the argument",
        max_length=200
    )

    confidence_threshold: float = Field(
        0.5,
        ge=0.0,
        le=1.0,
        description="Minimum confidence threshold for analysis results"
    )

    max_counterarguments: int = Field(
        10,
        ge=1,
        le=20,
        description="Maximum number of counterarguments to generate"
    )

    @field_validator('argument_text')
    @classmethod
    def validate_argument_text(cls, v):
        """Validate argument text"""
        v = v.strip()
        if len(v) < 20:
            raise ValueError("Argument text must be at least 20 characters")
        return v


class StructuredArgumentationResult(BaseModel):
    """Result of structured argumentation analysis"""

    argument_structure: ArgumentStructure = Field(
        ...,
        description="Analyzed argument structure"
    )

    argument_analysis: ArgumentAnalysis = Field(
        ...,
        description="Comprehensive argument analysis"
    )

    counterargument_analysis: CounterargumentAnalysis | None = Field(
        None,
        description="Counterargument analysis if requested"
    )

    debate_structure: DebateStructure | None = Field(
        None,
        description="Debate structure if multiple positions identified"
    )

    logic_quality_scores: dict[str, float] = Field(
        default_factory=dict,
        description="Quality scores for different aspects of logic"
    )

    improvement_roadmap: list[str] = Field(
        default_factory=list,
        description="Step-by-step improvement roadmap",
        max_items=20
    )

    logical_consistency_report: list[str] = Field(
        default_factory=list,
        description="Report on logical consistency issues",
        max_items=15
    )

    evidence_assessment: list[str] = Field(
        default_factory=list,
        description="Assessment of evidence quality and relevance",
        max_items=15
    )

    recommended_strengthening: list[str] = Field(
        default_factory=list,
        description="Recommendations for strengthening the argument",
        max_items=15
    )

    fallacy_summary: dict[str, int] = Field(
        default_factory=dict,
        description="Summary of fallacies detected by type"
    )

    processing_metrics: dict[str, Any] = Field(
        default_factory=dict,
        description="Processing metrics and statistics"
    )

    processing_time_ms: int = Field(
        0,
        description="Time taken to process in milliseconds"
    )

    def get_summary(self) -> dict[str, Any]:
        """Get concise summary of argumentation analysis"""
        return {
            'overall_quality': self.argument_analysis.overall_quality.value,
            'validity_score': self.argument_analysis.validity_score,
            'soundness_score': self.argument_analysis.soundness_score,
            'fallacies_detected': len(self.argument_analysis.detected_fallacies),
            'has_counterargument_analysis': self.counterargument_analysis is not None,
            'logic_chains_count': len(self.argument_structure.logic_chains),
            'evidence_pieces': len(self.argument_structure.supporting_evidence),
            'improvement_suggestions': len(self.improvement_roadmap)
        }
