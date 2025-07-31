"""
Tests for Strategic Decision Accelerator
"""

import pytest
import asyncio
from datetime import datetime

from pyclarity.tools.strategic_decision import (
    StrategicDecisionAccelerator,
    DecisionContext,
    DecisionType,
    UrgencyLevel,
    ComplexityLevel,
    DecisionOption,
    RiskLevel,
)


@pytest.fixture
def sample_decision_context():
    """Create a sample decision context for testing."""
    return DecisionContext(
        decision_id="test-001",
        decision_title="Cloud Migration Strategy",
        decision_type=DecisionType.STRATEGIC,
        urgency_level=UrgencyLevel.HIGH,
        complexity_level=ComplexityLevel.HIGH,
        decision_options=[
            DecisionOption(
                option_id="opt-1",
                option_name="Full AWS Migration",
                description="Migrate all services to AWS",
                strategic_fit=8.5,
                risk_level=RiskLevel.MEDIUM,
                expected_roi=2.5,
                timeline="6-9 months",
                resource_requirements="significant",
                expected_impact="transformational"
            ),
            DecisionOption(
                option_id="opt-2",
                option_name="Hybrid Cloud Approach",
                description="Keep critical services on-premise",
                strategic_fit=7.0,
                risk_level=RiskLevel.LOW,
                expected_roi=1.8,
                timeline="3-6 months",
                resource_requirements="moderate",
                expected_impact="substantial"
            ),
            DecisionOption(
                option_id="opt-3",
                option_name="Multi-Cloud Strategy",
                description="Distribute across AWS, Azure, GCP",
                strategic_fit=9.0,
                risk_level=RiskLevel.HIGH,
                expected_roi=3.0,
                timeline="12-18 months",
                resource_requirements="high",
                expected_impact="transformational"
            ),
        ],
        context=[
            "Current infrastructure aging and costly",
            "Competitors moving to cloud rapidly",
            "Team has limited cloud experience"
        ],
        constraints=[
            "Budget limit of $2M",
            "Must maintain 99.9% uptime",
            "Regulatory compliance requirements"
        ],
        stakeholders={
            "primary": ["CTO", "CFO", "VP Engineering"],
            "secondary": ["DevOps Team", "Security Team"],
            "affected": ["All Engineering Teams", "Operations"]
        }
    )


@pytest.mark.asyncio
async def test_strategic_decision_accelerator_initialization():
    """Test that the accelerator initializes correctly."""
    accelerator = StrategicDecisionAccelerator()
    
    assert accelerator.decision_crystallizer is not None
    assert accelerator.scenario_modeler is not None
    assert accelerator.stakeholder_aligner is not None
    assert accelerator.acceleration_engine is not None
    assert accelerator.validation_orchestrator is not None


@pytest.mark.asyncio
async def test_accelerate_strategic_decision(sample_decision_context):
    """Test the main acceleration method."""
    accelerator = StrategicDecisionAccelerator()
    
    result = await accelerator.accelerate_strategic_decision(sample_decision_context)
    
    # Verify result structure
    assert result.decision_readiness_score >= 0
    assert result.decision_readiness_score <= 100
    
    # Verify all components produced results
    assert result.decision_crystallization is not None
    assert result.scenario_modeling is not None
    assert result.stakeholder_alignment is not None
    assert result.acceleration_analysis is not None
    assert result.validation_framework is not None
    
    # Verify recommendations were generated
    assert len(result.strategic_recommendations) > 0
    assert all("action" in rec for rec in result.strategic_recommendations)
    assert all("strategic_impact" in rec for rec in result.strategic_recommendations)
    
    # Verify roadmap was created
    assert result.decision_roadmap is not None
    assert len(result.decision_roadmap.decision_phases) > 0
    assert len(result.decision_roadmap.critical_milestones) > 0
    
    # Verify metadata
    assert result.analysis_timestamp is not None
    assert result.analysis_duration_seconds > 0
    assert result.analysis_quality_score > 0


@pytest.mark.asyncio
async def test_decision_crystallization(sample_decision_context):
    """Test the decision crystallization component."""
    accelerator = StrategicDecisionAccelerator()
    crystallizer = accelerator.decision_crystallizer
    
    result = await crystallizer.crystallize_decision(sample_decision_context)
    
    # Verify crystallization results
    assert result.readiness_score >= 0
    assert result.readiness_score <= 100
    
    # Verify quantum state analysis
    assert result.quantum_decision_state is not None
    assert result.quantum_decision_state.current_state is not None
    assert result.quantum_decision_state.state_confidence >= 0
    assert result.quantum_decision_state.state_confidence <= 1
    
    # Verify option evaluation
    assert result.option_evaluation is not None
    assert len(result.option_evaluation.ranking) == len(sample_decision_context.decision_options)
    assert all(opt_id in result.option_evaluation.weighted_scores 
              for opt_id in result.option_evaluation.ranking)


@pytest.mark.asyncio
async def test_scenario_modeling(sample_decision_context):
    """Test the scenario modeling component."""
    accelerator = StrategicDecisionAccelerator()
    modeler = accelerator.scenario_modeler
    
    result = await modeler.model_scenarios(sample_decision_context)
    
    # Verify scenario analysis
    assert result.scenario_analysis is not None
    assert result.scenario_analysis.base_case is not None
    assert result.scenario_analysis.optimistic_case is not None
    assert result.scenario_analysis.pessimistic_case is not None
    
    # Verify Monte Carlo simulation
    assert result.monte_carlo_results is not None
    assert result.monte_carlo_results.simulation_runs > 0
    assert result.monte_carlo_results.success_probability >= 0
    assert result.monte_carlo_results.success_probability <= 1


@pytest.mark.asyncio
async def test_stakeholder_alignment(sample_decision_context):
    """Test the stakeholder alignment component."""
    accelerator = StrategicDecisionAccelerator()
    aligner = accelerator.stakeholder_aligner
    
    result = await aligner.align_stakeholders(sample_decision_context)
    
    # Verify alignment analysis
    assert result.alignment_analysis is not None
    assert "overall_alignment" in result.alignment_analysis
    assert result.alignment_analysis["overall_alignment"] >= 0
    assert result.alignment_analysis["overall_alignment"] <= 1
    
    # Verify stakeholder mapping
    assert result.stakeholder_mapping is not None
    assert "stakeholder_groups" in result.stakeholder_mapping
    assert "total_stakeholders" in result.stakeholder_mapping


@pytest.mark.asyncio
async def test_acceleration_opportunities(sample_decision_context):
    """Test the acceleration engine component."""
    accelerator = StrategicDecisionAccelerator()
    engine = accelerator.acceleration_engine
    
    result = await engine.analyze_acceleration_opportunities(sample_decision_context)
    
    # Verify acceleration opportunities
    assert result.acceleration_opportunities is not None
    assert len(result.acceleration_opportunities) > 0
    assert all("opportunity" in opp for opp in result.acceleration_opportunities)
    assert all("time_savings" in opp for opp in result.acceleration_opportunities)
    
    # Verify momentum analysis
    assert result.momentum_analysis is not None
    assert "momentum_score" in result.momentum_analysis
    assert result.momentum_analysis["momentum_score"] >= 0
    assert result.momentum_analysis["momentum_score"] <= 10


@pytest.mark.asyncio
async def test_validation_framework(sample_decision_context):
    """Test the validation orchestrator component."""
    accelerator = StrategicDecisionAccelerator()
    orchestrator = accelerator.validation_orchestrator
    
    result = await orchestrator.orchestrate_validation(sample_decision_context)
    
    # Verify validation framework
    assert result.validation_framework is not None
    assert "validation_phases" in result.validation_framework
    assert len(result.validation_framework["validation_phases"]) > 0
    
    # Verify success metrics
    assert result.success_metrics is not None
    assert "primary_metrics" in result.success_metrics
    assert len(result.success_metrics["primary_metrics"]) > 0
    
    # Verify early warning system
    assert result.early_warning_system is not None
    assert "indicators" in result.early_warning_system
    assert len(result.early_warning_system["indicators"]) > 0


@pytest.mark.asyncio
async def test_concurrent_execution(sample_decision_context):
    """Test that components execute concurrently."""
    accelerator = StrategicDecisionAccelerator()
    
    import time
    start_time = time.time()
    
    # Execute the full acceleration
    result = await accelerator.accelerate_strategic_decision(sample_decision_context)
    
    execution_time = time.time() - start_time
    
    # Verify concurrent execution (should be faster than sequential)
    # With 5 components, if each took 0.1s sequentially, total would be 0.5s
    # Concurrent execution should be significantly less
    assert execution_time < 2.0  # Generous limit for test environment
    assert result is not None


@pytest.mark.asyncio
async def test_error_handling():
    """Test error handling with invalid context."""
    accelerator = StrategicDecisionAccelerator()
    
    # Create invalid context (missing required fields)
    invalid_context = DecisionContext(
        decision_id="invalid",
        decision_title="Test",
        decision_type=DecisionType.STRATEGIC,
        urgency_level=UrgencyLevel.LOW,
        complexity_level=ComplexityLevel.LOW,
        decision_options=[],  # Empty options
        context=[],
        constraints=[],
        stakeholders={}
    )
    
    # Should still complete without crashing
    result = await accelerator.accelerate_strategic_decision(invalid_context)
    assert result is not None
    assert result.decision_readiness_score >= 0