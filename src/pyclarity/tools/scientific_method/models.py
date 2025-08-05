"""
Scientific Method Models

Data structures for hypothesis-driven reasoning through hypothesis formation
and testing, experimental design principles, evidence evaluation and analysis,
theory building and validation, and systematic inquiry processes.
"""

import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, field_validator, model_validator


class ComplexityLevel(str, Enum):
    """Problem complexity levels"""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    VERY_COMPLEX = "very_complex"


class HypothesisType(str, Enum):
    """Types of hypotheses in scientific reasoning"""

    DESCRIPTIVE = "descriptive"
    EXPLANATORY = "explanatory"
    PREDICTIVE = "predictive"
    CAUSAL = "causal"
    CORRELATIONAL = "correlational"
    COMPARATIVE = "comparative"
    NULL_HYPOTHESIS = "null_hypothesis"
    ALTERNATIVE_HYPOTHESIS = "alternative_hypothesis"

    @property
    def description(self) -> str:
        """Get description of the hypothesis type"""
        descriptions = {
            self.DESCRIPTIVE: "Describes what is observed or expected",
            self.EXPLANATORY: "Explains why something occurs",
            self.PREDICTIVE: "Predicts what will happen under certain conditions",
            self.CAUSAL: "Proposes a cause-and-effect relationship",
            self.CORRELATIONAL: "Suggests a relationship between variables",
            self.COMPARATIVE: "Compares different conditions or groups",
            self.NULL_HYPOTHESIS: "States no effect or no difference exists",
            self.ALTERNATIVE_HYPOTHESIS: "States an effect or difference exists"
        }
        return descriptions.get(self, "Unknown hypothesis type")


class EvidenceType(str, Enum):
    """Types of evidence for hypothesis testing"""

    OBSERVATIONAL = "observational"
    EXPERIMENTAL = "experimental"
    STATISTICAL = "statistical"
    ANECDOTAL = "anecdotal"
    EXPERT_OPINION = "expert_opinion"
    LITERATURE_REVIEW = "literature_review"
    CASE_STUDY = "case_study"
    SURVEY_DATA = "survey_data"
    ARCHIVAL_DATA = "archival_data"
    SIMULATION = "simulation"


class EvidenceQuality(str, Enum):
    """Quality levels for evidence"""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INSUFFICIENT = "insufficient"


class TestResult(str, Enum):
    """Results of hypothesis testing"""

    SUPPORTED = "supported"
    NOT_SUPPORTED = "not_supported"
    PARTIALLY_SUPPORTED = "partially_supported"
    INCONCLUSIVE = "inconclusive"
    REQUIRES_REFINEMENT = "requires_refinement"


class Hypothesis(BaseModel):
    """A scientific hypothesis to be tested"""

    hypothesis_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique hypothesis identifier"
    )

    statement: str = Field(
        ...,
        description="Clear statement of the hypothesis",
        min_length=10,
        max_length=500
    )

    hypothesis_type: HypothesisType = Field(
        ...,
        description="Type of hypothesis"
    )

    variables: list[str] = Field(
        default_factory=list,
        description="Variables involved in the hypothesis",
        max_length=10
    )

    assumptions: list[str] = Field(
        default_factory=list,
        description="Underlying assumptions",
        max_length=8
    )

    predictions: list[str] = Field(
        default_factory=list,
        description="Specific predictions made by the hypothesis",
        max_length=8
    )

    testability: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="How testable this hypothesis is"
    )

    falsifiability: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="How falsifiable this hypothesis is"
    )

    theoretical_foundation: str = Field(
        ...,
        description="Theoretical basis for the hypothesis",
        max_length=500
    )

    related_hypotheses: list[str] = Field(
        default_factory=list,
        description="Related or competing hypotheses",
        max_length=5
    )

    @field_validator('statement')
    @classmethod
    def validate_statement(cls, v):
        """Validate hypothesis statement"""
        if not v or v.strip() == "":
            raise ValueError("Hypothesis statement cannot be empty")
        return v.strip()

    @field_validator('variables')
    @classmethod
    def validate_variables(cls, v):
        """Validate variables list"""
        if v and len(v) == 0:
            raise ValueError("At least one variable must be specified if providing variables")
        return v


class Evidence(BaseModel):
    """Evidence for or against a hypothesis"""

    evidence_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique evidence identifier"
    )

    description: str = Field(
        ...,
        description="Description of the evidence",
        min_length=10,
        max_length=500
    )

    evidence_type: EvidenceType = Field(
        ...,
        description="Type of evidence"
    )

    quality: EvidenceQuality = Field(
        ...,
        description="Quality level of the evidence"
    )

    source: str = Field(
        ...,
        description="Source of the evidence",
        max_length=200
    )

    relevance_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="How relevant this evidence is"
    )

    reliability_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="How reliable this evidence is"
    )

    supporting_strength: float = Field(
        ...,
        ge=-1.0,
        le=1.0,
        description="How strongly it supports (+) or opposes (-) the hypothesis"
    )

    confidence_level: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence in this evidence"
    )

    methodology_notes: str | None = Field(
        None,
        description="Notes on methodology used to gather evidence",
        max_length=300
    )

    limitations: list[str] = Field(
        default_factory=list,
        description="Limitations of this evidence",
        max_length=5
    )


class Experiment(BaseModel):
    """An experiment designed to test a hypothesis"""

    experiment_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique experiment identifier"
    )

    name: str = Field(
        ...,
        description="Name of the experiment",
        min_length=5,
        max_length=200
    )

    objective: str = Field(
        ...,
        description="Objective of the experiment",
        min_length=10,
        max_length=300
    )

    hypothesis_tested: str = Field(
        ...,
        description="ID of hypothesis being tested"
    )

    experimental_design: str = Field(
        ...,
        description="Description of experimental design",
        max_length=500
    )

    variables_controlled: list[str] = Field(
        default_factory=list,
        description="Variables that are controlled",
        max_length=10
    )

    variables_measured: list[str] = Field(
        default_factory=list,
        description="Variables that are measured",
        max_length=10
    )

    methodology: str = Field(
        ...,
        description="Experimental methodology",
        max_length=500
    )

    expected_outcomes: list[str] = Field(
        default_factory=list,
        description="Expected outcomes",
        max_length=8
    )

    success_criteria: list[str] = Field(
        default_factory=list,
        description="Criteria for determining success",
        max_length=8
    )

    potential_confounds: list[str] = Field(
        default_factory=list,
        description="Potential confounding factors",
        max_length=8
    )

    ethical_considerations: list[str] = Field(
        default_factory=list,
        description="Ethical considerations",
        max_length=6
    )

    feasibility_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="How feasible this experiment is"
    )


class HypothesisTest(BaseModel):
    """Result of testing a hypothesis"""

    hypothesis_id: str = Field(
        ...,
        description="ID of hypothesis that was tested"
    )

    evidence_considered: list[str] = Field(
        default_factory=list,
        description="IDs of evidence considered",
        max_length=20
    )

    test_result: TestResult = Field(
        ...,
        description="Result of the test"
    )

    confidence_level: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence in the test result"
    )

    statistical_significance: float | None = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Statistical significance if applicable"
    )

    effect_size: float | None = Field(
        None,
        description="Effect size if applicable"
    )

    supporting_evidence_count: int = Field(
        default=0,
        ge=0,
        description="Number of supporting evidence pieces"
    )

    opposing_evidence_count: int = Field(
        default=0,
        ge=0,
        description="Number of opposing evidence pieces"
    )

    evidence_quality_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Overall quality of evidence"
    )

    alternative_explanations: list[str] = Field(
        default_factory=list,
        description="Alternative explanations considered",
        max_length=5
    )

    limitations: list[str] = Field(
        default_factory=list,
        description="Limitations of the test",
        max_length=6
    )

    recommendations: list[str] = Field(
        default_factory=list,
        description="Recommendations based on results",
        max_length=6
    )


class TheoryConstruction(BaseModel):
    """Construction of a theory from hypotheses and evidence"""

    theory_name: str = Field(
        ...,
        description="Name of the theory",
        min_length=5,
        max_length=200
    )

    theory_statement: str = Field(
        ...,
        description="Statement of the theory",
        min_length=20,
        max_length=500
    )

    supporting_hypotheses: list[str] = Field(
        default_factory=list,
        description="Hypotheses that support the theory",
        max_length=10
    )

    core_principles: list[str] = Field(
        default_factory=list,
        description="Core principles of the theory",
        min_length=1,
        max_length=8
    )

    explanatory_power: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="How well the theory explains phenomena"
    )

    predictive_power: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="How well the theory predicts outcomes"
    )

    parsimony_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="How parsimonious (simple) the theory is"
    )

    scope: str = Field(
        ...,
        description="Scope of the theory's applicability",
        max_length=300
    )

    testable_predictions: list[str] = Field(
        default_factory=list,
        description="Testable predictions from the theory",
        max_length=10
    )

    competing_theories: list[str] = Field(
        default_factory=list,
        description="Competing theories",
        max_length=5
    )

    theory_confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence in the theory"
    )


class ScientificMethodContext(BaseModel):
    """Context for scientific method analysis"""

    problem: str = Field(
        ...,
        description="The problem or phenomenon to analyze scientifically",
        min_length=20,
        max_length=2000
    )

    research_question: str = Field(
        ...,
        description="The specific research question to investigate",
        min_length=10,
        max_length=500
    )

    domain_knowledge: str = Field(
        ...,
        description="Existing knowledge in the domain",
        min_length=20,
        max_length=2000
    )

    complexity_level: ComplexityLevel = Field(
        ComplexityLevel.MODERATE,
        description="Complexity level of the problem"
    )

    hypothesis_generation_enabled: bool = Field(
        True,
        description="Enable hypothesis generation"
    )

    evidence_evaluation_enabled: bool = Field(
        True,
        description="Enable evidence evaluation"
    )

    experiment_design_enabled: bool = Field(
        True,
        description="Enable experiment design suggestions"
    )

    theory_construction_enabled: bool = Field(
        True,
        description="Enable theory construction"
    )

    max_hypotheses: int = Field(
        5,
        ge=1,
        le=20,
        description="Maximum number of hypotheses to generate"
    )

    evidence_sources: list[str] = Field(
        default_factory=list,
        description="Available evidence sources",
        max_length=10
    )

    constraints: list[str] = Field(
        default_factory=list,
        description="Constraints on investigation",
        max_length=8
    )

    prior_knowledge: str | None = Field(
        None,
        description="Prior knowledge or theories",
        max_length=1000
    )

    significance_threshold: float = Field(
        0.05,
        ge=0.001,
        le=0.1,
        description="Statistical significance threshold"
    )

    confidence_threshold: float = Field(
        0.8,
        ge=0.5,
        le=0.99,
        description="Confidence threshold for conclusions"
    )

    @field_validator('problem')
    @classmethod
    def validate_problem(cls, v):
        """Validate problem description"""
        v = v.strip()
        if len(v) < 20:
            raise ValueError("Problem description must be at least 20 characters")
        return v

    @field_validator('research_question')
    @classmethod
    def validate_research_question(cls, v):
        """Validate research question"""
        v = v.strip()
        if not v.endswith('?') and 'how' not in v.lower() and 'what' not in v.lower() and 'why' not in v.lower():
            raise ValueError("Research question should be phrased as a question")
        return v


class ScientificMethodResult(BaseModel):
    """Result of scientific method analysis"""

    hypotheses_generated: list[Hypothesis] = Field(
        default_factory=list,
        description="Hypotheses generated for testing"
    )

    evidence_collected: list[Evidence] = Field(
        default_factory=list,
        description="Evidence collected and evaluated"
    )

    experiments_designed: list[Experiment] = Field(
        default_factory=list,
        description="Experiments designed for testing"
    )

    hypothesis_tests: list[HypothesisTest] = Field(
        default_factory=list,
        description="Results of hypothesis testing"
    )

    theory_construction: TheoryConstruction | None = Field(
        None,
        description="Theory constructed from findings"
    )

    scientific_rigor_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Overall scientific rigor of the process"
    )

    methodology_quality: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Quality of methodology used"
    )

    evidence_strength: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Strength of evidence overall"
    )

    conclusions_supported: list[str] = Field(
        default_factory=list,
        description="Conclusions that are well-supported",
        max_length=10
    )

    areas_needing_research: list[str] = Field(
        default_factory=list,
        description="Areas that need further research",
        max_length=8
    )

    methodological_recommendations: list[str] = Field(
        default_factory=list,
        description="Recommendations for methodology",
        max_length=8
    )

    investigation_duration_minutes: float = Field(
        0.0,
        ge=0.0,
        description="Duration of scientific investigation"
    )

    hypotheses_tested: int = Field(
        0,
        ge=0,
        description="Number of hypotheses actually tested"
    )

    experiments_feasible: int = Field(
        0,
        ge=0,
        description="Number of experiments deemed feasible"
    )

    scientific_confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Overall scientific confidence in findings"
    )

    processing_time_ms: int = Field(
        0,
        description="Time taken to process in milliseconds"
    )

    @field_validator('conclusions_supported')
    @classmethod
    def validate_conclusions(cls, v):
        """Validate conclusions are not empty strings"""
        return [c for c in v if c and c.strip()]

    def get_summary(self) -> dict[str, Any]:
        """Get concise summary of scientific analysis"""
        return {
            'hypotheses_count': len(self.hypotheses_generated),
            'evidence_pieces': len(self.evidence_collected),
            'tests_conducted': len(self.hypothesis_tests),
            'theory_developed': bool(self.theory_construction),
            'scientific_confidence': self.scientific_confidence,
            'rigor_score': self.scientific_rigor_score,
            'top_conclusion': self.conclusions_supported[0] if self.conclusions_supported else None
        }
