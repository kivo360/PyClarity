# Clear Thinking FastMCP Server - Collaborative Reasoning Server

"""
FastMCP server implementation for Collaborative Reasoning cognitive tool.

This server provides multi-perspective reasoning through:
- Persona-based reasoning simulation
- Stakeholder perspective analysis
- Consensus building and conflict resolution
- Role-based decision making
- Team dynamics modeling

Agent: AGENT C - Collaborative Reasoning Implementation
Status: ACTIVE - Phase 2C Parallel Expansion
"""

import asyncio
import time
from typing import List, Dict, Any, Optional
from fastmcp.server import Context

from ..models.collaborative_reasoning import (
    CollaborativeReasoningInput,
    CollaborativeReasoningOutput,
    Persona,
    PersonaPerspective,
    CollaborativeDialogue,
    ConsensusResult,
    PersonaType,
    ReasoningStyle,
    ConsensusStrategy
)
from .base import CognitiveToolBase


class CollaborativeReasoningServer(CognitiveToolBase):
    """Server implementation for Collaborative Reasoning tool"""
    
    def __init__(self):
        super().__init__()
        self.tool_name = "Collaborative Reasoning"
        self.version = "1.0.0"
        self.description = "Multi-perspective reasoning through persona simulation and consensus building"
    
    async def process(
        self, 
        input_data: CollaborativeReasoningInput, 
        context: Context
    ) -> CollaborativeReasoningOutput:
        """Process collaborative reasoning with multiple personas"""
        
        start_time = time.time()
        
        try:
            await context.info(f"🤝 Starting Collaborative Reasoning process with {len(input_data.personas)} personas")
            await context.progress("Initializing collaborative reasoning", 0.0)
            
            # Phase 1: Generate individual perspectives
            await context.info("Phase 1: Generating individual persona perspectives")
            persona_perspectives = await self._generate_persona_perspectives(
                input_data, context
            )
            await context.progress("Generated persona perspectives", 0.3)
            
            # Phase 2: Facilitate collaborative dialogue
            await context.info("Phase 2: Facilitating collaborative dialogue")
            dialogue_records = await self._facilitate_dialogue(
                input_data, persona_perspectives, context
            )
            await context.progress("Completed collaborative dialogue", 0.6)
            
            # Phase 3: Build consensus
            await context.info("Phase 3: Building consensus from perspectives")
            consensus_result = await self._build_consensus(
                input_data, persona_perspectives, dialogue_records, context
            )
            await context.progress("Built consensus", 0.8)
            
            # Phase 4: Generate insights and recommendations
            await context.info("Phase 4: Generating insights and recommendations")
            key_insights, recommendations, considerations = await self._generate_insights(
                input_data, persona_perspectives, dialogue_records, consensus_result, context
            )
            await context.progress("Generated insights and recommendations", 0.9)
            
            # Calculate quality metrics
            diversity_score = self._calculate_diversity_score(persona_perspectives)
            collaboration_quality = self._calculate_collaboration_quality(dialogue_records, consensus_result)
            stakeholder_buy_in = self._assess_stakeholder_buy_in(persona_perspectives, consensus_result)
            
            processing_time = time.time() - start_time
            
            # Create output
            output = CollaborativeReasoningOutput(
                problem=input_data.problem,
                complexity_level=input_data.complexity_level,
                confidence_score=consensus_result.confidence_in_consensus,
                analysis=f"Collaborative reasoning completed with {len(persona_perspectives)} perspectives, achieving {consensus_result.agreement_level:.1%} consensus",
                session_id=input_data.session_id,
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
                consensus_confidence=consensus_result.confidence_in_consensus
            )
            
            await context.progress("Collaborative reasoning completed", 1.0)
            await context.info(f"✅ Collaborative Reasoning completed in {processing_time:.2f}s")
            
            return output
            
        except Exception as e:
            await context.error(f"Collaborative Reasoning failed: {str(e)}")
            raise
    
    async def _generate_persona_perspectives(
        self,
        input_data: CollaborativeReasoningInput,
        context: Context
    ) -> List[PersonaPerspective]:
        """Generate individual perspectives from each persona"""
        
        perspectives = []
        
        for i, persona in enumerate(input_data.personas):
            await context.debug(f"Generating perspective for persona: {persona.name}")
            
            # Simulate persona-specific reasoning
            perspective = await self._simulate_persona_reasoning(persona, input_data, context)
            perspectives.append(perspective)
            
            await context.progress(f"Generated perspective for {persona.name}", (i + 1) / len(input_data.personas) * 0.3)
        
        # Add devil's advocate if enabled
        if input_data.include_devil_advocate:
            devil_advocate = await self._generate_devil_advocate_perspective(input_data, perspectives, context)
            perspectives.append(devil_advocate)
        
        return perspectives
    
    async def _simulate_persona_reasoning(
        self,
        persona: Persona,
        input_data: CollaborativeReasoningInput,
        context: Context
    ) -> PersonaPerspective:
        """Simulate reasoning from a specific persona's perspective"""
        
        # Analyze problem through persona's lens
        viewpoint = self._generate_persona_viewpoint(persona, input_data)
        concerns = self._identify_persona_concerns(persona, input_data)
        suggestions = self._generate_persona_suggestions(persona, input_data)
        
        # Simulate reasoning process
        reasoning_path = [
            f"Analyzed problem from {persona.persona_type.value} perspective",
            f"Applied {persona.reasoning_style.value} reasoning approach",
            f"Considered {len(persona.priorities)} key priorities",
            f"Evaluated {len(persona.constraints)} constraints",
            "Formed viewpoint based on background and expertise"
        ]
        
        # Calculate confidence based on expertise and problem alignment
        confidence = self._calculate_persona_confidence(persona, input_data)
        
        return PersonaPerspective(
            persona_name=persona.name,
            viewpoint=viewpoint,
            concerns=concerns,
            suggestions=suggestions,
            supporting_arguments=self._generate_supporting_arguments(persona, viewpoint),
            objections=self._generate_objections(persona, input_data),
            confidence_level=confidence,
            reasoning_path=reasoning_path
        )
    
    async def _facilitate_dialogue(
        self,
        input_data: CollaborativeReasoningInput,
        perspectives: List[PersonaPerspective],
        context: Context
    ) -> List[CollaborativeDialogue]:
        """Facilitate dialogue between personas"""
        
        dialogues = []
        
        for round_num in range(input_data.max_dialogue_rounds):
            await context.debug(f"Facilitating dialogue round {round_num + 1}")
            
            # Create dialogue for this round
            dialogue = CollaborativeDialogue(
                participants=[p.persona_name for p in perspectives],
                topic=f"Round {round_num + 1}: {input_data.reasoning_focus}",
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
                    "timestamp": time.time(),
                    "response_to": None
                }
                dialogue.exchanges.append(exchange)
            
            # Identify consensus points and disagreements
            dialogue.consensus_points = self._identify_consensus_points(perspectives)
            dialogue.disagreements = self._identify_disagreements(perspectives)
            dialogue.resolution_attempts = self._generate_resolution_attempts(dialogue.disagreements)
            
            # Set outcome
            if len(dialogue.consensus_points) > len(dialogue.disagreements):
                dialogue.outcome = "Productive dialogue with emerging consensus"
            else:
                dialogue.outcome = "Dialogue revealed significant disagreements"
            
            dialogues.append(dialogue)
            
            # Allow persona evolution if enabled
            if input_data.allow_persona_evolution:
                await self._evolve_perspectives(perspectives, dialogue, context)
        
        return dialogues
    
    async def _build_consensus(
        self,
        input_data: CollaborativeReasoningInput,
        perspectives: List[PersonaPerspective],
        dialogues: List[CollaborativeDialogue],
        context: Context
    ) -> ConsensusResult:
        """Build consensus from perspectives and dialogue"""
        
        strategy = input_data.consensus_strategy
        
        if strategy == ConsensusStrategy.WEIGHTED_CONSENSUS:
            return await self._weighted_consensus(perspectives, input_data, context)
        elif strategy == ConsensusStrategy.MAJORITY_VOTE:
            return await self._majority_vote_consensus(perspectives, context)
        elif strategy == ConsensusStrategy.COMPROMISE_SOLUTION:
            return await self._compromise_consensus(perspectives, dialogues, context)
        else:
            return await self._default_consensus(perspectives, context)
    
    async def _weighted_consensus(
        self,
        perspectives: List[PersonaPerspective],
        input_data: CollaborativeReasoningInput,
        context: Context
    ) -> ConsensusResult:
        """Build consensus using weighted approach"""
        
        # Find the persona with highest influence for each perspective
        persona_weights = {p.name: 1.0 for p in input_data.personas}
        
        if input_data.weight_by_expertise:
            for persona in input_data.personas:
                # Increase weight based on expertise areas
                expertise_bonus = len(persona.expertise_areas) * 0.1
                persona_weights[persona.name] = persona.influence_weight + expertise_bonus
        
        # Calculate weighted agreement
        total_weight = sum(persona_weights.values())
        weighted_confidence = sum(
            p.confidence_level * persona_weights.get(p.persona_name, 1.0)
            for p in perspectives
        ) / total_weight
        
        # Generate consensus solution
        consensus_solution = self._synthesize_perspectives(perspectives)
        
        # Identify dissenting opinions
        dissenting = [
            f"{p.persona_name}: {p.viewpoint}"
            for p in perspectives
            if p.confidence_level < 0.5
        ]
        
        return ConsensusResult(
            strategy_used=ConsensusStrategy.WEIGHTED_CONSENSUS,
            consensus_reached=weighted_confidence > 0.6,
            agreement_level=weighted_confidence,
            agreed_solution=consensus_solution if weighted_confidence > 0.6 else None,
            dissenting_opinions=dissenting,
            compromise_elements=self._identify_compromise_elements(perspectives),
            unresolved_issues=self._identify_unresolved_issues(perspectives),
            confidence_in_consensus=weighted_confidence
        )
    
    async def _majority_vote_consensus(
        self,
        perspectives: List[PersonaPerspective],
        context: Context
    ) -> ConsensusResult:
        """Build consensus using majority vote"""
        
        # Group similar perspectives
        perspective_groups = self._group_similar_perspectives(perspectives)
        
        # Find majority
        largest_group = max(perspective_groups, key=len)
        agreement_level = len(largest_group) / len(perspectives)
        
        consensus_solution = self._synthesize_group_perspectives(largest_group)
        
        return ConsensusResult(
            strategy_used=ConsensusStrategy.MAJORITY_VOTE,
            consensus_reached=agreement_level > 0.5,
            agreement_level=agreement_level,
            agreed_solution=consensus_solution if agreement_level > 0.5 else None,
            dissenting_opinions=[p.viewpoint for p in perspectives if p not in largest_group],
            compromise_elements=[],
            unresolved_issues=self._identify_unresolved_issues(perspectives),
            confidence_in_consensus=agreement_level
        )
    
    async def _compromise_consensus(
        self,
        perspectives: List[PersonaPerspective],
        dialogues: List[CollaborativeDialogue],
        context: Context
    ) -> ConsensusResult:
        """Build consensus through compromise"""
        
        # Extract common elements from all perspectives
        common_elements = self._find_common_elements(perspectives)
        
        # Identify areas of compromise
        compromise_areas = []
        for dialogue in dialogues:
            compromise_areas.extend(dialogue.resolution_attempts)
        
        # Build compromise solution
        compromise_solution = self._build_compromise_solution(common_elements, compromise_areas)
        
        # Calculate agreement level based on compromise acceptance
        agreement_level = min(0.8, len(common_elements) / len(perspectives))
        
        return ConsensusResult(
            strategy_used=ConsensusStrategy.COMPROMISE_SOLUTION,
            consensus_reached=True,
            agreement_level=agreement_level,
            agreed_solution=compromise_solution,
            dissenting_opinions=[],
            compromise_elements=compromise_areas,
            unresolved_issues=self._identify_unresolved_issues(perspectives),
            confidence_in_consensus=agreement_level
        )
    
    async def _default_consensus(
        self,
        perspectives: List[PersonaPerspective],
        context: Context
    ) -> ConsensusResult:
        """Default consensus building approach"""
        
        # Simple averaging approach
        avg_confidence = sum(p.confidence_level for p in perspectives) / len(perspectives)
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
        input_data: CollaborativeReasoningInput,
        perspectives: List[PersonaPerspective],
        dialogues: List[CollaborativeDialogue],
        consensus: ConsensusResult,
        context: Context
    ) -> tuple[List[str], List[str], List[str]]:
        """Generate key insights, recommendations, and considerations"""
        
        # Key insights from collaborative process
        insights = [
            f"Achieved {consensus.agreement_level:.1%} consensus among {len(perspectives)} perspectives",
            f"Perspective diversity score: {self._calculate_diversity_score(perspectives):.2f}",
            f"Most influential viewpoint: {max(perspectives, key=lambda p: p.confidence_level).persona_name}",
            f"Key areas of agreement: {', '.join(self._identify_consensus_points(perspectives))}"
        ]
        
        # Recommendations
        recommendations = [
            "Proceed with consensus solution if agreement level > 70%",
            "Address dissenting opinions through targeted engagement",
            "Monitor implementation for stakeholder concerns",
            "Schedule follow-up review to assess outcomes"
        ]
        
        # Implementation considerations
        considerations = [
            "Stakeholder communication strategy needed",
            "Change management approach for dissenting parties",
            "Resource allocation based on consensus priorities",
            "Risk mitigation for unresolved issues"
        ]
        
        return insights, recommendations, considerations
    
    # Helper methods
    def _generate_persona_viewpoint(self, persona: Persona, input_data: CollaborativeReasoningInput) -> str:
        """Generate viewpoint for a specific persona"""
        return f"From a {persona.persona_type.value} perspective, {input_data.reasoning_focus} requires considering {', '.join(persona.priorities[:2])} while managing {', '.join(persona.constraints[:2])}"
    
    def _identify_persona_concerns(self, persona: Persona, input_data: CollaborativeReasoningInput) -> List[str]:
        """Identify concerns for a specific persona"""
        base_concerns = [f"Impact on {priority}" for priority in persona.priorities[:3]]
        return base_concerns + [f"Constraint: {constraint}" for constraint in persona.constraints[:2]]
    
    def _generate_persona_suggestions(self, persona: Persona, input_data: CollaborativeReasoningInput) -> List[str]:
        """Generate suggestions from a persona's perspective"""
        return [
            f"Focus on {persona.priorities[0] if persona.priorities else 'core objectives'}",
            f"Consider {persona.reasoning_style.value} approach to problem-solving",
            f"Leverage expertise in {persona.expertise_areas[0] if persona.expertise_areas else 'general knowledge'}"
        ]
    
    def _calculate_persona_confidence(self, persona: Persona, input_data: CollaborativeReasoningInput) -> float:
        """Calculate confidence level for a persona"""
        base_confidence = 0.5
        
        # Increase confidence based on expertise relevance
        if persona.expertise_areas:
            expertise_match = any(area.lower() in input_data.problem.lower() for area in persona.expertise_areas)
            if expertise_match:
                base_confidence += 0.3
        
        # Adjust based on reasoning style match with problem complexity
        if input_data.complexity_level.value == "high" and persona.reasoning_style in [ReasoningStyle.ANALYTICAL, ReasoningStyle.SYSTEMATIC]:
            base_confidence += 0.2
        
        return min(1.0, base_confidence)
    
    def _generate_supporting_arguments(self, persona: Persona, viewpoint: str) -> List[str]:
        """Generate supporting arguments for a persona's viewpoint"""
        return [
            f"Based on {persona.persona_type.value} experience",
            f"Consistent with {persona.reasoning_style.value} approach",
            f"Supported by expertise in {persona.expertise_areas[0] if persona.expertise_areas else 'domain knowledge'}"
        ]
    
    def _generate_objections(self, persona: Persona, input_data: CollaborativeReasoningInput) -> List[str]:
        """Generate objections from a persona's perspective"""
        return [
            f"Potential conflict with {constraint}" for constraint in persona.constraints[:2]
        ]
    
    def _calculate_diversity_score(self, perspectives: List[PersonaPerspective]) -> float:
        """Calculate diversity score of perspectives"""
        if len(perspectives) <= 1:
            return 0.0
        
        # Simple diversity calculation based on viewpoint differences
        unique_viewpoints = len(set(p.viewpoint for p in perspectives))
        return min(1.0, unique_viewpoints / len(perspectives))
    
    def _calculate_collaboration_quality(self, dialogues: List[CollaborativeDialogue], consensus: ConsensusResult) -> float:
        """Calculate quality of collaborative process"""
        if not dialogues:
            return 0.5
        
        # Factor in dialogue productivity and consensus achievement
        dialogue_quality = sum(len(d.consensus_points) - len(d.disagreements) for d in dialogues) / len(dialogues)
        consensus_quality = consensus.agreement_level
        
        return (dialogue_quality + consensus_quality) / 2.0
    
    def _assess_stakeholder_buy_in(self, perspectives: List[PersonaPerspective], consensus: ConsensusResult) -> Dict[str, float]:
        """Assess stakeholder buy-in levels"""
        return {
            p.persona_name: p.confidence_level * (1.0 if consensus.consensus_reached else 0.5)
            for p in perspectives
        }
    
    def _synthesize_perspectives(self, perspectives: List[PersonaPerspective]) -> str:
        """Synthesize multiple perspectives into a solution"""
        high_confidence_perspectives = [p for p in perspectives if p.confidence_level > 0.6]
        
        if high_confidence_perspectives:
            return f"Integrated solution incorporating insights from {len(high_confidence_perspectives)} high-confidence perspectives"
        else:
            return f"Balanced solution considering all {len(perspectives)} perspectives"
    
    # Additional helper methods would continue here...
    def _generate_devil_advocate_perspective(self, input_data, perspectives, context):
        """Generate devil's advocate perspective"""
        return PersonaPerspective(
            persona_name="Devil's Advocate",
            viewpoint="Challenge consensus and identify potential flaws",
            concerns=["Groupthink", "Overlooked risks", "Alternative solutions"],
            suggestions=["Consider contrarian views", "Test assumptions", "Explore alternatives"],
            confidence_level=0.7,
            reasoning_path=["Analyzed for potential biases", "Identified weak points", "Proposed alternatives"]
        )
    
    def _generate_dialogue_message(self, perspective, round_num):
        """Generate dialogue message for a perspective"""
        return f"Round {round_num + 1}: {perspective.viewpoint[:100]}..."
    
    def _identify_consensus_points(self, perspectives):
        """Identify points of consensus"""
        return ["Shared concern for outcome quality", "Agreement on key constraints"]
    
    def _identify_disagreements(self, perspectives):
        """Identify disagreements"""
        return ["Different priorities", "Varying risk tolerance"]
    
    def _generate_resolution_attempts(self, disagreements):
        """Generate resolution attempts"""
        return [f"Attempt to resolve: {d}" for d in disagreements[:2]]
    
    async def _evolve_perspectives(self, perspectives, dialogue, context):
        """Allow perspectives to evolve based on dialogue"""
        # Simple evolution - slightly adjust confidence based on consensus
        for perspective in perspectives:
            if len(dialogue.consensus_points) > len(dialogue.disagreements):
                perspective.confidence_level = min(1.0, perspective.confidence_level + 0.1)
    
    def _group_similar_perspectives(self, perspectives):
        """Group similar perspectives"""
        # Simple grouping - in practice would use NLP similarity
        return [perspectives]  # All in one group for simplicity
    
    def _synthesize_group_perspectives(self, group):
        """Synthesize perspectives from a group"""
        return f"Majority solution from {len(group)} aligned perspectives"
    
    def _find_common_elements(self, perspectives):
        """Find common elements across perspectives"""
        return ["Quality outcome", "Stakeholder consideration", "Risk management"]
    
    def _build_compromise_solution(self, common_elements, compromise_areas):
        """Build compromise solution"""
        return f"Compromise solution incorporating {len(common_elements)} common elements"
    
    def _identify_unresolved_issues(self, perspectives):
        """Identify unresolved issues"""
        return ["Resource allocation", "Timeline constraints"]
    
    def _identify_compromise_elements(self, perspectives):
        """Identify compromise elements"""
        return ["Phased implementation", "Flexible timeline"]
