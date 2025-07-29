# Clear Thinking FastMCP Server - Models Package

"""
Comprehensive Pydantic models for all 11 cognitive tools.

This package provides type-safe input/output models with validation,
serialization support, and FastMCP compatibility.

Agent: pydantic-model-engineer  
Status: ACTIVE - Core models implementation
"""

from .base import (
    CognitiveToolBase,
    CognitiveInputBase, 
    CognitiveOutputBase,
    CognitiveValidators,
    ModelSerializer
)

from .mental_models import (
    MentalModelType,
    MentalModelInput,
    MentalModelOutput,
    MentalModelInsight
)

from .sequential_thinking import (
    SequentialThinkingInput,
    SequentialThinkingOutput,
    ThoughtStep,
    RevisionPoint
)

from .collaborative_reasoning import (
    CollaborativeReasoningInput,
    CollaborativeReasoningOutput,
    PersonaType,
    PersonaContribution,
    DebateRound
)

__all__ = [
    # Base models
    "CognitiveToolBase",
    "CognitiveInputBase", 
    "CognitiveOutputBase",
    "CognitiveValidators",
    "ModelSerializer",
    
    # Mental Models
    "MentalModelType",
    "MentalModelInput",
    "MentalModelOutput", 
    "MentalModelInsight",
    
    # Sequential Thinking
    "SequentialThinkingInput",
    "SequentialThinkingOutput",
    "ThoughtStep",
    "RevisionPoint",
    
    # Collaborative Reasoning
    "CollaborativeReasoningInput",
    "CollaborativeReasoningOutput",
    "PersonaType",
    "PersonaContribution",
    "DebateRound",
]

__version__ = "2.0.0"
__author__ = "pydantic-model-engineer"