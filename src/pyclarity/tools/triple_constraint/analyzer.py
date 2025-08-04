"""
Triple Constraint Analyzer

Analyzes trade-offs between three competing dimensions and identifies
optimal strategies for constraint management and balance.
"""

from typing import List, Dict, Optional, Any
import asyncio

from ..base import BaseCognitiveAnalyzer
from .models import (
    TripleConstraintContext,
    TripleConstraintResult,
    Constraint,
    Tradeoff,
    Scenario,
    ConstraintDimension,
    ConstraintPriority,
    TradeoffImpact,
    OptimizationStrategy,
    ComplexityLevel
)


class TripleConstraintAnalyzer(BaseCognitiveAnalyzer):
    """
    Analyzer for triple constraint optimization.
    
    Helps manage competing constraints by analyzing trade-offs and
    identifying optimal balance strategies.
    """
    
    # Domain-specific constraint sets
    DOMAIN_CONSTRAINTS = {
        "project_management": [
            (ConstraintDimension.SCOPE, "Project deliverables and features"),
            (ConstraintDimension.TIME, "Schedule and deadlines"),
            (ConstraintDimension.BUDGET, "Financial resources and costs")
        ],
        "software_development": [
            (ConstraintDimension.QUALITY, "Code quality and reliability"),
            (ConstraintDimension.SPEED, "Development velocity and time to market"),
            (ConstraintDimension.COST, "Development resources and expenses")
        ],
        "product_design": [
            (ConstraintDimension.FEATURES, "Product capabilities and functionality"),
            (ConstraintDimension.USABILITY, "User experience and simplicity"),
            (ConstraintDimension.PERFORMANCE, "Speed and efficiency")
        ],
        "business_strategy": [
            (ConstraintDimension.GROWTH, "Market expansion and scaling"),
            (ConstraintDimension.PROFIT, "Financial returns and margins"),
            (ConstraintDimension.SUSTAINABILITY, "Long-term viability")
        ]
    }
    
    async def analyze(
        self, 
        context: TripleConstraintContext
    ) -> TripleConstraintResult:
        """
        Perform triple constraint analysis.
        
        Args:
            context: The scenario requiring constraint analysis
            
        Returns:
            TripleConstraintResult with complete constraint analysis
        """
        # Identify or generate constraints
        constraints = await self._identify_constraints(context)
        
        # Analyze current state
        current_state = await self._analyze_current_state(
            constraints,
            context
        )
        
        # Identify trade-offs
        tradeoffs = await self._identify_tradeoffs(
            constraints,
            context
        )
        
        # Generate optimization scenarios
        scenarios = await self._generate_scenarios(
            constraints,
            tradeoffs,
            context
        )
        
        # Select optimal scenario
        optimal_scenario = await self._select_optimal_scenario(
            scenarios,
            context
        )
        
        # Develop implementation strategy
        implementation_plan = await self._develop_implementation_plan(
            optimal_scenario,
            constraints,
            context
        )
        
        # Identify risk mitigation
        risk_mitigation = await self._identify_risk_mitigation(
            optimal_scenario,
            tradeoffs,
            context
        )
        
        # Create monitoring metrics
        monitoring_metrics = await self._create_monitoring_metrics(
            constraints,
            optimal_scenario
        )
        
        # Generate communication plan
        communication_plan = await self._generate_communication_plan(
            optimal_scenario,
            constraints,
            context
        )
        
        # Calculate success probability
        success_probability = self._calculate_success_probability(
            optimal_scenario,
            constraints,
            context
        )
        
        # Generate overall assessment
        overall_assessment = await self._generate_overall_assessment(
            constraints,
            optimal_scenario,
            success_probability,
            context
        )
        
        # Calculate confidence
        confidence_score = self._calculate_confidence(
            constraints,
            scenarios,
            context
        )
        
        return TripleConstraintResult(
            input_scenario=context.scenario,
            identified_constraints=constraints,
            current_state_analysis=current_state,
            tradeoff_analysis=tradeoffs,
            optimization_scenarios=scenarios,
            recommended_scenario=optimal_scenario,
            implementation_plan=implementation_plan,
            risk_mitigation_strategies=risk_mitigation,
            monitoring_metrics=monitoring_metrics,
            stakeholder_communication=communication_plan,
            success_probability=success_probability,
            overall_assessment=overall_assessment,
            confidence_score=confidence_score
        )
    
    async def _identify_constraints(
        self,
        context: TripleConstraintContext
    ) -> List[Constraint]:
        """Identify the three constraints for analysis."""
        # Use predefined if available
        if context.predefined_constraints:
            return context.predefined_constraints
        
        # Check domain-specific
        if context.domain:
            for domain, template in self.DOMAIN_CONSTRAINTS.items():
                if domain in context.domain.lower():
                    return await self._create_constraints_from_template(
                        template,
                        context
                    )
        
        # Generate generic constraints
        return await self._generate_generic_constraints(context)
    
    async def _create_constraints_from_template(
        self,
        template: List[tuple],
        context: TripleConstraintContext
    ) -> List[Constraint]:
        """Create constraints from domain template."""
        constraints = []
        
        for dimension, description in template:
            constraint = Constraint(
                dimension=dimension,
                description=description,
                current_value=50.0,  # Default midpoint
                target_value=80.0,   # Default target
                min_acceptable=30.0, # Default minimum
                max_possible=100.0,  # Default maximum
                priority=ConstraintPriority.HIGH,
                flexibility=0.5,
                impact_factors=[
                    "Resource availability",
                    "External dependencies",
                    "Stakeholder expectations"
                ]
            )
            constraints.append(constraint)
        
        return constraints
    
    async def _generate_generic_constraints(
        self,
        context: TripleConstraintContext
    ) -> List[Constraint]:
        """Generate generic triple constraints."""
        # Default to classic project triangle
        return [
            Constraint(
                dimension=ConstraintDimension.QUALITY,
                description="Quality or scope of deliverables",
                current_value=60.0,
                target_value=90.0,
                min_acceptable=50.0,
                max_possible=100.0,
                priority=ConstraintPriority.HIGH,
                flexibility=0.3,
                impact_factors=["Standards", "Requirements", "Expectations"]
            ),
            Constraint(
                dimension=ConstraintDimension.TIME,
                description="Timeline and schedule",
                current_value=40.0,
                target_value=80.0,
                min_acceptable=30.0,
                max_possible=100.0,
                priority=ConstraintPriority.MEDIUM,
                flexibility=0.5,
                impact_factors=["Resources", "Dependencies", "Complexity"]
            ),
            Constraint(
                dimension=ConstraintDimension.COST,
                description="Budget and resources",
                current_value=70.0,
                target_value=60.0,
                min_acceptable=40.0,
                max_possible=100.0,
                priority=ConstraintPriority.MEDIUM,
                flexibility=0.4,
                impact_factors=["Market rates", "Efficiency", "Scope"]
            )
        ]
    
    async def _analyze_current_state(
        self,
        constraints: List[Constraint],
        context: TripleConstraintContext
    ) -> str:
        """Analyze current state of constraints."""
        # Identify constraint status
        over_constraints = [
            c for c in constraints 
            if c.current_value > c.target_value
        ]
        under_constraints = [
            c for c in constraints
            if c.current_value < c.min_acceptable
        ]
        
        analysis = "Current state analysis:\n"
        
        if over_constraints:
            analysis += f"- {len(over_constraints)} constraint(s) exceeding targets\n"
            for c in over_constraints:
                analysis += f"  • {c.dimension}: {c.current_value:.0f}% (target: {c.target_value:.0f}%)\n"
        
        if under_constraints:
            analysis += f"- {len(under_constraints)} constraint(s) below minimum\n"
            for c in under_constraints:
                analysis += f"  • {c.dimension}: {c.current_value:.0f}% (min: {c.min_acceptable:.0f}%)\n"
        
        # Overall balance assessment
        variance = max(c.current_value for c in constraints) - min(c.current_value for c in constraints)
        if variance > 40:
            analysis += "- Significant imbalance detected between constraints\n"
        elif variance > 20:
            analysis += "- Moderate imbalance between constraints\n"
        else:
            analysis += "- Constraints relatively balanced\n"
        
        return analysis
    
    async def _identify_tradeoffs(
        self,
        constraints: List[Constraint],
        context: TripleConstraintContext
    ) -> List[Tradeoff]:
        """Identify trade-offs between constraints."""
        tradeoffs = []
        
        # Analyze each pair of constraints
        for i in range(len(constraints)):
            for j in range(i + 1, len(constraints)):
                constraint_a = constraints[i]
                constraint_b = constraints[j]
                
                # Determine relationship
                if self._are_competing(constraint_a, constraint_b):
                    tradeoff = Tradeoff(
                        constraint_a=constraint_a.dimension,
                        constraint_b=constraint_b.dimension,
                        relationship_type="inverse",
                        description=f"Improving {constraint_a.dimension} typically reduces {constraint_b.dimension}",
                        impact_factor=0.7,
                        examples=[
                            f"Increasing {constraint_a.dimension} by 20% may reduce {constraint_b.dimension} by 15%",
                            "Historical data shows strong negative correlation"
                        ],
                        mitigation_strategies=[
                            "Find creative solutions that benefit both",
                            "Optimize processes to reduce impact",
                            "Accept controlled trade-off"
                        ]
                    )
                else:
                    tradeoff = Tradeoff(
                        constraint_a=constraint_a.dimension,
                        constraint_b=constraint_b.dimension,
                        relationship_type="complementary",
                        description=f"{constraint_a.dimension} and {constraint_b.dimension} can be improved together",
                        impact_factor=0.3,
                        examples=[
                            "Process improvements benefit both dimensions",
                            "Synergies exist between these constraints"
                        ],
                        mitigation_strategies=[
                            "Leverage synergies",
                            "Coordinate improvements"
                        ]
                    )
                
                tradeoffs.append(tradeoff)
        
        return tradeoffs
    
    async def _generate_scenarios(
        self,
        constraints: List[Constraint],
        tradeoffs: List[Tradeoff],
        context: TripleConstraintContext
    ) -> List[Scenario]:
        """Generate optimization scenarios."""
        scenarios = []
        
        # Scenario 1: Balanced approach
        balanced_targets = {}
        for c in constraints:
            balanced_targets[c.dimension] = (c.target_value + c.current_value) / 2
        
        scenarios.append(Scenario(
            scenario_id="balanced",
            name="Balanced Optimization",
            description="Moderate improvements across all constraints",
            target_values=balanced_targets,
            strategy=OptimizationStrategy.BALANCED,
            expected_outcomes=[
                "Steady progress on all fronts",
                "Lower risk of failure",
                "Stakeholder satisfaction"
            ],
            required_changes=[
                "Incremental process improvements",
                "Resource reallocation",
                "Stakeholder alignment"
            ],
            timeline="Medium-term (3-6 months)",
            resource_requirements="Moderate",
            risk_level="Low",
            success_probability=0.75
        ))
        
        # Scenario 2: Priority focus
        priority_constraint = max(constraints, key=lambda c: c.priority.value)
        priority_targets = {}
        for c in constraints:
            if c == priority_constraint:
                priority_targets[c.dimension] = c.target_value
            else:
                priority_targets[c.dimension] = c.current_value * 0.9
        
        scenarios.append(Scenario(
            scenario_id="priority",
            name="Priority Constraint Focus",
            description=f"Maximize {priority_constraint.dimension} at controlled cost to others",
            target_values=priority_targets,
            strategy=OptimizationStrategy.MAXIMIZE_ONE,
            expected_outcomes=[
                f"Significant improvement in {priority_constraint.dimension}",
                "Some degradation in other areas",
                "Clear strategic direction"
            ],
            required_changes=[
                f"Resource concentration on {priority_constraint.dimension}",
                "Accept trade-offs",
                "Clear communication of priorities"
            ],
            timeline="Short-term (1-3 months)",
            resource_requirements="Focused",
            risk_level="Medium",
            success_probability=0.65
        ))
        
        # Scenario 3: Sequential optimization
        sequential_targets = {}
        for idx, c in enumerate(constraints):
            # Improve constraints one at a time
            if idx == 0:
                sequential_targets[c.dimension] = c.target_value * 0.8
            else:
                sequential_targets[c.dimension] = c.current_value
        
        scenarios.append(Scenario(
            scenario_id="sequential",
            name="Sequential Optimization",
            description="Improve constraints one at a time in priority order",
            target_values=sequential_targets,
            strategy=OptimizationStrategy.SEQUENTIAL,
            expected_outcomes=[
                "Clear milestones",
                "Easier to manage",
                "Learn and adapt between phases"
            ],
            required_changes=[
                "Phased approach",
                "Milestone planning",
                "Iterative improvements"
            ],
            timeline="Long-term (6-12 months)",
            resource_requirements="Sustained",
            risk_level="Low",
            success_probability=0.70
        ))
        
        return scenarios
    
    async def _select_optimal_scenario(
        self,
        scenarios: List[Scenario],
        context: TripleConstraintContext
    ) -> Scenario:
        """Select optimal scenario based on context."""
        # Score scenarios based on multiple criteria
        scenario_scores = {}
        
        for scenario in scenarios:
            score = 0
            
            # Success probability weight
            score += scenario.success_probability * 30
            
            # Risk tolerance matching
            if context.risk_tolerance == "high" and scenario.risk_level == "Medium":
                score += 10
            elif context.risk_tolerance == "low" and scenario.risk_level == "Low":
                score += 15
            
            # Timeline matching
            if context.timeline_flexibility == "high" and "Long-term" in scenario.timeline:
                score += 10
            elif context.timeline_flexibility == "low" and "Short-term" in scenario.timeline:
                score += 15
            
            # Strategy preference
            if scenario.strategy == OptimizationStrategy.BALANCED:
                score += 10  # Generally preferred
            
            scenario_scores[scenario.scenario_id] = score
        
        # Select highest scoring scenario
        optimal_id = max(scenario_scores, key=scenario_scores.get)
        return next(s for s in scenarios if s.scenario_id == optimal_id)
    
    async def _develop_implementation_plan(
        self,
        scenario: Scenario,
        constraints: List[Constraint],
        context: TripleConstraintContext
    ) -> List[str]:
        """Develop implementation plan for selected scenario."""
        plan = []
        
        # Phase 1: Preparation
        plan.append("Phase 1 - Preparation (Weeks 1-2):")
        plan.append("• Stakeholder alignment on chosen approach")
        plan.append("• Resource allocation and team formation")
        plan.append("• Baseline metrics establishment")
        
        # Phase 2: Initial changes
        plan.append("\nPhase 2 - Initial Implementation (Weeks 3-6):")
        for change in scenario.required_changes[:2]:
            plan.append(f"• {change}")
        plan.append("• Monitor early indicators")
        
        # Phase 3: Full implementation
        plan.append("\nPhase 3 - Full Implementation (Weeks 7-12):")
        plan.append("• Scale successful initiatives")
        plan.append("• Address emerging challenges")
        plan.append("• Continuous optimization")
        
        # Phase 4: Stabilization
        plan.append("\nPhase 4 - Stabilization (Weeks 13-16):")
        plan.append("• Lock in improvements")
        plan.append("• Document learnings")
        plan.append("• Plan next optimization cycle")
        
        return plan
    
    async def _identify_risk_mitigation(
        self,
        scenario: Scenario,
        tradeoffs: List[Tradeoff],
        context: TripleConstraintContext
    ) -> List[str]:
        """Identify risk mitigation strategies."""
        strategies = []
        
        # Scenario-specific risks
        if scenario.risk_level == "Medium":
            strategies.append("Implement phased rollout with go/no-go gates")
            strategies.append("Maintain rollback capability")
        
        # Trade-off risks
        for tradeoff in tradeoffs:
            if tradeoff.relationship_type == "inverse":
                strategies.extend(tradeoff.mitigation_strategies[:2])
        
        # General risk mitigation
        strategies.extend([
            "Regular stakeholder communication",
            "Continuous monitoring of all constraints",
            "Flexibility to adjust approach based on results",
            "Maintain contingency resources"
        ])
        
        return list(set(strategies))[:6]  # Top 6 unique strategies
    
    async def _create_monitoring_metrics(
        self,
        constraints: List[Constraint],
        scenario: Scenario
    ) -> List[str]:
        """Create monitoring metrics for constraint management."""
        metrics = []
        
        # Constraint-specific metrics
        for constraint in constraints:
            metrics.append(
                f"{constraint.dimension} performance: "
                f"Current vs Target ({scenario.target_values[constraint.dimension]:.0f}%)"
            )
        
        # Balance metrics
        metrics.append("Constraint balance index: Variance between dimensions")
        
        # Progress metrics
        metrics.append("Implementation progress: % of plan completed")
        metrics.append("Resource utilization: Actual vs planned")
        
        # Outcome metrics
        metrics.append("Stakeholder satisfaction scores")
        metrics.append("Risk materialization tracking")
        
        return metrics
    
    async def _generate_communication_plan(
        self,
        scenario: Scenario,
        constraints: List[Constraint],
        context: TripleConstraintContext
    ) -> List[str]:
        """Generate stakeholder communication plan."""
        plan = []
        
        # Key messages
        plan.append(f"Key message: {scenario.name} - {scenario.description}")
        
        # Stakeholder-specific communication
        if context.primary_stakeholders:
            for stakeholder in context.primary_stakeholders[:3]:
                plan.append(f"For {stakeholder}: Focus on relevant constraint impacts")
        else:
            plan.append("For executives: Strategic rationale and expected outcomes")
            plan.append("For teams: Implementation details and support needed")
            plan.append("For customers: Timeline and quality expectations")
        
        # Communication frequency
        plan.append("Weekly status updates during implementation")
        plan.append("Monthly executive briefings")
        plan.append("Immediate escalation for significant deviations")
        
        return plan
    
    def _calculate_success_probability(
        self,
        scenario: Scenario,
        constraints: List[Constraint],
        context: TripleConstraintContext
    ) -> float:
        """Calculate probability of successful implementation."""
        base_probability = scenario.success_probability
        
        # Adjust for constraint flexibility
        avg_flexibility = sum(c.flexibility for c in constraints) / len(constraints)
        base_probability += (avg_flexibility - 0.5) * 0.2
        
        # Adjust for context factors
        if context.organizational_readiness == "high":
            base_probability += 0.1
        elif context.organizational_readiness == "low":
            base_probability -= 0.1
        
        # Ensure within bounds
        return max(0.2, min(0.95, base_probability))
    
    async def _generate_overall_assessment(
        self,
        constraints: List[Constraint],
        scenario: Scenario,
        success_probability: float,
        context: TripleConstraintContext
    ) -> str:
        """Generate overall assessment of constraint optimization approach."""
        assessment = f"Triple constraint analysis for '{context.scenario}' reveals "
        
        # Constraint balance
        variance = max(c.current_value for c in constraints) - min(c.current_value for c in constraints)
        if variance > 40:
            assessment += "significant imbalance requiring strategic intervention. "
        else:
            assessment += "manageable constraint tensions. "
        
        # Recommended approach
        assessment += f"The {scenario.name} approach offers the best balance of "
        assessment += f"risk ({scenario.risk_level}) and reward, with {success_probability*100:.0f}% "
        assessment += "probability of success. "
        
        # Key success factors
        assessment += "Success depends on: "
        if scenario.strategy == OptimizationStrategy.BALANCED:
            assessment += "maintaining discipline across all constraints, "
        elif scenario.strategy == OptimizationStrategy.MAXIMIZE_ONE:
            assessment += "clear prioritization and stakeholder buy-in, "
        else:
            assessment += "effective phase management, "
        
        assessment += "proactive risk mitigation, and continuous monitoring. "
        
        # Timeline expectation
        assessment += f"Expected timeline: {scenario.timeline}."
        
        return assessment
    
    def _calculate_confidence(
        self,
        constraints: List[Constraint],
        scenarios: List[Scenario],
        context: TripleConstraintContext
    ) -> float:
        """Calculate confidence in the analysis."""
        confidence = 0.7  # Base confidence
        
        # Quality of input
        if context.predefined_constraints:
            confidence += 0.1
        
        if context.domain:
            confidence += 0.05
        
        # Analysis completeness
        if len(scenarios) >= 3:
            confidence += 0.05
        
        # Context factors
        if context.organizational_readiness:
            confidence += 0.05
        
        return min(0.95, confidence)
    
    def _are_competing(
        self,
        constraint_a: Constraint,
        constraint_b: Constraint
    ) -> bool:
        """Determine if two constraints compete."""
        competing_pairs = [
            (ConstraintDimension.TIME, ConstraintDimension.QUALITY),
            (ConstraintDimension.COST, ConstraintDimension.QUALITY),
            (ConstraintDimension.SPEED, ConstraintDimension.QUALITY),
            (ConstraintDimension.SCOPE, ConstraintDimension.TIME),
            (ConstraintDimension.FEATURES, ConstraintDimension.USABILITY)
        ]
        
        for pair in competing_pairs:
            if (constraint_a.dimension in pair and constraint_b.dimension in pair):
                return True
        
        return False