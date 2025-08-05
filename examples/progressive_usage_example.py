"""
Example: Using Progressive Analyzers as Default

This example demonstrates how progressive analyzers can be used as the
default interface for all cognitive tools, providing both simple single-use
and complex multi-step workflows.
"""

import asyncio
from pyclarity.tools.progressive_defaults import create_memory_toolkit
from pyclarity.tools.mental_models.models import MentalModelType
from pyclarity.tools.decision_framework.models import DecisionType, EvaluationMethod
from pyclarity.tools.creative_thinking.models import CreativeMode, CreativeMethod


async def simple_single_use_example():
    """Example of simple, single-use analysis (no explicit session management)."""
    print("=== Simple Single-Use Example ===\n")
    
    # Create toolkit with in-memory stores
    toolkit = create_memory_toolkit()
    
    # Example 1: Mental Model Analysis
    print("1. Applying First Principles to a problem:")
    result = await toolkit.apply_mental_model(
        problem_statement="How to improve code review process?",
        model_type=MentalModelType.FIRST_PRINCIPLES,
        context="Development team of 10 engineers"
    )
    
    print(f"Session ID: {result['session_id']}")
    print(f"Key Components: {len(result['components'])}")
    print(f"Insights Generated: {len(result['insights'])}")
    print(f"First Insight: {result['insights'][0] if result['insights'] else 'None'}\n")
    
    # Example 2: Creative Thinking
    print("2. Generating creative ideas:")
    creative_result = await toolkit.generate_ideas(
        challenge="Make code reviews more engaging",
        creative_mode=CreativeMode.DIVERGENT,
        domain="software development"
    )
    
    print(f"New Ideas Generated: {creative_result['new_ideas_count']}")
    print(f"Innovation Potential: {creative_result['innovation_potential']:.2f}")
    if creative_result['promising_ideas']:
        print(f"Top Idea: {creative_result['promising_ideas'][0]['title']}\n")
    
    # Example 3: Decision Analysis
    print("3. Analyzing a decision:")
    decision_result = await toolkit.analyze_decision(
        decision_context="Choose between synchronous and asynchronous code reviews",
        decision_type=DecisionType.OPERATIONAL,
        criteria=[
            {"name": "Developer productivity", "weight": 0.3},
            {"name": "Code quality", "weight": 0.4},
            {"name": "Team collaboration", "weight": 0.3}
        ],
        alternatives=[
            {"name": "Synchronous reviews", "description": "Real-time pair reviews"},
            {"name": "Asynchronous reviews", "description": "GitHub PR-style reviews"}
        ]
    )
    
    print(f"Decision Readiness: {decision_result['decision_readiness']:.2%}")
    print(f"Recommended Action: {decision_result['recommended_action']}")
    print(f"Next Steps: {', '.join(decision_result['next_steps'][:2])}\n")


async def multi_step_session_example():
    """Example of multi-step analysis with explicit session management."""
    print("\n=== Multi-Step Session Example ===\n")
    
    toolkit = create_memory_toolkit()
    
    # Step 1: Start with debugging
    print("Step 1: Debugging a performance issue")
    debug_result = await toolkit.debug_issue(
        issue_description="Application response time increased by 300%",
        debugging_type="systematic",
        error_message="No explicit errors, just slow performance"
    )
    
    session_id = debug_result['session_id']
    print(f"Session ID: {session_id}")
    print(f"Initial Hypothesis: {debug_result['current_hypothesis']}")
    print(f"Evidence Needed: {', '.join(debug_result['evidence_needed'][:2])}\n")
    
    # Step 2: Continue with more evidence in same session
    print("Step 2: Adding evidence to the debugging session")
    debug_result2 = await toolkit.debug_issue(
        session_id=session_id,  # Continue same session
        issue_description="Application response time increased by 300%",
        step_number=2,
        evidence=["Database queries taking 2-3 seconds", "CPU usage normal"],
        hypothesis="Database performance degradation"
    )
    
    print(f"Updated Hypothesis: {debug_result2['current_hypothesis']}")
    print(f"Hypothesis Confidence: {debug_result2['hypothesis_confidence']:.2%}")
    print(f"Suggested Tests: {', '.join(debug_result2['suggested_tests'][:2])}\n")
    
    # Step 3: Use systems thinking to understand the broader impact
    print("Step 3: Analyzing system-wide impact")
    systems_result = await toolkit.analyze_system(
        system_name="Application Performance System",
        system_description="Web app with database, cache, and CDN",
        components=[
            {"name": "Database", "type": "storage", "health": 0.3},
            {"name": "Application Server", "type": "compute", "health": 0.9},
            {"name": "Cache Layer", "type": "storage", "health": 0.8}
        ],
        relationships=[
            {"from": "Application Server", "to": "Database", "type": "queries"},
            {"from": "Application Server", "to": "Cache Layer", "type": "reads"},
            {"from": "Cache Layer", "to": "Database", "type": "miss-fetch"}
        ]
    )
    
    print(f"System Health Score: {systems_result['system_health_score']:.2f}")
    print(f"Bottlenecks Found: {len(systems_result['bottlenecks'])}")
    if systems_result['bottlenecks']:
        print(f"Primary Bottleneck: {systems_result['bottlenecks'][0]}")
    print(f"Leverage Points: {', '.join(systems_result['leverage_points'][:2])}\n")


async def integrated_workflow_example():
    """Example of integrated workflow using multiple tools together."""
    print("\n=== Integrated Workflow Example ===\n")
    print("Scenario: Designing a new feature with full cognitive analysis\n")
    
    toolkit = create_memory_toolkit()
    
    # 1. Start with creative ideation
    print("Phase 1: Creative Ideation")
    creative_result = await toolkit.generate_ideas(
        challenge="Design a feature to improve developer productivity",
        creative_mode=CreativeMode.DIVERGENT,
        creative_methods=[CreativeMethod.BRAINSTORMING, CreativeMethod.SCAMPER]
    )
    session_id = creative_result['session_id']
    print(f"Ideas Generated: {creative_result['new_ideas_count']}")
    
    # 2. Apply mental models to the best idea
    print("\nPhase 2: Mental Model Analysis")
    if creative_result['promising_ideas']:
        best_idea = creative_result['promising_ideas'][0]
        mental_result = await toolkit.apply_mental_model(
            problem_statement=f"How to implement: {best_idea['title']}",
            model_type=MentalModelType.SYSTEMS_THINKING,
            context="Feature design phase"
        )
        print(f"System Components Identified: {len(mental_result['components'])}")
        print(f"Key Relationships: {len(mental_result['relationships'])}")
    
    # 3. Collaborative reasoning to refine
    print("\nPhase 3: Collaborative Refinement")
    collab_result = await toolkit.collaborate(
        topic=f"Refining feature: {best_idea['title']}",
        context="Cross-functional team input needed",
        personas=[
            {"name": "Developer", "expertise": "Implementation feasibility"},
            {"name": "Product Manager", "expertise": "User value"},
            {"name": "UX Designer", "expertise": "User experience"}
        ]
    )
    print(f"Active Personas: {len(collab_result['active_personas'])}")
    print(f"Consensus Level: {collab_result['consensus_level']:.2%}")
    
    # 4. Decision framework for go/no-go
    print("\nPhase 4: Decision Analysis")
    decision_result = await toolkit.analyze_decision(
        decision_context=f"Should we build: {best_idea['title']}",
        decision_type=DecisionType.STRATEGIC,
        criteria=[
            {"name": "Development effort", "weight": 0.25},
            {"name": "User impact", "weight": 0.35},
            {"name": "Technical complexity", "weight": 0.2},
            {"name": "Strategic alignment", "weight": 0.2}
        ],
        alternatives=[
            {"name": "Build now", "description": "Start development immediately"},
            {"name": "Prototype first", "description": "Build MVP for validation"},
            {"name": "Defer", "description": "Wait for next quarter"}
        ],
        evaluation_method=EvaluationMethod.WEIGHTED_CRITERIA
    )
    
    print(f"Recommended: {decision_result['recommended_action']}")
    print(f"Decision Confidence: {decision_result['decision_readiness']:.2%}")
    
    # 5. Metacognitive reflection
    print("\nPhase 5: Metacognitive Reflection")
    meta_result = await toolkit.monitor_thinking(
        current_thought="Reviewing the entire feature design process",
        thinking_context="Post-analysis reflection",
        confidence_level=0.8,
        clarity_level=0.9
    )
    print(f"Thinking Quality Score: {meta_result['thinking_quality_score']:.2f}")
    print(f"Biases Detected: {len(meta_result['biases_detected'])}")
    if meta_result['thinking_strategies']:
        print(f"Improvement Strategy: {meta_result['thinking_strategies'][0]}")


async def main():
    """Run all examples."""
    await simple_single_use_example()
    await multi_step_session_example()
    await integrated_workflow_example()
    
    print("\n=== Summary ===")
    print("Progressive analyzers provide:")
    print("1. Simple single-use interface (automatic session management)")
    print("2. Multi-step session support (explicit session continuity)")
    print("3. Cross-tool integration (share insights between tools)")
    print("4. Full progress tracking and evolution analysis")


if __name__ == "__main__":
    asyncio.run(main())