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

# Missing imports that have implementations
from .collaborative_reasoning import (
    CollaborativeReasoningAnalyzer,
    CollaborativeReasoningContext,
    CollaborativeReasoningResult,
    PersonaType,
    ConsensusStrategy,
    ReasoningStyle,
    DialogueStyle,
)

from .metacognitive_monitoring import (
    MetacognitiveMonitoringAnalyzer,
    MetacognitiveMonitoringContext,
    MetacognitiveMonitoringResult,
    BiasType,
    MetaStrategies,
    MonitoringDepth,
    MonitoringFrequency,
)

# Temporarily comment out impact_propagation due to generic type issues
# from .impact_propagation import (
#     ImpactPropagationAnalyzer,
#     ImpactPropagationContext,
#     ImpactPropagationResult,
#     ImpactType,
#     PropagationPath,
#     Node,
#     PropagationSpeed,
#     EffectMagnitude,
# )

# New FastMCP tools
from .iterative_validation import (
    IterativeValidationAnalyzer,
    IterativeValidationContext,
    IterativeValidationResult,
    ValidationStatus,
    TestType,
    ConfidenceLevel,
    LearningType,
    Hypothesis,
    TestDesign,
    TestResults,
    Learning,
    Refinement,
    ValidationCycle,
)

from .multi_perspective import (
    MultiPerspectiveAnalyzer,
    MultiPerspectiveContext,
    MultiPerspectiveResult,
    StakeholderType,
    ConflictSeverity,
    IntegrationApproach,
    Perspective,
    ViewpointAnalysis,
    SynergyConflict,
    IntegrationStrategy,
)

from .sequential_readiness import (
    SequentialReadinessAnalyzer,
    SequentialReadinessContext,
    SequentialReadinessResult,
    ReadinessLevel,
    TransitionType,
    GapSeverity,
    InterventionType,
    ReadinessState,
    StateTransition,
    ReadinessGap,
    Intervention,
    Dependency,
)

from .triple_constraint import (
    TripleConstraintAnalyzer,
    TripleConstraintContext,
    TripleConstraintResult,
    ConstraintDimension,
    ConstraintPriority,
    TradeoffImpact,
    OptimizationStrategy,
    Constraint,
    Tradeoff,
    Scenario,
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
    
    # Collaborative Reasoning
    "CollaborativeReasoningAnalyzer",
    "CollaborativeReasoningContext", 
    "CollaborativeReasoningResult",
    "PersonaType",
    "ConsensusStrategy",
    "ReasoningStyle",
    "DialogueStyle",
    
    # Metacognitive Monitoring
    "MetacognitiveMonitoringAnalyzer",
    "MetacognitiveMonitoringContext",
    "MetacognitiveMonitoringResult", 
    "BiasType",
    "MetaStrategies",
    "MonitoringDepth",
    "MonitoringFrequency",
    
    # Impact Propagation - temporarily disabled
    # "ImpactPropagationAnalyzer",
    # "ImpactPropagationContext",
    # "ImpactPropagationResult",
    # "ImpactType",
    # "PropagationPath",
    # "Node",
    # "PropagationSpeed",
    # "EffectMagnitude",
    
    # Iterative Validation
    "IterativeValidationAnalyzer",
    "IterativeValidationContext",
    "IterativeValidationResult",
    "ValidationStatus",
    "TestType",
    "ConfidenceLevel",
    "LearningType",
    "Hypothesis",
    "TestDesign",
    "TestResults",
    "Learning",
    "Refinement",
    "ValidationCycle",
    
    # Multi-Perspective
    "MultiPerspectiveAnalyzer",
    "MultiPerspectiveContext",
    "MultiPerspectiveResult",
    "StakeholderType",
    "ConflictSeverity",
    "IntegrationApproach",
    "Perspective",
    "ViewpointAnalysis",
    "SynergyConflict",
    "IntegrationStrategy",
    
    # Sequential Readiness
    "SequentialReadinessAnalyzer",
    "SequentialReadinessContext",
    "SequentialReadinessResult",
    "ReadinessLevel",
    "TransitionType",
    "GapSeverity",
    "InterventionType",
    "ReadinessState",
    "StateTransition",
    "ReadinessGap",
    "Intervention",
    "Dependency",
    
    # Triple Constraint
    "TripleConstraintAnalyzer",
    "TripleConstraintContext",
    "TripleConstraintResult",
    "ConstraintDimension",
    "ConstraintPriority",
    "TradeoffImpact",
    "OptimizationStrategy",
    "Constraint",
    "Tradeoff",
    "Scenario",
]

__version__ = "0.1.0"