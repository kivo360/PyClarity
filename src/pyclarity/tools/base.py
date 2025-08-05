"""
Base classes for PyClarity cognitive analyzers.

Provides common interfaces and functionality for all cognitive tools.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, Generic, Optional, TypeVar

from pydantic import BaseModel


class ComplexityLevel(str, Enum):
    """Standard complexity levels used across all tools"""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    VERY_COMPLEX = "very_complex"


class BaseCognitiveContext(BaseModel):
    """Base context class for all cognitive tools"""
    problem: str
    complexity_level: ComplexityLevel = ComplexityLevel.MODERATE


class BaseCognitiveResult(BaseModel):
    """Base result class for all cognitive tools"""
    tool_name: str
    complexity_level: ComplexityLevel
    processing_time_ms: float
    success: bool
    error_message: str | None = None


# Generic type variables for context and result models
Ctx = TypeVar("Ctx", bound=BaseCognitiveContext)
Res = TypeVar("Res", bound=BaseCognitiveResult)


class BaseCognitiveAnalyzer(Generic[Ctx, Res], ABC):
    """Base class for all cognitive analyzers"""

    def __init__(
        self,
        tool_name: str = "Base Cognitive Analyzer",
        tool_description: str = "Generic cognitive analyzer.",
        version: str = "1.0.0",
    ) -> None:
        """Initialize a cognitive analyzer.

        Args:
            tool_name: Human-readable name of the tool.
            tool_description: Short description of what the tool does.
            version: Semantic version string.
        """
        self.tool_name = tool_name
        self.tool_description = tool_description
        self.version = version

    @abstractmethod
    async def analyze(self, context: Ctx) -> Res:
        """
        Perform cognitive analysis on the given context.

        Args:
            context: The analysis context

        Returns:
            Analysis results
        """
        pass

    def get_tool_info(self) -> dict[str, Any]:
        """Get information about this tool"""
        return {
            "name": self.tool_name,
            "version": self.version,
            "description": self.__doc__ or "No description available"
        }
