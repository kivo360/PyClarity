# Clear Thinking FastMCP Server - Sequential Readiness Framework Tool

"""
Sequential Readiness Framework implementation for FastMCP server.

This tool analyzes processes requiring progressive readiness through ordered states,
helping identify sequences, transitions, gaps, and progression strategies.
"""

from typing import Dict, List, Optional, Any
import asyncio
from fastmcp import Context

from ..models.sequential_readiness import (
    SequentialReadinessInput,
    SequentialReadinessAnalysis,
    State,
    StateTransition,
    GapAnalysis,
    ProgressionPlan,
    ReadinessLevel,
    TransitionType,
    ProgressionStrategy
)
from .base import CognitiveToolBase


class SequentialReadinessTool(CognitiveToolBase):
    """Implements Sequential Readiness Framework analysis."""
    
    # Domain-specific state templates
    DOMAIN_STATES = {
        "change_management": [
            ("Awareness", "Understanding the need for change", ["Can articulate why", "Understands impact"]),
            ("Desire", "Willingness to support and engage", ["Shows support", "Actively participates"]),
            ("Knowledge", "Having skills and behaviors needed", ["Demonstrates understanding", "Passes assessments"]),
            ("Ability", "Practical application of knowledge", ["Successfully applies", "Achieves targets"]),
            ("Reinforcement", "Sustaining the change", ["Maintains behaviors", "Helps others"])
        ],
        "skill_development": [
            ("Foundation", "Basic knowledge and concepts", ["Understands fundamentals", "Has prerequisites"]),
            ("Core Skills", "Essential practical abilities", ["Performs basic tasks", "Shows competence"]),
            ("Advanced Skills", "Complex techniques and methods", ["Handles complexity", "Shows expertise"]),
            ("Application", "Real-world problem solving", ["Completes projects", "Delivers value"]),
            ("Mastery", "Teaching and innovation", ["Mentors others", "Creates new methods"])
        ],
        "technology_adoption": [
            ("Discovery", "Learning about the technology", ["Aware of capabilities", "Sees potential"]),
            ("Evaluation", "Assessing fit and value", ["Completes assessment", "Has business case"]),
            ("Pilot", "Testing in controlled environment", ["Pilot running", "Collecting metrics"]),
            ("Deployment", "Rolling out to users", ["Users onboarded", "System operational"]),
            ("Optimization", "Improving and expanding", ["Meeting targets", "Expanding usage"])
        ],
        "project_lifecycle": [
            ("Initiation", "Project conception and approval", ["Charter approved", "Stakeholders identified"]),
            ("Planning", "Detailed planning and design", ["Plans complete", "Resources allocated"]),
            ("Execution", "Implementing the plan", ["Deliverables created", "Progress tracked"]),
            ("Monitoring", "Tracking and controlling", ["Metrics collected", "Issues managed"]),
            ("Closure", "Finalizing and transitioning", ["Deliverables accepted", "Lessons learned"])
        ]
    }
    
    async def analyze_sequential_readiness(
        self,
        input_data: SequentialReadinessInput,
        context: Context
    ) -> SequentialReadinessAnalysis:
        """Main method to analyze sequential readiness."""
        
        await context.progress("Starting sequential readiness analysis", 0.1)
        
        # Identify states
        states = await self._identify_states(input_data, context)
        await context.progress("States identified", 0.2)
        
        # Analyze transitions
        transitions = await self._analyze_transitions(states, input_data, context)
        await context.progress("Transitions analyzed", 0.3)
        
        # Assess current state
        current_assessment = await self._assess_current_state(
            states, input_data, context
        )
        await context.progress("Current state assessed", 0.4)
        
        # Perform gap analysis
        gap_analyses = await self._perform_gap_analysis(
            states, input_data, context
        )
        await context.progress("Gap analysis completed", 0.5)
        
        # Create progression plan
        progression_plan = await self._create_progression_plan(
            states, transitions, gap_analyses, input_data, context
        )
        await context.progress("Progression plan created", 0.6)
        
        # Identify critical path
        critical_path = await self._identify_critical_path(
            states, transitions, context
        )
        await context.progress("Critical path identified", 0.7)
        
        # Map dependencies
        dependency_map = self._create_dependency_map(states, transitions)
        
        # Assess risks
        risk_assessment = await self._assess_risks(
            states, transitions, gap_analyses, context
        )
        
        # Generate domain insights
        domain_insights = await self._generate_domain_insights(
            states, input_data, context
        )
        
        # Create visualization data
        viz_data = self._create_visualization_data(states, transitions)
        
        # Identify key decisions
        key_decisions = await self._identify_key_decisions(
            states, gap_analyses, input_data, context
        )
        
        # Create monitoring plan
        monitoring_plan = await self._create_monitoring_plan(
            states, transitions, context
        )
        
        # Generate overall recommendation
        overall_recommendation = await self._create_overall_recommendation(
            states, progression_plan, gap_analyses, context
        )
        
        # Calculate confidence
        confidence = self._calculate_confidence(
            states, transitions, progression_plan
        )
        
        await context.progress("Analysis complete", 1.0)
        
        return SequentialReadinessAnalysis(
            input_scenario=input_data.scenario,
            identified_states=states,
            state_transitions=transitions,
            current_state_assessment=current_assessment,
            gap_analyses=gap_analyses,
            progression_plan=progression_plan,
            critical_path=critical_path,
            dependency_map=dependency_map,
            risk_assessment=risk_assessment,
            domain_specific_insights=domain_insights,
            visual_representation=viz_data,
            key_decisions=key_decisions,
            monitoring_plan=monitoring_plan,
            overall_recommendation=overall_recommendation,
            confidence_level=confidence
        )
    
    async def _identify_states(
        self,
        input_data: SequentialReadinessInput,
        context: Context
    ) -> List[State]:
        """Identify sequential states for the process."""
        
        if input_data.predefined_states:
            return input_data.predefined_states
        
        # Use domain templates if available
        if input_data.domain_context and input_data.domain_context in self.DOMAIN_STATES:
            template_states = self.DOMAIN_STATES[input_data.domain_context]
            states = []
            
            for i, (name, desc, indicators) in enumerate(template_states):
                # Determine prerequisites
                prerequisites = []
                if i > 0:
                    prerequisites.append(template_states[i-1][0])
                
                # Determine current readiness
                readiness = ReadinessLevel.NOT_STARTED
                if input_data.current_status and name in input_data.current_status:
                    readiness = input_data.current_status[name]
                
                states.append(State(
                    name=name,
                    description=desc,
                    indicators=indicators,
                    prerequisites=prerequisites,
                    readiness_level=readiness
                ))
            
            return states
        
        # Generate generic states based on scenario
        return await self._generate_generic_states(input_data, context)
    
    async def _generate_generic_states(
        self,
        input_data: SequentialReadinessInput,
        context: Context
    ) -> List[State]:
        """Generate generic states from scenario analysis."""
        
        scenario_lower = input_data.scenario.lower()
        
        # Determine appropriate state sequence
        if "implement" in scenario_lower or "deploy" in scenario_lower:
            # Implementation sequence
            return [
                State(
                    name="Assessment",
                    description="Assess current state and requirements",
                    indicators=["Requirements documented", "Baseline established"],
                    readiness_level=ReadinessLevel.NOT_STARTED
                ),
                State(
                    name="Preparation",
                    description="Prepare resources and environment",
                    indicators=["Resources allocated", "Environment ready"],
                    prerequisites=["Assessment"],
                    readiness_level=ReadinessLevel.NOT_STARTED
                ),
                State(
                    name="Implementation",
                    description="Execute the implementation",
                    indicators=["Solution deployed", "Initial testing complete"],
                    prerequisites=["Preparation"],
                    readiness_level=ReadinessLevel.NOT_STARTED
                ),
                State(
                    name="Validation",
                    description="Validate and refine",
                    indicators=["Acceptance criteria met", "Performance verified"],
                    prerequisites=["Implementation"],
                    readiness_level=ReadinessLevel.NOT_STARTED
                ),
                State(
                    name="Stabilization",
                    description="Stabilize and optimize",
                    indicators=["System stable", "Users satisfied"],
                    prerequisites=["Validation"],
                    readiness_level=ReadinessLevel.NOT_STARTED
                )
            ]
        
        elif "learn" in scenario_lower or "develop" in scenario_lower:
            # Learning sequence
            return [
                State(
                    name="Orientation",
                    description="Understanding the domain",
                    indicators=["Concepts understood", "Goals clear"],
                    readiness_level=ReadinessLevel.NOT_STARTED
                ),
                State(
                    name="Acquisition",
                    description="Acquiring knowledge and skills",
                    indicators=["Knowledge gained", "Basic skills demonstrated"],
                    prerequisites=["Orientation"],
                    readiness_level=ReadinessLevel.NOT_STARTED
                ),
                State(
                    name="Practice",
                    description="Applying in controlled settings",
                    indicators=["Exercises completed", "Feedback received"],
                    prerequisites=["Acquisition"],
                    readiness_level=ReadinessLevel.NOT_STARTED
                ),
                State(
                    name="Integration",
                    description="Integrating into work",
                    indicators=["Applied to real tasks", "Value demonstrated"],
                    prerequisites=["Practice"],
                    readiness_level=ReadinessLevel.NOT_STARTED
                ),
                State(
                    name="Proficiency",
                    description="Achieving proficiency",
                    indicators=["Consistent performance", "Independence achieved"],
                    prerequisites=["Integration"],
                    readiness_level=ReadinessLevel.NOT_STARTED
                )
            ]
        
        else:
            # Generic progression
            return [
                State(
                    name="Initiation",
                    description="Beginning the process",
                    indicators=["Process started", "Resources identified"],
                    readiness_level=ReadinessLevel.NOT_STARTED
                ),
                State(
                    name="Development",
                    description="Developing capabilities",
                    indicators=["Progress visible", "Milestones achieved"],
                    prerequisites=["Initiation"],
                    readiness_level=ReadinessLevel.NOT_STARTED
                ),
                State(
                    name="Maturation",
                    description="Reaching maturity",
                    indicators=["Capabilities demonstrated", "Consistency shown"],
                    prerequisites=["Development"],
                    readiness_level=ReadinessLevel.NOT_STARTED
                ),
                State(
                    name="Optimization",
                    description="Optimizing performance",
                    indicators=["Efficiency improved", "Excellence achieved"],
                    prerequisites=["Maturation"],
                    readiness_level=ReadinessLevel.NOT_STARTED
                ),
                State(
                    name="Sustainability",
                    description="Ensuring long-term success",
                    indicators=["Self-sustaining", "Continuous improvement"],
                    prerequisites=["Optimization"],
                    readiness_level=ReadinessLevel.NOT_STARTED
                )
            ]
    
    async def _analyze_transitions(
        self,
        states: List[State],
        input_data: SequentialReadinessInput,
        context: Context
    ) -> List[StateTransition]:
        """Analyze transitions between states."""
        
        transitions = []
        
        for i in range(len(states) - 1):
            from_state = states[i]
            to_state = states[i + 1]
            
            # Determine transition type
            transition_type = await self._determine_transition_type(
                from_state, to_state, input_data
            )
            
            # Generate requirements
            requirements = await self._generate_transition_requirements(
                from_state, to_state, input_data.domain_context
            )
            
            # Identify risks
            risks = await self._identify_transition_risks(
                from_state, to_state, input_data
            )
            
            # Generate strategies
            strategies = await self._generate_transition_strategies(
                from_state, to_state, transition_type
            )
            
            # Estimate success rate
            success_rate = await self._estimate_success_rate(
                from_state, to_state, input_data
            )
            
            transitions.append(StateTransition(
                from_state=from_state.name,
                to_state=to_state.name,
                transition_type=transition_type,
                requirements=requirements,
                risks=risks,
                strategies=strategies,
                success_rate=success_rate
            ))
        
        # Check for parallel opportunities
        parallel_transitions = await self._identify_parallel_opportunities(
            states, transitions, input_data
        )
        transitions.extend(parallel_transitions)
        
        return transitions
    
    async def _determine_transition_type(
        self,
        from_state: State,
        to_state: State,
        input_data: SequentialReadinessInput
    ) -> TransitionType:
        """Determine the type of transition between states."""
        
        # Check if states can be parallel
        if not any(from_state.name in prereq for prereq in to_state.prerequisites):
            return TransitionType.PARALLEL
        
        # Check if transition is optional
        if input_data.constraints and "flexibility" in input_data.constraints:
            if input_data.constraints["flexibility"] == "high":
                return TransitionType.OPTIONAL
        
        # Check if iterative
        if "practice" in to_state.name.lower() or "iteration" in to_state.description.lower():
            return TransitionType.ITERATIVE
        
        # Default to sequential
        return TransitionType.SEQUENTIAL
    
    async def _generate_transition_requirements(
        self,
        from_state: State,
        to_state: State,
        domain_context: Optional[str]
    ) -> List[str]:
        """Generate requirements for transition."""
        
        requirements = []
        
        # Common transition patterns
        transition_patterns = {
            ("Awareness", "Desire"): [
                "Clear communication of benefits",
                "Address concerns and resistance",
                "Leadership visible support"
            ],
            ("Knowledge", "Ability"): [
                "Hands-on practice opportunities",
                "Safe environment for mistakes",
                "Coaching and feedback available"
            ],
            ("Planning", "Execution"): [
                "Resources allocated and available",
                "Team assembled and ready",
                "Risks identified and mitigated"
            ],
            ("Pilot", "Deployment"): [
                "Pilot results positive",
                "Lessons learned incorporated",
                "Scaling plan developed"
            ]
        }
        
        # Check for matching pattern
        key = (from_state.name, to_state.name)
        if key in transition_patterns:
            requirements.extend(transition_patterns[key])
        else:
            # Generic requirements
            requirements.extend([
                f"{from_state.name} objectives achieved",
                f"Resources for {to_state.name} secured",
                f"Stakeholders ready for {to_state.name}"
            ])
        
        # Add domain-specific requirements
        if domain_context == "technology_adoption":
            requirements.append("Technical infrastructure ready")
        elif domain_context == "change_management":
            requirements.append("Change champions identified")
        
        return requirements[:4]  # Limit to 4 requirements
    
    async def _identify_transition_risks(
        self,
        from_state: State,
        to_state: State,
        input_data: SequentialReadinessInput
    ) -> List[str]:
        """Identify risks in transition."""
        
        risks = []
        
        # Common transition risks
        if "knowledge" in from_state.name.lower() and "ability" in to_state.name.lower():
            risks.extend([
                "Insufficient practice time",
                "Lack of real-world application",
                "No support during application"
            ])
        elif "pilot" in from_state.name.lower():
            risks.extend([
                "Pilot success not representative",
                "Scaling challenges underestimated",
                "Different user populations"
            ])
        elif "planning" in from_state.name.lower():
            risks.extend([
                "Plans too theoretical",
                "Resource estimates incorrect",
                "Unforeseen dependencies"
            ])
        
        # Add constraint-based risks
        if input_data.constraints:
            if "timeline" in input_data.constraints:
                risks.append("Time pressure causing shortcuts")
            if "budget" in input_data.constraints:
                risks.append("Resource constraints limiting quality")
        
        return risks[:3]  # Limit to 3 risks
    
    async def _generate_transition_strategies(
        self,
        from_state: State,
        to_state: State,
        transition_type: TransitionType
    ) -> List[str]:
        """Generate strategies for successful transition."""
        
        strategies = []
        
        if transition_type == TransitionType.SEQUENTIAL:
            strategies.extend([
                f"Complete all {from_state.name} requirements first",
                f"Gradual transition with overlap period",
                f"Clear handoff procedures"
            ])
        elif transition_type == TransitionType.PARALLEL:
            strategies.extend([
                f"Coordinate {from_state.name} and {to_state.name} activities",
                f"Share resources efficiently",
                f"Regular synchronization meetings"
            ])
        elif transition_type == TransitionType.ITERATIVE:
            strategies.extend([
                f"Plan multiple cycles through {to_state.name}",
                f"Incorporate feedback loops",
                f"Continuous improvement approach"
            ])
        
        # Add state-specific strategies
        if "learning" in to_state.description.lower():
            strategies.append("Structured learning path with milestones")
        if "implementation" in to_state.name.lower():
            strategies.append("Phased rollout with checkpoints")
        
        return strategies[:4]  # Limit to 4 strategies
    
    async def _estimate_success_rate(
        self,
        from_state: State,
        to_state: State,
        input_data: SequentialReadinessInput
    ) -> float:
        """Estimate success rate for transition."""
        
        base_rate = 0.7
        
        # Adjust based on readiness
        if from_state.readiness_level == ReadinessLevel.READY:
            base_rate += 0.1
        elif from_state.readiness_level == ReadinessLevel.NOT_STARTED:
            base_rate -= 0.1
        
        # Adjust based on support factors
        if input_data.success_factors:
            base_rate += len(input_data.success_factors) * 0.02
        
        # Adjust based on constraints
        if input_data.constraints:
            if "high_pressure" in str(input_data.constraints).lower():
                base_rate -= 0.1
            if "strong_support" in str(input_data.constraints).lower():
                base_rate += 0.1
        
        return min(0.95, max(0.3, base_rate))
    
    async def _identify_parallel_opportunities(
        self,
        states: List[State],
        transitions: List[StateTransition],
        input_data: SequentialReadinessInput
    ) -> List[StateTransition]:
        """Identify opportunities for parallel progression."""
        
        parallel_transitions = []
        
        # Look for states that could run in parallel
        for i in range(len(states) - 2):
            for j in range(i + 2, len(states)):
                state_i = states[i]
                state_j = states[j]
                
                # Check if they have no direct dependencies
                intermediate_states = [states[k].name for k in range(i + 1, j)]
                if not any(state_j.name in s.prerequisites for s in states[i+1:j]):
                    # Could potentially be parallel
                    if await self._can_be_parallel(state_i, state_j, input_data):
                        parallel_transitions.append(StateTransition(
                            from_state=state_i.name,
                            to_state=state_j.name,
                            transition_type=TransitionType.PARALLEL,
                            requirements=[
                                f"{state_i.name} at minimum viable level",
                                f"Resources available for parallel work"
                            ],
                            strategies=[
                                "Dedicated resources for each stream",
                                "Regular coordination meetings"
                            ]
                        ))
        
        return parallel_transitions
    
    async def _can_be_parallel(
        self,
        state1: State,
        state2: State,
        input_data: SequentialReadinessInput
    ) -> bool:
        """Check if two states can progress in parallel."""
        
        # Domain-specific rules
        if input_data.domain_context == "technology_adoption":
            # Training can happen parallel to technical setup
            if "training" in state1.name.lower() and "technical" in state2.name.lower():
                return True
            if "technical" in state1.name.lower() and "training" in state2.name.lower():
                return True
        
        # Generic rules
        if "planning" in state1.name.lower() and "preparation" in state2.name.lower():
            return True
        
        return False
    
    async def _assess_current_state(
        self,
        states: List[State],
        input_data: SequentialReadinessInput,
        context: Context
    ) -> str:
        """Assess current position in the sequence."""
        
        # Count readiness levels
        readiness_counts = {
            ReadinessLevel.NOT_STARTED: 0,
            ReadinessLevel.INITIATED: 0,
            ReadinessLevel.PROGRESSING: 0,
            ReadinessLevel.NEARLY_READY: 0,
            ReadinessLevel.READY: 0,
            ReadinessLevel.EXCEEDED: 0
        }
        
        for state in states:
            readiness_counts[state.readiness_level] += 1
        
        # Find current active state
        current_state = None
        for i, state in enumerate(states):
            if state.readiness_level in [ReadinessLevel.INITIATED, ReadinessLevel.PROGRESSING, ReadinessLevel.NEARLY_READY]:
                current_state = state
                break
        
        if not current_state:
            # Look for last completed
            for i in range(len(states) - 1, -1, -1):
                if states[i].readiness_level == ReadinessLevel.READY:
                    if i < len(states) - 1:
                        current_state = states[i + 1]
                    break
        
        if not current_state and states:
            current_state = states[0]
        
        # Build assessment
        assessment = f"## Current State Assessment\n\n"
        
        if current_state:
            progress_pct = sum(1 for s in states if s.readiness_level in [ReadinessLevel.READY, ReadinessLevel.EXCEEDED]) / len(states) * 100
            assessment += f"**Current Focus**: {current_state.name} ({current_state.readiness_level.value})\n"
            assessment += f"**Overall Progress**: {progress_pct:.0f}% complete\n\n"
        
        assessment += f"**State Distribution**:\n"
        assessment += f"- Completed: {readiness_counts[ReadinessLevel.READY] + readiness_counts[ReadinessLevel.EXCEEDED]}\n"
        assessment += f"- In Progress: {readiness_counts[ReadinessLevel.PROGRESSING] + readiness_counts[ReadinessLevel.NEARLY_READY]}\n"
        assessment += f"- Initiated: {readiness_counts[ReadinessLevel.INITIATED]}\n"
        assessment += f"- Not Started: {readiness_counts[ReadinessLevel.NOT_STARTED]}\n\n"
        
        # Assess momentum
        if readiness_counts[ReadinessLevel.PROGRESSING] > 1:
            assessment += "⚠️ **Multiple states in progress** - Risk of diluted focus\n"
        elif readiness_counts[ReadinessLevel.READY] > 0 and readiness_counts[ReadinessLevel.NOT_STARTED] > 2:
            assessment += "✅ **Good foundation established** - Ready to accelerate\n"
        elif readiness_counts[ReadinessLevel.NOT_STARTED] == len(states):
            assessment += "🚀 **At the beginning** - Focus on strong start\n"
        
        return assessment
    
    async def _perform_gap_analysis(
        self,
        states: List[State],
        input_data: SequentialReadinessInput,
        context: Context
    ) -> List[GapAnalysis]:
        """Perform gap analysis for each state."""
        
        gap_analyses = []
        
        for state in states:
            # Determine target readiness
            target_readiness = ReadinessLevel.READY
            if input_data.target_outcome and "rapid" in input_data.target_outcome.lower():
                # May accept lower readiness for speed
                target_readiness = ReadinessLevel.NEARLY_READY
            
            # Skip if already at or above target
            if state.readiness_level in [ReadinessLevel.READY, ReadinessLevel.EXCEEDED]:
                continue
            
            # Calculate gap size
            gap_size = self._calculate_gap_size(state.readiness_level, target_readiness)
            
            # Identify missing elements
            missing_elements = await self._identify_missing_elements(
                state, input_data
            )
            
            # Generate recommended actions
            recommended_actions = await self._generate_gap_closure_actions(
                state, missing_elements, input_data
            )
            
            # Estimate effort
            estimated_effort = await self._estimate_gap_closure_effort(
                state, gap_size, input_data
            )
            
            # Determine priority
            priority = await self._determine_gap_priority(
                state, states, input_data
            )
            
            gap_analyses.append(GapAnalysis(
                state_name=state.name,
                current_readiness=state.readiness_level,
                target_readiness=target_readiness,
                gap_size=gap_size,
                missing_elements=missing_elements,
                recommended_actions=recommended_actions,
                estimated_effort=estimated_effort,
                priority=priority
            ))
        
        return gap_analyses
    
    def _calculate_gap_size(
        self,
        current: ReadinessLevel,
        target: ReadinessLevel
    ) -> str:
        """Calculate the size of readiness gap."""
        
        levels = [
            ReadinessLevel.NOT_STARTED,
            ReadinessLevel.INITIATED,
            ReadinessLevel.PROGRESSING,
            ReadinessLevel.NEARLY_READY,
            ReadinessLevel.READY,
            ReadinessLevel.EXCEEDED
        ]
        
        current_idx = levels.index(current)
        target_idx = levels.index(target)
        gap = target_idx - current_idx
        
        if gap <= 1:
            return "small"
        elif gap <= 3:
            return "medium"
        else:
            return "large"
    
    async def _identify_missing_elements(
        self,
        state: State,
        input_data: SequentialReadinessInput
    ) -> List[str]:
        """Identify what's missing to reach target readiness."""
        
        missing = []
        
        # Check against indicators
        for indicator in state.indicators:
            missing.append(f"Achievement of: {indicator}")
        
        # Check prerequisites
        if state.prerequisites:
            missing.append(f"Completion of prerequisites: {', '.join(state.prerequisites)}")
        
        # Check enablers
        if state.enablers:
            for enabler in state.enablers:
                missing.append(f"Enabler needed: {enabler}")
        
        # Domain-specific elements
        if input_data.domain_context == "change_management":
            if state.name == "Desire":
                missing.append("Address resistance and concerns")
            elif state.name == "Knowledge":
                missing.append("Comprehensive training program")
        
        return missing[:5]  # Limit to 5 elements
    
    async def _generate_gap_closure_actions(
        self,
        state: State,
        missing_elements: List[str],
        input_data: SequentialReadinessInput
    ) -> List[str]:
        """Generate actions to close the gap."""
        
        actions = []
        
        # Generic actions based on state type
        if "awareness" in state.name.lower():
            actions.extend([
                "Conduct information sessions",
                "Create communication materials",
                "Engage leadership for messaging"
            ])
        elif "knowledge" in state.name.lower() or "skill" in state.name.lower():
            actions.extend([
                "Develop training curriculum",
                "Schedule training sessions",
                "Create practice environments"
            ])
        elif "implementation" in state.name.lower() or "execution" in state.name.lower():
            actions.extend([
                "Establish project teams",
                "Create detailed work plans",
                "Set up tracking mechanisms"
            ])
        
        # Add actions for missing elements
        for element in missing_elements[:2]:
            if "training" in element.lower():
                actions.append("Design and deliver targeted training")
            elif "resistance" in element.lower():
                actions.append("Conduct resistance management workshops")
            elif "resource" in element.lower():
                actions.append("Secure necessary resources")
        
        return actions[:5]  # Limit to 5 actions
    
    async def _estimate_gap_closure_effort(
        self,
        state: State,
        gap_size: str,
        input_data: SequentialReadinessInput
    ) -> str:
        """Estimate effort to close the gap."""
        
        # Base estimates
        effort_map = {
            "small": ["1-2 weeks", "2-3 weeks", "1 week"],
            "medium": ["3-4 weeks", "4-6 weeks", "2-4 weeks"],
            "large": ["6-8 weeks", "2-3 months", "1-2 months"]
        }
        
        # Adjust based on constraints
        if input_data.constraints and "timeline" in input_data.constraints:
            if "urgent" in input_data.constraints["timeline"].lower():
                return effort_map[gap_size][2]  # Compressed timeline
        
        # Adjust based on complexity
        if input_data.complexity_level == "complex":
            return effort_map[gap_size][1]  # Longer estimate
        
        return effort_map[gap_size][0]  # Default estimate
    
    async def _determine_gap_priority(
        self,
        state: State,
        all_states: List[State],
        input_data: SequentialReadinessInput
    ) -> str:
        """Determine priority for addressing the gap."""
        
        # Find state position
        state_idx = next(i for i, s in enumerate(all_states) if s.name == state.name)
        
        # Check if it's blocking other states
        blocking_count = sum(1 for s in all_states[state_idx + 1:] 
                           if state.name in s.prerequisites)
        
        if blocking_count > 2:
            return "high"
        elif blocking_count > 0:
            return "medium"
        
        # Check if it's on critical path
        if input_data.target_outcome and "critical" in input_data.target_outcome.lower():
            if state_idx < len(all_states) / 2:  # Early states more critical
                return "high"
        
        return "low"
    
    async def _create_progression_plan(
        self,
        states: List[State],
        transitions: List[StateTransition],
        gap_analyses: List[GapAnalysis],
        input_data: SequentialReadinessInput,
        context: Context
    ) -> ProgressionPlan:
        """Create plan for progressing through states."""
        
        # Determine strategy
        strategy = await self._determine_progression_strategy(
            states, transitions, input_data
        )
        
        # Generate rationale
        rationale = await self._generate_strategy_rationale(
            strategy, states, input_data
        )
        
        # Create phases
        phases = await self._create_progression_phases(
            states, strategy, gap_analyses, input_data
        )
        
        # Define milestones
        milestones = await self._define_milestones(
            states, phases, input_data
        )
        
        # Estimate timeline
        timeline = await self._estimate_timeline(
            phases, gap_analyses, input_data
        )
        
        # Define success criteria
        success_criteria = await self._define_success_criteria(
            states, input_data
        )
        
        # Identify risk mitigation
        risk_mitigation = await self._identify_risk_mitigation(
            transitions, input_data
        )
        
        # Calculate confidence
        confidence = await self._calculate_plan_confidence(
            strategy, gap_analyses, input_data
        )
        
        return ProgressionPlan(
            strategy=strategy,
            rationale=rationale,
            phases=phases,
            milestones=milestones,
            timeline=timeline,
            success_criteria=success_criteria,
            risk_mitigation=risk_mitigation,
            confidence_level=confidence
        )
    
    async def _determine_progression_strategy(
        self,
        states: List[State],
        transitions: List[StateTransition],
        input_data: SequentialReadinessInput
    ) -> ProgressionStrategy:
        """Determine the best progression strategy."""
        
        # Check for parallel opportunities
        parallel_count = sum(1 for t in transitions if t.transition_type == TransitionType.PARALLEL)
        
        if parallel_count > len(transitions) * 0.3:
            return ProgressionStrategy.PARALLEL
        
        # Check constraints
        if input_data.constraints:
            if "urgent" in str(input_data.constraints).lower():
                return ProgressionStrategy.ACCELERATED
            if "flexible" in str(input_data.constraints).lower():
                return ProgressionStrategy.ADAPTIVE
        
        # Check for iterative needs
        iterative_count = sum(1 for t in transitions if t.transition_type == TransitionType.ITERATIVE)
        if iterative_count > 0:
            return ProgressionStrategy.ITERATIVE
        
        # Default to linear
        return ProgressionStrategy.LINEAR
    
    async def _generate_strategy_rationale(
        self,
        strategy: ProgressionStrategy,
        states: List[State],
        input_data: SequentialReadinessInput
    ) -> str:
        """Generate rationale for chosen strategy."""
        
        if strategy == ProgressionStrategy.ACCELERATED:
            return f"Urgent timeline requires accelerated approach to meet {input_data.target_outcome or 'objectives'}"
        elif strategy == ProgressionStrategy.PARALLEL:
            return "Multiple independent workstreams allow parallel progression for efficiency"
        elif strategy == ProgressionStrategy.ITERATIVE:
            return "Complex learning and adaptation needs require iterative cycles"
        elif strategy == ProgressionStrategy.ADAPTIVE:
            return "High uncertainty requires adaptive approach with regular adjustments"
        else:
            return "Sequential dependencies require systematic linear progression"
    
    async def _create_progression_phases(
        self,
        states: List[State],
        strategy: ProgressionStrategy,
        gap_analyses: List[GapAnalysis],
        input_data: SequentialReadinessInput
    ) -> List[Dict[str, Any]]:
        """Create phases for the progression plan."""
        
        phases = []
        
        if strategy == ProgressionStrategy.ACCELERATED:
            # Combine states into fewer phases
            phase1_states = [s.name for s in states[:2]]
            phase2_states = [s.name for s in states[2:4]]
            phase3_states = [s.name for s in states[4:]]
            
            phases = [
                {
                    "phase": 1,
                    "name": "Foundation",
                    "states": phase1_states,
                    "focus": "Establish baseline and initial capabilities",
                    "duration": "25% of timeline"
                },
                {
                    "phase": 2,
                    "name": "Core Development",
                    "states": phase2_states,
                    "focus": "Build main capabilities",
                    "duration": "50% of timeline"
                },
                {
                    "phase": 3,
                    "name": "Optimization",
                    "states": phase3_states,
                    "focus": "Refine and sustain",
                    "duration": "25% of timeline"
                }
            ]
        
        elif strategy == ProgressionStrategy.PARALLEL:
            # Group states that can run in parallel
            phases = [
                {
                    "phase": 1,
                    "name": "Sequential Foundation",
                    "states": [states[0].name],
                    "parallel": False,
                    "duration": "20% of timeline"
                },
                {
                    "phase": 2,
                    "name": "Parallel Development",
                    "states": [s.name for s in states[1:3]],
                    "parallel": True,
                    "duration": "40% of timeline"
                },
                {
                    "phase": 3,
                    "name": "Integration",
                    "states": [s.name for s in states[3:]],
                    "parallel": False,
                    "duration": "40% of timeline"
                }
            ]
        
        else:
            # Linear phases
            for i, state in enumerate(states):
                gap = next((g for g in gap_analyses if g.state_name == state.name), None)
                duration = gap.estimated_effort if gap else "2-3 weeks"
                
                phases.append({
                    "phase": i + 1,
                    "name": state.name,
                    "states": [state.name],
                    "focus": state.description,
                    "duration": duration,
                    "priority": gap.priority if gap else "medium"
                })
        
        return phases
    
    async def _define_milestones(
        self,
        states: List[State],
        phases: List[Dict[str, Any]],
        input_data: SequentialReadinessInput
    ) -> List[str]:
        """Define key milestones for tracking progress."""
        
        milestones = []
        
        # Phase-based milestones
        for phase in phases:
            phase_states = phase.get("states", [])
            if phase_states:
                milestones.append(f"{phase_states[0]} initiated")
                if len(phase_states) > 1:
                    milestones.append(f"All {phase['name']} states progressing")
        
        # State completion milestones
        key_states = [states[0], states[len(states)//2], states[-1]]
        for state in key_states:
            milestones.append(f"{state.name} fully ready")
        
        # Outcome-based milestones
        if input_data.target_outcome:
            milestones.append(f"Target outcome achieved: {input_data.target_outcome}")
        
        return milestones[:8]  # Limit to 8 milestones
    
    async def _estimate_timeline(
        self,
        phases: List[Dict[str, Any]],
        gap_analyses: List[GapAnalysis],
        input_data: SequentialReadinessInput
    ) -> str:
        """Estimate overall timeline."""
        
        # Sum up phase durations
        total_weeks = 0
        
        for gap in gap_analyses:
            effort = gap.estimated_effort
            if "week" in effort:
                # Extract weeks
                parts = effort.split()
                if "-" in parts[0]:
                    avg = sum(int(x) for x in parts[0].split("-")) / 2
                    total_weeks += avg
                else:
                    total_weeks += int(parts[0])
            elif "month" in effort:
                # Convert months to weeks
                parts = effort.split()
                if "-" in parts[0]:
                    avg = sum(int(x) for x in parts[0].split("-")) / 2
                    total_weeks += avg * 4
                else:
                    total_weeks += int(parts[0]) * 4
        
        # Apply strategy multiplier
        if len(phases) > 0 and phases[0].get("parallel"):
            total_weeks *= 0.7  # Parallel execution saves time
        
        # Format timeline
        if total_weeks <= 12:
            return f"{int(total_weeks)} weeks"
        else:
            return f"{int(total_weeks / 4)} months"
    
    async def _define_success_criteria(
        self,
        states: List[State],
        input_data: SequentialReadinessInput
    ) -> List[str]:
        """Define criteria for successful progression."""
        
        criteria = []
        
        # State-based criteria
        criteria.append(f"All {len(states)} states reach 'Ready' level")
        criteria.append("Smooth transitions between states without regression")
        
        # Include user-defined criteria
        if input_data.success_factors:
            for factor in input_data.success_factors[:2]:
                criteria.append(f"Success factor maintained: {factor}")
        
        # Outcome criteria
        if input_data.target_outcome:
            criteria.append(f"Achievement of: {input_data.target_outcome}")
        
        # Quality criteria
        criteria.append("Stakeholder satisfaction maintained throughout")
        criteria.append("No critical blockers unresolved for >1 week")
        
        return criteria[:6]  # Limit to 6 criteria
    
    async def _identify_risk_mitigation(
        self,
        transitions: List[StateTransition],
        input_data: SequentialReadinessInput
    ) -> List[str]:
        """Identify strategies to mitigate progression risks."""
        
        mitigation = []
        
        # Aggregate risks from transitions
        all_risks = []
        for transition in transitions:
            all_risks.extend(transition.risks)
        
        # Common mitigation strategies
        if any("resistance" in risk.lower() for risk in all_risks):
            mitigation.append("Implement comprehensive change management program")
        
        if any("resource" in risk.lower() for risk in all_risks):
            mitigation.append("Establish resource buffer and contingency plans")
        
        if any("skill" in risk.lower() or "knowledge" in risk.lower() for risk in all_risks):
            mitigation.append("Invest in training and capability development")
        
        if any("time" in risk.lower() or "timeline" in risk.lower() for risk in all_risks):
            mitigation.append("Build schedule buffers and parallel paths")
        
        # Add generic strategies
        mitigation.extend([
            "Regular progress reviews and adjustments",
            "Early warning indicators for each state",
            "Stakeholder engagement throughout"
        ])
        
        return mitigation[:5]  # Limit to 5 strategies
    
    async def _calculate_plan_confidence(
        self,
        strategy: ProgressionStrategy,
        gap_analyses: List[GapAnalysis],
        input_data: SequentialReadinessInput
    ) -> float:
        """Calculate confidence in the progression plan."""
        
        base_confidence = 0.7
        
        # Adjust based on gaps
        high_priority_gaps = sum(1 for gap in gap_analyses if gap.priority == "high")
        if high_priority_gaps > 2:
            base_confidence -= 0.1
        elif high_priority_gaps == 0:
            base_confidence += 0.1
        
        # Adjust based on strategy fit
        if strategy == ProgressionStrategy.ACCELERATED and input_data.constraints:
            if "urgent" in str(input_data.constraints).lower():
                base_confidence += 0.05  # Strategy matches need
        
        # Adjust based on support factors
        if input_data.success_factors:
            base_confidence += min(0.15, len(input_data.success_factors) * 0.03)
        
        # Adjust based on stakeholder involvement
        if input_data.stakeholders and len(input_data.stakeholders) > 3:
            base_confidence += 0.05
        
        return min(0.95, max(0.4, base_confidence))
    
    async def _identify_critical_path(
        self,
        states: List[State],
        transitions: List[StateTransition],
        context: Context
    ) -> List[str]:
        """Identify the critical path through states."""
        
        # Build dependency graph
        dependencies = {}
        for state in states:
            dependencies[state.name] = state.prerequisites
        
        # Find longest path (critical path)
        critical_path = []
        
        # Start with states that have no prerequisites
        start_states = [s for s in states if not s.prerequisites]
        
        if start_states:
            # Use first start state
            current = start_states[0]
            critical_path.append(current.name)
            
            # Follow the chain
            while True:
                # Find states that depend on current
                next_states = [s for s in states 
                             if current.name in s.prerequisites]
                
                if not next_states:
                    break
                
                # Choose the one with most future dependencies
                next_state = max(next_states, 
                               key=lambda s: sum(1 for t in transitions 
                                               if t.from_state == s.name))
                critical_path.append(next_state.name)
                current = next_state
        
        else:
            # No clear start, use all states in order
            critical_path = [s.name for s in states]
        
        return critical_path
    
    def _create_dependency_map(
        self,
        states: List[State],
        transitions: List[StateTransition]
    ) -> Dict[str, List[str]]:
        """Create a map of dependencies between states."""
        
        dependency_map = {}
        
        for state in states:
            dependencies = []
            
            # Direct prerequisites
            dependencies.extend(state.prerequisites)
            
            # Dependencies from transitions
            for transition in transitions:
                if transition.to_state == state.name:
                    dependencies.append(transition.from_state)
            
            dependency_map[state.name] = list(set(dependencies))
        
        return dependency_map
    
    async def _assess_risks(
        self,
        states: List[State],
        transitions: List[StateTransition],
        gap_analyses: List[GapAnalysis],
        context: Context
    ) -> str:
        """Assess overall risks for the progression."""
        
        risk_assessment = "## Risk Assessment\n\n"
        
        # Aggregate risks
        transition_risks = []
        for transition in transitions:
            transition_risks.extend(transition.risks)
        
        # Categorize risks
        high_risks = []
        medium_risks = []
        
        # High risks: Multiple transitions affected
        risk_counts = {}
        for risk in transition_risks:
            risk_counts[risk] = risk_counts.get(risk, 0) + 1
        
        for risk, count in risk_counts.items():
            if count > 1:
                high_risks.append(f"{risk} (affects {count} transitions)")
            else:
                medium_risks.append(risk)
        
        # Add gap-based risks
        critical_gaps = [gap for gap in gap_analyses if gap.priority == "high"]
        if len(critical_gaps) > 2:
            high_risks.append("Multiple critical gaps requiring simultaneous attention")
        
        # Build assessment
        if high_risks:
            risk_assessment += f"**High Risks** 🔴\n"
            for risk in high_risks[:3]:
                risk_assessment += f"- {risk}\n"
            risk_assessment += "\n"
        
        if medium_risks:
            risk_assessment += f"**Medium Risks** 🟡\n"
            for risk in medium_risks[:3]:
                risk_assessment += f"- {risk}\n"
            risk_assessment += "\n"
        
        # Overall risk level
        risk_level = "High" if len(high_risks) > 2 else "Medium" if high_risks else "Low"
        risk_assessment += f"**Overall Risk Level**: {risk_level}\n\n"
        
        # Mitigation priority
        if risk_level == "High":
            risk_assessment += "⚠️ **Recommendation**: Implement risk mitigation before aggressive progression"
        else:
            risk_assessment += "✅ **Recommendation**: Risks are manageable with standard mitigation"
        
        return risk_assessment
    
    async def _generate_domain_insights(
        self,
        states: List[State],
        input_data: SequentialReadinessInput,
        context: Context
    ) -> List[str]:
        """Generate domain-specific insights."""
        
        insights = []
        
        if input_data.domain_context == "change_management":
            insights.extend([
                "Focus on addressing emotional resistance before knowledge gaps",
                "Change champions can accelerate Desire and Knowledge states",
                "Reinforcement often requires 3-6 months of consistent effort",
                "Early wins in Ability state crucial for momentum"
            ])
        
        elif input_data.domain_context == "skill_development":
            insights.extend([
                "Practice environments critical for Ability development",
                "Peer learning accelerates progression through middle states",
                "Mastery requires teaching opportunities",
                "Foundation strength determines overall progression speed"
            ])
        
        elif input_data.domain_context == "technology_adoption":
            insights.extend([
                "Pilot results heavily influence organization-wide adoption",
                "Technical and people readiness can progress in parallel",
                "Integration challenges often emerge during Deployment",
                "User feedback loops essential for Optimization"
            ])
        
        elif input_data.domain_context == "project_lifecycle":
            insights.extend([
                "Planning quality directly impacts Execution efficiency",
                "Monitoring must start early in Execution phase",
                "Stakeholder engagement critical at phase transitions",
                "Lessons learned often skipped but vital for improvement"
            ])
        
        # Generic insights
        insights.extend([
            "Sequential readiness reduces implementation risks",
            "Skipping states often leads to future regression",
            "Parallel opportunities exist but require coordination"
        ])
        
        return insights[:5]  # Top 5 insights
    
    def _create_visualization_data(
        self,
        states: List[State],
        transitions: List[StateTransition]
    ) -> Dict[str, Any]:
        """Create data for visualizing sequential progression."""
        
        # Convert readiness levels to numeric values
        readiness_values = {
            ReadinessLevel.NOT_STARTED: 0,
            ReadinessLevel.INITIATED: 0.2,
            ReadinessLevel.PROGRESSING: 0.5,
            ReadinessLevel.NEARLY_READY: 0.8,
            ReadinessLevel.READY: 1.0,
            ReadinessLevel.EXCEEDED: 1.2
        }
        
        viz_data = {
            "type": "sequential_flow",
            "states": [
                {
                    "name": state.name,
                    "readiness": readiness_values[state.readiness_level],
                    "indicators": len(state.indicators),
                    "blockers": len(state.blockers)
                }
                for state in states
            ],
            "transitions": [
                {
                    "from": t.from_state,
                    "to": t.to_state,
                    "type": t.transition_type.value,
                    "success_rate": t.success_rate or 0.7
                }
                for t in transitions
            ],
            "progression": {
                "completed": sum(1 for s in states if s.readiness_level == ReadinessLevel.READY),
                "total": len(states),
                "percentage": sum(1 for s in states if s.readiness_level == ReadinessLevel.READY) / len(states) * 100
            }
        }
        
        return viz_data
    
    async def _identify_key_decisions(
        self,
        states: List[State],
        gap_analyses: List[GapAnalysis],
        input_data: SequentialReadinessInput,
        context: Context
    ) -> List[str]:
        """Identify key decisions for progression."""
        
        decisions = []
        
        # Decisions for high-priority gaps
        for gap in gap_analyses:
            if gap.priority == "high":
                decisions.append(f"How to rapidly close the {gap.state_name} gap?")
        
        # Strategy decisions
        decisions.append("Should we pursue sequential or parallel progression?")
        decisions.append("What is the minimum viable readiness for each state?")
        
        # Resource decisions
        if input_data.constraints and "budget" in input_data.constraints:
            decisions.append("How to optimize resource allocation across states?")
        
        # Risk decisions
        decisions.append("Which risks require immediate mitigation?")
        decisions.append("Where should we build in buffers or contingencies?")
        
        # Stakeholder decisions
        if input_data.stakeholders:
            decisions.append("How to maintain stakeholder engagement throughout?")
        
        # Success decisions
        decisions.append("What constitutes 'good enough' for moving forward?")
        
        return decisions[:8]  # Top 8 decisions
    
    async def _create_monitoring_plan(
        self,
        states: List[State],
        transitions: List[StateTransition],
        context: Context
    ) -> List[str]:
        """Create plan for monitoring progression."""
        
        monitoring_plan = []
        
        # State-level monitoring
        monitoring_plan.append("Weekly assessment of readiness levels for each state")
        monitoring_plan.append("Track achievement of state indicators")
        
        # Transition monitoring
        monitoring_plan.append("Monitor transition success rates and duration")
        monitoring_plan.append("Identify and address transition blockers")
        
        # Progress monitoring
        monitoring_plan.append("Overall progression velocity tracking")
        monitoring_plan.append("Comparison against planned timeline")
        
        # Quality monitoring
        monitoring_plan.append("Stakeholder satisfaction surveys at key milestones")
        monitoring_plan.append("Quality checks at state transitions")
        
        # Risk monitoring
        monitoring_plan.append("Weekly risk assessment updates")
        monitoring_plan.append("Early warning indicators for each state")
        
        # Adaptation monitoring
        monitoring_plan.append("Monthly strategy effectiveness review")
        monitoring_plan.append("Continuous improvement opportunities")
        
        return monitoring_plan[:10]  # Top 10 items
    
    async def _create_overall_recommendation(
        self,
        states: List[State],
        progression_plan: ProgressionPlan,
        gap_analyses: List[GapAnalysis],
        context: Context
    ) -> str:
        """Create overall recommendation for sequential readiness."""
        
        recommendation = "## Overall Recommendation\n\n"
        
        # Current status
        ready_count = sum(1 for s in states if s.readiness_level == ReadinessLevel.READY)
        progress_pct = ready_count / len(states) * 100
        
        # Critical gaps
        critical_gaps = [gap for gap in gap_analyses if gap.priority == "high"]
        
        # Strategy summary
        recommendation += f"**Recommended Approach**: {progression_plan.strategy.value.replace('_', ' ').title()}\n\n"
        
        if critical_gaps:
            recommendation += f"**Immediate Priority**: Address {len(critical_gaps)} critical gaps:\n"
            for gap in critical_gaps[:2]:
                recommendation += f"- {gap.state_name}: {gap.recommended_actions[0]}\n"
            recommendation += "\n"
        
        # Key actions
        recommendation += "**Key Actions**:\n"
        
        if progress_pct < 20:
            recommendation += "1. Establish strong foundation in initial states\n"
            recommendation += "2. Build momentum with quick wins\n"
            recommendation += "3. Engage stakeholders early and often\n"
        elif progress_pct < 60:
            recommendation += "1. Maintain momentum through middle states\n"
            recommendation += "2. Address emerging blockers quickly\n"
            recommendation += "3. Prepare for complex later transitions\n"
        else:
            recommendation += "1. Focus on successful completion\n"
            recommendation += "2. Ensure sustainability measures\n"
            recommendation += "3. Capture and share lessons learned\n"
        
        # Success outlook
        recommendation += f"\n**Success Outlook**: "
        if progression_plan.confidence_level > 0.8:
            recommendation += "High - Clear path with manageable risks"
        elif progression_plan.confidence_level > 0.6:
            recommendation += "Moderate - Success likely with focused effort"
        else:
            recommendation += "Challenging - Requires careful management and adaptation"
        
        # Timeline
        recommendation += f"\n**Expected Timeline**: {progression_plan.timeline}\n"
        
        # Final insight
        recommendation += f"\n💡 **Key Insight**: "
        if len(critical_gaps) > 2:
            recommendation += "Focus on sequential gap closure to build momentum"
        elif progression_plan.strategy == ProgressionStrategy.PARALLEL:
            recommendation += "Leverage parallel opportunities for efficiency"
        else:
            recommendation += "Steady progression with clear milestones is key"
        
        return recommendation
    
    def _calculate_confidence(
        self,
        states: List[State],
        transitions: List[StateTransition],
        progression_plan: ProgressionPlan
    ) -> float:
        """Calculate overall confidence in the analysis."""
        
        confidence_factors = []
        
        # State clarity
        if all(len(s.indicators) >= 2 for s in states):
            confidence_factors.append(0.9)
        else:
            confidence_factors.append(0.7)
        
        # Transition clarity
        avg_success_rate = sum(t.success_rate or 0.7 for t in transitions) / len(transitions)
        confidence_factors.append(avg_success_rate)
        
        # Plan confidence
        confidence_factors.append(progression_plan.confidence_level)
        
        # Current progress
        ready_count = sum(1 for s in states if s.readiness_level == ReadinessLevel.READY)
        if ready_count > 0:
            confidence_factors.append(0.8)  # Some progress already made
        else:
            confidence_factors.append(0.6)  # Starting from scratch
        
        return sum(confidence_factors) / len(confidence_factors) if confidence_factors else 0.7


# Create FastMCP tool instance
async def analyze_sequential_readiness_tool(
    input_data: SequentialReadinessInput,
    context: Context
) -> SequentialReadinessAnalysis:
    """FastMCP tool for sequential readiness analysis."""
    
    tool = SequentialReadinessTool()
    return await tool.analyze_sequential_readiness(input_data, context)