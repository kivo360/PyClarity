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
from pyclarity.db.collaborative_store import BaseCollaborativeStore
from pyclarity.db.creative_store import BaseCreativeStore
from pyclarity.db.debugging_store import BaseDebuggingStore
from pyclarity.db.decision_store import BaseDecisionStore
from pyclarity.db.mental_model_store import BaseMentalModelStore
from pyclarity.db.metacognitive_store import BaseMetacognitiveStore
from pyclarity.db.scientific_store import BaseScientificStore
from pyclarity.db.systems_store import BaseSystemsStore
from pyclarity.db.visual_store import BaseVisualStore
from pyclarity.server.tool_handlers import CognitiveToolHandler
from pyclarity.tools.collaborative_reasoning.progressive_analyzer import (
    ProgressiveCollaborativeAnalyzer,
    ProgressiveCollaborativeRequest,
)
from pyclarity.tools.creative_thinking.progressive_analyzer import (
    ProgressiveCreativeAnalyzer,
    ProgressiveCreativeRequest,
)
from pyclarity.tools.debugging_approaches.progressive_analyzer import (
    ProgressiveDebuggingAnalyzer,
    ProgressiveDebuggingRequest,
)
from pyclarity.tools.decision_framework.progressive_analyzer import (
    ProgressiveDecisionAnalyzer,
    ProgressiveDecisionRequest,
)
from pyclarity.tools.mental_models.progressive_analyzer import (
    ProgressiveMentalModelAnalyzer,
    ProgressiveMentalModelRequest,
)
from pyclarity.tools.metacognitive_monitoring.progressive_analyzer import (
    ProgressiveMetacognitiveAnalyzer,
    ProgressiveMetacognitiveRequest,
)
from pyclarity.tools.scientific_method.progressive_analyzer import (
    ProgressiveScientificAnalyzer,
    ProgressiveScientificRequest,
)
from pyclarity.tools.sequential_thinking.progressive_analyzer import (
    ProgressiveSequentialThinkingAnalyzer,
    ProgressiveThoughtRequest,
)
from pyclarity.tools.systems_thinking.progressive_analyzer import (
    ProgressiveSystemsAnalyzer,
    ProgressiveSystemsRequest,
)
from pyclarity.tools.visual_reasoning.progressive_analyzer import (
    ProgressiveVisualAnalyzer,
    ProgressiveVisualRequest,
)

logger = logging.getLogger(__name__)


class ProgressiveCognitiveToolHandlerV2(CognitiveToolHandler):
    """Extended handler with progressive support for ALL cognitive tools."""

    def __init__(
        self,
        session_store: BaseSessionStore | None = None,
        thought_store: BaseThoughtStore | None = None,
        mental_model_store: BaseMentalModelStore | None = None,
        debugging_store: BaseDebuggingStore | None = None,
        collaborative_store: BaseCollaborativeStore | None = None,
        decision_store: BaseDecisionStore | None = None,
        metacognitive_store: BaseMetacognitiveStore | None = None,
        scientific_store: BaseScientificStore | None = None,
        visual_store: BaseVisualStore | None = None,
        creative_store: BaseCreativeStore | None = None,
        systems_store: BaseSystemsStore | None = None,
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

            # Collaborative Reasoning
            if collaborative_store:
                self.progressive_collaborative = ProgressiveCollaborativeAnalyzer(
                    session_store, collaborative_store
                )
            else:
                self.progressive_collaborative = None

            # Decision Framework
            if decision_store:
                self.progressive_decision = ProgressiveDecisionAnalyzer(
                    session_store, decision_store
                )
            else:
                self.progressive_decision = None

            # Metacognitive Monitoring
            if metacognitive_store:
                self.progressive_metacognitive = ProgressiveMetacognitiveAnalyzer(
                    session_store, metacognitive_store
                )
            else:
                self.progressive_metacognitive = None

            # Scientific Method
            if scientific_store:
                self.progressive_scientific = ProgressiveScientificAnalyzer(
                    session_store, scientific_store
                )
            else:
                self.progressive_scientific = None

            # Visual Reasoning
            if visual_store:
                self.progressive_visual = ProgressiveVisualAnalyzer(session_store, visual_store)
            else:
                self.progressive_visual = None

            # Creative Thinking
            if creative_store:
                self.progressive_creative = ProgressiveCreativeAnalyzer(
                    session_store, creative_store
                )
            else:
                self.progressive_creative = None

            # Systems Thinking
            if systems_store:
                self.progressive_systems = ProgressiveSystemsAnalyzer(session_store, systems_store)
            else:
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
        session_id: str | None = None,
        model_type: str = "first_principles",
        problem_statement: str = "",
        context: str | None = None,
        previous_model_ids: list[int] | None = None,
        build_on_previous: bool = False,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Handle progressive mental model application."""
        if not self.progressive_mental_models:
            return {
                "tool": "Progressive Mental Models",
                "error": "Progressive mode not configured. Database stores required.",
                "success": False,
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
                "success": response.status == "success",
            }

        except Exception as e:
            logger.error(f"Progressive mental models failed: {e}")
            return {"tool": "Progressive Mental Models", "error": str(e), "success": False}

    async def handle_progressive_debugging(
        self,
        session_id: str | None = None,
        step_number: int = 1,
        debugging_type: str = "systematic",
        issue_description: str = "",
        error_message: str | None = None,
        stack_trace: str | None = None,
        hypothesis: str | None = None,
        evidence: list[str] | None = None,
        test_plan: str | None = None,
        previous_hypotheses: list[int] | None = None,
        build_on_previous: bool = True,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Handle progressive debugging analysis."""
        if not self.progressive_debugging:
            return {
                "tool": "Progressive Debugging",
                "error": "Progressive mode not configured. Database stores required.",
                "success": False,
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
                "success": response.status == "success",
            }

        except Exception as e:
            logger.error(f"Progressive debugging failed: {e}")
            return {"tool": "Progressive Debugging", "error": str(e), "success": False}

    async def handle_progressive_collaborative(
        self,
        session_id: str | None = None,
        step_number: int = 1,
        collaboration_type: str = "consensus_building",
        topic: str = "",
        context: str = "",
        personas: list[dict[str, Any]] | None = None,
        contributions: list[dict[str, Any]] | None = None,
        synthesis_approach: str = "integrative",
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Handle progressive collaborative reasoning."""
        if not self.progressive_collaborative:
            return {
                "tool": "Progressive Collaborative Reasoning",
                "error": "Progressive mode not configured. Database stores required.",
                "success": False,
            }

        try:
            from pyclarity.tools.collaborative_reasoning.models import (
                CollaborationType,
                SynthesisApproach,
            )

            request = ProgressiveCollaborativeRequest(
                session_id=session_id,
                step_number=step_number,
                collaboration_type=CollaborationType(collaboration_type),
                topic=topic,
                context=context,
                personas=personas or [],
                contributions=contributions or [],
                synthesis_approach=SynthesisApproach(synthesis_approach),
                metadata=metadata or {},
            )

            response = await self.progressive_collaborative.collaborate(request)

            return {
                "tool": "Progressive Collaborative Reasoning",
                "response": response.model_dump(by_alias=True),
                "success": response.status == "success",
            }

        except Exception as e:
            logger.error(f"Progressive collaborative reasoning failed: {e}")
            return {
                "tool": "Progressive Collaborative Reasoning",
                "error": str(e),
                "success": False,
            }

    async def handle_progressive_decision(
        self,
        session_id: str | None = None,
        step_number: int = 1,
        decision_context: str = "",
        decision_type: str = "strategic",
        criteria: list[dict[str, Any]] | None = None,
        alternatives: list[dict[str, Any]] | None = None,
        evaluation_method: str = "weighted_criteria",
        time_pressure: str = "moderate",
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Handle progressive decision framework analysis."""
        if not self.progressive_decision:
            return {
                "tool": "Progressive Decision Framework",
                "error": "Progressive mode not configured. Database stores required.",
                "success": False,
            }

        try:
            from pyclarity.tools.decision_framework.models import (
                DecisionType,
                EvaluationMethod,
                TimePressure,
            )

            request = ProgressiveDecisionRequest(
                session_id=session_id,
                step_number=step_number,
                decision_context=decision_context,
                decision_type=DecisionType(decision_type),
                criteria=criteria or [],
                alternatives=alternatives or [],
                evaluation_method=EvaluationMethod(evaluation_method),
                time_pressure=TimePressure(time_pressure),
                metadata=metadata or {},
            )

            response = await self.progressive_decision.analyze_decision(request)

            return {
                "tool": "Progressive Decision Framework",
                "response": response.model_dump(by_alias=True),
                "success": response.status == "success",
            }

        except Exception as e:
            logger.error(f"Progressive decision analysis failed: {e}")
            return {"tool": "Progressive Decision Framework", "error": str(e), "success": False}

    async def handle_progressive_metacognitive(
        self,
        session_id: str | None = None,
        step_number: int = 1,
        current_thought: str = "",
        thinking_context: str = "",
        thinking_mode: str = "analytical",
        confidence_level: float = 0.5,
        clarity_level: float = 0.5,
        reflection_depth: str = "moderate",
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Handle progressive metacognitive monitoring."""
        if not self.progressive_metacognitive:
            return {
                "tool": "Progressive Metacognitive Monitoring",
                "error": "Progressive mode not configured. Database stores required.",
                "success": False,
            }

        try:
            from pyclarity.tools.metacognitive_monitoring.models import (
                ReflectionDepth,
                ThinkingMode,
            )

            request = ProgressiveMetacognitiveRequest(
                session_id=session_id,
                step_number=step_number,
                current_thought=current_thought,
                thinking_context=thinking_context,
                thinking_mode=ThinkingMode(thinking_mode),
                confidence_level=confidence_level,
                clarity_level=clarity_level,
                reflection_depth=ReflectionDepth(reflection_depth),
                metadata=metadata or {},
            )

            response = await self.progressive_metacognitive.monitor_thinking(request)

            return {
                "tool": "Progressive Metacognitive Monitoring",
                "response": response.model_dump(by_alias=True),
                "success": response.status == "success",
            }

        except Exception as e:
            logger.error(f"Progressive metacognitive monitoring failed: {e}")
            return {
                "tool": "Progressive Metacognitive Monitoring",
                "error": str(e),
                "success": False,
            }

    async def handle_progressive_scientific(
        self,
        session_id: str | None = None,
        step_number: int = 1,
        research_phase: str = "observation",
        research_question: str = "",
        domain: str = "",
        observations: list[str] | None = None,
        hypothesis: str | None = None,
        experiment_design: dict[str, Any] | None = None,
        data: list[dict[str, Any]] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Handle progressive scientific method analysis."""
        if not self.progressive_scientific:
            return {
                "tool": "Progressive Scientific Method",
                "error": "Progressive mode not configured. Database stores required.",
                "success": False,
            }

        try:
            from pyclarity.tools.scientific_method.models import ResearchPhase

            request = ProgressiveScientificRequest(
                session_id=session_id,
                step_number=step_number,
                research_phase=ResearchPhase(research_phase),
                research_question=research_question,
                domain=domain,
                observations=observations or [],
                hypothesis=hypothesis,
                experiment_design=experiment_design,
                data=data or [],
                metadata=metadata or {},
            )

            response = await self.progressive_scientific.conduct_research(request)

            return {
                "tool": "Progressive Scientific Method",
                "response": response.model_dump(by_alias=True),
                "success": response.status == "success",
            }

        except Exception as e:
            logger.error(f"Progressive scientific method failed: {e}")
            return {"tool": "Progressive Scientific Method", "error": str(e), "success": False}

    async def handle_progressive_visual(
        self,
        session_id: str | None = None,
        step_number: int = 1,
        visualization_type: str = "conceptual",
        subject: str = "",
        context: str = "",
        visual_elements: list[dict[str, Any]] | None = None,
        relationships: list[dict[str, Any]] | None = None,
        spatial_arrangement: str = "hierarchical",
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Handle progressive visual reasoning."""
        if not self.progressive_visual:
            return {
                "tool": "Progressive Visual Reasoning",
                "error": "Progressive mode not configured. Database stores required.",
                "success": False,
            }

        try:
            from pyclarity.tools.visual_reasoning.models import (
                SpatialArrangement,
                VisualizationType,
            )

            request = ProgressiveVisualRequest(
                session_id=session_id,
                step_number=step_number,
                visualization_type=VisualizationType(visualization_type),
                subject=subject,
                context=context,
                visual_elements=visual_elements or [],
                relationships=relationships or [],
                spatial_arrangement=SpatialArrangement(spatial_arrangement),
                metadata=metadata or {},
            )

            response = await self.progressive_visual.analyze_visually(request)

            return {
                "tool": "Progressive Visual Reasoning",
                "response": response.model_dump(by_alias=True),
                "success": response.status == "success",
            }

        except Exception as e:
            logger.error(f"Progressive visual reasoning failed: {e}")
            return {"tool": "Progressive Visual Reasoning", "error": str(e), "success": False}

    async def handle_progressive_creative(
        self,
        session_id: str | None = None,
        step_number: int = 1,
        challenge: str = "",
        domain: str = "general",
        creative_mode: str = "divergent",
        ideas: list[dict[str, Any]] | None = None,
        constraints: list[dict[str, Any]] | None = None,
        creative_methods: list[str] | None = None,
        seek_novelty: bool = True,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Handle progressive creative thinking."""
        if not self.progressive_creative:
            return {
                "tool": "Progressive Creative Thinking",
                "error": "Progressive mode not configured. Database stores required.",
                "success": False,
            }

        try:
            from pyclarity.tools.creative_thinking.models import CreativeMethod, CreativeMode

            # Convert method strings to enums
            method_enums = []
            if creative_methods:
                for method in creative_methods:
                    try:
                        method_enums.append(CreativeMethod(method))
                    except ValueError:
                        logger.warning(f"Unknown creative method: {method}")

            request = ProgressiveCreativeRequest(
                session_id=session_id,
                step_number=step_number,
                challenge=challenge,
                domain=domain,
                creative_mode=CreativeMode(creative_mode),
                ideas=ideas or [],
                constraints=constraints or [],
                creative_methods=method_enums,
                seek_novelty=seek_novelty,
                metadata=metadata or {},
            )

            response = await self.progressive_creative.generate_ideas(request)

            return {
                "tool": "Progressive Creative Thinking",
                "response": response.model_dump(by_alias=True),
                "success": response.status == "success",
            }

        except Exception as e:
            logger.error(f"Progressive creative thinking failed: {e}")
            return {"tool": "Progressive Creative Thinking", "error": str(e), "success": False}

    async def handle_progressive_systems(
        self,
        session_id: str | None = None,
        step_number: int = 1,
        system_name: str = "",
        system_description: str = "",
        perspective: str = "holistic",
        components: list[dict[str, Any]] | None = None,
        relationships: list[dict[str, Any]] | None = None,
        boundaries: dict[str, Any] | None = None,
        analysis_focus: str = "structure",
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Handle progressive systems thinking."""
        if not self.progressive_systems:
            return {
                "tool": "Progressive Systems Thinking",
                "error": "Progressive mode not configured. Database stores required.",
                "success": False,
            }

        try:
            from pyclarity.tools.systems_thinking.models import AnalysisFocus, SystemPerspective

            request = ProgressiveSystemsRequest(
                session_id=session_id,
                step_number=step_number,
                system_name=system_name,
                system_description=system_description,
                perspective=SystemPerspective(perspective),
                components=components or [],
                relationships=relationships or [],
                boundaries=boundaries,
                analysis_focus=AnalysisFocus(analysis_focus),
                metadata=metadata or {},
            )

            response = await self.progressive_systems.analyze_system(request)

            return {
                "tool": "Progressive Systems Thinking",
                "response": response.model_dump(by_alias=True),
                "success": response.status == "success",
            }

        except Exception as e:
            logger.error(f"Progressive systems thinking failed: {e}")
            return {"tool": "Progressive Systems Thinking", "error": str(e), "success": False}


async def create_progressive_server_v2(db_url: str | None = None) -> FastMCP:
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
                AsyncPGCollaborativeStore,
                AsyncPGCreativeStore,
                AsyncPGDebuggingStore,
                AsyncPGDecisionStore,
                AsyncPGMentalModelStore,
                AsyncPGMetacognitiveStore,
                AsyncPGScientificStore,
                AsyncPGSystemsStore,
                AsyncPGVisualStore,
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

    # Register tools based on progressive mode availability
    if session_store:
        # Progressive mode: Use progressive analyzers as default
        _register_progressive_tools_v2(mcp, tool_handler)
        logger.info("Using progressive analyzers as default tool implementation")
    else:
        # Fallback mode: Use standard tools without session management
        _register_standard_tools(mcp, tool_handler)
        logger.info("Using standard tools (no session management)")

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
    async def mental_models(
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

    # Debugging Approaches Tool
    @mcp.tool()
    async def debugging_approaches(
        issue_description: str,
        error_message: str | None = None,
        debugging_type: str = "systematic",
        context: str | None = None,
        constraints: list[str] | None = None,
    ) -> dict[str, Any]:
        """
        Apply systematic debugging strategies.

        Standard implementation without session management.
        """
        return await handler.handle_debugging_approaches(
            issue_description=issue_description,
            error_message=error_message,
            debugging_type=debugging_type,
            context=context,
            constraints=constraints,
        )

    # Sequential Thinking Tool
    @mcp.tool()
    async def sequential_thinking(
        problem: str,
        context: str | None = None,
        reasoning_depth: int = 5,
        complexity_level: str = "medium",
    ) -> dict[str, Any]:
        """
        Break down complex problems into sequential steps.

        Standard implementation without session management.
        """
        return await handler.handle_sequential_thinking(
            problem=problem,
            context=context,
            reasoning_depth=reasoning_depth,
            complexity_level=complexity_level,
        )

    # Note: Add other standard tool implementations as needed


def _register_progressive_tools_v2(
    mcp: FastMCP, handler: ProgressiveCognitiveToolHandlerV2
) -> None:
    """Register ALL progressive cognitive tools that use session state."""

    # Sequential Thinking (Progressive)
    @mcp.tool()
    async def sequential_thinking(
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
        Sequential thinking analysis with step-by-step reasoning.

        Supports both single-use analysis and progressive multi-step sessions
        with branching, revision, and persistent state tracking.
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

    # Mental Models (Progressive)
    @mcp.tool()
    async def mental_models(
        session_id: str | None = None,
        model_type: str = "first_principles",
        problem_statement: str = "",
        context: str | None = None,
        previous_model_ids: list[int] | None = None,
        build_on_previous: bool = False,
    ) -> dict[str, Any]:
        """
        Analyze problems using structured mental model frameworks.

        Supports single-use analysis or progressive multi-model sessions
        where insights build upon each other with persistent state.
        """
        return await handler.handle_progressive_mental_models(
            session_id=session_id,
            model_type=model_type,
            problem_statement=problem_statement,
            context=context,
            previous_model_ids=previous_model_ids,
            build_on_previous=build_on_previous,
        )

    # Debugging Approaches (Progressive)
    @mcp.tool()
    async def debugging_approaches(
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
        Systematic debugging with hypothesis-driven approach.

        Supports both quick debugging and progressive multi-step investigations
        with evidence tracking and hypothesis validation.
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

    # Collaborative Reasoning (Progressive)
    @mcp.tool()
    async def collaborative_reasoning(
        session_id: str | None = None,
        step_number: int = 1,
        collaboration_type: str = "consensus_building",
        topic: str = "",
        context: str = "",
        personas: list[dict[str, Any]] | None = None,
        contributions: list[dict[str, Any]] | None = None,
        synthesis_approach: str = "integrative",
    ) -> dict[str, Any]:
        """
        Multi-perspective reasoning and consensus building.

        Analyze topics through diverse personas with support for both
        single discussions and progressive collaborative sessions.
        """
        return await handler.handle_progressive_collaborative(
            session_id=session_id,
            step_number=step_number,
            collaboration_type=collaboration_type,
            topic=topic,
            context=context,
            personas=personas,
            contributions=contributions,
            synthesis_approach=synthesis_approach,
        )

    # Decision Framework (Progressive)
    @mcp.tool()
    async def decision_framework(
        session_id: str | None = None,
        step_number: int = 1,
        decision_context: str = "",
        decision_type: str = "strategic",
        criteria: list[dict[str, Any]] | None = None,
        alternatives: list[dict[str, Any]] | None = None,
        evaluation_method: str = "weighted_criteria",
        time_pressure: str = "moderate",
    ) -> dict[str, Any]:
        """
        Structured decision analysis using multiple criteria.

        Evaluate decisions through weighted criteria with support for
        both quick analysis and progressive decision refinement.
        """
        return await handler.handle_progressive_decision(
            session_id=session_id,
            step_number=step_number,
            decision_context=decision_context,
            decision_type=decision_type,
            criteria=criteria,
            alternatives=alternatives,
            evaluation_method=evaluation_method,
            time_pressure=time_pressure,
        )

    # Metacognitive Monitoring (Progressive)
    @mcp.tool()
    async def metacognitive_monitoring(
        session_id: str | None = None,
        step_number: int = 1,
        current_thought: str = "",
        thinking_context: str = "",
        thinking_mode: str = "analytical",
        confidence_level: float = 0.5,
        clarity_level: float = 0.5,
        reflection_depth: str = "moderate",
    ) -> dict[str, Any]:
        """
        Monitor and improve thinking quality and patterns.

        Analyze cognitive processes with support for both single
        assessments and progressive thinking improvement tracking.
        """
        return await handler.handle_progressive_metacognitive(
            session_id=session_id,
            step_number=step_number,
            current_thought=current_thought,
            thinking_context=thinking_context,
            thinking_mode=thinking_mode,
            confidence_level=confidence_level,
            clarity_level=clarity_level,
            reflection_depth=reflection_depth,
        )

    # Scientific Method (Progressive)
    @mcp.tool()
    async def scientific_method(
        session_id: str | None = None,
        step_number: int = 1,
        research_phase: str = "observation",
        research_question: str = "",
        domain: str = "",
        observations: list[str] | None = None,
        hypothesis: str | None = None,
        experiment_design: dict[str, Any] | None = None,
        data: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """
        Apply scientific method for systematic investigation.

        Support research through all phases with both single-use
        analysis and progressive multi-phase research sessions.
        """
        return await handler.handle_progressive_scientific(
            session_id=session_id,
            step_number=step_number,
            research_phase=research_phase,
            research_question=research_question,
            domain=domain,
            observations=observations,
            hypothesis=hypothesis,
            experiment_design=experiment_design,
            data=data,
        )

    # Visual Reasoning (Progressive)
    @mcp.tool()
    async def visual_reasoning(
        session_id: str | None = None,
        step_number: int = 1,
        visualization_type: str = "conceptual",
        subject: str = "",
        context: str = "",
        visual_elements: list[dict[str, Any]] | None = None,
        relationships: list[dict[str, Any]] | None = None,
        spatial_arrangement: str = "hierarchical",
    ) -> dict[str, Any]:
        """
        Visual and spatial reasoning for complex problems.

        Analyze visual structures with support for both single
        visualizations and progressive visual model building.
        """
        return await handler.handle_progressive_visual(
            session_id=session_id,
            step_number=step_number,
            visualization_type=visualization_type,
            subject=subject,
            context=context,
            visual_elements=visual_elements,
            relationships=relationships,
            spatial_arrangement=spatial_arrangement,
        )

    # Creative Thinking (Progressive)
    @mcp.tool()
    async def creative_thinking(
        session_id: str | None = None,
        step_number: int = 1,
        challenge: str = "",
        domain: str = "general",
        creative_mode: str = "divergent",
        ideas: list[dict[str, Any]] | None = None,
        constraints: list[dict[str, Any]] | None = None,
        creative_methods: list[str] | None = None,
        seek_novelty: bool = True,
    ) -> dict[str, Any]:
        """
        Creative ideation and innovative problem solving.

        Generate ideas with support for both brainstorming bursts
        and progressive creative development sessions.
        """
        return await handler.handle_progressive_creative(
            session_id=session_id,
            step_number=step_number,
            challenge=challenge,
            domain=domain,
            creative_mode=creative_mode,
            ideas=ideas,
            constraints=constraints,
            creative_methods=creative_methods,
            seek_novelty=seek_novelty,
        )

    # Systems Thinking (Progressive)
    @mcp.tool()
    async def systems_thinking(
        session_id: str | None = None,
        step_number: int = 1,
        system_name: str = "",
        system_description: str = "",
        perspective: str = "holistic",
        components: list[dict[str, Any]] | None = None,
        relationships: list[dict[str, Any]] | None = None,
        boundaries: dict[str, Any] | None = None,
        analysis_focus: str = "structure",
    ) -> dict[str, Any]:
        """
        Analyze complex systems and their interactions.

        Explore system dynamics with support for both single analysis
        and progressive system modeling across multiple sessions.
        """
        return await handler.handle_progressive_systems(
            session_id=session_id,
            step_number=step_number,
            system_name=system_name,
            system_description=system_description,
            perspective=perspective,
            components=components,
            relationships=relationships,
            boundaries=boundaries,
            analysis_focus=analysis_focus,
        )

    logger.info("Progressive tools registered successfully")


if __name__ == "__main__":
    import asyncio

    async def main():
        # Example usage
        db_url = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/pyclarity")
        server = await create_progressive_server_v2(db_url)
        # Server would be run with FastMCP's run method

    asyncio.run(main())
