# Clear Thinking FastMCP Server - Impact Propagation Mapping Models

"""
Pydantic models for Impact Propagation Mapping cognitive tool.

This model enables systematic analysis of how changes ripple through
interconnected systems, revealing cascading effects, feedback loops,
and unintended consequences across various domains.
"""

from typing import List, Dict, Optional, Literal, Any
from pydantic import BaseModel, Field, field_validator, ConfigDict
from enum import Enum

from .base import CognitiveInputBase, CognitiveOutputBase, ComplexityLevel


class ImpactType(str, Enum):
    """Types of impacts in the system."""
    DIRECT = "direct"              # Immediate, first-order effect
    INDIRECT = "indirect"          # Second-order effect
    CASCADE = "cascade"            # Multi-level propagation
    FEEDBACK = "feedback"          # Circular/reinforcing effect
    EMERGENT = "emergent"          # Unexpected system behavior
    SYSTEMIC = "systemic"          # System-wide effect


class PropagationSpeed(str, Enum):
    """Speed of impact propagation."""
    IMMEDIATE = "immediate"        # Instant effect
    RAPID = "rapid"               # Hours to days
    MODERATE = "moderate"         # Days to weeks
    SLOW = "slow"                 # Weeks to months
    GRADUAL = "gradual"           # Months to years


class EffectMagnitude(str, Enum):
    """Magnitude of the effect."""
    NEGLIGIBLE = "negligible"
    MINOR = "minor"
    MODERATE = "moderate"
    SIGNIFICANT = "significant"
    MAJOR = "major"
    CRITICAL = "critical"


class FeedbackType(str, Enum):
    """Types of feedback loops."""
    POSITIVE = "positive"          # Reinforcing/amplifying
    NEGATIVE = "negative"          # Balancing/dampening
    OSCILLATING = "oscillating"    # Alternating effects
    COMPLEX = "complex"            # Mixed feedback patterns


class Node(BaseModel):
    """Represents a node in the impact propagation network."""
    model_config = ConfigDict(use_enum_values=True)
    
    id: str = Field(
        description="Unique identifier for the node"
    )
    
    name: str = Field(
        description="Name of the system element"
    )
    
    category: str = Field(
        description="Category of the node (e.g., 'technical', 'human', 'process')"
    )
    
    initial_state: Optional[str] = Field(
        None,
        description="Initial state before impact"
    )
    
    sensitivity: float = Field(
        default=0.5,
        description="Sensitivity to changes (0.0-1.0)",
        ge=0.0,
        le=1.0
    )
    
    resilience: float = Field(
        default=0.5,
        description="Resilience to disruption (0.0-1.0)",
        ge=0.0,
        le=1.0
    )
    
    influence_radius: int = Field(
        default=1,
        description="How many degrees of separation this node can influence",
        ge=1
    )


class Edge(BaseModel):
    """Represents a connection between nodes."""
    model_config = ConfigDict(use_enum_values=True)
    
    source_id: str = Field(
        description="Source node ID"
    )
    
    target_id: str = Field(
        description="Target node ID"
    )
    
    relationship_type: str = Field(
        description="Type of relationship (e.g., 'depends_on', 'influences', 'triggers')"
    )
    
    strength: float = Field(
        default=0.5,
        description="Strength of connection (0.0-1.0)",
        ge=0.0,
        le=1.0
    )
    
    propagation_speed: PropagationSpeed = Field(
        description="Speed of effect propagation"
    )
    
    bidirectional: bool = Field(
        default=False,
        description="Whether effects flow both ways"
    )


class ImpactEvent(BaseModel):
    """Represents an impact on a node."""
    model_config = ConfigDict(use_enum_values=True)
    
    node_id: str = Field(
        description="ID of impacted node"
    )
    
    impact_type: ImpactType = Field(
        description="Type of impact"
    )
    
    description: str = Field(
        description="Description of the impact"
    )
    
    magnitude: EffectMagnitude = Field(
        description="Magnitude of the impact"
    )
    
    probability: float = Field(
        default=1.0,
        description="Probability of occurrence (0.0-1.0)",
        ge=0.0,
        le=1.0
    )
    
    time_delay: Optional[str] = Field(
        None,
        description="Time delay before impact manifests"
    )


class PropagationPath(BaseModel):
    """Represents a path of impact propagation."""
    model_config = ConfigDict(use_enum_values=True)
    
    path_nodes: List[str] = Field(
        description="Ordered list of node IDs in the path",
        min_length=2
    )
    
    total_impact: EffectMagnitude = Field(
        description="Cumulative impact along the path"
    )
    
    propagation_time: str = Field(
        description="Total time for impact to propagate"
    )
    
    attenuation_factor: float = Field(
        description="How much impact diminishes along path (0.0-1.0)",
        ge=0.0,
        le=1.0
    )
    
    critical_points: List[str] = Field(
        default_factory=list,
        description="Node IDs that are critical in this path"
    )


class FeedbackLoop(BaseModel):
    """Represents a feedback loop in the system."""
    model_config = ConfigDict(use_enum_values=True)
    
    loop_nodes: List[str] = Field(
        description="Ordered list of nodes forming the loop",
        min_length=2
    )
    
    feedback_type: FeedbackType = Field(
        description="Type of feedback loop"
    )
    
    strength: float = Field(
        description="Strength of the feedback effect (0.0-1.0)",
        ge=0.0,
        le=1.0
    )
    
    cycle_time: str = Field(
        description="Time for one complete cycle"
    )
    
    stability_threshold: Optional[float] = Field(
        None,
        description="Threshold beyond which loop becomes unstable",
        ge=0.0,
        le=1.0
    )
    
    amplification_rate: Optional[float] = Field(
        None,
        description="Rate of amplification per cycle (for positive feedback)"
    )


class RiskArea(BaseModel):
    """Represents an area of risk in the propagation network."""
    model_config = ConfigDict(use_enum_values=True)
    
    description: str = Field(
        description="Description of the risk"
    )
    
    affected_nodes: List[str] = Field(
        description="Node IDs at risk",
        min_length=1
    )
    
    risk_level: str = Field(
        description="Level of risk (low, medium, high, critical)"
    )
    
    trigger_conditions: List[str] = Field(
        description="Conditions that could trigger this risk"
    )
    
    mitigation_strategies: List[str] = Field(
        default_factory=list,
        description="Strategies to mitigate the risk"
    )
    
    early_warning_indicators: List[str] = Field(
        default_factory=list,
        description="Indicators that risk is materializing"
    )


class InterventionPoint(BaseModel):
    """Represents a point where intervention can affect propagation."""
    model_config = ConfigDict(use_enum_values=True)
    
    node_id: str = Field(
        description="Node ID where intervention is possible"
    )
    
    intervention_type: str = Field(
        description="Type of intervention (e.g., 'block', 'dampen', 'redirect', 'amplify')"
    )
    
    effectiveness: float = Field(
        description="Expected effectiveness (0.0-1.0)",
        ge=0.0,
        le=1.0
    )
    
    cost: str = Field(
        description="Cost or effort required"
    )
    
    side_effects: List[str] = Field(
        default_factory=list,
        description="Potential side effects of intervention"
    )
    
    timing_critical: bool = Field(
        default=False,
        description="Whether timing is critical for effectiveness"
    )


class ImpactPropagationInput(CognitiveInputBase):
    """Input for Impact Propagation Mapping analysis."""
    
    scenario: str = Field(
        default="",
        description="The change or event to analyze for impact propagation"
    )
    
    domain_context: Optional[str] = Field(
        None,
        description="Domain context (e.g., 'organizational', 'technical', 'ecosystem', 'social')"
    )
    
    system_nodes: Optional[List[Node]] = Field(
        None,
        description="Pre-defined system nodes if known"
    )
    
    system_edges: Optional[List[Edge]] = Field(
        None,
        description="Pre-defined connections if known"
    )
    
    initial_impact: Optional[ImpactEvent] = Field(
        None,
        description="The initial impact event"
    )
    
    analysis_depth: Optional[int] = Field(
        3,
        description="How many degrees of propagation to analyze",
        ge=1,
        le=10
    )
    
    time_horizon: Optional[str] = Field(
        None,
        description="Time horizon for analysis"
    )
    
    focus_areas: Optional[List[str]] = Field(
        None,
        description="Specific areas to focus analysis on"
    )
    
    risk_tolerance: Optional[str] = Field(
        "medium",
        description="Risk tolerance level (low, medium, high)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "scenario": "Implementing new AI automation in customer service",
                "domain_context": "organizational",
                "initial_impact": {
                    "node_id": "customer_service_dept",
                    "impact_type": "direct",
                    "description": "Automation of routine inquiries",
                    "magnitude": "major",
                    "probability": 1.0
                },
                "analysis_depth": 4,
                "time_horizon": "6 months",
                "focus_areas": ["employee_impact", "customer_experience", "operational_efficiency"],
                "risk_tolerance": "low"
            }
        }


class ImpactPropagationAnalysis(CognitiveOutputBase):
    """Complete Impact Propagation Mapping analysis output."""
    
    input_scenario: str = Field(
        description="The analyzed scenario"
    )
    
    impact_network: Dict[str, Node] = Field(
        description="Network of system nodes"
    )
    
    connections: List[Edge] = Field(
        description="Connections between nodes"
    )
    
    primary_impacts: List[ImpactEvent] = Field(
        description="Direct, first-order impacts"
    )
    
    propagation_paths: List[PropagationPath] = Field(
        description="Paths of impact propagation"
    )
    
    feedback_loops: List[FeedbackLoop] = Field(
        description="Identified feedback loops"
    )
    
    cascade_effects: List[ImpactEvent] = Field(
        description="Cascading and emergent effects"
    )
    
    risk_areas: List[RiskArea] = Field(
        description="Identified risk areas"
    )
    
    intervention_points: List[InterventionPoint] = Field(
        description="Optimal intervention points"
    )
    
    critical_nodes: List[str] = Field(
        description="Node IDs that are critical for system stability"
    )
    
    timeline_projection: Dict[str, List[ImpactEvent]] = Field(
        description="Projected impacts over time"
    )
    
    mitigation_strategies: List[str] = Field(
        description="Recommended mitigation strategies"
    )
    
    amplification_risks: List[str] = Field(
        description="Risks of impact amplification"
    )
    
    system_resilience_score: float = Field(
        description="Overall system resilience (0.0-1.0)",
        ge=0.0,
        le=1.0
    )
    
    visual_representation: Optional[Dict[str, Any]] = Field(
        None,
        description="Data for visualizing the propagation network"
    )
    
    key_insights: List[str] = Field(
        description="Key insights from the analysis"
    )
    
    confidence_level: float = Field(
        description="Confidence in the analysis (0.0-1.0)",
        ge=0.0,
        le=1.0
    )