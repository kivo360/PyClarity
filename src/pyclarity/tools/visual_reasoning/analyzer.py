"""
Visual Reasoning Analyzer

Provides spatial and diagrammatic thinking capabilities including visual problem-solving,
pattern recognition, diagram analysis, and spatial relationship understanding.
"""

import asyncio
import time
import math
from typing import List, Dict, Any, Optional, Tuple
from collections import defaultdict

from .models import (
    VisualReasoningContext,
    VisualReasoningResult,
    VisualElement,
    SpatialMapping,
    PatternRecognition,
    DiagramAnalysis,
    VisualProblemSolving,
    VisualRepresentationType,
    SpatialRelationship,
    PatternType
)


class VisualReasoningAnalyzer:
    """
    Visual Reasoning Analyzer for spatial and diagrammatic thinking.
    
    Provides comprehensive visual analysis capabilities including:
    - Spatial relationship analysis
    - Visual pattern recognition  
    - Diagram interpretation
    - Visual problem-solving approaches
    """
    
    def __init__(self):
        """Initialize the Visual Reasoning Analyzer"""
        self.pattern_recognition_threshold = 0.6
        self.spatial_analysis_precision = 0.1
        self.max_relationship_distance = 100.0
    
    async def analyze(self, context: VisualReasoningContext) -> VisualReasoningResult:
        """
        Perform comprehensive visual reasoning analysis
        
        Args:
            context: Visual reasoning context with elements and analysis parameters
            
        Returns:
            VisualReasoningResult with complete analysis
        """
        start_time = time.time()
        
        # Phase 1: Process visual elements
        visual_elements = await self._process_visual_elements(context.visual_elements_data)
        
        # Phase 2: Spatial analysis if requested
        spatial_mapping = None
        spatial_relationships = {}
        if context.include_spatial_analysis:
            spatial_mapping = await self._create_spatial_mapping(
                visual_elements, context.coordinate_system
            )
            spatial_relationships = await self._analyze_spatial_relationships(visual_elements)
        
        # Phase 3: Pattern recognition if requested
        patterns_identified = []
        if context.include_pattern_recognition:
            patterns_identified = await self._recognize_visual_patterns(
                visual_elements, context.max_patterns, context.confidence_threshold
            )
        
        # Phase 4: Diagram analysis
        diagram_analysis = await self._analyze_diagram(
            visual_elements, context.representation_type, spatial_mapping, patterns_identified
        )
        
        # Phase 5: Visual problem solving if requested
        visual_problem_solving = None
        if context.include_problem_solving and context.problem_description:
            visual_problem_solving = await self._solve_visually(
                context.problem_description, visual_elements, 
                context.representation_type, diagram_analysis
            )
        
        # Phase 6: Generate insights and recommendations
        key_insights = await self._generate_insights(
            visual_elements, patterns_identified, spatial_relationships, diagram_analysis
        )
        
        recommendations = await self._generate_recommendations(
            context, visual_elements, patterns_identified, diagram_analysis
        )
        
        # Phase 7: Calculate confidence scores and metrics
        confidence_scores = await self._calculate_confidence_scores(
            visual_elements, patterns_identified, spatial_mapping, diagram_analysis
        )
        
        visual_reasoning_techniques = await self._identify_techniques_used(
            context, patterns_identified, spatial_mapping
        )
        
        processing_time = int((time.time() - start_time) * 1000)
        
        processing_metrics = {
            'elements_processed': len(visual_elements),
            'patterns_analyzed': len(patterns_identified),
            'spatial_relationships_found': sum(len(rels) for rels in spatial_relationships.values()),
            'analysis_depth': len(key_insights),
            'processing_phases': 7
        }
        
        return VisualReasoningResult(
            visual_elements=visual_elements,
            spatial_mapping=spatial_mapping,
            patterns_identified=patterns_identified,
            diagram_analysis=diagram_analysis,
            visual_problem_solving=visual_problem_solving,
            spatial_relationships=spatial_relationships,
            key_insights=key_insights,
            recommendations=recommendations,
            visual_reasoning_techniques=visual_reasoning_techniques,
            confidence_scores=confidence_scores,
            processing_metrics=processing_metrics,
            processing_time_ms=processing_time
        )
    
    async def _process_visual_elements(self, elements_data: List[Dict[str, Any]]) -> List[VisualElement]:
        """Process raw visual elements data into VisualElement objects"""
        visual_elements = []
        
        for elem_data in elements_data:
            # Calculate metadata
            x, y = elem_data['position']
            width, height = elem_data['size']
            
            metadata = {
                'area': width * height,
                'center': (x + width/2, y + width/2),
                'perimeter': 2 * (width + height),
                'aspect_ratio': width / height if height > 0 else 1.0,
                'bounds': {
                    'left': x,
                    'right': x + width,
                    'top': y,
                    'bottom': y + height
                }
            }
            
            element = VisualElement(
                element_id=elem_data['element_id'],
                element_type=elem_data['element_type'],
                position=tuple(elem_data['position']),
                size=tuple(elem_data['size']),
                properties=elem_data.get('properties', {}),
                relationships=elem_data.get('relationships', []),
                metadata=metadata
            )
            
            visual_elements.append(element)
        
        return visual_elements
    
    async def _create_spatial_mapping(
        self, 
        elements: List[VisualElement], 
        coordinate_system: str
    ) -> SpatialMapping:
        """Create spatial mapping of visual elements"""
        relationships = await self._analyze_spatial_relationships(elements)
        
        # Generate spatial constraints
        constraints = []
        for elem_id, rels in relationships.items():
            for rel in rels:
                constraints.append(f"{elem_id} has {rel} relationship")
        
        # Add boundary constraints
        if elements:
            min_x = min(elem.position[0] for elem in elements)
            max_x = max(elem.position[0] + elem.size[0] for elem in elements)
            min_y = min(elem.position[1] for elem in elements)
            max_y = max(elem.position[1] + elem.size[1] for elem in elements)
            
            constraints.extend([
                f"Bounding box: ({min_x}, {min_y}) to ({max_x}, {max_y})",
                f"Total area coverage: {(max_x - min_x) * (max_y - min_y)}"
            ])
        
        return SpatialMapping(
            elements=elements,
            relationships=relationships,
            spatial_constraints=constraints,
            coordinate_system=coordinate_system,
            scale_factor=1.0
        )
    
    async def _analyze_spatial_relationships(
        self, 
        elements: List[VisualElement]
    ) -> Dict[str, List[str]]:
        """Analyze spatial relationships between visual elements"""
        relationships = defaultdict(list)
        
        for i, elem1 in enumerate(elements):
            for j, elem2 in enumerate(elements):
                if i != j:
                    rel = await self._calculate_spatial_relationship(elem1, elem2)
                    if rel:
                        relationships[elem1.element_id].append(rel.value)
        
        return dict(relationships)
    
    async def _calculate_spatial_relationship(
        self, 
        elem1: VisualElement, 
        elem2: VisualElement
    ) -> Optional[SpatialRelationship]:
        """Calculate spatial relationship between two elements"""
        # Element 1 bounds
        x1, y1 = elem1.position
        w1, h1 = elem1.size
        left1, right1, top1, bottom1 = x1, x1 + w1, y1, y1 + h1
        
        # Element 2 bounds
        x2, y2 = elem2.position
        w2, h2 = elem2.size
        left2, right2, top2, bottom2 = x2, x2 + w2, y2, y2 + h2
        
        # Check for containment
        if (left1 >= left2 and right1 <= right2 and top1 >= top2 and bottom1 <= bottom2):
            return SpatialRelationship.INSIDE
        elif (left2 >= left1 and right2 <= right1 and top2 >= top1 and bottom2 <= bottom1):
            return SpatialRelationship.OUTSIDE
        
        # Check for directional relationships
        if right1 <= left2:
            return SpatialRelationship.LEFT_OF
        elif left1 >= right2:
            return SpatialRelationship.RIGHT_OF
        elif bottom1 <= top2:
            return SpatialRelationship.ABOVE
        elif top1 >= bottom2:
            return SpatialRelationship.BELOW
        
        # Check for adjacency
        overlap_x = max(0, min(right1, right2) - max(left1, left2))
        overlap_y = max(0, min(bottom1, bottom2) - max(top1, top2))
        
        if overlap_x > 0 or overlap_y > 0:
            return SpatialRelationship.ADJACENT
        
        # Check for proximity (within threshold)
        center1 = (x1 + w1/2, y1 + h1/2)
        center2 = (x2 + w2/2, y2 + h2/2)
        distance = math.sqrt((center1[0] - center2[0])**2 + (center1[1] - center2[1])**2)
        
        if distance <= self.max_relationship_distance:
            return SpatialRelationship.CONNECTED
        
        return None
    
    async def _recognize_visual_patterns(
        self, 
        elements: List[VisualElement], 
        max_patterns: int, 
        confidence_threshold: float
    ) -> List[PatternRecognition]:
        """Recognize patterns in visual elements"""
        patterns = []
        
        # Pattern detection methods
        pattern_detectors = [
            self._detect_symmetry_pattern,
            self._detect_repetition_pattern,
            self._detect_hierarchy_pattern,
            self._detect_circular_pattern,
            self._detect_linear_pattern,
            self._detect_branching_pattern
        ]
        
        for detector in pattern_detectors:
            if len(patterns) >= max_patterns:
                break
                
            pattern = await detector(elements)
            if pattern and pattern.confidence_level >= confidence_threshold:
                patterns.append(pattern)
        
        # Sort by confidence and return top patterns
        patterns.sort(key=lambda p: p.confidence_level, reverse=True)
        return patterns[:max_patterns]
    
    async def _detect_symmetry_pattern(self, elements: List[VisualElement]) -> Optional[PatternRecognition]:
        """Detect symmetrical patterns in elements"""
        if len(elements) < 2:
            return None
        
        # Calculate center of all elements
        center_x = sum(elem.position[0] + elem.size[0]/2 for elem in elements) / len(elements)
        center_y = sum(elem.position[1] + elem.size[1]/2 for elem in elements) / len(elements)
        
        symmetric_pairs = 0
        total_comparisons = 0
        
        for elem in elements:
            elem_center_x = elem.position[0] + elem.size[0]/2
            elem_center_y = elem.position[1] + elem.size[1]/2
            distance_from_center_x = abs(elem_center_x - center_x)
            distance_from_center_y = abs(elem_center_y - center_y)
            
            # Look for mirrored element
            for other_elem in elements:
                if elem != other_elem:
                    other_center_x = other_elem.position[0] + other_elem.size[0]/2
                    other_center_y = other_elem.position[1] + other_elem.size[1]/2
                    other_distance_x = abs(other_center_x - center_x)
                    other_distance_y = abs(other_center_y - center_y)
                    
                    # Check for symmetry in both axes
                    if (abs(distance_from_center_x - other_distance_x) < self.spatial_analysis_precision and
                        abs(distance_from_center_y - other_distance_y) < self.spatial_analysis_precision):
                        symmetric_pairs += 1
                        break
                
                total_comparisons += 1
        
        if total_comparisons == 0:
            return None
        
        confidence = symmetric_pairs / len(elements)
        
        if confidence >= self.pattern_recognition_threshold:
            return PatternRecognition(
                pattern_type=PatternType.SYMMETRICAL,
                confidence_level=confidence,
                pattern_elements=[elem.element_id for elem in elements],
                pattern_description=f"Symmetrical arrangement detected around center ({center_x:.1f}, {center_y:.1f})",
                pattern_rules=[
                    "Elements are mirrored around central axis",
                    f"Symmetry confidence: {confidence:.2f}"
                ],
                similarity_score=confidence,
                variations_detected=[]
            )
        
        return None
    
    async def _detect_repetition_pattern(self, elements: List[VisualElement]) -> Optional[PatternRecognition]:
        """Detect repetitive patterns in elements"""
        if len(elements) < 3:
            return None
        
        # Group elements by type and size
        type_groups = defaultdict(list)
        for elem in elements:
            key = f"{elem.element_type}_{elem.size[0]}x{elem.size[1]}"
            type_groups[key].append(elem)
        
        # Find the largest repeating group
        largest_group = max(type_groups.values(), key=len)
        
        if len(largest_group) >= 3:
            confidence = len(largest_group) / len(elements)
            
            return PatternRecognition(
                pattern_type=PatternType.REPETITIVE,
                confidence_level=confidence,
                pattern_elements=[elem.element_id for elem in largest_group],
                pattern_description=f"Repetitive pattern of {largest_group[0].element_type} elements",
                pattern_rules=[
                    f"Pattern repeats {len(largest_group)} times",
                    f"Element type: {largest_group[0].element_type}",
                    f"Element size: {largest_group[0].size}"
                ],
                similarity_score=confidence,
                variations_detected=[]
            )
        
        return None
    
    async def _detect_hierarchy_pattern(self, elements: List[VisualElement]) -> Optional[PatternRecognition]:
        """Detect hierarchical patterns based on size and position"""
        if len(elements) < 3:
            return None
        
        # Sort by size (area) and check if larger elements are positioned above smaller ones
        sorted_elements = sorted(elements, key=lambda e: e.size[0] * e.size[1], reverse=True)
        
        hierarchical_count = 0
        for i in range(len(sorted_elements) - 1):
            larger = sorted_elements[i]
            smaller = sorted_elements[i + 1]
            
            # Check if larger element is above (smaller y coordinate)
            if larger.position[1] <= smaller.position[1]:
                hierarchical_count += 1
        
        confidence = hierarchical_count / max(1, len(elements) - 1)
        
        if confidence >= self.pattern_recognition_threshold:
            return PatternRecognition(
                pattern_type=PatternType.HIERARCHICAL,
                confidence_level=confidence,
                pattern_elements=[elem.element_id for elem in sorted_elements],
                pattern_description="Hierarchical arrangement by size and vertical position",
                pattern_rules=[
                    "Larger elements positioned above smaller ones",
                    "Size-based hierarchy detected",
                    f"Hierarchy strength: {confidence:.2f}"
                ],
                similarity_score=confidence,
                variations_detected=[]
            )
        
        return None
    
    async def _detect_circular_pattern(self, elements: List[VisualElement]) -> Optional[PatternRecognition]:
        """Detect circular arrangement patterns"""
        if len(elements) < 4:
            return None
        
        # Calculate center point
        center_x = sum(elem.position[0] + elem.size[0]/2 for elem in elements) / len(elements)
        center_y = sum(elem.position[1] + elem.size[1]/2 for elem in elements) / len(elements)
        
        # Calculate distances from center
        distances = []
        for elem in elements:
            elem_center_x = elem.position[0] + elem.size[0]/2
            elem_center_y = elem.position[1] + elem.size[1]/2
            distance = math.sqrt((elem_center_x - center_x)**2 + (elem_center_y - center_y)**2)
            distances.append(distance)
        
        # Check if distances are roughly equal (circular arrangement)
        avg_distance = sum(distances) / len(distances)
        distance_variance = sum((d - avg_distance)**2 for d in distances) / len(distances)
        coefficient_of_variation = math.sqrt(distance_variance) / avg_distance if avg_distance > 0 else 1
        
        # Lower coefficient of variation indicates more circular arrangement
        confidence = max(0, 1 - coefficient_of_variation)
        
        if confidence >= self.pattern_recognition_threshold:
            return PatternRecognition(
                pattern_type=PatternType.CIRCULAR,
                confidence_level=confidence,
                pattern_elements=[elem.element_id for elem in elements],
                pattern_description=f"Circular arrangement around center ({center_x:.1f}, {center_y:.1f})",
                pattern_rules=[
                    f"Average radius: {avg_distance:.1f}",
                    f"Distance uniformity: {confidence:.2f}",
                    "Elements arranged in circular pattern"
                ],
                similarity_score=confidence,
                variations_detected=[]
            )
        
        return None
    
    async def _detect_linear_pattern(self, elements: List[VisualElement]) -> Optional[PatternRecognition]:
        """Detect linear arrangement patterns"""
        if len(elements) < 3:
            return None
        
        # Try to fit elements to a line using least squares
        centers = [(elem.position[0] + elem.size[0]/2, elem.position[1] + elem.size[1]/2) 
                  for elem in elements]
        
        # Calculate line of best fit
        n = len(centers)
        sum_x = sum(x for x, y in centers)
        sum_y = sum(y for x, y in centers)
        sum_xy = sum(x * y for x, y in centers)
        sum_x2 = sum(x * x for x, y in centers)
        
        # Calculate correlation coefficient
        if n * sum_x2 - sum_x * sum_x != 0:
            slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
            correlation = abs(slope) / (1 + abs(slope))  # Normalized correlation measure
            
            if correlation >= self.pattern_recognition_threshold:
                return PatternRecognition(
                    pattern_type=PatternType.LINEAR,
                    confidence_level=correlation,
                    pattern_elements=[elem.element_id for elem in elements],
                    pattern_description=f"Linear arrangement detected with slope {slope:.2f}",
                    pattern_rules=[
                        f"Line slope: {slope:.2f}",
                        f"Linear correlation: {correlation:.2f}",
                        "Elements arranged in linear pattern"
                    ],
                    similarity_score=correlation,
                    variations_detected=[]
                )
        
        return None
    
    async def _detect_branching_pattern(self, elements: List[VisualElement]) -> Optional[PatternRecognition]:
        """Detect branching patterns in element arrangement"""
        if len(elements) < 4:
            return None
        
        # Look for elements that could be connection points (hubs)
        connection_counts = defaultdict(int)
        
        for elem in elements:
            # Count how many other elements are close to this one
            elem_center = (elem.position[0] + elem.size[0]/2, elem.position[1] + elem.size[1]/2)
            
            for other_elem in elements:
                if elem != other_elem:
                    other_center = (other_elem.position[0] + other_elem.size[0]/2, 
                                  other_elem.position[1] + other_elem.size[1]/2)
                    distance = math.sqrt((elem_center[0] - other_center[0])**2 + 
                                       (elem_center[1] - other_center[1])**2)
                    
                    if distance <= self.max_relationship_distance:
                        connection_counts[elem.element_id] += 1
        
        # Find elements with multiple connections (potential branch points)
        branch_points = [elem_id for elem_id, count in connection_counts.items() if count >= 3]
        
        if branch_points:
            confidence = len(branch_points) / len(elements)
            
            return PatternRecognition(
                pattern_type=PatternType.BRANCHING,
                confidence_level=confidence,
                pattern_elements=branch_points,
                pattern_description=f"Branching pattern with {len(branch_points)} branch points",
                pattern_rules=[
                    f"Branch points: {len(branch_points)}",
                    f"Branching density: {confidence:.2f}",
                    "Tree-like or network structure detected"
                ],
                similarity_score=confidence,
                variations_detected=[]
            )
        
        return None
    
    async def _analyze_diagram(
        self, 
        elements: List[VisualElement],
        representation_type: VisualRepresentationType,
        spatial_mapping: Optional[SpatialMapping],
        patterns: List[PatternRecognition]
    ) -> DiagramAnalysis:
        """Analyze complete diagram structure"""
        # Generate key insights
        insights = []
        
        if patterns:
            insights.append(f"Identified {len(patterns)} visual patterns")
            pattern_types = [p.pattern_type.value for p in patterns]
            insights.append(f"Pattern types: {', '.join(set(pattern_types))}")
        
        element_types = set(elem.element_type for elem in elements)
        insights.append(f"Contains {len(element_types)} different element types: {', '.join(element_types)}")
        
        if spatial_mapping:
            total_relationships = sum(len(rels) for rels in spatial_mapping.relationships.values())
            insights.append(f"Found {total_relationships} spatial relationships")
        
        # Calculate total area coverage
        if elements:
            total_area = sum(elem.size[0] * elem.size[1] for elem in elements)
            insights.append(f"Total element area: {total_area:.1f} square units")
        
        # Generate interpretation
        interpretation = f"Diagram shows {representation_type.value} with {len(elements)} elements"
        if patterns:
            dominant_pattern = max(patterns, key=lambda p: p.confidence_level)
            interpretation += f", displaying primarily {dominant_pattern.pattern_type.value} patterns"
        
        # Calculate confidence based on pattern strength and completeness
        confidence = 0.5  # Base confidence
        if patterns:
            avg_pattern_confidence = sum(p.confidence_level for p in patterns) / len(patterns)
            confidence += avg_pattern_confidence * 0.3
        
        confidence += min(0.2, len(elements) * 0.02)  # Bonus for more elements
        confidence = min(1.0, confidence)
        
        return DiagramAnalysis(
            representation_type=representation_type,
            elements=elements,
            spatial_mapping=spatial_mapping or SpatialMapping(
                elements=elements,
                relationships={},
                spatial_constraints=[],
                coordinate_system="cartesian"
            ),
            patterns_identified=patterns,
            key_insights=insights,
            interpretation=interpretation,
            confidence_score=confidence
        )
    
    async def _solve_visually(
        self,
        problem_description: str,
        elements: List[VisualElement],
        representation_type: VisualRepresentationType,
        diagram_analysis: DiagramAnalysis
    ) -> VisualProblemSolving:
        """Apply visual reasoning to problem solving"""
        # Generate solution steps based on visual analysis
        solution_steps = [
            "1. Analyze visual representation structure and identify key elements",
            "2. Map problem constraints to spatial relationships",
            "3. Identify relevant visual patterns and their implications",
            "4. Apply spatial reasoning to explore solution paths",
            "5. Validate solution using visual verification methods"
        ]
        
        # Add problem-specific solution steps
        if "optimization" in problem_description.lower():
            solution_steps.append("6. Use visual analysis to identify optimization opportunities")
        elif "path" in problem_description.lower():
            solution_steps.append("6. Trace optimal paths through visual representation")
        elif "relationship" in problem_description.lower():
            solution_steps.append("6. Leverage spatial relationships for problem resolution")
        
        # Identify visual aids used
        visual_aids = [representation_type.value]
        if diagram_analysis.patterns_identified:
            pattern_types = [p.pattern_type.value for p in diagram_analysis.patterns_identified]
            visual_aids.extend(pattern_types)
        
        # Spatial reasoning techniques
        spatial_reasoning = ["spatial_relationship_analysis", "pattern_recognition"]
        if diagram_analysis.spatial_mapping.relationships:
            spatial_reasoning.append("relationship_mapping")
        if len(elements) > 10:
            spatial_reasoning.append("hierarchical_decomposition")
        
        # Calculate solution confidence
        solution_confidence = diagram_analysis.confidence_score * 0.8  # Slight discount for problem solving
        
        return VisualProblemSolving(
            problem_description=problem_description,
            visual_representation=diagram_analysis,
            solution_steps=solution_steps,
            visual_aids_used=visual_aids,
            spatial_reasoning_applied=spatial_reasoning,
            pattern_matching_used=diagram_analysis.patterns_identified,
            solution_confidence=solution_confidence
        )
    
    async def _generate_insights(
        self,
        elements: List[VisualElement],
        patterns: List[PatternRecognition],
        spatial_relationships: Dict[str, List[str]],
        diagram_analysis: DiagramAnalysis
    ) -> List[str]:
        """Generate key insights from visual analysis"""
        insights = []
        
        # Element distribution insights
        if elements:
            avg_area = sum(elem.size[0] * elem.size[1] for elem in elements) / len(elements)
            insights.append(f"Average element area: {avg_area:.1f} square units")
            
            element_types = [elem.element_type for elem in elements]
            most_common_type = max(set(element_types), key=element_types.count)
            insights.append(f"Most common element type: {most_common_type}")
        
        # Pattern insights
        if patterns:
            strongest_pattern = max(patterns, key=lambda p: p.confidence_level)
            insights.append(f"Strongest pattern: {strongest_pattern.pattern_type.value} "
                          f"(confidence: {strongest_pattern.confidence_level:.2f})")
            
            if len(patterns) > 1:
                insights.append(f"Multiple overlapping patterns detected: "
                              f"{len(patterns)} different pattern types")
        
        # Spatial relationship insights
        if spatial_relationships:
            total_relationships = sum(len(rels) for rels in spatial_relationships.values())
            insights.append(f"Spatial complexity: {total_relationships} relationships "
                          f"across {len(spatial_relationships)} elements")
            
            # Find most connected element
            most_connected = max(spatial_relationships.items(), key=lambda x: len(x[1]))
            insights.append(f"Most connected element: {most_connected[0]} "
                          f"({len(most_connected[1])} relationships)")
        
        # Layout insights
        if elements:
            positions = [elem.position for elem in elements]
            min_x = min(pos[0] for pos in positions)
            max_x = max(pos[0] + elem.size[0] for pos, elem in zip(positions, elements))
            min_y = min(pos[1] for pos in positions)
            max_y = max(pos[1] + elem.size[1] for pos, elem in zip(positions, elements))
            
            layout_width = max_x - min_x
            layout_height = max_y - min_y
            layout_ratio = layout_width / layout_height if layout_height > 0 else 1
            
            if layout_ratio > 2:
                insights.append("Layout orientation: Predominantly horizontal")
            elif layout_ratio < 0.5:
                insights.append("Layout orientation: Predominantly vertical")
            else:
                insights.append("Layout orientation: Balanced proportions")
        
        return insights[:15]  # Limit to max insights
    
    async def _generate_recommendations(
        self,
        context: VisualReasoningContext,
        elements: List[VisualElement],
        patterns: List[PatternRecognition],
        diagram_analysis: DiagramAnalysis
    ) -> List[str]:
        """Generate recommendations based on visual analysis"""
        recommendations = []
        
        # Pattern-based recommendations
        if patterns:
            for pattern in patterns:
                if pattern.pattern_type == PatternType.SYMMETRICAL:
                    recommendations.append("Leverage symmetrical layout for balanced design")
                elif pattern.pattern_type == PatternType.REPETITIVE:
                    recommendations.append("Consider template-based approach for repeated elements")
                elif pattern.pattern_type == PatternType.HIERARCHICAL:
                    recommendations.append("Utilize hierarchical structure for information organization")
                elif pattern.pattern_type == PatternType.CIRCULAR:
                    recommendations.append("Apply circular navigation or workflow patterns")
                elif pattern.pattern_type == PatternType.LINEAR:
                    recommendations.append("Consider sequential processing or pipeline approaches")
                elif pattern.pattern_type == PatternType.BRANCHING:
                    recommendations.append("Implement decision tree or network-based solutions")
        
        # Complexity-based recommendations
        if len(elements) > 20:
            recommendations.append("Consider grouping or clustering elements to reduce visual complexity")
        elif len(elements) < 5:
            recommendations.append("May benefit from additional visual elements for richer representation")
        
        # Spatial relationship recommendations
        spatial_rels = sum(len(rels) for rels in diagram_analysis.spatial_mapping.relationships.values())
        if spatial_rels > len(elements) * 3:
            recommendations.append("High spatial connectivity - consider simplifying relationships")
        elif spatial_rels < len(elements):
            recommendations.append("Low connectivity - consider adding relationship indicators")
        
        # Problem-solving recommendations
        if context.include_problem_solving:
            recommendations.append("Apply visual problem-solving techniques for complex scenarios")
            recommendations.append("Use spatial mapping to identify solution pathways")
        
        # Analysis improvement recommendations
        if context.confidence_threshold < 0.7:
            recommendations.append("Consider increasing confidence threshold for more reliable patterns")
        
        return recommendations[:12]  # Limit recommendations
    
    async def _calculate_confidence_scores(
        self,
        elements: List[VisualElement],
        patterns: List[PatternRecognition],
        spatial_mapping: Optional[SpatialMapping],
        diagram_analysis: DiagramAnalysis
    ) -> Dict[str, float]:
        """Calculate confidence scores for different analysis aspects"""
        scores = {}
        
        # Overall confidence
        base_confidence = 0.6
        if patterns:
            pattern_confidence = sum(p.confidence_level for p in patterns) / len(patterns)
            base_confidence += pattern_confidence * 0.3
        
        if spatial_mapping and spatial_mapping.relationships:
            relationship_strength = len(spatial_mapping.relationships) / len(elements)
            base_confidence += min(0.1, relationship_strength * 0.1)
        
        scores['overall'] = min(1.0, base_confidence)
        
        # Component-specific scores
        scores['element_processing'] = min(1.0, len(elements) / 10 * 0.5 + 0.5)
        scores['pattern_recognition'] = sum(p.confidence_level for p in patterns) / len(patterns) if patterns else 0.0
        scores['spatial_analysis'] = 0.8 if spatial_mapping and spatial_mapping.relationships else 0.3
        scores['diagram_analysis'] = diagram_analysis.confidence_score
        
        return scores
    
    async def _identify_techniques_used(
        self,
        context: VisualReasoningContext,
        patterns: List[PatternRecognition],
        spatial_mapping: Optional[SpatialMapping]
    ) -> List[str]:
        """Identify visual reasoning techniques used in analysis"""
        techniques = ["visual_element_processing"]
        
        if context.include_spatial_analysis:
            techniques.append("spatial_relationship_analysis")
        
        if context.include_pattern_recognition:
            techniques.append("pattern_recognition")
        
        if patterns:
            pattern_types = set(p.pattern_type.value for p in patterns)
            techniques.extend([f"{ptype}_pattern_detection" for ptype in pattern_types])
        
        if spatial_mapping and spatial_mapping.coordinate_system != "cartesian":
            techniques.append(f"{spatial_mapping.coordinate_system}_coordinate_analysis")
        
        if context.include_problem_solving:
            techniques.append("visual_problem_solving")
        
        techniques.append("diagram_interpretation")
        techniques.append("insight_generation")
        
        return techniques[:10]  # Limit techniques list