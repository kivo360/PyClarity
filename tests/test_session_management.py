"""
Comprehensive tests for session management across all cognitive tools.

Tests cover:
1. Session creation and retrieval
2. Progressive analysis flow
3. State persistence across calls
4. Concurrent session handling
5. Error recovery scenarios
"""

import asyncio
import pytest
import pytest_asyncio
from datetime import datetime, timezone
from typing import List
from unittest.mock import AsyncMock, MagicMock

from pyclarity.db.base import BaseSessionStore, BaseThoughtStore, SessionData, ThoughtData
from pyclarity.db.mental_model_store import BaseMentalModelStore, MentalModelData
from pyclarity.db.debugging_store import BaseDebuggingStore, DebuggingData, DebuggingHypothesis
from pyclarity.tools.mental_models.models import MentalModelType
from pyclarity.tools.sequential_thinking.progressive_analyzer import (
    ProgressiveSequentialThinkingAnalyzer,
    ProgressiveThoughtRequest,
    ProgressiveThoughtResponse,
)
from pyclarity.tools.mental_models.progressive_analyzer import (
    ProgressiveMentalModelAnalyzer,
    ProgressiveMentalModelRequest,
    ProgressiveMentalModelResponse,
)
from pyclarity.tools.debugging_approaches.progressive_analyzer import (
    ProgressiveDebuggingAnalyzer,
    ProgressiveDebuggingRequest,
    ProgressiveDebuggingResponse,
)


# ============================================================================
# Mock Store Implementations
# ============================================================================

class MockSessionStore(BaseSessionStore):
    """In-memory mock session store for testing."""
    
    def __init__(self):
        self.sessions = {}
    
    async def create_session(self, session_data: SessionData) -> SessionData:
        self.sessions[session_data.session_id] = session_data
        return session_data
    
    async def get_session(self, session_id: str) -> SessionData | None:
        return self.sessions.get(session_id)
    
    async def update_session(self, session_id: str, updates: dict) -> SessionData | None:
        if session_id in self.sessions:
            session = self.sessions[session_id]
            for key, value in updates.items():
                setattr(session, key, value)
            return session
        return None
    
    async def delete_session(self, session_id: str) -> bool:
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False
    
    async def list_sessions(self, tool_name=None, active_only=True, limit=100, offset=0) -> List[SessionData]:
        sessions = list(self.sessions.values())
        if tool_name:
            sessions = [s for s in sessions if s.tool_name == tool_name]
        if active_only:
            sessions = [s for s in sessions if s.active]
        return sessions[offset:offset + limit]
    
    async def cleanup_old_sessions(self, days_old: int = 7) -> int:
        # Mock implementation
        return 0


class MockThoughtStore(BaseThoughtStore):
    """In-memory mock thought store for testing."""
    
    def __init__(self):
        self.thoughts = {}
        self.next_id = 1
    
    async def save_thought(self, thought: ThoughtData) -> ThoughtData:
        thought.id = self.next_id
        self.next_id += 1
        self.thoughts[thought.id] = thought
        return thought
    
    async def get_thought(self, thought_id: int) -> ThoughtData | None:
        return self.thoughts.get(thought_id)
    
    async def get_session_thoughts(self, session_id: str, branch_id=None) -> List[ThoughtData]:
        thoughts = [t for t in self.thoughts.values() if t.session_id == session_id]
        if branch_id:
            thoughts = [t for t in thoughts if t.branch_id == branch_id]
        return sorted(thoughts, key=lambda t: t.thought_number)
    
    async def get_latest_thought(self, session_id: str, branch_id=None) -> ThoughtData | None:
        thoughts = await self.get_session_thoughts(session_id, branch_id)
        return thoughts[-1] if thoughts else None
    
    async def update_thought(self, thought_id: int, updates: dict) -> ThoughtData | None:
        if thought_id in self.thoughts:
            thought = self.thoughts[thought_id]
            for key, value in updates.items():
                setattr(thought, key, value)
            return thought
        return None
    
    async def delete_thought(self, thought_id: int) -> bool:
        if thought_id in self.thoughts:
            del self.thoughts[thought_id]
            return True
        return False
    
    async def count_session_thoughts(self, session_id: str) -> int:
        return len([t for t in self.thoughts.values() if t.session_id == session_id])
    
    async def get_branch_thoughts(self, session_id: str, branch_id: str) -> List[ThoughtData]:
        return await self.get_session_thoughts(session_id, branch_id)
    
    async def search_thoughts(self, session_id=None, content_query=None, thought_type=None, min_confidence=None, limit=100) -> List[ThoughtData]:
        thoughts = list(self.thoughts.values())
        if session_id:
            thoughts = [t for t in thoughts if t.session_id == session_id]
        if content_query:
            thoughts = [t for t in thoughts if content_query.lower() in t.content.lower()]
        if thought_type:
            thoughts = [t for t in thoughts if t.thought_type == thought_type]
        if min_confidence:
            thoughts = [t for t in thoughts if t.confidence >= min_confidence]
        return thoughts[:limit]


class MockMentalModelStore(BaseMentalModelStore):
    """In-memory mock mental model store for testing."""
    
    def __init__(self):
        self.models = {}
        self.next_id = 1
    
    async def save_model_application(self, model_data: MentalModelData) -> MentalModelData:
        model_data.id = self.next_id
        self.next_id += 1
        self.models[model_data.id] = model_data
        return model_data
    
    async def get_model_application(self, application_id: int) -> MentalModelData | None:
        return self.models.get(application_id)
    
    async def get_session_models(self, session_id: str) -> List[MentalModelData]:
        return [m for m in self.models.values() if m.session_id == session_id]
    
    async def get_models_by_type(self, session_id: str, model_type: MentalModelType) -> List[MentalModelData]:
        return [m for m in self.models.values() if m.session_id == session_id and m.model_type == model_type]
    
    async def update_model_insights(self, application_id: int, insights: List[dict]) -> MentalModelData | None:
        if application_id in self.models:
            self.models[application_id].insights = insights
            return self.models[application_id]
        return None
    
    async def update_model_confidence(self, application_id: int, confidence: float) -> MentalModelData | None:
        if application_id in self.models:
            self.models[application_id].confidence_score = confidence
            return self.models[application_id]
        return None
    
    async def search_models(self, session_id=None, problem_query=None, model_type=None, min_confidence=None, limit=100) -> List[MentalModelData]:
        models = list(self.models.values())
        if session_id:
            models = [m for m in models if m.session_id == session_id]
        if problem_query:
            models = [m for m in models if problem_query.lower() in m.problem_statement.lower()]
        if model_type:
            models = [m for m in models if m.model_type == model_type]
        if min_confidence:
            models = [m for m in models if m.confidence_score >= min_confidence]
        return models[:limit]
    
    async def get_model_sequence(self, session_id: str) -> List[MentalModelData]:
        models = await self.get_session_models(session_id)
        return sorted(models, key=lambda m: m.created_at)
    
    async def count_session_models(self, session_id: str) -> dict[str, int]:
        models = await self.get_session_models(session_id)
        counts = {}
        for model in models:
            model_type = model.model_type.value
            counts[model_type] = counts.get(model_type, 0) + 1
        return counts


class MockDebuggingStore(BaseDebuggingStore):
    """In-memory mock debugging store for testing."""
    
    def __init__(self):
        self.steps = {}
        self.next_id = 1
    
    async def save_debugging_step(self, debug_data: DebuggingData) -> DebuggingData:
        debug_data.id = self.next_id
        self.next_id += 1
        self.steps[debug_data.id] = debug_data
        return debug_data
    
    async def get_debugging_step(self, step_id: int) -> DebuggingData | None:
        return self.steps.get(step_id)
    
    async def get_session_steps(self, session_id: str) -> List[DebuggingData]:
        steps = [s for s in self.steps.values() if s.session_id == session_id]
        return sorted(steps, key=lambda s: s.step_number)
    
    async def get_hypotheses(self, session_id: str, status=None) -> List[DebuggingHypothesis]:
        steps = await self.get_session_steps(session_id)
        hypotheses = []
        for step in steps:
            if step.hypothesis:
                if status is None or step.hypothesis.status == status:
                    hypotheses.append(step.hypothesis)
        return hypotheses
    
    async def update_hypothesis_status(self, step_id: int, hypothesis_id: int, status: str, evidence: dict) -> DebuggingData | None:
        if step_id in self.steps and self.steps[step_id].hypothesis:
            self.steps[step_id].hypothesis.status = status
            self.steps[step_id].hypothesis.evidence_for.append(str(evidence))
            return self.steps[step_id]
        return None
    
    async def add_test_result(self, step_id: int, test_name: str, test_result: dict) -> DebuggingData | None:
        if step_id in self.steps:
            self.steps[step_id].tests_performed.append({
                "name": test_name,
                "result": test_result
            })
            return self.steps[step_id]
        return None
    
    async def mark_solution_found(self, session_id: str, root_cause: str, solution: str, confidence: float) -> DebuggingData | None:
        steps = await self.get_session_steps(session_id)
        if steps:
            last_step = steps[-1]
            last_step.root_cause = root_cause
            last_step.solution = solution
            last_step.confidence = confidence
            return last_step
        return None
    
    async def get_debugging_patterns(self, session_id=None, debugging_type=None, min_confidence=None) -> List[dict]:
        # Mock implementation
        return []
    
    async def search_debugging_sessions(self, issue_query=None, error_type=None, solved_only=False, limit=100) -> List[DebuggingData]:
        steps = list(self.steps.values())
        if issue_query:
            steps = [s for s in steps if issue_query.lower() in s.issue_description.lower()]
        if solved_only:
            steps = [s for s in steps if s.solution is not None]
        return steps[:limit]


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest_asyncio.fixture
async def mock_stores():
    """Create mock stores for testing."""
    return {
        "session": MockSessionStore(),
        "thought": MockThoughtStore(),
        "mental_model": MockMentalModelStore(),
        "debugging": MockDebuggingStore(),
    }


@pytest_asyncio.fixture
async def sequential_analyzer(mock_stores):
    """Create sequential thinking analyzer with mock stores."""
    return ProgressiveSequentialThinkingAnalyzer(
        mock_stores["session"],
        mock_stores["thought"]
    )


@pytest_asyncio.fixture
async def mental_model_analyzer(mock_stores):
    """Create mental model analyzer with mock stores."""
    return ProgressiveMentalModelAnalyzer(
        mock_stores["session"],
        mock_stores["mental_model"]
    )


@pytest_asyncio.fixture
async def debugging_analyzer(mock_stores):
    """Create debugging analyzer with mock stores."""
    return ProgressiveDebuggingAnalyzer(
        mock_stores["session"],
        mock_stores["debugging"]
    )


# ============================================================================
# Session Management Tests
# ============================================================================

@pytest.mark.asyncio
class TestSessionManagement:
    """Test suite for session management functionality."""
    
    async def test_session_creation(self, mock_stores):
        """Test that sessions are created properly."""
        session_store = mock_stores["session"]
        
        # Create a session
        session_data = SessionData(
            session_id="test-session-123",
            tool_name="Test Tool",
            metadata={"test": True}
        )
        
        created = await session_store.create_session(session_data)
        assert created.session_id == "test-session-123"
        assert created.tool_name == "Test Tool"
        assert created.active is True
        
        # Retrieve the session
        retrieved = await session_store.get_session("test-session-123")
        assert retrieved is not None
        assert retrieved.session_id == created.session_id
    
    async def test_session_update(self, mock_stores):
        """Test session update functionality."""
        session_store = mock_stores["session"]
        
        # Create a session
        session_data = SessionData(
            session_id="update-test",
            tool_name="Test Tool"
        )
        await session_store.create_session(session_data)
        
        # Update the session
        updated = await session_store.update_session(
            "update-test",
            {"active": False, "metadata": {"updated": True}}
        )
        
        assert updated is not None
        assert updated.active is False
        assert updated.metadata["updated"] is True
    
    async def test_session_cleanup(self, mock_stores):
        """Test session cleanup functionality."""
        session_store = mock_stores["session"]
        
        # Create multiple sessions
        for i in range(5):
            session_data = SessionData(
                session_id=f"session-{i}",
                tool_name="Test Tool"
            )
            await session_store.create_session(session_data)
        
        # List sessions
        sessions = await session_store.list_sessions()
        assert len(sessions) == 5
        
        # Delete a session
        deleted = await session_store.delete_session("session-2")
        assert deleted is True
        
        # Verify deletion
        sessions = await session_store.list_sessions()
        assert len(sessions) == 4
        assert all(s.session_id != "session-2" for s in sessions)


# ============================================================================
# Progressive Sequential Thinking Tests
# ============================================================================

@pytest.mark.asyncio
class TestProgressiveSequentialThinking:
    """Test suite for progressive sequential thinking with sessions."""
    
    async def test_progressive_thought_flow(self, sequential_analyzer):
        """Test progressive thought generation across multiple calls."""
        # First thought
        request1 = ProgressiveThoughtRequest(
            thought="Breaking down the problem into core components",
            thought_number=1,
            total_thoughts=3,
            next_thought_needed=True
        )
        
        response1 = await sequential_analyzer.process_thought(request1)
        assert response1.status == "success"
        assert response1.session_id is not None
        assert response1.thought_number == 1
        assert response1.next_thought_needed is True
        assert response1.suggestion is not None
        
        session_id = response1.session_id
        
        # Second thought, building on first
        request2 = ProgressiveThoughtRequest(
            session_id=session_id,
            thought="Based on the decomposition, the key issue appears to be resource allocation",
            thought_number=2,
            total_thoughts=3,
            next_thought_needed=True
        )
        
        response2 = await sequential_analyzer.process_thought(request2)
        assert response2.status == "success"
        assert response2.session_id == session_id
        assert response2.thought_number == 2
        
        # Final thought
        request3 = ProgressiveThoughtRequest(
            session_id=session_id,
            thought="The optimal solution involves dynamic resource balancing with feedback loops",
            thought_number=3,
            total_thoughts=3,
            next_thought_needed=False
        )
        
        response3 = await sequential_analyzer.process_thought(request3)
        assert response3.status == "success"
        assert response3.next_thought_needed is False
        assert response3.progress["percentComplete"] == 100
    
    async def test_thought_branching(self, sequential_analyzer):
        """Test branching in thought process."""
        # Initial thought
        request1 = ProgressiveThoughtRequest(
            thought="Initial analysis of the problem",
            thought_number=1,
            total_thoughts=5
        )
        response1 = await sequential_analyzer.process_thought(request1)
        session_id = response1.session_id
        
        # Create a branch
        request_branch = ProgressiveThoughtRequest(
            session_id=session_id,
            thought="Alternative hypothesis: the issue might be in the data layer",
            thought_number=2,
            total_thoughts=5,
            branch_from_thought=1,
            branch_id="data-hypothesis"
        )
        
        response_branch = await sequential_analyzer.process_thought(request_branch)
        assert response_branch.status == "success"
        assert response_branch.branch_id == "data-hypothesis"
        assert response_branch.progress["branch"] is True
    
    async def test_thought_revision(self, sequential_analyzer):
        """Test revision of previous thoughts."""
        # Initial thoughts
        request1 = ProgressiveThoughtRequest(
            thought="First analysis",
            thought_number=1,
            total_thoughts=3
        )
        response1 = await sequential_analyzer.process_thought(request1)
        session_id = response1.session_id
        
        request2 = ProgressiveThoughtRequest(
            session_id=session_id,
            thought="Second analysis",
            thought_number=2,
            total_thoughts=3
        )
        response2 = await sequential_analyzer.process_thought(request2)
        
        # Revise first thought
        request_revision = ProgressiveThoughtRequest(
            session_id=session_id,
            thought="Revised first analysis with new insights",
            thought_number=3,
            total_thoughts=4,  # Extended for revision
            is_revision=True,
            revises_thought=1
        )
        
        response_revision = await sequential_analyzer.process_thought(request_revision)
        assert response_revision.status == "success"
        assert response_revision.is_revision is True


# ============================================================================
# Progressive Mental Models Tests
# ============================================================================

@pytest.mark.asyncio
class TestProgressiveMentalModels:
    """Test suite for progressive mental model application."""
    
    async def test_single_model_application(self, mental_model_analyzer):
        """Test applying a single mental model."""
        request = ProgressiveMentalModelRequest(
            model_type=MentalModelType.FIRST_PRINCIPLES,
            problem_statement="How to improve system performance?",
            context="Web application with slow response times"
        )
        
        response = await mental_model_analyzer.apply_model(request)
        assert response.status == "success"
        assert response.model_type == MentalModelType.FIRST_PRINCIPLES.value
        assert len(response.insights) > 0
        assert len(response.recommendations) > 0
        assert response.fundamental_elements is not None
        assert response.confidence_score > 0
    
    async def test_multiple_model_sequence(self, mental_model_analyzer):
        """Test applying multiple models in sequence."""
        # First model: First Principles
        request1 = ProgressiveMentalModelRequest(
            model_type=MentalModelType.FIRST_PRINCIPLES,
            problem_statement="Design a scalable system"
        )
        response1 = await mental_model_analyzer.apply_model(request1)
        session_id = response1.session_id
        
        # Second model: Opportunity Cost
        request2 = ProgressiveMentalModelRequest(
            session_id=session_id,
            model_type=MentalModelType.OPPORTUNITY_COST,
            problem_statement="Design a scalable system",
            build_on_previous=True
        )
        response2 = await mental_model_analyzer.apply_model(request2)
        
        assert response2.session_id == session_id
        assert response2.models_applied_count == 2
        assert response2.trade_offs is not None
        
        # Third model: Error Propagation
        request3 = ProgressiveMentalModelRequest(
            session_id=session_id,
            model_type=MentalModelType.ERROR_PROPAGATION,
            problem_statement="Design a scalable system",
            build_on_previous=True
        )
        response3 = await mental_model_analyzer.apply_model(request3)
        
        assert response3.models_applied_count == 3
        assert response3.error_impacts is not None
        assert len(response3.suggested_models) > 0
    
    async def test_model_building_on_previous(self, mental_model_analyzer):
        """Test building on previous model insights."""
        # Apply first model
        request1 = ProgressiveMentalModelRequest(
            model_type=MentalModelType.PARETO_PRINCIPLE,
            problem_statement="Optimize feature development"
        )
        response1 = await mental_model_analyzer.apply_model(request1)
        
        # Apply second model building on first
        request2 = ProgressiveMentalModelRequest(
            session_id=response1.session_id,
            model_type=MentalModelType.OPPORTUNITY_COST,
            problem_statement="Optimize feature development",
            previous_model_ids=[response1.application_id],
            build_on_previous=True
        )
        response2 = await mental_model_analyzer.apply_model(request2)
        
        # Check for integration insight
        integration_insights = [
            i for i in response2.insights 
            if i.get("category") == "Integration"
        ]
        assert len(integration_insights) > 0


# ============================================================================
# Progressive Debugging Tests
# ============================================================================

@pytest.mark.asyncio
class TestProgressiveDebugging:
    """Test suite for progressive debugging with sessions."""
    
    async def test_systematic_debugging_flow(self, debugging_analyzer):
        """Test systematic debugging approach."""
        # Initial problem
        request1 = ProgressiveDebuggingRequest(
            step_number=1,
            debugging_type="systematic",
            issue_description="Application crashes on user login",
            error_message="NullPointerException in AuthService",
            evidence=["Happens only for new users", "OAuth flow involved"]
        )
        
        response1 = await debugging_analyzer.analyze_issue(request1)
        assert response1.status == "success"
        assert response1.debugging_type == "systematic"
        assert len(response1.next_steps) > 0
        assert response1.confidence > 0
        
        session_id = response1.session_id
        
        # Form hypothesis
        request2 = ProgressiveDebuggingRequest(
            session_id=session_id,
            step_number=2,
            debugging_type="systematic",
            issue_description="Application crashes on user login",
            hypothesis="OAuth token not properly initialized for new users",
            evidence=response1.evidence_gathered + ["Token is null in logs"],
            test_plan="Add logging to OAuth initialization flow"
        )
        
        response2 = await debugging_analyzer.analyze_issue(request2)
        assert response2.step_number == 2
        assert response2.current_hypothesis is not None
        assert response2.confidence > response1.confidence
    
    async def test_bisection_debugging(self, debugging_analyzer):
        """Test bisection debugging approach."""
        request = ProgressiveDebuggingRequest(
            debugging_type="bisection",
            issue_description="Performance degrades after 1000 records",
            step_number=1
        )
        
        response = await debugging_analyzer.analyze_issue(request)
        assert response.debugging_type == "bisection"
        assert "midpoint" in response.next_steps[0].lower()
        assert response.estimated_steps_remaining is not None
    
    async def test_debugging_with_solution(self, debugging_analyzer):
        """Test finding and marking solution."""
        # Build up evidence
        request1 = ProgressiveDebuggingRequest(
            debugging_type="pattern_matching",
            issue_description="Memory leak in background service",
            error_message="OutOfMemoryError after 24 hours"
        )
        response1 = await debugging_analyzer.analyze_issue(request1)
        
        # High confidence hypothesis
        request2 = ProgressiveDebuggingRequest(
            session_id=response1.session_id,
            step_number=2,
            debugging_type="pattern_matching",
            issue_description="Memory leak in background service",
            hypothesis="Event listeners not being properly removed",
            evidence=["Heap dump shows accumulating listeners", "Count increases linearly"]
        )
        response2 = await debugging_analyzer.analyze_issue(request2)
        
        # Solution found
        request3 = ProgressiveDebuggingRequest(
            session_id=response1.session_id,
            step_number=3,
            debugging_type="systematic",
            issue_description="Memory leak in background service",
            hypothesis="Confirmed: Event listeners not removed on service restart",
            evidence=response2.evidence_gathered + ["Fixed by adding cleanup in destroy()"]
        )
        
        # Manually set root cause for test
        debug_store = debugging_analyzer.debug_store
        await debug_store.mark_solution_found(
            response1.session_id,
            "Event listeners not properly cleaned up",
            "Add listener cleanup in service destroy method",
            0.95
        )
        
        response3 = await debugging_analyzer.analyze_issue(request3)
        # The analyzer should detect that a solution was found
        assert response3.confidence > 0.9


# ============================================================================
# Concurrent Session Tests
# ============================================================================

@pytest.mark.asyncio
class TestConcurrentSessions:
    """Test concurrent session handling."""
    
    async def test_multiple_concurrent_sessions(self, mental_model_analyzer):
        """Test that multiple sessions don't interfere."""
        # Create multiple concurrent sessions
        requests = []
        for i in range(5):
            request = ProgressiveMentalModelRequest(
                model_type=MentalModelType.FIRST_PRINCIPLES,
                problem_statement=f"Problem {i}"
            )
            requests.append(request)
        
        # Process all requests concurrently
        responses = await asyncio.gather(*[
            mental_model_analyzer.apply_model(req) for req in requests
        ])
        
        # Verify all succeeded with unique sessions
        session_ids = set()
        for i, response in enumerate(responses):
            assert response.status == "success"
            assert response.session_id not in session_ids
            session_ids.add(response.session_id)
            
            # Verify problem matches
            assert f"Problem {i}" in str(response.insights)
    
    async def test_session_isolation(self, sequential_analyzer, mock_stores):
        """Test that sessions are properly isolated."""
        # Create two sessions
        request1 = ProgressiveThoughtRequest(
            thought="Session 1 thought",
            thought_number=1,
            total_thoughts=2
        )
        response1 = await sequential_analyzer.process_thought(request1)
        
        request2 = ProgressiveThoughtRequest(
            thought="Session 2 thought",
            thought_number=1,
            total_thoughts=2
        )
        response2 = await sequential_analyzer.process_thought(request2)
        
        # Verify different sessions
        assert response1.session_id != response2.session_id
        
        # Check stored thoughts
        thought_store = mock_stores["thought"]
        
        session1_thoughts = await thought_store.get_session_thoughts(response1.session_id)
        session2_thoughts = await thought_store.get_session_thoughts(response2.session_id)
        
        assert len(session1_thoughts) == 1
        assert len(session2_thoughts) == 1
        assert session1_thoughts[0].content == "Session 1 thought"
        assert session2_thoughts[0].content == "Session 2 thought"


# ============================================================================
# Error Recovery Tests
# ============================================================================

@pytest.mark.asyncio
class TestErrorRecovery:
    """Test error handling and recovery scenarios."""
    
    async def test_invalid_session_recovery(self, mental_model_analyzer):
        """Test handling of invalid session IDs."""
        request = ProgressiveMentalModelRequest(
            session_id="non-existent-session",
            model_type=MentalModelType.OCCAMS_RAZOR,
            problem_statement="Test problem"
        )
        
        # Should create new session instead of failing
        response = await mental_model_analyzer.apply_model(request)
        assert response.status == "success"
        assert response.session_id == "non-existent-session"
    
    async def test_store_failure_handling(self, mock_stores):
        """Test handling of store failures."""
        # Create analyzer with failing store
        session_store = mock_stores["session"]
        thought_store = mock_stores["thought"]
        
        # Mock a failure
        original_save = thought_store.save_thought
        thought_store.save_thought = AsyncMock(side_effect=Exception("Database error"))
        
        analyzer = ProgressiveSequentialThinkingAnalyzer(session_store, thought_store)
        
        request = ProgressiveThoughtRequest(
            thought="Test thought",
            thought_number=1
        )
        
        response = await analyzer.process_thought(request)
        assert response.status == "error"
        assert "Database error" in response.error
        
        # Restore original method
        thought_store.save_thought = original_save
    
    async def test_partial_state_recovery(self, debugging_analyzer, mock_stores):
        """Test recovery from partial state."""
        # Create initial state
        request1 = ProgressiveDebuggingRequest(
            debugging_type="systematic",
            issue_description="Test issue",
            step_number=1
        )
        response1 = await debugging_analyzer.analyze_issue(request1)
        session_id = response1.session_id
        
        # Simulate partial state loss (delete from store but keep session)
        debug_store = mock_stores["debugging"]
        steps = await debug_store.get_session_steps(session_id)
        if steps:
            await debug_store.delete_step(steps[0].id)
        
        # Try to continue debugging
        request2 = ProgressiveDebuggingRequest(
            session_id=session_id,
            debugging_type="systematic",
            issue_description="Test issue",
            step_number=2,
            build_on_previous=False  # Don't rely on previous state
        )
        
        response2 = await debugging_analyzer.analyze_issue(request2)
        assert response2.status == "success"
        assert response2.step_number == 2


# ============================================================================
# Integration Tests
# ============================================================================

@pytest.mark.asyncio
class TestToolIntegration:
    """Test integration between different tools using sessions."""
    
    async def test_cross_tool_session_sharing(self, mock_stores):
        """Test sharing sessions between different tools."""
        session_store = mock_stores["session"]
        
        # Create session with sequential thinking
        thought_store = mock_stores["thought"]
        seq_analyzer = ProgressiveSequentialThinkingAnalyzer(session_store, thought_store)
        
        seq_request = ProgressiveThoughtRequest(
            thought="Analyzing system architecture",
            thought_number=1
        )
        seq_response = await seq_analyzer.process_thought(seq_request)
        session_id = seq_response.session_id
        
        # Use same session with mental models
        model_store = mock_stores["mental_model"]
        model_analyzer = ProgressiveMentalModelAnalyzer(session_store, model_store)
        
        model_request = ProgressiveMentalModelRequest(
            session_id=session_id,  # Reuse session
            model_type=MentalModelType.FIRST_PRINCIPLES,
            problem_statement="System architecture optimization"
        )
        model_response = await model_analyzer.apply_model(model_request)
        
        assert model_response.session_id == session_id
        
        # Verify session was updated by both tools
        session = await session_store.get_session(session_id)
        assert session is not None
        # Both tools should have updated the session
        assert session.updated_at > session.created_at


if __name__ == "__main__":
    pytest.main([__file__, "-v"])