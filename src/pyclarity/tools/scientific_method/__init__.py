"""
Scientific Method Cognitive Tool

Provides hypothesis-driven reasoning through hypothesis formation and testing,
experimental design principles, evidence evaluation and analysis,
theory building and validation, and systematic inquiry processes.
"""

from .models import (
    # Enums
    ComplexityLevel,
    HypothesisType,
    EvidenceType,
    EvidenceQuality,
    TestResult,
    # Supporting models
    Hypothesis,
    Evidence,
    Experiment,
    HypothesisTest,
    TheoryConstruction,
    # Main models
    ScientificMethodContext,
    ScientificMethodResult,
)

from .analyzer import ScientificMethodAnalyzer

__all__ = [
    # Enums
    "ComplexityLevel",
    "HypothesisType",
    "EvidenceType",
    "EvidenceQuality",
    "TestResult",
    # Supporting models
    "Hypothesis",
    "Evidence",
    "Experiment",
    "HypothesisTest",
    "TheoryConstruction",
    # Main models
    "ScientificMethodContext",
    "ScientificMethodResult",
    # Main class
    "ScientificMethodAnalyzer",
]