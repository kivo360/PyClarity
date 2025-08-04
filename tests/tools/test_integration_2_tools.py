# PyClarity - Two-Tool Integration Tests

"""
Integration test suite for Sequential Thinking → Decision Framework workflow.

This test suite validates the integration and coordination between the two 
cognitive tools following the incremental testing approach:
Start Small → Validate → Expand → Scale

Test Coverage:
- Sequential Thinking output → Decision Framework input conversion
- Async analyzer coordination
- Data compatibility and transformation
- Error propagation and recovery
- Performance integration testing
- Processing time tracking across tools
"""

import pytest
import pytest_asyncio
import time
import asyncio
from typing import List, Dict, Any, Optional

# Import Sequential Thinking models and analyzer
from pyclarity.tools.sequential_thinking.models import (
    SequentialThinkingContext,
    SequentialThinkingResult,
    ThoughtStep,
    ThoughtStepType,
    BranchStrategy,
    ComplexityLevel
)
from pyclarity.tools.sequential_thinking.analyzer import SequentialThinkingAnalyzer

# Import Decision Framework models and analyzer
from pyclarity.tools.decision_framework.models import (
    DecisionFrameworkContext,
    DecisionFrameworkResult,
    DecisionMethodType,
    DecisionCriteria,
    DecisionOption,
    CriteriaType
)
from pyclarity.tools.decision_framework.analyzer import DecisionFrameworkAnalyzer


# ============================================================================
# Test Fixtures and Data Generators
# ============================================================================

@pytest.fixture
def sequential_analyzer():
    """Create Sequential Thinking analyzer instance"""
    return SequentialThinkingAnalyzer()


@pytest.fixture
def decision_analyzer():
    """Create Decision Framework analyzer instance"""
    return DecisionFrameworkAnalyzer()


@pytest.fixture
def sample_problem():
    """Sample problem for testing tool chain"""
    return "Our web application is experiencing slow response times during peak hours. Users are reporting delays of 3-5 seconds for page loads, which is impacting customer satisfaction and conversion rates."


@pytest.fixture
def sample_sequential_context(sample_problem):
    """Generate sample Sequential Thinking context"""
    return SequentialThinkingContext(
        problem=sample_problem,
        complexity_level=ComplexityLevel.MODERATE,
        reasoning_depth=5,
        enable_branching=True,
        max_branches=2,
        allow_revisions=True,
        branch_strategy=BranchStrategy.CONVERGENT_SYNTHESIS,
        convergence_threshold=0.8,
        evidence_sources=["performance metrics", "user feedback", "system logs"],
        validation_criteria=["logical consistency", "empirical support"]
    )


@pytest.fixture
def sample_decision_context(sample_decision_criteria, sample_decision_options):
    """Generate sample Decision Framework context"""
    return DecisionFrameworkContext(
        decision_problem="Optimize web application performance during peak hours",
        complexity_level=ComplexityLevel.MODERATE,
        criteria=sample_decision_criteria,
        options=sample_decision_options,
        decision_methods=[DecisionMethodType.WEIGHTED_SUM, DecisionMethodType.TOPSIS],
        stakeholder_weights={"development_team": 0.4, "product_management": 0.3, "users": 0.3},
        uncertainty_factors=["Future load patterns", "Technology changes"],
        time_constraints="6 month implementation timeline"
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
        sequential_analyzer,
        decision_analyzer,
        sample_sequential_context,
        sample_decision_criteria,
        sample_decision_options
    ):
        """Test basic workflow from Sequential Thinking to Decision Framework"""
        
        # Step 1: Process Sequential Thinking
        sequential_result = await sequential_analyzer.analyze(
            sample_sequential_context
        )
        
        # Validate Sequential Thinking output
        assert isinstance(sequential_result, SequentialThinkingResult)
        assert len(sequential_result.reasoning_chain) > 0
        assert sequential_result.final_conclusion is not None
        assert 0.0 <= sequential_result.conclusion_confidence <= 1.0
        
        # Step 2: Create Decision Framework context using Sequential Thinking output
        decision_context = DecisionFrameworkContext(
            decision_problem=sequential_result.final_conclusion,
            complexity_level=ComplexityLevel.MODERATE,
            criteria=sample_decision_criteria,
            options=sample_decision_options,
            decision_methods=[DecisionMethodType.WEIGHTED_SUM],
            stakeholder_weights={
                "development_team": 0.4,
                "product_management": 0.3,
                "users": 0.3
            },
            uncertainty_factors=sequential_result.evidence_gaps[:3],  # Use gaps as uncertainties
            time_constraints="6 month timeline"
        )
        
        # Step 3: Process Decision Framework
        decision_result = await decision_analyzer.analyze(
            decision_context
        )
        
        # Validate Decision Framework output
        assert isinstance(decision_result, DecisionFrameworkResult)
        assert decision_result.recommended_option is not None
        assert len(decision_result.ranked_options) > 0
        assert decision_result.decision_matrix is not None
        assert 0.0 <= decision_result.confidence_score <= 1.0
        
        # Validate data flow between tools
        assert decision_context.decision_problem == sequential_result.final_conclusion
        
        print(f"✅ Basic tool chain test passed:")
        print(f"   Sequential Thinking: {len(sequential_result.reasoning_chain)} steps")
        print(f"   Decision Framework: {decision_result.recommended_option}")
        print(f"   Processing times: Seq={sequential_result.processing_time_ms}ms, Dec={decision_result.processing_time_ms}ms")
    
    @pytest.mark.asyncio
    async def test_processing_time_tracking(
        self,
        sequential_analyzer,
        decision_analyzer,
        sample_sequential_context,
        sample_decision_criteria,
        sample_decision_options
    ):
        """Test processing time tracking across tools"""
        
        # Process Sequential Thinking
        sequential_result = await sequential_analyzer.analyze(
            sample_sequential_context
        )
        
        # Create Decision Framework context
        decision_context = DecisionFrameworkContext(
            decision_problem=sequential_result.final_conclusion,
            complexity_level=ComplexityLevel.MODERATE,
            criteria=sample_decision_criteria,
            options=sample_decision_options,
            decision_methods=[DecisionMethodType.WEIGHTED_SUM]
        )
        
        # Process Decision Framework
        decision_result = await decision_analyzer.analyze(
            decision_context
        )
        
        # Verify processing times are tracked
        assert sequential_result.processing_time_ms > 0
        assert decision_result.processing_time_ms > 0
        
        total_time = sequential_result.processing_time_ms + decision_result.processing_time_ms
        
        print(f"✅ Processing time tracking test passed:")
        print(f"   Sequential Thinking: {sequential_result.processing_time_ms}ms")
        print(f"   Decision Framework: {decision_result.processing_time_ms}ms")
        print(f"   Total processing: {total_time}ms")


# ============================================================================
# Validate: Data Compatibility and Transformation
# ============================================================================

class TestDataCompatibility:
    """Test data flow and compatibility between tools"""
    
    @pytest.mark.asyncio
    async def test_reasoning_chain_to_decision_options_conversion(
        self,
        sequential_analyzer,
        sample_sequential_context
    ):
        """Test converting reasoning chain insights to decision options"""
        
        # Process Sequential Thinking
        sequential_result = await sequential_analyzer.analyze(
            sample_sequential_context
        )
        
        # Extract insights from reasoning chain
        reasoning_insights = []
        for step in sequential_result.reasoning_chain:
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
        sequential_analyzer,
        decision_analyzer,
        sample_sequential_context,
        sample_decision_criteria,
        sample_decision_options
    ):
        """Test confidence score propagation between tools"""
        
        # Process Sequential Thinking
        sequential_result = await sequential_analyzer.analyze(
            sample_sequential_context
        )
        
        # Create Decision Framework context with confidence-based weighting
        # Adjust criteria weights based on sequential thinking confidence
        adjusted_criteria = []
        confidence_factor = sequential_result.conclusion_confidence
        
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
        
        decision_context = DecisionFrameworkContext(
            decision_problem=sequential_result.final_conclusion,
            complexity_level=ComplexityLevel.MODERATE,
            criteria=adjusted_criteria,
            options=sample_decision_options,
            decision_methods=[DecisionMethodType.WEIGHTED_SUM]
        )
        
        decision_result = await decision_analyzer.analyze(
            decision_context
        )
        
        # Verify confidence propagation
        assert 0.0 <= decision_result.confidence_score <= 1.0
        
        # Check that confidence influenced the process
        weight_sum = sum(c.weight for c in adjusted_criteria)
        assert abs(weight_sum - 1.0) < 0.01  # Should sum to 1.0
        
        print(f"✅ Confidence propagation test passed:")
        print(f"   Sequential confidence: {sequential_result.conclusion_confidence:.3f}")
        print(f"   Decision confidence: {decision_result.confidence_score:.3f}")
        print(f"   Criteria weight sum: {weight_sum:.3f}")


# ============================================================================
# Expand: Error Handling and Recovery
# ============================================================================

class TestErrorHandling:
    """Test error propagation and recovery between tools"""
    
    @pytest.mark.asyncio
    async def test_sequential_thinking_error_propagation(
        self,
        decision_analyzer,
        sample_decision_criteria,
        sample_decision_options
    ):
        """Test handling of Sequential Thinking failures"""
        
        # Simulate Sequential Thinking failure by using empty conclusion
        invalid_sequential_result = SequentialThinkingResult(
            reasoning_chain=[ThoughtStep(
                step_number=1,
                step_type=ThoughtStepType.PROBLEM_DECOMPOSITION,
                content="Failed to properly analyze the problem",
                confidence_score=0.1
            )],
            branches_explored=[],
            revisions_made=[],
            final_conclusion="Unable to reach a meaningful conclusion",
            conclusion_confidence=0.1,
            reasoning_quality_score=0.1,
            critical_assumptions=[],
            evidence_gaps=["All evidence missing"],
            alternative_conclusions=[],
            reasoning_path_summary="Failed processing",
            recommendations=[],
            processing_time_ms=100
        )
        
        # Try to use invalid output in Decision Framework
        decision_context = DecisionFrameworkContext(
            decision_problem=invalid_sequential_result.final_conclusion or "Fallback problem statement",
            complexity_level=ComplexityLevel.SIMPLE,  # Reduce complexity
            criteria=sample_decision_criteria,
            options=sample_decision_options,
            decision_methods=[DecisionMethodType.WEIGHTED_SUM]
        )
        
        # Decision Framework should handle low-quality input gracefully
        decision_result = await decision_analyzer.analyze(
            decision_context
        )
        
        # Should still produce valid output with fallback values
        assert isinstance(decision_result, DecisionFrameworkResult)
        assert decision_result.recommended_option is not None
        # Confidence should be low due to poor input
        assert decision_result.confidence_score < 0.5
        
        print("✅ Error propagation test passed: Decision Framework handled low-quality input")
    
    @pytest.mark.asyncio
    async def test_alternative_conclusions_to_options(
        self,
        sequential_analyzer,
        decision_analyzer,
        sample_sequential_context,
        sample_decision_criteria
    ):
        """Test using alternative conclusions as decision options"""
        
        # Process Sequential Thinking
        sequential_result = await sequential_analyzer.analyze(
            sample_sequential_context
        )
        
        # Create decision options from alternative conclusions
        decision_options = []
        
        # Primary option from main conclusion
        primary_option = DecisionOption(
            name="Primary Solution",
            description=sequential_result.final_conclusion[:200],
            scores={
                "feasibility": sequential_result.conclusion_confidence,
                "impact": 0.8,
                "risk": 1.0 - sequential_result.conclusion_confidence
            },
            assumptions=sequential_result.critical_assumptions[:3]
        )
        decision_options.append(primary_option)
        
        # Alternative options from alternative conclusions
        for i, alt_conclusion in enumerate(sequential_result.alternative_conclusions[:2]):
            alt_option = DecisionOption(
                name=f"Alternative Solution {i+1}",
                description=alt_conclusion[:200],
                scores={
                    "feasibility": 0.6,  # Lower confidence for alternatives
                    "impact": 0.7,
                    "risk": 0.4
                },
                assumptions=["Alternative approach assumptions"]
            )
            decision_options.append(alt_option)
        
        # Create decision context with generated options
        decision_context = DecisionFrameworkContext(
            decision_problem=sequential_result.reasoning_path_summary,
            complexity_level=ComplexityLevel.MODERATE,
            criteria=sample_decision_criteria[:3],  # Use subset
            options=decision_options,
            decision_methods=[DecisionMethodType.WEIGHTED_SUM]
        )
        
        decision_result = await decision_analyzer.analyze(
            decision_context
        )
        
        assert len(decision_result.ranked_options) >= len(decision_options)
        print(f"✅ Alternative conclusions test passed: {len(decision_options)} options analyzed")


# ============================================================================
# Scale: Performance and Load Testing
# ============================================================================

class TestPerformanceIntegration:
    """Test performance and load characteristics of tool integration"""
    
    @pytest.mark.asyncio
    async def test_processing_time_reasonable(
        self,
        sequential_analyzer,
        decision_analyzer,
        sample_sequential_context,
        sample_decision_criteria,
        sample_decision_options
    ):
        """Test that combined processing time is reasonable"""
        
        start_time = time.time()
        
        # Process Sequential Thinking
        sequential_result = await sequential_analyzer.analyze(
            sample_sequential_context
        )
        
        # Process Decision Framework
        decision_context = DecisionFrameworkContext(
            decision_problem=sequential_result.final_conclusion,
            complexity_level=ComplexityLevel.MODERATE,
            criteria=sample_decision_criteria,
            options=sample_decision_options,
            decision_methods=[DecisionMethodType.WEIGHTED_SUM]
        )
        
        decision_result = await decision_analyzer.analyze(
            decision_context
        )
        
        total_time = time.time() - start_time
        
        # Convert ms to seconds for comparison
        sequential_time_s = sequential_result.processing_time_ms / 1000.0
        decision_time_s = decision_result.processing_time_ms / 1000.0
        
        # Validate performance requirements
        assert total_time < 10.0, f"Total processing time {total_time:.2f}s exceeds limit"
        
        print(f"✅ Performance test passed:")
        print(f"   Sequential Thinking: {sequential_time_s:.2f}s")
        print(f"   Decision Framework: {decision_time_s:.2f}s")
        print(f"   Total time: {total_time:.2f}s")
    
    @pytest.mark.asyncio
    async def test_concurrent_processing(
        self,
        sequential_analyzer,
        decision_analyzer,
        sample_decision_criteria,
        sample_decision_options
    ):
        """Test processing multiple problems concurrently"""
        
        # Create multiple problem inputs
        problems = [
            "Database performance optimization challenge",
            "User interface responsiveness issues",
            "API endpoint latency problems"
        ]
        
        async def process_problem_chain(problem: str):
            """Process one complete problem chain"""
            
            # Sequential Thinking
            seq_context = SequentialThinkingContext(
                problem=problem,
                complexity_level=ComplexityLevel.MODERATE,
                reasoning_depth=3,  # Reduced for performance
                enable_branching=False  # Simplified for concurrency
            )
            
            seq_result = await sequential_analyzer.analyze(seq_context)
            
            # Decision Framework
            dec_context = DecisionFrameworkContext(
                decision_problem=seq_result.final_conclusion,
                complexity_level=ComplexityLevel.MODERATE,
                criteria=sample_decision_criteria,
                options=sample_decision_options,
                decision_methods=[DecisionMethodType.WEIGHTED_SUM]
            )
            
            dec_result = await decision_analyzer.analyze(dec_context)
            
            return {
                "problem": problem,
                "sequential_result": seq_result,
                "decision_result": dec_result
            }
        
        # Process all problems concurrently
        start_time = time.time()
        
        tasks = [process_problem_chain(problem) for problem in problems]
        results = await asyncio.gather(*tasks)
        
        total_time = time.time() - start_time
        
        # Validate all results
        assert len(results) == len(problems)
        
        for result in results:
            assert isinstance(result["sequential_result"], SequentialThinkingResult)
            assert isinstance(result["decision_result"], DecisionFrameworkResult)
            assert result["sequential_result"].final_conclusion is not None
            assert result["decision_result"].recommended_option is not None
        
        print(f"✅ Concurrent processing test passed:")
        print(f"   Problems processed: {len(problems)}")
        print(f"   Total time: {total_time:.2f}s")
        print(f"   Average time per problem: {total_time/len(problems):.2f}s")


# ============================================================================
# Integration Health Check
# ============================================================================

class TestIntegrationHealthCheck:
    """Overall integration health and system validation"""
    
    @pytest.mark.asyncio
    async def test_end_to_end_integration_health(
        self,
        sequential_analyzer,
        decision_analyzer,
        sample_sequential_context,
        sample_decision_criteria,
        sample_decision_options
    ):
        """Comprehensive end-to-end integration health check"""
        
        health_results = {
            "sequential_thinking": "healthy",
            "decision_framework": "healthy",
            "integration": None,
            "performance": None
        }
        
        try:
            # Test integration workflow
            start_time = time.time()
            
            sequential_result = await sequential_analyzer.analyze(
                sample_sequential_context
            )
            
            decision_context = DecisionFrameworkContext(
                decision_problem=sequential_result.final_conclusion,
                complexity_level=ComplexityLevel.MODERATE,
                criteria=sample_decision_criteria,
                options=sample_decision_options,
                decision_methods=[DecisionMethodType.WEIGHTED_SUM, DecisionMethodType.TOPSIS]
            )
            
            decision_result = await decision_analyzer.analyze(
                decision_context
            )
            
            processing_time = time.time() - start_time
            
            # Validate integration health
            integration_healthy = (
                decision_result.recommended_option is not None and
                len(decision_result.ranked_options) > 0 and
                decision_result.confidence_score > 0 and
                processing_time < 10.0
            )
            
            health_results["integration"] = "healthy" if integration_healthy else "unhealthy"
            health_results["performance"] = f"{processing_time:.2f}s"
            
            # Additional validation
            assert len(sequential_result.reasoning_chain) >= sample_sequential_context.reasoning_depth
            assert len(decision_result.method_results) == len(decision_context.decision_methods)
            
        except Exception as e:
            health_results["integration"] = f"error: {e}"
        
        # Report health status
        print("🏥 Integration Health Check Results:")
        for component, status in health_results.items():
            print(f"   {component}: {status}")
        
        # Validate overall health
        assert health_results["integration"] == "healthy"
        
        print("✅ Integration health check passed")
        print(f"   Reasoning steps: {len(sequential_result.reasoning_chain)}")
        print(f"   Decision methods: {len(decision_result.method_results)}")
        print(f"   Confidence: Sequential={sequential_result.conclusion_confidence:.2f}, Decision={decision_result.confidence_score:.2f}")


async def test_evidence_gap_to_uncertainty_mapping(
        self,
        sequential_analyzer,
        decision_analyzer,
        sample_sequential_context,
        sample_decision_criteria,
        sample_decision_options
    ):
        """Test mapping evidence gaps to decision uncertainties"""
        
        # Process Sequential Thinking
        sequential_result = await sequential_analyzer.analyze(
            sample_sequential_context
        )
        
        # Map evidence gaps to uncertainty factors
        uncertainty_factors = sequential_result.evidence_gaps[:5]  # Use top 5 gaps
        
        # Create decision context with uncertainties
        decision_context = DecisionFrameworkContext(
            decision_problem=sequential_result.final_conclusion,
            complexity_level=ComplexityLevel.MODERATE,
            criteria=sample_decision_criteria,
            options=sample_decision_options,
            decision_methods=[DecisionMethodType.WEIGHTED_SUM],
            uncertainty_factors=uncertainty_factors
        )
        
        decision_result = await decision_analyzer.analyze(
            decision_context
        )
        
        # Verify uncertainty handling
        assert decision_context.uncertainty_factors == uncertainty_factors
        assert decision_result.sensitivity_analysis is not None
        
        print(f"✅ Evidence gap mapping test passed:")
        print(f"   Evidence gaps: {len(sequential_result.evidence_gaps)}")
        print(f"   Uncertainty factors: {len(uncertainty_factors)}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])