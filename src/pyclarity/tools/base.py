"""
Base classes for PyClarity cognitive analyzers.

Provides common interfaces and functionality for all cognitive tools.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from enum import Enum
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
    error_message: Optional[str] = None


class BaseCognitiveAnalyzer(ABC):
    """Base class for all cognitive analyzers"""
    
    def __init__(self):
        self.tool_name = "Base Cognitive Analyzer"
        self.version = "1.0.0"
    
    @abstractmethod
    async def analyze(self, context: BaseCognitiveContext) -> BaseCognitiveResult:
        """
        Perform cognitive analysis on the given context.
        
        Args:
            context: The analysis context
            
        Returns:
            Analysis results
        """
        pass
    
    def get_tool_info(self) -> Dict[str, Any]:
        """Get information about this tool"""
        return {
            "name": self.tool_name,
            "version": self.version,
            "description": self.__doc__ or "No description available"
        }