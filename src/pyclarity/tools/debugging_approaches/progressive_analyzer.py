"""
Progressive Debugging Approaches Analyzer.

This version supports step-by-step debugging with session state persistence,
allowing iterative hypothesis testing and validation.
"""

import logging
import uuid
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, ConfigDict

from pyclarity.db.base import BaseSessionStore, SessionData
from pyclarity.db.debugging_store import BaseDebuggingStore, DebuggingData, DebuggingHypothesis

logger = logging.getLogger(__name__)


class ProgressiveDebuggingRequest(BaseModel):
    """Request for progressive debugging step."""
    
    session_id: Optional[str] = Field(default=None, description="Session ID for continuing existing session")
    step_number: int = Field(1, description="Current step in debugging process")
    debugging_type: str = Field("systematic", description="Type: systematic, rubber_duck, bisection, pattern_matching")
    
    # Problem description
    issue_description: str = Field(..., description="Description of the issue")
    error_message: Optional[str] = Field(None, description="Error message if available")
    stack_trace: Optional[str] = Field(None, description="Stack trace if available")
    
    # Current hypothesis
    hypothesis: Optional[str] = Field(None, description="Current hypothesis about the issue")
    evidence: List[str] = Field(default_factory=list, description="Evidence gathered so far")
    test_plan: Optional[str] = Field(None, description="How to test the hypothesis")
    
    # For continuing sessions
    previous_hypotheses: List[int] = Field(default_factory=list, description="IDs of previous hypotheses")
    build_on_previous: bool = Field(True, description="Whether to consider previous findings")
    
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    def __init__(self, **data):
        super().__init__(**data)
        if self.session_id is None:
            self.session_id = str(uuid.uuid4())


class ProgressiveDebuggingResponse(BaseModel):
    """Response for progressive debugging step."""
    
    session_id: str = Field(..., description="Session ID", alias="sessionId")
    step_id: Optional[int] = Field(None, description="Database ID of this step", alias="stepId")
    step_number: int = Field(..., description="Step number", alias="stepNumber")
    debugging_type: str = Field(..., description="Debugging approach used", alias="debuggingType")
    status: str = Field("success", description="Status of the operation")
    
    # Current state
    current_hypothesis: Optional[DebuggingHypothesis] = Field(None, description="Current hypothesis", alias="currentHypothesis")
    evidence_gathered: List[str] = Field(default_factory=list, description="All evidence so far", alias="evidenceGathered")
    insights: List[str] = Field(default_factory=list, description="New insights discovered")
    
    # Next steps
    next_steps: List[str] = Field(default_factory=list, description="Suggested next actions", alias="nextSteps")
    tests_to_run: List[Dict[str, str]] = Field(default_factory=list, description="Suggested tests", alias="testsToRun")
    
    # Resolution
    root_cause_found: bool = Field(False, description="Whether root cause identified", alias="rootCauseFound")
    root_cause: Optional[str] = Field(None, description="Identified root cause", alias="rootCause")
    solution: Optional[str] = Field(None, description="Proposed solution")
    
    # Progress
    confidence: float = Field(0.5, description="Confidence in current direction")
    hypotheses_tested: int = Field(0, description="Number of hypotheses tested", alias="hypothesesTested")
    estimated_steps_remaining: Optional[int] = Field(None, description="Estimated steps to solution", alias="estimatedStepsRemaining")
    
    error: Optional[str] = Field(None, description="Error message if failed")
    
    model_config = ConfigDict(populate_by_name=True)


class ProgressiveDebuggingAnalyzer:
    """Progressive debugging analyzer with session state."""
    
    def __init__(
        self,
        session_store: BaseSessionStore,
        debug_store: BaseDebuggingStore,
    ):
        """Initialize with database stores."""
        self.session_store = session_store
        self.debug_store = debug_store
        self.tool_name = "Debugging Approaches (Progressive)"
        self.version = "3.0.0"
    
    async def analyze_issue(
        self, request: ProgressiveDebuggingRequest
    ) -> ProgressiveDebuggingResponse:
        """Analyze debugging issue progressively."""
        try:
            # Ensure session exists
            session = await self._ensure_session(request.session_id)
            
            # Get previous debugging steps
            previous_steps = await self.debug_store.get_session_steps(request.session_id)
            
            # Create hypothesis if provided
            hypothesis = None
            if request.hypothesis:
                hypothesis = DebuggingHypothesis(
                    statement=request.hypothesis,
                    evidence_for=request.evidence,
                    test_method=request.test_plan or "Direct testing",
                    confidence=self._calculate_hypothesis_confidence(request.evidence)
                )
            
            # Apply debugging approach
            if request.debugging_type == "systematic":
                debug_data = await self._systematic_debugging(request, hypothesis, previous_steps)
            elif request.debugging_type == "rubber_duck":
                debug_data = await self._rubber_duck_debugging(request, hypothesis, previous_steps)
            elif request.debugging_type == "bisection":
                debug_data = await self._bisection_debugging(request, hypothesis, previous_steps)
            elif request.debugging_type == "pattern_matching":
                debug_data = await self._pattern_matching_debugging(request, hypothesis, previous_steps)
            else:
                debug_data = await self._systematic_debugging(request, hypothesis, previous_steps)
            
            # Save debugging step
            saved_step = await self.debug_store.save_debugging_step(debug_data)
            
            # Update session
            await self.session_store.update_session(
                request.session_id,
                {"updated_at": debug_data.created_at}
            )
            
            # Generate next steps based on findings
            next_steps, tests_to_run = self._generate_next_steps(
                debug_data, previous_steps, request.debugging_type
            )
            
            # Estimate remaining steps
            estimated_remaining = self._estimate_steps_remaining(
                len(previous_steps) + 1,
                debug_data.confidence,
                bool(debug_data.root_cause)
            )
            
            return ProgressiveDebuggingResponse(
                session_id=request.session_id,
                step_id=saved_step.id,
                step_number=request.step_number,
                debugging_type=request.debugging_type,
                status="success",
                current_hypothesis=hypothesis,
                evidence_gathered=debug_data.evidence_gathered,
                insights=debug_data.insights,
                next_steps=next_steps,
                tests_to_run=tests_to_run,
                root_cause_found=bool(debug_data.root_cause),
                root_cause=debug_data.root_cause,
                solution=debug_data.solution,
                confidence=debug_data.confidence,
                hypotheses_tested=len([s for s in previous_steps if s.hypothesis]),
                estimated_steps_remaining=estimated_remaining,
            )
            
        except Exception as e:
            logger.error(f"Error in debugging analysis: {e}")
            return ProgressiveDebuggingResponse(
                session_id=request.session_id or "error",
                step_id=None,
                step_number=request.step_number,
                debugging_type=request.debugging_type,
                status="error",
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
    
    async def _systematic_debugging(
        self,
        request: ProgressiveDebuggingRequest,
        hypothesis: Optional[DebuggingHypothesis],
        previous_steps: List[DebuggingData]
    ) -> DebuggingData:
        """Apply systematic debugging approach."""
        insights = []
        
        # Analyze error pattern
        if request.error_message:
            insights.append(f"Error pattern suggests: {self._analyze_error_pattern(request.error_message)}")
        
        # Build on previous findings
        if previous_steps and request.build_on_previous:
            insights.append(f"Previous steps eliminated {len(previous_steps)} possibilities")
        
        # Systematic next steps
        next_steps = [
            "Verify input data validity",
            "Check system state at error point",
            "Trace execution path",
            "Examine related components"
        ]
        
        # Adjust confidence based on evidence
        confidence = 0.3 + (len(request.evidence) * 0.1)
        confidence = min(0.9, confidence)
        
        return DebuggingData(
            session_id=request.session_id,
            step_number=request.step_number,
            debugging_type="systematic",
            issue_description=request.issue_description,
            error_message=request.error_message,
            stack_trace=request.stack_trace,
            hypothesis=hypothesis,
            evidence_gathered=request.evidence,
            insights=insights,
            next_steps=next_steps[:3],  # Top 3 next steps
            confidence=confidence,
            metadata=request.metadata
        )
    
    async def _rubber_duck_debugging(
        self,
        request: ProgressiveDebuggingRequest,
        hypothesis: Optional[DebuggingHypothesis],
        previous_steps: List[DebuggingData]
    ) -> DebuggingData:
        """Apply rubber duck debugging approach."""
        insights = [
            "Breaking down the problem reveals hidden assumptions",
            "The issue might be simpler than initially thought"
        ]
        
        # Analyze problem statement for clarity
        if "should" in request.issue_description.lower():
            insights.append("Expected behavior needs clearer definition")
        
        next_steps = [
            "Explain the problem step-by-step aloud",
            "Write down exact vs expected behavior",
            "Question each assumption",
            "Look for the simplest explanation"
        ]
        
        return DebuggingData(
            session_id=request.session_id,
            step_number=request.step_number,
            debugging_type="rubber_duck",
            issue_description=request.issue_description,
            error_message=request.error_message,
            hypothesis=hypothesis,
            evidence_gathered=request.evidence,
            insights=insights,
            next_steps=next_steps[:3],
            confidence=0.6,
            metadata=request.metadata
        )
    
    async def _bisection_debugging(
        self,
        request: ProgressiveDebuggingRequest,
        hypothesis: Optional[DebuggingHypothesis],
        previous_steps: List[DebuggingData]
    ) -> DebuggingData:
        """Apply bisection debugging approach."""
        insights = [
            "Binary search can isolate the problem quickly",
            f"Current search space: {2 ** max(5 - request.step_number, 1)} possibilities"
        ]
        
        next_steps = [
            "Test at the midpoint of suspected range",
            "Eliminate half of the search space",
            "Narrow down to specific component",
            "Repeat until isolated"
        ]
        
        # Higher confidence as we narrow down
        confidence = min(0.9, 0.5 + (request.step_number * 0.1))
        
        return DebuggingData(
            session_id=request.session_id,
            step_number=request.step_number,
            debugging_type="bisection",
            issue_description=request.issue_description,
            error_message=request.error_message,
            hypothesis=hypothesis,
            evidence_gathered=request.evidence,
            insights=insights,
            next_steps=next_steps[:2],
            confidence=confidence,
            metadata=request.metadata
        )
    
    async def _pattern_matching_debugging(
        self,
        request: ProgressiveDebuggingRequest,
        hypothesis: Optional[DebuggingHypothesis],
        previous_steps: List[DebuggingData]
    ) -> DebuggingData:
        """Apply pattern matching debugging approach."""
        # Look for common patterns
        patterns = self._identify_error_patterns(request.error_message, request.stack_trace)
        
        insights = [
            f"Error pattern matches: {patterns[0] if patterns else 'No clear pattern'}",
            "Similar issues often have similar root causes"
        ]
        
        if patterns:
            insights.append(f"Confidence boost from pattern recognition")
        
        next_steps = [
            "Search for similar past issues",
            "Apply known solutions for this pattern",
            "Verify pattern-specific root causes",
            "Test pattern-based hypothesis"
        ]
        
        # Higher confidence if pattern matched
        confidence = 0.7 if patterns else 0.4
        
        return DebuggingData(
            session_id=request.session_id,
            step_number=request.step_number,
            debugging_type="pattern_matching",
            issue_description=request.issue_description,
            error_message=request.error_message,
            stack_trace=request.stack_trace,
            hypothesis=hypothesis,
            evidence_gathered=request.evidence,
            insights=insights,
            next_steps=next_steps[:3],
            confidence=confidence,
            metadata=request.metadata
        )
    
    def _calculate_hypothesis_confidence(self, evidence: List[str]) -> float:
        """Calculate confidence based on evidence."""
        base_confidence = 0.5
        evidence_boost = len(evidence) * 0.1
        return min(0.95, base_confidence + evidence_boost)
    
    def _analyze_error_pattern(self, error_message: str) -> str:
        """Analyze error message for patterns."""
        error_lower = error_message.lower()
        
        if "null" in error_lower or "none" in error_lower:
            return "Null reference or uninitialized variable"
        elif "index" in error_lower or "bounds" in error_lower:
            return "Array/collection bounds issue"
        elif "connection" in error_lower or "timeout" in error_lower:
            return "Network or connectivity issue"
        elif "permission" in error_lower or "denied" in error_lower:
            return "Authorization or permissions issue"
        elif "memory" in error_lower or "heap" in error_lower:
            return "Memory allocation issue"
        else:
            return "Custom application logic error"
    
    def _identify_error_patterns(
        self, 
        error_message: Optional[str], 
        stack_trace: Optional[str]
    ) -> List[str]:
        """Identify common error patterns."""
        patterns = []
        
        if error_message:
            pattern = self._analyze_error_pattern(error_message)
            patterns.append(pattern)
        
        if stack_trace and "recursive" in stack_trace.lower():
            patterns.append("Infinite recursion detected")
        
        return patterns
    
    def _generate_next_steps(
        self,
        current_step: DebuggingData,
        previous_steps: List[DebuggingData],
        debugging_type: str
    ) -> tuple[List[str], List[Dict[str, str]]]:
        """Generate next debugging steps and tests."""
        next_steps = current_step.next_steps.copy()
        
        # Add specific steps based on confidence
        if current_step.confidence < 0.5:
            next_steps.append("Consider alternative debugging approach")
        elif current_step.confidence > 0.8:
            next_steps.insert(0, "Focus on current hypothesis validation")
        
        # Generate test suggestions
        tests = []
        if current_step.hypothesis:
            tests.append({
                "name": "Hypothesis validation test",
                "description": f"Test: {current_step.hypothesis.statement}",
                "method": current_step.hypothesis.test_method or "Direct testing"
            })
        
        if debugging_type == "bisection":
            tests.append({
                "name": "Binary search test",
                "description": "Test at midpoint of current range",
                "method": "Conditional breakpoint or logging"
            })
        
        return next_steps, tests
    
    def _estimate_steps_remaining(
        self,
        steps_taken: int,
        confidence: float,
        root_cause_found: bool
    ) -> Optional[int]:
        """Estimate remaining debugging steps."""
        if root_cause_found:
            return 0
        
        if confidence > 0.8:
            return 1  # Very close
        elif confidence > 0.6:
            return 2 + int((1 - confidence) * 3)
        elif confidence > 0.4:
            return 3 + int((1 - confidence) * 5)
        else:
            # Low confidence, hard to estimate
            return None