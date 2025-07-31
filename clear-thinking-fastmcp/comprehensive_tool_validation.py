#!/usr/bin/env python
"""
Comprehensive validation script for all Clear Thinking FastMCP cognitive tools.

This script follows the incremental approach: Start Small → Validate → Expand → Scale
"""

import sys
from pathlib import Path
import importlib
import traceback

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# List of expected cognitive tools
COGNITIVE_TOOLS = [
    "mental_models",
    "sequential_thinking", 
    "collaborative_reasoning",
    "triple_constraint",
    "impact_propagation",
    "iterative_validation",
    "sequential_readiness",
    "multi_perspective",
    "scientific_method",
    "metacognitive_monitoring",
    "visual_reasoning",
    "debugging_approaches",
    "design_patterns",
    "programming_paradigms",
    "structured_argumentation",
    "decision_framework"
]

def validate_tool(tool_name):
    """Validate a single cognitive tool"""
    print(f"\n🔍 Testing {tool_name}...")
    
    try:
        # Try to import the module
        module_name = f"clear_thinking_fastmcp.models.{tool_name}"
        module = importlib.import_module(module_name)
        
        # Check for basic classes (Input, Output)
        input_class = None
        output_class = None
        enums_found = []
        
        # Look for common patterns
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            
            # Check for Input/Output classes
            if attr_name.endswith('Input') and hasattr(attr, '__bases__'):
                input_class = attr_name
            elif attr_name.endswith('Output') and hasattr(attr, '__bases__'):
                output_class = attr_name
            elif hasattr(attr, '__bases__') and any('Enum' in str(base) for base in attr.__bases__):
                enums_found.append(attr_name)
        
        # Try to create instances if possible
        validation_results = {
            'import_success': True,
            'input_class': input_class,
            'output_class': output_class,
            'enums_found': enums_found,
            'total_classes': len([name for name in dir(module) if not name.startswith('_') and hasattr(getattr(module, name), '__bases__')]),
            'pydantic_v2_compatible': True  # Will be set to False if validation fails
        }
        
        # Test basic Pydantic functionality if Input class exists
        if input_class:
            try:
                input_cls = getattr(module, input_class)
                # Try to examine the model fields (Pydantic V2 way)
                if hasattr(input_cls, 'model_fields'):
                    validation_results['pydantic_fields'] = len(input_cls.model_fields)
                else:
                    validation_results['pydantic_fields'] = 'unknown'
            except Exception as e:
                validation_results['pydantic_v2_compatible'] = False
                validation_results['pydantic_error'] = str(e)
        
        print(f"✅ {tool_name}: SUCCESS")
        print(f"   - Input class: {input_class}")
        print(f"   - Output class: {output_class}")  
        print(f"   - Enums found: {len(enums_found)} ({', '.join(enums_found[:3])}{'...' if len(enums_found) > 3 else ''})")
        print(f"   - Total classes: {validation_results['total_classes']}")
        print(f"   - Pydantic V2 compatible: {validation_results['pydantic_v2_compatible']}")
        
        return True, validation_results
        
    except Exception as e:
        print(f"❌ {tool_name}: FAILED")
        print(f"   Error: {str(e)}")
        print(f"   Type: {type(e).__name__}")
        if "validator" in str(e).lower() or "pydantic" in str(e).lower():
            print("   🔧 Likely Pydantic V2 compatibility issue")
        return False, {'error': str(e), 'error_type': type(e).__name__}

def main():
    """Main validation function"""
    print("🚀 Starting comprehensive Clear Thinking FastMCP tool validation")
    print(f"📋 Testing {len(COGNITIVE_TOOLS)} cognitive tools...")
    
    results = {}
    successful = 0
    failed = 0
    pydantic_issues = 0
    
    for tool in COGNITIVE_TOOLS:
        success, details = validate_tool(tool)
        results[tool] = details
        
        if success:
            successful += 1
            if not details.get('pydantic_v2_compatible', True):
                pydantic_issues += 1
        else:
            failed += 1
            if 'pydantic' in details.get('error', '').lower():
                pydantic_issues += 1
    
    # Summary
    print("\n" + "="*60)
    print("📊 VALIDATION SUMMARY")
    print("="*60)
    print(f"✅ Successful imports: {successful}/{len(COGNITIVE_TOOLS)}")
    print(f"❌ Failed imports: {failed}/{len(COGNITIVE_TOOLS)}")
    print(f"🔧 Pydantic V2 issues: {pydantic_issues}/{len(COGNITIVE_TOOLS)}")
    
    if failed > 0:
        print(f"\n🔍 Failed tools:")
        for tool, details in results.items():
            if 'error' in details:
                print(f"   - {tool}: {details['error_type']}")
    
    if pydantic_issues > 0:
        print(f"\n🔧 Tools needing Pydantic V2 fixes:")
        for tool, details in results.items():
            if not details.get('pydantic_v2_compatible', True):
                print(f"   - {tool}")
    
    # Success rate
    success_rate = (successful / len(COGNITIVE_TOOLS)) * 100
    print(f"\n📈 Overall success rate: {success_rate:.1f}%")
    
    if success_rate >= 80:
        print("🎉 Excellent! Most tools are working")
    elif success_rate >= 60:
        print("👍 Good progress, some fixes needed")
    else:
        print("🚨 Significant issues found, major fixes needed")
    
    return results

if __name__ == "__main__":
    results = main()