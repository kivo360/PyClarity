"""PyClarity - Cognitive tools for strategic thinking and decision-making.

PyClarity provides a comprehensive suite of cognitive analysis tools accessible
via an MCP (Model Context Protocol) server, enabling AI assistants to perform
sophisticated reasoning, decision-making, and problem-solving tasks.
"""

__version__ = "0.1.0"
__author__ = "Kevin Hill"
__email__ = "kevin@geodexes.com"

# Export main components
from .server import PyClarityMCPServer

__all__ = [
    "__version__",
    # Server functions
    "PyClarityMCPServer",
]
