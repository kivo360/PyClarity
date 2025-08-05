"""
Impact Propagation Mapping Tool

Analyzes how changes ripple through interconnected systems, revealing
cascading effects, feedback loops, and unintended consequences.
"""

from .analyzer import ImpactPropagationAnalyzer
from .models import (
    ComplexityLevel,
    Edge,
    EffectMagnitude,
    FeedbackLoop,
    FeedbackType,
    ImpactEvent,
    ImpactPropagationContext,
    ImpactPropagationResult,
    ImpactType,
    InterventionPoint,
    Node,
    PropagationPath,
    PropagationSpeed,
    RiskArea,
)

__all__ = [
    # Main classes
    "ImpactPropagationContext",
    "ImpactPropagationResult",
    "ImpactPropagationAnalyzer",

    # Enums
    "ImpactType",
    "PropagationSpeed",
    "EffectMagnitude",
    "FeedbackType",
    "ComplexityLevel",

    # Models
    "Node",
    "Edge",
    "ImpactEvent",
    "PropagationPath",
    "FeedbackLoop",
    "RiskArea",
    "InterventionPoint"
]
