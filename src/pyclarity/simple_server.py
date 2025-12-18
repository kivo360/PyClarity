#!/usr/bin/env python3
"""
Simple PyClarity MCP Server
A minimal FastMCP server for PyClarity cognitive tools.
"""

from fastmcp import FastMCP

from pyclarity.tools.sequential_thinking.analyzer import SequentialThinkingAnalyzer
from pyclarity.tools.sequential_thinking.models import (
    ComplexityLevel,
    SequentialThinkingContext,
    SequentialThinkingResult,
)

# Create the FastMCP server instance
app = FastMCP("PyClarity-Simple")

# Initialize cognitive tools
sequential_analyzer = SequentialThinkingAnalyzer()


@app.tool
def hello(name: str = "World") -> str:
    """A simple greeting tool to test the server."""
    return f"Hello, {name}! PyClarity server is working."


@app.tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b


@app.tool
async def sequential_thinking(problem: str, complexity_level: str = "moderate") -> dict:
    """
    Analyze a problem using sequential thinking methodology.

    Args:
        problem: The problem to analyze
        complexity_level: One of 'simple', 'moderate', 'complex', 'very_complex'

    Returns:
        Structured analysis with step-by-step breakdown
    """
    try:
        # Create context
        context = SequentialThinkingContext(
            problem=problem, complexity_level=ComplexityLevel(complexity_level)
        )

        # Run analysis
        result: SequentialThinkingResult = await sequential_analyzer.analyze(context)

        # Convert to dict for JSON serialization
        return result.model_dump()

    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}


if __name__ == "__main__":
    print("Starting PyClarity Simple MCP Server...")
    app.run()
