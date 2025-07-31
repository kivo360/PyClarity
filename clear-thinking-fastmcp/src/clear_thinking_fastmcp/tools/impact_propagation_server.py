# Clear Thinking FastMCP Server - Impact Propagation Mapping Tool

"""
Impact Propagation Mapping cognitive tool implementation.

This tool provides systematic analysis of cascading effects through
interconnected systems, helping identify how changes ripple through
networks and revealing feedback loops and unintended consequences.
"""

from typing import Dict, List, Any, Optional
from fastmcp import FastMCP, Context
from pydantic import BaseModel, Field

from ..models.impact_propagation import (
    ImpactPropagationInput,
    ImpactPropagationAnalysis,
    Node,
    Edge,
    ImpactEvent,
    PropagationPath,
    FeedbackLoop,
    RiskArea,
    InterventionPoint,
    ImpactType,
    PropagationSpeed,
    EffectMagnitude,
    FeedbackType
)
from ..models.base import CognitiveToolBase


mcp = FastMCP("Clear Thinking - Impact Propagation")


class ImpactPropagationTool(CognitiveToolBase):
    """Impact Propagation Mapping tool for analyzing cascading effects."""
    
    name = "impact_propagation_mapping"
    description = "Analyze cascading effects through interconnected systems"
    
    async def _execute(
        self,
        input_data: ImpactPropagationInput,
        context: Context
    ) -> ImpactPropagationAnalysis:
        """Execute impact propagation mapping analysis."""
        
        await context.info(f"Starting impact propagation analysis for: {input_data.scenario}")
        await context.progress("Building impact network", 0.1)
        
        # Build or use provided network
        if input_data.system_nodes and input_data.system_edges:
            impact_network = {node.id: node for node in input_data.system_nodes}
            connections = input_data.system_edges
        else:
            impact_network, connections = await self._build_impact_network(
                input_data, context
            )
        
        await context.progress("Identifying primary impacts", 0.2)
        primary_impacts = await self._identify_primary_impacts(
            input_data, impact_network, context
        )
        
        await context.progress("Tracing propagation paths", 0.3)
        propagation_paths = await self._trace_propagation_paths(
            primary_impacts, impact_network, connections, input_data.analysis_depth or 3, context
        )
        
        await context.progress("Detecting feedback loops", 0.4)
        feedback_loops = await self._detect_feedback_loops(
            connections, impact_network, context
        )
        
        await context.progress("Identifying cascade effects", 0.5)
        cascade_effects = await self._identify_cascade_effects(
            propagation_paths, impact_network, connections, context
        )
        
        await context.progress("Analyzing risk areas", 0.6)
        risk_areas = await self._analyze_risk_areas(
            impact_network, connections, propagation_paths, context
        )
        
        await context.progress("Identifying intervention points", 0.7)
        intervention_points = await self._identify_intervention_points(
            impact_network, connections, propagation_paths, feedback_loops, context
        )
        
        await context.progress("Calculating system resilience", 0.8)
        critical_nodes = await self._identify_critical_nodes(
            impact_network, connections, propagation_paths
        )
        system_resilience = await self._calculate_system_resilience(
            impact_network, critical_nodes
        )
        
        await context.progress("Generating timeline projection", 0.85)
        timeline_projection = await self._generate_timeline_projection(
            primary_impacts, cascade_effects, input_data.time_horizon
        )
        
        await context.progress("Developing mitigation strategies", 0.9)
        mitigation_strategies = await self._develop_mitigation_strategies(
            risk_areas, intervention_points, feedback_loops
        )
        
        amplification_risks = await self._identify_amplification_risks(
            feedback_loops, cascade_effects
        )
        
        # Generate visualization data
        visual_representation = await self._generate_visualization_data(
            impact_network, connections, propagation_paths, feedback_loops
        )
        
        # Extract key insights
        key_insights = await self._extract_key_insights(
            impact_network,
            propagation_paths,
            feedback_loops,
            risk_areas,
            system_resilience
        )
        
        await context.progress("Analysis complete", 1.0)
        
        return ImpactPropagationAnalysis(
            input_scenario=input_data.scenario,
            impact_network=impact_network,
            connections=connections,
            primary_impacts=primary_impacts,
            propagation_paths=propagation_paths,
            feedback_loops=feedback_loops,
            cascade_effects=cascade_effects,
            risk_areas=risk_areas,
            intervention_points=intervention_points,
            critical_nodes=critical_nodes,
            timeline_projection=timeline_projection,
            mitigation_strategies=mitigation_strategies,
            amplification_risks=amplification_risks,
            system_resilience_score=system_resilience,
            visual_representation=visual_representation,
            key_insights=key_insights,
            confidence_level=0.85,
            complexity_level=input_data.complexity_level,
            session_id=input_data.session_id
        )
    
    async def _build_impact_network(
        self,
        input_data: ImpactPropagationInput,
        context: Context
    ) -> tuple[Dict[str, Node], List[Edge]]:
        """Build the impact network based on domain context."""
        
        domain = input_data.domain_context or "general"
        
        if domain == "organizational":
            return await self._build_organizational_network(input_data, context)
        elif domain == "technical":
            return await self._build_technical_network(input_data, context)
        elif domain == "ecosystem":
            return await self._build_ecosystem_network(input_data, context)
        elif domain == "social":
            return await self._build_social_network(input_data, context)
        else:
            return await self._build_general_network(input_data, context)
    
    async def _build_organizational_network(
        self,
        input_data: ImpactPropagationInput,
        context: Context
    ) -> tuple[Dict[str, Node], List[Edge]]:
        """Build organizational impact network."""
        
        nodes = {
            "leadership": Node(
                id="leadership",
                name="Leadership Team",
                category="organizational",
                sensitivity=0.8,
                resilience=0.6,
                influence_radius=4
            ),
            "middle_mgmt": Node(
                id="middle_mgmt",
                name="Middle Management",
                category="organizational",
                sensitivity=0.7,
                resilience=0.5,
                influence_radius=3
            ),
            "employees": Node(
                id="employees",
                name="Employees",
                category="human",
                sensitivity=0.6,
                resilience=0.4,
                influence_radius=2
            ),
            "culture": Node(
                id="culture",
                name="Company Culture",
                category="social",
                sensitivity=0.5,
                resilience=0.7,
                influence_radius=5
            ),
            "processes": Node(
                id="processes",
                name="Business Processes",
                category="process",
                sensitivity=0.6,
                resilience=0.5,
                influence_radius=3
            ),
            "customers": Node(
                id="customers",
                name="Customer Relationships",
                category="external",
                sensitivity=0.7,
                resilience=0.3,
                influence_radius=2
            ),
            "productivity": Node(
                id="productivity",
                name="Productivity",
                category="metric",
                sensitivity=0.8,
                resilience=0.4,
                influence_radius=3
            ),
            "morale": Node(
                id="morale",
                name="Employee Morale",
                category="social",
                sensitivity=0.9,
                resilience=0.3,
                influence_radius=4
            )
        }
        
        edges = [
            Edge(
                source_id="leadership",
                target_id="middle_mgmt",
                relationship_type="directs",
                strength=0.9,
                propagation_speed=PropagationSpeed.RAPID,
                bidirectional=True
            ),
            Edge(
                source_id="middle_mgmt",
                target_id="employees",
                relationship_type="manages",
                strength=0.8,
                propagation_speed=PropagationSpeed.MODERATE,
                bidirectional=True
            ),
            Edge(
                source_id="leadership",
                target_id="culture",
                relationship_type="shapes",
                strength=0.7,
                propagation_speed=PropagationSpeed.GRADUAL
            ),
            Edge(
                source_id="culture",
                target_id="morale",
                relationship_type="influences",
                strength=0.8,
                propagation_speed=PropagationSpeed.MODERATE,
                bidirectional=True
            ),
            Edge(
                source_id="morale",
                target_id="productivity",
                relationship_type="affects",
                strength=0.7,
                propagation_speed=PropagationSpeed.MODERATE
            ),
            Edge(
                source_id="employees",
                target_id="processes",
                relationship_type="executes",
                strength=0.8,
                propagation_speed=PropagationSpeed.RAPID,
                bidirectional=True
            ),
            Edge(
                source_id="processes",
                target_id="customers",
                relationship_type="serves",
                strength=0.9,
                propagation_speed=PropagationSpeed.IMMEDIATE
            ),
            Edge(
                source_id="productivity",
                target_id="customers",
                relationship_type="impacts",
                strength=0.6,
                propagation_speed=PropagationSpeed.MODERATE
            )
        ]
        
        return nodes, edges
    
    async def _build_technical_network(
        self,
        input_data: ImpactPropagationInput,
        context: Context
    ) -> tuple[Dict[str, Node], List[Edge]]:
        """Build technical system impact network."""
        
        nodes = {
            "infrastructure": Node(
                id="infrastructure",
                name="Infrastructure Layer",
                category="technical",
                sensitivity=0.9,
                resilience=0.7,
                influence_radius=5
            ),
            "database": Node(
                id="database",
                name="Database Systems",
                category="technical",
                sensitivity=0.8,
                resilience=0.6,
                influence_radius=4
            ),
            "api_layer": Node(
                id="api_layer",
                name="API Layer",
                category="technical",
                sensitivity=0.7,
                resilience=0.5,
                influence_radius=3
            ),
            "frontend": Node(
                id="frontend",
                name="Frontend Applications",
                category="technical",
                sensitivity=0.6,
                resilience=0.4,
                influence_radius=2
            ),
            "cache": Node(
                id="cache",
                name="Caching Layer",
                category="technical",
                sensitivity=0.5,
                resilience=0.8,
                influence_radius=3
            ),
            "monitoring": Node(
                id="monitoring",
                name="Monitoring Systems",
                category="technical",
                sensitivity=0.4,
                resilience=0.9,
                influence_radius=2
            ),
            "users": Node(
                id="users",
                name="End Users",
                category="external",
                sensitivity=0.9,
                resilience=0.2,
                influence_radius=1
            ),
            "performance": Node(
                id="performance",
                name="System Performance",
                category="metric",
                sensitivity=0.8,
                resilience=0.3,
                influence_radius=4
            )
        }
        
        edges = [
            Edge(
                source_id="infrastructure",
                target_id="database",
                relationship_type="hosts",
                strength=1.0,
                propagation_speed=PropagationSpeed.IMMEDIATE
            ),
            Edge(
                source_id="database",
                target_id="api_layer",
                relationship_type="provides_data",
                strength=0.9,
                propagation_speed=PropagationSpeed.RAPID,
                bidirectional=True
            ),
            Edge(
                source_id="api_layer",
                target_id="frontend",
                relationship_type="serves",
                strength=0.9,
                propagation_speed=PropagationSpeed.RAPID
            ),
            Edge(
                source_id="api_layer",
                target_id="cache",
                relationship_type="uses",
                strength=0.7,
                propagation_speed=PropagationSpeed.IMMEDIATE,
                bidirectional=True
            ),
            Edge(
                source_id="frontend",
                target_id="users",
                relationship_type="interfaces_with",
                strength=1.0,
                propagation_speed=PropagationSpeed.IMMEDIATE,
                bidirectional=True
            ),
            Edge(
                source_id="monitoring",
                target_id="performance",
                relationship_type="tracks",
                strength=0.8,
                propagation_speed=PropagationSpeed.IMMEDIATE
            ),
            Edge(
                source_id="performance",
                target_id="users",
                relationship_type="affects",
                strength=0.8,
                propagation_speed=PropagationSpeed.RAPID
            )
        ]
        
        return nodes, edges
    
    async def _build_ecosystem_network(
        self,
        input_data: ImpactPropagationInput,
        context: Context
    ) -> tuple[Dict[str, Node], List[Edge]]:
        """Build ecosystem impact network."""
        
        nodes = {
            "suppliers": Node(
                id="suppliers",
                name="Suppliers",
                category="external",
                sensitivity=0.7,
                resilience=0.5,
                influence_radius=3
            ),
            "company": Node(
                id="company",
                name="Company",
                category="organizational",
                sensitivity=0.6,
                resilience=0.6,
                influence_radius=4
            ),
            "partners": Node(
                id="partners",
                name="Partners",
                category="external",
                sensitivity=0.6,
                resilience=0.5,
                influence_radius=3
            ),
            "customers": Node(
                id="customers",
                name="Customers",
                category="external",
                sensitivity=0.8,
                resilience=0.4,
                influence_radius=2
            ),
            "competitors": Node(
                id="competitors",
                name="Competitors",
                category="external",
                sensitivity=0.5,
                resilience=0.7,
                influence_radius=3
            ),
            "market": Node(
                id="market",
                name="Market Conditions",
                category="environment",
                sensitivity=0.9,
                resilience=0.3,
                influence_radius=5
            ),
            "regulations": Node(
                id="regulations",
                name="Regulatory Environment",
                category="environment",
                sensitivity=0.3,
                resilience=0.9,
                influence_radius=4
            )
        }
        
        edges = [
            Edge(
                source_id="suppliers",
                target_id="company",
                relationship_type="supplies",
                strength=0.8,
                propagation_speed=PropagationSpeed.MODERATE,
                bidirectional=True
            ),
            Edge(
                source_id="company",
                target_id="partners",
                relationship_type="collaborates",
                strength=0.7,
                propagation_speed=PropagationSpeed.MODERATE,
                bidirectional=True
            ),
            Edge(
                source_id="company",
                target_id="customers",
                relationship_type="serves",
                strength=0.9,
                propagation_speed=PropagationSpeed.RAPID
            ),
            Edge(
                source_id="company",
                target_id="competitors",
                relationship_type="competes",
                strength=0.6,
                propagation_speed=PropagationSpeed.MODERATE,
                bidirectional=True
            ),
            Edge(
                source_id="market",
                target_id="company",
                relationship_type="influences",
                strength=0.8,
                propagation_speed=PropagationSpeed.MODERATE
            ),
            Edge(
                source_id="regulations",
                target_id="company",
                relationship_type="constrains",
                strength=0.7,
                propagation_speed=PropagationSpeed.SLOW
            )
        ]
        
        return nodes, edges
    
    async def _build_social_network(
        self,
        input_data: ImpactPropagationInput,
        context: Context
    ) -> tuple[Dict[str, Node], List[Edge]]:
        """Build social impact network."""
        
        nodes = {
            "influencers": Node(
                id="influencers",
                name="Key Influencers",
                category="social",
                sensitivity=0.6,
                resilience=0.7,
                influence_radius=5
            ),
            "early_adopters": Node(
                id="early_adopters",
                name="Early Adopters",
                category="social",
                sensitivity=0.7,
                resilience=0.5,
                influence_radius=3
            ),
            "mainstream": Node(
                id="mainstream",
                name="Mainstream Users",
                category="social",
                sensitivity=0.5,
                resilience=0.6,
                influence_radius=2
            ),
            "social_media": Node(
                id="social_media",
                name="Social Media Platforms",
                category="channel",
                sensitivity=0.8,
                resilience=0.4,
                influence_radius=5
            ),
            "communities": Node(
                id="communities",
                name="Online Communities",
                category="social",
                sensitivity=0.6,
                resilience=0.7,
                influence_radius=4
            ),
            "sentiment": Node(
                id="sentiment",
                name="Public Sentiment",
                category="metric",
                sensitivity=0.9,
                resilience=0.2,
                influence_radius=4
            )
        }
        
        edges = [
            Edge(
                source_id="influencers",
                target_id="early_adopters",
                relationship_type="influences",
                strength=0.8,
                propagation_speed=PropagationSpeed.RAPID
            ),
            Edge(
                source_id="early_adopters",
                target_id="mainstream",
                relationship_type="leads",
                strength=0.6,
                propagation_speed=PropagationSpeed.MODERATE
            ),
            Edge(
                source_id="influencers",
                target_id="social_media",
                relationship_type="uses",
                strength=0.9,
                propagation_speed=PropagationSpeed.IMMEDIATE,
                bidirectional=True
            ),
            Edge(
                source_id="social_media",
                target_id="sentiment",
                relationship_type="shapes",
                strength=0.8,
                propagation_speed=PropagationSpeed.RAPID
            ),
            Edge(
                source_id="communities",
                target_id="sentiment",
                relationship_type="contributes",
                strength=0.7,
                propagation_speed=PropagationSpeed.MODERATE,
                bidirectional=True
            )
        ]
        
        return nodes, edges
    
    async def _build_general_network(
        self,
        input_data: ImpactPropagationInput,
        context: Context
    ) -> tuple[Dict[str, Node], List[Edge]]:
        """Build a general-purpose impact network."""
        
        # Parse scenario to identify key elements
        scenario_lower = input_data.scenario.lower()
        
        nodes = {}
        node_id = 1
        
        # Create basic nodes based on common patterns
        if any(word in scenario_lower for word in ["change", "implement", "introduce"]):
            nodes[f"node_{node_id}"] = Node(
                id=f"node_{node_id}",
                name="Change Initiative",
                category="initiative",
                sensitivity=0.8,
                resilience=0.5,
                influence_radius=4
            )
            node_id += 1
        
        if any(word in scenario_lower for word in ["team", "department", "organization"]):
            nodes[f"node_{node_id}"] = Node(
                id=f"node_{node_id}",
                name="Organizational Unit",
                category="organizational",
                sensitivity=0.7,
                resilience=0.6,
                influence_radius=3
            )
            node_id += 1
        
        if any(word in scenario_lower for word in ["system", "process", "workflow"]):
            nodes[f"node_{node_id}"] = Node(
                id=f"node_{node_id}",
                name="System/Process",
                category="process",
                sensitivity=0.6,
                resilience=0.5,
                influence_radius=3
            )
            node_id += 1
        
        if any(word in scenario_lower for word in ["customer", "user", "stakeholder"]):
            nodes[f"node_{node_id}"] = Node(
                id=f"node_{node_id}",
                name="Stakeholders",
                category="external",
                sensitivity=0.8,
                resilience=0.4,
                influence_radius=2
            )
            node_id += 1
        
        # Ensure we have at least a minimal network
        if len(nodes) < 3:
            nodes.update({
                "primary": Node(
                    id="primary",
                    name="Primary System",
                    category="core",
                    sensitivity=0.7,
                    resilience=0.5,
                    influence_radius=3
                ),
                "secondary": Node(
                    id="secondary",
                    name="Secondary System",
                    category="support",
                    sensitivity=0.6,
                    resilience=0.6,
                    influence_radius=2
                ),
                "environment": Node(
                    id="environment",
                    name="Environment",
                    category="external",
                    sensitivity=0.8,
                    resilience=0.4,
                    influence_radius=4
                )
            })
        
        # Create edges between nodes
        edges = []
        node_ids = list(nodes.keys())
        for i in range(len(node_ids) - 1):
            edges.append(Edge(
                source_id=node_ids[i],
                target_id=node_ids[i + 1],
                relationship_type="affects",
                strength=0.7,
                propagation_speed=PropagationSpeed.MODERATE
            ))
        
        return nodes, edges
    
    async def _identify_primary_impacts(
        self,
        input_data: ImpactPropagationInput,
        impact_network: Dict[str, Node],
        context: Context
    ) -> List[ImpactEvent]:
        """Identify primary (direct) impacts."""
        
        primary_impacts = []
        
        if input_data.initial_impact:
            primary_impacts.append(input_data.initial_impact)
        else:
            # Generate primary impacts based on scenario
            scenario_lower = input_data.scenario.lower()
            
            # Find the most likely affected nodes
            for node_id, node in impact_network.items():
                impact_probability = 0.0
                
                # Check if node is mentioned in scenario
                if node.name.lower() in scenario_lower:
                    impact_probability = 0.9
                elif node.category in scenario_lower:
                    impact_probability = 0.6
                
                # High sensitivity nodes are more likely to be impacted
                if node.sensitivity > 0.7:
                    impact_probability = max(impact_probability, 0.5)
                
                if impact_probability > 0.4:
                    primary_impacts.append(ImpactEvent(
                        node_id=node_id,
                        impact_type=ImpactType.DIRECT,
                        description=f"Direct impact on {node.name} from {input_data.scenario}",
                        magnitude=EffectMagnitude.SIGNIFICANT if impact_probability > 0.7 else EffectMagnitude.MODERATE,
                        probability=impact_probability
                    ))
        
        # Ensure at least one primary impact
        if not primary_impacts and impact_network:
            first_node_id = list(impact_network.keys())[0]
            primary_impacts.append(ImpactEvent(
                node_id=first_node_id,
                impact_type=ImpactType.DIRECT,
                description=f"Initial impact from {input_data.scenario}",
                magnitude=EffectMagnitude.MODERATE,
                probability=0.8
            ))
        
        return primary_impacts
    
    async def _trace_propagation_paths(
        self,
        primary_impacts: List[ImpactEvent],
        impact_network: Dict[str, Node],
        connections: List[Edge],
        max_depth: int,
        context: Context
    ) -> List[PropagationPath]:
        """Trace how impacts propagate through the network."""
        
        propagation_paths = []
        
        # Build adjacency map for efficient traversal
        adjacency = {}
        for edge in connections:
            if edge.source_id not in adjacency:
                adjacency[edge.source_id] = []
            adjacency[edge.source_id].append(edge)
            
            if edge.bidirectional:
                if edge.target_id not in adjacency:
                    adjacency[edge.target_id] = []
                adjacency[edge.target_id].append(Edge(
                    source_id=edge.target_id,
                    target_id=edge.source_id,
                    relationship_type=edge.relationship_type,
                    strength=edge.strength,
                    propagation_speed=edge.propagation_speed,
                    bidirectional=False
                ))
        
        # Trace paths from each primary impact
        for impact in primary_impacts:
            if impact.node_id not in impact_network:
                continue
                
            # BFS to find propagation paths
            visited = set()
            queue = [(impact.node_id, [impact.node_id], impact.magnitude, 0)]
            
            while queue:
                current_node, path, current_magnitude, depth = queue.pop(0)
                
                if depth >= max_depth:
                    continue
                
                if current_node in visited and len(path) > 2:
                    # Found a complete path
                    if len(path) > 1:
                        propagation_paths.append(PropagationPath(
                            path_nodes=path,
                            total_impact=current_magnitude,
                            propagation_time=self._calculate_propagation_time(path, connections),
                            attenuation_factor=0.2 * depth,  # 20% reduction per hop
                            critical_points=self._identify_critical_points_in_path(path, impact_network)
                        ))
                    continue
                
                visited.add(current_node)
                
                # Explore neighbors
                if current_node in adjacency:
                    for edge in adjacency[current_node]:
                        if edge.target_id not in path:  # Avoid cycles in path
                            # Calculate attenuated magnitude
                            new_magnitude = self._attenuate_magnitude(
                                current_magnitude,
                                edge.strength,
                                depth + 1
                            )
                            
                            new_path = path + [edge.target_id]
                            queue.append((edge.target_id, new_path, new_magnitude, depth + 1))
        
        return propagation_paths
    
    def _calculate_propagation_time(self, path: List[str], connections: List[Edge]) -> str:
        """Calculate total propagation time along a path."""
        
        total_hours = 0
        for i in range(len(path) - 1):
            for edge in connections:
                if edge.source_id == path[i] and edge.target_id == path[i + 1]:
                    speed_hours = {
                        PropagationSpeed.IMMEDIATE: 0,
                        PropagationSpeed.RAPID: 4,
                        PropagationSpeed.MODERATE: 24,
                        PropagationSpeed.SLOW: 168,
                        PropagationSpeed.GRADUAL: 720
                    }
                    total_hours += speed_hours.get(edge.propagation_speed, 24)
                    break
        
        if total_hours == 0:
            return "Immediate"
        elif total_hours <= 24:
            return f"{total_hours} hours"
        elif total_hours <= 168:
            return f"{total_hours // 24} days"
        elif total_hours <= 720:
            return f"{total_hours // 168} weeks"
        else:
            return f"{total_hours // 720} months"
    
    def _identify_critical_points_in_path(
        self,
        path: List[str],
        impact_network: Dict[str, Node]
    ) -> List[str]:
        """Identify critical points in a propagation path."""
        
        critical_points = []
        for node_id in path:
            if node_id in impact_network:
                node = impact_network[node_id]
                # Critical if high influence radius or low resilience
                if node.influence_radius >= 3 or node.resilience <= 0.3:
                    critical_points.append(node_id)
        
        return critical_points
    
    def _attenuate_magnitude(
        self,
        current_magnitude: EffectMagnitude,
        edge_strength: float,
        depth: int
    ) -> EffectMagnitude:
        """Calculate attenuated magnitude based on edge strength and depth."""
        
        magnitude_values = {
            EffectMagnitude.NEGLIGIBLE: 0.1,
            EffectMagnitude.MINOR: 0.3,
            EffectMagnitude.MODERATE: 0.5,
            EffectMagnitude.SIGNIFICANT: 0.7,
            EffectMagnitude.MAJOR: 0.85,
            EffectMagnitude.CRITICAL: 1.0
        }
        
        current_value = magnitude_values.get(current_magnitude, 0.5)
        # Attenuate based on edge strength and depth
        new_value = current_value * edge_strength * (0.8 ** depth)
        
        # Map back to magnitude
        if new_value >= 0.85:
            return EffectMagnitude.CRITICAL
        elif new_value >= 0.7:
            return EffectMagnitude.MAJOR
        elif new_value >= 0.5:
            return EffectMagnitude.SIGNIFICANT
        elif new_value >= 0.3:
            return EffectMagnitude.MODERATE
        elif new_value >= 0.1:
            return EffectMagnitude.MINOR
        else:
            return EffectMagnitude.NEGLIGIBLE
    
    async def _detect_feedback_loops(
        self,
        connections: List[Edge],
        impact_network: Dict[str, Node],
        context: Context
    ) -> List[FeedbackLoop]:
        """Detect feedback loops in the network."""
        
        feedback_loops = []
        
        # Build adjacency map
        adjacency = {}
        for edge in connections:
            if edge.source_id not in adjacency:
                adjacency[edge.source_id] = []
            adjacency[edge.source_id].append(edge.target_id)
            
            if edge.bidirectional:
                if edge.target_id not in adjacency:
                    adjacency[edge.target_id] = []
                adjacency[edge.target_id].append(edge.source_id)
        
        # DFS to find cycles
        visited = set()
        rec_stack = set()
        
        def find_cycles_from_node(node, path):
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            
            cycles = []
            
            if node in adjacency:
                for neighbor in adjacency[node]:
                    if neighbor not in visited:
                        cycles.extend(find_cycles_from_node(neighbor, path.copy()))
                    elif neighbor in rec_stack and neighbor in path:
                        # Found a cycle
                        cycle_start = path.index(neighbor)
                        cycle = path[cycle_start:] + [neighbor]
                        if len(cycle) > 2:  # Meaningful cycles only
                            cycles.append(cycle)
            
            rec_stack.remove(node)
            return cycles
        
        # Find all cycles
        all_cycles = []
        for node in impact_network:
            if node not in visited:
                all_cycles.extend(find_cycles_from_node(node, []))
        
        # Convert cycles to feedback loops
        for cycle in all_cycles:
            # Determine feedback type based on edge relationships
            positive_count = 0
            total_strength = 0.0
            
            for i in range(len(cycle) - 1):
                for edge in connections:
                    if edge.source_id == cycle[i] and edge.target_id == cycle[i + 1]:
                        total_strength += edge.strength
                        # Simple heuristic: reinforcing relationships create positive feedback
                        if edge.relationship_type in ["amplifies", "reinforces", "triggers"]:
                            positive_count += 1
                        break
            
            avg_strength = total_strength / (len(cycle) - 1) if len(cycle) > 1 else 0
            
            feedback_type = FeedbackType.POSITIVE if positive_count > len(cycle) // 2 else FeedbackType.NEGATIVE
            
            feedback_loops.append(FeedbackLoop(
                loop_nodes=cycle,
                feedback_type=feedback_type,
                strength=avg_strength,
                cycle_time=self._calculate_propagation_time(cycle, connections),
                stability_threshold=0.85 if feedback_type == FeedbackType.POSITIVE else None,
                amplification_rate=1.2 if feedback_type == FeedbackType.POSITIVE else 0.8
            ))
        
        return feedback_loops
    
    async def _identify_cascade_effects(
        self,
        propagation_paths: List[PropagationPath],
        impact_network: Dict[str, Node],
        connections: List[Edge],
        context: Context
    ) -> List[ImpactEvent]:
        """Identify cascade and emergent effects."""
        
        cascade_effects = []
        affected_nodes = {}
        
        # Track cumulative impacts on each node
        for path in propagation_paths:
            for i, node_id in enumerate(path.path_nodes[1:], 1):  # Skip origin
                if node_id not in affected_nodes:
                    affected_nodes[node_id] = {
                        'count': 0,
                        'max_magnitude': EffectMagnitude.NEGLIGIBLE,
                        'paths': []
                    }
                
                affected_nodes[node_id]['count'] += 1
                affected_nodes[node_id]['paths'].append(path)
                
                # Update maximum magnitude
                current_mag_value = self._magnitude_to_value(path.total_impact)
                max_mag_value = self._magnitude_to_value(affected_nodes[node_id]['max_magnitude'])
                
                if current_mag_value > max_mag_value:
                    affected_nodes[node_id]['max_magnitude'] = path.total_impact
        
        # Generate cascade effects for heavily impacted nodes
        for node_id, impact_data in affected_nodes.items():
            if impact_data['count'] >= 2:  # Multiple impact paths
                node = impact_network.get(node_id)
                if node:
                    # Determine impact type
                    if impact_data['count'] >= 3:
                        impact_type = ImpactType.CASCADE
                    elif node.influence_radius >= 4:
                        impact_type = ImpactType.SYSTEMIC
                    else:
                        impact_type = ImpactType.EMERGENT
                    
                    cascade_effects.append(ImpactEvent(
                        node_id=node_id,
                        impact_type=impact_type,
                        description=f"{'Cascade' if impact_type == ImpactType.CASCADE else 'Emergent'} effect on {node.name} from multiple impact paths",
                        magnitude=impact_data['max_magnitude'],
                        probability=min(0.9, 0.3 * impact_data['count']),  # Higher probability with more paths
                        time_delay=self._estimate_cascade_delay(impact_data['paths'])
                    ))
        
        return cascade_effects
    
    def _magnitude_to_value(self, magnitude: EffectMagnitude) -> float:
        """Convert magnitude enum to numeric value."""
        magnitude_values = {
            EffectMagnitude.NEGLIGIBLE: 0.1,
            EffectMagnitude.MINOR: 0.3,
            EffectMagnitude.MODERATE: 0.5,
            EffectMagnitude.SIGNIFICANT: 0.7,
            EffectMagnitude.MAJOR: 0.85,
            EffectMagnitude.CRITICAL: 1.0
        }
        return magnitude_values.get(magnitude, 0.5)
    
    def _estimate_cascade_delay(self, paths: List[PropagationPath]) -> str:
        """Estimate time delay for cascade effects."""
        
        # Use average propagation time from paths
        total_hours = 0
        count = 0
        
        for path in paths:
            time_str = path.propagation_time
            if "hour" in time_str:
                hours = int(time_str.split()[0])
                total_hours += hours
                count += 1
            elif "day" in time_str:
                days = int(time_str.split()[0])
                total_hours += days * 24
                count += 1
        
        if count > 0:
            avg_hours = total_hours // count
            if avg_hours <= 24:
                return f"{avg_hours} hours"
            else:
                return f"{avg_hours // 24} days"
        
        return "24 hours"
    
    async def _analyze_risk_areas(
        self,
        impact_network: Dict[str, Node],
        connections: List[Edge],
        propagation_paths: List[PropagationPath],
        context: Context
    ) -> List[RiskArea]:
        """Analyze and identify risk areas."""
        
        risk_areas = []
        
        # Risk 1: Single points of failure
        node_connections = {}
        for edge in connections:
            if edge.source_id not in node_connections:
                node_connections[edge.source_id] = {'in': 0, 'out': 0}
            if edge.target_id not in node_connections:
                node_connections[edge.target_id] = {'in': 0, 'out': 0}
            
            node_connections[edge.source_id]['out'] += 1
            node_connections[edge.target_id]['in'] += 1
        
        # Find nodes with high connectivity (potential single points of failure)
        for node_id, counts in node_connections.items():
            total_connections = counts['in'] + counts['out']
            if total_connections >= 4 and node_id in impact_network:
                node = impact_network[node_id]
                if node.resilience < 0.5:  # Low resilience + high connectivity = risk
                    risk_areas.append(RiskArea(
                        description=f"Single point of failure: {node.name}",
                        affected_nodes=[node_id] + [
                            edge.target_id for edge in connections 
                            if edge.source_id == node_id
                        ],
                        risk_level="critical" if node.resilience < 0.3 else "high",
                        trigger_conditions=[
                            f"{node.name} failure",
                            f"{node.name} overload",
                            "External disruption"
                        ],
                        mitigation_strategies=[
                            f"Add redundancy to {node.name}",
                            "Implement failover mechanisms",
                            "Distribute load across multiple nodes"
                        ],
                        early_warning_indicators=[
                            f"{node.name} performance degradation",
                            "Increased error rates",
                            "Resource utilization spikes"
                        ]
                    ))
        
        # Risk 2: Cascade amplification zones
        cascade_zones = {}
        for path in propagation_paths:
            if path.total_impact in [EffectMagnitude.MAJOR, EffectMagnitude.CRITICAL]:
                for node_id in path.path_nodes:
                    if node_id not in cascade_zones:
                        cascade_zones[node_id] = 0
                    cascade_zones[node_id] += 1
        
        for node_id, impact_count in cascade_zones.items():
            if impact_count >= 3 and node_id in impact_network:
                node = impact_network[node_id]
                risk_areas.append(RiskArea(
                    description=f"Cascade amplification zone: {node.name}",
                    affected_nodes=[node_id],
                    risk_level="high",
                    trigger_conditions=[
                        "Multiple simultaneous impacts",
                        "Feedback loop activation",
                        "System overload"
                    ],
                    mitigation_strategies=[
                        "Implement circuit breakers",
                        "Add dampening mechanisms",
                        "Monitor for early signs of cascade"
                    ]
                ))
        
        # Risk 3: Low resilience clusters
        low_resilience_nodes = [
            node_id for node_id, node in impact_network.items()
            if node.resilience < 0.4
        ]
        
        if len(low_resilience_nodes) >= 3:
            risk_areas.append(RiskArea(
                description="Low resilience cluster vulnerability",
                affected_nodes=low_resilience_nodes,
                risk_level="medium",
                trigger_conditions=[
                    "Sustained stress",
                    "Multiple minor disruptions",
                    "Resource constraints"
                ],
                mitigation_strategies=[
                    "Strengthen resilience through redundancy",
                    "Implement gradual rollout strategies",
                    "Enhance monitoring and response capabilities"
                ]
            ))
        
        return risk_areas
    
    async def _identify_intervention_points(
        self,
        impact_network: Dict[str, Node],
        connections: List[Edge],
        propagation_paths: List[PropagationPath],
        feedback_loops: List[FeedbackLoop],
        context: Context
    ) -> List[InterventionPoint]:
        """Identify optimal intervention points."""
        
        intervention_points = []
        
        # Strategy 1: Intervene at high-influence nodes
        for node_id, node in impact_network.items():
            if node.influence_radius >= 3:
                # Count how many paths pass through this node
                path_count = sum(1 for path in propagation_paths if node_id in path.path_nodes)
                
                if path_count >= 2:
                    intervention_points.append(InterventionPoint(
                        node_id=node_id,
                        intervention_type="dampen",
                        effectiveness=0.8,
                        cost=f"Medium - requires modification to {node.name}",
                        side_effects=[
                            "Temporary performance reduction",
                            "Requires stakeholder alignment"
                        ],
                        timing_critical=True
                    ))
        
        # Strategy 2: Break feedback loops
        for loop in feedback_loops:
            if loop.feedback_type == FeedbackType.POSITIVE and loop.strength > 0.7:
                # Find the weakest link in the loop
                weakest_edge = None
                min_strength = 1.0
                
                for i in range(len(loop.loop_nodes) - 1):
                    for edge in connections:
                        if (edge.source_id == loop.loop_nodes[i] and 
                            edge.target_id == loop.loop_nodes[i + 1] and
                            edge.strength < min_strength):
                            weakest_edge = edge
                            min_strength = edge.strength
                
                if weakest_edge:
                    intervention_points.append(InterventionPoint(
                        node_id=weakest_edge.source_id,
                        intervention_type="block",
                        effectiveness=0.9,
                        cost="Low - modify single connection",
                        side_effects=[
                            f"Disrupts {weakest_edge.relationship_type} relationship",
                            "May require alternative pathways"
                        ],
                        timing_critical=False
                    ))
        
        # Strategy 3: Amplify positive effects
        for node_id, node in impact_network.items():
            if node.category == "metric" and node.name.lower() in ["productivity", "performance", "morale"]:
                intervention_points.append(InterventionPoint(
                    node_id=node_id,
                    intervention_type="amplify",
                    effectiveness=0.7,
                    cost="High - requires investment",
                    side_effects=[
                        "Increased resource consumption",
                        "May create new dependencies"
                    ],
                    timing_critical=False
                ))
        
        return intervention_points
    
    async def _identify_critical_nodes(
        self,
        impact_network: Dict[str, Node],
        connections: List[Edge],
        propagation_paths: List[PropagationPath]
    ) -> List[str]:
        """Identify nodes critical for system stability."""
        
        critical_nodes = []
        
        # Calculate centrality metrics
        node_metrics = {}
        
        for node_id in impact_network:
            node_metrics[node_id] = {
                'degree': 0,
                'path_frequency': 0,
                'influence_reach': impact_network[node_id].influence_radius
            }
        
        # Degree centrality
        for edge in connections:
            if edge.source_id in node_metrics:
                node_metrics[edge.source_id]['degree'] += 1
            if edge.target_id in node_metrics:
                node_metrics[edge.target_id]['degree'] += 1
        
        # Path frequency
        for path in propagation_paths:
            for node_id in path.path_nodes:
                if node_id in node_metrics:
                    node_metrics[node_id]['path_frequency'] += 1
        
        # Identify critical nodes based on combined metrics
        for node_id, metrics in node_metrics.items():
            criticality_score = (
                metrics['degree'] * 0.3 +
                metrics['path_frequency'] * 0.4 +
                metrics['influence_reach'] * 0.3
            )
            
            if criticality_score >= 3.0 or metrics['degree'] >= 4:
                critical_nodes.append(node_id)
        
        return critical_nodes
    
    async def _calculate_system_resilience(
        self,
        impact_network: Dict[str, Node],
        critical_nodes: List[str]
    ) -> float:
        """Calculate overall system resilience score."""
        
        if not impact_network:
            return 0.5
        
        # Base resilience: average of all nodes
        total_resilience = sum(node.resilience for node in impact_network.values())
        avg_resilience = total_resilience / len(impact_network)
        
        # Adjust for critical nodes
        critical_weight = 1.5
        weighted_sum = 0.0
        weight_total = 0.0
        
        for node_id, node in impact_network.items():
            weight = critical_weight if node_id in critical_nodes else 1.0
            weighted_sum += node.resilience * weight
            weight_total += weight
        
        weighted_resilience = weighted_sum / weight_total if weight_total > 0 else avg_resilience
        
        # Penalty for too many critical nodes
        critical_ratio = len(critical_nodes) / len(impact_network)
        if critical_ratio > 0.3:  # More than 30% critical
            weighted_resilience *= (1 - 0.2 * (critical_ratio - 0.3))
        
        return max(0.0, min(1.0, weighted_resilience))
    
    async def _generate_timeline_projection(
        self,
        primary_impacts: List[ImpactEvent],
        cascade_effects: List[ImpactEvent],
        time_horizon: Optional[str]
    ) -> Dict[str, List[ImpactEvent]]:
        """Generate timeline projection of impacts."""
        
        timeline = {
            "immediate": [],
            "short_term": [],
            "medium_term": [],
            "long_term": []
        }
        
        all_impacts = primary_impacts + cascade_effects
        
        for impact in all_impacts:
            if not impact.time_delay or impact.time_delay == "0 hours" or "Immediate" in impact.time_delay:
                timeline["immediate"].append(impact)
            elif "hour" in impact.time_delay:
                hours = int(impact.time_delay.split()[0])
                if hours <= 24:
                    timeline["immediate"].append(impact)
                else:
                    timeline["short_term"].append(impact)
            elif "day" in impact.time_delay:
                days = int(impact.time_delay.split()[0])
                if days <= 7:
                    timeline["short_term"].append(impact)
                else:
                    timeline["medium_term"].append(impact)
            elif "week" in impact.time_delay:
                timeline["medium_term"].append(impact)
            else:
                timeline["long_term"].append(impact)
        
        return timeline
    
    async def _develop_mitigation_strategies(
        self,
        risk_areas: List[RiskArea],
        intervention_points: List[InterventionPoint],
        feedback_loops: List[FeedbackLoop]
    ) -> List[str]:
        """Develop comprehensive mitigation strategies."""
        
        strategies = []
        
        # Strategies from risk areas
        for risk in risk_areas:
            if risk.mitigation_strategies:
                strategies.extend(risk.mitigation_strategies)
        
        # Strategies from intervention points
        for intervention in intervention_points:
            if intervention.intervention_type == "dampen":
                strategies.append(f"Implement dampening controls at {intervention.node_id}")
            elif intervention.intervention_type == "block":
                strategies.append(f"Create circuit breaker at {intervention.node_id}")
            elif intervention.intervention_type == "amplify":
                strategies.append(f"Enhance positive effects at {intervention.node_id}")
        
        # Strategies for feedback loops
        for loop in feedback_loops:
            if loop.feedback_type == FeedbackType.POSITIVE and loop.strength > 0.7:
                strategies.append(f"Monitor and control positive feedback loop: {' -> '.join(loop.loop_nodes[:3])}...")
        
        # Remove duplicates and prioritize
        unique_strategies = list(dict.fromkeys(strategies))
        
        # Add general strategies if needed
        if len(unique_strategies) < 3:
            unique_strategies.extend([
                "Implement comprehensive monitoring system",
                "Develop incident response playbooks",
                "Create redundancy in critical paths"
            ])
        
        return unique_strategies[:10]  # Top 10 strategies
    
    async def _identify_amplification_risks(
        self,
        feedback_loops: List[FeedbackLoop],
        cascade_effects: List[ImpactEvent]
    ) -> List[str]:
        """Identify risks of impact amplification."""
        
        risks = []
        
        # Risks from positive feedback loops
        for loop in feedback_loops:
            if loop.feedback_type == FeedbackType.POSITIVE:
                if loop.amplification_rate and loop.amplification_rate > 1.1:
                    risks.append(
                        f"High amplification risk in feedback loop with {loop.amplification_rate:.1f}x growth rate"
                    )
                elif loop.strength > 0.8:
                    risks.append(
                        f"Strong positive feedback loop could lead to runaway effects"
                    )
        
        # Risks from cascade concentration
        cascade_nodes = {}
        for effect in cascade_effects:
            if effect.impact_type == ImpactType.CASCADE:
                if effect.node_id not in cascade_nodes:
                    cascade_nodes[effect.node_id] = 0
                cascade_nodes[effect.node_id] += 1
        
        for node_id, count in cascade_nodes.items():
            if count >= 3:
                risks.append(
                    f"Multiple cascade paths converging could create amplification at node {node_id}"
                )
        
        # General amplification risks
        if len(feedback_loops) >= 3:
            risks.append("Multiple feedback loops could interact to create complex amplification patterns")
        
        if any(effect.magnitude == EffectMagnitude.CRITICAL for effect in cascade_effects):
            risks.append("Critical-level cascade effects could trigger system-wide amplification")
        
        return risks
    
    async def _generate_visualization_data(
        self,
        impact_network: Dict[str, Node],
        connections: List[Edge],
        propagation_paths: List[PropagationPath],
        feedback_loops: List[FeedbackLoop]
    ) -> Dict[str, Any]:
        """Generate data for visualizing the impact network."""
        
        # Create node data with impact information
        nodes_data = []
        for node_id, node in impact_network.items():
            # Count appearances in propagation paths
            path_count = sum(1 for path in propagation_paths if node_id in path.path_nodes)
            
            nodes_data.append({
                "id": node_id,
                "label": node.name,
                "category": node.category,
                "sensitivity": node.sensitivity,
                "resilience": node.resilience,
                "influence_radius": node.influence_radius,
                "impact_level": "high" if path_count >= 3 else "medium" if path_count >= 1 else "low"
            })
        
        # Create edge data with propagation information
        edges_data = []
        for edge in connections:
            edges_data.append({
                "source": edge.source_id,
                "target": edge.target_id,
                "relationship": edge.relationship_type,
                "strength": edge.strength,
                "speed": edge.propagation_speed,
                "bidirectional": edge.bidirectional
            })
        
        # Add feedback loop information
        loops_data = []
        for loop in feedback_loops:
            loops_data.append({
                "nodes": loop.loop_nodes,
                "type": loop.feedback_type,
                "strength": loop.strength
            })
        
        return {
            "nodes": nodes_data,
            "edges": edges_data,
            "feedback_loops": loops_data,
            "layout_hint": "force-directed",
            "highlight_critical": True
        }
    
    async def _extract_key_insights(
        self,
        impact_network: Dict[str, Node],
        propagation_paths: List[PropagationPath],
        feedback_loops: List[FeedbackLoop],
        risk_areas: List[RiskArea],
        system_resilience: float
    ) -> List[str]:
        """Extract key insights from the analysis."""
        
        insights = []
        
        # Insight about system resilience
        if system_resilience < 0.3:
            insights.append("System has critically low resilience - urgent intervention needed")
        elif system_resilience < 0.5:
            insights.append("System resilience below optimal levels - consider strengthening key nodes")
        else:
            insights.append(f"System shows {'good' if system_resilience > 0.7 else 'moderate'} resilience to disruption")
        
        # Insight about propagation patterns
        avg_path_length = sum(len(path.path_nodes) for path in propagation_paths) / len(propagation_paths) if propagation_paths else 0
        if avg_path_length > 4:
            insights.append("Long propagation chains detected - impacts may be delayed but far-reaching")
        else:
            insights.append("Short propagation paths indicate rapid impact spread")
        
        # Insight about feedback loops
        positive_loops = [loop for loop in feedback_loops if loop.feedback_type == FeedbackType.POSITIVE]
        if len(positive_loops) > 2:
            insights.append(f"{len(positive_loops)} positive feedback loops could amplify impacts significantly")
        
        # Insight about risk concentration
        if len(risk_areas) > 0:
            critical_risks = [risk for risk in risk_areas if risk.risk_level == "critical"]
            if critical_risks:
                insights.append(f"{len(critical_risks)} critical risk areas require immediate attention")
        
        # Insight about intervention opportunities
        high_influence_nodes = [
            node_id for node_id, node in impact_network.items()
            if node.influence_radius >= 4
        ]
        if high_influence_nodes:
            insights.append(
                f"{len(high_influence_nodes)} high-influence nodes offer strategic intervention points"
            )
        
        return insights


@mcp.tool()
async def analyze_impact_propagation(
    scenario: str,
    complexity_level: str = "medium",
    session_id: str = "default",
    domain_context: Optional[str] = None,
    analysis_depth: Optional[int] = 3,
    time_horizon: Optional[str] = None,
    focus_areas: Optional[List[str]] = None,
    risk_tolerance: Optional[str] = "medium"
) -> ImpactPropagationAnalysis:
    """
    Analyze how impacts cascade through interconnected systems.
    
    This tool maps impact propagation networks to understand:
    - Direct and indirect effects
    - Cascade patterns and amplification
    - Feedback loops (positive/negative)
    - Critical intervention points
    - System resilience
    
    Args:
        scenario: The change or event to analyze
        complexity_level: Level of analysis detail (basic/medium/complex)
        session_id: Unique session identifier
        domain_context: Context domain (organizational/technical/ecosystem/social)
        analysis_depth: Degrees of propagation to analyze (1-10)
        time_horizon: Time period for analysis
        focus_areas: Specific areas to focus on
        risk_tolerance: Risk tolerance level (low/medium/high)
    
    Returns:
        Comprehensive impact propagation analysis with network visualization
    
    Example:
        >>> result = await analyze_impact_propagation(
        ...     scenario="Implementing AI automation in customer service",
        ...     domain_context="organizational",
        ...     analysis_depth=4,
        ...     focus_areas=["employee_impact", "customer_experience"]
        ... )
    """
    
    # Create input model
    input_data = ImpactPropagationInput(
        scenario=scenario,
        complexity_level=complexity_level,
        session_id=session_id,
        domain_context=domain_context,
        analysis_depth=analysis_depth,
        time_horizon=time_horizon,
        focus_areas=focus_areas,
        risk_tolerance=risk_tolerance
    )
    
    # Execute analysis
    tool = ImpactPropagationTool()
    context = Context()
    
    return await tool.execute(input_data, context)