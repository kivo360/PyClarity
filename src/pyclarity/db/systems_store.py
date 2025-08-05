"""Base store for Systems Thinking tool session management."""

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set

from pydantic import BaseModel, Field


class SystemComponent(BaseModel):
    """Model for a system component."""
    
    component_id: str = Field(..., description="Unique component identifier")
    name: str = Field(..., description="Component name")
    type: str = Field(..., description="Type: actor, process, store, flow, boundary")
    description: str = Field(..., description="Component description")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Component properties")
    inputs: List[str] = Field(default_factory=list, description="Input component IDs")
    outputs: List[str] = Field(default_factory=list, description="Output component IDs")
    constraints: List[str] = Field(default_factory=list, description="Component constraints")


class FeedbackLoop(BaseModel):
    """Model for system feedback loops."""
    
    loop_id: str = Field(..., description="Unique loop identifier")
    type: str = Field(..., description="Type: reinforcing, balancing")
    components: List[str] = Field(..., description="Component IDs in the loop")
    description: str = Field(..., description="Loop description")
    strength: float = Field(0.5, description="Loop strength (0-1)")
    delay: Optional[str] = Field(None, description="Time delay in loop")
    impact: str = Field(..., description="Impact on system behavior")


class SystemRelationship(BaseModel):
    """Model for relationships between components."""
    
    relationship_id: str = Field(..., description="Unique relationship identifier")
    source_id: str = Field(..., description="Source component ID")
    target_id: str = Field(..., description="Target component ID")
    relationship_type: str = Field(..., description="Type: causal, temporal, spatial, logical")
    strength: float = Field(0.5, description="Relationship strength (0-1)")
    polarity: str = Field("positive", description="positive or negative")
    delay: Optional[float] = Field(None, description="Time delay")
    description: Optional[str] = Field(None, description="Relationship description")


class EmergentProperty(BaseModel):
    """Model for emergent system properties."""
    
    property_name: str = Field(..., description="Name of emergent property")
    description: str = Field(..., description="Description of the property")
    contributing_components: List[str] = Field(..., description="Components that create this property")
    conditions: List[str] = Field(default_factory=list, description="Conditions for emergence")
    stability: float = Field(0.5, description="Stability of the property (0-1)")
    predictability: float = Field(0.5, description="How predictable it is (0-1)")


class SystemIntervention(BaseModel):
    """Model for system interventions."""
    
    intervention_id: Optional[int] = Field(None, description="Unique intervention ID")
    target_component: str = Field(..., description="Component to intervene on")
    intervention_type: str = Field(..., description="Type: modify, remove, add, connect")
    description: str = Field(..., description="What the intervention does")
    expected_effects: List[str] = Field(default_factory=list, description="Expected effects")
    side_effects: List[str] = Field(default_factory=list, description="Potential side effects")
    confidence: float = Field(0.5, description="Confidence in prediction (0-1)")


class SimulationResult(BaseModel):
    """Model for system simulation results."""
    
    simulation_id: Optional[int] = Field(None, description="Unique simulation ID")
    intervention_id: int = Field(..., description="Applied intervention ID")
    
    # Results
    direct_effects: List[Dict[str, Any]] = Field(default_factory=list, description="Direct effects observed")
    cascading_effects: List[Dict[str, Any]] = Field(default_factory=list, description="Cascading effects")
    new_equilibrium: Optional[Dict[str, Any]] = Field(None, description="New system state")
    
    # Metrics
    system_stability: float = Field(0.5, description="System stability after intervention (0-1)")
    unintended_consequences: List[str] = Field(default_factory=list, description="Unintended effects")
    time_to_stabilize: Optional[float] = Field(None, description="Time to reach new equilibrium")
    
    success_probability: float = Field(0.5, description="Probability of success (0-1)")


class SystemsData(BaseModel):
    """Data model for systems thinking session storage."""
    
    id: Optional[int] = Field(None, description="Database ID")
    session_id: str = Field(..., description="Session this system analysis belongs to")
    
    # System definition
    system_name: str = Field(..., description="Name of the system")
    system_purpose: str = Field(..., description="Purpose or function of the system")
    system_boundaries: List[str] = Field(default_factory=list, description="System boundaries")
    time_horizon: Optional[str] = Field(None, description="Time scope of analysis")
    
    # System structure
    components: List[SystemComponent] = Field(default_factory=list, description="All system components")
    relationships: List[SystemRelationship] = Field(default_factory=list, description="Component relationships")
    feedback_loops: List[FeedbackLoop] = Field(default_factory=list, description="Feedback loops")
    hierarchical_levels: Dict[int, List[str]] = Field(default_factory=dict, description="Components by level")
    
    # System dynamics
    emergent_properties: List[EmergentProperty] = Field(default_factory=list, description="Emergent properties")
    system_states: List[Dict[str, Any]] = Field(default_factory=list, description="Possible system states")
    attractors: List[Dict[str, Any]] = Field(default_factory=list, description="System attractors")
    
    # Analysis
    leverage_points: List[Dict[str, Any]] = Field(default_factory=list, description="High-impact intervention points")
    bottlenecks: List[str] = Field(default_factory=list, description="System bottlenecks")
    vulnerabilities: List[str] = Field(default_factory=list, description="System vulnerabilities")
    
    # Interventions and simulations
    proposed_interventions: List[SystemIntervention] = Field(default_factory=list, description="Proposed changes")
    simulation_results: List[SimulationResult] = Field(default_factory=list, description="Simulation outcomes")
    
    # Insights
    key_insights: List[str] = Field(default_factory=list, description="Main insights")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations")
    
    # Metrics
    complexity_score: float = Field(0.0, description="System complexity (0-1)")
    resilience_score: float = Field(0.0, description="System resilience (0-1)")
    adaptability_score: float = Field(0.0, description="System adaptability (0-1)")
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)


class BaseSystemsStore(ABC):
    """Abstract base class for systems thinking storage operations."""
    
    @abstractmethod
    async def save_system_analysis(self, systems_data: SystemsData) -> SystemsData:
        """Save a new system analysis."""
        pass
    
    @abstractmethod
    async def get_system_analysis(self, analysis_id: int) -> Optional[SystemsData]:
        """Get a system analysis by ID."""
        pass
    
    @abstractmethod
    async def get_session_systems(self, session_id: str) -> List[SystemsData]:
        """Get all system analyses for a session."""
        pass
    
    @abstractmethod
    async def add_component(
        self,
        analysis_id: int,
        component: SystemComponent
    ) -> Optional[SystemsData]:
        """Add a component to the system."""
        pass
    
    @abstractmethod
    async def add_relationship(
        self,
        analysis_id: int,
        relationship: SystemRelationship
    ) -> Optional[SystemsData]:
        """Add a relationship between components."""
        pass
    
    @abstractmethod
    async def identify_feedback_loops(
        self,
        analysis_id: int
    ) -> List[FeedbackLoop]:
        """Identify feedback loops in the system."""
        pass
    
    @abstractmethod
    async def add_emergent_property(
        self,
        analysis_id: int,
        property: EmergentProperty
    ) -> Optional[SystemsData]:
        """Add an identified emergent property."""
        pass
    
    @abstractmethod
    async def propose_intervention(
        self,
        analysis_id: int,
        intervention: SystemIntervention
    ) -> SystemIntervention:
        """Propose a system intervention."""
        pass
    
    @abstractmethod
    async def simulate_intervention(
        self,
        analysis_id: int,
        intervention_id: int
    ) -> SimulationResult:
        """Simulate an intervention's effects."""
        pass
    
    @abstractmethod
    async def find_leverage_points(
        self,
        analysis_id: int,
        min_impact: float = 0.7
    ) -> List[Dict[str, Any]]:
        """Find high-leverage intervention points."""
        pass
    
    @abstractmethod
    async def analyze_system_health(
        self,
        analysis_id: int
    ) -> Dict[str, Any]:
        """Analyze overall system health metrics."""
        pass
    
    @abstractmethod
    async def compare_systems(
        self,
        system_id_1: int,
        system_id_2: int
    ) -> Dict[str, Any]:
        """Compare two system analyses."""
        pass
    
    @abstractmethod
    async def search_systems(
        self,
        keywords: Optional[str] = None,
        min_complexity: Optional[float] = None,
        has_feedback_loops: Optional[bool] = None,
        limit: int = 100
    ) -> List[SystemsData]:
        """Search system analyses with filters."""
        pass