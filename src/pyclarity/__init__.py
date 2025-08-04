"""PyClarity - Cognitive tools for strategic thinking and decision-making.

PyClarity provides a comprehensive suite of cognitive analysis tools accessible
via an MCP (Model Context Protocol) server, enabling AI assistants to perform
sophisticated reasoning, decision-making, and problem-solving tasks.
"""

__version__ = "0.1.0"
__author__ = "Kevin Hill"
__email__ = "kevin@geodexes.com"

# Export main components
from .tools import (
    # Core analyzers
    SequentialThinkingAnalyzer,
    MentalModelsAnalyzer,
    DecisionFrameworkAnalyzer,
    ScientificMethodAnalyzer,
    # Analysis tools
    DesignPatternsAnalyzer,
    ProgrammingParadigmsAnalyzer,
    DebuggingApproachesAnalyzer,
    VisualReasoningAnalyzer,
    # Reasoning tools
    StructuredArgumentationAnalyzer,
    MetacognitiveMonitoringAnalyzer,
    CollaborativeReasoningAnalyzer,
    # New FastMCP tools
    IterativeValidationAnalyzer,
    MultiPerspectiveAnalyzer,
    SequentialReadinessAnalyzer,
    TripleConstraintAnalyzer,
)

from .server import create_server, start_server

__all__ = [
    "__version__",
    # Server functions
    "create_server",
    "start_server",
    # Core analyzers
    "SequentialThinkingAnalyzer",
    "MentalModelsAnalyzer", 
    "DecisionFrameworkAnalyzer",
    "ScientificMethodAnalyzer",
    # Analysis tools
    "DesignPatternsAnalyzer",
    "ProgrammingParadigmsAnalyzer",
    "DebuggingApproachesAnalyzer",
    "VisualReasoningAnalyzer",
    # Reasoning tools
    "StructuredArgumentationAnalyzer",
    "MetacognitiveMonitoringAnalyzer",
    "CollaborativeReasoningAnalyzer",
    # New FastMCP tools
    "IterativeValidationAnalyzer",
    "MultiPerspectiveAnalyzer",
    "SequentialReadinessAnalyzer",
    "TripleConstraintAnalyzer",
]
