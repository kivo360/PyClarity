# Clear Thinking FastMCP Server - Multi-Perspective Analysis Tool

"""
Multi-Perspective Analysis implementation for FastMCP server.

This tool analyzes situations from multiple stakeholder viewpoints to reveal
blind spots, conflicts, and opportunities for alignment and integration.
"""

from typing import Dict, List, Optional, Any
import asyncio
from fastmcp import Context

from ..models.multi_perspective import (
    MultiPerspectiveInput,
    MultiPerspectiveAnalysis,
    Perspective,
    PerspectiveComparison,
    BlindSpot,
    ConflictResolution,
    IntegrationOpportunity,
    PerspectiveType,
    AlignmentLevel,
    ConflictResolutionStrategy
)
from .base import CognitiveToolBase


class MultiPerspectiveTool(CognitiveToolBase):
    """Implements Multi-Perspective Analysis."""
    
    # Domain-specific perspective templates
    DOMAIN_PERSPECTIVES = {
        "organizational_change": [
            ("Leadership", PerspectiveType.STRATEGIC, ["Vision alignment", "ROI", "Speed"], 0.9),
            ("Employees", PerspectiveType.STAKEHOLDER, ["Job security", "Work satisfaction", "Growth"], 0.7),
            ("Customers", PerspectiveType.CUSTOMER, ["Service quality", "Continuity", "Value"], 0.8),
            ("HR Department", PerspectiveType.FUNCTIONAL, ["Policy compliance", "Culture", "Talent"], 0.6),
            ("Finance", PerspectiveType.ECONOMIC, ["Cost control", "Budget", "Efficiency"], 0.8)
        ],
        "product_development": [
            ("End Users", PerspectiveType.CUSTOMER, ["Usability", "Features", "Performance"], 0.9),
            ("Product Management", PerspectiveType.STRATEGIC, ["Market fit", "Roadmap", "Competition"], 0.8),
            ("Engineering", PerspectiveType.TECHNICAL, ["Feasibility", "Architecture", "Maintainability"], 0.7),
            ("Sales", PerspectiveType.FUNCTIONAL, ["Sellability", "Differentiation", "Pricing"], 0.7),
            ("Support", PerspectiveType.FUNCTIONAL, ["Supportability", "Documentation", "Training"], 0.6)
        ],
        "policy_making": [
            ("Citizens", PerspectiveType.STAKEHOLDER, ["Fairness", "Impact", "Rights"], 0.8),
            ("Government", PerspectiveType.REGULATORY, ["Compliance", "Feasibility", "Budget"], 0.9),
            ("Business", PerspectiveType.ECONOMIC, ["Cost", "Competitiveness", "Growth"], 0.7),
            ("NGOs", PerspectiveType.ETHICAL, ["Social good", "Environment", "Equity"], 0.6),
            ("Media", PerspectiveType.CULTURAL, ["Public interest", "Transparency", "Accountability"], 0.5)
        ]
    }
    
    async def analyze_multi_perspective(
        self,
        input_data: MultiPerspectiveInput,
        context: Context
    ) -> MultiPerspectiveAnalysis:
        """Main method to analyze multiple perspectives."""
        
        await context.progress("Starting multi-perspective analysis", 0.1)
        
        # Identify perspectives
        perspectives = await self._identify_perspectives(input_data, context)
        await context.progress("Perspectives identified", 0.2)
        
        # Compare perspectives
        comparisons = await self._compare_perspectives(perspectives, input_data, context)
        await context.progress("Perspective comparisons completed", 0.3)
        
        # Identify blind spots
        blind_spots = await self._identify_blind_spots(perspectives, comparisons, context)
        await context.progress("Blind spots identified", 0.4)
        
        # Generate conflict resolutions
        resolutions = await self._generate_conflict_resolutions(
            perspectives, comparisons, input_data, context
        )
        await context.progress("Conflict resolutions generated", 0.5)
        
        # Identify integration opportunities
        integration_opps = await self._identify_integration_opportunities(
            perspectives, comparisons, context
        )
        await context.progress("Integration opportunities identified", 0.6)
        
        # Create alignment matrix
        alignment_matrix = self._create_alignment_matrix(perspectives, comparisons)
        
        # Analyze influence
        influence_analysis = self._analyze_influence(perspectives)
        
        # Find consensus areas
        consensus_areas = await self._find_consensus_areas(perspectives, context)
        
        # Find divergence areas
        divergence_areas = await self._find_divergence_areas(perspectives, comparisons, context)
        
        # Generate synthesis insights
        synthesis_insights = await self._generate_synthesis_insights(
            perspectives, comparisons, blind_spots, context
        )
        
        # Create recommended approach
        recommended_approach = await self._create_recommended_approach(
            perspectives, resolutions, integration_opps, input_data, context
        )
        
        # Generate implementation considerations
        implementation_considerations = await self._generate_implementation_considerations(
            perspectives, resolutions, context
        )
        
        # Create communication strategy
        communication_strategy = await self._create_communication_strategy(
            perspectives, input_data, context
        )
        
        # Create visualization data
        viz_data = self._create_visualization_data(perspectives, comparisons)
        
        # Generate overall assessment
        overall_assessment = await self._create_overall_assessment(
            perspectives, comparisons, resolutions, context
        )
        
        # Calculate confidence
        confidence = self._calculate_confidence(perspectives, comparisons, resolutions)
        
        await context.progress("Analysis complete", 1.0)
        
        return MultiPerspectiveAnalysis(
            input_scenario=input_data.scenario,
            identified_perspectives=perspectives,
            perspective_comparisons=comparisons,
            blind_spots=blind_spots,
            conflict_resolutions=resolutions,
            integration_opportunities=integration_opps,
            alignment_matrix=alignment_matrix,
            influence_analysis=influence_analysis,
            consensus_areas=consensus_areas,
            divergence_areas=divergence_areas,
            synthesis_insights=synthesis_insights,
            recommended_approach=recommended_approach,
            implementation_considerations=implementation_considerations,
            communication_strategy=communication_strategy,
            visual_representation=viz_data,
            overall_assessment=overall_assessment,
            confidence_level=confidence
        )
    
    async def _identify_perspectives(
        self,
        input_data: MultiPerspectiveInput,
        context: Context
    ) -> List[Perspective]:
        """Identify relevant perspectives for analysis."""
        
        if input_data.predefined_perspectives:
            return input_data.predefined_perspectives
        
        perspectives = []
        
        # Use domain templates if available
        if input_data.domain_context and input_data.domain_context in self.DOMAIN_PERSPECTIVES:
            templates = self.DOMAIN_PERSPECTIVES[input_data.domain_context]
            
            for name, p_type, interests, influence in templates:
                # Customize based on scenario
                priorities = await self._determine_priorities(name, p_type, input_data)
                concerns = await self._determine_concerns(name, p_type, input_data)
                success_criteria = await self._determine_success_criteria(name, p_type, input_data)
                
                perspectives.append(Perspective(
                    name=name,
                    perspective_type=p_type,
                    key_interests=interests,
                    priorities=priorities,
                    concerns=concerns,
                    success_criteria=success_criteria,
                    influence_level=influence,
                    emotional_stance=await self._determine_emotional_stance(name, input_data)
                ))
        
        # Add from stakeholder map
        if input_data.stakeholder_map:
            for stakeholder, role in input_data.stakeholder_map.items():
                if not any(p.name == stakeholder for p in perspectives):
                    perspectives.append(await self._create_stakeholder_perspective(
                        stakeholder, role, input_data
                    ))
        
        # Ensure minimum perspectives
        if len(perspectives) < 3:
            perspectives.extend(await self._generate_generic_perspectives(input_data, context))
        
        return perspectives[:8]  # Limit to 8 perspectives for manageability
    
    async def _determine_priorities(
        self,
        name: str,
        p_type: PerspectiveType,
        input_data: MultiPerspectiveInput
    ) -> List[str]:
        """Determine priorities for a perspective."""
        
        priorities_map = {
            PerspectiveType.STRATEGIC: ["Long-term success", "Competitive advantage", "Growth"],
            PerspectiveType.STAKEHOLDER: ["Personal impact", "Fair treatment", "Opportunities"],
            PerspectiveType.CUSTOMER: ["Value received", "Quality", "Service"],
            PerspectiveType.TECHNICAL: ["Technical excellence", "Maintainability", "Innovation"],
            PerspectiveType.ECONOMIC: ["ROI", "Cost efficiency", "Financial stability"],
            PerspectiveType.ETHICAL: ["Fairness", "Social responsibility", "Transparency"]
        }
        
        return priorities_map.get(p_type, ["Success", "Efficiency", "Quality"])[:3]
    
    async def _determine_concerns(
        self,
        name: str,
        p_type: PerspectiveType,
        input_data: MultiPerspectiveInput
    ) -> List[str]:
        """Determine concerns for a perspective."""
        
        scenario_lower = input_data.scenario.lower()
        concerns = []
        
        if "change" in scenario_lower or "implement" in scenario_lower:
            if p_type == PerspectiveType.STAKEHOLDER:
                concerns.extend(["Disruption to current state", "Personal impact", "Uncertainty"])
            elif p_type == PerspectiveType.TECHNICAL:
                concerns.extend(["Technical debt", "Integration complexity", "Resource constraints"])
        
        if "cost" in scenario_lower or "budget" in scenario_lower:
            concerns.append("Financial implications")
        
        return concerns[:3]
    
    async def _determine_success_criteria(
        self,
        name: str,
        p_type: PerspectiveType,
        input_data: MultiPerspectiveInput
    ) -> List[str]:
        """Determine success criteria for a perspective."""
        
        criteria_map = {
            PerspectiveType.STRATEGIC: ["Strategic goals achieved", "Market position improved"],
            PerspectiveType.CUSTOMER: ["Needs met effectively", "Satisfaction increased"],
            PerspectiveType.TECHNICAL: ["System performs reliably", "Technical debt minimized"],
            PerspectiveType.ECONOMIC: ["ROI targets met", "Costs controlled"]
        }
        
        return criteria_map.get(p_type, ["Objectives achieved", "Quality maintained"])[:2]
    
    async def _determine_emotional_stance(
        self,
        name: str,
        input_data: MultiPerspectiveInput
    ) -> str:
        """Determine emotional stance of a perspective."""
        
        if "employee" in name.lower() and "change" in input_data.scenario.lower():
            return "resistant"
        elif "customer" in name.lower():
            return "expectant"
        elif "management" in name.lower() or "leadership" in name.lower():
            return "driving"
        else:
            return "neutral"
    
    async def _create_stakeholder_perspective(
        self,
        stakeholder: str,
        role: str,
        input_data: MultiPerspectiveInput
    ) -> Perspective:
        """Create perspective from stakeholder map entry."""
        
        # Determine type based on role
        p_type = PerspectiveType.STAKEHOLDER
        if "customer" in role.lower():
            p_type = PerspectiveType.CUSTOMER
        elif "technical" in role.lower() or "it" in role.lower():
            p_type = PerspectiveType.TECHNICAL
        elif "management" in role.lower() or "executive" in role.lower():
            p_type = PerspectiveType.STRATEGIC
        
        return Perspective(
            name=stakeholder,
            perspective_type=p_type,
            key_interests=["Role effectiveness", "Impact on work", "Future prospects"],
            priorities=await self._determine_priorities(stakeholder, p_type, input_data),
            concerns=await self._determine_concerns(stakeholder, p_type, input_data),
            success_criteria=await self._determine_success_criteria(stakeholder, p_type, input_data),
            influence_level=0.5,  # Default medium influence
            emotional_stance=await self._determine_emotional_stance(stakeholder, input_data)
        )
    
    async def _generate_generic_perspectives(
        self,
        input_data: MultiPerspectiveInput,
        context: Context
    ) -> List[Perspective]:
        """Generate generic perspectives based on scenario."""
        
        return [
            Perspective(
                name="Decision Makers",
                perspective_type=PerspectiveType.STRATEGIC,
                key_interests=["Outcomes", "Risks", "Benefits"],
                priorities=["Success", "Efficiency", "Sustainability"],
                success_criteria=["Goals achieved", "Risks managed"],
                influence_level=0.9
            ),
            Perspective(
                name="Implementers",
                perspective_type=PerspectiveType.FUNCTIONAL,
                key_interests=["Feasibility", "Resources", "Timeline"],
                priorities=["Clear requirements", "Adequate resources", "Realistic timeline"],
                success_criteria=["Delivered on time", "Quality standards met"],
                influence_level=0.7
            ),
            Perspective(
                name="Affected Parties",
                perspective_type=PerspectiveType.STAKEHOLDER,
                key_interests=["Impact", "Benefits", "Fairness"],
                priorities=["Minimal disruption", "Clear benefits", "Fair treatment"],
                success_criteria=["Positive impact", "Concerns addressed"],
                influence_level=0.6
            )
        ]
    
    async def _compare_perspectives(
        self,
        perspectives: List[Perspective],
        input_data: MultiPerspectiveInput,
        context: Context
    ) -> List[PerspectiveComparison]:
        """Compare all perspective pairs."""
        
        comparisons = []
        
        for i in range(len(perspectives)):
            for j in range(i + 1, len(perspectives)):
                p1, p2 = perspectives[i], perspectives[j]
                
                # Determine alignment level
                alignment = await self._determine_alignment(p1, p2)
                
                # Find common ground
                common_ground = await self._find_common_ground(p1, p2)
                
                # Identify conflicts
                conflicts = await self._identify_conflicts(p1, p2)
                
                # Find complementary aspects
                complementary = await self._find_complementary_aspects(p1, p2)
                
                # Identify tension points
                tensions = await self._identify_tension_points(p1, p2)
                
                # Find synergies
                synergies = await self._find_synergies(p1, p2)
                
                comparisons.append(PerspectiveComparison(
                    perspective_a=p1.name,
                    perspective_b=p2.name,
                    alignment_level=alignment,
                    common_ground=common_ground,
                    conflicts=conflicts,
                    complementary_aspects=complementary,
                    tension_points=tensions,
                    potential_synergies=synergies
                ))
        
        return comparisons
    
    async def _determine_alignment(
        self,
        p1: Perspective,
        p2: Perspective
    ) -> AlignmentLevel:
        """Determine alignment level between perspectives."""
        
        # Calculate overlap in interests and priorities
        interest_overlap = len(set(p1.key_interests) & set(p2.key_interests))
        priority_overlap = len(set(p1.priorities) & set(p2.priorities))
        
        # Check for direct conflicts
        if any(c1 in c2 or c2 in c1 for c1 in p1.concerns for c2 in p2.priorities):
            return AlignmentLevel.STRONG_CONFLICT
        
        # Calculate alignment score
        total_items = len(p1.key_interests) + len(p1.priorities) + len(p2.key_interests) + len(p2.priorities)
        overlap_score = (interest_overlap + priority_overlap) / (total_items / 4)
        
        if overlap_score > 0.6:
            return AlignmentLevel.STRONG_ALIGNMENT
        elif overlap_score > 0.4:
            return AlignmentLevel.MODERATE_ALIGNMENT
        elif overlap_score > 0.2:
            return AlignmentLevel.NEUTRAL
        elif overlap_score > 0.1:
            return AlignmentLevel.MODERATE_CONFLICT
        else:
            return AlignmentLevel.STRONG_CONFLICT
    
    async def _find_common_ground(
        self,
        p1: Perspective,
        p2: Perspective
    ) -> List[str]:
        """Find areas of agreement between perspectives."""
        
        common = []
        
        # Common interests
        for interest in p1.key_interests:
            if any(interest.lower() in i2.lower() or i2.lower() in interest.lower() 
                   for i2 in p2.key_interests):
                common.append(f"Shared interest in {interest}")
        
        # Common success criteria
        for criteria in p1.success_criteria:
            if any(criteria.lower() in c2.lower() or c2.lower() in criteria.lower()
                   for c2 in p2.success_criteria):
                common.append(f"Both want {criteria}")
        
        # Generic common ground
        if not common:
            common = ["Desire for positive outcome", "Interest in viable solution"]
        
        return common[:3]
    
    async def _identify_conflicts(
        self,
        p1: Perspective,
        p2: Perspective
    ) -> List[str]:
        """Identify conflicts between perspectives."""
        
        conflicts = []
        
        # Priority conflicts
        if "cost" in str(p1.priorities).lower() and "quality" in str(p2.priorities).lower():
            conflicts.append("Cost efficiency vs quality standards")
        
        if "speed" in str(p1.priorities).lower() and "thoroughness" in str(p2.priorities).lower():
            conflicts.append("Speed of delivery vs thoroughness")
        
        # Concern vs priority conflicts
        for concern in p1.concerns:
            for priority in p2.priorities:
                if any(word in concern.lower() for word in ["risk", "security", "stability"]) and \
                   any(word in priority.lower() for word in ["innovation", "change", "speed"]):
                    conflicts.append(f"{concern} vs {priority}")
        
        return conflicts[:3]
    
    async def _find_complementary_aspects(
        self,
        p1: Perspective,
        p2: Perspective
    ) -> List[str]:
        """Find ways perspectives complement each other."""
        
        complementary = []
        
        # Technical vs Business
        if p1.perspective_type == PerspectiveType.TECHNICAL and p2.perspective_type == PerspectiveType.STRATEGIC:
            complementary.append("Technical expertise complements strategic vision")
        
        # Customer vs Internal
        if p1.perspective_type == PerspectiveType.CUSTOMER and p2.perspective_type in [PerspectiveType.FUNCTIONAL, PerspectiveType.TECHNICAL]:
            complementary.append("External needs guide internal capabilities")
        
        # Short vs Long term
        if p1.perspective_type == PerspectiveType.TEMPORAL or p2.perspective_type == PerspectiveType.TEMPORAL:
            complementary.append("Different time horizons provide balance")
        
        return complementary[:2]
    
    async def _identify_tension_points(
        self,
        p1: Perspective,
        p2: Perspective
    ) -> List[str]:
        """Identify specific tension points."""
        
        tensions = []
        
        # Influence imbalance
        if abs(p1.influence_level - p2.influence_level) > 0.3:
            tensions.append("Significant influence imbalance")
        
        # Emotional stance differences
        if p1.emotional_stance and p2.emotional_stance:
            if p1.emotional_stance == "resistant" and p2.emotional_stance == "driving":
                tensions.append("Opposition between change resistance and drive")
        
        return tensions[:2]
    
    async def _find_synergies(
        self,
        p1: Perspective,
        p2: Perspective
    ) -> List[str]:
        """Find potential synergies between perspectives."""
        
        synergies = []
        
        # Complementary strengths
        if p1.perspective_type == PerspectiveType.CUSTOMER and p2.perspective_type == PerspectiveType.TECHNICAL:
            synergies.append("User needs can drive technical innovation")
        
        # Shared concerns leading to solutions
        common_concerns = set(p1.concerns) & set(p2.concerns)
        if common_concerns:
            synergies.append(f"Joint solutions for {list(common_concerns)[0]}")
        
        return synergies[:2]
    
    async def _identify_blind_spots(
        self,
        perspectives: List[Perspective],
        comparisons: List[PerspectiveComparison],
        context: Context
    ) -> List[BlindSpot]:
        """Identify blind spots across perspectives."""
        
        blind_spots = []
        
        # Check for missing perspective types
        existing_types = {p.perspective_type for p in perspectives}
        important_types = {
            PerspectiveType.CUSTOMER,
            PerspectiveType.TECHNICAL,
            PerspectiveType.ETHICAL,
            PerspectiveType.ECONOMIC
        }
        
        missing_types = important_types - existing_types
        for missing_type in missing_types:
            blind_spots.append(BlindSpot(
                description=f"Missing {missing_type.value} perspective",
                affected_perspectives=[p.name for p in perspectives],
                revealing_perspectives=[f"Potential {missing_type.value} stakeholder"],
                impact=f"May overlook {missing_type.value} considerations",
                mitigation_strategies=[f"Include {missing_type.value} expert in analysis"]
            ))
        
        # Check for unaddressed concerns
        all_concerns = set()
        for p in perspectives:
            all_concerns.update(p.concerns)
        
        addressed_in_priorities = set()
        for p in perspectives:
            addressed_in_priorities.update(p.priorities)
        
        unaddressed = all_concerns - addressed_in_priorities
        if unaddressed:
            concern = list(unaddressed)[0]
            affected = [p.name for p in perspectives if concern not in p.priorities]
            revealing = [p.name for p in perspectives if concern in p.concerns]
            
            blind_spots.append(BlindSpot(
                description=f"Unaddressed concern: {concern}",
                affected_perspectives=affected[:3],
                revealing_perspectives=revealing[:2] or ["External observer"],
                impact="May lead to unexpected resistance or failure",
                mitigation_strategies=["Address explicitly in planning", "Create mitigation plan"]
            ))
        
        return blind_spots[:5]
    
    async def _generate_conflict_resolutions(
        self,
        perspectives: List[Perspective],
        comparisons: List[PerspectiveComparison],
        input_data: MultiPerspectiveInput,
        context: Context
    ) -> List[ConflictResolution]:
        """Generate resolutions for identified conflicts."""
        
        resolutions = []
        
        # Find high-conflict comparisons
        high_conflicts = [c for c in comparisons 
                         if c.alignment_level in [AlignmentLevel.STRONG_CONFLICT, AlignmentLevel.MODERATE_CONFLICT]]
        
        for comparison in high_conflicts[:3]:  # Limit to top 3 conflicts
            # Determine resolution strategy
            strategy = await self._determine_resolution_strategy(comparison, input_data)
            
            # Generate action steps
            action_steps = await self._generate_resolution_steps(comparison, strategy)
            
            # Expected outcomes
            expected_outcomes = await self._generate_expected_outcomes(comparison, strategy)
            
            # Calculate success probability
            success_prob = await self._calculate_resolution_success(comparison, strategy, input_data)
            
            # Identify risks
            risks = await self._identify_resolution_risks(comparison, strategy)
            
            conflict_desc = comparison.conflicts[0] if comparison.conflicts else "Perspective misalignment"
            
            resolutions.append(ConflictResolution(
                conflict_description=conflict_desc,
                involved_perspectives=[comparison.perspective_a, comparison.perspective_b],
                resolution_strategy=strategy,
                action_steps=action_steps,
                expected_outcomes=expected_outcomes,
                success_probability=success_prob,
                risks=risks
            ))
        
        return resolutions
    
    async def _determine_resolution_strategy(
        self,
        comparison: PerspectiveComparison,
        input_data: MultiPerspectiveInput
    ) -> ConflictResolutionStrategy:
        """Determine best resolution strategy for a conflict."""
        
        # If there's significant common ground, try integration
        if len(comparison.common_ground) >= 2:
            return ConflictResolutionStrategy.INTEGRATION
        
        # If conflict tolerance is low, prioritize consensus
        if input_data.conflict_tolerance == "low":
            return ConflictResolutionStrategy.CONSENSUS_BUILDING
        
        # If there are synergies, try reframing
        if comparison.potential_synergies:
            return ConflictResolutionStrategy.REFRAMING
        
        # Default to compromise
        return ConflictResolutionStrategy.COMPROMISE
    
    async def _generate_resolution_steps(
        self,
        comparison: PerspectiveComparison,
        strategy: ConflictResolutionStrategy
    ) -> List[str]:
        """Generate action steps for resolution."""
        
        steps_map = {
            ConflictResolutionStrategy.INTEGRATION: [
                f"Joint workshop with {comparison.perspective_a} and {comparison.perspective_b}",
                "Identify shared objectives and complementary strengths",
                "Co-create integrated solution",
                "Establish ongoing collaboration mechanism"
            ],
            ConflictResolutionStrategy.COMPROMISE: [
                "Identify non-negotiable needs for each perspective",
                "Find middle ground on flexible areas",
                "Document agreed trade-offs",
                "Create review mechanism for adjustments"
            ],
            ConflictResolutionStrategy.REFRAMING: [
                "Redefine the problem to encompass both perspectives",
                "Identify higher-level shared goals",
                "Generate creative solutions for redefined problem",
                "Validate new approach with stakeholders"
            ],
            ConflictResolutionStrategy.CONSENSUS_BUILDING: [
                "Facilitate dialogue sessions",
                "Use structured consensus techniques",
                "Document areas of agreement progressively",
                "Address remaining differences systematically"
            ]
        }
        
        return steps_map.get(strategy, ["Engage in structured negotiation"])[:4]
    
    async def _generate_expected_outcomes(
        self,
        comparison: PerspectiveComparison,
        strategy: ConflictResolutionStrategy
    ) -> List[str]:
        """Generate expected outcomes from resolution."""
        
        outcomes = []
        
        if strategy == ConflictResolutionStrategy.INTEGRATION:
            outcomes.append("Stronger solution incorporating both perspectives")
            outcomes.append("Improved collaboration between groups")
        elif strategy == ConflictResolutionStrategy.COMPROMISE:
            outcomes.append("Acceptable solution for both parties")
            outcomes.append("Clear understanding of trade-offs")
        elif strategy == ConflictResolutionStrategy.REFRAMING:
            outcomes.append("New shared understanding of the problem")
            outcomes.append("Innovative solutions previously unconsidered")
        
        return outcomes[:3]
    
    async def _calculate_resolution_success(
        self,
        comparison: PerspectiveComparison,
        strategy: ConflictResolutionStrategy,
        input_data: MultiPerspectiveInput
    ) -> float:
        """Calculate probability of successful resolution."""
        
        base_prob = 0.6
        
        # Adjust based on alignment level
        if comparison.alignment_level == AlignmentLevel.MODERATE_CONFLICT:
            base_prob += 0.1
        elif comparison.alignment_level == AlignmentLevel.STRONG_CONFLICT:
            base_prob -= 0.1
        
        # Adjust based on common ground
        if len(comparison.common_ground) >= 3:
            base_prob += 0.15
        
        # Adjust based on strategy fit
        if strategy == ConflictResolutionStrategy.INTEGRATION and comparison.complementary_aspects:
            base_prob += 0.1
        
        return min(0.95, max(0.3, base_prob))
    
    async def _identify_resolution_risks(
        self,
        comparison: PerspectiveComparison,
        strategy: ConflictResolutionStrategy
    ) -> List[str]:
        """Identify risks in resolution approach."""
        
        risks = []
        
        if strategy == ConflictResolutionStrategy.COMPROMISE:
            risks.append("Neither party fully satisfied")
        elif strategy == ConflictResolutionStrategy.INTEGRATION:
            risks.append("Complexity of integrated solution")
        elif strategy == ConflictResolutionStrategy.PRIORITIZATION:
            risks.append("Alienation of deprioritized perspective")
        
        if comparison.tension_points:
            risks.append(f"Unresolved tension: {comparison.tension_points[0]}")
        
        return risks[:2]
    
    async def _identify_integration_opportunities(
        self,
        perspectives: List[Perspective],
        comparisons: List[PerspectiveComparison],
        context: Context
    ) -> List[IntegrationOpportunity]:
        """Identify opportunities to integrate perspectives."""
        
        opportunities = []
        
        # Look for complementary perspectives
        for comparison in comparisons:
            if comparison.complementary_aspects and comparison.alignment_level != AlignmentLevel.STRONG_CONFLICT:
                
                # Find the actual perspective objects
                p1 = next((p for p in perspectives if p.name == comparison.perspective_a), None)
                p2 = next((p for p in perspectives if p.name == comparison.perspective_b), None)
                
                if p1 and p2:
                    opportunity = await self._create_integration_opportunity(p1, p2, comparison)
                    if opportunity:
                        opportunities.append(opportunity)
        
        # Look for multi-perspective integration
        if len(perspectives) >= 4:
            multi_opp = await self._create_multi_perspective_opportunity(perspectives)
            if multi_opp:
                opportunities.append(multi_opp)
        
        return opportunities[:3]
    
    async def _create_integration_opportunity(
        self,
        p1: Perspective,
        p2: Perspective,
        comparison: PerspectiveComparison
    ) -> Optional[IntegrationOpportunity]:
        """Create integration opportunity from two perspectives."""
        
        if not comparison.complementary_aspects:
            return None
        
        return IntegrationOpportunity(
            opportunity_description=f"Integrate {p1.name} and {p2.name} perspectives",
            perspectives_to_integrate=[p1.name, p2.name],
            integration_approach=comparison.complementary_aspects[0],
            expected_benefits=[
                "Holistic solution addressing multiple needs",
                "Reduced conflict through collaboration",
                "Leveraged strengths of both perspectives"
            ],
            implementation_steps=[
                "Create joint task force",
                "Define integrated objectives",
                "Develop collaborative processes",
                "Monitor and adjust integration"
            ],
            complexity_level="medium"
        )
    
    async def _create_multi_perspective_opportunity(
        self,
        perspectives: List[Perspective]
    ) -> Optional[IntegrationOpportunity]:
        """Create opportunity to integrate multiple perspectives."""
        
        # Find perspectives with moderate to high influence
        key_perspectives = [p for p in perspectives if p.influence_level >= 0.6]
        
        if len(key_perspectives) >= 3:
            return IntegrationOpportunity(
                opportunity_description="Multi-stakeholder collaborative framework",
                perspectives_to_integrate=[p.name for p in key_perspectives[:4]],
                integration_approach="Create steering committee with key stakeholders",
                expected_benefits=[
                    "Comprehensive solution with broad buy-in",
                    "Balanced approach considering all key views",
                    "Sustainable implementation with stakeholder support"
                ],
                implementation_steps=[
                    "Establish governance structure",
                    "Define decision-making process",
                    "Create communication channels",
                    "Implement feedback loops"
                ],
                complexity_level="high"
            )
        
        return None
    
    def _create_alignment_matrix(
        self,
        perspectives: List[Perspective],
        comparisons: List[PerspectiveComparison]
    ) -> Dict[str, Dict[str, AlignmentLevel]]:
        """Create matrix of alignment levels between all perspectives."""
        
        matrix = {}
        
        for p in perspectives:
            matrix[p.name] = {}
            
            for p2 in perspectives:
                if p.name == p2.name:
                    matrix[p.name][p2.name] = AlignmentLevel.STRONG_ALIGNMENT
                else:
                    # Find comparison
                    comp = next((c for c in comparisons 
                               if (c.perspective_a == p.name and c.perspective_b == p2.name) or
                                  (c.perspective_a == p2.name and c.perspective_b == p.name)), None)
                    
                    if comp:
                        matrix[p.name][p2.name] = comp.alignment_level
                    else:
                        matrix[p.name][p2.name] = AlignmentLevel.NEUTRAL
        
        return matrix
    
    def _analyze_influence(
        self,
        perspectives: List[Perspective]
    ) -> Dict[str, float]:
        """Analyze influence levels of perspectives."""
        
        return {p.name: p.influence_level for p in perspectives}
    
    async def _find_consensus_areas(
        self,
        perspectives: List[Perspective],
        context: Context
    ) -> List[str]:
        """Find areas where most perspectives agree."""
        
        consensus_areas = []
        
        # Check interests
        all_interests = []
        for p in perspectives:
            all_interests.extend(p.key_interests)
        
        # Count occurrences
        interest_counts = {}
        for interest in all_interests:
            interest_lower = interest.lower()
            for key in interest_counts:
                if interest_lower in key.lower() or key.lower() in interest_lower:
                    interest_counts[key] += 1
                    break
            else:
                interest_counts[interest] = 1
        
        # Find high-consensus items
        threshold = len(perspectives) * 0.6
        for interest, count in interest_counts.items():
            if count >= threshold:
                consensus_areas.append(f"Shared interest in {interest}")
        
        # Generic consensus areas
        consensus_areas.extend([
            "Desire for successful outcome",
            "Need for clear communication",
            "Importance of stakeholder engagement"
        ])
        
        return consensus_areas[:5]
    
    async def _find_divergence_areas(
        self,
        perspectives: List[Perspective],
        comparisons: List[PerspectiveComparison],
        context: Context
    ) -> List[str]:
        """Find areas of significant divergence."""
        
        divergence_areas = []
        
        # Collect all conflicts
        for comp in comparisons:
            if comp.conflicts:
                divergence_areas.extend(comp.conflicts)
        
        # Add perspective-specific divergences
        if any(p.perspective_type == PerspectiveType.TEMPORAL for p in perspectives):
            divergence_areas.append("Time horizon differences (short vs long term)")
        
        if any(p.emotional_stance == "resistant" for p in perspectives) and \
           any(p.emotional_stance == "driving" for p in perspectives):
            divergence_areas.append("Change readiness levels")
        
        # Remove duplicates and limit
        unique_divergences = list(set(divergence_areas))
        return unique_divergences[:5]
    
    async def _generate_synthesis_insights(
        self,
        perspectives: List[Perspective],
        comparisons: List[PerspectiveComparison],
        blind_spots: List[BlindSpot],
        context: Context
    ) -> List[str]:
        """Generate insights from synthesizing all perspectives."""
        
        insights = []
        
        # Insight about influence distribution
        high_influence = [p for p in perspectives if p.influence_level >= 0.8]
        low_influence = [p for p in perspectives if p.influence_level <= 0.4]
        
        if high_influence and low_influence:
            insights.append("Significant influence imbalance may marginalize important perspectives")
        
        # Insight about alignment patterns
        conflict_count = sum(1 for c in comparisons 
                           if c.alignment_level in [AlignmentLevel.STRONG_CONFLICT, AlignmentLevel.MODERATE_CONFLICT])
        if conflict_count > len(comparisons) / 2:
            insights.append("High conflict level suggests need for extensive alignment efforts")
        
        # Insight about blind spots
        if blind_spots:
            insights.append(f"Critical blind spot: {blind_spots[0].description}")
        
        # Insight about emotional dynamics
        emotional_stances = [p.emotional_stance for p in perspectives if p.emotional_stance]
        if "resistant" in emotional_stances and "driving" in emotional_stances:
            insights.append("Emotional divide between change agents and resisters needs addressing")
        
        # Generic insights
        insights.extend([
            "Success requires balancing multiple valid viewpoints",
            "Integration opportunities exist despite conflicts",
            "Stakeholder engagement crucial for implementation"
        ])
        
        return insights[:6]
    
    async def _create_recommended_approach(
        self,
        perspectives: List[Perspective],
        resolutions: List[ConflictResolution],
        integration_opps: List[IntegrationOpportunity],
        input_data: MultiPerspectiveInput,
        context: Context
    ) -> str:
        """Create overall recommended approach."""
        
        approach = "## Recommended Multi-Perspective Approach\n\n"
        
        # Prioritize based on influence
        high_influence_perspectives = sorted(
            [p for p in perspectives if p.influence_level >= 0.7],
            key=lambda x: x.influence_level,
            reverse=True
        )
        
        if high_influence_perspectives:
            approach += f"**Primary Focus**: Address needs of {high_influence_perspectives[0].name} "
            approach += f"while ensuring {high_influence_perspectives[1].name if len(high_influence_perspectives) > 1 else 'other stakeholders'} support.\n\n"
        
        # Resolution priority
        if resolutions:
            approach += "**Conflict Resolution Priority**:\n"
            for i, res in enumerate(resolutions[:2], 1):
                approach += f"{i}. {res.conflict_description} - Use {res.resolution_strategy.value} approach\n"
            approach += "\n"
        
        # Integration strategy
        if integration_opps:
            approach += "**Integration Strategy**:\n"
            approach += f"- {integration_opps[0].opportunity_description}\n"
            approach += f"- Approach: {integration_opps[0].integration_approach}\n\n"
        
        # Phasing
        approach += "**Implementation Phases**:\n"
        approach += "1. **Alignment Phase**: Build consensus on shared goals\n"
        approach += "2. **Integration Phase**: Implement collaborative solutions\n"
        approach += "3. **Optimization Phase**: Refine based on multi-perspective feedback\n\n"
        
        # Success factors
        approach += "**Critical Success Factors**:\n"
        approach += "- Maintain open dialogue between all perspectives\n"
        approach += "- Address high-influence stakeholder concerns early\n"
        approach += "- Create feedback mechanisms for continuous adjustment"
        
        return approach
    
    async def _generate_implementation_considerations(
        self,
        perspectives: List[Perspective],
        resolutions: List[ConflictResolution],
        context: Context
    ) -> List[str]:
        """Generate key implementation considerations."""
        
        considerations = []
        
        # Power dynamics
        influence_variance = max(p.influence_level for p in perspectives) - min(p.influence_level for p in perspectives)
        if influence_variance > 0.5:
            considerations.append("Manage power imbalances to ensure all voices are heard")
        
        # Change resistance
        if any(p.emotional_stance == "resistant" for p in perspectives):
            considerations.append("Implement change management strategies for resistant groups")
        
        # Resource allocation
        considerations.append("Allocate resources proportionally to stakeholder needs")
        
        # Communication needs
        considerations.append("Tailor communication strategies to each perspective")
        
        # Monitoring
        considerations.append("Establish metrics meaningful to all stakeholders")
        
        # Flexibility
        considerations.append("Build in adaptation mechanisms for emerging concerns")
        
        return considerations[:6]
    
    async def _create_communication_strategy(
        self,
        perspectives: List[Perspective],
        input_data: MultiPerspectiveInput,
        context: Context
    ) -> List[str]:
        """Create communication strategy for different perspectives."""
        
        strategies = []
        
        for p in perspectives[:4]:  # Top 4 perspectives
            if p.perspective_type == PerspectiveType.STRATEGIC:
                strategies.append(f"For {p.name}: Focus on strategic outcomes and ROI")
            elif p.perspective_type == PerspectiveType.STAKEHOLDER:
                strategies.append(f"For {p.name}: Emphasize personal benefits and support")
            elif p.perspective_type == PerspectiveType.CUSTOMER:
                strategies.append(f"For {p.name}: Highlight value delivery and service improvements")
            elif p.perspective_type == PerspectiveType.TECHNICAL:
                strategies.append(f"For {p.name}: Provide detailed technical plans and support")
            else:
                strategies.append(f"For {p.name}: Address specific concerns and priorities")
        
        # General strategies
        strategies.extend([
            "Use multiple communication channels for reach",
            "Create feedback loops for two-way communication",
            "Regular updates on progress from all perspectives"
        ])
        
        return strategies[:7]
    
    def _create_visualization_data(
        self,
        perspectives: List[Perspective],
        comparisons: List[PerspectiveComparison]
    ) -> Dict[str, Any]:
        """Create data for visualizing perspective relationships."""
        
        # Create network graph data
        nodes = [
            {
                "id": p.name,
                "type": p.perspective_type.value,
                "influence": p.influence_level,
                "stance": p.emotional_stance or "neutral"
            }
            for p in perspectives
        ]
        
        # Create edges from comparisons
        edges = []
        for comp in comparisons:
            edges.append({
                "source": comp.perspective_a,
                "target": comp.perspective_b,
                "alignment": comp.alignment_level.value,
                "weight": 1.0 if comp.alignment_level in [AlignmentLevel.STRONG_ALIGNMENT, AlignmentLevel.MODERATE_ALIGNMENT] else 0.5
            })
        
        return {
            "type": "network_graph",
            "nodes": nodes,
            "edges": edges,
            "layout": "force-directed",
            "metrics": {
                "total_perspectives": len(perspectives),
                "conflict_ratio": sum(1 for c in comparisons if "conflict" in c.alignment_level.value) / len(comparisons) if comparisons else 0,
                "avg_influence": sum(p.influence_level for p in perspectives) / len(perspectives) if perspectives else 0
            }
        }
    
    async def _create_overall_assessment(
        self,
        perspectives: List[Perspective],
        comparisons: List[PerspectiveComparison],
        resolutions: List[ConflictResolution],
        context: Context
    ) -> str:
        """Create overall assessment of multi-perspective landscape."""
        
        assessment = "## Overall Multi-Perspective Assessment\n\n"
        
        # Perspective diversity
        unique_types = len(set(p.perspective_type for p in perspectives))
        assessment += f"**Perspective Diversity**: {unique_types} different viewpoint types across {len(perspectives)} stakeholders\n\n"
        
        # Alignment summary
        conflict_count = sum(1 for c in comparisons if "conflict" in c.alignment_level.value)
        alignment_count = sum(1 for c in comparisons if "alignment" in c.alignment_level.value and "conflict" not in c.alignment_level.value)
        
        assessment += f"**Alignment Landscape**:\n"
        assessment += f"- Aligned relationships: {alignment_count}\n"
        assessment += f"- Conflicted relationships: {conflict_count}\n"
        assessment += f"- Neutral relationships: {len(comparisons) - alignment_count - conflict_count}\n\n"
        
        # Influence distribution
        high_influence = sum(1 for p in perspectives if p.influence_level >= 0.7)
        assessment += f"**Power Dynamics**: {high_influence} high-influence stakeholders\n\n"
        
        # Resolution outlook
        if resolutions:
            avg_success = sum(r.success_probability for r in resolutions) / len(resolutions)
            assessment += f"**Conflict Resolution Outlook**: {avg_success:.0%} average success probability\n\n"
        
        # Overall recommendation
        if conflict_count > len(comparisons) / 2:
            assessment += "⚠️ **Key Finding**: High conflict level requires intensive alignment efforts"
        elif alignment_count > len(comparisons) / 2:
            assessment += "✅ **Key Finding**: Strong alignment foundation enables collaborative approach"
        else:
            assessment += "📊 **Key Finding**: Mixed alignment landscape requires targeted interventions"
        
        return assessment
    
    def _calculate_confidence(
        self,
        perspectives: List[Perspective],
        comparisons: List[PerspectiveComparison],
        resolutions: List[ConflictResolution]
    ) -> float:
        """Calculate confidence in the multi-perspective analysis."""
        
        confidence_factors = []
        
        # Perspective completeness
        if len(perspectives) >= 5:
            confidence_factors.append(0.9)
        elif len(perspectives) >= 3:
            confidence_factors.append(0.7)
        else:
            confidence_factors.append(0.5)
        
        # Analysis depth
        if comparisons and len(comparisons) >= len(perspectives) * (len(perspectives) - 1) / 4:
            confidence_factors.append(0.8)
        else:
            confidence_factors.append(0.6)
        
        # Resolution quality
        if resolutions:
            avg_resolution_confidence = sum(r.success_probability for r in resolutions) / len(resolutions)
            confidence_factors.append(avg_resolution_confidence)
        
        return sum(confidence_factors) / len(confidence_factors) if confidence_factors else 0.7


# Create FastMCP tool instance
async def analyze_multi_perspective_tool(
    input_data: MultiPerspectiveInput,
    context: Context
) -> MultiPerspectiveAnalysis:
    """FastMCP tool for multi-perspective analysis."""
    
    tool = MultiPerspectiveTool()
    return await tool.analyze_multi_perspective(input_data, context)