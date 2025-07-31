# Clear Thinking FastMCP Server - Iterative Validation Cycle Tool

"""
Iterative Validation Cycle cognitive tool implementation for FastMCP.

This tool provides systematic hypothesis-test-learn-refine cycles for
empirical validation and continuous improvement across any domain.
"""

from typing import List, Dict, Optional, Any
from fastmcp.tools import tool
from ..models.iterative_validation import (
    IterativeValidationInput,
    IterativeValidationAnalysis,
    Hypothesis,
    TestDesign,
    TestResults,
    Learning,
    Refinement,
    ValidationCycle,
    ValidationStatus,
    TestType,
    ConfidenceLevel,
    LearningType
)
from .base import CognitiveToolBase


class IterativeValidationTool(CognitiveToolBase):
    """
    Tool for systematic iterative validation cycles.
    
    Enables hypothesis-test-learn-refine patterns applicable to:
    - Research and development
    - Product development
    - Process improvement
    - Scientific investigation
    - Business experimentation
    """
    
    # Domain-specific test type mappings
    DOMAIN_TEST_TYPES = {
        "product_development": [
            TestType.PROTOTYPE,
            TestType.USER_TEST,
            TestType.A_B_TEST,
            TestType.PILOT
        ],
        "research": [
            TestType.EXPERIMENT,
            TestType.SIMULATION,
            TestType.ANALYSIS,
            TestType.TECHNICAL_TEST
        ],
        "business": [
            TestType.MARKET_TEST,
            TestType.PILOT,
            TestType.A_B_TEST,
            TestType.SURVEY
        ],
        "process_improvement": [
            TestType.PILOT,
            TestType.ANALYSIS,
            TestType.SIMULATION,
            TestType.A_B_TEST
        ]
    }
    
    # Domain templates for hypothesis patterns
    DOMAIN_TEMPLATES = {
        "product_development": {
            "focus_areas": ["user experience", "feature adoption", "performance", "value proposition"],
            "metrics": ["conversion rate", "retention", "user satisfaction", "feature usage"],
            "typical_cycles": 3
        },
        "research": {
            "focus_areas": ["algorithm performance", "accuracy", "scalability", "robustness"],
            "metrics": ["accuracy metrics", "performance benchmarks", "statistical significance", "reproducibility"],
            "typical_cycles": 4
        },
        "business": {
            "focus_areas": ["market fit", "pricing", "customer acquisition", "revenue model"],
            "metrics": ["revenue", "customer lifetime value", "acquisition cost", "market share"],
            "typical_cycles": 3
        },
        "process_improvement": {
            "focus_areas": ["efficiency", "quality", "cost reduction", "cycle time"],
            "metrics": ["throughput", "error rate", "cost per unit", "process time"],
            "typical_cycles": 2
        }
    }
    
    async def analyze_iterative_validation(
        self,
        scenario: str,
        domain_context: Optional[str],
        initial_hypothesis: Optional[Hypothesis],
        validation_constraints: Optional[Dict[str, str]],
        previous_cycles: Optional[List[ValidationCycle]],
        target_confidence: ConfidenceLevel,
        max_iterations: Optional[int],
        test_preferences: Optional[List[TestType]],
        context: Any
    ) -> IterativeValidationAnalysis:
        """Perform comprehensive iterative validation analysis."""
        
        await context.progress("Starting iterative validation analysis", 0.1)
        
        # Generate or refine hypothesis
        if not previous_cycles:
            current_hypothesis = await self._generate_initial_hypothesis(
                scenario, domain_context, initial_hypothesis, context
            )
            cycles = []
        else:
            current_hypothesis = await self._refine_hypothesis(
                previous_cycles[-1], context
            )
            cycles = previous_cycles
        
        await context.progress("Designing validation approach", 0.3)
        
        # Design next validation cycle
        next_cycle = await self._design_validation_cycle(
            current_hypothesis,
            domain_context,
            test_preferences,
            validation_constraints,
            len(cycles) + 1,
            context
        )
        
        # Simulate or plan the cycle
        cycles.append(next_cycle)
        
        await context.progress("Analyzing validation patterns", 0.5)
        
        # Extract cumulative learnings
        cumulative_learnings = await self._extract_cumulative_learnings(
            cycles, context
        )
        
        # Analyze convergence
        convergence_analysis = await self._analyze_convergence(
            cycles, target_confidence, context
        )
        
        await context.progress("Generating insights and recommendations", 0.7)
        
        # Track confidence progression
        confidence_progression = self._track_confidence_progression(cycles)
        
        # Identify key pivots
        key_pivots = await self._identify_pivots(cycles, context)
        
        # Identify remaining uncertainties
        remaining_uncertainties = await self._identify_uncertainties(
            current_hypothesis, cumulative_learnings, context
        )
        
        # Generate recommendations
        recommended_next_steps = await self._generate_next_steps(
            current_hypothesis,
            cycles,
            remaining_uncertainties,
            max_iterations,
            context
        )
        
        # Identify success and failure factors
        success_factors = await self._identify_success_factors(cycles, context)
        failure_points = await self._identify_failure_points(cycles, context)
        
        # Extract methodology insights
        methodology_insights = await self._extract_methodology_insights(
            cycles, domain_context, context
        )
        
        await context.progress("Finalizing analysis", 0.9)
        
        # Create visualization data
        visual_representation = self._create_visualization_data(
            cycles, confidence_progression
        )
        
        # Overall assessment
        overall_assessment = await self._generate_overall_assessment(
            cycles, convergence_analysis, target_confidence, context
        )
        
        # Calculate overall confidence
        confidence_level = self._calculate_overall_confidence(
            current_hypothesis, cycles, remaining_uncertainties
        )
        
        return IterativeValidationAnalysis(
            input_scenario=scenario,
            validation_cycles=cycles,
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
            visual_representation=visual_representation,
            overall_assessment=overall_assessment,
            confidence_level=confidence_level
        )
    
    async def _generate_initial_hypothesis(
        self,
        scenario: str,
        domain_context: Optional[str],
        provided_hypothesis: Optional[Hypothesis],
        context: Any
    ) -> Hypothesis:
        """Generate initial hypothesis if not provided."""
        if provided_hypothesis:
            return provided_hypothesis
        
        await context.info("Generating initial hypothesis from scenario")
        
        # Extract key elements from scenario
        assumptions = self._extract_assumptions(scenario, domain_context)
        success_criteria = self._generate_success_criteria(scenario, domain_context)
        
        return Hypothesis(
            statement=f"Solution approach for: {scenario}",
            assumptions=assumptions,
            success_criteria=success_criteria,
            confidence_level=ConfidenceLevel.LOW,
            rationale="Initial hypothesis based on scenario analysis",
            risks=["Untested assumptions", "Limited data", "Unknown variables"],
            related_hypotheses=[]
        )
    
    async def _refine_hypothesis(
        self,
        last_cycle: ValidationCycle,
        context: Any
    ) -> Hypothesis:
        """Refine hypothesis based on previous cycle learnings."""
        await context.info("Refining hypothesis based on learnings")
        
        # Apply refinements from last cycle
        if last_cycle.refinements:
            main_refinement = last_cycle.refinements[0]
            refined_statement = main_refinement.refinement_description
        else:
            refined_statement = last_cycle.hypothesis.statement + " (refined)"
        
        # Update confidence based on learnings
        new_confidence = self._update_confidence_level(
            last_cycle.hypothesis.confidence_level,
            last_cycle.learnings
        )
        
        # Update assumptions based on learnings
        refined_assumptions = self._refine_assumptions(
            last_cycle.hypothesis.assumptions,
            last_cycle.learnings
        )
        
        return Hypothesis(
            statement=refined_statement,
            assumptions=refined_assumptions,
            success_criteria=last_cycle.hypothesis.success_criteria,
            confidence_level=new_confidence,
            rationale=f"Refined based on: {last_cycle.learnings[0].key_insight if last_cycle.learnings else 'previous results'}",
            risks=self._update_risks(last_cycle),
            related_hypotheses=[last_cycle.hypothesis.statement]
        )
    
    async def _design_validation_cycle(
        self,
        hypothesis: Hypothesis,
        domain_context: Optional[str],
        test_preferences: Optional[List[TestType]],
        constraints: Optional[Dict[str, str]],
        cycle_number: int,
        context: Any
    ) -> ValidationCycle:
        """Design a validation cycle for the hypothesis."""
        await context.info(f"Designing validation cycle {cycle_number}")
        
        # Select appropriate test type
        test_type = self._select_test_type(
            hypothesis, domain_context, test_preferences, cycle_number
        )
        
        # Design the test
        test_design = await self._create_test_design(
            hypothesis, test_type, constraints, context
        )
        
        # Simulate test results (in real implementation, would await actual test)
        test_results = await self._simulate_test_results(
            hypothesis, test_design, context
        )
        
        # Extract learnings
        learnings = await self._extract_learnings(
            hypothesis, test_results, context
        )
        
        # Generate refinements
        refinements = await self._generate_refinements(
            hypothesis, learnings, context
        )
        
        # Determine status
        status = self._determine_cycle_status(learnings, refinements)
        
        return ValidationCycle(
            cycle_number=cycle_number,
            hypothesis=hypothesis,
            test_design=test_design,
            test_results=test_results,
            learnings=learnings,
            refinements=refinements,
            status=status,
            duration=constraints.get("timeline") if constraints else None
        )
    
    def _select_test_type(
        self,
        hypothesis: Hypothesis,
        domain_context: Optional[str],
        preferences: Optional[List[TestType]],
        cycle_number: int
    ) -> TestType:
        """Select appropriate test type based on context."""
        if preferences:
            # Use preferences if provided
            return preferences[0] if cycle_number == 1 else preferences[min(cycle_number - 1, len(preferences) - 1)]
        
        # Use domain-specific defaults
        if domain_context and domain_context in self.DOMAIN_TEST_TYPES:
            domain_types = self.DOMAIN_TEST_TYPES[domain_context]
            return domain_types[min(cycle_number - 1, len(domain_types) - 1)]
        
        # Default progression
        default_progression = [
            TestType.ANALYSIS,
            TestType.PROTOTYPE,
            TestType.PILOT,
            TestType.A_B_TEST
        ]
        return default_progression[min(cycle_number - 1, len(default_progression) - 1)]
    
    async def _create_test_design(
        self,
        hypothesis: Hypothesis,
        test_type: TestType,
        constraints: Optional[Dict[str, str]],
        context: Any
    ) -> TestDesign:
        """Create test design for the hypothesis."""
        await context.debug(f"Creating {test_type} test design")
        
        # Generate methodology based on test type
        methodology = self._generate_methodology(hypothesis, test_type)
        
        # Define metrics
        metrics = self._define_metrics(hypothesis, test_type)
        
        # Set sample size and duration
        sample_size = constraints.get("sample_size", "As needed") if constraints else "As needed"
        duration = constraints.get("timeline", "Flexible") if constraints else "Flexible"
        
        return TestDesign(
            test_type=test_type,
            methodology=methodology,
            metrics=metrics,
            sample_size=sample_size,
            duration=duration,
            resources_needed=self._identify_resources(test_type),
            controls=self._identify_controls(hypothesis),
            success_threshold=self._define_success_threshold(hypothesis)
        )
    
    async def _simulate_test_results(
        self,
        hypothesis: Hypothesis,
        test_design: TestDesign,
        context: Any
    ) -> TestResults:
        """Simulate test results (placeholder for actual testing)."""
        await context.debug("Simulating test results")
        
        # In real implementation, this would execute actual tests
        # For now, simulate based on hypothesis confidence
        success_rate = 0.5 + (0.1 * self._confidence_to_numeric(hypothesis.confidence_level))
        
        raw_data = {
            "primary_metric": success_rate,
            "sample_size": test_design.sample_size,
            "duration": test_design.duration
        }
        
        key_findings = self._generate_key_findings(success_rate, hypothesis)
        metrics_achieved = {metric: f"{success_rate * 100:.1f}%" for metric in test_design.metrics[:2]}
        
        return TestResults(
            raw_data=raw_data,
            key_findings=key_findings,
            metrics_achieved=metrics_achieved,
            unexpected_observations=self._generate_unexpected_observations(success_rate),
            confidence_in_results=self._determine_results_confidence(success_rate),
            limitations=["Simulated results", "Limited sample size"]
        )
    
    async def _extract_learnings(
        self,
        hypothesis: Hypothesis,
        results: TestResults,
        context: Any
    ) -> List[Learning]:
        """Extract learnings from test results."""
        await context.debug("Extracting learnings from results")
        
        learnings = []
        
        # Determine primary learning type
        success_rate = results.raw_data.get("primary_metric", 0.5)
        
        if success_rate > 0.8:
            learning_type = LearningType.CONFIRMATION
            key_insight = "Hypothesis strongly supported by evidence"
        elif success_rate > 0.6:
            learning_type = LearningType.PARTIAL
            key_insight = "Hypothesis partially validated with caveats"
        elif success_rate > 0.4:
            learning_type = LearningType.DIRECTIONAL
            key_insight = "Results indicate direction but need refinement"
        else:
            learning_type = LearningType.REFUTATION
            key_insight = "Hypothesis needs significant revision"
        
        # Add unexpected discoveries if any
        if results.unexpected_observations:
            learnings.append(Learning(
                learning_type=LearningType.UNEXPECTED,
                key_insight=results.unexpected_observations[0],
                supporting_evidence=results.unexpected_observations,
                implications=["Explore unexpected finding", "Adjust hypothesis"],
                confidence_level=ConfidenceLevel.MEDIUM,
                actionable_items=["Investigate further", "Design targeted test"]
            ))
        
        # Primary learning
        learnings.append(Learning(
            learning_type=learning_type,
            key_insight=key_insight,
            supporting_evidence=results.key_findings,
            implications=self._derive_implications(learning_type, hypothesis),
            confidence_level=results.confidence_in_results,
            actionable_items=self._generate_action_items(learning_type, hypothesis)
        ))
        
        return learnings
    
    async def _generate_refinements(
        self,
        hypothesis: Hypothesis,
        learnings: List[Learning],
        context: Any
    ) -> List[Refinement]:
        """Generate refinements based on learnings."""
        await context.debug("Generating refinements")
        
        refinements = []
        
        for learning in learnings:
            if learning.learning_type in [LearningType.REFUTATION, LearningType.PARTIAL]:
                refinement = Refinement(
                    original_element=hypothesis.statement,
                    refinement_description=self._create_refined_statement(hypothesis, learning),
                    rationale=learning.key_insight,
                    expected_improvement=self._estimate_improvement(learning),
                    implementation_steps=self._define_implementation_steps(learning)
                )
                refinements.append(refinement)
        
        return refinements
    
    async def _extract_cumulative_learnings(
        self,
        cycles: List[ValidationCycle],
        context: Any
    ) -> List[Learning]:
        """Extract cumulative learnings across all cycles."""
        await context.info("Extracting cumulative learnings")
        
        all_learnings = []
        for cycle in cycles:
            all_learnings.extend(cycle.learnings)
        
        # Synthesize and deduplicate
        return self._synthesize_learnings(all_learnings)
    
    async def _analyze_convergence(
        self,
        cycles: List[ValidationCycle],
        target_confidence: ConfidenceLevel,
        context: Any
    ) -> str:
        """Analyze convergence toward validated solution."""
        await context.info("Analyzing convergence patterns")
        
        if not cycles:
            return "No validation cycles completed yet"
        
        # Track confidence progression
        confidence_values = [
            self._confidence_to_numeric(cycle.hypothesis.confidence_level)
            for cycle in cycles
        ]
        
        # Check if converging
        if len(confidence_values) > 1:
            trend = confidence_values[-1] - confidence_values[0]
            rate = trend / len(cycles)
            
            if rate > 0.2:
                convergence = "Strong positive convergence"
            elif rate > 0.1:
                convergence = "Moderate convergence"
            elif rate > 0:
                convergence = "Slow convergence"
            else:
                convergence = "No clear convergence"
        else:
            convergence = "Initial cycle - convergence not yet measurable"
        
        # Estimate cycles to target
        current_confidence = confidence_values[-1]
        target_numeric = self._confidence_to_numeric(target_confidence)
        
        if current_confidence >= target_numeric:
            status = "Target confidence achieved"
        else:
            gap = target_numeric - current_confidence
            if rate > 0:
                cycles_needed = int(gap / rate) + 1
                status = f"Estimated {cycles_needed} more cycles to reach target"
            else:
                status = "Convergence stalled - hypothesis revision needed"
        
        return f"{convergence}. {status}"
    
    async def _identify_pivots(
        self,
        cycles: List[ValidationCycle],
        context: Any
    ) -> List[str]:
        """Identify major pivots in validation journey."""
        await context.debug("Identifying key pivots")
        
        pivots = []
        
        for i in range(1, len(cycles)):
            prev_hypothesis = cycles[i-1].hypothesis.statement
            curr_hypothesis = cycles[i].hypothesis.statement
            
            # Check for significant changes
            if self._is_significant_change(prev_hypothesis, curr_hypothesis):
                pivot_description = f"Cycle {i}: {self._describe_pivot(prev_hypothesis, curr_hypothesis)}"
                pivots.append(pivot_description)
        
        return pivots
    
    async def _identify_uncertainties(
        self,
        hypothesis: Hypothesis,
        learnings: List[Learning],
        context: Any
    ) -> List[str]:
        """Identify remaining uncertainties."""
        await context.debug("Identifying remaining uncertainties")
        
        uncertainties = []
        
        # Check untested assumptions
        tested_assumptions = set()
        for learning in learnings:
            tested_assumptions.update(self._extract_tested_assumptions(learning))
        
        for assumption in hypothesis.assumptions:
            if assumption not in tested_assumptions:
                uncertainties.append(f"Untested assumption: {assumption}")
        
        # Add domain-specific uncertainties
        uncertainties.extend([
            "Long-term sustainability of approach",
            "Scalability under different conditions",
            "Edge cases and failure modes",
            "External factor dependencies"
        ])
        
        return uncertainties
    
    async def _generate_next_steps(
        self,
        hypothesis: Hypothesis,
        cycles: List[ValidationCycle],
        uncertainties: List[str],
        max_iterations: Optional[int],
        context: Any
    ) -> List[str]:
        """Generate recommended next validation steps."""
        await context.info("Generating next steps")
        
        steps = []
        
        # Check iteration limit
        if max_iterations and len(cycles) >= max_iterations:
            steps.append("Maximum iterations reached - finalize conclusions")
            return steps
        
        # Based on current confidence
        confidence = hypothesis.confidence_level
        
        if confidence == ConfidenceLevel.VERY_HIGH:
            steps.extend([
                "Conduct final validation with larger sample",
                "Prepare for full implementation",
                "Document learnings and best practices"
            ])
        elif confidence == ConfidenceLevel.HIGH:
            steps.extend([
                "Test edge cases and failure modes",
                "Validate with different user segments",
                "Refine implementation details"
            ])
        else:
            steps.extend([
                "Address key uncertainties through targeted tests",
                "Consider alternative approaches",
                "Gather more diverse data points"
            ])
        
        # Address specific uncertainties
        for uncertainty in uncertainties[:2]:
            steps.append(f"Design test to address: {uncertainty}")
        
        return steps
    
    async def _identify_success_factors(
        self,
        cycles: List[ValidationCycle],
        context: Any
    ) -> List[str]:
        """Identify factors contributing to validation success."""
        await context.debug("Identifying success factors")
        
        factors = []
        
        for cycle in cycles:
            for learning in cycle.learnings:
                if learning.learning_type in [LearningType.CONFIRMATION, LearningType.PARTIAL]:
                    factors.extend(self._extract_success_factors(learning))
        
        # Deduplicate and prioritize
        return list(dict.fromkeys(factors))[:5]
    
    async def _identify_failure_points(
        self,
        cycles: List[ValidationCycle],
        context: Any
    ) -> List[str]:
        """Identify where validations failed or struggled."""
        await context.debug("Identifying failure points")
        
        failures = []
        
        for cycle in cycles:
            for learning in cycle.learnings:
                if learning.learning_type == LearningType.REFUTATION:
                    failures.append(f"Cycle {cycle.cycle_number}: {learning.key_insight}")
            
            # Check for limitations
            if cycle.test_results.limitations:
                failures.extend([f"Limitation in cycle {cycle.cycle_number}: {lim}" 
                               for lim in cycle.test_results.limitations[:1]])
        
        return failures
    
    async def _extract_methodology_insights(
        self,
        cycles: List[ValidationCycle],
        domain_context: Optional[str],
        context: Any
    ) -> List[str]:
        """Extract insights about the validation process itself."""
        await context.info("Extracting methodology insights")
        
        insights = []
        
        # Test type effectiveness
        test_type_success = {}
        for cycle in cycles:
            test_type = cycle.test_design.test_type
            success = self._evaluate_cycle_success(cycle)
            if test_type not in test_type_success:
                test_type_success[test_type] = []
            test_type_success[test_type].append(success)
        
        for test_type, successes in test_type_success.items():
            avg_success = sum(successes) / len(successes)
            if avg_success > 0.7:
                insights.append(f"{test_type} tests highly effective for this domain")
        
        # Cycle duration insights
        if len(cycles) > 1:
            insights.append(f"Optimal cycle duration: {cycles[0].duration or 'Flexible'}")
        
        # Domain-specific insights
        if domain_context:
            template = self.DOMAIN_TEMPLATES.get(domain_context, {})
            if len(cycles) >= template.get("typical_cycles", 3):
                insights.append(f"Validation aligns with typical {domain_context} patterns")
        
        return insights
    
    def _create_visualization_data(
        self,
        cycles: List[ValidationCycle],
        confidence_progression: Dict[int, ConfidenceLevel]
    ) -> Dict[str, Any]:
        """Create data for visualizing validation journey."""
        return {
            "timeline": {
                "cycles": [
                    {
                        "number": cycle.cycle_number,
                        "hypothesis": cycle.hypothesis.statement[:50] + "...",
                        "test_type": cycle.test_design.test_type,
                        "status": cycle.status
                    }
                    for cycle in cycles
                ]
            },
            "confidence_chart": {
                "x": list(confidence_progression.keys()),
                "y": [self._confidence_to_numeric(conf) for conf in confidence_progression.values()],
                "labels": list(confidence_progression.values())
            },
            "learning_distribution": {
                "types": [learning.learning_type for cycle in cycles for learning in cycle.learnings],
                "counts": {}  # Would be calculated from types
            }
        }
    
    async def _generate_overall_assessment(
        self,
        cycles: List[ValidationCycle],
        convergence: str,
        target_confidence: ConfidenceLevel,
        context: Any
    ) -> str:
        """Generate overall assessment of validation process."""
        await context.info("Generating overall assessment")
        
        if not cycles:
            return "Validation process not yet started"
        
        current_confidence = cycles[-1].hypothesis.confidence_level
        cycles_completed = len(cycles)
        
        # Assess progress
        if current_confidence == ConfidenceLevel.VERY_HIGH:
            progress = "Validation highly successful"
        elif current_confidence == ConfidenceLevel.HIGH:
            progress = "Strong validation progress"
        elif cycles_completed > 3 and current_confidence == ConfidenceLevel.MEDIUM:
            progress = "Moderate progress - consider approach revision"
        else:
            progress = "Early validation stage"
        
        # Assess efficiency
        if cycles_completed <= 2 and current_confidence >= ConfidenceLevel.HIGH:
            efficiency = "Highly efficient validation"
        elif cycles_completed <= 4 and current_confidence >= ConfidenceLevel.HIGH:
            efficiency = "Good validation efficiency"
        else:
            efficiency = "Extended validation required"
        
        return f"{progress}. {efficiency}. {convergence}"
    
    def _calculate_overall_confidence(
        self,
        hypothesis: Hypothesis,
        cycles: List[ValidationCycle],
        uncertainties: List[str]
    ) -> float:
        """Calculate overall confidence level (0.0-1.0)."""
        base_confidence = self._confidence_to_numeric(hypothesis.confidence_level)
        
        # Adjust for number of successful validations
        validation_bonus = min(0.2, len(cycles) * 0.05)
        
        # Adjust for uncertainties
        uncertainty_penalty = min(0.3, len(uncertainties) * 0.03)
        
        return max(0.0, min(1.0, base_confidence + validation_bonus - uncertainty_penalty))
    
    # Helper methods
    
    def _extract_assumptions(self, scenario: str, domain: Optional[str]) -> List[str]:
        """Extract assumptions from scenario."""
        assumptions = ["Solution is technically feasible", "Resources are available"]
        
        if domain:
            template = self.DOMAIN_TEMPLATES.get(domain, {})
            focus_areas = template.get("focus_areas", [])
            assumptions.extend([f"{area} can be optimized" for area in focus_areas[:2]])
        
        return assumptions
    
    def _generate_success_criteria(self, scenario: str, domain: Optional[str]) -> List[str]:
        """Generate success criteria."""
        criteria = ["Measurable improvement achieved", "Stakeholder satisfaction"]
        
        if domain:
            template = self.DOMAIN_TEMPLATES.get(domain, {})
            metrics = template.get("metrics", [])
            criteria.extend([f"Improvement in {metric}" for metric in metrics[:2]])
        
        return criteria
    
    def _confidence_to_numeric(self, confidence: ConfidenceLevel) -> float:
        """Convert confidence level to numeric value."""
        mapping = {
            ConfidenceLevel.VERY_LOW: 0.1,
            ConfidenceLevel.LOW: 0.3,
            ConfidenceLevel.MEDIUM: 0.5,
            ConfidenceLevel.HIGH: 0.7,
            ConfidenceLevel.VERY_HIGH: 0.9
        }
        return mapping.get(confidence, 0.5)
    
    def _update_confidence_level(
        self,
        current: ConfidenceLevel,
        learnings: List[Learning]
    ) -> ConfidenceLevel:
        """Update confidence based on learnings."""
        # Count positive learnings
        positive_learnings = sum(1 for l in learnings 
                               if l.learning_type in [LearningType.CONFIRMATION, LearningType.PARTIAL])
        
        # Progress confidence if mostly positive
        if positive_learnings > len(learnings) / 2:
            progression = [
                ConfidenceLevel.VERY_LOW,
                ConfidenceLevel.LOW,
                ConfidenceLevel.MEDIUM,
                ConfidenceLevel.HIGH,
                ConfidenceLevel.VERY_HIGH
            ]
            current_idx = progression.index(current)
            new_idx = min(current_idx + 1, len(progression) - 1)
            return progression[new_idx]
        
        return current
    
    def _refine_assumptions(
        self,
        original: List[str],
        learnings: List[Learning]
    ) -> List[str]:
        """Refine assumptions based on learnings."""
        refined = original.copy()
        
        # Add new assumptions from unexpected discoveries
        for learning in learnings:
            if learning.learning_type == LearningType.UNEXPECTED:
                refined.append(f"New insight: {learning.key_insight[:50]}")
        
        return refined[:5]  # Keep manageable
    
    def _update_risks(self, cycle: ValidationCycle) -> List[str]:
        """Update risks based on cycle results."""
        risks = []
        
        # Add risks from refuted assumptions
        for learning in cycle.learnings:
            if learning.learning_type == LearningType.REFUTATION:
                risks.append(f"Risk identified: {learning.key_insight[:50]}")
        
        # Add limitation-based risks
        risks.extend(cycle.test_results.limitations[:2])
        
        return risks
    
    def _generate_methodology(self, hypothesis: Hypothesis, test_type: TestType) -> str:
        """Generate test methodology."""
        methodologies = {
            TestType.A_B_TEST: "Split test comparing variations",
            TestType.EXPERIMENT: "Controlled experiment with variables",
            TestType.PROTOTYPE: "Build and test working prototype",
            TestType.PILOT: "Limited rollout to test group",
            TestType.SURVEY: "Structured feedback collection",
            TestType.SIMULATION: "Model-based scenario testing",
            TestType.USER_TEST: "Direct user interaction testing",
            TestType.ANALYSIS: "Data analysis and modeling",
            TestType.TECHNICAL_TEST: "Technical performance validation",
            TestType.MARKET_TEST: "Market response evaluation"
        }
        return methodologies.get(test_type, "Structured validation approach")
    
    def _define_metrics(self, hypothesis: Hypothesis, test_type: TestType) -> List[str]:
        """Define metrics for the test."""
        base_metrics = ["Success rate", "Completion time"]
        
        type_specific = {
            TestType.A_B_TEST: ["Conversion rate", "Statistical significance"],
            TestType.USER_TEST: ["User satisfaction", "Task completion"],
            TestType.TECHNICAL_TEST: ["Performance metrics", "Error rate"],
            TestType.MARKET_TEST: ["Market response", "Revenue impact"]
        }
        
        return base_metrics + type_specific.get(test_type, ["Quality score"])
    
    def _identify_resources(self, test_type: TestType) -> List[str]:
        """Identify resources needed for test type."""
        resource_map = {
            TestType.PROTOTYPE: ["Development time", "Technical resources"],
            TestType.USER_TEST: ["Test participants", "Testing environment"],
            TestType.MARKET_TEST: ["Marketing budget", "Analytics tools"],
            TestType.EXPERIMENT: ["Lab resources", "Control environment"]
        }
        return resource_map.get(test_type, ["Time", "Personnel"])
    
    def _identify_controls(self, hypothesis: Hypothesis) -> List[str]:
        """Identify control variables."""
        return ["Environmental factors", "Sample selection", "Timing"]
    
    def _define_success_threshold(self, hypothesis: Hypothesis) -> str:
        """Define success threshold."""
        return "Meets or exceeds success criteria with statistical significance"
    
    def _generate_key_findings(self, success_rate: float, hypothesis: Hypothesis) -> List[str]:
        """Generate key findings based on success rate."""
        findings = []
        
        if success_rate > 0.8:
            findings.append("Strong validation of core hypothesis")
            findings.append("Success criteria exceeded")
        elif success_rate > 0.6:
            findings.append("Partial validation with caveats")
            findings.append("Some success criteria met")
        else:
            findings.append("Hypothesis needs revision")
            findings.append("Success criteria not met")
        
        findings.append(f"Overall success rate: {success_rate * 100:.1f}%")
        return findings
    
    def _generate_unexpected_observations(self, success_rate: float) -> List[str]:
        """Generate unexpected observations."""
        if success_rate > 0.7:
            return ["Higher than expected adoption in specific segment"]
        elif success_rate < 0.3:
            return ["Unexpected resistance to change identified"]
        return []
    
    def _determine_results_confidence(self, success_rate: float) -> ConfidenceLevel:
        """Determine confidence in results."""
        if success_rate > 0.8:
            return ConfidenceLevel.VERY_HIGH
        elif success_rate > 0.6:
            return ConfidenceLevel.HIGH
        elif success_rate > 0.4:
            return ConfidenceLevel.MEDIUM
        else:
            return ConfidenceLevel.LOW
    
    def _derive_implications(self, learning_type: LearningType, hypothesis: Hypothesis) -> List[str]:
        """Derive implications from learning type."""
        implications_map = {
            LearningType.CONFIRMATION: ["Proceed with implementation", "Scale approach"],
            LearningType.REFUTATION: ["Revise fundamental assumptions", "Try alternative approach"],
            LearningType.PARTIAL: ["Refine specific aspects", "Test variations"],
            LearningType.DIRECTIONAL: ["Continue exploration", "Gather more data"],
            LearningType.UNEXPECTED: ["Investigate new opportunity", "Adjust strategy"],
            LearningType.INCONCLUSIVE: ["Redesign test", "Clarify metrics"]
        }
        return implications_map.get(learning_type, ["Analyze further"])
    
    def _generate_action_items(self, learning_type: LearningType, hypothesis: Hypothesis) -> List[str]:
        """Generate action items based on learning type."""
        action_map = {
            LearningType.CONFIRMATION: ["Document successful approach", "Plan rollout"],
            LearningType.REFUTATION: ["Brainstorm alternatives", "Revisit assumptions"],
            LearningType.PARTIAL: ["Design targeted tests", "Iterate on solution"],
            LearningType.UNEXPECTED: ["Explore discovery", "Update hypothesis"]
        }
        return action_map.get(learning_type, ["Plan next test"])
    
    def _create_refined_statement(self, hypothesis: Hypothesis, learning: Learning) -> str:
        """Create refined hypothesis statement."""
        if learning.learning_type == LearningType.REFUTATION:
            return f"Alternative approach to {hypothesis.statement}"
        elif learning.learning_type == LearningType.PARTIAL:
            return f"{hypothesis.statement} with modifications"
        return hypothesis.statement
    
    def _estimate_improvement(self, learning: Learning) -> str:
        """Estimate expected improvement from refinement."""
        if learning.confidence_level == ConfidenceLevel.HIGH:
            return "Significant improvement expected"
        return "Moderate improvement expected"
    
    def _define_implementation_steps(self, learning: Learning) -> List[str]:
        """Define steps to implement refinement."""
        return [
            "Update hypothesis based on learnings",
            "Design new test approach",
            "Implement changes",
            "Validate improvements"
        ]
    
    def _determine_cycle_status(
        self,
        learnings: List[Learning],
        refinements: List[Refinement]
    ) -> ValidationStatus:
        """Determine validation cycle status."""
        if refinements:
            return ValidationStatus.REFINED
        elif learnings:
            return ValidationStatus.LEARNINGS_EXTRACTED
        else:
            return ValidationStatus.ANALYSIS_COMPLETE
    
    def _synthesize_learnings(self, all_learnings: List[Learning]) -> List[Learning]:
        """Synthesize and deduplicate learnings."""
        # Group by insight similarity
        unique_learnings = []
        seen_insights = set()
        
        for learning in all_learnings:
            insight_key = learning.key_insight[:30]
            if insight_key not in seen_insights:
                seen_insights.add(insight_key)
                unique_learnings.append(learning)
        
        return unique_learnings
    
    def _track_confidence_progression(
        self,
        cycles: List[ValidationCycle]
    ) -> Dict[int, ConfidenceLevel]:
        """Track confidence level progression."""
        return {
            cycle.cycle_number: cycle.hypothesis.confidence_level
            for cycle in cycles
        }
    
    def _is_significant_change(self, prev: str, curr: str) -> bool:
        """Check if hypothesis change is significant."""
        # Simple heuristic - could be more sophisticated
        return len(set(prev.split()) ^ set(curr.split())) > len(prev.split()) / 2
    
    def _describe_pivot(self, prev: str, curr: str) -> str:
        """Describe the nature of a pivot."""
        if "alternative" in curr.lower():
            return "Shifted to alternative approach"
        elif "modified" in curr.lower():
            return "Modified core assumptions"
        else:
            return "Significant strategy change"
    
    def _extract_tested_assumptions(self, learning: Learning) -> List[str]:
        """Extract which assumptions were tested."""
        # Simplified - would analyze learning content
        return []
    
    def _extract_success_factors(self, learning: Learning) -> List[str]:
        """Extract success factors from learning."""
        factors = []
        if "user" in learning.key_insight.lower():
            factors.append("Strong user focus")
        if "data" in learning.key_insight.lower():
            factors.append("Data-driven approach")
        if "iterative" in learning.key_insight.lower():
            factors.append("Iterative refinement")
        return factors
    
    def _evaluate_cycle_success(self, cycle: ValidationCycle) -> float:
        """Evaluate success of a validation cycle."""
        # Count positive learnings
        positive = sum(1 for l in cycle.learnings 
                      if l.learning_type in [LearningType.CONFIRMATION, LearningType.PARTIAL])
        total = len(cycle.learnings)
        return positive / total if total > 0 else 0.5


# FastMCP tool registration
@tool()
async def analyze_iterative_validation(
    scenario: str,
    domain_context: Optional[str] = None,
    initial_hypothesis: Optional[Dict[str, Any]] = None,
    validation_constraints: Optional[Dict[str, str]] = None,
    previous_cycles: Optional[List[Dict[str, Any]]] = None,
    target_confidence: str = "high",
    max_iterations: Optional[int] = None,
    test_preferences: Optional[List[str]] = None,
    complexity_level: str = "standard",
    session_id: str = "default"
) -> str:
    """
    Analyze using Iterative Validation Cycle for systematic hypothesis testing and refinement.
    
    This tool enables hypothesis-test-learn-refine cycles for empirical validation
    and continuous improvement in any domain requiring systematic experimentation.
    
    Args:
        scenario: The problem or question requiring iterative validation
        domain_context: Domain context (e.g., 'product_development', 'research', 'business', 'process_improvement')
        initial_hypothesis: Starting hypothesis with statement, assumptions, success_criteria
        validation_constraints: Constraints like timeline, budget, resources
        previous_cycles: Previous validation cycles if continuing iteration
        target_confidence: Target confidence level to achieve
        max_iterations: Maximum number of iterations allowed
        test_preferences: Preferred test types (experiment, prototype, pilot, etc.)
        complexity_level: Analysis complexity ('quick', 'standard', 'comprehensive')
        session_id: Session identifier for context
    
    Returns:
        Comprehensive iterative validation analysis with cycles, learnings, and recommendations
    """
    
    # Convert inputs to proper types
    if initial_hypothesis:
        initial_hypothesis_obj = Hypothesis(**initial_hypothesis)
    else:
        initial_hypothesis_obj = None
    
    if previous_cycles:
        previous_cycles_obj = [ValidationCycle(**cycle) for cycle in previous_cycles]
    else:
        previous_cycles_obj = None
    
    if test_preferences:
        test_preferences_enum = [TestType(pref) for pref in test_preferences]
    else:
        test_preferences_enum = None
    
    target_confidence_enum = ConfidenceLevel(target_confidence)
    
    # Create input
    input_data = IterativeValidationInput(
        scenario=scenario,
        domain_context=domain_context,
        initial_hypothesis=initial_hypothesis_obj,
        validation_constraints=validation_constraints,
        previous_cycles=previous_cycles_obj,
        target_confidence=target_confidence_enum,
        max_iterations=max_iterations,
        test_preferences=test_preferences_enum,
        complexity_level=complexity_level,
        session_id=session_id
    )
    
    # Create tool instance
    tool_instance = IterativeValidationTool()
    
    # Mock context for logging
    from types import SimpleNamespace
    context = SimpleNamespace(
        progress=lambda msg, pct: None,
        info=lambda msg: None,
        debug=lambda msg: None,
        error=lambda msg: None
    )
    
    # Analyze
    result = await tool_instance.analyze_iterative_validation(
        scenario=input_data.scenario,
        domain_context=input_data.domain_context,
        initial_hypothesis=input_data.initial_hypothesis,
        validation_constraints=input_data.validation_constraints,
        previous_cycles=input_data.previous_cycles,
        target_confidence=input_data.target_confidence,
        max_iterations=input_data.max_iterations,
        test_preferences=input_data.test_preferences,
        context=context
    )
    
    # Format output
    output = f"""## Iterative Validation Analysis

**Scenario**: {result.input_scenario}

### Current Hypothesis
**Statement**: {result.current_hypothesis.statement}
**Confidence Level**: {result.current_hypothesis.confidence_level}
**Rationale**: {result.current_hypothesis.rationale}

### Validation Progress
**Cycles Completed**: {len(result.validation_cycles)}
**Convergence Analysis**: {result.convergence_analysis}

### Latest Cycle Results
"""
    
    if result.validation_cycles:
        latest_cycle = result.validation_cycles[-1]
        output += f"""
**Cycle {latest_cycle.cycle_number}**:
- Test Type: {latest_cycle.test_design.test_type}
- Methodology: {latest_cycle.test_design.methodology}
- Key Findings: {', '.join(latest_cycle.test_results.key_findings[:3])}
- Status: {latest_cycle.status}
"""
    
    output += f"""
### Cumulative Learnings
"""
    for i, learning in enumerate(result.cumulative_learnings[:5], 1):
        output += f"""
{i}. **{learning.key_insight}**
   - Type: {learning.learning_type}
   - Confidence: {learning.confidence_level}
   - Implications: {', '.join(learning.implications[:2])}
"""
    
    if result.key_pivots:
        output += f"""
### Key Pivots
"""
        for pivot in result.key_pivots[:3]:
            output += f"- {pivot}\n"
    
    output += f"""
### Remaining Uncertainties
"""
    for uncertainty in result.remaining_uncertainties[:5]:
        output += f"- {uncertainty}\n"
    
    output += f"""
### Recommended Next Steps
"""
    for i, step in enumerate(result.recommended_next_steps[:5], 1):
        output += f"{i}. {step}\n"
    
    if result.methodology_insights:
        output += f"""
### Methodology Insights
"""
        for insight in result.methodology_insights[:3]:
            output += f"- {insight}\n"
    
    output += f"""
### Overall Assessment
{result.overall_assessment}

**Overall Confidence**: {result.confidence_level:.1%}
"""
    
    return output