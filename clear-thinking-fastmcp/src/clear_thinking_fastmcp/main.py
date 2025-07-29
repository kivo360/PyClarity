# Clear Thinking FastMCP Server - Main Server

"""
Main FastMCP server implementing all 11 cognitive tools.

This server provides advanced cognitive reasoning capabilities through
the Model Context Protocol using the FastMCP framework.

Agent: cognitive-tool-implementer  
Status: ACTIVE - Core server implementation with Mental Models tool
"""

from fastmcp import FastMCP
from fastmcp.server import Context
import asyncio
import time
from typing import Dict, Any

# Import models (from pydantic-model-engineer)
from .models.mental_models import (
    MentalModelInput,
    MentalModelOutput, 
    MentalModelType,
    MentalModelInsight,
    MentalModelAssumption
)

# Import tool servers (to be implemented)
from .tools.mental_model_server import MentalModelServer


def create_server() -> FastMCP:
    """Create and configure the Clear Thinking FastMCP server"""
    
    mcp = FastMCP(
        name="ClearThinkingServer",
        version="2.0.0",
        description="Advanced cognitive reasoning tools via FastMCP"
    )
    
    # Initialize tool servers
    mental_model_server = MentalModelServer()
    
    # COGNITIVE TOOL 1: Mental Models
    @mcp.tool
    async def mental_model_tool(
        input_data: MentalModelInput,
        ctx: Context
    ) -> MentalModelOutput:
        """
        Apply structured mental model frameworks to problem analysis.
        
        This tool provides six different mental models:
        - First Principles: Break down to fundamental truths
        - Opportunity Cost: Analyze trade-offs and alternatives  
        - Error Propagation: Understand how failures cascade
        - Rubber Duck: Step-by-step problem explanation
        - Pareto Principle: Focus on critical 20% factors
        - Occam's Razor: Prefer simplest viable solutions
        """
        start_time = time.time()
        
        try:
            # Context integration - logging and progress
            ctx.info(f"Starting mental model analysis: {input_data.model_type.value}")
            ctx.debug(f"Problem: {input_data.problem[:100]}...")
            ctx.progress(0.0, 1.0, "Initializing mental model analysis")
            
            # Validate input compatibility
            ctx.progress(0.1, 1.0, "Validating input compatibility")
            if not await mental_model_server.validate_input(input_data):
                raise ValueError("Input data is not compatible with selected mental model")
            
            # Process with mental model server
            ctx.progress(0.3, 1.0, f"Applying {input_data.model_type.value} framework")
            result = await mental_model_server.process(input_data, ctx)
            
            # Add processing time
            processing_time = (time.time() - start_time) * 1000
            result.processing_time_ms = processing_time
            
            ctx.progress(1.0, 1.0, "Mental model analysis complete")
            ctx.info(f"Analysis completed in {processing_time:.1f}ms with confidence {result.confidence_score:.3f}")
            
            return result
            
        except Exception as e:
            ctx.error(f"Mental model analysis failed: {str(e)}")
            ctx.debug(f"Error details: {type(e).__name__}: {e}")
            raise
    
    # COGNITIVE TOOL 2: Sequential Thinking (Placeholder)
    @mcp.tool
    async def sequential_thinking_tool(
        problem: str,
        max_steps: int = 10,
        ctx: Context = None
    ) -> Dict[str, Any]:
        """
        Apply sequential thinking with dynamic thought progression and branching.
        
        This tool provides step-by-step reasoning with:
        - Thought chain progression
        - Branching for alternative paths
        - Revision capabilities
        - Context-aware reasoning
        """
        if ctx:
            ctx.info("Sequential thinking tool called (implementation pending)")
            ctx.progress(1.0, 1.0, "Placeholder response generated")
        
        return {
            "tool": "sequential_thinking",
            "status": "placeholder",
            "message": "Implementation pending - pydantic-model-engineer completing models"
        }
    
    # COGNITIVE TOOL 3: Collaborative Reasoning (Placeholder)
    @mcp.tool
    async def collaborative_reasoning_tool(
        problem: str,
        personas: list = None,
        ctx: Context = None
    ) -> Dict[str, Any]:
        """
        Apply collaborative reasoning with multi-persona simulation.
        
        This tool provides:
        - Multiple perspective analysis
        - Persona-based reasoning
        - Structured debate simulation
        - Consensus building
        """
        if ctx:
            ctx.info("Collaborative reasoning tool called (implementation pending)")
            ctx.progress(1.0, 1.0, "Placeholder response generated")
        
        return {
            "tool": "collaborative_reasoning", 
            "status": "placeholder",
            "message": "Implementation pending - pydantic-model-engineer completing models"
        }
    
    # TODO: Add remaining 8 cognitive tools as they are implemented
    # - Decision Framework
    # - Metacognitive Monitoring  
    # - Scientific Method
    # - Structured Argumentation
    # - Visual Reasoning
    # - Design Patterns
    # - Programming Paradigms
    # - Debugging Approaches
    
    return mcp


def main():
    """Main entry point for the server"""
    mcp = create_server()
    
    # Run with STDIO transport (compatible with Claude Desktop)
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()