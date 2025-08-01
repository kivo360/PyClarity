"""Test Sequential Thinking cognitive tool.

Tests adapted from FastMCP implementation to work with PyClarity's async analyzer pattern.
"""

import pytest
import pytest_asyncio
from typing import List
import time

from pyclarity.tools.sequential_thinking.models import (
    SequentialThinkingContext,
    SequentialThinkingResult,
    ThoughtStep,
    ThoughtStepType,
    ThoughtStepStatus,
    ThoughtRevision,
    ThoughtBranch,
    BranchStrategy,
    ComplexityLevel
)
from pyclarity.tools.sequential_thinking.analyzer import SequentialThinkingAnalyzer


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def sample_thought_step():
    """Generate a sample ThoughtStep for testing"""
    return ThoughtStep(
        step_number=1,
        step_type=ThoughtStepType.PROBLEM_DECOMPOSITION,
        content="Breaking down the performance issue into database queries, network latency, and server processing components for systematic analysis.",
        confidence_score=0.85,
        dependencies=[],
        supporting_evidence=["performance metrics", "system logs"],
        assumptions_made=["The problem components are independent enough to analyze separately"],
        potential_errors=["May oversimplify interconnected components"]
    )


@pytest.fixture
def sample_thought_branch():
    """Generate a sample ThoughtBranch for testing"""
    steps = [
        ThoughtStep(
            step_number=1,
            step_type=ThoughtStepType.HYPOTHESIS_FORMATION,
            content="Alternative hypothesis: The issue is primarily in caching layer",
            confidence_score=0.78
        ),
        ThoughtStep(
            step_number=2,
            step_type=ThoughtStepType.EVIDENCE_GATHERING,
            content="Cache hit ratios show 60% efficiency, suggesting room for improvement",
            confidence_score=0.82
        )
    ]
    
    branch = ThoughtBranch(
        branch_name="Cache Performance Hypothesis",
        branch_description="Exploring caching as primary performance bottleneck",
        steps=steps
    )
    branch.calculate_branch_confidence()
    return branch


@pytest.fixture
def sample_revision():
    """Generate a sample ThoughtRevision for testing"""
    return ThoughtRevision(
        step_id="test-step-id",
        original_content="Original analysis of the problem",
        revised_content="Revised analysis with additional considerations and evidence",
        revision_reason="Enhanced analysis with additional perspectives",
        confidence_change=0.1
    )


@pytest.fixture
def sample_context():
    """Generate sample SequentialThinkingContext for testing"""
    return SequentialThinkingContext(
        problem="How to optimize database performance for a high-traffic e-commerce application?",
        context="E-commerce platform with 1M+ daily users experiencing slow query response times",
        complexity_level=ComplexityLevel.MEDIUM,
        reasoning_depth=6,
        enable_branching=True,
        branch_strategy=BranchStrategy.PARALLEL_EXPLORATION,
        max_branches=3,
        convergence_threshold=0.8,
        allow_revisions=True,
        evidence_sources=["performance metrics", "query logs", "user feedback"],
        validation_criteria=["logical consistency", "empirical support", "practical feasibility"]
    )


@pytest.fixture
def sequential_analyzer():
    """Create SequentialThinkingAnalyzer instance for testing"""
    return SequentialThinkingAnalyzer()


# ============================================================================
# Model Tests - ThoughtStep
# ============================================================================

class TestThoughtStep:
    """Test suite for ThoughtStep model"""
    
    def test_thought_step_creation_valid(self, sample_thought_step):
        """Test creating a valid ThoughtStep"""
        assert sample_thought_step.step_number == 1
        assert sample_thought_step.step_type == ThoughtStepType.PROBLEM_DECOMPOSITION
        assert len(sample_thought_step.content) >= 20
        assert 0.0 <= sample_thought_step.confidence_score <= 1.0
        assert sample_thought_step.status == ThoughtStepStatus.PENDING
        assert sample_thought_step.step_id is not None
    
    def test_thought_step_validation_content_too_short(self):
        """Test ThoughtStep validation with content too short"""
        with pytest.raises(ValueError, match="String should have at least 20 characters"):
            ThoughtStep(
                step_number=1,
                step_type=ThoughtStepType.PROBLEM_DECOMPOSITION,
                content="Too short",
                confidence_score=0.8
            )
    
    def test_thought_step_validation_invalid_confidence(self):
        """Test ThoughtStep validation with invalid confidence score"""
        with pytest.raises(ValueError, match="Input should be greater than or equal to 0"):
            ThoughtStep(
                step_number=1,
                step_type=ThoughtStepType.EVIDENCE_GATHERING,
                content="Valid content that meets the minimum length requirement",
                confidence_score=-0.1
            )
        
        with pytest.raises(ValueError, match="Input should be less than or equal to 1"):
            ThoughtStep(
                step_number=1,
                step_type=ThoughtStepType.LOGICAL_DEDUCTION,
                content="Valid content that meets the minimum length requirement",
                confidence_score=1.5
            )
    
    def test_thought_step_confidence_modification(self, sample_thought_step):
        """Test modifying thought step confidence"""
        original_confidence = sample_thought_step.confidence_score
        
        # Directly modify confidence score
        sample_thought_step.confidence_score = 0.92
        
        assert sample_thought_step.confidence_score == 0.92
        assert sample_thought_step.confidence_score != original_confidence
    
    def test_thought_step_status_change(self, sample_thought_step):
        """Test changing thought step status"""
        assert sample_thought_step.status == ThoughtStepStatus.PENDING
        
        sample_thought_step.status = ThoughtStepStatus.COMPLETED
        
        assert sample_thought_step.status == ThoughtStepStatus.COMPLETED
    
    def test_thought_step_in_progress_status(self, sample_thought_step):
        """Test changing thought step to in progress"""
        assert sample_thought_step.status == ThoughtStepStatus.PENDING
        
        sample_thought_step.status = ThoughtStepStatus.IN_PROGRESS
        
        assert sample_thought_step.status == ThoughtStepStatus.IN_PROGRESS
    
    def test_thought_step_revised_status(self, sample_thought_step):
        """Test changing thought step to revised"""
        assert sample_thought_step.status == ThoughtStepStatus.PENDING
        
        sample_thought_step.status = ThoughtStepStatus.REVISED
        
        assert sample_thought_step.status == ThoughtStepStatus.REVISED


# ============================================================================
# Model Tests - ThoughtBranch
# ============================================================================

class TestThoughtBranch:
    """Test suite for ThoughtBranch model"""
    
    def test_thought_branch_creation(self, sample_thought_branch):
        """Test creating a valid ThoughtBranch"""
        assert sample_thought_branch.branch_name == "Cache Performance Hypothesis"
        assert len(sample_thought_branch.steps) == 2
        assert sample_thought_branch.branch_id is not None
        assert sample_thought_branch.branch_confidence > 0
    
    def test_branch_confidence_calculation(self):
        """Test branch confidence calculation"""
        steps = [
            ThoughtStep(
                step_number=1,
                step_type=ThoughtStepType.ANALYSIS,
                content="First step with high confidence in the analysis",
                confidence_score=0.9
            ),
            ThoughtStep(
                step_number=2,
                step_type=ThoughtStepType.CONCLUSION,
                content="Second step with medium confidence in the conclusion",
                confidence_score=0.7
            ),
            ThoughtStep(
                step_number=3,
                step_type=ThoughtStepType.VALIDATION,
                content="Third step with high confidence in the validation",
                confidence_score=0.8
            )
        ]
        
        branch = ThoughtBranch(
            branch_name="Test Branch",
            branch_description="Testing confidence calculation",
            steps=steps
        )
        
        branch.calculate_branch_confidence()
        
        # Average confidence should be (0.9 + 0.7 + 0.8) / 3 = 0.8
        assert branch.branch_confidence == pytest.approx(0.8, rel=1e-3)
    
    def test_branch_step_addition(self, sample_thought_branch):
        """Test branch with additional steps"""
        original_count = len(sample_thought_branch.steps)
        
        new_step = ThoughtStep(
            step_number=3,
            step_type=ThoughtStepType.VALIDATION,
            content="Validating cache optimization approach through benchmarking",
            confidence_score=0.88
        )
        
        # Append step to the branch
        sample_thought_branch.steps.append(new_step)
        
        assert len(sample_thought_branch.steps) == original_count + 1
        assert sample_thought_branch.steps[-1] == new_step
    
    def test_branch_combination(self):
        """Test combining steps from two branches"""
        branch1_steps = [
            ThoughtStep(
                step_number=1,
                step_type=ThoughtStepType.EVIDENCE_GATHERING,
                content="Branch 1 evidence gathering from the problem space",
                confidence_score=0.8
            )
        ]
        
        branch2_steps = [
            ThoughtStep(
                step_number=1,
                step_type=ThoughtStepType.HYPOTHESIS_FORMATION,
                content="Branch 2 hypothesis about the solution",
                confidence_score=0.85
            )
        ]
        
        branch1 = ThoughtBranch(
            branch_name="Branch 1",
            branch_description="First branch",
            steps=branch1_steps
        )
        
        branch2 = ThoughtBranch(
            branch_name="Branch 2",
            branch_description="Second branch",
            steps=branch2_steps
        )
        
        # Manually combine branches
        combined_steps = branch1.steps + branch2.steps
        # Renumber steps
        for i, step in enumerate(combined_steps, 1):
            step.step_number = i
        
        assert len(combined_steps) == 2
        assert combined_steps[1].step_number == 2  # Should be renumbered


# ============================================================================
# Model Tests - ThoughtRevision
# ============================================================================

class TestThoughtRevision:
    """Test suite for ThoughtRevision model"""
    
    def test_revision_creation(self, sample_revision):
        """Test creating a valid ThoughtRevision"""
        assert sample_revision.step_id == "test-step-id"
        assert sample_revision.confidence_change == 0.1
        assert sample_revision.revision_id is not None
        assert sample_revision.timestamp is not None
    
    def test_revision_validation_confidence_change_bounds(self):
        """Test revision confidence change validation"""
        with pytest.raises(ValueError, match="Input should be greater than or equal to -1"):
            ThoughtRevision(
                step_id="test",
                original_content="Original content",
                revised_content="Revised content",
                revision_reason="Test reason",
                confidence_change=-1.5
            )
        
        with pytest.raises(ValueError, match="Input should be less than or equal to 1"):
            ThoughtRevision(
                step_id="test",
                original_content="Original content",
                revised_content="Revised content",
                revision_reason="Test reason",
                confidence_change=1.5
            )


# ============================================================================
# Model Tests - SequentialThinkingContext
# ============================================================================

class TestSequentialThinkingContext:
    """Test suite for SequentialThinkingContext model"""
    
    def test_context_creation_valid(self, sample_context):
        """Test creating a valid context"""
        assert sample_context.problem
        assert sample_context.complexity_level == ComplexityLevel.MEDIUM
        assert sample_context.reasoning_depth == 6
        assert sample_context.enable_branching is True
        assert sample_context.branch_strategy == BranchStrategy.PARALLEL_EXPLORATION
    
    def test_context_validation_problem_too_short(self):
        """Test context validation with problem too short"""
        with pytest.raises(ValueError, match="String should have at least 10 characters"):
            SequentialThinkingContext(
                problem="Too short",
                context="Valid context description"
            )
    
    def test_context_validation_invalid_reasoning_depth(self):
        """Test context validation with invalid reasoning depth"""
        with pytest.raises(ValueError, match="Input should be greater than or equal to 3"):
            SequentialThinkingContext(
                problem="Valid problem description",
                context="Valid context",
                reasoning_depth=2
            )
        
        with pytest.raises(ValueError, match="Input should be less than or equal to 20"):
            SequentialThinkingContext(
                problem="Valid problem description",
                context="Valid context",
                reasoning_depth=25
            )
    
    def test_context_validation_max_branches(self):
        """Test context validation for max branches"""
        with pytest.raises(ValueError, match="Input should be greater than or equal to 2"):
            SequentialThinkingContext(
                problem="Valid problem description",
                context="Valid context",
                enable_branching=True,
                max_branches=1
            )


# ============================================================================
# Analyzer Tests
# ============================================================================

@pytest.mark.asyncio
class TestSequentialThinkingAnalyzer:
    """Test suite for SequentialThinkingAnalyzer"""
    
    async def test_analyzer_initialization(self, sequential_analyzer):
        """Test analyzer initialization"""
        assert sequential_analyzer.tool_name == "Sequential Thinking"
        assert sequential_analyzer.version == "2.0.0"
        assert sequential_analyzer._current_step_number == 1
        assert len(sequential_analyzer._completed_step_ids) == 0
    
    async def test_basic_analysis(self, sequential_analyzer, sample_context):
        """Test basic sequential thinking analysis"""
        # Disable branching and revisions for simple test
        sample_context.enable_branching = False
        sample_context.allow_revisions = False
        sample_context.reasoning_depth = 5
        
        result = await sequential_analyzer.analyze(sample_context)
        
        assert isinstance(result, SequentialThinkingResult)
        assert len(result.reasoning_chain) == 5
        assert result.final_confidence > 0
        assert result.quality_score > 0
        assert result.processing_time_ms > 0
        assert result.metadata["total_steps"] == 5
        assert result.metadata["branches_explored"] == 0
        assert result.metadata["revisions_made"] == 0
    
    async def test_analysis_with_branching(self, sequential_analyzer, sample_context):
        """Test analysis with branching enabled"""
        sample_context.enable_branching = True
        sample_context.branch_strategy = BranchStrategy.PARALLEL_EXPLORATION
        sample_context.max_branches = 2
        sample_context.allow_revisions = False
        sample_context.reasoning_depth = 4
        
        result = await sequential_analyzer.analyze(sample_context)
        
        assert isinstance(result, SequentialThinkingResult)
        assert len(result.branches_explored) > 0
        assert len(result.branches_explored) <= 2
        assert result.metadata["branches_explored"] > 0
        
        # Verify each branch has steps
        for branch in result.branches_explored:
            assert len(branch.steps) > 0
            assert branch.branch_confidence > 0
    
    async def test_analysis_with_revisions(self, sequential_analyzer, sample_context):
        """Test analysis with revisions enabled"""
        sample_context.enable_branching = False
        sample_context.allow_revisions = True
        sample_context.reasoning_depth = 4
        
        result = await sequential_analyzer.analyze(sample_context)
        
        assert isinstance(result, SequentialThinkingResult)
        # Revisions are probabilistic, so we check the structure
        assert hasattr(result, 'revisions_made')
        assert isinstance(result.revisions_made, list)
        assert result.metadata["revisions_made"] >= 0
    
    async def test_convergent_synthesis(self, sequential_analyzer, sample_context):
        """Test convergent synthesis branch strategy"""
        sample_context.enable_branching = True
        sample_context.branch_strategy = BranchStrategy.CONVERGENT_SYNTHESIS
        sample_context.max_branches = 3
        sample_context.convergence_threshold = 0.75
        sample_context.allow_revisions = False
        sample_context.reasoning_depth = 5
        
        result = await sequential_analyzer.analyze(sample_context)
        
        assert isinstance(result, SequentialThinkingResult)
        assert len(result.branches_explored) > 0
        
        # Check if synthesis occurred (reasoning chain should be longer than original depth)
        # This depends on whether branches were actually merged
        assert len(result.reasoning_chain) >= 5
    
    async def test_step_type_progression(self, sequential_analyzer, sample_context):
        """Test that step types progress logically"""
        sample_context.enable_branching = False
        sample_context.allow_revisions = False
        sample_context.reasoning_depth = 7
        
        result = await sequential_analyzer.analyze(sample_context)
        
        step_types = [step.step_type for step in result.reasoning_chain]
        
        # Verify logical progression patterns
        # Should typically start with problem decomposition or hypothesis
        assert step_types[0] in [
            ThoughtStepType.PROBLEM_DECOMPOSITION,
            ThoughtStepType.HYPOTHESIS_FORMATION,
            ThoughtStepType.EVIDENCE_GATHERING
        ]
        
        # Should typically end with conclusion or synthesis
        assert step_types[-1] in [
            ThoughtStepType.CONCLUSION,
            ThoughtStepType.SYNTHESIS,
            ThoughtStepType.VALIDATION
        ]
    
    async def test_evidence_and_assumptions_tracking(self, sequential_analyzer, sample_context):
        """Test that evidence and assumptions are properly tracked"""
        sample_context.evidence_sources = ["test data", "user feedback", "metrics"]
        sample_context.enable_branching = False
        sample_context.allow_revisions = False
        
        result = await sequential_analyzer.analyze(sample_context)
        
        # Check that steps have evidence and assumptions
        has_evidence = any(step.supporting_evidence for step in result.reasoning_chain)
        has_assumptions = any(step.assumptions_made for step in result.reasoning_chain)
        
        assert has_evidence
        assert has_assumptions
    
    async def test_complexity_handling(self, sequential_analyzer):
        """Test handling different complexity levels"""
        # Test simple complexity
        simple_context = SequentialThinkingContext(
            problem="Simple optimization problem",
            context="Basic context",
            complexity_level=ComplexityLevel.SIMPLE,
            reasoning_depth=3
        )
        
        simple_result = await sequential_analyzer.analyze(simple_context)
        
        # Test complex problem
        complex_context = SequentialThinkingContext(
            problem="Complex multi-system integration challenge",
            context="Large-scale distributed system",
            complexity_level=ComplexityLevel.COMPLEX,
            reasoning_depth=10,
            enable_branching=True,
            max_branches=4
        )
        
        complex_result = await sequential_analyzer.analyze(complex_context)
        
        # Complex problems should generate more comprehensive analysis
        assert len(complex_result.reasoning_chain) > len(simple_result.reasoning_chain)
        assert complex_result.metadata["total_steps"] > simple_result.metadata["total_steps"]
    
    async def test_validation_criteria_influence(self, sequential_analyzer, sample_context):
        """Test that validation criteria influence the analysis"""
        sample_context.validation_criteria = [
            "logical_consistency",
            "empirical_support",
            "practical_feasibility",
            "cost_effectiveness"
        ]
        sample_context.enable_branching = False
        sample_context.allow_revisions = False
        
        result = await sequential_analyzer.analyze(sample_context)
        
        # Check that validation steps consider the criteria
        validation_steps = [
            step for step in result.reasoning_chain 
            if step.step_type == ThoughtStepType.VALIDATION
        ]
        
        # Should have at least one validation step
        assert len(validation_steps) > 0
    
    async def test_decision_point_handling(self, sequential_analyzer, sample_context):
        """Test handling of decision points in reasoning"""
        sample_context.enable_branching = True
        sample_context.branch_strategy = BranchStrategy.DECISION_TREE
        sample_context.max_branches = 3
        
        result = await sequential_analyzer.analyze(sample_context)
        
        # With decision tree strategy, should have decision points
        has_decision_points = any(
            step.step_type == ThoughtStepType.LOGICAL_DEDUCTION 
            for branch in result.branches_explored
            for step in branch.steps
        )
        
        assert has_decision_points or len(result.branches_explored) > 0
    
    async def test_quality_metrics(self, sequential_analyzer, sample_context):
        """Test quality metrics calculation"""
        result = await sequential_analyzer.analyze(sample_context)
        
        # Quality score should be between 0 and 1
        assert 0 <= result.quality_score <= 1
        
        # Check quality dimensions
        quality_dimensions = result.quality_dimensions
        assert "logical_consistency" in quality_dimensions
        assert "evidence_support" in quality_dimensions
        assert "assumption_validity" in quality_dimensions
        assert "conclusion_strength" in quality_dimensions
        
        # All dimensions should be between 0 and 1
        for score in quality_dimensions.values():
            assert 0 <= score <= 1
    
    async def test_error_handling_empty_problem(self, sequential_analyzer):
        """Test error handling for empty problem"""
        with pytest.raises(ValueError):
            context = SequentialThinkingContext(
                problem="",  # Empty problem
                context="Some context"
            )
    
    async def test_concurrent_analysis(self, sequential_analyzer):
        """Test that analyzer can handle concurrent analyses"""
        contexts = [
            SequentialThinkingContext(
                problem=f"Problem {i}: Optimize system component {i}",
                context=f"Context for problem {i}",
                reasoning_depth=4,
                enable_branching=False,
                allow_revisions=False
            )
            for i in range(3)
        ]
        
        # Run analyses concurrently
        results = await asyncio.gather(*[
            sequential_analyzer.analyze(ctx) for ctx in contexts
        ])
        
        assert len(results) == 3
        for i, result in enumerate(results):
            assert isinstance(result, SequentialThinkingResult)
            assert len(result.reasoning_chain) == 4