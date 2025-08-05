"""
PyClarity MCP Server Implementation

Provides a secure MCP server with authentication for PyClarity's cognitive tools.
"""

import asyncio
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastmcp import FastMCP
from pydantic import BaseModel, Field

from pyclarity.auth.middleware import AuthMiddleware
from pyclarity.config import MCPConfig
from pyclarity.tools.registry import BaseTool, ToolRegistry

logger = logging.getLogger(__name__)


class ToolRequest(BaseModel):
    """Request model for tool execution"""

    tool_name: str = Field(..., description="Name of the tool to execute")
    parameters: dict[str, Any] = Field(default_factory=dict, description="Tool parameters")
    session_id: str | None = Field(None, description="Session ID for tracking")


class ToolResponse(BaseModel):
    """Response model for tool execution"""

    success: bool = Field(..., description="Whether the tool execution was successful")
    result: Any = Field(None, description="Tool execution result")
    error: str | None = Field(None, description="Error message if execution failed")
    session_id: str | None = Field(None, description="Session ID for tracking")


class AnalyzerAdapter(BaseTool):
    """Adapter class to make analyzers compatible with the tool registry"""

    def __init__(self, analyzer, tool_name: str, description: str = ""):
        super().__init__()
        self.analyzer = analyzer
        self.name = tool_name
        self.description = description or getattr(analyzer, "tool_description", "")
        self.requires_auth = True
        self.parameter_schema = {
            "type": "object",
            "properties": {
                "problem": {"type": "string", "description": "Problem to analyze"},
                "complexity_level": {
                    "type": "string",
                    "enum": ["simple", "moderate", "complex", "very_complex"],
                },
            },
            "required": ["problem"],
        }

    async def analyze(self, **kwargs) -> Any:
        """Execute the analyzer with the given parameters"""
        try:
            # Create context from parameters
            from pyclarity.tools.base import BaseCognitiveContext, ComplexityLevel

            complexity = kwargs.get("complexity_level", "moderate")
            context = BaseCognitiveContext(
                problem=kwargs.get("problem", ""), complexity_level=ComplexityLevel(complexity)
            )

            # Execute the analyzer
            result = await self.analyzer.analyze(context)
            return result
        except Exception as e:
            logger.error(f"Error executing analyzer {self.name}: {e}")
            raise


class PyClarityMCPServer:
    """Main MCP server class for PyClarity"""

    def __init__(self, config: MCPConfig | None = None):
        """Initialize the MCP server"""
        self.config = config or MCPConfig()
        self.fastmcp = FastMCP()
        self.auth = AuthMiddleware(self.config.auth.jwt_secret)
        self.tools = ToolRegistry()

        # Register default tools
        self._register_default_tools()

        # Setup FastAPI routes
        self._setup_routes()

    def _register_default_tools(self):
        """Register default cognitive tools"""
        try:
            from pyclarity.tools.decision_framework.analyzer import DecisionFrameworkAnalyzer
            from pyclarity.tools.mental_models.analyzer import MentalModelsAnalyzer
            from pyclarity.tools.sequential_thinking.analyzer import (
                SequentialThinkingAnalyzer,
            )

            # Create adapters for the analyzers
            sequential_analyzer = SequentialThinkingAnalyzer()
            decision_analyzer = DecisionFrameworkAnalyzer()
            mental_models_analyzer = MentalModelsAnalyzer()

            # Register tools with adapters
            self.tools.register_tool(
                "sequential_thinking",
                AnalyzerAdapter(
                    sequential_analyzer,
                    "Sequential Thinking",
                    "Step-by-step problem decomposition and reasoning",
                ),
            )
            self.tools.register_tool(
                "decision_framework",
                AnalyzerAdapter(
                    decision_analyzer, "Decision Framework", "Structured decision-making analysis"
                ),
            )
            self.tools.register_tool(
                "mental_models",
                AnalyzerAdapter(
                    mental_models_analyzer,
                    "Mental Models",
                    "Mental models analysis for complex problems",
                ),
            )

            logger.info("Default tools registered successfully")
        except ImportError as e:
            logger.warning(f"Could not register default tools: {e}")

    def _setup_routes(self):
        """Setup FastAPI routes for the MCP server"""
        # For now, we'll use a simple approach without FastMCP's app
        # In a real implementation, you'd integrate with FastMCP's routing system
        pass

    def _check_tool_permissions(self, tool_name: str, user: dict | None) -> bool:
        """Check if user has permission to execute the tool"""
        if not self.config.auth.enabled:
            return True

        if not user:
            return False

        tool = self.tools.get_tool(tool_name)
        requires_auth = getattr(tool, "requires_auth", True)

        if not requires_auth:
            return True

        # Check user permissions
        user_role = user.get("role", "user")
        if user_role == "admin":
            return True

        # Add more granular permission checks here
        return True

    async def start(self, host: str = "localhost", port: int = 8000):
        """Start the MCP server"""
        logger.info(f"Starting PyClarity MCP server on {host}:{port}")

        # For now, just log that the server would start
        # In a real implementation, you'd start the FastMCP server
        logger.info("MCP server would start here")
        logger.info(f"Available tools: {list(self.tools.list_tools().keys())}")

    async def stop(self):
        """Stop the MCP server"""
        logger.info("Stopping PyClarity MCP server")


async def main():
    """Main entry point for the MCP server"""
    import argparse

    parser = argparse.ArgumentParser(description="PyClarity MCP Server")
    parser.add_argument("--host", default="localhost", help="Server host")
    parser.add_argument("--port", type=int, default=8000, help="Server port")
    parser.add_argument("--config", help="Configuration file path")

    args = parser.parse_args()

    # Load configuration
    config = MCPConfig.from_file(args.config) if args.config else MCPConfig()

    # Create and start server
    server = PyClarityMCPServer(config)

    try:
        await server.start(host=args.host, port=args.port)
    except KeyboardInterrupt:
        logger.info("Received interrupt signal, shutting down...")
    finally:
        await server.stop()


if __name__ == "__main__":
    asyncio.run(main())
