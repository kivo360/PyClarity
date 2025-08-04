"""
Models for Sequential Readiness Assessment Cognitive Tool

Analyzes processes requiring progressive readiness through ordered states,
applicable to change management, skill development, system maturity, or any
domain with sequential dependencies.
"""

from typing import List, Dict, Optional, Literal, Any
from pydantic import BaseModel, Field, field_validator
from enum import Enum

from ..base import ComplexityLevel


class ReadinessLevel(str, Enum):
    """Readiness level for a state."""
    NOT_STARTED = "not_started"
    INITIATED = "initiated"
    PROGRESSING = "progressing"
    NEARLY_READY = "nearly_ready"
    READY = "ready"
    EXCEEDED = "exceeded"


class TransitionType(str, Enum):
    """Types of transitions between states."""
    SEQUENTIAL = "sequential"  # Must complete A before B
    PARALLEL = "parallel"      # Can progress simultaneously
    OPTIONAL = "optional"      # Can skip if conditions met
    CONDITIONAL = "conditional"  # Depends on external factors
    ITERATIVE = "iterative"    # May need multiple attempts


class ProgressionStrategy(str, Enum):
    """Strategies for progressing through states."""
    LINEAR = "linear"          # One state at a time
    ACCELERATED = "accelerated"  # Skip or combine states
    ITERATIVE = "iterative"    # Cycle through states
    ADAPTIVE = "adaptive"      # Adjust based on context
    PARALLEL = "parallel"      # Multiple states simultaneously


class GapSeverity(str, Enum):
    """Severity of readiness gaps."""
    MINOR = "minor"            # Small gap, easy to close
    MODERATE = "moderate"      # Medium gap, requires effort
    MAJOR = "major"           # Large gap, significant work needed
    CRITICAL = "critical"     # Blocking gap, must be resolved


class InterventionType(str, Enum):
    """Types of interventions to address gaps."""
    TRAINING = "training"              # Skills/knowledge development
    RESOURCE_ALLOCATION = "resource_allocation"  # Add resources
    PROCESS_IMPROVEMENT = "process_improvement"  # Optimize processes
    ORGANIZATIONAL_CHANGE = "organizational_change"  # Structural changes
    TECHNOLOGY_UPGRADE = "technology_upgrade"    # Tech improvements
    STAKEHOLDER_ENGAGEMENT = "stakeholder_engagement"  # Buy-in activities


class State(BaseModel):
    """Represents a single state in the sequence."""
    
    name: str = Field(
        description="Name of the state (e.g., 'Awareness', 'Understanding', 'Commitment')"
    )
    
    description: str = Field(
        description="What this state represents"
    )
    
    indicators: List[str] = Field(
        description="Observable indicators that show this state is achieved",
        min_length=1
    )
    
    prerequisites: List[str] = Field(
        default_factory=list,
        description="What must be in place before this state"
    )
    
    blockers: List[str] = Field(
        default_factory=list,
        description="Common obstacles preventing this state"
    )
    
    enablers: List[str] = Field(
        default_factory=list,
        description="Factors that facilitate reaching this state"
    )
    
    typical_duration: Optional[str] = Field(
        None,
        description="Typical time to achieve this state"
    )
    
    readiness_level: ReadinessLevel = Field(
        default=ReadinessLevel.NOT_STARTED,
        description="Current readiness level for this state"
    )


class StateTransition(BaseModel):
    """Represents a transition between states."""
    
    from_state: str = Field(
        description="Starting state name"
    )
    
    to_state: str = Field(
        description="Target state name"
    )
    
    transition_type: TransitionType = Field(
        description="Type of transition"
    )
    
    requirements: List[str] = Field(
        description="Requirements for successful transition",
        min_length=1
    )
    
    risks: List[str] = Field(
        default_factory=list,
        description="Risks during transition"
    )
    
    strategies: List[str] = Field(
        description="Strategies to facilitate transition",
        min_length=1
    )
    
    success_rate: Optional[float] = Field(
        None,
        description="Historical success rate for this transition (0.0-1.0)",
        ge=0.0,
        le=1.0
    )


class GapAnalysis(BaseModel):
    """Analysis of gaps between current and target states."""
    
    state_name: str = Field(
        description="Name of the state being analyzed"
    )
    
    current_readiness: ReadinessLevel = Field(
        description="Current readiness level"
    )
    
    target_readiness: ReadinessLevel = Field(
        description="Target readiness level"
    )
    
    gap_size: str = Field(
        description="Size of the gap (small, medium, large)"
    )
    
    missing_elements: List[str] = Field(
        description="What's missing to reach target readiness"
    )
    
    recommended_actions: List[str] = Field(
        description="Actions to close the gap"
    )
    
    estimated_effort: str = Field(
        description="Estimated effort to close gap"
    )
    
    priority: str = Field(
        description="Priority for addressing this gap (high, medium, low)"
    )


class ProgressionPlan(BaseModel):
    """Plan for progressing through sequential states."""
    
    strategy: ProgressionStrategy = Field(
        description="Overall progression strategy"
    )
    
    rationale: str = Field(
        description="Why this strategy is recommended"
    )
    
    phases: List[Dict[str, Any]] = Field(
        description="Phases of the progression plan"
    )
    
    milestones: List[str] = Field(
        description="Key milestones to track progress"
    )
    
    timeline: Optional[str] = Field(
        None,
        description="Overall timeline estimate"
    )
    
    success_criteria: List[str] = Field(
        description="How to measure successful progression"
    )
    
    risk_mitigation: List[str] = Field(
        default_factory=list,
        description="Strategies to mitigate progression risks"
    )
    
    confidence_level: float = Field(
        description="Confidence in plan success (0.0-1.0)",
        ge=0.0,
        le=1.0
    )


class ReadinessState(BaseModel):
    """Represents a single readiness state."""
    state_id: str = Field(description="Unique identifier for the state")
    name: str = Field(description="Name of the state")
    description: str = Field(description="Description of what this state represents")
    readiness_level: ReadinessLevel = Field(description="Current readiness level")
    criteria: List[str] = Field(description="Criteria to achieve this state")
    achieved: bool = Field(default=False, description="Whether the state has been achieved")
    dependencies: List[str] = Field(default_factory=list, description="Other states this depends on")


class Dependency(BaseModel):
    """Represents a dependency between states."""
    from_state: str = Field(description="State that has the dependency")
    to_state: str = Field(description="State that is depended upon")
    dependency_type: str = Field(description="Type of dependency (prerequisite, co-requisite, etc.)")
    is_satisfied: bool = Field(default=False, description="Whether the dependency is satisfied")


class ReadinessGap(BaseModel):
    """Represents a gap in readiness."""
    gap_id: str = Field(description="Unique identifier for the gap")
    state_id: str = Field(description="State with the gap")
    description: str = Field(description="Description of the gap")
    severity: GapSeverity = Field(description="Severity of the gap")
    impact: str = Field(description="Impact if gap is not addressed")
    remediation_options: List[str] = Field(description="Options to close the gap")


class Intervention(BaseModel):
    """Represents an intervention to address gaps."""
    intervention_id: str = Field(description="Unique identifier for the intervention")
    name: str = Field(description="Name of the intervention")
    description: str = Field(description="Description of the intervention")
    intervention_type: InterventionType = Field(description="Type of intervention")
    target_gaps: List[str] = Field(description="Gap IDs this intervention addresses")
    estimated_effort: str = Field(description="Estimated effort required")
    expected_impact: str = Field(description="Expected impact of the intervention")
    priority: int = Field(description="Priority of the intervention (1-10)", ge=1, le=10)


class SequentialReadinessContext(BaseModel):
    """Input for Sequential Readiness Framework analysis."""
    
    scenario: str = Field(
        description="The process or change requiring sequential readiness analysis"
    )
    
    domain_context: Optional[str] = Field(
        None,
        description="Domain context (e.g., 'change_management', 'skill_development', 'system_implementation')"
    )
    
    predefined_states: Optional[List[State]] = Field(
        None,
        description="Pre-defined states if known"
    )
    
    current_status: Optional[Dict[str, ReadinessLevel]] = Field(
        None,
        description="Current readiness levels for each state"
    )
    
    target_outcome: Optional[str] = Field(
        None,
        description="Desired end state or outcome"
    )
    
    constraints: Optional[Dict[str, str]] = Field(
        None,
        description="Constraints affecting progression (time, resources, dependencies)"
    )
    
    stakeholders: Optional[List[str]] = Field(
        default_factory=list,
        description="Key stakeholders involved in the process"
    )
    
    success_factors: Optional[List[str]] = Field(
        default_factory=list,
        description="Critical success factors for progression"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "scenario": "Implementing new AI-powered customer service system",
                "domain_context": "technology_adoption",
                "target_outcome": "Full adoption with 90% user satisfaction",
                "constraints": {
                    "timeline": "6 months",
                    "budget": "Limited training budget",
                    "change_resistance": "High due to job security concerns"
                },
                "stakeholders": [
                    "Customer service agents",
                    "IT department",
                    "Management",
                    "Customers"
                ],
                "success_factors": [
                    "Strong leadership support",
                    "Comprehensive training program",
                    "Clear communication of benefits"
                ]
            }
        }


class SequentialReadinessResult(BaseModel):
    """Complete Sequential Readiness Framework analysis output."""
    
    input_scenario: str = Field(
        description="The analyzed scenario"
    )
    
    identified_states: List[State] = Field(
        description="Sequential states identified for the process"
    )
    
    state_transitions: List[StateTransition] = Field(
        description="Transitions between states"
    )
    
    current_state_assessment: str = Field(
        description="Assessment of current position in the sequence"
    )
    
    gap_analyses: List[GapAnalysis] = Field(
        description="Gap analysis for each state"
    )
    
    progression_plan: ProgressionPlan = Field(
        description="Recommended plan for progression"
    )
    
    critical_path: List[str] = Field(
        description="The critical path through states"
    )
    
    dependency_map: Dict[str, List[str]] = Field(
        description="Dependencies between states"
    )
    
    risk_assessment: str = Field(
        description="Overall risk assessment for the progression"
    )
    
    domain_specific_insights: List[str] = Field(
        description="Insights specific to the domain"
    )
    
    visual_representation: Optional[Dict[str, Any]] = Field(
        None,
        description="Data for visualizing the sequential progression"
    )
    
    key_decisions: List[str] = Field(
        description="Key decisions needed for progression"
    )
    
    monitoring_plan: List[str] = Field(
        description="How to monitor progression through states"
    )
    
    overall_recommendation: str = Field(
        description="Overall recommendation for managing the sequential process"
    )
    
    confidence_score: float = Field(
        description="Overall confidence in the analysis (0.0-1.0)",
        ge=0.0,
        le=1.0
    )
    processing_time_ms: Optional[float] = Field(
        None,
        description="Processing time in milliseconds"
    )