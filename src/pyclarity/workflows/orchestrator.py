"""
Tool Orchestrator for PyClarity Workflows

Handles dependency resolution and execution planning using graph algorithms.
"""

import logging
from collections import defaultdict, deque
from typing import Any, Dict, List, Set, Tuple

import networkx as nx

from .models import ExecutionPlan, ToolConfig, ToolDependency, WorkflowConfig

logger = logging.getLogger(__name__)


class ToolOrchestrator:
    """
    Orchestrates tool execution by resolving dependencies and creating execution plans.

    Uses NetworkX for graph operations to handle complex dependency scenarios.
    """

    def create_execution_plan(self, config: WorkflowConfig) -> ExecutionPlan:
        """
        Create an execution plan from workflow configuration.

        Args:
            config: Workflow configuration with tools and dependencies

        Returns:
            ExecutionPlan with parallel execution batches
        """
        # Build dependency graph
        graph = self._build_dependency_graph(config)

        # Check for cycles (should already be validated, but double-check)
        if not nx.is_directed_acyclic_graph(graph):
            cycles = list(nx.simple_cycles(graph))
            raise ValueError(f"Circular dependencies detected: {cycles}")

        # Perform topological sort to get execution order
        execution_order = self._calculate_execution_batches(graph)

        # Extract dependencies for the plan
        dependencies = self._extract_dependencies(config)

        # Estimate execution time
        estimated_time = self._estimate_execution_time(config, execution_order)

        return ExecutionPlan(
            workflow_config=config,
            execution_order=execution_order,
            dependencies=dependencies,
            estimated_time_seconds=estimated_time
        )

    def _build_dependency_graph(self, config: WorkflowConfig) -> nx.DiGraph:
        """Build a directed graph of tool dependencies"""
        graph = nx.DiGraph()

        # Add all tools as nodes
        for tool in config.tools:
            graph.add_node(tool.name, config=tool)

        # Add edges for dependencies
        for tool in config.tools:
            for dep in tool.depends_on:
                # Edge from dependency to dependent (dep must run before tool)
                graph.add_edge(dep, tool.name)

        return graph

    def _calculate_execution_batches(self, graph: nx.DiGraph) -> list[list[str]]:
        """
        Calculate batches of tools that can execute in parallel.

        Uses Kahn's algorithm variant to group tools by levels.
        """
        # Create a copy to modify
        g = graph.copy()
        batches = []

        while g:
            # Find all nodes with no incoming edges (can execute now)
            ready_nodes = [n for n in g.nodes() if g.in_degree(n) == 0]

            if not ready_nodes:
                # This shouldn't happen if graph is DAG
                raise RuntimeError("No ready nodes found - possible circular dependency")

            # Add as a batch
            batches.append(ready_nodes)

            # Remove these nodes from graph
            g.remove_nodes_from(ready_nodes)

        return batches

    def _extract_dependencies(self, config: WorkflowConfig) -> list[ToolDependency]:
        """Extract all tool dependencies"""
        dependencies = []

        for tool in config.tools:
            for dep in tool.depends_on:
                dependencies.append(
                    ToolDependency(
                        source=dep,
                        target=tool.name,
                        data_mapping=None  # TODO: Add data mapping configuration
                    )
                )

        return dependencies

    def _estimate_execution_time(self, config: WorkflowConfig,
                               execution_order: list[list[str]]) -> float:
        """Estimate total execution time based on execution plan"""
        total_time = 0.0

        # Map tool names to configs for easy lookup
        tool_map = {tool.name: tool for tool in config.tools}

        for batch in execution_order:
            # In parallel execution, batch time is the max of individual times
            if config.parallel_execution and len(batch) > 1:
                batch_time = max(
                    tool_map[tool_name].timeout_seconds
                    for tool_name in batch
                )
            else:
                # Sequential execution
                batch_time = sum(
                    tool_map[tool_name].timeout_seconds
                    for tool_name in batch
                )

            total_time += batch_time

        # Add some overhead for orchestration
        total_time *= 1.1

        return total_time

    def optimize_execution_plan(self, plan: ExecutionPlan,
                              resource_constraints: dict[str, Any]) -> ExecutionPlan:
        """
        Optimize execution plan based on resource constraints.

        Args:
            plan: Original execution plan
            resource_constraints: Constraints like max_parallel, memory_limit, etc.

        Returns:
            Optimized execution plan
        """
        max_parallel = resource_constraints.get('max_parallel', 5)

        # Split large batches if they exceed max_parallel
        optimized_batches = []
        for batch in plan.execution_order:
            if len(batch) <= max_parallel:
                optimized_batches.append(batch)
            else:
                # Split into smaller batches
                for i in range(0, len(batch), max_parallel):
                    optimized_batches.append(batch[i:i + max_parallel])

        # Update plan with optimized batches
        plan.execution_order = optimized_batches

        # Recalculate estimated time
        plan.estimated_time_seconds = self._estimate_execution_time(
            plan.workflow_config,
            optimized_batches
        )

        return plan

    def validate_data_flow(self, config: WorkflowConfig) -> list[str]:
        """
        Validate that data can flow properly between dependent tools.

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []

        # For now, basic validation that dependencies exist
        # TODO: Add more sophisticated data contract validation

        tool_names = {tool.name for tool in config.tools}
        for tool in config.tools:
            for dep in tool.depends_on:
                if dep not in tool_names:
                    errors.append(
                        f"Tool '{tool.name}' depends on non-existent tool '{dep}'"
                    )

        return errors

    def suggest_parallelization(self, config: WorkflowConfig) -> list[tuple[str, str]]:
        """
        Suggest tools that could be parallelized but aren't due to false dependencies.

        Returns:
            List of (tool1, tool2) pairs that could potentially run in parallel
        """
        suggestions = []
        graph = self._build_dependency_graph(config)

        # Find tools at the same level that don't depend on each other
        batches = self._calculate_execution_batches(graph)

        for i, batch in enumerate(batches):
            if len(batch) > 1:
                # These are already parallel
                continue

            # Check if tools in next batch could be moved up
            if i + 1 < len(batches):
                for tool in batches[i + 1]:
                    # Check if this tool only depends on tools before current batch
                    tool_deps = set(config.tools[tool].depends_on)
                    prior_tools = set()
                    for j in range(i):
                        prior_tools.update(batches[j])

                    if tool_deps.issubset(prior_tools):
                        suggestions.append((batch[0], tool))

        return suggestions
