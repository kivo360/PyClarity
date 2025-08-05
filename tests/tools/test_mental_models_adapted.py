"""Test Mental Models cognitive tool.

Adapted to match the actual PyClarity implementation.
"""

import pytest
from pyclarity.tools.mental_models.models import (
    MentalModelContext,
    MentalModelResult,
    MentalModelType,
    ComplexityLevel,
    MentalModelInsight,
    MentalModelAssumption
)
from pyclarity.tools.mental_models.analyzer import MentalModelsAnalyzer


class TestMentalModelsAnalyzer:
    """Test suite for Mental Models Analyzer"""
    
    @pytest.fixture
    def analyzer(self):
        """Create analyzer instance"""
        return MentalModelsAnalyzer()
    
    @pytest.fixture
    def simple_context(self):
        """Create simple test context"""
        return MentalModelContext(
            problem="How to improve code review process in our development team? We have 8 developers with varying experience levels.",
            model_type=MentalModelType.FIRST_PRINCIPLES,
            complexity_level=ComplexityLevel.MODERATE,
            focus_areas=["code quality", "team efficiency", "knowledge sharing"]
        )
    
    @pytest.fixture
    def complex_context(self):
        """Create complex test context"""
        return MentalModelContext(
            problem="Design a scalable microservices architecture for an e-commerce platform with 1M+ daily users",
            model_type=MentalModelType.FIRST_PRINCIPLES,
            complexity_level=ComplexityLevel.COMPLEX,
            focus_areas=["scalability", "reliability", "performance"],
            constraints=["budget limitations", "team size", "timeline"]
        )
    
    async def test_analyze_simple_problem(self, analyzer, simple_context):
        """Test analyzing a simple problem"""
        result = await analyzer.analyze(simple_context)
        
        assert isinstance(result, MentalModelResult)
        assert result.model_applied == MentalModelType.FIRST_PRINCIPLES
        assert len(result.key_insights) >= 1
        assert len(result.recommendations) >= 1
        
        # Check insight structure
        for insight in result.key_insights:
            assert isinstance(insight, MentalModelInsight)
            assert 0.0 <= insight.relevance_score <= 1.0
            assert len(insight.insight) >= 20
    
    async def test_analyze_complex_problem(self, analyzer, complex_context):
        """Test analyzing a complex problem"""
        result = await analyzer.analyze(complex_context)
        
        assert isinstance(result, MentalModelResult)
        assert result.model_applied == MentalModelType.FIRST_PRINCIPLES
        assert len(result.key_insights) >= 3
        assert len(result.recommendations) >= 2
    
    async def test_opportunity_cost_analysis(self, analyzer):
        """Test opportunity cost mental model"""
        context = MentalModelContext(
            problem="Should we invest in building an in-house analytics platform or use a third-party solution?",
            model_type=MentalModelType.OPPORTUNITY_COST,
            complexity_level=ComplexityLevel.MODERATE
        )
        
        result = await analyzer.analyze(context)
        
        assert result.model_applied == MentalModelType.OPPORTUNITY_COST
        assert result.trade_offs is not None
        assert len(result.trade_offs) >= 1
        
        # Check trade-off structure
        for trade_off in result.trade_offs:
            assert "option" in trade_off
            assert "benefit" in trade_off
            assert "cost" in trade_off
    
    async def test_error_propagation_analysis(self, analyzer):
        """Test error propagation mental model"""
        context = MentalModelContext(
            problem="What are the failure modes in our payment processing system and how might they cascade?",
            model_type=MentalModelType.ERROR_PROPAGATION,
            complexity_level=ComplexityLevel.COMPLEX
        )
        
        result = await analyzer.analyze(context)
        
        assert result.model_applied == MentalModelType.ERROR_PROPAGATION
        assert result.error_paths is not None
        assert len(result.error_paths) >= 1
    
    async def test_pareto_principle_analysis(self, analyzer):
        """Test Pareto principle mental model"""
        context = MentalModelContext(
            problem="Which features should we prioritize to maximize user satisfaction with limited resources?",
            model_type=MentalModelType.PARETO_PRINCIPLE,
            complexity_level=ComplexityLevel.MODERATE
        )
        
        result = await analyzer.analyze(context)
        
        assert result.model_applied == MentalModelType.PARETO_PRINCIPLE
        assert result.critical_factors is not None
        assert len(result.critical_factors) >= 1
    
    async def test_occams_razor_analysis(self, analyzer):
        """Test Occam's Razor mental model"""
        context = MentalModelContext(
            problem="We have three different solutions for user authentication. Which approach should we choose?",
            model_type=MentalModelType.OCCAMS_RAZOR,
            complexity_level=ComplexityLevel.SIMPLE
        )
        
        result = await analyzer.analyze(context)
        
        assert result.model_applied == MentalModelType.OCCAMS_RAZOR
        assert result.simplified_explanation is not None
        assert len(result.simplified_explanation) >= 20
    
    async def test_rubber_duck_debugging(self, analyzer):
        """Test rubber duck debugging mental model"""
        context = MentalModelContext(
            problem="Our API responses are slow but we can't figure out why. Let me explain the system...",
            model_type=MentalModelType.RUBBER_DUCK,
            complexity_level=ComplexityLevel.MODERATE
        )
        
        result = await analyzer.analyze(context)
        
        assert result.model_applied == MentalModelType.RUBBER_DUCK
        assert len(result.key_insights) >= 1
        assert len(result.recommendations) >= 1
    
    def test_context_validation(self):
        """Test context validation"""
        # Problem too short
        with pytest.raises(ValueError):
            MentalModelContext(
                problem="Too short",
                model_type=MentalModelType.FIRST_PRINCIPLES
            )
        
        # Invalid model type
        with pytest.raises(ValueError):
            MentalModelContext(
                problem="This is a valid problem description for analysis",
                model_type="invalid_type"  # type: ignore
            )
    
    def test_model_utils(self):
        """Test mental model utility functions"""
        from pyclarity.tools.mental_models.models import MentalModelUtils
        
        # Test model suggestion
        problem = "I need to choose between multiple implementation options"
        suggestions = MentalModelUtils.suggest_mental_model(problem)
        assert MentalModelType.OPPORTUNITY_COST in suggestions
        
        # Test model compatibility
        assert MentalModelUtils.validate_model_compatibility(
            "How does this system fundamentally work?",
            MentalModelType.FIRST_PRINCIPLES
        )
