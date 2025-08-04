"""
Collaborative Reasoning Analyzer

Core implementation of the collaborative reasoning cognitive tool, providing
multi-perspective reasoning through persona simulation, stakeholder analysis,
consensus building, and team dynamics modeling.
"""

import asyncio
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from .models import (
    CollaborativeDialogue,
    CollaborativeReasoningContext,
    CollaborativeReasoningResult,
    ConsensusResult,
    ConsensusStrategy,
    DialogueStyle,
    Persona,
    PersonaPerspective,
    PersonaType,
    ReasoningStyle,
)


class CollaborativeReasoningAnalyzer:
    """Collaborative reasoning cognitive tool analyzer"""

    def __init__(self):
        """Initialize the collaborative reasoning analyzer"""
        self.tool_name = "Collaborative Reasoning"
        self.version = "1.0.0"

        # Internal state for processing
        self._processing_start_time = 0.0

    async def analyze(self, context: CollaborativeReasoningContext) -> CollaborativeReasoningResult:
        """
        Analyze a problem using collaborative reasoning with multiple personas.

        Args:
            context: Collaborative reasoning context with problem and personas

        Returns:
            CollaborativeReasoningResult with consensus and insights
        """
        self._processing_start_time = time.time()

        # Phase 1: Generate individual perspectives
        persona_perspectives = await self._generate_persona_perspectives(context)

        # Phase 2: Facilitate collaborative dialogue
        dialogue_records = await self._facilitate_dialogue(
            context, persona_perspectives
        )

        # Phase 3: Build consensus
        consensus_result = await self._build_consensus(
            context, persona_perspectives, dialogue_records
        )

        # Phase 4: Generate insights and recommendations
        key_insights, recommendations, considerations = await self._generate_insights(
            context, persona_perspectives, dialogue_records, consensus_result
        )

        # Calculate quality metrics
        diversity_score = self._calculate_diversity_score(persona_perspectives)
        collaboration_quality = self._calculate_collaboration_quality(
            dialogue_records, consensus_result
        )
        stakeholder_buy_in = self._assess_stakeholder_buy_in(
            persona_perspectives, consensus_result
        )

        # Calculate processing time
        processing_time = time.time() - self._processing_start_time

        return CollaborativeReasoningResult(
            persona_perspectives=persona_perspectives,
            dialogue_records=dialogue_records,
            consensus_result=consensus_result,
            key_insights=key_insights,
            perspective_diversity_score=diversity_score,
            collaboration_quality_score=collaboration_quality,
            unresolved_tensions=consensus_result.unresolved_issues,
            recommended_next_steps=recommendations,
            stakeholder_buy_in_assessment=stakeholder_buy_in,
            implementation_considerations=considerations,
            dialogue_duration_minutes=processing_time / 60.0,
            personas_engaged=len([p for p in persona_perspectives if p.confidence_level > 0.3]),
            consensus_confidence=consensus_result.confidence_in_consensus,
            processing_time_ms=round(processing_time * 1000)
        )

    async def _generate_persona_perspectives(
        self, context: CollaborativeReasoningContext
    ) -> list[PersonaPerspective]:
        """Generate individual perspectives from each persona"""
        perspectives = []

        # Simulate processing delay
        await asyncio.sleep(0.1)

        for persona in context.personas:
            perspective = await self._simulate_persona_reasoning(persona, context)
            perspectives.append(perspective)

        # Add devil's advocate if enabled
        if context.include_devil_advocate:
            devil_advocate = await self._generate_devil_advocate_perspective(
                context, perspectives
            )
            perspectives.append(devil_advocate)

        return perspectives

    async def _simulate_persona_reasoning(
        self, persona: Persona, context: CollaborativeReasoningContext
    ) -> PersonaPerspective:
        """Simulate reasoning from a specific persona's perspective"""

        # Analyze problem through persona's lens
        viewpoint = self._generate_persona_viewpoint(persona, context)
        concerns = self._identify_persona_concerns(persona, context)
        suggestions = self._generate_persona_suggestions(persona, context)

        # Simulate reasoning process
        reasoning_path = [
            f"Analyzed problem from {persona.persona_type.value} perspective",
            f"Applied {persona.reasoning_style.value} reasoning approach",
            f"Considered {len(persona.priorities)} key priorities",
            f"Evaluated {len(persona.constraints)} constraints",
            "Formed viewpoint based on background and expertise"
        ]

        # Calculate confidence based on expertise and problem alignment
        confidence = self._calculate_persona_confidence(persona, context)

        return PersonaPerspective(
            persona_name=persona.name,
            viewpoint=viewpoint,
            concerns=concerns,
            suggestions=suggestions,
            supporting_arguments=self._generate_supporting_arguments(persona, viewpoint),
            objections=self._generate_objections(persona, context),
            confidence_level=confidence,
            reasoning_path=reasoning_path
        )

    async def _facilitate_dialogue(
        self,
        context: CollaborativeReasoningContext,
        perspectives: list[PersonaPerspective]
    ) -> list[CollaborativeDialogue]:
        """Facilitate dialogue between personas"""
        dialogues = []

        # Simulate processing delay
        await asyncio.sleep(0.1)

        for round_num in range(context.max_dialogue_rounds):
            # Create dialogue for this round
            dialogue = CollaborativeDialogue(
                participants=[p.persona_name for p in perspectives],
                topic=f"Round {round_num + 1}: {context.reasoning_focus}",
                exchanges=[],
                consensus_points=[],
                disagreements=[],
                resolution_attempts=[],
                duration_minutes=2.0  # Simulated duration
            )

            # Simulate exchanges
            for perspective in perspectives:
                exchange = {
                    "speaker": perspective.persona_name,
                    "message": self._generate_dialogue_message(perspective, round_num),
                    "timestamp": datetime.now().isoformat(),
                    "response_to": None
                }
                dialogue.exchanges.append(exchange)

            # Identify consensus points and disagreements
            dialogue.consensus_points = self._identify_consensus_points(perspectives)
            dialogue.disagreements = self._identify_disagreements(perspectives)
            dialogue.resolution_attempts = self._generate_resolution_attempts(
                dialogue.disagreements
            )

            # Set outcome
            if len(dialogue.consensus_points) > len(dialogue.disagreements):
                dialogue.outcome = "Productive dialogue with emerging consensus"
            else:
                dialogue.outcome = "Dialogue revealed significant disagreements"

            dialogues.append(dialogue)

            # Allow persona evolution if enabled
            if context.allow_persona_evolution:
                await self._evolve_perspectives(perspectives, dialogue)

        return dialogues

    async def _build_consensus(
        self,
        context: CollaborativeReasoningContext,
        perspectives: list[PersonaPerspective],
        dialogues: list[CollaborativeDialogue]
    ) -> ConsensusResult:
        """Build consensus from perspectives and dialogue"""

        # Simulate processing delay
        await asyncio.sleep(0.1)

        strategy = context.consensus_strategy

        if strategy == ConsensusStrategy.WEIGHTED_CONSENSUS:
            return await self._weighted_consensus(perspectives, context)
        elif strategy == ConsensusStrategy.MAJORITY_VOTE:
            return await self._majority_vote_consensus(perspectives)
        elif strategy == ConsensusStrategy.COMPROMISE_SOLUTION:
            return await self._compromise_consensus(perspectives, dialogues)
        else:
            return await self._default_consensus(perspectives)

    async def _weighted_consensus(
        self,
        perspectives: list[PersonaPerspective],
        context: CollaborativeReasoningContext
    ) -> ConsensusResult:
        """Build consensus using weighted approach"""

        # Calculate persona weights
        persona_weights = {}
        for persona in context.personas:
            weight = persona.influence_weight
            if context.weight_by_expertise:
                # Increase weight based on expertise areas
                expertise_bonus = len(persona.expertise_areas) * 0.1
                weight += expertise_bonus
            persona_weights[persona.name] = weight

        # Add devil's advocate weight if present
        if context.include_devil_advocate:
            persona_weights["Devil's Advocate"] = 1.0

        # Calculate weighted agreement
        total_weight = sum(persona_weights.values())
        weighted_confidence = sum(
            p.confidence_level * persona_weights.get(p.persona_name, 1.0)
            for p in perspectives
        ) / total_weight if total_weight > 0 else 0.5

        # Generate consensus solution
        consensus_solution = self._synthesize_perspectives(perspectives)

        # Identify dissenting opinions
        dissenting = [
            f"{p.persona_name}: {p.viewpoint[:100]}..."
            for p in perspectives
            if p.confidence_level < 0.5
        ]

        return ConsensusResult(
            strategy_used=ConsensusStrategy.WEIGHTED_CONSENSUS,
            consensus_reached=weighted_confidence > 0.6,
            agreement_level=weighted_confidence,
            agreed_solution=consensus_solution if weighted_confidence > 0.6 else None,
            dissenting_opinions=dissenting[:5],  # Limit to 5
            compromise_elements=self._identify_compromise_elements(perspectives),
            unresolved_issues=self._identify_unresolved_issues(perspectives),
            confidence_in_consensus=weighted_confidence
        )

    async def _majority_vote_consensus(
        self, perspectives: list[PersonaPerspective]
    ) -> ConsensusResult:
        """Build consensus using majority vote"""

        # Group similar perspectives
        perspective_groups = self._group_similar_perspectives(perspectives)

        # Find majority
        largest_group = max(perspective_groups, key=len) if perspective_groups else []
        agreement_level = len(largest_group) / len(perspectives) if perspectives else 0.0

        consensus_solution = self._synthesize_group_perspectives(largest_group)

        # Find dissenting opinions
        dissenting = []
        for group in perspective_groups:
            if group != largest_group:
                for p in group:
                    dissenting.append(f"{p.persona_name}: {p.viewpoint[:100]}...")

        return ConsensusResult(
            strategy_used=ConsensusStrategy.MAJORITY_VOTE,
            consensus_reached=agreement_level > 0.5,
            agreement_level=agreement_level,
            agreed_solution=consensus_solution if agreement_level > 0.5 else None,
            dissenting_opinions=dissenting[:5],
            compromise_elements=[],
            unresolved_issues=self._identify_unresolved_issues(perspectives),
            confidence_in_consensus=agreement_level
        )

    async def _compromise_consensus(
        self,
        perspectives: list[PersonaPerspective],
        dialogues: list[CollaborativeDialogue]
    ) -> ConsensusResult:
        """Build consensus through compromise"""

        # Extract common elements from all perspectives
        common_elements = self._find_common_elements(perspectives)

        # Identify areas of compromise
        compromise_areas = []
        for dialogue in dialogues:
            compromise_areas.extend(dialogue.resolution_attempts)

        # Build compromise solution
        compromise_solution = self._build_compromise_solution(
            common_elements, compromise_areas
        )

        # Calculate agreement level based on compromise acceptance
        agreement_level = min(0.8, len(common_elements) / max(len(perspectives), 1))

        return ConsensusResult(
            strategy_used=ConsensusStrategy.COMPROMISE_SOLUTION,
            consensus_reached=True,
            agreement_level=agreement_level,
            agreed_solution=compromise_solution,
            dissenting_opinions=[],
            compromise_elements=compromise_areas[:5],
            unresolved_issues=self._identify_unresolved_issues(perspectives),
            confidence_in_consensus=agreement_level
        )

    async def _default_consensus(
        self, perspectives: list[PersonaPerspective]
    ) -> ConsensusResult:
        """Default consensus building approach"""

        # Simple averaging approach
        avg_confidence = sum(p.confidence_level for p in perspectives) / len(perspectives) if perspectives else 0.5
        consensus_solution = self._synthesize_perspectives(perspectives)

        return ConsensusResult(
            strategy_used=ConsensusStrategy.WEIGHTED_CONSENSUS,
            consensus_reached=avg_confidence > 0.6,
            agreement_level=avg_confidence,
            agreed_solution=consensus_solution if avg_confidence > 0.6 else None,
            dissenting_opinions=[],
            compromise_elements=[],
            unresolved_issues=[],
            confidence_in_consensus=avg_confidence
        )

    async def _generate_insights(
        self,
        context: CollaborativeReasoningContext,
        perspectives: list[PersonaPerspective],
        dialogues: list[CollaborativeDialogue],
        consensus: ConsensusResult
    ) -> tuple[list[str], list[str], list[str]]:
        """Generate key insights, recommendations, and considerations"""

        # Key insights from collaborative process
        insights = [
            f"Achieved {consensus.agreement_level:.1%} consensus among {len(perspectives)} perspectives",
            f"Perspective diversity score: {self._calculate_diversity_score(perspectives):.2f}",
            f"Most influential viewpoint: {max(perspectives, key=lambda p: p.confidence_level).persona_name}" if perspectives else "No clear leader",
        ]

        # Add consensus points if available
        if dialogues and dialogues[0].consensus_points:
            insights.append(f"Key areas of agreement: {', '.join(dialogues[0].consensus_points[:3])}")

        # Recommendations
        recommendations = []
        if consensus.agreement_level > 0.7:
            recommendations.append("Proceed with consensus solution given high agreement")
        else:
            recommendations.append("Consider additional dialogue rounds for better consensus")

        recommendations.extend([
            "Address dissenting opinions through targeted engagement",
            "Monitor implementation for stakeholder concerns",
            "Schedule follow-up review to assess outcomes"
        ])

        # Implementation considerations
        considerations = [
            "Stakeholder communication strategy needed",
            "Change management approach for dissenting parties",
            "Resource allocation based on consensus priorities",
            "Risk mitigation for unresolved issues"
        ]

        return insights[:5], recommendations[:5], considerations[:5]

    async def _generate_devil_advocate_perspective(
        self,
        context: CollaborativeReasoningContext,
        existing_perspectives: list[PersonaPerspective]
    ) -> PersonaPerspective:
        """Generate devil's advocate perspective"""

        # Analyze existing perspectives to challenge them
        common_themes = self._find_common_elements(existing_perspectives)

        return PersonaPerspective(
            persona_name="Devil's Advocate",
            viewpoint="Challenge the consensus and identify potential flaws in the proposed approach",
            concerns=[
                "Potential for groupthink in current perspectives",
                "Overlooked risks and negative consequences",
                "Alternative solutions not being considered",
                "Assumptions that may be invalid"
            ],
            suggestions=[
                "Consider contrarian viewpoints seriously",
                "Test all assumptions before proceeding",
                "Explore completely different approaches",
                "Plan for worst-case scenarios"
            ],
            supporting_arguments=[
                "History shows consensus can miss critical issues",
                "Diverse viewpoints prevent costly mistakes",
                "Challenging assumptions leads to innovation"
            ],
            objections=[
                f"The focus on {common_themes[0]} may be misguided" if common_themes else "Current approach lacks critical analysis"
            ],
            confidence_level=0.7,
            reasoning_path=[
                "Analyzed existing perspectives for blind spots",
                "Identified potential biases and groupthink",
                "Formulated alternative viewpoints",
                "Challenged core assumptions"
            ]
        )

    async def _evolve_perspectives(
        self,
        perspectives: list[PersonaPerspective],
        dialogue: CollaborativeDialogue
    ) -> None:
        """Allow perspectives to evolve based on dialogue"""
        # Simple evolution - adjust confidence based on consensus
        if len(dialogue.consensus_points) > len(dialogue.disagreements):
            for perspective in perspectives:
                perspective.confidence_level = min(1.0, perspective.confidence_level + 0.1)
        else:
            for perspective in perspectives:
                perspective.confidence_level = max(0.0, perspective.confidence_level - 0.05)

    # Helper methods for persona reasoning
    def _generate_persona_viewpoint(
        self, persona: Persona, context: CollaborativeReasoningContext
    ) -> str:
        """Generate viewpoint for a specific persona"""
        priorities_text = ', '.join(persona.priorities[:2]) if persona.priorities else "general objectives"
        constraints_text = ', '.join(persona.constraints[:2]) if persona.constraints else "standard limitations"

        return (
            f"From a {persona.persona_type.value} perspective, {context.reasoning_focus} "
            f"requires considering {priorities_text} while managing {constraints_text}"
        )

    def _identify_persona_concerns(
        self, persona: Persona, context: CollaborativeReasoningContext
    ) -> list[str]:
        """Identify concerns for a specific persona"""
        base_concerns = [f"Impact on {priority}" for priority in persona.priorities[:3]]
        constraint_concerns = [f"Constraint: {constraint}" for constraint in persona.constraints[:2]]
        return (base_concerns + constraint_concerns)[:5]

    def _generate_persona_suggestions(
        self, persona: Persona, context: CollaborativeReasoningContext
    ) -> list[str]:
        """Generate suggestions from a persona's perspective"""
        suggestions = []

        if persona.priorities:
            suggestions.append(f"Focus on {persona.priorities[0]}")

        suggestions.append(f"Consider {persona.reasoning_style.value} approach to problem-solving")

        if persona.expertise_areas:
            suggestions.append(f"Leverage expertise in {persona.expertise_areas[0]}")

        return suggestions[:3]

    def _calculate_persona_confidence(
        self, persona: Persona, context: CollaborativeReasoningContext
    ) -> float:
        """Calculate confidence level for a persona"""
        base_confidence = 0.5

        # Increase confidence based on expertise relevance
        if persona.expertise_areas:
            problem_words = context.problem.lower().split()
            for area in persona.expertise_areas:
                if any(word in area.lower() for word in problem_words):
                    base_confidence += 0.2
                    break

        # Adjust based on reasoning style match with problem complexity
        if context.complexity_level.value in ["complex", "very_complex"]:
            if persona.reasoning_style in [ReasoningStyle.ANALYTICAL, ReasoningStyle.SYSTEMATIC]:
                base_confidence += 0.1

        return min(1.0, base_confidence)

    def _generate_supporting_arguments(
        self, persona: Persona, viewpoint: str
    ) -> list[str]:
        """Generate supporting arguments for a persona's viewpoint"""
        arguments = [
            f"Based on {persona.persona_type.value} experience",
            f"Consistent with {persona.reasoning_style.value} approach"
        ]

        if persona.expertise_areas:
            arguments.append(f"Supported by expertise in {persona.expertise_areas[0]}")

        return arguments[:3]

    def _generate_objections(
        self, persona: Persona, context: CollaborativeReasoningContext
    ) -> list[str]:
        """Generate objections from a persona's perspective"""
        objections = []

        for constraint in persona.constraints[:2]:
            objections.append(f"Potential conflict with {constraint}")

        return objections

    def _generate_dialogue_message(
        self, perspective: PersonaPerspective, round_num: int
    ) -> str:
        """Generate dialogue message for a perspective"""
        return f"Round {round_num + 1}: {perspective.viewpoint[:100]}..."

    def _identify_consensus_points(
        self, perspectives: list[PersonaPerspective]
    ) -> list[str]:
        """Identify points of consensus among perspectives"""
        # Simple implementation - in practice would use NLP
        consensus_points = ["Need for clear problem definition"]

        # Check if majority share concerns
        all_concerns = [concern for p in perspectives for concern in p.concerns]
        if all_concerns:
            consensus_points.append("Shared concern for outcome quality")

        return consensus_points[:3]

    def _identify_disagreements(
        self, perspectives: list[PersonaPerspective]
    ) -> list[str]:
        """Identify disagreements among perspectives"""
        return [
            "Different priority rankings",
            "Varying risk tolerance levels",
            "Disagreement on resource allocation"
        ][:2]

    def _generate_resolution_attempts(self, disagreements: list[str]) -> list[str]:
        """Generate resolution attempts for disagreements"""
        return [f"Attempt to resolve: {d}" for d in disagreements[:2]]

    # Metric calculation methods
    def _calculate_diversity_score(self, perspectives: list[PersonaPerspective]) -> float:
        """Calculate diversity score of perspectives"""
        if len(perspectives) <= 1:
            return 0.0

        # Calculate based on viewpoint uniqueness
        unique_viewpoints = len(set(p.viewpoint[:50] for p in perspectives))
        return min(1.0, unique_viewpoints / len(perspectives))

    def _calculate_collaboration_quality(
        self,
        dialogues: list[CollaborativeDialogue],
        consensus: ConsensusResult
    ) -> float:
        """Calculate quality of collaborative process"""
        if not dialogues:
            return 0.5

        # Factor in dialogue productivity
        dialogue_scores = []
        for dialogue in dialogues:
            if dialogue.consensus_points or dialogue.disagreements:
                score = len(dialogue.consensus_points) / (
                    len(dialogue.consensus_points) + len(dialogue.disagreements)
                )
                dialogue_scores.append(score)

        dialogue_quality = sum(dialogue_scores) / len(dialogue_scores) if dialogue_scores else 0.5
        consensus_quality = consensus.agreement_level

        return (dialogue_quality + consensus_quality) / 2.0

    def _assess_stakeholder_buy_in(
        self,
        perspectives: list[PersonaPerspective],
        consensus: ConsensusResult
    ) -> dict[str, float]:
        """Assess stakeholder buy-in levels"""
        return {
            p.persona_name: p.confidence_level * (1.0 if consensus.consensus_reached else 0.5)
            for p in perspectives
        }

    # Consensus building helpers
    def _synthesize_perspectives(self, perspectives: list[PersonaPerspective]) -> str:
        """Synthesize multiple perspectives into a solution"""
        high_confidence_perspectives = [
            p for p in perspectives if p.confidence_level > 0.6
        ]

        if high_confidence_perspectives:
            return (
                f"Integrated solution incorporating insights from "
                f"{len(high_confidence_perspectives)} high-confidence perspectives, "
                f"balancing diverse viewpoints and constraints"
            )
        else:
            return f"Balanced solution considering all {len(perspectives)} perspectives equally"

    def _group_similar_perspectives(
        self, perspectives: list[PersonaPerspective]
    ) -> list[list[PersonaPerspective]]:
        """Group similar perspectives together"""
        # Simple grouping by confidence level
        high_confidence = [p for p in perspectives if p.confidence_level >= 0.7]
        medium_confidence = [p for p in perspectives if 0.4 <= p.confidence_level < 0.7]
        low_confidence = [p for p in perspectives if p.confidence_level < 0.4]

        groups = []
        if high_confidence:
            groups.append(high_confidence)
        if medium_confidence:
            groups.append(medium_confidence)
        if low_confidence:
            groups.append(low_confidence)

        return groups if groups else [[]]

    def _synthesize_group_perspectives(
        self, group: list[PersonaPerspective]
    ) -> str:
        """Synthesize perspectives from a group"""
        if not group:
            return "No clear consensus emerged"

        return f"Majority solution from {len(group)} aligned perspectives"

    def _find_common_elements(self, perspectives: list[PersonaPerspective]) -> list[str]:
        """Find common elements across perspectives"""
        if not perspectives:
            return []

        # Simple implementation - find common concerns
        common_elements = []

        # Check first perspective's concerns against others
        if perspectives[0].concerns:
            for concern in perspectives[0].concerns:
                if all(concern in p.concerns for p in perspectives[1:]):
                    common_elements.append(concern)

        # Add default common elements
        common_elements.extend([
            "Quality outcome",
            "Stakeholder satisfaction"
        ])

        return common_elements[:3]

    def _build_compromise_solution(
        self, common_elements: list[str], compromise_areas: list[str]
    ) -> str:
        """Build compromise solution from common elements"""
        return (
            f"Compromise solution incorporating {len(common_elements)} common elements "
            f"and {len(compromise_areas)} areas of compromise to achieve balanced outcome"
        )

    def _identify_unresolved_issues(
        self, perspectives: list[PersonaPerspective]
    ) -> list[str]:
        """Identify issues that remain unresolved"""
        unresolved = []

        # Find objections that weren't addressed
        all_objections = set()
        for p in perspectives:
            all_objections.update(p.objections)

        # Take first few objections as unresolved issues
        unresolved = list(all_objections)[:3]

        if not unresolved:
            unresolved = ["Resource allocation priorities", "Timeline constraints"]

        return unresolved[:5]

    def _identify_compromise_elements(
        self, perspectives: list[PersonaPerspective]
    ) -> list[str]:
        """Identify elements of compromise"""
        return [
            "Phased implementation approach",
            "Flexible timeline with milestones",
            "Balanced resource allocation"
        ][:3]
