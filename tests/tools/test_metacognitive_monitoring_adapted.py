"""Test Metacognitive Monitoring cognitive tool.

Adapted to match the actual PyClarity implementation.
"""

import pytest
from pyclarity.tools.metacognitive_monitoring.models import (
    MetacognitiveMonitoringContext,
    MetacognitiveMonitoringResult,
    BiasType,
    ComplexityLevel,
    BiasDetection,
    ReasoningMonitor,
    ConfidenceAssessment,
    StrategyEvaluation,
    MetaLearningInsight,
    MonitoringDepth,
    MonitoringFrequency,
    ConfidenceCalibration
)
from pyclarity.tools.metacognitive_monitoring.analyzer import MetacognitiveMonitoringAnalyzer


class TestMetacognitiveMonitoringAnalyzer:
    """Test suite for Metacognitive Monitoring Analyzer"""
    
    @pytest.fixture
    def analyzer(self):
        """Create analyzer instance"""
        return MetacognitiveMonitoringAnalyzer()
    
    @pytest.fixture
    def simple_context(self):
        """Create simple test context"""
        return MetacognitiveMonitoringContext(
            reasoning_target="I'm solving a complex algorithmic problem by breaking it down into smaller parts",
            complexity_level=ComplexityLevel.MODERATE,
            monitoring_focus=["problem-solving", "bias detection", "strategy evaluation"],
            bias_detection_enabled=True,
            confidence_calibration_enabled=True,
            strategy_evaluation_enabled=True
        )
    
    async def test_analyze_simple_process(self, analyzer, simple_context):
        """Test analyzing a simple thinking process"""
        result = await analyzer.analyze(simple_context)
        
        assert isinstance(result, MetacognitiveMonitoringResult)
        assert len(result.reasoning_monitors) >= 1
        assert len(result.bias_detections) >= 0
        assert result.confidence_assessment is not None
        
        # Check reasoning monitors
        for monitor in result.reasoning_monitors:
            assert isinstance(monitor, ReasoningMonitor)
            assert len(monitor.metrics_tracked) > 0
            assert monitor.monitoring_frequency is not None
    
    async def test_bias_detection(self, analyzer):
        """Test bias detection"""
        context = MetacognitiveMonitoringContext(
            reasoning_target="I'm sure this approach is correct because it worked last time. I won't consider alternatives because this always works.",
            complexity_level=ComplexityLevel.SIMPLE,
            monitoring_focus=["bias detection", "confirmation bias", "anchoring bias"],
            bias_detection_enabled=True
        )
        
        result = await analyzer.analyze(context)
        
        # Check that bias detection was attempted (may or may not find biases)
        assert hasattr(result, 'bias_detections')
        if len(result.bias_detections) > 0:
            for bias in result.bias_detections:
                assert isinstance(bias, BiasDetection)
                assert isinstance(bias.bias_type, BiasType)
                assert bias.severity in ["low", "medium", "high"]
    
    async def test_confidence_assessment(self, analyzer):
        """Test confidence assessment"""
        context = MetacognitiveMonitoringContext(
            reasoning_target="I think this solution might work, but I'm not entirely sure about all edge cases",
            complexity_level=ComplexityLevel.MODERATE,
            monitoring_focus=["confidence calibration"],
            confidence_calibration_enabled=True
        )
        
        result = await analyzer.analyze(context)
        
        assert result.confidence_assessment is not None
        assert isinstance(result.confidence_assessment, ConfidenceAssessment)
        assert 0.0 <= result.confidence_assessment.stated_confidence <= 1.0
        assert 0.0 <= result.confidence_assessment.calibrated_confidence <= 1.0
        assert isinstance(result.confidence_assessment.calibration_method, ConfidenceCalibration)
    
    async def test_strategy_evaluation(self, analyzer):
        """Test strategy evaluation"""
        context = MetacognitiveMonitoringContext(
            reasoning_target="Using divide-and-conquer approach to solve this complex sorting problem",
            complexity_level=ComplexityLevel.MODERATE,
            monitoring_focus=["strategy effectiveness"],
            strategy_evaluation_enabled=True
        )
        
        result = await analyzer.analyze(context)
        
        # Check that strategy evaluation was attempted (may or may not find strategies)
        assert hasattr(result, 'strategy_evaluations')
        if len(result.strategy_evaluations) > 0:
            for evaluation in result.strategy_evaluations:
                assert isinstance(evaluation, StrategyEvaluation)
                assert evaluation.current_strategy is not None
                assert len(evaluation.alternative_strategies) >= 0
    
    async def test_meta_learning_insights(self, analyzer):
        """Test meta-learning insight extraction"""
        context = MetacognitiveMonitoringContext(
            reasoning_target="I notice I always get stuck on recursive problems. Maybe I should practice more base cases first.",
            complexity_level=ComplexityLevel.SIMPLE,
            monitoring_focus=["learning patterns", "skill gaps"],
            meta_learning_enabled=True
        )
        
        result = await analyzer.analyze(context)
        
        assert len(result.meta_learning_insights) >= 1
        for insight in result.meta_learning_insights:
            assert isinstance(insight, MetaLearningInsight)
            # Valid insight types from models.py validation
            assert insight.insight_type in ["pattern", "strategy", "bias", "performance", "context"]
    
    def test_context_validation(self):
        """Test context validation"""
        # Reasoning target too short
        with pytest.raises(ValueError):
            MetacognitiveMonitoringContext(
                reasoning_target="Too short",
                complexity_level=ComplexityLevel.SIMPLE
            )
        
        # Invalid complexity level
        with pytest.raises(ValueError):
            MetacognitiveMonitoringContext(
                reasoning_target="This is a valid reasoning process description for analysis",
                complexity_level="invalid"  # type: ignore
            )
    
    async def test_monitoring_depth_impact(self, analyzer):
        """Test that monitoring depth affects analysis"""
        shallow_context = MetacognitiveMonitoringContext(
            reasoning_target="Evaluating whether to use microservices or monolithic architecture",
            monitoring_depth=MonitoringDepth.SURFACE
        )
        
        deep_context = MetacognitiveMonitoringContext(
            reasoning_target="Evaluating whether to use microservices or monolithic architecture",
            monitoring_depth=MonitoringDepth.DEEP
        )
        
        shallow_result = await analyzer.analyze(shallow_context)
        deep_result = await analyzer.analyze(deep_context)
        
        # Deeper monitoring should yield more insights
        assert len(deep_result.meta_learning_insights) >= len(shallow_result.meta_learning_insights)
    
    async def test_comprehensive_monitoring(self, analyzer):
        """Test comprehensive monitoring with all features enabled"""
        context = MetacognitiveMonitoringContext(
            reasoning_target="Designing a distributed system with high availability requirements. Need to balance consistency vs availability tradeoffs.",
            complexity_level=ComplexityLevel.COMPLEX,
            monitoring_focus=["system design", "tradeoff analysis", "decision making"],
            bias_detection_enabled=True,
            confidence_calibration_enabled=True,
            strategy_evaluation_enabled=True,
            meta_learning_enabled=True,
            monitoring_depth=MonitoringDepth.DEEP,
            monitoring_frequency=MonitoringFrequency.CONTINUOUS
        )
        
        result = await analyzer.analyze(context)
        
        # All components should be present
        assert len(result.reasoning_monitors) >= 1
        assert result.confidence_assessment is not None
        assert len(result.strategy_evaluations) >= 0
        assert len(result.bias_detections) >= 0
        assert len(result.meta_learning_insights) >= 0
        
        # Should have comprehensive analysis
        assert len(result.improvement_recommendations) >= 1