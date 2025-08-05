"""
Progressive Systems Thinking Analyzer

Enables systematic analysis of complex systems, feedback loops, and emergent properties
with session-based progression and system evolution tracking.
"""

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from pyclarity.db.base import BaseSessionStore, SessionData
from pyclarity.db.systems_store import (
    BaseSystemsStore,
    SystemsData,
    SystemComponent,
    SystemRelationship,
    FeedbackLoop,
    EmergentProperty,
)
from pyclarity.tools.systems_thinking.models import (
    SystemType,
    ComponentType,
    RelationshipNature,
    LoopType,
    SystemHealth,
)


class ProgressiveSystemsRequest(BaseModel):
    """Request for progressive systems thinking."""
    
    session_id: Optional[str] = Field(None, description="Session ID for continuing analysis")
    step_number: int = Field(1, description="Current step in systems analysis")
    
    # System context
    system_description: str = Field(..., description="System being analyzed")
    system_type: SystemType = Field(..., description="Type of system")
    domain: str = Field("general", description="Domain context")
    
    # System elements
    components: List[Dict[str, Any]] = Field(default_factory=list, description="System components")
    relationships: List[Dict[str, Any]] = Field(default_factory=list, description="Component relationships")
    
    # Analysis focus
    analysis_focus: str = Field(
        "structure",
        description="Focus: structure, dynamics, feedback, boundaries, emergence"
    )
    
    # System modifications
    add_components: List[Dict[str, Any]] = Field(default_factory=list, description="Components to add")
    modify_relationships: List[Dict[str, Any]] = Field(default_factory=list, description="Relationships to modify")
    
    # Previous analysis
    previous_analyses: List[int] = Field(default_factory=list, description="Previous analysis IDs")
    build_on_previous: bool = Field(True, description="Build on previous analyses")
    
    # Analysis settings
    identify_feedback_loops: bool = Field(True, description="Identify feedback loops")
    analyze_boundaries: bool = Field(True, description="Analyze system boundaries")
    predict_behavior: bool = Field(True, description="Predict system behavior")
    
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ProgressiveSystemsResponse(BaseModel):
    """Response from progressive systems thinking."""
    
    # Core response
    status: str = Field(..., description="Status of systems analysis")
    session_id: str = Field(..., description="Session identifier")
    analysis_id: int = Field(..., description="Database ID of this analysis")
    step_number: int = Field(..., description="Sequential step number")
    
    # System overview
    component_count: int = Field(0, description="Number of components")
    relationship_count: int = Field(0, description="Number of relationships")
    system_complexity: float = Field(0.0, description="Complexity score")
    
    # Structure analysis
    key_components: List[Dict[str, Any]] = Field(default_factory=list)
    subsystems: List[Dict[str, Any]] = Field(default_factory=list)
    boundaries: Dict[str, Any] = Field(default_factory=dict)
    
    # Dynamics analysis
    feedback_loops: List[Dict[str, Any]] = Field(default_factory=list)
    balancing_loops: int = Field(0, description="Number of balancing loops")
    reinforcing_loops: int = Field(0, description="Number of reinforcing loops")
    
    # Emergent properties
    emergent_properties: List[Dict[str, Any]] = Field(default_factory=list)
    system_behaviors: List[str] = Field(default_factory=list)
    
    # System health
    health_assessment: Dict[str, Any] = Field(default_factory=dict)
    bottlenecks: List[str] = Field(default_factory=list)
    vulnerabilities: List[str] = Field(default_factory=list)
    
    # Predictions
    behavior_predictions: List[str] = Field(default_factory=list)
    intervention_points: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Recommendations
    optimization_suggestions: List[str] = Field(default_factory=list)
    next_analysis_steps: List[str] = Field(default_factory=list)
    
    # Error handling
    error: Optional[str] = Field(None)
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "session_id": "systems-123",
                "component_count": 12,
                "system_complexity": 0.75,
                "feedback_loops": [{"type": "balancing", "components": ["A", "B", "C"]}],
                "emergent_properties": [{"property": "self-organization", "confidence": 0.8}]
            }
        }


class ProgressiveSystemsAnalyzer:
    """Progressive systems thinking with session management."""
    
    def __init__(
        self,
        session_store: BaseSessionStore,
        systems_store: BaseSystemsStore,
    ):
        """Initialize with required stores."""
        self.session_store = session_store
        self.systems_store = systems_store
    
    async def analyze_system(
        self, request: ProgressiveSystemsRequest
    ) -> ProgressiveSystemsResponse:
        """Process a systems thinking step."""
        try:
            # Get or create session
            session = await self._get_or_create_session(request)
            
            # Process components and relationships
            components = await self._process_components(session.session_id, request)
            relationships = await self._process_relationships(session.session_id, request, components)
            
            # Analyze system structure
            key_components = self._identify_key_components(components, relationships)
            subsystems = self._identify_subsystems(components, relationships)
            boundaries = self._analyze_boundaries(components, relationships, request.analyze_boundaries)
            
            # Analyze dynamics
            feedback_loops = []
            balancing = 0
            reinforcing = 0
            
            if request.identify_feedback_loops:
                feedback_loops = self._identify_feedback_loops(components, relationships)
                balancing = sum(1 for loop in feedback_loops if loop.loop_type == LoopType.BALANCING)
                reinforcing = sum(1 for loop in feedback_loops if loop.loop_type == LoopType.REINFORCING)
            
            # Identify emergent properties
            emergent = self._identify_emergent_properties(
                components,
                relationships,
                feedback_loops
            )
            
            behaviors = self._analyze_system_behaviors(
                components,
                relationships,
                feedback_loops,
                emergent
            )
            
            # Assess system health
            health = self._assess_system_health(components, relationships, feedback_loops)
            bottlenecks = self._identify_bottlenecks(components, relationships)
            vulnerabilities = self._identify_vulnerabilities(components, relationships, feedback_loops)
            
            # Make predictions
            predictions = []
            intervention_points = []
            
            if request.predict_behavior:
                predictions = self._predict_behaviors(
                    components,
                    relationships,
                    feedback_loops,
                    emergent
                )
                intervention_points = self._identify_intervention_points(
                    components,
                    relationships,
                    bottlenecks
                )
            
            # Calculate complexity
            complexity = self._calculate_complexity(components, relationships, feedback_loops)
            
            # Generate recommendations
            optimizations = self._suggest_optimizations(
                health,
                bottlenecks,
                vulnerabilities
            )
            
            next_steps = self._suggest_next_analysis(
                request.analysis_focus,
                subsystems,
                emergent
            )
            
            # Create and save systems data
            systems_data = await self._create_systems_data(
                session.session_id,
                request,
                components,
                relationships,
                feedback_loops,
                emergent
            )
            saved_data = await self.systems_store.save_analysis(systems_data)
            
            return ProgressiveSystemsResponse(
                status="success",
                session_id=session.session_id,
                analysis_id=saved_data.id,
                step_number=saved_data.step_number,
                component_count=len(components),
                relationship_count=len(relationships),
                system_complexity=complexity,
                key_components=[self._component_to_dict(c) for c in key_components],
                subsystems=subsystems,
                boundaries=boundaries,
                feedback_loops=[self._loop_to_dict(loop) for loop in feedback_loops],
                balancing_loops=balancing,
                reinforcing_loops=reinforcing,
                emergent_properties=[self._emergent_to_dict(e) for e in emergent],
                system_behaviors=behaviors,
                health_assessment=health,
                bottlenecks=bottlenecks,
                vulnerabilities=vulnerabilities,
                behavior_predictions=predictions,
                intervention_points=intervention_points,
                optimization_suggestions=optimizations,
                next_analysis_steps=next_steps,
            )
            
        except Exception as e:
            return ProgressiveSystemsResponse(
                status="error",
                session_id=request.session_id or str(uuid.uuid4()),
                analysis_id=0,
                step_number=request.step_number,
                error=str(e),
            )
    
    async def _get_or_create_session(
        self, request: ProgressiveSystemsRequest
    ) -> SessionData:
        """Get existing session or create new one."""
        if request.session_id:
            session = await self.session_store.get_session(request.session_id)
            if session:
                return session
        
        # Create new session
        session_data = SessionData(
            session_id=request.session_id or str(uuid.uuid4()),
            tool_name="Systems Thinking",
            created_at=datetime.now(timezone.utc),
            metadata={
                "system_description": request.system_description,
                "system_type": request.system_type.value,
                "domain": request.domain,
            }
        )
        
        return await self.session_store.create_session(session_data)
    
    async def _process_components(
        self,
        session_id: str,
        request: ProgressiveSystemsRequest
    ) -> List[SystemComponent]:
        """Process system components."""
        components = []
        
        # Get existing components if building on previous
        if request.build_on_previous and request.previous_analyses:
            existing = await self.systems_store.get_components_from_analyses(
                session_id,
                request.previous_analyses
            )
            components.extend(existing)
        
        # Add new components
        for comp_dict in request.components + request.add_components:
            component = SystemComponent(
                name=comp_dict.get("name", "Unnamed"),
                component_type=ComponentType(comp_dict.get("type", "element")),
                description=comp_dict.get("description", ""),
                properties=comp_dict.get("properties", {}),
                state=comp_dict.get("state", {}),
                inputs=comp_dict.get("inputs", []),
                outputs=comp_dict.get("outputs", []),
            )
            components.append(component)
        
        return components
    
    async def _process_relationships(
        self,
        session_id: str,
        request: ProgressiveSystemsRequest,
        components: List[SystemComponent]
    ) -> List[SystemRelationship]:
        """Process system relationships."""
        relationships = []
        component_names = {c.name for c in components}
        
        # Get existing relationships if building on previous
        if request.build_on_previous and request.previous_analyses:
            existing = await self.systems_store.get_relationships_from_analyses(
                session_id,
                request.previous_analyses
            )
            # Filter to only include relationships between current components
            relationships.extend([
                r for r in existing
                if r.source in component_names and r.target in component_names
            ])
        
        # Add new relationships
        for rel_dict in request.relationships:
            source = rel_dict.get("source", "")
            target = rel_dict.get("target", "")
            
            if source in component_names and target in component_names:
                relationship = SystemRelationship(
                    source=source,
                    target=target,
                    relationship_nature=RelationshipNature(rel_dict.get("nature", "influences")),
                    strength=rel_dict.get("strength", 1.0),
                    description=rel_dict.get("description", ""),
                    flow_type=rel_dict.get("flow_type", "information"),
                    bidirectional=rel_dict.get("bidirectional", False),
                )
                relationships.append(relationship)
        
        # Apply modifications
        for mod in request.modify_relationships:
            # Simple modification logic
            for rel in relationships:
                if rel.source == mod.get("source") and rel.target == mod.get("target"):
                    if "strength" in mod:
                        rel.strength = mod["strength"]
                    if "nature" in mod:
                        rel.relationship_nature = RelationshipNature(mod["nature"])
        
        return relationships
    
    def _identify_key_components(
        self,
        components: List[SystemComponent],
        relationships: List[SystemRelationship]
    ) -> List[SystemComponent]:
        """Identify most important components."""
        # Count connections
        connection_counts = {}
        
        for rel in relationships:
            connection_counts[rel.source] = connection_counts.get(rel.source, 0) + 1
            connection_counts[rel.target] = connection_counts.get(rel.target, 0) + 1
        
        # Find components with most connections
        if not connection_counts:
            return components[:3] if components else []
        
        sorted_components = sorted(
            connection_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        key_names = [name for name, _ in sorted_components[:5]]
        key_components = [c for c in components if c.name in key_names]
        
        return key_components
    
    def _identify_subsystems(
        self,
        components: List[SystemComponent],
        relationships: List[SystemRelationship]
    ) -> List[Dict[str, Any]]:
        """Identify subsystems within the larger system."""
        # Build adjacency graph
        adjacency = {}
        for comp in components:
            adjacency[comp.name] = set()
        
        for rel in relationships:
            if rel.source in adjacency:
                adjacency[rel.source].add(rel.target)
            if rel.bidirectional and rel.target in adjacency:
                adjacency[rel.target].add(rel.source)
        
        # Find strongly connected components (subsystems)
        visited = set()
        subsystems = []
        
        def dfs(node: str, subsystem: set):
            visited.add(node)
            subsystem.add(node)
            for neighbor in adjacency.get(node, set()):
                if neighbor not in visited:
                    dfs(neighbor, subsystem)
        
        for comp in components:
            if comp.name not in visited:
                subsystem = set()
                dfs(comp.name, subsystem)
                if len(subsystem) > 1:  # Only count multi-component subsystems
                    subsystems.append({
                        "components": list(subsystem),
                        "size": len(subsystem),
                        "type": self._classify_subsystem(subsystem, components, relationships),
                    })
        
        return subsystems
    
    def _analyze_boundaries(
        self,
        components: List[SystemComponent],
        relationships: List[SystemRelationship],
        analyze: bool
    ) -> Dict[str, Any]:
        """Analyze system boundaries."""
        if not analyze:
            return {}
        
        boundaries = {
            "internal_components": len(components),
            "external_interfaces": [],
            "boundary_components": [],
            "permeability": 0.0,
        }
        
        # Identify boundary components (those with external interfaces)
        for comp in components:
            if comp.inputs or comp.outputs:
                external_count = 0
                
                # Check if inputs/outputs connect to components not in system
                all_component_names = {c.name for c in components}
                
                for input_name in comp.inputs:
                    if input_name not in all_component_names:
                        external_count += 1
                
                for output_name in comp.outputs:
                    if output_name not in all_component_names:
                        external_count += 1
                
                if external_count > 0:
                    boundaries["boundary_components"].append(comp.name)
                    boundaries["external_interfaces"].append({
                        "component": comp.name,
                        "external_connections": external_count,
                    })
        
        # Calculate permeability
        if components:
            boundaries["permeability"] = len(boundaries["boundary_components"]) / len(components)
        
        return boundaries
    
    def _identify_feedback_loops(
        self,
        components: List[SystemComponent],
        relationships: List[SystemRelationship]
    ) -> List[FeedbackLoop]:
        """Identify feedback loops in the system."""
        loops = []
        
        # Build directed graph
        graph = {}
        for comp in components:
            graph[comp.name] = []
        
        for rel in relationships:
            if rel.source in graph:
                graph[rel.source].append(rel.target)
        
        # Find cycles using DFS
        def find_cycles(node: str, path: List[str], visited: set) -> List[List[str]]:
            if node in path:
                # Found a cycle
                cycle_start = path.index(node)
                return [path[cycle_start:] + [node]]
            
            if node in visited:
                return []
            
            visited.add(node)
            cycles = []
            
            for neighbor in graph.get(node, []):
                cycles.extend(find_cycles(neighbor, path + [node], visited.copy()))
            
            return cycles
        
        # Find all cycles
        all_cycles = []
        for start_node in graph:
            cycles = find_cycles(start_node, [], set())
            all_cycles.extend(cycles)
        
        # Remove duplicates and create FeedbackLoop objects
        unique_cycles = []
        seen = set()
        
        for cycle in all_cycles:
            cycle_key = tuple(sorted(cycle[:-1]))  # Exclude duplicate last element
            if cycle_key not in seen and len(cycle) > 2:
                seen.add(cycle_key)
                unique_cycles.append(cycle[:-1])
        
        # Classify loops
        for cycle in unique_cycles:
            loop_type = self._classify_loop(cycle, components, relationships)
            
            loop = FeedbackLoop(
                loop_id=f"loop_{len(loops)+1}",
                components_involved=cycle,
                loop_type=loop_type,
                strength=self._calculate_loop_strength(cycle, relationships),
                description=f"{loop_type.value} loop through {' -> '.join(cycle)}",
                time_delay=self._estimate_time_delay(cycle, components),
            )
            loops.append(loop)
        
        return loops
    
    def _identify_emergent_properties(
        self,
        components: List[SystemComponent],
        relationships: List[SystemRelationship],
        feedback_loops: List[FeedbackLoop]
    ) -> List[EmergentProperty]:
        """Identify emergent properties of the system."""
        properties = []
        
        # Self-organization
        if len(feedback_loops) >= 3 and len(components) > 10:
            properties.append(EmergentProperty(
                property_name="Self-organization",
                description="System shows capacity for self-organization through multiple feedback loops",
                contributing_components=[c.name for c in components[:5]],
                confidence=0.8,
                observable_behaviors=["Pattern formation", "Adaptive restructuring"],
            ))
        
        # Resilience
        balancing_loops = [l for l in feedback_loops if l.loop_type == LoopType.BALANCING]
        if len(balancing_loops) >= 2:
            properties.append(EmergentProperty(
                property_name="Resilience",
                description="System maintains stability through balancing feedback",
                contributing_components=[c for loop in balancing_loops for c in loop.components_involved][:5],
                confidence=0.7,
                observable_behaviors=["Disturbance recovery", "Homeostasis"],
            ))
        
        # Adaptation
        if len(components) > 5 and any(c.component_type == ComponentType.CONTROLLER for c in components):
            properties.append(EmergentProperty(
                property_name="Adaptation",
                description="System can adapt to changing conditions",
                contributing_components=[c.name for c in components if c.component_type == ComponentType.CONTROLLER],
                confidence=0.6,
                observable_behaviors=["Learning", "Environmental response"],
            ))
        
        # Emergence of hierarchy
        subsystems = self._identify_subsystems(components, relationships)
        if len(subsystems) >= 3:
            properties.append(EmergentProperty(
                property_name="Hierarchical organization",
                description="System naturally organizes into hierarchical levels",
                contributing_components=[],
                confidence=0.75,
                observable_behaviors=["Level formation", "Nested control"],
            ))
        
        return properties
    
    def _analyze_system_behaviors(
        self,
        components: List[SystemComponent],
        relationships: List[SystemRelationship],
        feedback_loops: List[FeedbackLoop],
        emergent_properties: List[EmergentProperty]
    ) -> List[str]:
        """Analyze overall system behaviors."""
        behaviors = []
        
        # Based on feedback loops
        reinforcing_count = sum(1 for l in feedback_loops if l.loop_type == LoopType.REINFORCING)
        balancing_count = sum(1 for l in feedback_loops if l.loop_type == LoopType.BALANCING)
        
        if reinforcing_count > balancing_count:
            behaviors.append("Growth-oriented behavior with positive feedback dominance")
        elif balancing_count > reinforcing_count:
            behaviors.append("Stability-seeking behavior with negative feedback dominance")
        elif reinforcing_count > 0 and balancing_count > 0:
            behaviors.append("Dynamic equilibrium between growth and stability")
        
        # Based on component types
        processors = [c for c in components if c.component_type == ComponentType.PROCESSOR]
        if len(processors) > len(components) * 0.5:
            behaviors.append("High information processing capacity")
        
        # Based on emergent properties
        for prop in emergent_properties:
            if prop.property_name == "Self-organization":
                behaviors.append("Spontaneous pattern formation capability")
            elif prop.property_name == "Resilience":
                behaviors.append("Robust response to perturbations")
        
        # Based on connectivity
        avg_connections = (len(relationships) * 2) / max(len(components), 1)
        if avg_connections > 3:
            behaviors.append("Highly interconnected with complex interactions")
        elif avg_connections < 1:
            behaviors.append("Loosely coupled with limited interactions")
        
        return behaviors
    
    def _assess_system_health(
        self,
        components: List[SystemComponent],
        relationships: List[SystemRelationship],
        feedback_loops: List[FeedbackLoop]
    ) -> Dict[str, Any]:
        """Assess overall system health."""
        health = {
            "overall_health": SystemHealth.GOOD,
            "health_score": 0.7,
            "indicators": {},
        }
        
        # Connectivity health
        if components:
            connectivity = len(relationships) / len(components)
            if connectivity < 0.5:
                health["indicators"]["connectivity"] = "Low - potential isolation"
                health["health_score"] -= 0.1
            elif connectivity > 5:
                health["indicators"]["connectivity"] = "Very high - potential over-complexity"
                health["health_score"] -= 0.05
            else:
                health["indicators"]["connectivity"] = "Healthy"
        
        # Feedback balance
        reinforcing = sum(1 for l in feedback_loops if l.loop_type == LoopType.REINFORCING)
        balancing = sum(1 for l in feedback_loops if l.loop_type == LoopType.BALANCING)
        
        if reinforcing > 0 and balancing == 0:
            health["indicators"]["feedback_balance"] = "No balancing feedback - risk of runaway"
            health["health_score"] -= 0.2
        elif balancing > 0 and reinforcing == 0:
            health["indicators"]["feedback_balance"] = "No growth mechanisms"
            health["health_score"] -= 0.1
        else:
            health["indicators"]["feedback_balance"] = "Balanced feedback mechanisms"
        
        # Component diversity
        component_types = set(c.component_type for c in components)
        if len(component_types) == 1:
            health["indicators"]["diversity"] = "Low component diversity"
            health["health_score"] -= 0.1
        else:
            health["indicators"]["diversity"] = "Good component diversity"
        
        # Determine overall health
        if health["health_score"] >= 0.8:
            health["overall_health"] = SystemHealth.EXCELLENT
        elif health["health_score"] >= 0.6:
            health["overall_health"] = SystemHealth.GOOD
        elif health["health_score"] >= 0.4:
            health["overall_health"] = SystemHealth.FAIR
        else:
            health["overall_health"] = SystemHealth.POOR
        
        return health
    
    def _identify_bottlenecks(
        self,
        components: List[SystemComponent],
        relationships: List[SystemRelationship]
    ) -> List[str]:
        """Identify system bottlenecks."""
        bottlenecks = []
        
        # Components with high input but low output
        flow_balance = {}
        
        for rel in relationships:
            flow_balance[rel.target] = flow_balance.get(rel.target, {"in": 0, "out": 0})
            flow_balance[rel.target]["in"] += 1
            
            flow_balance[rel.source] = flow_balance.get(rel.source, {"in": 0, "out": 0})
            flow_balance[rel.source]["out"] += 1
        
        for comp_name, flows in flow_balance.items():
            if flows["in"] > 3 and flows["out"] <= 1:
                bottlenecks.append(f"{comp_name}: High input, low output (potential processing bottleneck)")
            elif flows["in"] == 1 and flows["out"] > 3:
                bottlenecks.append(f"{comp_name}: Single input, multiple outputs (potential constraint)")
        
        # Components in every feedback loop (critical points)
        if len(feedback_loops) > 2:
            component_loop_count = {}
            for loop in feedback_loops:
                for comp in loop.components_involved:
                    component_loop_count[comp] = component_loop_count.get(comp, 0) + 1
            
            for comp, count in component_loop_count.items():
                if count >= len(feedback_loops) * 0.5:
                    bottlenecks.append(f"{comp}: Critical component in multiple feedback loops")
        
        return bottlenecks[:5]  # Limit to top 5
    
    def _identify_vulnerabilities(
        self,
        components: List[SystemComponent],
        relationships: List[SystemRelationship],
        feedback_loops: List[FeedbackLoop]
    ) -> List[str]:
        """Identify system vulnerabilities."""
        vulnerabilities = []
        
        # Single points of failure
        critical_components = self._identify_key_components(components, relationships)
        if len(critical_components) == 1:
            vulnerabilities.append(f"Single point of failure: {critical_components[0].name}")
        
        # Unbalanced feedback
        reinforcing_loops = [l for l in feedback_loops if l.loop_type == LoopType.REINFORCING]
        if len(reinforcing_loops) > 2 and not any(l.loop_type == LoopType.BALANCING for l in feedback_loops):
            vulnerabilities.append("No balancing feedback to control growth")
        
        # Isolated components
        connected_components = set()
        for rel in relationships:
            connected_components.add(rel.source)
            connected_components.add(rel.target)
        
        isolated = [c.name for c in components if c.name not in connected_components]
        if isolated:
            vulnerabilities.append(f"Isolated components: {', '.join(isolated[:3])}")
        
        # Over-reliance on specific relationship types
        relationship_types = {}
        for rel in relationships:
            rel_type = rel.relationship_nature.value
            relationship_types[rel_type] = relationship_types.get(rel_type, 0) + 1
        
        if relationship_types:
            max_type = max(relationship_types.items(), key=lambda x: x[1])
            if max_type[1] > len(relationships) * 0.7:
                vulnerabilities.append(f"Over-reliance on {max_type[0]} relationships")
        
        return vulnerabilities
    
    def _predict_behaviors(
        self,
        components: List[SystemComponent],
        relationships: List[SystemRelationship],
        feedback_loops: List[FeedbackLoop],
        emergent_properties: List[EmergentProperty]
    ) -> List[str]:
        """Predict future system behaviors."""
        predictions = []
        
        # Based on feedback loops
        reinforcing = [l for l in feedback_loops if l.loop_type == LoopType.REINFORCING]
        if len(reinforcing) > 2:
            predictions.append("System likely to exhibit exponential growth patterns")
        
        balancing = [l for l in feedback_loops if l.loop_type == LoopType.BALANCING]
        if len(balancing) > len(reinforcing):
            predictions.append("System will tend toward stable equilibrium")
        
        # Based on emergent properties
        for prop in emergent_properties:
            if prop.property_name == "Self-organization":
                predictions.append("New structures may spontaneously emerge over time")
            elif prop.property_name == "Adaptation":
                predictions.append("System will evolve in response to environmental changes")
        
        # Based on vulnerabilities
        if len(components) > 10 and len(relationships) < len(components):
            predictions.append("Risk of fragmentation into disconnected subsystems")
        
        # Time-based predictions
        if any(loop.time_delay > 0.5 for loop in feedback_loops):
            predictions.append("Delayed feedback may cause oscillatory behavior")
        
        return predictions
    
    def _identify_intervention_points(
        self,
        components: List[SystemComponent],
        relationships: List[SystemRelationship],
        bottlenecks: List[str]
    ) -> List[Dict[str, Any]]:
        """Identify leverage points for system intervention."""
        interventions = []
        
        # High-leverage components
        key_components = self._identify_key_components(components, relationships)
        for comp in key_components[:3]:
            interventions.append({
                "type": "component_modification",
                "target": comp.name,
                "description": f"Modify {comp.name} - high connectivity component",
                "impact": "high",
            })
        
        # Feedback loop interventions
        for bottleneck in bottlenecks[:2]:
            component_name = bottleneck.split(":")[0]
            interventions.append({
                "type": "bottleneck_relief",
                "target": component_name,
                "description": f"Address bottleneck at {component_name}",
                "impact": "medium",
            })
        
        # Relationship modifications
        weak_relationships = [r for r in relationships if r.strength < 0.3]
        if weak_relationships:
            interventions.append({
                "type": "strengthen_connection",
                "target": f"{weak_relationships[0].source} -> {weak_relationships[0].target}",
                "description": "Strengthen weak but important connection",
                "impact": "medium",
            })
        
        return interventions[:5]  # Top 5 interventions
    
    def _calculate_complexity(
        self,
        components: List[SystemComponent],
        relationships: List[SystemRelationship],
        feedback_loops: List[FeedbackLoop]
    ) -> float:
        """Calculate system complexity score."""
        if not components:
            return 0.0
        
        # Component complexity
        component_score = min(1.0, len(components) / 20)  # Normalize to 20 components
        
        # Relationship complexity
        max_relationships = len(components) * (len(components) - 1)
        relationship_score = len(relationships) / max(max_relationships, 1)
        
        # Feedback complexity
        feedback_score = min(1.0, len(feedback_loops) / 5)  # Normalize to 5 loops
        
        # Type diversity
        component_types = len(set(c.component_type for c in components))
        diversity_score = component_types / len(ComponentType)
        
        # Combined complexity
        complexity = (
            component_score * 0.25 +
            relationship_score * 0.35 +
            feedback_score * 0.25 +
            diversity_score * 0.15
        )
        
        return min(1.0, complexity)
    
    def _suggest_optimizations(
        self,
        health: Dict[str, Any],
        bottlenecks: List[str],
        vulnerabilities: List[str]
    ) -> List[str]:
        """Suggest system optimizations."""
        suggestions = []
        
        # Based on health
        if health["health_score"] < 0.6:
            if "connectivity" in health["indicators"] and "Low" in health["indicators"]["connectivity"]:
                suggestions.append("Increase component connectivity for better integration")
            if "feedback_balance" in health["indicators"] and "No balancing" in str(health["indicators"]["feedback_balance"]):
                suggestions.append("Add balancing feedback loops for stability")
        
        # Based on bottlenecks
        if bottlenecks:
            suggestions.append(f"Parallelize processing at bottleneck components")
            suggestions.append("Consider load balancing across multiple components")
        
        # Based on vulnerabilities
        if any("Single point of failure" in v for v in vulnerabilities):
            suggestions.append("Add redundancy for critical components")
        
        if any("Isolated components" in v for v in vulnerabilities):
            suggestions.append("Integrate or remove isolated components")
        
        return suggestions[:4]
    
    def _suggest_next_analysis(
        self,
        current_focus: str,
        subsystems: List[Dict[str, Any]],
        emergent_properties: List[EmergentProperty]
    ) -> List[str]:
        """Suggest next analysis steps."""
        suggestions = []
        
        focus_progression = {
            "structure": ["dynamics", "feedback"],
            "dynamics": ["feedback", "emergence"],
            "feedback": ["boundaries", "emergence"],
            "boundaries": ["emergence", "optimization"],
            "emergence": ["optimization", "prediction"],
        }
        
        if current_focus in focus_progression:
            next_focuses = focus_progression[current_focus]
            suggestions.extend([f"Analyze system {focus}" for focus in next_focuses])
        
        # Based on findings
        if len(subsystems) > 3:
            suggestions.append("Deep dive into individual subsystem behavior")
        
        if len(emergent_properties) > 2:
            suggestions.append("Study interactions between emergent properties")
        
        return suggestions[:3]
    
    async def _create_systems_data(
        self,
        session_id: str,
        request: ProgressiveSystemsRequest,
        components: List[SystemComponent],
        relationships: List[SystemRelationship],
        feedback_loops: List[FeedbackLoop],
        emergent_properties: List[EmergentProperty]
    ) -> SystemsData:
        """Create systems data for storage."""
        # Calculate metrics
        metrics = {
            "complexity": self._calculate_complexity(components, relationships, feedback_loops),
            "connectivity": len(relationships) / max(len(components), 1),
            "feedback_density": len(feedback_loops) / max(len(components), 1),
        }
        
        return SystemsData(
            session_id=session_id,
            step_number=request.step_number,
            system_type=request.system_type,
            system_description=request.system_description,
            components=components,
            relationships=relationships,
            feedback_loops=feedback_loops,
            emergent_properties=emergent_properties,
            system_boundaries=self._analyze_boundaries(components, relationships, False),
            analysis_focus=request.analysis_focus,
            metrics=metrics,
            metadata=request.metadata,
            created_at=datetime.now(timezone.utc),
        )
    
    # Helper methods
    
    def _classify_subsystem(
        self,
        subsystem: set,
        components: List[SystemComponent],
        relationships: List[SystemRelationship]
    ) -> str:
        """Classify type of subsystem."""
        # Get component types in subsystem
        subsystem_components = [c for c in components if c.name in subsystem]
        component_types = [c.component_type for c in subsystem_components]
        
        # Classify based on dominant type
        if all(ct == ComponentType.PROCESSOR for ct in component_types):
            return "processing_cluster"
        elif any(ct == ComponentType.CONTROLLER for ct in component_types):
            return "control_subsystem"
        elif any(ct == ComponentType.STORAGE for ct in component_types):
            return "storage_subsystem"
        else:
            return "functional_group"
    
    def _classify_loop(
        self,
        cycle: List[str],
        components: List[SystemComponent],
        relationships: List[SystemRelationship]
    ) -> LoopType:
        """Classify feedback loop type."""
        # Count positive and negative relationships in loop
        positive_count = 0
        negative_count = 0
        
        for i in range(len(cycle)):
            source = cycle[i]
            target = cycle[(i + 1) % len(cycle)]
            
            # Find relationship
            for rel in relationships:
                if rel.source == source and rel.target == target:
                    if rel.relationship_nature in [RelationshipNature.AMPLIFIES, RelationshipNature.ENABLES]:
                        positive_count += 1
                    elif rel.relationship_nature in [RelationshipNature.DAMPENS, RelationshipNature.INHIBITS]:
                        negative_count += 1
                    break
        
        # Even number of negative relationships = reinforcing
        # Odd number of negative relationships = balancing
        if negative_count % 2 == 0:
            return LoopType.REINFORCING
        else:
            return LoopType.BALANCING
    
    def _calculate_loop_strength(
        self,
        cycle: List[str],
        relationships: List[SystemRelationship]
    ) -> float:
        """Calculate strength of feedback loop."""
        strengths = []
        
        for i in range(len(cycle)):
            source = cycle[i]
            target = cycle[(i + 1) % len(cycle)]
            
            for rel in relationships:
                if rel.source == source and rel.target == target:
                    strengths.append(rel.strength)
                    break
        
        if not strengths:
            return 0.5
        
        # Loop strength is minimum of all relationship strengths (weakest link)
        return min(strengths)
    
    def _estimate_time_delay(
        self,
        cycle: List[str],
        components: List[SystemComponent]
    ) -> float:
        """Estimate time delay in feedback loop."""
        # Simplified estimation based on component types
        delay = 0.0
        
        component_dict = {c.name: c for c in components}
        
        for comp_name in cycle:
            if comp_name in component_dict:
                comp = component_dict[comp_name]
                if comp.component_type == ComponentType.PROCESSOR:
                    delay += 0.2
                elif comp.component_type == ComponentType.STORAGE:
                    delay += 0.5
                elif comp.component_type == ComponentType.CONTROLLER:
                    delay += 0.3
                else:
                    delay += 0.1
        
        return delay
    
    def _component_to_dict(self, component: SystemComponent) -> Dict[str, Any]:
        """Convert component to dictionary."""
        return {
            "name": component.name,
            "type": component.component_type.value,
            "description": component.description,
            "connections": len(component.inputs) + len(component.outputs),
        }
    
    def _loop_to_dict(self, loop: FeedbackLoop) -> Dict[str, Any]:
        """Convert feedback loop to dictionary."""
        return {
            "id": loop.loop_id,
            "type": loop.loop_type.value,
            "components": loop.components_involved,
            "strength": loop.strength,
            "delay": loop.time_delay,
        }
    
    def _emergent_to_dict(self, emergent: EmergentProperty) -> Dict[str, Any]:
        """Convert emergent property to dictionary."""
        return {
            "property": emergent.property_name,
            "description": emergent.description,
            "confidence": emergent.confidence,
            "behaviors": emergent.observable_behaviors,
        }