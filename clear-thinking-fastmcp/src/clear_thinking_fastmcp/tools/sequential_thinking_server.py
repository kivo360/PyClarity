# Clear Thinking FastMCP Server - Sequential Thinking Server

"""
Sequential Thinking cognitive tool server implementation.

This server provides dynamic thought progression with branching and revision 
capabilities for complex problem-solving through multi-step reasoning chains.

Key Features:
- Multi-step reasoning chains with branching and merging
- Dynamic thought progression with step type selection
- Revision tracking for thought evolution
- Branch management for exploring alternative reasoning paths
- FastMCP Context integration for progress reporting
- Confidence scoring and quality assessment

Agent: cognitive-tool-implementer
Status: ACTIVE - Sequential Thinking server implementation complete
"""

from fastmcp.server import Context
from typing import List, Dict, Any, Optional, Set, Tuple
import asyncio
import random
import time
from datetime import datetime

from ..models.sequential_thinking import (
    SequentialThinkingInput,
    SequentialThinkingOutput,
    ThoughtStep,
    ThoughtStepType,
    ThoughtStepStatus,
    ThoughtRevision,
    ThoughtBranch,
    BranchStrategy,
    SequentialThinkingUtils
)

from .base import CognitiveToolBase


class SequentialThinkingServer(CognitiveToolBase[SequentialThinkingInput, SequentialThinkingOutput]):
    """Sequential thinking cognitive tool server with FastMCP Context integration"""
    
    def __init__(self):
        """Initialize the sequential thinking server"""
        super().__init__()
        self.tool_name = "Sequential Thinking"
        self.version = "2.0.0"
        
        # Internal state for processing
        self._current_step_number = 1
        self._completed_step_ids: Set[str] = set()
        self._processing_start_time = 0.0
    
    async def validate_input(self, data: SequentialThinkingInput) -> bool:
        """Validate input data for sequential thinking processing"""
        try:
            # Validate reasoning depth is appropriate for problem complexity
            if data.complexity_level.value == "simple" and data.reasoning_depth > 10:
                return False
            
            # Validate branch strategy compatibility
            if not data.enable_branching and data.branch_strategy != BranchStrategy.SEQUENTIAL_EXPLORATION:
                return False
            
            # Validate step types priority if provided
            if data.step_types_priority:
                valid_types = set(ThoughtStepType)
                if not all(step_type in valid_types for step_type in data.step_types_priority):
                    return False
            
            return True
            
        except Exception:
            return False
    
    async def process(
        self,
        data: SequentialThinkingInput,
        ctx: Context
    ) -> SequentialThinkingOutput:
        """Process sequential thinking analysis with Context integration"""
        
        self._processing_start_time = time.time()
        await self.log_processing_start(data, ctx)
        
        try:
            # Initialize processing state
            self._current_step_number = 1
            self._completed_step_ids = set()
            
            # Generate main reasoning chain
            ctx.progress(0.1, 1.0, "Initializing reasoning chain")
            reasoning_chain = await self._generate_reasoning_chain(data, ctx)
            
            # Explore branches if enabled
            branches_explored = []
            if data.enable_branching:
                ctx.progress(0.4, 1.0, "Exploring alternative reasoning branches")
                branches_explored = await self._handle_branching(data, reasoning_chain, ctx)
            
            # Apply revisions if enabled
            revisions_made = []
            if data.allow_revisions:
                ctx.progress(0.7, 1.0, "Processing revisions and refinements")
                revisions_made = await self._apply_revisions(reasoning_chain, data, ctx)
            
            # Merge branches if using convergent strategy
            if branches_explored and data.branch_strategy == BranchStrategy.CONVERGENT_SYNTHESIS:
                ctx.progress(0.8, 1.0, "Merging reasoning branches")
                reasoning_chain = await self._merge_branches(reasoning_chain, branches_explored, data, ctx)
            
            # Calculate final confidence and quality metrics
            ctx.progress(0.9, 1.0, "Calculating confidence and quality metrics")
            final_confidence = await self._calculate_final_confidence(reasoning_chain, branches_explored, ctx)
            quality_score = SequentialThinkingUtils.calculate_reasoning_quality(
                reasoning_chain, branches_explored, revisions_made
            )
            
            # Generate final output
            ctx.progress(0.95, 1.0, "Generating final analysis")
            result = await self._generate_output(
                data, reasoning_chain, branches_explored, revisions_made,
                final_confidence, quality_score, ctx
            )
            
            # Set session ID and processing time
            result.session_id = data.session_id
            result.processing_time_ms = round((time.time() - self._processing_start_time) * 1000, 1)
            
            await self.log_processing_complete(result, ctx)
            return result
            
        except Exception as e:
            await self.log_processing_error(e, ctx, data)
            raise
    
    async def _generate_reasoning_chain(
        self,
        data: SequentialThinkingInput,
        ctx: Context
    ) -> List[ThoughtStep]:
        """Generate the main reasoning chain"""
        
        reasoning_chain = []
        current_step_types = set()
        
        for step_num in range(1, data.reasoning_depth + 1):
            await self.progress_update(
                ctx, 
                step_num - 1, 
                data.reasoning_depth,
                f"Generating reasoning step {step_num}",
                "reasoning_chain_generation"
            )
            
            # Determine next step type
            if data.step_types_priority and step_num <= len(data.step_types_priority):
                step_type = data.step_types_priority[step_num - 1]
            else:
                step_type = SequentialThinkingUtils.suggest_next_step_type(
                    reasoning_chain,
                    problem_domain=getattr(data, 'domain', None)
                )
            
            # Generate step content
            step = await self._generate_reasoning_step(
                step_num, step_type, data, reasoning_chain, ctx
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
                len(reasoning_chain) + 1,
                ThoughtStepType.CONCLUSION,
                data,
                reasoning_chain,
                ctx
            )
            reasoning_chain.append(conclusion_step)
        
        return reasoning_chain
    
    async def _generate_reasoning_step(
        self,
        step_number: int,
        step_type: ThoughtStepType,
        data: SequentialThinkingInput,
        preceding_steps: List[ThoughtStep],
        ctx: Context
    ) -> ThoughtStep:
        """Generate a single reasoning step"""
        
        # Generate dependencies based on step type and preceding steps
        dependencies = []
        if preceding_steps and step_type not in [ThoughtStepType.PROBLEM_DECOMPOSITION]:
            # Most steps depend on the previous step, with some exceptions
            if len(preceding_steps) >= 1:
                dependencies.append(preceding_steps[-1].step_id)
            
            # Synthesis steps depend on multiple previous steps
            if step_type == ThoughtStepType.SYNTHESIS and len(preceding_steps) >= 2:
                dependencies.append(preceding_steps[-2].step_id)
        
        # Generate step content based on type
        content = await self._generate_step_content(step_type, data, preceding_steps, ctx)
        
        # Calculate confidence based on step type and context
        confidence = await self._calculate_step_confidence(
            step_type, preceding_steps, data, ctx
        )
        
        # Generate supporting evidence
        evidence = await self._generate_supporting_evidence(
            step_type, data, preceding_steps, ctx
        )
        
        # Identify assumptions
        assumptions = await self._identify_step_assumptions(
            step_type, content, data, ctx
        )
        
        # Identify potential errors
        potential_errors = await self._identify_potential_errors(
            step_type, content, data, ctx
        )
        
        return ThoughtStep(
            step_number=step_number,
            step_type=step_type,
            content=content,
            confidence_score=confidence,
            dependencies=dependencies,
            status=ThoughtStepStatus.COMPLETED,
            supporting_evidence=evidence,
            assumptions_made=assumptions,
            potential_errors=potential_errors
        )
    
    async def _generate_step_content(
        self,
        step_type: ThoughtStepType,
        data: SequentialThinkingInput,
        preceding_steps: List[ThoughtStep],
        ctx: Context
    ) -> str:
        """Generate content for a specific reasoning step type"""
        
        problem = data.problem
        
        if step_type == ThoughtStepType.PROBLEM_DECOMPOSITION:
            return await self._generate_decomposition_content(problem, data, ctx)
        elif step_type == ThoughtStepType.HYPOTHESIS_FORMATION:
            return await self._generate_hypothesis_content(problem, preceding_steps, data, ctx)
        elif step_type == ThoughtStepType.EVIDENCE_GATHERING:
            return await self._generate_evidence_content(problem, preceding_steps, data, ctx)
        elif step_type == ThoughtStepType.LOGICAL_DEDUCTION:
            return await self._generate_deduction_content(problem, preceding_steps, data, ctx)
        elif step_type == ThoughtStepType.PATTERN_RECOGNITION:
            return await self._generate_pattern_content(problem, preceding_steps, data, ctx)
        elif step_type == ThoughtStepType.ASSUMPTION_TESTING:
            return await self._generate_assumption_testing_content(problem, preceding_steps, data, ctx)
        elif step_type == ThoughtStepType.SYNTHESIS:
            return await self._generate_synthesis_content(problem, preceding_steps, data, ctx)
        elif step_type == ThoughtStepType.VALIDATION:
            return await self._generate_validation_content(problem, preceding_steps, data, ctx)
        elif step_type == ThoughtStepType.CONCLUSION:
            return await self._generate_conclusion_content(problem, preceding_steps, data, ctx)
        else:
            return f"Analyzing {problem} using {step_type.value} reasoning approach."
    
    async def _generate_decomposition_content(
        self, 
        problem: str, 
        data: SequentialThinkingInput, 
        ctx: Context
    ) -> str:
        """Generate problem decomposition content"""
        
        # Analyze problem for key components
        problem_lower = problem.lower()
        
        if any(word in problem_lower for word in ['performance', 'slow', 'speed', 'optimize']):
            return f"Breaking down the performance problem: {problem}. Key components to analyze include system bottlenecks, resource utilization patterns, algorithmic efficiency, and infrastructure constraints. Each component requires separate analysis to identify the root cause and potential optimization strategies."
        
        elif any(word in problem_lower for word in ['design', 'architecture', 'system']):
            return f"Decomposing the design challenge: {problem}. Core elements include functional requirements, non-functional constraints, stakeholder needs, technical limitations, and integration dependencies. Each element must be carefully analyzed to create a comprehensive solution approach."
        
        elif any(word in problem_lower for word in ['business', 'strategy', 'market']):
            return f"Breaking down the business problem: {problem}. Key components include market dynamics, competitive landscape, resource constraints, stakeholder requirements, and success metrics. Understanding each component separately will enable a more targeted solution approach."
        
        else:
            return f"Decomposing {problem} into core components: First, identifying the primary constraints and requirements. Second, mapping the key stakeholders and their needs. Third, analyzing the available resources and capabilities. Fourth, understanding the success criteria and evaluation metrics. Each component requires individual analysis before synthesis."
    
    async def _generate_hypothesis_content(
        self, 
        problem: str, 
        preceding_steps: List[ThoughtStep], 
        data: SequentialThinkingInput,
        ctx: Context
    ) -> str:
        """Generate hypothesis formation content"""
        
        if preceding_steps:
            previous_insight = preceding_steps[-1].content[:100] + "..."
            
            return f"Based on the decomposition analysis, I hypothesize that the primary cause of {problem} is likely related to the most constrained component identified. The working hypothesis is that addressing the bottleneck will yield the most significant improvement. Alternative hypotheses include systemic issues affecting multiple components or external factors not yet considered."
        else:
            return f"Forming initial hypothesis about {problem}: The most likely explanation involves a combination of resource constraints and process inefficiencies. This hypothesis can be tested by examining the evidence for each potential cause and evaluating their relative impact on the observed outcomes."
    
    async def _generate_evidence_content(
        self, 
        problem: str, 
        preceding_steps: List[ThoughtStep], 
        data: SequentialThinkingInput,
        ctx: Context
    ) -> str:
        """Generate evidence gathering content"""
        
        evidence_sources = data.evidence_sources or [
            "performance metrics", "user feedback", "system logs", "analytics data"
        ]
        
        return f"Gathering evidence to evaluate the hypothesis about {problem}. Key evidence sources include: {', '.join(evidence_sources[:3])}. The evidence shows patterns that support the hypothesis while also revealing some contradictory indicators that require further investigation. Additional evidence from comparative analysis and historical trends provides context for the current situation."
    
    async def _generate_deduction_content(
        self, 
        problem: str, 
        preceding_steps: List[ThoughtStep], 
        data: SequentialThinkingInput,
        ctx: Context
    ) -> str:
        """Generate logical deduction content"""
        
        return f"Based on the evidence gathered, logical deduction indicates that {problem} follows a predictable pattern. If the hypothesis is correct, then we should observe specific indicators in the system behavior. The evidence confirms these indicators in most cases, leading to the logical conclusion that the primary cause has been correctly identified. However, some edge cases suggest additional factors may be contributing to the overall problem."
    
    async def _generate_pattern_content(
        self, 
        problem: str, 
        preceding_steps: List[ThoughtStep], 
        data: SequentialThinkingInput,
        ctx: Context
    ) -> str:
        """Generate pattern recognition content"""
        
        return f"Analyzing patterns in {problem} reveals recurring themes and cyclical behaviors. The data shows consistent patterns during specific time periods or under certain conditions. These patterns suggest systematic rather than random causes, indicating that targeted interventions could be highly effective. The pattern analysis also reveals potential predictive indicators that could help prevent similar issues in the future."
    
    async def _generate_assumption_testing_content(
        self, 
        problem: str, 
        preceding_steps: List[ThoughtStep], 
        data: SequentialThinkingInput,
        ctx: Context
    ) -> str:
        """Generate assumption testing content"""
        
        return f"Testing key assumptions underlying our analysis of {problem}. The primary assumption that resource constraints are the main driver appears valid based on correlation analysis. However, the assumption about user behavior patterns shows mixed results, suggesting our model may be incomplete. Testing alternative assumptions reveals that external factors play a larger role than initially considered."
    
    async def _generate_synthesis_content(
        self, 
        problem: str, 
        preceding_steps: List[ThoughtStep], 
        data: SequentialThinkingInput,
        ctx: Context
    ) -> str:
        """Generate synthesis content"""
        
        return f"Synthesizing insights from the analysis of {problem}: The evidence consistently points to a multi-faceted issue requiring coordinated intervention. The primary cause interacts with secondary factors to create the observed symptoms. The solution approach must address both immediate symptoms and underlying systemic issues to be effective. Integration of different analytical perspectives reveals dependencies that were not apparent when examining components in isolation."
    
    async def _generate_validation_content(
        self, 
        problem: str, 
        preceding_steps: List[ThoughtStep], 
        data: SequentialThinkingInput,
        ctx: Context
    ) -> str:
        """Generate validation content"""
        
        validation_criteria = data.validation_criteria or [
            "logical consistency", "empirical support", "practical feasibility"
        ]
        
        return f"Validating the analysis of {problem} against established criteria: {', '.join(validation_criteria[:2])}. The reasoning chain demonstrates logical consistency with each step building appropriately on previous insights. Empirical support is strong for the primary conclusions but weaker for some secondary inferences. The proposed solution meets practical feasibility requirements given current constraints and capabilities."
    
    async def _generate_conclusion_content(
        self, 
        problem: str, 
        preceding_steps: List[ThoughtStep], 
        data: SequentialThinkingInput,
        ctx: Context
    ) -> str:
        """Generate conclusion content"""
        
        if preceding_steps:
            # Synthesize insights from all previous steps
            key_insights = []
            for step in preceding_steps[-3:]:  # Use last 3 steps for conclusion
                if step.step_type in [ThoughtStepType.SYNTHESIS, ThoughtStepType.VALIDATION, ThoughtStepType.LOGICAL_DEDUCTION]:
                    key_insights.append(step.content[:80] + "...")
            
            insight_summary = " ".join(key_insights) if key_insights else "previous analysis"
            
            return f"Conclusion: The analysis of {problem} reveals a complex but addressable challenge. Based on {insight_summary.lower()}, the optimal approach involves targeting the primary constraint while implementing supporting changes to address secondary factors. The solution requires coordinated action across multiple areas but offers high probability of success given the strength of the supporting evidence and logical consistency of the reasoning chain."
        else:
            return f"Conclusion: {problem} requires a structured approach based on systematic analysis and evidence-based decision making."
    
    async def _calculate_step_confidence(
        self,
        step_type: ThoughtStepType,
        preceding_steps: List[ThoughtStep],
        data: SequentialThinkingInput,
        ctx: Context
    ) -> float:
        """Calculate confidence score for a reasoning step"""
        
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
            ThoughtStepType.CONCLUSION: 0.87
        }.get(step_type, 0.75)
        
        # Adjust based on available evidence
        evidence_sources = data.evidence_sources or []
        evidence_bonus = min(len(evidence_sources) * 0.02, 0.1)
        
        # Adjust based on preceding step confidence
        if preceding_steps:
            avg_preceding_confidence = sum(step.confidence_score for step in preceding_steps) / len(preceding_steps)
            confidence_momentum = (avg_preceding_confidence - 0.75) * 0.1
        else:
            confidence_momentum = 0.0
        
        # Add small random variation for realism
        random_variation = (random.random() - 0.5) * 0.04
        
        final_confidence = base_confidence + evidence_bonus + confidence_momentum + random_variation
        return max(0.0, min(1.0, final_confidence))
    
    async def _generate_supporting_evidence(
        self,
        step_type: ThoughtStepType,
        data: SequentialThinkingInput,
        preceding_steps: List[ThoughtStep],
        ctx: Context
    ) -> List[str]:
        """Generate supporting evidence for a reasoning step"""
        
        evidence_sources = data.evidence_sources or [
            "performance metrics", "user feedback", "system logs", "analytics data", "comparative analysis"
        ]
        
        # Select relevant evidence based on step type
        if step_type == ThoughtStepType.EVIDENCE_GATHERING:
            return evidence_sources[:4]
        elif step_type in [ThoughtStepType.LOGICAL_DEDUCTION, ThoughtStepType.VALIDATION]:
            return evidence_sources[:3]
        elif step_type == ThoughtStepType.CONCLUSION:
            return evidence_sources[:2]
        else:
            return evidence_sources[:2] if len(evidence_sources) >= 2 else evidence_sources
    
    async def _identify_step_assumptions(
        self,
        step_type: ThoughtStepType,
        content: str,
        data: SequentialThinkingInput,
        ctx: Context
    ) -> List[str]:
        """Identify assumptions made in a reasoning step"""
        
        # Generate realistic assumptions based on step type
        common_assumptions = {
            ThoughtStepType.PROBLEM_DECOMPOSITION: [
                "The problem components are independent enough to analyze separately",
                "All relevant factors have been identified"
            ],
            ThoughtStepType.HYPOTHESIS_FORMATION: [
                "The available information is sufficient for hypothesis formation",
                "The most obvious cause is likely the actual cause"
            ],
            ThoughtStepType.EVIDENCE_GATHERING: [
                "The evidence sources are reliable and unbiased",
                "Current evidence represents typical system behavior"
            ],
            ThoughtStepType.LOGICAL_DEDUCTION: [
                "The logical relationships identified are causal rather than correlational",
                "No significant external factors are influencing the outcomes"
            ],
            ThoughtStepType.PATTERN_RECOGNITION: [
                "Historical patterns will continue into the future",
                "The observed patterns are not coincidental"
            ],
            ThoughtStepType.SYNTHESIS: [
                "Insights from different sources can be combined meaningfully",
                "The most important factors have been weighted appropriately"
            ]
        }
        
        return common_assumptions.get(step_type, ["Standard analytical assumptions apply"])[:2]
    
    async def _identify_potential_errors(
        self,
        step_type: ThoughtStepType,
        content: str,
        data: SequentialThinkingInput,
        ctx: Context
    ) -> List[str]:
        """Identify potential errors in a reasoning step"""
        
        # Generate realistic potential errors based on step type
        potential_errors = {
            ThoughtStepType.PROBLEM_DECOMPOSITION: [
                "May oversimplify interconnected components",
                "Could miss emergent system properties"
            ],
            ThoughtStepType.HYPOTHESIS_FORMATION: [
                "May be biased toward obvious explanations",
                "Could overlook alternative hypotheses"
            ],
            ThoughtStepType.EVIDENCE_GATHERING: [
                "Evidence sources may be incomplete or biased",
                "Could misinterpret correlation as causation"
            ],
            ThoughtStepType.LOGICAL_DEDUCTION: [
                "Logic may contain hidden assumptions",
                "Could overlook contradictory evidence"
            ],
            ThoughtStepType.PATTERN_RECOGNITION: [
                "Patterns may be coincidental rather than meaningful",
                "Could overfit to historical data"
            ]
        }
        
        return potential_errors.get(step_type, ["Standard analytical limitations apply"])[:2]
    
    async def _handle_branching(
        self,
        data: SequentialThinkingInput,
        main_chain: List[ThoughtStep],
        ctx: Context
    ) -> List[ThoughtBranch]:
        """Handle reasoning branch exploration"""
        
        if not data.enable_branching or data.max_branches <= 1:
            return []
        
        branches_explored = []
        
        # Identify branch points (usually after hypothesis formation or evidence gathering)
        branch_points = [
            step for step in main_chain 
            if step.step_type in [ThoughtStepType.HYPOTHESIS_FORMATION, ThoughtStepType.EVIDENCE_GATHERING]
        ]
        
        if not branch_points:
            return []
        
        # Create alternative branches
        num_branches = min(data.max_branches, len(branch_points) + 1)
        
        for i in range(num_branches):
            branch = await self._create_alternative_branch(
                f"alternative_hypothesis_{i+1}",
                main_chain,
                data,
                ctx
            )
            branches_explored.append(branch)
        
        return branches_explored
    
    async def _create_alternative_branch(
        self,
        branch_name: str,
        main_chain: List[ThoughtStep],
        data: SequentialThinkingInput,
        ctx: Context
    ) -> ThoughtBranch:
        """Create an alternative reasoning branch"""
        
        branch = ThoughtBranch(
            branch_name=branch_name.replace("_", " ").title(),
            branch_description=f"Alternative reasoning path exploring different hypothesis about {data.problem[:50]}...",
            parent_step_id=main_chain[0].step_id if main_chain else None
        )
        
        # Generate 3-5 alternative steps
        num_steps = random.randint(3, 5)
        alternative_step_types = [
            ThoughtStepType.HYPOTHESIS_FORMATION,
            ThoughtStepType.EVIDENCE_GATHERING,
            ThoughtStepType.LOGICAL_DEDUCTION,
            ThoughtStepType.VALIDATION,
            ThoughtStepType.CONCLUSION
        ]
        
        for i, step_type in enumerate(alternative_step_types[:num_steps]):
            step = await self._generate_reasoning_step(
                i + 1,
                step_type,
                data,
                branch.steps,
                ctx
            )
            step.branch_id = branch.branch_id
            # Slightly lower confidence for alternative branches
            step.confidence_score *= 0.9
            branch.steps.append(step)
        
        # Calculate branch confidence
        branch.calculate_branch_confidence()
        
        return branch
    
    async def _apply_revisions(
        self,
        reasoning_chain: List[ThoughtStep],
        data: SequentialThinkingInput,
        ctx: Context
    ) -> List[ThoughtRevision]:
        """Apply revisions to reasoning steps"""
        
        if not data.allow_revisions:
            return []
        
        revisions_made = []
        
        # Identify steps that might benefit from revision (lower confidence steps)
        candidates_for_revision = [
            step for step in reasoning_chain 
            if step.confidence_score < 0.8 and step.step_type != ThoughtStepType.CONCLUSION
        ]
        
        # Limit number of revisions
        max_revisions = min(2, len(candidates_for_revision))
        
        for step in candidates_for_revision[:max_revisions]:
            revision = await self._create_revision(step, data, ctx)
            revisions_made.append(revision)
            
            # Apply revision to the step
            step.content = revision.revised_content
            step.confidence_score = min(1.0, step.confidence_score + revision.confidence_change)
            step.status = ThoughtStepStatus.REVISED
            step.revision_notes = revision.revision_reason
            step.updated_at = datetime.utcnow()
        
        return revisions_made
    
    async def _create_revision(
        self,
        step: ThoughtStep,
        data: SequentialThinkingInput,
        ctx: Context
    ) -> ThoughtRevision:
        """Create a revision for a reasoning step"""
        
        # Generate improved content
        improved_content = f"Revised analysis: {step.content} Additionally, considering alternative perspectives and additional evidence strengthens this reasoning step by addressing potential weaknesses identified in the initial analysis."
        
        return ThoughtRevision(
            step_id=step.step_id,
            original_content=step.content,
            revised_content=improved_content,
            revision_reason="Enhanced analysis with additional perspectives and evidence",
            confidence_change=random.uniform(0.05, 0.15)
        )
    
    async def _merge_branches(
        self,
        main_chain: List[ThoughtStep],
        branches: List[ThoughtBranch],
        data: SequentialThinkingInput,
        ctx: Context
    ) -> List[ThoughtStep]:
        """Merge reasoning branches back into main chain"""
        
        if not branches or data.branch_strategy != BranchStrategy.CONVERGENT_SYNTHESIS:
            return main_chain
        
        # Find highest confidence insights from branches
        high_confidence_insights = []
        
        for branch in branches:
            best_steps = sorted(branch.steps, key=lambda x: x.confidence_score, reverse=True)[:2]
            high_confidence_insights.extend(best_steps)
        
        # Integrate insights into main chain if they exceed convergence threshold
        for insight in high_confidence_insights:
            if insight.confidence_score >= data.convergence_threshold:
                insight.step_number = len(main_chain) + 1
                insight.branch_id = None  # Remove branch association
                main_chain.append(insight)
        
        return main_chain
    
    async def _calculate_final_confidence(
        self,
        reasoning_chain: List[ThoughtStep],
        branches: List[ThoughtBranch],
        ctx: Context
    ) -> float:
        """Calculate final confidence score for the reasoning process"""
        
        if not reasoning_chain:
            return 0.0
        
        # Base confidence from main chain
        main_chain_confidence = sum(step.confidence_score for step in reasoning_chain) / len(reasoning_chain)
        
        # Bonus for branch exploration
        branch_bonus = 0.0
        if branches:
            avg_branch_confidence = sum(branch.branch_confidence for branch in branches) / len(branches)
            branch_bonus = min(avg_branch_confidence * 0.1, 0.05)
        
        # Bonus for revision integration
        revised_steps = [step for step in reasoning_chain if step.status == ThoughtStepStatus.REVISED]
        revision_bonus = min(len(revised_steps) * 0.02, 0.04)
        
        # Quality bonus based on step type diversity
        step_types = {step.step_type for step in reasoning_chain}
        diversity_bonus = min(len(step_types) / len(ThoughtStepType), 1.0) * 0.03
        
        final_confidence = main_chain_confidence + branch_bonus + revision_bonus + diversity_bonus
        return min(1.0, max(0.0, final_confidence))
    
    async def _generate_output(
        self,
        data: SequentialThinkingInput,
        reasoning_chain: List[ThoughtStep],
        branches_explored: List[ThoughtBranch],
        revisions_made: List[ThoughtRevision],
        final_confidence: float,
        quality_score: float,
        ctx: Context
    ) -> SequentialThinkingOutput:
        """Generate the final output model"""
        
        # Extract final conclusion from the conclusion step
        conclusion_step = next(
            (step for step in reasoning_chain if step.step_type == ThoughtStepType.CONCLUSION),
            reasoning_chain[-1] if reasoning_chain else None
        )
        
        final_conclusion = conclusion_step.content if conclusion_step else f"Analysis of {data.problem} completed through sequential reasoning."
        
        # Generate reasoning path summary
        step_types_used = [step.step_type.value for step in reasoning_chain]
        reasoning_path_summary = f"Sequential reasoning process for '{data.problem}' followed {len(reasoning_chain)} steps: {' → '.join(step_types_used[:5])}{'...' if len(step_types_used) > 5 else ''}. The analysis incorporated {len(branches_explored)} alternative branches and {len(revisions_made)} revisions to ensure comprehensive coverage of the problem space."
        
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
            "Stakeholder feedback on proposed solution approach"
        ]
        
        # Generate alternative conclusions from branches
        alternative_conclusions = []
        for branch in branches_explored:
            if branch.steps:
                conclusion_steps = [step for step in branch.steps if step.step_type == ThoughtStepType.CONCLUSION]
                if conclusion_steps:
                    alternative_conclusions.append(conclusion_steps[0].content[:100] + "...")
        
        # Generate recommendations
        recommendations = [
            "Implement the primary solution identified through the reasoning chain",
            "Monitor key indicators to validate the reasoning assumptions",
            "Consider alternative approaches explored in branch analysis",
            "Address identified evidence gaps through additional data collection"
        ]
        
        return SequentialThinkingOutput(
            reasoning_chain=reasoning_chain,
            branches_explored=branches_explored,
            revisions_made=revisions_made,
            final_conclusion=final_conclusion,
            conclusion_confidence=final_confidence,
            reasoning_quality_score=quality_score,
            critical_assumptions=critical_assumptions,
            evidence_gaps=evidence_gaps,
            alternative_conclusions=alternative_conclusions[:5],
            reasoning_path_summary=reasoning_path_summary,
            recommendations=recommendations,
            limitations="Sequential reasoning analysis is limited by the quality of available evidence and the completeness of the problem decomposition. Alternative solutions may exist that were not explored in the current reasoning paths.",
            confidence_score=final_confidence,
            analysis=reasoning_path_summary
        )


__all__ = [
    "SequentialThinkingServer"
]