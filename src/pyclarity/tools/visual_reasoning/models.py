"""
Visual Reasoning Models

Data structures for spatial and diagrammatic thinking patterns,
visual problem-solving, pattern recognition, and diagram analysis capabilities.
"""

import math
import uuid
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel, Field, field_validator


class VisualRepresentationType(str, Enum):
    """Types of visual representations"""
    DIAGRAM = "diagram"
    CHART = "chart"
    FLOWCHART = "flowchart"
    MINDMAP = "mindmap"
    GRAPH = "graph"
    TREE = "tree"
    MATRIX = "matrix"
    SPATIAL_MAP = "spatial_map"


class SpatialRelationship(str, Enum):
    """Spatial relationship types"""
    ABOVE = "above"
    BELOW = "below"
    LEFT_OF = "left_of"
    RIGHT_OF = "right_of"
    INSIDE = "inside"
    OUTSIDE = "outside"
    ADJACENT = "adjacent"
    CONNECTED = "connected"
    PARALLEL = "parallel"
    PERPENDICULAR = "perpendicular"


class PatternType(str, Enum):
    """Visual pattern types"""
    SYMMETRICAL = "symmetrical"
    ASYMMETRICAL = "asymmetrical"
    REPETITIVE = "repetitive"
    GRADIENT = "gradient"
    HIERARCHICAL = "hierarchical"
    CIRCULAR = "circular"
    LINEAR = "linear"
    BRANCHING = "branching"


class VisualElement(BaseModel):
    """Represents a visual element in a diagram or representation"""

    element_id: str = Field(
        ...,
        description="Unique identifier for the element",
        min_length=1,
        max_length=100
    )

    element_type: str = Field(
        ...,
        description="Type of visual element (rectangle, circle, text, etc.)",
        min_length=1,
        max_length=50
    )

    position: tuple[float, float] = Field(
        ...,
        description="X, Y coordinates of the element"
    )

    size: tuple[float, float] = Field(
        ...,
        description="Width, height of the element"
    )

    properties: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional properties of the element"
    )

    relationships: list[str] = Field(
        default_factory=list,
        description="IDs of related elements",
        max_items=20
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Element metadata including calculated properties"
    )

    @field_validator('position')
    @classmethod
    def validate_position(cls, v):
        """Validate position coordinates"""
        if len(v) != 2:
            raise ValueError("Position must be a tuple of exactly 2 coordinates")
        x, y = v
        if not isinstance(x, int | float) or not isinstance(y, int | float):
            raise ValueError("Position coordinates must be numeric")
        return v

    @field_validator('size')
    @classmethod
    def validate_size(cls, v):
        """Validate size dimensions"""
        if len(v) != 2:
            raise ValueError("Size must be a tuple of exactly 2 dimensions")
        width, height = v
        if not isinstance(width, int | float) or not isinstance(height, int | float):
            raise ValueError("Size dimensions must be numeric")
        if width <= 0 or height <= 0:
            raise ValueError("Size dimensions must be positive")
        return v


class SpatialMapping(BaseModel):
    """Maps relationships between visual elements"""

    mapping_id: str = Field(
        default_factory=lambda: f"mapping_{str(uuid.uuid4())[:8]}",
        description="Unique mapping identifier"
    )

    elements: list[VisualElement] = Field(
        ...,
        description="Visual elements in the mapping",
        min_items=1,
        max_items=100
    )

    relationships: dict[str, list[SpatialRelationship]] = Field(
        default_factory=dict,
        description="Spatial relationships between elements"
    )

    spatial_constraints: list[str] = Field(
        default_factory=list,
        description="Spatial constraints and rules",
        max_items=50
    )

    coordinate_system: str = Field(
        "cartesian",
        description="Coordinate system used",
        pattern="^(cartesian|polar|spherical|cylindrical)$"
    )

    scale_factor: float = Field(
        1.0,
        ge=0.1,
        le=100.0,
        description="Scale factor for the mapping"
    )


class PatternRecognition(BaseModel):
    """Results of visual pattern analysis"""

    pattern_id: str = Field(
        default_factory=lambda: f"pattern_{str(uuid.uuid4())[:8]}",
        description="Unique pattern identifier"
    )

    pattern_type: PatternType = Field(
        ...,
        description="Type of pattern identified"
    )

    confidence_level: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence in pattern recognition"
    )

    pattern_elements: list[str] = Field(
        ...,
        description="Element IDs involved in the pattern",
        min_items=1,
        max_items=50
    )

    pattern_description: str = Field(
        ...,
        description="Description of the identified pattern",
        min_length=10,
        max_length=500
    )

    pattern_rules: list[str] = Field(
        default_factory=list,
        description="Rules that define the pattern",
        max_items=10
    )

    similarity_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Similarity score for pattern matching"
    )

    variations_detected: list[str] = Field(
        default_factory=list,
        description="Variations of the pattern detected",
        max_items=8
    )


class DiagramAnalysis(BaseModel):
    """Analysis of diagram structure and meaning"""

    diagram_id: str = Field(
        default_factory=lambda: f"diagram_{str(uuid.uuid4())[:8]}",
        description="Unique diagram identifier"
    )

    representation_type: VisualRepresentationType = Field(
        ...,
        description="Type of visual representation"
    )

    elements: list[VisualElement] = Field(
        ...,
        description="Visual elements in the diagram",
        min_items=1,
        max_items=200
    )

    spatial_mapping: SpatialMapping = Field(
        ...,
        description="Spatial mapping of elements"
    )

    patterns_identified: list[PatternRecognition] = Field(
        default_factory=list,
        description="Patterns identified in the diagram",
        max_items=20
    )

    key_insights: list[str] = Field(
        default_factory=list,
        description="Key insights from the analysis",
        max_items=15
    )

    interpretation: str = Field(
        ...,
        description="Overall interpretation of the diagram",
        min_length=20,
        max_length=1000
    )

    confidence_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence in the analysis"
    )


class VisualProblemSolving(BaseModel):
    """Visual approach to problem solving"""

    problem_id: str = Field(
        default_factory=lambda: f"problem_{str(uuid.uuid4())[:8]}",
        description="Unique problem identifier"
    )

    problem_description: str = Field(
        ...,
        description="Description of the problem to solve",
        min_length=20,
        max_length=2000
    )

    visual_representation: DiagramAnalysis = Field(
        ...,
        description="Visual representation used for solving"
    )

    solution_steps: list[str] = Field(
        default_factory=list,
        description="Steps in the visual solution",
        max_items=20
    )

    visual_aids_used: list[str] = Field(
        default_factory=list,
        description="Visual aids utilized in solving",
        max_items=10
    )

    spatial_reasoning_applied: list[str] = Field(
        default_factory=list,
        description="Spatial reasoning techniques applied",
        max_items=10
    )

    pattern_matching_used: list[PatternRecognition] = Field(
        default_factory=list,
        description="Pattern matching techniques used",
        max_items=10
    )

    solution_confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence in the solution"
    )


class VisualReasoningContext(BaseModel):
    """Context for visual reasoning analysis"""

    problem_type: str = Field(
        ...,
        description="Type of visual reasoning problem",
        min_length=5,
        max_length=100
    )

    visual_elements_data: list[dict[str, Any]] = Field(
        ...,
        description="Data for visual elements to analyze",
        min_items=1,
        max_items=100
    )

    representation_type: VisualRepresentationType = Field(
        VisualRepresentationType.DIAGRAM,
        description="Type of visual representation"
    )

    coordinate_system: str = Field(
        "cartesian",
        description="Coordinate system to use",
        pattern="^(cartesian|polar|spherical|cylindrical)$"
    )

    analysis_goals: list[str] = Field(
        default_factory=list,
        description="Goals for the visual analysis",
        max_items=10
    )

    include_pattern_recognition: bool = Field(
        True,
        description="Whether to include pattern recognition"
    )

    include_spatial_analysis: bool = Field(
        True,
        description="Whether to include spatial relationship analysis"
    )

    include_problem_solving: bool = Field(
        False,
        description="Whether to include problem-solving approach"
    )

    problem_description: str | None = Field(
        None,
        description="Problem description for visual problem solving",
        max_length=2000
    )

    max_patterns: int = Field(
        10,
        ge=1,
        le=20,
        description="Maximum number of patterns to identify"
    )

    confidence_threshold: float = Field(
        0.5,
        ge=0.0,
        le=1.0,
        description="Minimum confidence threshold for results"
    )

    @field_validator('visual_elements_data')
    @classmethod
    def validate_visual_elements(cls, v):
        """Validate visual elements data"""
        required_fields = ['element_id', 'element_type', 'position', 'size']
        for i, element in enumerate(v):
            for field in required_fields:
                if field not in element:
                    raise ValueError(f"Element {i} missing required field: {field}")

            # Validate position
            if not isinstance(element['position'], list | tuple) or len(element['position']) != 2:
                raise ValueError(f"Element {i} position must be [x, y] coordinates")

            # Validate size
            if not isinstance(element['size'], list | tuple) or len(element['size']) != 2:
                raise ValueError(f"Element {i} size must be [width, height] dimensions")

        return v


class VisualReasoningResult(BaseModel):
    """Result of visual reasoning analysis"""

    visual_elements: list[VisualElement] = Field(
        default_factory=list,
        description="Processed visual elements"
    )

    spatial_mapping: SpatialMapping | None = Field(
        None,
        description="Spatial mapping of elements"
    )

    patterns_identified: list[PatternRecognition] = Field(
        default_factory=list,
        description="Visual patterns identified"
    )

    diagram_analysis: DiagramAnalysis | None = Field(
        None,
        description="Complete diagram analysis"
    )

    visual_problem_solving: VisualProblemSolving | None = Field(
        None,
        description="Visual problem-solving results"
    )

    spatial_relationships: dict[str, list[str]] = Field(
        default_factory=dict,
        description="Spatial relationships between elements"
    )

    key_insights: list[str] = Field(
        default_factory=list,
        description="Key insights from visual analysis",
        max_items=20
    )

    recommendations: list[str] = Field(
        default_factory=list,
        description="Recommendations based on analysis",
        max_items=15
    )

    visual_reasoning_techniques: list[str] = Field(
        default_factory=list,
        description="Visual reasoning techniques applied",
        max_items=10
    )

    confidence_scores: dict[str, float] = Field(
        default_factory=dict,
        description="Confidence scores for different analyses"
    )

    processing_metrics: dict[str, Any] = Field(
        default_factory=dict,
        description="Processing metrics and statistics"
    )

    processing_time_ms: int = Field(
        0,
        description="Time taken to process in milliseconds"
    )

    def get_summary(self) -> dict[str, Any]:
        """Get concise summary of visual reasoning analysis"""
        return {
            'elements_analyzed': len(self.visual_elements),
            'patterns_found': len(self.patterns_identified),
            'spatial_relationships': sum(len(rels) for rels in self.spatial_relationships.values()),
            'has_diagram_analysis': self.diagram_analysis is not None,
            'has_problem_solving': self.visual_problem_solving is not None,
            'key_insights_count': len(self.key_insights),
            'overall_confidence': self.confidence_scores.get('overall', 0.0),
            'techniques_used': len(self.visual_reasoning_techniques)
        }
