"""
Debugging Approaches Cognitive Tool

Provides systematic troubleshooting methodologies, error classification and resolution,
debugging strategy selection, and root cause analysis frameworks.
"""

from .analyzer import DebuggingApproachesAnalyzer
from .models import (
    # Enums
    ComplexityLevel,
    # Supporting models
    DebugContext,
    # Main models
    DebuggingApproachesContext,
    DebuggingApproachesResult,
    DebuggingHypothesis,
    DebuggingPhase,
    DebuggingRecommendation,
    DebuggingSession,
    DebuggingStep,
    DebuggingStrategy,
    ErrorCategory,
    ErrorClassification,
    RootCauseAnalysis,
    Severity,
)

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
