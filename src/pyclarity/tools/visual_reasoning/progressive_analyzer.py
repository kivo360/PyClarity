"""
Progressive Visual Reasoning Analyzer

Enables step-by-step visual analysis, diagram creation, and spatial reasoning
with session-based progression and visual element tracking.
"""

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from pyclarity.db.base import BaseSessionStore, SessionData
from pyclarity.db.visual_store import (
    BaseVisualStore,
    VisualData,
    VisualElement,
    SpatialRelationship,
    VisualPattern,
)
from pyclarity.tools.visual_reasoning.models import (
    VisualizationType,
    ElementType,
    RelationshipType,
    PatternType,
)


class ProgressiveVisualRequest(BaseModel):
    """Request for progressive visual reasoning."""
    
    session_id: Optional[str] = Field(None, description="Session ID for continuing analysis")
    step_number: int = Field(1, description="Current step in visual analysis")
    
    # Visual context
    problem_description: str = Field(..., description="Problem requiring visual reasoning")
    visualization_type: VisualizationType = Field(..., description="Type of visualization")
    domain: str = Field("general", description="Domain context")
    
    # Visual elements
    elements: List[Dict[str, Any]] = Field(default_factory=list, description="Visual elements to add")
    relationships: List[Dict[str, Any]] = Field(default_factory=list, description="Relationships between elements")
    
    # Analysis focus
    analysis_focus: str = Field(
        "structure",
        description="Focus: structure, patterns, relationships, flow, hierarchy"
    )
    
    # Modifications
    modifications: List[Dict[str, Any]] = Field(default_factory=list, description="Changes to existing elements")
    transformations: List[Dict[str, Any]] = Field(default_factory=list, description="Spatial transformations")
    
    # Previous work
    previous_visualizations: List[int] = Field(default_factory=list, description="Previous visualization IDs")
    build_on_previous: bool = Field(True, description="Build on previous visualizations")
    
    # Visual settings
    complexity_level: str = Field("moderate", description="Visual complexity level")
    include_annotations: bool = Field(True, description="Include helpful annotations")
    
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ProgressiveVisualResponse(BaseModel):
    """Response from progressive visual reasoning."""
    
    # Core response
    status: str = Field(..., description="Status of visual analysis")
    session_id: str = Field(..., description="Session identifier")
    visualization_id: int = Field(..., description="Database ID of this visualization")
    step_number: int = Field(..., description="Sequential step number")
    
    # Visualization summary
    visualization_type: str = Field(..., description="Type of visualization created")
    element_count: int = Field(0, description="Number of visual elements")
    relationship_count: int = Field(0, description="Number of relationships")
    
    # Visual structure
    structure_analysis: Dict[str, Any] = Field(default_factory=dict)
    spatial_organization: str = Field(..., description="How elements are organized")
    
    # Pattern detection
    patterns_detected: List[Dict[str, Any]] = Field(default_factory=list)
    symmetries: List[str] = Field(default_factory=list)
    groupings: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Relationships
    key_relationships: List[Dict[str, Any]] = Field(default_factory=list)
    hierarchy_levels: int = Field(0, description="Levels in hierarchy if applicable")
    
    # Insights
    visual_insights: List[str] = Field(default_factory=list)
    emergent_properties: List[str] = Field(default_factory=list)
    
    # Recommendations
    suggested_improvements: List[str] = Field(default_factory=list)
    alternative_visualizations: List[str] = Field(default_factory=list)
    next_steps: List[str] = Field(default_factory=list)
    
    # Visual description (for accessibility)
    textual_description: str = Field(..., description="Text description of visualization")
    
    # Error handling
    error: Optional[str] = Field(None)
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "session_id": "visual-123",
                "visualization_type": "concept_map",
                "element_count": 8,
                "patterns_detected": [{"type": "clustering", "description": "Related concepts grouped"}],
                "visual_insights": ["Central concept has most connections"]
            }
        }


class ProgressiveVisualAnalyzer:
    """Progressive visual reasoning with session management."""
    
    def __init__(
        self,
        session_store: BaseSessionStore,
        visual_store: BaseVisualStore,
    ):
        """Initialize with required stores."""
        self.session_store = session_store
        self.visual_store = visual_store
    
    async def analyze_visually(
        self, request: ProgressiveVisualRequest
    ) -> ProgressiveVisualResponse:
        """Process a visual reasoning step."""
        try:
            # Get or create session
            session = await self._get_or_create_session(request)
            
            # Process visual elements
            elements = self._process_elements(request.elements)
            relationships = self._process_relationships(request.relationships, elements)
            
            # Apply modifications if any
            if request.modifications and request.build_on_previous:
                elements, relationships = await self._apply_modifications(
                    session.session_id,
                    request.modifications,
                    elements,
                    relationships
                )
            
            # Analyze structure
            structure_analysis = self._analyze_structure(elements, relationships)
            spatial_org = self._determine_spatial_organization(
                request.visualization_type,
                elements,
                relationships
            )
            
            # Detect patterns
            patterns = self._detect_patterns(elements, relationships)
            symmetries = self._detect_symmetries(elements, relationships)
            groupings = self._identify_groupings(elements, relationships)
            
            # Analyze relationships
            key_rels = self._identify_key_relationships(relationships)
            hierarchy_levels = self._count_hierarchy_levels(elements, relationships)
            
            # Generate insights
            insights = self._generate_visual_insights(
                structure_analysis,
                patterns,
                key_rels
            )
            
            emergent = self._identify_emergent_properties(
                elements,
                relationships,
                patterns
            )
            
            # Create visualization data
            visual_data = await self._create_visual_data(
                session.session_id,
                request,
                elements,
                relationships,
                patterns
            )
            saved_data = await self.visual_store.save_visualization(visual_data)
            
            # Generate recommendations
            improvements = self._suggest_improvements(
                request.visualization_type,
                structure_analysis,
                patterns
            )
            
            alternatives = self._suggest_alternative_visualizations(
                request.problem_description,
                elements,
                relationships
            )
            
            next_steps = self._suggest_next_steps(
                request.analysis_focus,
                insights,
                patterns
            )
            
            # Generate textual description
            description = self._generate_textual_description(
                request.visualization_type,
                elements,
                relationships,
                insights
            )
            
            return ProgressiveVisualResponse(
                status="success",
                session_id=session.session_id,
                visualization_id=saved_data.id,
                step_number=saved_data.step_number,
                visualization_type=request.visualization_type.value,
                element_count=len(elements),
                relationship_count=len(relationships),
                structure_analysis=structure_analysis,
                spatial_organization=spatial_org,
                patterns_detected=[self._pattern_to_dict(p) for p in patterns],
                symmetries=symmetries,
                groupings=groupings,
                key_relationships=key_rels,
                hierarchy_levels=hierarchy_levels,
                visual_insights=insights,
                emergent_properties=emergent,
                suggested_improvements=improvements,
                alternative_visualizations=alternatives,
                next_steps=next_steps,
                textual_description=description,
            )
            
        except Exception as e:
            return ProgressiveVisualResponse(
                status="error",
                session_id=request.session_id or str(uuid.uuid4()),
                visualization_id=0,
                step_number=request.step_number,
                visualization_type=request.visualization_type.value,
                spatial_organization="unknown",
                textual_description="Error in visual analysis",
                error=str(e),
            )
    
    async def _get_or_create_session(
        self, request: ProgressiveVisualRequest
    ) -> SessionData:
        """Get existing session or create new one."""
        if request.session_id:
            session = await self.session_store.get_session(request.session_id)
            if session:
                return session
        
        # Create new session
        session_data = SessionData(
            session_id=request.session_id or str(uuid.uuid4()),
            tool_name="Visual Reasoning",
            created_at=datetime.now(timezone.utc),
            metadata={
                "problem_description": request.problem_description,
                "visualization_type": request.visualization_type.value,
                "domain": request.domain,
            }
        )
        
        return await self.session_store.create_session(session_data)
    
    def _process_elements(self, element_dicts: List[Dict[str, Any]]) -> List[VisualElement]:
        """Process element dictionaries into VisualElement objects."""
        elements = []
        
        for i, elem_dict in enumerate(element_dicts):
            element = VisualElement(
                element_id=elem_dict.get("id", f"elem_{i}"),
                element_type=ElementType(elem_dict.get("type", "node")),
                label=elem_dict.get("label", f"Element {i}"),
                position=elem_dict.get("position", {"x": i * 100, "y": 0}),
                size=elem_dict.get("size", {"width": 50, "height": 50}),
                style=elem_dict.get("style", {}),
                properties=elem_dict.get("properties", {}),
            )
            elements.append(element)
        
        return elements
    
    def _process_relationships(
        self,
        rel_dicts: List[Dict[str, Any]],
        elements: List[VisualElement]
    ) -> List[SpatialRelationship]:
        """Process relationship dictionaries into SpatialRelationship objects."""
        relationships = []
        element_ids = {e.element_id for e in elements}
        
        for i, rel_dict in enumerate(rel_dicts):
            source = rel_dict.get("source", "")
            target = rel_dict.get("target", "")
            
            # Validate elements exist
            if source in element_ids and target in element_ids:
                relationship = SpatialRelationship(
                    source_id=source,
                    target_id=target,
                    relationship_type=RelationshipType(rel_dict.get("type", "connected_to")),
                    label=rel_dict.get("label", ""),
                    strength=rel_dict.get("strength", 1.0),
                    properties=rel_dict.get("properties", {}),
                )
                relationships.append(relationship)
        
        return relationships
    
    async def _apply_modifications(
        self,
        session_id: str,
        modifications: List[Dict[str, Any]],
        elements: List[VisualElement],
        relationships: List[SpatialRelationship]
    ) -> tuple[List[VisualElement], List[SpatialRelationship]]:
        """Apply modifications to existing visualization."""
        # Get previous visualizations if building on them
        if modifications:
            # Apply each modification
            for mod in modifications:
                mod_type = mod.get("type", "")
                
                if mod_type == "move":
                    element_id = mod.get("element_id")
                    new_position = mod.get("position")
                    for elem in elements:
                        if elem.element_id == element_id:
                            elem.position = new_position
                
                elif mod_type == "resize":
                    element_id = mod.get("element_id")
                    new_size = mod.get("size")
                    for elem in elements:
                        if elem.element_id == element_id:
                            elem.size = new_size
                
                elif mod_type == "restyle":
                    element_id = mod.get("element_id")
                    new_style = mod.get("style")
                    for elem in elements:
                        if elem.element_id == element_id:
                            elem.style.update(new_style)
                
                elif mod_type == "remove":
                    element_id = mod.get("element_id")
                    elements = [e for e in elements if e.element_id != element_id]
                    relationships = [
                        r for r in relationships
                        if r.source_id != element_id and r.target_id != element_id
                    ]
        
        return elements, relationships
    
    def _analyze_structure(
        self,
        elements: List[VisualElement],
        relationships: List[SpatialRelationship]
    ) -> Dict[str, Any]:
        """Analyze the overall structure of the visualization."""
        structure = {
            "density": len(relationships) / max(1, len(elements)),
            "connectivity": self._calculate_connectivity(elements, relationships),
            "centrality": self._identify_central_elements(elements, relationships),
            "clusters": self._identify_clusters(elements, relationships),
            "isolated_elements": self._find_isolated_elements(elements, relationships),
        }
        
        return structure
    
    def _determine_spatial_organization(
        self,
        viz_type: VisualizationType,
        elements: List[VisualElement],
        relationships: List[SpatialRelationship]
    ) -> str:
        """Determine how elements are spatially organized."""
        if not elements:
            return "empty"
        
        # Check positions
        positions = [e.position for e in elements]
        x_coords = [p.get("x", 0) for p in positions]
        y_coords = [p.get("y", 0) for p in positions]
        
        # Determine organization pattern
        if viz_type == VisualizationType.HIERARCHY:
            return "hierarchical"
        elif viz_type == VisualizationType.NETWORK:
            return "network"
        elif viz_type == VisualizationType.FLOWCHART:
            return "flow-based"
        elif viz_type == VisualizationType.MIND_MAP:
            return "radial"
        
        # Infer from positions
        x_variance = max(x_coords) - min(x_coords) if x_coords else 0
        y_variance = max(y_coords) - min(y_coords) if y_coords else 0
        
        if x_variance > y_variance * 2:
            return "horizontal"
        elif y_variance > x_variance * 2:
            return "vertical"
        elif len(set(x_coords)) == 1:
            return "vertical-aligned"
        elif len(set(y_coords)) == 1:
            return "horizontal-aligned"
        else:
            return "scattered"
    
    def _detect_patterns(
        self,
        elements: List[VisualElement],
        relationships: List[SpatialRelationship]
    ) -> List[VisualPattern]:
        """Detect visual patterns in the layout."""
        patterns = []
        
        # Clustering pattern
        clusters = self._identify_clusters(elements, relationships)
        if len(clusters) > 1:
            patterns.append(VisualPattern(
                pattern_type=PatternType.CLUSTERING,
                description=f"Elements form {len(clusters)} distinct clusters",
                elements_involved=[e for cluster in clusters for e in cluster],
                confidence=0.8,
            ))
        
        # Hierarchy pattern
        if self._has_hierarchy_pattern(elements, relationships):
            patterns.append(VisualPattern(
                pattern_type=PatternType.HIERARCHY,
                description="Elements arranged in hierarchical structure",
                elements_involved=[e.element_id for e in elements],
                confidence=0.9,
            ))
        
        # Symmetry pattern
        if self._has_symmetry_pattern(elements):
            patterns.append(VisualPattern(
                pattern_type=PatternType.SYMMETRY,
                description="Layout exhibits symmetrical properties",
                elements_involved=[e.element_id for e in elements],
                confidence=0.7,
            ))
        
        # Flow pattern
        if self._has_flow_pattern(relationships):
            patterns.append(VisualPattern(
                pattern_type=PatternType.FLOW,
                description="Clear directional flow in relationships",
                elements_involved=list(set(
                    [r.source_id for r in relationships] +
                    [r.target_id for r in relationships]
                )),
                confidence=0.85,
            ))
        
        return patterns
    
    def _detect_symmetries(
        self,
        elements: List[VisualElement],
        relationships: List[SpatialRelationship]
    ) -> List[str]:
        """Detect symmetrical properties."""
        symmetries = []
        
        if not elements:
            return symmetries
        
        # Check vertical symmetry
        positions = [e.position for e in elements]
        x_coords = [p.get("x", 0) for p in positions]
        
        if x_coords:
            center_x = sum(x_coords) / len(x_coords)
            left_elements = [e for e in elements if e.position.get("x", 0) < center_x]
            right_elements = [e for e in elements if e.position.get("x", 0) > center_x]
            
            if abs(len(left_elements) - len(right_elements)) <= 1:
                symmetries.append("Approximate vertical symmetry")
        
        # Check horizontal symmetry
        y_coords = [p.get("y", 0) for p in positions]
        
        if y_coords:
            center_y = sum(y_coords) / len(y_coords)
            top_elements = [e for e in elements if e.position.get("y", 0) < center_y]
            bottom_elements = [e for e in elements if e.position.get("y", 0) > center_y]
            
            if abs(len(top_elements) - len(bottom_elements)) <= 1:
                symmetries.append("Approximate horizontal symmetry")
        
        # Check radial symmetry
        if self._has_radial_symmetry(elements):
            symmetries.append("Radial symmetry around center")
        
        return symmetries
    
    def _identify_groupings(
        self,
        elements: List[VisualElement],
        relationships: List[SpatialRelationship]
    ) -> List[Dict[str, Any]]:
        """Identify logical groupings of elements."""
        groupings = []
        
        # Group by element type
        type_groups = {}
        for elem in elements:
            elem_type = elem.element_type.value
            if elem_type not in type_groups:
                type_groups[elem_type] = []
            type_groups[elem_type].append(elem.element_id)
        
        for elem_type, elem_ids in type_groups.items():
            if len(elem_ids) > 1:
                groupings.append({
                    "type": "by_element_type",
                    "name": f"{elem_type} elements",
                    "elements": elem_ids,
                    "size": len(elem_ids),
                })
        
        # Group by connectivity
        clusters = self._identify_clusters(elements, relationships)
        for i, cluster in enumerate(clusters):
            if len(cluster) > 1:
                groupings.append({
                    "type": "by_connectivity",
                    "name": f"Connected group {i+1}",
                    "elements": cluster,
                    "size": len(cluster),
                })
        
        return groupings
    
    def _identify_key_relationships(
        self, relationships: List[SpatialRelationship]
    ) -> List[Dict[str, Any]]:
        """Identify the most important relationships."""
        key_rels = []
        
        # Count connections per element
        connection_counts = {}
        for rel in relationships:
            connection_counts[rel.source_id] = connection_counts.get(rel.source_id, 0) + 1
            connection_counts[rel.target_id] = connection_counts.get(rel.target_id, 0) + 1
        
        # Find hub elements
        if connection_counts:
            max_connections = max(connection_counts.values())
            hubs = [elem_id for elem_id, count in connection_counts.items() if count == max_connections]
            
            # Key relationships involve hubs
            for rel in relationships:
                if rel.source_id in hubs or rel.target_id in hubs:
                    key_rels.append({
                        "source": rel.source_id,
                        "target": rel.target_id,
                        "type": rel.relationship_type.value,
                        "importance": "high",
                        "reason": "Involves hub element",
                    })
        
        # Limit to top 5
        return key_rels[:5]
    
    def _count_hierarchy_levels(
        self,
        elements: List[VisualElement],
        relationships: List[SpatialRelationship]
    ) -> int:
        """Count levels in hierarchical structure."""
        if not elements or not relationships:
            return 0
        
        # Build parent-child relationships
        children = {}
        for rel in relationships:
            if rel.relationship_type in [RelationshipType.PARENT_OF, RelationshipType.ABOVE]:
                if rel.source_id not in children:
                    children[rel.source_id] = []
                children[rel.source_id].append(rel.target_id)
        
        if not children:
            return 1  # Flat structure
        
        # Find roots (elements with no parents)
        all_children = set()
        for child_list in children.values():
            all_children.update(child_list)
        
        roots = []
        for elem in elements:
            if elem.element_id not in all_children:
                roots.append(elem.element_id)
        
        if not roots:
            return 1  # No clear hierarchy
        
        # Count depth
        def count_depth(node_id: str, depth: int = 1) -> int:
            if node_id not in children:
                return depth
            
            max_child_depth = depth
            for child in children[node_id]:
                child_depth = count_depth(child, depth + 1)
                max_child_depth = max(max_child_depth, child_depth)
            
            return max_child_depth
        
        max_depth = 0
        for root in roots:
            depth = count_depth(root)
            max_depth = max(max_depth, depth)
        
        return max_depth
    
    def _generate_visual_insights(
        self,
        structure: Dict[str, Any],
        patterns: List[VisualPattern],
        key_relationships: List[Dict[str, Any]]
    ) -> List[str]:
        """Generate insights from visual analysis."""
        insights = []
        
        # Structure insights
        if structure["density"] > 1.5:
            insights.append("High connectivity suggests strong interdependencies")
        elif structure["density"] < 0.5:
            insights.append("Sparse connections indicate loosely coupled elements")
        
        if structure["centrality"]:
            central = structure["centrality"][0]
            insights.append(f"'{central}' appears to be the central/focal element")
        
        if structure["isolated_elements"]:
            count = len(structure["isolated_elements"])
            insights.append(f"{count} isolated element(s) may need integration")
        
        # Pattern insights
        for pattern in patterns:
            if pattern.pattern_type == PatternType.CLUSTERING:
                insights.append("Natural groupings suggest modular organization")
            elif pattern.pattern_type == PatternType.HIERARCHY:
                insights.append("Hierarchical structure indicates clear levels of abstraction")
            elif pattern.pattern_type == PatternType.FLOW:
                insights.append("Directional flow shows process or data movement")
        
        # Relationship insights
        if len(key_relationships) > 3:
            insights.append("Multiple key relationships create complex interactions")
        
        return insights[:5]  # Top 5 insights
    
    def _identify_emergent_properties(
        self,
        elements: List[VisualElement],
        relationships: List[SpatialRelationship],
        patterns: List[VisualPattern]
    ) -> List[str]:
        """Identify properties that emerge from the whole visualization."""
        properties = []
        
        # Check for network effects
        if len(relationships) > len(elements) * 1.5:
            properties.append("Network effect: relationships dominate structure")
        
        # Check for hierarchy emergence
        hierarchy_pattern = next((p for p in patterns if p.pattern_type == PatternType.HIERARCHY), None)
        if hierarchy_pattern and len(elements) > 5:
            properties.append("Clear organizational hierarchy emerges")
        
        # Check for system boundaries
        clusters = self._identify_clusters(elements, relationships)
        if len(clusters) > 1:
            properties.append(f"System naturally divides into {len(clusters)} subsystems")
        
        # Check for feedback loops
        if self._has_cycles(relationships):
            properties.append("Feedback loops present in the system")
        
        return properties
    
    async def _create_visual_data(
        self,
        session_id: str,
        request: ProgressiveVisualRequest,
        elements: List[VisualElement],
        relationships: List[SpatialRelationship],
        patterns: List[VisualPattern]
    ) -> VisualData:
        """Create visual data for storage."""
        return VisualData(
            session_id=session_id,
            step_number=request.step_number,
            visualization_type=request.visualization_type,
            problem_description=request.problem_description,
            elements=elements,
            relationships=relationships,
            patterns=patterns,
            layout_algorithm="manual",  # Would be determined by viz type
            visual_insights=self._generate_visual_insights(
                self._analyze_structure(elements, relationships),
                patterns,
                self._identify_key_relationships(relationships)
            ),
            metadata=request.metadata,
            created_at=datetime.now(timezone.utc),
        )
    
    def _suggest_improvements(
        self,
        viz_type: VisualizationType,
        structure: Dict[str, Any],
        patterns: List[VisualPattern]
    ) -> List[str]:
        """Suggest improvements to the visualization."""
        improvements = []
        
        # Structure-based improvements
        if structure["density"] > 2:
            improvements.append("Consider hierarchical grouping to reduce visual complexity")
        
        if structure["isolated_elements"]:
            improvements.append("Connect or annotate isolated elements for clarity")
        
        # Type-specific improvements
        if viz_type == VisualizationType.MIND_MAP and not any(p.pattern_type == PatternType.RADIAL for p in patterns):
            improvements.append("Consider radial layout for better mind map organization")
        
        if viz_type == VisualizationType.FLOWCHART and not any(p.pattern_type == PatternType.FLOW for p in patterns):
            improvements.append("Establish clearer directional flow")
        
        # General improvements
        if len(structure.get("clusters", [])) > 4:
            improvements.append("Use color or spacing to better distinguish groups")
        
        return improvements[:3]
    
    def _suggest_alternative_visualizations(
        self,
        problem: str,
        elements: List[VisualElement],
        relationships: List[SpatialRelationship]
    ) -> List[str]:
        """Suggest alternative visualization types."""
        alternatives = []
        
        # Based on structure
        if len(relationships) > len(elements) * 2:
            alternatives.append("Network diagram for complex relationships")
        
        if self._has_hierarchy_pattern(elements, relationships):
            alternatives.append("Tree diagram for hierarchical data")
        
        # Based on problem type
        problem_lower = problem.lower()
        if "process" in problem_lower or "flow" in problem_lower:
            alternatives.append("Flowchart for process visualization")
        
        if "compare" in problem_lower or "contrast" in problem_lower:
            alternatives.append("Venn diagram for comparisons")
        
        if "time" in problem_lower or "sequence" in problem_lower:
            alternatives.append("Timeline for temporal relationships")
        
        return alternatives[:3]
    
    def _suggest_next_steps(
        self,
        focus: str,
        insights: List[str],
        patterns: List[VisualPattern]
    ) -> List[str]:
        """Suggest next steps in visual analysis."""
        steps = []
        
        focus_steps = {
            "structure": [
                "Analyze individual clusters in detail",
                "Optimize layout for clarity",
                "Add hierarchical levels if needed"
            ],
            "patterns": [
                "Investigate pattern anomalies",
                "Strengthen emerging patterns",
                "Look for hidden patterns"
            ],
            "relationships": [
                "Analyze relationship strengths",
                "Identify missing connections",
                "Simplify redundant relationships"
            ],
            "flow": [
                "Trace critical paths",
                "Identify bottlenecks",
                "Optimize flow direction"
            ],
            "hierarchy": [
                "Balance hierarchy levels",
                "Clarify parent-child relationships",
                "Add intermediate levels if needed"
            ],
        }
        
        if focus in focus_steps:
            steps.extend(focus_steps[focus][:2])
        
        # Add pattern-specific steps
        for pattern in patterns[:1]:  # Just the primary pattern
            if pattern.pattern_type == PatternType.CLUSTERING:
                steps.append("Define cluster boundaries more clearly")
            elif pattern.pattern_type == PatternType.FLOW:
                steps.append("Annotate flow direction and decision points")
        
        return steps[:3]
    
    def _generate_textual_description(
        self,
        viz_type: VisualizationType,
        elements: List[VisualElement],
        relationships: List[SpatialRelationship],
        insights: List[str]
    ) -> str:
        """Generate accessible text description of visualization."""
        parts = []
        
        # Overall description
        parts.append(f"A {viz_type.value} visualization containing {len(elements)} elements")
        
        if relationships:
            parts.append(f"connected by {len(relationships)} relationships")
        
        # Element types
        element_types = {}
        for elem in elements:
            elem_type = elem.element_type.value
            element_types[elem_type] = element_types.get(elem_type, 0) + 1
        
        if element_types:
            type_desc = ", ".join([f"{count} {etype}(s)" for etype, count in element_types.items()])
            parts.append(f"including {type_desc}")
        
        # Key insight
        if insights:
            parts.append(f"Key insight: {insights[0]}")
        
        return ". ".join(parts) + "."
    
    # Helper methods
    
    def _calculate_connectivity(
        self,
        elements: List[VisualElement],
        relationships: List[SpatialRelationship]
    ) -> float:
        """Calculate average connectivity of elements."""
        if not elements:
            return 0.0
        
        connections = {}
        for rel in relationships:
            connections[rel.source_id] = connections.get(rel.source_id, 0) + 1
            connections[rel.target_id] = connections.get(rel.target_id, 0) + 1
        
        total_connections = sum(connections.values())
        return total_connections / (2 * len(elements))  # Divide by 2 since we count each edge twice
    
    def _identify_central_elements(
        self,
        elements: List[VisualElement],
        relationships: List[SpatialRelationship]
    ) -> List[str]:
        """Identify most central/connected elements."""
        connections = {}
        
        for rel in relationships:
            connections[rel.source_id] = connections.get(rel.source_id, 0) + 1
            connections[rel.target_id] = connections.get(rel.target_id, 0) + 1
        
        if not connections:
            return []
        
        # Sort by connection count
        sorted_elements = sorted(connections.items(), key=lambda x: x[1], reverse=True)
        
        # Return top 3 most connected
        return [elem_id for elem_id, _ in sorted_elements[:3]]
    
    def _identify_clusters(
        self,
        elements: List[VisualElement],
        relationships: List[SpatialRelationship]
    ) -> List[List[str]]:
        """Identify connected clusters of elements."""
        if not elements:
            return []
        
        # Build adjacency list
        adjacency = {}
        for elem in elements:
            adjacency[elem.element_id] = set()
        
        for rel in relationships:
            if rel.source_id in adjacency:
                adjacency[rel.source_id].add(rel.target_id)
            if rel.target_id in adjacency:
                adjacency[rel.target_id].add(rel.source_id)
        
        # Find connected components
        visited = set()
        clusters = []
        
        def dfs(node: str, cluster: List[str]):
            visited.add(node)
            cluster.append(node)
            for neighbor in adjacency.get(node, set()):
                if neighbor not in visited:
                    dfs(neighbor, cluster)
        
        for elem in elements:
            if elem.element_id not in visited:
                cluster = []
                dfs(elem.element_id, cluster)
                clusters.append(cluster)
        
        return clusters
    
    def _find_isolated_elements(
        self,
        elements: List[VisualElement],
        relationships: List[SpatialRelationship]
    ) -> List[str]:
        """Find elements with no connections."""
        connected = set()
        
        for rel in relationships:
            connected.add(rel.source_id)
            connected.add(rel.target_id)
        
        isolated = []
        for elem in elements:
            if elem.element_id not in connected:
                isolated.append(elem.element_id)
        
        return isolated
    
    def _has_hierarchy_pattern(
        self,
        elements: List[VisualElement],
        relationships: List[SpatialRelationship]
    ) -> bool:
        """Check if elements form a hierarchical pattern."""
        # Check for parent-child relationships
        hierarchy_types = {RelationshipType.PARENT_OF, RelationshipType.ABOVE}
        hierarchy_rels = [r for r in relationships if r.relationship_type in hierarchy_types]
        
        # Need at least some hierarchical relationships
        return len(hierarchy_rels) >= len(elements) * 0.3
    
    def _has_symmetry_pattern(self, elements: List[VisualElement]) -> bool:
        """Check if layout has symmetrical properties."""
        if len(elements) < 4:
            return False
        
        # Check position distribution
        positions = [e.position for e in elements]
        x_coords = [p.get("x", 0) for p in positions]
        y_coords = [p.get("y", 0) for p in positions]
        
        if not x_coords or not y_coords:
            return False
        
        # Calculate center
        center_x = sum(x_coords) / len(x_coords)
        center_y = sum(y_coords) / len(y_coords)
        
        # Check distribution around center
        quadrants = {"tl": 0, "tr": 0, "bl": 0, "br": 0}
        
        for x, y in zip(x_coords, y_coords):
            if x < center_x and y < center_y:
                quadrants["tl"] += 1
            elif x >= center_x and y < center_y:
                quadrants["tr"] += 1
            elif x < center_x and y >= center_y:
                quadrants["bl"] += 1
            else:
                quadrants["br"] += 1
        
        # Check if reasonably balanced
        counts = list(quadrants.values())
        max_diff = max(counts) - min(counts)
        
        return max_diff <= 2  # Allow small imbalance
    
    def _has_flow_pattern(self, relationships: List[SpatialRelationship]) -> bool:
        """Check if relationships show directional flow."""
        if not relationships:
            return False
        
        # Count directional relationships
        directional_types = {
            RelationshipType.FLOWS_TO,
            RelationshipType.LEADS_TO,
            RelationshipType.ABOVE,
            RelationshipType.BEFORE,
        }
        
        directional_count = sum(1 for r in relationships if r.relationship_type in directional_types)
        
        return directional_count >= len(relationships) * 0.5
    
    def _has_radial_symmetry(self, elements: List[VisualElement]) -> bool:
        """Check for radial symmetry pattern."""
        if len(elements) < 5:
            return False
        
        positions = [e.position for e in elements]
        x_coords = [p.get("x", 0) for p in positions]
        y_coords = [p.get("y", 0) for p in positions]
        
        if not x_coords or not y_coords:
            return False
        
        # Calculate center
        center_x = sum(x_coords) / len(x_coords)
        center_y = sum(y_coords) / len(y_coords)
        
        # Calculate distances from center
        distances = []
        for x, y in zip(x_coords, y_coords):
            dist = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
            distances.append(dist)
        
        # Check if distances are similar (within 20%)
        if not distances:
            return False
        
        avg_dist = sum(distances) / len(distances)
        variance = sum((d - avg_dist) ** 2 for d in distances) / len(distances)
        std_dev = variance ** 0.5
        
        return std_dev / avg_dist < 0.2 if avg_dist > 0 else False
    
    def _has_cycles(self, relationships: List[SpatialRelationship]) -> bool:
        """Check if relationships contain cycles."""
        # Build directed graph
        graph = {}
        for rel in relationships:
            if rel.source_id not in graph:
                graph[rel.source_id] = []
            graph[rel.source_id].append(rel.target_id)
        
        # DFS to detect cycles
        visited = set()
        rec_stack = set()
        
        def has_cycle(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    if has_cycle(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            
            rec_stack.remove(node)
            return False
        
        for node in graph:
            if node not in visited:
                if has_cycle(node):
                    return True
        
        return False
    
    def _pattern_to_dict(self, pattern: VisualPattern) -> Dict[str, Any]:
        """Convert pattern to dictionary."""
        return {
            "type": pattern.pattern_type.value,
            "description": pattern.description,
            "confidence": pattern.confidence,
            "element_count": len(pattern.elements_involved),
        }