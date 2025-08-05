"""
Workflow Models for PyClarity

Pydantic models for workflow configuration, state management, and execution planning.
"""

import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set

from pydantic import BaseModel, Field, field_validator, model_validator


class WorkflowStatus(str, Enum):
    """Workflow execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PARTIAL = "partial"  # Some tools succeeded, some failed


class ToolExecutionStatus(str, Enum):
    """Individual tool execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
    RETRYING = "retrying"


class ToolType(str, Enum):
    """Type of tool in the workflow"""
    COGNITIVE = "cognitive"  # PyClarity cognitive tools
    PROMPT = "prompt"  # Prompt-based tools
    LLM = "llm"  # Direct LLM calls
    CUSTOM = "custom"  # Custom tool implementations


class ToolConfig(BaseModel):
    """Configuration for a single tool in the workflow"""
    name: str = Field(..., description="Name of the tool")
    tool_type: ToolType = Field(default=ToolType.COGNITIVE, description="Type of tool")
    depends_on: list[str] = Field(default_factory=list, description="Tools this depends on")
    config: dict[str, Any] = Field(default_factory=dict, description="Tool-specific configuration")
    timeout_seconds: int = Field(default=30, description="Maximum execution time")
    retry_count: int = Field(default=2, description="Number of retries on failure")

    # Prompt-specific fields
    prompt_template: str | None = Field(None, description="Prompt template for PROMPT tools")
    llm_config: dict[str, Any] | None = Field(None, description="LLM configuration for LLM tools")

    @model_validator(mode='after')
    def validate_tool_name(self) -> 'ToolConfig':
        """Ensure tool name is valid based on tool type"""
        if self.tool_type == ToolType.COGNITIVE:
            valid_tools = {
                'mental_models', 'sequential_thinking', 'decision_framework',
                'scientific_method', 'design_patterns', 'programming_paradigms',
                'debugging_approaches', 'visual_reasoning', 'structured_argumentation',
                'metacognitive_monitoring', 'collaborative_reasoning', 'impact_propagation',
                'iterative_validation', 'multi_perspective_analysis', 'sequential_readiness_assessment',
                'triple_constraint_optimization'
            }
            if self.name not in valid_tools:
                raise ValueError(f"Unknown cognitive tool: {self.name}. Valid tools: {valid_tools}")

        # Other tool types can have any name
        return self


class WorkflowConfig(BaseModel):
    """Configuration for a complete workflow"""
    name: str = Field(..., description="Workflow name")
    description: str | None = Field(None, description="Workflow description")
    tools: list[ToolConfig] = Field(..., description="Tools to execute")
    parallel_execution: bool = Field(default=True, description="Allow parallel execution")
    max_parallel: int = Field(default=5, description="Maximum parallel executions")
    timeout_seconds: int = Field(default=300, description="Total workflow timeout")

    def validate_dependencies(self) -> None:
        """Validate that all dependencies reference valid tools"""
        tool_names = {tool.name for tool in self.tools}
        for tool in self.tools:
            for dep in tool.depends_on:
                if dep not in tool_names:
                    raise ValueError(f"Tool '{tool.name}' depends on unknown tool '{dep}'")

    def has_circular_dependency(self) -> bool:
        """Check for circular dependencies using DFS"""
        def visit(tool_name: str, visited: set[str], rec_stack: set[str]) -> bool:
            visited.add(tool_name)
            rec_stack.add(tool_name)

            tool = next((t for t in self.tools if t.name == tool_name), None)
            if tool:
                for dep in tool.depends_on:
                    if dep not in visited:
                        if visit(dep, visited, rec_stack):
                            return True
                    elif dep in rec_stack:
                        return True

            rec_stack.remove(tool_name)
            return False

        visited = set()
        rec_stack = set()

        for tool in self.tools:
            if tool.name not in visited:
                if visit(tool.name, visited, rec_stack):
                    return True
        return False


class ToolDependency(BaseModel):
    """Represents a dependency between tools"""
    source: str = Field(..., description="Source tool name")
    target: str = Field(..., description="Target tool name")
    data_mapping: dict[str, str] | None = Field(
        None,
        description="How to map output from source to input of target"
    )


class ToolExecution(BaseModel):
    """State of a single tool execution"""
    tool_name: str
    status: ToolExecutionStatus = ToolExecutionStatus.PENDING
    started_at: datetime | None = None
    completed_at: datetime | None = None
    input_data: dict[str, Any] | None = None
    output_data: dict[str, Any] | None = None
    error: str | None = None
    retry_count: int = 0
    execution_time_ms: float | None = None


class WorkflowState(BaseModel):
    """Current state of workflow execution"""
    workflow_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    config: WorkflowConfig
    status: WorkflowStatus = WorkflowStatus.PENDING
    started_at: datetime | None = None
    completed_at: datetime | None = None
    tool_executions: dict[str, ToolExecution] = Field(default_factory=dict)
    error: str | None = None

    def get_ready_tools(self) -> list[str]:
        """Get tools that are ready to execute (dependencies satisfied)"""
        ready = []
        for tool in self.config.tools:
            if self.tool_executions.get(tool.name, ToolExecution(tool_name=tool.name)).status != ToolExecutionStatus.PENDING:
                continue

            # Check if all dependencies are completed
            deps_satisfied = all(
                self.tool_executions.get(dep, ToolExecution(tool_name=dep)).status == ToolExecutionStatus.COMPLETED
                for dep in tool.depends_on
            )

            if deps_satisfied:
                ready.append(tool.name)

        return ready

    def is_complete(self) -> bool:
        """Check if workflow execution is complete"""
        return all(
            self.tool_executions.get(tool.name, ToolExecution(tool_name=tool.name)).status
            in [ToolExecutionStatus.COMPLETED, ToolExecutionStatus.FAILED, ToolExecutionStatus.SKIPPED]
            for tool in self.config.tools
        )


class ExecutionPlan(BaseModel):
    """Execution plan with dependency graph"""
    workflow_config: WorkflowConfig
    execution_order: list[list[str]] = Field(
        ...,
        description="Batches of tools that can run in parallel"
    )
    dependencies: list[ToolDependency] = Field(default_factory=list)
    estimated_time_seconds: float = Field(..., description="Estimated total execution time")

    @classmethod
    def from_workflow_config(cls, config: WorkflowConfig) -> "ExecutionPlan":
        """Generate execution plan from workflow configuration"""
        # This will be implemented in the orchestrator
        # For now, return a simple sequential plan
        return cls(
            workflow_config=config,
            execution_order=[[tool.name] for tool in config.tools],
            dependencies=[],
            estimated_time_seconds=len(config.tools) * 10.0
        )


class WorkflowResult(BaseModel):
    """Result of workflow execution"""
    workflow_id: str
    status: WorkflowStatus
    started_at: datetime
    completed_at: datetime
    execution_time_ms: float
    tool_results: dict[str, Any] = Field(..., description="Results from each tool")
    errors: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    def to_human_readable(self) -> str:
        """Convert results to human-readable format"""
        lines = [
            f"Workflow '{self.workflow_id}' {self.status.value}",
            f"Execution time: {self.execution_time_ms/1000:.2f}s",
            ""
        ]

        if self.tool_results:
            lines.append("Tool Results:")
            for tool, result in self.tool_results.items():
                lines.append(f"  {tool}: {result.get('summary', 'No summary available')}")

        if self.errors:
            lines.append("\nErrors:")
            for error in self.errors:
                lines.append(f"  - {error}")

        return "\n".join(lines)

    def to_agent_format(self) -> dict[str, Any]:
        """Convert results to structured format for agent consumption"""
        return {
            "workflow_id": self.workflow_id,
            "status": self.status.value,
            "execution_time_ms": self.execution_time_ms,
            "tool_results": self.tool_results,
            "errors": self.errors,
            "metadata": {
                **self.metadata,
                "started_at": self.started_at.isoformat(),
                "completed_at": self.completed_at.isoformat()
            }
        }
