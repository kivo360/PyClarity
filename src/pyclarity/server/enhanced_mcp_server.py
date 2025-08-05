"""Enhanced MCP server with automatic schema generation and progressive thinking."""

import asyncio
import logging
import os
from typing import Any, Dict, Optional

from fastmcp.mcp import FastMCP
from pydantic import BaseModel, Field

from pyclarity.db.asyncpg_adapter import AsyncPGSessionStore, AsyncPGThoughtStore
from pyclarity.schema_generator.auto_detector import (
    ensure_schema_examples,
    get_auto_generator,
)
from pyclarity.server.progressive_mcp_server import (
    ProgressiveThoughtRequest,
    ProgressiveThoughtResponse,
    SessionThoughtsRequest,
    SessionThoughtsResponse,
)
from pyclarity.tools.sequential_thinking.progressive_analyzer import (
    ProgressiveSequentialThinkingAnalyzer,
)

# Import all cognitive tools for registration
from pyclarity.tools import (
    MentalModelsAnalyzer,
    DecisionFrameworkAnalyzer,
    # ... other tools
)

logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("PyClarity Enhanced Server")


class ToolRegistrationInfo(BaseModel):
    """Information for registering a tool with the server."""
    
    name: str
    handler: Any
    input_model: type[BaseModel]
    output_model: Optional[type[BaseModel]] = None
    description: str = ""


# Database stores (initialized on startup)
session_store: Optional[AsyncPGSessionStore] = None
thought_store: Optional[AsyncPGThoughtStore] = None
progressive_analyzer: Optional[ProgressiveSequentialThinkingAnalyzer] = None


async def initialize_server():
    """Initialize server components."""
    global session_store, thought_store, progressive_analyzer
    
    # Get database URL from environment
    db_url = os.getenv("DATABASE_URL", "postgresql://pyclarity:pyclarity@localhost:5432/pyclarity")
    
    # Initialize database stores
    session_store = AsyncPGSessionStore(db_url)
    thought_store = AsyncPGThoughtStore(db_url)
    
    # Initialize database tables
    await session_store.init_db()
    await thought_store.init_db()
    
    # Initialize progressive analyzer
    progressive_analyzer = ProgressiveSequentialThinkingAnalyzer(
        session_store=session_store,
        thought_store=thought_store
    )
    
    # Initialize schema generator
    generator = get_auto_generator()
    await generator.initialize()
    
    logger.info("Server components initialized")


async def shutdown_server():
    """Cleanup server components."""
    if session_store:
        await session_store.close()
    if thought_store:
        await thought_store.close()
    
    logger.info("Server components shut down")


# Register progressive sequential thinking tool
@mcp.tool()
async def progressive_sequential_thinking(
    thought: str = Field(..., description="The current thought to process"),
    thought_number: int = Field(..., description="The number of this thought in the sequence"),
    total_thoughts: int = Field(..., description="Total expected thoughts in this sequence"),
    next_thought_needed: bool = Field(True, description="Whether another thought is needed"),
    session_id: Optional[str] = Field(None, description="Session ID for continuing existing session"),
    branch_from_thought: Optional[int] = Field(None, description="Thought number to branch from"),
    branch_id: Optional[str] = Field(None, description="Unique identifier for this branch"),
    is_revision: bool = Field(False, description="Whether this revises a previous thought"),
    revises_thought: Optional[int] = Field(None, description="Which thought this revises"),
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
) -> ProgressiveThoughtResponse:
    """Process a single thought in a progressive sequential thinking session."""
    if not progressive_analyzer:
        raise RuntimeError("Server not initialized")
    
    request = ProgressiveThoughtRequest(
        thought=thought,
        thought_number=thought_number,
        total_thoughts=total_thoughts,
        next_thought_needed=next_thought_needed,
        session_id=session_id,
        branch_from_thought=branch_from_thought,
        branch_id=branch_id,
        is_revision=is_revision,
        revises_thought=revises_thought,
        metadata=metadata or {}
    )
    
    return await progressive_analyzer.process_thought(request)


@mcp.tool()
async def get_session_thoughts(
    session_id: str = Field(..., description="Session ID to retrieve thoughts for"),
    branch_id: Optional[str] = Field(None, description="Optional branch ID to filter by")
) -> SessionThoughtsResponse:
    """Retrieve all thoughts from a sequential thinking session."""
    if not thought_store:
        raise RuntimeError("Server not initialized")
    
    thoughts = await thought_store.get_session_thoughts(session_id, branch_id)
    
    return SessionThoughtsResponse(
        success=True,
        thoughts=[
            {
                "thoughtNumber": t.thought_number,
                "content": t.content,
                "thoughtType": t.thought_type,
                "confidence": t.confidence,
                "branchId": t.branch_id,
                "isRevision": t.is_revision,
                "metadata": t.metadata
            }
            for t in thoughts
        ],
        count=len(thoughts),
        sessionId=session_id,
        branchId=branch_id
    )


async def register_cognitive_tools():
    """Register all cognitive tools with automatic schema generation."""
    tools_to_register = [
        ToolRegistrationInfo(
            name="mental_models",
            handler=lambda req: MentalModelsAnalyzer().analyze(req),
            input_model=MentalModelsAnalyzer.Request,
            output_model=MentalModelsAnalyzer.Response,
            description="Apply different mental models to analyze a situation from multiple perspectives"
        ),
        ToolRegistrationInfo(
            name="decision_framework",
            handler=lambda req: DecisionFrameworkAnalyzer().analyze(req),
            input_model=DecisionFrameworkAnalyzer.Request,
            output_model=DecisionFrameworkAnalyzer.Response,
            description="Evaluate decisions using multiple criteria and weighted scoring"
        ),
        # Add more tools here...
    ]
    
    for tool_info in tools_to_register:
        # Generate schema examples if LLM is available
        example = await ensure_schema_examples(
            tool_name=tool_info.name,
            input_model=tool_info.input_model,
            output_model=tool_info.output_model,
            description=tool_info.description
        )
        
        # Register the tool with MCP
        # Note: This is pseudo-code - actual registration depends on FastMCP API
        # mcp.register_tool(
        #     name=tool_info.name,
        #     handler=tool_info.handler,
        #     description=tool_info.description,
        #     examples=example.examples if example else None
        # )
        
        if example:
            logger.info(f"Registered {tool_info.name} with {len(example.examples)} auto-generated examples")
        else:
            logger.info(f"Registered {tool_info.name} without examples (no LLM available)")


# Server lifecycle hooks
@mcp.on_startup()
async def on_startup():
    """Initialize server on startup."""
    await initialize_server()
    await register_cognitive_tools()
    
    # Log LLM availability
    generator = get_auto_generator()
    if await generator.initialize():
        logger.info("✅ LLM detected - automatic schema generation enabled")
    else:
        logger.warning("⚠️  No LLM detected - schema generation disabled")
        logger.info("   To enable: Set OPENAI_API_KEY, ANTHROPIC_API_KEY, or LOCAL_LLM_BASE_URL in .env")


@mcp.on_shutdown()
async def on_shutdown():
    """Cleanup on shutdown."""
    await shutdown_server()


# Example: Test schema generation
async def test_schema_generation():
    """Test automatic schema generation."""
    # This would be called during development to test the system
    generator = get_auto_generator()
    
    if await generator.initialize():
        # Test with progressive thinking
        example = await ensure_schema_examples(
            tool_name="progressive_sequential_thinking",
            input_model=ProgressiveThoughtRequest,
            output_model=ProgressiveThoughtResponse,
            description="Process thoughts one at a time with session state"
        )
        
        if example:
            print(f"Generated {len(example.examples)} examples:")
            for ex in example.examples:
                print(f"  - {ex.get('example_name', 'Example')}: {ex.get('description', 'No description')}")
        else:
            print("Failed to generate examples")
    else:
        print("No LLM available for testing")


if __name__ == "__main__":
    # For testing the schema generation
    asyncio.run(test_schema_generation())