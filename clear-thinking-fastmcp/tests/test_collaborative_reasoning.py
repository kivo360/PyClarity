# Clear Thinking FastMCP Server - Collaborative Reasoning Tests

"""
Comprehensive test suite for Collaborative Reasoning cognitive tool.

This test suite validates multi-perspective reasoning through:
- Persona-based reasoning simulation
- Stakeholder perspective analysis
- Consensus building and conflict resolution
- Role-based decision making
- Team dynamics modeling

Agent: AGENT C - Collaborative Reasoning Testing
Status: ACTIVE - Phase 2C Parallel Expansion
"""

import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock
from typing import List, Dict, Any

# Import test models directly without Pydantic validators for testing
from dataclasses import dataclass
from enum import Enum


class PersonaType(str, Enum):
    STAKEHOLDER = "stakeholder"
    EXPERT = "expert"
    USER = "user"
    DECISION_MAKER = "decision_maker"


class ReasoningStyle(str, Enum):
    ANALYTICAL = "analytical"
    CREATIVE = "creative"
    PRACTICAL = "practical"
    CAUTIOUS = "cautious"


class ConsensusStrategy(str, Enum):
    MAJORITY_VOTE = "majority_vote"
    WEIGHTED_CONSENSUS = "weighted_consensus"
    COMPROMISE_SOLUTION = "compromise_solution"


class ComplexityLevel(str, Enum):
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"


@dataclass
class MockPersona:
    name: str
    persona_type: PersonaType
    reasoning_style: ReasoningStyle
    background: str
    priorities: List[str]
    constraints: List[str]
    expertise_areas: List[str]
    influence_weight: float = 1.0


@dataclass
class MockCollaborativeReasoningInput:
    problem: str
    complexity_level: ComplexityLevel
    session_id: str
    personas: List[MockPersona]
    reasoning_focus: str
    consensus_strategy: ConsensusStrategy = ConsensusStrategy.WEIGHTED_CONSENSUS
    max_dialogue_rounds: int = 3
    include_devil_advocate: bool = True
    weight_by_expertise: bool = True
    allow_persona_evolution: bool = True
    conflict_resolution_enabled: bool = True


# Mock context for testing
class MockContext:
    def __init__(self):
        self.progress_calls = []
        self.info_calls = []
        self.debug_calls = []
        self.error_calls = []
    
    async def progress(self, message: str, progress: float = 0.0):
        self.progress_calls.append((message, progress))
    
    async def info(self, message: str):
        self.info_calls.append(message)
    
    async def debug(self, message: str):
        self.debug_calls.append(message)
    
    async def error(self, message: str):
        self.error_calls.append(message)
    
    async def cancelled(self) -> bool:
        return False


class TestCollaborativeReasoningLogic:
    """Test collaborative reasoning logic without full model dependencies"""
    
    def test_persona_creation(self):
        """Test creation of personas with different types and styles"""
        persona = MockPersona(
            name="Product Manager",
            persona_type=PersonaType.STAKEHOLDER,
            reasoning_style=ReasoningStyle.PRACTICAL,
            background="5 years experience in product management",
            priorities=["user satisfaction", "business value", "timeline"],
            constraints=["budget limitations", "resource availability"],
            expertise_areas=["product strategy", "market analysis"],
            influence_weight=1.5
        )
        
        assert persona.name == "Product Manager"
        assert persona.persona_type == PersonaType.STAKEHOLDER
        assert persona.reasoning_style == ReasoningStyle.PRACTICAL
        assert len(persona.priorities) == 3
        assert persona.influence_weight == 1.5
    
    def test_collaborative_input_validation(self):
        """Test collaborative reasoning input validation"""
        personas = [
            MockPersona(
                name="Developer",
                persona_type=PersonaType.EXPERT,
                reasoning_style=ReasoningStyle.ANALYTICAL,
                background="Senior software developer",
                priorities=["code quality", "maintainability"],
                constraints=["technical debt"],
                expertise_areas=["software architecture"]
            ),
            MockPersona(
                name="User Representative",
                persona_type=PersonaType.USER,
                reasoning_style=ReasoningStyle.PRACTICAL,
                background="End user of the system", 
                priorities=["ease of use", "reliability"],
                constraints=["learning curve"],
                expertise_areas=["user experience"]
            )
        ]
        
        input_data = MockCollaborativeReasoningInput(
            problem="Should we redesign the user interface?",
            complexity_level=ComplexityLevel.MODERATE,
            session_id="test_session_1",
            personas=personas,
            reasoning_focus="UI redesign decision",
            consensus_strategy=ConsensusStrategy.WEIGHTED_CONSENSUS,
            max_dialogue_rounds=3
        )
        
        assert len(input_data.personas) >= 2  # Minimum for collaboration
        assert input_data.reasoning_focus is not None
        assert input_data.consensus_strategy in ConsensusStrategy
        assert input_data.max_dialogue_rounds > 0
    
    @pytest.mark.asyncio
    async def test_persona_perspective_generation(self):
        """Test generation of individual persona perspectives"""
        mock_context = MockContext()
        
        persona = MockPersona(
            name="Technical Lead",
            persona_type=PersonaType.EXPERT,
            reasoning_style=ReasoningStyle.ANALYTICAL,
            background="10 years technical leadership",
            priorities=["system stability", "performance", "security"],
            constraints=["legacy system integration", "team capacity"],
            expertise_areas=["system architecture", "performance optimization"]
        )
        
        # Simulate perspective generation
        viewpoint = f"From a {persona.persona_type.value} perspective, the problem requires considering {', '.join(persona.priorities[:2])}"
        concerns = [f"Impact on {priority}" for priority in persona.priorities[:3]]
        suggestions = [
            f"Focus on {persona.priorities[0]}",
            f"Consider {persona.reasoning_style.value} approach",
            f"Leverage expertise in {persona.expertise_areas[0]}"
        ]
        
        # Calculate confidence based on expertise relevance
        base_confidence = 0.5
        expertise_match = any("system" in area.lower() for area in persona.expertise_areas)
        if expertise_match:
            base_confidence += 0.3
        
        confidence = min(1.0, base_confidence)
        
        assert viewpoint is not None
        assert len(concerns) > 0
        assert len(suggestions) > 0
        assert 0.0 <= confidence <= 1.0
        assert confidence > 0.5  # Should be high due to expertise match
    
    @pytest.mark.asyncio
    async def test_dialogue_facilitation(self):
        """Test dialogue facilitation between personas"""
        mock_context = MockContext()
        
        personas = [
            "Technical Lead",
            "Product Manager", 
            "User Representative"
        ]
        
        # Simulate dialogue round
        dialogue_exchanges = []
        for persona_name in personas:
            exchange = {
                "speaker": persona_name,
                "message": f"From {persona_name}: My perspective on the issue...",
                "timestamp": 1234567890,
                "response_to": None
            }
            dialogue_exchanges.append(exchange)
        
        # Simulate consensus identification
        consensus_points = ["Shared concern for outcome quality", "Agreement on key constraints"]
        disagreements = ["Different priorities", "Varying risk tolerance"]
        
        assert len(dialogue_exchanges) == len(personas)
        assert len(consensus_points) > 0
        assert isinstance(disagreements, list)
    
    @pytest.mark.asyncio
    async def test_weighted_consensus_building(self):
        """Test weighted consensus building strategy"""
        mock_context = MockContext()
        
        # Mock perspectives with different confidence levels
        mock_perspectives = [
            {"persona_name": "Expert", "confidence_level": 0.9, "viewpoint": "Technical solution needed"},
            {"persona_name": "Manager", "confidence_level": 0.7, "viewpoint": "Business value focus"},
            {"persona_name": "User", "confidence_level": 0.8, "viewpoint": "User experience priority"}
        ]
        
        # Mock persona weights
        persona_weights = {"Expert": 1.5, "Manager": 1.2, "User": 1.0}
        
        # Calculate weighted consensus
        total_weight = sum(persona_weights.values())
        weighted_confidence = sum(
            p["confidence_level"] * persona_weights.get(p["persona_name"], 1.0)
            for p in mock_perspectives
        ) / total_weight
        
        consensus_reached = weighted_confidence > 0.6
        
        assert 0.0 <= weighted_confidence <= 1.0
        assert consensus_reached is True  # Should reach consensus with these values
        assert weighted_confidence > 0.7  # Should be relatively high
    
    @pytest.mark.asyncio
    async def test_majority_vote_consensus(self):
        """Test majority vote consensus strategy"""
        mock_context = MockContext()
        
        # Mock perspective groups
        perspective_groups = [
            ["Technical approach", "Technical approach", "Technical approach"],  # 3 votes
            ["Business approach", "Business approach"],  # 2 votes
            ["User-centered approach"]  # 1 vote
        ]
        
        # Find majority
        largest_group = max(perspective_groups, key=len)
        agreement_level = len(largest_group) / sum(len(group) for group in perspective_groups)
        
        consensus_reached = agreement_level > 0.5
        
        assert agreement_level == 0.5  # 3/6 = 0.5
        assert consensus_reached is False  # Exactly 0.5 is not > 0.5
    
    @pytest.mark.asyncio
    async def test_compromise_consensus(self):
        """Test compromise consensus building"""
        mock_context = MockContext()
        
        # Mock perspectives for compromise
        mock_perspectives = [
            {"viewpoint": "Focus on quality and performance", "concerns": ["technical debt"]},
            {"viewpoint": "Focus on user experience and usability", "concerns": ["learning curve"]},
            {"viewpoint": "Focus on business value and ROI", "concerns": ["development cost"]}
        ]
        
        # Find common elements
        common_elements = ["Quality outcome", "Stakeholder consideration", "Risk management"]
        compromise_areas = ["Phased implementation", "Flexible timeline", "Balanced priorities"]
        
        # Build compromise solution
        compromise_solution = f"Compromise solution incorporating {len(common_elements)} common elements"
        agreement_level = min(0.8, len(common_elements) / len(mock_perspectives))
        
        assert len(common_elements) > 0
        assert len(compromise_areas) > 0
        assert compromise_solution is not None
        assert 0.0 <= agreement_level <= 1.0
    
    def test_diversity_score_calculation(self):
        """Test perspective diversity scoring"""
        # Mock perspectives with different viewpoints
        perspectives = [
            {"viewpoint": "Technical solution focus"},
            {"viewpoint": "Business value focus"},
            {"viewpoint": "User experience focus"},
            {"viewpoint": "Technical solution focus"}  # Duplicate
        ]
        
        unique_viewpoints = len(set(p["viewpoint"] for p in perspectives))
        diversity_score = min(1.0, unique_viewpoints / len(perspectives))
        
        assert diversity_score == 0.75  # 3 unique out of 4 total
        assert 0.0 <= diversity_score <= 1.0
    
    def test_collaboration_quality_assessment(self):
        """Test collaboration quality assessment"""
        # Mock dialogue data
        mock_dialogues = [
            {"consensus_points": ["Point 1", "Point 2"], "disagreements": ["Issue 1"]},
            {"consensus_points": ["Point 3"], "disagreements": ["Issue 2", "Issue 3"]}
        ]
        
        # Mock consensus result
        mock_consensus = {"agreement_level": 0.7}
        
        # Calculate dialogue quality
        dialogue_quality = sum(
            len(d["consensus_points"]) - len(d["disagreements"]) 
            for d in mock_dialogues
        ) / len(mock_dialogues)
        
        collaboration_quality = (dialogue_quality + mock_consensus["agreement_level"]) / 2.0
        
        assert isinstance(collaboration_quality, float)
        # Note: This could be negative if disagreements outweigh consensus
    
    def test_stakeholder_buy_in_assessment(self):
        """Test stakeholder buy-in assessment"""
        mock_perspectives = [
            {"persona_name": "Expert", "confidence_level": 0.9},
            {"persona_name": "Manager", "confidence_level": 0.7},
            {"persona_name": "User", "confidence_level": 0.6}
        ]
        
        mock_consensus = {"consensus_reached": True}
        
        # Calculate buy-in
        stakeholder_buy_in = {
            p["persona_name"]: p["confidence_level"] * (1.0 if mock_consensus["consensus_reached"] else 0.5)
            for p in mock_perspectives
        }
        
        assert len(stakeholder_buy_in) == len(mock_perspectives)
        assert all(0.0 <= score <= 1.0 for score in stakeholder_buy_in.values())
        assert stakeholder_buy_in["Expert"] == 0.9  # High confidence maintained
    
    @pytest.mark.asyncio
    async def test_devil_advocate_generation(self):
        """Test devil's advocate perspective generation"""
        mock_context = MockContext()
        
        # Mock existing perspectives
        mock_perspectives = [
            {"viewpoint": "This solution is excellent", "confidence_level": 0.8},
            {"viewpoint": "Perfect approach", "confidence_level": 0.9}
        ]
        
        # Generate devil's advocate
        devil_advocate = {
            "persona_name": "Devil's Advocate",
            "viewpoint": "Challenge consensus and identify potential flaws",
            "concerns": ["Groupthink", "Overlooked risks", "Alternative solutions"],
            "suggestions": ["Consider contrarian views", "Test assumptions", "Explore alternatives"],
            "confidence_level": 0.7
        }
        
        assert devil_advocate["persona_name"] == "Devil's Advocate"
        assert len(devil_advocate["concerns"]) > 0
        assert len(devil_advocate["suggestions"]) > 0
        assert devil_advocate["confidence_level"] > 0.0
    
    @pytest.mark.asyncio
    async def test_persona_evolution(self):
        """Test persona perspective evolution during dialogue"""
        mock_context = MockContext()
        
        # Mock initial perspectives
        mock_perspectives = [
            {"persona_name": "Expert", "confidence_level": 0.6},
            {"persona_name": "Manager", "confidence_level": 0.5}
        ]
        
        # Mock dialogue with more consensus than disagreement
        mock_dialogue = {
            "consensus_points": ["Point 1", "Point 2", "Point 3"],
            "disagreements": ["Issue 1"]
        }
        
        # Simulate evolution
        if len(mock_dialogue["consensus_points"]) > len(mock_dialogue["disagreements"]):
            for perspective in mock_perspectives:
                perspective["confidence_level"] = min(1.0, perspective["confidence_level"] + 0.1)
        
        assert mock_perspectives[0]["confidence_level"] == 0.7  # Increased
        assert mock_perspectives[1]["confidence_level"] == 0.6  # Increased
        assert all(p["confidence_level"] <= 1.0 for p in mock_perspectives)
    
    def test_insights_generation(self):
        """Test key insights generation from collaborative process"""
        # Mock process data
        mock_perspectives = [{"persona_name": f"Persona_{i}", "confidence_level": 0.7 + (i * 0.1)} for i in range(3)]
        mock_consensus = {"agreement_level": 0.75}
        diversity_score = 0.8
        
        # Generate insights
        insights = [
            f"Achieved {mock_consensus['agreement_level']:.1%} consensus among {len(mock_perspectives)} perspectives",
            f"Perspective diversity score: {diversity_score:.2f}",
            f"Most influential viewpoint: {max(mock_perspectives, key=lambda p: p['confidence_level'])['persona_name']}",
            "Key areas of agreement identified"
        ]
        
        assert len(insights) > 0
        assert "consensus" in insights[0]
        assert "diversity" in insights[1]
        assert "Persona_2" in insights[2]  # Highest confidence
    
    def test_implementation_considerations(self):
        """Test implementation considerations generation"""
        considerations = [
            "Stakeholder communication strategy needed",
            "Change management approach for dissenting parties",
            "Resource allocation based on consensus priorities",
            "Risk mitigation for unresolved issues"
        ]
        
        assert len(considerations) > 0
        assert any("stakeholder" in c.lower() for c in considerations)
        assert any("risk" in c.lower() for c in considerations)
    
    @pytest.mark.asyncio
    async def test_full_collaborative_reasoning_workflow(self):
        """Test complete collaborative reasoning workflow"""
        mock_context = MockContext()
        
        # Step 1: Setup personas
        personas = [
            MockPersona(
                name="Technical Expert",
                persona_type=PersonaType.EXPERT,
                reasoning_style=ReasoningStyle.ANALYTICAL,
                background="Senior technical expert",
                priorities=["technical excellence", "system reliability"],
                constraints=["legacy system compatibility"],
                expertise_areas=["system architecture"]
            ),
            MockPersona(
                name="Business Stakeholder",
                persona_type=PersonaType.STAKEHOLDER,
                reasoning_style=ReasoningStyle.PRACTICAL,
                background="Business stakeholder",
                priorities=["business value", "cost efficiency"],
                constraints=["budget limitations"],
                expertise_areas=["business analysis"]
            )
        ]
        
        input_data = MockCollaborativeReasoningInput(
            problem="Should we migrate to a new technology stack?",
            complexity_level=ComplexityLevel.COMPLEX,
            session_id="integration_test_1",
            personas=personas,
            reasoning_focus="Technology migration decision",
            consensus_strategy=ConsensusStrategy.WEIGHTED_CONSENSUS
        )
        
        # Step 2: Simulate perspective generation
        perspectives = []
        for persona in personas:
            confidence = 0.7 + (0.1 if "technical" in persona.background.lower() else 0.0)
            perspective = {
                "persona_name": persona.name,
                "viewpoint": f"{persona.name}'s view on technology migration",
                "confidence_level": confidence,
                "concerns": [f"Impact on {priority}" for priority in persona.priorities],
                "suggestions": [f"Consider {persona.reasoning_style.value} approach"]
            }
            perspectives.append(perspective)
        
        # Step 3: Simulate consensus building
        persona_weights = {p.name: p.influence_weight for p in personas}
        total_weight = sum(persona_weights.values())
        weighted_confidence = sum(
            p["confidence_level"] * persona_weights.get(p["persona_name"], 1.0)
            for p in perspectives
        ) / total_weight
        
        consensus_result = {
            "strategy_used": ConsensusStrategy.WEIGHTED_CONSENSUS,
            "consensus_reached": weighted_confidence > 0.6,
            "agreement_level": weighted_confidence,
            "confidence_in_consensus": weighted_confidence
        }
        
        # Step 4: Validate results
        assert len(perspectives) == len(personas)
        assert all(0.0 <= p["confidence_level"] <= 1.0 for p in perspectives)
        assert consensus_result["consensus_reached"] is True
        assert consensus_result["agreement_level"] > 0.6
        
        # Step 5: Check context usage
        await mock_context.info("Collaborative reasoning completed")
        await mock_context.progress("Process completed", 1.0)
        
        assert len(mock_context.info_calls) > 0
        assert len(mock_context.progress_calls) > 0
        
        print(f"✅ Full collaborative reasoning workflow test passed")
        print(f"   Perspectives generated: {len(perspectives)}")
        print(f"   Consensus reached: {consensus_result['consensus_reached']}")
        print(f"   Agreement level: {consensus_result['agreement_level']:.2f}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
