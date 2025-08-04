"""
Impact Propagation Models

Data structures for impact propagation mapping including nodes, edges,
propagation paths, feedback loops, and risk areas.
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime
import uuid


class ComplexityLevel(str, Enum):
    """Analysis complexity levels"""
    SIMPLE = "simple"
    MODERATE = "moderate" 
    COMPLEX = "complex"
    VERY_COMPLEX = "very_complex"


class ImpactType(str, Enum):
    """Types of impacts in the system"""
    DIRECT = "direct"              # Immediate, first-order effect
    INDIRECT = "indirect"          # Second-order effect  
    CASCADE = "cascade"            # Multi-level propagation
    FEEDBACK = "feedback"          # Circular/reinforcing effect
    EMERGENT = "emergent"          # Unexpected system behavior
    SYSTEMIC = "systemic"          # System-wide effect


class PropagationSpeed(str, Enum):
    """Speed of impact propagation"""
    IMMEDIATE = "immediate"        # Instant effect
    RAPID = "rapid"               # Hours to days
    MODERATE = "moderate"         # Days to weeks
    SLOW = "slow"                 # Weeks to months
    GRADUAL = "gradual"           # Months to years


class EffectMagnitude(str, Enum):
    """Magnitude of the effect"""
    NEGLIGIBLE = "negligible"
    MINOR = "minor"
    MODERATE = "moderate"
    SIGNIFICANT = "significant"
    MAJOR = "major"
    CRITICAL = "critical"


class FeedbackType(str, Enum):
    """Types of feedback loops"""
    POSITIVE = "positive"          # Reinforcing/amplifying
    NEGATIVE = "negative"          # Balancing/dampening
    OSCILLATING = "oscillating"    # Alternating effects
    COMPLEX = "complex"            # Mixed feedback patterns


class Node(BaseModel):
    """Represents a node in the impact propagation network"""
    
    id: str = Field(
        ...,
        description="Unique identifier for the node"
    )
    
    name: str = Field(
        ...,
        description="Name of the system element",
        min_length=1,
        max_length=200
    )
    
    category: str = Field(
        ...,
        description="Category of the node (e.g., 'technical', 'human', 'process')",
        min_length=1,
        max_length=100
    )
    
    initial_state: Optional[str] = Field(
        None,
        description="Initial state before impact",
        max_length=500
    )
    
    sensitivity: float = Field(
        0.5,
        description="Sensitivity to changes (0.0-1.0)",
        ge=0.0,
        le=1.0
    )
    
    resilience: float = Field(
        0.5,
        description="Resilience to disruption (0.0-1.0)",
        ge=0.0,
        le=1.0
    )
    
    influence_radius: int = Field(
        1,
        description="How many degrees of separation this node can influence",
        ge=1,
        le=10
    )
    
    @field_validator('name', 'category')
    @classmethod
    def validate_non_empty(cls, v):
        """Validate fields are not empty"""
        if not v or v.strip() == "":
            raise ValueError("Field cannot be empty")
        return v.strip()


class Edge(BaseModel):
    """Represents a connection between nodes"""
    
    source_id: str = Field(
        ...,
        description="Source node ID"
    )
    
    target_id: str = Field(
        ...,
        description="Target node ID"
    )
    
    relationship_type: str = Field(
        ...,
        description="Type of relationship (e.g., 'depends_on', 'influences', 'triggers')",
        min_length=1,
        max_length=100
    )
    
    strength: float = Field(
        0.5,
        description="Strength of connection (0.0-1.0)",
        ge=0.0,
        le=1.0
    )
    
    propagation_speed: PropagationSpeed = Field(
        ...,
        description="Speed of effect propagation"
    )
    
    bidirectional: bool = Field(
        False,
        description="Whether effects flow both ways"
    )
    
    @field_validator('source_id', 'target_id')
    @classmethod
    def validate_ids_different(cls, v, info):
        """Validate source and target are different"""
        if 'source_id' in info.data and v == info.data['source_id']:
            raise ValueError("Source and target IDs must be different")
        return v


class ImpactEvent(BaseModel):
    """Represents an impact on a node"""
    
    node_id: str = Field(
        ...,
        description="ID of impacted node"
    )
    
    impact_type: ImpactType = Field(
        ...,
        description="Type of impact"
    )
    
    description: str = Field(
        ...,
        description="Description of the impact",
        min_length=10,
        max_length=1000
    )
    
    magnitude: EffectMagnitude = Field(
        ...,
        description="Magnitude of the impact"
    )
    
    probability: float = Field(
        1.0,
        description="Probability of occurrence (0.0-1.0)",
        ge=0.0,
        le=1.0
    )
    
    time_delay: Optional[str] = Field(
        None,
        description="Time delay before impact manifests",
        max_length=100
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="When this impact was identified"
    )


class PropagationPath(BaseModel):
    """Represents a path of impact propagation"""
    
    path_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for this path"
    )
    
    path_nodes: List[str] = Field(
        ...,
        description="Ordered list of node IDs in the path",
        min_items=2,
        max_items=20
    )
    
    total_impact: EffectMagnitude = Field(
        ...,
        description="Cumulative impact along the path"
    )
    
    propagation_time: str = Field(
        ...,
        description="Total time for impact to propagate",
        min_length=1,
        max_length=100
    )
    
    attenuation_factor: float = Field(
        ...,
        description="How much impact diminishes along path (0.0-1.0)",
        ge=0.0,
        le=1.0
    )
    
    critical_points: List[str] = Field(
        default_factory=list,
        description="Node IDs that are critical in this path",
        max_items=10
    )
    
    @field_validator('path_nodes')
    @classmethod
    def validate_path_nodes(cls, v):
        """Validate path has no loops"""
        if len(v) != len(set(v)):
            raise ValueError("Path cannot contain duplicate nodes")
        return v


class FeedbackLoop(BaseModel):
    """Represents a feedback loop in the system"""
    
    loop_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for this loop"
    )
    
    loop_nodes: List[str] = Field(
        ...,
        description="Ordered list of nodes forming the loop",
        min_items=2,
        max_items=15
    )
    
    feedback_type: FeedbackType = Field(
        ...,
        description="Type of feedback loop"
    )
    
    strength: float = Field(
        ...,
        description="Strength of the feedback effect (0.0-1.0)",
        ge=0.0,
        le=1.0
    )
    
    cycle_time: str = Field(
        ...,
        description="Time for one complete cycle",
        min_length=1,
        max_length=100
    )
    
    stability_threshold: Optional[float] = Field(
        None,
        description="Threshold beyond which loop becomes unstable",
        ge=0.0,
        le=1.0
    )
    
    amplification_rate: Optional[float] = Field(
        None,
        description="Rate of amplification per cycle (for positive feedback)",
        ge=0.0,
        le=10.0
    )
    
    @field_validator('loop_nodes')
    @classmethod
    def validate_loop_nodes(cls, v):
        """Validate loop forms a cycle"""
        if len(v) > 2 and v[0] != v[-1]:
            raise ValueError("Loop must end where it starts")
        return v


class RiskArea(BaseModel):
    """Represents an area of risk in the propagation network"""
    
    risk_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for this risk"
    )
    
    description: str = Field(
        ...,
        description="Description of the risk",
        min_length=20,
        max_length=1000
    )
    
    affected_nodes: List[str] = Field(
        ...,
        description="Node IDs at risk",
        min_items=1,
        max_items=50
    )
    
    risk_level: str = Field(
        ...,
        description="Level of risk (low, medium, high, critical)"
    )
    
    trigger_conditions: List[str] = Field(
        ...,
        description="Conditions that could trigger this risk",
        min_items=1,
        max_items=10
    )
    
    mitigation_strategies: List[str] = Field(
        default_factory=list,
        description="Strategies to mitigate the risk",
        max_items=10
    )
    
    early_warning_indicators: List[str] = Field(
        default_factory=list,
        description="Indicators that risk is materializing",
        max_items=10
    )
    
    @field_validator('risk_level')
    @classmethod
    def validate_risk_level(cls, v):
        """Validate risk level is valid"""
        valid_levels = ["low", "medium", "high", "critical"]
        if v.lower() not in valid_levels:
            raise ValueError(f"Risk level must be one of: {', '.join(valid_levels)}")
        return v.lower()


class InterventionPoint(BaseModel):
    """Represents a point where intervention can affect propagation"""
    
    intervention_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for this intervention"
    )
    
    node_id: str = Field(
        ...,
        description="Node ID where intervention is possible"
    )
    
    intervention_type: str = Field(
        ...,
        description="Type of intervention (e.g., 'block', 'dampen', 'redirect', 'amplify')",
        min_length=1,
        max_length=100
    )
    
    effectiveness: float = Field(
        ...,
        description="Expected effectiveness (0.0-1.0)",
        ge=0.0,
        le=1.0
    )
    
    cost: str = Field(
        ...,
        description="Cost or effort required",
        min_length=1,
        max_length=500
    )
    
    side_effects: List[str] = Field(
        default_factory=list,
        description="Potential side effects of intervention",
        max_items=10
    )
    
    timing_critical: bool = Field(
        False,
        description="Whether timing is critical for effectiveness"
    )
    
    implementation_time: Optional[str] = Field(
        None,
        description="Time required to implement intervention",
        max_length=100
    )


class ImpactPropagationContext(BaseModel):
    """Context for impact propagation analysis"""
    
    scenario: str = Field(
        ...,
        description="The change or event to analyze for impact propagation",
        min_length=10,
        max_length=2000
    )
    
    complexity_level: ComplexityLevel = Field(
        ComplexityLevel.MODERATE,
        description="Complexity level of the analysis"
    )
    
    domain_context: Optional[str] = Field(
        None,
        description="Domain context (e.g., 'organizational', 'technical', 'ecosystem', 'social')",
        max_length=100
    )
    
    system_nodes: Optional[List[Node]] = Field(
        None,
        description="Pre-defined system nodes if known",
        max_items=100
    )
    
    system_edges: Optional[List[Edge]] = Field(
        None,
        description="Pre-defined connections if known",
        max_items=500
    )
    
    initial_impact: Optional[ImpactEvent] = Field(
        None,
        description="The initial impact event"
    )
    
    analysis_depth: int = Field(
        3,
        description="How many degrees of propagation to analyze",
        ge=1,
        le=10
    )
    
    time_horizon: Optional[str] = Field(
        None,
        description="Time horizon for analysis",
        max_length=100
    )
    
    focus_areas: Optional[List[str]] = Field(
        None,
        description="Specific areas to focus analysis on",
        max_items=10
    )
    
    risk_tolerance: str = Field(
        "medium",
        description="Risk tolerance level (low, medium, high)"
    )
    
    @field_validator('scenario')
    @classmethod
    def validate_scenario(cls, v):
        """Validate scenario is meaningful"""
        if not v or v.strip() == "":
            raise ValueError("Scenario cannot be empty")
        return v.strip()
    
    @field_validator('risk_tolerance')
    @classmethod
    def validate_risk_tolerance(cls, v):
        """Validate risk tolerance level"""
        valid_levels = ["low", "medium", "high"]
        if v.lower() not in valid_levels:
            raise ValueError(f"Risk tolerance must be one of: {', '.join(valid_levels)}")
        return v.lower()


class ImpactPropagationResult(BaseModel):
    """Result of impact propagation analysis"""
    
    input_scenario: str = Field(
        ...,
        description="The analyzed scenario"
    )
    
    impact_network: Dict[str, Node] = Field(
        ...,
        description="Network of system nodes"
    )
    
    connections: List[Edge] = Field(
        ...,
        description="Connections between nodes"
    )
    
    primary_impacts: List[ImpactEvent] = Field(
        ...,
        description="Direct, first-order impacts",
        min_items=1
    )
    
    propagation_paths: List[PropagationPath] = Field(
        ...,
        description="Paths of impact propagation"
    )
    
    feedback_loops: List[FeedbackLoop] = Field(
        default_factory=list,
        description="Identified feedback loops"
    )
    
    cascade_effects: List[ImpactEvent] = Field(
        default_factory=list,
        description="Cascading and emergent effects"
    )
    
    risk_areas: List[RiskArea] = Field(
        ...,
        description="Identified risk areas",
        min_items=1
    )
    
    intervention_points: List[InterventionPoint] = Field(
        ...,
        description="Optimal intervention points"
    )
    
    critical_nodes: List[str] = Field(
        ...,
        description="Node IDs that are critical for system stability",
        min_items=1
    )
    
    timeline_projection: Dict[str, List[ImpactEvent]] = Field(
        default_factory=dict,
        description="Projected impacts over time"
    )
    
    mitigation_strategies: List[str] = Field(
        ...,
        description="Recommended mitigation strategies",
        min_items=1,
        max_items=15
    )
    
    amplification_risks: List[str] = Field(
        default_factory=list,
        description="Risks of impact amplification",
        max_items=10
    )
    
    system_resilience_score: float = Field(
        ...,
        description="Overall system resilience (0.0-1.0)",
        ge=0.0,
        le=1.0
    )
    
    visualization_data: Optional[Dict[str, Any]] = Field(
        None,
        description="Data for visualizing the propagation network"
    )
    
    key_insights: List[str] = Field(
        ...,
        description="Key insights from the analysis",
        min_items=3,
        max_items=10
    )
    
    confidence_score: float = Field(
        ...,
        description="Confidence in the analysis (0.0-1.0)",
        ge=0.0,
        le=1.0
    )
    
    processing_time_ms: int = Field(
        0,
        description="Time taken to process in milliseconds"
    )
    
    def get_critical_risks(self) -> List[RiskArea]:
        """Get risks marked as critical"""
        return [risk for risk in self.risk_areas if risk.risk_level == "critical"]
    
    def get_immediate_impacts(self) -> List[ImpactEvent]:
        """Get impacts that occur immediately"""
        return [
            impact for impact in self.primary_impacts + self.cascade_effects
            if impact.time_delay is None or impact.time_delay == "0 hours"
        ]
    
    def get_intervention_by_effectiveness(self, min_effectiveness: float = 0.7) -> List[InterventionPoint]:
        """Get interventions above a certain effectiveness threshold"""
        return sorted(
            [i for i in self.intervention_points if i.effectiveness >= min_effectiveness],
            key=lambda x: x.effectiveness,
            reverse=True
        )