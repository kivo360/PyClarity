"""
Multi-Perspective Analyzer

Analyzes scenarios from multiple stakeholder perspectives to identify
synergies, conflicts, and integration opportunities.
"""

import asyncio
from typing import Any, Dict, List, Optional

from ..base import BaseCognitiveAnalyzer
from .models import (
    ComplexityLevel,
    ConflictSeverity,
    IntegrationApproach,
    IntegrationStrategy,
    MultiPerspectiveContext,
    MultiPerspectiveResult,
    Perspective,
    StakeholderType,
    SynergyConflict,
    ViewpointAnalysis,
)


class MultiPerspectiveAnalyzer(BaseCognitiveAnalyzer):
    """
    Analyzer for multi-perspective analysis.

    Evaluates scenarios from multiple stakeholder viewpoints to identify
    synergies, conflicts, and create comprehensive integration strategies.
    """

    # Domain-specific perspective templates
    DOMAIN_PERSPECTIVES = {
        "business": [
            (StakeholderType.EXECUTIVE, "Leadership and strategic vision"),
            (StakeholderType.CUSTOMER, "End-user needs and experience"),
            (StakeholderType.EMPLOYEE, "Internal workforce and operations"),
            (StakeholderType.PARTNER, "External collaborators and suppliers")
        ],
        "product": [
            (StakeholderType.CUSTOMER, "User needs and preferences"),
            (StakeholderType.TECHNICAL, "Engineering feasibility"),
            (StakeholderType.BUSINESS, "Commercial viability"),
            (StakeholderType.REGULATORY, "Compliance requirements")
        ],
        "technology": [
            (StakeholderType.TECHNICAL, "Technical implementation"),
            (StakeholderType.SECURITY, "Security and risk management"),
            (StakeholderType.OPERATIONS, "Operational sustainability"),
            (StakeholderType.END_USER, "User adoption and experience")
        ]
    }

    async def analyze(
        self,
        context: MultiPerspectiveContext
    ) -> MultiPerspectiveResult:
        """
        Perform multi-perspective analysis.

        Args:
            context: The scenario requiring multi-perspective evaluation

        Returns:
            MultiPerspectiveResult with complete perspective analysis
        """
        # Identify or generate perspectives
        perspectives = await self._identify_perspectives(context)

        # Analyze each perspective
        viewpoint_analyses = []
        for perspective in perspectives:
            analysis = await self._analyze_viewpoint(perspective, context)
            viewpoint_analyses.append(analysis)

        # Identify synergies and conflicts
        synergies_conflicts = await self._identify_synergies_conflicts(
            perspectives,
            viewpoint_analyses,
            context
        )

        # Develop integration strategies
        integration_strategies = await self._develop_integration_strategies(
            perspectives,
            synergies_conflicts,
            context
        )

        # Find common ground
        common_ground = await self._find_common_ground(
            viewpoint_analyses,
            perspectives
        )

        # Identify critical divergences
        critical_divergences = await self._identify_critical_divergences(
            viewpoint_analyses,
            synergies_conflicts
        )

        # Create negotiation framework
        negotiation_framework = await self._create_negotiation_framework(
            perspectives,
            critical_divergences,
            common_ground
        )

        # Develop communication strategy
        communication_strategies = await self._develop_communication_strategies(
            perspectives,
            viewpoint_analyses,
            integration_strategies
        )

        # Generate win-win opportunities
        win_win_opportunities = await self._identify_win_win_opportunities(
            perspectives,
            synergies_conflicts,
            viewpoint_analyses
        )

        # Create implementation roadmap
        implementation_roadmap = await self._create_implementation_roadmap(
            integration_strategies,
            perspectives,
            context
        )

        # Assess overall feasibility
        feasibility_assessment = await self._assess_feasibility(
            integration_strategies,
            critical_divergences,
            context
        )

        # Generate overall assessment
        overall_assessment = await self._generate_overall_assessment(
            perspectives,
            integration_strategies,
            feasibility_assessment,
            context
        )

        # Calculate confidence score
        confidence_score = self._calculate_confidence(
            perspectives,
            synergies_conflicts,
            integration_strategies
        )

        return MultiPerspectiveResult(
            input_scenario=context.scenario,
            identified_perspectives=perspectives,
            viewpoint_analyses=viewpoint_analyses,
            synergies_conflicts=synergies_conflicts,
            integration_strategies=integration_strategies,
            common_ground=common_ground,
            critical_divergences=critical_divergences,
            negotiation_framework=negotiation_framework,
            communication_strategies=communication_strategies,
            win_win_opportunities=win_win_opportunities,
            implementation_roadmap=implementation_roadmap,
            feasibility_assessment=feasibility_assessment,
            overall_assessment=overall_assessment,
            confidence_score=confidence_score
        )

    async def _identify_perspectives(
        self,
        context: MultiPerspectiveContext
    ) -> list[Perspective]:
        """Identify relevant perspectives for analysis."""
        # Use predefined perspectives if available
        if context.predefined_perspectives:
            return context.predefined_perspectives

        # Check domain-specific templates
        if context.domain_context:
            for domain, template in self.DOMAIN_PERSPECTIVES.items():
                if domain in context.domain_context.lower():
                    return await self._create_perspectives_from_template(
                        template,
                        context
                    )

        # Generate generic perspectives
        return await self._generate_generic_perspectives(context)

    async def _create_perspectives_from_template(
        self,
        template: list[tuple],
        context: MultiPerspectiveContext
    ) -> list[Perspective]:
        """Create perspectives from domain template."""
        perspectives = []

        for stakeholder_type, description in template:
            perspective = Perspective(
                perspective_id=f"perspective_{stakeholder_type.value}",
                stakeholder_type=stakeholder_type,
                stakeholder_name=f"{stakeholder_type.value.title()} Stakeholder",
                description=description,
                primary_concerns=[
                    f"Primary concern 1 for {stakeholder_type.value}",
                    f"Primary concern 2 for {stakeholder_type.value}",
                    f"Primary concern 3 for {stakeholder_type.value}"
                ],
                success_criteria=[
                    f"Success criterion 1 for {stakeholder_type.value}",
                    f"Success criterion 2 for {stakeholder_type.value}"
                ],
                influence_level=0.8,
                flexibility=0.6
            )
            perspectives.append(perspective)

        return perspectives

    async def _generate_generic_perspectives(
        self,
        context: MultiPerspectiveContext
    ) -> list[Perspective]:
        """Generate generic stakeholder perspectives."""
        # Default to key stakeholder types
        default_types = [
            (StakeholderType.BUSINESS, "Business and strategic interests"),
            (StakeholderType.TECHNICAL, "Technical feasibility and implementation"),
            (StakeholderType.END_USER, "User experience and needs")
        ]

        perspectives = []
        for stakeholder_type, description in default_types:
            perspective = Perspective(
                perspective_id=f"perspective_{stakeholder_type.value}",
                stakeholder_type=stakeholder_type,
                stakeholder_name=f"{stakeholder_type.value.title()} Perspective",
                description=description,
                primary_concerns=[
                    f"Concern about {context.scenario} impact",
                    "Resource and timeline considerations",
                    "Quality and outcome expectations"
                ],
                success_criteria=[
                    f"Successful outcome for {stakeholder_type.value}",
                    "Acceptable trade-offs and compromises"
                ],
                influence_level=0.7,
                flexibility=0.5
            )
            perspectives.append(perspective)

        return perspectives

    async def _analyze_viewpoint(
        self,
        perspective: Perspective,
        context: MultiPerspectiveContext
    ) -> ViewpointAnalysis:
        """Analyze scenario from a specific perspective."""
        # Evaluate priorities based on perspective type
        priorities = await self._evaluate_priorities(perspective, context)

        # Assess constraints from this viewpoint
        constraints = await self._assess_constraints(perspective, context)

        # Identify opportunities
        opportunities = await self._identify_opportunities(perspective, context)

        # Determine risks
        risks = await self._determine_risks(perspective, context)

        # Generate preferred approach
        preferred_approach = await self._generate_preferred_approach(
            perspective,
            priorities,
            constraints
        )

        # Identify acceptable compromises
        acceptable_compromises = await self._identify_compromises(
            perspective,
            context
        )

        # Determine deal breakers
        deal_breakers = await self._identify_deal_breakers(
            perspective,
            priorities
        )

        # Calculate alignment score
        alignment_score = self._calculate_alignment_score(
            perspective,
            context,
            priorities
        )

        return ViewpointAnalysis(
            perspective_id=perspective.perspective_id,
            priorities=priorities,
            constraints=constraints,
            opportunities=opportunities,
            risks=risks,
            preferred_approach=preferred_approach,
            acceptable_compromises=acceptable_compromises,
            deal_breakers=deal_breakers,
            emotional_factors=[
                f"Trust in process from {perspective.stakeholder_name}",
                "Historical experiences and biases",
                "Cultural and organizational factors"
            ],
            communication_preferences=[
                f"Preferred communication style for {perspective.stakeholder_type.value}",
                "Decision-making process expectations",
                "Information requirements"
            ],
            influence_dynamics=f"{perspective.stakeholder_name} has {perspective.influence_level*100:.0f}% influence",
            alignment_score=alignment_score
        )

    async def _identify_synergies_conflicts(
        self,
        perspectives: list[Perspective],
        analyses: list[ViewpointAnalysis],
        context: MultiPerspectiveContext
    ) -> list[SynergyConflict]:
        """Identify synergies and conflicts between perspectives."""
        synergies_conflicts = []

        # Compare each pair of perspectives
        for i in range(len(perspectives)):
            for j in range(i + 1, len(perspectives)):
                perspective_a = perspectives[i]
                perspective_b = perspectives[j]
                analysis_a = analyses[i]
                analysis_b = analyses[j]

                # Check for synergies
                synergies = self._find_synergies(
                    analysis_a,
                    analysis_b,
                    perspective_a,
                    perspective_b
                )

                # Check for conflicts
                conflicts = self._find_conflicts(
                    analysis_a,
                    analysis_b,
                    perspective_a,
                    perspective_b
                )

                # Create synergy entries
                for synergy in synergies:
                    synergies_conflicts.append(SynergyConflict(
                        item_id=f"synergy_{len(synergies_conflicts)}",
                        type="synergy",
                        perspective_a=perspective_a.perspective_id,
                        perspective_b=perspective_b.perspective_id,
                        description=synergy,
                        impact="Positive alignment of interests",
                        severity=ConflictSeverity.NONE,
                        resolution_difficulty=0.2,
                        mutual_benefit=True,
                        exploitation_strategy="Leverage shared interests for momentum"
                    ))

                # Create conflict entries
                for conflict in conflicts:
                    synergies_conflicts.append(SynergyConflict(
                        item_id=f"conflict_{len(synergies_conflicts)}",
                        type="conflict",
                        perspective_a=perspective_a.perspective_id,
                        perspective_b=perspective_b.perspective_id,
                        description=conflict["description"],
                        impact=conflict["impact"],
                        severity=conflict["severity"],
                        resolution_difficulty=0.7,
                        mutual_benefit=False,
                        resolution_options=[
                            "Negotiated compromise",
                            "Phased approach",
                            "Creative alternative solution"
                        ]
                    ))

        return synergies_conflicts

    async def _develop_integration_strategies(
        self,
        perspectives: list[Perspective],
        synergies_conflicts: list[SynergyConflict],
        context: MultiPerspectiveContext
    ) -> list[IntegrationStrategy]:
        """Develop strategies to integrate multiple perspectives."""
        strategies = []

        # Strategy 1: Consensus building
        strategies.append(IntegrationStrategy(
            strategy_id="consensus",
            name="Consensus Building Approach",
            description="Build agreement through inclusive dialogue and compromise",
            approach_type=IntegrationApproach.CONSENSUS,
            target_perspectives=[p.perspective_id for p in perspectives],
            implementation_steps=[
                "Establish common ground and shared values",
                "Facilitate structured dialogue sessions",
                "Identify mutually beneficial outcomes",
                "Negotiate acceptable compromises",
                "Document agreements and commitments"
            ],
            expected_outcomes=[
                "Broad stakeholder buy-in",
                "Sustainable long-term solution",
                "Reduced implementation resistance"
            ],
            resource_requirements=[
                "Skilled facilitator",
                "Time for dialogue process",
                "Compromise flexibility"
            ],
            timeline="4-8 weeks for full consensus",
            success_probability=0.7,
            key_risks=[
                "Time-intensive process",
                "Potential for lowest common denominator",
                "Some stakeholders may disengage"
            ]
        ))

        # Strategy 2: Prioritization approach
        high_influence = max(perspectives, key=lambda p: p.influence_level)
        strategies.append(IntegrationStrategy(
            strategy_id="prioritization",
            name="Stakeholder Prioritization",
            description=f"Prioritize {high_influence.stakeholder_name} while addressing others' concerns",
            approach_type=IntegrationApproach.PRIORITIZATION,
            target_perspectives=[high_influence.perspective_id],
            implementation_steps=[
                f"Align with {high_influence.stakeholder_name} requirements",
                "Address critical concerns of other stakeholders",
                "Implement mitigation for negative impacts",
                "Communicate rationale clearly"
            ],
            expected_outcomes=[
                "Faster decision making",
                "Clear direction",
                "Some stakeholder dissatisfaction"
            ],
            resource_requirements=[
                "Executive support",
                "Change management",
                "Communication plan"
            ],
            timeline="2-4 weeks implementation",
            success_probability=0.6,
            key_risks=[
                "Stakeholder alienation",
                "Long-term relationship damage",
                "Implementation resistance"
            ]
        ))

        # Strategy 3: Hybrid approach
        strategies.append(IntegrationStrategy(
            strategy_id="hybrid",
            name="Hybrid Integration",
            description="Combine multiple perspectives through creative synthesis",
            approach_type=IntegrationApproach.SYNTHESIS,
            target_perspectives=[p.perspective_id for p in perspectives],
            implementation_steps=[
                "Identify core non-negotiables for each perspective",
                "Design creative solutions addressing multiple needs",
                "Test integrated approach with stakeholders",
                "Iterate based on feedback",
                "Implement with monitoring"
            ],
            expected_outcomes=[
                "Innovative solutions",
                "Balanced stakeholder satisfaction",
                "Potential for breakthrough outcomes"
            ],
            resource_requirements=[
                "Creative problem-solving team",
                "Iteration capacity",
                "Stakeholder engagement"
            ],
            timeline="6-10 weeks for development",
            success_probability=0.75,
            key_risks=[
                "Complexity in implementation",
                "Higher resource requirements",
                "Need for ongoing coordination"
            ]
        ))

        return strategies

    async def _find_common_ground(
        self,
        analyses: list[ViewpointAnalysis],
        perspectives: list[Perspective]
    ) -> list[str]:
        """Identify areas of agreement across perspectives."""
        common_ground = []

        # Check shared priorities
        all_priorities = [set(a.priorities) for a in analyses]
        if all_priorities:
            shared_priorities = set.intersection(*all_priorities)
            for priority in shared_priorities:
                common_ground.append(f"Shared priority: {priority}")

        # Check aligned success criteria
        all_success = [set(p.success_criteria) for p in perspectives]
        if all_success:
            shared_success = set.intersection(*all_success)
            for criterion in shared_success:
                common_ground.append(f"Agreed success metric: {criterion}")

        # Add universal agreements
        common_ground.extend([
            "Need for clear communication throughout process",
            "Importance of achieving sustainable outcomes",
            "Value of stakeholder engagement",
            "Desire for efficient resource utilization"
        ])

        return common_ground[:8]  # Top 8 areas

    async def _identify_critical_divergences(
        self,
        analyses: list[ViewpointAnalysis],
        synergies_conflicts: list[SynergyConflict]
    ) -> list[str]:
        """Identify critical areas of disagreement."""
        divergences = []

        # Extract high-severity conflicts
        critical_conflicts = [
            sc for sc in synergies_conflicts
            if sc.type == "conflict" and sc.severity in [ConflictSeverity.HIGH, ConflictSeverity.CRITICAL]
        ]

        for conflict in critical_conflicts:
            divergences.append(conflict.description)

        # Check deal breakers
        for analysis in analyses:
            for deal_breaker in analysis.deal_breakers:
                divergences.append(f"Deal breaker: {deal_breaker}")

        return divergences[:6]  # Top 6 divergences

    async def _create_negotiation_framework(
        self,
        perspectives: list[Perspective],
        divergences: list[str],
        common_ground: list[str]
    ) -> dict[str, Any]:
        """Create framework for negotiating differences."""
        return {
            "principles": [
                "Start with areas of agreement",
                "Focus on interests, not positions",
                "Generate options for mutual gain",
                "Use objective criteria for decisions"
            ],
            "process": [
                f"1. Establish {len(common_ground)} agreed principles",
                f"2. Address {len(divergences)} critical divergences systematically",
                "3. Explore creative alternatives",
                "4. Test solutions against all perspectives",
                "5. Document agreements and next steps"
            ],
            "facilitation_approach": {
                "style": "Collaborative problem-solving",
                "tools": ["Interest mapping", "Option generation", "Trade-off analysis"],
                "ground_rules": [
                    "All perspectives heard equally",
                    "Focus on future, not past",
                    "Separate people from positions"
                ]
            },
            "escalation_path": [
                "Facilitator intervention",
                "Executive arbitration",
                "External mediation"
            ]
        }

    async def _develop_communication_strategies(
        self,
        perspectives: list[Perspective],
        analyses: list[ViewpointAnalysis],
        strategies: list[IntegrationStrategy]
    ) -> list[str]:
        """Develop communication approaches for each perspective."""
        communications = []

        for perspective, analysis in zip(perspectives, analyses):
            comm_strategy = (
                f"For {perspective.stakeholder_name}: "
                f"Emphasize {analysis.priorities[0] if analysis.priorities else 'key benefits'}, "
                f"address {analysis.constraints[0] if analysis.constraints else 'concerns'}, "
                f"use {analysis.communication_preferences[0] if analysis.communication_preferences else 'preferred style'}"
            )
            communications.append(comm_strategy)

        # Add general communication principles
        communications.extend([
            "Regular updates on progress and decisions",
            "Transparent handling of trade-offs",
            "Clear escalation and feedback channels"
        ])

        return communications

    async def _identify_win_win_opportunities(
        self,
        perspectives: list[Perspective],
        synergies_conflicts: list[SynergyConflict],
        analyses: list[ViewpointAnalysis]
    ) -> list[str]:
        """Identify opportunities that benefit multiple stakeholders."""
        opportunities = []

        # Leverage synergies
        synergies = [sc for sc in synergies_conflicts if sc.type == "synergy"]
        for synergy in synergies[:3]:
            opportunities.append(
                f"Leverage synergy: {synergy.description} for mutual benefit"
            )

        # Find overlapping opportunities
        all_opportunities = [set(a.opportunities) for a in analyses]
        if len(all_opportunities) > 1:
            shared_opps = set.intersection(*all_opportunities)
            for opp in list(shared_opps)[:2]:
                opportunities.append(f"Shared opportunity: {opp}")

        # Add creative win-wins
        opportunities.extend([
            "Phased implementation allowing early wins for all",
            "Resource sharing reducing costs for everyone",
            "Joint innovation creating new value"
        ])

        return opportunities[:7]  # Top 7 opportunities

    async def _create_implementation_roadmap(
        self,
        strategies: list[IntegrationStrategy],
        perspectives: list[Perspective],
        context: MultiPerspectiveContext
    ) -> list[str]:
        """Create roadmap for implementing integrated approach."""
        roadmap = []

        # Select optimal strategy (highest success probability)
        optimal_strategy = max(strategies, key=lambda s: s.success_probability)

        roadmap.append(f"Phase 1 (Weeks 1-2): {optimal_strategy.implementation_steps[0]}")
        roadmap.append(f"Phase 2 (Weeks 3-4): {optimal_strategy.implementation_steps[1]}")
        roadmap.append(f"Phase 3 (Weeks 5-6): {optimal_strategy.implementation_steps[2]}")

        # Add stakeholder checkpoints
        roadmap.append("Key Milestones:")
        roadmap.append("- Week 2: Stakeholder alignment checkpoint")
        roadmap.append("- Week 4: Mid-point review and adjustment")
        roadmap.append("- Week 6: Final integration and sign-off")

        # Add success metrics
        roadmap.append("Success Metrics:")
        roadmap.append("- Stakeholder satisfaction scores")
        roadmap.append("- Implementation progress vs plan")
        roadmap.append("- Issue resolution rate")

        return roadmap

    async def _assess_feasibility(
        self,
        strategies: list[IntegrationStrategy],
        divergences: list[str],
        context: MultiPerspectiveContext
    ) -> str:
        """Assess overall feasibility of integration."""
        # Calculate feasibility factors
        avg_success_prob = sum(s.success_probability for s in strategies) / len(strategies)
        critical_divergences = len([d for d in divergences if "Deal breaker" in d])

        if avg_success_prob >= 0.7 and critical_divergences == 0:
            assessment = (
                "High feasibility for successful integration. Strong alignment "
                "potential with multiple viable strategies. No critical blockers "
                "identified. Recommend proceeding with confidence."
            )
        elif avg_success_prob >= 0.5 and critical_divergences <= 2:
            assessment = (
                "Moderate feasibility with manageable challenges. Some critical "
                "divergences require careful negotiation. Success depends on "
                "stakeholder flexibility and skilled facilitation."
            )
        else:
            assessment = (
                "Significant feasibility concerns. Multiple critical divergences "
                "and limited integration options. Consider phased approach or "
                "alternative problem framing to improve alignment."
            )

        return assessment

    async def _generate_overall_assessment(
        self,
        perspectives: list[Perspective],
        strategies: list[IntegrationStrategy],
        feasibility: str,
        context: MultiPerspectiveContext
    ) -> str:
        """Generate comprehensive assessment of multi-perspective analysis."""
        # Summarize key findings
        num_perspectives = len(perspectives)
        num_strategies = len(strategies)
        optimal_strategy = max(strategies, key=lambda s: s.success_probability)

        assessment = (
            f"Multi-perspective analysis of '{context.scenario}' examined "
            f"{num_perspectives} key stakeholder viewpoints, revealing both "
            f"significant synergies and critical divergences. "
        )

        assessment += (
            f"The {optimal_strategy.name} strategy offers the highest success "
            f"probability ({optimal_strategy.success_probability*100:.0f}%) by "
            f"{optimal_strategy.description.lower()}. "
        )

        assessment += feasibility + " "

        assessment += (
            f"Implementation success requires addressing {num_perspectives} distinct "
            f"stakeholder needs through structured engagement, creative problem-solving, "
            f"and commitment to finding mutually beneficial outcomes."
        )

        return assessment

    def _calculate_confidence(
        self,
        perspectives: list[Perspective],
        synergies_conflicts: list[SynergyConflict],
        strategies: list[IntegrationStrategy]
    ) -> float:
        """Calculate confidence in the analysis."""
        # Base confidence
        confidence = 0.7

        # Adjust for completeness
        if len(perspectives) >= 3:
            confidence += 0.1

        if len(strategies) >= 3:
            confidence += 0.05

        # Adjust for synergies vs conflicts
        synergies = len([sc for sc in synergies_conflicts if sc.type == "synergy"])
        conflicts = len([sc for sc in synergies_conflicts if sc.type == "conflict"])

        if synergies > conflicts:
            confidence += 0.05
        elif conflicts > synergies * 2:
            confidence -= 0.1

        return max(0.5, min(0.95, confidence))

    # Helper methods
    async def _evaluate_priorities(
        self,
        perspective: Perspective,
        context: MultiPerspectiveContext
    ) -> list[str]:
        """Evaluate priorities for a perspective."""
        base_priorities = perspective.primary_concerns[:2]

        # Add context-specific priorities
        if "cost" in context.scenario.lower():
            base_priorities.append("Cost efficiency and budget control")
        if "time" in context.scenario.lower():
            base_priorities.append("Timeline and speed of delivery")
        if "quality" in context.scenario.lower():
            base_priorities.append("Quality standards and excellence")

        return base_priorities[:5]

    async def _assess_constraints(
        self,
        perspective: Perspective,
        context: MultiPerspectiveContext
    ) -> list[str]:
        """Assess constraints from a perspective."""
        constraints = []

        # Standard constraints by stakeholder type
        if perspective.stakeholder_type == StakeholderType.BUSINESS:
            constraints.extend(["Budget limitations", "ROI requirements"])
        elif perspective.stakeholder_type == StakeholderType.TECHNICAL:
            constraints.extend(["Technical debt", "System limitations"])
        elif perspective.stakeholder_type == StakeholderType.REGULATORY:
            constraints.extend(["Compliance requirements", "Legal restrictions"])

        # Add context constraints
        if context.known_constraints:
            constraints.extend(context.known_constraints[:2])

        return constraints[:4]

    async def _identify_opportunities(
        self,
        perspective: Perspective,
        context: MultiPerspectiveContext
    ) -> list[str]:
        """Identify opportunities from a perspective."""
        return [
            f"Opportunity to improve {perspective.primary_concerns[0]}",
            f"Potential for innovation in {context.domain_context or 'solution approach'}",
            "Chance to strengthen stakeholder relationships",
            "Possibility of creating competitive advantage"
        ][:3]

    async def _determine_risks(
        self,
        perspective: Perspective,
        context: MultiPerspectiveContext
    ) -> list[str]:
        """Determine risks from a perspective."""
        risks = [
            f"Risk of not meeting {perspective.success_criteria[0]}",
            "Potential for stakeholder misalignment",
            "Resource constraints impact"
        ]

        if perspective.flexibility < 0.5:
            risks.append("Low flexibility increases failure risk")

        return risks

    async def _generate_preferred_approach(
        self,
        perspective: Perspective,
        priorities: list[str],
        constraints: list[str]
    ) -> str:
        """Generate preferred approach for a perspective."""
        if perspective.stakeholder_type == StakeholderType.BUSINESS:
            return "Phased implementation with clear ROI milestones and risk mitigation"
        elif perspective.stakeholder_type == StakeholderType.TECHNICAL:
            return "Iterative development with technical excellence and scalability focus"
        elif perspective.stakeholder_type == StakeholderType.CUSTOMER:
            return "User-centric design with continuous feedback and rapid iteration"
        else:
            return f"Balanced approach addressing {priorities[0]} within {constraints[0] if constraints else 'given constraints'}"

    async def _identify_compromises(
        self,
        perspective: Perspective,
        context: MultiPerspectiveContext
    ) -> list[str]:
        """Identify acceptable compromises for a perspective."""
        compromises = []

        if perspective.flexibility >= 0.6:
            compromises.extend([
                "Timeline extension for quality improvement",
                "Phased delivery instead of big bang",
                "Shared resources with other initiatives"
            ])
        else:
            compromises.append("Minor scope adjustments for core delivery")

        return compromises[:3]

    async def _identify_deal_breakers(
        self,
        perspective: Perspective,
        priorities: list[str]
    ) -> list[str]:
        """Identify deal breakers for a perspective."""
        deal_breakers = []

        if perspective.stakeholder_type == StakeholderType.REGULATORY:
            deal_breakers.append("Non-compliance with regulations")
        elif perspective.stakeholder_type == StakeholderType.SECURITY:
            deal_breakers.append("Unacceptable security vulnerabilities")

        # High priority items become deal breakers
        if priorities:
            deal_breakers.append(f"Failure to address {priorities[0]}")

        return deal_breakers[:2]

    def _calculate_alignment_score(
        self,
        perspective: Perspective,
        context: MultiPerspectiveContext,
        priorities: list[str]
    ) -> float:
        """Calculate how well scenario aligns with perspective."""
        score = 0.5  # Base score

        # Check if concerns are addressed
        scenario_lower = context.scenario.lower()
        for concern in perspective.primary_concerns:
            if any(word in concern.lower() for word in scenario_lower.split()):
                score += 0.1

        # Adjust for flexibility
        score += perspective.flexibility * 0.2

        return min(1.0, score)

    def _find_synergies(
        self,
        analysis_a: ViewpointAnalysis,
        analysis_b: ViewpointAnalysis,
        perspective_a: Perspective,
        perspective_b: Perspective
    ) -> list[str]:
        """Find synergies between two perspectives."""
        synergies = []

        # Check shared priorities
        shared_priorities = set(analysis_a.priorities) & set(analysis_b.priorities)
        for priority in shared_priorities:
            synergies.append(
                f"Both {perspective_a.stakeholder_name} and {perspective_b.stakeholder_name} "
                f"prioritize {priority}"
            )

        # Check complementary strengths
        if analysis_a.opportunities and analysis_b.constraints:
            synergies.append(
                f"{perspective_a.stakeholder_name} strengths can address "
                f"{perspective_b.stakeholder_name} constraints"
            )

        return synergies[:2]

    def _find_conflicts(
        self,
        analysis_a: ViewpointAnalysis,
        analysis_b: ViewpointAnalysis,
        perspective_a: Perspective,
        perspective_b: Perspective
    ) -> list[dict[str, Any]]:
        """Find conflicts between two perspectives."""
        conflicts = []

        # Check opposing priorities
        if analysis_a.priorities and analysis_b.priorities:
            if "speed" in str(analysis_a.priorities).lower() and "quality" in str(analysis_b.priorities).lower():
                conflicts.append({
                    "description": f"{perspective_a.stakeholder_name} prioritizes speed while "
                                 f"{perspective_b.stakeholder_name} prioritizes quality",
                    "impact": "Timeline vs quality trade-off required",
                    "severity": ConflictSeverity.MODERATE
                })

        # Check deal breaker conflicts
        for deal_breaker in analysis_a.deal_breakers:
            if any(comp in deal_breaker for comp in analysis_b.acceptable_compromises):
                conflicts.append({
                    "description": f"{perspective_a.stakeholder_name}'s deal breaker conflicts with "
                                 f"{perspective_b.stakeholder_name}'s approach",
                    "impact": "Fundamental misalignment requiring resolution",
                    "severity": ConflictSeverity.HIGH
                })

        return conflicts[:2]
