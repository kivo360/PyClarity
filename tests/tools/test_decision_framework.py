"""Test Decision Framework cognitive tool.

Tests adapted from FastMCP implementation to work with PyClarity's async analyzer pattern.
"""

import pytest
import pytest_asyncio
import math
from typing import List, Dict

from pyclarity.tools.decision_framework.models import (
    DecisionFrameworkContext,
    DecisionFrameworkResult,
    DecisionCriteria,
    DecisionOption,
    DecisionMatrix,
    RiskAssessment,
    RiskLevel,
    TradeOffAnalysis,
    SensitivityAnalysis,
    DecisionMethodType,
    CriteriaType,
    ComplexityLevel
)
from pyclarity.tools.decision_framework.analyzer import DecisionFrameworkAnalyzer


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def simple_criteria():
    """Generate simple 2-criteria test data"""
    return [
        DecisionCriteria(
            name="Cost",
            description="Implementation cost in USD",
            weight=0.6,
            criteria_type=CriteriaType.COST,
            measurement_unit="USD",
            maximum_threshold=50000.0
        ),
        DecisionCriteria(
            name="Performance",
            description="System performance rating",
            weight=0.4,
            criteria_type=CriteriaType.BENEFIT,
            measurement_unit="Score",
            minimum_threshold=0.7
        )
    ]


@pytest.fixture
def simple_options():
    """Generate simple 3-option test data"""
    return [
        DecisionOption(
            name="Option A",
            description="Low-cost basic solution",
            scores={"Cost": 0.8, "Performance": 0.6},
            raw_values={"Cost": 20000, "Performance": 0.6},
            confidence_scores={"Cost": 0.9, "Performance": 0.7},
            risks=["Limited scalability", "Basic features only"],
            assumptions=["Current requirements remain stable"]
        ),
        DecisionOption(
            name="Option B", 
            description="Balanced mid-range solution",
            scores={"Cost": 0.5, "Performance": 0.8},
            raw_values={"Cost": 35000, "Performance": 0.8},
            confidence_scores={"Cost": 0.8, "Performance": 0.9},
            risks=["Moderate complexity"],
            assumptions=["Team can handle moderate complexity"]
        ),
        DecisionOption(
            name="Option C",
            description="High-performance premium solution", 
            scores={"Cost": 0.2, "Performance": 0.95},
            raw_values={"Cost": 48000, "Performance": 0.95},
            confidence_scores={"Cost": 0.85, "Performance": 0.95},
            risks=["High initial investment", "Complex maintenance"],
            assumptions=["Budget approval available", "Technical expertise in team"]
        )
    ]


@pytest.fixture  
def complex_criteria():
    """Generate complex multi-criteria test data"""
    return [
        DecisionCriteria(name="Cost", weight=0.25, criteria_type=CriteriaType.COST),
        DecisionCriteria(name="Performance", weight=0.2, criteria_type=CriteriaType.BENEFIT),
        DecisionCriteria(name="Reliability", weight=0.2, criteria_type=CriteriaType.BENEFIT),
        DecisionCriteria(name="Scalability", weight=0.15, criteria_type=CriteriaType.BENEFIT),
        DecisionCriteria(name="Security", weight=0.2, criteria_type=CriteriaType.CONSTRAINT)
    ]


@pytest.fixture
def complex_options():
    """Generate complex multi-option test data"""
    return [
        DecisionOption(
            name="Cloud Solution",
            scores={"Cost": 0.7, "Performance": 0.9, "Reliability": 0.85, "Scalability": 0.95, "Security": 0.8},
            risks=["Vendor lock-in", "Data privacy concerns"]
        ),
        DecisionOption(
            name="On-Premise Solution", 
            scores={"Cost": 0.4, "Performance": 0.8, "Reliability": 0.9, "Scalability": 0.6, "Security": 0.95},
            risks=["High maintenance overhead", "Limited scalability"]
        ),
        DecisionOption(
            name="Hybrid Solution",
            scores={"Cost": 0.55, "Performance": 0.85, "Reliability": 0.88, "Scalability": 0.8, "Security": 0.9},
            risks=["Complex architecture", "Integration challenges"]
        )
    ]


@pytest.fixture
def sample_context(simple_criteria, simple_options):
    """Generate sample DecisionFrameworkContext for testing"""
    return DecisionFrameworkContext(
        decision_problem="Select the best solution for our e-commerce platform",
        criteria=simple_criteria,
        options=simple_options,
        decision_methods=[DecisionMethodType.WEIGHTED_SUM, DecisionMethodType.TOPSIS],
        uncertainty_factors=["Market volatility", "Technology changes"],
        time_constraints="3 months for implementation"
    )


@pytest.fixture
def decision_analyzer():
    """Create DecisionFrameworkAnalyzer instance for testing"""
    return DecisionFrameworkAnalyzer()


# ============================================================================
# Model Tests - DecisionCriteria
# ============================================================================

class TestDecisionCriteria:
    """Test suite for DecisionCriteria model"""
    
    def test_criteria_creation_valid(self, simple_criteria):
        """Test creating valid decision criteria"""
        cost_criteria = simple_criteria[0]
        assert cost_criteria.name == "Cost"
        assert cost_criteria.weight == 0.6
        assert cost_criteria.criteria_type == CriteriaType.COST
        assert cost_criteria.measurement_unit == "USD"
        assert cost_criteria.maximum_threshold == 50000.0
    
    def test_criteria_weight_validation(self):
        """Test criteria weight validation"""
        with pytest.raises(ValueError, match="Input should be greater than or equal to 0"):
            DecisionCriteria(
                name="Invalid",
                weight=-0.1,
                criteria_type=CriteriaType.BENEFIT
            )
        
        with pytest.raises(ValueError, match="Input should be less than or equal to 1"):
            DecisionCriteria(
                name="Invalid",
                weight=1.5,
                criteria_type=CriteriaType.BENEFIT
            )
    
    def test_criteria_threshold_validation(self):
        """Test criteria threshold validation"""
        # Valid criteria with both thresholds
        criteria = DecisionCriteria(
            name="Test",
            weight=0.5,
            criteria_type=CriteriaType.BENEFIT,
            minimum_threshold=0.5,
            maximum_threshold=0.9
        )
        assert criteria.minimum_threshold == 0.5
        assert criteria.maximum_threshold == 0.9


# ============================================================================
# Model Tests - DecisionOption
# ============================================================================

class TestDecisionOption:
    """Test suite for DecisionOption model"""
    
    def test_option_creation_valid(self, simple_options):
        """Test creating valid decision options"""
        option_a = simple_options[0]
        assert option_a.name == "Option A"
        assert option_a.scores["Cost"] == 0.8
        assert option_a.scores["Performance"] == 0.6
        assert len(option_a.risks) == 2
        assert len(option_a.assumptions) == 1
    
    def test_option_score_validation(self):
        """Test option score validation"""
        with pytest.raises(ValueError):
            DecisionOption(
                name="Invalid",
                scores={"Criteria1": 1.5},  # Invalid score > 1
                risks=[]
            )
        
        with pytest.raises(ValueError):
            DecisionOption(
                name="Invalid",
                scores={"Criteria1": -0.1},  # Invalid score < 0
                risks=[]
            )
    
    def test_option_calculate_weighted_score(self, simple_options, simple_criteria):
        """Test weighted score calculation"""
        option_a = simple_options[0]
        criteria_weights = {c.name: c.weight for c in simple_criteria}
        
        weighted_score = option_a.calculate_weighted_score(criteria_weights)
        
        # Expected: 0.8 * 0.6 + 0.6 * 0.4 = 0.48 + 0.24 = 0.72
        assert weighted_score == pytest.approx(0.72, rel=1e-3)


# ============================================================================
# Model Tests - DecisionMatrix
# ============================================================================

class TestDecisionMatrix:
    """Test suite for DecisionMatrix model"""
    
    def test_matrix_creation(self, simple_criteria, simple_options):
        """Test creating a decision matrix"""
        matrix = DecisionMatrix(
            criteria=simple_criteria,
            options=simple_options
        )
        
        assert len(matrix.criteria) == 2
        assert len(matrix.options) == 3
        assert matrix.matrix_id is not None
    
    def test_get_score_matrix(self, simple_criteria, simple_options):
        """Test getting score matrix"""
        matrix = DecisionMatrix(
            criteria=simple_criteria,
            options=simple_options
        )
        
        score_matrix = matrix.get_score_matrix()
        
        assert len(score_matrix) == 3  # 3 options
        assert len(score_matrix[0]) == 2  # 2 criteria
        assert score_matrix[0][0] == 0.8  # Option A, Cost
        assert score_matrix[0][1] == 0.6  # Option A, Performance
    
    def test_get_weighted_scores(self, simple_criteria, simple_options):
        """Test getting weighted scores"""
        matrix = DecisionMatrix(
            criteria=simple_criteria,
            options=simple_options
        )
        
        weighted_scores = matrix.get_weighted_scores()
        
        assert len(weighted_scores) == 3
        # Option A: 0.8 * 0.6 + 0.6 * 0.4 = 0.72
        assert weighted_scores[0] == pytest.approx(0.72, rel=1e-3)


# ============================================================================
# Model Tests - RiskAssessment
# ============================================================================

class TestRiskAssessment:
    """Test suite for RiskAssessment model"""
    
    def test_risk_assessment_creation(self):
        """Test creating a risk assessment"""
        risk = RiskAssessment(
            risk_description="Vendor lock-in with cloud provider",
            probability=0.7,
            impact=0.8,
            risk_level=RiskLevel.HIGH,
            mitigation_strategies=["Multi-cloud strategy", "Open standards"]
        )
        
        assert risk.probability == 0.7
        assert risk.impact == 0.8
        assert risk.risk_level == RiskLevel.HIGH
        assert len(risk.mitigation_strategies) == 2
    
    def test_risk_score_calculation(self):
        """Test risk score calculation"""
        risk = RiskAssessment(
            risk_description="Test risk",
            probability=0.6,
            impact=0.8,
            risk_level=RiskLevel.MEDIUM
        )
        
        # Risk score = probability * impact = 0.6 * 0.8 = 0.48
        assert risk.risk_score == pytest.approx(0.48, rel=1e-3)


# ============================================================================
# Analyzer Tests
# ============================================================================

@pytest.mark.asyncio
class TestDecisionFrameworkAnalyzer:
    """Test suite for DecisionFrameworkAnalyzer"""
    
    async def test_analyzer_initialization(self, decision_analyzer):
        """Test analyzer initialization"""
        assert decision_analyzer.tool_name == "Decision Framework"
        assert decision_analyzer.version == "2.0.0"
    
    async def test_basic_analysis(self, decision_analyzer, sample_context):
        """Test basic decision analysis"""
        result = await decision_analyzer.analyze(sample_context)
        
        assert isinstance(result, DecisionFrameworkResult)
        assert result.recommended_option is not None
        assert result.confidence_score > 0
        assert len(result.method_results) == 2  # Two methods requested
        assert result.processing_time_ms > 0
    
    async def test_weighted_sum_method(self, decision_analyzer, sample_context):
        """Test weighted sum decision method"""
        sample_context.decision_methods = [DecisionMethodType.WEIGHTED_SUM]
        
        result = await decision_analyzer.analyze(sample_context)
        
        assert DecisionMethodType.WEIGHTED_SUM in result.method_results
        ws_result = result.method_results[DecisionMethodType.WEIGHTED_SUM]
        
        # Verify rankings
        assert len(ws_result["rankings"]) == 3
        assert ws_result["rankings"][0]["rank"] == 1
        assert ws_result["rankings"][0]["score"] > ws_result["rankings"][1]["score"]
    
    async def test_topsis_method(self, decision_analyzer, sample_context):
        """Test TOPSIS decision method"""
        sample_context.decision_methods = [DecisionMethodType.TOPSIS]
        
        result = await decision_analyzer.analyze(sample_context)
        
        assert DecisionMethodType.TOPSIS in result.method_results
        topsis_result = result.method_results[DecisionMethodType.TOPSIS]
        
        # Verify TOPSIS specific outputs
        assert "ideal_positive" in topsis_result
        assert "ideal_negative" in topsis_result
        assert "rankings" in topsis_result
        
        # Check closeness coefficients
        for ranking in topsis_result["rankings"]:
            assert 0 <= ranking["closeness_coefficient"] <= 1
    
    async def test_analytic_hierarchy_process(self, decision_analyzer, complex_criteria, complex_options):
        """Test AHP decision method"""
        context = DecisionFrameworkContext(
            decision_problem="Complex multi-criteria decision",
            criteria=complex_criteria,
            options=complex_options,
            decision_methods=[DecisionMethodType.ANALYTIC_HIERARCHY_PROCESS]
        )
        
        result = await decision_analyzer.analyze(context)
        
        assert DecisionMethodType.ANALYTIC_HIERARCHY_PROCESS in result.method_results
        ahp_result = result.method_results[DecisionMethodType.ANALYTIC_HIERARCHY_PROCESS]
        
        # Verify AHP outputs
        assert "consistency_ratio" in ahp_result
        assert ahp_result["consistency_ratio"] >= 0
    
    async def test_expected_value_method(self, decision_analyzer, sample_context):
        """Test expected value decision method"""
        sample_context.decision_methods = [DecisionMethodType.EXPECTED_VALUE]
        
        result = await decision_analyzer.analyze(sample_context)
        
        assert DecisionMethodType.EXPECTED_VALUE in result.method_results
        ev_result = result.method_results[DecisionMethodType.EXPECTED_VALUE]
        
        # Verify expected value calculations
        assert "rankings" in ev_result
        for ranking in ev_result["rankings"]:
            assert "expected_value" in ranking
    
    async def test_decision_tree_method(self, decision_analyzer, sample_context):
        """Test decision tree method"""
        sample_context.decision_methods = [DecisionMethodType.DECISION_TREE]
        
        result = await decision_analyzer.analyze(sample_context)
        
        assert DecisionMethodType.DECISION_TREE in result.method_results
        dt_result = result.method_results[DecisionMethodType.DECISION_TREE]
        
        # Verify decision tree structure
        assert "decision_paths" in dt_result
        assert len(dt_result["decision_paths"]) > 0
    
    async def test_monte_carlo_simulation(self, decision_analyzer, sample_context):
        """Test Monte Carlo simulation method"""
        sample_context.decision_methods = [DecisionMethodType.MONTE_CARLO]
        
        result = await decision_analyzer.analyze(sample_context)
        
        assert DecisionMethodType.MONTE_CARLO in result.method_results
        mc_result = result.method_results[DecisionMethodType.MONTE_CARLO]
        
        # Verify Monte Carlo outputs
        assert "simulations" in mc_result
        assert mc_result["simulations"] > 0
        assert "confidence_intervals" in mc_result
    
    async def test_risk_assessment_generation(self, decision_analyzer, sample_context):
        """Test risk assessment generation"""
        result = await decision_analyzer.analyze(sample_context)
        
        assert len(result.risk_assessments) > 0
        
        for risk in result.risk_assessments:
            assert isinstance(risk, RiskAssessment)
            assert risk.probability > 0
            assert risk.impact > 0
            assert risk.risk_level in RiskLevel
    
    async def test_tradeoff_analysis(self, decision_analyzer, sample_context):
        """Test trade-off analysis"""
        result = await decision_analyzer.analyze(sample_context)
        
        assert len(result.tradeoff_analyses) > 0
        
        for tradeoff in result.tradeoff_analyses:
            assert isinstance(tradeoff, TradeOffAnalysis)
            assert tradeoff.option1 != tradeoff.option2
            assert len(tradeoff.criteria_comparisons) > 0
    
    async def test_sensitivity_analysis(self, decision_analyzer, sample_context):
        """Test sensitivity analysis"""
        result = await decision_analyzer.analyze(sample_context)
        
        assert result.sensitivity_analysis is not None
        assert len(result.sensitivity_analysis.criteria_sensitivities) > 0
        
        for criteria_name, sensitivity_data in result.sensitivity_analysis.criteria_sensitivities.items():
            assert "impact_on_ranking" in sensitivity_data
            assert "threshold_values" in sensitivity_data
    
    async def test_multiple_method_consensus(self, decision_analyzer, sample_context):
        """Test consensus building across multiple methods"""
        sample_context.decision_methods = [
            DecisionMethodType.WEIGHTED_SUM,
            DecisionMethodType.TOPSIS,
            DecisionMethodType.EXPECTED_VALUE
        ]
        
        result = await decision_analyzer.analyze(sample_context)
        
        assert len(result.method_results) == 3
        assert result.consensus_analysis is not None
        assert "agreement_level" in result.consensus_analysis
        assert "method_correlations" in result.consensus_analysis
    
    async def test_uncertainty_handling(self, decision_analyzer, sample_context):
        """Test uncertainty factor handling"""
        sample_context.uncertainty_factors = [
            "Market volatility",
            "Technology changes",
            "Regulatory changes"
        ]
        
        result = await decision_analyzer.analyze(sample_context)
        
        # Check that uncertainty is reflected in confidence scores
        assert result.confidence_score < 1.0
        assert "uncertainty_impact" in result.decision_rationale
    
    async def test_constraint_handling(self, decision_analyzer, simple_criteria, simple_options):
        """Test constraint criteria handling"""
        # Add a constraint criteria
        constraint_criteria = DecisionCriteria(
            name="Compliance",
            weight=0.0,  # Constraints can have 0 weight
            criteria_type=CriteriaType.CONSTRAINT,
            minimum_threshold=0.8
        )
        
        criteria_with_constraint = simple_criteria + [constraint_criteria]
        
        # Update options to include constraint scores
        for option in simple_options:
            option.scores["Compliance"] = 0.85
        
        context = DecisionFrameworkContext(
            decision_problem="Decision with constraints",
            criteria=criteria_with_constraint,
            options=simple_options,
            decision_methods=[DecisionMethodType.WEIGHTED_SUM]
        )
        
        result = await decision_analyzer.analyze(context)
        
        # Verify constraint handling
        assert "constraint_violations" in result.method_results[DecisionMethodType.WEIGHTED_SUM]
    
    async def test_empty_options_error(self, decision_analyzer, simple_criteria):
        """Test error handling for empty options"""
        with pytest.raises(ValueError, match="List should have at least 2 items"):
            context = DecisionFrameworkContext(
                decision_problem="Test problem",
                criteria=simple_criteria,
                options=[],  # Empty options
                decision_methods=[DecisionMethodType.WEIGHTED_SUM]
            )
    
    async def test_criteria_weight_normalization(self, decision_analyzer):
        """Test that criteria weights are normalized"""
        # Create criteria with weights that don't sum to 1
        criteria = [
            DecisionCriteria(name="A", weight=0.5, criteria_type=CriteriaType.BENEFIT),
            DecisionCriteria(name="B", weight=0.3, criteria_type=CriteriaType.BENEFIT),
            DecisionCriteria(name="C", weight=0.4, criteria_type=CriteriaType.COST)
        ]
        
        options = [
            DecisionOption(name="Opt1", scores={"A": 0.8, "B": 0.7, "C": 0.6}),
            DecisionOption(name="Opt2", scores={"A": 0.6, "B": 0.9, "C": 0.4})
        ]
        
        context = DecisionFrameworkContext(
            decision_problem="Test normalization",
            criteria=criteria,
            options=options,
            decision_methods=[DecisionMethodType.WEIGHTED_SUM]
        )
        
        result = await decision_analyzer.analyze(context)
        
        # Should complete successfully with normalized weights
        assert result.recommended_option is not None