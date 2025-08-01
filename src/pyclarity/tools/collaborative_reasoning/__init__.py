"""
Collaborative Reasoning Cognitive Tool

Provides multi-perspective reasoning through persona simulation,
stakeholder perspective analysis, consensus building, conflict resolution,
role-based decision making, and team dynamics modeling.
"""

from .models import (
    # Enums
    ComplexityLevel,
    PersonaType,
    ReasoningStyle,
    ConsensusStrategy,
    DialogueStyle,
    # Supporting models
    Persona,
    PersonaPerspective,
    CollaborativeDialogue,
    ConsensusResult,
    # Main models
    CollaborativeReasoningContext,
    CollaborativeReasoningResult,
)

from .analyzer import CollaborativeReasoningAnalyzer

__all__ = [
    # Enums
    "ComplexityLevel",
    "PersonaType",
    "ReasoningStyle", 
    "ConsensusStrategy",
    "DialogueStyle",
    # Supporting models
    "Persona",
    "PersonaPerspective",
    "CollaborativeDialogue",
    "ConsensusResult",
    # Main models
    "CollaborativeReasoningContext",
    "CollaborativeReasoningResult",
    # Main class
    "CollaborativeReasoningAnalyzer",
]