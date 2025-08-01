"""
PyClarity Tools Package

Cognitive tools for strategic thinking, problem-solving, and decision-making.
"""

from .sequential_thinking import (
    SequentialThinkingAnalyzer,
    SequentialThinkingContext,
    SequentialThinkingResult,
    ComplexityLevel,
    ThoughtStepType,
    BranchStrategy,
    ThoughtStepStatus,
    ThoughtStep,
    ThoughtRevision,
    ThoughtBranch,
)

# Cognitive Tools - Core Reasoning
from .mental_models import (
    MentalModelsAnalyzer,
    MentalModelContext,
    MentalModelResult,
    MentalModelType,
    MentalModelInsight,
    MentalModelAssumption,
)

from .decision_framework import (
    DecisionFrameworkAnalyzer,
    DecisionFrameworkContext,
    DecisionFrameworkResult,
    DecisionMethodType,
    CriteriaType,
    RiskLevel,
    DecisionCriteria,
    DecisionOption,
    DecisionMatrix,
)

from .scientific_method import (
    ScientificMethodAnalyzer,
    ScientificMethodContext,
    ScientificMethodResult,
    HypothesisType,
    EvidenceType,
    TestResult,
    Hypothesis,
    Evidence,
    Experiment,
)

# Cognitive Tools - Analysis & Problem Solving
from .design_patterns import (
    DesignPatternsAnalyzer,
    DesignPatternsContext,
    DesignPatternsResult,
    PatternCategory,
    DesignPattern,
    PatternApplication,
)

from .programming_paradigms import (
    ProgrammingParadigmsAnalyzer,
    ProgrammingParadigmsContext,
    ProgrammingParadigmsResult,
    ProgrammingParadigm,
    ParadigmProfile,
    ParadigmAnalysis,
)

from .debugging_approaches import (
    DebuggingApproachesAnalyzer,
    DebuggingApproachesContext,
    DebuggingApproachesResult,
    DebuggingStrategy,
    ErrorCategory,
    ErrorClassification,
)

from .visual_reasoning import (
    VisualReasoningAnalyzer,
    VisualReasoningContext,
    VisualReasoningResult,
    VisualRepresentationType,
    SpatialRelationship,
    PatternType,
    VisualElement,
)

from .structured_argumentation import (
    StructuredArgumentationAnalyzer,
    StructuredArgumentationContext,
    StructuredArgumentationResult,
    ArgumentType,
    LogicalFallacy,
    EvidenceType,
    StrengthLevel,
)

__all__ = [
    # Sequential Thinking
    "SequentialThinkingAnalyzer",
    "SequentialThinkingContext",
    "SequentialThinkingResult",
    "ComplexityLevel",
    "ThoughtStepType",
    "BranchStrategy",
    "ThoughtStepStatus",
    "ThoughtStep",
    "ThoughtRevision",
    "ThoughtBranch",
    
    # Mental Models
    "MentalModelsAnalyzer",
    "MentalModelContext",
    "MentalModelResult",
    "MentalModelType",
    "MentalModelInsight",
    "MentalModelAssumption",
    
    # Decision Framework
    "DecisionFrameworkAnalyzer",
    "DecisionFrameworkContext",
    "DecisionFrameworkResult",
    "DecisionMethodType",
    "CriteriaType",
    "RiskLevel",
    "DecisionCriteria",
    "DecisionOption",
    "DecisionMatrix",
    
    # Scientific Method
    "ScientificMethodAnalyzer",
    "ScientificMethodContext",
    "ScientificMethodResult",
    "HypothesisType",
    "EvidenceType",
    "TestResult",
    "Hypothesis",
    "Evidence",
    "Experiment",
    
    # Design Patterns
    "DesignPatternsAnalyzer",
    "DesignPatternsContext",
    "DesignPatternsResult",
    "PatternCategory",
    "DesignPattern",
    "PatternApplication",
    
    # Programming Paradigms
    "ProgrammingParadigmsAnalyzer",
    "ProgrammingParadigmsContext",
    "ProgrammingParadigmsResult",
    "ProgrammingParadigm",
    "ParadigmProfile",
    "ParadigmAnalysis",
    
    # Debugging Approaches
    "DebuggingApproachesAnalyzer",
    "DebuggingApproachesContext",
    "DebuggingApproachesResult",
    "DebuggingStrategy",
    "ErrorCategory",
    "ErrorClassification",
    
    # Visual Reasoning  
    "VisualReasoningAnalyzer",
    "VisualReasoningContext",
    "VisualReasoningResult",
    "VisualRepresentationType",
    "SpatialRelationship",
    "PatternType",
    "VisualElement",
    
    # Structured Argumentation
    "StructuredArgumentationAnalyzer",
    "StructuredArgumentationContext",
    "StructuredArgumentationResult",
    "ArgumentType",
    "LogicalFallacy",
    "EvidenceType",
    "StrengthLevel",
]

__version__ = "0.1.0"