"""
Visual Reasoning Cognitive Tool

Provides spatial and diagrammatic thinking capabilities including visual problem-solving,
pattern recognition, diagram analysis, and spatial relationship understanding.
"""

from .analyzer import VisualReasoningAnalyzer
from .models import (
    DiagramAnalysis,
    PatternRecognition,
    PatternType,
    SpatialMapping,
    SpatialRelationship,
    # Supporting models
    VisualElement,
    VisualProblemSolving,
    # Main models
    VisualReasoningContext,
    VisualReasoningResult,
    # Enums
    VisualRepresentationType,
)

__all__ = [
    # Enums
    "VisualRepresentationType",
    "SpatialRelationship",
    "PatternType",
    # Supporting models
    "VisualElement",
    "SpatialMapping",
    "PatternRecognition",
    "DiagramAnalysis",
    "VisualProblemSolving",
    # Main models
    "VisualReasoningContext",
    "VisualReasoningResult",
    # Main class
    "VisualReasoningAnalyzer",
]
