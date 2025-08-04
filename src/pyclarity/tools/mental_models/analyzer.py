"""
Mental Models Analyzer

Core implementation of the mental models cognitive tool, applying structured
frameworks including First Principles, Opportunity Cost, Error Propagation,
Rubber Duck Debugging, Pareto Principle, and Occam's Razor.
"""

import asyncio
import random
import time
from typing import Any, Dict, List, Optional

from .models import (
    MentalModelAssumption,
    MentalModelContext,
    MentalModelInsight,
    MentalModelResult,
    MentalModelType,
    MentalModelUtils,
)


class MentalModelsAnalyzer:
    """Mental models cognitive tool analyzer"""

    def __init__(self):
        """Initialize the mental models analyzer"""
        self.tool_name = "Mental Models"
        self.version = "2.0.0"

        # Internal state for processing
        self._processing_start_time = 0.0

    async def analyze(self, context: MentalModelContext) -> MentalModelResult:
        """
        Analyze a problem using the specified mental model framework.

        Args:
            context: Mental model context with problem and model type

        Returns:
            MentalModelResult with insights and recommendations
        """
        self._processing_start_time = time.time()

        # Route to specific mental model implementation
        if context.model_type == MentalModelType.FIRST_PRINCIPLES:
            result = await self._apply_first_principles(context)
        elif context.model_type == MentalModelType.OPPORTUNITY_COST:
            result = await self._apply_opportunity_cost(context)
        elif context.model_type == MentalModelType.ERROR_PROPAGATION:
            result = await self._apply_error_propagation(context)
        elif context.model_type == MentalModelType.RUBBER_DUCK:
            result = await self._apply_rubber_duck(context)
        elif context.model_type == MentalModelType.PARETO_PRINCIPLE:
            result = await self._apply_pareto_principle(context)
        elif context.model_type == MentalModelType.OCCAMS_RAZOR:
            result = await self._apply_occams_razor(context)
        else:
            raise ValueError(f"Unsupported mental model: {context.model_type}")

        # Set processing time
        processing_time = time.time() - self._processing_start_time
        result.processing_time_ms = round(processing_time * 1000)

        return result

    async def _apply_first_principles(self, context: MentalModelContext) -> MentalModelResult:
        """Apply first principles thinking to the problem"""

        # Simulate processing time
        await asyncio.sleep(0.1)

        # Generate fundamental elements
        fundamental_elements = await self._identify_fundamental_elements(context.problem)

        # Generate insights based on first principles
        insights = [
            MentalModelInsight(
                insight=f"The fundamental constraint appears to be {fundamental_elements[0].lower()}",
                relevance_score=0.92,
                supporting_evidence="Breaking down the problem reveals this as the core bottleneck",
                category="Core Constraint"
            ),
            MentalModelInsight(
                insight=f"The system can be rebuilt from first principles by focusing on {fundamental_elements[1].lower()}",
                relevance_score=0.87,
                supporting_evidence="Fundamental analysis shows this as the key building block",
                category="Solution Path"
            ),
            MentalModelInsight(
                insight="Current assumptions may be masking simpler underlying solutions",
                relevance_score=0.79,
                supporting_evidence="First principles often reveal over-engineered approaches",
                category="Assumption Challenge"
            )
        ]

        # Generate recommendations
        recommendations = [
            f"Start by addressing the fundamental constraint: {fundamental_elements[0].lower()}",
            f"Build solution incrementally from {fundamental_elements[1].lower()}",
            "Question all current assumptions and approaches",
            "Focus on the core problem without inherited complexity"
        ]

        # Identify assumptions
        assumptions = [
            MentalModelAssumption(
                assumption="Current implementation approach is necessary",
                confidence=0.3,
                impact_if_wrong="May be over-engineering the solution",
                verification_method="Test simpler approaches"
            ),
            MentalModelAssumption(
                assumption="All current requirements are actually needed",
                confidence=0.4,
                impact_if_wrong="May be solving unnecessary problems",
                verification_method="Validate requirements with stakeholders"
            )
        ]

        return MentalModelResult(
            model_applied=MentalModelType.FIRST_PRINCIPLES,
            key_insights=insights,
            recommendations=recommendations,
            assumptions_identified=assumptions,
            fundamental_elements=fundamental_elements,
            limitations="First principles analysis may oversimplify complex domain-specific constraints",
            next_steps=[
                "Validate fundamental elements with domain experts",
                "Test simplified approach before full implementation",
                "Challenge remaining assumptions systematically"
            ]
        )

    async def _apply_opportunity_cost(self, context: MentalModelContext) -> MentalModelResult:
        """Apply opportunity cost analysis to the problem"""

        await asyncio.sleep(0.1)

        # Generate trade-offs
        trade_offs = [
            {
                "option": "Quick implementation",
                "benefit": "Faster time to market",
                "cost": "Technical debt and maintenance overhead"
            },
            {
                "option": "Comprehensive solution",
                "benefit": "Long-term stability and scalability",
                "cost": "Extended development time and higher upfront cost"
            },
            {
                "option": "Buy existing solution",
                "benefit": "Immediate availability and proven track record",
                "cost": "Vendor lock-in and customization limitations"
            }
        ]

        insights = [
            MentalModelInsight(
                insight="The highest opportunity cost comes from delaying the decision",
                relevance_score=0.91,
                supporting_evidence="Each day of delay compounds the costs of all alternatives",
                category="Decision Timing"
            ),
            MentalModelInsight(
                insight="Quick wins may have hidden long-term costs",
                relevance_score=0.84,
                supporting_evidence="Technical debt often exceeds initial development savings",
                category="Hidden Costs"
            ),
            MentalModelInsight(
                insight="The middle path often has the best risk/reward profile",
                relevance_score=0.78,
                supporting_evidence="Balanced approaches avoid extremes of both alternatives",
                category="Risk Management"
            )
        ]

        recommendations = [
            "Quantify the costs of delay to inform urgency",
            "Consider hybrid approaches that balance speed and quality",
            "Factor in long-term maintenance costs, not just development time",
            "Evaluate the cost of switching if initial choice proves wrong"
        ]

        return MentalModelResult(
            model_applied=MentalModelType.OPPORTUNITY_COST,
            key_insights=insights,
            recommendations=recommendations,
            trade_offs=trade_offs,
            assumptions_identified=[
                MentalModelAssumption(
                    assumption="All alternatives have been identified",
                    confidence=0.6,
                    impact_if_wrong="May miss optimal solutions",
                    verification_method="Brainstorm additional alternatives"
                )
            ],
            limitations="Opportunity cost analysis requires accurate cost estimation, which may be difficult to predict",
            next_steps=[
                "Quantify costs for each alternative",
                "Establish decision timeline and criteria",
                "Consider partial implementations to reduce risk"
            ]
        )

    async def _apply_error_propagation(self, context: MentalModelContext) -> MentalModelResult:
        """Apply error propagation analysis to the problem"""

        await asyncio.sleep(0.1)

        # Identify potential error paths
        error_paths = [
            "Input validation failure → Invalid data processing → Corrupt outputs",
            "Network timeout → Service unavailability → Cascade failure across dependent services",
            "Memory leak → Performance degradation → System instability → Complete service failure",
            "Configuration error → Wrong behavior → User confusion → Support overhead",
            "Security vulnerability → Data breach → Compliance violation → Legal consequences"
        ]

        insights = [
            MentalModelInsight(
                insight="Small errors at input boundaries can cascade into major system failures",
                relevance_score=0.89,
                supporting_evidence="Input validation failures often propagate through entire processing chains",
                category="Boundary Failures"
            ),
            MentalModelInsight(
                insight="Error propagation speed often exceeds error detection speed",
                relevance_score=0.86,
                supporting_evidence="Automated systems can propagate errors faster than humans can identify them",
                category="Detection Lag"
            ),
            MentalModelInsight(
                insight="Circuit breaker patterns can limit error propagation scope",
                relevance_score=0.81,
                supporting_evidence="Isolation mechanisms prevent cascade failures across system boundaries",
                category="Error Isolation"
            )
        ]

        recommendations = [
            "Implement robust input validation at all system boundaries",
            "Design circuit breakers to isolate failing subsystems",
            "Add comprehensive monitoring for early error detection",
            "Create graceful degradation paths for critical workflows",
            "Regular failure mode analysis and testing"
        ]

        return MentalModelResult(
            model_applied=MentalModelType.ERROR_PROPAGATION,
            key_insights=insights,
            recommendations=recommendations,
            error_paths=error_paths[:6],  # Limit to 6 as per model
            assumptions_identified=[
                MentalModelAssumption(
                    assumption="Current error handling is sufficient",
                    confidence=0.2,
                    impact_if_wrong="Errors may propagate unchecked through the system",
                    verification_method="Conduct failure mode analysis and chaos testing"
                )
            ],
            limitations="Error propagation analysis cannot predict all possible failure combinations",
            next_steps=[
                "Map detailed error propagation flows",
                "Implement circuit breaker patterns",
                "Conduct chaos engineering tests",
                "Establish error monitoring and alerting"
            ]
        )

    async def _apply_rubber_duck(self, context: MentalModelContext) -> MentalModelResult:
        """Apply rubber duck debugging method to the problem"""

        await asyncio.sleep(0.1)

        insights = [
            MentalModelInsight(
                insight="Explaining the problem out loud reveals hidden assumptions",
                relevance_score=0.85,
                supporting_evidence="Verbalization forces explicit reasoning about implicit knowledge",
                category="Assumption Discovery"
            ),
            MentalModelInsight(
                insight="The act of structured explanation often reveals the solution",
                relevance_score=0.82,
                supporting_evidence="Step-by-step breakdown exposes logical gaps and connections",
                category="Solution Emergence"
            ),
            MentalModelInsight(
                insight="Simple questions often have complex answers that weren't obvious",
                relevance_score=0.79,
                supporting_evidence="Basic questioning reveals complexity hidden by familiarity",
                category="Complexity Discovery"
            )
        ]

        recommendations = [
            "Walk through the problem step-by-step out loud",
            "Question every assumption as if explaining to a beginner",
            "Break down complex concepts into simple, verifiable components",
            "Ask 'why' at each step to ensure understanding",
            "Document the explanation process for future reference"
        ]

        # Generate structured explanation
        structured_explanation = f"""When we break down '{context.problem}' step by step:

1. What exactly is the problem? (Define clearly without jargon)
2. What have we tried already? (Document previous approaches)
3. What are we assuming? (Make implicit knowledge explicit)
4. Where are we getting stuck? (Identify specific roadblocks)
5. What would we do if we had unlimited resources? (Remove artificial constraints)

This methodical explanation process often reveals that the real problem is different from the perceived problem."""

        return MentalModelResult(
            model_applied=MentalModelType.RUBBER_DUCK,
            key_insights=insights,
            recommendations=recommendations,
            assumptions_identified=[
                MentalModelAssumption(
                    assumption="I fully understand the problem domain",
                    confidence=0.5,
                    impact_if_wrong="May be solving the wrong problem or missing key constraints",
                    verification_method="Explain the problem to someone unfamiliar with the domain"
                ),
                MentalModelAssumption(
                    assumption="The current approach is the right direction",
                    confidence=0.4,
                    impact_if_wrong="May be pursuing suboptimal or incorrect solution paths",
                    verification_method="Question each step of the current approach"
                )
            ],
            limitations="Rubber duck method effectiveness depends on the quality of self-questioning",
            next_steps=[
                "Schedule dedicated time for step-by-step explanation",
                "Find someone unfamiliar with the problem to explain to",
                "Document the explanation process and identified assumptions",
                "Question each revealed assumption systematically"
            ],
            simplified_explanation=structured_explanation
        )

    async def _apply_pareto_principle(self, context: MentalModelContext) -> MentalModelResult:
        """Apply Pareto Principle (80/20 rule) to the problem"""

        await asyncio.sleep(0.1)

        # Generate critical factors based on problem analysis
        critical_factors = await self._identify_critical_factors(context.problem)

        insights = [
            MentalModelInsight(
                insight=f"20% of factors ({critical_factors[0]}) likely drive 80% of the outcomes",
                relevance_score=0.87,
                supporting_evidence="Pareto distribution commonly appears in complex systems",
                category="Impact Concentration"
            ),
            MentalModelInsight(
                insight="Most effort is typically spent on low-impact activities",
                relevance_score=0.83,
                supporting_evidence="Human tendency to focus on easy tasks rather than important ones",
                category="Effort Misallocation"
            ),
            MentalModelInsight(
                insight="Small improvements in critical areas yield disproportionate results",
                relevance_score=0.80,
                supporting_evidence="High-leverage activities compound their impact",
                category="Leverage Points"
            )
        ]

        recommendations = [
            f"Focus primary effort on {critical_factors[0]} as the highest-impact factor",
            "Measure and monitor the critical 20% factors continuously",
            "Automate or eliminate low-impact activities where possible",
            "Allocate resources proportional to factor impact, not perceived urgency",
            "Regularly reassess what constitutes the critical 20%"
        ]

        return MentalModelResult(
            model_applied=MentalModelType.PARETO_PRINCIPLE,
            key_insights=insights,
            recommendations=recommendations,
            critical_factors=critical_factors[:5],  # Limit to 5 as per model
            assumptions_identified=[
                MentalModelAssumption(
                    assumption="Pareto distribution applies to this problem domain",
                    confidence=0.7,
                    impact_if_wrong="May over-focus on few factors while neglecting important distributed effects",
                    verification_method="Measure impact distribution across all factors"
                )
            ],
            limitations="Pareto analysis may oversimplify problems with more uniform impact distributions",
            next_steps=[
                "Quantify impact of each identified critical factor",
                "Implement focused interventions on top 20% factors",
                "Monitor results to validate Pareto distribution assumption",
                "Reassess factor criticality regularly"
            ]
        )

    async def _apply_occams_razor(self, context: MentalModelContext) -> MentalModelResult:
        """Apply Occam's Razor to find simplest viable solution"""

        await asyncio.sleep(0.1)

        # Generate simplified explanation
        simplified_explanation = await self._generate_simplified_explanation(context.problem)

        insights = [
            MentalModelInsight(
                insight="The simplest explanation that fits the facts is usually correct",
                relevance_score=0.88,
                supporting_evidence="Complex solutions often introduce unnecessary assumptions",
                category="Simplicity Principle"
            ),
            MentalModelInsight(
                insight="Adding complexity should require strong justification",
                relevance_score=0.84,
                supporting_evidence="Each additional component increases system fragility",
                category="Complexity Burden"
            ),
            MentalModelInsight(
                insight="Simple solutions are easier to understand, maintain, and debug",
                relevance_score=0.81,
                supporting_evidence="Cognitive load increases exponentially with solution complexity",
                category="Maintenance Advantage"
            )
        ]

        recommendations = [
            "Start with the simplest solution that could possibly work",
            "Add complexity only when simple solutions prove insufficient",
            "Regularly question whether existing complexity is still justified",
            "Prefer well-understood simple tools over sophisticated alternatives",
            "Document why complexity was added to prevent unnecessary accumulation"
        ]

        return MentalModelResult(
            model_applied=MentalModelType.OCCAMS_RAZOR,
            key_insights=insights,
            recommendations=recommendations,
            simplified_explanation=simplified_explanation,
            assumptions_identified=[
                MentalModelAssumption(
                    assumption="Simple solutions will be sufficient for the requirements",
                    confidence=0.6,
                    impact_if_wrong="May need to add complexity later, potentially requiring rework",
                    verification_method="Test simple solution against real requirements"
                ),
                MentalModelAssumption(
                    assumption="Complexity is not inherently required by the problem domain",
                    confidence=0.7,
                    impact_if_wrong="May oversimplify genuinely complex requirements",
                    verification_method="Validate requirements with domain experts"
                )
            ],
            limitations="Occam's Razor may oversimplify problems that have inherent complexity",
            next_steps=[
                "Implement the simplest viable solution first",
                "Test against real requirements and constraints",
                "Add complexity only when simple solution proves inadequate",
                "Document rationale for any added complexity"
            ]
        )

    async def _identify_fundamental_elements(self, problem: str) -> list[str]:
        """Identify fundamental elements for first principles analysis"""
        problem_lower = problem.lower()

        if any(word in problem_lower for word in ['database', 'data', 'storage', 'query']):
            return ["Data access patterns", "Storage constraints", "Query optimization", "Consistency requirements"]
        elif any(word in problem_lower for word in ['performance', 'speed', 'slow', 'optimize']):
            return ["Resource bottlenecks", "Processing efficiency", "Network latency", "Caching strategies"]
        elif any(word in problem_lower for word in ['scale', 'scaling', 'users', 'load']):
            return ["Capacity limits", "Resource allocation", "Distribution patterns", "State management"]
        elif any(word in problem_lower for word in ['security', 'auth', 'permission', 'access']):
            return ["Authentication mechanisms", "Authorization boundaries", "Data protection", "Trust relationships"]
        else:
            return ["Core requirements", "Resource constraints", "User needs", "System boundaries"]

    async def _identify_critical_factors(self, problem: str) -> list[str]:
        """Identify critical 20% factors for Pareto analysis"""
        problem_lower = problem.lower()

        if any(word in problem_lower for word in ['performance', 'speed', 'optimize']):
            return ["CPU utilization", "Memory allocation", "I/O bottlenecks", "Network latency", "Algorithm complexity"]
        elif any(word in problem_lower for word in ['user', 'experience', 'interface']):
            return ["User workflow efficiency", "Error handling", "Response time", "Information clarity", "Navigation design"]
        elif any(word in problem_lower for word in ['business', 'revenue', 'cost', 'profit']):
            return ["Customer acquisition cost", "Revenue per user", "Operational efficiency", "Market positioning", "Resource utilization"]
        elif any(word in problem_lower for word in ['team', 'organization', 'process']):
            return ["Communication effectiveness", "Decision-making speed", "Skill alignment", "Process bottlenecks", "Information flow"]
        else:
            return ["Primary constraint", "Key resource limitation", "Critical dependency", "Main user need", "Core functionality"]

    async def _generate_simplified_explanation(self, problem: str) -> str:
        """Generate simplified explanation for Occam's Razor analysis"""
        problem_lower = problem.lower()

        if any(word in problem_lower for word in ['database', 'data', 'query']):
            return "The system needs to store and retrieve data efficiently. The simplest approach is to use appropriate data structures and indexing."
        elif any(word in problem_lower for word in ['performance', 'slow', 'speed']):
            return "Something is taking too long. The simplest solution is to identify and eliminate the bottleneck causing the delay."
        elif any(word in problem_lower for word in ['user', 'interface', 'experience']):
            return "Users need to accomplish a task easily. The simplest approach is to remove unnecessary steps and make the required actions obvious."
        elif any(word in problem_lower for word in ['scale', 'growth', 'users']):
            return "The system needs to handle more load. The simplest approach is to increase capacity where the constraint exists."
        else:
            return "The core issue can likely be addressed directly without complex intermediary solutions or abstractions."
