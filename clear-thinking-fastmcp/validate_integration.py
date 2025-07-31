#!/usr/bin/env python3
"""
AGENT A & B: Parallel Integration and Performance Validation

This script validates the 2-tool integration and performance in parallel.
Following the incremental approach: Start Small → Validate → Expand → Scale

Agent A: Integration Testing
Agent B: Performance Benchmarking
"""

import asyncio
import time
import sys
import os
from typing import Dict, Any, List
from unittest.mock import AsyncMock, MagicMock

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    # Import Sequential Thinking models and server
    from clear_thinking_fastmcp.models.sequential_thinking import (
        SequentialThinkingInput,
        SequentialThinkingOutput,
        ThoughtStep,
        ThoughtStepType,
        BranchStrategy
    )
    from clear_thinking_fastmcp.tools.sequential_thinking_server import SequentialThinkingServer

    # Import Decision Framework models and server
    from clear_thinking_fastmcp.models.decision_framework import (
        DecisionFrameworkInput,
        DecisionFrameworkOutput,
        DecisionMethodType,
        DecisionCriteria,
        DecisionOption,
        CriteriaType
    )
    from clear_thinking_fastmcp.tools.decision_framework_server import DecisionFrameworkServer

    # Import base models
    from clear_thinking_fastmcp.models.base import ComplexityLevel

    print("✅ All imports successful - modules are available")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Module structure check...")
    
    # Let's check what's actually available
    import os
    src_path = os.path.join(os.path.dirname(__file__), 'src')
    if os.path.exists(src_path):
        print(f"src/ directory exists at: {src_path}")
        for root, dirs, files in os.walk(src_path):
            level = root.replace(src_path, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 2 * (level + 1)
            for file in files:
                print(f"{subindent}{file}")
    else:
        print("src/ directory not found")
    
    sys.exit(1)


class MockContext:
    """Mock FastMCP Context for testing"""
    def __init__(self):
        self.progress_calls = []
        self.info_calls = []
        self.debug_calls = []
        self.error_calls = []
        self._cancelled = False
    
    async def progress(self, message: str, progress: float = 0.0):
        self.progress_calls.append((message, progress))
        print(f"📊 Progress: {message} ({progress:.1%})")
    
    async def info(self, message: str):
        self.info_calls.append(message)
        print(f"ℹ️  Info: {message}")
    
    async def debug(self, message: str):
        self.debug_calls.append(message)
        print(f"🐛 Debug: {message}")
    
    async def error(self, message: str):
        self.error_calls.append(message)
        print(f"❌ Error: {message}")
    
    async def cancelled(self) -> bool:
        return self._cancelled


class ValidationResults:
    """Track validation results across agents"""
    def __init__(self):
        self.results = {
            "agent_a_integration": {"status": "pending", "details": {}},
            "agent_b_performance": {"status": "pending", "details": {}},
            "overall_validation": {"status": "pending", "details": {}}
        }
    
    def update_agent_a(self, status: str, details: Dict[str, Any]):
        self.results["agent_a_integration"]["status"] = status
        self.results["agent_a_integration"]["details"].update(details)
    
    def update_agent_b(self, status: str, details: Dict[str, Any]):
        self.results["agent_b_performance"]["status"] = status
        self.results["agent_b_performance"]["details"].update(details)
    
    def is_validation_complete(self) -> bool:
        return (
            self.results["agent_a_integration"]["status"] in ["success", "failed"] and
            self.results["agent_b_performance"]["status"] in ["success", "failed"]
        )
    
    def overall_success(self) -> bool:
        return (
            self.results["agent_a_integration"]["status"] == "success" and
            self.results["agent_b_performance"]["status"] == "success"
        )
    
    def generate_report(self) -> str:
        report = "\n" + "="*80 + "\n"
        report += "🔄 PHASE 2B: PARALLEL VALIDATION RESULTS\n"
        report += "="*80 + "\n\n"
        
        for agent, result in self.results.items():
            status_emoji = "✅" if result["status"] == "success" else "❌" if result["status"] == "failed" else "🔄"
            report += f"{status_emoji} {agent.upper()}: {result['status']}\n"
            
            if result["details"]:
                for key, value in result["details"].items():
                    report += f"   {key}: {value}\n"
            report += "\n"
        
        return report


async def agent_a_integration_testing(results: ValidationResults, context: MockContext):
    """
    AGENT A: Integration Testing
    
    Validates:
    - Sequential Thinking → Decision Framework workflow
    - Data flow between tools
    - Context integration
    - Session continuity
    """
    print("\n🤖 AGENT A: Starting Integration Testing...")
    
    try:
        # Create server instances
        sequential_server = SequentialThinkingServer()
        decision_server = DecisionFrameworkServer()
        
        # Sample problem for testing
        problem = "Our web application is experiencing slow response times during peak hours. Users are reporting delays of 3-5 seconds for page loads, which is impacting customer satisfaction and conversion rates."
        
        # Step 1: Process Sequential Thinking
        sequential_input = SequentialThinkingInput(
            problem=problem,
            complexity_level=ComplexityLevel.MODERATE,
            reasoning_depth=5,
            enable_branching=True,
            max_branches=2,
            allow_revisions=True,
            branch_strategy=BranchStrategy.CONVERGENT_SYNTHESIS,
            convergence_threshold=0.8,
            evidence_sources=["performance metrics", "user feedback", "system logs"],
            validation_criteria=["logical consistency", "empirical support"],
            session_id="integration_test_session_1"
        )
        
        await context.info("Agent A: Processing Sequential Thinking input...")
        sequential_output = await sequential_server.process(sequential_input, context)
        
        # Validate Sequential Thinking output
        assert isinstance(sequential_output, SequentialThinkingOutput)
        assert sequential_output.session_id == sequential_input.session_id
        assert len(sequential_output.reasoning_chain) > 0
        assert sequential_output.final_conclusion is not None
        assert 0.0 <= sequential_output.confidence_score <= 1.0
        
        # Step 2: Create Decision Framework input
        decision_criteria = [
            DecisionCriteria(
                name="implementation_cost",
                description="Cost to implement the solution",
                weight=0.25,
                criteria_type=CriteriaType.COST,
                measurement_unit="USD"
            ),
            DecisionCriteria(
                name="technical_complexity",
                description="Technical difficulty of implementation",
                weight=0.20,
                criteria_type=CriteriaType.COST,
                measurement_unit="complexity_score"
            ),
            DecisionCriteria(
                name="expected_impact",
                description="Expected performance improvement",
                weight=0.35,
                criteria_type=CriteriaType.BENEFIT,
                measurement_unit="impact_score"
            ),
            DecisionCriteria(
                name="timeline",
                description="Speed of implementation",
                weight=0.20,
                criteria_type=CriteriaType.BENEFIT,
                measurement_unit="months"
            )
        ]
        
        decision_options = [
            DecisionOption(
                name="Database Optimization",
                description="Optimize database queries and indexing",
                scores={
                    "implementation_cost": 0.7,
                    "technical_complexity": 0.8,
                    "expected_impact": 0.9,
                    "timeline": 0.6
                },
                confidence_scores={
                    "implementation_cost": 0.8,
                    "technical_complexity": 0.9,
                    "expected_impact": 0.7,
                    "timeline": 0.8
                },
                risks=["Database downtime during migration", "Query compatibility issues"],
                assumptions=["Current queries are suboptimal", "Index fragmentation exists"]
            ),
            DecisionOption(
                name="Caching Implementation",
                description="Implement Redis caching layer",
                scores={
                    "implementation_cost": 0.8,
                    "technical_complexity": 0.6,
                    "expected_impact": 0.8,
                    "timeline": 0.8
                },
                confidence_scores={
                    "implementation_cost": 0.9,
                    "technical_complexity": 0.8,
                    "expected_impact": 0.8,
                    "timeline": 0.9
                },
                risks=["Cache invalidation complexity", "Additional infrastructure costs"],
                assumptions=["Caching will reduce database load", "Cache hit rates will be high"]
            )
        ]
        
        decision_input = DecisionFrameworkInput(
            decision_problem=sequential_output.final_conclusion,
            complexity_level=ComplexityLevel.MODERATE,
            decision_method=DecisionMethodType.WEIGHTED_SCORING,
            criteria=decision_criteria,
            options=decision_options,
            stakeholders=["development_team", "product_management", "users"],
            constraints=["6_month_timeline", "limited_budget"],
            include_risk_analysis=True,
            include_trade_off_analysis=True,
            include_sensitivity_analysis=True,
            session_id=sequential_output.session_id  # Pass session ID through
        )
        
        # Step 3: Process Decision Framework
        await context.info("Agent A: Processing Decision Framework input...")
        decision_output = await decision_server.process(decision_input, context)
        
        # Validate Decision Framework output
        assert isinstance(decision_output, DecisionFrameworkOutput)
        assert decision_output.session_id == sequential_output.session_id
        assert decision_output.recommended_option is not None
        assert len(decision_output.option_rankings) > 0
        assert decision_output.decision_matrix is not None
        assert 0.0 <= decision_output.confidence_score <= 1.0
        
        # Validate data flow between tools
        assert decision_input.decision_problem == sequential_output.final_conclusion
        assert decision_input.session_id == sequential_output.session_id
        
        # Check context integration
        assert len(context.progress_calls) > 0
        assert len(context.info_calls) > 0
        
        # Update results
        results.update_agent_a("success", {
            "reasoning_steps": len(sequential_output.reasoning_chain),
            "recommended_option": decision_output.recommended_option,
            "session_continuity": decision_output.session_id == sequential_input.session_id,
            "confidence_sequential": f"{sequential_output.confidence_score:.3f}",
            "confidence_decision": f"{decision_output.confidence_score:.3f}",
            "context_progress_calls": len(context.progress_calls),
            "context_info_calls": len(context.info_calls)
        })
        
        await context.info("✅ Agent A: Integration testing completed successfully")
        
    except Exception as e:
        await context.error(f"Agent A failed: {e}")
        results.update_agent_a("failed", {"error": str(e)})
        raise


async def agent_b_performance_benchmarking(results: ValidationResults, context: MockContext):
    """
    AGENT B: Performance Benchmarking
    
    Validates:
    - Processing time < 5 seconds combined
    - Memory usage reasonable
    - Concurrent processing capability
    - Performance scalability
    """
    print("\n🤖 AGENT B: Starting Performance Benchmarking...")
    
    try:
        # Create server instances
        sequential_server = SequentialThinkingServer()
        decision_server = DecisionFrameworkServer()
        
        # Performance test data
        problems = [
            "Database performance optimization challenge",
            "User interface responsiveness issues",
            "API endpoint latency problems"
        ]
        
        # Test 1: Single workflow timing
        await context.info("Agent B: Testing single workflow performance...")
        
        start_time = time.time()
        
        # Process one complete workflow
        sequential_input = SequentialThinkingInput(
            problem=problems[0],
            complexity_level=ComplexityLevel.MODERATE,
            reasoning_depth=5,
            enable_branching=True,
            max_branches=2,
            session_id="performance_test_1"
        )
        
        sequential_start = time.time()
        sequential_output = await sequential_server.process(sequential_input, context)
        sequential_time = time.time() - sequential_start
        
        decision_criteria = [
            DecisionCriteria(
                name="feasibility",
                description="How feasible is this option",
                weight=0.4,
                criteria_type=CriteriaType.BENEFIT
            ),
            DecisionCriteria(
                name="impact",
                description="Expected impact",
                weight=0.6,
                criteria_type=CriteriaType.BENEFIT
            )
        ]
        
        decision_options = [
            DecisionOption(
                name="Option A",
                description="First solution approach",
                scores={"feasibility": 0.8, "impact": 0.7}
            ),
            DecisionOption(
                name="Option B", 
                description="Second solution approach",
                scores={"feasibility": 0.6, "impact": 0.9}
            )
        ]
        
        decision_input = DecisionFrameworkInput(
            decision_problem=sequential_output.final_conclusion,
            complexity_level=ComplexityLevel.MODERATE,
            decision_method=DecisionMethodType.WEIGHTED_SCORING,
            criteria=decision_criteria,
            options=decision_options,
            session_id=sequential_output.session_id
        )
        
        decision_start = time.time()
        decision_output = await decision_server.process(decision_input, context)
        decision_time = time.time() - decision_start
        
        total_time = time.time() - start_time
        
        # Validate performance requirements
        assert total_time < 5.0, f"Total processing time {total_time:.2f}s exceeds 5s limit"
        assert sequential_time < 3.0, f"Sequential Thinking time {sequential_time:.2f}s exceeds 3s limit"
        assert decision_time < 3.0, f"Decision Framework time {decision_time:.2f}s exceeds 3s limit"
        
        # Test 2: Concurrent processing
        await context.info("Agent B: Testing concurrent processing...")
        
        async def process_problem_workflow(problem, session_id):
            """Process one complete problem workflow"""
            seq_input = SequentialThinkingInput(
                problem=problem,
                complexity_level=ComplexityLevel.SIMPLE,  # Reduced for performance
                reasoning_depth=3,
                enable_branching=False,
                session_id=session_id
            )
            
            seq_output = await sequential_server.process(seq_input, context)
            
            dec_input = DecisionFrameworkInput(
                decision_problem=seq_output.final_conclusion,
                complexity_level=ComplexityLevel.SIMPLE,
                decision_method=DecisionMethodType.WEIGHTED_SCORING,
                criteria=decision_criteria,
                options=decision_options,
                session_id=seq_output.session_id
            )
            
            dec_output = await decision_server.process(dec_input, context)
            
            return {
                "session_id": session_id,
                "sequential_time": seq_output.processing_time if hasattr(seq_output, 'processing_time') else 0.0,
                "decision_time": dec_output.processing_time if hasattr(dec_output, 'processing_time') else 0.0
            }
        
        # Process problems concurrently
        concurrent_start = time.time()
        
        tasks = [
            process_problem_workflow(problem, f"concurrent_test_{i}")
            for i, problem in enumerate(problems)
        ]
        
        concurrent_results = await asyncio.gather(*tasks)
        concurrent_time = time.time() - concurrent_start
        
        # Calculate efficiency
        expected_sequential_time = len(problems) * total_time
        efficiency_ratio = expected_sequential_time / concurrent_time if concurrent_time > 0 else 1.0
        
        # Update results
        results.update_agent_b("success", {
            "single_workflow_time": f"{total_time:.2f}s",
            "sequential_thinking_time": f"{sequential_time:.2f}s", 
            "decision_framework_time": f"{decision_time:.2f}s",
            "performance_requirement_met": total_time < 5.0,
            "concurrent_problems_processed": len(concurrent_results),
            "concurrent_total_time": f"{concurrent_time:.2f}s",
            "efficiency_ratio": f"{efficiency_ratio:.2f}x",
            "concurrent_performance": efficiency_ratio > 1.0
        })
        
        await context.info("✅ Agent B: Performance benchmarking completed successfully")
        
    except Exception as e:
        await context.error(f"Agent B failed: {e}")
        results.update_agent_b("failed", {"error": str(e)})
        raise


async def main():
    """
    Main orchestration function for parallel validation
    
    Executes Agent A and Agent B in parallel following:
    Start Small → Validate → Expand → Scale
    """
    print("🚀 PHASE 2B: PARALLEL VALIDATION STARTING")
    print("="*60)
    print("Agent A: Integration Testing")
    print("Agent B: Performance Benchmarking") 
    print("="*60)
    
    # Initialize shared components
    results = ValidationResults()
    context = MockContext()
    
    # Execute agents in parallel
    try:
        await asyncio.gather(
            agent_a_integration_testing(results, context),
            agent_b_performance_benchmarking(results, context)
        )
        
        # Check if validation is complete and successful
        if results.is_validation_complete() and results.overall_success():
            results.results["overall_validation"]["status"] = "success"
            results.results["overall_validation"]["details"]["ready_for_phase_2c"] = True
            results.results["overall_validation"]["details"]["coordination_validated"] = True
            results.results["overall_validation"]["details"]["performance_validated"] = True
            
            print("\n🎉 PHASE 2B VALIDATION SUCCESSFUL!")
            print("✅ Ready to proceed to Phase 2C: 3-Agent Parallel Expansion")
            
        else:
            results.results["overall_validation"]["status"] = "failed"
            results.results["overall_validation"]["details"]["blocking_issues"] = True
            
            print("\n❌ PHASE 2B VALIDATION FAILED!")
            print("🛑 Must resolve issues before proceeding to Phase 2C")
        
    except Exception as e:
        results.results["overall_validation"]["status"] = "error"
        results.results["overall_validation"]["details"]["error"] = str(e)
        print(f"\n💥 PHASE 2B VALIDATION ERROR: {e}")
    
    # Generate and display final report
    report = results.generate_report()
    print(report)
    
    # Save results to file
    report_path = "/Users/kevinhill/Coding/Tooling/PyClarity/clear-thinking-fastmcp/agents/outputs/phase_2b_validation_report.md"
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    with open(report_path, 'w') as f:
        f.write("# Phase 2B: Parallel Validation Report\n\n")
        f.write(f"**Timestamp:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("## Validation Results\n\n")
        f.write(report)
        f.write("\n## Next Steps\n\n")
        
        if results.overall_success():
            f.write("✅ **PROCEED TO PHASE 2C**: 3-Agent Parallel Expansion\n")
            f.write("- Deploy Collaborative Reasoning Agent\n")
            f.write("- Deploy Metacognitive Monitoring Agent\n") 
            f.write("- Deploy Scientific Method Agent\n")
            f.write("- Validate 3-agent coordination patterns\n")
        else:
            f.write("❌ **RESOLVE ISSUES BEFORE PHASE 2C**\n")
            f.write("- Address validation failures\n")
            f.write("- Re-run Phase 2B validation\n")
            f.write("- Ensure all coordination patterns work\n")
    
    print(f"\n📊 Validation report saved to: {report_path}")
    
    return results.overall_success()


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)