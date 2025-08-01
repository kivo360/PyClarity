"""
Visual Reasoning Cognitive Tool

Provides spatial and diagrammatic thinking capabilities including visual problem-solving,
pattern recognition, diagram analysis, and spatial relationship understanding.
"""

from .models import (
    # Enums
    VisualRepresentationType,
    SpatialRelationship,
    PatternType,
    # Supporting models
    VisualElement,
    SpatialMapping,
    PatternRecognition,
    DiagramAnalysis,
    VisualProblemSolving,
    # Main models
    VisualReasoningContext,
    VisualReasoningResult,
)

from .analyzer import VisualReasoningAnalyzer

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