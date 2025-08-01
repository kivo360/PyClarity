"""
Metacognitive Monitoring Models

Data structures for self-reflection and thinking about thinking, including
reasoning process monitoring, bias detection, confidence calibration, and
strategy evaluation.
"""

from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List, Dict, Any, Optional
from enum import Enum
from datetime import datetime
import uuid


class ComplexityLevel(str, Enum):
    """Problem complexity levels"""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    VERY_COMPLEX = "very_complex"


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


class MonitoringDepth(str, Enum):
    """Depth of metacognitive monitoring"""
    SURFACE = "surface"
    MODERATE = "moderate"
    DEEP = "deep"


class MonitoringFrequency(str, Enum):
    """How often monitoring occurs"""
    CONTINUOUS = "continuous"
    PERIODIC = "periodic"
    MILESTONE = "milestone"


class BiasDetection(BaseModel):
    """Detection of a specific cognitive bias"""
    
    bias_type: BiasType = Field(
        ...,
        description="Type of bias detected"
    )
    
    confidence_level: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence that this bias is present"
    )
    
    evidence: List[str] = Field(
        default_factory=list,
        description="Evidence supporting bias detection",
        max_items=10
    )
    
    manifestation: str = Field(
        ...,
        description="How the bias manifests in the reasoning",
        min_length=20,
        max_length=500
    )
    
    impact_assessment: str = Field(
        ...,
        description="Assessment of the bias's impact on reasoning",
        min_length=20,
        max_length=500
    )
    
    severity: str = Field(
        ...,
        description="Severity of the bias: low, medium, or high"
    )
    
    correction_suggestions: List[str] = Field(
        default_factory=list,
        description="Suggestions for correcting the bias",
        max_items=5
    )
    
    @field_validator('severity')
    @classmethod
    def validate_severity(cls, v):
        """Validate severity is valid value"""
        valid_severities = ["low", "medium", "high"]
        if v not in valid_severities:
            raise ValueError(f"Severity must be one of {valid_severities}")
        return v
    
    @field_validator('evidence', 'correction_suggestions')
    @classmethod
    def validate_string_lists(cls, v):
        """Validate string lists are non-empty when provided"""
        if v:
            cleaned = [item.strip() for item in v if item.strip()]
            return cleaned
        return v


class ReasoningMonitor(BaseModel):
    """Monitor for tracking reasoning process"""
    
    monitor_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique monitor identifier"
    )
    
    monitoring_target: str = Field(
        ...,
        description="What aspect of reasoning is being monitored",
        min_length=10,
        max_length=200
    )
    
    monitoring_frequency: MonitoringFrequency = Field(
        MonitoringFrequency.PERIODIC,
        description="How often monitoring occurs"
    )
    
    metrics_tracked: List[str] = Field(
        default_factory=list,
        description="Specific metrics being tracked",
        max_items=10
    )
    
    thresholds: Dict[str, float] = Field(
        default_factory=dict,
        description="Threshold values for triggering interventions"
    )
    
    current_values: Dict[str, float] = Field(
        default_factory=dict,
        description="Current values of tracked metrics"
    )
    
    alerts_triggered: List[str] = Field(
        default_factory=list,
        description="Alerts that have been triggered",
        max_items=20
    )
    
    interventions_suggested: List[str] = Field(
        default_factory=list,
        description="Interventions suggested by the monitor",
        max_items=10
    )
    
    @field_validator('metrics_tracked', 'alerts_triggered', 'interventions_suggested')
    @classmethod
    def validate_string_lists(cls, v):
        """Validate string lists are non-empty when provided"""
        if v:
            cleaned = [item.strip() for item in v if item.strip()]
            return cleaned
        return v


class ConfidenceAssessment(BaseModel):
    """Assessment of confidence calibration"""
    
    stated_confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Originally stated confidence level"
    )
    
    calibrated_confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Calibrated confidence level"
    )
    
    calibration_method: ConfidenceCalibration = Field(
        ...,
        description="Method used for calibration"
    )
    
    calibration_factors: List[str] = Field(
        default_factory=list,
        description="Factors considered in calibration",
        max_items=8
    )
    
    overconfidence_detected: bool = Field(
        False,
        description="Whether overconfidence was detected"
    )
    
    underconfidence_detected: bool = Field(
        False,
        description="Whether underconfidence was detected"
    )
    
    confidence_interval: Dict[str, float] = Field(
        default_factory=dict,
        description="Confidence interval bounds (lower and upper)"
    )
    
    reliability_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Reliability of the confidence assessment"
    )
    
    @model_validator(mode='after')
    def validate_confidence_consistency(self):
        """Validate confidence values are consistent"""
        # Set over/under confidence flags based on calibration
        confidence_diff = self.calibrated_confidence - self.stated_confidence
        
        if confidence_diff < -0.15:  # Stated confidence higher than calibrated
            self.overconfidence_detected = True
            self.underconfidence_detected = False
        elif confidence_diff > 0.15:  # Stated confidence lower than calibrated
            self.underconfidence_detected = True
            self.overconfidence_detected = False
        else:
            self.overconfidence_detected = False
            self.underconfidence_detected = False
        
        # Ensure confidence interval makes sense
        if self.confidence_interval:
            if 'lower' in self.confidence_interval and 'upper' in self.confidence_interval:
                if self.confidence_interval['lower'] > self.confidence_interval['upper']:
                    raise ValueError("Lower confidence bound cannot be greater than upper bound")
        
        return self


class StrategyEvaluation(BaseModel):
    """Evaluation of reasoning strategy effectiveness"""
    
    strategy_name: str = Field(
        ...,
        description="Name of the strategy being evaluated",
        min_length=5,
        max_length=100
    )
    
    strategy_description: str = Field(
        ...,
        description="Description of the strategy",
        min_length=20,
        max_length=500
    )
    
    effectiveness_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="How effective the strategy was"
    )
    
    efficiency_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="How efficient the strategy was"
    )
    
    appropriateness_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="How appropriate the strategy was for the task"
    )
    
    strengths: List[str] = Field(
        default_factory=list,
        description="Strengths of the strategy",
        max_items=8
    )
    
    weaknesses: List[str] = Field(
        default_factory=list,
        description="Weaknesses of the strategy",
        max_items=8
    )
    
    alternative_strategies: List[str] = Field(
        default_factory=list,
        description="Alternative strategies that could be considered",
        max_items=5
    )
    
    improvement_suggestions: List[str] = Field(
        default_factory=list,
        description="Suggestions for improving the strategy",
        max_items=8
    )
    
    context_suitability: str = Field(
        ...,
        description="Assessment of how suitable the strategy is for this context",
        min_length=20,
        max_length=300
    )
    
    @field_validator('strengths', 'weaknesses', 'alternative_strategies', 'improvement_suggestions')
    @classmethod
    def validate_string_lists(cls, v):
        """Validate string lists are non-empty when provided"""
        if v:
            cleaned = [item.strip() for item in v if item.strip()]
            return cleaned
        return v


class MetaLearningInsight(BaseModel):
    """Insight gained from meta-learning process"""
    
    insight_type: str = Field(
        ...,
        description="Type of insight: pattern, strategy, bias, performance, or context"
    )
    
    insight_description: str = Field(
        ...,
        description="Description of the insight",
        min_length=50,
        max_length=1000
    )
    
    supporting_evidence: List[str] = Field(
        default_factory=list,
        description="Evidence supporting this insight",
        max_items=10
    )
    
    generalizability: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="How generalizable this insight is"
    )
    
    actionability: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="How actionable this insight is"
    )
    
    implications: List[str] = Field(
        default_factory=list,
        description="Implications of this insight",
        max_items=8
    )
    
    related_insights: List[str] = Field(
        default_factory=list,
        description="Related insights or patterns",
        max_items=5
    )
    
    confidence_in_insight: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence in this insight"
    )
    
    @field_validator('insight_type')
    @classmethod
    def validate_insight_type(cls, v):
        """Validate insight type is valid"""
        valid_types = ["pattern", "strategy", "bias", "performance", "context"]
        if v not in valid_types:
            raise ValueError(f"Insight type must be one of {valid_types}")
        return v
    
    @field_validator('supporting_evidence', 'implications', 'related_insights')
    @classmethod
    def validate_string_lists(cls, v):
        """Validate string lists are non-empty when provided"""
        if v:
            cleaned = [item.strip() for item in v if item.strip()]
            return cleaned
        return v


class MetacognitiveMonitoringContext(BaseModel):
    """Context for metacognitive monitoring analysis"""
    
    reasoning_target: str = Field(
        ...,
        description="The reasoning process or decision to monitor",
        min_length=10,
        max_length=2000
    )
    
    complexity_level: ComplexityLevel = Field(
        ComplexityLevel.MODERATE,
        description="Complexity level of the reasoning task"
    )
    
    monitoring_focus: List[str] = Field(
        default_factory=list,
        description="Specific aspects to focus monitoring on",
        max_items=8
    )
    
    bias_detection_enabled: bool = Field(
        True,
        description="Enable bias detection"
    )
    
    confidence_calibration_enabled: bool = Field(
        True,
        description="Enable confidence calibration"
    )
    
    strategy_evaluation_enabled: bool = Field(
        True,
        description="Enable strategy evaluation"
    )
    
    meta_learning_enabled: bool = Field(
        True,
        description="Enable meta-learning from the process"
    )
    
    monitoring_depth: MonitoringDepth = Field(
        MonitoringDepth.MODERATE,
        description="Depth of monitoring"
    )
    
    historical_context: Optional[str] = Field(
        None,
        description="Historical context for comparison",
        max_length=1000
    )
    
    peer_comparison_data: Optional[Dict[str, Any]] = Field(
        None,
        description="Data for peer comparison"
    )
    
    calibration_method: ConfidenceCalibration = Field(
        ConfidenceCalibration.EVIDENCE_BASED,
        description="Method for calibrating confidence"
    )
    
    intervention_threshold: float = Field(
        0.7,
        ge=0.0,
        le=1.0,
        description="Threshold for triggering interventions"
    )
    
    @field_validator('reasoning_target')
    @classmethod
    def validate_reasoning_target(cls, v):
        """Validate reasoning target is meaningful"""
        if not v or v.strip() == "":
            raise ValueError("Reasoning target cannot be empty")
        return v.strip()
    
    @field_validator('monitoring_focus')
    @classmethod
    def validate_monitoring_focus(cls, v):
        """Validate monitoring focus list"""
        if v:
            cleaned = [item.strip() for item in v if item.strip()]
            return cleaned
        return v


class MetacognitiveMonitoringResult(BaseModel):
    """Result of metacognitive monitoring analysis"""
    
    bias_detections: List[BiasDetection] = Field(
        default_factory=list,
        description="Biases detected in the reasoning",
        max_items=10
    )
    
    reasoning_monitors: List[ReasoningMonitor] = Field(
        default_factory=list,
        description="Monitors tracking reasoning process",
        max_items=10
    )
    
    confidence_assessment: ConfidenceAssessment = Field(
        ...,
        description="Assessment of confidence calibration"
    )
    
    strategy_evaluations: List[StrategyEvaluation] = Field(
        default_factory=list,
        description="Evaluations of reasoning strategies",
        max_items=8
    )
    
    meta_learning_insights: List[MetaLearningInsight] = Field(
        default_factory=list,
        description="Insights from meta-learning",
        max_items=10
    )
    
    overall_reasoning_quality: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Overall quality of reasoning process"
    )
    
    metacognitive_awareness_level: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Level of metacognitive awareness demonstrated"
    )
    
    improvement_recommendations: List[str] = Field(
        default_factory=list,
        description="Recommendations for improving reasoning",
        max_items=10
    )
    
    intervention_alerts: List[str] = Field(
        default_factory=list,
        description="Alerts for immediate interventions",
        max_items=5
    )
    
    reasoning_patterns_identified: List[str] = Field(
        default_factory=list,
        description="Patterns identified in reasoning",
        max_items=8
    )
    
    monitoring_duration_seconds: float = Field(
        0.0,
        ge=0.0,
        description="Duration of monitoring process"
    )
    
    monitors_activated: int = Field(
        0,
        ge=0,
        description="Number of monitors that were activated"
    )
    
    biases_corrected: int = Field(
        0,
        ge=0,
        description="Number of biases corrected during process"
    )
    
    metacognitive_efficiency: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Efficiency of metacognitive process"
    )
    
    processing_time_ms: int = Field(
        0,
        description="Time taken to process in milliseconds"
    )
    
    @field_validator('improvement_recommendations', 'intervention_alerts', 'reasoning_patterns_identified')
    @classmethod
    def validate_string_lists(cls, v):
        """Validate string lists are non-empty when provided"""
        if v:
            cleaned = [item.strip() for item in v if item.strip()]
            return cleaned
        return v
    
    @model_validator(mode='after')
    def validate_consistency(self):
        """Validate consistency across fields"""
        # Update monitors_activated count
        self.monitors_activated = len(self.reasoning_monitors)
        
        # Count corrected biases
        corrected_count = sum(1 for bias in self.bias_detections 
                            if any("corrected" in s.lower() or "addressed" in s.lower() 
                                 for s in bias.correction_suggestions))
        self.biases_corrected = corrected_count
        
        return self
    
    def get_most_severe_biases(self, n: int = 3) -> List[BiasDetection]:
        """Get N most severe biases detected"""
        severe_biases = sorted(
            self.bias_detections,
            key=lambda x: (x.severity == "high", x.severity == "medium", x.confidence_level),
            reverse=True
        )
        return severe_biases[:n]
    
    def get_high_impact_insights(self, threshold: float = 0.7) -> List[MetaLearningInsight]:
        """Get insights with high impact (actionability * generalizability)"""
        return [
            insight for insight in self.meta_learning_insights
            if (insight.actionability * insight.generalizability) >= threshold
        ]
    
    def needs_intervention(self) -> bool:
        """Check if immediate intervention is needed"""
        return len(self.intervention_alerts) > 0 or any(
            bias.severity == "high" for bias in self.bias_detections
        )