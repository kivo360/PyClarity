"""
Progressive PyClarity MCP Server V2

Enhanced FastMCP-based server with session state management for ALL cognitive tools.
This version supports progressive analysis across all tools with session persistence.
"""

import logging
import os
from typing import Any, Dict, Optional

from fastmcp import FastMCP

from pyclarity.db.asyncpg_adapter import AsyncPGSessionStore, AsyncPGThoughtStore
from pyclarity.db.base import BaseSessionStore, BaseThoughtStore
from pyclarity.db.mental_model_store import BaseMentalModelStore
from pyclarity.db.debugging_store import BaseDebuggingStore
from pyclarity.db.collaborative_store import BaseCollaborativeStore
from pyclarity.db.decision_store import BaseDecisionStore
from pyclarity.db.metacognitive_store import BaseMetacognitiveStore
from pyclarity.db.scientific_store import BaseScientificStore
from pyclarity.db.visual_store import BaseVisualStore
from pyclarity.db.creative_store import BaseCreativeStore
from pyclarity.db.systems_store import BaseSystemsStore

from pyclarity.server.tool_handlers import CognitiveToolHandler
from pyclarity.tools.sequential_thinking.progressive_analyzer import (
    ProgressiveSequentialThinkingAnalyzer,
    ProgressiveThoughtRequest,
)
from pyclarity.tools.mental_models.progressive_analyzer import (
    ProgressiveMentalModelAnalyzer,
    ProgressiveMentalModelRequest,
)
from pyclarity.tools.debugging_approaches.progressive_analyzer import (
    ProgressiveDebuggingAnalyzer,
    ProgressiveDebuggingRequest,
)

logger = logging.getLogger(__name__)


class ProgressiveCognitiveToolHandlerV2(CognitiveToolHandler):
    """Extended handler with progressive support for ALL cognitive tools."""
    
    def __init__(
        self,
        session_store: Optional[BaseSessionStore] = None,
        thought_store: Optional[BaseThoughtStore] = None,
        mental_model_store: Optional[BaseMentalModelStore] = None,
        debugging_store: Optional[BaseDebuggingStore] = None,
        collaborative_store: Optional[BaseCollaborativeStore] = None,
        decision_store: Optional[BaseDecisionStore] = None,
        metacognitive_store: Optional[BaseMetacognitiveStore] = None,
        scientific_store: Optional[BaseScientificStore] = None,
        visual_store: Optional[BaseVisualStore] = None,
        creative_store: Optional[BaseCreativeStore] = None,
        systems_store: Optional[BaseSystemsStore] = None,
    ):
        """Initialize with all database stores."""
        super().__init__()
        self.session_store = session_store
        
        # Tool-specific stores
        self.thought_store = thought_store
        self.mental_model_store = mental_model_store
        self.debugging_store = debugging_store
        self.collaborative_store = collaborative_store
        self.decision_store = decision_store
        self.metacognitive_store = metacognitive_store
        self.scientific_store = scientific_store
        self.visual_store = visual_store
        self.creative_store = creative_store
        self.systems_store = systems_store
        
        # Initialize progressive analyzers if stores are provided
        if session_store:
            # Sequential Thinking
            if thought_store:
                self.progressive_sequential = ProgressiveSequentialThinkingAnalyzer(
                    session_store, thought_store
                )
            else:
                self.progressive_sequential = None
            
            # Mental Models
            if mental_model_store:
                self.progressive_mental_models = ProgressiveMentalModelAnalyzer(
                    session_store, mental_model_store
                )
            else:
                self.progressive_mental_models = None
            
            # Debugging Approaches
            if debugging_store:
                self.progressive_debugging = ProgressiveDebuggingAnalyzer(
                    session_store, debugging_store
                )
            else:
                self.progressive_debugging = None
            
            # TODO: Initialize other progressive analyzers as they're implemented
            self.progressive_collaborative = None
            self.progressive_decision = None
            self.progressive_metacognitive = None
            self.progressive_scientific = None
            self.progressive_visual = None
            self.progressive_creative = None
            self.progressive_systems = None
        else:
            # No progressive mode without session store
            self.progressive_sequential = None
            self.progressive_mental_models = None
            self.progressive_debugging = None
            self.progressive_collaborative = None
            self.progressive_decision = None
            self.progressive_metacognitive = None
            self.progressive_scientific = None
            self.progressive_visual = None
            self.progressive_creative = None
            self.progressive_systems = None
    
    async def handle_progressive_mental_models(
        self,
        session_id: Optional[str] = None,
        model_type: str = "first_principles",
        problem_statement: str = "",
        context: Optional[str] = None,
        previous_model_ids: Optional[list[int]] = None,
        build_on_previous: bool = False,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Handle progressive mental model application."""
        if not self.progressive_mental_models:
            return {
                "tool": "Progressive Mental Models",
                "error": "Progressive mode not configured. Database stores required.",
                "success": False
            }
        
        try:
            from pyclarity.tools.mental_models.models import MentalModelType
            
            # Convert string to enum
            model_type_enum = MentalModelType(model_type)
            
            request = ProgressiveMentalModelRequest(
                session_id=session_id,
                model_type=model_type_enum,
                problem_statement=problem_statement,
                context=context,
                previous_model_ids=previous_model_ids or [],
                build_on_previous=build_on_previous,
                metadata=metadata or {},
            )
            
            response = await self.progressive_mental_models.apply_model(request)
            
            return {
                "tool": "Progressive Mental Models",
                "response": response.model_dump(by_alias=True),
                "success": response.status == "success"
            }
            
        except Exception as e:
            logger.error(f"Progressive mental models failed: {e}")
            return {
                "tool": "Progressive Mental Models",
                "error": str(e),
                "success": False
            }
    
    async def handle_progressive_debugging(
        self,
        session_id: Optional[str] = None,
        step_number: int = 1,
        debugging_type: str = "systematic",
        issue_description: str = "",
        error_message: Optional[str] = None,
        stack_trace: Optional[str] = None,
        hypothesis: Optional[str] = None,
        evidence: Optional[list[str]] = None,
        test_plan: Optional[str] = None,
        previous_hypotheses: Optional[list[int]] = None,
        build_on_previous: bool = True,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Handle progressive debugging analysis."""
        if not self.progressive_debugging:
            return {
                "tool": "Progressive Debugging",
                "error": "Progressive mode not configured. Database stores required.",
                "success": False
            }
        
        try:
            request = ProgressiveDebuggingRequest(
                session_id=session_id,
                step_number=step_number,
                debugging_type=debugging_type,
                issue_description=issue_description,
                error_message=error_message,
                stack_trace=stack_trace,
                hypothesis=hypothesis,
                evidence=evidence or [],
                test_plan=test_plan,
                previous_hypotheses=previous_hypotheses or [],
                build_on_previous=build_on_previous,
                metadata=metadata or {},
            )
            
            response = await self.progressive_debugging.analyze_issue(request)
            
            return {
                "tool": "Progressive Debugging",
                "response": response.model_dump(by_alias=True),
                "success": response.status == "success"
            }
            
        except Exception as e:
            logger.error(f"Progressive debugging failed: {e}")
            return {
                "tool": "Progressive Debugging",
                "error": str(e),
                "success": False
            }


async def create_progressive_server_v2(db_url: Optional[str] = None) -> FastMCP:
    """
    Create PyClarity MCP server V2 with comprehensive progressive features.
    
    Args:
        db_url: Database URL for session persistence (e.g., postgresql://user:pass@host/db)
                If not provided, falls back to standard non-progressive mode.
    
    Returns:
        FastMCP: Configured server instance
    """
    # Initialize the FastMCP server
    mcp = FastMCP("PyClarity Progressive V2")
    
    # Initialize database stores if URL provided
    session_store = None
    thought_store = None
    mental_model_store = None
    debugging_store = None
    collaborative_store = None
    decision_store = None
    metacognitive_store = None
    scientific_store = None
    visual_store = None
    creative_store = None
    systems_store = None
    
    if db_url:
        logger.info("Initializing database stores for progressive mode...")
        
        if db_url.startswith("postgresql://"):
            # Use asyncpg for PostgreSQL
            from pyclarity.db.asyncpg_stores import (
                AsyncPGMentalModelStore,
                AsyncPGDebuggingStore,
                AsyncPGCollaborativeStore,
                AsyncPGDecisionStore,
                AsyncPGMetacognitiveStore,
                AsyncPGScientificStore,
                AsyncPGVisualStore,
                AsyncPGCreativeStore,
                AsyncPGSystemsStore,
            )
            
            # Base stores
            session_store = AsyncPGSessionStore(db_url)
            thought_store = AsyncPGThoughtStore(db_url)
            
            # Tool-specific stores
            mental_model_store = AsyncPGMentalModelStore(db_url)
            debugging_store = AsyncPGDebuggingStore(db_url)
            collaborative_store = AsyncPGCollaborativeStore(db_url)
            decision_store = AsyncPGDecisionStore(db_url)
            metacognitive_store = AsyncPGMetacognitiveStore(db_url)
            scientific_store = AsyncPGScientificStore(db_url)
            visual_store = AsyncPGVisualStore(db_url)
            creative_store = AsyncPGCreativeStore(db_url)
            systems_store = AsyncPGSystemsStore(db_url)
            
            # Initialize all database tables
            await session_store.init_db()
            await thought_store.init_db()
            await mental_model_store.init_db()
            await debugging_store.init_db()
            await collaborative_store.init_db()
            await decision_store.init_db()
            await metacognitive_store.init_db()
            await scientific_store.init_db()
            await visual_store.init_db()
            await creative_store.init_db()
            await systems_store.init_db()
            
            logger.info("All databases initialized for progressive mode")
        else:
            logger.warning(f"Unsupported database URL: {db_url}")
    
    # Initialize the cognitive tool handler with all stores
    tool_handler = ProgressiveCognitiveToolHandlerV2(
        session_store=session_store,
        thought_store=thought_store,
        mental_model_store=mental_model_store,
        debugging_store=debugging_store,
        collaborative_store=collaborative_store,
        decision_store=decision_store,
        metacognitive_store=metacognitive_store,
        scientific_store=scientific_store,
        visual_store=visual_store,
        creative_store=creative_store,
        systems_store=systems_store,
    )
    
    # Register all standard cognitive tools
    _register_standard_tools(mcp, tool_handler)
    
    # Register progressive tools if stores are available
    if session_store:
        _register_progressive_tools_v2(mcp, tool_handler)
    
    # Add server info
    logger.info("PyClarity Progressive MCP server V2 initialized")
    logger.info(f"Progressive mode: {'Enabled' if db_url else 'Disabled'}")
    if db_url:
        stores_initialized = [
            ("Sequential Thinking", bool(thought_store)),
            ("Mental Models", bool(mental_model_store)),
            ("Debugging", bool(debugging_store)),
            ("Collaborative", bool(collaborative_store)),
            ("Decision", bool(decision_store)),
            ("Metacognitive", bool(metacognitive_store)),
            ("Scientific", bool(scientific_store)),
            ("Visual", bool(visual_store)),
            ("Creative", bool(creative_store)),
            ("Systems", bool(systems_store)),
        ]
        for tool_name, initialized in stores_initialized:
            logger.info(f"  {tool_name}: {'✓' if initialized else '✗'}")
    
    return mcp


def _register_standard_tools(mcp: FastMCP, handler: ProgressiveCognitiveToolHandlerV2) -> None:
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
    
    # TODO: Register other standard tools...


def _register_progressive_tools_v2(mcp: FastMCP, handler: ProgressiveCognitiveToolHandlerV2) -> None:
    """Register ALL progressive cognitive tools that use session state."""
    
    # Progressive Sequential Thinking
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
    ) -> dict[str, Any]:
        """
        Progressive sequential thinking - one thought at a time with session state.
        
        Maintains context across calls, allowing for true step-by-step reasoning,
        branching, and revision of previous thoughts.
        """
        # Delegate to existing handler method
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
        )
    
    # Progressive Mental Models
    @mcp.tool()
    async def progressive_mental_models(
        session_id: str | None = None,
        model_type: str = "first_principles",
        problem_statement: str = "",
        context: str | None = None,
        previous_model_ids: list[int] | None = None,
        build_on_previous: bool = False,
    ) -> dict[str, Any]:
        """
        Apply mental models progressively with session persistence.
        
        Build complex analyses by layering different mental models,
        with each application building on previous insights.
        """
        return await handler.handle_progressive_mental_models(
            session_id=session_id,
            model_type=model_type,
            problem_statement=problem_statement,
            context=context,
            previous_model_ids=previous_model_ids,
            build_on_previous=build_on_previous,
        )
    
    # Progressive Debugging
    @mcp.tool()
    async def progressive_debugging(
        session_id: str | None = None,
        step_number: int = 1,
        debugging_type: str = "systematic",
        issue_description: str = "",
        error_message: str | None = None,
        stack_trace: str | None = None,
        hypothesis: str | None = None,
        evidence: list[str] | None = None,
        test_plan: str | None = None,
    ) -> dict[str, Any]:
        """
        Progressive debugging with hypothesis tracking and validation.
        
        Systematically debug issues with persistent session state,
        building evidence and testing hypotheses iteratively.
        """
        return await handler.handle_progressive_debugging(
            session_id=session_id,
            step_number=step_number,
            debugging_type=debugging_type,
            issue_description=issue_description,
            error_message=error_message,
            stack_trace=stack_trace,
            hypothesis=hypothesis,
            evidence=evidence,
            test_plan=test_plan,
        )
    
    # TODO: Add other progressive tools as they're implemented...
    
    logger.info("Progressive tools registered successfully")


if __name__ == "__main__":
    import asyncio
    
    async def main():
        # Example usage
        db_url = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/pyclarity")
        server = await create_progressive_server_v2(db_url)
        # Server would be run with FastMCP's run method
    
    asyncio.run(main())