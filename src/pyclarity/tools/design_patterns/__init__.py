"""
Design Patterns Cognitive Tool

Provides software architecture patterns, design principle applications,
pattern selection frameworks, and architecture decision support.
"""

from .models import (
    # Enums
    ComplexityLevel,
    PatternCategory,
    DesignPrinciple,
    PatternComplexity,
    # Supporting models
    DesignPattern,
    PatternApplication,
    ArchitecturalDecision,
    PatternCombination,
    DesignAnalysis,
    # Main models
    DesignPatternsContext,
    DesignPatternsResult,
)

from .analyzer import DesignPatternsAnalyzer

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