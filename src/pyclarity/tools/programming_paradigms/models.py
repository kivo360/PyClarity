"""
Programming Paradigms Models

Data structures for Object-Oriented, Functional, Procedural, and other programming
paradigms with selection criteria, optimization guidance, and paradigm combinations.
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


class ProgrammingParadigm(str, Enum):
    """Programming paradigm types"""
    OBJECT_ORIENTED = "object_oriented"
    FUNCTIONAL = "functional"
    PROCEDURAL = "procedural"
    DECLARATIVE = "declarative"
    IMPERATIVE = "imperative"
    LOGIC = "logic"
    CONCURRENT = "concurrent"
    REACTIVE = "reactive"
    EVENT_DRIVEN = "event_driven"
    ASPECT_ORIENTED = "aspect_oriented"


class ParadigmCharacteristic(str, Enum):
    """Key characteristics of programming paradigms"""
    ENCAPSULATION = "encapsulation"
    INHERITANCE = "inheritance"
    POLYMORPHISM = "polymorphism"
    IMMUTABILITY = "immutability"
    HIGHER_ORDER_FUNCTIONS = "higher_order_functions"
    PURE_FUNCTIONS = "pure_functions"
    SIDE_EFFECTS = "side_effects"
    STATE_MANAGEMENT = "state_management"
    MODULARITY = "modularity"
    ABSTRACTION = "abstraction"
    COMPOSITION = "composition"


class ProblemDomain(str, Enum):
    """Problem domains suitable for different paradigms"""
    WEB_DEVELOPMENT = "web_development"
    DATA_PROCESSING = "data_processing"
    SYSTEM_PROGRAMMING = "system_programming"
    SCIENTIFIC_COMPUTING = "scientific_computing"
    GAME_DEVELOPMENT = "game_development"
    ENTERPRISE_SOFTWARE = "enterprise_software"
    EMBEDDED_SYSTEMS = "embedded_systems"
    MACHINE_LEARNING = "machine_learning"
    CONCURRENT_SYSTEMS = "concurrent_systems"
    USER_INTERFACES = "user_interfaces"


class ParadigmProfile(BaseModel):
    """Comprehensive profile of a programming paradigm"""

    paradigm: ProgrammingParadigm = Field(
        ...,
        description="The programming paradigm"
    )

    description: str = Field(
        ...,
        description="Description of the paradigm",
        min_length=20,
        max_length=500
    )

    key_characteristics: list[ParadigmCharacteristic] = Field(
        default_factory=list,
        description="Key characteristics of the paradigm",
        max_length=8
    )

    strengths: list[str] = Field(
        default_factory=list,
        description="Strengths of the paradigm",
        max_length=8
    )

    weaknesses: list[str] = Field(
        default_factory=list,
        description="Weaknesses of the paradigm",
        max_length=8
    )

    suitable_domains: list[ProblemDomain] = Field(
        default_factory=list,
        description="Domains where this paradigm excels",
        max_length=8
    )

    languages: list[str] = Field(
        default_factory=list,
        description="Languages that support this paradigm",
        max_length=10
    )

    concepts: list[str] = Field(
        default_factory=list,
        description="Core concepts of the paradigm",
        max_length=8
    )

    best_practices: list[str] = Field(
        default_factory=list,
        description="Best practices for the paradigm",
        max_length=10
    )

    antipatterns: list[str] = Field(
        default_factory=list,
        description="Common antipatterns to avoid",
        max_length=8
    )

    learning_curve: str = Field(
        ...,
        description="Learning difficulty level",
        pattern="^(easy|moderate|steep)$"
    )

    performance_profile: dict[str, str] = Field(
        default_factory=dict,
        description="Performance characteristics (memory, cpu, scalability)"
    )


class ParadigmAnalysis(BaseModel):
    """Analysis of paradigm suitability for a specific context"""

    analysis_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique analysis identifier"
    )

    paradigm: ProgrammingParadigm = Field(
        ...,
        description="The paradigm being analyzed"
    )

    context_description: str = Field(
        ...,
        description="Description of the context",
        min_length=20,
        max_length=1000
    )

    suitability_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Suitability score (0.0 to 1.0)"
    )

    matching_characteristics: list[ParadigmCharacteristic] = Field(
        default_factory=list,
        description="Characteristics that match the context",
        max_length=8
    )

    benefits_for_context: list[str] = Field(
        default_factory=list,
        description="Benefits for this specific context",
        max_length=8
    )

    challenges_for_context: list[str] = Field(
        default_factory=list,
        description="Challenges for this specific context",
        max_length=8
    )

    implementation_guidance: list[str] = Field(
        default_factory=list,
        description="Implementation guidance",
        max_length=8
    )

    code_structure_recommendations: list[str] = Field(
        default_factory=list,
        description="Code structure recommendations",
        max_length=8
    )

    performance_considerations: list[str] = Field(
        default_factory=list,
        description="Performance considerations",
        max_length=6
    )


class ParadigmComparison(BaseModel):
    """Comparison between multiple paradigms"""

    comparison_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique comparison identifier"
    )

    paradigms: list[ProgrammingParadigm] = Field(
        ...,
        description="Paradigms being compared",
        min_length=2,
        max_length=8
    )

    comparison_criteria: list[str] = Field(
        ...,
        description="Criteria for comparison",
        min_length=1,
        max_length=10
    )

    scores: dict[str, dict[str, float]] = Field(
        default_factory=dict,
        description="Scores for each paradigm-criterion combination"
    )

    recommendations: dict[str, str] = Field(
        default_factory=dict,
        description="Recommendations for each criterion"
    )

    hybrid_opportunities: list[str] = Field(
        default_factory=list,
        description="Opportunities for combining paradigms",
        max_length=8
    )

    decision_matrix: dict[str, dict[str, str]] = Field(
        default_factory=dict,
        description="Decision matrix with ratings"
    )


class ParadigmMix(BaseModel):
    """Analysis of combining multiple paradigms"""

    mix_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique mix identifier"
    )

    primary_paradigm: ProgrammingParadigm = Field(
        ...,
        description="Primary paradigm"
    )

    secondary_paradigms: list[ProgrammingParadigm] = Field(
        ...,
        description="Secondary paradigms",
        min_length=1,
        max_length=4
    )

    integration_strategy: str = Field(
        ...,
        description="Strategy for integrating paradigms",
        min_length=20,
        max_length=500
    )

    synergies: list[str] = Field(
        default_factory=list,
        description="Synergies between paradigms",
        max_length=8
    )

    conflicts: list[str] = Field(
        default_factory=list,
        description="Potential conflicts",
        max_length=6
    )

    implementation_patterns: list[str] = Field(
        default_factory=list,
        description="Implementation patterns",
        max_length=8
    )

    use_cases: list[str] = Field(
        default_factory=list,
        description="Use cases for this mix",
        max_length=8
    )

    complexity_impact: str = Field(
        ...,
        description="Impact on complexity",
        min_length=10,
        max_length=200
    )


class CodeStructureAnalysis(BaseModel):
    """Analysis of code structure from paradigm perspective"""

    analysis_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique analysis identifier"
    )

    detected_paradigms: list[ProgrammingParadigm] = Field(
        default_factory=list,
        description="Detected paradigms in the code",
        max_length=6
    )

    paradigm_purity: dict[str, float] = Field(
        default_factory=dict,
        description="Purity score for each detected paradigm"
    )

    structural_patterns: list[str] = Field(
        default_factory=list,
        description="Identified structural patterns",
        max_length=8
    )

    paradigm_violations: list[str] = Field(
        default_factory=list,
        description="Paradigm violations found",
        max_length=8
    )

    improvement_suggestions: list[str] = Field(
        default_factory=list,
        description="Suggestions for improvement",
        max_length=8
    )

    refactoring_opportunities: list[str] = Field(
        default_factory=list,
        description="Refactoring opportunities",
        max_length=8
    )

    paradigm_consistency_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Overall paradigm consistency score"
    )


class ProgrammingParadigmsContext(BaseModel):
    """Context for programming paradigms analysis"""

    problem_description: str = Field(
        ...,
        description="Description of the programming problem",
        min_length=20,
        max_length=2000
    )

    project_type: str = Field(
        ...,
        description="Type of project or system",
        min_length=5,
        max_length=100
    )

    complexity_level: ComplexityLevel = Field(
        ComplexityLevel.MODERATE,
        description="Complexity level of the problem"
    )

    requirements: list[str] = Field(
        default_factory=list,
        description="Functional and non-functional requirements",
        max_length=15
    )

    constraints: list[str] = Field(
        default_factory=list,
        description="Technical constraints",
        max_length=10
    )

    team_experience: list[ProgrammingParadigm] = Field(
        default_factory=list,
        description="Paradigms the team is experienced with",
        max_length=8
    )

    performance_requirements: str | None = Field(
        None,
        description="Performance requirements",
        max_length=500
    )

    scalability_needs: str | None = Field(
        None,
        description="Scalability requirements",
        max_length=500
    )

    maintenance_considerations: str | None = Field(
        None,
        description="Maintenance and evolution considerations",
        max_length=500
    )

    target_languages: list[str] = Field(
        default_factory=list,
        description="Target programming languages",
        max_length=5
    )

    existing_codebase: str | None = Field(
        None,
        description="Description of existing codebase if applicable",
        max_length=1000
    )

    include_hybrid_analysis: bool = Field(
        True,
        description="Whether to include hybrid paradigm analysis"
    )

    max_paradigm_recommendations: int = Field(
        5,
        ge=1,
        le=10,
        description="Maximum number of paradigm recommendations"
    )

    @field_validator('problem_description')
    @classmethod
    def validate_problem_description(cls, v):
        """Validate problem description"""
        v = v.strip()
        if len(v) < 20:
            raise ValueError("Problem description must be at least 20 characters")
        return v


class ProgrammingParadigmsResult(BaseModel):
    """Result of programming paradigms analysis"""

    paradigm_analyses: list[ParadigmAnalysis] = Field(
        default_factory=list,
        description="Analysis results for each paradigm"
    )

    paradigm_comparisons: list[ParadigmComparison] = Field(
        default_factory=list,
        description="Paradigm comparison results"
    )

    paradigm_mixes: list[ParadigmMix] = Field(
        default_factory=list,
        description="Hybrid paradigm combinations"
    )

    code_structure_analysis: CodeStructureAnalysis | None = Field(
        None,
        description="Code structure analysis if applicable"
    )

    top_recommended_paradigm: str | None = Field(
        None,
        description="Top recommended paradigm"
    )

    paradigm_suitability_scores: dict[str, float] = Field(
        default_factory=dict,
        description="Suitability scores for each paradigm"
    )

    implementation_roadmap: list[str] = Field(
        default_factory=list,
        description="Implementation roadmap suggestions",
        max_length=10
    )

    learning_path_recommendations: list[str] = Field(
        default_factory=list,
        description="Learning path recommendations for the team",
        max_length=8
    )

    risk_considerations: list[str] = Field(
        default_factory=list,
        description="Risk considerations for paradigm selection",
        max_length=8
    )

    success_factors: list[str] = Field(
        default_factory=list,
        description="Success factors for paradigm adoption",
        max_length=8
    )

    alternatives_analysis: dict[str, str] = Field(
        default_factory=dict,
        description="Analysis of alternative approaches"
    )

    processing_time_ms: int = Field(
        0,
        description="Time taken to process in milliseconds"
    )

    @field_validator('implementation_roadmap')
    @classmethod
    def validate_roadmap(cls, v):
        """Validate roadmap items are not empty"""
        return [item for item in v if item and item.strip()]

    def get_summary(self) -> dict[str, Any]:
        """Get concise summary of paradigms analysis"""
        return {
            'paradigms_analyzed': len(self.paradigm_analyses),
            'comparisons_performed': len(self.paradigm_comparisons),
            'hybrid_options': len(self.paradigm_mixes),
            'top_recommendation': self.top_recommended_paradigm,
            'has_code_analysis': self.code_structure_analysis is not None,
            'roadmap_steps': len(self.implementation_roadmap)
        }
