"""
Pydantic models for Strategic Decision Accelerator.

These models define the data structures for quantum decision states,
scenario modeling, stakeholder alignment, and strategic acceleration.
"""

from enum import Enum
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
from pydantic import BaseModel, Field, validator
import uuid


class DecisionState(str, Enum):
    """Quantum decision states representing decision maturity."""
    EXPLORATION = "exploration"
    CONVERGENCE = "convergence"
    COMMITMENT = "commitment"
    VALIDATION = "validation"
    ACCELERATION = "acceleration"


class DecisionType(str, Enum):
    """Types of strategic decisions."""
    STRATEGIC_GROWTH = "strategic_growth"
    INNOVATION_STRATEGY = "innovation_strategy"
    CRISIS_RESPONSE = "crisis_response"
    MERGER_ACQUISITION = "merger_acquisition"
    TRANSFORMATION = "transformation"
    DIVESTITURE = "divestiture"
    OPERATIONAL = "operational"


class UrgencyLevel(str, Enum):
    """Decision urgency levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    IMMEDIATE = "immediate"


class ComplexityLevel(str, Enum):
    """Decision complexity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"
    EXTREME = "extreme"


class RiskLevel(str, Enum):
    """Risk assessment levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"
    CRITICAL = "critical"


# Core Data Models

class DecisionOption(BaseModel):
    """A strategic decision option."""
    option_id: str = Field(..., description="Unique identifier for the option")
    title: str = Field(..., description="Option title")
    description: str = Field(..., description="Detailed option description")
    strategic_fit: float = Field(..., ge=0, le=10, description="Strategic alignment score")
    risk_level: RiskLevel = Field(..., description="Risk assessment")
    resource_requirements: str = Field(..., description="Resource requirements description")
    timeline: str = Field(..., description="Implementation timeline")
    expected_impact: str = Field(..., description="Expected impact description")
    investment_required: Optional[float] = Field(None, description="Financial investment required")
    expected_roi: Optional[float] = Field(None, description="Expected return on investment")


class DecisionCriterion(BaseModel):
    """A decision evaluation criterion."""
    name: str = Field(..., description="Criterion name")
    weight: float = Field(..., ge=0, le=1, description="Criterion weight (0-1)")
    description: str = Field(..., description="Criterion description")


class StakeholderGroup(BaseModel):
    """A stakeholder group."""
    group: str = Field(..., description="Stakeholder group name")
    members: int = Field(..., ge=1, description="Number of members")
    influence: str = Field(..., description="Influence level")
    interest: str = Field(..., description="Interest level")
    current_position: str = Field(..., description="Current position on decision")
    decision_power: str = Field(..., description="Decision-making power")


class ScenarioProjection(BaseModel):
    """Financial and strategic projections for a scenario."""
    revenue_impact: float = Field(..., description="Revenue impact percentage")
    cost_impact: float = Field(..., description="Cost impact percentage") 
    roi: float = Field(..., description="Return on investment")
    payback_months: int = Field(..., ge=0, description="Payback period in months")


class RiskFactor(BaseModel):
    """A risk factor in decision scenarios."""
    risk: str = Field(..., description="Risk description")
    probability: float = Field(..., ge=0, le=1, description="Probability of occurrence")
    impact: str = Field(..., description="Impact level")
    mitigation: str = Field(..., description="Mitigation strategy")


# Input Models

class DecisionContext(BaseModel):
    """Complete context for a strategic decision."""
    decision_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique decision ID")
    decision_title: str = Field(..., description="Decision title")
    decision_type: DecisionType = Field(..., description="Type of decision")
    urgency_level: UrgencyLevel = Field(..., description="Urgency level")
    complexity_level: ComplexityLevel = Field(..., description="Complexity level")
    decision_scope: str = Field(..., description="Scope of decision impact")
    timeline_pressure: str = Field(..., description="Timeline pressure description")
    
    context: Dict[str, Any] = Field(default_factory=dict, description="Business context")
    decision_options: List[DecisionOption] = Field(default_factory=list, description="Available decision options")
    stakeholders: Dict[str, List[str]] = Field(default_factory=dict, description="Stakeholder mapping")
    constraints: Dict[str, str] = Field(default_factory=dict, description="Decision constraints")
    
    @validator('decision_options')
    def validate_options(cls, v):
        if len(v) < 2:
            raise ValueError("At least 2 decision options are required")
        return v


# Output Models

class QuantumDecisionState(BaseModel):
    """Quantum decision state analysis."""
    current_state: DecisionState = Field(..., description="Current quantum state")
    state_confidence: float = Field(..., ge=0, le=1, description="Confidence in state assessment")
    state_transitions: Dict[str, float] = Field(..., description="State transition probabilities")
    state_characteristics: Dict[str, float] = Field(..., description="Current state characteristics")
    next_state_triggers: List[str] = Field(..., description="Triggers for next state transition")


class OptionEvaluation(BaseModel):
    """Option evaluation results."""
    evaluation_matrix: Dict[str, Dict[str, float]] = Field(..., description="Evaluation scores matrix")
    weighted_scores: Dict[str, float] = Field(..., description="Weighted total scores")
    ranking: List[str] = Field(..., description="Ranked option IDs")
    score_sensitivity: str = Field(..., description="Sensitivity analysis result")
    evaluation_confidence: float = Field(..., ge=0, le=1, description="Confidence in evaluation")


class DecisionCrystallization(BaseModel):
    """Decision crystallization results."""
    readiness_score: float = Field(..., ge=0, le=100, description="Decision readiness score")
    quantum_decision_state: QuantumDecisionState = Field(..., description="Quantum state analysis")
    decision_options: List[DecisionOption] = Field(..., description="Crystallized options")
    decision_criteria: Dict[str, Any] = Field(..., description="Decision criteria analysis")
    option_evaluation: OptionEvaluation = Field(..., description="Option evaluation results")
    crystallization_quality: Dict[str, float] = Field(..., description="Quality metrics")
    decision_complexity: Dict[str, Any] = Field(..., description="Complexity analysis")
    recommendations: List[Dict[str, Any]] = Field(default_factory=list, description="Crystallization recommendations")


class ScenarioAnalysis(BaseModel):
    """Comprehensive scenario analysis."""
    base_case: Dict[str, Any] = Field(..., description="Base case scenario")
    optimistic_case: Dict[str, Any] = Field(..., description="Optimistic scenario")
    pessimistic_case: Dict[str, Any] = Field(..., description="Pessimistic scenario")
    scenario_robustness: float = Field(..., ge=0, le=1, description="Scenario robustness score")
    scenario_diversity: str = Field(..., description="Scenario diversity assessment")


class MonteCarloResults(BaseModel):
    """Monte Carlo simulation results."""
    simulation_runs: int = Field(..., ge=1000, description="Number of simulation runs")
    outcome_distribution: Dict[str, float] = Field(..., description="Outcome distribution statistics")
    success_probability: float = Field(..., ge=0, le=1, description="Probability of success")
    risk_of_failure: float = Field(..., ge=0, le=1, description="Probability of failure")
    confidence_intervals: Dict[str, List[float]] = Field(..., description="Confidence intervals")
    simulation_quality: str = Field(..., description="Simulation quality assessment")


class ScenarioModeling(BaseModel):
    """Scenario modeling results."""
    readiness_score: float = Field(..., ge=0, le=100, description="Scenario readiness score")
    scenario_analysis: ScenarioAnalysis = Field(..., description="Scenario analysis results")
    outcome_projections: Dict[str, Any] = Field(..., description="Outcome projections")
    risk_modeling: Dict[str, Any] = Field(..., description="Risk modeling results")
    sensitivity_analysis: Dict[str, Any] = Field(..., description="Sensitivity analysis")
    monte_carlo_results: MonteCarloResults = Field(..., description="Monte Carlo simulation")
    scenario_planning: Dict[str, Any] = Field(..., description="Scenario planning framework")
    recommendations: List[Dict[str, Any]] = Field(default_factory=list, description="Scenario recommendations")


class StakeholderAlignment(BaseModel):
    """Stakeholder alignment analysis."""
    readiness_score: float = Field(..., ge=0, le=100, description="Alignment readiness score")
    stakeholder_mapping: Dict[str, Any] = Field(..., description="Stakeholder mapping results")
    alignment_analysis: Dict[str, Any] = Field(..., description="Current alignment analysis")
    influence_dynamics: Dict[str, Any] = Field(..., description="Influence dynamics analysis")
    consensus_building: Dict[str, Any] = Field(..., description="Consensus building strategy")
    communication_strategy: Dict[str, Any] = Field(..., description="Communication strategy")
    resistance_management: Dict[str, Any] = Field(..., description="Resistance management plan")
    recommendations: List[Dict[str, Any]] = Field(default_factory=list, description="Alignment recommendations")


class AccelerationAnalysis(BaseModel):
    """Process acceleration analysis."""
    readiness_score: float = Field(..., ge=0, le=100, description="Acceleration readiness score")
    acceleration_opportunities: List[Dict[str, Any]] = Field(..., description="Acceleration opportunities")
    momentum_analysis: Dict[str, Any] = Field(..., description="Current momentum analysis")
    velocity_optimization: Dict[str, Any] = Field(..., description="Velocity optimization strategies")
    bottleneck_elimination: Dict[str, Any] = Field(..., description="Bottleneck elimination plan")
    fast_track_options: Dict[str, Any] = Field(..., description="Fast-track options")
    quick_wins_identification: List[Dict[str, Any]] = Field(..., description="Quick wins identified")
    recommendations: List[Dict[str, Any]] = Field(default_factory=list, description="Acceleration recommendations")


class ValidationFramework(BaseModel):
    """Decision validation framework."""
    readiness_score: float = Field(..., ge=0, le=100, description="Validation readiness score")
    validation_framework: Dict[str, Any] = Field(..., description="Validation approach")
    success_metrics: Dict[str, Any] = Field(..., description="Success metrics definition")
    learning_loops: Dict[str, Any] = Field(..., description="Learning loop mechanisms")
    course_correction: Dict[str, Any] = Field(..., description="Course correction planning")
    validation_timeline: Dict[str, Any] = Field(..., description="Validation timeline")
    early_warning_system: Dict[str, Any] = Field(..., description="Early warning system")
    recommendations: List[Dict[str, Any]] = Field(default_factory=list, description="Validation recommendations")


class DecisionRoadmap(BaseModel):
    """Decision implementation roadmap."""
    decision_phases: List[Dict[str, Any]] = Field(..., description="Decision implementation phases")
    critical_milestones: List[str] = Field(..., description="Critical milestones")
    success_metrics: List[str] = Field(..., description="Success measurement metrics")


class StrategicDecisionResult(BaseModel):
    """Complete strategic decision acceleration result."""
    decision_readiness_score: float = Field(..., ge=0, le=100, description="Overall readiness score")
    decision_crystallization: DecisionCrystallization = Field(..., description="Decision crystallization results")
    scenario_modeling: ScenarioModeling = Field(..., description="Scenario modeling results")
    stakeholder_alignment: StakeholderAlignment = Field(..., description="Stakeholder alignment results")
    acceleration_analysis: AccelerationAnalysis = Field(..., description="Acceleration analysis results")
    validation_framework: ValidationFramework = Field(..., description="Validation framework")
    strategic_recommendations: List[Dict[str, Any]] = Field(..., description="Strategic recommendations")
    decision_roadmap: DecisionRoadmap = Field(..., description="Implementation roadmap")
    
    # Metadata
    analysis_timestamp: datetime = Field(default_factory=datetime.now, description="Analysis timestamp")
    analysis_duration_seconds: Optional[float] = Field(None, description="Analysis duration")
    analysis_quality_score: float = Field(default=0.0, ge=0, le=10, description="Analysis quality score")


# Request/Response Models for API

class StrategicDecisionRequest(BaseModel):
    """Request model for strategic decision acceleration."""
    context: DecisionContext = Field(..., description="Decision context")
    analysis_depth: str = Field(default="comprehensive", description="Analysis depth level")
    focus_areas: List[str] = Field(default_factory=list, description="Specific focus areas")
    time_limit_seconds: Optional[int] = Field(None, description="Analysis time limit")


class StrategicDecisionResponse(BaseModel):
    """Response model for strategic decision acceleration."""
    success: bool = Field(..., description="Operation success status")
    result: Optional[StrategicDecisionResult] = Field(None, description="Analysis results")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    processing_time_seconds: float = Field(..., description="Processing time")
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Request ID")