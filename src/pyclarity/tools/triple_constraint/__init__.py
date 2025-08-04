"""
Triple Constraint Optimizer Cognitive Tool

Analyzes situations requiring balance between three competing dimensions,
identifying optimal trade-offs and strategies for constraint management.
"""

from .models import (
    # Enums
    ComplexityLevel,
    ConstraintDimension,
    ConstraintPriority,
    TradeoffImpact,
    OptimizationStrategy,
    # Supporting models
    Constraint,
    Tradeoff,
    Scenario,
    # Main models
    TripleConstraintContext,
    TripleConstraintResult,
)

from .analyzer import TripleConstraintAnalyzer

__all__ = [
    # Enums
    "ComplexityLevel",
    "ConstraintDimension",
    "ConstraintPriority",
    "TradeoffImpact",
    "OptimizationStrategy",
    # Supporting models
    "Constraint",
    "Tradeoff",
    "Scenario",
    # Main models
    "TripleConstraintContext",
    "TripleConstraintResult",
    # Main class
    "TripleConstraintAnalyzer",
]