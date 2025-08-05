"""Base store for Scientific Method tool session management."""

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Variable(BaseModel):
    """Model for experimental variables."""
    
    name: str = Field(..., description="Variable name")
    type: str = Field(..., description="Type: independent, dependent, controlled")
    description: str = Field(..., description="What this variable represents")
    measurement_unit: Optional[str] = Field(None, description="Unit of measurement")
    expected_range: Optional[Dict[str, Any]] = Field(None, description="Expected value range")


class ExperimentDesign(BaseModel):
    """Model for experiment design."""
    
    design_id: Optional[int] = Field(None, description="Unique design ID")
    name: str = Field(..., description="Experiment name")
    methodology: str = Field(..., description="Experimental methodology")
    sample_size: Optional[int] = Field(None, description="Number of samples/trials")
    control_group: bool = Field(False, description="Whether control group exists")
    randomization: bool = Field(False, description="Whether randomization is used")
    blinding: Optional[str] = Field(None, description="Blinding type: single, double, none")
    duration: Optional[str] = Field(None, description="Expected duration")
    resources_needed: List[str] = Field(default_factory=list, description="Required resources")


class Observation(BaseModel):
    """Model for experimental observations."""
    
    observation_id: Optional[int] = Field(None, description="Unique observation ID")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    data_point: Dict[str, Any] = Field(..., description="Observed data")
    conditions: Dict[str, Any] = Field(default_factory=dict, description="Experimental conditions")
    notes: Optional[str] = Field(None, description="Additional notes")
    anomaly: bool = Field(False, description="Whether this is an anomaly")


class ExperimentResults(BaseModel):
    """Model for experiment results."""
    
    observations: List[Observation] = Field(default_factory=list, description="All observations")
    statistical_analysis: Dict[str, Any] = Field(default_factory=dict, description="Statistical results")
    patterns_found: List[str] = Field(default_factory=list, description="Patterns identified")
    anomalies: List[Dict[str, Any]] = Field(default_factory=list, description="Anomalies detected")
    conclusions: List[str] = Field(default_factory=list, description="Conclusions drawn")
    confidence_level: float = Field(0.95, description="Statistical confidence level")


class HypothesisData(BaseModel):
    """Data model for scientific hypothesis storage."""
    
    id: Optional[int] = Field(None, description="Database ID")
    session_id: str = Field(..., description="Session this hypothesis belongs to")
    
    # Hypothesis formulation
    hypothesis_statement: str = Field(..., description="The hypothesis being tested")
    null_hypothesis: Optional[str] = Field(None, description="Null hypothesis")
    theoretical_basis: str = Field(..., description="Theoretical foundation")
    
    # Variables
    variables: List[Variable] = Field(default_factory=list, description="All variables")
    relationships: List[str] = Field(default_factory=list, description="Expected relationships")
    
    # Predictions and testing
    predictions: List[str] = Field(default_factory=list, description="Specific predictions")
    falsifiable_conditions: List[str] = Field(default_factory=list, description="How it can be falsified")
    experiment_designs: List[ExperimentDesign] = Field(default_factory=list, description="Proposed experiments")
    
    # Results and validation
    test_results: Optional[ExperimentResults] = Field(None, description="Experimental results")
    status: str = Field("proposed", description="Status: proposed, testing, validated, refuted, inconclusive")
    confidence: float = Field(0.5, description="Confidence in hypothesis")
    
    # Implications
    implications_if_true: List[str] = Field(default_factory=list, description="What it means if true")
    implications_if_false: List[str] = Field(default_factory=list, description="What it means if false")
    next_steps: List[str] = Field(default_factory=list, description="Follow-up research needed")
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    tested_at: Optional[datetime] = Field(None, description="When testing was completed")
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ExperimentData(BaseModel):
    """Data model for experiment execution storage."""
    
    id: Optional[int] = Field(None, description="Database ID")
    hypothesis_id: int = Field(..., description="Associated hypothesis ID")
    session_id: str = Field(..., description="Session this experiment belongs to")
    
    # Experiment setup
    design: ExperimentDesign = Field(..., description="Experiment design used")
    actual_conditions: Dict[str, Any] = Field(default_factory=dict, description="Actual conditions")
    deviations_from_plan: List[str] = Field(default_factory=list, description="Any deviations")
    
    # Execution
    start_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    end_time: Optional[datetime] = Field(None, description="When experiment ended")
    observations: List[Observation] = Field(default_factory=list, description="All observations")
    
    # Analysis
    results: Optional[ExperimentResults] = Field(None, description="Final results")
    validity_assessment: Dict[str, Any] = Field(default_factory=dict, description="Internal/external validity")
    limitations: List[str] = Field(default_factory=list, description="Experimental limitations")
    
    # Replication
    replicable: bool = Field(True, description="Whether experiment is replicable")
    replication_instructions: Optional[str] = Field(None, description="How to replicate")
    
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ScientificConclusion(BaseModel):
    """Model for scientific conclusions."""
    
    session_id: str = Field(..., description="Session ID")
    hypotheses_tested: List[int] = Field(default_factory=list, description="IDs of hypotheses tested")
    
    # Findings
    supported_hypotheses: List[int] = Field(default_factory=list, description="Hypotheses supported")
    refuted_hypotheses: List[int] = Field(default_factory=list, description="Hypotheses refuted")
    inconclusive_hypotheses: List[int] = Field(default_factory=list, description="Inconclusive results")
    
    # Synthesis
    key_findings: List[str] = Field(default_factory=list, description="Main findings")
    theoretical_implications: List[str] = Field(default_factory=list, description="Theory implications")
    practical_applications: List[str] = Field(default_factory=list, description="Practical uses")
    
    # Future research
    new_questions: List[str] = Field(default_factory=list, description="New questions raised")
    recommended_studies: List[str] = Field(default_factory=list, description="Recommended follow-ups")
    
    confidence_in_conclusions: float = Field(0.85, description="Overall confidence")
    peer_review_needed: bool = Field(True, description="Whether peer review is recommended")


class BaseScientificStore(ABC):
    """Abstract base class for scientific method storage operations."""
    
    @abstractmethod
    async def save_hypothesis(self, hypothesis_data: HypothesisData) -> HypothesisData:
        """Save a new hypothesis."""
        pass
    
    @abstractmethod
    async def get_hypothesis(self, hypothesis_id: int) -> Optional[HypothesisData]:
        """Get a specific hypothesis by ID."""
        pass
    
    @abstractmethod
    async def get_session_hypotheses(self, session_id: str) -> List[HypothesisData]:
        """Get all hypotheses for a session."""
        pass
    
    @abstractmethod
    async def save_experiment(self, experiment_data: ExperimentData) -> ExperimentData:
        """Save a new experiment."""
        pass
    
    @abstractmethod
    async def get_experiment(self, experiment_id: int) -> Optional[ExperimentData]:
        """Get a specific experiment by ID."""
        pass
    
    @abstractmethod
    async def add_observation(
        self,
        experiment_id: int,
        observation: Observation
    ) -> Optional[ExperimentData]:
        """Add an observation to an experiment."""
        pass
    
    @abstractmethod
    async def save_results(
        self,
        experiment_id: int,
        results: ExperimentResults
    ) -> Optional[ExperimentData]:
        """Save experiment results."""
        pass
    
    @abstractmethod
    async def update_hypothesis_status(
        self,
        hypothesis_id: int,
        status: str,
        test_results: ExperimentResults
    ) -> Optional[HypothesisData]:
        """Update hypothesis status based on test results."""
        pass
    
    @abstractmethod
    async def save_conclusion(
        self,
        conclusion: ScientificConclusion
    ) -> ScientificConclusion:
        """Save scientific conclusions for a session."""
        pass
    
    @abstractmethod
    async def get_experiment_results(
        self,
        experiment_id: int
    ) -> Optional[ExperimentResults]:
        """Get results for a specific experiment."""
        pass
    
    @abstractmethod
    async def search_hypotheses(
        self,
        keywords: Optional[str] = None,
        status: Optional[str] = None,
        min_confidence: Optional[float] = None,
        has_results: Optional[bool] = None,
        limit: int = 100
    ) -> List[HypothesisData]:
        """Search hypotheses with various filters."""
        pass
    
    @abstractmethod
    async def get_replication_candidates(
        self,
        min_confidence: float = 0.7,
        max_replications: int = 3
    ) -> List[ExperimentData]:
        """Find experiments that should be replicated."""
        pass