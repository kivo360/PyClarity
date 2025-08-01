"""
Mental Models Cognitive Tool

Applies structured mental model frameworks for problem analysis including
First Principles, Opportunity Cost, Error Propagation, Rubber Duck Debugging,
Pareto Principle, and Occam's Razor approaches.
"""

from .models import (
    # Enums
    ComplexityLevel,
    MentalModelType,
    # Supporting models
    MentalModelInsight,
    MentalModelAssumption,
    # Main models
    MentalModelContext,
    MentalModelResult,
    # Utilities
    MentalModelUtils,
)

from .analyzer import MentalModelsAnalyzer

__all__ = [
    # Enums
    "ComplexityLevel",
    "MentalModelType",
    # Supporting models
    "MentalModelInsight", 
    "MentalModelAssumption",
    # Main models
    "MentalModelContext",
    "MentalModelResult",
    # Utilities
    "MentalModelUtils",
    # Main class
    "MentalModelsAnalyzer",
]