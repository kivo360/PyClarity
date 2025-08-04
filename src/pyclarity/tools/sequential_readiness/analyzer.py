"""
Sequential Readiness Analyzer

Analyzes processes requiring progressive readiness through ordered states,
helping identify sequences, transitions, gaps, and progression strategies.
"""

from typing import Any, Dict, List, Optional

from pyclarity.tools.sequential_readiness.models import (
    ComplexityLevel,
    Dependency,
    GapSeverity,
    Intervention,
    InterventionType,
    ReadinessGap,
    ReadinessLevel,
    ReadinessState,
    SequentialReadinessContext,
    SequentialReadinessResult,
    StateTransition,
    TransitionType,
)

from ..base import BaseCognitiveAnalyzer


class SequentialReadinessAnalyzer(BaseCognitiveAnalyzer):
    """
    Analyzer for sequential readiness assessment.

    Evaluates processes requiring progressive readiness through ordered states,
    ensuring prerequisites are met and success conditions are established.
    """

    # Domain-specific state templates
    DOMAIN_STATES = {
        "change_management": [
            (
                "Awareness",
                "Understanding the need for change",
                ["Can articulate why", "Understands impact"],
            ),
            (
                "Desire",
                "Willingness to support and engage",
                ["Shows support", "Actively participates"],
            ),
            (
                "Knowledge",
                "Having skills and behaviors needed",
                ["Demonstrates understanding", "Passes assessments"],
            ),
            (
                "Ability",
                "Practical application of knowledge",
                ["Successfully applies", "Achieves targets"],
            ),
            ("Reinforcement", "Sustaining the change", ["Maintains behaviors", "Helps others"]),
        ],
        "skill_development": [
            (
                "Foundation",
                "Basic knowledge and concepts",
                ["Understands fundamentals", "Has prerequisites"],
            ),
            (
                "Core Skills",
                "Essential practical abilities",
                ["Performs basic tasks", "Shows competence"],
            ),
            (
                "Advanced Skills",
                "Complex techniques and methods",
                ["Handles complexity", "Shows expertise"],
            ),
            ("Application", "Real-world problem solving", ["Completes projects", "Delivers value"]),
            ("Mastery", "Teaching and innovation", ["Mentors others", "Creates new methods"]),
        ],
        "technology_adoption": [
            (
                "Discovery",
                "Learning about the technology",
                ["Aware of capabilities", "Sees potential"],
            ),
            (
                "Evaluation",
                "Assessing fit and value",
                ["Completes assessment", "Has business case"],
            ),
            ("Pilot", "Testing in controlled environment", ["Pilot running", "Collecting metrics"]),
            ("Implementation", "Rolling out to production", ["Systems deployed", "Users trained"]),
            ("Optimization", "Improving and scaling", ["Metrics improving", "Value demonstrated"]),
        ],
        "project_phases": [
            (
                "Initiation",
                "Defining project and securing approval",
                ["Charter approved", "Team assigned"],
            ),
            (
                "Planning",
                "Developing comprehensive project plan",
                ["Plan approved", "Resources allocated"],
            ),
            (
                "Execution",
                "Carrying out the project work",
                ["Deliverables progressing", "Quality standards met"],
            ),
            (
                "Monitoring",
                "Tracking progress and managing changes",
                ["On schedule", "Risks managed"],
            ),
            (
                "Closure",
                "Finalizing and transitioning",
                ["Deliverables accepted", "Lessons learned"],
            ),
        ],
    }

    async def analyze(self, context: SequentialReadinessContext) -> SequentialReadinessResult:
        """
        Perform sequential readiness analysis.

        Args:
            context: The process requiring readiness assessment

        Returns:
            SequentialReadinessResult with complete readiness analysis
        """
        # Identify states based on domain or generate generic
        states = await self._identify_states(context)

        # Analyze transitions between states
        transitions = await self._analyze_transitions(states, context)

        # Assess current readiness
        current_state_idx = await self._assess_current_state(states, context)
        current_state = states[current_state_idx]

        # Identify gaps and blockers
        gaps = await self._identify_gaps(states, current_state_idx, context)

        # Generate interventions
        interventions = await self._generate_interventions(gaps, states, context)

        # Create progression strategy
        progression_strategy = await self._create_progression_strategy(
            states, transitions, current_state_idx, gaps, context
        )

        # Identify parallel opportunities
        parallel_opportunities = await self._identify_parallel_opportunities(states, transitions)

        # Calculate overall readiness
        overall_readiness = await self._calculate_overall_readiness(states, current_state_idx, gaps)

        # Generate recommendations
        recommendations = await self._generate_recommendations(
            current_state, gaps, interventions, context
        )

        # Identify risks
        risks = await self._identify_risks(states, transitions, gaps, context)

        # Create monitoring plan
        monitoring_plan = await self._create_monitoring_plan(
            states, current_state_idx, progression_strategy
        )

        # Generate overall recommendation
        overall_recommendation = await self._generate_overall_recommendation(
            overall_readiness, gaps, risks, context
        )

        # Calculate confidence
        confidence_score = self._calculate_confidence(states, gaps, context)

        return SequentialReadinessResult(
            input_scenario=context.scenario,
            identified_states=states,
            state_transitions=transitions,
            current_state=current_state,
            readiness_gaps=gaps,
            recommended_interventions=interventions,
            progression_strategy=progression_strategy,
            overall_readiness_percentage=overall_readiness,
            critical_blockers=[g.description for g in gaps if g.severity == GapSeverity.CRITICAL],
            success_factors=[
                f"Strong foundation in {states[0].name}",
                f"Clear progression path through {len(states)} states",
                f"Identified {len(interventions)} targeted interventions",
            ],
            risk_factors=risks[:5],  # Top 5 risks
            parallel_opportunities=parallel_opportunities,
            immediate_actions=recommendations[:3],  # Top 3 actions
            key_decisions=[
                f"Priority order for addressing {len(gaps)} gaps",
                "Resource allocation for interventions",
                "Timeline for progression milestones",
            ],
            monitoring_plan=monitoring_plan,
            overall_recommendation=overall_recommendation,
            confidence_score=confidence_score,
        )

    async def _identify_states(self, context: SequentialReadinessContext) -> list[ReadinessState]:
        """Identify relevant states for the process."""
        # Check for domain-specific states
        if context.domain_context:
            for domain, template_states in self.DOMAIN_STATES.items():
                if domain in context.domain_context.lower():
                    return await self._create_states_from_template(template_states, context)

        # Use predefined states if provided
        if context.predefined_states:
            return context.predefined_states

        # Generate generic states based on complexity
        return await self._generate_generic_states(context)

    async def _create_states_from_template(
        self, template: list[tuple], context: SequentialReadinessContext
    ) -> list[ReadinessState]:
        """Create states from domain template."""
        states = []
        for idx, (name, desc, criteria) in enumerate(template):
            state = ReadinessState(
                state_id=f"state_{idx}",
                name=name,
                description=desc,
                required_capabilities=criteria[:3],
                success_criteria=criteria,
                prerequisites=[f"state_{idx - 1}"] if idx > 0 else [],
                typical_duration=self._estimate_duration(context.complexity_level),
                readiness_level=ReadinessLevel.NOT_STARTED,
            )
            states.append(state)
        return states

    async def _generate_generic_states(
        self, context: SequentialReadinessContext
    ) -> list[ReadinessState]:
        """Generate generic sequential states."""
        num_states = {
            ComplexityLevel.SIMPLE: 3,
            ComplexityLevel.MODERATE: 5,
            ComplexityLevel.COMPLEX: 7,
        }.get(context.complexity_level, 5)

        state_names = [
            "Foundation",
            "Preparation",
            "Initial Implementation",
            "Expansion",
            "Optimization",
            "Maturity",
            "Excellence",
        ][:num_states]

        states = []
        for idx, name in enumerate(state_names):
            state = ReadinessState(
                state_id=f"state_{idx}",
                name=name,
                description=f"{name} phase of {context.scenario}",
                required_capabilities=[f"Capability {i + 1} for {name}" for i in range(2)],
                success_criteria=[f"Success criterion {i + 1} for {name}" for i in range(3)],
                prerequisites=[f"state_{idx - 1}"] if idx > 0 else [],
                typical_duration=self._estimate_duration(context.complexity_level),
                readiness_level=ReadinessLevel.NOT_STARTED,
            )
            states.append(state)

        return states

    async def _analyze_transitions(
        self, states: list[ReadinessState], context: SequentialReadinessContext
    ) -> list[StateTransition]:
        """Analyze transitions between states."""
        transitions = []

        for i in range(len(states) - 1):
            from_state = states[i]
            to_state = states[i + 1]

            transition = StateTransition(
                from_state=from_state.state_id,
                to_state=to_state.state_id,
                transition_type=TransitionType.SEQUENTIAL,
                requirements=await self._generate_transition_requirements(from_state, to_state),
                dependencies=[
                    Dependency(
                        dependency_id=f"dep_{i}",
                        description=f"Complete {from_state.name}",
                        type="completion",
                        required_state=from_state.state_id,
                        criticality="high",
                    )
                ],
                risks=await self._identify_transition_risks(from_state, to_state, context),
                estimated_duration=self._estimate_duration(context.complexity_level),
                success_rate=0.8,
                strategies=[
                    f"Gradual transition from {from_state.name}",
                    f"Pilot approach for {to_state.name}",
                    "Continuous monitoring and adjustment",
                ],
            )
            transitions.append(transition)

        return transitions

    async def _assess_current_state(
        self, states: list[ReadinessState], context: SequentialReadinessContext
    ) -> int:
        """Assess which state the process is currently in."""
        # Simple heuristic based on scenario description
        scenario_lower = context.scenario.lower()

        if any(word in scenario_lower for word in ["starting", "beginning", "initial"]):
            return 0
        elif any(word in scenario_lower for word in ["implementing", "rolling out"]):
            return min(2, len(states) - 1)
        elif any(word in scenario_lower for word in ["optimizing", "improving"]):
            return min(len(states) - 2, len(states) - 1)
        else:
            return 1  # Default to second state

    async def _identify_gaps(
        self, states: list[ReadinessState], current_idx: int, context: SequentialReadinessContext
    ) -> list[ReadinessGap]:
        """Identify readiness gaps."""
        gaps = []

        # Check gaps for progressing to next state
        if current_idx < len(states) - 1:
            next_state = states[current_idx + 1]
            current_state = states[current_idx]

            # Capability gaps
            for capability in next_state.required_capabilities:
                gap = ReadinessGap(
                    gap_id=f"gap_cap_{len(gaps)}",
                    description=f"Missing capability: {capability}",
                    current_state=current_state.state_id,
                    target_state=next_state.state_id,
                    gap_type="capability",
                    severity=GapSeverity.MODERATE,
                    impact=f"Cannot progress to {next_state.name}",
                    root_causes=[
                        "Insufficient preparation",
                        "Resource constraints",
                        "Knowledge gaps",
                    ],
                    estimated_effort="Medium",
                )
                gaps.append(gap)

        # Add constraint-based gaps
        if context.key_constraints:
            for constraint in context.key_constraints[:2]:
                gap = ReadinessGap(
                    gap_id=f"gap_constraint_{len(gaps)}",
                    description=f"Constraint impact: {constraint}",
                    current_state=states[current_idx].state_id,
                    target_state=states[min(current_idx + 1, len(states) - 1)].state_id,
                    gap_type="constraint",
                    severity=GapSeverity.MINOR,
                    impact="Slows progression",
                    root_causes=[constraint],
                    estimated_effort="Low",
                )
                gaps.append(gap)

        return gaps

    async def _generate_interventions(
        self,
        gaps: list[ReadinessGap],
        states: list[ReadinessState],
        context: SequentialReadinessContext,
    ) -> list[Intervention]:
        """Generate interventions to address gaps."""
        interventions = []

        for gap in gaps:
            if gap.gap_type == "capability":
                intervention = Intervention(
                    intervention_id=f"int_{len(interventions)}",
                    name=f"Build {gap.description.replace('Missing capability: ', '')}",
                    description=f"Intervention to address: {gap.description}",
                    type=InterventionType.TRAINING,
                    target_gaps=[gap.gap_id],
                    implementation_steps=[
                        "Assess current capability level",
                        "Design targeted training program",
                        "Implement with pilot group",
                        "Measure effectiveness",
                        "Scale to full implementation",
                    ],
                    required_resources=[
                        "Training materials",
                        "Subject matter experts",
                        "Practice environment",
                    ],
                    estimated_duration="2-4 weeks",
                    success_metrics=[
                        "Capability assessment scores",
                        "Practical application success",
                        "Stakeholder confidence",
                    ],
                    risk_mitigation=[
                        "Provide multiple learning formats",
                        "Include hands-on practice",
                        "Offer ongoing support",
                    ],
                )
            else:  # constraint type
                intervention = Intervention(
                    intervention_id=f"int_{len(interventions)}",
                    name=f"Mitigate {gap.description}",
                    description="Strategy to work within constraint",
                    type=InterventionType.PROCESS_CHANGE,
                    target_gaps=[gap.gap_id],
                    implementation_steps=[
                        "Analyze constraint impact",
                        "Identify workarounds",
                        "Implement adjustments",
                        "Monitor effectiveness",
                    ],
                    required_resources=["Process analysis", "Change management support"],
                    estimated_duration="1-2 weeks",
                    success_metrics=["Constraint impact reduced", "Progress maintained"],
                    risk_mitigation=["Regular constraint review", "Flexible approach"],
                )

            interventions.append(intervention)

        return interventions

    async def _create_progression_strategy(
        self,
        states: list[ReadinessState],
        transitions: list[StateTransition],
        current_idx: int,
        gaps: list[ReadinessGap],
        context: SequentialReadinessContext,
    ) -> str:
        """Create overall progression strategy."""
        remaining_states = len(states) - current_idx - 1
        critical_gaps = [g for g in gaps if g.severity == GapSeverity.CRITICAL]

        if critical_gaps:
            strategy = (
                f"Address {len(critical_gaps)} critical gaps before progression. "
                f"Focus on capability building and risk mitigation. "
            )
        elif remaining_states <= 2:
            strategy = (
                f"Near completion with {remaining_states} states remaining. "
                f"Maintain momentum and ensure quality standards. "
            )
        else:
            strategy = (
                f"Systematic progression through {remaining_states} remaining states. "
                f"Implement phased approach with regular checkpoints. "
            )

        strategy += (
            f"Timeline estimate: {remaining_states * 4} to {remaining_states * 8} weeks. "
            f"Success depends on addressing {len(gaps)} identified gaps."
        )

        return strategy

    async def _identify_parallel_opportunities(
        self, states: list[ReadinessState], transitions: list[StateTransition]
    ) -> list[str]:
        """Identify opportunities for parallel progress."""
        opportunities = []

        # Look for independent capabilities
        for i, state in enumerate(states[:-1]):
            if len(state.required_capabilities) > 2:
                opportunities.append(
                    f"Parallel capability development in {state.name}: "
                    f"Train multiple teams simultaneously"
                )

        # Look for non-dependent preparations
        if len(states) > 3:
            opportunities.append("Begin preparation for future states while completing current")

        return opportunities[:3]  # Top 3 opportunities

    async def _calculate_overall_readiness(
        self, states: list[ReadinessState], current_idx: int, gaps: list[ReadinessGap]
    ) -> float:
        """Calculate overall readiness percentage."""
        # Base progress on current state
        base_progress = (current_idx / len(states)) * 100

        # Adjust for gaps
        gap_penalty = len(gaps) * 2  # 2% penalty per gap
        critical_penalty = sum(10 for g in gaps if g.severity == GapSeverity.CRITICAL)

        overall = max(0, base_progress - gap_penalty - critical_penalty)
        return min(100, overall)

    async def _generate_recommendations(
        self,
        current_state: ReadinessState,
        gaps: list[ReadinessGap],
        interventions: list[Intervention],
        context: SequentialReadinessContext,
    ) -> list[str]:
        """Generate immediate action recommendations."""
        recommendations = []

        # Address critical gaps first
        critical_gaps = [g for g in gaps if g.severity == GapSeverity.CRITICAL]
        if critical_gaps:
            recommendations.append(f"Immediately address {len(critical_gaps)} critical gaps")

        # Focus on current state completion
        recommendations.append(f"Complete remaining criteria for {current_state.name}")

        # Prepare for next transition
        if interventions:
            recommendations.append(f"Initiate {interventions[0].name} intervention")

        # Consider constraints
        if context.key_constraints:
            recommendations.append(f"Develop mitigation plan for: {context.key_constraints[0]}")

        return recommendations

    async def _identify_risks(
        self,
        states: list[ReadinessState],
        transitions: list[StateTransition],
        gaps: list[ReadinessGap],
        context: SequentialReadinessContext,
    ) -> list[str]:
        """Identify key risks to progression."""
        risks = []

        # Gap-related risks
        if len(gaps) > 5:
            risks.append(f"High number of gaps ({len(gaps)}) may delay progression")

        # Transition risks
        for transition in transitions[:2]:  # Next 2 transitions
            if transition.risks:
                risks.extend(transition.risks[:2])

        # Constraint risks
        if context.key_constraints:
            risks.append(f"Constraint risk: {context.key_constraints[0]}")

        # Complexity risks
        if context.complexity_level == ComplexityLevel.COMPLEX:
            risks.append("High complexity increases failure probability")

        return risks

    async def _create_monitoring_plan(
        self, states: list[ReadinessState], current_idx: int, strategy: str
    ) -> list[str]:
        """Create monitoring plan for progression."""
        plan = []

        # Current state monitoring
        current = states[current_idx]
        plan.append(f"Weekly assessment of {current.name} success criteria")

        # Transition readiness
        if current_idx < len(states) - 1:
            next_state = states[current_idx + 1]
            plan.append(f"Bi-weekly readiness review for {next_state.name}")

        # Gap closure tracking
        plan.append("Track gap closure progress with metrics dashboard")

        # Risk monitoring
        plan.append("Monthly risk assessment and mitigation review")

        # Stakeholder communication
        plan.append("Regular stakeholder updates on progression status")

        return plan

    async def _generate_overall_recommendation(
        self,
        readiness: float,
        gaps: list[ReadinessGap],
        risks: list[str],
        context: SequentialReadinessContext,
    ) -> str:
        """Generate overall recommendation."""
        if readiness >= 80:
            recommendation = (
                "Strong readiness position. Proceed with confidence while "
                "maintaining vigilance on identified risks. "
            )
        elif readiness >= 60:
            recommendation = (
                "Moderate readiness level. Focus on gap closure before aggressive progression. "
            )
        else:
            recommendation = (
                "Significant readiness gaps exist. Prioritize foundational "
                "improvements before attempting progression. "
            )

        # Add specific guidance
        critical_gaps = [g for g in gaps if g.severity == GapSeverity.CRITICAL]
        if critical_gaps:
            recommendation += (
                f"Critical: Address {len(critical_gaps)} blocking issues immediately. "
            )

        if len(risks) > 3:
            recommendation += "Implement comprehensive risk mitigation plan. "

        recommendation += (
            "Success requires systematic approach with regular checkpoints and adaptive strategies."
        )

        return recommendation

    def _calculate_confidence(
        self,
        states: list[ReadinessState],
        gaps: list[ReadinessGap],
        context: SequentialReadinessContext,
    ) -> float:
        """Calculate confidence in the assessment."""
        # Start with base confidence
        confidence = 0.8

        # Adjust based on information quality
        if context.predefined_states:
            confidence += 0.1

        if context.domain_context:
            confidence += 0.05

        # Reduce for high complexity
        if context.complexity_level == ComplexityLevel.COMPLEX:
            confidence -= 0.1

        # Reduce for many gaps
        if len(gaps) > 10:
            confidence -= 0.1

        return max(0.5, min(0.95, confidence))

    def _estimate_duration(self, complexity: ComplexityLevel) -> str:
        """Estimate duration based on complexity."""
        durations = {
            ComplexityLevel.SIMPLE: "1-2 weeks",
            ComplexityLevel.MODERATE: "2-4 weeks",
            ComplexityLevel.COMPLEX: "4-8 weeks",
        }
        return durations.get(complexity, "2-4 weeks")

    async def _generate_transition_requirements(
        self, from_state: ReadinessState, to_state: ReadinessState
    ) -> list[str]:
        """Generate requirements for state transition."""
        return [
            f"Complete all {from_state.name} success criteria",
            f"Prepare resources for {to_state.name}",
            f"Stakeholder alignment on {to_state.name} objectives",
            "Risk mitigation measures in place",
        ]

    async def _identify_transition_risks(
        self,
        from_state: ReadinessState,
        to_state: ReadinessState,
        context: SequentialReadinessContext,
    ) -> list[str]:
        """Identify risks in state transition."""
        risks = [
            f"Premature transition from {from_state.name}",
            f"Resource availability for {to_state.name}",
            "Change resistance from stakeholders",
        ]

        if context.complexity_level == ComplexityLevel.COMPLEX:
            risks.append("Complex dependencies may cause delays")

        return risks
