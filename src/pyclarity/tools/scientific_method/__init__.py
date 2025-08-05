"""
Scientific Method Cognitive Tool

Provides hypothesis-driven reasoning through hypothesis formation and testing,
experimental design principles, evidence evaluation and analysis,
theory building and validation, and systematic inquiry processes.
"""

from .analyzer import ScientificMethodAnalyzer
from .models import (
    # Enums
    ComplexityLevel,
    Evidence,
    EvidenceQuality,
    EvidenceType,
    Experiment,
    # Supporting models
    Hypothesis,
    HypothesisTest,
    HypothesisType,
    # Main models
    ScientificMethodContext,
    ScientificMethodResult,
    TestResult,
    TheoryConstruction,
)

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
