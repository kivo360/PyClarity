"""
Progressive Scientific Method Analyzer

Guides systematic scientific inquiry through hypothesis formation,
experimentation, and analysis with session-based progression.
"""

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from pyclarity.db.base import BaseSessionStore, SessionData
from pyclarity.db.scientific_store import (
    BaseScientificStore,
    ScientificData,
    Hypothesis,
    Experiment,
    Result,
    Conclusion,
)
from pyclarity.tools.scientific_method.models import (
    ScientificPhase,
    HypothesisType,
    ExperimentType,
    ConfidenceLevel,
)


class ProgressiveScientificRequest(BaseModel):
    """Request for progressive scientific method analysis."""
    
    session_id: Optional[str] = Field(None, description="Session ID for continuing research")
    step_number: int = Field(1, description="Current step in scientific process")
    phase: ScientificPhase = Field(..., description="Current phase of scientific method")
    
    # Research context
    research_question: str = Field(..., description="Primary research question")
    domain: str = Field(..., description="Research domain/field")
    context: Optional[str] = Field(None, description="Additional context")
    
    # Phase-specific inputs
    observations: List[str] = Field(default_factory=list, description="New observations")
    hypothesis: Optional[Dict[str, Any]] = Field(None, description="Hypothesis details")
    experiment_design: Optional[Dict[str, Any]] = Field(None, description="Experiment design")
    results: Optional[Dict[str, Any]] = Field(None, description="Experimental results")
    analysis: Optional[Dict[str, Any]] = Field(None, description="Data analysis")
    
    # Previous work
    previous_hypotheses: List[int] = Field(default_factory=list, description="Previous hypothesis IDs")
    previous_experiments: List[int] = Field(default_factory=list, description="Previous experiment IDs")
    build_on_previous: bool = Field(True, description="Build on previous findings")
    
    # Research settings
    rigor_level: str = Field("moderate", description="Level of scientific rigor")
    peer_review: bool = Field(False, description="Include peer review considerations")
    
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ProgressiveScientificResponse(BaseModel):
    """Response from progressive scientific method analysis."""
    
    # Core response
    status: str = Field(..., description="Status of scientific step")
    session_id: str = Field(..., description="Session identifier")
    step_id: int = Field(..., description="Database ID of this step")
    step_number: int = Field(..., description="Sequential step number")
    
    # Phase results
    phase: str = Field(..., description="Current phase")
    phase_summary: str = Field(..., description="Summary of phase results")
    
    # Scientific progress
    observations_count: int = Field(0, description="Total observations recorded")
    hypotheses_generated: List[Dict[str, Any]] = Field(default_factory=list)
    experiments_designed: List[Dict[str, Any]] = Field(default_factory=list)
    results_obtained: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Current hypothesis status
    active_hypothesis: Optional[Dict[str, Any]] = Field(None)
    hypothesis_confidence: float = Field(0.0, description="Confidence in hypothesis")
    supporting_evidence: List[str] = Field(default_factory=list)
    contradicting_evidence: List[str] = Field(default_factory=list)
    
    # Recommendations
    next_phase_suggested: Optional[ScientificPhase] = Field(None)
    next_actions: List[str] = Field(default_factory=list)
    required_resources: List[str] = Field(default_factory=list)
    
    # Quality indicators
    scientific_rigor_score: float = Field(0.0, description="0-1 score")
    reproducibility_score: float = Field(0.0, description="0-1 score")
    
    # Insights and conclusions
    key_findings: List[str] = Field(default_factory=list)
    preliminary_conclusions: List[str] = Field(default_factory=list)
    
    # Error handling
    error: Optional[str] = Field(None)
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "session_id": "sci-123",
                "phase": "hypothesis",
                "phase_summary": "Generated testable hypothesis",
                "active_hypothesis": {"statement": "X causes Y", "type": "causal"},
                "hypothesis_confidence": 0.7
            }
        }


class ProgressiveScientificAnalyzer:
    """Progressive scientific method with session management."""
    
    def __init__(
        self,
        session_store: BaseSessionStore,
        scientific_store: BaseScientificStore,
    ):
        """Initialize with required stores."""
        self.session_store = session_store
        self.scientific_store = scientific_store
    
    async def conduct_research(
        self, request: ProgressiveScientificRequest
    ) -> ProgressiveScientificResponse:
        """Conduct a step in scientific research."""
        try:
            # Get or create session
            session = await self._get_or_create_session(request)
            
            # Process based on phase
            phase_result = await self._process_phase(session.session_id, request)
            
            # Create and save scientific data
            scientific_data = await self._create_scientific_data(
                session.session_id,
                request,
                phase_result
            )
            saved_data = await self.scientific_store.save_research_step(scientific_data)
            
            # Get cumulative research state
            observations_count = await self._count_observations(session.session_id)
            all_hypotheses = await self._get_all_hypotheses(session.session_id)
            all_experiments = await self._get_all_experiments(session.session_id)
            all_results = await self._get_all_results(session.session_id)
            
            # Determine active hypothesis
            active_hypothesis = await self._get_active_hypothesis(session.session_id)
            hypothesis_confidence = 0.0
            supporting = []
            contradicting = []
            
            if active_hypothesis:
                hypothesis_confidence, supporting, contradicting = await self._evaluate_hypothesis(
                    session.session_id,
                    active_hypothesis
                )
            
            # Calculate quality scores
            rigor_score = self._calculate_rigor_score(
                observations_count,
                len(all_experiments),
                len(all_results),
                request.rigor_level
            )
            
            reproducibility_score = self._calculate_reproducibility_score(
                all_experiments,
                all_results
            )
            
            # Generate insights
            key_findings = await self._extract_key_findings(session.session_id)
            preliminary_conclusions = await self._generate_preliminary_conclusions(
                session.session_id,
                active_hypothesis
            )
            
            # Determine next phase
            next_phase = self._suggest_next_phase(
                request.phase,
                observations_count,
                len(all_hypotheses),
                len(all_experiments),
                len(all_results)
            )
            
            # Generate next actions
            next_actions = self._generate_next_actions(
                request.phase,
                next_phase,
                phase_result
            )
            
            # Identify required resources
            required_resources = self._identify_required_resources(
                next_phase,
                all_experiments
            )
            
            return ProgressiveScientificResponse(
                status="success",
                session_id=session.session_id,
                step_id=saved_data.id,
                step_number=saved_data.step_number,
                phase=request.phase.value,
                phase_summary=phase_result.get("summary", ""),
                observations_count=observations_count,
                hypotheses_generated=[self._hypothesis_to_dict(h) for h in all_hypotheses],
                experiments_designed=[self._experiment_to_dict(e) for e in all_experiments],
                results_obtained=[self._result_to_dict(r) for r in all_results],
                active_hypothesis=self._hypothesis_to_dict(active_hypothesis) if active_hypothesis else None,
                hypothesis_confidence=hypothesis_confidence,
                supporting_evidence=supporting,
                contradicting_evidence=contradicting,
                next_phase_suggested=next_phase,
                next_actions=next_actions,
                required_resources=required_resources,
                scientific_rigor_score=rigor_score,
                reproducibility_score=reproducibility_score,
                key_findings=key_findings,
                preliminary_conclusions=preliminary_conclusions,
            )
            
        except Exception as e:
            return ProgressiveScientificResponse(
                status="error",
                session_id=request.session_id or str(uuid.uuid4()),
                step_id=0,
                step_number=request.step_number,
                phase=request.phase.value,
                phase_summary="",
                error=str(e),
            )
    
    async def _get_or_create_session(
        self, request: ProgressiveScientificRequest
    ) -> SessionData:
        """Get existing session or create new one."""
        if request.session_id:
            session = await self.session_store.get_session(request.session_id)
            if session:
                return session
        
        # Create new session
        session_data = SessionData(
            session_id=request.session_id or str(uuid.uuid4()),
            tool_name="Scientific Method",
            created_at=datetime.now(timezone.utc),
            metadata={
                "research_question": request.research_question,
                "domain": request.domain,
                "rigor_level": request.rigor_level,
            }
        )
        
        return await self.session_store.create_session(session_data)
    
    async def _process_phase(
        self, session_id: str, request: ProgressiveScientificRequest
    ) -> Dict[str, Any]:
        """Process the specific scientific phase."""
        if request.phase == ScientificPhase.OBSERVATION:
            return await self._process_observation_phase(request)
        elif request.phase == ScientificPhase.QUESTION:
            return await self._process_question_phase(session_id, request)
        elif request.phase == ScientificPhase.HYPOTHESIS:
            return await self._process_hypothesis_phase(session_id, request)
        elif request.phase == ScientificPhase.EXPERIMENT:
            return await self._process_experiment_phase(session_id, request)
        elif request.phase == ScientificPhase.ANALYSIS:
            return await self._process_analysis_phase(session_id, request)
        elif request.phase == ScientificPhase.CONCLUSION:
            return await self._process_conclusion_phase(session_id, request)
        else:
            return {"summary": f"Processed {request.phase.value} phase"}
    
    async def _process_observation_phase(
        self, request: ProgressiveScientificRequest
    ) -> Dict[str, Any]:
        """Process observation collection."""
        obs_count = len(request.observations)
        
        # Categorize observations
        categories = {
            "quantitative": [],
            "qualitative": [],
            "anomalies": [],
        }
        
        for obs in request.observations:
            if any(char.isdigit() for char in obs):
                categories["quantitative"].append(obs)
            elif any(word in obs.lower() for word in ["unusual", "unexpected", "strange"]):
                categories["anomalies"].append(obs)
            else:
                categories["qualitative"].append(obs)
        
        return {
            "summary": f"Recorded {obs_count} new observations",
            "categories": categories,
            "patterns_detected": self._detect_observation_patterns(request.observations),
        }
    
    async def _process_question_phase(
        self, session_id: str, request: ProgressiveScientificRequest
    ) -> Dict[str, Any]:
        """Process research question refinement."""
        # Analyze question components
        question_type = self._classify_research_question(request.research_question)
        
        # Get related observations
        observations = await self._get_all_observations(session_id)
        
        # Suggest sub-questions
        sub_questions = self._generate_sub_questions(
            request.research_question,
            observations
        )
        
        return {
            "summary": f"Refined {question_type} research question",
            "question_type": question_type,
            "sub_questions": sub_questions,
            "variables_identified": self._identify_variables(request.research_question),
        }
    
    async def _process_hypothesis_phase(
        self, session_id: str, request: ProgressiveScientificRequest
    ) -> Dict[str, Any]:
        """Process hypothesis formation."""
        if not request.hypothesis:
            return {"summary": "No hypothesis provided", "error": "Hypothesis required"}
        
        # Validate hypothesis
        hypothesis_type = HypothesisType(request.hypothesis.get("type", "descriptive"))
        testability_score = self._assess_testability(request.hypothesis.get("statement", ""))
        
        # Check against previous hypotheses
        previous = []
        if request.build_on_previous and request.previous_hypotheses:
            previous = await self._get_hypotheses_by_ids(session_id, request.previous_hypotheses)
        
        # Generate predictions
        predictions = self._generate_predictions(
            request.hypothesis.get("statement", ""),
            hypothesis_type
        )
        
        return {
            "summary": f"Formulated {hypothesis_type.value} hypothesis",
            "hypothesis_type": hypothesis_type.value,
            "testability_score": testability_score,
            "predictions": predictions,
            "builds_on": [h.statement for h in previous] if previous else [],
        }
    
    async def _process_experiment_phase(
        self, session_id: str, request: ProgressiveScientificRequest
    ) -> Dict[str, Any]:
        """Process experiment design."""
        if not request.experiment_design:
            return {"summary": "No experiment design provided", "error": "Design required"}
        
        design = request.experiment_design
        
        # Analyze experiment quality
        control_quality = self._assess_controls(design.get("controls", []))
        variable_isolation = self._assess_variable_isolation(design.get("variables", {}))
        
        # Check resources
        resource_availability = self._check_resource_availability(
            design.get("required_resources", [])
        )
        
        # Generate protocol
        protocol = self._generate_experiment_protocol(design)
        
        return {
            "summary": f"Designed {design.get('type', 'standard')} experiment",
            "control_quality": control_quality,
            "variable_isolation": variable_isolation,
            "resource_availability": resource_availability,
            "protocol": protocol,
        }
    
    async def _process_analysis_phase(
        self, session_id: str, request: ProgressiveScientificRequest
    ) -> Dict[str, Any]:
        """Process data analysis."""
        if not request.results:
            return {"summary": "No results provided", "error": "Results required"}
        
        # Statistical analysis (simplified)
        stats = self._perform_statistical_analysis(request.results)
        
        # Pattern detection
        patterns = self._detect_result_patterns(request.results)
        
        # Significance assessment
        significance = self._assess_significance(stats, request.rigor_level)
        
        # Error analysis
        errors = self._analyze_errors(request.results)
        
        return {
            "summary": "Completed data analysis",
            "statistics": stats,
            "patterns": patterns,
            "significance": significance,
            "error_analysis": errors,
        }
    
    async def _process_conclusion_phase(
        self, session_id: str, request: ProgressiveScientificRequest
    ) -> Dict[str, Any]:
        """Process conclusion formation."""
        # Get all research data
        hypotheses = await self._get_all_hypotheses(session_id)
        results = await self._get_all_results(session_id)
        
        # Evaluate hypothesis support
        hypothesis_evaluation = await self._evaluate_all_hypotheses(
            session_id,
            hypotheses,
            results
        )
        
        # Generate conclusions
        conclusions = self._formulate_conclusions(
            hypothesis_evaluation,
            results
        )
        
        # Identify limitations
        limitations = self._identify_limitations(session_id)
        
        # Suggest future research
        future_directions = self._suggest_future_research(
            conclusions,
            limitations
        )
        
        return {
            "summary": "Formulated research conclusions",
            "hypothesis_evaluation": hypothesis_evaluation,
            "conclusions": conclusions,
            "limitations": limitations,
            "future_directions": future_directions,
        }
    
    async def _create_scientific_data(
        self,
        session_id: str,
        request: ProgressiveScientificRequest,
        phase_result: Dict[str, Any]
    ) -> ScientificData:
        """Create scientific data for storage."""
        # Create hypothesis if provided
        hypothesis = None
        if request.hypothesis:
            hypothesis = Hypothesis(
                statement=request.hypothesis.get("statement", ""),
                hypothesis_type=HypothesisType(request.hypothesis.get("type", "descriptive")),
                predictions=phase_result.get("predictions", []),
                testability_score=phase_result.get("testability_score", 0.5),
                confidence_level=ConfidenceLevel(request.hypothesis.get("confidence", "medium")),
            )
        
        # Create experiment if provided
        experiment = None
        if request.experiment_design:
            design = request.experiment_design
            experiment = Experiment(
                name=design.get("name", "Experiment"),
                experiment_type=ExperimentType(design.get("type", "controlled")),
                hypothesis_id=0,  # Would be linked properly in real implementation
                variables=design.get("variables", {}),
                controls=design.get("controls", []),
                procedure=phase_result.get("protocol", []),
                expected_duration=design.get("duration", "unknown"),
                required_resources=design.get("required_resources", []),
            )
        
        # Create results if provided
        results = []
        if request.results:
            result = Result(
                experiment_id=0,  # Would be linked properly
                data=request.results.get("data", {}),
                statistical_analysis=phase_result.get("statistics", {}),
                patterns_found=phase_result.get("patterns", []),
                anomalies=request.results.get("anomalies", []),
                confidence_interval=request.results.get("confidence_interval", {}),
            )
            results.append(result)
        
        # Create conclusion if in conclusion phase
        conclusion = None
        if request.phase == ScientificPhase.CONCLUSION:
            conclusion = Conclusion(
                summary=phase_result.get("conclusions", [""])[0] if phase_result.get("conclusions") else "",
                supported_hypotheses=phase_result.get("hypothesis_evaluation", {}).get("supported", []),
                rejected_hypotheses=phase_result.get("hypothesis_evaluation", {}).get("rejected", []),
                limitations=phase_result.get("limitations", []),
                future_work=phase_result.get("future_directions", []),
                confidence_level=ConfidenceLevel.MEDIUM,
            )
        
        return ScientificData(
            session_id=session_id,
            step_number=request.step_number,
            phase=request.phase,
            research_question=request.research_question,
            domain=request.domain,
            observations=request.observations,
            hypothesis=hypothesis,
            experiment=experiment,
            results=results,
            conclusion=conclusion,
            metadata=request.metadata,
            created_at=datetime.now(timezone.utc),
        )
    
    async def _count_observations(self, session_id: str) -> int:
        """Count total observations in session."""
        steps = await self.scientific_store.get_session_steps(session_id)
        return sum(len(step.observations) for step in steps)
    
    async def _get_all_observations(self, session_id: str) -> List[str]:
        """Get all observations from session."""
        steps = await self.scientific_store.get_session_steps(session_id)
        observations = []
        for step in steps:
            observations.extend(step.observations)
        return observations
    
    async def _get_all_hypotheses(self, session_id: str) -> List[Hypothesis]:
        """Get all hypotheses from session."""
        steps = await self.scientific_store.get_session_steps(session_id)
        return [step.hypothesis for step in steps if step.hypothesis]
    
    async def _get_all_experiments(self, session_id: str) -> List[Experiment]:
        """Get all experiments from session."""
        steps = await self.scientific_store.get_session_steps(session_id)
        return [step.experiment for step in steps if step.experiment]
    
    async def _get_all_results(self, session_id: str) -> List[Result]:
        """Get all results from session."""
        steps = await self.scientific_store.get_session_steps(session_id)
        results = []
        for step in steps:
            results.extend(step.results)
        return results
    
    async def _get_active_hypothesis(self, session_id: str) -> Optional[Hypothesis]:
        """Get currently active hypothesis."""
        hypotheses = await self.scientific_store.get_active_hypotheses(session_id)
        return hypotheses[0] if hypotheses else None
    
    async def _evaluate_hypothesis(
        self,
        session_id: str,
        hypothesis: Hypothesis
    ) -> tuple[float, List[str], List[str]]:
        """Evaluate hypothesis against evidence."""
        results = await self._get_all_results(session_id)
        
        supporting = []
        contradicting = []
        
        # Simplified evaluation
        for result in results:
            for pattern in result.patterns_found:
                if "supports" in pattern.lower():
                    supporting.append(pattern)
                elif "contradicts" in pattern.lower():
                    contradicting.append(pattern)
        
        # Calculate confidence
        if not results:
            confidence = 0.3
        else:
            support_ratio = len(supporting) / max(1, len(supporting) + len(contradicting))
            confidence = 0.3 + (0.7 * support_ratio)
        
        return confidence, supporting, contradicting
    
    def _calculate_rigor_score(
        self,
        observations: int,
        experiments: int,
        results: int,
        rigor_level: str
    ) -> float:
        """Calculate scientific rigor score."""
        base_score = 0.5
        
        # Observation factor
        if observations >= 10:
            base_score += 0.1
        elif observations >= 5:
            base_score += 0.05
        
        # Experiment factor
        if experiments >= 3:
            base_score += 0.15
        elif experiments >= 1:
            base_score += 0.1
        
        # Results factor
        if results >= experiments and experiments > 0:
            base_score += 0.15
        
        # Rigor level modifier
        rigor_modifiers = {
            "low": 0.8,
            "moderate": 1.0,
            "high": 1.2,
        }
        
        return min(1.0, base_score * rigor_modifiers.get(rigor_level, 1.0))
    
    def _calculate_reproducibility_score(
        self,
        experiments: List[Experiment],
        results: List[Result]
    ) -> float:
        """Calculate reproducibility score."""
        if not experiments:
            return 0.0
        
        score = 0.5  # Base score
        
        # Check for detailed procedures
        detailed_procedures = sum(1 for e in experiments if len(e.procedure) >= 5)
        score += 0.2 * (detailed_procedures / len(experiments))
        
        # Check for controls
        controlled_experiments = sum(1 for e in experiments if e.controls)
        score += 0.2 * (controlled_experiments / len(experiments))
        
        # Check for statistical analysis
        if results:
            analyzed_results = sum(1 for r in results if r.statistical_analysis)
            score += 0.1 * (analyzed_results / len(results))
        
        return min(1.0, score)
    
    async def _extract_key_findings(self, session_id: str) -> List[str]:
        """Extract key findings from research."""
        findings = []
        
        # Get results
        results = await self._get_all_results(session_id)
        
        # Extract patterns
        for result in results:
            for pattern in result.patterns_found[:2]:  # Top 2 patterns per result
                findings.append(f"Pattern: {pattern}")
        
        # Get conclusions
        steps = await self.scientific_store.get_session_steps(session_id)
        for step in steps:
            if step.conclusion:
                findings.append(f"Conclusion: {step.conclusion.summary}")
        
        return findings[:5]  # Return top 5 findings
    
    async def _generate_preliminary_conclusions(
        self,
        session_id: str,
        active_hypothesis: Optional[Hypothesis]
    ) -> List[str]:
        """Generate preliminary conclusions."""
        conclusions = []
        
        if active_hypothesis:
            confidence, supporting, contradicting = await self._evaluate_hypothesis(
                session_id,
                active_hypothesis
            )
            
            if confidence > 0.7:
                conclusions.append(f"Strong support for: {active_hypothesis.statement}")
            elif confidence > 0.5:
                conclusions.append(f"Moderate support for: {active_hypothesis.statement}")
            else:
                conclusions.append(f"Limited support for: {active_hypothesis.statement}")
        
        # Add general conclusions
        observations = await self._count_observations(session_id)
        if observations > 10:
            conclusions.append("Sufficient observations for pattern identification")
        
        return conclusions
    
    def _suggest_next_phase(
        self,
        current_phase: ScientificPhase,
        observations: int,
        hypotheses: int,
        experiments: int,
        results: int
    ) -> Optional[ScientificPhase]:
        """Suggest next phase in scientific process."""
        # Standard progression
        phase_order = [
            ScientificPhase.OBSERVATION,
            ScientificPhase.QUESTION,
            ScientificPhase.HYPOTHESIS,
            ScientificPhase.EXPERIMENT,
            ScientificPhase.ANALYSIS,
            ScientificPhase.CONCLUSION,
        ]
        
        current_idx = phase_order.index(current_phase)
        
        # Check if ready for next phase
        if current_phase == ScientificPhase.OBSERVATION and observations < 3:
            return ScientificPhase.OBSERVATION  # Need more observations
        elif current_phase == ScientificPhase.HYPOTHESIS and hypotheses == 0:
            return ScientificPhase.HYPOTHESIS  # Need hypothesis first
        elif current_phase == ScientificPhase.EXPERIMENT and experiments == 0:
            return ScientificPhase.EXPERIMENT  # Need experiment design
        elif current_phase == ScientificPhase.ANALYSIS and results == 0:
            return ScientificPhase.EXPERIMENT  # Need to run experiment first
        
        # Progress to next phase
        if current_idx < len(phase_order) - 1:
            return phase_order[current_idx + 1]
        
        return None  # Research complete
    
    def _generate_next_actions(
        self,
        current_phase: ScientificPhase,
        next_phase: Optional[ScientificPhase],
        phase_result: Dict[str, Any]
    ) -> List[str]:
        """Generate next actions."""
        actions = []
        
        phase_actions = {
            ScientificPhase.OBSERVATION: [
                "Continue systematic observation",
                "Document environmental conditions",
                "Look for patterns and anomalies"
            ],
            ScientificPhase.QUESTION: [
                "Refine research question for clarity",
                "Identify measurable variables",
                "Review relevant literature"
            ],
            ScientificPhase.HYPOTHESIS: [
                "Formulate testable predictions",
                "Identify null hypothesis",
                "Consider alternative explanations"
            ],
            ScientificPhase.EXPERIMENT: [
                "Design control conditions",
                "Plan data collection methods",
                "Prepare required materials"
            ],
            ScientificPhase.ANALYSIS: [
                "Apply statistical tests",
                "Visualize data patterns",
                "Check for confounding factors"
            ],
            ScientificPhase.CONCLUSION: [
                "Synthesize all findings",
                "Address original question",
                "Identify study limitations"
            ],
        }
        
        if next_phase and next_phase in phase_actions:
            actions.extend(phase_actions[next_phase][:2])
        
        # Add phase-specific actions based on results
        if "error" in phase_result:
            actions.insert(0, f"Address: {phase_result['error']}")
        
        return actions
    
    def _identify_required_resources(
        self,
        next_phase: Optional[ScientificPhase],
        experiments: List[Experiment]
    ) -> List[str]:
        """Identify resources needed for next phase."""
        resources = []
        
        if next_phase == ScientificPhase.EXPERIMENT:
            resources.extend([
                "Laboratory/workspace access",
                "Measurement instruments",
                "Safety equipment"
            ])
            
            # Add specific resources from experiments
            for exp in experiments:
                resources.extend(exp.required_resources[:2])
        
        elif next_phase == ScientificPhase.ANALYSIS:
            resources.extend([
                "Statistical software",
                "Data visualization tools",
                "Computing resources"
            ])
        
        return list(set(resources))[:5]  # Unique resources, max 5
    
    # Helper methods for phase processing
    
    def _detect_observation_patterns(self, observations: List[str]) -> List[str]:
        """Detect patterns in observations."""
        patterns = []
        
        # Simple pattern detection
        if len(observations) >= 3:
            # Check for recurring terms
            words = ' '.join(observations).lower().split()
            word_freq = {}
            for word in words:
                if len(word) > 4:  # Skip short words
                    word_freq[word] = word_freq.get(word, 0) + 1
            
            # Find frequent terms
            for word, freq in word_freq.items():
                if freq >= 2:
                    patterns.append(f"Recurring observation: {word}")
        
        return patterns[:3]
    
    def _classify_research_question(self, question: str) -> str:
        """Classify type of research question."""
        question_lower = question.lower()
        
        if any(word in question_lower for word in ["how", "why", "cause"]):
            return "explanatory"
        elif any(word in question_lower for word in ["what", "which", "when"]):
            return "descriptive"
        elif any(word in question_lower for word in ["compare", "difference", "versus"]):
            return "comparative"
        elif any(word in question_lower for word in ["predict", "forecast", "future"]):
            return "predictive"
        else:
            return "exploratory"
    
    def _generate_sub_questions(self, main_question: str, observations: List[str]) -> List[str]:
        """Generate sub-questions for research."""
        sub_questions = []
        
        # Based on question type
        if "how" in main_question.lower():
            sub_questions.append("What mechanisms might be involved?")
            sub_questions.append("What are the key variables?")
        elif "why" in main_question.lower():
            sub_questions.append("What are potential causes?")
            sub_questions.append("What evidence supports each cause?")
        
        # Based on observations
        if len(observations) > 3:
            sub_questions.append("Do observations show consistent patterns?")
        
        return sub_questions[:3]
    
    def _identify_variables(self, question: str) -> Dict[str, List[str]]:
        """Identify variables in research question."""
        return {
            "independent": ["Variable that is manipulated"],
            "dependent": ["Variable that is measured"],
            "controlled": ["Variables kept constant"],
        }
    
    def _assess_testability(self, hypothesis_statement: str) -> float:
        """Assess how testable a hypothesis is."""
        score = 0.5
        
        # Check for measurable terms
        measurable_terms = ["increase", "decrease", "correlate", "affect", "change"]
        if any(term in hypothesis_statement.lower() for term in measurable_terms):
            score += 0.2
        
        # Check for specificity
        if len(hypothesis_statement.split()) > 10:
            score += 0.1
        
        # Check for vague terms (reduce score)
        vague_terms = ["might", "maybe", "possibly", "sometimes"]
        if any(term in hypothesis_statement.lower() for term in vague_terms):
            score -= 0.2
        
        return max(0.0, min(1.0, score))
    
    def _generate_predictions(self, hypothesis: str, hypothesis_type: HypothesisType) -> List[str]:
        """Generate testable predictions from hypothesis."""
        predictions = []
        
        if hypothesis_type == HypothesisType.CAUSAL:
            predictions.append("If X increases, then Y will increase")
            predictions.append("Removing X will eliminate the effect on Y")
        elif hypothesis_type == HypothesisType.CORRELATIONAL:
            predictions.append("X and Y will vary together")
            predictions.append("The relationship will be consistent across conditions")
        elif hypothesis_type == HypothesisType.DESCRIPTIVE:
            predictions.append("The phenomenon will be observed under conditions A")
            predictions.append("The characteristics will match the description")
        
        return predictions[:2]
    
    def _assess_controls(self, controls: List[str]) -> float:
        """Assess quality of experimental controls."""
        if not controls:
            return 0.0
        
        score = 0.3 + (0.1 * min(len(controls), 5))
        
        # Check for key control types
        control_types = ["negative", "positive", "placebo", "blank"]
        for control_type in control_types:
            if any(control_type in c.lower() for c in controls):
                score += 0.1
        
        return min(1.0, score)
    
    def _assess_variable_isolation(self, variables: Dict[str, Any]) -> float:
        """Assess how well variables are isolated."""
        if not variables:
            return 0.0
        
        score = 0.5
        
        if "independent" in variables and len(variables["independent"]) == 1:
            score += 0.3  # Single independent variable is good
        
        if "controlled" in variables and len(variables.get("controlled", [])) >= 3:
            score += 0.2  # Multiple controlled variables
        
        return score
    
    def _check_resource_availability(self, required: List[str]) -> Dict[str, bool]:
        """Check availability of required resources."""
        # Simplified - would check actual availability
        availability = {}
        for resource in required:
            # Assume common resources are available
            common = ["computer", "software", "basic equipment"]
            availability[resource] = any(c in resource.lower() for c in common)
        
        return availability
    
    def _generate_experiment_protocol(self, design: Dict[str, Any]) -> List[str]:
        """Generate step-by-step protocol."""
        protocol = [
            "1. Prepare all materials and equipment",
            "2. Establish baseline measurements",
            "3. Apply experimental conditions",
            "4. Record observations at regular intervals",
            "5. Repeat for all trials",
            "6. Compile and organize data",
        ]
        
        # Customize based on experiment type
        exp_type = design.get("type", "controlled")
        if exp_type == "observational":
            protocol[2] = "3. Begin systematic observation"
        elif exp_type == "comparative":
            protocol.insert(3, "3a. Apply condition A")
            protocol.insert(4, "3b. Apply condition B")
        
        return protocol
    
    def _perform_statistical_analysis(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Perform basic statistical analysis."""
        # Simplified statistics
        return {
            "mean": results.get("mean", 0),
            "std_dev": results.get("std_dev", 0),
            "sample_size": results.get("n", 0),
            "p_value": results.get("p_value", 0.05),
            "effect_size": results.get("effect_size", 0),
        }
    
    def _detect_result_patterns(self, results: Dict[str, Any]) -> List[str]:
        """Detect patterns in results."""
        patterns = []
        
        if results.get("trend") == "increasing":
            patterns.append("Positive trend observed")
        elif results.get("trend") == "decreasing":
            patterns.append("Negative trend observed")
        
        if results.get("correlation"):
            patterns.append(f"Correlation detected: {results['correlation']}")
        
        return patterns
    
    def _assess_significance(self, stats: Dict[str, Any], rigor_level: str) -> Dict[str, Any]:
        """Assess statistical significance."""
        p_value = stats.get("p_value", 1.0)
        
        # Significance thresholds by rigor level
        thresholds = {
            "low": 0.10,
            "moderate": 0.05,
            "high": 0.01,
        }
        
        threshold = thresholds.get(rigor_level, 0.05)
        
        return {
            "is_significant": p_value < threshold,
            "confidence_level": 1 - p_value,
            "threshold_used": threshold,
        }
    
    def _analyze_errors(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze potential errors."""
        return {
            "measurement_error": results.get("measurement_error", "±5%"),
            "systematic_errors": results.get("systematic_errors", []),
            "random_errors": results.get("random_errors", []),
            "error_propagation": "Calculated based on individual errors",
        }
    
    async def _get_hypotheses_by_ids(
        self, session_id: str, hypothesis_ids: List[int]
    ) -> List[Hypothesis]:
        """Get specific hypotheses by IDs."""
        all_hypotheses = await self._get_all_hypotheses(session_id)
        # In real implementation, would filter by actual IDs
        return all_hypotheses[:len(hypothesis_ids)]
    
    async def _evaluate_all_hypotheses(
        self,
        session_id: str,
        hypotheses: List[Hypothesis],
        results: List[Result]
    ) -> Dict[str, List[str]]:
        """Evaluate all hypotheses against results."""
        evaluation = {
            "supported": [],
            "rejected": [],
            "inconclusive": [],
        }
        
        for hypothesis in hypotheses:
            confidence, supporting, contradicting = await self._evaluate_hypothesis(
                session_id,
                hypothesis
            )
            
            if confidence > 0.7:
                evaluation["supported"].append(hypothesis.statement)
            elif confidence < 0.3:
                evaluation["rejected"].append(hypothesis.statement)
            else:
                evaluation["inconclusive"].append(hypothesis.statement)
        
        return evaluation
    
    def _formulate_conclusions(
        self,
        hypothesis_evaluation: Dict[str, List[str]],
        results: List[Result]
    ) -> List[str]:
        """Formulate research conclusions."""
        conclusions = []
        
        # Based on hypothesis evaluation
        if hypothesis_evaluation["supported"]:
            conclusions.append(
                f"Research supports: {hypothesis_evaluation['supported'][0]}"
            )
        
        if hypothesis_evaluation["rejected"]:
            conclusions.append(
                f"Research rejects: {hypothesis_evaluation['rejected'][0]}"
            )
        
        # Based on results
        if results:
            conclusions.append("Empirical evidence gathered through systematic experimentation")
        
        return conclusions
    
    def _identify_limitations(self, session_id: str) -> List[str]:
        """Identify research limitations."""
        return [
            "Sample size limitations",
            "Temporal constraints",
            "Measurement precision limits",
            "Generalizability constraints",
        ]
    
    def _suggest_future_research(
        self,
        conclusions: List[str],
        limitations: List[str]
    ) -> List[str]:
        """Suggest future research directions."""
        suggestions = []
        
        # Address limitations
        if "Sample size" in str(limitations):
            suggestions.append("Expand study with larger sample size")
        
        if "Temporal" in str(limitations):
            suggestions.append("Conduct longitudinal study")
        
        # Build on conclusions
        if conclusions:
            suggestions.append("Investigate mechanisms underlying findings")
            suggestions.append("Test findings in different contexts")
        
        return suggestions[:3]
    
    # Conversion helpers
    
    def _hypothesis_to_dict(self, hypothesis: Optional[Hypothesis]) -> Optional[Dict[str, Any]]:
        """Convert hypothesis to dictionary."""
        if not hypothesis:
            return None
        
        return {
            "statement": hypothesis.statement,
            "type": hypothesis.hypothesis_type.value,
            "predictions": hypothesis.predictions,
            "testability": hypothesis.testability_score,
            "confidence": hypothesis.confidence_level.value,
        }
    
    def _experiment_to_dict(self, experiment: Experiment) -> Dict[str, Any]:
        """Convert experiment to dictionary."""
        return {
            "name": experiment.name,
            "type": experiment.experiment_type.value,
            "variables": experiment.variables,
            "controls": experiment.controls,
            "procedure_steps": len(experiment.procedure),
            "duration": experiment.expected_duration,
        }
    
    def _result_to_dict(self, result: Result) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            "data_points": len(result.data),
            "patterns": result.patterns_found,
            "anomalies": result.anomalies,
            "statistical_summary": result.statistical_analysis,
        }