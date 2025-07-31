# Clear Thinking FastMCP Server - Metacognitive Monitoring Models

"""
Pydantic models for the Metacognitive Monitoring cognitive tool.

This tool supports self-reflection and thinking about thinking through:
- Reasoning process monitoring
- Bias detection and correction
- Confidence calibration
- Strategy evaluation and adjustment
- Meta-learning from reasoning patterns

Agent: AGENT D - Metacognitive Monitoring Implementation
Status: ACTIVE - Phase 2C Parallel Expansion
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union, Literal
from enum import Enum
from datetime import datetime
import uuid

from .base import CognitiveInputBase, CognitiveOutputBase, ComplexityLevel


class BiasType(str, Enum):
    """Types of cognitive biases to monitor"""
    
    CONFIRMATION_BIAS = "confirmation_bias"
    ANCHORING_BIAS = "anchoring_bias"
    AVAILABILITY_HEURISTIC = "availability_heuristic"
    REPRESENTATIVENESS_HEURISTIC = "representativeness_heuristic"
    OVERCONFIDENCE_BIAS = "overconfidence_bias"
    HINDSIGHT_BIAS = "hindsight_bias"
    FRAMING_EFFECT = "framing_effect"
    SUNK_COST_FALLACY = "sunk_cost_fallacy"
    GROUPTHINK = "groupthink"
    STATUS_QUO_BIAS = "status_quo_bias"
    
    @property
    def description(self) -> str:
        """Get description of the bias type"""
        descriptions = {
            self.CONFIRMATION_BIAS: "Tendency to search for or interpret information that confirms preconceptions",
            self.ANCHORING_BIAS: "Over-reliance on the first piece of information encountered",
            self.AVAILABILITY_HEURISTIC: "Overestimate likelihood of events based on memory availability",
            self.REPRESENTATIVENESS_HEURISTIC: "Judge probability by similarity to mental prototypes",
            self.OVERCONFIDENCE_BIAS: "Tendency to overestimate one's abilities or knowledge",
            self.HINDSIGHT_BIAS: "Tendency to perceive past events as more predictable than they were",
            self.FRAMING_EFFECT: "Drawing different conclusions from the same information based on presentation",
            self.SUNK_COST_FALLACY: "Continue investing based on previously invested resources",
            self.GROUPTHINK: "Conformity pressure leading to irrational decision making",
            self.STATUS_QUO_BIAS: "Preference for things to stay the same by doing nothing"
        }
        return descriptions.get(self, "Unknown bias type")


class MetaStrategies(str, Enum):
    """Metacognitive strategies for monitoring and control"""
    
    PLANNING = "planning"
    MONITORING = "monitoring"
    EVALUATING = "evaluating"
    REVISING = "revising"
    DEBUGGING = "debugging"
    PREDICTING = "predicting"
    CHECKING = "checking"
    REFLECTING = "reflecting"


class ConfidenceCalibration(str, Enum):
    """Methods for calibrating confidence levels"""
    
    FREQUENCY_BASED = "frequency_based"
    EVIDENCE_BASED = "evidence_based"
    EXPERTISE_BASED = "expertise_based"
    HISTORICAL_PERFORMANCE = "historical_performance"
    PEER_COMPARISON = "peer_comparison"


class BiasDetection(BaseModel):
    """Detection of a specific cognitive bias"""
    
    bias_type: BiasType = Field(..., description="Type of bias detected")
    confidence_level: float = Field(..., ge=0.0, le=1.0, description="Confidence that this bias is present")
    evidence: List[str] = Field(default_factory=list, description="Evidence supporting bias detection")
    manifestation: str = Field(..., description="How the bias manifests in the reasoning")
    impact_assessment: str = Field(..., description="Assessment of the bias's impact on reasoning")
    severity: Literal["low", "medium", "high"] = Field(..., description="Severity of the bias")
    correction_suggestions: List[str] = Field(default_factory=list, description="Suggestions for correcting the bias")
    
    class Config:
        json_encoders = {
            BiasType: lambda v: v.value
        }


class ReasoningMonitor(BaseModel):
    """Monitor for tracking reasoning process"""
    
    monitor_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique monitor identifier")
    monitoring_target: str = Field(..., description="What aspect of reasoning is being monitored")
    monitoring_frequency: Literal["continuous", "periodic", "milestone"] = Field(default="periodic", description="How often monitoring occurs")
    metrics_tracked: List[str] = Field(default_factory=list, description="Specific metrics being tracked")
    thresholds: Dict[str, float] = Field(default_factory=dict, description="Threshold values for triggering interventions")
    current_values: Dict[str, float] = Field(default_factory=dict, description="Current values of tracked metrics")
    alerts_triggered: List[str] = Field(default_factory=list, description="Alerts that have been triggered")
    interventions_suggested: List[str] = Field(default_factory=list, description="Interventions suggested by the monitor")


class ConfidenceAssessment(BaseModel):
    """Assessment of confidence calibration"""
    
    stated_confidence: float = Field(..., ge=0.0, le=1.0, description="Originally stated confidence level")
    calibrated_confidence: float = Field(..., ge=0.0, le=1.0, description="Calibrated confidence level")
    calibration_method: ConfidenceCalibration = Field(..., description="Method used for calibration")
    calibration_factors: List[str] = Field(default_factory=list, description="Factors considered in calibration")
    overconfidence_detected: bool = Field(default=False, description="Whether overconfidence was detected")
    underconfidence_detected: bool = Field(default=False, description="Whether underconfidence was detected")
    confidence_interval: Dict[str, float] = Field(default_factory=dict, description="Confidence interval bounds")
    reliability_score: float = Field(..., ge=0.0, le=1.0, description="Reliability of the confidence assessment")
    
    class Config:
        json_encoders = {
            ConfidenceCalibration: lambda v: v.value
        }


class StrategyEvaluation(BaseModel):
    """Evaluation of reasoning strategy effectiveness"""
    
    strategy_name: str = Field(..., description="Name of the strategy being evaluated")
    strategy_description: str = Field(..., description="Description of the strategy")
    effectiveness_score: float = Field(..., ge=0.0, le=1.0, description="How effective the strategy was")
    efficiency_score: float = Field(..., ge=0.0, le=1.0, description="How efficient the strategy was")
    appropriateness_score: float = Field(..., ge=0.0, le=1.0, description="How appropriate the strategy was for the task")
    strengths: List[str] = Field(default_factory=list, description="Strengths of the strategy")
    weaknesses: List[str] = Field(default_factory=list, description="Weaknesses of the strategy")
    alternative_strategies: List[str] = Field(default_factory=list, description="Alternative strategies that could be considered")
    improvement_suggestions: List[str] = Field(default_factory=list, description="Suggestions for improving the strategy")
    context_suitability: str = Field(..., description="Assessment of how suitable the strategy is for this context")


class MetaLearningInsight(BaseModel):
    """Insight gained from meta-learning process"""
    
    insight_type: Literal["pattern", "strategy", "bias", "performance", "context"] = Field(..., description="Type of insight")
    insight_description: str = Field(..., description="Description of the insight")
    supporting_evidence: List[str] = Field(default_factory=list, description="Evidence supporting this insight")
    generalizability: float = Field(..., ge=0.0, le=1.0, description="How generalizable this insight is")
    actionability: float = Field(..., ge=0.0, le=1.0, description="How actionable this insight is")
    implications: List[str] = Field(default_factory=list, description="Implications of this insight")
    related_insights: List[str] = Field(default_factory=list, description="Related insights or patterns")
    confidence_in_insight: float = Field(..., ge=0.0, le=1.0, description="Confidence in this insight")


class MetacognitiveMonitoringInput(CognitiveInputBase):
    """Input model for Metacognitive Monitoring tool"""
    
    reasoning_target: str = Field(..., description="The reasoning process or decision to monitor")
    monitoring_focus: List[str] = Field(default_factory=list, description="Specific aspects to focus monitoring on")
    bias_detection_enabled: bool = Field(default=True, description="Enable bias detection")
    confidence_calibration_enabled: bool = Field(default=True, description="Enable confidence calibration")
    strategy_evaluation_enabled: bool = Field(default=True, description="Enable strategy evaluation")
    meta_learning_enabled: bool = Field(default=True, description="Enable meta-learning from the process")
    monitoring_depth: Literal["surface", "moderate", "deep"] = Field(default="moderate", description="Depth of monitoring")
    historical_context: Optional[str] = Field(None, description="Historical context for comparison")
    peer_comparison_data: Optional[Dict[str, Any]] = Field(None, description="Data for peer comparison")
    calibration_method: ConfidenceCalibration = Field(default=ConfidenceCalibration.EVIDENCE_BASED, description="Method for calibrating confidence")
    intervention_threshold: float = Field(default=0.7, ge=0.0, le=1.0, description="Threshold for triggering interventions")
    
    class Config:
        json_encoders = {
            ConfidenceCalibration: lambda v: v.value
        }


class MetacognitiveMonitoringOutput(CognitiveOutputBase):
    """Output model for Metacognitive Monitoring tool"""
    
    bias_detections: List[BiasDetection] = Field(default_factory=list, description="Biases detected in the reasoning")
    reasoning_monitors: List[ReasoningMonitor] = Field(default_factory=list, description="Monitors tracking reasoning process")
    confidence_assessment: ConfidenceAssessment = Field(..., description="Assessment of confidence calibration")
    strategy_evaluations: List[StrategyEvaluation] = Field(default_factory=list, description="Evaluations of reasoning strategies")
    meta_learning_insights: List[MetaLearningInsight] = Field(default_factory=list, description="Insights from meta-learning")
    overall_reasoning_quality: float = Field(..., ge=0.0, le=1.0, description="Overall quality of reasoning process")
    metacognitive_awareness_level: float = Field(..., ge=0.0, le=1.0, description="Level of metacognitive awareness demonstrated")
    improvement_recommendations: List[str] = Field(default_factory=list, description="Recommendations for improving reasoning")
    intervention_alerts: List[str] = Field(default_factory=list, description="Alerts for immediate interventions")
    reasoning_patterns_identified: List[str] = Field(default_factory=list, description="Patterns identified in reasoning")
    
    # Additional fields for FastMCP Context integration
    monitoring_duration_seconds: float = Field(default=0.0, ge=0.0, description="Duration of monitoring process")
    monitors_activated: int = Field(..., ge=0, description="Number of monitors that were activated")
    biases_corrected: int = Field(default=0, ge=0, description="Number of biases corrected during process")
    metacognitive_efficiency: float = Field(..., ge=0.0, le=1.0, description="Efficiency of metacognitive process")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
