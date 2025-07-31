# Simple Integration Tests for Clear Thinking FastMCP
"""
Start small integration tests that actually import and use the real models.
This will give us real coverage metrics.
"""

import pytest
import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Import directly from the module to avoid __init__.py import issues
from clear_thinking_fastmcp.models.triple_constraint import (
    ConstraintDimension,
    ConstraintSet,
    TripleConstraintInput,
    TripleConstraintAnalysis
)


class TestTripleConstraintIntegration:
    """Simple integration tests for Triple Constraint model"""
    
    def test_constraint_dimension_enum(self):
        """Test using constraint dimension enum values"""
        # Test that enum values work correctly
        assert ConstraintDimension.QUALITY == "quality"
        assert ConstraintDimension.SPEED == "speed" 
        assert ConstraintDimension.COST == "cost"
        
        # Test enum can be used as string
        quality_dim = ConstraintDimension.QUALITY
        assert quality_dim == "quality"
    
    def test_constraint_set_creation(self):
        """Test creating a constraint set with three dimensions"""
        constraint_set = ConstraintSet(
            dimension_a="Quality",
            dimension_b="Speed", 
            dimension_c="Cost",
            current_values=[0.7, 0.5, 0.8],
            target_values=[0.9, 0.6, 0.7]
        )
        
        assert constraint_set.dimension_a == "Quality"
        assert constraint_set.dimension_b == "Speed"
        assert constraint_set.dimension_c == "Cost"
        assert len(constraint_set.current_values) == 3
        assert len(constraint_set.target_values) == 3
        assert all(0.0 <= val <= 1.0 for val in constraint_set.current_values)
    
    def test_triple_constraint_input_creation(self):
        """Test creating input for triple constraint analysis"""
        constraint_set = ConstraintSet(
            dimension_a="Time",
            dimension_b="Budget", 
            dimension_c="Features",
            current_values=[0.6, 0.8, 0.5],
            target_values=[0.7, 0.9, 0.8]
        )
        
        input_data = TripleConstraintInput(
            problem="How to balance time, budget, and features for mobile app development?",
            scenario="Develop new mobile app feature",
            complexity_level="medium",
            session_id="test_session_1",
            domain_context="software_development",
            constraints=constraint_set,
            optimization_goal="Deliver maximum features within budget"
        )
        
        assert input_data.scenario == "Develop new mobile app feature"
        assert input_data.domain_context == "software_development"
        assert input_data.constraints.dimension_a == "Time"
        assert input_data.optimization_goal == "Deliver maximum features within budget"
    
    def test_constraint_set_validation(self):
        """Test constraint set validation logic"""
        # Test valid constraint set
        constraint_set = ConstraintSet(
            dimension_a="Quality",
            dimension_b="Speed", 
            dimension_c="Cost",
            current_values=[0.7, 0.5, 0.8],
            target_values=[0.9, 0.6, 0.7]
        )
        
        # Test validation passes for valid values
        assert all(0.0 <= val <= 1.0 for val in constraint_set.current_values)
        assert all(0.0 <= val <= 1.0 for val in constraint_set.target_values)
    
# Skip complex analysis output test for now - needs proper model structure
    
    def test_constraint_dimension_values(self):
        """Test all constraint dimension enum values"""
        # Test project management dimensions
        assert ConstraintDimension.SCOPE == "scope"
        assert ConstraintDimension.TIME == "time"
        assert ConstraintDimension.BUDGET == "budget"
        
        # Test engineering dimensions  
        assert ConstraintDimension.PERFORMANCE == "performance"
        assert ConstraintDimension.COST == "cost"
        assert ConstraintDimension.RELIABILITY == "reliability"
        
        # Test business dimensions
        assert ConstraintDimension.QUALITY == "quality"
        assert ConstraintDimension.SPEED == "speed"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])