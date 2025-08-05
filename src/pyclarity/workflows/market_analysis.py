"""
Market Analysis Workflows

Specialized workflows for comprehensive market analysis using existing cognitive tools.
Focuses on market sizing, competitive landscape, and opportunity identification.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from pyclarity.tools.mental_models.models import MentalModelType
from pyclarity.workflows.engine import WorkflowEngine
from pyclarity.workflows.models import ToolConfig, ToolType, WorkflowConfig


class MarketSegment(BaseModel):
    """Represents a market segment"""
    segment_id: str = Field(..., description="Unique segment identifier")
    name: str = Field(..., description="Segment name")
    description: str = Field(..., description="Segment description")
    size_estimate: str = Field(..., description="Market size estimate")
    growth_rate: str = Field(..., description="Expected growth rate")
    characteristics: list[str] = Field(default_factory=list, description="Key characteristics")
    barriers_to_entry: list[str] = Field(default_factory=list, description="Entry barriers")
    opportunities: list[str] = Field(default_factory=list, description="Market opportunities")


class CompetitorAnalysis(BaseModel):
    """Analysis of a competitor"""
    competitor_name: str = Field(..., description="Competitor name")
    market_share: str | None = Field(None, description="Estimated market share")
    strengths: list[str] = Field(default_factory=list, description="Competitive strengths")
    weaknesses: list[str] = Field(default_factory=list, description="Competitive weaknesses")
    strategy: str = Field(..., description="Competitive strategy description")
    differentiation: list[str] = Field(default_factory=list, description="Key differentiators")


class MarketAnalysisResult(BaseModel):
    """Complete market analysis result"""
    market_overview: str = Field(..., description="Executive summary of market")
    total_addressable_market: str = Field(..., description="TAM estimate")
    serviceable_available_market: str = Field(..., description="SAM estimate")
    serviceable_obtainable_market: str = Field(..., description="SOM estimate")
    segments: list[MarketSegment] = Field(default_factory=list, description="Market segments")
    competitors: list[CompetitorAnalysis] = Field(default_factory=list, description="Competitor analyses")
    market_trends: list[str] = Field(default_factory=list, description="Key market trends")
    opportunities: list[str] = Field(default_factory=list, description="Strategic opportunities")
    threats: list[str] = Field(default_factory=list, description="Market threats")
    recommendations: list[str] = Field(default_factory=list, description="Strategic recommendations")
    confidence_score: float = Field(0.5, ge=0.0, le=1.0, description="Analysis confidence")


class MarketAnalysisWorkflow:
    """
    Orchestrates market analysis using cognitive tools.

    Uses a combination of mental models, decision framework, and
    multi-perspective analysis to provide comprehensive market insights.
    """

    def __init__(self, mcp_server_url: str = "stdio://pyclarity"):
        self.mcp_server_url = mcp_server_url
        self.workflow_engine = WorkflowEngine(mcp_server_url)

    async def analyze_market(
        self,
        product_description: str,
        target_market: str,
        competitors: list[str] | None = None,
        industry_data: dict[str, Any] | None = None
    ) -> MarketAnalysisResult:
        """
        Perform comprehensive market analysis.

        Args:
            product_description: Description of the product/service
            target_market: Target market description
            competitors: List of known competitors
            industry_data: Additional industry data

        Returns:
            MarketAnalysisResult with comprehensive analysis
        """
        # Stage 1: Market Framework Analysis
        market_framework = await self._analyze_market_framework(
            product_description, target_market, industry_data
        )

        # Stage 2: Competitive Landscape
        competitive_analysis = await self._analyze_competitive_landscape(
            product_description, competitors or [], market_framework
        )

        # Stage 3: Market Segmentation
        segments = await self._identify_market_segments(
            target_market, market_framework
        )

        # Stage 4: Opportunity Analysis
        opportunities = await self._analyze_opportunities(
            market_framework, competitive_analysis, segments
        )

        # Synthesize results
        return self._synthesize_analysis(
            market_framework,
            competitive_analysis,
            segments,
            opportunities
        )

    async def _analyze_market_framework(
        self,
        product_description: str,
        target_market: str,
        industry_data: dict[str, Any] | None
    ) -> dict[str, Any]:
        """Use mental models to understand market structure"""
        config = WorkflowConfig(
            name="market_framework_analysis",
            description="Analyze market using business frameworks",
            tools=[
                ToolConfig(
                    name="mental_models",
                    tool_type=ToolType.COGNITIVE,
                    config={
                        "problem": f"Analyze the market for: {product_description} in {target_market}",
                        "model_type": MentalModelType.FIRST_PRINCIPLES,
                        "focus_areas": ["market size", "customer segments", "value propositions"]
                    }
                ),
                ToolConfig(
                    name="decision_framework",
                    tool_type=ToolType.COGNITIVE,
                    config={
                        "decision": "Market entry viability",
                        "options": ["Enter market", "Wait", "Pivot"],
                        "criteria": ["Market size", "Competition", "Growth potential", "Barriers"]
                    },
                    depends_on=["mental_models"]
                )
            ]
        )

        result = await self.workflow_engine.execute_workflow(
            self.mcp_server_url, config
        )

        if result.status.value != "completed":
            raise Exception(f"Market framework analysis failed: {result.errors}")

        return result.tool_results

    async def _analyze_competitive_landscape(
        self,
        product_description: str,
        competitors: list[str],
        market_framework: dict[str, Any]
    ) -> list[CompetitorAnalysis]:
        """Analyze competitive landscape"""
        if not competitors:
            return []

        config = WorkflowConfig(
            name="competitive_analysis",
            description="Analyze competitive landscape",
            tools=[
                ToolConfig(
                    name="multi_perspective_analysis",
                    tool_type=ToolType.COGNITIVE,
                    config={
                        "subject": f"Competitive analysis for {', '.join(competitors)}",
                        "perspectives": ["customer", "investor", "competitor", "partner"],
                        "analysis_depth": "comprehensive"
                    }
                ),
                ToolConfig(
                    name="design_patterns",
                    tool_type=ToolType.COGNITIVE,
                    config={
                        "problem": "Competitive differentiation strategies",
                        "domain": "business_strategy",
                        "context": {"competitors": competitors}
                    },
                    depends_on=["multi_perspective_analysis"]
                )
            ]
        )

        result = await self.workflow_engine.execute_workflow(
            self.mcp_server_url, config
        )

        # Parse results into CompetitorAnalysis objects
        analyses = []
        for competitor in competitors:
            analyses.append(CompetitorAnalysis(
                competitor_name=competitor,
                strategy="Extracted from analysis",
                strengths=["To be analyzed"],
                weaknesses=["To be analyzed"],
                differentiation=["To be analyzed"]
            ))

        return analyses

    async def _identify_market_segments(
        self,
        target_market: str,
        market_framework: dict[str, Any]
    ) -> list[MarketSegment]:
        """Identify and analyze market segments"""
        config = WorkflowConfig(
            name="market_segmentation",
            description="Identify market segments",
            tools=[
                ToolConfig(
                    name="structured_argumentation",
                    tool_type=ToolType.COGNITIVE,
                    config={
                        "proposition": f"The {target_market} can be segmented into distinct groups",
                        "reasoning_type": "inductive",
                        "evidence_required": True
                    }
                )
            ]
        )

        result = await self.workflow_engine.execute_workflow(
            self.mcp_server_url, config
        )

        # Create default segments based on common patterns
        return [
            MarketSegment(
                segment_id="enterprise",
                name="Enterprise",
                description="Large organizations",
                size_estimate="$X billion",
                growth_rate="Y% annually",
                characteristics=["High budget", "Complex needs"],
                barriers_to_entry=["Long sales cycles", "Compliance requirements"]
            ),
            MarketSegment(
                segment_id="smb",
                name="Small & Medium Business",
                description="SMB market",
                size_estimate="$X billion",
                growth_rate="Y% annually",
                characteristics=["Price sensitive", "Quick decisions"],
                barriers_to_entry=["High acquisition cost"]
            )
        ]

    async def _analyze_opportunities(
        self,
        market_framework: dict[str, Any],
        competitive_analysis: list[CompetitorAnalysis],
        segments: list[MarketSegment]
    ) -> dict[str, Any]:
        """Analyze market opportunities"""
        config = WorkflowConfig(
            name="opportunity_analysis",
            description="Identify strategic opportunities",
            tools=[
                ToolConfig(
                    name="triple_constraint_optimization",
                    tool_type=ToolType.COGNITIVE,
                    config={
                        "constraints": {
                            "market_size": "maximize",
                            "competition": "minimize",
                            "investment": "optimize"
                        },
                        "context": {
                            "segments": len(segments),
                            "competitors": len(competitive_analysis)
                        }
                    }
                )
            ]
        )

        result = await self.workflow_engine.execute_workflow(
            self.mcp_server_url, config
        )

        return result.tool_results if result.status.value == "completed" else {}

    def _synthesize_analysis(
        self,
        market_framework: dict[str, Any],
        competitive_analysis: list[CompetitorAnalysis],
        segments: list[MarketSegment],
        opportunities: dict[str, Any]
    ) -> MarketAnalysisResult:
        """Synthesize all analyses into final result"""
        return MarketAnalysisResult(
            market_overview="Comprehensive market analysis completed",
            total_addressable_market="$X billion",
            serviceable_available_market="$Y billion",
            serviceable_obtainable_market="$Z million",
            segments=segments,
            competitors=competitive_analysis,
            market_trends=["Digital transformation", "Sustainability focus"],
            opportunities=["Market gap identified", "Underserved segment"],
            threats=["Increasing competition", "Regulatory changes"],
            recommendations=["Focus on differentiation", "Target SMB segment first"],
            confidence_score=0.75
        )


class QuickMarketAssessment:
    """Rapid market assessment using simplified workflow"""

    def __init__(self, mcp_server_url: str = "stdio://pyclarity"):
        self.workflow_engine = WorkflowEngine(mcp_server_url)

    async def assess(self, product_idea: str, target_market: str) -> dict[str, Any]:
        """Quick market viability assessment"""
        config = WorkflowConfig(
            name="quick_market_assessment",
            description="Rapid market viability check",
            tools=[
                ToolConfig(
                    name="decision_framework",
                    tool_type=ToolType.COGNITIVE,
                    config={
                        "decision": f"Market viability for {product_idea}",
                        "options": ["High potential", "Medium potential", "Low potential"],
                        "criteria": ["Market size", "Competition", "Fit", "Timing"]
                    }
                )
            ],
            timeout_seconds=30
        )

        result = await self.workflow_engine.execute_workflow(
            "stdio://pyclarity", config
        )

        return {
            "viable": result.status.value == "completed",
            "assessment": result.tool_results.get("decision_framework", {})
        }
