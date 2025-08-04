"""
Test suite for Product Discovery Pipeline

Tests the complete product discovery workflow from persona analysis
to optimized product model generation.
"""

import pytest
from unittest.mock import AsyncMock

from pyclarity.workflows.product_discovery import (
    ProductDiscoveryPipeline,
    AnalysisStage,
    PersonaInsight,
    PainPointCluster,
    ProductIdea,
    ValidationResult,
    USPOption,
    OptimizedProductModel
)
from pyclarity.workflows.models import WorkflowStatus, WorkflowConfig, WorkflowResult
from datetime import datetime


@pytest.fixture
def sample_personas():
    """Sample persona data for testing"""
    return [
        """
        Name: Sarah Chen
        Age: 28
        Occupation: Marketing Manager at a tech startup
        
        Daily Activities:
        - Managing social media campaigns across multiple platforms
        - Analyzing campaign performance metrics
        - Coordinating with design team for content creation
        - Budget tracking and ROI reporting
        
        Pain Points:
        - Switching between multiple tools is time-consuming
        - Difficult to get real-time performance insights
        - Manual reporting takes hours each week
        - Hard to prove marketing ROI to executives
        
        Goals:
        - Streamline marketing workflow
        - Demonstrate clear value to leadership
        - Reduce time spent on manual tasks
        - Improve campaign performance
        """,
        """
        Name: Marcus Rodriguez
        Age: 35
        Occupation: Small Business Owner (E-commerce)
        
        Daily Activities:
        - Managing online store inventory
        - Processing customer orders
        - Responding to customer inquiries
        - Marketing on social media
        
        Pain Points:
        - Inventory management across multiple channels
        - Time-consuming order fulfillment process
        - Limited marketing expertise and resources
        - Difficulty competing with larger retailers
        
        Goals:
        - Grow revenue by 50% this year
        - Reduce operational overhead
        - Build customer loyalty
        - Expand to new markets
        """
    ]


@pytest.fixture
def mock_workflow_engine():
    """Mock WorkflowEngine for testing"""
    engine = AsyncMock()
    
    # Default successful workflow result
    default_result = WorkflowResult(
        workflow_id="test_workflow",
        status=WorkflowStatus.COMPLETED,
        started_at=datetime.now(),
        completed_at=datetime.now(),
        execution_time_ms=100.0,
        tool_results={},
        errors=[]
    )
    
    engine.execute_workflow.return_value = default_result
    return engine


@pytest.fixture
def product_discovery_pipeline(mock_workflow_engine):
    """Create ProductDiscoveryPipeline with mocked dependencies"""
    pipeline = ProductDiscoveryPipeline()
    pipeline.workflow_engine = mock_workflow_engine
    return pipeline


class TestProductDiscoveryPipeline:
    """Test suite for ProductDiscoveryPipeline"""
    
    async def test_pipeline_initialization(self):
        """Test pipeline initializes correctly"""
        pipeline = ProductDiscoveryPipeline()
        
        assert pipeline.mcp_server_url == "stdio://pyclarity"
        assert pipeline.workflow_engine is not None
        assert len(pipeline.persona_insights) == 0
        assert len(pipeline.pain_point_clusters) == 0
        assert len(pipeline.product_ideas) == 0
        assert pipeline.current_stage is None
        
    async def test_persona_analysis(self, product_discovery_pipeline, mock_workflow_engine, sample_personas):
        """Test persona analysis stage"""
        pipeline = product_discovery_pipeline
        
        # Configure mock responses
        mock_workflow_engine.execute_workflow.return_value = WorkflowResult(
            workflow_id="persona_analysis",
            status=WorkflowStatus.COMPLETED,
            started_at=datetime.now(),
            completed_at=datetime.now(),
            execution_time_ms=100.0,
            tool_results={
                "sequential_thinking": {
                    "demographics": {"age": 28, "occupation": "Marketing Manager"},
                    "activities": ["Managing campaigns", "Analyzing metrics"],
                    "pain_points": ["Multiple tools", "Manual reporting"],
                    "goals": ["Streamline workflow", "Demonstrate value"],
                    "tech_comfort": 0.8
                },
                "collaborative_reasoning": {
                    "perspectives": [
                        {
                            "role": "UX Researcher",
                            "activities": ["Campaign management"],
                            "pain_points": ["Tool fragmentation"]
                        }
                    ]
                }
            },
            errors=[]
        )
        
        # Execute persona analysis
        await pipeline._analyze_personas(sample_personas)
        
        # Verify results
        assert len(pipeline.persona_insights) == 2
        assert pipeline.current_stage == AnalysisStage.PERSONA_ANALYSIS
        
        # Check first persona
        persona = pipeline.persona_insights[0]
        assert persona.persona_id == "persona_0"
        assert persona.tech_comfort_level == 0.8
        assert "Managing campaigns" in persona.activities
        assert "Multiple tools" in persona.pain_points
        
    async def test_pain_point_clustering(self, product_discovery_pipeline, mock_workflow_engine):
        """Test pain point extraction and clustering"""
        pipeline = product_discovery_pipeline
        
        # Add sample personas
        pipeline.persona_insights = [
            PersonaInsight(
                persona_id="p1",
                pain_points=["Tool fragmentation", "Manual reporting"],
                activities=["Marketing tasks"]
            ),
            PersonaInsight(
                persona_id="p2",
                pain_points=["Inventory management", "Manual reporting"],
                activities=["Business operations"]
            )
        ]
        
        # Configure mock response
        mock_workflow_engine.execute_workflow.return_value = WorkflowResult(
            workflow_id="pain_point_clustering",
            status=WorkflowStatus.COMPLETED,
            started_at=datetime.now(),
            completed_at=datetime.now(),
            execution_time_ms=100.0,
            tool_results={
                "impact_propagation": {
                    "relationships": [
                        {"points": ["Tool fragmentation", "Manual reporting"]},
                        {"points": ["Inventory management", "Manual reporting"]}
                    ]
                }
            },
            errors=[]
        )
        
        # Execute clustering
        await pipeline._extract_pain_points()
        
        # Verify clusters created
        assert len(pipeline.pain_point_clusters) > 0
        assert pipeline.current_stage == AnalysisStage.PAIN_POINT_EXTRACTION
        
    async def test_idea_generation(self, product_discovery_pipeline, mock_workflow_engine):
        """Test product idea generation"""
        pipeline = product_discovery_pipeline
        
        # Add sample cluster
        pipeline.pain_point_clusters = [
            PainPointCluster(
                cluster_id="c1",
                pain_points=["Tool fragmentation", "Manual reporting"],
                affected_personas=["p1", "p2"],
                severity_score=0.8,
                frequency_score=0.9
            )
        ]
        
        # Configure mock response
        mock_workflow_engine.execute_workflow.return_value = WorkflowResult(
            workflow_id="idea_generation",
            status=WorkflowStatus.COMPLETED,
            started_at=datetime.now(),
            completed_at=datetime.now(),
            execution_time_ms=100.0,
            tool_results={
                "decision_framework": {
                    "recommendations": [
                        {
                            "title": "Unified Marketing Dashboard",
                            "description": "All-in-one marketing analytics platform",
                            "problem": "Tool fragmentation",
                            "value_proposition": "Single source of truth",
                            "feasibility": 0.7,
                            "innovation": 0.6
                        }
                    ]
                },
                "design_patterns": {
                    "patterns": []
                }
            },
            errors=[]
        )
        
        # Execute idea generation
        await pipeline._generate_ideas()
        
        # Verify ideas generated
        assert len(pipeline.product_ideas) == 1
        assert pipeline.current_stage == AnalysisStage.IDEA_GENERATION
        
        idea = pipeline.product_ideas[0]
        assert idea.title == "Unified Marketing Dashboard"
        assert idea.feasibility_score == 0.7
        
    async def test_multi_perspective_validation(self, product_discovery_pipeline, mock_workflow_engine):
        """Test multi-perspective validation of ideas"""
        pipeline = product_discovery_pipeline
        
        # Setup test data
        pipeline.persona_insights = [
            PersonaInsight(persona_id="p1", pain_points=["Tool fragmentation"])
        ]
        pipeline.product_ideas = [
            ProductIdea(
                idea_id="idea1",
                title="Test Product",
                description="Test description",
                problem_solved="Tool fragmentation",
                unique_value="Unified solution",
                target_clusters=["c1"],
                feasibility_score=0.7,
                innovation_score=0.6
            )
        ]
        pipeline.pain_point_clusters = [
            PainPointCluster(
                cluster_id="c1",
                pain_points=["Tool fragmentation"],
                affected_personas=["p1"],
                severity_score=0.8,
                frequency_score=0.9
            )
        ]
        
        # Configure mock response
        mock_workflow_engine.execute_workflow.return_value = WorkflowResult(
            workflow_id="idea_validation",
            status=WorkflowStatus.COMPLETED,
            started_at=datetime.now(),
            completed_at=datetime.now(),
            execution_time_ms=100.0,
            tool_results={
                "multi_perspective_analysis": {
                    "feedback": "Strong alignment with user needs",
                    "concerns": ["Implementation complexity"],
                    "opportunities": ["Market expansion"],
                    "score": 0.8
                }
            },
            errors=[]
        )
        
        # Execute validation
        await pipeline._validate_ideas()
        
        # Verify validations
        assert len(pipeline.validations) > 0
        assert pipeline.current_stage == AnalysisStage.MULTI_PERSPECTIVE_VALIDATION
        
    async def test_market_analysis(self, product_discovery_pipeline, mock_workflow_engine):
        """Test market analysis stage"""
        pipeline = product_discovery_pipeline
        
        # Setup validated ideas
        pipeline.product_ideas = [
            ProductIdea(
                idea_id="idea1",
                title="Test Product",
                description="Test",
                problem_solved="Problem",
                unique_value="Value",
                feasibility_score=0.7,
                innovation_score=0.6
            )
        ]
        pipeline.validations = [
            ValidationResult(
                idea_id="idea1",
                perspective_type="primary",
                feedback="Good",
                validation_score=0.8
            )
        ]
        
        # Configure mock response
        mock_workflow_engine.execute_workflow.return_value = WorkflowResult(
            workflow_id="market_analysis",
            status=WorkflowStatus.COMPLETED,
            started_at=datetime.now(),
            completed_at=datetime.now(),
            execution_time_ms=100.0,
            tool_results={
                "mental_models": {
                    "tam": "$10M",
                    "growth_rate": "high",
                    "competition": "moderate",
                    "barriers": ["Technical expertise"]
                },
                "decision_framework": {
                    "regulations": [],
                    "viability_score": 0.75
                }
            },
            errors=[]
        )
        
        # Execute market analysis
        await pipeline._analyze_market()
        
        # Verify analysis
        assert len(pipeline.market_analyses) > 0
        assert pipeline.current_stage == AnalysisStage.MARKET_ANALYSIS
        
        analysis = pipeline.market_analyses[0]
        assert analysis.market_size == "$10M"
        assert analysis.market_fit_score == 0.75
        
    async def test_end_to_end_pipeline(self, product_discovery_pipeline, mock_workflow_engine, sample_personas):
        """Test complete pipeline execution"""
        pipeline = product_discovery_pipeline
        
        # Configure mock to return appropriate responses for each stage
        async def mock_execute(*args, **kwargs):
            workflow_config = args[1]
            
            # Return different results based on workflow_id
            if workflow_config.name == "persona_analysis":
                return WorkflowResult(
                    workflow_id="persona_analysis",
                    status=WorkflowStatus.COMPLETED,
                    started_at=datetime.now(),
            completed_at=datetime.now(),
            execution_time_ms=100.0,
            tool_results={
                        "sequential_thinking": {
                            "demographics": {},
                            "activities": ["Activity 1"],
                            "pain_points": ["Pain point 1"],
                            "goals": ["Goal 1"]
                        },
                        "collaborative_reasoning": {"perspectives": []}
                    },
                    errors=[]
                )
            elif workflow_config.name == "pain_point_clustering":
                return WorkflowResult(
                    workflow_id="pain_point_clustering",
                    status=WorkflowStatus.COMPLETED,
                    started_at=datetime.now(),
            completed_at=datetime.now(),
            execution_time_ms=100.0,
            tool_results={"impact_propagation": {"relationships": []}},
                    errors=[]
                )
            # Add other stages as needed
            else:
                return WorkflowResult(
                    workflow_id=workflow_config.name,
                    status=WorkflowStatus.COMPLETED,
                    started_at=datetime.now(),
            completed_at=datetime.now(),
            execution_time_ms=100.0,
            tool_results={},
                    errors=[]
                )
                
        mock_workflow_engine.execute_workflow.side_effect = mock_execute
        
        # Execute full pipeline
        models = await pipeline.execute_pipeline(sample_personas)
        
        # Verify pipeline completed
        assert pipeline.current_stage == AnalysisStage.MODEL_OPTIMIZATION
        assert isinstance(models, list)
        
    async def test_error_handling(self, product_discovery_pipeline, mock_workflow_engine):
        """Test error handling in pipeline"""
        pipeline = product_discovery_pipeline
        
        # Configure mock to return error
        mock_workflow_engine.execute_workflow.return_value = WorkflowResult(
            workflow_id="test",
            status=WorkflowStatus.FAILED,
            started_at=datetime.now(),
            completed_at=datetime.now(),
            execution_time_ms=100.0,
            tool_results={},
            errors=["Test error"]
        )
        
        # Execute should handle error gracefully
        with pytest.raises(Exception):
            await pipeline._analyze_personas(["test persona"])
            
    def test_helper_methods(self, product_discovery_pipeline):
        """Test various helper methods"""
        pipeline = product_discovery_pipeline
        
        # Test _get_top_ideas
        pipeline.product_ideas = [
            ProductIdea(
                idea_id=f"idea{i}",
                title=f"Idea {i}",
                description="Test",
                problem_solved="Problem",
                unique_value="Value",
                feasibility_score=min(0.5 + i * 0.05, 1.0),
                innovation_score=min(0.5 + i * 0.05, 1.0)
            )
            for i in range(10)
        ]
        
        top_ideas = pipeline._get_top_ideas()
        assert len(top_ideas) <= 5
        assert all(idea.feasibility_score >= 0.5 for idea in top_ideas)
        
        # Test _select_best_usp
        pipeline.usp_options = [
            USPOption(
                usp_id="usp_idea1_0",
                statement="USP 1",
                target_audience="Everyone",
                effectiveness_score=0.7
            ),
            USPOption(
                usp_id="usp_idea1_1",
                statement="USP 2",
                target_audience="Everyone",
                effectiveness_score=0.9
            )
        ]
        
        best_usp = pipeline._select_best_usp("idea1")
        assert best_usp is not None
        assert best_usp.effectiveness_score == 0.9


class TestDataModels:
    """Test Pydantic models used in product discovery"""
    
    def test_persona_insight_model(self):
        """Test PersonaInsight model validation"""
        persona = PersonaInsight(
            persona_id="test1",
            demographics={"age": 30},
            activities=["coding", "meetings"],
            pain_points=["time management"],
            goals=["efficiency"],
            tech_comfort_level=0.8,
            decision_factors=["cost", "ease of use"]
        )
        
        assert persona.persona_id == "test1"
        assert persona.tech_comfort_level == 0.8
        assert len(persona.activities) == 2
        
        # Test model_dump (not dict)
        data = persona.model_dump()
        assert isinstance(data, dict)
        assert data["persona_id"] == "test1"
        
    def test_product_idea_model(self):
        """Test ProductIdea model validation"""
        idea = ProductIdea(
            idea_id="idea1",
            title="Test Product",
            description="A test product",
            problem_solved="Test problem",
            unique_value="Test value",
            target_clusters=["c1", "c2"],
            feasibility_score=0.7,
            innovation_score=0.8
        )
        
        assert idea.feasibility_score == 0.7
        assert len(idea.target_clusters) == 2
        
        # Test score bounds
        with pytest.raises(ValueError):
            ProductIdea(
                idea_id="bad",
                title="Bad",
                description="Bad",
                problem_solved="Bad",
                unique_value="Bad",
                feasibility_score=1.5  # Out of bounds
            )
            
    def test_optimized_product_model(self):
        """Test OptimizedProductModel validation"""
        model = OptimizedProductModel(
            model_id="model1",
            product_name="Test Product",
            description="Test description",
            target_personas=[],
            core_features=[],
            unique_selling_proposition=USPOption(
                usp_id="usp1",
                statement="Test USP",
                target_audience="Everyone",
                effectiveness_score=0.8
            ),
            business_model="SaaS",
            go_to_market_strategy="Digital",
            success_metrics=["metric1"],
            risk_factors=["risk1"],
            confidence_score=0.85
        )
        
        assert model.confidence_score == 0.85
        assert model.business_model == "SaaS"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])