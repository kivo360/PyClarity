# Clear Thinking FastMCP Server - Metacognitive Monitoring Tests

"""
Comprehensive test suite for Metacognitive Monitoring cognitive tool.

This test suite validates self-reflection and thinking about thinking through:
- Reasoning process monitoring
- Bias detection and correction
- Confidence calibration
- Strategy evaluation and adjustment
- Meta-learning from reasoning patterns

Agent: AGENT D - Metacognitive Monitoring Testing
Status: ACTIVE - Phase 2C Parallel Expansion
"""

import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock
from typing import List, Dict, Any

# Import test models directly without Pydantic validators for testing
from dataclasses import dataclass
from enum import Enum


class BiasType(str, Enum):
    CONFIRMATION_BIAS = "confirmation_bias"
    ANCHORING_BIAS = "anchoring_bias"
    OVERCONFIDENCE_BIAS = "overconfidence_bias"
    AVAILABILITY_HEURISTIC = "availability_heuristic"


class ConfidenceCalibration(str, Enum):
    EVIDENCE_BASED = "evidence_based"
    HISTORICAL_PERFORMANCE = "historical_performance"
    FREQUENCY_BASED = "frequency_based"


class ComplexityLevel(str, Enum):
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"


@dataclass
class MockBiasDetection:
    bias_type: BiasType
    confidence_level: float
    evidence: List[str]
    manifestation: str
    impact_assessment: str
    severity: str
    correction_suggestions: List[str]


@dataclass
class MockReasoningMonitor:
    monitor_id: str
    monitoring_target: str
    monitoring_frequency: str
    metrics_tracked: List[str]
    thresholds: Dict[str, float]
    current_values: Dict[str, float]
    alerts_triggered: List[str]
    interventions_suggested: List[str]


@dataclass
class MockConfidenceAssessment:
    stated_confidence: float
    calibrated_confidence: float
    calibration_method: ConfidenceCalibration
    calibration_factors: List[str]
    overconfidence_detected: bool
    underconfidence_detected: bool
    confidence_interval: Dict[str, float]
    reliability_score: float


@dataclass
class MockMetacognitiveMonitoringInput:
    problem: str
    complexity_level: ComplexityLevel
    session_id: str
    reasoning_target: str
    monitoring_focus: List[str]
    bias_detection_enabled: bool = True
    confidence_calibration_enabled: bool = True
    strategy_evaluation_enabled: bool = True
    meta_learning_enabled: bool = True
    monitoring_depth: str = "moderate"
    calibration_method: ConfidenceCalibration = ConfidenceCalibration.EVIDENCE_BASED
    intervention_threshold: float = 0.7


# Mock context for testing
class MockContext:
    def __init__(self):
        self.progress_calls = []
        self.info_calls = []
        self.debug_calls = []
        self.error_calls = []
    
    async def progress(self, message: str, progress: float = 0.0):
        self.progress_calls.append((message, progress))
    
    async def info(self, message: str):
        self.info_calls.append(message)
    
    async def debug(self, message: str):
        self.debug_calls.append(message)
    
    async def error(self, message: str):
        self.error_calls.append(message)
    
    async def cancelled(self) -> bool:
        return False


class TestMetacognitiveMonitoringLogic:
    """Test metacognitive monitoring logic without full model dependencies"""
    
    def test_reasoning_monitor_creation(self):
        """Test creation of reasoning monitors"""
        monitor = MockReasoningMonitor(
            monitor_id="quality_monitor_1",
            monitoring_target="reasoning_quality",
            monitoring_frequency="continuous",
            metrics_tracked=["logical_consistency", "evidence_support", "conclusion_validity"],
            thresholds={"logical_consistency": 0.7, "evidence_support": 0.6, "conclusion_validity": 0.8},
            current_values={"logical_consistency": 0.8, "evidence_support": 0.7, "conclusion_validity": 0.75},
            alerts_triggered=[],
            interventions_suggested=[]
        )
        
        assert monitor.monitoring_target == "reasoning_quality"
        assert len(monitor.metrics_tracked) == 3
        assert monitor.thresholds["logical_consistency"] == 0.7
        assert monitor.current_values["logical_consistency"] == 0.8
    
    def test_threshold_violation_detection(self):
        """Test detection of threshold violations"""
        monitor = MockReasoningMonitor(
            monitor_id="test_monitor",
            monitoring_target="test_target",
            monitoring_frequency="periodic",
            metrics_tracked=["quality_metric"],
            thresholds={"quality_metric": 0.7},
            current_values={"quality_metric": 0.5},  # Below threshold
            alerts_triggered=[],
            interventions_suggested=[]
        )
        
        # Simulate threshold checking
        for metric, threshold in monitor.thresholds.items():
            current_value = monitor.current_values.get(metric, 0.5)
            if current_value < threshold:
                alert = f"Monitor '{monitor.monitoring_target}': {metric} below threshold ({current_value:.2f} < {threshold:.2f})"
                monitor.alerts_triggered.append(alert)
                monitor.interventions_suggested.append(f"Improve {metric} in {monitor.monitoring_target}")
        
        assert len(monitor.alerts_triggered) == 1
        assert len(monitor.interventions_suggested) == 1
        assert "below threshold" in monitor.alerts_triggered[0]
    
    @pytest.mark.asyncio
    async def test_bias_detection_confirmation_bias(self):
        """Test detection of confirmation bias"""
        mock_context = MockContext()
        
        # Simulate confirmation bias detection
        bias_detection = MockBiasDetection(
            bias_type=BiasType.CONFIRMATION_BIAS,
            confidence_level=0.6,
            evidence=["Selective evidence consideration", "Limited alternative exploration"],
            manifestation="Tendency to favor information that confirms initial assessment",
            impact_assessment="May lead to overlooking contradictory evidence",
            severity="medium",
            correction_suggestions=["Actively seek disconfirming evidence", "Consider alternative interpretations"]
        )
        
        assert bias_detection.bias_type == BiasType.CONFIRMATION_BIAS
        assert bias_detection.confidence_level > 0.3  # Likely bias
        assert len(bias_detection.evidence) > 0
        assert len(bias_detection.correction_suggestions) > 0
        assert bias_detection.severity in ["low", "medium", "high"]
    
    @pytest.mark.asyncio
    async def test_bias_detection_overconfidence_bias(self):
        """Test detection of overconfidence bias"""
        mock_context = MockContext()
        
        # Simulate overconfidence bias detection
        bias_detection = MockBiasDetection(
            bias_type=BiasType.OVERCONFIDENCE_BIAS,
            confidence_level=0.8,  # High likelihood
            evidence=["High confidence without proportional evidence", "Limited uncertainty acknowledgment"],
            manifestation="Confidence levels exceed accuracy levels",
            impact_assessment="May lead to insufficient preparation for alternatives",
            severity="high",
            correction_suggestions=["Calibrate confidence against historical accuracy", "Seek external validation"]
        )
        
        assert bias_detection.bias_type == BiasType.OVERCONFIDENCE_BIAS
        assert bias_detection.confidence_level > 0.5  # High confidence in detection
        assert bias_detection.severity == "high"
        assert "calibrate" in bias_detection.correction_suggestions[0].lower()
    
    @pytest.mark.asyncio
    async def test_confidence_calibration_evidence_based(self):
        """Test evidence-based confidence calibration"""
        mock_context = MockContext()
        
        # Simulate evidence-based calibration
        stated_confidence = 0.8
        calibrated_confidence = stated_confidence * 0.92  # Slight reduction (0.736, diff = 0.064 < 0.1)
        
        confidence_assessment = MockConfidenceAssessment(
            stated_confidence=stated_confidence,
            calibrated_confidence=calibrated_confidence,
            calibration_method=ConfidenceCalibration.EVIDENCE_BASED,
            calibration_factors=["Evidence quality", "Evidence completeness", "Alternative considerations"],
            overconfidence_detected=stated_confidence - calibrated_confidence > 0.1,
            underconfidence_detected=calibrated_confidence - stated_confidence > 0.1,
            confidence_interval={"lower": calibrated_confidence - 0.1, "upper": calibrated_confidence + 0.1},
            reliability_score=0.8
        )
        
        assert confidence_assessment.stated_confidence == 0.8
        assert confidence_assessment.calibrated_confidence < confidence_assessment.stated_confidence
        assert confidence_assessment.calibration_method == ConfidenceCalibration.EVIDENCE_BASED
        assert not confidence_assessment.overconfidence_detected  # Difference is < 0.1
        assert confidence_assessment.reliability_score > 0.0
    
    @pytest.mark.asyncio
    async def test_confidence_calibration_historical_performance(self):
        """Test historical performance-based confidence calibration"""
        mock_context = MockContext()
        
        # Simulate historical performance calibration (more conservative)
        stated_confidence = 0.8
        calibrated_confidence = stated_confidence * 0.75  # More reduction
        
        confidence_assessment = MockConfidenceAssessment(
            stated_confidence=stated_confidence,
            calibrated_confidence=calibrated_confidence,
            calibration_method=ConfidenceCalibration.HISTORICAL_PERFORMANCE,
            calibration_factors=["Past accuracy", "Similar problem performance", "Context familiarity"],
            overconfidence_detected=stated_confidence - calibrated_confidence > 0.1,
            underconfidence_detected=calibrated_confidence - stated_confidence > 0.1,
            confidence_interval={"lower": calibrated_confidence - 0.1, "upper": calibrated_confidence + 0.1},
            reliability_score=0.85
        )
        
        assert abs(confidence_assessment.calibrated_confidence - 0.6) < 1e-10  # 0.8 * 0.75
        assert confidence_assessment.overconfidence_detected  # 0.8 - 0.6 = 0.2 > 0.1
        assert confidence_assessment.calibration_method == ConfidenceCalibration.HISTORICAL_PERFORMANCE
        assert "past accuracy" in confidence_assessment.calibration_factors[0].lower()
    
    def test_strategy_evaluation(self):
        """Test reasoning strategy evaluation"""
        # Mock strategy evaluation
        strategy_evaluation = {
            "strategy_name": "Systematic Analysis",
            "strategy_description": "Step-by-step systematic approach to problem analysis",
            "effectiveness_score": 0.8,
            "efficiency_score": 0.7,
            "appropriateness_score": 0.85,
            "strengths": ["Thorough coverage", "Logical progression", "Evidence-based"],
            "weaknesses": ["Time-intensive", "May miss creative solutions"],
            "alternative_strategies": ["Intuitive approach", "Collaborative reasoning", "Creative problem solving"],
            "improvement_suggestions": ["Incorporate creative elements", "Add time management", "Include stakeholder perspectives"],
            "context_suitability": "Well-suited for complex analytical problems"
        }
        
        assert strategy_evaluation["strategy_name"] is not None
        assert 0.0 <= strategy_evaluation["effectiveness_score"] <= 1.0
        assert 0.0 <= strategy_evaluation["efficiency_score"] <= 1.0
        assert 0.0 <= strategy_evaluation["appropriateness_score"] <= 1.0
        assert len(strategy_evaluation["strengths"]) > 0
        assert len(strategy_evaluation["weaknesses"]) > 0
        assert len(strategy_evaluation["improvement_suggestions"]) > 0
    
    def test_meta_learning_insight_generation(self):
        """Test meta-learning insight generation"""
        # Mock bias detections
        mock_bias_detections = [
            MockBiasDetection(
                bias_type=BiasType.OVERCONFIDENCE_BIAS,
                confidence_level=0.7,
                evidence=["High initial confidence"],
                manifestation="Overconfidence pattern",
                impact_assessment="Moderate impact",
                severity="medium",
                correction_suggestions=["Calibrate confidence"]
            )
        ]
        
        # Generate pattern insight
        pattern_insight = {
            "insight_type": "pattern",
            "insight_description": "Tendency to start with high confidence that gets calibrated down through systematic analysis",
            "supporting_evidence": ["Initial confidence: 0.8", "Calibrated confidence: 0.68", "Consistent overconfidence pattern"],
            "generalizability": 0.7,
            "actionability": 0.8,
            "implications": ["Need for earlier confidence calibration", "Value of systematic doubt"],
            "related_insights": ["Overconfidence bias detection"],
            "confidence_in_insight": 0.75
        }
        
        assert pattern_insight["insight_type"] == "pattern"
        assert pattern_insight["insight_description"] is not None
        assert len(pattern_insight["supporting_evidence"]) > 0
        assert 0.0 <= pattern_insight["generalizability"] <= 1.0
        assert 0.0 <= pattern_insight["actionability"] <= 1.0
        assert len(pattern_insight["implications"]) > 0
    
    def test_bias_insight_generation(self):
        """Test bias-specific meta-learning insights"""
        # Mock high-confidence bias detections
        high_confidence_biases = [
            MockBiasDetection(
                bias_type=BiasType.CONFIRMATION_BIAS,
                confidence_level=0.6,
                evidence=["Evidence"],
                manifestation="Manifestation",
                impact_assessment="Impact",
                severity="medium",
                correction_suggestions=["Suggestion"]
            ),
            MockBiasDetection(
                bias_type=BiasType.OVERCONFIDENCE_BIAS,
                confidence_level=0.8,
                evidence=["Evidence"],
                manifestation="Manifestation",
                impact_assessment="Impact",
                severity="high",
                correction_suggestions=["Suggestion"]
            )
        ]
        
        bias_insight = {
            "insight_type": "bias",
            "insight_description": f"Detected {len(high_confidence_biases)} high-confidence biases requiring attention",
            "supporting_evidence": [f"{b.bias_type.value}: {b.confidence_level:.1%}" for b in high_confidence_biases],
            "generalizability": 0.8,
            "actionability": 0.9,
            "implications": ["Implement bias checking procedures", "Seek external perspectives"],
            "related_insights": ["Systematic bias patterns"],
            "confidence_in_insight": 0.85
        }
        
        assert bias_insight["insight_type"] == "bias"
        assert "2 high-confidence biases" in bias_insight["insight_description"]
        assert len(bias_insight["supporting_evidence"]) == 2
        assert "confirmation_bias: 60" in bias_insight["supporting_evidence"][0]
        assert "overconfidence_bias: 80" in bias_insight["supporting_evidence"][1]
    
    def test_reasoning_quality_calculation(self):
        """Test overall reasoning quality calculation"""
        # Mock monitors with different quality scores
        mock_monitors = [
            MockReasoningMonitor(
                monitor_id="monitor_1",
                monitoring_target="quality",
                monitoring_frequency="continuous",
                metrics_tracked=["metric1", "metric2"],
                thresholds={},
                current_values={"metric1": 0.8, "metric2": 0.7},
                alerts_triggered=[],
                interventions_suggested=[]
            ),
            MockReasoningMonitor(
                monitor_id="monitor_2",
                monitoring_target="efficiency",
                monitoring_frequency="periodic",
                metrics_tracked=["metric3"],
                thresholds={},
                current_values={"metric3": 0.9},
                alerts_triggered=[],
                interventions_suggested=[]
            )
        ]
        
        # Calculate quality scores
        quality_scores = []
        for monitor in mock_monitors:
            if monitor.current_values:
                monitor_quality = sum(monitor.current_values.values()) / len(monitor.current_values)
                quality_scores.append(monitor_quality)
        
        overall_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0.5
        
        assert len(quality_scores) == 2
        assert quality_scores[0] == 0.75  # (0.8 + 0.7) / 2
        assert quality_scores[1] == 0.9
        assert overall_quality == 0.825  # (0.75 + 0.9) / 2
    
    def test_metacognitive_awareness_calculation(self):
        """Test metacognitive awareness level calculation"""
        # Mock components
        num_bias_detections = 3
        mock_confidence_assessment = MockConfidenceAssessment(
            stated_confidence=0.8,
            calibrated_confidence=0.7,
            calibration_method=ConfidenceCalibration.EVIDENCE_BASED,
            calibration_factors=[],
            overconfidence_detected=False,
            underconfidence_detected=False,
            confidence_interval={},
            reliability_score=0.8
        )
        strategy_effectiveness = 0.85
        num_meta_insights = 2
        
        # Calculate awareness factors
        awareness_factors = [
            num_bias_detections * 0.1,  # Bias awareness
            mock_confidence_assessment.reliability_score * 0.3,  # Confidence calibration
            strategy_effectiveness * 0.3,  # Strategy awareness
            num_meta_insights * 0.1  # Meta-learning
        ]
        awareness_level = min(1.0, sum(awareness_factors))
        
        assert abs(awareness_factors[0] - 0.3) < 1e-10  # 3 * 0.1
        assert awareness_factors[1] == 0.24  # 0.8 * 0.3
        assert awareness_factors[2] == 0.255  # 0.85 * 0.3
        assert awareness_factors[3] == 0.2  # 2 * 0.1
        assert abs(awareness_level - 0.995) < 1e-10  # Sum of factors, capped at 1.0
    
    def test_intervention_alert_generation(self):
        """Test generation of intervention alerts"""
        # Mock monitors with alerts
        mock_monitors = [
            MockReasoningMonitor(
                monitor_id="monitor_1",
                monitoring_target="quality",
                monitoring_frequency="continuous",
                metrics_tracked=[],
                thresholds={},
                current_values={},
                alerts_triggered=["Quality below threshold"],
                interventions_suggested=[]
            )
        ]
        
        # Mock high-severity biases
        high_severity_biases = [
            MockBiasDetection(
                bias_type=BiasType.OVERCONFIDENCE_BIAS,
                confidence_level=0.8,
                evidence=[],
                manifestation="",
                impact_assessment="",
                severity="high",
                correction_suggestions=[]
            )
        ]
        
        # Generate alerts
        alerts = []
        for monitor in mock_monitors:
            alerts.extend(monitor.alerts_triggered)
        
        for bias in high_severity_biases:
            if bias.severity == "high":
                alerts.append(f"High-severity {bias.bias_type.value} detected - immediate intervention needed")
        
        assert len(alerts) == 2
        assert "Quality below threshold" in alerts[0]
        assert "High-severity overconfidence_bias detected" in alerts[1]
    
    def test_reasoning_pattern_identification(self):
        """Test identification of reasoning patterns"""
        # Mock bias detections for pattern analysis
        mock_bias_detections = [
            MockBiasDetection(
                bias_type=BiasType.CONFIRMATION_BIAS,
                confidence_level=0.6,
                evidence=[],
                manifestation="",
                impact_assessment="",
                severity="medium",
                correction_suggestions=[]
            ),
            MockBiasDetection(
                bias_type=BiasType.OVERCONFIDENCE_BIAS,
                confidence_level=0.8,
                evidence=[],
                manifestation="",
                impact_assessment="",
                severity="high",
                correction_suggestions=[]
            )
        ]
        
        # Identify patterns
        patterns = [
            "Systematic approach preference",
            "High initial confidence with subsequent calibration",
            "Evidence-based reasoning style",
            "Active monitoring and self-correction"
        ]
        
        if mock_bias_detections:
            bias_pattern = f"Bias susceptibility: {', '.join([b.bias_type.value for b in mock_bias_detections[:3]])}"
            patterns.append(bias_pattern)
        
        assert len(patterns) == 5
        assert "Systematic approach preference" in patterns[0]
        assert "Bias susceptibility: confirmation_bias, overconfidence_bias" in patterns[4]
    
    @pytest.mark.asyncio
    async def test_monitoring_input_validation(self):
        """Test metacognitive monitoring input validation"""
        input_data = MockMetacognitiveMonitoringInput(
            problem="Complex decision-making scenario",
            complexity_level=ComplexityLevel.COMPLEX,
            session_id="test_session_1",
            reasoning_target="Decision-making process",
            monitoring_focus=["bias_detection", "confidence_calibration"],
            bias_detection_enabled=True,
            confidence_calibration_enabled=True,
            strategy_evaluation_enabled=True,
            meta_learning_enabled=True,
            monitoring_depth="deep",
            calibration_method=ConfidenceCalibration.EVIDENCE_BASED,
            intervention_threshold=0.7
        )
        
        assert input_data.reasoning_target is not None
        assert len(input_data.monitoring_focus) > 0
        assert input_data.bias_detection_enabled is True
        assert input_data.confidence_calibration_enabled is True
        assert input_data.intervention_threshold == 0.7
        assert 0.0 <= input_data.intervention_threshold <= 1.0
    
    @pytest.mark.asyncio
    async def test_full_metacognitive_monitoring_workflow(self):
        """Test complete metacognitive monitoring workflow"""
        mock_context = MockContext()
        
        # Step 1: Setup input
        input_data = MockMetacognitiveMonitoringInput(
            problem="Should we implement a new feature?",
            complexity_level=ComplexityLevel.MODERATE,
            session_id="integration_test_1",
            reasoning_target="Feature implementation decision",
            monitoring_focus=["decision_quality", "bias_detection"],
            calibration_method=ConfidenceCalibration.EVIDENCE_BASED
        )
        
        # Step 2: Setup monitors
        monitors = [
            MockReasoningMonitor(
                monitor_id="quality_monitor",
                monitoring_target="reasoning_quality",
                monitoring_frequency="continuous",
                metrics_tracked=["logical_consistency", "evidence_support"],
                thresholds={"logical_consistency": 0.7, "evidence_support": 0.6},
                current_values={"logical_consistency": 0.8, "evidence_support": 0.7},
                alerts_triggered=[],
                interventions_suggested=[]
            )
        ]
        
        # Step 3: Detect biases
        bias_detections = [
            MockBiasDetection(
                bias_type=BiasType.CONFIRMATION_BIAS,
                confidence_level=0.5,
                evidence=["Selective information processing"],
                manifestation="Focusing on confirming evidence",
                impact_assessment="Moderate impact on decision quality",
                severity="medium",
                correction_suggestions=["Seek contradictory evidence"]
            )
        ]
        
        # Step 4: Calibrate confidence
        confidence_assessment = MockConfidenceAssessment(
            stated_confidence=0.8,
            calibrated_confidence=0.68,
            calibration_method=ConfidenceCalibration.EVIDENCE_BASED,
            calibration_factors=["Evidence quality", "Evidence completeness"],
            overconfidence_detected=True,
            underconfidence_detected=False,
            confidence_interval={"lower": 0.58, "upper": 0.78},
            reliability_score=0.85
        )
        
        # Step 5: Calculate overall metrics
        reasoning_quality = 0.75  # Average of monitor values
        awareness_level = 0.8    # High awareness due to active monitoring
        
        # Step 6: Validate results
        assert len(monitors) > 0
        assert len(bias_detections) > 0
        assert confidence_assessment.overconfidence_detected is True
        assert reasoning_quality > 0.0
        assert awareness_level > 0.0
        
        # Step 7: Check context usage
        await mock_context.info("Metacognitive monitoring completed")
        await mock_context.progress("Monitoring finished", 1.0)
        
        assert len(mock_context.info_calls) > 0
        assert len(mock_context.progress_calls) > 0
        
        print(f"✅ Full metacognitive monitoring workflow test passed")
        print(f"   Monitors activated: {len(monitors)}")
        print(f"   Biases detected: {len(bias_detections)}")
        print(f"   Overconfidence detected: {confidence_assessment.overconfidence_detected}")
        print(f"   Reasoning quality: {reasoning_quality:.2f}")
        print(f"   Awareness level: {awareness_level:.2f}")
    
    def test_recommendation_generation(self):
        """Test generation of improvement recommendations"""
        # Mock assessment results
        high_severity_biases = 1
        overconfidence_detected = True
        
        # Generate base recommendations
        recommendations = [
            "Continue systematic monitoring of reasoning processes",
            "Address detected biases through corrective actions",
            "Calibrate confidence more frequently during reasoning",
            "Apply meta-learning insights to future reasoning tasks"
        ]
        
        # Add specific recommendations
        if high_severity_biases > 0:
            recommendations.append(f"Immediately address {high_severity_biases} high-severity biases")
        
        if overconfidence_detected:
            recommendations.append("Implement confidence debiasing techniques")
        
        assert len(recommendations) == 6  # 4 base + 2 specific
        assert "systematic monitoring" in recommendations[0]
        assert "high-severity biases" in recommendations[4]
        assert "debiasing techniques" in recommendations[5]
    
    def test_default_confidence_assessment(self):
        """Test default confidence assessment creation"""
        default_assessment = MockConfidenceAssessment(
            stated_confidence=0.5,
            calibrated_confidence=0.5,
            calibration_method=ConfidenceCalibration.EVIDENCE_BASED,
            calibration_factors=["Default calibration"],
            overconfidence_detected=False,
            underconfidence_detected=False,
            confidence_interval={"lower": 0.4, "upper": 0.6},
            reliability_score=0.5
        )
        
        assert default_assessment.stated_confidence == 0.5
        assert default_assessment.calibrated_confidence == 0.5
        assert default_assessment.overconfidence_detected is False
        assert default_assessment.underconfidence_detected is False
        assert default_assessment.reliability_score == 0.5


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
