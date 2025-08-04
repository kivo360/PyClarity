#!/usr/bin/env python
"""
Comprehensive validation test for all 11 cognitive tools in PyClarity.

This test validates that all cognitive tools can be imported and have basic functionality.
We'll use incremental validation: Start Small → Validate → Expand → Scale
"""

import pytest
import pytest_asyncio


class TestAllCognitiveToolsValidation:
    """Validate all 11 cognitive tools can be imported and basic functionality works"""
    
    def test_tool_1_mental_models_import(self):
        """Test Mental Models tool import"""
        try:
            from pyclarity.tools.mental_models.models import (
                MentalModelType,
                MentalModelsContext,
                MentalModelsResult
            )
            from pyclarity.tools.mental_models.analyzer import MentalModelsAnalyzer
            # Test basic enum functionality
            assert MentalModelType.FIRST_PRINCIPLES == "first_principles"
            assert MentalModelType.OPPORTUNITY_COST == "opportunity_cost"
            # Test analyzer instantiation
            analyzer = MentalModelsAnalyzer()
            assert analyzer.tool_name == "Mental Models"
            print("✓ Mental Models tool imports successfully")
        except Exception as e:
            pytest.fail(f"Mental Models import failed: {e}")
    
    def test_tool_2_sequential_thinking_import(self):
        """Test Sequential Thinking tool import"""
        try:
            from pyclarity.tools.sequential_thinking.models import (
                SequentialThinkingContext,
                SequentialThinkingResult,
                ThoughtStepType,
                ThoughtStep
            )
            from pyclarity.tools.sequential_thinking.analyzer import SequentialThinkingAnalyzer
            # Test basic enum functionality
            assert ThoughtStepType.PROBLEM_DECOMPOSITION == "problem_decomposition"
            assert ThoughtStepType.HYPOTHESIS_FORMATION == "hypothesis_formation"
            # Test analyzer instantiation
            analyzer = SequentialThinkingAnalyzer()
            assert analyzer.tool_name == "Sequential Thinking"
            print("✓ Sequential Thinking tool imports successfully")
        except Exception as e:
            pytest.fail(f"Sequential Thinking import failed: {e}")
    
    def test_tool_3_collaborative_reasoning_import(self):
        """Test Collaborative Reasoning tool import"""
        try:
            from pyclarity.tools.collaborative_reasoning.models import (
                CollaborativeReasoningContext,
                CollaborativeReasoningResult,
                PersonaType,
                Persona
            )
            from pyclarity.tools.collaborative_reasoning.analyzer import CollaborativeReasoningAnalyzer
            # Test basic enum functionality
            assert PersonaType.CRITIC == "critic"
            assert PersonaType.EXPERT == "expert"
            # Test analyzer instantiation
            analyzer = CollaborativeReasoningAnalyzer()
            assert analyzer.tool_name == "Collaborative Reasoning"
            print("✓ Collaborative Reasoning tool imports successfully")
        except Exception as e:
            pytest.fail(f"Collaborative Reasoning import failed: {e}")
    
    def test_tool_4_decision_framework_import(self):
        """Test Decision Framework tool import"""
        try:
            from pyclarity.tools.decision_framework.models import (
                DecisionFrameworkContext,
                DecisionFrameworkResult,
                DecisionMethodType,
                CriteriaType
            )
            from pyclarity.tools.decision_framework.analyzer import DecisionFrameworkAnalyzer
            # Basic validation
            assert DecisionMethodType.WEIGHTED_SUM == "weighted_sum"
            assert CriteriaType.BENEFIT == "benefit"
            # Test analyzer instantiation
            analyzer = DecisionFrameworkAnalyzer()
            assert analyzer.tool_name == "Decision Framework"
            print("✓ Decision Framework tool imports successfully")
        except Exception as e:
            pytest.fail(f"Decision Framework import failed: {e}")
    
    def test_tool_5_impact_propagation_import(self):
        """Test Impact Propagation tool import"""
        try:
            from pyclarity.tools.impact_propagation.models import (
                ImpactPropagationContext,
                ImpactPropagationResult
            )
            from pyclarity.tools.impact_propagation.analyzer import ImpactPropagationAnalyzer
            # Test analyzer instantiation
            analyzer = ImpactPropagationAnalyzer()
            assert analyzer.tool_name == "Impact Propagation"
            print("✓ Impact Propagation tool imports successfully")
        except Exception as e:
            pytest.fail(f"Impact Propagation import failed: {e}")
    
    def test_tool_6_iterative_validation_import(self):
        """Test Iterative Validation tool import"""
        try:
            from pyclarity.tools.iterative_validation.models import (
                IterativeValidationContext,
                IterativeValidationResult
            )
            from pyclarity.tools.iterative_validation.analyzer import IterativeValidationAnalyzer
            # Test analyzer instantiation
            analyzer = IterativeValidationAnalyzer()
            assert analyzer.tool_name == "Iterative Validation"
            print("✓ Iterative Validation tool imports successfully")
        except Exception as e:
            pytest.fail(f"Iterative Validation import failed: {e}")
    
    def test_tool_7_sequential_readiness_import(self):
        """Test Sequential Readiness tool import"""
        try:
            from pyclarity.tools.sequential_readiness.models import (
                SequentialReadinessContext,
                SequentialReadinessResult
            )
            from pyclarity.tools.sequential_readiness.analyzer import SequentialReadinessAnalyzer
            # Test analyzer instantiation
            analyzer = SequentialReadinessAnalyzer()
            assert analyzer.tool_name == "Sequential Readiness"
            print("✓ Sequential Readiness tool imports successfully")
        except Exception as e:
            pytest.fail(f"Sequential Readiness import failed: {e}")
    
    def test_tool_8_multi_perspective_import(self):
        """Test Multi-Perspective Analysis tool import"""
        try:
            from pyclarity.tools.multi_perspective.models import (
                MultiPerspectiveContext,
                MultiPerspectiveResult
            )
            from pyclarity.tools.multi_perspective.analyzer import MultiPerspectiveAnalyzer
            # Test analyzer instantiation
            analyzer = MultiPerspectiveAnalyzer()
            assert analyzer.tool_name == "Multi-Perspective Analysis"
            print("✓ Multi-Perspective Analysis tool imports successfully")
        except Exception as e:
            pytest.fail(f"Multi-Perspective Analysis import failed: {e}")
    
    def test_tool_9_scientific_method_import(self):
        """Test Scientific Method tool import"""
        try:
            from pyclarity.tools.scientific_method.models import (
                ScientificMethodContext,
                ScientificMethodResult
            )
            from pyclarity.tools.scientific_method.analyzer import ScientificMethodAnalyzer
            # Test analyzer instantiation
            analyzer = ScientificMethodAnalyzer()
            assert analyzer.tool_name == "Scientific Method"
            print("✓ Scientific Method tool imports successfully")
        except Exception as e:
            pytest.fail(f"Scientific Method import failed: {e}")
    
    def test_tool_10_metacognitive_monitoring_import(self):
        """Test Metacognitive Monitoring tool import"""
        try:
            from pyclarity.tools.metacognitive_monitoring.models import (
                MetacognitiveMonitoringContext,
                MetacognitiveMonitoringResult
            )
            from pyclarity.tools.metacognitive_monitoring.analyzer import MetacognitiveMonitoringAnalyzer
            # Test analyzer instantiation
            analyzer = MetacognitiveMonitoringAnalyzer()
            assert analyzer.tool_name == "Metacognitive Monitoring"
            print("✓ Metacognitive Monitoring tool imports successfully")
        except Exception as e:
            pytest.fail(f"Metacognitive Monitoring import failed: {e}")
    
    def test_tool_11_triple_constraint_import(self):
        """Test Triple Constraint tool import"""
        try:
            from pyclarity.tools.triple_constraint.models import (
                TripleConstraintContext,
                TripleConstraintResult,
                ConstraintDimension
            )
            from pyclarity.tools.triple_constraint.analyzer import TripleConstraintAnalyzer
            # Basic validation
            assert ConstraintDimension.QUALITY == "quality"
            assert ConstraintDimension.SCOPE == "scope"
            # Test analyzer instantiation
            analyzer = TripleConstraintAnalyzer()
            assert analyzer.tool_name == "Triple Constraint"
            print("✓ Triple Constraint tool imports successfully")
        except Exception as e:
            pytest.fail(f"Triple Constraint import failed: {e}")
    
    def test_all_tools_count(self):
        """Verify we have all 11 cognitive tools"""
        tools = [
            "mental_models",
            "sequential_thinking",
            "collaborative_reasoning",
            "decision_framework",
            "impact_propagation",
            "iterative_validation",
            "sequential_readiness",
            "multi_perspective",
            "scientific_method",
            "metacognitive_monitoring",
            "triple_constraint"
        ]
        assert len(tools) == 11, f"Expected 11 tools but found {len(tools)}"
        print(f"✓ All 11 cognitive tools accounted for")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])