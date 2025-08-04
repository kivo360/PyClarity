"""
Stakeholder Alignment Component

Aligns stakeholders through influence mapping, consensus building,
and strategic communication orchestration.
"""

import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, List, Set, Tuple

from .models import (
    DecisionContext,
    DecisionState,
    StakeholderAlignment,
)

logger = logging.getLogger(__name__)


class StakeholderAligner:
    """Aligns stakeholders for strategic decisions."""

    async def align_stakeholders(self, context: DecisionContext) -> StakeholderAlignment:
        """Align stakeholders through systematic engagement."""
        try:
            stakeholder_mapping = await self._map_stakeholders(context)
            alignment_analysis = await self._analyze_alignment(context, stakeholder_mapping)
            influence_dynamics = await self._analyze_influence_dynamics(stakeholder_mapping)
            consensus_building = await self._build_consensus_strategy(context, alignment_analysis)
            communication_strategy = await self._develop_communication_strategy(context, stakeholder_mapping)
            resistance_management = await self._plan_resistance_management(alignment_analysis)

            readiness_score = self._calculate_alignment_readiness(
                alignment_analysis, influence_dynamics, consensus_building
            )

            recommendations = self._generate_alignment_recommendations(
                alignment_analysis, influence_dynamics, resistance_management
            )

            return StakeholderAlignment(
                readiness_score=readiness_score,
                stakeholder_mapping=stakeholder_mapping,
                alignment_analysis=alignment_analysis,
                influence_dynamics=influence_dynamics,
                consensus_building=consensus_building,
                communication_strategy=communication_strategy,
                resistance_management=resistance_management,
                recommendations=recommendations
            )

        except Exception as e:
            logger.error(f"Error in stakeholder alignment: {e}")
            raise

    async def _map_stakeholders(self, context: DecisionContext) -> dict[str, Any]:
        """Create comprehensive stakeholder mapping."""
        stakeholder_groups = {
            "champions": [],
            "supporters": [],
            "neutral": [],
            "skeptics": [],
            "blockers": []
        }

        # Analyze each stakeholder group
        for group_name, stakeholders in context.stakeholders.items():
            for stakeholder in stakeholders:
                # Determine stakeholder stance based on context
                if group_name == "primary":
                    # Primary stakeholders likely to be champions/supporters
                    if "executive" in stakeholder.lower() or "sponsor" in stakeholder.lower():
                        stakeholder_groups["champions"].append({
                            "name": stakeholder,
                            "influence": "high",
                            "interest": "high",
                            "group": group_name
                        })
                    else:
                        stakeholder_groups["supporters"].append({
                            "name": stakeholder,
                            "influence": "medium",
                            "interest": "high",
                            "group": group_name
                        })
                elif group_name == "secondary":
                    stakeholder_groups["neutral"].append({
                        "name": stakeholder,
                        "influence": "medium",
                        "interest": "medium",
                        "group": group_name
                    })
                else:
                    # Affected stakeholders might have concerns
                    stakeholder_groups["skeptics"].append({
                        "name": stakeholder,
                        "influence": "low",
                        "interest": "high",
                        "group": group_name
                    })

        # Create influence/interest matrix
        influence_interest_matrix = {
            "high_influence_high_interest": stakeholder_groups["champions"],
            "high_influence_low_interest": [],
            "low_influence_high_interest": stakeholder_groups["skeptics"],
            "low_influence_low_interest": []
        }

        total_stakeholders = sum(len(group) for group in stakeholder_groups.values())

        return {
            "stakeholder_groups": stakeholder_groups,
            "influence_interest_matrix": influence_interest_matrix,
            "total_stakeholders": total_stakeholders,
            "stakeholder_diversity": len([g for g in stakeholder_groups.values() if g]),
            "power_concentration": "balanced" if len(stakeholder_groups["champions"]) < total_stakeholders * 0.3 else "concentrated"
        }

    async def _analyze_alignment(self, context: DecisionContext,
                               stakeholder_mapping: dict[str, Any]) -> dict[str, Any]:
        """Analyze current stakeholder alignment levels."""
        stakeholder_groups = stakeholder_mapping["stakeholder_groups"]

        # Calculate alignment scores
        champion_count = len(stakeholder_groups["champions"])
        supporter_count = len(stakeholder_groups["supporters"])
        neutral_count = len(stakeholder_groups["neutral"])
        skeptic_count = len(stakeholder_groups["skeptics"])
        blocker_count = len(stakeholder_groups["blockers"])

        total = stakeholder_mapping["total_stakeholders"]

        if total == 0:
            alignment_score = 0.5
        else:
            # Weighted alignment calculation
            positive_weight = (champion_count * 1.0 + supporter_count * 0.7) / total
            negative_weight = (skeptic_count * 0.3 + blocker_count * 0.0) / total
            neutral_weight = (neutral_count * 0.5) / total

            alignment_score = positive_weight + neutral_weight - negative_weight
            alignment_score = max(0, min(1, alignment_score))  # Clamp to [0, 1]

        # Identify alignment gaps
        alignment_gaps = []
        if skeptic_count > supporter_count:
            alignment_gaps.append({
                "gap": "skeptic_majority",
                "impact": "high",
                "description": "More skeptics than supporters"
            })

        if blocker_count > 0:
            alignment_gaps.append({
                "gap": "active_blockers",
                "impact": "critical",
                "description": "Active blockers present"
            })

        if neutral_count > total * 0.4:
            alignment_gaps.append({
                "gap": "high_neutrality",
                "impact": "medium",
                "description": "Large neutral population"
            })

        # Determine consensus potential
        if alignment_score > 0.7:
            consensus_potential = "high"
        elif alignment_score > 0.5:
            consensus_potential = "moderate"
        else:
            consensus_potential = "low"

        return {
            "overall_alignment": alignment_score,
            "alignment_distribution": {
                "champions": champion_count / total if total > 0 else 0,
                "supporters": supporter_count / total if total > 0 else 0,
                "neutral": neutral_count / total if total > 0 else 0,
                "skeptics": skeptic_count / total if total > 0 else 0,
                "blockers": blocker_count / total if total > 0 else 0
            },
            "alignment_gaps": alignment_gaps,
            "consensus_potential": consensus_potential,
            "critical_mass_achieved": (champion_count + supporter_count) > total * 0.6
        }

    async def _analyze_influence_dynamics(self, stakeholder_mapping: dict[str, Any]) -> dict[str, Any]:
        """Analyze influence networks and dynamics."""
        stakeholder_groups = stakeholder_mapping["stakeholder_groups"]

        # Build influence network
        influence_network = []
        key_influencers = []

        # Identify key influencers (champions with high influence)
        for champion in stakeholder_groups["champions"]:
            if champion["influence"] == "high":
                key_influencers.append(champion["name"])
                # Create influence connections
                for group_name, group in stakeholder_groups.items():
                    if group_name != "champions":
                        for stakeholder in group:
                            influence_network.append({
                                "from": champion["name"],
                                "to": stakeholder["name"],
                                "strength": 0.7 if group_name == "supporters" else 0.4
                            })

        # Analyze coalition potential
        coalition_opportunities = []
        if len(stakeholder_groups["supporters"]) > 2:
            coalition_opportunities.append({
                "coalition": "supporter_alliance",
                "members": [s["name"] for s in stakeholder_groups["supporters"]],
                "potential_impact": "high"
            })

        # Identify influence gaps
        influence_gaps = []
        if not key_influencers:
            influence_gaps.append({
                "gap": "no_strong_champions",
                "recommendation": "identify_and_recruit_champions"
            })

        if len(stakeholder_groups["skeptics"]) > len(key_influencers) * 2:
            influence_gaps.append({
                "gap": "insufficient_influence_coverage",
                "recommendation": "expand_champion_network"
            })

        return {
            "network_analysis": {
                "nodes": stakeholder_mapping["total_stakeholders"],
                "edges": len(influence_network),
                "density": len(influence_network) / (stakeholder_mapping["total_stakeholders"] ** 2) if stakeholder_mapping["total_stakeholders"] > 0 else 0
            },
            "key_influencers": key_influencers,
            "influence_pathways": influence_network[:10],  # Top 10 connections
            "coalition_opportunities": coalition_opportunities,
            "influence_gaps": influence_gaps,
            "network_centralization": "high" if len(key_influencers) < 3 else "distributed"
        }

    async def _build_consensus_strategy(self, context: DecisionContext,
                                      alignment_analysis: dict[str, Any]) -> dict[str, Any]:
        """Build consensus building strategy."""
        consensus_approach = []

        # Based on alignment analysis, choose strategies
        if alignment_analysis["consensus_potential"] == "high":
            consensus_approach = [
                {
                    "technique": "structured_workshops",
                    "target": "all_stakeholders",
                    "timeline": "1-2 weeks",
                    "success_probability": 0.85
                },
                {
                    "technique": "quick_wins_showcase",
                    "target": "neutral_stakeholders",
                    "timeline": "2-3 weeks",
                    "success_probability": 0.75
                }
            ]
        elif alignment_analysis["consensus_potential"] == "moderate":
            consensus_approach = [
                {
                    "technique": "one_on_one_sessions",
                    "target": "skeptics_and_neutrals",
                    "timeline": "2-3 weeks",
                    "success_probability": 0.70
                },
                {
                    "technique": "pilot_demonstration",
                    "target": "all_stakeholders",
                    "timeline": "3-4 weeks",
                    "success_probability": 0.80
                }
            ]
        else:
            consensus_approach = [
                {
                    "technique": "coalition_building",
                    "target": "supporters_and_neutrals",
                    "timeline": "3-4 weeks",
                    "success_probability": 0.65
                },
                {
                    "technique": "iterative_negotiation",
                    "target": "skeptics_and_blockers",
                    "timeline": "4-6 weeks",
                    "success_probability": 0.60
                }
            ]

        # Define engagement sequence
        engagement_sequence = [
            {"phase": "champion_activation", "week": 1, "activities": ["align_champions", "prepare_messaging"]},
            {"phase": "supporter_mobilization", "week": 2, "activities": ["engage_supporters", "build_momentum"]},
            {"phase": "neutral_engagement", "week": 3, "activities": ["educate_neutrals", "address_concerns"]},
            {"phase": "skeptic_conversion", "week": 4, "activities": ["targeted_sessions", "evidence_sharing"]}
        ]

        return {
            "consensus_approach": consensus_approach,
            "engagement_sequence": engagement_sequence,
            "facilitation_methods": ["workshops", "surveys", "feedback_loops"],
            "decision_tools": ["weighted_voting", "consensus_mapping", "option_ranking"],
            "expected_timeline": "4-6 weeks",
            "success_metrics": ["alignment_score", "participation_rate", "decision_quality"]
        }

    async def _develop_communication_strategy(self, context: DecisionContext,
                                            stakeholder_mapping: dict[str, Any]) -> dict[str, Any]:
        """Develop comprehensive communication strategy."""
        # Define communication channels based on stakeholder groups
        channels = {
            "executive_briefings": {
                "audience": "champions",
                "frequency": "weekly",
                "format": "concise_updates",
                "key_messages": ["progress", "wins", "next_steps"]
            },
            "team_meetings": {
                "audience": "supporters",
                "frequency": "bi-weekly",
                "format": "interactive_sessions",
                "key_messages": ["involvement", "impact", "recognition"]
            },
            "email_updates": {
                "audience": "all_stakeholders",
                "frequency": "weekly",
                "format": "newsletter_style",
                "key_messages": ["transparency", "progress", "opportunities"]
            },
            "one_on_ones": {
                "audience": "skeptics",
                "frequency": "as_needed",
                "format": "personal_dialogue",
                "key_messages": ["concerns", "benefits", "compromise"]
            }
        }

        # Create messaging framework
        messaging_framework = {
            "core_narrative": "Accelerating strategic success through collaborative decision-making",
            "value_propositions": {
                "champions": "Lead transformational change",
                "supporters": "Shape the future direction",
                "neutral": "Contribute valuable perspectives",
                "skeptics": "Ensure balanced decisions"
            },
            "proof_points": ["data_driven_approach", "stakeholder_inclusion", "risk_mitigation"]
        }

        # Define feedback mechanisms
        feedback_loops = [
            {"mechanism": "pulse_surveys", "frequency": "weekly", "scope": "sentiment_tracking"},
            {"mechanism": "feedback_sessions", "frequency": "bi-weekly", "scope": "deep_insights"},
            {"mechanism": "suggestion_box", "frequency": "ongoing", "scope": "continuous_input"}
        ]

        return {
            "channels": channels,
            "messaging_framework": messaging_framework,
            "content_calendar": {
                "week_1": ["launch_announcement", "champion_toolkit"],
                "week_2": ["progress_update", "success_stories"],
                "week_3": ["feedback_summary", "next_phase"],
                "week_4": ["decision_preview", "final_input"]
            },
            "feedback_loops": feedback_loops,
            "communication_principles": ["transparency", "consistency", "two-way", "action-oriented"]
        }

    async def _plan_resistance_management(self, alignment_analysis: dict[str, Any]) -> dict[str, Any]:
        """Plan for resistance management."""
        resistance_sources = []

        # Identify resistance based on alignment gaps
        for gap in alignment_analysis["alignment_gaps"]:
            if gap["gap"] == "skeptic_majority":
                resistance_sources.append({
                    "source": "widespread_skepticism",
                    "root_cause": "change_fatigue_or_past_failures",
                    "intensity": "medium"
                })
            elif gap["gap"] == "active_blockers":
                resistance_sources.append({
                    "source": "active_opposition",
                    "root_cause": "conflicting_interests_or_loss_aversion",
                    "intensity": "high"
                })
            elif gap["gap"] == "high_neutrality":
                resistance_sources.append({
                    "source": "passive_resistance",
                    "root_cause": "lack_of_engagement_or_understanding",
                    "intensity": "low"
                })

        # Develop mitigation strategies
        mitigation_strategies = []
        for source in resistance_sources:
            if source["intensity"] == "high":
                mitigation_strategies.append({
                    "resistance_type": source["source"],
                    "strategy": "direct_negotiation_and_compromise",
                    "tactics": ["identify_win_wins", "address_losses", "find_alternatives"],
                    "timeline": "immediate"
                })
            elif source["intensity"] == "medium":
                mitigation_strategies.append({
                    "resistance_type": source["source"],
                    "strategy": "evidence_based_persuasion",
                    "tactics": ["share_success_stories", "pilot_results", "peer_testimonials"],
                    "timeline": "2-3_weeks"
                })
            else:
                mitigation_strategies.append({
                    "resistance_type": source["source"],
                    "strategy": "engagement_and_education",
                    "tactics": ["interactive_workshops", "q&a_sessions", "involvement_opportunities"],
                    "timeline": "ongoing"
                })

        # Early warning indicators
        early_warnings = [
            {"indicator": "declining_participation", "threshold": "below_60_percent", "action": "immediate_outreach"},
            {"indicator": "negative_feedback_spike", "threshold": "above_30_percent", "action": "root_cause_analysis"},
            {"indicator": "champion_withdrawal", "threshold": "any_champion", "action": "executive_intervention"}
        ]

        return {
            "resistance_sources": resistance_sources,
            "mitigation_strategies": mitigation_strategies,
            "proactive_measures": ["early_involvement", "transparent_process", "quick_wins"],
            "escalation_path": ["team_lead", "project_sponsor", "executive_committee"],
            "early_warning_indicators": early_warnings
        }

    def _calculate_alignment_readiness(self, alignment_analysis: dict[str, Any],
                                     influence_dynamics: dict[str, Any],
                                     consensus_building: dict[str, Any]) -> float:
        """Calculate overall stakeholder alignment readiness."""
        # Weighted factors
        alignment_factor = alignment_analysis["overall_alignment"] * 35
        influence_factor = (len(influence_dynamics["key_influencers"]) / 5) * 20  # Normalize to 5 influencers
        consensus_factor = 0.7 * 25  # Based on consensus potential
        network_factor = (1 - len(influence_dynamics["influence_gaps"]) / 3) * 20  # Penalty for gaps

        return min(100.0, alignment_factor + influence_factor + consensus_factor + network_factor)

    def _generate_alignment_recommendations(self, alignment_analysis: dict[str, Any],
                                          influence_dynamics: dict[str, Any],
                                          resistance_management: dict[str, Any]) -> list[dict[str, Any]]:
        """Generate stakeholder alignment recommendations."""
        recommendations = []

        # Check for critical alignment issues
        if alignment_analysis["overall_alignment"] < 0.5:
            recommendations.append({
                "action": "Launch intensive stakeholder engagement campaign",
                "strategic_impact": 9.2,
                "urgency": "high",
                "category": "alignment_improvement"
            })

        # Check for influence gaps
        if len(influence_dynamics["influence_gaps"]) > 0:
            recommendations.append({
                "action": "Recruit additional champions and expand influence network",
                "strategic_impact": 8.7,
                "urgency": "high",
                "category": "influence_building"
            })

        # Check for resistance
        if len(resistance_management["resistance_sources"]) > 0:
            recommendations.append({
                "action": "Implement targeted resistance mitigation strategies",
                "strategic_impact": 8.5,
                "urgency": "medium",
                "category": "resistance_management"
            })

        # Always recommend continuous engagement
        recommendations.append({
            "action": "Establish ongoing stakeholder feedback mechanisms",
            "strategic_impact": 7.8,
            "urgency": "medium",
            "category": "continuous_improvement"
        })

        return sorted(recommendations, key=lambda x: x["strategic_impact"], reverse=True)
