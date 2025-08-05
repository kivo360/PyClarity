"""
Sequential Thinking Models

Data structures for sequential thinking analysis including thought steps,
branches, revisions, and reasoning chains.
"""

import uuid
from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator


class ComplexityLevel(str, Enum):
    """Problem complexity levels"""

    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    VERY_COMPLEX = "very_complex"


class ThoughtStepType(str, Enum):
    """Types of thought steps in sequential reasoning"""

    PROBLEM_DECOMPOSITION = "problem_decomposition"
    HYPOTHESIS_FORMATION = "hypothesis_formation"
    EVIDENCE_GATHERING = "evidence_gathering"
    LOGICAL_DEDUCTION = "logical_deduction"
    PATTERN_RECOGNITION = "pattern_recognition"
    ASSUMPTION_TESTING = "assumption_testing"
    SYNTHESIS = "synthesis"
    VALIDATION = "validation"
    CONCLUSION = "conclusion"

    @property
    def description(self) -> str:
        """Get description of the thought step type"""
        descriptions = {
            self.PROBLEM_DECOMPOSITION: "Breaking down complex problems into manageable components",
            self.HYPOTHESIS_FORMATION: "Forming testable hypotheses or potential solutions",
            self.EVIDENCE_GATHERING: "Collecting relevant information and data points",
            self.LOGICAL_DEDUCTION: "Drawing logical conclusions from available information",
            self.PATTERN_RECOGNITION: "Identifying patterns, trends, or recurring themes",
            self.ASSUMPTION_TESTING: "Testing and validating underlying assumptions",
            self.SYNTHESIS: "Combining insights from multiple sources or steps",
            self.VALIDATION: "Verifying conclusions against known facts or constraints",
            self.CONCLUSION: "Final reasoning outcome or decision point",
        }
        return descriptions.get(self, "Unknown thought step type")


class BranchStrategy(str, Enum):
    """Strategies for handling reasoning branches"""

    PARALLEL_EXPLORATION = "parallel_exploration"
    SEQUENTIAL_EXPLORATION = "sequential_exploration"
    CONVERGENT_SYNTHESIS = "convergent_synthesis"
    COMPETITIVE_SELECTION = "competitive_selection"
    HYBRID_APPROACH = "hybrid_approach"

    @property
    def description(self) -> str:
        """Get description of the branch strategy"""
        descriptions = {
            self.PARALLEL_EXPLORATION: "Explore multiple reasoning paths simultaneously",
            self.SEQUENTIAL_EXPLORATION: "Explore reasoning paths one at a time",
            self.CONVERGENT_SYNTHESIS: "Merge multiple branches at key synthesis points",
            self.COMPETITIVE_SELECTION: "Select the highest confidence branch at decision points",
            self.HYBRID_APPROACH: "Combine multiple branching strategies as appropriate",
        }
        return descriptions.get(self, "Unknown branch strategy")


class ThoughtStepStatus(str, Enum):
    """Status of individual thought steps"""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REVISED = "revised"
    REJECTED = "rejected"
    MERGED = "merged"


class ThoughtStep(BaseModel):
    """Individual step in sequential reasoning chain"""

    step_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for this thought step",
    )

    step_number: int = Field(..., ge=1, description="Sequential position in the reasoning chain")

    step_type: ThoughtStepType = Field(..., description="Type of reasoning step being performed")

    content: str = Field(
        ..., description="The reasoning content for this step", min_length=20, max_length=2000
    )

    confidence_score: float = Field(
        ..., ge=0.0, le=1.0, description="Confidence level in this reasoning step"
    )

    dependencies: list[str] = Field(
        default_factory=list, description="Step IDs that this step depends on", max_length=5
    )

    branch_id: str | None = Field(
        None, description="Branch identifier if this step is part of a branch"
    )

    status: ThoughtStepStatus = Field(
        ThoughtStepStatus.PENDING, description="Current status of this thought step"
    )

    supporting_evidence: list[str] = Field(
        default_factory=list, description="Evidence or facts supporting this step", max_length=8
    )

    assumptions_made: list[str] = Field(
        default_factory=list, description="Assumptions made in this reasoning step", max_length=5
    )

    potential_errors: list[str] = Field(
        default_factory=list, description="Potential errors or weaknesses in this step", max_length=3
    )

    revision_notes: str | None = Field(
        None, description="Notes about revisions made to this step", max_length=500
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="When this step was created"
    )

    updated_at: datetime | None = Field(None, description="When this step was last updated")

    @field_validator("content")
    @classmethod
    def validate_content(cls, v):
        """Validate thought step content is meaningful"""
        if not v or v.strip() == "":
            raise ValueError("Content cannot be empty")
        return v.strip()

    @field_validator("dependencies")
    @classmethod
    def validate_dependencies(cls, v):
        """Validate dependencies list"""
        if v and len(set(v)) != len(v):
            raise ValueError("Dependencies must be unique")
        return v

    def is_ready_to_execute(self, completed_steps: list[str]) -> bool:
        """Check if all dependencies are completed"""
        return all(dep_id in completed_steps for dep_id in self.dependencies)

    def update_status(self, new_status: ThoughtStepStatus) -> None:
        """Update step status and timestamp"""
        self.status = new_status
        self.updated_at = datetime.utcnow()


class ThoughtRevision(BaseModel):
    """Revision history for a thought step"""

    revision_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()), description="Unique identifier for this revision"
    )

    step_id: str = Field(..., description="ID of the step being revised")

    original_content: str = Field(
        ..., description="Original content before revision", min_length=10
    )

    revised_content: str = Field(..., description="New content after revision", min_length=10)

    revision_reason: str = Field(
        ..., description="Reason for the revision", min_length=10, max_length=500
    )

    confidence_change: float = Field(
        ..., ge=-1.0, le=1.0, description="Change in confidence score (-1.0 to 1.0)"
    )

    revision_timestamp: datetime = Field(
        default_factory=datetime.utcnow, description="When this revision was made"
    )


class ThoughtBranch(BaseModel):
    """Alternative reasoning path or branch"""

    branch_id: str = Field(
        default_factory=lambda: f"branch_{uuid.uuid4().hex[:8]}",
        description="Unique identifier for this branch",
    )

    branch_name: str = Field(
        ..., description="Descriptive name for this branch", min_length=5, max_length=100
    )

    branch_description: str = Field(
        ...,
        description="Detailed description of this reasoning path",
        min_length=20,
        max_length=500,
    )

    parent_step_id: str | None = Field(None, description="Step ID where this branch originated")

    steps: list[ThoughtStep] = Field(
        default_factory=list, description="Thought steps in this branch", max_length=20
    )

    branch_confidence: float = Field(
        0.0, ge=0.0, le=1.0, description="Overall confidence in this branch's reasoning"
    )

    is_active: bool = Field(True, description="Whether this branch is currently being explored")

    merge_target: str | None = Field(None, description="Branch ID this branch should merge into")

    completion_criteria: list[str] = Field(
        default_factory=list,
        description="Criteria for considering this branch complete",
        max_length=5,
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="When this branch was created"
    )

    @field_validator("branch_name")
    @classmethod
    def validate_branch_name(cls, v):
        """Validate branch name is meaningful"""
        if not v or v.strip() == "":
            raise ValueError("Branch name cannot be empty")
        return v.strip()

    @field_validator("steps")
    @classmethod
    def validate_steps_order(cls, v):
        """Validate steps are properly ordered"""
        if v:
            step_numbers = [step.step_number for step in v]
            if step_numbers != sorted(step_numbers):
                raise ValueError("Steps must be ordered by step_number")
        return v

    def calculate_branch_confidence(self) -> float:
        """Calculate overall branch confidence from steps"""
        if not self.steps:
            return 0.0

        # Weight recent steps more heavily
        total_weighted_confidence = 0.0
        total_weight = 0.0

        for i, step in enumerate(self.steps):
            weight = 1.0 + (i * 0.1)
            total_weighted_confidence += step.confidence_score * weight
            total_weight += weight

        self.branch_confidence = round(total_weighted_confidence / total_weight, 3)
        return self.branch_confidence

    def get_active_steps(self) -> list[ThoughtStep]:
        """Get steps that are currently active (not rejected)"""
        return [step for step in self.steps if step.status != ThoughtStepStatus.REJECTED]


class SequentialThinkingContext(BaseModel):
    """Context for sequential thinking analysis"""

    problem: str = Field(
        ..., description="The problem or question to analyze", min_length=10, max_length=2000
    )

    complexity_level: ComplexityLevel = Field(
        ComplexityLevel.MODERATE, description="Complexity level of the problem"
    )

    reasoning_depth: int = Field(
        5, ge=3, le=20, description="Maximum number of reasoning steps to perform"
    )

    enable_branching: bool = Field(
        True, description="Whether to allow branching into alternative reasoning paths"
    )

    branch_strategy: BranchStrategy = Field(
        BranchStrategy.PARALLEL_EXPLORATION, description="Strategy for handling reasoning branches"
    )

    max_branches: int = Field(
        3, ge=1, le=5, description="Maximum number of simultaneous branches to explore"
    )

    convergence_threshold: float = Field(
        0.8, ge=0.5, le=1.0, description="Confidence threshold for branch convergence"
    )

    allow_revisions: bool = Field(True, description="Whether to allow revision of previous steps")

    step_types_priority: list[ThoughtStepType] | None = Field(
        None, description="Preferred order of thought step types", max_length=9
    )

    domain_constraints: list[str] = Field(
        default_factory=list, description="Domain-specific constraints to consider", max_length=8
    )

    evidence_sources: list[str] = Field(
        default_factory=list, description="Available evidence sources to consider", max_length=10
    )

    validation_criteria: list[str] = Field(
        default_factory=list, description="Criteria for validating reasoning steps", max_length=6
    )

    @field_validator("problem")
    @classmethod
    def validate_problem(cls, v):
        """Validate problem statement"""
        if not v or v.strip() == "":
            raise ValueError("Problem statement cannot be empty")
        return v.strip()

    @field_validator("step_types_priority")
    @classmethod
    def validate_step_types_priority(cls, v):
        """Validate step types priority list"""
        if v is not None:
            # Remove duplicates while preserving order
            seen = set()
            unique_types = []
            for step_type in v:
                if step_type not in seen:
                    seen.add(step_type)
                    unique_types.append(step_type)
            return unique_types
        return v


class SequentialThinkingResult(BaseModel):
    """Result of sequential thinking analysis"""

    reasoning_chain: list[ThoughtStep] = Field(
        ..., description="Complete sequence of reasoning steps", min_length=1, max_length=20
    )

    branches_explored: list[ThoughtBranch] = Field(
        default_factory=list,
        description="Alternative reasoning branches that were explored",
        max_length=5,
    )

    revisions_made: list[ThoughtRevision] = Field(
        default_factory=list,
        description="Revisions made during the reasoning process",
        max_length=10,
    )

    final_conclusion: str = Field(
        ...,
        description="Final conclusion from the reasoning process",
        min_length=50,
        max_length=2000,
    )

    conclusion_confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Confidence in the final conclusion"
    )

    reasoning_quality_score: float = Field(
        ..., ge=0.0, le=1.0, description="Overall quality score of the reasoning process"
    )

    critical_assumptions: list[str] = Field(
        default_factory=list,
        description="Critical assumptions underlying the reasoning",
        max_length=8,
    )

    evidence_gaps: list[str] = Field(
        default_factory=list,
        description="Areas where additional evidence would strengthen reasoning",
        max_length=6,
    )

    alternative_conclusions: list[str] = Field(
        default_factory=list,
        description="Alternative conclusions that were considered",
        max_length=5,
    )

    reasoning_path_summary: str = Field(
        ...,
        description="High-level summary of the reasoning path taken",
        min_length=100,
        max_length=1000,
    )

    branch_statistics: dict[str, Any] | None = Field(
        None, description="Statistics about branch exploration and convergence"
    )

    step_type_distribution: dict[str, int] = Field(
        default_factory=dict, description="Count of each type of reasoning step used"
    )

    recommendations: list[str] = Field(
        default_factory=list,
        description="Actionable recommendations based on the reasoning",
        max_length=8,
    )

    limitations: str | None = Field(
        None, description="Limitations of the reasoning process or conclusions", max_length=500
    )

    processing_time_ms: int = Field(0, description="Time taken to process in milliseconds")

    @field_validator("reasoning_chain")
    @classmethod
    def validate_reasoning_chain(cls, v):
        """Validate reasoning chain structure and order"""
        if not v:
            raise ValueError("Reasoning chain cannot be empty")

        # Check step numbering is sequential
        step_numbers = [step.step_number for step in v]
        expected_numbers = list(range(1, len(v) + 1))

        if step_numbers != expected_numbers:
            raise ValueError("Reasoning chain steps must be sequentially numbered starting from 1")

        # Ensure final step is a conclusion
        if v[-1].step_type != ThoughtStepType.CONCLUSION:
            raise ValueError("Final step in reasoning chain must be a conclusion")

        return v

    @model_validator(mode="after")
    def validate_consistency(self):
        """Validate consistency across fields"""
        reasoning_chain = self.reasoning_chain
        branches_explored = self.branches_explored or []

        # Count step types
        step_type_counts = {}
        for step in reasoning_chain:
            step_type = step.step_type.value
            step_type_counts[step_type] = step_type_counts.get(step_type, 0) + 1

        self.step_type_distribution = step_type_counts

        # Calculate branch statistics if branches exist
        if branches_explored:
            total_steps_in_branches = sum(len(branch.steps) for branch in branches_explored)
            active_branches = sum(1 for branch in branches_explored if branch.is_active)
            avg_branch_confidence = sum(
                branch.branch_confidence for branch in branches_explored
            ) / len(branches_explored)

            self.branch_statistics = {
                "total_branches": len(branches_explored),
                "active_branches": active_branches,
                "total_branch_steps": total_steps_in_branches,
                "average_branch_confidence": round(avg_branch_confidence, 3),
            }

        return self

    def get_highest_confidence_steps(self, n: int = 3) -> list[ThoughtStep]:
        """Get N highest confidence reasoning steps"""
        return sorted(self.reasoning_chain, key=lambda x: x.confidence_score, reverse=True)[:n]

    def get_step_by_type(self, step_type: ThoughtStepType) -> list[ThoughtStep]:
        """Get all steps of a specific type"""
        return [step for step in self.reasoning_chain if step.step_type == step_type]

    def get_reasoning_timeline(self) -> list[dict[str, Any]]:
        """Get chronological timeline of reasoning process"""
        events = []

        # Add main reasoning steps
        for step in self.reasoning_chain:
            events.append(
                {
                    "timestamp": step.created_at,
                    "type": "reasoning_step",
                    "content": f"Step {step.step_number}: {step.step_type.value}",
                    "confidence": step.confidence_score,
                }
            )

        # Add revisions
        for revision in self.revisions_made:
            events.append(
                {
                    "timestamp": revision.revision_timestamp,
                    "type": "revision",
                    "content": f"Revised step: {revision.revision_reason}",
                    "confidence_change": revision.confidence_change,
                }
            )

        # Sort by timestamp
        return sorted(events, key=lambda x: x["timestamp"])
