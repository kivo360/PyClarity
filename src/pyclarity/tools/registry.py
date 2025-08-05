"""
Tool registry for PyClarity MCP Server

Manages registration and execution of cognitive tools.
"""

import logging
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class BaseTool(ABC):
    """Base class for all cognitive tools"""

    def __init__(self):
        self.name = self.__class__.__name__
        self.description = getattr(self, "description", "No description available")
        self.requires_auth = getattr(self, "requires_auth", True)
        self.parameter_schema = getattr(self, "parameter_schema", {})

    @abstractmethod
    async def analyze(self, **kwargs) -> Any:
        """Analyze the input and return results"""
        pass

    def get_schema(self) -> dict[str, Any]:
        """Get the tool's parameter schema"""
        return self.parameter_schema

    def get_description(self) -> str:
        """Get the tool's description"""
        return self.description


class ToolRegistry:
    """Registry for managing cognitive tools"""

    def __init__(self):
        self.tools: dict[str, BaseTool] = {}
        self.metadata: dict[str, dict[str, Any]] = {}

    def register_tool(self, name: str, tool: BaseTool) -> None:
        """Register a tool with the registry"""
        if not isinstance(tool, BaseTool):
            raise ValueError(f"Tool must inherit from BaseTool: {type(tool)}")

        self.tools[name] = tool
        self.metadata[name] = {
            "name": name,
            "description": tool.get_description(),
            "requires_auth": tool.requires_auth,
            "parameter_schema": tool.get_schema(),
            "class": tool.__class__.__name__,
        }

        logger.info(f"Registered tool: {name} ({tool.__class__.__name__})")

    def unregister_tool(self, name: str) -> None:
        """Unregister a tool from the registry"""
        if name in self.tools:
            del self.tools[name]
            del self.metadata[name]
            logger.info(f"Unregistered tool: {name}")

    def get_tool(self, name: str) -> BaseTool | None:
        """Get a tool by name"""
        return self.tools.get(name)

    def list_tools(self) -> dict[str, BaseTool]:
        """List all registered tools"""
        return self.tools.copy()

    def list_tool_names(self) -> list[str]:
        """List all registered tool names"""
        return list(self.tools.keys())

    def get_tool_metadata(self, name: str) -> dict[str, Any] | None:
        """Get metadata for a specific tool"""
        return self.metadata.get(name)

    def get_all_metadata(self) -> dict[str, dict[str, Any]]:
        """Get metadata for all tools"""
        return self.metadata.copy()

    def tool_exists(self, name: str) -> bool:
        """Check if a tool exists"""
        return name in self.tools

    def get_tool_count(self) -> int:
        """Get the total number of registered tools"""
        return len(self.tools)

    def clear(self) -> None:
        """Clear all registered tools"""
        self.tools.clear()
        self.metadata.clear()
        logger.info("Cleared all tools from registry")

    def validate_tool_parameters(self, name: str, parameters: dict[str, Any]) -> bool:
        """Validate parameters for a tool"""
        tool = self.get_tool(name)
        if not tool:
            return False

        schema = tool.get_schema()
        if not schema:
            return True  # No schema means no validation needed

        # Simple validation - in a real implementation, you'd use JSON Schema
        for param_name, param_info in schema.items():
            if param_name in parameters:
                param_type = param_info.get("type", "string")
                param_value = parameters[param_name]

                # Basic type checking
                if param_type == "string" and not isinstance(param_value, str):
                    return False
                elif param_type == "integer" and not isinstance(param_value, int):
                    return False
                elif param_type == "boolean" and not isinstance(param_value, bool):
                    return False

        return True

    async def execute_tool(self, name: str, **kwargs) -> Any:
        """Execute a tool with the given parameters"""
        tool = self.get_tool(name)
        if not tool:
            raise ValueError(f"Tool '{name}' not found")

        # Validate parameters
        if not self.validate_tool_parameters(name, kwargs):
            raise ValueError(f"Invalid parameters for tool '{name}'")

        # Execute the tool
        try:
            result = await tool.analyze(**kwargs)
            logger.info(f"Successfully executed tool: {name}")
            return result
        except Exception as e:
            logger.error(f"Error executing tool '{name}': {e}")
            raise


# Global tool registry instance
tool_registry = ToolRegistry()
