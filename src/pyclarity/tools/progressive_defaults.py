"""
Progressive Analyzers as Default Interface

This module provides a unified interface where progressive analyzers
are used by default for all cognitive tools, with automatic session
management for single-use cases.
"""

import uuid
from typing import Any, Dict, Optional

from pyclarity.db.base import BaseSessionStore
from pyclarity.db.mental_model_store import BaseMentalModelStore
from pyclarity.db.debugging_store import BaseDebuggingStore
from pyclarity.db.collaborative_store import BaseCollaborativeStore
from pyclarity.db.decision_store import BaseDecisionStore
from pyclarity.db.metacognitive_store import BaseMetacognitiveStore
from pyclarity.db.scientific_store import BaseScientificStore
from pyclarity.db.visual_store import BaseVisualStore
from pyclarity.db.creative_store import BaseCreativeStore
from pyclarity.db.systems_store import BaseSystemsStore

# Import all progressive analyzers
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

# Import models for convenience
from pyclarity.tools.mental_models.models import MentalModelType
from pyclarity.tools.collaborative_reasoning.models import CollaborationType, SynthesisApproach
from pyclarity.tools.decision_framework.models import DecisionType, EvaluationMethod, TimePressure
from pyclarity.tools.metacognitive_monitoring.models import ThinkingMode, ReflectionDepth
from pyclarity.tools.scientific_method.models import ResearchPhase
from pyclarity.tools.visual_reasoning.models import VisualizationType, SpatialArrangement
from pyclarity.tools.creative_thinking.models import CreativeMode
from pyclarity.tools.systems_thinking.models import SystemPerspective, AnalysisFocus


class ProgressiveToolKit:
    """
    Unified interface for all cognitive tools using progressive analyzers.
    
    This class provides a simple interface where each tool method automatically
    uses the progressive analyzer, managing sessions transparently for single-use
    cases while still supporting multi-step sessions.
    """
    
    def __init__(
        self,
        session_store: BaseSessionStore,
        mental_model_store: Optional[BaseMentalModelStore] = None,
        debugging_store: Optional[BaseDebuggingStore] = None,
        collaborative_store: Optional[BaseCollaborativeStore] = None,
        decision_store: Optional[BaseDecisionStore] = None,
        metacognitive_store: Optional[BaseMetacognitiveStore] = None,
        scientific_store: Optional[BaseScientificStore] = None,
        visual_store: Optional[BaseVisualStore] = None,
        creative_store: Optional[BaseCreativeStore] = None,
        systems_store: Optional[BaseSystemsStore] = None,
    ):
        """Initialize toolkit with required stores."""
        self.session_store = session_store
        
        # Initialize analyzers for available stores
        self.mental_models = (
            ProgressiveMentalModelAnalyzer(session_store, mental_model_store)
            if mental_model_store else None
        )
        
        self.debugging = (
            ProgressiveDebuggingAnalyzer(session_store, debugging_store)
            if debugging_store else None
        )
        
        self.collaborative = (
            ProgressiveCollaborativeAnalyzer(session_store, collaborative_store)
            if collaborative_store else None
        )
        
        self.decision = (
            ProgressiveDecisionAnalyzer(session_store, decision_store)
            if decision_store else None
        )
        
        self.metacognitive = (
            ProgressiveMetacognitiveAnalyzer(session_store, metacognitive_store)
            if metacognitive_store else None
        )
        
        self.scientific = (
            ProgressiveScientificAnalyzer(session_store, scientific_store)
            if scientific_store else None
        )
        
        self.visual = (
            ProgressiveVisualAnalyzer(session_store, visual_store)
            if visual_store else None
        )
        
        self.creative = (
            ProgressiveCreativeAnalyzer(session_store, creative_store)
            if creative_store else None
        )
        
        self.systems = (
            ProgressiveSystemsAnalyzer(session_store, systems_store)
            if systems_store else None
        )
    
    async def apply_mental_model(
        self,
        problem_statement: str,
        model_type: MentalModelType = MentalModelType.FIRST_PRINCIPLES,
        context: Optional[str] = None,
        session_id: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Apply mental model analysis."""
        if not self.mental_models:
            return {"error": "Mental models analyzer not configured"}
        
        request = ProgressiveMentalModelRequest(
            session_id=session_id,
            model_type=model_type,
            problem_statement=problem_statement,
            context=context,
            **kwargs
        )
        
        response = await self.mental_models.apply_model(request)
        return response.model_dump()
    
    async def debug_issue(
        self,
        issue_description: str,
        debugging_type: str = "systematic",
        session_id: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Debug an issue systematically."""
        if not self.debugging:
            return {"error": "Debugging analyzer not configured"}
        
        request = ProgressiveDebuggingRequest(
            session_id=session_id,
            debugging_type=debugging_type,
            issue_description=issue_description,
            **kwargs
        )
        
        response = await self.debugging.analyze_issue(request)
        return response.model_dump()
    
    async def collaborate(
        self,
        topic: str,
        context: str = "",
        collaboration_type: CollaborationType = CollaborationType.CONSENSUS_BUILDING,
        session_id: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Run collaborative reasoning."""
        if not self.collaborative:
            return {"error": "Collaborative analyzer not configured"}
        
        request = ProgressiveCollaborativeRequest(
            session_id=session_id,
            collaboration_type=collaboration_type,
            topic=topic,
            context=context,
            **kwargs
        )
        
        response = await self.collaborative.collaborate(request)
        return response.model_dump()
    
    async def analyze_decision(
        self,
        decision_context: str,
        decision_type: DecisionType = DecisionType.STRATEGIC,
        session_id: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Analyze a decision."""
        if not self.decision:
            return {"error": "Decision analyzer not configured"}
        
        request = ProgressiveDecisionRequest(
            session_id=session_id,
            decision_context=decision_context,
            decision_type=decision_type,
            **kwargs
        )
        
        response = await self.decision.analyze_decision(request)
        return response.model_dump()
    
    async def monitor_thinking(
        self,
        current_thought: str,
        thinking_context: str,
        thinking_mode: ThinkingMode = ThinkingMode.ANALYTICAL,
        session_id: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Monitor metacognitive processes."""
        if not self.metacognitive:
            return {"error": "Metacognitive analyzer not configured"}
        
        request = ProgressiveMetacognitiveRequest(
            session_id=session_id,
            current_thought=current_thought,
            thinking_context=thinking_context,
            thinking_mode=thinking_mode,
            **kwargs
        )
        
        response = await self.metacognitive.monitor_thinking(request)
        return response.model_dump()
    
    async def conduct_research(
        self,
        research_question: str,
        domain: str,
        research_phase: ResearchPhase = ResearchPhase.OBSERVATION,
        session_id: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Conduct scientific research."""
        if not self.scientific:
            return {"error": "Scientific analyzer not configured"}
        
        request = ProgressiveScientificRequest(
            session_id=session_id,
            research_question=research_question,
            domain=domain,
            research_phase=research_phase,
            **kwargs
        )
        
        response = await self.scientific.conduct_research(request)
        return response.model_dump()
    
    async def analyze_visually(
        self,
        subject: str,
        context: str,
        visualization_type: VisualizationType = VisualizationType.CONCEPTUAL,
        session_id: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Analyze using visual reasoning."""
        if not self.visual:
            return {"error": "Visual analyzer not configured"}
        
        request = ProgressiveVisualRequest(
            session_id=session_id,
            subject=subject,
            context=context,
            visualization_type=visualization_type,
            **kwargs
        )
        
        response = await self.visual.analyze_visually(request)
        return response.model_dump()
    
    async def generate_ideas(
        self,
        challenge: str,
        creative_mode: CreativeMode = CreativeMode.DIVERGENT,
        session_id: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate creative ideas."""
        if not self.creative:
            return {"error": "Creative analyzer not configured"}
        
        request = ProgressiveCreativeRequest(
            session_id=session_id,
            challenge=challenge,
            creative_mode=creative_mode,
            **kwargs
        )
        
        response = await self.creative.generate_ideas(request)
        return response.model_dump()
    
    async def analyze_system(
        self,
        system_name: str,
        system_description: str,
        perspective: SystemPerspective = SystemPerspective.HOLISTIC,
        session_id: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Analyze a system."""
        if not self.systems:
            return {"error": "Systems analyzer not configured"}
        
        request = ProgressiveSystemsRequest(
            session_id=session_id,
            system_name=system_name,
            system_description=system_description,
            perspective=perspective,
            **kwargs
        )
        
        response = await self.systems.analyze_system(request)
        return response.model_dump()


def create_memory_toolkit() -> ProgressiveToolKit:
    """
    Create a simple in-memory toolkit for testing or single-use cases.
    
    This uses in-memory stores that don't persist data, useful for
    one-off analyses or testing.
    """
    from pyclarity.db.memory_stores import (
        MemorySessionStore,
        MemoryMentalModelStore,
        MemoryDebuggingStore,
        MemoryCollaborativeStore,
        MemoryDecisionStore,
        MemoryMetacognitiveStore,
        MemoryScientificStore,
        MemoryVisualStore,
        MemoryCreativeStore,
        MemorySystemsStore,
    )
    
    session_store = MemorySessionStore()
    
    return ProgressiveToolKit(
        session_store=session_store,
        mental_model_store=MemoryMentalModelStore(),
        debugging_store=MemoryDebuggingStore(),
        collaborative_store=MemoryCollaborativeStore(),
        decision_store=MemoryDecisionStore(),
        metacognitive_store=MemoryMetacognitiveStore(),
        scientific_store=MemoryScientificStore(),
        visual_store=MemoryVisualStore(),
        creative_store=MemoryCreativeStore(),
        systems_store=MemorySystemsStore(),
    )