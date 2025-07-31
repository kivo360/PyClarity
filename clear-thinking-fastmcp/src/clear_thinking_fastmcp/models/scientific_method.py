# Clear Thinking FastMCP Server - Scientific Method Models

"""
Pydantic models for the Scientific Method cognitive tool.

This tool supports hypothesis-driven reasoning through:
- Hypothesis formation and testing
- Experimental design principles
- Evidence evaluation and analysis
- Theory building and validation
- Systematic inquiry processes

Agent: AGENT E - Scientific Method Implementation
Status: ACTIVE - Phase 2C Parallel Expansion
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union, Literal
from enum import Enum
from datetime import datetime
import uuid

from .base import CognitiveInputBase, CognitiveOutputBase, ComplexityLevel


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
    
    hypothesis_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique hypothesis identifier")
    statement: str = Field(..., description="Clear statement of the hypothesis")
    hypothesis_type: HypothesisType = Field(..., description="Type of hypothesis")
    variables: List[str] = Field(default_factory=list, description="Variables involved in the hypothesis")
    assumptions: List[str] = Field(default_factory=list, description="Underlying assumptions")
    predictions: List[str] = Field(default_factory=list, description="Specific predictions made by the hypothesis")
    testability: float = Field(..., ge=0.0, le=1.0, description="How testable this hypothesis is")
    falsifiability: float = Field(..., ge=0.0, le=1.0, description="How falsifiable this hypothesis is")
    theoretical_foundation: str = Field(..., description="Theoretical basis for the hypothesis")
    related_hypotheses: List[str] = Field(default_factory=list, description="Related or competing hypotheses")
    
    class Config:
        json_encoders = {
            HypothesisType: lambda v: v.value
        }


class Evidence(BaseModel):
    """Evidence for or against a hypothesis"""
    
    evidence_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique evidence identifier")
    description: str = Field(..., description="Description of the evidence")
    evidence_type: EvidenceType = Field(..., description="Type of evidence")
    quality: EvidenceQuality = Field(..., description="Quality level of the evidence")
    source: str = Field(..., description="Source of the evidence")
    relevance_score: float = Field(..., ge=0.0, le=1.0, description="How relevant this evidence is")
    reliability_score: float = Field(..., ge=0.0, le=1.0, description="How reliable this evidence is")
    supporting_strength: float = Field(..., ge=-1.0, le=1.0, description="How strongly it supports (+) or opposes (-) the hypothesis")
    confidence_level: float = Field(..., ge=0.0, le=1.0, description="Confidence in this evidence")
    methodology_notes: Optional[str] = Field(None, description="Notes on methodology used to gather evidence")
    limitations: List[str] = Field(default_factory=list, description="Limitations of this evidence")
    
    class Config:
        json_encoders = {
            EvidenceType: lambda v: v.value,
            EvidenceQuality: lambda v: v.value
        }


class Experiment(BaseModel):
    """An experiment designed to test a hypothesis"""
    
    experiment_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique experiment identifier")
    name: str = Field(..., description="Name of the experiment")
    objective: str = Field(..., description="Objective of the experiment")
    hypothesis_tested: str = Field(..., description="ID of hypothesis being tested")
    experimental_design: str = Field(..., description="Description of experimental design")
    variables_controlled: List[str] = Field(default_factory=list, description="Variables that are controlled")
    variables_measured: List[str] = Field(default_factory=list, description="Variables that are measured")
    methodology: str = Field(..., description="Experimental methodology")
    expected_outcomes: List[str] = Field(default_factory=list, description="Expected outcomes")
    success_criteria: List[str] = Field(default_factory=list, description="Criteria for determining success")
    potential_confounds: List[str] = Field(default_factory=list, description="Potential confounding factors")
    ethical_considerations: List[str] = Field(default_factory=list, description="Ethical considerations")
    feasibility_score: float = Field(..., ge=0.0, le=1.0, description="How feasible this experiment is")


class HypothesisTest(BaseModel):
    """Result of testing a hypothesis"""
    
    hypothesis_id: str = Field(..., description="ID of hypothesis that was tested")
    evidence_considered: List[str] = Field(default_factory=list, description="IDs of evidence considered")
    test_result: TestResult = Field(..., description="Result of the test")
    confidence_level: float = Field(..., ge=0.0, le=1.0, description="Confidence in the test result")
    statistical_significance: Optional[float] = Field(None, ge=0.0, le=1.0, description="Statistical significance if applicable")
    effect_size: Optional[float] = Field(None, description="Effect size if applicable")
    supporting_evidence_count: int = Field(default=0, ge=0, description="Number of supporting evidence pieces")
    opposing_evidence_count: int = Field(default=0, ge=0, description="Number of opposing evidence pieces")
    evidence_quality_score: float = Field(..., ge=0.0, le=1.0, description="Overall quality of evidence")
    alternative_explanations: List[str] = Field(default_factory=list, description="Alternative explanations considered")
    limitations: List[str] = Field(default_factory=list, description="Limitations of the test")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations based on results")
    
    class Config:
        json_encoders = {
            TestResult: lambda v: v.value
        }


class TheoryConstruction(BaseModel):
    """Construction of a theory from hypotheses and evidence"""
    
    theory_name: str = Field(..., description="Name of the theory")
    theory_statement: str = Field(..., description="Statement of the theory")
    supporting_hypotheses: List[str] = Field(default_factory=list, description="Hypotheses that support the theory")
    core_principles: List[str] = Field(default_factory=list, description="Core principles of the theory")
    explanatory_power: float = Field(..., ge=0.0, le=1.0, description="How well the theory explains phenomena")
    predictive_power: float = Field(..., ge=0.0, le=1.0, description="How well the theory predicts outcomes")
    parsimony_score: float = Field(..., ge=0.0, le=1.0, description="How parsimonious (simple) the theory is")
    scope: str = Field(..., description="Scope of the theory's applicability")
    testable_predictions: List[str] = Field(default_factory=list, description="Testable predictions from the theory")
    competing_theories: List[str] = Field(default_factory=list, description="Competing theories")
    theory_confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence in the theory")


class ScientificMethodInput(CognitiveInputBase):
    """Input model for Scientific Method tool"""
    
    research_question: str = Field(..., description="The research question to investigate")
    domain_knowledge: str = Field(..., description="Existing knowledge in the domain")
    hypothesis_generation_enabled: bool = Field(default=True, description="Enable hypothesis generation")
    evidence_evaluation_enabled: bool = Field(default=True, description="Enable evidence evaluation")
    experiment_design_enabled: bool = Field(default=True, description="Enable experiment design suggestions")
    theory_construction_enabled: bool = Field(default=True, description="Enable theory construction")
    max_hypotheses: int = Field(default=5, ge=1, le=20, description="Maximum number of hypotheses to generate")
    evidence_sources: List[str] = Field(default_factory=list, description="Available evidence sources")
    constraints: List[str] = Field(default_factory=list, description="Constraints on investigation")
    prior_knowledge: Optional[str] = Field(None, description="Prior knowledge or theories")
    significance_threshold: float = Field(default=0.05, ge=0.001, le=0.1, description="Statistical significance threshold")
    confidence_threshold: float = Field(default=0.8, ge=0.5, le=0.99, description="Confidence threshold for conclusions")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ScientificMethodOutput(CognitiveOutputBase):
    """Output model for Scientific Method tool"""
    
    hypotheses_generated: List[Hypothesis] = Field(default_factory=list, description="Hypotheses generated for testing")
    evidence_collected: List[Evidence] = Field(default_factory=list, description="Evidence collected and evaluated")
    experiments_designed: List[Experiment] = Field(default_factory=list, description="Experiments designed for testing")
    hypothesis_tests: List[HypothesisTest] = Field(default_factory=list, description="Results of hypothesis testing")
    theory_construction: Optional[TheoryConstruction] = Field(None, description="Theory constructed from findings")
    scientific_rigor_score: float = Field(..., ge=0.0, le=1.0, description="Overall scientific rigor of the process")
    methodology_quality: float = Field(..., ge=0.0, le=1.0, description="Quality of methodology used")
    evidence_strength: float = Field(..., ge=0.0, le=1.0, description="Strength of evidence overall")
    conclusions_supported: List[str] = Field(default_factory=list, description="Conclusions that are well-supported")
    areas_needing_research: List[str] = Field(default_factory=list, description="Areas that need further research")
    methodological_recommendations: List[str] = Field(default_factory=list, description="Recommendations for methodology")
    
    # Additional fields for FastMCP Context integration
    investigation_duration_minutes: float = Field(default=0.0, ge=0.0, description="Duration of scientific investigation")
    hypotheses_tested: int = Field(..., ge=0, description="Number of hypotheses actually tested")
    experiments_feasible: int = Field(default=0, ge=0, description="Number of experiments deemed feasible")
    scientific_confidence: float = Field(..., ge=0.0, le=1.0, description="Overall scientific confidence in findings")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
