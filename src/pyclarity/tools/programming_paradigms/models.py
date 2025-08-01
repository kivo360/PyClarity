"""
Programming Paradigms Models

Data structures for Object-Oriented, Functional, Procedural, and other programming
paradigms with selection criteria, optimization guidance, and paradigm combinations.
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Any, Optional
from enum import Enum
import uuid
from datetime import datetime


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
    
    key_characteristics: List[ParadigmCharacteristic] = Field(
        default_factory=list,
        description="Key characteristics of the paradigm",
        max_items=8
    )
    
    strengths: List[str] = Field(
        default_factory=list,
        description="Strengths of the paradigm",
        max_items=8
    )
    
    weaknesses: List[str] = Field(
        default_factory=list,
        description="Weaknesses of the paradigm",
        max_items=8
    )
    
    suitable_domains: List[ProblemDomain] = Field(
        default_factory=list,
        description="Domains where this paradigm excels",
        max_items=8
    )
    
    languages: List[str] = Field(
        default_factory=list,
        description="Languages that support this paradigm",
        max_items=10
    )
    
    concepts: List[str] = Field(
        default_factory=list,
        description="Core concepts of the paradigm",
        max_items=8
    )
    
    best_practices: List[str] = Field(
        default_factory=list,
        description="Best practices for the paradigm",
        max_items=10
    )
    
    antipatterns: List[str] = Field(
        default_factory=list,
        description="Common antipatterns to avoid",
        max_items=8
    )
    
    learning_curve: str = Field(
        ...,
        description="Learning difficulty level",
        pattern="^(easy|moderate|steep)$"
    )
    
    performance_profile: Dict[str, str] = Field(
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
    
    matching_characteristics: List[ParadigmCharacteristic] = Field(
        default_factory=list,
        description="Characteristics that match the context",
        max_items=8
    )
    
    benefits_for_context: List[str] = Field(
        default_factory=list,
        description="Benefits for this specific context",
        max_items=8
    )
    
    challenges_for_context: List[str] = Field(
        default_factory=list,
        description="Challenges for this specific context",
        max_items=8
    )
    
    implementation_guidance: List[str] = Field(
        default_factory=list,
        description="Implementation guidance",
        max_items=8
    )
    
    code_structure_recommendations: List[str] = Field(
        default_factory=list,
        description="Code structure recommendations",
        max_items=8
    )
    
    performance_considerations: List[str] = Field(
        default_factory=list,
        description="Performance considerations",
        max_items=6
    )


class ParadigmComparison(BaseModel):
    """Comparison between multiple paradigms"""
    
    comparison_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique comparison identifier"
    )
    
    paradigms: List[ProgrammingParadigm] = Field(
        ...,
        description="Paradigms being compared",
        min_items=2,
        max_items=8
    )
    
    comparison_criteria: List[str] = Field(
        ...,
        description="Criteria for comparison",
        min_items=1,
        max_items=10
    )
    
    scores: Dict[str, Dict[str, float]] = Field(
        default_factory=dict,
        description="Scores for each paradigm-criterion combination"
    )
    
    recommendations: Dict[str, str] = Field(
        default_factory=dict,
        description="Recommendations for each criterion"
    )
    
    hybrid_opportunities: List[str] = Field(
        default_factory=list,
        description="Opportunities for combining paradigms",
        max_items=8
    )
    
    decision_matrix: Dict[str, Dict[str, str]] = Field(
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
    
    secondary_paradigms: List[ProgrammingParadigm] = Field(
        ...,
        description="Secondary paradigms",
        min_items=1,
        max_items=4
    )
    
    integration_strategy: str = Field(
        ...,
        description="Strategy for integrating paradigms",
        min_length=20,
        max_length=500
    )
    
    synergies: List[str] = Field(
        default_factory=list,
        description="Synergies between paradigms",
        max_items=8
    )
    
    conflicts: List[str] = Field(
        default_factory=list,
        description="Potential conflicts",
        max_items=6
    )
    
    implementation_patterns: List[str] = Field(
        default_factory=list,
        description="Implementation patterns",
        max_items=8
    )
    
    use_cases: List[str] = Field(
        default_factory=list,
        description="Use cases for this mix",
        max_items=8
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
    
    detected_paradigms: List[ProgrammingParadigm] = Field(
        default_factory=list,
        description="Detected paradigms in the code",
        max_items=6
    )
    
    paradigm_purity: Dict[str, float] = Field(
        default_factory=dict,
        description="Purity score for each detected paradigm"
    )
    
    structural_patterns: List[str] = Field(
        default_factory=list,
        description="Identified structural patterns",
        max_items=8
    )
    
    paradigm_violations: List[str] = Field(
        default_factory=list,
        description="Paradigm violations found",
        max_items=8
    )
    
    improvement_suggestions: List[str] = Field(
        default_factory=list,
        description="Suggestions for improvement",
        max_items=8
    )
    
    refactoring_opportunities: List[str] = Field(
        default_factory=list,
        description="Refactoring opportunities",
        max_items=8
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
    
    requirements: List[str] = Field(
        default_factory=list,
        description="Functional and non-functional requirements",
        max_items=15
    )
    
    constraints: List[str] = Field(
        default_factory=list,
        description="Technical constraints",
        max_items=10
    )
    
    team_experience: List[ProgrammingParadigm] = Field(
        default_factory=list,
        description="Paradigms the team is experienced with",
        max_items=8
    )
    
    performance_requirements: Optional[str] = Field(
        None,
        description="Performance requirements",
        max_length=500
    )
    
    scalability_needs: Optional[str] = Field(
        None,
        description="Scalability requirements",
        max_length=500
    )
    
    maintenance_considerations: Optional[str] = Field(
        None,
        description="Maintenance and evolution considerations",
        max_length=500
    )
    
    target_languages: List[str] = Field(
        default_factory=list,
        description="Target programming languages",
        max_items=5
    )
    
    existing_codebase: Optional[str] = Field(
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
    
    paradigm_analyses: List[ParadigmAnalysis] = Field(
        default_factory=list,
        description="Analysis results for each paradigm"
    )
    
    paradigm_comparisons: List[ParadigmComparison] = Field(
        default_factory=list,
        description="Paradigm comparison results"
    )
    
    paradigm_mixes: List[ParadigmMix] = Field(
        default_factory=list,
        description="Hybrid paradigm combinations"
    )
    
    code_structure_analysis: Optional[CodeStructureAnalysis] = Field(
        None,
        description="Code structure analysis if applicable"
    )
    
    top_recommended_paradigm: Optional[str] = Field(
        None,
        description="Top recommended paradigm"
    )
    
    paradigm_suitability_scores: Dict[str, float] = Field(
        default_factory=dict,
        description="Suitability scores for each paradigm"
    )
    
    implementation_roadmap: List[str] = Field(
        default_factory=list,
        description="Implementation roadmap suggestions",
        max_items=10
    )
    
    learning_path_recommendations: List[str] = Field(
        default_factory=list,
        description="Learning path recommendations for the team",
        max_items=8
    )
    
    risk_considerations: List[str] = Field(
        default_factory=list,
        description="Risk considerations for paradigm selection",
        max_items=8
    )
    
    success_factors: List[str] = Field(
        default_factory=list,
        description="Success factors for paradigm adoption",
        max_items=8
    )
    
    alternatives_analysis: Dict[str, str] = Field(
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
    
    def get_summary(self) -> Dict[str, Any]:
        """Get concise summary of paradigms analysis"""
        return {
            'paradigms_analyzed': len(self.paradigm_analyses),
            'comparisons_performed': len(self.paradigm_comparisons),
            'hybrid_options': len(self.paradigm_mixes),
            'top_recommendation': self.top_recommended_paradigm,
            'has_code_analysis': self.code_structure_analysis is not None,
            'roadmap_steps': len(self.implementation_roadmap)
        }