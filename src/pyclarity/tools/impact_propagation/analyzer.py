"""
Impact Propagation Analyzer

Analyzes how changes ripple through interconnected systems.
"""

import asyncio
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple

import networkx as nx

from ..base import BaseCognitiveAnalyzer
from .models import (
    ComplexityLevel,
    Edge,
    EffectMagnitude,
    FeedbackLoop,
    FeedbackType,
    ImpactEvent,
    ImpactPropagationContext,
    ImpactPropagationResult,
    ImpactType,
    InterventionPoint,
    Node,
    PropagationPath,
    PropagationSpeed,
    RiskArea,
)


class ImpactPropagationAnalyzer(BaseCognitiveAnalyzer[ImpactPropagationContext, ImpactPropagationResult]):
    """
    Analyzes impact propagation through interconnected systems.

    This analyzer maps how changes cascade through networks, identifies
    feedback loops, and suggests intervention points.
    """

    def __init__(self):
        super().__init__(
            tool_name="Impact Propagation",
            tool_description="Maps cascading effects through interconnected systems",
            version="2.0.0"
        )

        # Domain-specific node categories
        self._domain_categories = {
            "organizational": ["department", "team", "role", "process", "policy"],
            "technical": ["system", "service", "database", "network", "interface"],
            "ecosystem": ["species", "habitat", "resource", "climate", "population"],
            "social": ["community", "institution", "norm", "behavior", "relationship"]
        }

        # Propagation speed mappings (in hours)
        self._speed_hours = {
            PropagationSpeed.IMMEDIATE: 0,
            PropagationSpeed.RAPID: 4,
            PropagationSpeed.MODERATE: 24,
            PropagationSpeed.SLOW: 168,  # 1 week
            PropagationSpeed.GRADUAL: 720  # 1 month
        }

        # Effect magnitude values
        self._magnitude_values = {
            EffectMagnitude.NEGLIGIBLE: 0.1,
            EffectMagnitude.MINOR: 0.3,
            EffectMagnitude.MODERATE: 0.5,
            EffectMagnitude.SIGNIFICANT: 0.7,
            EffectMagnitude.MAJOR: 0.85,
            EffectMagnitude.CRITICAL: 1.0
        }

    async def analyze(self, context: ImpactPropagationContext) -> ImpactPropagationResult:
        """
        Analyze impact propagation through the system.

        Args:
            context: The impact propagation context

        Returns:
            Complete analysis of cascading effects
        """
        start_time = datetime.utcnow()

        # Build or enhance the network
        network = await self._build_network(context)

        # Identify initial impacts
        primary_impacts = await self._identify_primary_impacts(context, network)

        # Trace propagation paths
        propagation_paths = await self._trace_propagation_paths(
            network, primary_impacts, context.analysis_depth
        )

        # Detect feedback loops
        feedback_loops = await self._detect_feedback_loops(network)

        # Identify cascade effects
        cascade_effects = await self._identify_cascade_effects(
            network, propagation_paths, context.time_horizon
        )

        # Assess risks
        risk_areas = await self._assess_risk_areas(
            network, propagation_paths, feedback_loops, context.risk_tolerance
        )

        # Find intervention points
        intervention_points = await self._find_intervention_points(
            network, risk_areas, propagation_paths
        )

        # Identify critical nodes
        critical_nodes = await self._identify_critical_nodes(network)

        # Generate timeline projection
        timeline = await self._project_timeline(
            primary_impacts, cascade_effects, context.time_horizon
        )

        # Develop mitigation strategies
        mitigation_strategies = await self._develop_mitigation_strategies(
            risk_areas, intervention_points, context.risk_tolerance
        )

        # Calculate system resilience
        resilience_score = await self._calculate_resilience(network, critical_nodes)

        # Generate visualization data
        viz_data = await self._generate_visualization_data(
            network, propagation_paths, feedback_loops
        )

        # Extract key insights
        key_insights = await self._extract_key_insights(
            primary_impacts, cascade_effects, risk_areas, resilience_score
        )

        # Calculate confidence
        confidence = self._calculate_confidence(
            context.complexity_level,
            len(network["nodes"]),
            len(feedback_loops)
        )

        processing_time = int((datetime.utcnow() - start_time).total_seconds() * 1000)

        return ImpactPropagationResult(
            input_scenario=context.scenario,
            impact_network=network["nodes"],
            connections=network["edges"],
            primary_impacts=primary_impacts,
            propagation_paths=propagation_paths,
            feedback_loops=feedback_loops,
            cascade_effects=cascade_effects,
            risk_areas=risk_areas,
            intervention_points=intervention_points,
            critical_nodes=critical_nodes,
            timeline_projection=timeline,
            mitigation_strategies=mitigation_strategies,
            amplification_risks=[
                f"Positive feedback in {loop.loop_id} could amplify impacts"
                for loop in feedback_loops
                if loop.feedback_type == FeedbackType.POSITIVE
            ],
            system_resilience_score=resilience_score,
            visualization_data=viz_data,
            key_insights=key_insights,
            confidence_score=confidence,
            processing_time_ms=processing_time
        )

    async def _build_network(self, context: ImpactPropagationContext) -> dict[str, Any]:
        """Build the impact network from context or generate it"""
        if context.system_nodes and context.system_edges:
            # Use provided network
            nodes = {node.id: node for node in context.system_nodes}
            edges = context.system_edges
        else:
            # Generate network based on domain and scenario
            nodes, edges = await self._generate_network(context)

        return {"nodes": nodes, "edges": edges}

    async def _generate_network(
        self, context: ImpactPropagationContext
    ) -> tuple[dict[str, Node], list[Edge]]:
        """Generate a network based on the scenario and domain"""
        nodes = {}
        edges = []

        # Extract entities from scenario
        entities = await self._extract_entities(context.scenario, context.domain_context)

        # Create nodes for entities
        for i, entity in enumerate(entities[:20]):  # Limit to 20 nodes
            node = Node(
                id=f"node_{i}",
                name=entity["name"],
                category=entity["category"],
                sensitivity=entity.get("sensitivity", 0.5),
                resilience=entity.get("resilience", 0.5),
                influence_radius=entity.get("influence", 2)
            )
            nodes[node.id] = node

        # Create edges based on relationships
        node_ids = list(nodes.keys())
        for i, source_id in enumerate(node_ids):
            # Connect to nearby nodes
            for j in range(i + 1, min(i + 4, len(node_ids))):
                target_id = node_ids[j]
                edge = Edge(
                    source_id=source_id,
                    target_id=target_id,
                    relationship_type="influences",
                    strength=0.6,
                    propagation_speed=PropagationSpeed.MODERATE,
                    bidirectional=j - i == 1  # Adjacent nodes have bidirectional influence
                )
                edges.append(edge)

        return nodes, edges

    async def _extract_entities(self, scenario: str, domain: str | None) -> list[dict[str, Any]]:
        """Extract entities from the scenario description"""
        # Simplified entity extraction
        entities = []

        # Common keywords by domain
        if domain == "organizational":
            keywords = ["department", "team", "process", "employee", "manager", "system"]
            categories = self._domain_categories["organizational"]
        elif domain == "technical":
            keywords = ["system", "database", "api", "service", "server", "network"]
            categories = self._domain_categories["technical"]
        else:
            keywords = ["element", "component", "factor", "aspect", "part"]
            categories = ["general"]

        # Extract entities based on keywords (simplified)
        scenario_lower = scenario.lower()
        for i, keyword in enumerate(keywords):
            if keyword in scenario_lower:
                entities.append({
                    "name": f"{keyword.title()} {i+1}",
                    "category": categories[i % len(categories)],
                    "sensitivity": 0.5 + (i * 0.1) % 0.5,
                    "resilience": 0.7 - (i * 0.1) % 0.5,
                    "influence": 2 + i % 3
                })

        # Ensure at least some entities
        if len(entities) < 5:
            for i in range(5 - len(entities)):
                entities.append({
                    "name": f"Element {i+1}",
                    "category": "general",
                    "sensitivity": 0.5,
                    "resilience": 0.5,
                    "influence": 2
                })

        return entities

    async def _identify_primary_impacts(
        self, context: ImpactPropagationContext, network: dict[str, Any]
    ) -> list[ImpactEvent]:
        """Identify primary (direct) impacts"""
        primary_impacts = []

        if context.initial_impact:
            primary_impacts.append(context.initial_impact)
        else:
            # Generate primary impact based on scenario
            first_node_id = list(network["nodes"].keys())[0]
            primary_impact = ImpactEvent(
                node_id=first_node_id,
                impact_type=ImpactType.DIRECT,
                description=f"Initial impact from {context.scenario[:100]}",
                magnitude=EffectMagnitude.SIGNIFICANT,
                probability=1.0,
                time_delay="0 hours"
            )
            primary_impacts.append(primary_impact)

        # Add additional direct impacts based on high sensitivity nodes
        for node_id, node in network["nodes"].items():
            if node.sensitivity > 0.8 and node_id != primary_impacts[0].node_id:
                impact = ImpactEvent(
                    node_id=node_id,
                    impact_type=ImpactType.DIRECT,
                    description=f"High sensitivity of {node.name} to change",
                    magnitude=EffectMagnitude.MODERATE,
                    probability=0.8,
                    time_delay="2 hours"
                )
                primary_impacts.append(impact)
                if len(primary_impacts) >= 3:
                    break

        return primary_impacts

    async def _trace_propagation_paths(
        self, network: dict[str, Any], impacts: list[ImpactEvent], max_depth: int
    ) -> list[PropagationPath]:
        """Trace how impacts propagate through the network"""
        paths = []
        edges = network["edges"]

        # Build graph for path finding
        graph = nx.DiGraph()
        for edge in edges:
            graph.add_edge(
                edge.source_id,
                edge.target_id,
                weight=1.0 - edge.strength,
                speed=edge.propagation_speed
            )
            if edge.bidirectional:
                graph.add_edge(
                    edge.target_id,
                    edge.source_id,
                    weight=1.0 - edge.strength,
                    speed=edge.propagation_speed
                )

        # Trace paths from each impact
        for impact in impacts[:5]:  # Limit to first 5 impacts
            if impact.node_id not in graph:
                continue

            # Find reachable nodes within max_depth
            reachable = nx.single_source_shortest_path_length(
                graph, impact.node_id, cutoff=max_depth
            )

            # Create paths to significant destinations
            for target, distance in reachable.items():
                if distance > 1 and target != impact.node_id:
                    try:
                        path_nodes = nx.shortest_path(graph, impact.node_id, target)
                        if len(path_nodes) >= 2:
                            # Calculate cumulative effect
                            attenuation = 0.9 ** (len(path_nodes) - 1)
                            magnitude_value = self._magnitude_values[impact.magnitude]
                            final_magnitude_value = magnitude_value * attenuation

                            # Map back to magnitude enum
                            final_magnitude = self._value_to_magnitude(final_magnitude_value)

                            # Calculate propagation time
                            total_hours = sum(
                                self._speed_hours[
                                    graph[path_nodes[i]][path_nodes[i+1]].get(
                                        "speed", PropagationSpeed.MODERATE
                                    )
                                ]
                                for i in range(len(path_nodes) - 1)
                            )

                            path = PropagationPath(
                                path_nodes=path_nodes,
                                total_impact=final_magnitude,
                                propagation_time=f"{total_hours} hours",
                                attenuation_factor=1.0 - attenuation,
                                critical_points=path_nodes[1:-1][:2]  # Middle nodes are critical
                            )
                            paths.append(path)

                            if len(paths) >= 10:  # Limit total paths
                                return paths
                    except nx.NetworkXNoPath:
                        continue

        return paths

    async def _detect_feedback_loops(self, network: dict[str, Any]) -> list[FeedbackLoop]:
        """Detect feedback loops in the network"""
        loops = []
        edges = network["edges"]

        # Build graph
        graph = nx.DiGraph()
        for edge in edges:
            graph.add_edge(edge.source_id, edge.target_id, edge=edge)
            if edge.bidirectional:
                graph.add_edge(edge.target_id, edge.source_id, edge=edge)

        # Find cycles
        try:
            cycles = list(nx.simple_cycles(graph))

            for cycle in cycles[:5]:  # Limit to 5 loops
                if len(cycle) >= 2:
                    # Add first node again to close the loop
                    loop_nodes = cycle + [cycle[0]]

                    # Determine feedback type based on edge count
                    positive_edges = sum(
                        1 for i in range(len(cycle))
                        if graph[cycle[i]][cycle[(i+1) % len(cycle)]].get("edge").strength > 0.7
                    )

                    if positive_edges > len(cycle) / 2:
                        feedback_type = FeedbackType.POSITIVE
                        amplification = 1.1
                    else:
                        feedback_type = FeedbackType.NEGATIVE
                        amplification = 0.9

                    loop = FeedbackLoop(
                        loop_nodes=loop_nodes,
                        feedback_type=feedback_type,
                        strength=0.6 + len(cycle) * 0.05,
                        cycle_time=f"{len(cycle) * 12} hours",
                        stability_threshold=0.85,
                        amplification_rate=amplification
                    )
                    loops.append(loop)
        except (nx.NetworkXError, ValueError):
            # No cycles found or graph issues
            pass

        return loops

    async def _identify_cascade_effects(
        self, network: dict[str, Any], paths: list[PropagationPath], time_horizon: str | None
    ) -> list[ImpactEvent]:
        """Identify cascading and emergent effects"""
        cascade_effects = []

        # Track affected nodes
        affected_nodes = set()
        for path in paths:
            affected_nodes.update(path.path_nodes[1:])  # Exclude origin

        # Generate cascade effects for heavily affected nodes
        node_impact_count = {}
        for node_id in affected_nodes:
            count = sum(1 for path in paths if node_id in path.path_nodes)
            node_impact_count[node_id] = count

        # Create cascade effects for nodes hit by multiple paths
        for node_id, count in sorted(node_impact_count.items(), key=lambda x: x[1], reverse=True)[:5]:
            if count >= 2:
                node = network["nodes"].get(node_id)
                if node:
                    effect = ImpactEvent(
                        node_id=node_id,
                        impact_type=ImpactType.CASCADE if count < 3 else ImpactType.EMERGENT,
                        description=f"Compound effects on {node.name} from multiple impact paths",
                        magnitude=EffectMagnitude.MODERATE if count < 3 else EffectMagnitude.SIGNIFICANT,
                        probability=0.7 + count * 0.05,
                        time_delay=f"{count * 6} hours"
                    )
                    cascade_effects.append(effect)

        return cascade_effects

    async def _assess_risk_areas(
        self,
        network: dict[str, Any],
        paths: list[PropagationPath],
        loops: list[FeedbackLoop],
        risk_tolerance: str
    ) -> list[RiskArea]:
        """Assess areas of risk in the network"""
        risk_areas = []

        # Risk from critical path dependencies
        critical_nodes = set()
        for path in paths:
            critical_nodes.update(path.critical_points)

        if critical_nodes:
            risk = RiskArea(
                description="Single points of failure in critical propagation paths",
                affected_nodes=list(critical_nodes)[:10],
                risk_level="high" if risk_tolerance == "low" else "medium",
                trigger_conditions=[
                    "Failure of any critical node",
                    "Overload of critical connections"
                ],
                mitigation_strategies=[
                    "Add redundancy to critical paths",
                    "Strengthen resilience of critical nodes",
                    "Create alternative pathways"
                ]
            )
            risk_areas.append(risk)

        # Risk from positive feedback loops
        positive_loops = [l for l in loops if l.feedback_type == FeedbackType.POSITIVE]
        if positive_loops:
            risk = RiskArea(
                description="Amplifying feedback loops could cause runaway effects",
                affected_nodes=list(set(
                    node for loop in positive_loops for node in loop.loop_nodes[:-1]
                ))[:10],
                risk_level="critical" if len(positive_loops) > 2 else "high",
                trigger_conditions=[
                    "Initial disturbance in feedback loop",
                    "Threshold breach in loop nodes"
                ],
                mitigation_strategies=[
                    "Install circuit breakers in feedback paths",
                    "Monitor loop activity closely",
                    "Prepare dampening interventions"
                ],
                early_warning_indicators=[
                    "Increasing activity in loop nodes",
                    "Accelerating change rates"
                ]
            )
            risk_areas.append(risk)

        # Risk from low resilience clusters
        low_resilience_nodes = [
            node_id for node_id, node in network["nodes"].items()
            if node.resilience < 0.3
        ]
        if low_resilience_nodes:
            risk = RiskArea(
                description="Low resilience nodes vulnerable to disruption",
                affected_nodes=low_resilience_nodes[:10],
                risk_level="high",
                trigger_conditions=[
                    "Any significant impact",
                    "Cascading effects from connected nodes"
                ],
                mitigation_strategies=[
                    "Strengthen resilience through redundancy",
                    "Implement protective buffers",
                    "Develop rapid recovery procedures"
                ]
            )
            risk_areas.append(risk)

        return risk_areas

    async def _find_intervention_points(
        self,
        network: dict[str, Any],
        risks: list[RiskArea],
        paths: list[PropagationPath]
    ) -> list[InterventionPoint]:
        """Find optimal points for intervention"""
        interventions = []

        # Find nodes that appear in multiple paths
        path_frequency = {}
        for path in paths:
            for node_id in path.path_nodes[1:-1]:  # Exclude endpoints
                path_frequency[node_id] = path_frequency.get(node_id, 0) + 1

        # High-frequency nodes are good intervention points
        for node_id, frequency in sorted(path_frequency.items(), key=lambda x: x[1], reverse=True)[:5]:
            node = network["nodes"].get(node_id)
            if node:
                intervention = InterventionPoint(
                    node_id=node_id,
                    intervention_type="dampen" if frequency > 3 else "redirect",
                    effectiveness=0.7 + frequency * 0.05,
                    cost=f"Medium - affects {frequency} propagation paths",
                    side_effects=[
                        f"May slow legitimate information flow through {node.name}",
                        "Requires coordination with connected nodes"
                    ],
                    timing_critical=True if frequency > 4 else False,
                    implementation_time="2-4 hours"
                )
                interventions.append(intervention)

        # Add interventions for high-risk areas
        for risk in risks[:2]:
            if risk.risk_level in ["high", "critical"] and risk.affected_nodes:
                intervention = InterventionPoint(
                    node_id=risk.affected_nodes[0],
                    intervention_type="block" if risk.risk_level == "critical" else "dampen",
                    effectiveness=0.85,
                    cost="High - requires significant changes",
                    side_effects=["Disruption to normal operations"],
                    timing_critical=True
                )
                interventions.append(intervention)

        return interventions

    async def _identify_critical_nodes(self, network: dict[str, Any]) -> list[str]:
        """Identify nodes critical for system stability"""
        # Build graph for centrality analysis
        graph = nx.DiGraph()
        for edge in network["edges"]:
            graph.add_edge(edge.source_id, edge.target_id, weight=edge.strength)
            if edge.bidirectional:
                graph.add_edge(edge.target_id, edge.source_id, weight=edge.strength)

        # Calculate centrality measures
        if len(graph.nodes()) > 0:
            try:
                betweenness = nx.betweenness_centrality(graph)
                degree = nx.degree_centrality(graph)

                # Combine measures to identify critical nodes
                criticality = {}
                for node in graph.nodes():
                    node_obj = network["nodes"].get(node)
                    if node_obj:
                        criticality[node] = (
                            betweenness.get(node, 0) * 0.5 +
                            degree.get(node, 0) * 0.3 +
                            (1.0 - node_obj.resilience) * 0.2
                        )

                # Return top critical nodes
                critical_nodes = sorted(criticality.items(), key=lambda x: x[1], reverse=True)
                return [node[0] for node in critical_nodes[:10]]
            except (nx.NetworkXError, KeyError, ValueError):
                # Fallback if graph analysis fails
                return list(network["nodes"].keys())[:5]

        return []

    async def _project_timeline(
        self,
        primary: list[ImpactEvent],
        cascade: list[ImpactEvent],
        time_horizon: str | None
    ) -> dict[str, list[ImpactEvent]]:
        """Project impacts over time"""
        timeline = {
            "immediate": [],
            "short_term": [],  # < 24 hours
            "medium_term": [],  # 1-7 days
            "long_term": []    # > 7 days
        }

        all_impacts = primary + cascade

        for impact in all_impacts:
            # Parse time delay
            if not impact.time_delay or impact.time_delay == "0 hours":
                timeline["immediate"].append(impact)
            else:
                try:
                    hours = int(impact.time_delay.split()[0])
                    if hours < 24:
                        timeline["short_term"].append(impact)
                    elif hours < 168:  # 7 days
                        timeline["medium_term"].append(impact)
                    else:
                        timeline["long_term"].append(impact)
                except (KeyError, ValueError):
                    timeline["short_term"].append(impact)

        return timeline

    async def _develop_mitigation_strategies(
        self,
        risks: list[RiskArea],
        interventions: list[InterventionPoint],
        risk_tolerance: str
    ) -> list[str]:
        """Develop mitigation strategies"""
        strategies = []

        # Core strategies based on risk tolerance
        if risk_tolerance == "low":
            strategies.extend([
                "Implement redundancy at all critical nodes",
                "Establish continuous monitoring with real-time alerts",
                "Pre-position intervention resources at key points"
            ])
        else:
            strategies.extend([
                "Monitor critical paths for early warning signs",
                "Develop rapid response procedures"
            ])

        # Risk-specific strategies
        for risk in risks[:3]:
            if risk.mitigation_strategies:
                strategies.extend(risk.mitigation_strategies[:2])

        # Intervention-based strategies
        if interventions:
            strategies.append(
                f"Prepare to implement {len(interventions)} intervention points within critical time windows"
            )

        # Remove duplicates and limit
        unique_strategies = []
        for strategy in strategies:
            if strategy not in unique_strategies:
                unique_strategies.append(strategy)
                if len(unique_strategies) >= 8:
                    break

        return unique_strategies

    async def _calculate_resilience(
        self, network: dict[str, Any], critical_nodes: list[str]
    ) -> float:
        """Calculate overall system resilience"""
        nodes = network["nodes"]

        if not nodes:
            return 0.5

        # Base resilience from all nodes
        avg_resilience = sum(node.resilience for node in nodes.values()) / len(nodes)

        # Adjust for critical nodes
        if critical_nodes:
            critical_resilience = sum(
                nodes[node_id].resilience
                for node_id in critical_nodes
                if node_id in nodes
            ) / len(critical_nodes)

            # Weight critical nodes more heavily
            system_resilience = avg_resilience * 0.6 + critical_resilience * 0.4
        else:
            system_resilience = avg_resilience

        # Adjust for network connectivity
        edge_count = len(network["edges"])
        node_count = len(nodes)
        connectivity_factor = min(edge_count / (node_count * 2), 1.0)

        # Higher connectivity can help or hurt resilience
        if connectivity_factor > 0.7:
            # Too connected - vulnerabilities spread easily
            system_resilience *= 0.9
        elif connectivity_factor < 0.3:
            # Too isolated - no redundancy
            system_resilience *= 0.8

        return round(system_resilience, 3)

    async def _generate_visualization_data(
        self,
        network: dict[str, Any],
        paths: list[PropagationPath],
        loops: list[FeedbackLoop]
    ) -> dict[str, Any]:
        """Generate data for network visualization"""
        viz_data = {
            "nodes": [],
            "edges": [],
            "highlights": {
                "critical_paths": [],
                "feedback_loops": [],
                "intervention_points": []
            }
        }

        # Node data
        for node_id, node in network["nodes"].items():
            viz_data["nodes"].append({
                "id": node_id,
                "label": node.name,
                "category": node.category,
                "size": 10 + node.influence_radius * 5,
                "color": self._get_node_color(node)
            })

        # Edge data
        for edge in network["edges"]:
            viz_data["edges"].append({
                "source": edge.source_id,
                "target": edge.target_id,
                "weight": edge.strength,
                "type": edge.relationship_type,
                "bidirectional": edge.bidirectional
            })

        # Highlight critical paths
        for path in paths[:5]:
            viz_data["highlights"]["critical_paths"].append(path.path_nodes)

        # Highlight feedback loops
        for loop in loops[:3]:
            viz_data["highlights"]["feedback_loops"].append(loop.loop_nodes)

        return viz_data

    async def _extract_key_insights(
        self,
        primary: list[ImpactEvent],
        cascade: list[ImpactEvent],
        risks: list[RiskArea],
        resilience: float
    ) -> list[str]:
        """Extract key insights from the analysis"""
        insights = []

        # Primary impact insight
        if primary:
            insights.append(
                f"Initial impact will directly affect {len(primary)} nodes with "
                f"{primary[0].magnitude} magnitude"
            )

        # Cascade insight
        if cascade:
            emergent = [e for e in cascade if e.impact_type == ImpactType.EMERGENT]
            if emergent:
                insights.append(
                    f"Analysis reveals {len(emergent)} emergent effects not immediately "
                    "apparent from initial conditions"
                )
            else:
                insights.append(
                    f"Cascading effects will impact {len(cascade)} additional nodes "
                    "through network propagation"
                )

        # Risk insight
        critical_risks = [r for r in risks if r.risk_level == "critical"]
        if critical_risks:
            insights.append(
                f"CRITICAL: {len(critical_risks)} high-severity risks identified "
                "requiring immediate attention"
            )
        elif risks:
            insights.append(
                f"{len(risks)} risk areas identified with mitigation strategies available"
            )

        # Resilience insight
        if resilience < 0.3:
            insights.append(
                "System shows LOW resilience - significant vulnerability to disruption"
            )
        elif resilience > 0.7:
            insights.append(
                "System demonstrates HIGH resilience with good recovery capacity"
            )
        else:
            insights.append(
                f"System resilience is MODERATE ({resilience:.1%}) with room for improvement"
            )

        # Timing insight
        insights.append(
            "Time-critical interventions needed within first 24 hours for maximum effectiveness"
        )

        return insights[:5]  # Return top 5 insights

    def _value_to_magnitude(self, value: float) -> EffectMagnitude:
        """Convert numeric value to magnitude enum"""
        if value <= 0.1:
            return EffectMagnitude.NEGLIGIBLE
        elif value <= 0.3:
            return EffectMagnitude.MINOR
        elif value <= 0.5:
            return EffectMagnitude.MODERATE
        elif value <= 0.7:
            return EffectMagnitude.SIGNIFICANT
        elif value <= 0.85:
            return EffectMagnitude.MAJOR
        else:
            return EffectMagnitude.CRITICAL

    def _get_node_color(self, node: Node) -> str:
        """Get visualization color for node based on properties"""
        if node.resilience < 0.3:
            return "#ff4444"  # Red for vulnerable
        elif node.sensitivity > 0.7:
            return "#ff8844"  # Orange for sensitive
        elif node.influence_radius >= 3:
            return "#4444ff"  # Blue for influential
        else:
            return "#44ff44"  # Green for stable

    def _calculate_confidence(
        self, complexity: ComplexityLevel, node_count: int, loop_count: int
    ) -> float:
        """Calculate confidence in the analysis"""
        # Base confidence by complexity
        base_confidence = {
            ComplexityLevel.SIMPLE: 0.9,
            ComplexityLevel.MODERATE: 0.8,
            ComplexityLevel.COMPLEX: 0.7,
            ComplexityLevel.VERY_COMPLEX: 0.6
        }

        confidence = base_confidence.get(complexity, 0.7)

        # Adjust for network size
        if node_count > 50:
            confidence *= 0.9
        elif node_count < 10:
            confidence *= 0.95

        # Adjust for feedback loops
        if loop_count > 5:
            confidence *= 0.9  # Complex dynamics harder to predict

        return round(confidence, 2)
