"""
Programming Paradigms Cognitive Tool

Provides analysis of Object-Oriented, Functional, Procedural, and other programming
paradigms with selection criteria, optimization guidance, and paradigm combinations.
"""

from .analyzer import ProgrammingParadigmsAnalyzer
from .models import (
    CodeStructureAnalysis,
    # Enums
    ComplexityLevel,
    ParadigmAnalysis,
    ParadigmCharacteristic,
    ParadigmComparison,
    ParadigmMix,
    # Supporting models
    ParadigmProfile,
    ProblemDomain,
    ProgrammingParadigm,
    # Main models
    ProgrammingParadigmsContext,
    ProgrammingParadigmsResult,
)

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
