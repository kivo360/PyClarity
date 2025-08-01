"""
Debugging Approaches Cognitive Tool

Provides systematic troubleshooting methodologies, error classification and resolution,
debugging strategy selection, and root cause analysis frameworks.
"""

from .models import (
    # Enums
    ComplexityLevel,
    DebuggingStrategy,
    ErrorCategory,
    Severity,
    DebuggingPhase,
    # Supporting models
    DebugContext,
    ErrorClassification,
    DebuggingHypothesis,
    DebuggingStep,
    RootCauseAnalysis,
    DebuggingSession,
    DebuggingRecommendation,
    # Main models
    DebuggingApproachesContext,
    DebuggingApproachesResult,
)

from .analyzer import DebuggingApproachesAnalyzer

__all__ = [
    # Enums
    "ComplexityLevel",
    "DebuggingStrategy",
    "ErrorCategory",
    "Severity",
    "DebuggingPhase",
    # Supporting models
    "DebugContext",
    "ErrorClassification",
    "DebuggingHypothesis",
    "DebuggingStep",
    "RootCauseAnalysis",
    "DebuggingSession",
    "DebuggingRecommendation",
    # Main models
    "DebuggingApproachesContext",
    "DebuggingApproachesResult",
    # Main class
    "DebuggingApproachesAnalyzer",
]