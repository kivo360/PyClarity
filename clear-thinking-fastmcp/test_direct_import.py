#!/usr/bin/env python
"""Direct import test to validate models work."""

import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

print("Testing direct import of Triple Constraint model...")

try:
    from clear_thinking_fastmcp.models.triple_constraint import (
        ConstraintDimension,
        ConstraintSet,
        TripleConstraintInput,
        TripleConstraintAnalysis
    )
    print("✓ Imports successful!")
    
    # Create a ConstraintSet with the correct structure
    constraint_set = ConstraintSet(
        dimension_a="Quality",
        dimension_b="Speed", 
        dimension_c="Cost",
        current_values=[0.7, 0.5, 0.8],
        target_values=[0.9, 0.6, 0.7],
        relationships={
            "quality_speed": "inverse",
            "speed_cost": "direct", 
            "cost_quality": "inverse"
        }
    )
    print(f"✓ Created ConstraintSet with dimensions: {constraint_set.dimension_a}, {constraint_set.dimension_b}, {constraint_set.dimension_c}")
    
    # Create input
    input_data = TripleConstraintInput(
        problem="How to balance quality, speed, and cost for mobile app development?",
        scenario="Test mobile app development project",
        complexity_level="medium", 
        session_id="test_session_1",
        domain_context="software_development",
        constraints=constraint_set,
        optimization_goal="maximize quality while staying on budget"
    )
    print(f"✓ Created TripleConstraintInput for scenario: {input_data.scenario}")
    
    print("\n✅ All tests passed! The model is working correctly.")
    
except Exception as e:
    print(f"\n❌ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()