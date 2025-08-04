"""
Iterative Validation Analyzer

Implements systematic hypothesis-test-learn-refine cycles for continuous improvement.
"""

import asyncio
from typing import List, Dict, Optional, Any

from ..base import BaseCognitiveAnalyzer
from .models import (
    IterativeValidationContext,
    IterativeValidationResult,
    Hypothesis,
    TestDesign,
    TestResults,
    Learning,
    Refinement,
    ValidationCycle,
    ValidationStatus,
    TestType,
    ConfidenceLevel,
    LearningType,
    ComplexityLevel
)


class IterativeValidationAnalyzer(BaseCognitiveAnalyzer):
    """
    Analyzer for iterative validation cycles.
    
    Guides through systematic hypothesis formation, testing, learning extraction,
    and refinement for continuous improvement in any domain.
    """
    
    async def analyze(
        self, 
        context: IterativeValidationContext
    ) -> IterativeValidationResult:
        """
        Perform iterative validation analysis.
        
        Args:
            context: The validation scenario and parameters
            
        Returns:
            IterativeValidationResult with complete validation analysis
        """
        # Generate initial hypothesis if not provided
        if not context.initial_hypothesis:
            initial_hypothesis = await self._generate_initial_hypothesis(context)
        else:
            initial_hypothesis = context.initial_hypothesis
        
        # Initialize validation cycles
        validation_cycles = context.previous_cycles or []
        current_hypothesis = initial_hypothesis
        cumulative_learnings = []
        confidence_progression = {}
        key_pivots = []
        
        # Determine number of cycles based on complexity and constraints
        max_cycles = context.max_iterations or self._determine_max_cycles(context)
        
        # Run validation cycles
        for cycle_num in range(len(validation_cycles) + 1, max_cycles + 1):
            # Design test for current hypothesis
            test_design = await self._design_test(
                current_hypothesis,
                context,
                validation_cycles
            )
            
            # Simulate test execution and results
            test_results = await self._simulate_test_results(
                current_hypothesis,
                test_design,
                context
            )
            
            # Extract learnings from results
            learnings = await self._extract_learnings(
                current_hypothesis,
                test_results,
                context
            )
            cumulative_learnings.extend(learnings)
            
            # Generate refinements based on learnings
            refinements = await self._generate_refinements(
                current_hypothesis,
                learnings,
                context
            )
            
            # Create validation cycle
            cycle = ValidationCycle(
                cycle_number=cycle_num,
                hypothesis=current_hypothesis,
                test_design=test_design,
                test_results=test_results,
                learnings=learnings,
                refinements=refinements,
                status=ValidationStatus.REFINED,
                duration=f"Cycle {cycle_num} duration"
            )
            validation_cycles.append(cycle)
            
            # Track confidence progression
            confidence_progression[cycle_num] = test_results.confidence_in_results
            
            # Check for pivots
            if self._is_pivot(current_hypothesis, refinements):
                key_pivots.append(
                    f"Cycle {cycle_num}: {refinements[0].refinement_description}"
                )
            
            # Refine hypothesis for next cycle
            if refinements and cycle_num < max_cycles:
                current_hypothesis = await self._refine_hypothesis(
                    current_hypothesis,
                    refinements,
                    learnings
                )
            
            # Check if target confidence reached
            if (context.target_confidence and 
                test_results.confidence_in_results == context.target_confidence):
                break
        
        # Analyze convergence
        convergence_analysis = await self._analyze_convergence(
            validation_cycles,
            confidence_progression
        )
        
        # Identify remaining uncertainties
        remaining_uncertainties = await self._identify_uncertainties(
            current_hypothesis,
            cumulative_learnings,
            context
        )
        
        # Generate recommendations
        recommended_next_steps = await self._generate_recommendations(
            current_hypothesis,
            validation_cycles,
            remaining_uncertainties,
            context
        )
        
        # Analyze success and failure factors
        success_factors = await self._identify_success_factors(validation_cycles)
        failure_points = await self._identify_failure_points(validation_cycles)
        
        # Extract methodology insights
        methodology_insights = await self._extract_methodology_insights(
            validation_cycles,
            context
        )
        
        # Calculate overall confidence
        confidence_score = self._calculate_overall_confidence(
            confidence_progression,
            cumulative_learnings
        )
        
        # Generate overall assessment
        overall_assessment = await self._generate_overall_assessment(
            validation_cycles,
            convergence_analysis,
            confidence_score
        )
        
        return IterativeValidationResult(
            input_scenario=context.scenario,
            validation_cycles=validation_cycles,
            current_hypothesis=current_hypothesis,
            cumulative_learnings=cumulative_learnings,
            convergence_analysis=convergence_analysis,
            confidence_progression=confidence_progression,
            key_pivots=key_pivots,
            remaining_uncertainties=remaining_uncertainties,
            recommended_next_steps=recommended_next_steps,
            success_factors=success_factors,
            failure_points=failure_points,
            methodology_insights=methodology_insights,
            overall_assessment=overall_assessment,
            confidence_score=confidence_score
        )
    
    async def _generate_initial_hypothesis(
        self,
        context: IterativeValidationContext
    ) -> Hypothesis:
        """Generate initial hypothesis from scenario."""
        # Extract key elements from scenario
        scenario_analysis = f"Analyzing: {context.scenario}"
        
        # Generate hypothesis based on domain and scenario
        if "pricing" in context.scenario.lower():
            statement = "The proposed pricing model will achieve target adoption rates"
            assumptions = [
                "Market demand exists at this price point",
                "Value proposition justifies the pricing",
                "Competitive positioning is favorable"
            ]
            success_criteria = [
                "Conversion rate meets or exceeds target",
                "Customer satisfaction remains high",
                "Revenue goals are achievable"
            ]
        elif "product" in context.scenario.lower():
            statement = "The product concept addresses the identified user need effectively"
            assumptions = [
                "User need is accurately understood",
                "Proposed solution is technically feasible",
                "Market timing is appropriate"
            ]
            success_criteria = [
                "User engagement metrics meet targets",
                "Problem-solution fit is validated",
                "Technical implementation is successful"
            ]
        else:
            statement = f"The proposed approach to {context.scenario} will achieve desired outcomes"
            assumptions = [
                "Key factors have been identified",
                "Approach is feasible within constraints",
                "Success metrics are well-defined"
            ]
            success_criteria = [
                "Primary objectives are met",
                "Key metrics show improvement",
                "Stakeholder satisfaction is achieved"
            ]
        
        return Hypothesis(
            statement=statement,
            assumptions=assumptions,
            success_criteria=success_criteria,
            confidence_level=ConfidenceLevel.MEDIUM,
            rationale=f"Initial hypothesis based on {scenario_analysis}",
            risks=[
                "Assumptions may be incomplete",
                "External factors not fully considered",
                "Success criteria may need refinement"
            ]
        )
    
    async def _design_test(
        self,
        hypothesis: Hypothesis,
        context: IterativeValidationContext,
        previous_cycles: List[ValidationCycle]
    ) -> TestDesign:
        """Design test for hypothesis validation."""
        # Select appropriate test type
        if context.test_preferences:
            test_type = context.test_preferences[0]
        elif "pricing" in context.scenario.lower():
            test_type = TestType.A_B_TEST
        elif "product" in context.scenario.lower():
            test_type = TestType.PROTOTYPE
        else:
            test_type = TestType.EXPERIMENT
        
        # Define methodology based on test type
        methodology_map = {
            TestType.A_B_TEST: "Split testing with control and variant groups",
            TestType.PROTOTYPE: "Build minimal viable prototype and test with users",
            TestType.EXPERIMENT: "Controlled experiment with defined variables",
            TestType.PILOT: "Limited rollout to test in real conditions",
            TestType.USER_TEST: "Direct user testing with feedback collection"
        }
        
        methodology = methodology_map.get(
            test_type,
            "Systematic testing approach"
        )
        
        # Define metrics based on success criteria
        metrics = [
            f"Metric for: {criterion}"
            for criterion in hypothesis.success_criteria[:3]
        ]
        
        return TestDesign(
            test_type=test_type,
            methodology=methodology,
            metrics=metrics,
            sample_size="Statistically significant sample",
            duration="Test duration based on constraints",
            resources_needed=[
                "Testing infrastructure",
                "Target audience access",
                "Analysis tools"
            ],
            controls=[
                "Baseline measurement",
                "Environmental factors",
                "Selection bias mitigation"
            ],
            success_threshold="Defined success threshold"
        )
    
    async def _simulate_test_results(
        self,
        hypothesis: Hypothesis,
        test_design: TestDesign,
        context: IterativeValidationContext
    ) -> TestResults:
        """Simulate test execution and results."""
        # Simulate results based on complexity and domain
        if context.complexity_level == ComplexityLevel.SIMPLE:
            confidence = ConfidenceLevel.HIGH
            success_rate = 0.8
        elif context.complexity_level == ComplexityLevel.COMPLEX:
            confidence = ConfidenceLevel.MEDIUM
            success_rate = 0.6
        else:
            confidence = ConfidenceLevel.MEDIUM
            success_rate = 0.7
        
        # Generate test results
        key_findings = [
            f"Primary metric achieved {success_rate*100:.0f}% of target",
            "User feedback indicates positive reception",
            "Some assumptions validated, others need revision"
        ]
        
        metrics_achieved = {
            metric: f"{success_rate*100:.0f}% of target"
            for metric in test_design.metrics
        }
        
        return TestResults(
            raw_data={
                "sample_size": 100,
                "completion_rate": success_rate,
                "feedback_scores": [4.2, 4.5, 3.8],
                "conversion_metrics": {"baseline": 0.05, "variant": 0.08}
            },
            key_findings=key_findings,
            metrics_achieved=metrics_achieved,
            unexpected_observations=[
                "Higher engagement from unexpected user segment",
                "Feature X more important than anticipated"
            ],
            confidence_in_results=confidence,
            limitations=[
                "Limited sample size",
                "Short test duration",
                "Single market segment tested"
            ]
        )
    
    async def _extract_learnings(
        self,
        hypothesis: Hypothesis,
        test_results: TestResults,
        context: IterativeValidationContext
    ) -> List[Learning]:
        """Extract learnings from test results."""
        learnings = []
        
        # Analyze primary findings
        if any("achieved" in finding for finding in test_results.key_findings):
            learnings.append(Learning(
                learning_type=LearningType.PARTIAL,
                key_insight="Hypothesis partially validated with room for improvement",
                supporting_evidence=test_results.key_findings[:2],
                implications=[
                    "Core approach is sound",
                    "Refinements needed for full validation",
                    "Scale testing to confirm results"
                ],
                confidence_level=test_results.confidence_in_results,
                actionable_items=[
                    "Refine approach based on feedback",
                    "Expand testing to broader audience",
                    "Iterate on weak performing areas"
                ]
            ))
        
        # Analyze unexpected observations
        if test_results.unexpected_observations:
            learnings.append(Learning(
                learning_type=LearningType.UNEXPECTED,
                key_insight="New opportunities discovered through testing",
                supporting_evidence=test_results.unexpected_observations,
                implications=[
                    "Market understanding needs updating",
                    "Additional value propositions possible",
                    "Pivot potential identified"
                ],
                confidence_level=ConfidenceLevel.MEDIUM,
                actionable_items=[
                    "Investigate unexpected findings further",
                    "Consider strategic pivots",
                    "Update market research"
                ]
            ))
        
        return learnings
    
    async def _generate_refinements(
        self,
        hypothesis: Hypothesis,
        learnings: List[Learning],
        context: IterativeValidationContext
    ) -> List[Refinement]:
        """Generate refinements based on learnings."""
        refinements = []
        
        for learning in learnings:
            if learning.learning_type == LearningType.PARTIAL:
                refinements.append(Refinement(
                    original_element="hypothesis",
                    refinement_description="Adjust hypothesis based on partial validation",
                    rationale=learning.key_insight,
                    expected_improvement="Higher validation confidence in next cycle",
                    implementation_steps=[
                        "Update assumptions based on evidence",
                        "Refine success criteria",
                        "Adjust test parameters"
                    ]
                ))
            elif learning.learning_type == LearningType.UNEXPECTED:
                refinements.append(Refinement(
                    original_element="approach",
                    refinement_description="Incorporate unexpected discoveries",
                    rationale="Leverage new opportunities identified",
                    expected_improvement="Expanded value proposition",
                    implementation_steps=[
                        "Research unexpected findings",
                        "Update strategy to include new insights",
                        "Design tests for new opportunities"
                    ]
                ))
        
        return refinements
    
    def _determine_max_cycles(self, context: IterativeValidationContext) -> int:
        """Determine maximum cycles based on complexity."""
        if context.complexity_level == ComplexityLevel.SIMPLE:
            return 2
        elif context.complexity_level == ComplexityLevel.COMPLEX:
            return 5
        else:
            return 3
    
    def _is_pivot(
        self,
        hypothesis: Hypothesis,
        refinements: List[Refinement]
    ) -> bool:
        """Check if refinements constitute a major pivot."""
        return any(
            "pivot" in r.refinement_description.lower() or
            "major change" in r.rationale.lower()
            for r in refinements
        )
    
    async def _refine_hypothesis(
        self,
        current: Hypothesis,
        refinements: List[Refinement],
        learnings: List[Learning]
    ) -> Hypothesis:
        """Create refined hypothesis for next cycle."""
        # Update statement based on refinements
        refined_statement = current.statement
        if refinements:
            refined_statement = f"Refined: {current.statement} with adjustments"
        
        # Update assumptions based on learnings
        refined_assumptions = current.assumptions.copy()
        for learning in learnings:
            if learning.learning_type == LearningType.REFUTATION:
                # Remove invalidated assumptions
                refined_assumptions = [
                    a for a in refined_assumptions
                    if not any(e in a for e in learning.supporting_evidence)
                ]
            elif learning.learning_type == LearningType.UNEXPECTED:
                # Add new assumptions
                refined_assumptions.append(
                    f"New insight: {learning.key_insight}"
                )
        
        # Update confidence based on learnings
        confidence_map = {
            LearningType.CONFIRMATION: ConfidenceLevel.HIGH,
            LearningType.PARTIAL: ConfidenceLevel.MEDIUM,
            LearningType.REFUTATION: ConfidenceLevel.LOW,
            LearningType.UNEXPECTED: ConfidenceLevel.MEDIUM
        }
        
        new_confidence = confidence_map.get(
            learnings[0].learning_type if learnings else LearningType.PARTIAL,
            current.confidence_level
        )
        
        return Hypothesis(
            statement=refined_statement,
            assumptions=refined_assumptions[:5],  # Keep manageable
            success_criteria=current.success_criteria,
            confidence_level=new_confidence,
            rationale=f"Refined based on cycle learnings",
            risks=current.risks,
            related_hypotheses=current.related_hypotheses
        )
    
    async def _analyze_convergence(
        self,
        cycles: List[ValidationCycle],
        confidence_progression: Dict[int, ConfidenceLevel]
    ) -> str:
        """Analyze convergence toward validated solution."""
        if not cycles:
            return "No cycles completed yet"
        
        # Analyze confidence trend
        confidence_values = list(confidence_progression.values())
        if all(c == ConfidenceLevel.HIGH for c in confidence_values[-2:]):
            trend = "Strong convergence achieved"
        elif confidence_values[-1] > confidence_values[0]:
            trend = "Positive convergence trend"
        else:
            trend = "Limited convergence observed"
        
        # Analyze learning stability
        recent_learnings = cycles[-1].learnings if cycles else []
        learning_types = [l.learning_type for l in recent_learnings]
        
        if LearningType.CONFIRMATION in learning_types:
            stability = "hypothesis stabilizing"
        elif LearningType.UNEXPECTED in learning_types:
            stability = "new directions emerging"
        else:
            stability = "continued iteration needed"
        
        return f"{trend} with {stability}. {len(cycles)} cycles completed with progressive refinement."
    
    async def _identify_uncertainties(
        self,
        hypothesis: Hypothesis,
        learnings: List[Learning],
        context: IterativeValidationContext
    ) -> List[str]:
        """Identify remaining uncertainties."""
        uncertainties = []
        
        # Check unvalidated assumptions
        validated_assumptions = set()
        for learning in learnings:
            if learning.learning_type == LearningType.CONFIRMATION:
                validated_assumptions.update(learning.supporting_evidence)
        
        for assumption in hypothesis.assumptions:
            if assumption not in validated_assumptions:
                uncertainties.append(f"Assumption not fully validated: {assumption}")
        
        # Add domain-specific uncertainties
        if "market" in context.scenario.lower():
            uncertainties.append("Long-term market dynamics remain uncertain")
        if "technical" in context.scenario.lower():
            uncertainties.append("Scalability under real-world conditions")
        
        return uncertainties[:5]  # Top uncertainties
    
    async def _generate_recommendations(
        self,
        hypothesis: Hypothesis,
        cycles: List[ValidationCycle],
        uncertainties: List[str],
        context: IterativeValidationContext
    ) -> List[str]:
        """Generate next step recommendations."""
        recommendations = []
        
        # Based on confidence level
        if hypothesis.confidence_level == ConfidenceLevel.HIGH:
            recommendations.append("Proceed to full implementation with monitoring")
            recommendations.append("Establish success metrics for production")
        elif hypothesis.confidence_level == ConfidenceLevel.MEDIUM:
            recommendations.append("Conduct one more validation cycle focused on uncertainties")
            recommendations.append("Expand testing to address remaining risks")
        else:
            recommendations.append("Reconsider fundamental assumptions")
            recommendations.append("Explore alternative approaches")
        
        # Address specific uncertainties
        for uncertainty in uncertainties[:2]:
            recommendations.append(f"Design targeted test for: {uncertainty}")
        
        return recommendations
    
    async def _identify_success_factors(
        self,
        cycles: List[ValidationCycle]
    ) -> List[str]:
        """Identify factors contributing to success."""
        success_factors = []
        
        for cycle in cycles:
            # Check for positive outcomes
            if any(l.learning_type == LearningType.CONFIRMATION for l in cycle.learnings):
                success_factors.append(
                    f"Cycle {cycle.cycle_number}: Effective {cycle.test_design.test_type} methodology"
                )
            
            # Check for useful unexpected findings
            if any(l.learning_type == LearningType.UNEXPECTED for l in cycle.learnings):
                success_factors.append(
                    f"Cycle {cycle.cycle_number}: Openness to unexpected discoveries"
                )
        
        # General success factors
        success_factors.extend([
            "Systematic approach to validation",
            "Clear success criteria definition",
            "Iterative refinement based on evidence"
        ])
        
        return success_factors[:5]
    
    async def _identify_failure_points(
        self,
        cycles: List[ValidationCycle]
    ) -> List[str]:
        """Identify where validations struggled."""
        failure_points = []
        
        for cycle in cycles:
            # Check for refutations
            if any(l.learning_type == LearningType.REFUTATION for l in cycle.learnings):
                failure_points.append(
                    f"Cycle {cycle.cycle_number}: Hypothesis refuted"
                )
            
            # Check for low confidence
            if cycle.test_results.confidence_in_results in [ConfidenceLevel.LOW, ConfidenceLevel.VERY_LOW]:
                failure_points.append(
                    f"Cycle {cycle.cycle_number}: Low confidence in results"
                )
            
            # Check limitations
            if len(cycle.test_results.limitations) > 3:
                failure_points.append(
                    f"Cycle {cycle.cycle_number}: Significant test limitations"
                )
        
        return failure_points
    
    async def _extract_methodology_insights(
        self,
        cycles: List[ValidationCycle],
        context: IterativeValidationContext
    ) -> List[str]:
        """Extract insights about the validation process."""
        insights = []
        
        # Test type effectiveness
        test_types_used = [c.test_design.test_type for c in cycles]
        if len(set(test_types_used)) > 1:
            insights.append("Multiple test types provided complementary insights")
        
        # Cycle efficiency
        if len(cycles) <= 2 and cycles[-1].test_results.confidence_in_results == ConfidenceLevel.HIGH:
            insights.append("Efficient validation achieved with minimal cycles")
        elif len(cycles) > 4:
            insights.append("Complex validation required extended iteration")
        
        # Learning patterns
        learning_types = [l.learning_type for c in cycles for l in c.learnings]
        if LearningType.UNEXPECTED in learning_types:
            insights.append("Process enabled discovery of unanticipated opportunities")
        
        # Domain-specific insights
        if context.domain_context:
            insights.append(
                f"Domain-specific approach for {context.domain_context} proved effective"
            )
        
        return insights
    
    def _calculate_overall_confidence(
        self,
        progression: Dict[int, ConfidenceLevel],
        learnings: List[Learning]
    ) -> float:
        """Calculate overall confidence score."""
        if not progression:
            return 0.5
        
        # Map confidence levels to scores
        confidence_scores = {
            ConfidenceLevel.VERY_LOW: 0.2,
            ConfidenceLevel.LOW: 0.4,
            ConfidenceLevel.MEDIUM: 0.6,
            ConfidenceLevel.HIGH: 0.8,
            ConfidenceLevel.VERY_HIGH: 0.95
        }
        
        # Weight recent cycles more heavily
        weights = [0.1, 0.2, 0.3, 0.4]  # Recent cycles weighted more
        weighted_sum = 0
        weight_total = 0
        
        cycles = sorted(progression.keys())
        for i, cycle in enumerate(cycles[-4:]):  # Last 4 cycles
            weight = weights[min(i, len(weights)-1)]
            score = confidence_scores.get(progression[cycle], 0.5)
            weighted_sum += weight * score
            weight_total += weight
        
        return weighted_sum / weight_total if weight_total > 0 else 0.5
    
    async def _generate_overall_assessment(
        self,
        cycles: List[ValidationCycle],
        convergence: str,
        confidence: float
    ) -> str:
        """Generate overall assessment of validation process."""
        # Determine validation success level
        if confidence >= 0.8:
            success_level = "highly successful"
        elif confidence >= 0.6:
            success_level = "moderately successful"
        else:
            success_level = "partially successful"
        
        # Count key metrics
        total_learnings = sum(len(c.learnings) for c in cycles)
        total_refinements = sum(len(c.refinements) for c in cycles)
        
        assessment = (
            f"The iterative validation process was {success_level} "
            f"with {len(cycles)} cycles completed. {convergence} "
            f"The process generated {total_learnings} key learnings and "
            f"{total_refinements} refinements, achieving a final confidence "
            f"score of {confidence:.2f}. "
        )
        
        if confidence >= 0.7:
            assessment += (
                "The validated approach is ready for implementation with "
                "appropriate monitoring and continued iteration."
            )
        else:
            assessment += (
                "Additional validation cycles are recommended before "
                "full-scale implementation."
            )
        
        return assessment