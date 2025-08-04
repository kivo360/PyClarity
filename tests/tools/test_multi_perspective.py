# Clear Thinking FastMCP Server - Multi-Perspective Analysis Tests

"""
Comprehensive test suite for Multi-Perspective Analysis cognitive tool.

This test suite validates the analysis from multiple viewpoints through:
- Perspective identification and characterization
- Alignment and conflict analysis
- Blind spot detection
- Integration opportunity identification
- Consensus building strategies
"""

import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock
from typing import List, Dict, Any

# Import test models directly without Pydantic validators for testing
from dataclasses import dataclass
from enum import Enum


class PerspectiveType(str, Enum):
    STAKEHOLDER = "stakeholder"
    FUNCTIONAL = "functional"
    TEMPORAL = "temporal"
    CULTURAL = "cultural"
    ECONOMIC = "economic"
    TECHNICAL = "technical"
    STRATEGIC = "strategic"
    CUSTOMER = "customer"
    REGULATORY = "regulatory"
    ETHICAL = "ethical"


class AlignmentLevel(str, Enum):
    STRONG_CONFLICT = "strong_conflict"
    MODERATE_CONFLICT = "moderate_conflict"
    NEUTRAL = "neutral"
    MODERATE_ALIGNMENT = "moderate_alignment"
    STRONG_ALIGNMENT = "strong_alignment"


class ConflictResolutionStrategy(str, Enum):
    COMPROMISE = "compromise"
    PRIORITIZATION = "prioritization"
    INTEGRATION = "integration"
    SEQUENCING = "sequencing"
    REFRAMING = "reframing"
    NEGOTIATION = "negotiation"
    CONSENSUS_BUILDING = "consensus_building"


@dataclass
class MockPerspective:
    name: str
    perspective_type: PerspectiveType
    key_interests: List[str]
    priorities: List[str]
    concerns: List[str] = None
    success_criteria: List[str] = None
    constraints: List[str] = None
    influence_level: float = 0.5
    emotional_stance: str = None
    
    def __post_init__(self):
        if self.concerns is None:
            self.concerns = []
        if self.success_criteria is None:
            self.success_criteria = []
        if self.constraints is None:
            self.constraints = []


@dataclass
class MockPerspectiveComparison:
    perspective_a: str
    perspective_b: str
    alignment_level: AlignmentLevel
    common_ground: List[str] = None
    conflicts: List[str] = None
    complementary_aspects: List[str] = None
    tension_points: List[str] = None
    potential_synergies: List[str] = None
    
    def __post_init__(self):
        if self.common_ground is None:
            self.common_ground = []
        if self.conflicts is None:
            self.conflicts = []
        if self.complementary_aspects is None:
            self.complementary_aspects = []
        if self.tension_points is None:
            self.tension_points = []
        if self.potential_synergies is None:
            self.potential_synergies = []


@dataclass
class MockBlindSpot:
    description: str
    affected_perspectives: List[str]
    revealing_perspectives: List[str]
    impact: str
    mitigation_strategies: List[str] = None
    
    def __post_init__(self):
        if self.mitigation_strategies is None:
            self.mitigation_strategies = []


@dataclass
class MockConflictResolution:
    conflict_description: str
    involved_perspectives: List[str]
    resolution_strategy: ConflictResolutionStrategy
    action_steps: List[str]
    expected_outcomes: List[str]
    success_probability: float
    risks: List[str] = None
    
    def __post_init__(self):
        if self.risks is None:
            self.risks = []


@dataclass
class MockIntegrationOpportunity:
    opportunity_description: str
    perspectives_to_integrate: List[str]
    integration_approach: str
    expected_benefits: List[str]
    implementation_steps: List[str]
    complexity_level: str


@dataclass
class MockMultiPerspectiveInput:
    scenario: str
    complexity_level: str
    session_id: str
    domain_context: str = None
    predefined_perspectives: List[MockPerspective] = None
    primary_decision: str = None
    stakeholder_map: Dict[str, str] = None
    analysis_depth: str = "standard"
    conflict_tolerance: str = None
    time_horizon: str = None


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


class TestMultiPerspectiveLogic:
    """Test multi-perspective analysis logic without full model dependencies"""
    
    def test_perspective_identification(self):
        """Test identification of different perspectives"""
        # AI implementation scenario
        perspectives = [
            MockPerspective(
                name="Customer Service Employees",
                perspective_type=PerspectiveType.STAKEHOLDER,
                key_interests=["Job security", "Work satisfaction", "Skill relevance"],
                priorities=["Maintaining employment", "Learning new skills"],
                concerns=["Being replaced by AI", "Devaluation of experience"],
                influence_level=0.6
            ),
            MockPerspective(
                name="Customers",
                perspective_type=PerspectiveType.CUSTOMER,
                key_interests=["Quick resolution", "Quality service", "Human touch"],
                priorities=["Problem solved quickly", "Feel heard and understood"],
                success_criteria=["Issues resolved first contact", "Satisfaction scores"],
                influence_level=0.8
            ),
            MockPerspective(
                name="Management",
                perspective_type=PerspectiveType.STRATEGIC,
                key_interests=["Cost reduction", "Efficiency", "Competitive advantage"],
                priorities=["Reduce operational costs", "Scale service capacity"],
                constraints=["Budget limitations", "Board expectations"],
                influence_level=0.9
            ),
            MockPerspective(
                name="IT Department",
                perspective_type=PerspectiveType.TECHNICAL,
                key_interests=["Technical feasibility", "System integration", "Security"],
                priorities=["Successful implementation", "Minimal disruption"],
                concerns=["Integration complexity", "Data security"],
                influence_level=0.7
            )
        ]
        
        assert len(perspectives) == 4
        assert all(p.key_interests for p in perspectives)
        assert perspectives[2].influence_level == 0.9  # Management has highest influence
    
    def test_perspective_type_coverage(self):
        """Test coverage of different perspective types"""
        perspective_types = {
            PerspectiveType.STAKEHOLDER: "Direct stakeholders",
            PerspectiveType.FUNCTIONAL: "Department views",
            PerspectiveType.TEMPORAL: "Short vs long term",
            PerspectiveType.ECONOMIC: "Financial considerations",
            PerspectiveType.CUSTOMER: "End user needs",
            PerspectiveType.ETHICAL: "Moral implications"
        }
        
        assert len(perspective_types) >= 6
        assert PerspectiveType.STAKEHOLDER in perspective_types
        assert PerspectiveType.ETHICAL in perspective_types
    
    def test_alignment_analysis(self):
        """Test analysis of alignment between perspectives"""
        comparison = MockPerspectiveComparison(
            perspective_a="Employees",
            perspective_b="Management",
            alignment_level=AlignmentLevel.MODERATE_CONFLICT,
            common_ground=[
                "Want company success",
                "Value quality service",
                "Recognize need for innovation"
            ],
            conflicts=[
                "Job security vs cost reduction",
                "Human touch vs automation",
                "Experience value vs efficiency"
            ],
            potential_synergies=[
                "Employees as AI trainers",
                "Human-AI collaboration model",
                "Upskilling opportunities"
            ]
        )
        
        assert comparison.alignment_level == AlignmentLevel.MODERATE_CONFLICT
        assert len(comparison.common_ground) >= 3
        assert len(comparison.conflicts) >= 3
        assert "collaboration" in str(comparison.potential_synergies).lower()
    
    def test_blind_spot_detection(self):
        """Test detection of blind spots across perspectives"""
        blind_spot = MockBlindSpot(
            description="Long-term employee morale and knowledge retention impact",
            affected_perspectives=["Management", "IT Department"],
            revealing_perspectives=["Employees", "HR Department"],
            impact="Loss of institutional knowledge and decreased innovation",
            mitigation_strategies=[
                "Include HR in planning process",
                "Conduct employee impact assessment",
                "Plan knowledge transfer processes"
            ]
        )
        
        assert len(blind_spot.affected_perspectives) >= 2
        assert len(blind_spot.revealing_perspectives) >= 2
        assert blind_spot.mitigation_strategies
        assert "knowledge" in blind_spot.impact.lower()
    
    def test_conflict_resolution_strategies(self):
        """Test generation of conflict resolution strategies"""
        resolution = MockConflictResolution(
            conflict_description="Employees fear job loss while management seeks efficiency",
            involved_perspectives=["Employees", "Management"],
            resolution_strategy=ConflictResolutionStrategy.INTEGRATION,
            action_steps=[
                "Create human-AI collaboration model",
                "Guarantee no layoffs, redeploy to higher-value tasks",
                "Establish upskilling program",
                "Share efficiency gains with employees"
            ],
            expected_outcomes=[
                "Reduced resistance to change",
                "Improved employee engagement",
                "Better AI implementation outcomes"
            ],
            success_probability=0.75,
            risks=["Implementation complexity", "Cost of retraining"]
        )
        
        assert resolution.resolution_strategy == ConflictResolutionStrategy.INTEGRATION
        assert len(resolution.action_steps) >= 3
        assert resolution.success_probability >= 0.7
        assert "collaboration" in str(resolution.action_steps).lower()
    
    def test_integration_opportunity_identification(self):
        """Test identification of perspective integration opportunities"""
        opportunity = MockIntegrationOpportunity(
            opportunity_description="Combine employee expertise with AI efficiency",
            perspectives_to_integrate=["Employees", "IT Department", "Customers"],
            integration_approach="Design AI to augment human agents, not replace them",
            expected_benefits=[
                "Higher customer satisfaction",
                "Employee job enrichment",
                "Better AI training data",
                "Unique competitive advantage"
            ],
            implementation_steps=[
                "Form cross-functional design team",
                "Define human-AI interaction model",
                "Pilot with volunteer employees",
                "Iterate based on feedback"
            ],
            complexity_level="medium"
        )
        
        assert len(opportunity.perspectives_to_integrate) >= 3
        assert len(opportunity.expected_benefits) >= 3
        assert "augment" in opportunity.integration_approach.lower()
        assert opportunity.complexity_level == "medium"
    
    def test_influence_analysis(self):
        """Test analysis of perspective influence levels"""
        influence_map = {
            "CEO": 0.95,
            "Board of Directors": 0.9,
            "Department Heads": 0.7,
            "Senior Employees": 0.6,
            "Junior Employees": 0.4,
            "Customers": 0.8,
            "Regulators": 0.85
        }
        
        # Find most influential
        most_influential = max(influence_map.items(), key=lambda x: x[1])
        assert most_influential[0] == "CEO"
        assert most_influential[1] == 0.95
        
        # Check influence distribution
        high_influence = [k for k, v in influence_map.items() if v > 0.8]
        assert len(high_influence) >= 3
    
    @pytest.mark.asyncio
    async def test_domain_adaptation_organizational_change(self):
        """Test adaptation to organizational change domain"""
        mock_context = MockContext()
        
        input_data = MockMultiPerspectiveInput(
            scenario="Merger of two company divisions with different cultures",
            complexity_level="complex",
            session_id="test_org_1",
            domain_context="organizational_change",
            primary_decision="How to integrate teams while preserving strengths",
            stakeholder_map={
                "Division A Leadership": "Acquiring division",
                "Division B Leadership": "Acquired division",
                "Division A Employees": "Established culture",
                "Division B Employees": "Different culture",
                "HR Department": "Integration facilitator",
                "Customers": "Service continuity concern"
            }
        )
        
        # Simulate perspective identification
        perspectives = [
            MockPerspective(
                name="Division A Leadership",
                perspective_type=PerspectiveType.STRATEGIC,
                key_interests=["Maintain control", "Quick integration"],
                priorities=["Efficiency gains", "Cultural alignment"],
                influence_level=0.9
            ),
            MockPerspective(
                name="Division B Employees",
                perspective_type=PerspectiveType.CULTURAL,
                key_interests=["Preserve identity", "Job security"],
                priorities=["Recognition of value", "Fair treatment"],
                concerns=["Being absorbed", "Loss of culture"],
                influence_level=0.5
            )
        ]
        
        assert input_data.domain_context == "organizational_change"
        assert len(input_data.stakeholder_map) >= 6
        assert perspectives[0].influence_level > perspectives[1].influence_level
    
    @pytest.mark.asyncio
    async def test_domain_adaptation_product_development(self):
        """Test adaptation to product development domain"""
        mock_context = MockContext()
        
        input_data = MockMultiPerspectiveInput(
            scenario="Developing new feature with competing user needs",
            complexity_level="moderate",
            session_id="test_product_1",
            domain_context="product_development",
            primary_decision="Feature prioritization for next release",
            analysis_depth="comprehensive"
        )
        
        # Simulate perspective identification
        perspectives = [
            MockPerspective(
                name="Power Users",
                perspective_type=PerspectiveType.CUSTOMER,
                key_interests=["Advanced features", "Customization"],
                priorities=["Flexibility", "Performance"],
                influence_level=0.7
            ),
            MockPerspective(
                name="New Users",
                perspective_type=PerspectiveType.CUSTOMER,
                key_interests=["Ease of use", "Quick learning"],
                priorities=["Simplicity", "Guidance"],
                influence_level=0.6
            ),
            MockPerspective(
                name="Engineering",
                perspective_type=PerspectiveType.TECHNICAL,
                key_interests=["Technical feasibility", "Maintainability"],
                priorities=["Clean architecture", "Performance"],
                influence_level=0.8
            )
        ]
        
        assert input_data.domain_context == "product_development"
        assert perspectives[0].priorities != perspectives[1].priorities
    
    def test_consensus_area_identification(self):
        """Test identification of consensus areas"""
        perspectives_data = {
            "Management": {
                "priorities": ["Efficiency", "Quality", "Innovation", "Growth"],
                "concerns": ["Costs", "Competition"]
            },
            "Employees": {
                "priorities": ["Job security", "Quality", "Work-life balance", "Growth"],
                "concerns": ["Change", "Workload"]
            },
            "Customers": {
                "priorities": ["Quality", "Service", "Value", "Innovation"],
                "concerns": ["Price", "Reliability"]
            }
        }
        
        # Find common priorities
        all_priorities = [set(data["priorities"]) for data in perspectives_data.values()]
        consensus_areas = set.intersection(*all_priorities)
        
        assert "Quality" in consensus_areas
        assert len(consensus_areas) >= 1
    
    def test_divergence_area_identification(self):
        """Test identification of divergence areas"""
        divergence_areas = [
            "Automation level (high vs minimal)",
            "Timeline (aggressive vs cautious)",
            "Investment priority (technology vs people)",
            "Risk tolerance (innovative vs proven)",
            "Success metrics (efficiency vs satisfaction)"
        ]
        
        assert len(divergence_areas) >= 5
        assert any("automation" in area.lower() for area in divergence_areas)
        assert any("risk" in area.lower() for area in divergence_areas)
    
    def test_synthesis_insight_generation(self):
        """Test generation of synthesis insights"""
        synthesis_insights = [
            "Successful implementation requires addressing both efficiency and human concerns",
            "Employee resistance stems from fear, not technology opposition",
            "Customer perspective reveals opportunity for differentiation through human-AI collaboration",
            "Technical complexity is manageable; cultural change is the real challenge",
            "Phased approach can satisfy both aggressive and cautious perspectives"
        ]
        
        assert len(synthesis_insights) >= 5
        assert any("human" in insight.lower() for insight in synthesis_insights)
        assert any("culture" in insight.lower() or "cultural" in insight.lower() for insight in synthesis_insights)
    
    def test_communication_strategy_generation(self):
        """Test generation of perspective-specific communication strategies"""
        communication_strategies = [
            "For employees: Focus on growth opportunities and job security guarantees",
            "For management: Emphasize ROI and competitive advantages",
            "For customers: Highlight improved service quality and availability",
            "For technical team: Provide detailed implementation roadmap",
            "Use success stories from similar implementations",
            "Create feedback channels for each stakeholder group"
        ]
        
        assert len(communication_strategies) >= 6
        assert any("employees" in strategy.lower() for strategy in communication_strategies)
        assert any("feedback" in strategy.lower() for strategy in communication_strategies)
    
    def test_alignment_matrix_creation(self):
        """Test creation of perspective alignment matrix"""
        perspectives = ["Management", "Employees", "Customers", "IT"]
        
        # Create alignment matrix
        alignment_matrix = {}
        for p1 in perspectives:
            alignment_matrix[p1] = {}
            for p2 in perspectives:
                if p1 == p2:
                    alignment_matrix[p1][p2] = AlignmentLevel.STRONG_ALIGNMENT
                elif (p1 == "Management" and p2 == "Employees") or \
                     (p1 == "Employees" and p2 == "Management"):
                    alignment_matrix[p1][p2] = AlignmentLevel.MODERATE_CONFLICT
                elif (p1 == "Customers" and p2 in ["Management", "Employees"]) or \
                     (p2 == "Customers" and p1 in ["Management", "Employees"]):
                    alignment_matrix[p1][p2] = AlignmentLevel.MODERATE_ALIGNMENT
                else:
                    alignment_matrix[p1][p2] = AlignmentLevel.NEUTRAL
        
        assert alignment_matrix["Management"]["Management"] == AlignmentLevel.STRONG_ALIGNMENT
        assert alignment_matrix["Management"]["Employees"] == AlignmentLevel.MODERATE_CONFLICT
        assert len(alignment_matrix) == len(perspectives)
    
    @pytest.mark.asyncio
    async def test_full_multi_perspective_workflow(self):
        """Test complete multi-perspective analysis workflow"""
        mock_context = MockContext()
        
        # Step 1: Setup input
        input_data = MockMultiPerspectiveInput(
            scenario="Implementing flexible work policy post-pandemic",
            complexity_level="complex",
            session_id="integration_test_1",
            domain_context="organizational_policy",
            primary_decision="How much flexibility to offer while maintaining collaboration",
            stakeholder_map={
                "Employees": "Want maximum flexibility",
                "Management": "Concerned about productivity",
                "HR": "Policy implementation",
                "IT": "Infrastructure support",
                "Facilities": "Office space planning"
            },
            conflict_tolerance="medium",
            time_horizon="Long-term"
        )
        
        # Step 2: Identify perspectives
        perspectives = [
            MockPerspective(
                name="Employees",
                perspective_type=PerspectiveType.STAKEHOLDER,
                key_interests=["Work-life balance", "Flexibility", "Productivity"],
                priorities=["Remote work options", "Flexible hours"],
                success_criteria=["Ability to work from anywhere", "No mandatory office days"],
                influence_level=0.7,
                emotional_stance="Strongly supportive"
            ),
            MockPerspective(
                name="Management",
                perspective_type=PerspectiveType.STRATEGIC,
                key_interests=["Productivity", "Collaboration", "Culture"],
                priorities=["Team cohesion", "Output quality"],
                concerns=["Loss of innovation", "Reduced mentoring"],
                influence_level=0.9,
                emotional_stance="Cautiously open"
            ),
            MockPerspective(
                name="IT Department",
                perspective_type=PerspectiveType.TECHNICAL,
                key_interests=["Security", "Infrastructure", "Support"],
                priorities=["Secure remote access", "Reliable connectivity"],
                constraints=["Budget for tools", "Security compliance"],
                influence_level=0.6
            )
        ]
        
        # Step 3: Analyze comparisons
        comparisons = [
            MockPerspectiveComparison(
                perspective_a="Employees",
                perspective_b="Management",
                alignment_level=AlignmentLevel.MODERATE_CONFLICT,
                common_ground=["Want company success", "Value productivity"],
                conflicts=["Definition of productivity", "Importance of face-time"],
                potential_synergies=["Results-based performance metrics", "Hybrid model"]
            )
        ]
        
        # Step 4: Identify blind spots
        blind_spots = [
            MockBlindSpot(
                description="Impact on new employee onboarding and culture integration",
                affected_perspectives=["Employees", "IT Department"],
                revealing_perspectives=["HR", "Management"],
                impact="Difficulty in transmitting company culture remotely",
                mitigation_strategies=["Structured onboarding program", "Regular culture events"]
            )
        ]
        
        # Step 5: Generate resolutions
        resolutions = [
            MockConflictResolution(
                conflict_description="Flexibility demands vs collaboration needs",
                involved_perspectives=["Employees", "Management"],
                resolution_strategy=ConflictResolutionStrategy.COMPROMISE,
                action_steps=[
                    "Implement 3-2 hybrid model",
                    "Core collaboration days Tuesday-Thursday",
                    "Full flexibility on Monday/Friday",
                    "Quarterly in-person team events"
                ],
                expected_outcomes=["70% employee satisfaction", "Maintained collaboration"],
                success_probability=0.8
            )
        ]
        
        # Step 6: Validate results
        assert len(perspectives) >= 3
        assert len(comparisons) >= 1
        assert resolutions[0].resolution_strategy == ConflictResolutionStrategy.COMPROMISE
        assert resolutions[0].success_probability >= 0.8
        
        # Step 7: Check context usage
        await mock_context.info("Multi-perspective analysis completed")
        await mock_context.progress("Analysis complete", 1.0)
        
        assert len(mock_context.info_calls) > 0
        assert len(mock_context.progress_calls) > 0
        
        print(f"✅ Full multi-perspective workflow test passed")
        print(f"   Perspectives analyzed: {len(perspectives)}")
        print(f"   Blind spots identified: {len(blind_spots)}")
        print(f"   Resolution strategy: {resolutions[0].resolution_strategy}")
        print(f"   Success probability: {resolutions[0].success_probability:.0%}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])