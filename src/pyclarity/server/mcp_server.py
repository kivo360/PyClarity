"""
PyClarity MCP Server

FastMCP-based server providing cognitive tools for strategic thinking and decision-making.
Integrates with Claude Desktop and other MCP clients to provide analysis capabilities.
"""

import asyncio
import logging
from typing import Any, Dict, Optional

from fastmcp import FastMCP

from .tool_handlers import CognitiveToolHandler

logger = logging.getLogger(__name__)


def create_server() -> FastMCP:
    """
    Create and configure the PyClarity MCP server.

    Returns:
        FastMCP: Configured server instance
    """
    # Initialize the FastMCP server
    mcp = FastMCP("PyClarity")

    # Initialize the cognitive tool handler
    tool_handler = CognitiveToolHandler()

    # Register all cognitive tools
    _register_cognitive_tools(mcp, tool_handler)

    # Add server info
    logger.info("Registering PyClarity cognitive tools...")
    logger.info("Available tools:")

    tools = [
        "Mental Models Analysis",
        "Sequential Thinking",
        "Decision Framework",
        "Scientific Method",
        "Design Patterns",
        "Programming Paradigms",
        "Debugging Approaches",
        "Visual Reasoning",
        "Structured Argumentation",
        "Metacognitive Monitoring",
        "Collaborative Reasoning",
        "Impact Propagation (disabled)",
        "Iterative Validation",
        "Multi-Perspective Analysis",
        "Sequential Readiness Assessment",
        "Triple Constraint Optimization"
    ]

    for tool in tools:
        logger.info(f"  • {tool}")

    return mcp


def _register_cognitive_tools(mcp: FastMCP, handler: CognitiveToolHandler) -> None:
    """Register all cognitive tools with the MCP server."""

    # Mental Models Tool
    @mcp.tool()
    async def mental_models_analysis(
        problem: str,
        model_type: str = "first_principles",
        complexity_level: str = "moderate",
        focus_areas: list[str] | None = None,
        constraints: list[str] | None = None,
        domain_expertise: str | None = None
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

        Args:
            problem: The problem or question to analyze
            model_type: Mental model framework to apply
            complexity_level: Analysis depth (simple, moderate, complex)
            focus_areas: Specific areas to focus analysis on
            constraints: Known limitations or constraints
            domain_expertise: Relevant domain expertise level

        Returns:
            Analysis results with insights and recommendations
        """
        return await handler.handle_mental_models(
            problem=problem,
            model_type=model_type,
            complexity_level=complexity_level,
            focus_areas=focus_areas,
            constraints=constraints,
            domain_expertise=domain_expertise
        )

    # Sequential Thinking Tool
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

        Provides step-by-step logical reasoning with the ability to explore
        alternative paths and revise conclusions based on new insights.

        Args:
            problem: The problem to analyze step by step
            complexity_level: Analysis complexity (simple, moderate, complex)
            reasoning_depth: Number of reasoning steps to perform
            enable_branching: Allow exploration of alternative reasoning paths
            enable_revision: Enable revision of earlier steps based on new insights
            branch_strategy: How to handle branching (linear, adaptive, exhaustive)

        Returns:
            Sequential analysis with reasoning steps and conclusions
        """
        return await handler.handle_sequential_thinking(
            problem=problem,
            complexity_level=complexity_level,
            reasoning_depth=reasoning_depth,
            enable_branching=enable_branching,
            enable_revision=enable_revision,
            branch_strategy=branch_strategy
        )

    # Decision Framework Tool
    @mcp.tool()
    async def decision_framework(
        decision_problem: str,
        complexity_level: str = "moderate",
        criteria: list[dict] | None = None,
        options: list[dict] | None = None,
        decision_methods: list[str] | None = None,
        stakeholder_weights: dict[str, float] | None = None,
        time_constraints: str | None = None
    ) -> dict[str, Any]:
        """
        Systematic decision-making using multi-criteria analysis.

        Supports various decision methods including weighted scoring,
        AHP (Analytical Hierarchy Process), and consensus building.

        Args:
            decision_problem: The decision to be made
            complexity_level: Analysis complexity (simple, moderate, complex)
            criteria: Decision criteria with weights and types
            options: Available decision options with scores
            decision_methods: Methods to use (weighted_sum, ahp, consensus)
            stakeholder_weights: Importance weighting by stakeholder group
            time_constraints: Timeline or urgency considerations

        Returns:
            Decision analysis with recommendations and rationale
        """
        return await handler.handle_decision_framework(
            decision_problem=decision_problem,
            complexity_level=complexity_level,
            criteria=criteria,
            options=options,
            decision_methods=decision_methods,
            stakeholder_weights=stakeholder_weights,
            time_constraints=time_constraints
        )

    # Scientific Method Tool
    @mcp.tool()
    async def scientific_method(
        problem: str,
        complexity_level: str = "moderate",
        research_question: str | None = None,
        domain_knowledge: str | None = None,
        max_hypotheses: int = 3,
        evidence_sources: list[str] | None = None,
        significance_threshold: float = 0.05
    ) -> dict[str, Any]:
        """
        Apply scientific method for hypothesis-driven problem solving.

        Structures analysis around hypothesis formation, evidence gathering,
        experimentation design, and statistical validation.

        Args:
            problem: The problem to investigate scientifically
            complexity_level: Analysis complexity (simple, moderate, complex)
            research_question: Specific research question to investigate
            domain_knowledge: Existing knowledge and context
            max_hypotheses: Maximum number of hypotheses to generate
            evidence_sources: Available sources of evidence
            significance_threshold: Statistical significance threshold

        Returns:
            Scientific analysis with hypotheses, evidence, and conclusions
        """
        return await handler.handle_scientific_method(
            problem=problem,
            complexity_level=complexity_level,
            research_question=research_question,
            domain_knowledge=domain_knowledge,
            max_hypotheses=max_hypotheses,
            evidence_sources=evidence_sources,
            significance_threshold=significance_threshold
        )

    # Add remaining tools with similar pattern...
    # (Continuing with abbreviated versions for brevity)

    @mcp.tool()
    async def design_patterns(
        problem: str,
        complexity_level: str = "moderate",
        problem_domain: str | None = None,
        system_scale: str | None = None,
        constraints: list[str] | None = None
    ) -> dict[str, Any]:
        """Apply design pattern analysis for architectural solutions."""
        return await handler.handle_design_patterns(
            problem=problem,
            complexity_level=complexity_level,
            problem_domain=problem_domain,
            system_scale=system_scale,
            constraints=constraints
        )

    @mcp.tool()
    async def programming_paradigms(
        problem: str,
        complexity_level: str = "moderate",
        current_paradigms: list[str] | None = None,
        target_paradigms: list[str] | None = None,
        project_constraints: list[str] | None = None
    ) -> dict[str, Any]:
        """Analyze programming paradigm selection and application."""
        return await handler.handle_programming_paradigms(
            problem=problem,
            complexity_level=complexity_level,
            current_paradigms=current_paradigms,
            target_paradigms=target_paradigms,
            project_constraints=project_constraints
        )

    @mcp.tool()
    async def debugging_approaches(
        problem: str,
        complexity_level: str = "moderate",
        problem_domain: str | None = None,
        error_symptoms: list[str] | None = None,
        system_complexity: str | None = None,
        available_tools: list[str] | None = None,
        time_constraints: str | None = None
    ) -> dict[str, Any]:
        """Systematic debugging methodology and approach selection."""
        return await handler.handle_debugging_approaches(
            problem=problem,
            complexity_level=complexity_level,
            problem_domain=problem_domain,
            error_symptoms=error_symptoms,
            system_complexity=system_complexity,
            available_tools=available_tools,
            time_constraints=time_constraints
        )

    @mcp.tool()
    async def visual_reasoning(
        problem: str,
        visual_elements: list[dict] | None = None,
        representation_type: str = "diagram",
        analysis_focus: list[str] | None = None
    ) -> dict[str, Any]:
        """Visual problem representation and spatial reasoning analysis."""
        return await handler.handle_visual_reasoning(
            problem=problem,
            visual_elements=visual_elements,
            representation_type=representation_type,
            analysis_focus=analysis_focus
        )

    @mcp.tool()
    async def structured_argumentation(
        problem: str,
        complexity_level: str = "moderate",
        main_claim: str | None = None,
        premises: list[str] | None = None,
        evidence_sources: list[str] | None = None,
        counter_arguments: list[str] | None = None
    ) -> dict[str, Any]:
        """Logical argumentation structure and fallacy analysis."""
        return await handler.handle_structured_argumentation(
            problem=problem,
            complexity_level=complexity_level,
            main_claim=main_claim,
            premises=premises,
            evidence_sources=evidence_sources,
            counter_arguments=counter_arguments
        )

    @mcp.tool()
    async def metacognitive_monitoring(
        problem: str,
        complexity_level: str = "moderate",
        reasoning_target: str | None = None,
        monitoring_focus: list[str] | None = None,
        monitoring_depth: str = "standard",
        intervention_threshold: float = 0.7
    ) -> dict[str, Any]:
        """Self-awareness and reasoning quality monitoring."""
        return await handler.handle_metacognitive_monitoring(
            problem=problem,
            complexity_level=complexity_level,
            reasoning_target=reasoning_target,
            monitoring_focus=monitoring_focus,
            monitoring_depth=monitoring_depth,
            intervention_threshold=intervention_threshold
        )

    @mcp.tool()
    async def collaborative_reasoning(
        problem: str,
        complexity_level: str = "moderate",
        collaboration_objective: str | None = None,
        perspectives_needed: list[str] | None = None,
        max_rounds: int = 3,
        consensus_threshold: float = 0.7
    ) -> dict[str, Any]:
        """Multi-perspective collaborative problem-solving."""
        return await handler.handle_collaborative_reasoning(
            problem=problem,
            complexity_level=complexity_level,
            collaboration_objective=collaboration_objective,
            perspectives_needed=perspectives_needed,
            max_rounds=max_rounds,
            consensus_threshold=consensus_threshold
        )

    # Temporarily disabled due to dependency issues
    # @mcp.tool()
    # async def impact_propagation(
    #     scenario: str,
    #     complexity_level: str = "moderate",
    #     domain_context: str = "general",
    #     analysis_depth: int = 3,
    #     time_horizon: Optional[str] = None,
    #     risk_tolerance: str = "medium"
    # ) -> Dict[str, Any]:
    #     """Analyze cascading effects and system-wide impacts."""
    #     return await handler.handle_impact_propagation(
    #         scenario=scenario,
    #         complexity_level=complexity_level,
    #         domain_context=domain_context,
    #         analysis_depth=analysis_depth,
    #         time_horizon=time_horizon,
    #         risk_tolerance=risk_tolerance
    #     )

    # New FastMCP tools
    @mcp.tool()
    async def iterative_validation(
        scenario: str,
        complexity_level: str = "moderate",
        initial_hypothesis: str | None = None,
        test_preferences: list[str] | None = None,
        max_iterations: int = 5,
        target_confidence: float | None = None,
        previous_cycles: list[dict] | None = None
    ) -> dict[str, Any]:
        """
        Hypothesis-test-learn-refine cycles for continuous improvement.

        Implements iterative validation methodology with structured testing,
        learning extraction, and hypothesis refinement across multiple cycles.

        Args:
            scenario: The situation or problem to validate iteratively
            complexity_level: Analysis depth (simple, moderate, complex)
            initial_hypothesis: Starting hypothesis to test and refine
            test_preferences: Preferred testing approaches or constraints
            max_iterations: Maximum validation cycles to perform
            target_confidence: Desired confidence level to achieve
            previous_cycles: History of previous validation attempts

        Returns:
            Validation analysis with cycles, learnings, and refinements
        """
        return await handler.handle_iterative_validation(
            scenario=scenario,
            complexity_level=complexity_level,
            initial_hypothesis=initial_hypothesis,
            test_preferences=test_preferences,
            max_iterations=max_iterations,
            target_confidence=target_confidence,
            previous_cycles=previous_cycles
        )

    @mcp.tool()
    async def multi_perspective_analysis(
        scenario: str,
        domain_context: str | None = None,
        predefined_perspectives: list[dict] | None = None,
        focus_areas: list[str] | None = None,
        known_constraints: list[str] | None = None,
        desired_outcome: str | None = None,
        time_horizon: str | None = None,
        cultural_context: str | None = None
    ) -> dict[str, Any]:
        """
        Analyze from multiple stakeholder viewpoints to find integration paths.

        Identifies different perspectives, analyzes viewpoints, detects
        synergies and conflicts, and creates comprehensive integration strategies.

        Args:
            scenario: The situation to analyze from multiple perspectives
            domain_context: Business, technical, social, or other domain context
            predefined_perspectives: Known stakeholder perspectives to include
            focus_areas: Specific areas to focus the analysis on
            known_constraints: Constraints that affect all perspectives
            desired_outcome: The ideal outcome being sought
            time_horizon: Timeframe for implementation or impact
            cultural_context: Cultural factors affecting perspectives

        Returns:
            Multi-perspective analysis with viewpoints and integration strategies
        """
        return await handler.handle_multi_perspective(
            scenario=scenario,
            domain_context=domain_context,
            predefined_perspectives=predefined_perspectives,
            focus_areas=focus_areas,
            known_constraints=known_constraints,
            desired_outcome=desired_outcome,
            time_horizon=time_horizon,
            cultural_context=cultural_context
        )

    @mcp.tool()
    async def sequential_readiness_assessment(
        scenario: str,
        complexity_level: str = "moderate",
        domain_context: str | None = None,
        predefined_states: list[dict] | None = None,
        assessment_criteria: list[str] | None = None,
        key_constraints: list[str] | None = None,
        timeline_flexibility: str = "medium",
        risk_tolerance: str = "medium",
        organizational_readiness: str = "medium"
    ) -> dict[str, Any]:
        """
        Assess readiness progression through sequential states or phases.

        Evaluates current state, identifies required transitions, detects gaps,
        and recommends interventions for successful progression.

        Args:
            scenario: The transition or change to assess readiness for
            complexity_level: Analysis complexity (simple, moderate, complex)
            domain_context: Specific domain or industry context
            predefined_states: Known states or phases in the sequence
            assessment_criteria: Criteria for evaluating readiness
            key_constraints: Major constraints affecting progression
            timeline_flexibility: Flexibility in transition timing (low, medium, high)
            risk_tolerance: Acceptable risk level (low, medium, high)
            organizational_readiness: Overall organizational maturity level

        Returns:
            Readiness assessment with states, gaps, and intervention recommendations
        """
        return await handler.handle_sequential_readiness(
            scenario=scenario,
            complexity_level=complexity_level,
            domain_context=domain_context,
            predefined_states=predefined_states,
            assessment_criteria=assessment_criteria,
            key_constraints=key_constraints,
            timeline_flexibility=timeline_flexibility,
            risk_tolerance=risk_tolerance,
            organizational_readiness=organizational_readiness
        )

    @mcp.tool()
    async def triple_constraint_optimization(
        scenario: str,
        complexity_level: str = "moderate",
        domain: str | None = None,
        predefined_constraints: list[dict] | None = None,
        optimization_focus: str | None = None,
        flexibility_parameters: dict[str, float] | None = None,
        risk_tolerance: str = "medium",
        timeline_flexibility: str = "medium",
        primary_stakeholders: list[str] | None = None,
        organizational_readiness: str = "medium"
    ) -> dict[str, Any]:
        """
        Optimize trade-offs between competing constraints (scope/time/cost).

        Analyzes constraint relationships, evaluates trade-offs, generates
        optimization scenarios, and recommends balanced solutions.

        Args:
            scenario: The situation requiring constraint optimization
            complexity_level: Analysis depth (simple, moderate, complex)
            domain: Project, product, business, or other domain
            predefined_constraints: Known constraints and their current values
            optimization_focus: Primary optimization goal or priority
            flexibility_parameters: How flexible each constraint dimension is
            risk_tolerance: Acceptable risk level (low, medium, high)
            timeline_flexibility: Schedule flexibility (low, medium, high)
            primary_stakeholders: Key stakeholders affected by trade-offs
            organizational_readiness: Organizational capacity for change

        Returns:
            Optimization analysis with scenarios and balanced recommendations
        """
        return await handler.handle_triple_constraint(
            scenario=scenario,
            complexity_level=complexity_level,
            domain=domain,
            predefined_constraints=predefined_constraints,
            optimization_focus=optimization_focus,
            flexibility_parameters=flexibility_parameters,
            risk_tolerance=risk_tolerance,
            timeline_flexibility=timeline_flexibility,
            primary_stakeholders=primary_stakeholders,
            organizational_readiness=organizational_readiness
        )


async def start_server(
    host: str = "localhost",
    port: int = 8000,
    debug: bool = False
) -> None:
    """
    Start the PyClarity MCP server.

    Args:
        host: Host to bind to
        port: Port to listen on
        debug: Enable debug logging
    """
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    # Create the server
    mcp = create_server()

    # Start the server
    logger.info(f"Starting PyClarity MCP server on {host}:{port}")
    await mcp.run(host=host, port=port)
