"""
Triple Constraint Optimizer Cognitive Tool

Analyzes situations requiring balance between three competing dimensions,
identifying optimal trade-offs and strategies for constraint management.
"""

from .analyzer import TripleConstraintAnalyzer
from .models import (
    # Core models
    Constraint,
    # Enums
    ConstraintDimension,
    ConstraintPriority,
    # Supporting models
    ConstraintSet,
    OptimizationRecommendation,
    OptimizationStrategy,
    Scenario,
    Tradeoff,
    TradeOffAnalysis,
    TradeoffImpact,
    # Main models
    TripleConstraintContext,
    TripleConstraintResult,
)

__all__ = [
    # Enums
    "ConstraintDimension",
    "ConstraintPriority",
    "TradeoffImpact",
    "OptimizationStrategy",
    # Core models
    "Constraint",
    "Tradeoff",
    "Scenario",
    # Supporting models
    "ConstraintSet",
    "TradeOffAnalysis",
    "OptimizationRecommendation",
    # Main models
    "TripleConstraintContext",
    "TripleConstraintResult",
    # Main class
    "TripleConstraintAnalyzer",
]
