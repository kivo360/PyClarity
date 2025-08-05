#!/usr/bin/env python3
"""
Simple example demonstrating PyClarity Progressive Analyzers

This example shows how the progressive analyzers work as the default
implementation for all cognitive tools.
"""

import asyncio
import logging
from typing import Dict, Any

# Configure logging to see what's happening
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Import the toolkit
from pyclarity.tools.progressive_defaults import create_memory_toolkit
from pyclarity.tools.mental_models.models import MentalModelType
from pyclarity.tools.decision_framework.models import DecisionType
from pyclarity.tools.creative_thinking.models import CreativeMode


async def example_1_simple_analysis():
    """Example 1: Simple single-use analysis"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Simple Mental Model Analysis")
    print("="*60 + "\n")
    
    # Create in-memory toolkit (no database needed for demo)
    toolkit = create_memory_toolkit()
    
    # Apply first principles thinking
    result = await toolkit.apply_mental_model(
        problem_statement="How can we improve code review efficiency?",
        model_type=MentalModelType.FIRST_PRINCIPLES,
        context="Development team of 10 engineers, averaging 5 PRs per day"
    )
    
    print(f"✅ Analysis Complete!")
    print(f"📍 Session ID: {result['session_id']}")
    print(f"🔍 Step Number: {result['step_number']}")
    print(f"\n📊 Components Found: {len(result.get('components', []))}")
    
    if result.get('components'):
        print("\n🧩 Key Components:")
        for i, comp in enumerate(result['components'][:3], 1):
            print(f"  {i}. {comp['name']}: {comp['description'][:50]}...")
    
    if result.get('insights'):
        print("\n💡 Key Insights:")
        for i, insight in enumerate(result['insights'][:3], 1):
            print(f"  {i}. {insight}")
    
    return result


async def example_2_progressive_session():
    """Example 2: Progressive multi-step analysis"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Progressive Multi-Step Debugging")
    print("="*60 + "\n")
    
    toolkit = create_memory_toolkit()
    
    # Step 1: Initial problem analysis
    print("🔍 Step 1: Initial Problem Analysis")
    debug_result = await toolkit.debug_issue(
        issue_description="API response times have increased from 200ms to 2s",
        debugging_type="systematic"
    )
    
    session_id = debug_result['session_id']
    print(f"📍 Session ID: {session_id}")
    print(f"🎯 Initial Hypothesis: {debug_result.get('current_hypothesis', 'None')}")
    print(f"📋 Evidence Needed: {', '.join(debug_result.get('evidence_needed', [])[:3])}")
    
    # Step 2: Add evidence
    print("\n🔍 Step 2: Adding Evidence")
    debug_result2 = await toolkit.debug_issue(
        session_id=session_id,  # Continue same session
        step_number=2,
        evidence=["Database queries taking 1.8s", "No increase in traffic"],
        hypothesis="Database performance issue"
    )
    
    print(f"🎯 Updated Hypothesis: {debug_result2.get('current_hypothesis', 'None')}")
    print(f"📊 Confidence: {debug_result2.get('hypothesis_confidence', 0):.0%}")
    print(f"🧪 Suggested Tests:")
    for i, test in enumerate(debug_result2.get('suggested_tests', [])[:3], 1):
        print(f"  {i}. {test}")
    
    return debug_result2


async def example_3_cross_tool_workflow():
    """Example 3: Using multiple tools together"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Cross-Tool Workflow")
    print("="*60 + "\n")
    
    toolkit = create_memory_toolkit()
    
    # Phase 1: Creative ideation
    print("💡 Phase 1: Creative Ideation")
    creative_result = await toolkit.generate_ideas(
        challenge="Design a feature to reduce context switching for developers",
        creative_mode=CreativeMode.DIVERGENT
    )
    
    print(f"✨ Generated {creative_result['new_ideas_count']} new ideas")
    print(f"🚀 Innovation Potential: {creative_result['innovation_potential']:.0%}")
    
    if creative_result.get('promising_ideas'):
        best_idea = creative_result['promising_ideas'][0]
        print(f"\n🏆 Top Idea: {best_idea['title']}")
        print(f"   Score: {best_idea.get('score', 0):.2f}")
        
        # Phase 2: Decision analysis on the best idea
        print(f"\n📊 Phase 2: Decision Analysis")
        decision_result = await toolkit.analyze_decision(
            decision_context=f"Should we implement: {best_idea['title']}",
            decision_type=DecisionType.TACTICAL,
            criteria=[
                {"name": "Development Effort", "weight": 0.3, "description": "Time and resources needed"},
                {"name": "User Impact", "weight": 0.4, "description": "Expected improvement in productivity"},
                {"name": "Risk", "weight": 0.3, "description": "Technical and adoption risks"}
            ],
            alternatives=[
                {"name": "Implement Now", "description": "Start development immediately"},
                {"name": "Prototype First", "description": "Build a minimal proof of concept"},
                {"name": "Research More", "description": "Conduct user studies first"}
            ]
        )
        
        print(f"🎯 Recommended: {decision_result.get('recommended_action', 'None')}")
        print(f"📈 Decision Readiness: {decision_result.get('decision_readiness', 0):.0%}")
        
        if decision_result.get('evaluated_alternatives'):
            print("\n📊 Alternative Scores:")
            for alt in decision_result['evaluated_alternatives']:
                print(f"  • {alt['name']}: {alt.get('total_score', 0):.2f}")
    
    return creative_result, decision_result if 'decision_result' in locals() else None


async def example_4_session_details():
    """Example 4: Examining session details"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Session Management Details")
    print("="*60 + "\n")
    
    toolkit = create_memory_toolkit()
    
    # Start a systems thinking analysis
    systems_result = await toolkit.analyze_system(
        system_name="Software Development Pipeline",
        system_description="CI/CD pipeline with testing, building, and deployment stages",
        components=[
            {"name": "Source Control", "type": "input", "description": "Git repository"},
            {"name": "CI Server", "type": "processor", "description": "Jenkins/GitHub Actions"},
            {"name": "Test Suite", "type": "validator", "description": "Unit and integration tests"},
            {"name": "Build System", "type": "processor", "description": "Compilation and packaging"},
            {"name": "Deployment", "type": "output", "description": "Production deployment"}
        ]
    )
    
    print(f"🔧 System Analysis Complete")
    print(f"📍 Session ID: {systems_result['session_id']}")
    print(f"💯 System Health: {systems_result.get('system_health_score', 0):.0%}")
    
    if systems_result.get('bottlenecks'):
        print(f"\n🚧 Bottlenecks Found: {len(systems_result['bottlenecks'])}")
        for bottleneck in systems_result['bottlenecks'][:2]:
            print(f"  • {bottleneck}")
    
    if systems_result.get('leverage_points'):
        print(f"\n🎯 Leverage Points:")
        for point in systems_result['leverage_points'][:3]:
            print(f"  • {point}")
    
    print("\n📝 Session Benefits:")
    print("  ✓ Automatic session creation and management")
    print("  ✓ Progress tracking across steps")
    print("  ✓ Rich insights and recommendations")
    print("  ✓ Can continue analysis in future steps")
    
    return systems_result


async def main():
    """Run all examples"""
    print("\n🚀 PyClarity Progressive Analyzers Demo")
    print("=====================================")
    print("This demo shows progressive analyzers as the default tool implementation.")
    print("No database required - using in-memory stores for this demo.\n")
    
    try:
        # Run examples
        await example_1_simple_analysis()
        await example_2_progressive_session()
        await example_3_cross_tool_workflow()
        await example_4_session_details()
        
        print("\n" + "="*60)
        print("✅ Demo Complete!")
        print("="*60)
        print("\nKey Takeaways:")
        print("• Progressive analyzers provide rich, multi-step analysis")
        print("• Sessions are managed automatically")
        print("• Tools can be used for both simple and complex workflows")
        print("• Cross-tool integration enables powerful workflows")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())