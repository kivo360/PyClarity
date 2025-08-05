"""
PyClarity Tools Package

Cognitive tools for strategic thinking, problem-solving, and decision-making.
"""

# Missing imports that have implementations
from pyclarity.tools.collaborative_reasoning import (
    CollaborativeReasoningAnalyzer,
    CollaborativeReasoningContext,
    CollaborativeReasoningResult,
    ConsensusStrategy,
    DialogueStyle,
    PersonaType,
    ReasoningStyle,
)
from pyclarity.tools.debugging_approaches import (
    DebuggingApproachesAnalyzer,
    DebuggingApproachesContext,
    DebuggingApproachesResult,
    DebuggingStrategy,
    ErrorCategory,
    ErrorClassification,
)
from pyclarity.tools.decision_framework import (
    CriteriaType,
    DecisionCriteria,
    DecisionFrameworkAnalyzer,
    DecisionFrameworkContext,
    DecisionFrameworkResult,
    DecisionMatrix,
    DecisionMethodType,
    DecisionOption,
    RiskLevel,
)

# Cognitive Tools - Analysis & Problem Solving
from pyclarity.tools.design_patterns import (
    DesignPattern,
    DesignPatternsAnalyzer,
    DesignPatternsContext,
    DesignPatternsResult,
    PatternApplication,
    PatternCategory,
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
from pyclarity.tools.iterative_validation import (
    ConfidenceLevel,
    Hypothesis,
    IterativeValidationAnalyzer,
    IterativeValidationContext,
    IterativeValidationResult,
    Learning,
    LearningType,
    Refinement,
    TestDesign,
    TestResults,
    TestType,
    ValidationCycle,
    ValidationStatus,
)

# Cognitive Tools - Core Reasoning
from pyclarity.tools.mental_models import (
    MentalModelAssumption,
    MentalModelContext,
    MentalModelInsight,
    MentalModelResult,
    MentalModelsAnalyzer,
    MentalModelType,
)
from pyclarity.tools.metacognitive_monitoring import (
    BiasType,
    MetacognitiveMonitoringAnalyzer,
    MetacognitiveMonitoringContext,
    MetacognitiveMonitoringResult,
    MetaStrategies,
    MonitoringDepth,
    MonitoringFrequency,
)
from pyclarity.tools.multi_perspective import (
    ConflictSeverity,
    IntegrationApproach,
    IntegrationStrategy,
    MultiPerspectiveAnalyzer,
    MultiPerspectiveContext,
    MultiPerspectiveResult,
    Perspective,
    StakeholderType,
    SynergyConflict,
    ViewpointAnalysis,
)
from pyclarity.tools.programming_paradigms import (
    ParadigmAnalysis,
    ParadigmProfile,
    ProgrammingParadigm,
    ProgrammingParadigmsAnalyzer,
    ProgrammingParadigmsContext,
    ProgrammingParadigmsResult,
)
from pyclarity.tools.scientific_method import (
    Evidence,
    EvidenceType,
    Experiment,
    Hypothesis,
    HypothesisType,
    ScientificMethodAnalyzer,
    ScientificMethodContext,
    ScientificMethodResult,
    TestResult,
)
from pyclarity.tools.sequential_readiness import (
    Dependency,
    GapSeverity,
    Intervention,
    InterventionType,
    ReadinessGap,
    ReadinessLevel,
    ReadinessState,
    SequentialReadinessAnalyzer,
    SequentialReadinessContext,
    SequentialReadinessResult,
    StateTransition,
    TransitionType,
)

from .sequential_thinking import (
    BranchStrategy,
    ComplexityLevel,
    SequentialThinkingAnalyzer,
    SequentialThinkingContext,
    SequentialThinkingResult,
    ThoughtBranch,
    ThoughtRevision,
    ThoughtStep,
    ThoughtStepStatus,
    ThoughtStepType,
)
from .structured_argumentation import (
    ArgumentType,
    LogicalFallacy,
    StrengthLevel,
    StructuredArgumentationAnalyzer,
    StructuredArgumentationContext,
    StructuredArgumentationResult,
)
from .triple_constraint import (
    Constraint,
    ConstraintDimension,
    ConstraintPriority,
    OptimizationStrategy,
    Scenario,
    Tradeoff,
    TradeoffImpact,
    TripleConstraintAnalyzer,
    TripleConstraintContext,
    TripleConstraintResult,
)
from .visual_reasoning import (
    PatternType,
    SpatialRelationship,
    VisualElement,
    VisualReasoningAnalyzer,
    VisualReasoningContext,
    VisualReasoningResult,
    VisualRepresentationType,
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
