"""Test Metacognitive Monitoring cognitive tool.

Tests for self-awareness analysis, bias detection, and cognitive load assessment.
"""

import pytest
import pytest_asyncio
from typing import List

from pyclarity.tools.metacognitive_monitoring.models import (
    MetacognitiveMonitoringContext,
    MetacognitiveMonitoringResult,
    CognitiveState,
    BiasDetection,
    BiasType,
    CognitiveLoad,
    SelfAssessment,
    ThinkingPattern,
    PatternType,
    ComplexityLevel
)
from pyclarity.tools.metacognitive_monitoring.analyzer import MetacognitiveMonitoringAnalyzer


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def simple_context():
    """Generate simple MetacognitiveMonitoringContext for testing"""
    return MetacognitiveMonitoringContext(
        thinking_process="I believe microservices are always better than monoliths because they're modern",
        context="Evaluating architecture decisions for a small startup",
        specific_biases_to_check=[BiasType.CONFIRMATION_BIAS, BiasType.RECENCY_BIAS],
        awareness_depth=5
    )


@pytest.fixture
def complex_context():
    """Generate complex MetacognitiveMonitoringContext for testing"""
    return MetacognitiveMonitoringContext(
        thinking_process="Our team has always used this approach and it's worked well. The new proposal seems risky and I don't think we have time to learn new things. Plus, the last project that tried something different failed.",
        context="Team discussing adoption of new development methodology",
        specific_biases_to_check=[
            BiasType.STATUS_QUO_BIAS,
            BiasType.ANCHORING_BIAS,
            BiasType.AVAILABILITY_CASCADE,
            BiasType.BANDWAGON_EFFECT
        ],
        awareness_depth=8,
        include_improvement_strategies=True,
        track_cognitive_load=True,
        complexity_level=ComplexityLevel.COMPLEX
    )


@pytest.fixture
def metacognitive_analyzer():
    """Create MetacognitiveMonitoringAnalyzer instance for testing"""
    return MetacognitiveMonitoringAnalyzer()


# ============================================================================
# Model Tests
# ============================================================================

class TestBiasDetection:
    """Test suite for BiasDetection model"""
    
    def test_bias_detection_creation(self):
        """Test creating a bias detection"""
        bias = BiasDetection(
            bias_type=BiasType.CONFIRMATION_BIAS,
            description="Seeking only information that confirms existing beliefs",
            evidence=["Only cited sources that support the position", "Ignored contradictory data"],
            impact_level="high",
            confidence=0.85
        )
        
        assert bias.bias_type == BiasType.CONFIRMATION_BIAS
        assert len(bias.evidence) == 2
        assert bias.impact_level == "high"
        assert bias.confidence == 0.85


class TestCognitiveLoad:
    """Test suite for CognitiveLoad model"""
    
    def test_cognitive_load_creation(self):
        """Test creating cognitive load assessment"""
        load = CognitiveLoad(
            current_level="high",
            factors=["Multiple complex decisions", "Time pressure", "Information overload"],
            capacity_usage=0.85,
            bottlenecks=["Working memory", "Decision fatigue"]
        )
        
        assert load.current_level == "high"
        assert len(load.factors) == 3
        assert load.capacity_usage == 0.85
        assert "Working memory" in load.bottlenecks


# ============================================================================
# Analyzer Tests
# ============================================================================

@pytest.mark.asyncio
class TestMetacognitiveMonitoringAnalyzer:
    """Test suite for MetacognitiveMonitoringAnalyzer"""
    
    async def test_analyzer_initialization(self, metacognitive_analyzer):
        """Test analyzer initialization"""
        assert metacognitive_analyzer.tool_name == "Metacognitive Monitoring"
        assert metacognitive_analyzer.version == "2.0.0"
    
    async def test_basic_analysis(self, metacognitive_analyzer, simple_context):
        """Test basic metacognitive analysis"""
        result = await metacognitive_analyzer.analyze(simple_context)
        
        assert isinstance(result, MetacognitiveMonitoringResult)
        assert result.cognitive_state is not None
        assert len(result.detected_biases) > 0
        assert result.self_assessment is not None
        assert result.confidence_score > 0
        assert result.processing_time_ms > 0
    
    async def test_bias_detection(self, metacognitive_analyzer, simple_context):
        """Test bias detection functionality"""
        result = await metacognitive_analyzer.analyze(simple_context)
        
        # Should detect the biases mentioned in the thinking process
        bias_types = [b.bias_type for b in result.detected_biases]
        
        # The thinking mentions "always better" and "modern" - signs of bias
        assert any(b.bias_type in [BiasType.CONFIRMATION_BIAS, BiasType.RECENCY_BIAS] 
                  for b in result.detected_biases)
    
    async def test_cognitive_state_assessment(self, metacognitive_analyzer, simple_context):
        """Test cognitive state assessment"""
        result = await metacognitive_analyzer.analyze(simple_context)
        
        state = result.cognitive_state
        assert isinstance(state, CognitiveState)
        assert state.clarity_level in ["low", "medium", "high"]
        assert 0 <= state.confidence_calibration <= 1
        assert state.emotional_influence in ["low", "medium", "high"]
        assert len(state.active_biases) >= 0
    
    async def test_thinking_pattern_identification(self, metacognitive_analyzer, complex_context):
        """Test identification of thinking patterns"""
        result = await metacognitive_analyzer.analyze(complex_context)
        
        assert len(result.thinking_patterns_identified) > 0
        
        for pattern in result.thinking_patterns_identified:
            assert isinstance(pattern, ThinkingPattern)
            assert pattern.pattern_type in PatternType
            assert pattern.description
            assert pattern.frequency in ["rare", "occasional", "frequent"]
    
    async def test_self_assessment_generation(self, metacognitive_analyzer, simple_context):
        """Test self-assessment generation"""
        result = await metacognitive_analyzer.analyze(simple_context)
        
        assessment = result.self_assessment
        assert isinstance(assessment, SelfAssessment)
        assert len(assessment.strengths_identified) > 0
        assert len(assessment.weaknesses_identified) > 0
        assert len(assessment.blind_spots) >= 0
        assert 0 <= assessment.overall_awareness_score <= 1
    
    async def test_cognitive_load_tracking(self, metacognitive_analyzer, complex_context):
        """Test cognitive load assessment"""
        complex_context.track_cognitive_load = True
        
        result = await metacognitive_analyzer.analyze(complex_context)
        
        assert result.cognitive_load_assessment is not None
        load = result.cognitive_load_assessment
        assert load.current_level in ["low", "medium", "high"]
        assert len(load.factors) > 0
        assert 0 <= load.capacity_usage <= 1
    
    async def test_improvement_strategies(self, metacognitive_analyzer, complex_context):
        """Test improvement strategy generation"""
        complex_context.include_improvement_strategies = True
        
        result = await metacognitive_analyzer.analyze(complex_context)
        
        assert len(result.improvement_strategies) > 0
        assert len(result.improvement_strategies) <= 10
        
        for strategy in result.improvement_strategies:
            assert len(strategy) > 20  # Should be meaningful
    
    async def test_metacognitive_insights(self, metacognitive_analyzer, simple_context):
        """Test metacognitive insights generation"""
        result = await metacognitive_analyzer.analyze(simple_context)
        
        assert len(result.metacognitive_insights) > 0
        
        for insight in result.metacognitive_insights:
            assert len(insight) > 30  # Should be substantial
    
    async def test_awareness_depth_impact(self, metacognitive_analyzer):
        """Test that awareness depth affects analysis"""
        shallow_context = MetacognitiveMonitoringContext(
            thinking_process="This seems like a good idea",
            context="Quick decision",
            awareness_depth=2
        )
        
        deep_context = MetacognitiveMonitoringContext(
            thinking_process="This seems like a good idea",
            context="Quick decision",
            awareness_depth=10
        )
        
        shallow_result = await metacognitive_analyzer.analyze(shallow_context)
        deep_result = await metacognitive_analyzer.analyze(deep_context)
        
        # Deeper awareness should yield more insights
        assert len(deep_result.metacognitive_insights) >= len(shallow_result.metacognitive_insights)
    
    async def test_multiple_bias_detection(self, metacognitive_analyzer):
        """Test detection of multiple biases"""
        context = MetacognitiveMonitoringContext(
            thinking_process="""
            Everyone on the team agrees this is the best approach. 
            The last time we tried something different it failed. 
            All the recent articles I've read support this.
            We've always done it this way and it works.
            """,
            context="Technical decision making",
            specific_biases_to_check=[
                BiasType.BANDWAGON_EFFECT,
                BiasType.AVAILABILITY_CASCADE,
                BiasType.CONFIRMATION_BIAS,
                BiasType.STATUS_QUO_BIAS
            ]
        )
        
        result = await metacognitive_analyzer.analyze(context)
        
        # Should detect multiple biases from the thinking process
        assert len(result.detected_biases) >= 2
        
        detected_types = [b.bias_type for b in result.detected_biases]
        # Should detect at least some of these obvious biases
        expected_biases = [
            BiasType.BANDWAGON_EFFECT,  # "Everyone agrees"
            BiasType.STATUS_QUO_BIAS,   # "always done it this way"
        ]
        assert any(bias in detected_types for bias in expected_biases)
    
    async def test_emotional_influence_detection(self, metacognitive_analyzer):
        """Test detection of emotional influence"""
        context = MetacognitiveMonitoringContext(
            thinking_process="I'm really frustrated with this problem and just want to move on. This solution seems good enough.",
            context="Problem-solving under stress",
            track_cognitive_load=True
        )
        
        result = await metacognitive_analyzer.analyze(context)
        
        # Should detect emotional influence
        assert result.cognitive_state.emotional_influence in ["medium", "high"]
    
    async def test_pattern_type_variety(self, metacognitive_analyzer, complex_context):
        """Test identification of various thinking pattern types"""
        result = await metacognitive_analyzer.analyze(complex_context)
        
        pattern_types = [p.pattern_type for p in result.thinking_patterns_identified]
        
        # Should identify some patterns given the complex thinking
        assert len(pattern_types) > 0
        
        # Check that patterns are valid enum values
        for pt in pattern_types:
            assert pt in PatternType
    
    async def test_recommendations_relevance(self, metacognitive_analyzer, complex_context):
        """Test that recommendations are relevant to detected issues"""
        result = await metacognitive_analyzer.analyze(complex_context)
        
        # If biases were detected, should have improvement strategies
        if result.detected_biases:
            assert len(result.improvement_strategies) > 0
        
        # Recommendations should address identified weaknesses
        if result.self_assessment.weaknesses_identified:
            assert any(
                "bias" in strategy.lower() or "awareness" in strategy.lower()
                for strategy in result.improvement_strategies
            )