"""
Sequential Thinking Cognitive Tool

Step-by-step problem decomposition and reasoning with dynamic thought
progression, branching capabilities, and revision tracking.
"""

from .analyzer import SequentialThinkingAnalyzer
from .models import (
    BranchStrategy,
    ComplexityLevel,
    SequentialThinkingContext,
    SequentialThinkingResult,
    ThoughtBranch,
    ThoughtRevision,
    ThoughtStep,
    ThoughtStepStatus,
    ThoughtStepType,
)

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
