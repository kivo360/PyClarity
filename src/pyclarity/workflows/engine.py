"""
Workflow Engine for PyClarity

Acts as a FastMCP client to orchestrate cognitive tool execution.
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from fastmcp import Client
from pydantic import BaseModel, Field

from .iterative_optimizer import IterativeOptimizer
from .models import (
    ExecutionPlan,
    ToolExecution,
    ToolExecutionStatus,
    WorkflowConfig,
    WorkflowResult,
    WorkflowState,
    WorkflowStatus,
)
from .orchestrator import ToolOrchestrator
from .prompt_manager import PromptManager

logger = logging.getLogger(__name__)


class WorkflowEngine:
    """
    Workflow engine that orchestrates cognitive tools via FastMCP client.

    This engine acts as an MCP client, calling tools on the PyClarity MCP server
    and managing the execution flow, state, and dependencies.
    """

    def __init__(self,
                 server_config: dict[str, Any] | None = None,
                 prompt_templates_dir: Path | None = None,
                 enable_iterative_prompting: bool = True):
        """
        Initialize workflow engine with MCP server connection.

        Args:
            server_config: FastMCP client configuration dict
            prompt_templates_dir: Directory containing prompt templates
            enable_iterative_prompting: Enable iterative prompt optimization
        """
        # Default config for local PyClarity server
        # Can be either a path to .py file or a config dict
        if server_config is None:
            # Simple path-based config for stdio transport
            self.server_config = "src/pyclarity/server/mcp_server.py"
        else:
            self.server_config = server_config

        self.orchestrator = ToolOrchestrator()
        self.prompt_manager = PromptManager(templates_dir=prompt_templates_dir)
        self.iterative_optimizer = IterativeOptimizer() if enable_iterative_prompting else None

        self._client: Client | None = None
        self._active_workflows: dict[str, WorkflowState] = {}
        self._embedded_llms: dict[str, Any] = {}  # For future LLM integration

    async def initialize(self) -> None:
        """Initialize MCP client connection"""
        logger.info("Initializing FastMCP client for PyClarity server")

        try:
            # Create FastMCP client - just store config, actual connection happens in context
            self._client = Client(self.server_config)
            logger.info("FastMCP client created successfully")

            # Load prompt templates
            await self.prompt_manager.load_templates()

        except Exception as e:
            logger.error(f"Failed to initialize FastMCP client: {e}")
            raise

    async def close(self) -> None:
        """Close the MCP client connection"""
        # Client connection is managed by async context manager
        # No explicit close needed
        logger.info("WorkflowEngine closed")

    async def execute_workflow(self, config: WorkflowConfig) -> WorkflowResult:
        """
        Execute a workflow based on configuration.

        Args:
            config: Workflow configuration

        Returns:
            WorkflowResult with execution details
        """
        # Validate configuration
        config.validate_dependencies()
        if config.has_circular_dependency():
            raise ValueError("Workflow contains circular dependencies")

        # Create workflow state
        state = WorkflowState(config=config)
        self._active_workflows[state.workflow_id] = state

        # Generate execution plan
        execution_plan = self.orchestrator.create_execution_plan(config)

        # Start execution
        state.status = WorkflowStatus.RUNNING
        state.started_at = datetime.utcnow()

        try:
            # Execute workflow
            await self._execute_plan(state, execution_plan)

            # Mark as completed or partial based on results
            failed_tools = [
                name for name, exec in state.tool_executions.items()
                if exec.status == ToolExecutionStatus.FAILED
            ]

            if failed_tools:
                state.status = WorkflowStatus.PARTIAL
            else:
                state.status = WorkflowStatus.COMPLETED

        except Exception as e:
            state.status = WorkflowStatus.FAILED
            state.error = str(e)
            logger.error(f"Workflow {state.workflow_id} failed: {e}")

        finally:
            state.completed_at = datetime.utcnow()

        # Create result
        result = self._create_result(state)

        # Clean up
        del self._active_workflows[state.workflow_id]

        return result

    async def _execute_plan(self, state: WorkflowState, plan: ExecutionPlan) -> None:
        """Execute the workflow plan"""
        for batch in plan.execution_order:
            # Execute tools in parallel within each batch
            if state.config.parallel_execution and len(batch) > 1:
                await self._execute_parallel_batch(state, batch)
            else:
                # Execute sequentially
                for tool_name in batch:
                    await self._execute_tool(state, tool_name)

                    # Check if we should continue
                    tool_exec = state.tool_executions[tool_name]
                    if tool_exec.status == ToolExecutionStatus.FAILED:
                        # Check if other tools depend on this
                        dependent_tools = self._get_dependent_tools(state.config, tool_name)
                        if dependent_tools:
                            logger.warning(
                                f"Tool {tool_name} failed, skipping dependent tools: {dependent_tools}"
                            )
                            for dep_tool in dependent_tools:
                                state.tool_executions[dep_tool] = ToolExecution(
                                    tool_name=dep_tool,
                                    status=ToolExecutionStatus.SKIPPED,
                                    error=f"Skipped due to {tool_name} failure"
                                )

    async def _execute_parallel_batch(self, state: WorkflowState, batch: list[str]) -> None:
        """Execute a batch of tools in parallel"""
        tasks = []
        for tool_name in batch:
            task = asyncio.create_task(self._execute_tool(state, tool_name))
            tasks.append(task)

        # Wait for all tasks, but don't fail if some fail
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for tool_name, result in zip(batch, results):
            if isinstance(result, Exception):
                logger.error(f"Tool {tool_name} failed in parallel execution: {result}")

    async def _execute_tool(self, state: WorkflowState, tool_name: str) -> None:
        """Execute a single tool"""
        # Get tool config
        tool_config = next(t for t in state.config.tools if t.name == tool_name)

        # Create tool execution record
        tool_exec = ToolExecution(tool_name=tool_name)
        state.tool_executions[tool_name] = tool_exec

        # Prepare input data
        input_data = self._prepare_tool_input(state, tool_config)
        tool_exec.input_data = input_data

        # Execute with retries
        for attempt in range(tool_config.retry_count + 1):
            try:
                tool_exec.status = ToolExecutionStatus.RUNNING
                tool_exec.started_at = datetime.utcnow()

                # Call MCP tool
                result = await self._call_mcp_tool(tool_name, input_data, tool_config.config)

                tool_exec.output_data = result
                tool_exec.status = ToolExecutionStatus.COMPLETED
                tool_exec.completed_at = datetime.utcnow()
                tool_exec.execution_time_ms = (
                    tool_exec.completed_at - tool_exec.started_at
                ).total_seconds() * 1000

                logger.info(f"Tool {tool_name} completed in {tool_exec.execution_time_ms:.2f}ms")
                break

            except Exception as e:
                tool_exec.retry_count = attempt
                if attempt < tool_config.retry_count:
                    tool_exec.status = ToolExecutionStatus.RETRYING
                    logger.warning(f"Tool {tool_name} failed (attempt {attempt + 1}), retrying: {e}")
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                else:
                    tool_exec.status = ToolExecutionStatus.FAILED
                    tool_exec.error = str(e)
                    tool_exec.completed_at = datetime.utcnow()
                    logger.error(f"Tool {tool_name} failed after {attempt + 1} attempts: {e}")

    async def _call_mcp_tool(self, tool_name: str, input_data: dict[str, Any],
                            tool_config: dict[str, Any]) -> dict[str, Any]:
        """
        Call an MCP tool via FastMCP client.

        Supports both cognitive tools and prompt-based tools.
        """
        if not self._client:
            raise RuntimeError("FastMCP client not initialized")

        try:
            # Apply iterative prompting if enabled and applicable
            if self.iterative_optimizer and tool_name in self.iterative_optimizer.supported_tools:
                input_data = await self.iterative_optimizer.optimize_input(
                    tool_name, input_data, tool_config
                )

            # Apply prompt templates if available
            if self.prompt_manager.has_template(tool_name):
                input_data = await self.prompt_manager.apply_template(
                    tool_name, input_data
                )

            # Call the actual MCP tool - must use async context
            async with self._client:
                result = await self._client.call_tool(
                    tool_name,
                    input_data  # Pass as single dict, not unpacked
                )

            # Post-process with iterative optimizer if applicable
            if self.iterative_optimizer and self.iterative_optimizer.should_iterate(result):
                result = await self.iterative_optimizer.iterate_on_result(
                    tool_name, input_data, result
                )

            return result

        except Exception as e:
            logger.error(f"Error calling MCP tool {tool_name}: {e}")
            raise

    def _prepare_tool_input(self, state: WorkflowState, tool_config) -> dict[str, Any]:
        """Prepare input data for a tool based on dependencies"""
        # Base input with problem description
        input_data = {
            "problem": state.config.description or "Workflow analysis",
            "scenario": state.config.description,  # Some tools use 'scenario'
            "complexity_level": tool_config.config.get("complexity_level", "moderate")
        }

        # Add outputs from dependencies with intelligent mapping
        for dep_name in tool_config.depends_on:
            if dep_name in state.tool_executions:
                dep_exec = state.tool_executions[dep_name]
                if dep_exec.output_data:
                    # Map dependency outputs to expected inputs
                    dep_data = dep_exec.output_data

                    # Common mappings between tools
                    if "insights" in dep_data:
                        input_data["domain_knowledge"] = dep_data["insights"]
                    if "recommendations" in dep_data:
                        input_data["constraints"] = dep_data["recommendations"]
                    if "analysis" in dep_data:
                        input_data["previous_analysis"] = dep_data["analysis"]

                    # Store full output for reference
                    input_data[f"{dep_name}_output"] = dep_data

        # Add tool-specific config, filtering out None values
        tool_specific = {k: v for k, v in tool_config.config.items() if v is not None}
        input_data.update(tool_specific)

        return input_data

    def _get_dependent_tools(self, config: WorkflowConfig, tool_name: str) -> list[str]:
        """Get all tools that depend on the given tool"""
        dependents = []
        for tool in config.tools:
            if tool_name in tool.depends_on:
                dependents.append(tool.name)
                # Recursively get tools that depend on this one
                dependents.extend(self._get_dependent_tools(config, tool.name))
        return list(set(dependents))

    def _create_result(self, state: WorkflowState) -> WorkflowResult:
        """Create workflow result from state"""
        tool_results = {}
        errors = []

        for tool_name, exec in state.tool_executions.items():
            if exec.output_data:
                tool_results[tool_name] = exec.output_data
            if exec.error:
                errors.append(f"{tool_name}: {exec.error}")

        if state.error:
            errors.append(f"Workflow: {state.error}")

        execution_time = 0.0
        if state.started_at and state.completed_at:
            execution_time = (state.completed_at - state.started_at).total_seconds() * 1000

        return WorkflowResult(
            workflow_id=state.workflow_id,
            status=state.status,
            started_at=state.started_at or datetime.utcnow(),
            completed_at=state.completed_at or datetime.utcnow(),
            execution_time_ms=execution_time,
            tool_results=tool_results,
            errors=errors,
            metadata={
                "config_name": state.config.name,
                "tools_executed": len(state.tool_executions),
                "tools_succeeded": sum(
                    1 for e in state.tool_executions.values()
                    if e.status == ToolExecutionStatus.COMPLETED
                )
            }
        )

    async def get_workflow_state(self, workflow_id: str) -> WorkflowState | None:
        """Get current state of a workflow"""
        return self._active_workflows.get(workflow_id)

    async def cancel_workflow(self, workflow_id: str) -> bool:
        """Cancel a running workflow"""
        if workflow_id in self._active_workflows:
            state = self._active_workflows[workflow_id]
            state.status = WorkflowStatus.CANCELLED
            state.completed_at = datetime.utcnow()
            return True
        return False
