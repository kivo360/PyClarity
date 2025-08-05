"""
Debugging Approaches Models

Data structures for systematic troubleshooting methodologies, error classification
and resolution, debugging strategy selection, and root cause analysis frameworks.
"""

import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


class ComplexityLevel(str, Enum):
    """Problem complexity levels"""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    VERY_COMPLEX = "very_complex"


class DebuggingStrategy(str, Enum):
    """Different debugging strategies"""
    PRINT_DEBUGGING = "print_debugging"
    INTERACTIVE_DEBUGGING = "interactive_debugging"
    LOG_ANALYSIS = "log_analysis"
    BINARY_SEARCH = "binary_search"
    RUBBER_DUCK = "rubber_duck"
    UNIT_TESTING = "unit_testing"
    INTEGRATION_TESTING = "integration_testing"
    PROFILING = "profiling"
    STATIC_ANALYSIS = "static_analysis"
    CODE_REVIEW = "code_review"
    DIVIDE_AND_CONQUER = "divide_and_conquer"
    HYPOTHESIS_TESTING = "hypothesis_testing"


class ErrorCategory(str, Enum):
    """Categories of errors"""
    SYNTAX_ERROR = "syntax_error"
    RUNTIME_ERROR = "runtime_error"
    LOGIC_ERROR = "logic_error"
    PERFORMANCE_ERROR = "performance_error"
    MEMORY_ERROR = "memory_error"
    CONCURRENCY_ERROR = "concurrency_error"
    CONFIGURATION_ERROR = "configuration_error"
    INTEGRATION_ERROR = "integration_error"
    USER_INPUT_ERROR = "user_input_error"
    ENVIRONMENT_ERROR = "environment_error"


class Severity(str, Enum):
    """Error severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFORMATIONAL = "informational"


class DebuggingPhase(str, Enum):
    """Phases of the debugging process"""
    PROBLEM_IDENTIFICATION = "problem_identification"
    REPRODUCTION = "reproduction"
    ISOLATION = "isolation"
    ANALYSIS = "analysis"
    HYPOTHESIS_FORMATION = "hypothesis_formation"
    TESTING = "testing"
    RESOLUTION = "resolution"
    VERIFICATION = "verification"
    DOCUMENTATION = "documentation"


class DebugContext(BaseModel):
    """Context information for debugging session"""

    context_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique context identifier"
    )

    system_description: str = Field(
        ...,
        description="Description of the system being debugged",
        min_length=20,
        max_length=1000
    )

    environment: dict[str, str] = Field(
        default_factory=dict,
        description="Environment details (OS, language, framework, etc.)"
    )

    error_symptoms: list[str] = Field(
        ...,
        description="Observable symptoms of the error",
        min_length=1,
        max_length=10
    )

    reproduction_steps: list[str] = Field(
        default_factory=list,
        description="Steps to reproduce the error",
        max_length=15
    )

    constraints: list[str] = Field(
        default_factory=list,
        description="Debugging constraints (time, resources, access)",
        max_length=8
    )

    available_tools: list[str] = Field(
        default_factory=list,
        description="Available debugging tools",
        max_length=15
    )

    time_constraints: str | None = Field(
        None,
        description="Time constraints for debugging",
        max_length=200
    )

    impact_assessment: str = Field(
        ...,
        description="Assessment of the error's impact",
        min_length=10,
        max_length=500
    )

    @field_validator('system_description')
    @classmethod
    def validate_system_description(cls, v):
        """Validate system description"""
        v = v.strip()
        if len(v) < 20:
            raise ValueError("System description must be at least 20 characters")
        return v


class ErrorClassification(BaseModel):
    """Classification of an error or bug"""

    classification_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique classification identifier"
    )

    error_category: ErrorCategory = Field(
        ...,
        description="Category of the error"
    )

    severity: Severity = Field(
        ...,
        description="Severity level of the error"
    )

    error_message: str | None = Field(
        None,
        description="Actual error message if available",
        max_length=1000
    )

    stack_trace: str | None = Field(
        None,
        description="Stack trace if available",
        max_length=5000
    )

    symptoms: list[str] = Field(
        ...,
        description="Observable symptoms",
        min_length=1,
        max_length=10
    )

    potential_causes: list[str] = Field(
        default_factory=list,
        description="Potential causes of the error",
        max_length=8
    )

    affected_components: list[str] = Field(
        default_factory=list,
        description="Components affected by the error",
        max_length=10
    )

    frequency: str = Field(
        ...,
        description="How often the error occurs",
        pattern="^(rare|occasional|frequent|constant)$"
    )

    reproducibility: str = Field(
        ...,
        description="How reproducible the error is",
        pattern="^(always|sometimes|never)$"
    )

    confidence_level: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence in the classification"
    )


class DebuggingHypothesis(BaseModel):
    """A hypothesis about the cause of a bug"""

    hypothesis_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique hypothesis identifier"
    )

    description: str = Field(
        ...,
        description="Description of the hypothesis",
        min_length=20,
        max_length=500
    )

    confidence_level: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence in this hypothesis"
    )

    supporting_evidence: list[str] = Field(
        default_factory=list,
        description="Evidence supporting this hypothesis",
        max_length=8
    )

    contradicting_evidence: list[str] = Field(
        default_factory=list,
        description="Evidence contradicting this hypothesis",
        max_length=8
    )

    test_plan: list[str] = Field(
        default_factory=list,
        description="Steps to test this hypothesis",
        max_length=10
    )

    estimated_effort: str = Field(
        ...,
        description="Estimated effort to test hypothesis",
        pattern="^(low|medium|high)$"
    )

    risk_level: str = Field(
        ...,
        description="Risk level of testing this hypothesis",
        pattern="^(low|medium|high)$"
    )

    alternative_hypotheses: list[str] = Field(
        default_factory=list,
        description="Alternative hypotheses to consider",
        max_length=5
    )


class DebuggingStep(BaseModel):
    """A single step in the debugging process"""

    step_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique step identifier"
    )

    phase: DebuggingPhase = Field(
        ...,
        description="Phase of debugging this step belongs to"
    )

    description: str = Field(
        ...,
        description="Description of the step",
        min_length=10,
        max_length=500
    )

    strategy_used: DebuggingStrategy = Field(
        ...,
        description="Strategy used in this step"
    )

    expected_outcome: str = Field(
        ...,
        description="Expected outcome of this step",
        min_length=10,
        max_length=300
    )

    actual_outcome: str | None = Field(
        None,
        description="Actual outcome after execution",
        max_length=500
    )

    tools_used: list[str] = Field(
        default_factory=list,
        description="Tools used in this step",
        max_length=8
    )

    evidence_gathered: list[str] = Field(
        default_factory=list,
        description="Evidence gathered from this step",
        max_length=10
    )

    time_spent: str | None = Field(
        None,
        description="Time spent on this step",
        max_length=50
    )

    success: bool | None = Field(
        None,
        description="Whether the step was successful"
    )

    next_steps: list[str] = Field(
        default_factory=list,
        description="Recommended next steps",
        max_length=5
    )


class RootCauseAnalysis(BaseModel):
    """Root cause analysis results"""

    analysis_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique analysis identifier"
    )

    problem_statement: str = Field(
        ...,
        description="Clear statement of the problem",
        min_length=20,
        max_length=500
    )

    root_causes: list[str] = Field(
        default_factory=list,
        description="Identified root causes",
        max_length=8
    )

    contributing_factors: list[str] = Field(
        default_factory=list,
        description="Contributing factors to the problem",
        max_length=10
    )

    analysis_method: str = Field(
        ...,
        description="Method used for analysis",
        pattern="^(five_whys|fishbone|fault_tree|pareto_analysis)$"
    )

    evidence_chain: list[str] = Field(
        default_factory=list,
        description="Chain of evidence leading to root cause",
        max_length=10
    )

    prevention_measures: list[str] = Field(
        default_factory=list,
        description="Measures to prevent recurrence",
        max_length=10
    )

    systemic_issues: list[str] = Field(
        default_factory=list,
        description="Systemic issues identified",
        max_length=8
    )

    confidence_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence in the root cause analysis"
    )


class DebuggingSession(BaseModel):
    """Complete debugging session record"""

    session_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique session identifier"
    )

    context: DebugContext = Field(
        ...,
        description="Debugging context"
    )

    error_classification: ErrorClassification = Field(
        ...,
        description="Classification of the error"
    )

    hypotheses: list[DebuggingHypothesis] = Field(
        default_factory=list,
        description="Generated hypotheses",
        max_length=10
    )

    debugging_steps: list[DebuggingStep] = Field(
        default_factory=list,
        description="Steps taken during debugging",
        max_length=20
    )

    root_cause_analysis: RootCauseAnalysis | None = Field(
        None,
        description="Root cause analysis if performed"
    )

    resolution: str | None = Field(
        None,
        description="Final resolution of the problem",
        max_length=1000
    )

    lessons_learned: list[str] = Field(
        default_factory=list,
        description="Lessons learned from the session",
        max_length=10
    )

    prevention_recommendations: list[str] = Field(
        default_factory=list,
        description="Recommendations to prevent similar issues",
        max_length=10
    )

    session_duration: str | None = Field(
        None,
        description="Total duration of the session",
        max_length=50
    )

    success_rate: float = Field(
        0.0,
        ge=0.0,
        le=1.0,
        description="Success rate of debugging steps"
    )


class DebuggingRecommendation(BaseModel):
    """Recommendation for debugging approach"""

    recommendation_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique recommendation identifier"
    )

    recommended_strategy: DebuggingStrategy = Field(
        ...,
        description="Recommended debugging strategy"
    )

    context_match_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="How well the strategy matches the context"
    )

    reasoning: str = Field(
        ...,
        description="Reasoning for the recommendation",
        min_length=20,
        max_length=500
    )

    expected_effectiveness: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Expected effectiveness of the strategy"
    )

    estimated_time: str = Field(
        ...,
        description="Estimated time requirement",
        pattern="^(low|medium|high)$"
    )

    required_tools: list[str] = Field(
        default_factory=list,
        description="Tools required for this strategy",
        max_length=8
    )

    prerequisites: list[str] = Field(
        default_factory=list,
        description="Prerequisites for using this strategy",
        max_length=8
    )

    alternative_strategies: list[DebuggingStrategy] = Field(
        default_factory=list,
        description="Alternative strategies to consider",
        max_length=5
    )

    risk_factors: list[str] = Field(
        default_factory=list,
        description="Risk factors and limitations",
        max_length=8
    )


class DebuggingApproachesContext(BaseModel):
    """Context for debugging approaches analysis"""

    problem_description: str = Field(
        ...,
        description="Description of the debugging problem",
        min_length=20,
        max_length=2000
    )

    system_context: str = Field(
        ...,
        description="Context of the system being debugged",
        min_length=20,
        max_length=1000
    )

    complexity_level: ComplexityLevel = Field(
        ComplexityLevel.MODERATE,
        description="Complexity level of the debugging task"
    )

    error_symptoms: list[str] = Field(
        ...,
        description="Observable symptoms of the error",
        min_length=1,
        max_length=10
    )

    environment_details: dict[str, str] = Field(
        default_factory=dict,
        description="Environment details (OS, language, framework, etc.)"
    )

    available_tools: list[str] = Field(
        default_factory=list,
        description="Available debugging tools and resources",
        max_length=15
    )

    time_constraints: str | None = Field(
        None,
        description="Time constraints for debugging",
        max_length=200
    )

    impact_level: Severity = Field(
        Severity.MEDIUM,
        description="Impact level of the error on the system"
    )

    reproduction_steps: list[str] = Field(
        default_factory=list,
        description="Known steps to reproduce the error",
        max_length=15
    )

    previous_attempts: list[str] = Field(
        default_factory=list,
        description="Previous debugging attempts and their results",
        max_length=10
    )

    team_expertise: list[str] = Field(
        default_factory=list,
        description="Team's expertise and skills",
        max_length=10
    )

    include_root_cause_analysis: bool = Field(
        True,
        description="Whether to include root cause analysis"
    )

    include_prevention_measures: bool = Field(
        True,
        description="Whether to include prevention recommendations"
    )

    max_strategy_recommendations: int = Field(
        5,
        ge=1,
        le=10,
        description="Maximum number of strategy recommendations"
    )

    @field_validator('problem_description')
    @classmethod
    def validate_problem_description(cls, v):
        """Validate problem description"""
        v = v.strip()
        if len(v) < 20:
            raise ValueError("Problem description must be at least 20 characters")
        return v


class DebuggingApproachesResult(BaseModel):
    """Result of debugging approaches analysis"""

    error_classification: ErrorClassification = Field(
        ...,
        description="Classification of the error"
    )

    debugging_recommendations: list[DebuggingRecommendation] = Field(
        default_factory=list,
        description="Recommended debugging strategies"
    )

    debugging_session: DebuggingSession | None = Field(
        None,
        description="Generated debugging session if requested"
    )

    root_cause_analysis: RootCauseAnalysis | None = Field(
        None,
        description="Root cause analysis if performed"
    )

    top_recommended_strategy: str | None = Field(
        None,
        description="Top recommended debugging strategy"
    )

    strategy_effectiveness_scores: dict[str, float] = Field(
        default_factory=dict,
        description="Effectiveness scores for each strategy"
    )

    debugging_roadmap: list[str] = Field(
        default_factory=list,
        description="Step-by-step debugging roadmap",
        max_length=15
    )

    prevention_measures: list[str] = Field(
        default_factory=list,
        description="Measures to prevent similar issues",
        max_length=10
    )

    risk_assessment: list[str] = Field(
        default_factory=list,
        description="Risk factors and mitigation strategies",
        max_length=8
    )

    tool_recommendations: list[str] = Field(
        default_factory=list,
        description="Recommended tools for debugging",
        max_length=10
    )

    best_practices: list[str] = Field(
        default_factory=list,
        description="Best practices for this type of debugging",
        max_length=10
    )

    learning_opportunities: list[str] = Field(
        default_factory=list,
        description="Learning opportunities from this debugging scenario",
        max_length=8
    )

    processing_time_ms: int = Field(
        0,
        description="Time taken to process in milliseconds"
    )

    @field_validator('debugging_roadmap')
    @classmethod
    def validate_roadmap(cls, v):
        """Validate roadmap items are not empty"""
        return [item for item in v if item and item.strip()]

    def get_summary(self) -> dict[str, Any]:
        """Get concise summary of debugging analysis"""
        return {
            'error_category': self.error_classification.error_category.value,
            'severity': self.error_classification.severity.value,
            'strategies_recommended': len(self.debugging_recommendations),
            'top_strategy': self.top_recommended_strategy,
            'has_root_cause_analysis': self.root_cause_analysis is not None,
            'prevention_measures_count': len(self.prevention_measures),
            'roadmap_steps': len(self.debugging_roadmap)
        }
