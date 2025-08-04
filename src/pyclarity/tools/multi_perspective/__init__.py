"""
Multi-Perspective Analysis Cognitive Tool

Analyzes scenarios from multiple stakeholder viewpoints to identify
synergies, conflicts, and create comprehensive integration strategies.
"""

from .models import (
    # Enums
    StakeholderType,
    ConflictSeverity,
    IntegrationApproach,
    ComplexityLevel,
    # Supporting models
    Perspective,
    ViewpointAnalysis,
    SynergyConflict,
    IntegrationStrategy,
    # Main models
    MultiPerspectiveContext,
    MultiPerspectiveResult,
)

from .analyzer import MultiPerspectiveAnalyzer

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