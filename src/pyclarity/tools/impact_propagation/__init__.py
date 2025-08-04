"""
Impact Propagation Mapping Tool

Analyzes how changes ripple through interconnected systems, revealing
cascading effects, feedback loops, and unintended consequences.
"""

from .models import (
    ImpactPropagationContext,
    ImpactPropagationResult,
    ImpactType,
    PropagationSpeed,
    EffectMagnitude,
    FeedbackType,
    Node,
    Edge,
    ImpactEvent,
    PropagationPath,
    FeedbackLoop,
    RiskArea,
    InterventionPoint,
    ComplexityLevel
)
from .analyzer import ImpactPropagationAnalyzer

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