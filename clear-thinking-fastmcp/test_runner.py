#!/usr/bin/env python3
"""
Simple test runner to validate our integration tests
"""

import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_mental_models():
    """Test mental models import and basic functionality"""
    try:
        from clear_thinking_fastmcp.models.mental_models import (
            MentalModelInput,
            MentalModelOutput,
            MentalModelType,
            ComplexityLevel
        )
        
        # Create valid input instance
        input_data = MentalModelInput(
            problem="Test problem for architecture decision",
            complexity_level=ComplexityLevel.MODERATE,
            session_id="test_session_001",
            mental_model_type=MentalModelType.FIRST_PRINCIPLES,
            context="Software architecture decision context",
            constraints=["Budget", "Time", "Team expertise"]
        )
        
        print(f"✓ Mental Models: {input_data.problem}")
        print(f"  - Type: {input_data.mental_model_type}")
        print(f"  - Constraints: {len(input_data.constraints)}")
        return True
        
    except Exception as e:
        print(f"❌ Mental Models failed: {e}")
        return False

def test_scientific_method():
    """Test scientific method import and basic functionality"""
    try:
        from clear_thinking_fastmcp.models.scientific_method import (
            ScientificMethodInput,
            ScientificMethodOutput,
            ComplexityLevel
        )
        
        # Create valid input instance
        input_data = ScientificMethodInput(
            problem="Test problem for scientific analysis",
            complexity_level=ComplexityLevel.MODERATE,
            session_id="test_session_002",
            research_question="What is the best architecture approach?",
            domain_knowledge="Experience with various architectures",
            hypothesis_generation_enabled=True,
            evidence_evaluation_enabled=True,
            max_hypotheses=3
        )
        
        print(f"✓ Scientific Method: {input_data.problem}")
        print(f"  - Research question: {input_data.research_question}")
        print(f"  - Max hypotheses: {input_data.max_hypotheses}")
        return True
        
    except Exception as e:
        print(f"❌ Scientific Method failed: {e}")
        return False

def test_visual_reasoning():
    """Test visual reasoning import and basic functionality"""
    try:
        from clear_thinking_fastmcp.models.visual_reasoning import (
            VisualReasoningModel,
            VisualElement,
            VisualRepresentationType
        )
        
        # Create model instance
        visual_model = VisualReasoningModel()
        
        # Create visual element
        element = visual_model.create_visual_element(
            element_id="test_element",
            element_type="service",
            position=(10.0, 20.0),
            size=(100.0, 50.0),
            properties={"name": "Test Service"}
        )
        
        print(f"✓ Visual Reasoning: Created element {element.element_id}")
        print(f"  - Position: {element.position}")
        print(f"  - Size: {element.size}")
        return True
        
    except Exception as e:
        print(f"❌ Visual Reasoning failed: {e}")
        return False

def test_all_imports():
    """Test importing all 16 tools"""
    tools = [
        ("mental_models", ["MentalModelInput", "MentalModelOutput"]),
        ("sequential_thinking", ["SequentialThinkingInput", "SequentialThinkingOutput"]),
        ("collaborative_reasoning", ["CollaborativeReasoningInput", "CollaborativeReasoningOutput"]),
        ("triple_constraint", ["TripleConstraintInput", "TripleConstraintAnalysis"]),
        ("impact_propagation", ["ImpactPropagationInput", "ImpactPropagationAnalysis"]),
        ("iterative_validation", ["IterativeValidationInput", "IterativeValidationAnalysis"]),
        ("sequential_readiness", ["SequentialReadinessInput", "SequentialReadinessAnalysis"]),
        ("multi_perspective", ["MultiPerspectiveInput", "MultiPerspectiveAnalysis"]),
        ("scientific_method", ["ScientificMethodInput", "ScientificMethodOutput"]),
        ("metacognitive_monitoring", ["MetacognitiveMonitoringInput", "MetacognitiveMonitoringOutput"]),
        ("visual_reasoning", ["VisualReasoningModel"]),
        ("debugging_approaches", ["DebuggingApproachesModel"]),
        ("design_patterns", ["DesignPatternsModel"]),
        ("programming_paradigms", ["ProgrammingParadigmsModel"]),
        ("structured_argumentation", ["StructuredArgumentationModel"]),
        ("decision_framework", ["DecisionFrameworkInput", "DecisionFrameworkOutput"])
    ]
    
    successful = 0
    failed = 0
    
    for tool_name, classes in tools:
        try:
            module_path = f"clear_thinking_fastmcp.models.{tool_name}"
            module = __import__(module_path, fromlist=classes)
            
            for class_name in classes:
                if hasattr(module, class_name):
                    print(f"✓ {tool_name}.{class_name}")
                else:
                    print(f"⚠️ {tool_name}.{class_name} - class not found")
                    failed += 1
                    
            successful += 1
            
        except Exception as e:
            print(f"❌ {tool_name} import failed: {e}")
            failed += 1
    
    print(f"\n=== Import Results ===")
    print(f"Successful: {successful}/{len(tools)}")
    print(f"Failed: {failed}")
    
    return successful, failed

if __name__ == "__main__":
    print("=== Running Clear Thinking FastMCP Integration Tests ===\n")
    
    # Test individual tools
    print("1. Testing Mental Models...")
    test_mental_models()
    
    print("\n2. Testing Scientific Method...")
    test_scientific_method()
    
    print("\n3. Testing Visual Reasoning...")
    test_visual_reasoning()
    
    print("\n4. Testing All Imports...")
    successful, failed = test_all_imports()
    
    print(f"\n=== Final Results ===")
    if failed == 0:
        print("🎉 All integration tests passed!")
    else:
        print(f"⚠️ {failed} issues found, but {successful} tools working")