"""Test Scientific Method cognitive tool.

Tests adapted from FastMCP implementation to work with PyClarity's async analyzer pattern.
"""

import pytest
import pytest_asyncio
from typing import List, Dict
import math

from pyclarity.tools.scientific_method.models import (
    ScientificMethodContext,
    ScientificMethodResult,
    Hypothesis,
    Experiment,
    ExperimentResult,
    DataPoint,
    StatisticalAnalysis,
    Conclusion,
    ExperimentType,
    VariableType,
    Variable,
    ComplexityLevel
)
from pyclarity.tools.scientific_method.analyzer import ScientificMethodAnalyzer


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def simple_hypothesis():
    """Generate simple hypothesis for testing"""
    return Hypothesis(
        statement="Implementing caching will reduce API response time by 50%",
        rationale="Database queries are the primary bottleneck",
        testable_predictions=[
            "Response time will decrease from 200ms to 100ms",
            "Database load will decrease by 60%"
        ],
        variables_involved=["cache_enabled", "response_time", "db_load"],
        assumptions=["Current traffic patterns remain stable"]
    )


@pytest.fixture
def simple_variables():
    """Generate simple variables for testing"""
    return [
        Variable(
            name="cache_enabled",
            variable_type=VariableType.INDEPENDENT,
            description="Whether caching is enabled",
            measurement_unit="boolean",
            expected_range="true/false"
        ),
        Variable(
            name="response_time",
            variable_type=VariableType.DEPENDENT,
            description="API response time",
            measurement_unit="milliseconds",
            expected_range="50-500"
        ),
        Variable(
            name="traffic_volume",
            variable_type=VariableType.CONTROLLED,
            description="Number of requests per second",
            measurement_unit="requests/second",
            expected_range="100-1000"
        )
    ]


@pytest.fixture
def simple_experiment(simple_hypothesis):
    """Generate simple experiment for testing"""
    return Experiment(
        name="Cache Performance Test",
        description="Test impact of caching on API performance",
        hypothesis=simple_hypothesis,
        experiment_type=ExperimentType.CONTROLLED,
        control_variables=["traffic_volume", "data_size"],
        independent_variables=["cache_enabled"],
        dependent_variables=["response_time", "db_load"],
        methodology="A/B test with cache enabled/disabled",
        sample_size=1000,
        duration_hours=24
    )


@pytest.fixture
def simple_context(simple_hypothesis, simple_variables):
    """Generate simple ScientificMethodContext for testing"""
    return ScientificMethodContext(
        research_question="How can we improve API performance?",
        domain_context="E-commerce API with high read traffic",
        hypotheses=[simple_hypothesis],
        variables=simple_variables,
        available_data=["API logs", "Database metrics"],
        constraints=["Production system", "Limited test window"],
        success_criteria=["50% reduction in response time", "No increase in error rate"]
    )


@pytest.fixture
def scientific_analyzer():
    """Create ScientificMethodAnalyzer instance for testing"""
    return ScientificMethodAnalyzer()


# ============================================================================
# Model Tests
# ============================================================================

class TestHypothesis:
    """Test suite for Hypothesis model"""
    
    def test_hypothesis_creation_valid(self, simple_hypothesis):
        """Test creating valid hypothesis"""
        assert simple_hypothesis.statement
        assert len(simple_hypothesis.testable_predictions) == 2
        assert len(simple_hypothesis.variables_involved) == 3
        assert simple_hypothesis.hypothesis_id is not None
        assert simple_hypothesis.confidence_score == 0.0  # Initial confidence
    
    def test_hypothesis_validation_statement_too_short(self):
        """Test hypothesis statement validation"""
        with pytest.raises(ValueError, match="String should have at least 10 characters"):
            Hypothesis(
                statement="Too short",
                rationale="Valid rationale",
                testable_predictions=["prediction"],
                variables_involved=["var1"]
            )
    
    def test_hypothesis_validation_no_predictions(self):
        """Test hypothesis must have predictions"""
        with pytest.raises(ValueError, match="List should have at least 1 item"):
            Hypothesis(
                statement="Valid hypothesis statement",
                rationale="Valid rationale",
                testable_predictions=[],
                variables_involved=["var1"]
            )


class TestExperiment:
    """Test suite for Experiment model"""
    
    def test_experiment_creation_valid(self, simple_experiment):
        """Test creating valid experiment"""
        assert simple_experiment.name == "Cache Performance Test"
        assert simple_experiment.experiment_type == ExperimentType.CONTROLLED
        assert simple_experiment.sample_size == 1000
        assert simple_experiment.status == "planned"
    
    def test_experiment_validation_sample_size(self):
        """Test experiment sample size validation"""
        with pytest.raises(ValueError, match="Input should be greater than or equal to 1"):
            Experiment(
                name="Test",
                description="Test experiment",
                hypothesis=Hypothesis(
                    statement="Test hypothesis",
                    rationale="Test",
                    testable_predictions=["pred"],
                    variables_involved=["var"]
                ),
                experiment_type=ExperimentType.OBSERVATIONAL,
                sample_size=0
            )


class TestDataPoint:
    """Test suite for DataPoint model"""
    
    def test_datapoint_creation(self):
        """Test creating data points"""
        dp = DataPoint(
            timestamp="2024-01-01T10:00:00",
            variable_name="response_time",
            value=150.5,
            metadata={"server": "api-1", "cache_hit": True}
        )
        
        assert dp.variable_name == "response_time"
        assert dp.value == 150.5
        assert dp.metadata["cache_hit"] is True


class TestStatisticalAnalysis:
    """Test suite for StatisticalAnalysis model"""
    
    def test_statistical_analysis_creation(self):
        """Test creating statistical analysis"""
        analysis = StatisticalAnalysis(
            test_type="t-test",
            test_statistic=2.45,
            p_value=0.014,
            confidence_level=0.95,
            sample_size=1000,
            degrees_of_freedom=999,
            effect_size=0.35,
            power_analysis=0.80
        )
        
        assert analysis.test_type == "t-test"
        assert analysis.p_value == 0.014
        assert analysis.effect_size == 0.35
        assert analysis.is_significant is True  # p < 0.05


# ============================================================================
# Analyzer Tests
# ============================================================================

@pytest.mark.asyncio
class TestScientificMethodAnalyzer:
    """Test suite for ScientificMethodAnalyzer"""
    
    async def test_analyzer_initialization(self, scientific_analyzer):
        """Test analyzer initialization"""
        assert scientific_analyzer.tool_name == "Scientific Method"
        assert scientific_analyzer.version == "2.0.0"
    
    async def test_basic_analysis(self, scientific_analyzer, simple_context):
        """Test basic scientific method analysis"""
        result = await scientific_analyzer.analyze(simple_context)
        
        assert isinstance(result, ScientificMethodResult)
        assert len(result.hypotheses) == 1
        assert len(result.experiments) > 0
        assert result.synthesis is not None
        assert result.processing_time_ms > 0
    
    async def test_hypothesis_formulation(self, scientific_analyzer, simple_context):
        """Test hypothesis formulation"""
        result = await scientific_analyzer.analyze(simple_context)
        
        # Should have the input hypothesis
        assert len(result.hypotheses) >= 1
        hypothesis = result.hypotheses[0]
        assert hypothesis.statement
        assert len(hypothesis.testable_predictions) > 0
        assert hypothesis.confidence_score >= 0
    
    async def test_experiment_design(self, scientific_analyzer, simple_context):
        """Test experiment design generation"""
        result = await scientific_analyzer.analyze(simple_context)
        
        assert len(result.experiments) > 0
        
        for experiment in result.experiments:
            assert isinstance(experiment, Experiment)
            assert experiment.name
            assert experiment.methodology
            assert experiment.experiment_type in ExperimentType
            assert len(experiment.dependent_variables) > 0
    
    async def test_controlled_experiment_type(self, scientific_analyzer, simple_context):
        """Test controlled experiment design"""
        result = await scientific_analyzer.analyze(simple_context)
        
        controlled_experiments = [e for e in result.experiments if e.experiment_type == ExperimentType.CONTROLLED]
        
        if controlled_experiments:
            exp = controlled_experiments[0]
            assert len(exp.control_variables) > 0
            assert len(exp.independent_variables) > 0
            assert len(exp.dependent_variables) > 0
    
    async def test_experiment_results_simulation(self, scientific_analyzer, simple_context):
        """Test experiment results simulation"""
        simple_context.simulate_results = True
        
        result = await scientific_analyzer.analyze(simple_context)
        
        assert len(result.experiment_results) > 0
        
        for exp_result in result.experiment_results:
            assert isinstance(exp_result, ExperimentResult)
            assert len(exp_result.data_points) > 0
            assert exp_result.summary_statistics
            assert "mean" in exp_result.summary_statistics
    
    async def test_statistical_analysis_generation(self, scientific_analyzer, simple_context):
        """Test statistical analysis generation"""
        simple_context.simulate_results = True
        
        result = await scientific_analyzer.analyze(simple_context)
        
        assert len(result.statistical_analyses) > 0
        
        for analysis in result.statistical_analyses:
            assert isinstance(analysis, StatisticalAnalysis)
            assert analysis.test_type
            assert analysis.p_value >= 0
            assert analysis.confidence_level > 0
    
    async def test_conclusion_generation(self, scientific_analyzer, simple_context):
        """Test conclusion generation"""
        result = await scientific_analyzer.analyze(simple_context)
        
        assert len(result.conclusions) > 0
        
        for conclusion in result.conclusions:
            assert isinstance(conclusion, Conclusion)
            assert conclusion.statement
            assert conclusion.supporting_evidence
            assert 0 <= conclusion.confidence_level <= 1
    
    async def test_peer_review_suggestions(self, scientific_analyzer, simple_context):
        """Test peer review suggestions generation"""
        result = await scientific_analyzer.analyze(simple_context)
        
        assert len(result.peer_review_suggestions) > 0
        
        for suggestion in result.peer_review_suggestions:
            assert len(suggestion) > 20  # Meaningful suggestion
    
    async def test_multiple_hypotheses(self, scientific_analyzer, simple_variables):
        """Test handling multiple hypotheses"""
        hypothesis1 = Hypothesis(
            statement="Caching improves performance",
            rationale="Reduces database load",
            testable_predictions=["Response time decreases"],
            variables_involved=["cache_enabled", "response_time"]
        )
        
        hypothesis2 = Hypothesis(
            statement="Connection pooling improves performance",
            rationale="Reduces connection overhead",
            testable_predictions=["Connection time decreases"],
            variables_involved=["pool_size", "connection_time"]
        )
        
        context = ScientificMethodContext(
            research_question="How to improve system performance?",
            domain_context="Web application",
            hypotheses=[hypothesis1, hypothesis2],
            variables=simple_variables
        )
        
        result = await scientific_analyzer.analyze(context)
        
        assert len(result.hypotheses) >= 2
        assert len(result.experiments) >= 2  # At least one experiment per hypothesis
    
    async def test_observational_study_design(self, scientific_analyzer):
        """Test observational study design"""
        context = ScientificMethodContext(
            research_question="What factors affect user engagement?",
            domain_context="Social media platform",
            hypotheses=[
                Hypothesis(
                    statement="Post timing affects engagement",
                    rationale="User activity varies by time",
                    testable_predictions=["Peak hours show higher engagement"],
                    variables_involved=["post_time", "engagement_rate"]
                )
            ],
            variables=[
                Variable(name="post_time", variable_type=VariableType.INDEPENDENT),
                Variable(name="engagement_rate", variable_type=VariableType.DEPENDENT)
            ],
            constraints=["Cannot control when users post"]
        )
        
        result = await scientific_analyzer.analyze(context)
        
        observational = [e for e in result.experiments if e.experiment_type == ExperimentType.OBSERVATIONAL]
        assert len(observational) > 0
    
    async def test_longitudinal_study_design(self, scientific_analyzer):
        """Test longitudinal study design"""
        context = ScientificMethodContext(
            research_question="How does system performance degrade over time?",
            domain_context="Long-running service",
            hypotheses=[
                Hypothesis(
                    statement="Performance degrades linearly with uptime",
                    rationale="Memory leaks accumulate",
                    testable_predictions=["Response time increases with uptime"],
                    variables_involved=["uptime", "response_time"]
                )
            ],
            variables=[
                Variable(name="uptime", variable_type=VariableType.INDEPENDENT),
                Variable(name="response_time", variable_type=VariableType.DEPENDENT)
            ]
        )
        
        result = await scientific_analyzer.analyze(context)
        
        longitudinal = [e for e in result.experiments if e.experiment_type == ExperimentType.LONGITUDINAL]
        assert len(longitudinal) > 0
        assert longitudinal[0].duration_hours > 24  # Should be long-term
    
    async def test_complexity_impact(self, scientific_analyzer, simple_variables):
        """Test that complexity affects analysis depth"""
        simple_context = ScientificMethodContext(
            research_question="Simple optimization test",
            domain_context="Basic system",
            hypotheses=[
                Hypothesis(
                    statement="Simple change improves performance",
                    rationale="Basic reasoning",
                    testable_predictions=["Metric improves"],
                    variables_involved=["var1", "var2"]
                )
            ],
            variables=simple_variables[:2],
            complexity_level=ComplexityLevel.SIMPLE
        )
        
        complex_context = ScientificMethodContext(
            research_question="Complex system optimization with multiple interacting factors",
            domain_context="Large-scale distributed system with multiple dependencies",
            hypotheses=[
                Hypothesis(
                    statement="Multi-factor optimization improves overall system performance",
                    rationale="Complex interactions between components",
                    testable_predictions=[
                        "Latency decreases across all services",
                        "Throughput increases non-linearly",
                        "Resource utilization optimizes"
                    ],
                    variables_involved=["var1", "var2", "var3", "var4"]
                )
            ],
            variables=simple_variables,
            complexity_level=ComplexityLevel.COMPLEX
        )
        
        simple_result = await scientific_analyzer.analyze(simple_context)
        complex_result = await scientific_analyzer.analyze(complex_context)
        
        # Complex analysis should be more thorough
        assert len(complex_result.experiments) >= len(simple_result.experiments)
        assert len(complex_result.peer_review_suggestions) >= len(simple_result.peer_review_suggestions)
    
    async def test_future_work_recommendations(self, scientific_analyzer, simple_context):
        """Test future work recommendations"""
        result = await scientific_analyzer.analyze(simple_context)
        
        assert len(result.future_work_recommendations) > 0
        
        for recommendation in result.future_work_recommendations:
            assert len(recommendation) > 30  # Should be detailed
    
    async def test_confidence_score_calculation(self, scientific_analyzer, simple_context):
        """Test overall confidence score calculation"""
        result = await scientific_analyzer.analyze(simple_context)
        
        assert 0 <= result.confidence_score <= 1
        
        # With well-defined context, confidence should be reasonable
        assert result.confidence_score > 0.4