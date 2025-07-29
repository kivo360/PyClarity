# Clear Thinking FastMCP Server - Sequential Thinking Models

"""
Pydantic models for the Sequential Thinking cognitive tool.

This tool supports dynamic thought progression with:
- Multi-step reasoning chains with branching and merging
- Revision tracking for thought evolution
- Alternative reasoning path exploration
- Confidence scoring and progress tracking
- Branch management for complex problem decomposition

Agent: pydantic-model-engineer
Status: ACTIVE - Sequential Thinking implementation complete
"""

from pydantic import BaseModel, Field, validator, root_validator
from typing import List, Dict, Any, Optional, Union, Literal
from enum import Enum
from datetime import datetime
import uuid

from .base import CognitiveInputBase, CognitiveOutputBase, CognitiveValidators, ComplexityLevel


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
            self.CONCLUSION: "Final reasoning outcome or decision point"
        }
        return descriptions.get(self, "Unknown thought step type")


class BranchStrategy(str, Enum):
    """Strategies for handling reasoning branches"""
    
    PARALLEL_EXPLORATION = "parallel_exploration"  # Explore multiple paths simultaneously
    SEQUENTIAL_EXPLORATION = "sequential_exploration"  # Explore one path at a time
    CONVERGENT_SYNTHESIS = "convergent_synthesis"  # Merge branches at synthesis points
    COMPETITIVE_SELECTION = "competitive_selection"  # Select best branch based on confidence
    HYBRID_APPROACH = "hybrid_approach"  # Combine multiple strategies
    
    @property
    def description(self) -> str:
        """Get description of the branch strategy"""
        descriptions = {
            self.PARALLEL_EXPLORATION: "Explore multiple reasoning paths simultaneously",
            self.SEQUENTIAL_EXPLORATION: "Explore reasoning paths one at a time",
            self.CONVERGENT_SYNTHESIS: "Merge multiple branches at key synthesis points",
            self.COMPETITIVE_SELECTION: "Select the highest confidence branch at decision points",
            self.HYBRID_APPROACH: "Combine multiple branching strategies as appropriate"
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
        example="550e8400-e29b-41d4-a716-446655440000"
    )
    
    step_number: int = Field(
        ...,
        ge=1,
        description="Sequential position in the reasoning chain",
        example=3
    )
    
    step_type: ThoughtStepType = Field(
        ...,
        description="Type of reasoning step being performed",
        example="logical_deduction"
    )
    
    content: str = Field(
        ...,
        description="The reasoning content for this step",
        min_length=20,
        max_length=1000,
        example="Based on the performance metrics, the bottleneck appears to be in the database query optimization layer"
    )
    
    confidence_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence level in this reasoning step",
        example=0.85
    )
    
    dependencies: List[str] = Field(
        default_factory=list,
        description="Step IDs that this step depends on",
        max_items=5
    )
    
    branch_id: Optional[str] = Field(
        None,
        description="Branch identifier if this step is part of a branch",
        example="branch_hypothesis_a"
    )
    
    status: ThoughtStepStatus = Field(
        ThoughtStepStatus.PENDING,
        description="Current status of this thought step"
    )
    
    supporting_evidence: Optional[List[str]] = Field(
        None,
        description="Evidence or facts supporting this step",
        max_items=8
    )
    
    assumptions_made: Optional[List[str]] = Field(
        None,
        description="Assumptions made in this reasoning step",
        max_items=5
    )
    
    potential_errors: Optional[List[str]] = Field(
        None,
        description="Potential errors or weaknesses in this step",
        max_items=3
    )
    
    revision_notes: Optional[str] = Field(
        None,
        description="Notes about revisions made to this step",
        max_length=300
    )
    
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When this step was created"
    )
    
    updated_at: Optional[datetime] = Field(
        None,
        description="When this step was last updated"
    )
    
    # Apply validators
    _validate_confidence = validator('confidence_score', allow_reuse=True)(
        CognitiveValidators.validate_confidence_score
    )
    
    @validator('content')
    def validate_content(cls, v):
        """Validate thought step content is meaningful"""
        return CognitiveValidators.validate_string_not_empty(cls, v, "content")
    
    @validator('dependencies')
    def validate_dependencies(cls, v):
        """Validate dependencies list"""
        if v and len(set(v)) != len(v):
            raise ValueError("Dependencies must be unique")
        return v
    
    def is_ready_to_execute(self, completed_steps: List[str]) -> bool:
        """Check if all dependencies are completed"""
        return all(dep_id in completed_steps for dep_id in self.dependencies)
    
    def update_status(self, new_status: ThoughtStepStatus) -> None:
        """Update step status and timestamp"""
        self.status = new_status
        self.updated_at = datetime.utcnow()


class ThoughtRevision(BaseModel):
    """Revision history for a thought step"""
    
    revision_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for this revision"
    )
    
    step_id: str = Field(
        ...,
        description="ID of the step being revised"
    )
    
    original_content: str = Field(
        ...,
        description="Original content before revision",
        min_length=10
    )
    
    revised_content: str = Field(
        ...,
        description="New content after revision",
        min_length=10
    )
    
    revision_reason: str = Field(
        ...,
        description="Reason for the revision",
        min_length=10,
        max_length=300,
        example="Initial hypothesis was too narrow; expanding to consider alternative causes"
    )
    
    confidence_change: float = Field(
        ...,
        ge=-1.0,
        le=1.0,
        description="Change in confidence score (-1.0 to 1.0)",
        example=0.15
    )
    
    revision_timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="When this revision was made"
    )
    
    @validator('original_content', 'revised_content')
    def validate_content_fields(cls, v):
        """Validate content fields are meaningful"""
        return CognitiveValidators.validate_string_not_empty(cls, v, "content")


class ThoughtBranch(BaseModel):
    """Alternative reasoning path or branch"""
    
    branch_id: str = Field(
        default_factory=lambda: f"branch_{uuid.uuid4().hex[:8]}",
        description="Unique identifier for this branch",
        example="branch_a1b2c3d4"
    )
    
    branch_name: str = Field(
        ...,
        description="Descriptive name for this branch",
        min_length=5,
        max_length=100,
        example="Database Performance Hypothesis"
    )
    
    branch_description: str = Field(
        ...,
        description="Detailed description of this reasoning path",
        min_length=20,
        max_length=500,
        example="Exploring the hypothesis that database query optimization is the primary performance bottleneck"
    )
    
    parent_step_id: Optional[str] = Field(
        None,
        description="Step ID where this branch originated"
    )
    
    steps: List[ThoughtStep] = Field(
        default_factory=list,
        description="Thought steps in this branch",
        max_items=20
    )
    
    branch_confidence: float = Field(
        0.0,
        ge=0.0,
        le=1.0,
        description="Overall confidence in this branch's reasoning"
    )
    
    is_active: bool = Field(
        True,
        description="Whether this branch is currently being explored"
    )
    
    merge_target: Optional[str] = Field(
        None,
        description="Branch ID this branch should merge into"
    )
    
    completion_criteria: Optional[List[str]] = Field(
        None,
        description="Criteria for considering this branch complete",
        max_items=5
    )
    
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When this branch was created"
    )
    
    @validator('branch_name')
    def validate_branch_name(cls, v):
        """Validate branch name is meaningful"""
        return CognitiveValidators.validate_string_not_empty(cls, v, "branch_name")
    
    @validator('steps')
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
            # More recent steps get higher weight
            weight = 1.0 + (i * 0.1)
            total_weighted_confidence += step.confidence_score * weight
            total_weight += weight
        
        self.branch_confidence = round(total_weighted_confidence / total_weight, 3)
        return self.branch_confidence
    
    def get_active_steps(self) -> List[ThoughtStep]:
        """Get steps that are currently active (not rejected)"""
        return [
            step for step in self.steps 
            if step.status != ThoughtStepStatus.REJECTED
        ]


class SequentialThinkingInput(CognitiveInputBase):
    """Input model for sequential thinking cognitive tool"""
    
    reasoning_depth: int = Field(
        5,
        ge=3,
        le=20,
        description="Maximum number of reasoning steps to perform",
        example=8
    )
    
    enable_branching: bool = Field(
        True,
        description="Whether to allow branching into alternative reasoning paths"
    )
    
    branch_strategy: BranchStrategy = Field(
        BranchStrategy.PARALLEL_EXPLORATION,
        description="Strategy for handling reasoning branches"
    )
    
    max_branches: int = Field(
        3,
        ge=1,
        le=5,
        description="Maximum number of simultaneous branches to explore"
    )
    
    convergence_threshold: float = Field(
        0.8,
        ge=0.5,
        le=1.0,
        description="Confidence threshold for branch convergence"
    )
    
    allow_revisions: bool = Field(
        True,
        description="Whether to allow revision of previous steps"
    )
    
    step_types_priority: Optional[List[ThoughtStepType]] = Field(
        None,
        description="Preferred order of thought step types",
        max_items=9
    )
    
    domain_constraints: Optional[List[str]] = Field(
        None,
        description="Domain-specific constraints to consider",
        max_items=8,
        example=["must be implementable within 3 months", "budget constraint: $50k max"]
    )
    
    evidence_sources: Optional[List[str]] = Field(
        None,
        description="Available evidence sources to consider",
        max_items=10,
        example=["performance metrics", "user feedback", "system logs"]
    )
    
    validation_criteria: Optional[List[str]] = Field(
        None,
        description="Criteria for validating reasoning steps",
        max_items=6,
        example=["logical consistency", "empirical support", "practical feasibility"]
    )
    
    @validator('step_types_priority')
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
    
    @validator('domain_constraints', 'evidence_sources', 'validation_criteria')
    def validate_string_lists(cls, v, field):
        """Validate string list fields"""
        if v is not None:
            cleaned = [item.strip() for item in v if item.strip()]
            return cleaned if cleaned else None
        return v


class SequentialThinkingOutput(CognitiveOutputBase):
    """Output model for sequential thinking cognitive tool"""
    
    reasoning_chain: List[ThoughtStep] = Field(
        ...,
        description="Complete sequence of reasoning steps",
        min_items=1,
        max_items=20
    )
    
    branches_explored: List[ThoughtBranch] = Field(
        default_factory=list,
        description="Alternative reasoning branches that were explored",
        max_items=5
    )
    
    revisions_made: List[ThoughtRevision] = Field(
        default_factory=list,
        description="Revisions made during the reasoning process",
        max_items=10
    )
    
    final_conclusion: str = Field(
        ...,
        description="Final conclusion from the reasoning process",
        min_length=50,
        max_length=1000,
        example="The primary performance bottleneck is database connection pooling, requiring immediate optimization of connection management and query batching strategies"
    )
    
    conclusion_confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence in the final conclusion"
    )
    
    reasoning_quality_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Overall quality score of the reasoning process"
    )
    
    critical_assumptions: List[str] = Field(
        default_factory=list,
        description="Critical assumptions underlying the reasoning",
        max_items=8
    )
    
    evidence_gaps: List[str] = Field(
        default_factory=list,
        description="Areas where additional evidence would strengthen reasoning",
        max_items=6
    )
    
    alternative_conclusions: Optional[List[str]] = Field(
        None,
        description="Alternative conclusions that were considered",
        max_items=5
    )
    
    reasoning_path_summary: str = Field(
        ...,
        description="High-level summary of the reasoning path taken",
        min_length=100,
        max_length=500,
        example="Started with problem decomposition, formed multiple hypotheses, gathered evidence from system metrics, applied logical deduction to identify the bottleneck, and validated against known constraints"
    )
    
    branch_statistics: Optional[Dict[str, Any]] = Field(
        None,
        description="Statistics about branch exploration and convergence"
    )
    
    step_type_distribution: Dict[str, int] = Field(
        default_factory=dict,
        description="Count of each type of reasoning step used"
    )
    
    recommendations: List[str] = Field(
        default_factory=list,
        description="Actionable recommendations based on the reasoning",
        max_items=8
    )
    
    limitations: Optional[str] = Field(
        None,
        description="Limitations of the reasoning process or conclusions",
        max_length=400
    )
    
    # Apply validators
    _validate_conclusion_confidence = validator('conclusion_confidence', allow_reuse=True)(
        CognitiveValidators.validate_confidence_score
    )
    
    _validate_quality_score = validator('reasoning_quality_score', allow_reuse=True)(
        CognitiveValidators.validate_confidence_score
    )
    
    @validator('reasoning_chain')
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
    
    @validator('final_conclusion')
    def validate_final_conclusion(cls, v):
        """Validate final conclusion is comprehensive"""
        return CognitiveValidators.validate_string_not_empty(cls, v, "final_conclusion")
    
    @validator('branches_explored')
    def validate_branches_explored(cls, v):
        """Validate branch exploration data"""
        if v:
            # Check for unique branch IDs
            branch_ids = [branch.branch_id for branch in v]
            if len(set(branch_ids)) != len(branch_ids):
                raise ValueError("Branch IDs must be unique")
        return v
    
    @root_validator
    def validate_consistency(cls, values):
        """Validate consistency across fields"""
        reasoning_chain = values.get('reasoning_chain', [])
        branches_explored = values.get('branches_explored', [])
        
        # Count step types
        step_type_counts = {}
        for step in reasoning_chain:
            step_type = step.step_type.value
            step_type_counts[step_type] = step_type_counts.get(step_type, 0) + 1
        
        values['step_type_distribution'] = step_type_counts
        
        # Calculate branch statistics if branches exist
        if branches_explored:
            total_steps_in_branches = sum(len(branch.steps) for branch in branches_explored)
            active_branches = sum(1 for branch in branches_explored if branch.is_active)
            avg_branch_confidence = sum(branch.branch_confidence for branch in branches_explored) / len(branches_explored)
            
            values['branch_statistics'] = {
                'total_branches': len(branches_explored),
                'active_branches': active_branches,
                'total_branch_steps': total_steps_in_branches,
                'average_branch_confidence': round(avg_branch_confidence, 3)
            }
        
        return values
    
    def get_highest_confidence_steps(self, n: int = 3) -> List[ThoughtStep]:
        """Get N highest confidence reasoning steps"""
        return sorted(self.reasoning_chain, key=lambda x: x.confidence_score, reverse=True)[:n]
    
    def get_step_by_type(self, step_type: ThoughtStepType) -> List[ThoughtStep]:
        """Get all steps of a specific type"""
        return [step for step in self.reasoning_chain if step.step_type == step_type]
    
    def get_reasoning_timeline(self) -> List[Dict[str, Any]]:
        """Get chronological timeline of reasoning process"""
        events = []
        
        # Add main reasoning steps
        for step in self.reasoning_chain:
            events.append({
                'timestamp': step.created_at,
                'type': 'reasoning_step',
                'content': f"Step {step.step_number}: {step.step_type.value}",
                'confidence': step.confidence_score
            })
        
        # Add revisions
        for revision in self.revisions_made:
            events.append({
                'timestamp': revision.revision_timestamp,
                'type': 'revision',
                'content': f"Revised step: {revision.revision_reason}",
                'confidence_change': revision.confidence_change
            })
        
        # Sort by timestamp
        return sorted(events, key=lambda x: x['timestamp'])


# Utility functions for sequential thinking processing
class SequentialThinkingUtils:
    """Utility functions for sequential thinking processing"""
    
    @staticmethod
    def validate_step_dependencies(steps: List[ThoughtStep]) -> bool:
        """Validate that step dependencies form a valid DAG"""
        step_ids = {step.step_id for step in steps}
        
        for step in steps:
            # Check all dependencies exist
            for dep_id in step.dependencies:
                if dep_id not in step_ids:
                    return False
            
            # Check for self-reference
            if step.step_id in step.dependencies:
                return False
        
        # TODO: Add cycle detection for more robust validation
        return True
    
    @staticmethod
    def calculate_reasoning_quality(
        steps: List[ThoughtStep],
        branches: List[ThoughtBranch],
        revisions: List[ThoughtRevision]
    ) -> float:
        """Calculate overall reasoning quality score"""
        if not steps:
            return 0.0
        
        # Base score from step confidence
        avg_confidence = sum(step.confidence_score for step in steps) / len(steps)
        
        # Bonus for step type diversity
        step_types = {step.step_type for step in steps}
        diversity_bonus = min(len(step_types) / len(ThoughtStepType), 1.0) * 0.1
        
        # Bonus for thoughtful revisions (not too many, not too few)
        revision_ratio = len(revisions) / len(steps)
        revision_bonus = 0.05 if 0.1 <= revision_ratio <= 0.3 else 0.0
        
        # Bonus for branch exploration
        branch_bonus = min(len(branches) * 0.02, 0.1)
        
        quality_score = avg_confidence + diversity_bonus + revision_bonus + branch_bonus
        return min(quality_score, 1.0)
    
    @staticmethod
    def suggest_next_step_type(
        current_steps: List[ThoughtStep],
        problem_domain: Optional[str] = None
    ) -> ThoughtStepType:
        """Suggest the next logical step type based on current progress"""
        if not current_steps:
            return ThoughtStepType.PROBLEM_DECOMPOSITION
        
        current_types = {step.step_type for step in current_steps}
        last_step_type = current_steps[-1].step_type
        
        # Define logical progressions
        progressions = {
            ThoughtStepType.PROBLEM_DECOMPOSITION: [
                ThoughtStepType.HYPOTHESIS_FORMATION,
                ThoughtStepType.EVIDENCE_GATHERING
            ],
            ThoughtStepType.HYPOTHESIS_FORMATION: [
                ThoughtStepType.EVIDENCE_GATHERING,
                ThoughtStepType.ASSUMPTION_TESTING
            ],
            ThoughtStepType.EVIDENCE_GATHERING: [
                ThoughtStepType.PATTERN_RECOGNITION,
                ThoughtStepType.LOGICAL_DEDUCTION
            ],
            ThoughtStepType.LOGICAL_DEDUCTION: [
                ThoughtStepType.VALIDATION,
                ThoughtStepType.SYNTHESIS
            ],
            ThoughtStepType.PATTERN_RECOGNITION: [
                ThoughtStepType.LOGICAL_DEDUCTION,
                ThoughtStepType.SYNTHESIS
            ],
            ThoughtStepType.ASSUMPTION_TESTING: [
                ThoughtStepType.LOGICAL_DEDUCTION,
                ThoughtStepType.VALIDATION
            ],
            ThoughtStepType.SYNTHESIS: [
                ThoughtStepType.VALIDATION,
                ThoughtStepType.CONCLUSION
            ],
            ThoughtStepType.VALIDATION: [
                ThoughtStepType.CONCLUSION
            ]
        }
        
        # Get possible next steps
        possible_next = progressions.get(last_step_type, [ThoughtStepType.CONCLUSION])
        
        # Filter out already used types (unless it's a repeatable type)
        repeatable_types = {
            ThoughtStepType.EVIDENCE_GATHERING,
            ThoughtStepType.LOGICAL_DEDUCTION,
            ThoughtStepType.VALIDATION
        }
        
        available_next = [
            step_type for step_type in possible_next
            if step_type not in current_types or step_type in repeatable_types
        ]
        
        # Return first available or default to conclusion
        return available_next[0] if available_next else ThoughtStepType.CONCLUSION
    
    @staticmethod
    def merge_branches(
        primary_branch: ThoughtBranch,
        secondary_branch: ThoughtBranch,
        merge_strategy: str = "best_steps"
    ) -> ThoughtBranch:
        """Merge two reasoning branches using specified strategy"""
        merged_branch = ThoughtBranch(
            branch_name=f"Merged: {primary_branch.branch_name} + {secondary_branch.branch_name}",
            branch_description=f"Merged branch combining insights from both reasoning paths"
        )
        
        if merge_strategy == "best_steps":
            # Select steps with highest confidence from both branches
            all_steps = primary_branch.steps + secondary_branch.steps
            sorted_steps = sorted(all_steps, key=lambda x: x.confidence_score, reverse=True)
            
            # Renumber and add best steps
            for i, step in enumerate(sorted_steps[:10], 1):  # Limit to top 10 steps
                step.step_number = i
                merged_branch.steps.append(step)
        
        elif merge_strategy == "sequential":
            # Combine steps sequentially
            merged_branch.steps = primary_branch.steps + secondary_branch.steps
            # Renumber steps
            for i, step in enumerate(merged_branch.steps, 1):
                step.step_number = i
        
        merged_branch.calculate_branch_confidence()
        return merged_branch


__all__ = [
    "ThoughtStepType",
    "BranchStrategy", 
    "ThoughtStepStatus",
    "ThoughtStep",
    "ThoughtRevision",
    "ThoughtBranch",
    "SequentialThinkingInput",
    "SequentialThinkingOutput",
    "SequentialThinkingUtils"
]