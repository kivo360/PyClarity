"""
Iterative Validation Cognitive Tool

Systematic hypothesis-test-learn-refine cycles for research, development,
problem-solving, and continuous improvement through empirical validation.
"""

from .models import (
    # Enums
    ComplexityLevel,
    ValidationStatus,
    TestType,
    ConfidenceLevel,
    LearningType,
    # Supporting models
    Hypothesis,
    TestDesign,
    TestResults,
    Learning,
    Refinement,
    ValidationCycle,
    # Main models
    IterativeValidationContext,
    IterativeValidationResult,
)

from .analyzer import IterativeValidationAnalyzer

__all__ = [
    # Enums
    "ComplexityLevel",
    "ValidationStatus",
    "TestType",
    "ConfidenceLevel",
    "LearningType",
    # Supporting models
    "Hypothesis",
    "TestDesign", 
    "TestResults",
    "Learning",
    "Refinement",
    "ValidationCycle",
    # Main models
    "IterativeValidationContext",
    "IterativeValidationResult",
    # Main class
    "IterativeValidationAnalyzer",
]