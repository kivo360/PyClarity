"""Test Mental Models cognitive tool.

Tests adapted from FastMCP implementation to work with PyClarity's async analyzer pattern.
"""

import pytest
import pytest_asyncio
from typing import List, Dict

from pyclarity.tools.mental_models.models import (
    MentalModelsContext,
    MentalModelsResult,
    FrameworkType,
    FrameworkApplication,
    CrossFrameworkInsight,
    FrameworkSynergy,
    ComplexityLevel
)
from pyclarity.tools.mental_models.analyzer import MentalModelsAnalyzer


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def simple_context():
    """Generate simple MentalModelsContext for testing"""
    return MentalModelsContext(
        problem="How to improve code review process in our development team?",
        context="Team of 8 developers, varying experience levels, distributed across timezones",
        frameworks=[FrameworkType.FIRST_PRINCIPLES, FrameworkType.PARETO_PRINCIPLE],
        complexity_level=ComplexityLevel.MEDIUM
    )


@pytest.fixture
def complex_context():
    """Generate complex MentalModelsContext for testing"""
    return MentalModelsContext(
        problem="Design a scalable microservices architecture for an e-commerce platform",
        context="High-traffic platform with 1M+ daily users, need for reliability and scalability",
        frameworks=[
            FrameworkType.FIRST_PRINCIPLES,
            FrameworkType.OPPORTUNITY_COST,
            FrameworkType.ERROR_PROPAGATION,
            FrameworkType.OCCAMS_RAZOR
        ],
        complexity_level=ComplexityLevel.COMPLEX,
        enable_cross_framework_analysis=True,
        max_thinking_depth=8
    )


@pytest.fixture
def mental_models_analyzer():
    """Create MentalModelsAnalyzer instance for testing"""
    return MentalModelsAnalyzer()


# ============================================================================
# Model Tests
# ============================================================================

class TestMentalModelsContext:
    """Test suite for MentalModelsContext model"""
    
    def test_context_creation_valid(self, simple_context):
        """Test creating a valid context"""
        assert simple_context.problem
        assert simple_context.complexity_level == ComplexityLevel.MEDIUM
        assert len(simple_context.frameworks) == 2
        assert FrameworkType.FIRST_PRINCIPLES in simple_context.frameworks
    
    def test_context_validation_problem_too_short(self):
        """Test context validation with problem too short"""
        with pytest.raises(ValueError, match="String should have at least 10 characters"):
            MentalModelsContext(
                problem="Too short",
                context="Valid context",
                frameworks=[FrameworkType.FIRST_PRINCIPLES]
            )
    
    def test_context_validation_no_frameworks(self):
        """Test context validation with no frameworks"""
        with pytest.raises(ValueError, match="List should have at least 1 item"):
            MentalModelsContext(
                problem="Valid problem description",
                context="Valid context",
                frameworks=[]
            )
    
    def test_context_max_thinking_depth_validation(self):
        """Test max thinking depth validation"""
        with pytest.raises(ValueError, match="Input should be greater than or equal to 3"):
            MentalModelsContext(
                problem="Valid problem",
                context="Valid context",
                frameworks=[FrameworkType.FIRST_PRINCIPLES],
                max_thinking_depth=2
            )
        
        with pytest.raises(ValueError, match="Input should be less than or equal to 15"):
            MentalModelsContext(
                problem="Valid problem",
                context="Valid context",
                frameworks=[FrameworkType.FIRST_PRINCIPLES],
                max_thinking_depth=20
            )


class TestFrameworkApplication:
    """Test suite for FrameworkApplication model"""
    
    def test_framework_application_creation(self):
        """Test creating a framework application"""
        app = FrameworkApplication(
            framework_type=FrameworkType.FIRST_PRINCIPLES,
            framework_name="First Principles Thinking",
            analysis_steps=[
                "Break down the code review process into fundamental components",
                "Identify the core purpose of code reviews",
                "Rebuild the process from basic principles"
            ],
            insights=[
                "Code reviews serve quality assurance and knowledge sharing",
                "Current process has unnecessary complexity"
            ],
            recommendations=[
                "Simplify review checklist to essential items",
                "Focus on knowledge transfer over nitpicking"
            ],
            confidence_score=0.85
        )
        
        assert app.framework_type == FrameworkType.FIRST_PRINCIPLES
        assert len(app.analysis_steps) == 3
        assert len(app.insights) == 2
        assert app.confidence_score == 0.85


# ============================================================================
# Analyzer Tests
# ============================================================================

@pytest.mark.asyncio
class TestMentalModelsAnalyzer:
    """Test suite for MentalModelsAnalyzer"""
    
    async def test_analyzer_initialization(self, mental_models_analyzer):
        """Test analyzer initialization"""
        assert mental_models_analyzer.tool_name == "Mental Models"
        assert mental_models_analyzer.version == "2.0.0"
    
    async def test_basic_analysis(self, mental_models_analyzer, simple_context):
        """Test basic mental models analysis"""
        result = await mental_models_analyzer.analyze(simple_context)
        
        assert isinstance(result, MentalModelsResult)
        assert len(result.framework_applications) == 2
        assert result.synthesis is not None
        assert result.confidence_score > 0
        assert result.processing_time_ms > 0
    
    async def test_first_principles_framework(self, mental_models_analyzer):
        """Test First Principles framework application"""
        context = MentalModelsContext(
            problem="How to optimize database performance?",
            context="E-commerce platform with slow queries",
            frameworks=[FrameworkType.FIRST_PRINCIPLES]
        )
        
        result = await mental_models_analyzer.analyze(context)
        
        assert len(result.framework_applications) == 1
        app = result.framework_applications[0]
        assert app.framework_type == FrameworkType.FIRST_PRINCIPLES
        assert len(app.analysis_steps) > 0
        assert len(app.insights) > 0
    
    async def test_opportunity_cost_framework(self, mental_models_analyzer):
        """Test Opportunity Cost framework application"""
        context = MentalModelsContext(
            problem="Should we refactor the legacy codebase or build new features?",
            context="Limited development resources, technical debt accumulating",
            frameworks=[FrameworkType.OPPORTUNITY_COST]
        )
        
        result = await mental_models_analyzer.analyze(context)
        
        app = next(a for a in result.framework_applications if a.framework_type == FrameworkType.OPPORTUNITY_COST)
        assert "cost" in app.framework_name.lower()
        assert any("alternative" in step.lower() for step in app.analysis_steps)
    
    async def test_error_propagation_framework(self, mental_models_analyzer):
        """Test Error Propagation framework application"""
        context = MentalModelsContext(
            problem="Design error handling for distributed system",
            context="Microservices architecture with multiple failure points",
            frameworks=[FrameworkType.ERROR_PROPAGATION]
        )
        
        result = await mental_models_analyzer.analyze(context)
        
        app = next(a for a in result.framework_applications if a.framework_type == FrameworkType.ERROR_PROPAGATION)
        assert any("propagat" in step.lower() for step in app.analysis_steps)
        assert any("failure" in insight.lower() or "error" in insight.lower() for insight in app.insights)
    
    async def test_rubber_duck_debugging_framework(self, mental_models_analyzer):
        """Test Rubber Duck Debugging framework application"""
        context = MentalModelsContext(
            problem="Debug complex state management issue in React application",
            context="State updates not reflecting in UI components",
            frameworks=[FrameworkType.RUBBER_DUCK_DEBUGGING]
        )
        
        result = await mental_models_analyzer.analyze(context)
        
        app = next(a for a in result.framework_applications if a.framework_type == FrameworkType.RUBBER_DUCK_DEBUGGING)
        assert any("explain" in step.lower() or "describe" in step.lower() for step in app.analysis_steps)
    
    async def test_pareto_principle_framework(self, mental_models_analyzer):
        """Test Pareto Principle framework application"""
        context = MentalModelsContext(
            problem="Optimize application performance",
            context="Multiple performance bottlenecks identified",
            frameworks=[FrameworkType.PARETO_PRINCIPLE]
        )
        
        result = await mental_models_analyzer.analyze(context)
        
        app = next(a for a in result.framework_applications if a.framework_type == FrameworkType.PARETO_PRINCIPLE)
        assert any("80" in step or "20" in step for step in app.analysis_steps)
        assert any("focus" in rec.lower() or "prioritize" in rec.lower() for rec in app.recommendations)
    
    async def test_occams_razor_framework(self, mental_models_analyzer):
        """Test Occam's Razor framework application"""
        context = MentalModelsContext(
            problem="Choose between complex and simple architectural solutions",
            context="Multiple proposed solutions with varying complexity",
            frameworks=[FrameworkType.OCCAMS_RAZOR]
        )
        
        result = await mental_models_analyzer.analyze(context)
        
        app = next(a for a in result.framework_applications if a.framework_type == FrameworkType.OCCAMS_RAZOR)
        assert any("simple" in step.lower() or "complex" in step.lower() for step in app.analysis_steps)
    
    async def test_cross_framework_analysis(self, mental_models_analyzer, complex_context):
        """Test cross-framework analysis"""
        result = await mental_models_analyzer.analyze(complex_context)
        
        assert len(result.cross_framework_insights) > 0
        
        for insight in result.cross_framework_insights:
            assert isinstance(insight, CrossFrameworkInsight)
            assert len(insight.frameworks_involved) >= 2
            assert insight.insight_description
            assert insight.confidence_score > 0
    
    async def test_framework_synergies(self, mental_models_analyzer):
        """Test framework synergy detection"""
        context = MentalModelsContext(
            problem="Design a fault-tolerant system",
            context="Critical system requiring high reliability",
            frameworks=[
                FrameworkType.FIRST_PRINCIPLES,
                FrameworkType.ERROR_PROPAGATION,
                FrameworkType.OCCAMS_RAZOR
            ],
            enable_cross_framework_analysis=True
        )
        
        result = await mental_models_analyzer.analyze(context)
        
        assert len(result.framework_synergies) > 0
        
        for synergy in result.framework_synergies:
            assert isinstance(synergy, FrameworkSynergy)
            assert synergy.framework1 != synergy.framework2
            assert synergy.synergy_score > 0
    
    async def test_synthesis_generation(self, mental_models_analyzer, simple_context):
        """Test synthesis generation"""
        result = await mental_models_analyzer.analyze(simple_context)
        
        assert result.synthesis is not None
        assert len(result.synthesis) > 50  # Should be meaningful
        assert result.synthesis != simple_context.problem  # Should not just repeat the problem
    
    async def test_actionable_recommendations(self, mental_models_analyzer, simple_context):
        """Test actionable recommendations generation"""
        result = await mental_models_analyzer.analyze(simple_context)
        
        assert len(result.actionable_recommendations) > 0
        assert len(result.actionable_recommendations) <= 10
        
        for rec in result.actionable_recommendations:
            assert len(rec) > 10  # Should be meaningful
    
    async def test_complexity_level_impact(self, mental_models_analyzer):
        """Test that complexity level affects analysis depth"""
        simple_context = MentalModelsContext(
            problem="Simple optimization problem",
            context="Basic context",
            frameworks=[FrameworkType.FIRST_PRINCIPLES],
            complexity_level=ComplexityLevel.SIMPLE
        )
        
        complex_context = MentalModelsContext(
            problem="Complex system design problem",
            context="Large-scale distributed system",
            frameworks=[FrameworkType.FIRST_PRINCIPLES],
            complexity_level=ComplexityLevel.COMPLEX,
            max_thinking_depth=10
        )
        
        simple_result = await mental_models_analyzer.analyze(simple_context)
        complex_result = await mental_models_analyzer.analyze(complex_context)
        
        # Complex analysis should be more thorough
        simple_steps = simple_result.framework_applications[0].analysis_steps
        complex_steps = complex_result.framework_applications[0].analysis_steps
        
        assert len(complex_steps) >= len(simple_steps)
    
    async def test_multiple_frameworks_integration(self, mental_models_analyzer):
        """Test integration of multiple frameworks"""
        context = MentalModelsContext(
            problem="Optimize team productivity while maintaining code quality",
            context="Growing development team with mixed experience levels",
            frameworks=[
                FrameworkType.PARETO_PRINCIPLE,
                FrameworkType.OPPORTUNITY_COST,
                FrameworkType.FIRST_PRINCIPLES
            ]
        )
        
        result = await mental_models_analyzer.analyze(context)
        
        assert len(result.framework_applications) == 3
        
        # Check that insights reference each other
        all_insights = []
        for app in result.framework_applications:
            all_insights.extend(app.insights)
        
        # Synthesis should integrate insights from multiple frameworks
        assert any(
            framework.value.replace('_', ' ').lower() in result.synthesis.lower()
            for framework in context.frameworks
        )
    
    async def test_confidence_score_calculation(self, mental_models_analyzer, simple_context):
        """Test confidence score calculation"""
        result = await mental_models_analyzer.analyze(simple_context)
        
        assert 0 <= result.confidence_score <= 1
        
        # Confidence should be reasonable for a valid analysis
        assert result.confidence_score > 0.5
    
    async def test_empty_context_error(self, mental_models_analyzer):
        """Test error handling for empty context"""
        with pytest.raises(ValueError):
            context = MentalModelsContext(
                problem="",  # Empty problem
                context="Some context",
                frameworks=[FrameworkType.FIRST_PRINCIPLES]
            )