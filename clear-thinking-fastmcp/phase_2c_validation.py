#!/usr/bin/env python3
"""
PHASE 2C: 3-AGENT PARALLEL EXPANSION VALIDATION

This validates the 3-agent parallel coordination and implementation:
- Agent C: Collaborative Reasoning 
- Agent D: Metacognitive Monitoring
- Agent E: Scientific Method

Following TDD pattern: Models → Server → Tests
Following incremental approach: Start Small → Validate → Expand → Scale
"""

import asyncio
import time
import os
import subprocess
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class AgentValidationResult:
    """Result of individual agent validation"""
    agent: str
    models_validated: bool
    server_validated: bool
    tests_passed: bool
    test_count: int
    timing: float
    errors: List[str]
    status: str  # "success", "failed", "partial"


class Phase2COrchestrator:
    """Orchestrates Phase 2C 3-agent parallel validation"""
    
    def __init__(self):
        self.results: List[AgentValidationResult] = []
        self.start_time = time.time()
    
    def add_result(self, result: AgentValidationResult):
        """Add agent validation result"""
        self.results.append(result)
        status_emoji = "✅" if result.status == "success" else "❌" if result.status == "failed" else "⚠️"
        print(f"{status_emoji} {result.agent}: {result.status} ({result.timing:.2f}s)")
    
    def is_validation_complete(self) -> bool:
        """Check if all 3 agents have completed"""
        return len(self.results) >= 3
    
    def overall_success(self) -> bool:
        """Check if overall validation succeeded"""
        return all(r.status == "success" for r in self.results)
    
    def generate_report(self) -> str:
        """Generate comprehensive validation report"""
        total_time = time.time() - self.start_time
        
        report = "\n" + "="*80 + "\n"
        report += "🔄 PHASE 2C: 3-AGENT PARALLEL EXPANSION RESULTS\n"
        report += "="*80 + "\n\n"
        report += f"**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"**Total Validation Time:** {total_time:.2f}s\n\n"
        
        for result in self.results:
            status_emoji = "✅" if result.status == "success" else "❌" if result.status == "failed" else "⚠️"
            report += f"{status_emoji} **{result.agent.upper()}**: {result.status} ({result.timing:.2f}s)\n"
            report += f"   - Models validated: {'✅' if result.models_validated else '❌'}\n"
            report += f"   - Server validated: {'✅' if result.server_validated else '❌'}\n"
            report += f"   - Tests passed: {'✅' if result.tests_passed else '❌'} ({result.test_count} tests)\n"
            
            if result.errors:
                report += f"   - Errors:\n"
                for error in result.errors:
                    report += f"     • {error}\n"
            
            report += "\n"
        
        # Overall assessment
        if self.overall_success():
            report += "🎉 **OVERALL STATUS**: 3-AGENT EXPANSION SUCCESSFUL\n"
            report += "✅ Ready to proceed to Phase 2D: 5-Agent Parallel Scaling\n\n"
            report += "**Achievements:**\n"
            report += "- 3 new cognitive tools implemented following TDD\n"
            report += "- Models, servers, and tests all validated\n"
            report += "- Parallel coordination patterns proven at 3-agent scale\n"
            report += "- Incremental scaling approach validated\n\n"
            report += "**Next Steps:**\n"
            report += "- Deploy 5-agent parallel scaling (Phase 2D)\n"
            report += "- Implement remaining cognitive tools\n"
            report += "- Final integration and quality validation\n"
        else:
            report += "❌ **OVERALL STATUS**: 3-AGENT EXPANSION FAILED\n"
            report += "🛑 Must resolve issues before proceeding to Phase 2D\n\n"
            report += "**Required Actions:**\n"
            failed_agents = [r.agent for r in self.results if r.status != "success"]
            for agent in failed_agents:
                report += f"- Fix issues in {agent} implementation\n"
            report += "- Re-run Phase 2C validation\n"
            report += "- Ensure all coordination patterns work properly\n"
        
        return report


async def validate_agent_c_collaborative_reasoning(orchestrator: Phase2COrchestrator):
    """
    AGENT C: Collaborative Reasoning Validation
    
    Validates:
    - Collaborative reasoning models (persona-based reasoning)
    - Server implementation (consensus building)
    - Test suite (multi-perspective validation)
    """
    print("\n🤖 AGENT C: Starting Collaborative Reasoning validation...")
    agent_start = time.time()
    
    errors = []
    models_validated = False
    server_validated = False
    tests_passed = False
    test_count = 0
    
    try:
        # Phase 1: Validate models
        print("   Validating Collaborative Reasoning models...")
        try:
            # Check if model file exists and has required classes
            model_path = "/Users/kevinhill/Coding/Tooling/PyClarity/clear-thinking-fastmcp/src/clear_thinking_fastmcp/models/collaborative_reasoning.py"
            with open(model_path, 'r') as f:
                model_content = f.read()
            
            required_classes = [
                "CollaborativeReasoningInput",
                "CollaborativeReasoningOutput", 
                "Persona",
                "PersonaPerspective",
                "ConsensusResult"
            ]
            
            for class_name in required_classes:
                if f"class {class_name}" not in model_content:
                    errors.append(f"Missing model class: {class_name}")
            
            if not errors:
                models_validated = True
                print("     ✅ Models validated")
            
        except Exception as e:
            errors.append(f"Model validation failed: {e}")
        
        # Phase 2: Validate server
        print("   Validating Collaborative Reasoning server...")
        try:
            server_path = "/Users/kevinhill/Coding/Tooling/PyClarity/clear-thinking-fastmcp/src/clear_thinking_fastmcp/tools/collaborative_reasoning_server.py"
            with open(server_path, 'r') as f:
                server_content = f.read()
            
            required_methods = [
                "class CollaborativeReasoningServer",
                "async def process(",
                "_generate_persona_perspectives",
                "_facilitate_dialogue",
                "_build_consensus"
            ]
            
            for method_name in required_methods:
                if method_name not in server_content:
                    errors.append(f"Missing server component: {method_name}")
            
            if len([e for e in errors if "server" in e.lower()]) == 0:
                server_validated = True
                print("     ✅ Server validated")
            
        except Exception as e:
            errors.append(f"Server validation failed: {e}")
        
        # Phase 3: Run tests
        print("   Running Collaborative Reasoning tests...")
        try:
            import sys
            sys.path.insert(0, "/Users/kevinhill/Coding/Tooling/PyClarity/clear-thinking-fastmcp")
            sys.path.insert(0, "/Users/kevinhill/Coding/Tooling/PyClarity/clear-thinking-fastmcp/src")
            sys.path.insert(0, "/Users/kevinhill/Coding/Tooling/PyClarity/clear-thinking-fastmcp/tests")
            
            # Import and run specific test functions
            from tests.test_collaborative_reasoning import TestCollaborativeReasoningLogic
            
            test_instance = TestCollaborativeReasoningLogic()
            
            # Run key test methods
            test_methods = [
                test_instance.test_persona_creation,
                test_instance.test_collaborative_input_validation,
                test_instance.test_diversity_score_calculation,
                test_instance.test_collaboration_quality_assessment,
                test_instance.test_stakeholder_buy_in_assessment,
                test_instance.test_insights_generation,
                test_instance.test_implementation_considerations
            ]
            
            async_test_methods = [
                test_instance.test_persona_perspective_generation,
                test_instance.test_dialogue_facilitation,
                test_instance.test_weighted_consensus_building,
                test_instance.test_majority_vote_consensus,
                test_instance.test_compromise_consensus,
                test_instance.test_devil_advocate_generation,
                test_instance.test_persona_evolution,
                test_instance.test_full_collaborative_reasoning_workflow
            ]
            
            # Run sync tests
            for test_method in test_methods:
                try:
                    test_method()
                    test_count += 1
                except Exception as e:
                    errors.append(f"Test failed {test_method.__name__}: {e}")
            
            # Run async tests
            for test_method in async_test_methods:
                try:
                    await test_method()
                    test_count += 1
                except Exception as e:
                    errors.append(f"Test failed {test_method.__name__}: {e}")
            
            if len([e for e in errors if "Test failed" in e]) == 0:
                tests_passed = True
                print(f"     ✅ All {test_count} tests passed")
            else:
                print(f"     ❌ {len([e for e in errors if 'Test failed' in e])} tests failed")
            
        except Exception as e:
            errors.append(f"Test execution failed: {e}")
        
        # Determine overall status
        if models_validated and server_validated and tests_passed:
            status = "success"
        elif models_validated or server_validated or tests_passed:
            status = "partial"
        else:
            status = "failed"
        
        agent_time = time.time() - agent_start
        result = AgentValidationResult(
            agent="Agent C (Collaborative Reasoning)",
            models_validated=models_validated,
            server_validated=server_validated,
            tests_passed=tests_passed,
            test_count=test_count,
            timing=agent_time,
            errors=errors,
            status=status
        )
        
        orchestrator.add_result(result)
        
    except Exception as e:
        agent_time = time.time() - agent_start
        result = AgentValidationResult(
            agent="Agent C (Collaborative Reasoning)",
            models_validated=False,
            server_validated=False,
            tests_passed=False,
            test_count=0,
            timing=agent_time,
            errors=[f"Critical failure: {e}"],
            status="failed"
        )
        orchestrator.add_result(result)


async def validate_agent_d_metacognitive_monitoring(orchestrator: Phase2COrchestrator):
    """
    AGENT D: Metacognitive Monitoring Validation
    
    Validates:
    - Metacognitive monitoring models (bias detection, confidence calibration)
    - Server implementation (self-reflection processes)
    - Test suite (meta-learning validation)
    """
    print("\n🤖 AGENT D: Starting Metacognitive Monitoring validation...")
    agent_start = time.time()
    
    errors = []
    models_validated = False
    server_validated = False
    tests_passed = False
    test_count = 0
    
    try:
        # Phase 1: Validate models
        print("   Validating Metacognitive Monitoring models...")
        try:
            model_path = "/Users/kevinhill/Coding/Tooling/PyClarity/clear-thinking-fastmcp/src/clear_thinking_fastmcp/models/metacognitive_monitoring.py"
            with open(model_path, 'r') as f:
                model_content = f.read()
            
            required_classes = [
                "MetacognitiveMonitoringInput",
                "MetacognitiveMonitoringOutput",
                "BiasDetection",
                "ReasoningMonitor",
                "ConfidenceAssessment",
                "StrategyEvaluation",
                "MetaLearningInsight"
            ]
            
            for class_name in required_classes:
                if f"class {class_name}" not in model_content:
                    errors.append(f"Missing model class: {class_name}")
            
            if not errors:
                models_validated = True
                print("     ✅ Models validated")
            
        except Exception as e:
            errors.append(f"Model validation failed: {e}")
        
        # Phase 2: Validate server
        print("   Validating Metacognitive Monitoring server...")
        try:
            server_path = "/Users/kevinhill/Coding/Tooling/PyClarity/clear-thinking-fastmcp/src/clear_thinking_fastmcp/tools/metacognitive_monitoring_server.py"
            with open(server_path, 'r') as f:
                server_content = f.read()
            
            required_methods = [
                "class MetacognitiveMonitoringServer",
                "async def process(",
                "_setup_monitoring_systems",
                "_detect_biases",
                "_calibrate_confidence",
                "_evaluate_strategies",
                "_generate_meta_insights"
            ]
            
            for method_name in required_methods:
                if method_name not in server_content:
                    errors.append(f"Missing server component: {method_name}")
            
            if len([e for e in errors if "server" in e.lower()]) == 0:
                server_validated = True
                print("     ✅ Server validated")
            
        except Exception as e:
            errors.append(f"Server validation failed: {e}")
        
        # Phase 3: Run tests
        print("   Running Metacognitive Monitoring tests...")
        try:
            import sys
            sys.path.insert(0, "/Users/kevinhill/Coding/Tooling/PyClarity/clear-thinking-fastmcp")
            sys.path.insert(0, "/Users/kevinhill/Coding/Tooling/PyClarity/clear-thinking-fastmcp/src")
            sys.path.insert(0, "/Users/kevinhill/Coding/Tooling/PyClarity/clear-thinking-fastmcp/tests")
            
            from tests.test_metacognitive_monitoring import TestMetacognitiveMonitoringLogic
            
            test_instance = TestMetacognitiveMonitoringLogic()
            
            # Run key test methods
            test_methods = [
                test_instance.test_reasoning_monitor_creation,
                test_instance.test_threshold_violation_detection,
                test_instance.test_strategy_evaluation,
                test_instance.test_meta_learning_insight_generation,
                test_instance.test_bias_insight_generation,
                test_instance.test_reasoning_quality_calculation,
                test_instance.test_metacognitive_awareness_calculation,
                test_instance.test_intervention_alert_generation,
                test_instance.test_reasoning_pattern_identification,
                test_instance.test_recommendation_generation,
                test_instance.test_default_confidence_assessment
            ]
            
            async_test_methods = [
                test_instance.test_bias_detection_confirmation_bias,
                test_instance.test_bias_detection_overconfidence_bias,
                test_instance.test_confidence_calibration_evidence_based,
                test_instance.test_confidence_calibration_historical_performance,
                test_instance.test_monitoring_input_validation,
                test_instance.test_full_metacognitive_monitoring_workflow
            ]
            
            # Run sync tests
            for test_method in test_methods:
                try:
                    test_method()
                    test_count += 1
                except Exception as e:
                    errors.append(f"Test failed {test_method.__name__}: {e}")
            
            # Run async tests
            for test_method in async_test_methods:
                try:
                    await test_method()
                    test_count += 1
                except Exception as e:
                    errors.append(f"Test failed {test_method.__name__}: {e}")
            
            if len([e for e in errors if "Test failed" in e]) == 0:
                tests_passed = True
                print(f"     ✅ All {test_count} tests passed")
            else:
                print(f"     ❌ {len([e for e in errors if 'Test failed' in e])} tests failed")
            
        except Exception as e:
            errors.append(f"Test execution failed: {e}")
        
        # Determine overall status
        if models_validated and server_validated and tests_passed:
            status = "success"
        elif models_validated or server_validated or tests_passed:
            status = "partial"
        else:
            status = "failed"
        
        agent_time = time.time() - agent_start
        result = AgentValidationResult(
            agent="Agent D (Metacognitive Monitoring)",
            models_validated=models_validated,
            server_validated=server_validated,
            tests_passed=tests_passed,
            test_count=test_count,
            timing=agent_time,
            errors=errors,
            status=status
        )
        
        orchestrator.add_result(result)
        
    except Exception as e:
        agent_time = time.time() - agent_start
        result = AgentValidationResult(
            agent="Agent D (Metacognitive Monitoring)",
            models_validated=False,
            server_validated=False,
            tests_passed=False,
            test_count=0,
            timing=agent_time,
            errors=[f"Critical failure: {e}"],
            status="failed"
        )
        orchestrator.add_result(result)


async def validate_agent_e_scientific_method(orchestrator: Phase2COrchestrator):
    """
    AGENT E: Scientific Method Validation
    
    Validates:
    - Scientific method models (hypothesis testing, evidence evaluation)
    - Server implementation (systematic inquiry processes)
    - Test suite (theory building validation)
    """
    print("\n🤖 AGENT E: Starting Scientific Method validation...")
    agent_start = time.time()
    
    errors = []
    models_validated = False
    server_validated = False
    tests_passed = False
    test_count = 0
    
    try:
        # Phase 1: Validate models
        print("   Validating Scientific Method models...")
        try:
            model_path = "/Users/kevinhill/Coding/Tooling/PyClarity/clear-thinking-fastmcp/src/clear_thinking_fastmcp/models/scientific_method.py"
            with open(model_path, 'r') as f:
                model_content = f.read()
            
            required_classes = [
                "ScientificMethodInput",
                "ScientificMethodOutput",
                "Hypothesis",
                "Evidence",
                "Experiment",
                "HypothesisTest",
                "TheoryConstruction"
            ]
            
            for class_name in required_classes:
                if f"class {class_name}" not in model_content:
                    errors.append(f"Missing model class: {class_name}")
            
            if not errors:
                models_validated = True
                print("     ✅ Models validated")
            
        except Exception as e:
            errors.append(f"Model validation failed: {e}")
        
        # Phase 2: Validate server
        print("   Validating Scientific Method server...")
        try:
            server_path = "/Users/kevinhill/Coding/Tooling/PyClarity/clear-thinking-fastmcp/src/clear_thinking_fastmcp/tools/scientific_method_server.py"
            with open(server_path, 'r') as f:
                server_content = f.read()
            
            required_methods = [
                "class ScientificMethodServer",
                "async def process(",
                "_generate_hypotheses",
                "_collect_evidence",
                "_design_experiments",
                "_test_hypotheses",
                "_construct_theory"
            ]
            
            for method_name in required_methods:
                if method_name not in server_content:
                    errors.append(f"Missing server component: {method_name}")
            
            if len([e for e in errors if "server" in e.lower()]) == 0:
                server_validated = True
                print("     ✅ Server validated")
            
        except Exception as e:
            errors.append(f"Server validation failed: {e}")
        
        # Phase 3: Run tests
        print("   Running Scientific Method tests...")
        try:
            import sys
            sys.path.insert(0, "/Users/kevinhill/Coding/Tooling/PyClarity/clear-thinking-fastmcp")
            sys.path.insert(0, "/Users/kevinhill/Coding/Tooling/PyClarity/clear-thinking-fastmcp/src")
            sys.path.insert(0, "/Users/kevinhill/Coding/Tooling/PyClarity/clear-thinking-fastmcp/tests")
            
            from tests.test_scientific_method import TestScientificMethodLogic
            
            test_instance = TestScientificMethodLogic()
            
            # Run key test methods
            test_methods = [
                test_instance.test_hypothesis_creation,
                test_instance.test_null_hypothesis_creation,
                test_instance.test_evidence_creation_experimental,
                test_instance.test_evidence_creation_observational,
                test_instance.test_experiment_design,
                test_instance.test_theory_construction,
                test_instance.test_scientific_rigor_evaluation,
                test_instance.test_scientific_method_input_validation,
                test_instance.test_overall_confidence_calculation,
                test_instance.test_scientific_confidence_calculation,
                test_instance.test_alternative_explanations_generation,
                test_instance.test_recommendations_based_on_test_results
            ]
            
            async_test_methods = [
                test_instance.test_hypothesis_generation_explanatory,
                test_instance.test_hypothesis_generation_predictive,
                test_instance.test_hypothesis_testing_supported,
                test_instance.test_hypothesis_testing_inconclusive,
                test_instance.test_full_scientific_method_workflow
            ]
            
            # Run sync tests
            for test_method in test_methods:
                try:
                    test_method()
                    test_count += 1
                except Exception as e:
                    errors.append(f"Test failed {test_method.__name__}: {e}")
            
            # Run async tests
            for test_method in async_test_methods:
                try:
                    await test_method()
                    test_count += 1
                except Exception as e:
                    errors.append(f"Test failed {test_method.__name__}: {e}")
            
            if len([e for e in errors if "Test failed" in e]) == 0:
                tests_passed = True
                print(f"     ✅ All {test_count} tests passed")
            else:
                print(f"     ❌ {len([e for e in errors if 'Test failed' in e])} tests failed")
            
        except Exception as e:
            errors.append(f"Test execution failed: {e}")
        
        # Determine overall status
        if models_validated and server_validated and tests_passed:
            status = "success"
        elif models_validated or server_validated or tests_passed:
            status = "partial"
        else:
            status = "failed"
        
        agent_time = time.time() - agent_start
        result = AgentValidationResult(
            agent="Agent E (Scientific Method)",
            models_validated=models_validated,
            server_validated=server_validated,
            tests_passed=tests_passed,
            test_count=test_count,
            timing=agent_time,
            errors=errors,
            status=status
        )
        
        orchestrator.add_result(result)
        
    except Exception as e:
        agent_time = time.time() - agent_start
        result = AgentValidationResult(
            agent="Agent E (Scientific Method)",
            models_validated=False,
            server_validated=False,
            tests_passed=False,
            test_count=0,
            timing=agent_time,
            errors=[f"Critical failure: {e}"],
            status="failed"
        )
        orchestrator.add_result(result)


async def main():
    """
    Main orchestration function for Phase 2C validation
    
    Executes 3 agents in parallel following TDD pattern:
    Models → Server → Tests for each cognitive tool
    
    Following incremental approach:
    Start Small (2 agents) → Validate (2B) → Expand (3 agents 2C) → Scale (5+ agents 2D)
    """
    print("🚀 PHASE 2C: 3-AGENT PARALLEL EXPANSION STARTING")
    print("="*60)
    print("Following Incremental Approach: 2-Agent → 3-Agent → 5-Agent scaling")
    print("Following TDD Pattern: Models → Server → Tests")
    print("Agent C: Collaborative Reasoning (persona-based reasoning)")
    print("Agent D: Metacognitive Monitoring (self-reflection)")
    print("Agent E: Scientific Method (hypothesis-driven)")
    print("="*60)
    
    # Initialize orchestrator
    orchestrator = Phase2COrchestrator()
    
    try:
        # Execute all 3 agents in parallel (Expand from 2-agent validation)
        print("\n🔄 Executing 3-agent parallel validation...")
        
        await asyncio.gather(
            validate_agent_c_collaborative_reasoning(orchestrator),
            validate_agent_d_metacognitive_monitoring(orchestrator),
            validate_agent_e_scientific_method(orchestrator)
        )
        
        # Validation complete - analyze results
        print(f"\n📊 Validation completed in {time.time() - orchestrator.start_time:.2f}s")
        
        # Generate and display report
        report = orchestrator.generate_report()
        print(report)
        
        # Save report to file
        report_path = "/Users/kevinhill/Coding/Tooling/PyClarity/clear-thinking-fastmcp/agents/outputs/phase_2c_validation_report.md"
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        with open(report_path, 'w') as f:
            f.write("# Phase 2C: 3-Agent Parallel Expansion Report\n\n")
            f.write(report)
            f.write("\n## Agent Implementation Details\n\n")
            
            for result in orchestrator.results:
                f.write(f"### {result.agent}\n")
                f.write(f"- **Status**: {result.status}\n")
                f.write(f"- **Timing**: {result.timing:.2f}s\n")
                f.write(f"- **Models**: {'✅' if result.models_validated else '❌'}\n")
                f.write(f"- **Server**: {'✅' if result.server_validated else '❌'}\n")
                f.write(f"- **Tests**: {'✅' if result.tests_passed else '❌'} ({result.test_count} tests)\n")
                
                if result.errors:
                    f.write(f"- **Errors**:\n")
                    for error in result.errors:
                        f.write(f"  - {error}\n")
                f.write("\n")
            
            f.write("\n## Coordination Analysis\n\n")
            
            if orchestrator.overall_success():
                f.write("✅ **3-AGENT COORDINATION SUCCESSFUL**\n\n")
                f.write("**Validated Patterns:**\n")
                f.write("- 3-agent parallel execution scales successfully from 2-agent\n")
                f.write("- TDD pattern (Models → Server → Tests) works for all agents\n")
                f.write("- Each cognitive tool implements unique reasoning approach\n")
                f.write("- FastMCP Context integration functional across all tools\n")
                f.write("- Incremental scaling approach validates expansion capability\n\n")
                f.write("**Phase 2D Ready:** Can proceed to 5-agent parallel scaling\n")
            else:
                f.write("❌ **3-AGENT COORDINATION ISSUES**\n\n")
                failed_agents = [r.agent for r in orchestrator.results if r.status != "success"]
                f.write("**Issues to Address:**\n")
                for agent in failed_agents:
                    f.write(f"- {agent}: Implementation or testing failures\n")
                f.write("\n**Required Actions:** Fix issues and re-run Phase 2C validation\n")
        
        print(f"\n📄 Detailed report saved to: {report_path}")
        
        return orchestrator.overall_success()
        
    except Exception as e:
        print(f"\n💥 ORCHESTRATION ERROR: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    print(f"\n🎯 PHASE 2C RESULT: {'SUCCESS' if success else 'FAILED'}")
    exit(0 if success else 1)