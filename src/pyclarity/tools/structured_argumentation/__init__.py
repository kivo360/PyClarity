"""
Structured Argumentation Cognitive Tool

Provides logic chain construction, argument validity assessment, evidence evaluation,
and reasoning quality validation for structured arguments.
"""

from .models import (
    # Enums
    ArgumentType,
    LogicalFallacy,
    EvidenceType,
    StrengthLevel,
    # Supporting models
    Premise,
    Evidence,
    LogicChain,
    ArgumentStructure,
    FallacyDetection,
    ArgumentAnalysis,
    CounterargumentAnalysis,
    DebateStructure,
    # Main models
    StructuredArgumentationContext,
    StructuredArgumentationResult,
)

from .analyzer import StructuredArgumentationAnalyzer

__all__ = [
    # Enums
    "ArgumentType",
    "LogicalFallacy",
    "EvidenceType",
    "StrengthLevel",
    # Supporting models
    "Premise",
    "Evidence",
    "LogicChain",
    "ArgumentStructure",
    "FallacyDetection",
    "ArgumentAnalysis",
    "CounterargumentAnalysis",
    "DebateStructure",
    # Main models
    "StructuredArgumentationContext",
    "StructuredArgumentationResult",
    # Main class
    "StructuredArgumentationAnalyzer",
]