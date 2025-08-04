# Simple Integration Tests for PyClarity
"""
Start small integration tests that actually import and use the real models.
This gives us real coverage metrics for PyClarity tools.
"""

import pytest

# Test with a simple implemented tool (Mental Models)
from pyclarity.tools.mental_models import (
    MentalModelsAnalyzer,
    MentalModelContext,
    MentalModelResult,
    MentalModelType,
    ComplexityLevel
)


class TestMentalModelsIntegration:
    """Simple integration tests for Mental Models tool"""
    
    def test_mental_model_type_enum(self):
        """Test using mental model type enum values"""
        # Test that enum values work correctly
        assert MentalModelType.FIRST_PRINCIPLES == "first_principles"
        assert MentalModelType.OPPORTUNITY_COST == "opportunity_cost"
        assert MentalModelType.ERROR_PROPAGATION == "error_propagation"
        
        # Test enum can be used as string
        first_principles = MentalModelType.FIRST_PRINCIPLES
        assert first_principles == "first_principles"
    
    def test_complexity_level_enum(self):
        """Test complexity level enum values"""
        assert ComplexityLevel.SIMPLE == "simple"
        assert ComplexityLevel.MODERATE == "moderate"
        assert ComplexityLevel.COMPLEX == "complex"
    
    def test_mental_model_context_creation(self):
        """Test creating context for mental model analysis"""
        context = MentalModelContext(
            problem="How to improve software architecture scalability?",
            model_type=MentalModelType.FIRST_PRINCIPLES,
            complexity_level=ComplexityLevel.MODERATE,
            constraints=["Budget limitations", "Team expertise", "Time constraints"]
        )
        
        assert context.problem == "How to improve software architecture scalability?"
        assert context.model_type == MentalModelType.FIRST_PRINCIPLES
        assert context.complexity_level == ComplexityLevel.MODERATE
        assert len(context.constraints) == 3
    
    def test_mental_models_analyzer_creation(self):
        """Test creating mental models analyzer"""
        analyzer = MentalModelsAnalyzer()
        
        # Test analyzer has expected properties
        assert analyzer.tool_name == "Mental Models"
        assert hasattr(analyzer, 'analyze')
    
    def test_context_validation(self):
        """Test context validation logic"""
        # Test valid context
        context = MentalModelContext(
            problem="Test problem for validation - need longer text for min length requirement",
            model_type=MentalModelType.FIRST_PRINCIPLES,
            complexity_level=ComplexityLevel.SIMPLE
        )
        
        # Test validation passes for valid values
        assert context.problem is not None
        assert len(context.problem) > 0
        assert context.model_type in [
            MentalModelType.FIRST_PRINCIPLES,
            MentalModelType.OPPORTUNITY_COST,
            MentalModelType.ERROR_PROPAGATION,
            MentalModelType.RUBBER_DUCK,
            MentalModelType.PARETO_PRINCIPLE,
            MentalModelType.OCCAMS_RAZOR
        ]
    
    def test_all_mental_model_types(self):
        """Test all mental model type enum values"""
        # Test available mental model types
        assert MentalModelType.FIRST_PRINCIPLES == "first_principles"
        assert MentalModelType.OPPORTUNITY_COST == "opportunity_cost"
        assert MentalModelType.ERROR_PROPAGATION == "error_propagation"
        assert MentalModelType.RUBBER_DUCK == "rubber_duck"
        assert MentalModelType.PARETO_PRINCIPLE == "pareto_principle"
        assert MentalModelType.OCCAMS_RAZOR == "occams_razor"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])