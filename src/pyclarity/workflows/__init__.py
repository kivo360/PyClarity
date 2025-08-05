"""
PyClarity Workflow Engine

Orchestrates cognitive tools through FastMCP client-server architecture.
Supports prompt templates, iterative optimization, and LLM integration.
"""

from .engine import WorkflowEngine
from .iterative_optimizer import IterativeOptimizer, OptimizationStrategy
from .models import (
    ExecutionPlan,
    ToolConfig,
    ToolDependency,
    ToolExecutionStatus,
    ToolType,
    WorkflowConfig,
    WorkflowResult,
    WorkflowState,
    WorkflowStatus,
)
from .orchestrator import ToolOrchestrator
from .prompt_manager import PromptManager, PromptTemplate

__all__ = [
    # Models
    "WorkflowConfig",
    "WorkflowState",
    "ExecutionPlan",
    "ToolDependency",
    "WorkflowResult",
    "WorkflowStatus",
    "ToolConfig",
    "ToolType",
    "ToolExecutionStatus",
    # Engine components
    "WorkflowEngine",
    "ToolOrchestrator",
    "PromptManager",
    "PromptTemplate",
    "IterativeOptimizer",
    "OptimizationStrategy",
]
