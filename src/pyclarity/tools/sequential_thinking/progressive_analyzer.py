"""
Progressive Sequential Thinking Analyzer.

This version supports step-by-step thought generation with session state persistence,
allowing the MCP server to return one thought at a time instead of generating all
thoughts at once.
"""

import logging
import uuid
from typing import Any, Dict, Optional, Tuple

from pydantic import BaseModel, Field, ConfigDict

from pyclarity.db.base import BaseSessionStore, BaseThoughtStore, SessionData, ThoughtData
from pyclarity.tools.sequential_thinking.models import (
    ComplexityLevel,
    ThoughtStepType,
)

logger = logging.getLogger(__name__)


class ProgressiveThoughtRequest(BaseModel):
    """Request for a single progressive thought step."""
    
    session_id: Optional[str] = Field(default=None, description="Session ID for continuing existing session")
    thought: str = Field(..., description="The current thought to process")
    thought_number: int = Field(1, description="The number of this thought in the sequence")
    total_thoughts: int = Field(5, description="Total expected thoughts in this sequence")
    next_thought_needed: bool = Field(True, description="Whether another thought is needed")
    is_revision: bool = Field(False, description="Whether this revises a previous thought")
    revises_thought: Optional[int] = Field(None, description="Which thought this revises")
    branch_from_thought: Optional[int] = Field(None, description="Thought number to branch from")
    branch_id: Optional[str] = Field(None, description="Unique identifier for this branch")
    needs_more_thoughts: bool = Field(False, description="Whether more thoughts are needed beyond total")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    def __init__(self, **data):
        super().__init__(**data)
        if self.session_id is None:
            self.session_id = str(uuid.uuid4())


class ProgressiveThoughtResponse(BaseModel):
    """Response for a single progressive thought step."""
    
    session_id: str = Field(..., description="Session ID", alias="sessionId")
    thought_id: Optional[int] = Field(None, description="Database ID of the thought", alias="thoughtId")
    thought_number: int = Field(..., description="Thought number in sequence", alias="thoughtNumber")
    total_thoughts: int = Field(..., description="Total expected thoughts", alias="totalThoughts")
    status: str = Field("success", description="Status of the operation")
    next_thought_needed: bool = Field(True, description="Whether another thought is needed", alias="nextThoughtNeeded")
    is_revision: bool = Field(False, description="Whether this is a revision", alias="isRevision")
    branch_id: Optional[str] = Field(None, description="Branch identifier", alias="branchId")
    message: str = Field("", description="Status message")
    suggestion: Optional[str] = Field(None, description="Suggestion for next thought")
    confidence: float = Field(0.85, description="Confidence score")
    thought_type: Optional[str] = Field(None, description="Type of thinking step", alias="thoughtType")
    progress: Dict[str, Any] = Field(default_factory=dict, description="Progress information")
    error: Optional[str] = Field(None, description="Error message if failed")
    
    model_config = ConfigDict(populate_by_name=True)  # Allow both snake_case and camelCase


class ProgressiveSequentialThinkingAnalyzer:
    """Progressive sequential thinking analyzer with session state."""
    
    def __init__(
        self,
        session_store: BaseSessionStore,
        thought_store: BaseThoughtStore,
    ):
        """Initialize with database stores."""
        self.session_store = session_store
        self.thought_store = thought_store
        self.tool_name = "Sequential Thinking (Progressive)"
        self.version = "3.0.0"
    
    async def process_thought(
        self, request: ProgressiveThoughtRequest
    ) -> ProgressiveThoughtResponse:
        """Process a single thought in the reasoning chain."""
        try:
            # Ensure session exists
            session = await self._ensure_session(request.session_id)
            
            # Get previous thoughts for context
            previous_thoughts = await self.thought_store.get_session_thoughts(
                request.session_id, request.branch_id
            )
            
            # Determine thought type
            thought_type = self._determine_thought_type(
                request.thought_number, request.total_thoughts, previous_thoughts
            )
            
            # Generate supporting evidence and assumptions
            evidence, assumptions, errors = self._analyze_thought_content(
                request.thought, thought_type, previous_thoughts
            )
            
            # Calculate confidence
            confidence = self._calculate_confidence(
                thought_type, len(previous_thoughts), request.is_revision
            )
            
            # Save the thought
            thought_data = ThoughtData(
                session_id=request.session_id,
                thought_number=request.thought_number,
                total_thoughts=request.total_thoughts,
                content=request.thought,
                thought_type=thought_type.value,
                confidence=confidence,
                branch_id=request.branch_id,
                branch_from_thought=request.branch_from_thought,
                revises_thought=request.revises_thought,
                is_revision=request.is_revision,
                needs_more_thoughts=request.needs_more_thoughts,
                next_thought_needed=request.next_thought_needed,
                supporting_evidence=evidence,
                assumptions_made=assumptions,
                potential_errors=errors,
                metadata=request.metadata,
            )
            
            saved_thought = await self.thought_store.save_thought(thought_data)
            
            # Update session
            await self.session_store.update_session(
                request.session_id,
                {"updated_at": thought_data.created_at}
            )
            
            # Generate suggestion for next thought
            suggestion = None
            if request.next_thought_needed:
                suggestion = self._generate_next_suggestion(
                    thought_type, request.thought, previous_thoughts
                )
            
            # Calculate progress
            progress = self._calculate_progress(
                request.thought_number,
                request.total_thoughts,
                len(previous_thoughts) + 1,
                request.branch_id
            )
            
            return ProgressiveThoughtResponse(
                session_id=request.session_id,
                thought_id=saved_thought.id,
                thought_number=request.thought_number,
                total_thoughts=request.total_thoughts,
                status="success",
                next_thought_needed=request.next_thought_needed,
                is_revision=request.is_revision,
                branch_id=request.branch_id,
                message=f"Processed thought {request.thought_number}/{request.total_thoughts}",
                suggestion=suggestion,
                confidence=confidence,
                thought_type=thought_type.value,
                progress=progress,
            )
            
        except Exception as e:
            logger.error(f"Error processing thought: {e}")
            return ProgressiveThoughtResponse(
                session_id=request.session_id or "error",
                thought_id=None,
                thought_number=request.thought_number,
                total_thoughts=request.total_thoughts,
                status="error",
                next_thought_needed=False,
                error=str(e),
            )
    
    async def _ensure_session(self, session_id: str) -> SessionData:
        """Ensure session exists, create if needed."""
        session = await self.session_store.get_session(session_id)
        
        if not session:
            session = SessionData(
                session_id=session_id,
                tool_name=self.tool_name,
                metadata={"version": self.version}
            )
            session = await self.session_store.create_session(session)
        
        return session
    
    def _determine_thought_type(
        self,
        thought_number: int,
        total_thoughts: int,
        previous_thoughts: list[ThoughtData]
    ) -> ThoughtStepType:
        """Determine the type of reasoning step."""
        if thought_number == 1:
            return ThoughtStepType.PROBLEM_DECOMPOSITION
        
        if thought_number == total_thoughts:
            return ThoughtStepType.CONCLUSION
        
        # Analyze previous thought types
        previous_types = [t.thought_type for t in previous_thoughts if t.thought_type]
        
        # Progressive reasoning flow
        if ThoughtStepType.PROBLEM_DECOMPOSITION.value in previous_types:
            if ThoughtStepType.HYPOTHESIS_FORMATION.value not in previous_types:
                return ThoughtStepType.HYPOTHESIS_FORMATION
        
        if ThoughtStepType.HYPOTHESIS_FORMATION.value in previous_types:
            if ThoughtStepType.EVIDENCE_GATHERING.value not in previous_types:
                return ThoughtStepType.EVIDENCE_GATHERING
        
        if ThoughtStepType.EVIDENCE_GATHERING.value in previous_types:
            if thought_number / total_thoughts > 0.7:
                return ThoughtStepType.SYNTHESIS
            return ThoughtStepType.LOGICAL_DEDUCTION
        
        # Default progression
        if thought_number / total_thoughts < 0.3:
            return ThoughtStepType.PATTERN_RECOGNITION
        elif thought_number / total_thoughts < 0.6:
            return ThoughtStepType.LOGICAL_DEDUCTION
        elif thought_number / total_thoughts < 0.8:
            return ThoughtStepType.VALIDATION
        else:
            return ThoughtStepType.SYNTHESIS
    
    def _analyze_thought_content(
        self,
        thought: str,
        thought_type: ThoughtStepType,
        previous_thoughts: list[ThoughtData]
    ) -> Tuple[list[str], list[str], list[str]]:
        """Analyze thought content to extract evidence, assumptions, and errors."""
        thought_lower = thought.lower()
        
        # Extract evidence indicators
        evidence = []
        if any(word in thought_lower for word in ["data", "shows", "indicates", "evidence"]):
            evidence.append("Empirical data referenced")
        if any(word in thought_lower for word in ["research", "study", "analysis"]):
            evidence.append("Research findings cited")
        if any(word in thought_lower for word in ["observed", "measured", "recorded"]):
            evidence.append("Direct observation mentioned")
        
        # Extract assumptions
        assumptions = []
        if thought_type == ThoughtStepType.HYPOTHESIS_FORMATION:
            assumptions.append("Hypothesis based on available information")
        if any(word in thought_lower for word in ["assume", "likely", "probably"]):
            assumptions.append("Probabilistic reasoning applied")
        if any(word in thought_lower for word in ["should", "would", "could"]):
            assumptions.append("Conditional logic employed")
        
        # Identify potential errors
        errors = []
        if any(word in thought_lower for word in ["might", "perhaps", "unclear"]):
            errors.append("Uncertainty acknowledged")
        if len(previous_thoughts) < 2 and thought_type == ThoughtStepType.CONCLUSION:
            errors.append("Potentially premature conclusion")
        
        return evidence, assumptions, errors
    
    def _calculate_confidence(
        self,
        thought_type: ThoughtStepType,
        num_previous: int,
        is_revision: bool
    ) -> float:
        """Calculate confidence score for the thought."""
        # Base confidence by type
        base_confidence = {
            ThoughtStepType.PROBLEM_DECOMPOSITION: 0.85,
            ThoughtStepType.HYPOTHESIS_FORMATION: 0.70,
            ThoughtStepType.EVIDENCE_GATHERING: 0.80,
            ThoughtStepType.LOGICAL_DEDUCTION: 0.88,
            ThoughtStepType.PATTERN_RECOGNITION: 0.75,
            ThoughtStepType.ASSUMPTION_TESTING: 0.82,
            ThoughtStepType.SYNTHESIS: 0.85,
            ThoughtStepType.VALIDATION: 0.90,
            ThoughtStepType.CONCLUSION: 0.87,
        }.get(thought_type, 0.75)
        
        # Adjust for context
        if num_previous > 3:
            base_confidence += 0.05  # More context increases confidence
        
        if is_revision:
            base_confidence += 0.03  # Revisions typically improve confidence
        
        return min(0.95, max(0.5, base_confidence))
    
    def _generate_next_suggestion(
        self,
        current_type: ThoughtStepType,
        current_thought: str,
        previous_thoughts: list[ThoughtData]
    ) -> str:
        """Generate suggestion for the next thought."""
        thought_lower = current_thought.lower()
        
        suggestions = {
            ThoughtStepType.PROBLEM_DECOMPOSITION: "Identify key components and constraints of the problem",
            ThoughtStepType.HYPOTHESIS_FORMATION: "Formulate testable hypotheses based on the decomposition",
            ThoughtStepType.EVIDENCE_GATHERING: "Gather evidence to support or refute the hypotheses",
            ThoughtStepType.LOGICAL_DEDUCTION: "Apply logical reasoning to derive conclusions from evidence",
            ThoughtStepType.PATTERN_RECOGNITION: "Identify patterns and relationships in the data",
            ThoughtStepType.ASSUMPTION_TESTING: "Test and validate key assumptions",
            ThoughtStepType.SYNTHESIS: "Integrate insights from previous steps",
            ThoughtStepType.VALIDATION: "Validate the reasoning chain for consistency",
            ThoughtStepType.CONCLUSION: "Synthesize final conclusions and recommendations",
        }
        
        # Context-aware suggestions
        if "problem" in thought_lower and "complex" in thought_lower:
            return "Break down the complexity into manageable sub-problems"
        
        if "hypothesis" in thought_lower and not any("evidence" in t.content.lower() for t in previous_thoughts):
            return "Identify what evidence would support or refute this hypothesis"
        
        if "evidence" in thought_lower and "pattern" not in thought_lower:
            return "Look for patterns or trends in the evidence gathered"
        
        return suggestions.get(current_type, "Continue developing the reasoning chain")
    
    def _calculate_progress(
        self,
        thought_number: int,
        total_thoughts: int,
        actual_count: int,
        branch_id: Optional[str]
    ) -> Dict[str, Any]:
        """Calculate progress metrics."""
        percent_complete = round((thought_number / total_thoughts) * 100)
        
        return {
            "currentChainLength": actual_count,
            "percentComplete": percent_complete,
            "thoughtsRemaining": max(0, total_thoughts - thought_number),
            "onTrack": thought_number <= total_thoughts,
            "branch": branch_id is not None,
        }