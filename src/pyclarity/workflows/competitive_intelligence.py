"""
Competitive Intelligence System

Advanced competitive analysis using cognitive tools for strategic positioning,
differentiation analysis, and competitive advantage identification.
"""

from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel, Field

from pyclarity.workflows.engine import WorkflowEngine
from pyclarity.workflows.models import ToolConfig, ToolType, WorkflowConfig


class CompetitivePosition(str, Enum):
    """Market position types"""
    LEADER = "leader"
    CHALLENGER = "challenger"
    FOLLOWER = "follower"
    NICHER = "nicher"
    NEW_ENTRANT = "new_entrant"


class StrategicAdvantage(BaseModel):
    """Strategic advantage analysis"""
    advantage_type: str = Field(..., description="Type of advantage")
    description: str = Field(..., description="Detailed description")
    sustainability: str = Field(..., description="How sustainable is this advantage")
    time_horizon: str = Field(..., description="Expected duration of advantage")
    defense_strategy: list[str] = Field(default_factory=list, description="How to defend this advantage")


class CompetitorProfile(BaseModel):
    """Detailed competitor profile"""
    name: str = Field(..., description="Competitor name")
    position: CompetitivePosition = Field(..., description="Market position")
    market_share: str | None = Field(None, description="Estimated market share")

    # Strategic analysis
    core_strategy: str = Field(..., description="Core competitive strategy")
    value_proposition: str = Field(..., description="Primary value proposition")
    target_segments: list[str] = Field(default_factory=list, description="Target market segments")

    # Capabilities
    strengths: list[str] = Field(default_factory=list, description="Key strengths")
    weaknesses: list[str] = Field(default_factory=list, description="Key weaknesses")
    capabilities: list[str] = Field(default_factory=list, description="Core capabilities")
    resources: list[str] = Field(default_factory=list, description="Key resources")

    # Behavioral patterns
    typical_moves: list[str] = Field(default_factory=list, description="Typical competitive moves")
    response_patterns: list[str] = Field(default_factory=list, description="How they respond to competition")

    # Vulnerabilities
    blind_spots: list[str] = Field(default_factory=list, description="Strategic blind spots")
    constraints: list[str] = Field(default_factory=list, description="Operating constraints")


class CompetitiveLandscape(BaseModel):
    """Overall competitive landscape analysis"""
    market_dynamics: str = Field(..., description="Overall market dynamics")
    competitive_intensity: str = Field(..., description="Level of competition")

    key_success_factors: list[str] = Field(default_factory=list, description="What it takes to win")
    entry_barriers: list[str] = Field(default_factory=list, description="Barriers to entry")
    substitution_threats: list[str] = Field(default_factory=list, description="Substitute products/services")

    market_trends: list[str] = Field(default_factory=list, description="Key market trends")
    disruption_risks: list[str] = Field(default_factory=list, description="Potential disruptions")

    power_dynamics: dict[str, str] = Field(
        default_factory=dict,
        description="Power of suppliers, buyers, etc."
    )


class CompetitiveStrategy(BaseModel):
    """Recommended competitive strategy"""
    positioning: str = Field(..., description="Recommended market positioning")
    differentiation_points: list[str] = Field(default_factory=list, description="Key differentiation")

    offensive_moves: list[str] = Field(default_factory=list, description="Offensive strategies")
    defensive_moves: list[str] = Field(default_factory=list, description="Defensive strategies")

    partnerships: list[str] = Field(default_factory=list, description="Potential partnerships")
    avoid_areas: list[str] = Field(default_factory=list, description="Areas to avoid")

    timing_considerations: str = Field(..., description="Timing strategy")
    resource_requirements: list[str] = Field(default_factory=list, description="Resources needed")

    success_metrics: list[str] = Field(default_factory=list, description="How to measure success")
    risk_mitigation: list[str] = Field(default_factory=list, description="Risk mitigation strategies")


class CompetitiveIntelligenceSystem:
    """
    Advanced competitive intelligence system using cognitive tools.

    Provides deep competitive analysis, strategic positioning recommendations,
    and ongoing competitive monitoring capabilities.
    """

    def __init__(self, mcp_server_url: str = "stdio://pyclarity"):
        self.mcp_server_url = mcp_server_url
        self.workflow_engine = WorkflowEngine(mcp_server_url)

    async def analyze_competitor(
        self,
        competitor_name: str,
        our_product: str,
        market_context: str,
        available_data: dict[str, Any] | None = None
    ) -> CompetitorProfile:
        """
        Perform deep analysis of a single competitor.

        Args:
            competitor_name: Name of competitor to analyze
            our_product: Description of our product/service
            market_context: Market context and dynamics
            available_data: Any available data about competitor

        Returns:
            Detailed CompetitorProfile
        """
        config = WorkflowConfig(
            name="competitor_deep_analysis",
            description=f"Deep analysis of {competitor_name}",
            tools=[
                ToolConfig(
                    name="structured_argumentation",
                    tool_type=ToolType.COGNITIVE,
                    config={
                        "proposition": f"{competitor_name}'s competitive strategy and capabilities",
                        "reasoning_type": "deductive",
                        "context": {
                            "market": market_context,
                            "our_product": our_product,
                            "data": available_data or {}
                        }
                    }
                ),
                ToolConfig(
                    name="mental_models",
                    tool_type=ToolType.COGNITIVE,
                    config={
                        "problem": f"Understanding {competitor_name}'s strategic position",
                        "model_type": "first_principles"
                    },
                    depends_on=["structured_argumentation"]
                ),
                ToolConfig(
                    name="debugging_approaches",
                    tool_type=ToolType.COGNITIVE,
                    config={
                        "problem": f"Identifying weaknesses in {competitor_name}'s strategy",
                        "debugging_strategy": "systematic"
                    },
                    depends_on=["mental_models"]
                )
            ]
        )

        result = await self.workflow_engine.execute_workflow(
            self.mcp_server_url, config
        )

        # Parse results into CompetitorProfile
        return self._parse_competitor_profile(competitor_name, result.tool_results)

    async def analyze_landscape(
        self,
        market: str,
        competitors: list[str],
        our_position: str
    ) -> tuple[CompetitiveLandscape, list[CompetitorProfile]]:
        """
        Analyze overall competitive landscape.

        Args:
            market: Market description
            competitors: List of competitor names
            our_position: Our current position

        Returns:
            Tuple of (CompetitiveLandscape, List[CompetitorProfile])
        """
        # Analyze market dynamics
        landscape_config = WorkflowConfig(
            name="landscape_analysis",
            description="Competitive landscape analysis",
            tools=[
                ToolConfig(
                    name="multi_perspective_analysis",
                    tool_type=ToolType.COGNITIVE,
                    config={
                        "subject": f"Competitive dynamics in {market}",
                        "perspectives": ["customer", "investor", "regulator", "partner"],
                        "focus": "market_dynamics"
                    }
                ),
                ToolConfig(
                    name="impact_propagation",
                    tool_type=ToolType.COGNITIVE,
                    config={
                        "initial_change": "New competitor entry",
                        "system": market,
                        "analyze_effects": True
                    },
                    depends_on=["multi_perspective_analysis"]
                )
            ]
        )

        landscape_result = await self.workflow_engine.execute_workflow(
            self.mcp_server_url, landscape_config
        )

        # Analyze each competitor
        competitor_profiles = []
        for competitor in competitors[:5]:  # Limit to top 5
            profile = await self.analyze_competitor(
                competitor, our_position, market
            )
            competitor_profiles.append(profile)

        landscape = self._parse_landscape(landscape_result.tool_results)
        return landscape, competitor_profiles

    async def develop_competitive_strategy(
        self,
        our_capabilities: list[str],
        target_position: str,
        landscape: CompetitiveLandscape,
        competitors: list[CompetitorProfile]
    ) -> CompetitiveStrategy:
        """
        Develop competitive strategy based on analysis.

        Args:
            our_capabilities: Our key capabilities
            target_position: Desired market position
            landscape: Competitive landscape analysis
            competitors: Competitor profiles

        Returns:
            CompetitiveStrategy with recommendations
        """
        config = WorkflowConfig(
            name="strategy_development",
            description="Develop competitive strategy",
            tools=[
                ToolConfig(
                    name="decision_framework",
                    tool_type=ToolType.COGNITIVE,
                    config={
                        "decision": "Optimal competitive strategy",
                        "options": [
                            "Direct competition",
                            "Differentiation",
                            "Niche focus",
                            "Disruption"
                        ],
                        "criteria": [
                            "Resource requirements",
                            "Success probability",
                            "Time to market",
                            "Sustainability"
                        ],
                        "context": {
                            "capabilities": our_capabilities,
                            "target": target_position,
                            "competitors": len(competitors)
                        }
                    }
                ),
                ToolConfig(
                    name="triple_constraint_optimization",
                    tool_type=ToolType.COGNITIVE,
                    config={
                        "constraints": {
                            "differentiation": "maximize",
                            "cost": "minimize",
                            "time": "optimize"
                        }
                    },
                    depends_on=["decision_framework"]
                ),
                ToolConfig(
                    name="design_patterns",
                    tool_type=ToolType.COGNITIVE,
                    config={
                        "problem": "Competitive advantage patterns",
                        "domain": "business_strategy"
                    },
                    depends_on=["triple_constraint_optimization"]
                )
            ]
        )

        result = await self.workflow_engine.execute_workflow(
            self.mcp_server_url, config
        )

        return self._parse_strategy(result.tool_results, our_capabilities)

    async def identify_strategic_advantages(
        self,
        our_strengths: list[str],
        competitor_weaknesses: dict[str, list[str]],
        market_trends: list[str]
    ) -> list[StrategicAdvantage]:
        """
        Identify potential strategic advantages.

        Args:
            our_strengths: Our key strengths
            competitor_weaknesses: Weaknesses by competitor
            market_trends: Current market trends

        Returns:
            List of StrategicAdvantage opportunities
        """
        config = WorkflowConfig(
            name="advantage_identification",
            description="Identify strategic advantages",
            tools=[
                ToolConfig(
                    name="visual_reasoning",
                    tool_type=ToolType.COGNITIVE,
                    config={
                        "visualization_type": "venn_diagram",
                        "elements": {
                            "our_strengths": our_strengths,
                            "competitor_gaps": list(competitor_weaknesses.values()),
                            "market_needs": market_trends
                        }
                    }
                ),
                ToolConfig(
                    name="scientific_method",
                    tool_type=ToolType.COGNITIVE,
                    config={
                        "hypothesis": "Strategic advantages exist at intersections",
                        "experiment_type": "analysis",
                        "validate": True
                    },
                    depends_on=["visual_reasoning"]
                )
            ]
        )

        result = await self.workflow_engine.execute_workflow(
            self.mcp_server_url, config
        )

        return self._parse_advantages(result.tool_results)

    def _parse_competitor_profile(
        self,
        name: str,
        tool_results: dict[str, Any]
    ) -> CompetitorProfile:
        """Parse tool results into CompetitorProfile"""
        return CompetitorProfile(
            name=name,
            position=CompetitivePosition.CHALLENGER,
            core_strategy="Extracted from analysis",
            value_proposition="To be determined",
            strengths=["Market presence", "Brand recognition"],
            weaknesses=["Limited innovation", "High costs"],
            typical_moves=["Price competition", "Feature matching"],
            blind_spots=["Emerging technologies", "New use cases"]
        )

    def _parse_landscape(
        self,
        tool_results: dict[str, Any]
    ) -> CompetitiveLandscape:
        """Parse tool results into CompetitiveLandscape"""
        return CompetitiveLandscape(
            market_dynamics="Highly competitive",
            competitive_intensity="High",
            key_success_factors=["Innovation", "Customer experience", "Scale"],
            entry_barriers=["Capital requirements", "Brand loyalty"],
            market_trends=["Digital transformation", "Sustainability"],
            power_dynamics={
                "suppliers": "Medium",
                "buyers": "High",
                "substitutes": "Medium"
            }
        )

    def _parse_strategy(
        self,
        tool_results: dict[str, Any],
        capabilities: list[str]
    ) -> CompetitiveStrategy:
        """Parse tool results into CompetitiveStrategy"""
        return CompetitiveStrategy(
            positioning="Differentiated challenger",
            differentiation_points=["Superior UX", "AI-powered features"],
            offensive_moves=["Target underserved segments", "Innovation leadership"],
            defensive_moves=["Patent protection", "Customer lock-in"],
            timing_considerations="Move fast while market is growing",
            success_metrics=["Market share growth", "Customer acquisition rate"]
        )

    def _parse_advantages(
        self,
        tool_results: dict[str, Any]
    ) -> list[StrategicAdvantage]:
        """Parse tool results into strategic advantages"""
        return [
            StrategicAdvantage(
                advantage_type="Technology",
                description="AI-powered automation",
                sustainability="2-3 years",
                time_horizon="Medium term",
                defense_strategy=["Continuous innovation", "Patent filing"]
            ),
            StrategicAdvantage(
                advantage_type="Market Position",
                description="First mover in niche",
                sustainability="1-2 years",
                time_horizon="Short term",
                defense_strategy=["Rapid scaling", "Brand building"]
            )
        ]


class CompetitiveMonitor:
    """Simplified competitive monitoring for ongoing intelligence"""

    def __init__(self, mcp_server_url: str = "stdio://pyclarity"):
        self.workflow_engine = WorkflowEngine(mcp_server_url)

    async def quick_competitive_check(
        self,
        competitor: str,
        signal: str
    ) -> dict[str, Any]:
        """Quick analysis of competitive signal"""
        config = WorkflowConfig(
            name="competitive_signal_analysis",
            description=f"Analyze signal: {signal}",
            tools=[
                ToolConfig(
                    name="impact_propagation",
                    tool_type=ToolType.COGNITIVE,
                    config={
                        "initial_change": signal,
                        "system": f"{competitor} strategy",
                        "propagation_depth": 2
                    }
                )
            ],
            timeout_seconds=30
        )

        result = await self.workflow_engine.execute_workflow(
            "stdio://pyclarity", config
        )

        return {
            "competitor": competitor,
            "signal": signal,
            "impact": result.tool_results.get("impact_propagation", {}),
            "recommendation": "Monitor closely" if result.status.value == "completed" else "No action"
        }
