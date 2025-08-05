"""
Multi-Perspective Analysis Cognitive Tool

Analyzes scenarios from multiple stakeholder viewpoints to identify
synergies, conflicts, and create comprehensive integration strategies.
"""

from .analyzer import MultiPerspectiveAnalyzer
from .models import (
    ComplexityLevel,
    ConflictSeverity,
    IntegrationApproach,
    IntegrationStrategy,
    # Main models
    MultiPerspectiveContext,
    MultiPerspectiveResult,
    # Supporting models
    Perspective,
    # Enums
    StakeholderType,
    SynergyConflict,
    ViewpointAnalysis,
)

__all__ = [
    # Enums
    "StakeholderType",
    "ConflictSeverity",
    "IntegrationApproach",
    "ComplexityLevel",
    # Supporting models
    "Perspective",
    "ViewpointAnalysis",
    "SynergyConflict",
    "IntegrationStrategy",
    # Main models
    "MultiPerspectiveContext",
    "MultiPerspectiveResult",
    # Main class
    "MultiPerspectiveAnalyzer",
]
