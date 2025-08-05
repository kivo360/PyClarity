"""
Progressive Metacognitive Monitoring Analyzer

Tracks thinking patterns, cognitive biases, and reasoning quality
across sessions with progressive self-reflection capabilities.
"""

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from pyclarity.db.base import BaseSessionStore, SessionData
from pyclarity.db.metacognitive_store import (
    BaseMetacognitiveStore,
    MetacognitiveData,
    ThinkingPattern,
    CognitiveBias,
    ReasoningAssessment,
)
from pyclarity.tools.metacognitive_monitoring.models import (
    BiasType,
    ThinkingMode,
    ReflectionDepth,
)


class ProgressiveMetacognitiveRequest(BaseModel):
    """Request for progressive metacognitive monitoring."""
    
    session_id: Optional[str] = Field(None, description="Session ID for continuing monitoring")
    step_number: int = Field(1, description="Current monitoring step")
    
    # Current thinking to monitor
    current_thought: str = Field(..., description="Current thought or reasoning to monitor")
    thinking_context: str = Field(..., description="Context of the thinking process")
    thinking_mode: ThinkingMode = Field(..., description="Current mode of thinking")
    
    # Self-assessment
    confidence_level: float = Field(0.5, ge=0.0, le=1.0, description="Self-assessed confidence")
    clarity_level: float = Field(0.5, ge=0.0, le=1.0, description="Clarity of thinking")
    
    # Monitoring focus
    monitor_for_biases: bool = Field(True, description="Check for cognitive biases")
    monitor_patterns: bool = Field(True, description="Track thinking patterns")
    monitor_quality: bool = Field(True, description="Assess reasoning quality")
    
    # Reflection settings
    reflection_depth: ReflectionDepth = Field(ReflectionDepth.MODERATE)
    include_improvement_suggestions: bool = Field(True)
    
    # Previous monitoring
    previous_assessments: List[int] = Field(default_factory=list, description="Previous assessment IDs")
    build_on_previous: bool = Field(True)
    
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ProgressiveMetacognitiveResponse(BaseModel):
    """Response from progressive metacognitive monitoring."""
    
    # Core response
    status: str = Field(..., description="Status of monitoring")
    session_id: str = Field(..., description="Session identifier")
    assessment_id: int = Field(..., description="Database ID of this assessment")
    step_number: int = Field(..., description="Sequential step number")
    
    # Thinking assessment
    thinking_quality_score: float = Field(..., ge=0.0, le=1.0)
    clarity_score: float = Field(..., ge=0.0, le=1.0)
    coherence_score: float = Field(..., ge=0.0, le=1.0)
    
    # Pattern detection
    patterns_detected: List[Dict[str, Any]] = Field(default_factory=list)
    dominant_thinking_mode: str = Field(..., description="Primary thinking mode observed")
    
    # Bias detection
    biases_detected: List[Dict[str, Any]] = Field(default_factory=list)
    bias_mitigation_suggestions: List[str] = Field(default_factory=list)
    
    # Quality assessment
    strengths_identified: List[str] = Field(default_factory=list)
    weaknesses_identified: List[str] = Field(default_factory=list)
    improvement_areas: List[str] = Field(default_factory=list)
    
    # Metacognitive insights
    self_awareness_indicators: List[str] = Field(default_factory=list)
    cognitive_load_assessment: str = Field(..., description="Low, moderate, or high")
    
    # Progress tracking
    thinking_evolution: Optional[Dict[str, Any]] = Field(None)
    pattern_trends: List[str] = Field(default_factory=list)
    
    # Recommendations
    thinking_strategies: List[str] = Field(default_factory=list)
    next_steps: List[str] = Field(default_factory=list)
    
    # Error handling
    error: Optional[str] = Field(None)
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "session_id": "meta-123",
                "thinking_quality_score": 0.75,
                "patterns_detected": [{"pattern": "analytical", "frequency": 0.8}],
                "biases_detected": [{"bias": "confirmation_bias", "severity": "moderate"}]
            }
        }


class ProgressiveMetacognitiveAnalyzer:
    """Progressive metacognitive monitoring with session management."""
    
    def __init__(
        self,
        session_store: BaseSessionStore,
        metacognitive_store: BaseMetacognitiveStore,
    ):
        """Initialize with required stores."""
        self.session_store = session_store
        self.metacognitive_store = metacognitive_store
    
    async def monitor_thinking(
        self, request: ProgressiveMetacognitiveRequest
    ) -> ProgressiveMetacognitiveResponse:
        """Monitor and assess thinking process."""
        try:
            # Get or create session
            session = await self._get_or_create_session(request)
            
            # Assess current thinking
            quality_scores = self._assess_thinking_quality(request)
            
            # Detect patterns
            patterns = await self._detect_patterns(session.session_id, request)
            
            # Check for biases
            biases = []
            mitigation = []
            if request.monitor_for_biases:
                biases = self._detect_biases(request)
                mitigation = self._suggest_bias_mitigation(biases)
            
            # Identify strengths and weaknesses
            strengths, weaknesses = self._assess_strengths_weaknesses(request, quality_scores)
            
            # Track cognitive load
            cognitive_load = self._assess_cognitive_load(request)
            
            # Generate insights
            self_awareness = self._assess_self_awareness(request)
            
            # Track evolution if building on previous
            evolution = None
            trends = []
            if request.build_on_previous and request.previous_assessments:
                evolution, trends = await self._track_thinking_evolution(
                    session.session_id,
                    request.previous_assessments
                )
            
            # Generate recommendations
            strategies = self._generate_thinking_strategies(
                patterns,
                biases,
                weaknesses
            )
            
            next_steps = self._suggest_next_steps(
                request.thinking_mode,
                quality_scores,
                biases
            )
            
            # Create and save assessment
            assessment_data = await self._create_assessment_data(
                session.session_id,
                request,
                quality_scores,
                patterns,
                biases
            )
            saved_data = await self.metacognitive_store.save_assessment(assessment_data)
            
            # Determine improvement areas
            improvement_areas = self._identify_improvement_areas(
                quality_scores,
                patterns,
                biases
            )
            
            return ProgressiveMetacognitiveResponse(
                status="success",
                session_id=session.session_id,
                assessment_id=saved_data.id,
                step_number=saved_data.step_number,
                thinking_quality_score=quality_scores["overall"],
                clarity_score=quality_scores["clarity"],
                coherence_score=quality_scores["coherence"],
                patterns_detected=[self._pattern_to_dict(p) for p in patterns],
                dominant_thinking_mode=self._get_dominant_mode(patterns),
                biases_detected=[self._bias_to_dict(b) for b in biases],
                bias_mitigation_suggestions=mitigation,
                strengths_identified=strengths,
                weaknesses_identified=weaknesses,
                improvement_areas=improvement_areas,
                self_awareness_indicators=self_awareness,
                cognitive_load_assessment=cognitive_load,
                thinking_evolution=evolution,
                pattern_trends=trends,
                thinking_strategies=strategies,
                next_steps=next_steps,
            )
            
        except Exception as e:
            return ProgressiveMetacognitiveResponse(
                status="error",
                session_id=request.session_id or str(uuid.uuid4()),
                assessment_id=0,
                step_number=request.step_number,
                thinking_quality_score=0.0,
                clarity_score=0.0,
                coherence_score=0.0,
                dominant_thinking_mode="unknown",
                cognitive_load_assessment="unknown",
                error=str(e),
            )
    
    async def _get_or_create_session(
        self, request: ProgressiveMetacognitiveRequest
    ) -> SessionData:
        """Get existing session or create new one."""
        if request.session_id:
            session = await self.session_store.get_session(request.session_id)
            if session:
                return session
        
        # Create new session
        session_data = SessionData(
            session_id=request.session_id or str(uuid.uuid4()),
            tool_name="Metacognitive Monitoring",
            created_at=datetime.now(timezone.utc),
            metadata={
                "thinking_context": request.thinking_context,
                "initial_mode": request.thinking_mode.value,
                "reflection_depth": request.reflection_depth.value,
            }
        )
        
        return await self.session_store.create_session(session_data)
    
    def _assess_thinking_quality(
        self, request: ProgressiveMetacognitiveRequest
    ) -> Dict[str, float]:
        """Assess quality of thinking."""
        # Analyze thought structure
        thought_length = len(request.current_thought.split())
        sentence_count = len(request.current_thought.split('.'))
        
        # Base scores
        clarity = request.clarity_level  # Start with self-assessment
        coherence = 0.7  # Default
        depth = 0.5
        
        # Adjust based on content analysis
        if thought_length > 20:
            depth += 0.2
        if thought_length > 50:
            depth += 0.1
        
        # Check for logical connectors
        logical_words = ['because', 'therefore', 'however', 'although', 'thus', 'consequently']
        logical_count = sum(1 for word in logical_words if word in request.current_thought.lower())
        coherence += min(0.3, logical_count * 0.1)
        
        # Check for evidence words
        evidence_words = ['evidence', 'data', 'research', 'study', 'analysis', 'observation']
        evidence_count = sum(1 for word in evidence_words if word in request.current_thought.lower())
        if evidence_count > 0:
            clarity += 0.1
            depth += 0.1
        
        # Overall quality
        overall = (clarity + coherence + depth) / 3
        
        return {
            "overall": min(1.0, overall),
            "clarity": min(1.0, clarity),
            "coherence": min(1.0, coherence),
            "depth": min(1.0, depth),
        }
    
    async def _detect_patterns(
        self,
        session_id: str,
        request: ProgressiveMetacognitiveRequest
    ) -> List[ThinkingPattern]:
        """Detect thinking patterns."""
        patterns = []
        
        # Analyze current thought for patterns
        thought_lower = request.current_thought.lower()
        
        # Analytical pattern
        if any(word in thought_lower for word in ['analyze', 'examine', 'investigate', 'breakdown']):
            patterns.append(ThinkingPattern(
                pattern_type="analytical",
                description="Breaking down complex ideas into components",
                frequency=0.8,
                effectiveness=0.7,
            ))
        
        # Creative pattern
        if any(word in thought_lower for word in ['imagine', 'create', 'innovate', 'what if']):
            patterns.append(ThinkingPattern(
                pattern_type="creative",
                description="Generating novel ideas and connections",
                frequency=0.6,
                effectiveness=0.8,
            ))
        
        # Critical pattern
        if any(word in thought_lower for word in ['however', 'but', 'challenge', 'question']):
            patterns.append(ThinkingPattern(
                pattern_type="critical",
                description="Questioning assumptions and evaluating evidence",
                frequency=0.7,
                effectiveness=0.8,
            ))
        
        # Systems thinking
        if any(word in thought_lower for word in ['system', 'interact', 'relationship', 'connected']):
            patterns.append(ThinkingPattern(
                pattern_type="systems",
                description="Considering interconnections and relationships",
                frequency=0.5,
                effectiveness=0.9,
            ))
        
        # Get historical patterns if available
        if request.build_on_previous:
            assessments = await self.metacognitive_store.get_session_assessments(session_id)
            # Aggregate historical patterns (simplified)
            for assessment in assessments[-3:]:  # Last 3 assessments
                for pattern in assessment.thinking_patterns:
                    # Update frequency based on recurrence
                    existing = next((p for p in patterns if p.pattern_type == pattern.pattern_type), None)
                    if existing:
                        existing.frequency = min(1.0, existing.frequency + 0.1)
        
        return patterns
    
    def _detect_biases(self, request: ProgressiveMetacognitiveRequest) -> List[CognitiveBias]:
        """Detect potential cognitive biases."""
        biases = []
        thought_lower = request.current_thought.lower()
        
        # Confirmation bias
        if any(phrase in thought_lower for phrase in ['as expected', 'confirms my', 'proves that']):
            biases.append(CognitiveBias(
                bias_type=BiasType.CONFIRMATION,
                severity="moderate",
                description="Tendency to favor information confirming existing beliefs",
                evidence=["Uses confirming language"],
            ))
        
        # Anchoring bias
        if 'first' in thought_lower and any(word in thought_lower for word in ['therefore', 'so', 'thus']):
            biases.append(CognitiveBias(
                bias_type=BiasType.ANCHORING,
                severity="low",
                description="Over-reliance on first piece of information",
                evidence=["Heavy emphasis on initial information"],
            ))
        
        # Availability heuristic
        if any(phrase in thought_lower for phrase in ['recent', 'just saw', 'reminds me']):
            biases.append(CognitiveBias(
                bias_type=BiasType.AVAILABILITY,
                severity="low",
                description="Overweighting easily recalled information",
                evidence=["References to recent or memorable events"],
            ))
        
        # Overconfidence bias
        if request.confidence_level > 0.9 and request.clarity_level < 0.7:
            biases.append(CognitiveBias(
                bias_type=BiasType.OVERCONFIDENCE,
                severity="high",
                description="Excessive confidence despite unclear thinking",
                evidence=["High confidence with low clarity"],
            ))
        
        return biases
    
    def _suggest_bias_mitigation(self, biases: List[CognitiveBias]) -> List[str]:
        """Suggest ways to mitigate detected biases."""
        suggestions = []
        
        bias_mitigations = {
            BiasType.CONFIRMATION: [
                "Actively seek disconfirming evidence",
                "Consider alternative explanations",
                "Ask: What would prove this wrong?"
            ],
            BiasType.ANCHORING: [
                "Question initial assumptions",
                "Consider multiple starting points",
                "Evaluate information independently"
            ],
            BiasType.AVAILABILITY: [
                "Look for base rate information",
                "Consider systematic data over anecdotes",
                "Question if recent events are representative"
            ],
            BiasType.OVERCONFIDENCE: [
                "Identify uncertainties explicitly",
                "Seek external validation",
                "Consider confidence intervals"
            ],
        }
        
        for bias in biases:
            if bias.bias_type in bias_mitigations:
                suggestions.extend(bias_mitigations[bias.bias_type])
        
        return list(set(suggestions))[:5]  # Return up to 5 unique suggestions
    
    def _assess_strengths_weaknesses(
        self,
        request: ProgressiveMetacognitiveRequest,
        quality_scores: Dict[str, float]
    ) -> tuple[List[str], List[str]]:
        """Identify cognitive strengths and weaknesses."""
        strengths = []
        weaknesses = []
        
        # Based on quality scores
        if quality_scores["clarity"] > 0.7:
            strengths.append("Clear articulation of ideas")
        else:
            weaknesses.append("Clarity of expression needs improvement")
        
        if quality_scores["coherence"] > 0.7:
            strengths.append("Logical flow and connections")
        else:
            weaknesses.append("Logical coherence could be stronger")
        
        if quality_scores["depth"] > 0.7:
            strengths.append("Thorough analysis and depth")
        else:
            weaknesses.append("Could explore ideas more deeply")
        
        # Based on thinking mode
        if request.thinking_mode == ThinkingMode.ANALYTICAL:
            strengths.append("Strong analytical approach")
        elif request.thinking_mode == ThinkingMode.CREATIVE:
            strengths.append("Creative and innovative thinking")
        elif request.thinking_mode == ThinkingMode.CRITICAL:
            strengths.append("Effective critical evaluation")
        
        # Based on self-assessment
        if request.confidence_level > 0.7 and request.clarity_level > 0.7:
            strengths.append("High self-awareness")
        
        return strengths, weaknesses
    
    def _assess_cognitive_load(self, request: ProgressiveMetacognitiveRequest) -> str:
        """Assess current cognitive load."""
        # Simple heuristic based on complexity indicators
        complexity_score = 0
        
        # Length and density
        thought_length = len(request.current_thought.split())
        if thought_length > 100:
            complexity_score += 2
        elif thought_length > 50:
            complexity_score += 1
        
        # Number of concepts
        concept_indicators = ['and', 'but', 'however', 'furthermore', 'additionally']
        concept_count = sum(1 for word in concept_indicators if word in request.current_thought.lower())
        complexity_score += min(2, concept_count)
        
        # Self-reported clarity inversely related to load
        if request.clarity_level < 0.5:
            complexity_score += 2
        elif request.clarity_level < 0.7:
            complexity_score += 1
        
        # Determine load level
        if complexity_score >= 5:
            return "high"
        elif complexity_score >= 3:
            return "moderate"
        else:
            return "low"
    
    def _assess_self_awareness(self, request: ProgressiveMetacognitiveRequest) -> List[str]:
        """Assess indicators of self-awareness."""
        indicators = []
        thought_lower = request.current_thought.lower()
        
        # Meta-cognitive language
        if any(phrase in thought_lower for phrase in ['i think', 'i believe', 'i wonder']):
            indicators.append("Uses self-referential language")
        
        if any(phrase in thought_lower for phrase in ['not sure', 'uncertain', 'might be']):
            indicators.append("Acknowledges uncertainty")
        
        if any(phrase in thought_lower for phrase in ['on second thought', 'actually', 'wait']):
            indicators.append("Shows self-correction")
        
        # Alignment of confidence and clarity
        if abs(request.confidence_level - request.clarity_level) < 0.2:
            indicators.append("Confidence aligns with clarity")
        
        # Reflection depth
        if request.reflection_depth == ReflectionDepth.DEEP:
            indicators.append("Engages in deep reflection")
        
        return indicators
    
    async def _track_thinking_evolution(
        self,
        session_id: str,
        previous_assessments: List[int]
    ) -> tuple[Optional[Dict[str, Any]], List[str]]:
        """Track how thinking has evolved."""
        assessments = await self.metacognitive_store.get_session_assessments(session_id)
        
        if len(assessments) < 2:
            return None, []
        
        # Get relevant assessments
        relevant = [a for a in assessments if a.id in previous_assessments or a == assessments[-1]]
        
        if len(relevant) < 2:
            return None, []
        
        # Compare first and last
        first = relevant[0]
        last = relevant[-1]
        
        evolution = {
            "quality_change": last.reasoning_assessment.overall_quality - first.reasoning_assessment.overall_quality,
            "clarity_change": last.reasoning_assessment.clarity - first.reasoning_assessment.clarity,
            "patterns_emerged": [],
            "patterns_strengthened": [],
            "biases_reduced": [],
            "biases_increased": [],
        }
        
        # Track pattern changes
        first_patterns = {p.pattern_type: p.frequency for p in first.thinking_patterns}
        last_patterns = {p.pattern_type: p.frequency for p in last.thinking_patterns}
        
        for pattern_type, frequency in last_patterns.items():
            if pattern_type not in first_patterns:
                evolution["patterns_emerged"].append(pattern_type)
            elif frequency > first_patterns[pattern_type]:
                evolution["patterns_strengthened"].append(pattern_type)
        
        # Track bias changes
        first_biases = {b.bias_type.value: b.severity for b in first.biases_detected}
        last_biases = {b.bias_type.value: b.severity for b in last.biases_detected}
        
        for bias_type in first_biases:
            if bias_type not in last_biases:
                evolution["biases_reduced"].append(bias_type)
        
        for bias_type in last_biases:
            if bias_type not in first_biases:
                evolution["biases_increased"].append(bias_type)
        
        # Generate trends
        trends = []
        if evolution["quality_change"] > 0.1:
            trends.append("Overall thinking quality improving")
        elif evolution["quality_change"] < -0.1:
            trends.append("Overall thinking quality declining")
        
        if evolution["patterns_strengthened"]:
            trends.append(f"Strengthening {', '.join(evolution['patterns_strengthened'])} patterns")
        
        if evolution["biases_reduced"]:
            trends.append(f"Successfully reducing {', '.join(evolution['biases_reduced'])} biases")
        
        return evolution, trends
    
    def _generate_thinking_strategies(
        self,
        patterns: List[ThinkingPattern],
        biases: List[CognitiveBias],
        weaknesses: List[str]
    ) -> List[str]:
        """Generate strategies to improve thinking."""
        strategies = []
        
        # Based on patterns
        pattern_types = [p.pattern_type for p in patterns]
        if "analytical" not in pattern_types:
            strategies.append("Try breaking down the problem into smaller components")
        if "creative" not in pattern_types:
            strategies.append("Explore alternative perspectives and novel connections")
        if "critical" not in pattern_types:
            strategies.append("Question underlying assumptions more actively")
        
        # Based on biases
        if biases:
            strategies.append("Implement structured decision-making to reduce bias")
            strategies.append("Seek diverse perspectives to challenge your thinking")
        
        # Based on weaknesses
        if "clarity" in str(weaknesses).lower():
            strategies.append("Use concrete examples to clarify abstract concepts")
        if "coherence" in str(weaknesses).lower():
            strategies.append("Create explicit logical connections between ideas")
        if "depth" in str(weaknesses).lower():
            strategies.append("Ask 'why' and 'how' questions to deepen analysis")
        
        return strategies[:5]  # Return top 5 strategies
    
    def _suggest_next_steps(
        self,
        thinking_mode: ThinkingMode,
        quality_scores: Dict[str, float],
        biases: List[CognitiveBias]
    ) -> List[str]:
        """Suggest immediate next steps."""
        steps = []
        
        # Based on quality scores
        if quality_scores["clarity"] < 0.6:
            steps.append("Clarify key concepts before proceeding")
        
        if quality_scores["coherence"] < 0.6:
            steps.append("Review logical flow and connections")
        
        # Based on thinking mode
        mode_steps = {
            ThinkingMode.ANALYTICAL: "Synthesize findings into actionable insights",
            ThinkingMode.CREATIVE: "Evaluate feasibility of generated ideas",
            ThinkingMode.CRITICAL: "Balance criticism with constructive alternatives",
            ThinkingMode.REFLECTIVE: "Apply reflections to future thinking",
        }
        
        if thinking_mode in mode_steps:
            steps.append(mode_steps[thinking_mode])
        
        # Based on biases
        if len(biases) > 2:
            steps.append("Pause to actively counter identified biases")
        
        # General improvement
        if quality_scores["overall"] < 0.7:
            steps.append("Take a break to refresh cognitive resources")
        else:
            steps.append("Document key insights for future reference")
        
        return steps
    
    async def _create_assessment_data(
        self,
        session_id: str,
        request: ProgressiveMetacognitiveRequest,
        quality_scores: Dict[str, float],
        patterns: List[ThinkingPattern],
        biases: List[CognitiveBias]
    ) -> MetacognitiveData:
        """Create assessment data for storage."""
        reasoning = ReasoningAssessment(
            overall_quality=quality_scores["overall"],
            clarity=quality_scores["clarity"],
            coherence=quality_scores["coherence"],
            depth=quality_scores["depth"],
            logical_consistency=quality_scores["coherence"],  # Using coherence as proxy
            evidence_usage=0.5,  # Would need more sophisticated analysis
        )
        
        return MetacognitiveData(
            session_id=session_id,
            step_number=request.step_number,
            thinking_context=request.thinking_context,
            current_thought=request.current_thought,
            thinking_mode=request.thinking_mode,
            thinking_patterns=patterns,
            biases_detected=biases,
            reasoning_assessment=reasoning,
            self_awareness_level=request.confidence_level,
            improvement_suggestions=self._generate_thinking_strategies(patterns, biases, []),
            metadata=request.metadata,
            created_at=datetime.now(timezone.utc),
        )
    
    def _identify_improvement_areas(
        self,
        quality_scores: Dict[str, float],
        patterns: List[ThinkingPattern],
        biases: List[CognitiveBias]
    ) -> List[str]:
        """Identify specific areas for improvement."""
        areas = []
        
        # Quality-based improvements
        if quality_scores["clarity"] < 0.7:
            areas.append("Enhance clarity through structured expression")
        
        if quality_scores["depth"] < 0.7:
            areas.append("Develop deeper analytical capabilities")
        
        # Pattern-based improvements
        weak_patterns = [p for p in patterns if p.effectiveness < 0.7]
        for pattern in weak_patterns:
            areas.append(f"Strengthen {pattern.pattern_type} thinking skills")
        
        # Bias-based improvements
        severe_biases = [b for b in biases if b.severity == "high"]
        if severe_biases:
            areas.append("Develop stronger bias recognition and mitigation")
        
        return areas
    
    def _pattern_to_dict(self, pattern: ThinkingPattern) -> Dict[str, Any]:
        """Convert pattern to dictionary."""
        return {
            "pattern": pattern.pattern_type,
            "description": pattern.description,
            "frequency": pattern.frequency,
            "effectiveness": pattern.effectiveness,
        }
    
    def _bias_to_dict(self, bias: CognitiveBias) -> Dict[str, Any]:
        """Convert bias to dictionary."""
        return {
            "bias": bias.bias_type.value,
            "severity": bias.severity,
            "description": bias.description,
            "evidence": bias.evidence,
        }
    
    def _get_dominant_mode(self, patterns: List[ThinkingPattern]) -> str:
        """Determine dominant thinking mode from patterns."""
        if not patterns:
            return "balanced"
        
        # Find pattern with highest frequency
        dominant = max(patterns, key=lambda p: p.frequency)
        return dominant.pattern_type