"""
Test suite for Market Analysis Workflows
"""

from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest

from pyclarity.workflows.market_analysis import (
    CompetitorAnalysis,
    MarketAnalysisResult,
    MarketAnalysisWorkflow,
    MarketSegment,
    QuickMarketAssessment,
)
from pyclarity.workflows.models import WorkflowResult, WorkflowStatus


@pytest.fixture
def mock_workflow_engine():
    """Mock WorkflowEngine for testing"""
    engine = AsyncMock()

    # Default successful result
    engine.execute_workflow.return_value = WorkflowResult(
        workflow_id="test_workflow",
        status=WorkflowStatus.COMPLETED,
        started_at=datetime.now(UTC),
        completed_at=datetime.now(UTC),
        execution_time_ms=100.0,
        tool_results={
            "mental_models": {
                "market_size": "Large",
                "growth_potential": "High",
                "key_segments": ["Enterprise", "SMB"],
            },
            "decision_framework": {
                "recommendation": "Enter market",
                "confidence": 0.8,
                "key_factors": ["Growing demand", "Limited competition"],
            },
        },
        errors=[],
    )

    return engine


@pytest.fixture
def market_analysis_workflow(mock_workflow_engine):
    """Create MarketAnalysisWorkflow with mocked engine"""
    workflow = MarketAnalysisWorkflow()
    workflow.workflow_engine = mock_workflow_engine
    return workflow


class TestMarketAnalysisWorkflow:
    """Test suite for MarketAnalysisWorkflow"""

    async def test_analyze_market_basic(self, market_analysis_workflow):
        """Test basic market analysis"""
        result = await market_analysis_workflow.analyze_market(
            product_description="AI-powered analytics platform", target_market="B2B SaaS"
        )

        assert isinstance(result, MarketAnalysisResult)
        assert result.market_overview
        assert result.total_addressable_market
        assert len(result.segments) > 0
        assert result.confidence_score > 0

    async def test_analyze_market_with_competitors(self, market_analysis_workflow):
        """Test market analysis with competitor data"""
        competitors = ["CompetitorA", "CompetitorB", "CompetitorC"]

        result = await market_analysis_workflow.analyze_market(
            product_description="Project management tool",
            target_market="Software teams",
            competitors=competitors,
        )

        assert len(result.competitors) == len(competitors)
        for comp_analysis in result.competitors:
            assert isinstance(comp_analysis, CompetitorAnalysis)
            assert comp_analysis.competitor_name in competitors

    async def test_market_framework_analysis(self, market_analysis_workflow):
        """Test market framework analysis stage"""
        framework = await market_analysis_workflow._analyze_market_framework(
            product_description="Test product",
            target_market="Test market",
            industry_data={"size": "10B"},
        )

        assert isinstance(framework, dict)
        assert "mental_models" in framework
        assert "decision_framework" in framework

    async def test_competitive_landscape_empty(self, market_analysis_workflow):
        """Test competitive analysis with no competitors"""
        result = await market_analysis_workflow._analyze_competitive_landscape(
            product_description="New product", competitors=[], market_framework={}
        )

        assert result == []

    async def test_market_segmentation(self, market_analysis_workflow):
        """Test market segmentation identification"""
        segments = await market_analysis_workflow._identify_market_segments(
            target_market="B2B software", market_framework={"segments": ["Enterprise", "SMB"]}
        )

        assert len(segments) >= 2
        for segment in segments:
            assert isinstance(segment, MarketSegment)
            assert segment.segment_id
            assert segment.name
            assert segment.size_estimate

    async def test_error_handling(self, market_analysis_workflow, mock_workflow_engine):
        """Test error handling in market analysis"""
        # Configure mock to return error
        mock_workflow_engine.execute_workflow.return_value = WorkflowResult(
            workflow_id="test",
            status=WorkflowStatus.FAILED,
            started_at=datetime.now(),
            completed_at=datetime.now(),
            execution_time_ms=100.0,
            tool_results={},
            errors=["Analysis failed"],
        )

        with pytest.raises(Exception, match="Market framework analysis failed"):
            await market_analysis_workflow.analyze_market(
                product_description="Test", target_market="Test"
            )


class TestQuickMarketAssessment:
    """Test suite for QuickMarketAssessment"""

    @pytest.fixture
    def quick_assessment(self, mock_workflow_engine):
        """Create QuickMarketAssessment with mocked engine"""
        assessment = QuickMarketAssessment()
        assessment.workflow_engine = mock_workflow_engine
        return assessment

    async def test_quick_assessment_viable(self, quick_assessment):
        """Test quick assessment for viable market"""
        result = await quick_assessment.assess(
            product_idea="AI chatbot", target_market="Customer service"
        )

        assert result["viable"] is True
        assert "assessment" in result

    async def test_quick_assessment_not_viable(self, quick_assessment, mock_workflow_engine):
        """Test quick assessment for non-viable market"""
        # Configure mock for failed assessment
        mock_workflow_engine.execute_workflow.return_value = WorkflowResult(
            workflow_id="test",
            status=WorkflowStatus.FAILED,
            started_at=datetime.now(),
            completed_at=datetime.now(),
            execution_time_ms=100.0,
            tool_results={},
            errors=["Low market potential"],
        )

        result = await quick_assessment.assess(
            product_idea="Obsolete tech", target_market="Shrinking market"
        )

        assert result["viable"] is False


class TestMarketAnalysisModels:
    """Test Pydantic models for market analysis"""

    def test_market_segment_validation(self):
        """Test MarketSegment model validation"""
        segment = MarketSegment(
            segment_id="test_seg",
            name="Test Segment",
            description="A test market segment",
            size_estimate="$1B",
            growth_rate="10% YoY",
        )

        assert segment.segment_id == "test_seg"
        assert len(segment.opportunities) == 0  # Default empty list

    def test_competitor_analysis_validation(self):
        """Test CompetitorAnalysis model validation"""
        competitor = CompetitorAnalysis(
            competitor_name="Acme Corp", strategy="Low-cost provider", market_share="25%"
        )

        assert competitor.competitor_name == "Acme Corp"
        assert competitor.market_share == "25%"

    def test_market_analysis_result_validation(self):
        """Test MarketAnalysisResult model validation"""
        result = MarketAnalysisResult(
            market_overview="Test overview",
            total_addressable_market="$10B",
            serviceable_available_market="$5B",
            serviceable_obtainable_market="$500M",
        )

        assert result.confidence_score == 0.5  # Default value
        assert len(result.segments) == 0
        assert len(result.competitors) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
