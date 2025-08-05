"""
Tool Handlers for PyClarity MCP Server

Bridges between MCP tool calls and PyClarity cognitive analyzers.
Handles parameter validation, context creation, and result formatting.
"""

import logging
from typing import Any, Dict, List, Optional

from pyclarity.tools.collaborative_reasoning import (
    CollaborativeReasoningAnalyzer,
    CollaborativeReasoningContext,
)
from pyclarity.tools.debugging_approaches import (
    DebuggingApproachesAnalyzer,
    DebuggingApproachesContext,
)
from pyclarity.tools.decision_framework import (
    CriteriaType,
    DecisionCriteria,
    DecisionFrameworkAnalyzer,
    DecisionFrameworkContext,
    DecisionOption,
)
from pyclarity.tools.design_patterns import DesignPatternsAnalyzer, DesignPatternsContext
from pyclarity.tools.impact_propagation import (
    ImpactPropagationAnalyzer,
    ImpactPropagationContext,
)

# New FastMCP tools
from pyclarity.tools.iterative_validation import (
    IterativeValidationAnalyzer,
    IterativeValidationContext,
)

# Import working analyzers (skip problematic ones for now)
from pyclarity.tools.mental_models import (
    ComplexityLevel,
    MentalModelContext,
    MentalModelsAnalyzer,
    MentalModelType,
)
from pyclarity.tools.metacognitive_monitoring import (
    MetacognitiveMonitoringAnalyzer,
    MetacognitiveMonitoringContext,
)
from pyclarity.tools.multi_perspective import MultiPerspectiveAnalyzer, MultiPerspectiveContext
from pyclarity.tools.programming_paradigms import (
    ProgrammingParadigmsAnalyzer,
    ProgrammingParadigmsContext,
)
from pyclarity.tools.scientific_method import ScientificMethodAnalyzer, ScientificMethodContext
from pyclarity.tools.sequential_readiness import (
    SequentialReadinessAnalyzer,
    SequentialReadinessContext,
)
from pyclarity.tools.sequential_thinking import (
    BranchStrategy,
    SequentialThinkingAnalyzer,
    SequentialThinkingContext,
)
from pyclarity.tools.structured_argumentation import (
    StructuredArgumentationAnalyzer,
    StructuredArgumentationContext,
)
from pyclarity.tools.triple_constraint import TripleConstraintAnalyzer, TripleConstraintContext
from pyclarity.tools.visual_reasoning import (
    VisualElement,
    VisualReasoningAnalyzer,
    VisualReasoningContext,
    VisualRepresentationType,
)

logger = logging.getLogger(__name__)


class CognitiveToolHandler:
    """Handles MCP tool calls for cognitive analyzers."""

    def __init__(self):
        """Initialize all cognitive analyzers."""
        self.analyzers = {
            'mental_models': MentalModelsAnalyzer(),
            'sequential_thinking': SequentialThinkingAnalyzer(),
            'decision_framework': DecisionFrameworkAnalyzer(),
            'scientific_method': ScientificMethodAnalyzer(),
            'design_patterns': DesignPatternsAnalyzer(),
            'programming_paradigms': ProgrammingParadigmsAnalyzer(),
            'debugging_approaches': DebuggingApproachesAnalyzer(),
            'visual_reasoning': VisualReasoningAnalyzer(),
            'structured_argumentation': StructuredArgumentationAnalyzer(),
            'metacognitive_monitoring': MetacognitiveMonitoringAnalyzer(),
            'collaborative_reasoning': CollaborativeReasoningAnalyzer(),
            # Temporarily disabled
            # 'impact_propagation': ImpactPropagationAnalyzer(),
            # New FastMCP tools
            'iterative_validation': IterativeValidationAnalyzer(),
            'multi_perspective': MultiPerspectiveAnalyzer(),
            'sequential_readiness': SequentialReadinessAnalyzer(),
            'triple_constraint': TripleConstraintAnalyzer(),
        }

        logger.info(f"Initialized {len(self.analyzers)} cognitive analyzers")

    async def handle_mental_models(
        self,
        problem: str,
        model_type: str = "first_principles",
        complexity_level: str = "moderate",
        focus_areas: list[str] | None = None,
        constraints: list[str] | None = None,
        domain_expertise: str | None = None
    ) -> dict[str, Any]:
        """Handle mental models analysis."""
        try:
            # Convert string to enum
            model_type_enum = MentalModelType(model_type)
            complexity_enum = ComplexityLevel(complexity_level)

            # Create context
            context = MentalModelContext(
                problem=problem,
                model_type=model_type_enum,
                complexity_level=complexity_enum,
                focus_areas=focus_areas,
                constraints=constraints,
                domain_expertise=domain_expertise
            )

            # Run analysis
            analyzer = self.analyzers['mental_models']
            result = await analyzer.analyze(context)

            # Convert to dict for MCP response
            return {
                "tool": "Mental Models",
                "model_type": model_type,
                "complexity_level": complexity_level,
                "analysis": result.model_dump(),
                "success": True
            }

        except Exception as e:
            logger.error(f"Mental models analysis failed: {e}")
            return {
                "tool": "Mental Models",
                "error": str(e),
                "success": False
            }

    async def handle_sequential_thinking(
        self,
        problem: str,
        complexity_level: str = "moderate",
        reasoning_depth: int = 5,
        enable_branching: bool = True,
        enable_revision: bool = True,
        branch_strategy: str = "adaptive"
    ) -> dict[str, Any]:
        """Handle sequential thinking analysis."""
        try:
            # Convert enums
            complexity_enum = ComplexityLevel(complexity_level)
            strategy_enum = BranchStrategy(branch_strategy)

            # Create context
            context = SequentialThinkingContext(
                problem=problem,
                complexity_level=complexity_enum,
                reasoning_depth=reasoning_depth,
                enable_branching=enable_branching,
                enable_revision=enable_revision,
                branch_strategy=strategy_enum
            )

            # Run analysis
            analyzer = self.analyzers['sequential_thinking']
            result = await analyzer.analyze(context)

            return {
                "tool": "Sequential Thinking",
                "reasoning_depth": reasoning_depth,
                "enable_branching": enable_branching,
                "analysis": result.model_dump(),
                "success": True
            }

        except Exception as e:
            logger.error(f"Sequential thinking analysis failed: {e}")
            return {
                "tool": "Sequential Thinking",
                "error": str(e),
                "success": False
            }

    async def handle_decision_framework(
        self,
        decision_problem: str,
        complexity_level: str = "moderate",
        criteria: list[dict] | None = None,
        options: list[dict] | None = None,
        decision_methods: list[str] | None = None,
        stakeholder_weights: dict[str, float] | None = None,
        time_constraints: str | None = None
    ) -> dict[str, Any]:
        """Handle decision framework analysis."""
        try:
            complexity_enum = ComplexityLevel(complexity_level)

            # Convert criteria and options if provided
            criteria_objs = []
            if criteria:
                for c in criteria:
                    criteria_objs.append(DecisionCriteria(
                        name=c.get('name', ''),
                        description=c.get('description', ''),
                        weight=c.get('weight', 1.0),
                        criteria_type=CriteriaType(c.get('type', 'benefit')),
                        measurement_unit=c.get('unit', 'score')
                    ))

            options_objs = []
            if options:
                for o in options:
                    options_objs.append(DecisionOption(
                        name=o.get('name', ''),
                        description=o.get('description', ''),
                        scores=o.get('scores', {})
                    ))

            # Create context
            context = DecisionFrameworkContext(
                decision_problem=decision_problem,
                complexity_level=complexity_enum,
                criteria=criteria_objs,
                options=options_objs,
                decision_methods=decision_methods or ["WEIGHTED_SUM"],
                stakeholder_weights=stakeholder_weights,
                time_constraints=time_constraints
            )

            # Run analysis
            analyzer = self.analyzers['decision_framework']
            result = await analyzer.analyze(context)

            return {
                "tool": "Decision Framework",
                "decision_problem": decision_problem,
                "methods_used": decision_methods,
                "analysis": result.model_dump(),
                "success": True
            }

        except Exception as e:
            logger.error(f"Decision framework analysis failed: {e}")
            return {
                "tool": "Decision Framework",
                "error": str(e),
                "success": False
            }

    async def handle_scientific_method(
        self,
        problem: str,
        complexity_level: str = "moderate",
        research_question: str | None = None,
        domain_knowledge: str | None = None,
        max_hypotheses: int = 3,
        evidence_sources: list[str] | None = None,
        significance_threshold: float = 0.05
    ) -> dict[str, Any]:
        """Handle scientific method analysis."""
        try:
            complexity_enum = ComplexityLevel(complexity_level)

            context = ScientificMethodContext(
                problem=problem,
                complexity_level=complexity_enum,
                research_question=research_question,
                domain_knowledge=domain_knowledge,
                max_hypotheses=max_hypotheses,
                evidence_sources=evidence_sources,
                significance_threshold=significance_threshold
            )

            analyzer = self.analyzers['scientific_method']
            result = await analyzer.analyze(context)

            return {
                "tool": "Scientific Method",
                "research_question": research_question,
                "max_hypotheses": max_hypotheses,
                "analysis": result.model_dump(),
                "success": True
            }

        except Exception as e:
            logger.error(f"Scientific method analysis failed: {e}")
            return {
                "tool": "Scientific Method",
                "error": str(e),
                "success": False
            }

    async def handle_design_patterns(
        self,
        problem: str,
        complexity_level: str = "moderate",
        problem_domain: str | None = None,
        system_scale: str | None = None,
        constraints: list[str] | None = None
    ) -> dict[str, Any]:
        """Handle design patterns analysis."""
        try:
            complexity_enum = ComplexityLevel(complexity_level)

            context = DesignPatternsContext(
                problem=problem,
                complexity_level=complexity_enum,
                problem_domain=problem_domain,
                system_scale=system_scale,
                constraints=constraints
            )

            analyzer = self.analyzers['design_patterns']
            result = await analyzer.analyze(context)

            return {
                "tool": "Design Patterns",
                "problem_domain": problem_domain,
                "system_scale": system_scale,
                "analysis": result.model_dump(),
                "success": True
            }

        except Exception as e:
            logger.error(f"Design patterns analysis failed: {e}")
            return {
                "tool": "Design Patterns",
                "error": str(e),
                "success": False
            }

    # Add handlers for remaining tools with similar pattern...

    async def handle_programming_paradigms(self, **kwargs) -> dict[str, Any]:
        """Handle programming paradigms analysis."""
        try:
            complexity_enum = ComplexityLevel(kwargs.get('complexity_level', 'moderate'))

            context = ProgrammingParadigmsContext(
                problem=kwargs['problem'],
                complexity_level=complexity_enum,
                current_paradigms=kwargs.get('current_paradigms'),
                target_paradigms=kwargs.get('target_paradigms'),
                project_constraints=kwargs.get('project_constraints')
            )

            analyzer = self.analyzers['programming_paradigms']
            result = await analyzer.analyze(context)

            return {
                "tool": "Programming Paradigms",
                "analysis": result.model_dump(),
                "success": True
            }
        except Exception as e:
            logger.error(f"Programming paradigms analysis failed: {e}")
            return {"tool": "Programming Paradigms", "error": str(e), "success": False}

    async def handle_debugging_approaches(self, **kwargs) -> dict[str, Any]:
        """Handle debugging approaches analysis."""
        try:
            complexity_enum = ComplexityLevel(kwargs.get('complexity_level', 'moderate'))

            context = DebuggingApproachesContext(
                problem=kwargs['problem'],
                complexity_level=complexity_enum,
                problem_domain=kwargs.get('problem_domain'),
                error_symptoms=kwargs.get('error_symptoms'),
                system_complexity=kwargs.get('system_complexity'),
                available_tools=kwargs.get('available_tools'),
                time_constraints=kwargs.get('time_constraints')
            )

            analyzer = self.analyzers['debugging_approaches']
            result = await analyzer.analyze(context)

            return {
                "tool": "Debugging Approaches",
                "analysis": result.model_dump(),
                "success": True
            }
        except Exception as e:
            logger.error(f"Debugging approaches analysis failed: {e}")
            return {"tool": "Debugging Approaches", "error": str(e), "success": False}

    async def handle_visual_reasoning(self, **kwargs) -> dict[str, Any]:
        """Handle visual reasoning analysis."""
        try:
            # Convert visual elements if provided
            visual_elements = []
            if kwargs.get('visual_elements'):
                for elem in kwargs['visual_elements']:
                    visual_elements.append(VisualElement(
                        element_id=elem.get('id', ''),
                        element_type=elem.get('type', ''),
                        position=tuple(elem.get('position', (0, 0))),
                        size=tuple(elem.get('size', (1, 1))),
                        properties=elem.get('properties', {})
                    ))

            context = VisualReasoningContext(
                problem=kwargs['problem'],
                visual_elements=visual_elements,
                representation_type=VisualRepresentationType(kwargs.get('representation_type', 'diagram')),
                analysis_focus=kwargs.get('analysis_focus')
            )

            analyzer = self.analyzers['visual_reasoning']
            result = await analyzer.analyze(context)

            return {
                "tool": "Visual Reasoning",
                "analysis": result.model_dump(),
                "success": True
            }
        except Exception as e:
            logger.error(f"Visual reasoning analysis failed: {e}")
            return {"tool": "Visual Reasoning", "error": str(e), "success": False}

    async def handle_structured_argumentation(self, **kwargs) -> dict[str, Any]:
        """Handle structured argumentation analysis."""
        try:
            complexity_enum = ComplexityLevel(kwargs.get('complexity_level', 'moderate'))

            context = StructuredArgumentationContext(
                problem=kwargs['problem'],
                complexity_level=complexity_enum,
                main_claim=kwargs.get('main_claim'),
                premises=kwargs.get('premises'),
                evidence_sources=kwargs.get('evidence_sources'),
                counter_arguments=kwargs.get('counter_arguments')
            )

            analyzer = self.analyzers['structured_argumentation']
            result = await analyzer.analyze(context)

            return {
                "tool": "Structured Argumentation",
                "analysis": result.model_dump(),
                "success": True
            }
        except Exception as e:
            logger.error(f"Structured argumentation analysis failed: {e}")
            return {"tool": "Structured Argumentation", "error": str(e), "success": False}

    async def handle_metacognitive_monitoring(self, **kwargs) -> dict[str, Any]:
        """Handle metacognitive monitoring analysis."""
        try:
            complexity_enum = ComplexityLevel(kwargs.get('complexity_level', 'moderate'))

            context = MetacognitiveMonitoringContext(
                problem=kwargs['problem'],
                complexity_level=complexity_enum,
                reasoning_target=kwargs.get('reasoning_target'),
                monitoring_focus=kwargs.get('monitoring_focus'),
                monitoring_depth=kwargs.get('monitoring_depth', 'standard'),
                intervention_threshold=kwargs.get('intervention_threshold', 0.7)
            )

            analyzer = self.analyzers['metacognitive_monitoring']
            result = await analyzer.analyze(context)

            return {
                "tool": "Metacognitive Monitoring",
                "analysis": result.model_dump(),
                "success": True
            }
        except Exception as e:
            logger.error(f"Metacognitive monitoring analysis failed: {e}")
            return {"tool": "Metacognitive Monitoring", "error": str(e), "success": False}

    async def handle_collaborative_reasoning(self, **kwargs) -> dict[str, Any]:
        """Handle collaborative reasoning analysis."""
        try:
            complexity_enum = ComplexityLevel(kwargs.get('complexity_level', 'moderate'))

            context = CollaborativeReasoningContext(
                problem=kwargs['problem'],
                complexity_level=complexity_enum,
                collaboration_objective=kwargs.get('collaboration_objective'),
                perspectives_needed=kwargs.get('perspectives_needed'),
                max_rounds=kwargs.get('max_rounds', 3),
                consensus_threshold=kwargs.get('consensus_threshold', 0.7)
            )

            analyzer = self.analyzers['collaborative_reasoning']
            result = await analyzer.analyze(context)

            return {
                "tool": "Collaborative Reasoning",
                "analysis": result.model_dump(),
                "success": True
            }
        except Exception as e:
            logger.error(f"Collaborative reasoning analysis failed: {e}")
            return {"tool": "Collaborative Reasoning", "error": str(e), "success": False}

    async def handle_impact_propagation(self, **kwargs) -> dict[str, Any]:
        """Handle impact propagation analysis."""
        try:
            complexity_enum = ComplexityLevel(kwargs.get('complexity_level', 'moderate'))

            context = ImpactPropagationContext(
                scenario=kwargs['scenario'],
                complexity_level=complexity_enum,
                domain_context=kwargs.get('domain_context', 'general'),
                analysis_depth=kwargs.get('analysis_depth', 3),
                time_horizon=kwargs.get('time_horizon'),
                risk_tolerance=kwargs.get('risk_tolerance', 'medium')
            )

            analyzer = self.analyzers['impact_propagation']
            result = await analyzer.analyze(context)

            return {
                "tool": "Impact Propagation",
                "analysis": result.model_dump(),
                "success": True
            }
        except Exception as e:
            logger.error(f"Impact propagation analysis failed: {e}")
            return {"tool": "Impact Propagation", "error": str(e), "success": False}

    async def handle_iterative_validation(self, **kwargs) -> dict[str, Any]:
        """Handle iterative validation analysis."""
        try:
            complexity_enum = ComplexityLevel(kwargs.get('complexity_level', 'moderate'))

            context = IterativeValidationContext(
                scenario=kwargs['scenario'],
                complexity_level=complexity_enum,
                initial_hypothesis=kwargs.get('initial_hypothesis'),
                test_preferences=kwargs.get('test_preferences'),
                max_iterations=kwargs.get('max_iterations', 5),
                target_confidence=kwargs.get('target_confidence'),
                previous_cycles=kwargs.get('previous_cycles')
            )

            analyzer = self.analyzers['iterative_validation']
            result = await analyzer.analyze(context)

            return {
                "tool": "Iterative Validation",
                "analysis": result.model_dump(),
                "success": True
            }
        except Exception as e:
            logger.error(f"Iterative validation analysis failed: {e}")
            return {"tool": "Iterative Validation", "error": str(e), "success": False}

    async def handle_multi_perspective(self, **kwargs) -> dict[str, Any]:
        """Handle multi-perspective analysis."""
        try:
            context = MultiPerspectiveContext(
                scenario=kwargs['scenario'],
                domain_context=kwargs.get('domain_context'),
                predefined_perspectives=kwargs.get('predefined_perspectives'),
                focus_areas=kwargs.get('focus_areas'),
                known_constraints=kwargs.get('known_constraints'),
                desired_outcome=kwargs.get('desired_outcome'),
                time_horizon=kwargs.get('time_horizon'),
                cultural_context=kwargs.get('cultural_context')
            )

            analyzer = self.analyzers['multi_perspective']
            result = await analyzer.analyze(context)

            return {
                "tool": "Multi-Perspective Analysis",
                "analysis": result.model_dump(),
                "success": True
            }
        except Exception as e:
            logger.error(f"Multi-perspective analysis failed: {e}")
            return {"tool": "Multi-Perspective Analysis", "error": str(e), "success": False}

    async def handle_sequential_readiness(self, **kwargs) -> dict[str, Any]:
        """Handle sequential readiness assessment."""
        try:
            complexity_enum = ComplexityLevel(kwargs.get('complexity_level', 'moderate'))

            context = SequentialReadinessContext(
                scenario=kwargs['scenario'],
                complexity_level=complexity_enum,
                domain_context=kwargs.get('domain_context'),
                predefined_states=kwargs.get('predefined_states'),
                assessment_criteria=kwargs.get('assessment_criteria'),
                key_constraints=kwargs.get('key_constraints'),
                timeline_flexibility=kwargs.get('timeline_flexibility', 'medium'),
                risk_tolerance=kwargs.get('risk_tolerance', 'medium'),
                organizational_readiness=kwargs.get('organizational_readiness', 'medium')
            )

            analyzer = self.analyzers['sequential_readiness']
            result = await analyzer.analyze(context)

            return {
                "tool": "Sequential Readiness",
                "analysis": result.model_dump(),
                "success": True
            }
        except Exception as e:
            logger.error(f"Sequential readiness analysis failed: {e}")
            return {"tool": "Sequential Readiness", "error": str(e), "success": False}

    async def handle_triple_constraint(self, **kwargs) -> dict[str, Any]:
        """Handle triple constraint optimization."""
        try:
            complexity_enum = ComplexityLevel(kwargs.get('complexity_level', 'moderate'))

            context = TripleConstraintContext(
                scenario=kwargs['scenario'],
                complexity_level=complexity_enum,
                domain=kwargs.get('domain'),
                predefined_constraints=kwargs.get('predefined_constraints'),
                optimization_focus=kwargs.get('optimization_focus'),
                flexibility_parameters=kwargs.get('flexibility_parameters'),
                risk_tolerance=kwargs.get('risk_tolerance', 'medium'),
                timeline_flexibility=kwargs.get('timeline_flexibility', 'medium'),
                primary_stakeholders=kwargs.get('primary_stakeholders'),
                organizational_readiness=kwargs.get('organizational_readiness', 'medium')
            )

            analyzer = self.analyzers['triple_constraint']
            result = await analyzer.analyze(context)

            return {
                "tool": "Triple Constraint Optimizer",
                "analysis": result.model_dump(),
                "success": True
            }
        except Exception as e:
            logger.error(f"Triple constraint analysis failed: {e}")
            return {"tool": "Triple Constraint Optimizer", "error": str(e), "success": False}
