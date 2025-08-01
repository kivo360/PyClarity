"""
Programming Paradigms Cognitive Tool

Provides analysis of Object-Oriented, Functional, Procedural, and other programming
paradigms with selection criteria, optimization guidance, and paradigm combinations.
"""

from .models import (
    # Enums
    ComplexityLevel,
    ProgrammingParadigm,
    ParadigmCharacteristic,
    ProblemDomain,
    # Supporting models
    ParadigmProfile,
    ParadigmAnalysis,
    ParadigmComparison,
    ParadigmMix,
    CodeStructureAnalysis,
    # Main models
    ProgrammingParadigmsContext,
    ProgrammingParadigmsResult,
)

from .analyzer import ProgrammingParadigmsAnalyzer

__all__ = [
    # Enums
    "ComplexityLevel",
    "ProgrammingParadigm",
    "ParadigmCharacteristic",
    "ProblemDomain",
    # Supporting models
    "ParadigmProfile",
    "ParadigmAnalysis",
    "ParadigmComparison",
    "ParadigmMix",
    "CodeStructureAnalysis",
    # Main models
    "ProgrammingParadigmsContext",
    "ProgrammingParadigmsResult",
    # Main class
    "ProgrammingParadigmsAnalyzer",
]