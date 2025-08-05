"""Tests for progressive Sequential Thinking with session state."""

import pytest
from unittest.mock import AsyncMock, MagicMock

from pyclarity.db.base import SessionData, ThoughtData
from pyclarity.tools.sequential_thinking.progressive_analyzer import (
    ProgressiveSequentialThinkingAnalyzer,
    ProgressiveThoughtRequest,
    ProgressiveThoughtResponse,
)
from pyclarity.tools.sequential_thinking.models import ThoughtStepType


@pytest.fixture
def mock_session_store():
    """Create mock session store."""
    store = AsyncMock()
    store.get_session.return_value = None  # Default: no existing session
    store.create_session.return_value = SessionData(
        session_id="test-session-123",
        tool_name="Sequential Thinking (Progressive)",
        metadata={}
    )
    return store


@pytest.fixture
def mock_thought_store():
    """Create mock thought store."""
    store = AsyncMock()
    store.get_session_thoughts.return_value = []  # Default: no previous thoughts
    store.save_thought.return_value = ThoughtData(
        id=1,
        session_id="test-session-123",
        thought_number=1,
        total_thoughts=5,
        content="Test thought",
        confidence=0.85
    )
    return store


@pytest.fixture
def analyzer(mock_session_store, mock_thought_store):
    """Create analyzer with mock stores."""
    return ProgressiveSequentialThinkingAnalyzer(
        session_store=mock_session_store,
        thought_store=mock_thought_store
    )


@pytest.mark.asyncio
async def test_first_thought_creates_session(analyzer, mock_session_store):
    """Test that first thought creates a new session."""
    request = ProgressiveThoughtRequest(
        thought="Let me analyze this problem step by step",
        thought_number=1,
        total_thoughts=5,
        next_thought_needed=True
    )
    
    response = await analyzer.process_thought(request)
    
    assert response.status == "success"
    assert response.session_id is not None
    assert response.thought_number == 1
    assert response.next_thought_needed is True
    assert response.suggestion is not None
    
    # Verify session was created
    mock_session_store.create_session.assert_called_once()


@pytest.mark.asyncio
async def test_subsequent_thought_uses_existing_session(analyzer, mock_session_store, mock_thought_store):
    """Test that subsequent thoughts use existing session."""
    # Setup existing session
    mock_session_store.get_session.return_value = SessionData(
        session_id="existing-session",
        tool_name="Sequential Thinking (Progressive)",
        metadata={}
    )
    
    # Setup previous thoughts
    mock_thought_store.get_session_thoughts.return_value = [
        ThoughtData(
            id=1,
            session_id="existing-session",
            thought_number=1,
            total_thoughts=5,
            content="First thought",
            thought_type=ThoughtStepType.PROBLEM_DECOMPOSITION.value,
            confidence=0.85
        )
    ]
    
    request = ProgressiveThoughtRequest(
        session_id="existing-session",
        thought="Building on the previous analysis...",
        thought_number=2,
        total_thoughts=5,
        next_thought_needed=True
    )
    
    response = await analyzer.process_thought(request)
    
    assert response.status == "success"
    assert response.session_id == "existing-session"
    assert response.thought_number == 2
    
    # Verify session was not recreated
    mock_session_store.create_session.assert_not_called()


@pytest.mark.asyncio
async def test_thought_type_progression(analyzer, mock_thought_store):
    """Test that thought types progress logically."""
    # Test first thought
    request = ProgressiveThoughtRequest(
        thought="Breaking down the problem",
        thought_number=1,
        total_thoughts=5
    )
    
    response = await analyzer.process_thought(request)
    assert response.thought_type == ThoughtStepType.PROBLEM_DECOMPOSITION.value
    
    # Test middle thought with previous context
    mock_thought_store.get_session_thoughts.return_value = [
        ThoughtData(
            id=1,
            session_id="test-session",
            thought_number=1,
            total_thoughts=5,
            content="Problem decomposed",
            thought_type=ThoughtStepType.PROBLEM_DECOMPOSITION.value,
            confidence=0.85
        )
    ]
    
    request = ProgressiveThoughtRequest(
        session_id="test-session",
        thought="Forming hypothesis",
        thought_number=2,
        total_thoughts=5
    )
    
    response = await analyzer.process_thought(request)
    assert response.thought_type == ThoughtStepType.HYPOTHESIS_FORMATION.value


@pytest.mark.asyncio
async def test_final_thought_is_conclusion(analyzer, mock_thought_store):
    """Test that final thought is always a conclusion."""
    request = ProgressiveThoughtRequest(
        thought="Final analysis and recommendations",
        thought_number=5,
        total_thoughts=5,
        next_thought_needed=False
    )
    
    response = await analyzer.process_thought(request)
    assert response.thought_type == ThoughtStepType.CONCLUSION.value
    assert response.next_thought_needed is False


@pytest.mark.asyncio
async def test_branching_support(analyzer, mock_thought_store):
    """Test branching functionality."""
    request = ProgressiveThoughtRequest(
        session_id="test-session",
        thought="Alternative hypothesis to explore",
        thought_number=3,
        total_thoughts=7,
        branch_from_thought=2,
        branch_id="alt-hypothesis",
        next_thought_needed=True
    )
    
    response = await analyzer.process_thought(request)
    
    assert response.status == "success"
    assert response.branch_id == "alt-hypothesis"
    
    # Verify thought was saved with branch info
    saved_thought = mock_thought_store.save_thought.call_args[0][0]
    assert saved_thought.branch_id == "alt-hypothesis"
    assert saved_thought.branch_from_thought == 2


@pytest.mark.asyncio
async def test_revision_support(analyzer, mock_thought_store):
    """Test revision functionality."""
    request = ProgressiveThoughtRequest(
        session_id="test-session",
        thought="Revised analysis based on new evidence",
        thought_number=4,
        total_thoughts=6,
        is_revision=True,
        revises_thought=2,
        next_thought_needed=True
    )
    
    response = await analyzer.process_thought(request)
    
    assert response.status == "success"
    assert response.is_revision is True
    
    # Verify thought was saved with revision info
    saved_thought = mock_thought_store.save_thought.call_args[0][0]
    assert saved_thought.is_revision is True
    assert saved_thought.revises_thought == 2


@pytest.mark.asyncio
async def test_confidence_calculation(analyzer):
    """Test confidence score calculation."""
    # Problem decomposition should have high confidence
    request = ProgressiveThoughtRequest(
        thought="Breaking down the problem",
        thought_number=1,
        total_thoughts=5
    )
    
    response = await analyzer.process_thought(request)
    assert 0.8 <= response.confidence <= 0.9
    
    # Revisions should have slightly higher confidence
    request = ProgressiveThoughtRequest(
        thought="Revised analysis",
        thought_number=4,
        total_thoughts=5,
        is_revision=True
    )
    
    response = await analyzer.process_thought(request)
    assert response.confidence >= 0.85


@pytest.mark.asyncio
async def test_progress_tracking(analyzer, mock_thought_store):
    """Test progress tracking functionality."""
    # Setup some previous thoughts
    mock_thought_store.get_session_thoughts.return_value = [
        ThoughtData(id=i, session_id="test", thought_number=i, 
                   total_thoughts=5, content=f"Thought {i}", confidence=0.8)
        for i in range(1, 3)
    ]
    
    request = ProgressiveThoughtRequest(
        session_id="test",
        thought="Third thought",
        thought_number=3,
        total_thoughts=5
    )
    
    response = await analyzer.process_thought(request)
    
    assert response.progress["currentChainLength"] == 3
    assert response.progress["percentComplete"] == 60
    assert response.progress["thoughtsRemaining"] == 2
    assert response.progress["onTrack"] is True


@pytest.mark.asyncio
async def test_error_handling(analyzer, mock_thought_store):
    """Test error handling."""
    # Simulate database error
    mock_thought_store.save_thought.side_effect = Exception("Database error")
    
    request = ProgressiveThoughtRequest(
        thought="This will fail",
        thought_number=1,
        total_thoughts=5
    )
    
    response = await analyzer.process_thought(request)
    
    assert response.status == "error"
    assert response.error == "Database error"
    assert response.next_thought_needed is False


@pytest.mark.asyncio
async def test_suggestions_generation(analyzer):
    """Test that suggestions are context-aware."""
    # After problem decomposition, should suggest hypothesis
    request = ProgressiveThoughtRequest(
        thought="I've broken down the problem into components",
        thought_number=1,
        total_thoughts=5,
        next_thought_needed=True
    )
    
    response = await analyzer.process_thought(request)
    assert "hypothesis" in response.suggestion.lower() or "formulate" in response.suggestion.lower()
    
    # After evidence mention, should suggest pattern analysis
    request = ProgressiveThoughtRequest(
        thought="The evidence shows clear trends",
        thought_number=3,
        total_thoughts=5,
        next_thought_needed=True
    )
    
    response = await analyzer.process_thought(request)
    assert "pattern" in response.suggestion.lower() or "trend" in response.suggestion.lower()


@pytest.mark.asyncio
async def test_metadata_preservation(analyzer, mock_thought_store):
    """Test that metadata is preserved."""
    metadata = {"user_id": "user123", "context": "product_analysis"}
    
    request = ProgressiveThoughtRequest(
        thought="Analysis with metadata",
        thought_number=1,
        total_thoughts=5,
        metadata=metadata
    )
    
    response = await analyzer.process_thought(request)
    
    # Verify metadata was saved
    saved_thought = mock_thought_store.save_thought.call_args[0][0]
    assert saved_thought.metadata == metadata