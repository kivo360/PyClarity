"""
Structured Argumentation Cognitive Tool

Provides logic chain construction, argument validity assessment, evidence evaluation,
and reasoning quality validation for structured arguments.
"""

from .analyzer import StructuredArgumentationAnalyzer
from .models import (
    ArgumentAnalysis,
    ArgumentStructure,
    # Enums
    ArgumentType,
    CounterargumentAnalysis,
    DebateStructure,
    Evidence,
    EvidenceType,
    FallacyDetection,
    LogicalFallacy,
    LogicChain,
    # Supporting models
    Premise,
    StrengthLevel,
    # Main models
    StructuredArgumentationContext,
    StructuredArgumentationResult,
)

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
