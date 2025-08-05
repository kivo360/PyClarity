"""
Design Patterns Cognitive Tool

Provides software architecture patterns, design principle applications,
pattern selection frameworks, and architecture decision support.
"""

from .analyzer import DesignPatternsAnalyzer
from .models import (
    ArchitecturalDecision,
    # Enums
    ComplexityLevel,
    DesignAnalysis,
    # Supporting models
    DesignPattern,
    # Main models
    DesignPatternsContext,
    DesignPatternsResult,
    DesignPrinciple,
    PatternApplication,
    PatternCategory,
    PatternCombination,
    PatternComplexity,
)

__all__ = [
    # Enums
    "ComplexityLevel",
    "PatternCategory",
    "DesignPrinciple",
    "PatternComplexity",
    # Supporting models
    "DesignPattern",
    "PatternApplication",
    "ArchitecturalDecision",
    "PatternCombination",
    "DesignAnalysis",
    # Main models
    "DesignPatternsContext",
    "DesignPatternsResult",
    # Main class
    "DesignPatternsAnalyzer",
]
