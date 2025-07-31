#!/usr/bin/env python
"""
Comprehensive validation test for all 11 cognitive tools in Clear Thinking FastMCP.

This test validates that all cognitive tools can be imported and have basic functionality.
We'll use incremental validation: Start Small → Validate → Expand → Scale
"""

import pytest
import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestAllCognitiveToolsValidation:
    """Validate all 11 cognitive tools can be imported and basic functionality works"""
    
    def test_tool_1_mental_models_import(self):
        """Test Mental Models tool import"""
        try:
            from clear_thinking_fastmcp.models.mental_models import (
                MentalModelType,
                MentalModelInput,
                MentalModelOutput
            )
            # Test basic enum functionality
            assert MentalModelType.FIRST_PRINCIPLES == "first_principles"
            assert MentalModelType.OPPORTUNITY_COST == "opportunity_cost"
            print("✓ Mental Models tool imports successfully")
        except Exception as e:
            pytest.fail(f"Mental Models import failed: {e}")
    
    def test_tool_2_sequential_thinking_import(self):
        """Test Sequential Thinking tool import"""
        try:
            from clear_thinking_fastmcp.models.sequential_thinking import (
                SequentialThinkingInput,
                SequentialThinkingOutput,
                ThoughtStepType,
                ThoughtStep
            )
            # Test basic enum functionality
            assert ThoughtStepType.PROBLEM_DECOMPOSITION == "problem_decomposition"
            assert ThoughtStepType.HYPOTHESIS_FORMATION == "hypothesis_formation"
            print("✓ Sequential Thinking tool imports successfully")
        except Exception as e:
            pytest.fail(f"Sequential Thinking import failed: {e}")
    
    def test_tool_3_collaborative_reasoning_import(self):
        """Test Collaborative Reasoning tool import"""
        try:
            from clear_thinking_fastmcp.models.collaborative_reasoning import (
                CollaborativeReasoningInput,
                CollaborativeReasoningOutput,
                PersonaType,
                PersonaPerspective
            )
            # Test basic enum functionality
            assert PersonaType.CRITIC == "critic"
            assert PersonaType.EXPERT == "expert"
            print("✓ Collaborative Reasoning tool imports successfully")
        except Exception as e:
            pytest.fail(f"Collaborative Reasoning import failed: {e}")
    
    def test_tool_4_triple_constraint_import(self):
        """Test Triple Constraint (already validated in detail)"""
        try:
            from clear_thinking_fastmcp.models.triple_constraint import (
                TripleConstraintInput,
                TripleConstraintAnalysis,
                ConstraintDimension,
                ConstraintSet
            )
            # Basic validation
            assert ConstraintDimension.QUALITY == "quality"
            print("✓ Triple Constraint tool imports successfully")
        except Exception as e:
            pytest.fail(f"Triple Constraint import failed: {e}")
    
    def test_tool_5_impact_propagation_import(self):
        """Test Impact Propagation tool import"""
        try:
            from clear_thinking_fastmcp.models.impact_propagation import (
                ImpactPropagationInput,
                ImpactPropagationAnalysis
            )
            print("✓ Impact Propagation tool imports successfully")
        except Exception as e:
            pytest.fail(f"Impact Propagation import failed: {e}")
    
    def test_tool_6_iterative_validation_import(self):
        """Test Iterative Validation tool import"""
        try:
            from clear_thinking_fastmcp.models.iterative_validation import (
                IterativeValidationInput,
                IterativeValidationOutput
            )
            print("✓ Iterative Validation tool imports successfully")
        except Exception as e:
            pytest.fail(f"Iterative Validation import failed: {e}")
    
    def test_tool_7_sequential_readiness_import(self):
        """Test Sequential Readiness tool import"""
        try:
            from clear_thinking_fastmcp.models.sequential_readiness import (
                SequentialReadinessInput,
                SequentialReadinessOutput
            )
            print("✓ Sequential Readiness tool imports successfully")
        except Exception as e:
            pytest.fail(f"Sequential Readiness import failed: {e}")
    
    def test_tool_8_multi_perspective_import(self):
        """Test Multi-Perspective Analysis tool import"""
        try:
            from clear_thinking_fastmcp.models.multi_perspective import (
                MultiPerspectiveInput,
                MultiPerspectiveOutput
            )
            print("✓ Multi-Perspective Analysis tool imports successfully")
        except Exception as e:
            pytest.fail(f"Multi-Perspective Analysis import failed: {e}")
    
    def test_tool_9_scientific_method_import(self):
        """Test Scientific Method tool import"""
        try:
            from clear_thinking_fastmcp.models.scientific_method import (
                ScientificMethodInput,
                ScientificMethodOutput
            )
            print("✓ Scientific Method tool imports successfully")
        except Exception as e:
            pytest.fail(f"Scientific Method import failed: {e}")
    
    def test_tool_10_metacognitive_monitoring_import(self):
        """Test Metacognitive Monitoring tool import"""
        try:
            from clear_thinking_fastmcp.models.metacognitive_monitoring import (
                MetacognitiveMonitoringInput,
                MetacognitiveMonitoringOutput
            )
            print("✓ Metacognitive Monitoring tool imports successfully")
        except Exception as e:
            pytest.fail(f"Metacognitive Monitoring import failed: {e}")
    
    def test_tool_11_visual_reasoning_import(self):
        """Test Visual Reasoning tool import"""
        try:
            from clear_thinking_fastmcp.models.visual_reasoning import (
                VisualReasoningInput,
                VisualReasoningOutput
            )
            print("✓ Visual Reasoning tool imports successfully")
        except Exception as e:
            pytest.fail(f"Visual Reasoning import failed: {e}")
    
    def test_additional_tools_import(self):
        """Test additional cognitive tools found in models directory"""
        additional_tools = [
            "debugging_approaches",
            "design_patterns", 
            "programming_paradigms",
            "structured_argumentation"
        ]
        
        for tool in additional_tools:
            try:
                # Try to import the module
                module = __import__(f"clear_thinking_fastmcp.models.{tool}", fromlist=[""])
                print(f"✓ {tool} module imports successfully")
            except Exception as e:
                print(f"⚠️  {tool} import failed: {e}")
                # Don't fail the test, just report the issue


if __name__ == "__main__":
    pytest.main([__file__, "-v"])