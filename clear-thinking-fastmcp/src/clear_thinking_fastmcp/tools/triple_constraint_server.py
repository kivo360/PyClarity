# Clear Thinking FastMCP Server - Triple Constraint Thinking Tool

"""
Triple Constraint Thinking implementation for FastMCP server.

This tool analyzes any situation requiring balance between three competing
dimensions, helping identify trade-offs and optimization strategies.
"""

from typing import Dict, List, Optional, Any
import asyncio
from fastmcp import Context

from ..models.triple_constraint import (
    TripleConstraintInput,
    TripleConstraintAnalysis,
    ConstraintSet,
    TradeOffAnalysis,
    OptimizationRecommendation,
    OptimizationStrategy
)
from .base import CognitiveToolBase


class TripleConstraintTool(CognitiveToolBase):
    """Implements Triple Constraint Thinking analysis."""
    
    # Domain-specific constraint mappings
    DOMAIN_CONSTRAINTS = {
        "project_management": {
            "dimension_a": "scope",
            "dimension_b": "time",
            "dimension_c": "budget"
        },
        "software_development": {
            "dimension_a": "features",
            "dimension_b": "timeline",
            "dimension_c": "quality"
        },
        "engineering": {
            "dimension_a": "performance",
            "dimension_b": "cost",
            "dimension_c": "reliability"
        },
        "business_strategy": {
            "dimension_a": "quality",
            "dimension_b": "speed",
            "dimension_c": "price"
        },
        "product_development": {
            "dimension_a": "innovation",
            "dimension_b": "time_to_market",
            "dimension_c": "resources"
        }
    }
    
    async def analyze_triple_constraint(
        self,
        input_data: TripleConstraintInput,
        context: Context
    ) -> TripleConstraintAnalysis:
        """Main method to analyze triple constraints."""
        
        await context.progress("Starting triple constraint analysis", 0.1)
        
        # Identify constraints
        constraints = await self._identify_constraints(input_data, context)
        await context.progress("Constraints identified", 0.3)
        
        # Analyze current state
        current_state_analysis = await self._analyze_current_state(
            constraints, input_data, context
        )
        await context.progress("Current state analyzed", 0.4)
        
        # Analyze trade-offs
        trade_offs = await self._analyze_trade_offs(
            constraints, input_data, context
        )
        await context.progress("Trade-offs analyzed", 0.6)
        
        # Generate optimization recommendations
        recommendations = await self._generate_optimization_recommendations(
            constraints, trade_offs, input_data, context
        )
        await context.progress("Recommendations generated", 0.8)
        
        # Generate domain insights
        domain_insights = await self._generate_domain_insights(
            constraints, input_data, context
        )
        
        # Create visualization data
        viz_data = self._create_visualization_data(constraints)
        
        # Identify key decisions
        key_decisions = await self._identify_key_decisions(
            constraints, input_data, context
        )
        
        # Define success metrics
        success_metrics = await self._define_success_metrics(
            constraints, input_data, context
        )
        
        # Overall assessment
        overall_assessment = await self._create_overall_assessment(
            constraints, trade_offs, recommendations, context
        )
        
        # Calculate confidence
        confidence = self._calculate_confidence(
            constraints, trade_offs, recommendations
        )
        
        await context.progress("Analysis complete", 1.0)
        
        return TripleConstraintAnalysis(
            input_scenario=input_data.scenario,
            identified_constraints=constraints,
            current_state_analysis=current_state_analysis,
            trade_off_analyses=trade_offs,
            optimization_recommendations=recommendations,
            domain_specific_insights=domain_insights,
            visual_representation=viz_data,
            key_decisions=key_decisions,
            success_metrics=success_metrics,
            overall_assessment=overall_assessment,
            confidence_level=confidence
        )
    
    async def _identify_constraints(
        self,
        input_data: TripleConstraintInput,
        context: Context
    ) -> ConstraintSet:
        """Identify the three competing constraints."""
        
        if input_data.constraints:
            return input_data.constraints
        
        # Use domain knowledge if available
        if input_data.domain_context and input_data.domain_context in self.DOMAIN_CONSTRAINTS:
            domain_constraints = self.DOMAIN_CONSTRAINTS[input_data.domain_context]
            dimension_a = domain_constraints["dimension_a"]
            dimension_b = domain_constraints["dimension_b"]
            dimension_c = domain_constraints["dimension_c"]
        else:
            # Extract from scenario
            dimension_a, dimension_b, dimension_c = await self._extract_constraints_from_scenario(
                input_data.scenario, context
            )
        
        # Initialize with balanced values if not provided
        current_values = [0.5, 0.5, 0.5]
        
        return ConstraintSet(
            dimension_a=dimension_a,
            dimension_b=dimension_b,
            dimension_c=dimension_c,
            current_values=current_values,
            target_values=None
        )
    
    async def _extract_constraints_from_scenario(
        self,
        scenario: str,
        context: Context
    ) -> tuple[str, str, str]:
        """Extract constraints from scenario description."""
        
        scenario_lower = scenario.lower()
        
        # Look for common constraint patterns
        if "project" in scenario_lower or "develop" in scenario_lower:
            if "software" in scenario_lower or "app" in scenario_lower:
                return "features", "timeline", "quality"
            else:
                return "scope", "time", "budget"
        elif "product" in scenario_lower:
            return "quality", "speed", "cost"
        elif "system" in scenario_lower or "engineer" in scenario_lower:
            return "performance", "cost", "reliability"
        elif "business" in scenario_lower or "strategy" in scenario_lower:
            return "quality", "speed", "price"
        else:
            # Generic constraints
            return "dimension_a", "dimension_b", "dimension_c"
    
    async def _analyze_current_state(
        self,
        constraints: ConstraintSet,
        input_data: TripleConstraintInput,
        context: Context
    ) -> str:
        """Analyze the current state of constraints."""
        
        values = constraints.current_values
        mean = sum(values) / 3
        variance = sum((v - mean) ** 2 for v in values) / 3
        balance_score = 1.0 - (variance * 10)  # Scale to 0-1
        
        # Identify highest and lowest dimensions
        max_idx = values.index(max(values))
        min_idx = values.index(min(values))
        
        dimensions = [
            constraints.dimension_a,
            constraints.dimension_b,
            constraints.dimension_c
        ]
        
        analysis = f"Current constraint balance analysis:\n\n"
        
        if balance_score > 0.8:
            analysis += f"✅ **Well-balanced constraints** (balance score: {balance_score:.2f})\n"
            analysis += f"All three dimensions are relatively aligned.\n"
        elif balance_score > 0.6:
            analysis += f"⚠️ **Moderate imbalance** (balance score: {balance_score:.2f})\n"
            analysis += f"Some optimization needed to achieve better balance.\n"
        else:
            analysis += f"❌ **Significant imbalance** (balance score: {balance_score:.2f})\n"
            analysis += f"Major adjustments required for sustainable balance.\n"
        
        analysis += f"\n**Current emphasis:**\n"
        analysis += f"- Highest: {dimensions[max_idx]} ({values[max_idx]:.2f})\n"
        analysis += f"- Lowest: {dimensions[min_idx]} ({values[min_idx]:.2f})\n"
        
        if input_data.optimization_goal:
            analysis += f"\n**Optimization goal:** {input_data.optimization_goal}"
        
        return analysis
    
    async def _analyze_trade_offs(
        self,
        constraints: ConstraintSet,
        input_data: TripleConstraintInput,
        context: Context
    ) -> List[TradeOffAnalysis]:
        """Analyze trade-offs between constraint dimensions."""
        
        trade_offs = []
        dimensions = [
            constraints.dimension_a,
            constraints.dimension_b,
            constraints.dimension_c
        ]
        
        # Analyze each pair of dimensions
        pairs = [(0, 1), (0, 2), (1, 2)]
        
        for i, j in pairs:
            dim_i, dim_j = dimensions[i], dimensions[j]
            
            # Generate trade-off analysis
            relationship = await self._analyze_dimension_relationship(
                dim_i, dim_j, input_data.domain_context
            )
            
            impact_score = await self._calculate_trade_off_impact(
                dim_i, dim_j, constraints.current_values[i], constraints.current_values[j]
            )
            
            examples = await self._generate_trade_off_examples(
                dim_i, dim_j, input_data.domain_context
            )
            
            mitigation_options = await self._generate_mitigation_options(
                dim_i, dim_j, relationship
            )
            
            trade_offs.append(TradeOffAnalysis(
                relationship=relationship,
                impact_score=impact_score,
                examples=examples,
                mitigation_options=mitigation_options
            ))
        
        return trade_offs
    
    async def _analyze_dimension_relationship(
        self,
        dim1: str,
        dim2: str,
        domain_context: Optional[str]
    ) -> str:
        """Analyze the relationship between two dimensions."""
        
        # Common relationships
        relationships = {
            ("scope", "time"): "Expanding scope directly increases time requirements",
            ("scope", "budget"): "More scope requires proportionally more budget",
            ("time", "budget"): "Accelerating timeline often increases costs",
            ("features", "timeline"): "More features extend development timeline",
            ("features", "quality"): "More features can dilute overall quality",
            ("timeline", "quality"): "Rushed timeline typically reduces quality",
            ("performance", "cost"): "Higher performance usually requires more investment",
            ("performance", "reliability"): "Peak performance can compromise reliability",
            ("cost", "reliability"): "Lower cost may reduce reliability margins",
            ("quality", "speed"): "Increased speed often reduces quality",
            ("quality", "price"): "Higher quality typically commands higher price",
            ("speed", "price"): "Faster delivery often costs more"
        }
        
        # Check direct match
        key = (dim1, dim2)
        if key in relationships:
            return relationships[key]
        
        # Check reverse match
        key_reverse = (dim2, dim1)
        if key_reverse in relationships:
            return relationships[key_reverse]
        
        # Generic relationship
        return f"Changes in {dim1} typically affect {dim2} inversely"
    
    async def _calculate_trade_off_impact(
        self,
        dim1: str,
        dim2: str,
        val1: float,
        val2: float
    ) -> float:
        """Calculate the impact score of a trade-off."""
        
        # Base impact on current imbalance
        imbalance = abs(val1 - val2)
        
        # Some trade-offs are naturally stronger
        strong_trade_offs = [
            ("quality", "speed"),
            ("features", "timeline"),
            ("scope", "time"),
            ("performance", "cost")
        ]
        
        is_strong = any(
            (dim1 in pair and dim2 in pair) 
            for pair in strong_trade_offs
        )
        
        base_impact = 0.8 if is_strong else 0.6
        
        # Adjust based on current imbalance
        impact = base_impact + (imbalance * 0.3)
        
        return min(1.0, impact)
    
    async def _generate_trade_off_examples(
        self,
        dim1: str,
        dim2: str,
        domain_context: Optional[str]
    ) -> List[str]:
        """Generate concrete examples of trade-offs."""
        
        examples_map = {
            ("scope", "time"): [
                "Adding new feature requests extends project by 2-3 weeks",
                "Each additional requirement adds integration complexity",
                "Scope creep is the primary cause of timeline delays"
            ],
            ("features", "timeline"): [
                "Each feature requires design, development, and testing cycles",
                "Feature dependencies create scheduling constraints",
                "Complex features have non-linear time requirements"
            ],
            ("quality", "speed"): [
                "Rushed code contains 3x more defects on average",
                "Skipping code reviews saves time but increases technical debt",
                "Fast iterations reduce testing thoroughness"
            ],
            ("performance", "cost"): [
                "High-performance hardware costs exponentially more",
                "Optimization requires senior developer time",
                "Performance testing infrastructure is expensive"
            ]
        }
        
        key = (dim1, dim2)
        if key in examples_map:
            return examples_map[key]
        
        key_reverse = (dim2, dim1)
        if key_reverse in examples_map:
            return examples_map[key_reverse]
        
        # Generic examples
        return [
            f"Prioritizing {dim1} often requires compromising on {dim2}",
            f"Resources allocated to {dim1} reduce availability for {dim2}",
            f"Stakeholder pressure on {dim1} impacts {dim2} delivery"
        ]
    
    async def _generate_mitigation_options(
        self,
        dim1: str,
        dim2: str,
        relationship: str
    ) -> List[str]:
        """Generate options to mitigate trade-offs."""
        
        mitigation_strategies = {
            ("scope", "time"): [
                "Implement phased delivery approach",
                "Use MVP methodology to deliver core features first",
                "Establish clear scope change control process"
            ],
            ("features", "timeline"): [
                "Prioritize features using MoSCoW method",
                "Implement feature flags for gradual rollout",
                "Use parallel development streams where possible"
            ],
            ("quality", "speed"): [
                "Invest in automated testing infrastructure",
                "Implement continuous integration/deployment",
                "Use proven design patterns and frameworks",
                "Establish quality gates without blocking progress"
            ],
            ("performance", "cost"): [
                "Use cloud auto-scaling to optimize costs",
                "Implement performance budgets",
                "Profile and optimize critical paths only"
            ]
        }
        
        key = (dim1, dim2)
        if key in mitigation_strategies:
            return mitigation_strategies[key]
        
        key_reverse = (dim2, dim1)
        if key_reverse in mitigation_strategies:
            return mitigation_strategies[key_reverse]
        
        # Generic mitigation options
        return [
            f"Find creative solutions that improve both {dim1} and {dim2}",
            f"Identify waste that doesn't contribute to either dimension",
            f"Engage stakeholders to understand true priorities",
            f"Look for process improvements that benefit all constraints"
        ]
    
    async def _generate_optimization_recommendations(
        self,
        constraints: ConstraintSet,
        trade_offs: List[TradeOffAnalysis],
        input_data: TripleConstraintInput,
        context: Context
    ) -> List[OptimizationRecommendation]:
        """Generate recommendations for optimizing constraints."""
        
        recommendations = []
        values = constraints.current_values
        
        # Analyze current state
        mean = sum(values) / 3
        variance = sum((v - mean) ** 2 for v in values) / 3
        balance_score = 1.0 - (variance * 10)
        
        dimensions = [
            constraints.dimension_a,
            constraints.dimension_b,
            constraints.dimension_c
        ]
        
        # Identify primary strategy
        if balance_score > 0.8:
            # Already balanced - maintain
            strategy = OptimizationStrategy.BALANCED
            rationale = "Constraints are well-balanced; focus on maintaining equilibrium"
        else:
            # Find dimension needing attention
            min_idx = values.index(min(values))
            max_idx = values.index(max(values))
            
            if values[min_idx] < 0.4:
                # Critical dimension too low
                strategy = [
                    OptimizationStrategy.PRIORITIZE_A,
                    OptimizationStrategy.PRIORITIZE_B,
                    OptimizationStrategy.PRIORITIZE_C
                ][min_idx]
                rationale = f"{dimensions[min_idx]} is critically low and needs immediate attention"
            else:
                # Rebalance from highest
                strategy = OptimizationStrategy.MINIMIZE_TRADE_OFFS
                rationale = f"Reduce emphasis on {dimensions[max_idx]} to improve overall balance"
        
        # Generate action steps based on strategy
        action_steps = await self._generate_action_steps(
            strategy, constraints, input_data
        )
        
        # Expected outcomes
        expected_outcomes = await self._generate_expected_outcomes(
            strategy, constraints, values
        )
        
        # Identify risks
        risks = await self._identify_optimization_risks(
            strategy, constraints, trade_offs
        )
        
        # Calculate confidence
        confidence = self._calculate_recommendation_confidence(
            strategy, balance_score, input_data
        )
        
        recommendations.append(OptimizationRecommendation(
            strategy=strategy,
            rationale=rationale,
            action_steps=action_steps,
            expected_outcomes=expected_outcomes,
            risks=risks,
            confidence_level=confidence
        ))
        
        # Add alternative recommendation if confidence is moderate
        if confidence < 0.8:
            alt_recommendation = await self._generate_alternative_recommendation(
                constraints, strategy, input_data
            )
            if alt_recommendation:
                recommendations.append(alt_recommendation)
        
        return recommendations
    
    async def _generate_action_steps(
        self,
        strategy: OptimizationStrategy,
        constraints: ConstraintSet,
        input_data: TripleConstraintInput
    ) -> List[str]:
        """Generate concrete action steps for optimization strategy."""
        
        if strategy == OptimizationStrategy.BALANCED:
            return [
                "Continue monitoring all three constraints regularly",
                "Establish early warning indicators for imbalance",
                "Document current processes that maintain balance",
                "Create contingency plans for common disruptions"
            ]
        
        elif strategy == OptimizationStrategy.MINIMIZE_TRADE_OFFS:
            return [
                "Identify and eliminate non-value-adding activities",
                "Implement process improvements that benefit all constraints",
                "Seek innovative solutions that break traditional trade-offs",
                "Engage cross-functional teams for creative problem-solving"
            ]
        
        elif strategy in [OptimizationStrategy.PRIORITIZE_A, 
                         OptimizationStrategy.PRIORITIZE_B,
                         OptimizationStrategy.PRIORITIZE_C]:
            # Determine which dimension
            idx = ["A", "B", "C"].index(strategy.value.split("_")[-1])
            dimensions = [
                constraints.dimension_a,
                constraints.dimension_b,
                constraints.dimension_c
            ]
            target_dim = dimensions[idx]
            
            return [
                f"Conduct detailed assessment of {target_dim} requirements",
                f"Allocate additional resources to improve {target_dim}",
                f"Set clear targets and milestones for {target_dim} improvement",
                f"Identify quick wins that can boost {target_dim} immediately",
                f"Establish metrics to track {target_dim} progress"
            ]
        
        else:
            return [
                "Define clear optimization objectives",
                "Assess resource allocation across all constraints",
                "Implement measurement and tracking systems",
                "Create feedback loops for continuous improvement"
            ]
    
    async def _generate_expected_outcomes(
        self,
        strategy: OptimizationStrategy,
        constraints: ConstraintSet,
        current_values: List[float]
    ) -> List[str]:
        """Generate expected outcomes from optimization."""
        
        dimensions = [
            constraints.dimension_a,
            constraints.dimension_b,
            constraints.dimension_c
        ]
        
        if strategy == OptimizationStrategy.BALANCED:
            return [
                "Maintained equilibrium across all constraints",
                "Reduced risk of crisis in any dimension",
                "Improved stakeholder satisfaction",
                "More predictable outcomes"
            ]
        
        elif strategy == OptimizationStrategy.MINIMIZE_TRADE_OFFS:
            return [
                "10-15% improvement possible in all dimensions",
                "Reduced conflict between competing priorities",
                "More efficient resource utilization",
                "Better overall project outcomes"
            ]
        
        elif strategy in [OptimizationStrategy.PRIORITIZE_A,
                         OptimizationStrategy.PRIORITIZE_B,
                         OptimizationStrategy.PRIORITIZE_C]:
            idx = ["A", "B", "C"].index(strategy.value.split("_")[-1])
            target_dim = dimensions[idx]
            current_val = current_values[idx]
            
            improvement = (0.8 - current_val) * 0.7  # 70% of gap to 0.8
            
            return [
                f"{target_dim} improvement of {improvement:.0%}",
                f"Minor trade-offs in other dimensions (5-10%)",
                f"Better alignment with {target_dim} requirements",
                "Reduced risk in critical constraint area"
            ]
        
        else:
            return [
                "Optimized constraint balance",
                "Improved project success probability",
                "Better resource efficiency",
                "Enhanced stakeholder value"
            ]
    
    async def _identify_optimization_risks(
        self,
        strategy: OptimizationStrategy,
        constraints: ConstraintSet,
        trade_offs: List[TradeOffAnalysis]
    ) -> List[str]:
        """Identify risks associated with optimization strategy."""
        
        risks = []
        
        if strategy == OptimizationStrategy.BALANCED:
            risks = [
                "May miss opportunities for breakthrough improvements",
                "Could maintain mediocrity across all dimensions",
                "Requires constant vigilance and adjustment"
            ]
        
        elif strategy == OptimizationStrategy.MINIMIZE_TRADE_OFFS:
            risks = [
                "Solutions may be more complex to implement",
                "Could require significant upfront investment",
                "Benefits may take time to materialize"
            ]
        
        elif strategy in [OptimizationStrategy.PRIORITIZE_A,
                         OptimizationStrategy.PRIORITIZE_B,
                         OptimizationStrategy.PRIORITIZE_C]:
            # Add risks from focusing on one dimension
            risks = [
                "Other constraints may degrade below acceptable levels",
                "Stakeholders focused on other dimensions may resist",
                "Could create future imbalances requiring correction"
            ]
            
            # Add specific risks from high-impact trade-offs
            for trade_off in trade_offs:
                if trade_off.impact_score > 0.7:
                    risks.append(f"High impact from: {trade_off.relationship}")
        
        else:
            risks = [
                "Strategy implementation complexity",
                "Resistance to change from stakeholders",
                "Unforeseen consequences of optimization"
            ]
        
        return risks[:5]  # Limit to top 5 risks
    
    def _calculate_recommendation_confidence(
        self,
        strategy: OptimizationStrategy,
        balance_score: float,
        input_data: TripleConstraintInput
    ) -> float:
        """Calculate confidence in recommendation."""
        
        base_confidence = 0.7
        
        # Adjust based on current balance
        if balance_score > 0.8:
            base_confidence += 0.1  # Clear situation
        elif balance_score < 0.4:
            base_confidence += 0.1  # Obviously needs fixing
        
        # Adjust based on input completeness
        if input_data.optimization_goal:
            base_confidence += 0.05
        if input_data.success_criteria:
            base_confidence += 0.05
        if input_data.constraints_flexibility:
            base_confidence += 0.05
        
        # Some strategies are more certain
        if strategy in [OptimizationStrategy.PRIORITIZE_A,
                       OptimizationStrategy.PRIORITIZE_B,
                       OptimizationStrategy.PRIORITIZE_C]:
            base_confidence += 0.05  # Clear direction
        
        return min(0.95, base_confidence)
    
    async def _generate_alternative_recommendation(
        self,
        constraints: ConstraintSet,
        primary_strategy: OptimizationStrategy,
        input_data: TripleConstraintInput
    ) -> Optional[OptimizationRecommendation]:
        """Generate alternative recommendation."""
        
        # If primary is focused, suggest balanced
        if primary_strategy in [OptimizationStrategy.PRIORITIZE_A,
                               OptimizationStrategy.PRIORITIZE_B,
                               OptimizationStrategy.PRIORITIZE_C]:
            return OptimizationRecommendation(
                strategy=OptimizationStrategy.MAXIMIZE_VALUE,
                rationale="Alternative: Focus on maximizing overall value rather than individual constraints",
                action_steps=[
                    "Define value metrics that span all constraints",
                    "Identify high-value activities that benefit multiple dimensions",
                    "Optimize for stakeholder value, not constraint balance"
                ],
                expected_outcomes=[
                    "Better alignment with business objectives",
                    "More flexible constraint management",
                    "Improved stakeholder satisfaction"
                ],
                risks=[
                    "Requires clear value definition",
                    "May be harder to measure progress"
                ],
                confidence_level=0.7
            )
        
        return None
    
    async def _generate_domain_insights(
        self,
        constraints: ConstraintSet,
        input_data: TripleConstraintInput,
        context: Context
    ) -> List[str]:
        """Generate domain-specific insights."""
        
        insights = []
        
        if input_data.domain_context == "project_management":
            insights.extend([
                "Consider using agile methodologies for better constraint flexibility",
                "Implement change control processes to manage scope creep",
                "Regular stakeholder communication helps manage expectations"
            ])
        
        elif input_data.domain_context == "software_development":
            insights.extend([
                "Technical debt accumulates when quality is sacrificed for speed",
                "Automated testing can improve both quality and timeline",
                "Modular architecture allows parallel feature development"
            ])
        
        elif input_data.domain_context == "engineering":
            insights.extend([
                "Over-engineering for performance can impact cost and schedule",
                "Reliability requirements often drive both cost and timeline",
                "Early prototyping helps validate performance assumptions"
            ])
        
        elif input_data.domain_context == "business_strategy":
            insights.extend([
                "Market timing can be more important than perfect quality",
                "Premium pricing requires consistent quality delivery",
                "Speed advantages erode quickly in competitive markets"
            ])
        
        # Add general insights
        insights.extend([
            "Regular constraint review prevents drift and crisis",
            "Stakeholder alignment on priorities is crucial",
            "Small, continuous adjustments are better than major corrections"
        ])
        
        return insights[:5]  # Top 5 insights
    
    def _create_visualization_data(
        self,
        constraints: ConstraintSet
    ) -> Dict[str, Any]:
        """Create data for constraint triangle visualization."""
        
        viz_data = {
            "type": "radar_chart",
            "data": {
                "labels": [
                    constraints.dimension_a,
                    constraints.dimension_b,
                    constraints.dimension_c
                ],
                "datasets": [
                    {
                        "label": "Current State",
                        "data": constraints.current_values,
                        "backgroundColor": "rgba(54, 162, 235, 0.2)",
                        "borderColor": "rgba(54, 162, 235, 1)",
                        "borderWidth": 2
                    }
                ]
            },
            "options": {
                "scale": {
                    "min": 0,
                    "max": 1,
                    "ticks": {
                        "stepSize": 0.2
                    }
                },
                "title": "Triple Constraint Balance"
            }
        }
        
        # Add target if available
        if constraints.target_values:
            viz_data["data"]["datasets"].append({
                "label": "Target State",
                "data": constraints.target_values,
                "backgroundColor": "rgba(75, 192, 192, 0.2)",
                "borderColor": "rgba(75, 192, 192, 1)",
                "borderWidth": 2,
                "borderDash": [5, 5]
            })
        
        return viz_data
    
    async def _identify_key_decisions(
        self,
        constraints: ConstraintSet,
        input_data: TripleConstraintInput,
        context: Context
    ) -> List[str]:
        """Identify key decisions for constraint management."""
        
        decisions = []
        
        # Decisions based on constraint values
        values = constraints.current_values
        dimensions = [
            constraints.dimension_a,
            constraints.dimension_b,
            constraints.dimension_c
        ]
        
        # Low dimension decisions
        for i, (dim, val) in enumerate(zip(dimensions, values)):
            if val < 0.4:
                decisions.append(f"How much can we improve {dim} without breaking other constraints?")
                decisions.append(f"What is the minimum acceptable level for {dim}?")
        
        # High dimension decisions
        for i, (dim, val) in enumerate(zip(dimensions, values)):
            if val > 0.8:
                decisions.append(f"Can we maintain current {dim} levels with less resource?")
                decisions.append(f"Is the high {dim} providing proportional value?")
        
        # General strategic decisions
        decisions.extend([
            "What is our primary success criterion?",
            "Which constraint has the most flexibility?",
            "Where can we find win-win improvements?",
            "How do we measure constraint optimization success?"
        ])
        
        # Domain-specific decisions
        if input_data.domain_context == "project_management":
            decisions.append("Should we adjust project phases to better balance constraints?")
        elif input_data.domain_context == "software_development":
            decisions.append("Can we use different technologies to improve constraint balance?")
        
        return decisions[:6]  # Top 6 decisions
    
    async def _define_success_metrics(
        self,
        constraints: ConstraintSet,
        input_data: TripleConstraintInput,
        context: Context
    ) -> List[str]:
        """Define metrics to track constraint management success."""
        
        metrics = []
        
        # Balance metrics
        metrics.append("Constraint Balance Score (variance from mean)")
        metrics.append("Minimum Constraint Value (no dimension below threshold)")
        
        # Dimension-specific metrics
        dimensions = [
            constraints.dimension_a,
            constraints.dimension_b,
            constraints.dimension_c
        ]
        
        for dim in dimensions:
            if dim == "scope" or dim == "features":
                metrics.append(f"{dim}: Percentage of requirements delivered")
            elif dim == "time" or dim == "timeline":
                metrics.append(f"{dim}: Schedule variance percentage")
            elif dim == "budget" or dim == "cost":
                metrics.append(f"{dim}: Cost variance percentage")
            elif dim == "quality":
                metrics.append(f"{dim}: Defect density or customer satisfaction")
            elif dim == "performance":
                metrics.append(f"{dim}: Performance benchmarks achieved")
            elif dim == "reliability":
                metrics.append(f"{dim}: Uptime or failure rate")
        
        # Stakeholder metrics
        metrics.append("Stakeholder satisfaction across all dimensions")
        metrics.append("Frequency of crisis interventions required")
        
        # Include custom success criteria
        if input_data.success_criteria:
            for criterion in input_data.success_criteria[:2]:
                metrics.append(f"Custom: {criterion}")
        
        return metrics[:8]  # Top 8 metrics
    
    async def _create_overall_assessment(
        self,
        constraints: ConstraintSet,
        trade_offs: List[TradeOffAnalysis],
        recommendations: List[OptimizationRecommendation],
        context: Context
    ) -> str:
        """Create overall assessment of constraint situation."""
        
        values = constraints.current_values
        mean = sum(values) / 3
        variance = sum((v - mean) ** 2 for v in values) / 3
        balance_score = 1.0 - (variance * 10)
        
        # High-impact trade-offs
        high_impact_count = sum(1 for t in trade_offs if t.impact_score > 0.7)
        
        # Primary recommendation
        primary_rec = recommendations[0] if recommendations else None
        
        assessment = "## Overall Triple Constraint Assessment\n\n"
        
        # Current state summary
        if balance_score > 0.8:
            assessment += "**Current State**: ✅ Well-balanced constraints with good alignment.\n"
        elif balance_score > 0.6:
            assessment += "**Current State**: ⚠️ Moderate imbalance requiring attention.\n"
        else:
            assessment += "**Current State**: ❌ Significant imbalance needing immediate action.\n"
        
        # Trade-off complexity
        assessment += f"\n**Trade-off Complexity**: {high_impact_count} high-impact trade-offs identified.\n"
        
        # Recommendation summary
        if primary_rec:
            assessment += f"\n**Recommended Approach**: {primary_rec.strategy.value.replace('_', ' ').title()}\n"
            assessment += f"- **Confidence**: {primary_rec.confidence_level:.0%}\n"
            assessment += f"- **Key Action**: {primary_rec.action_steps[0]}\n"
        
        # Success outlook
        assessment += "\n**Success Outlook**: "
        if balance_score > 0.7 and primary_rec and primary_rec.confidence_level > 0.8:
            assessment += "High - Clear path to optimization with manageable risks."
        elif balance_score > 0.5 or (primary_rec and primary_rec.confidence_level > 0.7):
            assessment += "Moderate - Success achievable with focused effort and monitoring."
        else:
            assessment += "Challenging - Significant effort required, consider external support."
        
        # Key insight
        dimensions = [constraints.dimension_a, constraints.dimension_b, constraints.dimension_c]
        min_idx = values.index(min(values))
        assessment += f"\n\n**Key Insight**: Focus on improving {dimensions[min_idx]} while maintaining balance."
        
        return assessment
    
    def _calculate_confidence(
        self,
        constraints: ConstraintSet,
        trade_offs: List[TradeOffAnalysis],
        recommendations: List[OptimizationRecommendation]
    ) -> float:
        """Calculate overall analysis confidence."""
        
        confidence_factors = []
        
        # Constraint identification confidence
        if constraints.dimension_a != "dimension_a":  # Not generic
            confidence_factors.append(0.9)
        else:
            confidence_factors.append(0.6)
        
        # Trade-off analysis depth
        avg_examples = sum(len(t.examples) for t in trade_offs) / len(trade_offs)
        trade_off_confidence = min(0.9, 0.6 + (avg_examples * 0.1))
        confidence_factors.append(trade_off_confidence)
        
        # Recommendation confidence
        if recommendations:
            avg_rec_confidence = sum(r.confidence_level for r in recommendations) / len(recommendations)
            confidence_factors.append(avg_rec_confidence)
        
        # Overall confidence
        return sum(confidence_factors) / len(confidence_factors) if confidence_factors else 0.7


# Create FastMCP tool instance
async def analyze_triple_constraint_tool(
    input_data: TripleConstraintInput,
    context: Context
) -> TripleConstraintAnalysis:
    """FastMCP tool for triple constraint analysis."""
    
    tool = TripleConstraintTool()
    return await tool.analyze_triple_constraint(input_data, context)