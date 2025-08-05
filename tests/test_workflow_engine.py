"""
Test suite for PyClarity Workflow Engine

Tests workflow orchestration, prompt management, and iterative optimization.
"""

import pytest
import asyncio
from pathlib import Path
from typing import Dict, Any

from pyclarity.workflows import (
    WorkflowEngine,
    WorkflowConfig,
    ToolConfig,
    ToolType,
    WorkflowStatus,
    PromptManager,
    IterativeOptimizer,
    OptimizationStrategy,
)


@pytest.fixture
def sample_workflow_config():
    """Create a sample workflow configuration"""
    return WorkflowConfig(
        name="Product Discovery Workflow",
        description="Analyze a new product idea through multiple cognitive lenses",
        tools=[
            ToolConfig(
                name="sequential_thinking",
                tool_type=ToolType.COGNITIVE,
                config={
                    "complexity_level": "moderate",
                    "reasoning_depth": 5,
                    "enable_branching": True
                }
            ),
            ToolConfig(
                name="mental_models",
                tool_type=ToolType.COGNITIVE,
                depends_on=["sequential_thinking"],
                config={
                    "model_type": "first_principles",
                    "complexity_level": "moderate"
                }
            ),
            ToolConfig(
                name="decision_framework",
                tool_type=ToolType.COGNITIVE,
                depends_on=["mental_models"],
                config={
                    "complexity_level": "complex",
                    "decision_methods": ["weighted_sum", "ahp"]
                }
            ),
        ]
    )


@pytest.fixture
def prompt_workflow_config():
    """Create a workflow with prompt-based tools"""
    return WorkflowConfig(
        name="Prompt-Enhanced Analysis",
        description="Use prompt templates for enhanced analysis",
        tools=[
            ToolConfig(
                name="lean_startup_analysis",
                tool_type=ToolType.PROMPT,
                prompt_template="Apply Lean Startup methodology to analyze: {problem}",
                config={
                    "template_name": "lean_startup"
                }
            ),
            ToolConfig(
                name="summarize_insights",
                tool_type=ToolType.LLM,
                depends_on=["lean_startup_analysis"],
                llm_config={
                    "model": "gpt-4",
                    "temperature": 0.7,
                    "max_tokens": 500
                }
            ),
        ]
    )


class TestWorkflowEngine:
    """Test the WorkflowEngine component"""
    
    @pytest.mark.asyncio
    async def test_engine_initialization(self):
        """Test engine initialization"""
        engine = WorkflowEngine()
        
        assert engine.server_config is not None
        assert engine.orchestrator is not None
        assert engine.prompt_manager is not None
        assert engine.iterative_optimizer is not None
        
    @pytest.mark.asyncio
    async def test_workflow_validation(self, sample_workflow_config):
        """Test workflow configuration validation"""
        # Valid config should not raise
        sample_workflow_config.validate_dependencies()
        assert not sample_workflow_config.has_circular_dependency()
        
        # Test circular dependency detection
        circular_config = WorkflowConfig(
            name="Circular Test",
            tools=[
                ToolConfig(name="tool_a", tool_type=ToolType.CUSTOM, depends_on=["tool_b"]),
                ToolConfig(name="tool_b", tool_type=ToolType.CUSTOM, depends_on=["tool_c"]),
                ToolConfig(name="tool_c", tool_type=ToolType.CUSTOM, depends_on=["tool_a"]),
            ]
        )
        assert circular_config.has_circular_dependency()
        
    @pytest.mark.asyncio
    async def test_execution_plan_creation(self, sample_workflow_config):
        """Test execution plan generation"""
        engine = WorkflowEngine()
        plan = engine.orchestrator.create_execution_plan(sample_workflow_config)
        
        assert plan is not None
        assert len(plan.execution_order) == 3  # Three batches for sequential deps
        assert plan.execution_order[0] == ["sequential_thinking"]
        assert plan.execution_order[1] == ["mental_models"]
        assert plan.execution_order[2] == ["decision_framework"]
        
    @pytest.mark.asyncio
    async def test_parallel_execution_plan(self):
        """Test parallel execution planning"""
        config = WorkflowConfig(
            name="Parallel Test",
            tools=[
                ToolConfig(name="tool_a", tool_type=ToolType.CUSTOM),
                ToolConfig(name="tool_b", tool_type=ToolType.CUSTOM),
                ToolConfig(name="tool_c", tool_type=ToolType.CUSTOM, depends_on=["tool_a", "tool_b"]),
                ToolConfig(name="tool_d", tool_type=ToolType.CUSTOM, depends_on=["tool_a"]),
            ]
        )
        
        engine = WorkflowEngine()
        plan = engine.orchestrator.create_execution_plan(config)
        
        # First batch should have parallel tools
        assert len(plan.execution_order[0]) == 2
        assert set(plan.execution_order[0]) == {"tool_a", "tool_b"}
        
        # Second batch should have tools that depend on first
        assert len(plan.execution_order[1]) == 2
        assert set(plan.execution_order[1]) == {"tool_c", "tool_d"}


class TestPromptManager:
    """Test the PromptManager component"""
    
    @pytest.mark.asyncio
    async def test_prompt_manager_initialization(self):
        """Test prompt manager initialization"""
        manager = PromptManager()
        await manager.load_templates()
        
        # Check built-in templates loaded
        assert len(manager.library.cognitive_tools) > 0
        assert "sequential_thinking" in manager.library.cognitive_tools
        assert "mental_models" in manager.library.cognitive_tools
        
    @pytest.mark.asyncio
    async def test_template_application(self):
        """Test applying templates to input data"""
        manager = PromptManager()
        await manager.load_templates()
        
        input_data = {
            "problem": "How to validate a new product idea?",
            "complexity_level": "moderate",
            "model_type": "first_principles"
        }
        
        # Apply mental models template
        enhanced = await manager.apply_template("mental_models", input_data)
        
        assert "problem" in enhanced
        assert len(enhanced["problem"]) > len(input_data["problem"])
        assert "first_principles" in enhanced["problem"]
        
    def test_template_suggestions(self):
        """Test template suggestion based on context"""
        manager = PromptManager()
        
        context = {"problem": "How to design a product for market fit?"}
        suggestions = manager.get_template_suggestions(context)
        
        assert "lean_startup" in suggestions
        assert "value_proposition" in suggestions


class TestIterativeOptimizer:
    """Test the IterativeOptimizer component"""
    
    def test_optimizer_initialization(self):
        """Test optimizer initialization"""
        optimizer = IterativeOptimizer()
        
        assert optimizer.config is not None
        assert optimizer.config.max_iterations == 5
        assert optimizer.config.convergence_threshold == 0.85
        assert len(optimizer.supported_tools) > 0
        
    @pytest.mark.asyncio
    async def test_input_quality_evaluation(self):
        """Test input quality evaluation"""
        optimizer = IterativeOptimizer()
        
        # Low quality input
        low_quality = {"problem": "help"}
        score = await optimizer._evaluate_input_quality(low_quality, "sequential_thinking")
        assert score < 0.3
        
        # High quality input
        high_quality = {
            "problem": "How can I validate a new SaaS product idea for the developer tools market? "
                      "I need to understand market fit, pricing strategy, and feature prioritization.",
            "constraints": ["Limited budget", "3-month timeline"],
            "complexity_level": "complex"
        }
        score = await optimizer._evaluate_input_quality(high_quality, "sequential_thinking")
        assert score >= 0.6  # 2.5/4.0 = 0.625 is expected for this input
        
    def test_strategy_selection(self):
        """Test optimization strategy selection"""
        optimizer = IterativeOptimizer()
        
        # Low quality should get clarity enhancement
        strategy = optimizer._select_strategy(0.2, [])
        assert strategy == OptimizationStrategy.CLARITY_ENHANCEMENT
        
        # Medium quality should get constraint refinement
        strategy = optimizer._select_strategy(0.5, [])
        assert strategy == OptimizationStrategy.CONSTRAINT_REFINEMENT
        
        # High quality should get example generation
        strategy = optimizer._select_strategy(0.8, [])
        assert strategy == OptimizationStrategy.EXAMPLE_GENERATION
        
    @pytest.mark.asyncio
    async def test_optimization_application(self):
        """Test applying optimization strategies"""
        optimizer = IterativeOptimizer()
        
        original = {"problem": "validate product"}
        
        # Test clarity enhancement
        enhanced = await optimizer._apply_optimization(
            original,
            OptimizationStrategy.CLARITY_ENHANCEMENT,
            "sequential_thinking",
            {}
        )
        assert enhanced["problem"].endswith(".")
        
        # Test specificity increase
        specific = await optimizer._apply_optimization(
            original,
            OptimizationStrategy.SPECIFICITY_INCREASE,
            "sequential_thinking",
            {"reasoning_depth": 5}
        )
        assert "Specific requirements:" in specific["problem"]
        assert "5 concrete steps" in specific["problem"]
        
    def test_result_issue_analysis(self):
        """Test analyzing issues in results"""
        optimizer = IterativeOptimizer()
        
        # Low confidence result
        result1 = {"confidence": 0.5, "analysis": "Some analysis"}
        issues1 = optimizer._analyze_result_issues(result1)
        assert "low_confidence" in issues1
        
        # Error result
        result2 = {"error": "Failed to process", "status": "failed"}
        issues2 = optimizer._analyze_result_issues(result2)
        assert "error" in issues2
        
        # Incomplete result
        result3 = {"partial": True, "data": "Limited"}
        issues3 = optimizer._analyze_result_issues(result3)
        assert "incomplete" in issues3


class TestWorkflowIntegration:
    """Test integrated workflow execution"""
    
    @pytest.mark.asyncio
    async def test_workflow_state_management(self, sample_workflow_config):
        """Test workflow state tracking"""
        from pyclarity.workflows.models import WorkflowState, ToolExecution, ToolExecutionStatus
        
        state = WorkflowState(config=sample_workflow_config)
        
        # Initially all tools should be ready or pending
        ready = state.get_ready_tools()
        assert "sequential_thinking" in ready
        assert "mental_models" not in ready  # Has dependency
        
        # Mark first tool as completed
        state.tool_executions["sequential_thinking"] = ToolExecution(
            tool_name="sequential_thinking",
            status=ToolExecutionStatus.COMPLETED
        )
        
        # Now mental_models should be ready
        ready = state.get_ready_tools()
        assert "mental_models" in ready
        assert "sequential_thinking" not in ready  # Already completed
        
    @pytest.mark.asyncio 
    async def test_tool_type_validation(self):
        """Test different tool types in workflow"""
        config = WorkflowConfig(
            name="Mixed Tool Types",
            tools=[
                ToolConfig(
                    name="sequential_thinking",
                    tool_type=ToolType.COGNITIVE
                ),
                ToolConfig(
                    name="custom_analyzer",
                    tool_type=ToolType.CUSTOM,
                    config={"custom_param": "value"}
                ),
                ToolConfig(
                    name="prompt_tool",
                    tool_type=ToolType.PROMPT,
                    prompt_template="Analyze this: {input}"
                ),
            ]
        )
        
        # Should validate without errors
        config.validate_dependencies()
        assert len(config.tools) == 3
        assert config.tools[1].tool_type == ToolType.CUSTOM
        assert config.tools[2].prompt_template is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])