"""
Progressive Collaborative Reasoning Analyzer

Provides step-by-step collaborative reasoning with multiple personas,
maintaining session state for iterative collaboration.
"""

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from pyclarity.db.base import BaseSessionStore, SessionData
from pyclarity.db.collaborative_store import BaseCollaborativeStore, PerspectiveData, ConflictData, CollaborativeSynthesis
from pyclarity.tools.collaborative_reasoning.models import (
    CollaborationPattern,
    PersonaType,
    ConsensusLevel,
)


class ProgressiveCollaborativeRequest(BaseModel):
    """Request for progressive collaborative reasoning."""
    
    session_id: Optional[str] = Field(None, description="Session ID for continuing collaboration")
    step_number: int = Field(1, description="Current step in collaboration")
    persona_type: PersonaType = Field(..., description="Active persona for this step")
    problem_statement: str = Field(..., description="Problem being discussed")
    contribution: str = Field(..., description="This persona's contribution")
    context: Optional[str] = Field(None, description="Additional context")
    
    # Building on previous
    previous_contributions: List[int] = Field(default_factory=list, description="IDs of previous contributions to consider")
    responding_to: Optional[int] = Field(None, description="ID of contribution being responded to")
    build_on_previous: bool = Field(True, description="Whether to build on previous contributions")
    
    # Collaboration settings
    collaboration_pattern: CollaborationPattern = Field(
        CollaborationPattern.ROUND_ROBIN,
        description="Pattern for collaboration"
    )
    seek_consensus: bool = Field(True, description="Whether to work toward consensus")
    allow_dissent: bool = Field(True, description="Whether to allow dissenting views")
    
    # Metadata
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ProgressiveCollaborativeResponse(BaseModel):
    """Response from progressive collaborative reasoning."""
    
    # Core response
    status: str = Field(..., description="Status of the collaboration step")
    session_id: str = Field(..., description="Session identifier")
    step_id: int = Field(..., description="Database ID of this step")
    step_number: int = Field(..., description="Sequential step number")
    
    # Contribution details
    persona: str = Field(..., description="Persona who contributed")
    contribution_summary: str = Field(..., description="Summary of contribution")
    key_points: List[str] = Field(default_factory=list, description="Key points made")
    
    # Collaboration state
    consensus_level: ConsensusLevel = Field(..., description="Current consensus level")
    areas_of_agreement: List[str] = Field(default_factory=list)
    areas_of_disagreement: List[str] = Field(default_factory=list)
    
    # Next steps
    next_persona_suggested: Optional[PersonaType] = Field(None, description="Suggested next persona")
    questions_raised: List[str] = Field(default_factory=list, description="Questions for next persona")
    collaboration_complete: bool = Field(False, description="Whether collaboration is complete")
    
    # Progress tracking
    personas_contributed: List[str] = Field(default_factory=list, description="Personas who have contributed")
    total_contributions: int = Field(0, description="Total contributions so far")
    
    # Error handling
    error: Optional[str] = Field(None, description="Error message if any")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "session_id": "collab-123",
                "step_id": 1,
                "step_number": 1,
                "persona": "Technical Expert",
                "contribution_summary": "Proposed microservices architecture",
                "consensus_level": "emerging",
                "next_persona_suggested": "risk_analyst"
            }
        }


class ProgressiveCollaborativeAnalyzer:
    """Progressive collaborative reasoning with session management."""
    
    def __init__(
        self,
        session_store: BaseSessionStore,
        collaborative_store: BaseCollaborativeStore,
    ):
        """Initialize with required stores."""
        self.session_store = session_store
        self.collaborative_store = collaborative_store
    
    async def collaborate(
        self, request: ProgressiveCollaborativeRequest
    ) -> ProgressiveCollaborativeResponse:
        """Process a collaborative reasoning step."""
        try:
            # Get or create session
            session = await self._get_or_create_session(request)
            
            # Create collaborative data
            collab_data = await self._create_collaboration_step(session.session_id, request)
            
            # Save to store
            saved_data = await self.collaborative_store.save_collaboration_step(collab_data)
            
            # Analyze collaboration state
            consensus = await self._analyze_consensus(session.session_id)
            agreements, disagreements = await self._identify_agreement_areas(session.session_id)
            
            # Determine next steps
            next_persona = self._suggest_next_persona(
                request.persona_type,
                request.collaboration_pattern,
                await self._get_contributed_personas(session.session_id)
            )
            
            # Get questions for next persona
            questions = self._generate_questions_for_next(
                request.persona_type,
                request.contribution,
                next_persona
            )
            
            # Check if collaboration is complete
            is_complete = await self._check_collaboration_complete(
                session.session_id,
                consensus,
                request.seek_consensus
            )
            
            # Get contributed personas
            contributed_personas = await self._get_contributed_personas(session.session_id)
            
            # Build response
            return ProgressiveCollaborativeResponse(
                status="success",
                session_id=session.session_id,
                step_id=saved_data.id,
                step_number=saved_data.step_number,
                persona=request.persona_type.value,
                contribution_summary=self._summarize_contribution(request.contribution),
                key_points=self._extract_key_points(request.contribution),
                consensus_level=consensus,
                areas_of_agreement=agreements,
                areas_of_disagreement=disagreements,
                next_persona_suggested=next_persona,
                questions_raised=questions,
                collaboration_complete=is_complete,
                personas_contributed=[p.value for p in contributed_personas],
                total_contributions=len(await self.collaborative_store.get_session_steps(session.session_id)),
            )
            
        except Exception as e:
            return ProgressiveCollaborativeResponse(
                status="error",
                session_id=request.session_id or str(uuid.uuid4()),
                step_id=0,
                step_number=request.step_number,
                persona=request.persona_type.value,
                contribution_summary="",
                consensus_level=ConsensusLevel.NONE,
                error=str(e),
            )
    
    async def _get_or_create_session(
        self, request: ProgressiveCollaborativeRequest
    ) -> SessionData:
        """Get existing session or create new one."""
        if request.session_id:
            session = await self.session_store.get_session(request.session_id)
            if session:
                return session
        
        # Create new session
        session_data = SessionData(
            session_id=request.session_id or str(uuid.uuid4()),
            tool_name="Collaborative Reasoning",
            created_at=datetime.now(timezone.utc),
            metadata={
                "problem_statement": request.problem_statement,
                "collaboration_pattern": request.collaboration_pattern.value,
                "initial_persona": request.persona_type.value,
            }
        )
        
        return await self.session_store.create_session(session_data)
    
    async def _create_collaboration_step(
        self, session_id: str, request: ProgressiveCollaborativeRequest
    ) -> CollaborativeData:
        """Create collaboration step data."""
        # Get previous contributions if building on them
        previous_insights = []
        if request.build_on_previous and request.previous_contributions:
            for contrib_id in request.previous_contributions:
                prev_data = await self.collaborative_store.get_collaboration_step(contrib_id)
                if prev_data and prev_data.contribution:
                    previous_insights.append({
                        "persona": prev_data.contribution.persona.value,
                        "insight": prev_data.contribution.main_point
                    })
        
        # Create persona contribution
        contribution = PersonaContribution(
            persona=request.persona_type,
            main_point=self._extract_main_point(request.contribution),
            supporting_arguments=self._extract_arguments(request.contribution),
            questions_raised=self._extract_questions(request.contribution),
            assumptions_challenged=self._extract_challenged_assumptions(
                request.contribution,
                previous_insights
            ),
            confidence_level=0.8,  # Would be calculated based on content
        )
        
        return CollaborativeData(
            session_id=session_id,
            step_number=request.step_number,
            problem_statement=request.problem_statement,
            context=request.context,
            contribution=contribution,
            collaboration_pattern=request.collaboration_pattern,
            responding_to_id=request.responding_to,
            synthesis=None,  # Will be added when synthesizing
            metadata=request.metadata,
            created_at=datetime.now(timezone.utc),
        )
    
    async def _analyze_consensus(self, session_id: str) -> ConsensusLevel:
        """Analyze current consensus level."""
        steps = await self.collaborative_store.get_session_steps(session_id)
        
        if len(steps) < 2:
            return ConsensusLevel.NONE
        
        # Simple heuristic - would be more sophisticated in practice
        unique_personas = set(s.contribution.persona for s in steps if s.contribution)
        
        if len(unique_personas) < 2:
            return ConsensusLevel.NONE
        elif len(unique_personas) == 2:
            return ConsensusLevel.EMERGING
        elif len(unique_personas) >= 3:
            # Check for agreement patterns
            # This is simplified - real implementation would analyze content
            return ConsensusLevel.PARTIAL
        
        return ConsensusLevel.STRONG
    
    async def _identify_agreement_areas(
        self, session_id: str
    ) -> tuple[List[str], List[str]]:
        """Identify areas of agreement and disagreement."""
        steps = await self.collaborative_store.get_session_steps(session_id)
        
        # Simplified - would use NLP in practice
        agreements = []
        disagreements = []
        
        if len(steps) >= 2:
            agreements.append("Problem requires systematic approach")
            agreements.append("Multiple perspectives are valuable")
            
            if len(steps) >= 3:
                disagreements.append("Implementation timeline")
                disagreements.append("Resource allocation priorities")
        
        return agreements, disagreements
    
    def _suggest_next_persona(
        self,
        current: PersonaType,
        pattern: CollaborationPattern,
        contributed: List[PersonaType]
    ) -> Optional[PersonaType]:
        """Suggest next persona based on pattern."""
        all_personas = list(PersonaType)
        remaining = [p for p in all_personas if p not in contributed]
        
        if not remaining:
            return None
        
        if pattern == CollaborationPattern.ROUND_ROBIN:
            # Get next in sequence
            current_idx = all_personas.index(current)
            next_idx = (current_idx + 1) % len(all_personas)
            next_persona = all_personas[next_idx]
            
            # Skip if already contributed
            while next_persona in contributed and remaining:
                next_idx = (next_idx + 1) % len(all_personas)
                next_persona = all_personas[next_idx]
            
            return next_persona if next_persona in remaining else remaining[0]
        
        elif pattern == CollaborationPattern.DEVILS_ADVOCATE:
            # Suggest contrasting persona
            contrasts = {
                PersonaType.OPTIMIST: PersonaType.CRITIC,
                PersonaType.CRITIC: PersonaType.OPTIMIST,
                PersonaType.TECHNICAL_EXPERT: PersonaType.BUSINESS_STRATEGIST,
                PersonaType.BUSINESS_STRATEGIST: PersonaType.TECHNICAL_EXPERT,
            }
            
            suggested = contrasts.get(current, remaining[0])
            return suggested if suggested in remaining else remaining[0]
        
        # Default to first remaining
        return remaining[0]
    
    def _generate_questions_for_next(
        self,
        current_persona: PersonaType,
        contribution: str,
        next_persona: Optional[PersonaType]
    ) -> List[str]:
        """Generate questions for next persona."""
        if not next_persona:
            return []
        
        # Persona-specific questions
        questions_map = {
            PersonaType.RISK_ANALYST: [
                "What are the main risks in this approach?",
                "How can we mitigate potential failures?",
                "What's our contingency plan?"
            ],
            PersonaType.INNOVATOR: [
                "How can we make this more innovative?",
                "What emerging technologies could help?",
                "Are there unconventional approaches to consider?"
            ],
            PersonaType.PRAGMATIST: [
                "Is this feasible with current resources?",
                "What's the minimum viable approach?",
                "How do we measure success?"
            ],
        }
        
        return questions_map.get(next_persona, [
            "What's your perspective on this?",
            "Do you see any issues we've missed?",
            "How would you approach this differently?"
        ])
    
    async def _check_collaboration_complete(
        self,
        session_id: str,
        consensus: ConsensusLevel,
        seek_consensus: bool
    ) -> bool:
        """Check if collaboration is complete."""
        steps = await self.collaborative_store.get_session_steps(session_id)
        
        # Complete if consensus reached (if seeking)
        if seek_consensus and consensus == ConsensusLevel.STRONG:
            return True
        
        # Complete if all personas contributed
        contributed = await self._get_contributed_personas(session_id)
        if len(contributed) == len(PersonaType):
            return True
        
        # Complete if synthesis exists
        if any(s.synthesis for s in steps):
            return True
        
        return False
    
    async def _get_contributed_personas(self, session_id: str) -> List[PersonaType]:
        """Get list of personas who have contributed."""
        steps = await self.collaborative_store.get_session_steps(session_id)
        return list(set(
            s.contribution.persona 
            for s in steps 
            if s.contribution
        ))
    
    def _summarize_contribution(self, contribution: str) -> str:
        """Create summary of contribution."""
        # Simplified - would use NLP summarization
        sentences = contribution.split('.')
        if sentences:
            return sentences[0].strip() + "."
        return contribution[:100] + "..."
    
    def _extract_key_points(self, contribution: str) -> List[str]:
        """Extract key points from contribution."""
        # Simplified - would use NLP
        points = []
        
        # Look for numbered points
        lines = contribution.split('\n')
        for line in lines:
            if any(line.strip().startswith(marker) for marker in ['1.', '2.', '3.', '-', '*']):
                points.append(line.strip().lstrip('1234567890.-* '))
        
        if not points and contribution:
            # Take first 2 sentences
            sentences = contribution.split('.')[:2]
            points = [s.strip() for s in sentences if s.strip()]
        
        return points[:3]  # Max 3 points
    
    def _extract_main_point(self, contribution: str) -> str:
        """Extract main point from contribution."""
        return self._summarize_contribution(contribution)
    
    def _extract_arguments(self, contribution: str) -> List[str]:
        """Extract supporting arguments."""
        return self._extract_key_points(contribution)
    
    def _extract_questions(self, contribution: str) -> List[str]:
        """Extract questions from contribution."""
        questions = []
        sentences = contribution.split('.')
        
        for sentence in sentences:
            if '?' in sentence:
                questions.append(sentence.strip() + '?')
        
        return questions
    
    def _extract_challenged_assumptions(
        self,
        contribution: str,
        previous_insights: List[Dict[str, str]]
    ) -> List[str]:
        """Extract assumptions being challenged."""
        # Simplified - would use NLP to identify challenges
        challenges = []
        
        challenge_keywords = ['however', 'but', 'although', 'contrary', 'disagree', 'challenge']
        
        for keyword in challenge_keywords:
            if keyword in contribution.lower():
                challenges.append(f"Questions {keyword}-based assumption")
        
        return challenges[:2]  # Max 2 challenges