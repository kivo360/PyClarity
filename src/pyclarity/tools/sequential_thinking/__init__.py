"""
Sequential Thinking Cognitive Tool

Step-by-step problem decomposition and reasoning with dynamic thought 
progression, branching capabilities, and revision tracking.
"""

from .models import (
    ComplexityLevel,
    ThoughtStepType,
    BranchStrategy,
    ThoughtStepStatus,
    ThoughtStep,
    ThoughtRevision,
    ThoughtBranch,
    SequentialThinkingContext,
    SequentialThinkingResult,
)

from .analyzer import SequentialThinkingAnalyzer

__all__ = [
    # Enums
    "ComplexityLevel",
    "ThoughtStepType",
    "BranchStrategy",
    "ThoughtStepStatus",
    # Models
    "ThoughtStep",
    "ThoughtRevision", 
    "ThoughtBranch",
    "SequentialThinkingContext",
    "SequentialThinkingResult",
    # Main class
    "SequentialThinkingAnalyzer",
]