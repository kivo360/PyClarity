"""
Design Patterns Models

Data structures for software architecture patterns, design principle applications,
pattern selection frameworks, and architecture decision support.
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


class PatternCategory(str, Enum):
    """Categories of design patterns"""
    CREATIONAL = "creational"
    STRUCTURAL = "structural"
    BEHAVIORAL = "behavioral"
    ARCHITECTURAL = "architectural"
    CONCURRENCY = "concurrency"
    ENTERPRISE = "enterprise"


class DesignPrinciple(str, Enum):
    """Core design principles"""
    SINGLE_RESPONSIBILITY = "single_responsibility"
    OPEN_CLOSED = "open_closed"
    LISKOV_SUBSTITUTION = "liskov_substitution"
    INTERFACE_SEGREGATION = "interface_segregation"
    DEPENDENCY_INVERSION = "dependency_inversion"
    DRY = "dont_repeat_yourself"
    KISS = "keep_it_simple_stupid"
    YAGNI = "you_arent_gonna_need_it"
    COMPOSITION_OVER_INHERITANCE = "composition_over_inheritance"
    LOOSE_COUPLING = "loose_coupling"
    HIGH_COHESION = "high_cohesion"


class PatternComplexity(str, Enum):
    """Pattern implementation complexity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class DesignPattern(BaseModel):
    """Represents a design pattern with its characteristics"""
    
    pattern_id: str = Field(
        ...,
        description="Unique pattern identifier",
        min_length=2,
        max_length=50
    )
    
    name: str = Field(
        ...,
        description="Name of the design pattern",
        min_length=3,
        max_length=100
    )
    
    category: PatternCategory = Field(
        ...,
        description="Category of the pattern"
    )
    
    description: str = Field(
        ...,
        description="Brief description of the pattern",
        min_length=20,
        max_length=500
    )
    
    intent: str = Field(
        ...,
        description="The intent or purpose of the pattern",
        min_length=20,
        max_length=300
    )
    
    applicability: List[str] = Field(
        default_factory=list,
        description="When to apply this pattern",
        max_items=10
    )
    
    structure: Dict[str, Any] = Field(
        default_factory=dict,
        description="Structural components of the pattern"
    )
    
    participants: List[str] = Field(
        default_factory=list,
        description="Classes and objects participating in the pattern",
        max_items=10
    )
    
    collaborations: List[str] = Field(
        default_factory=list,
        description="How participants collaborate",
        max_items=8
    )
    
    consequences: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="Benefits and drawbacks of using the pattern"
    )
    
    implementation_notes: List[str] = Field(
        default_factory=list,
        description="Implementation considerations",
        max_items=8
    )
    
    related_patterns: List[str] = Field(
        default_factory=list,
        description="Related or similar patterns",
        max_items=8
    )
    
    complexity: PatternComplexity = Field(
        ...,
        description="Implementation complexity level"
    )
    
    principles_supported: List[DesignPrinciple] = Field(
        default_factory=list,
        description="Design principles this pattern supports",
        max_items=6
    )
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        """Validate pattern name"""
        if not v or v.strip() == "":
            raise ValueError("Pattern name cannot be empty")
        return v.strip()
    
    @field_validator('consequences')
    @classmethod
    def validate_consequences(cls, v):
        """Validate consequences structure"""
        if v and not isinstance(v, dict):
            raise ValueError("Consequences must be a dictionary")
        
        # Ensure standard keys exist
        if 'benefits' not in v:
            v['benefits'] = []
        if 'drawbacks' not in v:
            v['drawbacks'] = []
        
        return v


class PatternApplication(BaseModel):
    """Analysis of applying a pattern to a specific context"""
    
    application_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique application identifier"
    )
    
    pattern: DesignPattern = Field(
        ...,
        description="The design pattern being applied"
    )
    
    context_description: str = Field(
        ...,
        description="Description of the application context",
        min_length=20,
        max_length=1000
    )
    
    fit_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="How well the pattern fits (0.0 to 1.0)"
    )
    
    benefits: List[str] = Field(
        default_factory=list,
        description="Benefits of applying this pattern",
        max_items=8
    )
    
    drawbacks: List[str] = Field(
        default_factory=list,
        description="Potential drawbacks or risks",
        max_items=8
    )
    
    implementation_effort: PatternComplexity = Field(
        ...,
        description="Estimated implementation effort"
    )
    
    prerequisites: List[str] = Field(
        default_factory=list,
        description="Prerequisites for implementation",
        max_items=6
    )
    
    alternatives: List[str] = Field(
        default_factory=list,
        description="Alternative patterns to consider",
        max_items=5
    )
    
    recommendation: str = Field(
        ...,
        description="Overall recommendation for using this pattern",
        min_length=20,
        max_length=300
    )


class ArchitecturalDecision(BaseModel):
    """Represents an architectural decision point"""
    
    decision_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique decision identifier"
    )
    
    title: str = Field(
        ...,
        description="Title of the architectural decision",
        min_length=5,
        max_length=200
    )
    
    context: str = Field(
        ...,
        description="Context in which the decision is made",
        min_length=20,
        max_length=1000
    )
    
    problem_statement: str = Field(
        ...,
        description="Problem that needs to be solved",
        min_length=20,
        max_length=500
    )
    
    decision: str = Field(
        ...,
        description="The decision that was made",
        min_length=20,
        max_length=500
    )
    
    status: str = Field(
        "proposed",
        description="Status of the decision",
        pattern="^(proposed|accepted|rejected|superseded)$"
    )
    
    alternatives_considered: List[str] = Field(
        default_factory=list,
        description="Alternative solutions that were considered",
        max_items=8
    )
    
    consequences: List[str] = Field(
        default_factory=list,
        description="Consequences of this decision",
        max_items=8
    )
    
    patterns_involved: List[str] = Field(
        default_factory=list,
        description="Design patterns involved in this decision",
        max_items=5
    )
    
    principles_applied: List[DesignPrinciple] = Field(
        default_factory=list,
        description="Design principles applied in this decision",
        max_items=6
    )
    
    decision_date: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="When the decision was made"
    )
    
    stakeholders: List[str] = Field(
        default_factory=list,
        description="Stakeholders involved in the decision",
        max_items=10
    )


class PatternCombination(BaseModel):
    """Analysis of combining multiple patterns"""
    
    combination_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique combination identifier"
    )
    
    patterns: List[DesignPattern] = Field(
        ...,
        description="Patterns in the combination",
        min_items=2,
        max_items=5
    )
    
    interaction_type: str = Field(
        ...,
        description="Type of interaction between patterns",
        pattern="^(complementary|conflicting|synergistic|neutral)$"
    )
    
    combined_benefits: List[str] = Field(
        default_factory=list,
        description="Benefits of combining these patterns",
        max_items=8
    )
    
    potential_conflicts: List[str] = Field(
        default_factory=list,
        description="Potential conflicts when combining patterns",
        max_items=6
    )
    
    integration_complexity: PatternComplexity = Field(
        ...,
        description="Complexity of integrating these patterns"
    )
    
    usage_scenarios: List[str] = Field(
        default_factory=list,
        description="Scenarios where this combination is useful",
        max_items=6
    )
    
    best_practices: List[str] = Field(
        default_factory=list,
        description="Best practices for combining these patterns",
        max_items=8
    )


class DesignAnalysis(BaseModel):
    """Comprehensive design pattern analysis"""
    
    analysis_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique analysis identifier"
    )
    
    system_description: str = Field(
        ...,
        description="Description of the system being analyzed",
        min_length=20,
        max_length=2000
    )
    
    identified_patterns: List[DesignPattern] = Field(
        default_factory=list,
        description="Patterns identified in the system"
    )
    
    pattern_applications: List[PatternApplication] = Field(
        default_factory=list,
        description="Recommended pattern applications"
    )
    
    architectural_decisions: List[ArchitecturalDecision] = Field(
        default_factory=list,
        description="Architectural decisions made"
    )
    
    pattern_combinations: List[PatternCombination] = Field(
        default_factory=list,
        description="Pattern combinations analyzed"
    )
    
    design_quality_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Overall design quality score"
    )
    
    improvement_suggestions: List[str] = Field(
        default_factory=list,
        description="Suggestions for improving the design",
        max_items=10
    )
    
    principle_adherence: Dict[DesignPrinciple, float] = Field(
        default_factory=dict,
        description="Adherence to design principles"
    )


class DesignPatternsContext(BaseModel):
    """Context for design patterns analysis"""
    
    problem: str = Field(
        ...,
        description="The problem or system to analyze",
        min_length=20,
        max_length=2000
    )
    
    system_description: str = Field(
        ...,
        description="Description of the system or code",
        min_length=20,
        max_length=2000
    )
    
    complexity_level: ComplexityLevel = Field(
        ComplexityLevel.MODERATE,
        description="Complexity level of the system"
    )
    
    requirements: List[str] = Field(
        default_factory=list,
        description="System requirements",
        max_items=15
    )
    
    constraints: List[str] = Field(
        default_factory=list,
        description="Design constraints",
        max_items=10
    )
    
    existing_patterns: List[str] = Field(
        default_factory=list,
        description="Patterns already used in the system",
        max_items=10
    )
    
    target_principles: List[DesignPrinciple] = Field(
        default_factory=list,
        description="Design principles to emphasize",
        max_items=8
    )
    
    performance_requirements: Optional[str] = Field(
        None,
        description="Performance requirements or constraints",
        max_length=500
    )
    
    team_experience_level: str = Field(
        "intermediate",
        description="Team's experience level with design patterns",
        pattern="^(beginner|intermediate|advanced|expert)$"
    )
    
    include_architectural_decisions: bool = Field(
        True,
        description="Whether to include architectural decision analysis"
    )
    
    include_pattern_combinations: bool = Field(
        True,
        description="Whether to analyze pattern combinations"
    )
    
    max_recommendations: int = Field(
        5,
        ge=1,
        le=15,
        description="Maximum number of pattern recommendations"
    )
    
    @field_validator('problem')
    @classmethod
    def validate_problem(cls, v):
        """Validate problem description"""
        v = v.strip()
        if len(v) < 20:
            raise ValueError("Problem description must be at least 20 characters")
        return v


class DesignPatternsResult(BaseModel):
    """Result of design patterns analysis"""
    
    identified_patterns: List[DesignPattern] = Field(
        default_factory=list,
        description="Patterns identified in the system"
    )
    
    pattern_recommendations: List[PatternApplication] = Field(
        default_factory=list,
        description="Recommended pattern applications"
    )
    
    architectural_decisions: List[ArchitecturalDecision] = Field(
        default_factory=list,
        description="Architectural decisions analyzed"
    )
    
    pattern_combinations: List[PatternCombination] = Field(
        default_factory=list,
        description="Pattern combinations analyzed"
    )
    
    design_quality_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Overall design quality score"
    )
    
    principle_adherence: Dict[str, float] = Field(
        default_factory=dict,
        description="Adherence to design principles (principle -> score)"
    )
    
    improvement_suggestions: List[str] = Field(
        default_factory=list,
        description="Suggestions for improving the design",
        max_items=10
    )
    
    pattern_catalog_size: int = Field(
        0,
        ge=0,
        description="Number of patterns in the catalog"
    )
    
    top_recommended_pattern: Optional[str] = Field(
        None,
        description="Top recommended pattern name"
    )
    
    complexity_assessment: str = Field(
        ...,
        description="Assessment of the system's complexity"
    )
    
    maintainability_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Estimated maintainability score"
    )
    
    extensibility_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Estimated extensibility score"
    )
    
    processing_time_ms: int = Field(
        0,
        description="Time taken to process in milliseconds"
    )
    
    @field_validator('improvement_suggestions')
    @classmethod
    def validate_suggestions(cls, v):
        """Validate suggestions are not empty strings"""
        return [s for s in v if s and s.strip()]
    
    def get_summary(self) -> Dict[str, Any]:
        """Get concise summary of design patterns analysis"""
        return {
            'patterns_identified': len(self.identified_patterns),
            'recommendations_count': len(self.pattern_recommendations),
            'design_quality': self.design_quality_score,
            'maintainability': self.maintainability_score,
            'extensibility': self.extensibility_score,
            'top_recommendation': self.top_recommended_pattern,
            'improvement_needed': len(self.improvement_suggestions) > 0
        }