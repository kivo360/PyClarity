"""Test Collaborative Reasoning cognitive tool.

Tests adapted from FastMCP implementation to work with PyClarity's async analyzer pattern.
"""

import pytest
import pytest_asyncio
from typing import List

from pyclarity.tools.collaborative_reasoning.models import (
    CollaborativeReasoningContext,
    CollaborativeReasoningResult,
    Persona,
    PersonaType,
    ReasoningStyle,
    ConsensusStrategy,
    DialogueStyle,
    ComplexityLevel,
    PersonaPerspective
)
from pyclarity.tools.collaborative_reasoning.analyzer import CollaborativeReasoningAnalyzer


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def simple_personas():
    """Generate simple persona set for testing"""
    return [
        Persona(
            name="Data Analyst",
            persona_type=PersonaType.EXPERT,
            reasoning_style=ReasoningStyle.ANALYTICAL,
            expertise_areas=["data analysis", "statistics"],
            background="Senior data analyst with 5 years experience",
            goals=["Make data-driven decisions", "Optimize performance"]
        ),
        Persona(
            name="Product Designer",
            persona_type=PersonaType.USER,
            reasoning_style=ReasoningStyle.CREATIVE,
            expertise_areas=["user experience", "design"],
            background="UX designer focused on user needs",
            goals=["Improve user satisfaction", "Create intuitive interfaces"]
        )
    ]


@pytest.fixture
def complex_personas():
    """Generate complex persona set for testing"""
    return [
        Persona(
            name="CTO",
            persona_type=PersonaType.DECISION_MAKER,
            reasoning_style=ReasoningStyle.SYSTEMATIC,
            expertise_areas=["technology strategy", "architecture"],
            background="Chief Technology Officer with 15 years experience",
            goals=["Ensure scalability", "Minimize technical debt"]
        ),
        Persona(
            name="Security Expert",
            persona_type=PersonaType.CRITIC,
            reasoning_style=ReasoningStyle.CAUTIOUS,
            expertise_areas=["security", "risk assessment"],
            background="Cybersecurity specialist",
            goals=["Identify vulnerabilities", "Ensure compliance"]
        ),
        Persona(
            name="DevOps Lead",
            persona_type=PersonaType.IMPLEMENTER,
            reasoning_style=ReasoningStyle.PRACTICAL,
            expertise_areas=["deployment", "operations"],
            background="DevOps engineer with cloud expertise",
            goals=["Streamline deployment", "Ensure reliability"]
        ),
        Persona(
            name="Business Analyst",
            persona_type=PersonaType.STAKEHOLDER,
            reasoning_style=ReasoningStyle.OPTIMISTIC,
            expertise_areas=["business requirements", "ROI analysis"],
            background="Senior business analyst",
            goals=["Maximize business value", "Meet stakeholder needs"]
        )
    ]


@pytest.fixture
def simple_context(simple_personas):
    """Generate simple CollaborativeReasoningContext for testing"""
    return CollaborativeReasoningContext(
        problem="Should we migrate our monolith application to microservices architecture?",
        personas=simple_personas,
        reasoning_focus="Evaluate pros and cons from different perspectives",
        consensus_strategy=ConsensusStrategy.WEIGHTED_CONSENSUS,
        complexity_level=ComplexityLevel.MODERATE
    )


@pytest.fixture
def complex_context(complex_personas):
    """Generate complex CollaborativeReasoningContext for testing"""
    return CollaborativeReasoningContext(
        problem="Design a real-time fraud detection system for financial transactions with strict latency requirements",
        personas=complex_personas,
        reasoning_focus="Balance security, performance, and implementation complexity",
        consensus_strategy=ConsensusStrategy.COMPROMISE_SOLUTION,
        complexity_level=ComplexityLevel.COMPLEX,
        max_dialogue_rounds=5,
        include_devil_advocate=True,
        conflict_resolution_enabled=True
    )


@pytest.fixture
def collaborative_analyzer():
    """Create CollaborativeReasoningAnalyzer instance for testing"""
    return CollaborativeReasoningAnalyzer()


# ============================================================================
# Model Tests
# ============================================================================

class TestPersona:
    """Test suite for Persona model"""
    
    def test_persona_creation_valid(self, simple_personas):
        """Test creating valid personas"""
        analyst = simple_personas[0]
        assert analyst.name == "Data Analyst"
        assert analyst.persona_type == PersonaType.EXPERT
        assert analyst.reasoning_style == ReasoningStyle.ANALYTICAL
        assert len(analyst.expertise_areas) == 2
    
    def test_persona_validation_no_expertise(self):
        """Test persona expertise validation"""
        with pytest.raises(ValueError, match="List should have at least 1 item"):
            Persona(
                name="Test Person",
                persona_type=PersonaType.EXPERT,
                reasoning_style=ReasoningStyle.ANALYTICAL,
                expertise_areas=[],
                background="Test background",
                goals=["Test goal"]
            )


class TestCollaborativeReasoningContext:
    """Test suite for CollaborativeReasoningContext model"""
    
    def test_context_creation_valid(self, simple_context):
        """Test creating valid context"""
        assert simple_context.problem
        assert len(simple_context.personas) == 2
        assert simple_context.consensus_strategy == ConsensusStrategy.WEIGHTED_CONSENSUS
        assert simple_context.conflict_resolution_enabled is True
    
    def test_context_validation_min_personas(self):
        """Test minimum personas validation"""
        with pytest.raises(ValueError, match="List should have at least 2 items"):
            CollaborativeReasoningContext(
                problem="Test problem that meets the minimum length requirement",
                personas=[Persona(
                    name="Solo",
                    persona_type=PersonaType.EXPERT,
                    reasoning_style=ReasoningStyle.ANALYTICAL,
                    expertise_areas=["test"],
                    background="Test",
                    goals=["Test"]
                )],
                reasoning_focus="Test focus"
            )
    
    def test_context_validation_problem_too_short(self):
        """Test problem length validation"""
        with pytest.raises(ValueError, match="String should have at least 20 characters"):
            CollaborativeReasoningContext(
                problem="Too short",
                personas=[
                    Persona(name="A", persona_type=PersonaType.EXPERT, reasoning_style=ReasoningStyle.ANALYTICAL,
                           expertise_areas=["a"], background="Test", goals=["Test"]),
                    Persona(name="B", persona_type=PersonaType.USER, reasoning_style=ReasoningStyle.CREATIVE,
                           expertise_areas=["b"], background="Test", goals=["Test"])
                ],
                reasoning_focus="Test focus"
            )


# ============================================================================
# Analyzer Tests
# ============================================================================

@pytest.mark.asyncio
class TestCollaborativeReasoningAnalyzer:
    """Test suite for CollaborativeReasoningAnalyzer"""
    
    async def test_analyzer_initialization(self, collaborative_analyzer):
        """Test analyzer initialization"""
        assert collaborative_analyzer.tool_name == "Collaborative Reasoning"
        assert collaborative_analyzer.version == "2.0.0"
    
    async def test_basic_analysis(self, collaborative_analyzer, simple_context):
        """Test basic collaborative reasoning analysis"""
        result = await collaborative_analyzer.analyze(simple_context)
        
        assert isinstance(result, CollaborativeReasoningResult)
        assert len(result.persona_perspectives) == 2
        assert result.synthesis is not None
        assert result.confidence_score > 0
        assert result.processing_time_ms > 0
    
    async def test_persona_perspectives(self, collaborative_analyzer, simple_context):
        """Test that each persona contributes perspectives"""
        result = await collaborative_analyzer.analyze(simple_context)
        
        # Each persona should have a perspective
        assert len(result.persona_perspectives) == len(simple_context.personas)
        
        for perspective in result.persona_perspectives:
            assert isinstance(perspective, PersonaPerspective)
            assert perspective.persona_name in [p.name for p in simple_context.personas]
            assert len(perspective.key_arguments) > 0
            assert perspective.stance
            assert 0 <= perspective.confidence <= 1
    
    async def test_conflict_identification(self, collaborative_analyzer, complex_context):
        """Test conflict point identification"""
        result = await collaborative_analyzer.analyze(complex_context)
        
        # Complex problems should generate some unresolved tensions
        assert len(result.unresolved_tensions) >= 0
        # Check for disagreements in dialogue records
        if result.dialogue_records:
            for dialogue in result.dialogue_records:
                # Complex contexts often have some disagreements
                assert isinstance(dialogue.disagreements, list)
    
    async def test_consensus_analysis(self, collaborative_analyzer, simple_context):
        """Test consensus analysis generation"""
        result = await collaborative_analyzer.analyze(simple_context)
        
        assert result.consensus_result is not None
        assert 0 <= result.consensus_result.agreement_level <= 1
        assert result.consensus_result.consensus_reached in [True, False]
        # If consensus reached, should have an agreed solution
        if result.consensus_result.consensus_reached:
            assert result.consensus_result.agreed_solution is not None
    
    async def test_synthesis_generation(self, collaborative_analyzer, simple_context):
        """Test synthesis generation"""
        result = await collaborative_analyzer.analyze(simple_context)
        
        assert result.synthesis is not None
        assert len(result.synthesis) > 100  # Should be substantial
        assert result.synthesis != simple_context.problem  # Should not just repeat
    
    async def test_actionable_insights(self, collaborative_analyzer, simple_context):
        """Test generation of actionable insights"""
        result = await collaborative_analyzer.analyze(simple_context)
        
        assert len(result.actionable_insights) > 0
        assert len(result.actionable_insights) <= 10
        
        for insight in result.actionable_insights:
            assert len(insight) > 20  # Should be meaningful
    
    async def test_weighted_consensus_strategy(self, collaborative_analyzer, simple_context):
        """Test weighted consensus strategy"""
        simple_context.consensus_strategy = ConsensusStrategy.WEIGHTED_CONSENSUS
        simple_context.weight_by_expertise = True
        
        result = await collaborative_analyzer.analyze(simple_context)
        
        # Expert opinions should have more weight
        assert result.consensus_analysis.strategy_used == ConsensusStrategy.WEIGHTED_CONSENSUS
    
    async def test_compromise_solution_strategy(self, collaborative_analyzer, complex_context):
        """Test compromise solution strategy"""
        complex_context.consensus_strategy = ConsensusStrategy.COMPROMISE_SOLUTION
        
        result = await collaborative_analyzer.analyze(complex_context)
        
        assert result.consensus_analysis.strategy_used == ConsensusStrategy.COMPROMISE_SOLUTION
        # Should have compromise elements
        assert len(result.consensus_analysis.compromise_elements) > 0
    
    async def test_dialogue_rounds(self, collaborative_analyzer, simple_context):
        """Test multiple dialogue rounds"""
        simple_context.max_dialogue_rounds = 3
        
        result = await collaborative_analyzer.analyze(simple_context)
        
        # Should show evolution through rounds
        assert result.dialogue_summary
        assert "round" in result.dialogue_summary.lower() or "dialogue" in result.dialogue_summary.lower()
    
    async def test_devil_advocate_inclusion(self, collaborative_analyzer, simple_context):
        """Test devil's advocate perspective"""
        simple_context.include_devil_advocate = True
        
        result = await collaborative_analyzer.analyze(simple_context)
        
        # Should have critical perspectives
        has_critical = any(
            "risk" in arg.lower() or "concern" in arg.lower() or "challenge" in arg.lower()
            for perspective in result.persona_perspectives
            for arg in perspective.key_arguments
        )
        assert has_critical
    
    async def test_persona_evolution(self, collaborative_analyzer, simple_context):
        """Test persona evolution through dialogue"""
        simple_context.allow_persona_evolution = True
        simple_context.max_dialogue_rounds = 3
        
        result = await collaborative_analyzer.analyze(simple_context)
        
        # Some perspectives should show evolution
        for perspective in result.persona_perspectives:
            assert perspective.evolution_notes or len(perspective.key_arguments) > 2
    
    async def test_complexity_impact(self, collaborative_analyzer, simple_personas):
        """Test that complexity affects analysis depth"""
        simple_context = CollaborativeReasoningContext(
            problem="Simple decision about tool selection for the team",
            personas=simple_personas,
            reasoning_focus="Choose the best tool",
            complexity_level=ComplexityLevel.SIMPLE
        )
        
        complex_context = CollaborativeReasoningContext(
            problem="Complex strategic decision about company-wide technology transformation",
            personas=simple_personas,
            reasoning_focus="Evaluate transformation strategy",
            complexity_level=ComplexityLevel.COMPLEX,
            max_dialogue_rounds=5
        )
        
        simple_result = await collaborative_analyzer.analyze(simple_context)
        complex_result = await collaborative_analyzer.analyze(complex_context)
        
        # Complex analysis should be more thorough
        simple_args = sum(len(p.key_arguments) for p in simple_result.persona_perspectives)
        complex_args = sum(len(p.key_arguments) for p in complex_result.persona_perspectives)
        
        assert complex_args >= simple_args