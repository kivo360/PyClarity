"""
Test Progressive Analyzers as Default Interface

This demonstrates how progressive analyzers can be used as the default
interface for all cognitive tools, providing session management and
step-by-step analysis capabilities.
"""

import pytest
from typing import Dict, Any

from pyclarity.db.base import BaseSessionStore, SessionData
from pyclarity.db.mental_model_store import BaseMentalModelStore
from pyclarity.db.debugging_store import BaseDebuggingStore
from pyclarity.db.collaborative_store import BaseCollaborativeStore
from pyclarity.db.decision_store import BaseDecisionStore
from pyclarity.db.metacognitive_store import BaseMetacognitiveStore
from pyclarity.db.scientific_store import BaseScientificStore
from pyclarity.db.visual_store import BaseVisualStore
from pyclarity.db.creative_store import BaseCreativeStore
from pyclarity.db.systems_store import BaseSystemsStore

# Import progressive analyzers
from pyclarity.tools.mental_models.progressive_analyzer import (
    ProgressiveMentalModelAnalyzer,
    ProgressiveMentalModelRequest,
)
from pyclarity.tools.debugging_approaches.progressive_analyzer import (
    ProgressiveDebuggingAnalyzer,
    ProgressiveDebuggingRequest,
)
from pyclarity.tools.collaborative_reasoning.progressive_analyzer import (
    ProgressiveCollaborativeAnalyzer,
    ProgressiveCollaborativeRequest,
)
from pyclarity.tools.decision_framework.progressive_analyzer import (
    ProgressiveDecisionAnalyzer,
    ProgressiveDecisionRequest,
)
from pyclarity.tools.metacognitive_monitoring.progressive_analyzer import (
    ProgressiveMetacognitiveAnalyzer,
    ProgressiveMetacognitiveRequest,
)
from pyclarity.tools.scientific_method.progressive_analyzer import (
    ProgressiveScientificAnalyzer,
    ProgressiveScientificRequest,
)
from pyclarity.tools.visual_reasoning.progressive_analyzer import (
    ProgressiveVisualAnalyzer,
    ProgressiveVisualRequest,
)
from pyclarity.tools.creative_thinking.progressive_analyzer import (
    ProgressiveCreativeAnalyzer,
    ProgressiveCreativeRequest,
)
from pyclarity.tools.systems_thinking.progressive_analyzer import (
    ProgressiveSystemsAnalyzer,
    ProgressiveSystemsRequest,
)

# Import models
from pyclarity.tools.mental_models.models import MentalModelType
from pyclarity.tools.collaborative_reasoning.models import CollaborationType, SynthesisApproach
from pyclarity.tools.decision_framework.models import DecisionType, EvaluationMethod, TimePressure
from pyclarity.tools.metacognitive_monitoring.models import ThinkingMode, ReflectionDepth
from pyclarity.tools.scientific_method.models import ResearchPhase
from pyclarity.tools.visual_reasoning.models import VisualizationType, SpatialArrangement
from pyclarity.tools.creative_thinking.models import CreativeMode
from pyclarity.tools.systems_thinking.models import SystemPerspective, AnalysisFocus


class MockSessionStore(BaseSessionStore):
    """Mock session store for testing."""
    
    def __init__(self):
        self.sessions = {}
    
    async def create_session(self, session: SessionData) -> SessionData:
        self.sessions[session.session_id] = session
        session.id = len(self.sessions)
        return session
    
    async def get_session(self, session_id: str) -> SessionData | None:
        return self.sessions.get(session_id)
    
    async def update_session(self, session_id: str, **kwargs) -> SessionData | None:
        if session_id in self.sessions:
            for key, value in kwargs.items():
                setattr(self.sessions[session_id], key, value)
            return self.sessions[session_id]
        return None
    
    async def list_sessions(self, limit: int = 100, offset: int = 0) -> list[SessionData]:
        return list(self.sessions.values())[offset:offset+limit]


# Create mock stores for each tool
class MockMentalModelStore(BaseMentalModelStore):
    async def save_model_application(self, data: Any) -> Any:
        data.id = 1
        return data
    
    async def get_session_models(self, session_id: str) -> list[Any]:
        return []
    
    async def get_model_by_id(self, session_id: str, model_id: int) -> Any | None:
        return None


class MockDebuggingStore(BaseDebuggingStore):
    async def save_debugging_step(self, data: Any) -> Any:
        data.id = 1
        return data
    
    async def get_session_steps(self, session_id: str) -> list[Any]:
        return []
    
    async def get_hypotheses(self, session_id: str) -> list[Any]:
        return []


class MockCollaborativeStore(BaseCollaborativeStore):
    async def save_collaboration(self, data: Any) -> Any:
        data.id = 1
        return data
    
    async def get_session_collaborations(self, session_id: str) -> list[Any]:
        return []
    
    async def get_personas(self, session_id: str) -> list[Any]:
        return []


class MockDecisionStore(BaseDecisionStore):
    async def save_decision_step(self, data: Any) -> Any:
        data.id = 1
        return data
    
    async def get_session_decisions(self, session_id: str) -> list[Any]:
        return []
    
    async def get_criteria(self, session_id: str) -> list[Any]:
        return []
    
    async def get_alternatives(self, session_id: str) -> list[Any]:
        return []


class MockMetacognitiveStore(BaseMetacognitiveStore):
    async def save_assessment(self, data: Any) -> Any:
        data.id = 1
        return data
    
    async def get_session_assessments(self, session_id: str) -> list[Any]:
        return []


class MockScientificStore(BaseScientificStore):
    async def save_research_step(self, data: Any) -> Any:
        data.id = 1
        return data
    
    async def get_session_research(self, session_id: str) -> list[Any]:
        return []
    
    async def get_hypotheses(self, session_id: str) -> list[Any]:
        return []
    
    async def get_experiments(self, session_id: str) -> list[Any]:
        return []


class MockVisualStore(BaseVisualStore):
    async def save_visualization(self, data: Any) -> Any:
        data.id = 1
        return data
    
    async def get_session_visualizations(self, session_id: str) -> list[Any]:
        return []
    
    async def get_visual_elements(self, session_id: str) -> list[Any]:
        return []


class MockCreativeStore(BaseCreativeStore):
    async def save_creative_step(self, data: Any) -> Any:
        data.id = 1
        return data
    
    async def get_session_ideas(self, session_id: str) -> list[Any]:
        return []
    
    async def count_session_ideas(self, session_id: str) -> int:
        return 0
    
    async def get_ideas_by_ids(self, session_id: str, idea_ids: list[int]) -> list[Any]:
        return []


class MockSystemsStore(BaseSystemsStore):
    async def save_analysis_step(self, data: Any) -> Any:
        data.id = 1
        return data
    
    async def get_session_analyses(self, session_id: str) -> list[Any]:
        return []
    
    async def get_components(self, session_id: str) -> list[Any]:
        return []
    
    async def get_relationships(self, session_id: str) -> list[Any]:
        return []


@pytest.fixture
def session_store():
    return MockSessionStore()


@pytest.fixture
def all_stores(session_store):
    """Fixture providing all stores needed for progressive analyzers."""
    return {
        'session_store': session_store,
        'mental_model_store': MockMentalModelStore(),
        'debugging_store': MockDebuggingStore(),
        'collaborative_store': MockCollaborativeStore(),
        'decision_store': MockDecisionStore(),
        'metacognitive_store': MockMetacognitiveStore(),
        'scientific_store': MockScientificStore(),
        'visual_store': MockVisualStore(),
        'creative_store': MockCreativeStore(),
        'systems_store': MockSystemsStore(),
    }


@pytest.mark.asyncio
class TestProgressiveAnalyzersAsDefault:
    """Test suite demonstrating progressive analyzers as default interface."""
    
    async def test_mental_models_progressive(self, all_stores):
        """Test Mental Models using progressive analyzer."""
        analyzer = ProgressiveMentalModelAnalyzer(
            all_stores['session_store'],
            all_stores['mental_model_store']
        )
        
        request = ProgressiveMentalModelRequest(
            model_type=MentalModelType.FIRST_PRINCIPLES,
            problem_statement="How to optimize database performance?",
            context="E-commerce application with high traffic"
        )
        
        response = await analyzer.apply_model(request)
        
        assert response.status == "success"
        assert response.session_id is not None
        assert response.model_application_id == 1
        assert len(response.components) > 0
        assert len(response.insights) > 0
    
    async def test_debugging_progressive(self, all_stores):
        """Test Debugging using progressive analyzer."""
        analyzer = ProgressiveDebuggingAnalyzer(
            all_stores['session_store'],
            all_stores['debugging_store']
        )
        
        request = ProgressiveDebuggingRequest(
            debugging_type="systematic",
            issue_description="Application crashes on startup",
            error_message="NullPointerException in MainController"
        )
        
        response = await analyzer.analyze_issue(request)
        
        assert response.status == "success"
        assert response.session_id is not None
        assert response.current_hypothesis is not None
        assert len(response.evidence_gathered) >= 0
    
    async def test_collaborative_progressive(self, all_stores):
        """Test Collaborative Reasoning using progressive analyzer."""
        analyzer = ProgressiveCollaborativeAnalyzer(
            all_stores['session_store'],
            all_stores['collaborative_store']
        )
        
        request = ProgressiveCollaborativeRequest(
            collaboration_type=CollaborationType.CONSENSUS_BUILDING,
            topic="Best approach for microservices migration",
            context="Legacy monolithic application",
            synthesis_approach=SynthesisApproach.INTEGRATIVE
        )
        
        response = await analyzer.collaborate(request)
        
        assert response.status == "success"
        assert response.session_id is not None
        assert len(response.active_personas) > 0
        assert response.synthesis is not None
    
    async def test_decision_progressive(self, all_stores):
        """Test Decision Framework using progressive analyzer."""
        analyzer = ProgressiveDecisionAnalyzer(
            all_stores['session_store'],
            all_stores['decision_store']
        )
        
        request = ProgressiveDecisionRequest(
            decision_context="Choose cloud provider for new project",
            decision_type=DecisionType.STRATEGIC,
            evaluation_method=EvaluationMethod.WEIGHTED_CRITERIA,
            time_pressure=TimePressure.MODERATE
        )
        
        response = await analyzer.analyze_decision(request)
        
        assert response.status == "success"
        assert response.session_id is not None
        assert response.decision_readiness >= 0
        assert len(response.next_steps) > 0
    
    async def test_metacognitive_progressive(self, all_stores):
        """Test Metacognitive Monitoring using progressive analyzer."""
        analyzer = ProgressiveMetacognitiveAnalyzer(
            all_stores['session_store'],
            all_stores['metacognitive_store']
        )
        
        request = ProgressiveMetacognitiveRequest(
            current_thought="Considering different architectural patterns",
            thinking_context="System design phase",
            thinking_mode=ThinkingMode.ANALYTICAL,
            reflection_depth=ReflectionDepth.MODERATE
        )
        
        response = await analyzer.monitor_thinking(request)
        
        assert response.status == "success"
        assert response.session_id is not None
        assert response.thinking_quality_score >= 0
        assert len(response.thinking_strategies) > 0
    
    async def test_scientific_progressive(self, all_stores):
        """Test Scientific Method using progressive analyzer."""
        analyzer = ProgressiveScientificAnalyzer(
            all_stores['session_store'],
            all_stores['scientific_store']
        )
        
        request = ProgressiveScientificRequest(
            research_phase=ResearchPhase.OBSERVATION,
            research_question="What causes slow query performance?",
            domain="Database optimization",
            observations=["Queries slow during peak hours"]
        )
        
        response = await analyzer.conduct_research(request)
        
        assert response.status == "success"
        assert response.session_id is not None
        assert response.current_phase == ResearchPhase.OBSERVATION
        assert len(response.next_actions) > 0
    
    async def test_visual_progressive(self, all_stores):
        """Test Visual Reasoning using progressive analyzer."""
        analyzer = ProgressiveVisualAnalyzer(
            all_stores['session_store'],
            all_stores['visual_store']
        )
        
        request = ProgressiveVisualRequest(
            visualization_type=VisualizationType.CONCEPTUAL,
            subject="System architecture",
            context="Microservices design",
            spatial_arrangement=SpatialArrangement.HIERARCHICAL
        )
        
        response = await analyzer.analyze_visually(request)
        
        assert response.status == "success"
        assert response.session_id is not None
        assert len(response.visual_insights) > 0
        assert len(response.suggested_visualizations) > 0
    
    async def test_creative_progressive(self, all_stores):
        """Test Creative Thinking using progressive analyzer."""
        analyzer = ProgressiveCreativeAnalyzer(
            all_stores['session_store'],
            all_stores['creative_store']
        )
        
        request = ProgressiveCreativeRequest(
            challenge="Improve user onboarding experience",
            creative_mode=CreativeMode.DIVERGENT,
            seek_novelty=True
        )
        
        response = await analyzer.generate_ideas(request)
        
        assert response.status == "success"
        assert response.session_id is not None
        assert response.new_ideas_count > 0
        assert response.innovation_potential >= 0
    
    async def test_systems_progressive(self, all_stores):
        """Test Systems Thinking using progressive analyzer."""
        analyzer = ProgressiveSystemsAnalyzer(
            all_stores['session_store'],
            all_stores['systems_store']
        )
        
        request = ProgressiveSystemsRequest(
            system_name="E-commerce platform",
            system_description="Online retail system with inventory, orders, and payments",
            perspective=SystemPerspective.HOLISTIC,
            analysis_focus=AnalysisFocus.STRUCTURE
        )
        
        response = await analyzer.analyze_system(request)
        
        assert response.status == "success"
        assert response.session_id is not None
        assert len(response.system_insights) > 0
        assert response.system_health_score >= 0
    
    async def test_session_continuity(self, all_stores):
        """Test that sessions can be continued across multiple steps."""
        analyzer = ProgressiveMentalModelAnalyzer(
            all_stores['session_store'],
            all_stores['mental_model_store']
        )
        
        # First step
        request1 = ProgressiveMentalModelRequest(
            model_type=MentalModelType.FIRST_PRINCIPLES,
            problem_statement="How to scale a web application?",
            context="Growing startup"
        )
        
        response1 = await analyzer.apply_model(request1)
        session_id = response1.session_id
        
        # Second step - continue same session
        request2 = ProgressiveMentalModelRequest(
            session_id=session_id,
            model_type=MentalModelType.SYSTEMS_THINKING,
            problem_statement="How to scale a web application?",
            context="Growing startup",
            build_on_previous=True,
            previous_model_ids=[response1.model_application_id]
        )
        
        response2 = await analyzer.apply_model(request2)
        
        assert response2.session_id == session_id
        assert response2.step_number == 2
        assert response2.built_on_models == [response1.model_application_id]


@pytest.mark.asyncio
class TestProgressiveToolIntegration:
    """Test integration between multiple progressive tools."""
    
    async def test_mental_models_to_decision(self, all_stores):
        """Test flow from mental models analysis to decision making."""
        # First: Apply mental models to understand the problem
        mm_analyzer = ProgressiveMentalModelAnalyzer(
            all_stores['session_store'],
            all_stores['mental_model_store']
        )
        
        mm_request = ProgressiveMentalModelRequest(
            model_type=MentalModelType.OPPORTUNITY_COST,
            problem_statement="Should we rebuild or refactor the legacy system?",
            context="10-year-old monolithic application"
        )
        
        mm_response = await mm_analyzer.apply_model(mm_request)
        
        # Then: Use insights for decision analysis
        decision_analyzer = ProgressiveDecisionAnalyzer(
            all_stores['session_store'],
            all_stores['decision_store']
        )
        
        # Extract insights as criteria
        criteria = [
            {"name": insight, "weight": 0.2}
            for insight in mm_response.key_insights[:3]
        ]
        
        decision_request = ProgressiveDecisionRequest(
            decision_context="Rebuild vs Refactor decision",
            decision_type=DecisionType.STRATEGIC,
            criteria=criteria,
            alternatives=[
                {"name": "Complete rebuild", "description": "Start fresh with modern stack"},
                {"name": "Incremental refactor", "description": "Gradual modernization"}
            ],
            evaluation_method=EvaluationMethod.WEIGHTED_CRITERIA
        )
        
        decision_response = await decision_analyzer.analyze_decision(decision_request)
        
        assert decision_response.status == "success"
        assert len(decision_response.evaluated_alternatives) > 0
    
    async def test_debugging_with_metacognitive_monitoring(self, all_stores):
        """Test debugging process with metacognitive monitoring."""
        # Start debugging
        debug_analyzer = ProgressiveDebuggingAnalyzer(
            all_stores['session_store'],
            all_stores['debugging_store']
        )
        
        debug_request = ProgressiveDebuggingRequest(
            debugging_type="systematic",
            issue_description="Memory leak in production",
            hypothesis="Possible connection pool issue"
        )
        
        debug_response = await debug_analyzer.analyze_issue(debug_request)
        
        # Monitor thinking about the debugging process
        meta_analyzer = ProgressiveMetacognitiveAnalyzer(
            all_stores['session_store'],
            all_stores['metacognitive_store']
        )
        
        meta_request = ProgressiveMetacognitiveRequest(
            current_thought=f"Hypothesis: {debug_response.current_hypothesis}",
            thinking_context="Debugging memory leak",
            thinking_mode=ThinkingMode.CRITICAL,
            confidence_level=debug_response.hypothesis_confidence
        )
        
        meta_response = await meta_analyzer.monitor_thinking(meta_request)
        
        assert meta_response.status == "success"
        assert len(meta_response.bias_mitigation_suggestions) >= 0