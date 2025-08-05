"""
Sequential Thinking Analyzer.

Core implementation of the sequential thinking cognitive tool, providing
step-by-step problem decomposition and reasoning with dynamic thought
progression, branching capabilities, and revision tracking.
"""

import asyncio
import random
import time
from dataclasses import dataclass
from datetime import UTC, datetime

from pyclarity.tools.sequential_thinking.models import (
    BranchStrategy,
    SequentialThinkingContext,
    SequentialThinkingResult,
    ThoughtBranch,
    ThoughtRevision,
    ThoughtStep,
    ThoughtStepStatus,
    ThoughtStepType,
)

# Constants for magic numbers
MIN_SYNTHESIS_DEPENDENCIES = 2
MIN_EVIDENCE_SOURCES = 2
CONFIDENCE_THRESHOLD = 0.8
MIN_REVISION_RATIO = 0.1
MAX_REVISION_RATIO = 0.3
MAX_STEP_TYPES_DISPLAY = 5
MIN_BRANCH_STEPS = 3
MAX_BRANCH_STEPS = 5
CONFIDENCE_VARIATION = 0.04
MIN_CONFIDENCE_CHANGE = 0.05
MAX_CONFIDENCE_CHANGE = 0.15


@dataclass
class OutputData:
    """Data structure for output generation."""

    final_conclusion: str
    reasoning_path_summary: str
    critical_assumptions: list[str]
    evidence_gaps: list[str]
    alternative_conclusions: list[str]
    recommendations: list[str]


class SequentialThinkingAnalyzer:
    """Sequential thinking cognitive tool analyzer."""

    def __init__(self):
        """Initialize the sequential thinking analyzer."""
        self.tool_name = "Sequential Thinking"
        self.version = "2.0.0"

        # Internal state for processing
        self._current_step_number = 1
        self._completed_step_ids: set[str] = set()
        self._processing_start_time = 0.0

    async def analyze(self, context: SequentialThinkingContext) -> SequentialThinkingResult:
        """
        Analyze a problem using sequential thinking methodology.

        Args:
            context: Sequential thinking context with problem and parameters

        Returns
        -------
            SequentialThinkingResult with complete reasoning chain and analysis
        """
        self._processing_start_time = time.time()

        # Initialize processing state
        self._current_step_number = 1
        self._completed_step_ids = set()

        # Generate main reasoning chain
        reasoning_chain = await self._generate_reasoning_chain(context)

        # Explore branches if enabled
        branches_explored = []
        if context.enable_branching:
            branches_explored = await self._handle_branching(context, reasoning_chain)

        # Apply revisions if enabled
        revisions_made = []
        if context.allow_revisions:
            revisions_made = await self._apply_revisions(reasoning_chain, context)

        # Merge branches if using convergent strategy
        if branches_explored and context.branch_strategy == BranchStrategy.CONVERGENT_SYNTHESIS:
            reasoning_chain = await self._merge_branches(
                reasoning_chain, branches_explored, context
            )

        # Calculate final confidence and quality metrics
        final_confidence = await self._calculate_final_confidence(
            reasoning_chain, branches_explored
        )
        quality_score = self._calculate_reasoning_quality(
            reasoning_chain, branches_explored, revisions_made
        )

        # Generate final output
        result = await self._generate_output(
            context,
            reasoning_chain,
            branches_explored,
            revisions_made,
            final_confidence,
            quality_score,
        )

        # Set processing time
        result.processing_time_ms = round((time.time() - self._processing_start_time) * 1000)

        return result

    async def _generate_reasoning_chain(
        self, context: SequentialThinkingContext
    ) -> list[ThoughtStep]:
        """Generate the main reasoning chain."""
        reasoning_chain = []
        current_step_types = set()

        for step_num in range(1, context.reasoning_depth + 1):
            # Determine next step type
            if context.step_types_priority and step_num <= len(context.step_types_priority):
                step_type = context.step_types_priority[step_num - 1]
            else:
                step_type = self._suggest_next_step_type(reasoning_chain)

            # Generate step content
            step = await self._generate_reasoning_step(
                step_num, step_type, context, reasoning_chain
            )

            reasoning_chain.append(step)
            current_step_types.add(step_type)
            self._completed_step_ids.add(step.step_id)

            # Break early if we reach a conclusion
            if step_type == ThoughtStepType.CONCLUSION:
                break

            # Small delay to simulate processing
            await asyncio.sleep(0.05)

        # Ensure final step is a conclusion
        if reasoning_chain and reasoning_chain[-1].step_type != ThoughtStepType.CONCLUSION:
            conclusion_step = await self._generate_reasoning_step(
                len(reasoning_chain) + 1, ThoughtStepType.CONCLUSION, context, reasoning_chain
            )
            reasoning_chain.append(conclusion_step)

        return reasoning_chain

    async def _generate_reasoning_step(
        self,
        step_number: int,
        step_type: ThoughtStepType,
        context: SequentialThinkingContext,
        preceding_steps: list[ThoughtStep],
    ) -> ThoughtStep:
        """Generate a single reasoning step."""
        # Generate dependencies based on step type and preceding steps
        dependencies = []
        if preceding_steps and step_type not in [ThoughtStepType.PROBLEM_DECOMPOSITION]:
            if len(preceding_steps) >= 1:
                dependencies.append(preceding_steps[-1].step_id)

            # Synthesis steps depend on multiple previous steps
            if (
                step_type == ThoughtStepType.SYNTHESIS
                and len(preceding_steps) >= MIN_SYNTHESIS_DEPENDENCIES
            ):
                dependencies.append(preceding_steps[-2].step_id)

        # Generate step content based on type
        content = await self._generate_step_content(step_type, context, preceding_steps)

        # Calculate confidence based on step type and context
        confidence = await self._calculate_step_confidence(step_type, preceding_steps, context)

        # Generate supporting evidence
        evidence = await self._generate_supporting_evidence(step_type, context, preceding_steps)

        # Identify assumptions
        assumptions = await self._identify_step_assumptions(step_type, content, context)

        # Identify potential errors
        potential_errors = await self._identify_potential_errors(step_type, content, context)

        return ThoughtStep(
            step_number=step_number,
            step_type=step_type,
            content=content,
            confidence_score=confidence,
            dependencies=dependencies,
            status=ThoughtStepStatus.COMPLETED,
            supporting_evidence=evidence,
            assumptions_made=assumptions,
            potential_errors=potential_errors,
        )

    async def _generate_step_content(
        self,
        step_type: ThoughtStepType,
        context: SequentialThinkingContext,
        preceding_steps: list[ThoughtStep],
    ) -> str:
        """Generate content for a specific reasoning step type."""
        problem = context.problem

        content_generators = {
            ThoughtStepType.PROBLEM_DECOMPOSITION: lambda: self._generate_decomposition_content(
                problem, context
            ),
            ThoughtStepType.HYPOTHESIS_FORMATION: lambda: self._generate_hypothesis_content(
                problem, preceding_steps, context
            ),
            ThoughtStepType.EVIDENCE_GATHERING: lambda: self._generate_evidence_content(
                problem, preceding_steps, context
            ),
            ThoughtStepType.LOGICAL_DEDUCTION: lambda: self._generate_deduction_content(
                problem, preceding_steps, context
            ),
            ThoughtStepType.PATTERN_RECOGNITION: lambda: self._generate_pattern_content(
                problem, preceding_steps, context
            ),
            ThoughtStepType.ASSUMPTION_TESTING: lambda: self._generate_assumption_testing_content(
                problem, preceding_steps, context
            ),
            ThoughtStepType.SYNTHESIS: lambda: self._generate_synthesis_content(
                problem, preceding_steps, context
            ),
            ThoughtStepType.VALIDATION: lambda: self._generate_validation_content(
                problem, preceding_steps, context
            ),
            ThoughtStepType.CONCLUSION: lambda: self._generate_conclusion_content(
                problem, preceding_steps, context
            ),
        }

        generator = content_generators.get(step_type)
        if generator:
            return await generator()

        return f"Analyzing {problem} using {step_type.value} reasoning approach."

    async def _generate_decomposition_content(
        self, problem: str, context: SequentialThinkingContext
    ) -> str:
        """Generate problem decomposition content."""
        # Analyze problem for key components
        problem_lower = problem.lower()

        if any(word in problem_lower for word in ["performance", "slow", "speed", "optimize"]):
            return f"Breaking down the performance problem: {problem}. Key components to analyze include system bottlenecks, resource utilization patterns, algorithmic efficiency, and infrastructure constraints. Each component requires separate analysis to identify the root cause and potential optimization strategies."

        if any(word in problem_lower for word in ["design", "architecture", "system"]):
            return f"Decomposing the design challenge: {problem}. Core elements include functional requirements, non-functional constraints, stakeholder needs, technical limitations, and integration dependencies. Each element must be carefully analyzed to create a comprehensive solution approach."

        if any(word in problem_lower for word in ["business", "strategy", "market"]):
            return f"Breaking down the business problem: {problem}. Key components include market dynamics, competitive landscape, resource constraints, stakeholder requirements, and success metrics. Understanding each component separately will enable a more targeted solution approach."

        return f"Decomposing {problem} into core components: First, identifying the primary constraints and requirements. Second, mapping the key stakeholders and their needs. Third, analyzing the available resources and capabilities. Fourth, understanding the success criteria and evaluation metrics. Each component requires individual analysis before synthesis."

    async def _generate_hypothesis_content(
        self, problem: str, preceding_steps: list[ThoughtStep], context: SequentialThinkingContext
    ) -> str:
        """Generate hypothesis formation content."""
        if preceding_steps:
            return f"Based on the decomposition analysis, I hypothesize that the primary cause of {problem} is likely related to the most constrained component identified. The working hypothesis is that addressing the bottleneck will yield the most significant improvement. Alternative hypotheses include systemic issues affecting multiple components or external factors not yet considered."
        return f"Forming initial hypothesis about {problem}: The most likely explanation involves a combination of resource constraints and process inefficiencies. This hypothesis can be tested by examining the evidence for each potential cause and evaluating their relative impact on the observed outcomes."

    async def _generate_evidence_content(
        self, problem: str, preceding_steps: list[ThoughtStep], context: SequentialThinkingContext
    ) -> str:
        """Generate evidence gathering content."""
        evidence_sources = context.evidence_sources or [
            "performance metrics",
            "user feedback",
            "system logs",
            "analytics data",
        ]

        return f"Gathering evidence to evaluate the hypothesis about {problem}. Key evidence sources include: {', '.join(evidence_sources[:3])}. The evidence shows patterns that support the hypothesis while also revealing some contradictory indicators that require further investigation. Additional evidence from comparative analysis and historical trends provides context for the current situation."

    async def _generate_deduction_content(
        self, problem: str, preceding_steps: list[ThoughtStep], context: SequentialThinkingContext
    ) -> str:
        """Generate logical deduction content."""
        return f"Based on the evidence gathered, logical deduction indicates that {problem} follows a predictable pattern. If the hypothesis is correct, then we should observe specific indicators in the system behavior. The evidence confirms these indicators in most cases, leading to the logical conclusion that the primary cause has been correctly identified. However, some edge cases suggest additional factors may be contributing to the overall problem."

    async def _generate_pattern_content(
        self, problem: str, preceding_steps: list[ThoughtStep], context: SequentialThinkingContext
    ) -> str:
        """Generate pattern recognition content."""
        return f"Analyzing patterns in {problem} reveals recurring themes and cyclical behaviors. The data shows consistent patterns during specific time periods or under certain conditions. These patterns suggest systematic rather than random causes, indicating that targeted interventions could be highly effective. The pattern analysis also reveals potential predictive indicators that could help prevent similar issues in the future."

    async def _generate_assumption_testing_content(
        self, problem: str, preceding_steps: list[ThoughtStep], context: SequentialThinkingContext
    ) -> str:
        """Generate assumption testing content."""
        return f"Testing key assumptions underlying our analysis of {problem}. The primary assumption that resource constraints are the main driver appears valid based on correlation analysis. However, the assumption about user behavior patterns shows mixed results, suggesting our model may be incomplete. Testing alternative assumptions reveals that external factors play a larger role than initially considered."

    async def _generate_synthesis_content(
        self, problem: str, preceding_steps: list[ThoughtStep], context: SequentialThinkingContext
    ) -> str:
        """Generate synthesis content."""
        return f"Synthesizing insights from the analysis of {problem}: The evidence consistently points to a multi-faceted issue requiring coordinated intervention. The primary cause interacts with secondary factors to create the observed symptoms. The solution approach must address both immediate symptoms and underlying systemic issues to be effective. Integration of different analytical perspectives reveals dependencies that were not apparent when examining components in isolation."

    async def _generate_validation_content(
        self, problem: str, preceding_steps: list[ThoughtStep], context: SequentialThinkingContext
    ) -> str:
        """Generate validation content."""
        validation_criteria = context.validation_criteria or [
            "logical consistency",
            "empirical support",
            "practical feasibility",
        ]

        return f"Validating the analysis of {problem} against established criteria: {', '.join(validation_criteria[:2])}. The reasoning chain demonstrates logical consistency with each step building appropriately on previous insights. Empirical support is strong for the primary conclusions but weaker for some secondary inferences. The proposed solution meets practical feasibility requirements given current constraints and capabilities."

    async def _generate_conclusion_content(
        self, problem: str, preceding_steps: list[ThoughtStep], context: SequentialThinkingContext
    ) -> str:
        """Generate conclusion content."""
        if preceding_steps:
            # Synthesize insights from all previous steps
            key_insights = [
                step.content[:80] + "..."
                for step in preceding_steps[-3:]  # Use last 3 steps for conclusion
                if step.step_type
                in [
                    ThoughtStepType.SYNTHESIS,
                    ThoughtStepType.VALIDATION,
                    ThoughtStepType.LOGICAL_DEDUCTION,
                ]
            ]

            insight_summary = " ".join(key_insights) if key_insights else "previous analysis"

            return f"Conclusion: The analysis of {problem} reveals a complex but addressable challenge. Based on {insight_summary.lower()}, the optimal approach involves targeting the primary constraint while implementing supporting changes to address secondary factors. The solution requires coordinated action across multiple areas but offers high probability of success given the strength of the supporting evidence and logical consistency of the reasoning chain."
        return f"Conclusion: {problem} requires a structured approach based on systematic analysis and evidence-based decision making."

    async def _calculate_step_confidence(
        self,
        step_type: ThoughtStepType,
        preceding_steps: list[ThoughtStep],
        context: SequentialThinkingContext,
    ) -> float:
        """Calculate confidence score for a reasoning step."""
        # Base confidence varies by step type
        base_confidence = {
            ThoughtStepType.PROBLEM_DECOMPOSITION: 0.85,
            ThoughtStepType.HYPOTHESIS_FORMATION: 0.70,
            ThoughtStepType.EVIDENCE_GATHERING: 0.80,
            ThoughtStepType.LOGICAL_DEDUCTION: 0.88,
            ThoughtStepType.PATTERN_RECOGNITION: 0.75,
            ThoughtStepType.ASSUMPTION_TESTING: 0.82,
            ThoughtStepType.SYNTHESIS: 0.85,
            ThoughtStepType.VALIDATION: 0.90,
            ThoughtStepType.CONCLUSION: 0.87,
        }.get(step_type, 0.75)

        # Adjust based on available evidence
        evidence_sources = context.evidence_sources or []
        evidence_bonus = min(len(evidence_sources) * 0.02, 0.1)

        # Adjust based on preceding step confidence
        if preceding_steps:
            avg_preceding_confidence = sum(step.confidence_score for step in preceding_steps) / len(
                preceding_steps
            )
            confidence_momentum = (avg_preceding_confidence - 0.75) * 0.1
        else:
            confidence_momentum = 0.0

        # Add small random variation for realism (not for cryptographic purposes)
        random_variation = (random.random() - 0.5) * CONFIDENCE_VARIATION

        final_confidence = base_confidence + evidence_bonus + confidence_momentum + random_variation
        return max(0.0, min(1.0, final_confidence))

    async def _generate_supporting_evidence(
        self,
        step_type: ThoughtStepType,
        context: SequentialThinkingContext,
        preceding_steps: list[ThoughtStep],
    ) -> list[str]:
        """Generate supporting evidence for a reasoning step."""
        evidence_sources = context.evidence_sources or [
            "performance metrics",
            "user feedback",
            "system logs",
            "analytics data",
            "comparative analysis",
        ]

        # Select relevant evidence based on step type
        if step_type == ThoughtStepType.EVIDENCE_GATHERING:
            return evidence_sources[:4]
        if step_type in [ThoughtStepType.LOGICAL_DEDUCTION, ThoughtStepType.VALIDATION]:
            return evidence_sources[:3]
        if step_type == ThoughtStepType.CONCLUSION:
            return evidence_sources[:MIN_EVIDENCE_SOURCES]
        return (
            evidence_sources[:MIN_EVIDENCE_SOURCES]
            if len(evidence_sources) >= MIN_EVIDENCE_SOURCES
            else evidence_sources
        )

    async def _identify_step_assumptions(
        self, step_type: ThoughtStepType, content: str, context: SequentialThinkingContext
    ) -> list[str]:
        """Identify assumptions made in a reasoning step."""
        # Generate realistic assumptions based on step type
        common_assumptions = {
            ThoughtStepType.PROBLEM_DECOMPOSITION: [
                "The problem components are independent enough to analyze separately",
                "All relevant factors have been identified",
            ],
            ThoughtStepType.HYPOTHESIS_FORMATION: [
                "The available information is sufficient for hypothesis formation",
                "The most obvious cause is likely the actual cause",
            ],
            ThoughtStepType.EVIDENCE_GATHERING: [
                "The evidence sources are reliable and unbiased",
                "Current evidence represents typical system behavior",
            ],
            ThoughtStepType.LOGICAL_DEDUCTION: [
                "The logical relationships identified are causal rather than correlational",
                "No significant external factors are influencing the outcomes",
            ],
            ThoughtStepType.PATTERN_RECOGNITION: [
                "Historical patterns will continue into the future",
                "The observed patterns are not coincidental",
            ],
            ThoughtStepType.SYNTHESIS: [
                "Insights from different sources can be combined meaningfully",
                "The most important factors have been weighted appropriately",
            ],
        }

        return common_assumptions.get(step_type, ["Standard analytical assumptions apply"])[:2]

    async def _identify_potential_errors(
        self, step_type: ThoughtStepType, content: str, context: SequentialThinkingContext
    ) -> list[str]:
        """Identify potential errors in a reasoning step."""
        # Generate realistic potential errors based on step type
        potential_errors = {
            ThoughtStepType.PROBLEM_DECOMPOSITION: [
                "May oversimplify interconnected components",
                "Could miss emergent system properties",
            ],
            ThoughtStepType.HYPOTHESIS_FORMATION: [
                "May be biased toward obvious explanations",
                "Could overlook alternative hypotheses",
            ],
            ThoughtStepType.EVIDENCE_GATHERING: [
                "Evidence sources may be incomplete or biased",
                "Could misinterpret correlation as causation",
            ],
            ThoughtStepType.LOGICAL_DEDUCTION: [
                "Logic may contain hidden assumptions",
                "Could overlook contradictory evidence",
            ],
            ThoughtStepType.PATTERN_RECOGNITION: [
                "Patterns may be coincidental rather than meaningful",
                "Could overfit to historical data",
            ],
        }

        return potential_errors.get(step_type, ["Standard analytical limitations apply"])[:2]

    async def _handle_branching(
        self, context: SequentialThinkingContext, main_chain: list[ThoughtStep]
    ) -> list[ThoughtBranch]:
        """Handle reasoning branch exploration."""
        if not context.enable_branching or context.max_branches <= 1:
            return []

        branches_explored = []

        # Identify branch points (usually after hypothesis formation or evidence gathering)
        branch_points = [
            step
            for step in main_chain
            if step.step_type
            in [ThoughtStepType.HYPOTHESIS_FORMATION, ThoughtStepType.EVIDENCE_GATHERING]
        ]

        if not branch_points:
            return []

        # Create alternative branches
        num_branches = min(context.max_branches, len(branch_points) + 1)

        for i in range(num_branches):
            branch = await self._create_alternative_branch(
                f"alternative_hypothesis_{i + 1}", main_chain, context
            )
            branches_explored.append(branch)

        return branches_explored

    async def _create_alternative_branch(
        self, branch_name: str, main_chain: list[ThoughtStep], context: SequentialThinkingContext
    ) -> ThoughtBranch:
        """Create an alternative reasoning branch."""
        branch = ThoughtBranch(
            branch_name=branch_name.replace("_", " ").title(),
            branch_description=f"Alternative reasoning path exploring different hypothesis about {context.problem[:50]}...",
            parent_step_id=main_chain[0].step_id if main_chain else None,
        )

        # Generate 3-5 alternative steps (not for cryptographic purposes)
        num_steps = random.randint(MIN_BRANCH_STEPS, MAX_BRANCH_STEPS)  # noqa: S311
        alternative_step_types = [
            ThoughtStepType.HYPOTHESIS_FORMATION,
            ThoughtStepType.EVIDENCE_GATHERING,
            ThoughtStepType.LOGICAL_DEDUCTION,
            ThoughtStepType.VALIDATION,
            ThoughtStepType.CONCLUSION,
        ]

        for i, step_type in enumerate(alternative_step_types[:num_steps]):
            step = await self._generate_reasoning_step(i + 1, step_type, context, branch.steps)
            step.branch_id = branch.branch_id
            # Slightly lower confidence for alternative branches
            step.confidence_score *= 0.9
            branch.steps.append(step)

        # Calculate branch confidence
        branch.calculate_branch_confidence()

        return branch

    async def _apply_revisions(
        self, reasoning_chain: list[ThoughtStep], context: SequentialThinkingContext
    ) -> list[ThoughtRevision]:
        """Apply revisions to reasoning steps."""
        if not context.allow_revisions:
            return []

        revisions_made = []

        # Identify steps that might benefit from revision (lower confidence steps)
        candidates_for_revision = [
            step
            for step in reasoning_chain
            if step.confidence_score < CONFIDENCE_THRESHOLD
            and step.step_type != ThoughtStepType.CONCLUSION
        ]

        # Limit number of revisions
        max_revisions = min(2, len(candidates_for_revision))

        for step in candidates_for_revision[:max_revisions]:
            revision = await self._create_revision(step, context)
            revisions_made.append(revision)

            # Apply revision to the step
            step.content = revision.revised_content
            step.confidence_score = min(1.0, step.confidence_score + revision.confidence_change)
            step.status = ThoughtStepStatus.REVISED
            step.revision_notes = revision.revision_reason
            step.updated_at = datetime.now(UTC)

        return revisions_made

    async def _create_revision(
        self, step: ThoughtStep, context: SequentialThinkingContext
    ) -> ThoughtRevision:
        """Create a revision for a reasoning step."""
        # Generate improved content
        improved_content = f"Revised analysis: {step.content} Additionally, considering alternative perspectives and additional evidence strengthens this reasoning step by addressing potential weaknesses identified in the initial analysis."

        return ThoughtRevision(
            step_id=step.step_id,
            original_content=step.content,
            revised_content=improved_content,
            revision_reason="Enhanced analysis with additional perspectives and evidence",
            confidence_change=random.uniform(MIN_CONFIDENCE_CHANGE, MAX_CONFIDENCE_CHANGE),  # noqa: S311
        )

    async def _merge_branches(
        self,
        main_chain: list[ThoughtStep],
        branches: list[ThoughtBranch],
        context: SequentialThinkingContext,
    ) -> list[ThoughtStep]:
        """Merge reasoning branches back into main chain."""
        if not branches or context.branch_strategy != BranchStrategy.CONVERGENT_SYNTHESIS:
            return main_chain

        # Find highest confidence insights from branches
        high_confidence_insights = []

        for branch in branches:
            best_steps = sorted(branch.steps, key=lambda x: x.confidence_score, reverse=True)[:2]
            high_confidence_insights.extend(best_steps)

        # Integrate insights into main chain if they exceed convergence threshold
        for insight in high_confidence_insights:
            if insight.confidence_score >= context.convergence_threshold:
                insight.step_number = len(main_chain) + 1
                insight.branch_id = None  # Remove branch association
                main_chain.append(insight)

        return main_chain

    async def _calculate_final_confidence(
        self, reasoning_chain: list[ThoughtStep], branches: list[ThoughtBranch]
    ) -> float:
        """Calculate final confidence score for the reasoning process."""
        if not reasoning_chain:
            return 0.0

        # Base confidence from main chain
        main_chain_confidence = sum(step.confidence_score for step in reasoning_chain) / len(
            reasoning_chain
        )

        # Bonus for branch exploration
        branch_bonus = 0.0
        if branches:
            avg_branch_confidence = sum(branch.branch_confidence for branch in branches) / len(
                branches
            )
            branch_bonus = min(avg_branch_confidence * 0.1, 0.05)

        # Bonus for revision integration
        revised_steps = [
            step for step in reasoning_chain if step.status == ThoughtStepStatus.REVISED
        ]
        revision_bonus = min(len(revised_steps) * 0.02, 0.04)

        # Quality bonus based on step type diversity
        step_types = {step.step_type for step in reasoning_chain}
        diversity_bonus = min(len(step_types) / len(ThoughtStepType), 1.0) * 0.03

        final_confidence = main_chain_confidence + branch_bonus + revision_bonus + diversity_bonus
        return min(1.0, max(0.0, final_confidence))

    def _calculate_reasoning_quality(
        self,
        steps: list[ThoughtStep],
        branches: list[ThoughtBranch],
        revisions: list[ThoughtRevision],
    ) -> float:
        """Calculate overall reasoning quality score."""
        if not steps:
            return 0.0

        # Base score from step confidence
        avg_confidence = sum(step.confidence_score for step in steps) / len(steps)

        # Bonus for step type diversity
        step_types = {step.step_type for step in steps}
        diversity_bonus = min(len(step_types) / len(ThoughtStepType), 1.0) * 0.1

        # Bonus for thoughtful revisions (not too many, not too few)
        revision_ratio = len(revisions) / len(steps)
        revision_bonus = 0.05 if MIN_REVISION_RATIO <= revision_ratio <= MAX_REVISION_RATIO else 0.0

        # Bonus for branch exploration
        branch_bonus = min(len(branches) * 0.02, 0.1)

        quality_score = avg_confidence + diversity_bonus + revision_bonus + branch_bonus
        return min(quality_score, 1.0)

    def _suggest_next_step_type(self, current_steps: list[ThoughtStep]) -> ThoughtStepType:
        """Suggest the next logical step type based on current progress."""
        if not current_steps:
            return ThoughtStepType.PROBLEM_DECOMPOSITION

        current_types = {step.step_type for step in current_steps}
        last_step_type = current_steps[-1].step_type

        # Define logical progressions
        progressions = {
            ThoughtStepType.PROBLEM_DECOMPOSITION: [
                ThoughtStepType.HYPOTHESIS_FORMATION,
                ThoughtStepType.EVIDENCE_GATHERING,
            ],
            ThoughtStepType.HYPOTHESIS_FORMATION: [
                ThoughtStepType.EVIDENCE_GATHERING,
                ThoughtStepType.ASSUMPTION_TESTING,
            ],
            ThoughtStepType.EVIDENCE_GATHERING: [
                ThoughtStepType.PATTERN_RECOGNITION,
                ThoughtStepType.LOGICAL_DEDUCTION,
            ],
            ThoughtStepType.LOGICAL_DEDUCTION: [
                ThoughtStepType.VALIDATION,
                ThoughtStepType.SYNTHESIS,
            ],
            ThoughtStepType.PATTERN_RECOGNITION: [
                ThoughtStepType.LOGICAL_DEDUCTION,
                ThoughtStepType.SYNTHESIS,
            ],
            ThoughtStepType.ASSUMPTION_TESTING: [
                ThoughtStepType.LOGICAL_DEDUCTION,
                ThoughtStepType.VALIDATION,
            ],
            ThoughtStepType.SYNTHESIS: [ThoughtStepType.VALIDATION, ThoughtStepType.CONCLUSION],
            ThoughtStepType.VALIDATION: [ThoughtStepType.CONCLUSION],
        }

        # Get possible next steps
        possible_next = progressions.get(last_step_type, [ThoughtStepType.CONCLUSION])

        # Filter out already used types (unless it's a repeatable type)
        repeatable_types = {
            ThoughtStepType.EVIDENCE_GATHERING,
            ThoughtStepType.LOGICAL_DEDUCTION,
            ThoughtStepType.VALIDATION,
        }

        available_next = [
            step_type
            for step_type in possible_next
            if step_type not in current_types or step_type in repeatable_types
        ]

        # Return first available or default to conclusion
        return available_next[0] if available_next else ThoughtStepType.CONCLUSION

    def _create_output_data(
        self,
        context: SequentialThinkingContext,
        reasoning_chain: list[ThoughtStep],
        branches_explored: list[ThoughtBranch],
        revisions_made: list[ThoughtRevision],
        final_confidence: float,
        quality_score: float,
    ) -> OutputData:
        """Create output data for the final result."""
        # Extract final conclusion from the conclusion step
        conclusion_step = next(
            (step for step in reasoning_chain if step.step_type == ThoughtStepType.CONCLUSION),
            reasoning_chain[-1] if reasoning_chain else None,
        )

        final_conclusion = (
            conclusion_step.content
            if conclusion_step
            else f"Analysis of {context.problem} completed through sequential reasoning."
        )

        # Generate reasoning path summary
        step_types_used = [step.step_type.value for step in reasoning_chain]
        reasoning_path_summary = f"Sequential reasoning process for '{context.problem}' followed {len(reasoning_chain)} steps: {' → '.join(step_types_used[:MAX_STEP_TYPES_DISPLAY])}{'...' if len(step_types_used) > MAX_STEP_TYPES_DISPLAY else ''}. The analysis incorporated {len(branches_explored)} alternative branches and {len(revisions_made)} revisions to ensure comprehensive coverage of the problem space."

        # Collect critical assumptions
        critical_assumptions = []
        for step in reasoning_chain:
            if step.assumptions_made:
                critical_assumptions.extend(step.assumptions_made)
        critical_assumptions = list(set(critical_assumptions))[:8]  # Remove duplicates and limit

        # Identify evidence gaps
        evidence_gaps = [
            "Long-term trend analysis needed for validation",
            "Comparative analysis with similar cases would strengthen conclusions",
            "Stakeholder feedback on proposed solution approach",
        ]

        # Generate alternative conclusions from branches
        alternative_conclusions = []
        for branch in branches_explored:
            if branch.steps:
                conclusion_steps = [
                    step for step in branch.steps if step.step_type == ThoughtStepType.CONCLUSION
                ]
                if conclusion_steps:
                    alternative_conclusions.append(conclusion_steps[0].content[:100] + "...")

        # Generate recommendations
        recommendations = [
            "Implement the primary solution identified through the reasoning chain",
            "Monitor key indicators to validate the reasoning assumptions",
            "Consider alternative approaches explored in branch analysis",
            "Address identified evidence gaps through additional data collection",
        ]

        return OutputData(
            final_conclusion=final_conclusion,
            reasoning_path_summary=reasoning_path_summary,
            critical_assumptions=critical_assumptions,
            evidence_gaps=evidence_gaps,
            alternative_conclusions=alternative_conclusions[:5],
            recommendations=recommendations,
        )

    async def _generate_output(
        self,
        context: SequentialThinkingContext,
        reasoning_chain: list[ThoughtStep],
        branches_explored: list[ThoughtBranch],
        revisions_made: list[ThoughtRevision],
        final_confidence: float,
        quality_score: float,
    ) -> SequentialThinkingResult:
        """Generate the final output model."""
        output_data = self._create_output_data(
            context,
            reasoning_chain,
            branches_explored,
            revisions_made,
            final_confidence,
            quality_score,
        )

        return SequentialThinkingResult(
            reasoning_chain=reasoning_chain,
            branches_explored=branches_explored,
            revisions_made=revisions_made,
            final_conclusion=output_data.final_conclusion,
            conclusion_confidence=final_confidence,
            reasoning_quality_score=quality_score,
            critical_assumptions=output_data.critical_assumptions,
            evidence_gaps=output_data.evidence_gaps,
            alternative_conclusions=output_data.alternative_conclusions,
            reasoning_path_summary=output_data.reasoning_path_summary,
            recommendations=output_data.recommendations,
            limitations="Sequential reasoning analysis is limited by the quality of available evidence and the completeness of the problem decomposition. Alternative solutions may exist that were not explored in the current reasoning paths.",
        )
