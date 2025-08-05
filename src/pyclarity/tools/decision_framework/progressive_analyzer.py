"""
Progressive Decision Framework Analyzer

Enables step-by-step decision analysis with criteria evaluation,
alternative assessment, and trade-off analysis across sessions.
"""

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from pyclarity.db.base import BaseSessionStore, SessionData
from pyclarity.db.decision_store import (
    BaseDecisionStore,
    DecisionData,
    DecisionCriterion,
    DecisionAlternative,
    TradeOff,
)
from pyclarity.tools.decision_framework.models import (
    DecisionType,
    CriterionWeight,
    DecisionComplexity,
)


class ProgressiveDecisionRequest(BaseModel):
    """Request for progressive decision analysis."""
    
    session_id: Optional[str] = Field(None, description="Session ID for continuing analysis")
    step_number: int = Field(1, description="Current step in decision process")
    decision_type: DecisionType = Field(..., description="Type of decision")
    decision_statement: str = Field(..., description="What decision needs to be made")
    
    # Current step focus
    step_focus: str = Field(
        "criteria",
        description="Focus of this step: criteria, alternatives, evaluation, trade-offs, recommendation"
    )
    
    # Step-specific inputs
    criteria: List[Dict[str, Any]] = Field(default_factory=list, description="Decision criteria")
    alternatives: List[Dict[str, Any]] = Field(default_factory=list, description="Decision alternatives")
    evaluations: Dict[str, Dict[str, float]] = Field(default_factory=dict, description="Alternative evaluations")
    trade_offs: List[Dict[str, Any]] = Field(default_factory=list, description="Trade-offs identified")
    
    # Context and constraints
    context: Optional[str] = Field(None, description="Decision context")
    constraints: List[str] = Field(default_factory=list, description="Decision constraints")
    stakeholders: List[str] = Field(default_factory=list, description="Key stakeholders")
    
    # Process settings
    decision_complexity: DecisionComplexity = Field(DecisionComplexity.MODERATE)
    require_consensus: bool = Field(False, description="Whether consensus is required")
    time_pressure: Optional[str] = Field(None, description="Time constraints")
    
    # Building on previous
    build_on_previous: bool = Field(True, description="Build on previous analysis")
    revise_step: Optional[int] = Field(None, description="Step number to revise")
    
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ProgressiveDecisionResponse(BaseModel):
    """Response from progressive decision analysis."""
    
    # Core response
    status: str = Field(..., description="Status of the analysis step")
    session_id: str = Field(..., description="Session identifier")
    step_id: int = Field(..., description="Database ID of this step")
    step_number: int = Field(..., description="Sequential step number")
    
    # Step results
    step_focus: str = Field(..., description="What this step focused on")
    step_summary: str = Field(..., description="Summary of step results")
    
    # Cumulative analysis
    criteria_defined: List[Dict[str, Any]] = Field(default_factory=list)
    alternatives_identified: List[Dict[str, Any]] = Field(default_factory=list)
    evaluations_complete: bool = Field(False)
    trade_offs_analyzed: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Recommendations (when ready)
    recommendation: Optional[Dict[str, Any]] = Field(None)
    confidence_score: float = Field(0.0, description="Confidence in recommendation")
    sensitivity_analysis: Optional[Dict[str, Any]] = Field(None)
    
    # Next steps
    next_step_suggested: Optional[str] = Field(None)
    missing_information: List[str] = Field(default_factory=list)
    questions_to_consider: List[str] = Field(default_factory=list)
    
    # Progress
    decision_readiness: float = Field(0.0, description="0-1 score of decision readiness")
    steps_completed: List[str] = Field(default_factory=list)
    
    # Error handling
    error: Optional[str] = Field(None)
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "session_id": "decision-123",
                "step_focus": "criteria",
                "step_summary": "Defined 5 key decision criteria",
                "criteria_defined": [{"name": "Cost", "weight": 0.3}],
                "decision_readiness": 0.2,
                "next_step_suggested": "alternatives"
            }
        }


class ProgressiveDecisionAnalyzer:
    """Progressive decision analysis with session management."""
    
    def __init__(
        self,
        session_store: BaseSessionStore,
        decision_store: BaseDecisionStore,
    ):
        """Initialize with required stores."""
        self.session_store = session_store
        self.decision_store = decision_store
    
    async def analyze_decision(
        self, request: ProgressiveDecisionRequest
    ) -> ProgressiveDecisionResponse:
        """Process a decision analysis step."""
        try:
            # Get or create session
            session = await self._get_or_create_session(request)
            
            # Process based on step focus
            step_result = await self._process_step(session.session_id, request)
            
            # Save decision data
            decision_data = await self._create_decision_data(session.session_id, request, step_result)
            saved_data = await self.decision_store.save_decision_step(decision_data)
            
            # Get cumulative state
            all_criteria = await self._get_all_criteria(session.session_id)
            all_alternatives = await self._get_all_alternatives(session.session_id)
            all_evaluations = await self._check_evaluations_complete(session.session_id)
            all_trade_offs = await self._get_all_trade_offs(session.session_id)
            
            # Calculate decision readiness
            readiness = self._calculate_readiness(
                len(all_criteria),
                len(all_alternatives),
                all_evaluations,
                len(all_trade_offs)
            )
            
            # Get recommendation if ready
            recommendation = None
            confidence = 0.0
            if readiness >= 0.8:
                recommendation, confidence = await self._generate_recommendation(session.session_id)
            
            # Determine next step
            next_step = self._suggest_next_step(
                request.step_focus,
                len(all_criteria),
                len(all_alternatives),
                all_evaluations
            )
            
            # Identify missing information
            missing = self._identify_missing_info(
                all_criteria,
                all_alternatives,
                all_evaluations
            )
            
            # Generate questions
            questions = self._generate_questions(request.step_focus, next_step)
            
            # Track completed steps
            completed_steps = await self._get_completed_steps(session.session_id)
            
            return ProgressiveDecisionResponse(
                status="success",
                session_id=session.session_id,
                step_id=saved_data.id,
                step_number=saved_data.step_number,
                step_focus=request.step_focus,
                step_summary=step_result.get("summary", ""),
                criteria_defined=all_criteria,
                alternatives_identified=all_alternatives,
                evaluations_complete=all_evaluations,
                trade_offs_analyzed=all_trade_offs,
                recommendation=recommendation,
                confidence_score=confidence,
                sensitivity_analysis=step_result.get("sensitivity"),
                next_step_suggested=next_step,
                missing_information=missing,
                questions_to_consider=questions,
                decision_readiness=readiness,
                steps_completed=completed_steps,
            )
            
        except Exception as e:
            return ProgressiveDecisionResponse(
                status="error",
                session_id=request.session_id or str(uuid.uuid4()),
                step_id=0,
                step_number=request.step_number,
                step_focus=request.step_focus,
                step_summary="",
                decision_readiness=0.0,
                error=str(e),
            )
    
    async def _get_or_create_session(
        self, request: ProgressiveDecisionRequest
    ) -> SessionData:
        """Get existing session or create new one."""
        if request.session_id:
            session = await self.session_store.get_session(request.session_id)
            if session:
                return session
        
        # Create new session
        session_data = SessionData(
            session_id=request.session_id or str(uuid.uuid4()),
            tool_name="Decision Framework",
            created_at=datetime.now(timezone.utc),
            metadata={
                "decision_statement": request.decision_statement,
                "decision_type": request.decision_type.value,
                "complexity": request.decision_complexity.value,
            }
        )
        
        return await self.session_store.create_session(session_data)
    
    async def _process_step(
        self, session_id: str, request: ProgressiveDecisionRequest
    ) -> Dict[str, Any]:
        """Process the specific step focus."""
        if request.step_focus == "criteria":
            return await self._process_criteria_step(request)
        elif request.step_focus == "alternatives":
            return await self._process_alternatives_step(request)
        elif request.step_focus == "evaluation":
            return await self._process_evaluation_step(session_id, request)
        elif request.step_focus == "trade-offs":
            return await self._process_tradeoffs_step(session_id, request)
        elif request.step_focus == "recommendation":
            return await self._process_recommendation_step(session_id, request)
        else:
            return {"summary": f"Processed {request.step_focus} step"}
    
    async def _process_criteria_step(self, request: ProgressiveDecisionRequest) -> Dict[str, Any]:
        """Process criteria definition step."""
        criteria_count = len(request.criteria)
        
        # Validate criteria weights
        if criteria_count > 0:
            total_weight = sum(c.get("weight", 0) for c in request.criteria)
            if abs(total_weight - 1.0) > 0.01:  # Allow small floating point errors
                # Normalize weights
                for c in request.criteria:
                    c["weight"] = c.get("weight", 0) / total_weight if total_weight > 0 else 1.0 / criteria_count
        
        return {
            "summary": f"Defined {criteria_count} decision criteria with normalized weights",
            "criteria": request.criteria,
        }
    
    async def _process_alternatives_step(self, request: ProgressiveDecisionRequest) -> Dict[str, Any]:
        """Process alternatives identification step."""
        alt_count = len(request.alternatives)
        
        # Analyze alternative diversity
        diversity_score = min(1.0, alt_count / 5.0)  # Assume 5 alternatives is good diversity
        
        return {
            "summary": f"Identified {alt_count} decision alternatives",
            "alternatives": request.alternatives,
            "diversity_score": diversity_score,
        }
    
    async def _process_evaluation_step(
        self, session_id: str, request: ProgressiveDecisionRequest
    ) -> Dict[str, Any]:
        """Process alternative evaluation step."""
        # Get criteria for validation
        criteria = await self._get_all_criteria(session_id)
        
        # Validate evaluations
        missing_evals = []
        for alt_name, evals in request.evaluations.items():
            for criterion in criteria:
                if criterion["name"] not in evals:
                    missing_evals.append(f"{alt_name} - {criterion['name']}")
        
        completeness = 1.0 - (len(missing_evals) / max(1, len(criteria) * len(request.evaluations)))
        
        return {
            "summary": f"Evaluated alternatives with {completeness:.0%} completeness",
            "evaluations": request.evaluations,
            "missing_evaluations": missing_evals,
            "completeness": completeness,
        }
    
    async def _process_tradeoffs_step(
        self, session_id: str, request: ProgressiveDecisionRequest
    ) -> Dict[str, Any]:
        """Process trade-offs analysis step."""
        # Analyze trade-offs
        trade_off_count = len(request.trade_offs)
        
        # Simple sensitivity analysis
        sensitivity = {
            "high_impact_criteria": [],
            "low_impact_criteria": [],
        }
        
        # Would do actual sensitivity analysis here
        criteria = await self._get_all_criteria(session_id)
        for criterion in criteria:
            if criterion.get("weight", 0) > 0.3:
                sensitivity["high_impact_criteria"].append(criterion["name"])
            elif criterion.get("weight", 0) < 0.1:
                sensitivity["low_impact_criteria"].append(criterion["name"])
        
        return {
            "summary": f"Analyzed {trade_off_count} key trade-offs",
            "trade_offs": request.trade_offs,
            "sensitivity": sensitivity,
        }
    
    async def _process_recommendation_step(
        self, session_id: str, request: ProgressiveDecisionRequest
    ) -> Dict[str, Any]:
        """Process recommendation generation step."""
        # Generate recommendation based on all data
        recommendation, confidence = await self._generate_recommendation(session_id)
        
        return {
            "summary": f"Generated recommendation with {confidence:.0%} confidence",
            "recommendation": recommendation,
            "confidence": confidence,
        }
    
    async def _create_decision_data(
        self,
        session_id: str,
        request: ProgressiveDecisionRequest,
        step_result: Dict[str, Any]
    ) -> DecisionData:
        """Create decision data for storage."""
        # Convert criteria
        criteria = []
        for c in request.criteria:
            criteria.append(DecisionCriterion(
                name=c.get("name", ""),
                description=c.get("description", ""),
                weight=c.get("weight", 0.0),
                criterion_type=c.get("type", "quantitative"),
                measurement_scale=c.get("scale", "1-10"),
            ))
        
        # Convert alternatives
        alternatives = []
        for a in request.alternatives:
            alternatives.append(DecisionAlternative(
                name=a.get("name", ""),
                description=a.get("description", ""),
                pros=a.get("pros", []),
                cons=a.get("cons", []),
                risks=a.get("risks", []),
                cost_estimate=a.get("cost"),
                time_estimate=a.get("time"),
                scores={},  # Will be filled from evaluations
            ))
        
        # Add evaluation scores
        for alt in alternatives:
            if alt.name in request.evaluations:
                alt.scores = request.evaluations[alt.name]
        
        # Convert trade-offs
        trade_offs = []
        for t in request.trade_offs:
            trade_offs.append(TradeOff(
                option_a=t.get("option_a", ""),
                option_b=t.get("option_b", ""),
                trade_off_description=t.get("description", ""),
                impact_analysis=t.get("impact", {}),
            ))
        
        return DecisionData(
            session_id=session_id,
            step_number=request.step_number,
            decision_type=request.decision_type,
            decision_statement=request.decision_statement,
            context=request.context,
            criteria=criteria,
            alternatives=alternatives,
            trade_offs=trade_offs,
            recommendation=step_result.get("recommendation"),
            confidence_score=step_result.get("confidence", 0.0),
            sensitivity_analysis=step_result.get("sensitivity", {}),
            metadata=request.metadata,
            created_at=datetime.now(timezone.utc),
        )
    
    async def _get_all_criteria(self, session_id: str) -> List[Dict[str, Any]]:
        """Get all criteria defined in session."""
        steps = await self.decision_store.get_session_steps(session_id)
        
        criteria = {}
        for step in steps:
            for criterion in step.criteria:
                criteria[criterion.name] = {
                    "name": criterion.name,
                    "description": criterion.description,
                    "weight": criterion.weight,
                    "type": criterion.criterion_type,
                }
        
        return list(criteria.values())
    
    async def _get_all_alternatives(self, session_id: str) -> List[Dict[str, Any]]:
        """Get all alternatives identified in session."""
        steps = await self.decision_store.get_session_steps(session_id)
        
        alternatives = {}
        for step in steps:
            for alt in step.alternatives:
                alternatives[alt.name] = {
                    "name": alt.name,
                    "description": alt.description,
                    "pros": alt.pros,
                    "cons": alt.cons,
                }
        
        return list(alternatives.values())
    
    async def _check_evaluations_complete(self, session_id: str) -> bool:
        """Check if all evaluations are complete."""
        criteria = await self._get_all_criteria(session_id)
        alternatives = await self._get_all_alternatives(session_id)
        
        if not criteria or not alternatives:
            return False
        
        steps = await self.decision_store.get_session_steps(session_id)
        
        # Check if we have scores for all combinations
        required_scores = len(criteria) * len(alternatives)
        actual_scores = 0
        
        for step in steps:
            for alt in step.alternatives:
                actual_scores += len(alt.scores)
        
        return actual_scores >= required_scores
    
    async def _get_all_trade_offs(self, session_id: str) -> List[Dict[str, Any]]:
        """Get all trade-offs analyzed in session."""
        steps = await self.decision_store.get_session_steps(session_id)
        
        trade_offs = []
        for step in steps:
            for t in step.trade_offs:
                trade_offs.append({
                    "option_a": t.option_a,
                    "option_b": t.option_b,
                    "description": t.trade_off_description,
                    "impact": t.impact_analysis,
                })
        
        return trade_offs
    
    def _calculate_readiness(
        self,
        criteria_count: int,
        alternatives_count: int,
        evaluations_complete: bool,
        trade_offs_count: int
    ) -> float:
        """Calculate decision readiness score."""
        readiness = 0.0
        
        # Criteria (25%)
        if criteria_count >= 3:
            readiness += 0.25
        elif criteria_count > 0:
            readiness += 0.25 * (criteria_count / 3)
        
        # Alternatives (25%)
        if alternatives_count >= 3:
            readiness += 0.25
        elif alternatives_count > 0:
            readiness += 0.25 * (alternatives_count / 3)
        
        # Evaluations (30%)
        if evaluations_complete:
            readiness += 0.30
        
        # Trade-offs (20%)
        if trade_offs_count >= 2:
            readiness += 0.20
        elif trade_offs_count > 0:
            readiness += 0.20 * (trade_offs_count / 2)
        
        return readiness
    
    async def _generate_recommendation(
        self, session_id: str
    ) -> tuple[Optional[Dict[str, Any]], float]:
        """Generate recommendation based on analysis."""
        # Get all data
        criteria = await self._get_all_criteria(session_id)
        alternatives = await self._get_all_alternatives(session_id)
        
        if not criteria or not alternatives:
            return None, 0.0
        
        # Calculate weighted scores
        steps = await self.decision_store.get_session_steps(session_id)
        
        alternative_scores = {}
        for step in steps:
            for alt in step.alternatives:
                if alt.scores:
                    weighted_score = 0.0
                    for criterion in criteria:
                        score = alt.scores.get(criterion["name"], 0)
                        weight = criterion["weight"]
                        weighted_score += score * weight
                    
                    alternative_scores[alt.name] = weighted_score
        
        if not alternative_scores:
            return None, 0.0
        
        # Find best alternative
        best_alt = max(alternative_scores.items(), key=lambda x: x[1])
        
        # Calculate confidence based on score separation
        scores = list(alternative_scores.values())
        if len(scores) > 1:
            scores.sort(reverse=True)
            separation = (scores[0] - scores[1]) / max(scores[0], 1)
            confidence = min(0.95, 0.5 + separation)
        else:
            confidence = 0.7
        
        recommendation = {
            "recommended_alternative": best_alt[0],
            "score": best_alt[1],
            "rationale": f"Highest weighted score across all criteria",
            "runner_up": None,
        }
        
        # Add runner up if exists
        if len(alternative_scores) > 1:
            sorted_alts = sorted(alternative_scores.items(), key=lambda x: x[1], reverse=True)
            recommendation["runner_up"] = {
                "name": sorted_alts[1][0],
                "score": sorted_alts[1][1],
            }
        
        return recommendation, confidence
    
    def _suggest_next_step(
        self,
        current_focus: str,
        criteria_count: int,
        alternatives_count: int,
        evaluations_complete: bool
    ) -> Optional[str]:
        """Suggest next step in process."""
        if current_focus == "criteria" and criteria_count == 0:
            return "criteria"  # Need to define criteria first
        elif criteria_count > 0 and alternatives_count == 0:
            return "alternatives"
        elif criteria_count > 0 and alternatives_count > 0 and not evaluations_complete:
            return "evaluation"
        elif evaluations_complete:
            return "trade-offs"
        else:
            return "recommendation"
    
    def _identify_missing_info(
        self,
        criteria: List[Dict[str, Any]],
        alternatives: List[Dict[str, Any]],
        evaluations_complete: bool
    ) -> List[str]:
        """Identify missing information."""
        missing = []
        
        if len(criteria) < 3:
            missing.append(f"Only {len(criteria)} criteria defined (recommend at least 3)")
        
        if len(alternatives) < 2:
            missing.append(f"Only {len(alternatives)} alternatives identified (need at least 2)")
        
        if not evaluations_complete and criteria and alternatives:
            missing.append("Alternative evaluations incomplete")
        
        # Check for criteria without weights
        for c in criteria:
            if c.get("weight", 0) == 0:
                missing.append(f"Criterion '{c['name']}' has no weight assigned")
        
        return missing
    
    def _generate_questions(self, current_focus: str, next_step: Optional[str]) -> List[str]:
        """Generate questions for consideration."""
        questions = []
        
        focus_questions = {
            "criteria": [
                "What factors are most important for this decision?",
                "How should we weight each criterion?",
                "Are there any constraints we haven't considered?"
            ],
            "alternatives": [
                "What are all possible options?",
                "Are there creative alternatives we haven't thought of?",
                "Can we combine elements of different alternatives?"
            ],
            "evaluation": [
                "How does each alternative perform on each criterion?",
                "Do we have data to support our evaluations?",
                "Should we gather more information before scoring?"
            ],
            "trade-offs": [
                "What are we giving up with each choice?",
                "Which trade-offs are acceptable?",
                "How sensitive is our decision to weight changes?"
            ],
            "recommendation": [
                "Does the recommendation align with our goals?",
                "What could change our decision?",
                "How do we implement the chosen alternative?"
            ],
        }
        
        if next_step and next_step in focus_questions:
            questions.extend(focus_questions[next_step][:2])
        
        return questions
    
    async def _get_completed_steps(self, session_id: str) -> List[str]:
        """Get list of completed step types."""
        steps = await self.decision_store.get_session_steps(session_id)
        
        completed = set()
        for step in steps:
            if step.criteria:
                completed.add("criteria")
            if step.alternatives:
                completed.add("alternatives")
            if any(alt.scores for alt in step.alternatives):
                completed.add("evaluation")
            if step.trade_offs:
                completed.add("trade-offs")
            if step.recommendation:
                completed.add("recommendation")
        
        return list(completed)