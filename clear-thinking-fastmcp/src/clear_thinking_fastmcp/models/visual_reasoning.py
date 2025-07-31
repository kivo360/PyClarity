"""
Visual Reasoning Models for Clear Thinking FastMCP

Provides spatial and diagrammatic thinking patterns for visual problem-solving,
pattern recognition, and diagram-based analysis capabilities.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum

from .base import BaseClearThinkingModel


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


@dataclass
class VisualElement:
    """Represents a visual element in a diagram or representation"""
    element_id: str
    element_type: str
    position: Tuple[float, float]  # x, y coordinates
    size: Tuple[float, float]  # width, height
    properties: Dict[str, Any]
    relationships: List[str]  # IDs of related elements
    metadata: Dict[str, Any]


@dataclass
class SpatialMapping:
    """Maps relationships between visual elements"""
    mapping_id: str
    elements: List[VisualElement]
    relationships: Dict[str, List[SpatialRelationship]]
    spatial_constraints: List[str]
    coordinate_system: str
    scale_factor: float


@dataclass
class PatternRecognition:
    """Results of visual pattern analysis"""
    pattern_id: str
    pattern_type: PatternType
    confidence_level: float
    pattern_elements: List[str]  # Element IDs
    pattern_description: str
    pattern_rules: List[str]
    similarity_score: float
    variations_detected: List[str]


@dataclass
class DiagramAnalysis:
    """Analysis of diagram structure and meaning"""
    diagram_id: str
    representation_type: VisualRepresentationType
    elements: List[VisualElement]
    spatial_mapping: SpatialMapping
    patterns_identified: List[PatternRecognition]
    key_insights: List[str]
    interpretation: str
    confidence_score: float


@dataclass
class VisualProblemSolving:
    """Visual approach to problem solving"""
    problem_id: str
    problem_description: str
    visual_representation: DiagramAnalysis
    solution_steps: List[str]
    visual_aids_used: List[str]
    spatial_reasoning_applied: List[str]
    pattern_matching_used: List[PatternRecognition]
    solution_confidence: float


class VisualReasoningModel(BaseClearThinkingModel):
    """
    Visual Reasoning cognitive model for spatial and diagrammatic thinking.
    
    Capabilities:
    - Spatial relationship analysis
    - Visual pattern recognition
    - Diagram interpretation
    - Visual problem-solving approaches
    """
    
    def create_visual_element(
        self,
        element_id: str,
        element_type: str,
        position: Tuple[float, float],
        size: Tuple[float, float],
        properties: Optional[Dict[str, Any]] = None,
        relationships: Optional[List[str]] = None
    ) -> VisualElement:
        """Create a visual element with spatial properties"""
        return VisualElement(
            element_id=element_id,
            element_type=element_type,
            position=position,
            size=size,
            properties=properties or {},
            relationships=relationships or [],
            metadata={
                "created_at": self._get_current_timestamp(),
                "area": size[0] * size[1],
                "center": (position[0] + size[0]/2, position[1] + size[1]/2)
            }
        )
    
    def analyze_spatial_relationships(
        self,
        elements: List[VisualElement]
    ) -> Dict[str, List[SpatialRelationship]]:
        """Analyze spatial relationships between visual elements"""
        relationships = {}
        
        for i, elem1 in enumerate(elements):
            relationships[elem1.element_id] = []
            
            for j, elem2 in enumerate(elements):
                if i != j:
                    # Calculate spatial relationships
                    rel = self._calculate_spatial_relationship(elem1, elem2)
                    if rel:
                        relationships[elem1.element_id].append(rel)
        
        return relationships
    
    def _calculate_spatial_relationship(
        self,
        elem1: VisualElement,
        elem2: VisualElement
    ) -> Optional[SpatialRelationship]:
        """Calculate spatial relationship between two elements"""
        x1, y1 = elem1.position
        w1, h1 = elem1.size
        x2, y2 = elem2.position
        w2, h2 = elem2.size
        
        # Element 1 boundaries
        left1, right1 = x1, x1 + w1
        top1, bottom1 = y1, y1 + h1
        
        # Element 2 boundaries
        left2, right2 = x2, x2 + w2
        top2, bottom2 = y2, y2 + h2
        
        # Check relationships
        if right1 < left2:
            return SpatialRelationship.LEFT_OF
        elif left1 > right2:
            return SpatialRelationship.RIGHT_OF
        elif bottom1 < top2:
            return SpatialRelationship.ABOVE
        elif top1 > bottom2:
            return SpatialRelationship.BELOW
        elif (left1 >= left2 and right1 <= right2 and 
              top1 >= top2 and bottom1 <= bottom2):
            return SpatialRelationship.INSIDE
        elif (left2 >= left1 and right2 <= right1 and 
              top2 >= top1 and bottom2 <= bottom1):
            return SpatialRelationship.OUTSIDE
        else:
            # Check for adjacency or connection
            overlap_x = max(0, min(right1, right2) - max(left1, left2))
            overlap_y = max(0, min(bottom1, bottom2) - max(top1, top2))
            
            if overlap_x > 0 or overlap_y > 0:
                return SpatialRelationship.ADJACENT
        
        return None
    
    def recognize_visual_patterns(
        self,
        elements: List[VisualElement]
    ) -> List[PatternRecognition]:
        """Recognize patterns in visual elements"""
        patterns = []
        
        # Check for symmetrical patterns
        symmetry_pattern = self._detect_symmetry(elements)
        if symmetry_pattern:
            patterns.append(symmetry_pattern)
        
        # Check for repetitive patterns
        repetition_pattern = self._detect_repetition(elements)
        if repetition_pattern:
            patterns.append(repetition_pattern)
        
        # Check for hierarchical patterns
        hierarchy_pattern = self._detect_hierarchy(elements)
        if hierarchy_pattern:
            patterns.append(hierarchy_pattern)
        
        return patterns
    
    def _detect_symmetry(self, elements: List[VisualElement]) -> Optional[PatternRecognition]:
        """Detect symmetrical patterns in elements"""
        if len(elements) < 2:
            return None
        
        # Simple symmetry detection based on position mirroring
        center_x = sum(elem.position[0] + elem.size[0]/2 for elem in elements) / len(elements)
        
        symmetric_pairs = 0
        for elem in elements:
            elem_center_x = elem.position[0] + elem.size[0]/2
            distance_from_center = abs(elem_center_x - center_x)
            
            # Look for mirrored element
            for other_elem in elements:
                if elem != other_elem:
                    other_center_x = other_elem.position[0] + other_elem.size[0]/2
                    other_distance = abs(other_center_x - center_x)
                    
                    if abs(distance_from_center - other_distance) < 0.1:
                        symmetric_pairs += 1
                        break
        
        if symmetric_pairs >= len(elements) * 0.6:  # 60% threshold
            return PatternRecognition(
                pattern_id=f"symmetry_{self._generate_id()}",
                pattern_type=PatternType.SYMMETRICAL,
                confidence_level=symmetric_pairs / len(elements),
                pattern_elements=[elem.element_id for elem in elements],
                pattern_description="Symmetrical arrangement detected",
                pattern_rules=["Elements are mirrored around center axis"],
                similarity_score=symmetric_pairs / len(elements),
                variations_detected=[]
            )
        
        return None
    
    def _detect_repetition(self, elements: List[VisualElement]) -> Optional[PatternRecognition]:
        """Detect repetitive patterns in elements"""
        if len(elements) < 3:
            return None
        
        # Group elements by type
        type_groups = {}
        for elem in elements:
            if elem.element_type not in type_groups:
                type_groups[elem.element_type] = []
            type_groups[elem.element_type].append(elem)
        
        # Check for repeated types
        repeated_types = [group for group in type_groups.values() if len(group) >= 3]
        
        if repeated_types:
            largest_group = max(repeated_types, key=len)
            return PatternRecognition(
                pattern_id=f"repetition_{self._generate_id()}",
                pattern_type=PatternType.REPETITIVE,
                confidence_level=len(largest_group) / len(elements),
                pattern_elements=[elem.element_id for elem in largest_group],
                pattern_description=f"Repetitive pattern of {largest_group[0].element_type}",
                pattern_rules=["Similar elements repeated multiple times"],
                similarity_score=len(largest_group) / len(elements),
                variations_detected=[]
            )
        
        return None
    
    def _detect_hierarchy(self, elements: List[VisualElement]) -> Optional[PatternRecognition]:
        """Detect hierarchical patterns based on size and position"""
        if len(elements) < 3:
            return None
        
        # Sort by size (area)
        sorted_elements = sorted(elements, key=lambda e: e.size[0] * e.size[1], reverse=True)
        
        # Check if larger elements are positioned above smaller ones
        hierarchical_count = 0
        for i in range(len(sorted_elements) - 1):
            larger = sorted_elements[i]
            smaller = sorted_elements[i + 1]
            
            if larger.position[1] < smaller.position[1]:  # y increases downward
                hierarchical_count += 1
        
        if hierarchical_count >= len(elements) * 0.5:  # 50% threshold
            return PatternRecognition(
                pattern_id=f"hierarchy_{self._generate_id()}",
                pattern_type=PatternType.HIERARCHICAL,
                confidence_level=hierarchical_count / (len(elements) - 1),
                pattern_elements=[elem.element_id for elem in sorted_elements],
                pattern_description="Hierarchical arrangement by size and position",
                pattern_rules=["Larger elements positioned above smaller ones"],
                similarity_score=hierarchical_count / (len(elements) - 1),
                variations_detected=[]
            )
        
        return None
    
    def create_spatial_mapping(
        self,
        elements: List[VisualElement],
        coordinate_system: str = "cartesian"
    ) -> SpatialMapping:
        """Create spatial mapping of visual elements"""
        relationships = self.analyze_spatial_relationships(elements)
        
        # Generate spatial constraints
        constraints = []
        for elem_id, rels in relationships.items():
            for rel in rels:
                constraints.append(f"{elem_id} {rel.value} related_element")
        
        return SpatialMapping(
            mapping_id=f"mapping_{self._generate_id()}",
            elements=elements,
            relationships=relationships,
            spatial_constraints=constraints,
            coordinate_system=coordinate_system,
            scale_factor=1.0
        )
    
    def analyze_diagram(
        self,
        elements: List[VisualElement],
        representation_type: VisualRepresentationType
    ) -> DiagramAnalysis:
        """Analyze diagram structure and extract insights"""
        spatial_mapping = self.create_spatial_mapping(elements)
        patterns = self.recognize_visual_patterns(elements)
        
        # Generate key insights
        insights = []
        if patterns:
            insights.append(f"Identified {len(patterns)} visual patterns")
        
        element_types = set(elem.element_type for elem in elements)
        insights.append(f"Contains {len(element_types)} different element types")
        
        # Calculate confidence based on pattern recognition and completeness
        confidence = min(1.0, (len(patterns) * 0.3 + len(elements) * 0.1) / 2.0)
        
        return DiagramAnalysis(
            diagram_id=f"diagram_{self._generate_id()}",
            representation_type=representation_type,
            elements=elements,
            spatial_mapping=spatial_mapping,
            patterns_identified=patterns,
            key_insights=insights,
            interpretation=f"Diagram shows {representation_type.value} with {len(elements)} elements",
            confidence_score=confidence
        )
    
    def solve_visually(
        self,
        problem_description: str,
        visual_elements: List[VisualElement],
        representation_type: VisualRepresentationType
    ) -> VisualProblemSolving:
        """Apply visual reasoning to problem solving"""
        diagram_analysis = self.analyze_diagram(visual_elements, representation_type)
        
        # Generate solution steps based on visual analysis
        solution_steps = [
            "1. Analyze visual representation structure",
            "2. Identify key patterns and relationships",
            "3. Map problem elements to visual elements",
            "4. Apply spatial reasoning to solution path"
        ]
        
        # Identify visual aids used
        visual_aids = [representation_type.value]
        if diagram_analysis.patterns_identified:
            visual_aids.extend([pattern.pattern_type.value for pattern in diagram_analysis.patterns_identified])
        
        # Spatial reasoning techniques applied
        spatial_reasoning = ["spatial_relationship_analysis", "pattern_recognition"]
        if diagram_analysis.spatial_mapping.relationships:
            spatial_reasoning.append("relationship_mapping")
        
        return VisualProblemSolving(
            problem_id=f"visual_problem_{self._generate_id()}",
            problem_description=problem_description,
            visual_representation=diagram_analysis,
            solution_steps=solution_steps,
            visual_aids_used=visual_aids,
            spatial_reasoning_applied=spatial_reasoning,
            pattern_matching_used=diagram_analysis.patterns_identified,
            solution_confidence=diagram_analysis.confidence_score
        )