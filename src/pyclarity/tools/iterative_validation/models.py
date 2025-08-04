"""
Models for Iterative Validation Cognitive Tool

Defines data structures for systematic hypothesis-test-learn-refine cycles.
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field, field_validator
from enum import Enum

from ..base import ComplexityLevel


class ValidationStatus(str, Enum):
    """Status of a validation cycle."""
    NOT_STARTED = "not_started"
    HYPOTHESIS_FORMED = "hypothesis_formed"
    TEST_DESIGNED = "test_designed"
    TEST_IN_PROGRESS = "test_in_progress"
    RESULTS_COLLECTED = "results_collected"
    ANALYSIS_COMPLETE = "analysis_complete"
    LEARNINGS_EXTRACTED = "learnings_extracted"
    REFINED = "refined"


class TestType(str, Enum):
    """Types of tests for validation."""
    EXPERIMENT = "experiment"          # Controlled experiment
    PROTOTYPE = "prototype"            # Build and test prototype
    SURVEY = "survey"                  # Gather feedback
    A_B_TEST = "a_b_test"             # Compare alternatives
    SIMULATION = "simulation"          # Model-based testing
    PILOT = "pilot"                    # Real-world trial
    ANALYSIS = "analysis"              # Data analysis
    USER_TEST = "user_test"           # User experience testing
    TECHNICAL_TEST = "technical_test"  # Technical validation
    MARKET_TEST = "market_test"       # Market validation


class ConfidenceLevel(str, Enum):
    """Confidence level in hypothesis or results."""
    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class LearningType(str, Enum):
    """Types of learnings from validation."""
    CONFIRMATION = "confirmation"      # Hypothesis confirmed
    REFUTATION = "refutation"         # Hypothesis rejected
    PARTIAL = "partial"               # Partially validated
    UNEXPECTED = "unexpected"         # Unexpected discovery
    INCONCLUSIVE = "inconclusive"     # No clear conclusion
    DIRECTIONAL = "directional"       # Indicates direction


class Hypothesis(BaseModel):
    """Represents a hypothesis to be validated."""
    statement: str = Field(description="Clear statement of the hypothesis")
    assumptions: List[str] = Field(description="Underlying assumptions", min_length=1)
    success_criteria: List[str] = Field(
        description="Criteria for validating the hypothesis",
        min_length=1
    )
    confidence_level: ConfidenceLevel = Field(
        description="Initial confidence in the hypothesis"
    )
    rationale: str = Field(description="Reasoning behind the hypothesis")
    risks: List[str] = Field(
        default_factory=list,
        description="Risks if hypothesis is wrong"
    )
    related_hypotheses: List[str] = Field(
        default_factory=list,
        description="Related or dependent hypotheses"
    )


class TestDesign(BaseModel):
    """Design for testing a hypothesis."""
    test_type: TestType = Field(description="Type of test to conduct")
    methodology: str = Field(description="How the test will be conducted")
    metrics: List[str] = Field(
        description="What will be measured",
        min_length=1
    )
    sample_size: Optional[str] = Field(
        None,
        description="Size of test sample/scope"
    )
    duration: Optional[str] = Field(
        None,
        description="Expected test duration"
    )
    resources_needed: List[str] = Field(
        default_factory=list,
        description="Resources required for the test"
    )
    controls: List[str] = Field(
        default_factory=list,
        description="Control variables or conditions"
    )
    success_threshold: Optional[str] = Field(
        None,
        description="Threshold for success"
    )


class TestResults(BaseModel):
    """Results from a validation test."""
    raw_data: Dict[str, Any] = Field(
        description="Raw test data/observations"
    )
    key_findings: List[str] = Field(
        description="Main findings from the test",
        min_length=1
    )
    metrics_achieved: Dict[str, str] = Field(
        description="Metrics and their achieved values"
    )
    unexpected_observations: List[str] = Field(
        default_factory=list,
        description="Unexpected findings"
    )
    confidence_in_results: ConfidenceLevel = Field(
        description="Confidence in the results"
    )
    limitations: List[str] = Field(
        default_factory=list,
        description="Limitations of the test"
    )


class Learning(BaseModel):
    """Learning extracted from validation cycle."""
    learning_type: LearningType = Field(description="Type of learning")
    key_insight: str = Field(description="Main insight gained")
    supporting_evidence: List[str] = Field(
        description="Evidence supporting the learning",
        min_length=1
    )
    implications: List[str] = Field(
        description="Implications of this learning"
    )
    confidence_level: ConfidenceLevel = Field(
        description="Confidence in the learning"
    )
    actionable_items: List[str] = Field(
        default_factory=list,
        description="Actions based on this learning"
    )


class Refinement(BaseModel):
    """Refinement based on learnings."""
    original_element: str = Field(
        description="What is being refined (hypothesis, approach, etc.)"
    )
    refinement_description: str = Field(
        description="Description of the refinement"
    )
    rationale: str = Field(description="Why this refinement is needed")
    expected_improvement: str = Field(
        description="Expected improvement from refinement"
    )
    implementation_steps: List[str] = Field(
        description="Steps to implement the refinement"
    )


class ValidationCycle(BaseModel):
    """Complete validation cycle from hypothesis to refinement."""
    cycle_number: int = Field(
        description="Which iteration this is",
        ge=1
    )
    hypothesis: Hypothesis = Field(description="The hypothesis being tested")
    test_design: TestDesign = Field(description="How the hypothesis was tested")
    test_results: TestResults = Field(description="Results from the test")
    learnings: List[Learning] = Field(description="Learnings extracted")
    refinements: List[Refinement] = Field(
        description="Refinements based on learnings"
    )
    status: ValidationStatus = Field(
        description="Current status of the cycle"
    )
    duration: Optional[str] = Field(
        None,
        description="Time taken for this cycle"
    )


class IterativeValidationContext(BaseModel):
    """Input context for Iterative Validation analysis."""
    scenario: str = Field(
        description="The problem or question requiring iterative validation"
    )
    complexity_level: ComplexityLevel = Field(
        default=ComplexityLevel.MODERATE,
        description="Complexity of analysis"
    )
    domain_context: Optional[str] = Field(
        None,
        description="Domain context (e.g., 'product_development', 'research')"
    )
    initial_hypothesis: Optional[Hypothesis] = Field(
        None,
        description="Starting hypothesis if available"
    )
    validation_constraints: Optional[Dict[str, str]] = Field(
        None,
        description="Constraints on validation (time, resources, scope)"
    )
    previous_cycles: Optional[List[ValidationCycle]] = Field(
        default_factory=list,
        description="Previous validation cycles if continuing"
    )
    target_confidence: Optional[ConfidenceLevel] = Field(
        ConfidenceLevel.HIGH,
        description="Target confidence level to achieve"
    )
    max_iterations: Optional[int] = Field(
        None,
        description="Maximum number of iterations allowed"
    )
    test_preferences: Optional[List[TestType]] = Field(
        default_factory=list,
        description="Preferred types of tests"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "scenario": "Determining optimal pricing strategy for new SaaS product",
                "complexity_level": "moderate",
                "domain_context": "product_development",
                "validation_constraints": {
                    "timeline": "3 months",
                    "budget": "$10,000"
                },
                "target_confidence": "high",
                "max_iterations": 3
            }
        }


class IterativeValidationResult(BaseModel):
    """Output from Iterative Validation analysis."""
    input_scenario: str = Field(description="The analyzed scenario")
    validation_cycles: List[ValidationCycle] = Field(
        description="All validation cycles conducted"
    )
    current_hypothesis: Hypothesis = Field(
        description="Current refined hypothesis"
    )
    cumulative_learnings: List[Learning] = Field(
        description="All learnings across cycles"
    )
    convergence_analysis: str = Field(
        description="Analysis of convergence toward validated solution"
    )
    confidence_progression: Dict[int, ConfidenceLevel] = Field(
        description="Confidence level progression across cycles"
    )
    key_pivots: List[str] = Field(
        description="Major pivots or direction changes"
    )
    remaining_uncertainties: List[str] = Field(
        description="Uncertainties still to be resolved"
    )
    recommended_next_steps: List[str] = Field(
        description="Recommended next validation steps"
    )
    success_factors: List[str] = Field(
        description="Factors contributing to validation success"
    )
    failure_points: List[str] = Field(
        description="Where validations failed or struggled"
    )
    methodology_insights: List[str] = Field(
        description="Insights about the validation process itself"
    )
    overall_assessment: str = Field(
        description="Overall assessment of the validation process"
    )
    confidence_score: float = Field(
        description="Overall confidence in the conclusions (0.0-1.0)",
        ge=0.0,
        le=1.0
    )
    processing_time_ms: Optional[float] = Field(
        None,
        description="Processing time in milliseconds"
    )