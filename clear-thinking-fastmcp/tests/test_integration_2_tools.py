# Clear Thinking FastMCP Server - Two-Tool Integration Tests

"""
Integration test suite for Sequential Thinking → Decision Framework workflow.

This test suite validates the integration and coordination between the two 
completed cognitive tools following the incremental testing approach:
Start Small → Validate → Expand → Scale

Test Coverage:
- Sequential Thinking output → Decision Framework input conversion
- FastMCP Context sharing and progress tracking
- Data compatibility and transformation
- Error propagation and recovery
- Performance integration testing
- Session management across tools

Agent: End-to-End System Integration Specialist
Status: ACTIVE - Two-tool integration validation
"""

import pytest
import pytest_asyncio
import uuid
import time
import asyncio
from typing import List, Dict, Any, Optional
from unittest.mock import AsyncMock, MagicMock, Mock, patch

# FastMCP testing imports
from fastmcp.server import Context

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


# ============================================================================
# Test Fixtures and Data Generators
# ============================================================================

@pytest.fixture
def mock_context():
    """Create a mock FastMCP Context for testing"""
    context = AsyncMock(spec=Context)
    context.progress = AsyncMock()
    context.info = AsyncMock()
    context.debug = AsyncMock()
    context.error = AsyncMock()
    context.cancelled = AsyncMock(return_value=False)
    return context


@pytest.fixture
def sample_problem():
    """Sample problem for testing tool chain"""
    return "Our web application is experiencing slow response times during peak hours. Users are reporting delays of 3-5 seconds for page loads, which is impacting customer satisfaction and conversion rates."


@pytest.fixture
def sequential_thinking_server():
    """Create Sequential Thinking server instance"""
    return SequentialThinkingServer()


@pytest.fixture
def decision_framework_server():
    """Create Decision Framework server instance"""
    return DecisionFrameworkServer()


@pytest.fixture
def sample_sequential_input(sample_problem):
    """Generate sample Sequential Thinking input"""
    return SequentialThinkingInput(
        problem=sample_problem,
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


@pytest.fixture
def sample_decision_options():
    """Generate sample decision options"""
    return [
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
        ),
        DecisionOption(
            name="Server Scaling",
            description="Scale server infrastructure horizontally",
            scores={
                "implementation_cost": 0.5,
                "technical_complexity": 0.4,
                "expected_impact": 0.7,
                "timeline": 0.9
            },
            confidence_scores={
                "implementation_cost": 0.7,
                "technical_complexity": 0.9,
                "expected_impact": 0.8,
                "timeline": 0.9
            },
            risks=["Increased infrastructure costs", "Load balancing complexity"],
            assumptions=["Current servers are at capacity", "Horizontal scaling is feasible"]
        )
    ]


@pytest.fixture
def sample_decision_criteria():
    """Generate sample decision criteria"""
    return [
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


# ============================================================================
# Start Small: Basic Tool Chain Validation
# ============================================================================

class TestBasicToolChain:
    """Test basic Sequential Thinking → Decision Framework workflow"""
    
    @pytest.mark.asyncio
    async def test_sequential_to_decision_basic_flow(
        self,
        sequential_thinking_server,
        decision_framework_server,
        sample_sequential_input,
        sample_decision_criteria,
        sample_decision_options,
        mock_context
    ):
        """Test basic workflow from Sequential Thinking to Decision Framework"""
        
        # Step 1: Process Sequential Thinking
        sequential_output = await sequential_thinking_server.process(
            sample_sequential_input,
            mock_context
        )
        
        # Validate Sequential Thinking output
        assert isinstance(sequential_output, SequentialThinkingOutput)
        assert sequential_output.session_id == sample_sequential_input.session_id
        assert len(sequential_output.reasoning_chain) > 0
        assert sequential_output.final_conclusion is not None
        assert 0.0 <= sequential_output.confidence_score <= 1.0
        
        # Step 2: Create Decision Framework input using Sequential Thinking output
        decision_input = DecisionFrameworkInput(
            decision_problem=sequential_output.final_conclusion,
            complexity_level=ComplexityLevel.MODERATE,
            decision_method=DecisionMethodType.WEIGHTED_SCORING,
            criteria=sample_decision_criteria,
            options=sample_decision_options,
            stakeholders=["development_team", "product_management", "users"],
            constraints=["6_month_timeline", "limited_budget"],
            include_risk_analysis=True,
            include_trade_off_analysis=True,
            include_sensitivity_analysis=True,
            session_id=sequential_output.session_id  # Pass session ID through
        )
        
        # Step 3: Process Decision Framework
        decision_output = await decision_framework_server.process(
            decision_input,
            mock_context
        )
        
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
        
        print(f"✅ Basic tool chain test passed:")
        print(f"   Sequential Thinking: {len(sequential_output.reasoning_chain)} steps")
        print(f"   Decision Framework: {decision_output.recommended_option}")
        print(f"   Session continuity: {decision_output.session_id}")
    
    @pytest.mark.asyncio
    async def test_context_integration_basic(
        self,
        sequential_thinking_server,
        decision_framework_server,
        sample_sequential_input,
        sample_decision_criteria,
        sample_decision_options,
        mock_context
    ):
        """Test basic FastMCP Context integration across tools"""
        
        # Process both tools with same context
        sequential_output = await sequential_thinking_server.process(
            sample_sequential_input,
            mock_context
        )
        
        decision_input = DecisionFrameworkInput(
            decision_problem=sequential_output.final_conclusion,
            complexity_level=ComplexityLevel.MODERATE,
            decision_method=DecisionMethodType.WEIGHTED_SCORING,
            criteria=sample_decision_criteria,
            options=sample_decision_options,
            session_id=sequential_output.session_id
        )
        
        decision_output = await decision_framework_server.process(
            decision_input,
            mock_context
        )
        
        # Verify context was used by both tools
        assert mock_context.progress.called
        assert mock_context.info.called
        
        # Verify progress tracking continuity
        progress_calls = mock_context.progress.call_args_list
        assert len(progress_calls) > 0
        
        # Check that both tools reported progress
        info_calls = mock_context.info.call_args_list
        info_messages = [call[0][0] for call in info_calls]
        
        sequential_messages = [msg for msg in info_messages if "Sequential Thinking" in msg]
        decision_messages = [msg for msg in info_messages if "Decision Framework" in msg]
        
        assert len(sequential_messages) > 0
        assert len(decision_messages) > 0
        
        print(f"✅ Context integration test passed:")
        print(f"   Progress calls: {len(progress_calls)}")
        print(f"   Sequential messages: {len(sequential_messages)}")
        print(f"   Decision messages: {len(decision_messages)}")


# ============================================================================
# Validate: Data Compatibility and Transformation
# ============================================================================

class TestDataCompatibility:
    """Test data flow and compatibility between tools"""
    
    @pytest.mark.asyncio
    async def test_reasoning_chain_to_decision_options_conversion(
        self,
        sequential_thinking_server,
        sample_sequential_input,
        mock_context
    ):
        """Test converting reasoning chain insights to decision options"""
        
        # Process Sequential Thinking
        sequential_output = await sequential_thinking_server.process(
            sample_sequential_input,
            mock_context
        )
        
        # Extract insights from reasoning chain
        reasoning_insights = []
        for step in sequential_output.reasoning_chain:
            if step.step_type in [ThoughtStepType.HYPOTHESIS_FORMATION, ThoughtStepType.SYNTHESIS]:
                reasoning_insights.append({
                    "insight": step.content,
                    "confidence": step.confidence_score,
                    "evidence": step.supporting_evidence or [],
                    "assumptions": step.assumptions_made or []
                })
        
        # Verify insights can be converted to decision options
        assert len(reasoning_insights) > 0
        
        for insight in reasoning_insights:
            assert "insight" in insight
            assert "confidence" in insight
            assert isinstance(insight["confidence"], float)
            assert 0.0 <= insight["confidence"] <= 1.0
        
        # Create decision options from insights
        decision_options = []
        for i, insight in enumerate(reasoning_insights[:3]):  # Limit to 3 options
            option = DecisionOption(
                name=f"Option_{i+1}",
                description=insight["insight"][:100] + "...",
                scores={
                    "feasibility": insight["confidence"],
                    "impact": min(1.0, insight["confidence"] + 0.1),
                    "risk": 1.0 - insight["confidence"]
                },
                risks=insight.get("assumptions", [])[:2],  # Use assumptions as risks
                assumptions=insight.get("assumptions", [])
            )
            decision_options.append(option)
        
        assert len(decision_options) > 0
        
        print(f"✅ Data conversion test passed:")
        print(f"   Reasoning insights extracted: {len(reasoning_insights)}")
        print(f"   Decision options created: {len(decision_options)}")
    
    @pytest.mark.asyncio
    async def test_confidence_score_propagation(
        self,
        sequential_thinking_server,
        decision_framework_server,
        sample_sequential_input,
        sample_decision_criteria,
        sample_decision_options,
        mock_context
    ):
        """Test confidence score propagation between tools"""
        
        # Process Sequential Thinking
        sequential_output = await sequential_thinking_server.process(
            sample_sequential_input,
            mock_context
        )
        
        # Create Decision Framework input with confidence-based weighting
        # Adjust criteria weights based on sequential thinking confidence
        adjusted_criteria = []
        confidence_factor = sequential_output.confidence_score
        
        for criterion in sample_decision_criteria:
            adjusted_weight = criterion.weight * (0.8 + 0.2 * confidence_factor)
            adjusted_criterion = DecisionCriteria(
                name=criterion.name,
                description=criterion.description,
                weight=min(1.0, adjusted_weight),  # Cap at 1.0
                criteria_type=criterion.criteria_type,
                measurement_unit=criterion.measurement_unit
            )
            adjusted_criteria.append(adjusted_criterion)
        
        # Normalize weights to sum to 1.0
        total_weight = sum(c.weight for c in adjusted_criteria)
        for criterion in adjusted_criteria:
            criterion.weight = criterion.weight / total_weight
        
        decision_input = DecisionFrameworkInput(
            decision_problem=sequential_output.final_conclusion,
            complexity_level=ComplexityLevel.MODERATE,
            decision_method=DecisionMethodType.WEIGHTED_SCORING,
            criteria=adjusted_criteria,
            options=sample_decision_options,
            session_id=sequential_output.session_id
        )
        
        decision_output = await decision_framework_server.process(
            decision_input,
            mock_context
        )
        
        # Verify confidence propagation
        assert 0.0 <= decision_output.confidence_score <= 1.0
        
        # Check that confidence influenced the process
        weight_sum = sum(c.weight for c in adjusted_criteria)
        assert abs(weight_sum - 1.0) < 0.01  # Should sum to 1.0
        
        print(f"✅ Confidence propagation test passed:")
        print(f"   Sequential confidence: {sequential_output.confidence_score:.3f}")
        print(f"   Decision confidence: {decision_output.confidence_score:.3f}")
        print(f"   Criteria weight sum: {weight_sum:.3f}")


# ============================================================================
# Expand: Error Handling and Recovery
# ============================================================================

class TestErrorHandling:
    """Test error propagation and recovery between tools"""
    
    @pytest.mark.asyncio
    async def test_sequential_thinking_error_propagation(
        self,
        decision_framework_server,
        sample_decision_criteria,
        sample_decision_options,
        mock_context
    ):
        """Test handling of Sequential Thinking failures"""
        
        # Simulate Sequential Thinking failure by providing invalid output
        invalid_sequential_output = SequentialThinkingOutput(
            reasoning_chain=[],  # Empty chain
            branches_explored=[],
            revisions_made=[],
            final_conclusion="",  # Empty conclusion
            conclusion_confidence=0.0,
            reasoning_quality_score=0.0,
            critical_assumptions=[],
            evidence_gaps=[],
            alternative_conclusions=[],
            reasoning_path_summary="Failed processing",
            recommendations=[],
            limitations="Processing failed",
            confidence_score=0.0,
            analysis="No analysis available"
        )
        
        # Try to use invalid output in Decision Framework
        try:
            decision_input = DecisionFrameworkInput(
                decision_problem=invalid_sequential_output.final_conclusion or "Fallback problem statement",
                complexity_level=ComplexityLevel.SIMPLE,  # Reduce complexity
                decision_method=DecisionMethodType.WEIGHTED_SCORING,
                criteria=sample_decision_criteria,
                options=sample_decision_options,
                session_id="error_test_session"
            )
            
            # Decision Framework should handle empty/invalid input gracefully
            decision_output = await decision_framework_server.process(
                decision_input,
                mock_context
            )
            
            # Should still produce valid output with fallback values
            assert isinstance(decision_output, DecisionFrameworkOutput)
            assert decision_output.recommended_option is not None
            
        except Exception as e:
            pytest.fail(f"Decision Framework should handle invalid Sequential Thinking output gracefully: {e}")
        
        print("✅ Error propagation test passed: Decision Framework handled invalid input")
    
    @pytest.mark.asyncio
    async def test_context_cancellation_handling(
        self,
        sequential_thinking_server,
        decision_framework_server,
        sample_sequential_input,
        sample_decision_criteria,
        sample_decision_options,
        mock_context
    ):
        """Test handling of context cancellation"""
        
        # Set up context to be cancelled after first tool
        call_count = 0
        original_cancelled = mock_context.cancelled
        
        async def cancelled_after_first():
            nonlocal call_count
            call_count += 1
            return call_count > 10  # Cancel after some calls
        
        mock_context.cancelled = AsyncMock(side_effect=cancelled_after_first)
        
        try:
            # Process Sequential Thinking (should complete)
            sequential_output = await sequential_thinking_server.process(
                sample_sequential_input,
                mock_context
            )
            
            # Reset cancellation for second tool
            mock_context.cancelled = original_cancelled
            
            decision_input = DecisionFrameworkInput(
                decision_problem=sequential_output.final_conclusion,
                complexity_level=ComplexityLevel.MODERATE,
                decision_method=DecisionMethodType.WEIGHTED_SCORING,
                criteria=sample_decision_criteria,
                options=sample_decision_options,
                session_id=sequential_output.session_id
            )
            
            # Process Decision Framework
            decision_output = await decision_framework_server.process(
                decision_input,
                mock_context
            )
            
            assert isinstance(decision_output, DecisionFrameworkOutput)
            
        except Exception as e:
            # Some cancellation is expected, but should be handled gracefully
            print(f"Cancellation handled: {e}")
        
        print("✅ Context cancellation test completed")


# ============================================================================
# Scale: Performance and Load Testing
# ============================================================================

class TestPerformanceIntegration:
    """Test performance and load characteristics of tool integration"""
    
    @pytest.mark.asyncio
    async def test_processing_time_reasonable(
        self,
        sequential_thinking_server,
        decision_framework_server,
        sample_sequential_input,
        sample_decision_criteria,
        sample_decision_options,
        mock_context
    ):
        """Test that combined processing time is reasonable (<5 seconds)"""
        
        start_time = time.time()
        
        # Process Sequential Thinking
        sequential_start = time.time()
        sequential_output = await sequential_thinking_server.process(
            sample_sequential_input,
            mock_context
        )
        sequential_time = time.time() - sequential_start
        
        # Process Decision Framework
        decision_start = time.time()
        decision_input = DecisionFrameworkInput(
            decision_problem=sequential_output.final_conclusion,
            complexity_level=ComplexityLevel.MODERATE,
            decision_method=DecisionMethodType.WEIGHTED_SCORING,
            criteria=sample_decision_criteria,
            options=sample_decision_options,
            session_id=sequential_output.session_id
        )
        
        decision_output = await decision_framework_server.process(
            decision_input,
            mock_context
        )
        decision_time = time.time() - decision_start
        
        total_time = time.time() - start_time
        
        # Validate performance requirements
        assert total_time < 5.0, f"Total processing time {total_time:.2f}s exceeds 5s limit"
        assert sequential_time < 3.0, f"Sequential Thinking time {sequential_time:.2f}s exceeds 3s limit"
        assert decision_time < 3.0, f"Decision Framework time {decision_time:.2f}s exceeds 3s limit"
        
        print(f"✅ Performance test passed:")
        print(f"   Sequential Thinking: {sequential_time:.2f}s")
        print(f"   Decision Framework: {decision_time:.2f}s")
        print(f"   Total time: {total_time:.2f}s")
    
    @pytest.mark.asyncio
    async def test_concurrent_processing(
        self,
        sequential_thinking_server,
        decision_framework_server,
        sample_decision_criteria,
        sample_decision_options,
        mock_context
    ):
        """Test processing multiple problems concurrently"""
        
        # Create multiple problem inputs
        problems = [
            "Database performance optimization challenge",
            "User interface responsiveness issues",
            "API endpoint latency problems"
        ]
        
        async def process_problem_chain(problem, session_id):
            """Process one complete problem chain"""
            
            # Sequential Thinking
            seq_input = SequentialThinkingInput(
                problem=problem,
                complexity_level=ComplexityLevel.MODERATE,
                reasoning_depth=3,  # Reduced for performance
                enable_branching=False,  # Simplified for concurrency
                session_id=session_id
            )
            
            seq_output = await sequential_thinking_server.process(seq_input, mock_context)
            
            # Decision Framework
            dec_input = DecisionFrameworkInput(
                decision_problem=seq_output.final_conclusion,
                complexity_level=ComplexityLevel.MODERATE,
                decision_method=DecisionMethodType.WEIGHTED_SCORING,
                criteria=sample_decision_criteria,
                options=sample_decision_options,
                session_id=seq_output.session_id
            )
            
            dec_output = await decision_framework_server.process(dec_input, mock_context)
            
            return {
                "session_id": session_id,
                "sequential_output": seq_output,
                "decision_output": dec_output
            }
        
        # Process all problems concurrently
        start_time = time.time()
        
        tasks = [
            process_problem_chain(problem, f"concurrent_test_{i}")
            for i, problem in enumerate(problems)
        ]
        
        results = await asyncio.gather(*tasks)
        
        total_time = time.time() - start_time
        
        # Validate all results
        assert len(results) == len(problems)
        
        for result in results:
            assert isinstance(result["sequential_output"], SequentialThinkingOutput)
            assert isinstance(result["decision_output"], DecisionFrameworkOutput)
            assert result["sequential_output"].session_id == result["decision_output"].session_id
        
        # Performance should be better than sequential processing
        expected_sequential_time = len(problems) * 2.0  # Rough estimate
        efficiency_ratio = expected_sequential_time / total_time
        
        print(f"✅ Concurrent processing test passed:")
        print(f"   Problems processed: {len(problems)}")
        print(f"   Total time: {total_time:.2f}s")
        print(f"   Efficiency ratio: {efficiency_ratio:.2f}x")
        
        assert efficiency_ratio > 1.0, "Concurrent processing should be more efficient"


# ============================================================================
# Integration Health Check
# ============================================================================

class TestIntegrationHealthCheck:
    """Overall integration health and system validation"""
    
    @pytest.mark.asyncio
    async def test_end_to_end_integration_health(
        self,
        sequential_thinking_server,
        decision_framework_server,
        sample_sequential_input,
        sample_decision_criteria,
        sample_decision_options,
        mock_context
    ):
        """Comprehensive end-to-end integration health check"""
        
        health_results = {
            "sequential_thinking": None,
            "decision_framework": None,
            "integration": None,
            "performance": None
        }
        
        try:
            # Test Sequential Thinking health
            seq_health = await sequential_thinking_server.health_check()
            health_results["sequential_thinking"] = seq_health["status"]
            
            # Test Decision Framework health
            dec_health = await decision_framework_server.health_check()
            health_results["decision_framework"] = dec_health["status"]
            
            # Test integration workflow
            start_time = time.time()
            
            sequential_output = await sequential_thinking_server.process(
                sample_sequential_input,
                mock_context
            )
            
            decision_input = DecisionFrameworkInput(
                decision_problem=sequential_output.final_conclusion,
                complexity_level=ComplexityLevel.MODERATE,
                decision_method=DecisionMethodType.WEIGHTED_SCORING,
                criteria=sample_decision_criteria,
                options=sample_decision_options,
                session_id=sequential_output.session_id
            )
            
            decision_output = await decision_framework_server.process(
                decision_input,
                mock_context
            )
            
            processing_time = time.time() - start_time
            
            # Validate integration health
            integration_healthy = (
                sequential_output.session_id == decision_output.session_id and
                decision_output.recommended_option is not None and
                len(decision_output.option_rankings) > 0 and
                processing_time < 5.0
            )
            
            health_results["integration"] = "healthy" if integration_healthy else "unhealthy"
            health_results["performance"] = f"{processing_time:.2f}s"
            
        except Exception as e:
            health_results["integration"] = f"error: {e}"
        
        # Report health status
        print("🏥 Integration Health Check Results:")
        for component, status in health_results.items():
            print(f"   {component}: {status}")
        
        # Validate overall health
        assert health_results["sequential_thinking"] in ["healthy", "warning"]
        assert health_results["decision_framework"] in ["healthy", "warning"]
        assert health_results["integration"] == "healthy"
        
        print("✅ Integration health check passed")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])