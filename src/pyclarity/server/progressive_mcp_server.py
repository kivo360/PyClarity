"""
Progressive PyClarity MCP Server

FastMCP-based server with session state management for progressive cognitive tools.
This version supports step-by-step thought generation for Sequential Thinking.
"""

import logging
import os
from typing import Any, Dict, Optional

from fastmcp import FastMCP

from pyclarity.db.asyncpg_adapter import AsyncPGSessionStore, AsyncPGThoughtStore
from pyclarity.db.base import BaseSessionStore, BaseThoughtStore
from pyclarity.server.tool_handlers import CognitiveToolHandler
from pyclarity.tools.sequential_thinking.progressive_analyzer import (
    ProgressiveSequentialThinkingAnalyzer,
    ProgressiveThoughtRequest,
)

logger = logging.getLogger(__name__)


class ProgressiveCognitiveToolHandler(CognitiveToolHandler):
    """Extended handler with progressive Sequential Thinking support."""
    
    def __init__(
        self,
        session_store: Optional[BaseSessionStore] = None,
        thought_store: Optional[BaseThoughtStore] = None,
    ):
        """Initialize with optional database stores."""
        super().__init__()
        self.session_store = session_store
        self.thought_store = thought_store
        
        # Initialize progressive analyzer if stores are provided
        if session_store and thought_store:
            self.progressive_sequential = ProgressiveSequentialThinkingAnalyzer(
                session_store, thought_store
            )
        else:
            self.progressive_sequential = None
    
    async def handle_progressive_sequential_thinking(
        self,
        session_id: Optional[str] = None,
        thought: str = "",
        thought_number: int = 1,
        total_thoughts: int = 5,
        next_thought_needed: bool = True,
        is_revision: bool = False,
        revises_thought: Optional[int] = None,
        branch_from_thought: Optional[int] = None,
        branch_id: Optional[str] = None,
        needs_more_thoughts: bool = False,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Handle progressive sequential thinking with session state."""
        if not self.progressive_sequential:
            return {
                "tool": "Progressive Sequential Thinking",
                "error": "Progressive mode not configured. Database stores required.",
                "success": False
            }
        
        try:
            request = ProgressiveThoughtRequest(
                session_id=session_id,
                thought=thought,
                thought_number=thought_number,
                total_thoughts=total_thoughts,
                next_thought_needed=next_thought_needed,
                is_revision=is_revision,
                revises_thought=revises_thought,
                branch_from_thought=branch_from_thought,
                branch_id=branch_id,
                needs_more_thoughts=needs_more_thoughts,
                metadata=metadata,
            )
            
            response = await self.progressive_sequential.process_thought(request)
            
            return {
                "tool": "Progressive Sequential Thinking",
                "response": response.to_dict(),
                "success": response.status == "success"
            }
            
        except Exception as e:
            logger.error(f"Progressive sequential thinking failed: {e}")
            return {
                "tool": "Progressive Sequential Thinking",
                "error": str(e),
                "success": False
            }


async def create_progressive_server(db_url: Optional[str] = None) -> FastMCP:
    """
    Create PyClarity MCP server with optional progressive features.
    
    Args:
        db_url: Database URL for session persistence (e.g., postgresql://user:pass@host/db)
                If not provided, falls back to standard non-progressive mode.
    
    Returns:
        FastMCP: Configured server instance
    """
    # Initialize the FastMCP server
    mcp = FastMCP("PyClarity Progressive")
    
    # Initialize database stores if URL provided
    session_store = None
    thought_store = None
    
    if db_url:
        logger.info("Initializing database stores for progressive mode...")
        
        if db_url.startswith("postgresql://"):
            # Use asyncpg for PostgreSQL
            session_store = AsyncPGSessionStore(db_url)
            thought_store = AsyncPGThoughtStore(db_url)
            
            # Initialize database tables
            await session_store.init_db()
            await thought_store.init_db()
            
            logger.info("Database initialized for progressive mode")
        else:
            logger.warning(f"Unsupported database URL: {db_url}")
    
    # Initialize the cognitive tool handler
    tool_handler = ProgressiveCognitiveToolHandler(session_store, thought_store)
    
    # Register all standard cognitive tools
    _register_standard_tools(mcp, tool_handler)
    
    # Register progressive sequential thinking if available
    if session_store and thought_store:
        _register_progressive_tools(mcp, tool_handler)
    
    # Add server info
    logger.info("PyClarity Progressive MCP server initialized")
    logger.info(f"Progressive mode: {'Enabled' if db_url else 'Disabled'}")
    
    return mcp


def _register_standard_tools(mcp: FastMCP, handler: ProgressiveCognitiveToolHandler) -> None:
    """Register standard cognitive tools (existing functionality)."""
    
    # Mental Models Tool
    @mcp.tool()
    async def mental_models_analysis(
        problem: str,
        model_type: str = "first_principles",
        complexity_level: str = "moderate",
        focus_areas: list[str] | None = None,
        constraints: list[str] | None = None,
        domain_expertise: str | None = None,
    ) -> dict[str, Any]:
        """
        Analyze problems using structured mental model frameworks.
        
        Available model types:
        - first_principles: Break down to fundamental truths
        - opportunity_cost: Analyze trade-offs and alternatives
        - error_propagation: Understand how errors compound
        - rubber_duck: Step-by-step explanation methodology
        - pareto_principle: Focus on highest-impact factors
        - occams_razor: Find simplest viable solutions
        """
        return await handler.handle_mental_models(
            problem=problem,
            model_type=model_type,
            complexity_level=complexity_level,
            focus_areas=focus_areas,
            constraints=constraints,
            domain_expertise=domain_expertise,
        )
    
    # Standard Sequential Thinking Tool (all at once)
    @mcp.tool()
    async def sequential_thinking(
        problem: str,
        complexity_level: str = "moderate",
        reasoning_depth: int = 5,
        enable_branching: bool = True,
        enable_revision: bool = True,
        branch_strategy: str = "adaptive"
    ) -> dict[str, Any]:
        """
        Apply structured sequential thinking with branching and revision.
        
        This version generates all thoughts at once. For progressive, step-by-step
        thinking, use progressive_sequential_thinking instead.
        """
        return await handler.handle_sequential_thinking(
            problem=problem,
            complexity_level=complexity_level,
            reasoning_depth=reasoning_depth,
            enable_branching=enable_branching,
            enable_revision=enable_revision,
            branch_strategy=branch_strategy
        )
    
    # Register other standard tools...
    # (Decision Framework, Scientific Method, etc. - same as original)


def _register_progressive_tools(mcp: FastMCP, handler: ProgressiveCognitiveToolHandler) -> None:
    """Register progressive cognitive tools that use session state."""
    
    @mcp.tool()
    async def progressive_sequential_thinking(
        session_id: str | None = None,
        thought: str = "",
        thought_number: int = 1,
        total_thoughts: int = 5,
        next_thought_needed: bool = True,
        is_revision: bool = False,
        revises_thought: int | None = None,
        branch_from_thought: int | None = None,
        branch_id: str | None = None,
        needs_more_thoughts: bool = False,
    ) -> dict[str, Any]:
        """
        Progressive sequential thinking - process one thought at a time.
        
        This tool maintains session state between calls, allowing for true
        step-by-step reasoning where each thought builds on previous ones.
        
        Args:
            session_id: Session identifier (auto-generated if not provided)
            thought: The current thought content
            thought_number: Sequential number of this thought (1-based)
            total_thoughts: Expected total thoughts in the sequence
            next_thought_needed: Whether another thought should follow
            is_revision: Whether this thought revises a previous one
            revises_thought: ID of thought being revised
            branch_from_thought: Parent thought for branching
            branch_id: Identifier for the branch
            needs_more_thoughts: Whether more thoughts than total are needed
        
        Returns:
            Response with thought ID, suggestions, and session info
        """
        return await handler.handle_progressive_sequential_thinking(
            session_id=session_id,
            thought=thought,
            thought_number=thought_number,
            total_thoughts=total_thoughts,
            next_thought_needed=next_thought_needed,
            is_revision=is_revision,
            revises_thought=revises_thought,
            branch_from_thought=branch_from_thought,
            branch_id=branch_id,
            needs_more_thoughts=needs_more_thoughts,
        )
    
    @mcp.tool()
    async def get_session_thoughts(
        session_id: str,
        branch_id: str | None = None,
    ) -> dict[str, Any]:
        """
        Retrieve all thoughts from a session.
        
        Args:
            session_id: Session identifier
            branch_id: Optional branch filter
        
        Returns:
            List of thoughts in the session/branch
        """
        try:
            thoughts = await handler.thought_store.get_session_thoughts(
                session_id, branch_id
            )
            
            return {
                "tool": "Get Session Thoughts",
                "session_id": session_id,
                "branch_id": branch_id,
                "thoughts": [
                    {
                        "id": t.id,
                        "thoughtNumber": t.thought_number,
                        "content": t.content,
                        "confidence": t.confidence,
                        "thoughtType": t.thought_type,
                        "isRevision": t.is_revision,
                        "createdAt": t.created_at.isoformat(),
                    }
                    for t in thoughts
                ],
                "count": len(thoughts),
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Failed to retrieve session thoughts: {e}")
            return {
                "tool": "Get Session Thoughts",
                "error": str(e),
                "success": False
            }


async def start_progressive_server(
    host: str = "localhost",
    port: int = 8000,
    debug: bool = False,
    db_url: Optional[str] = None,
) -> FastMCP:
    """
    Start the PyClarity Progressive MCP server.
    
    Args:
        host: Host to bind to
        port: Port to listen on
        debug: Enable debug logging
        db_url: Database URL for progressive features
    """
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    
    # Get database URL from environment if not provided
    if not db_url:
        db_url = os.getenv("PYCLARITY_DATABASE_URL")
    
    # Create the server
    mcp = await create_progressive_server(db_url)
    
    # Start the server
    logger.info(f"Starting PyClarity Progressive MCP server on {host}:{port}")
    if db_url:
        logger.info("Progressive mode enabled with session persistence")
    else:
        logger.info("Running in standard mode (no session persistence)")
    
    return mcp