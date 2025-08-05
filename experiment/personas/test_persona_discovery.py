"""Test the persona discovery system"""

import pytest
from persona_driven_discovery import (
    PersonaDrivenDiscovery, 
    PersonaInsights,
    AppConcept,
    PerspectiveTest
)


class TestPersonaDiscovery:
    """Test persona discovery functionality"""
    
    def test_persona_insights_creation(self):
        """Test creating persona insights"""
        insights = PersonaInsights(
            name="Elena Rodriguez",
            role="Startup Founder",
            demographics={"age": 34, "location": "San Francisco"},
            daily_activities=["Team meetings", "Product planning"],
            pain_points=["Resource allocation", "Time management"],
            user_journey={
                "stages": {
                    "awareness": {"touchpoints": ["Blog posts"], "emotions": ["curious"]}
                }
            },
            goals=["Scale business", "Work-life balance"],
            tech_proficiency="advanced",
            decision_drivers=["ROI", "Efficiency"],
            budget_range="$1K-10K/month"
        )
        
        assert insights.name == "Elena Rodriguez"
        assert insights.role == "Startup Founder"
        assert len(insights.pain_points) == 2
        assert "awareness" in insights.user_journey["stages"]
        
    def test_extract_persona_insights(self):
        """Test extracting insights from text"""
        discovery = PersonaDrivenDiscovery()
        
        persona_text = """
        Name: Sarah Chen
        Age: 35
        Role: Marketing Manager at Fortune 500 company
        Location: Chicago, IL
        
        Sarah struggles with team coordination and spends time on strategic planning.
        Her goals include career advancement and improving team productivity.
        She regularly analyzes marketing data and manages campaigns.
        """
        
        insights = discovery.extract_persona_insights(persona_text)
        
        assert insights.name == "Sarah Chen"
        assert insights.role == "Marketing Manager at Fortune 500 company"
        assert insights.demographics["age"] == 35
        assert insights.demographics["location"] == "Chicago, IL"
        assert any("team coordination" in pain for pain in insights.pain_points)
        assert any("strategic planning" in activity for activity in insights.daily_activities)
        
    def test_user_journey_extraction(self):
        """Test user journey mapping"""
        discovery = PersonaDrivenDiscovery()
        
        activities = [
            "Research new tools",
            "Evaluate solutions",
            "Team meetings",
            "Performance reviews"
        ]
        pain_points = [
            "Complex workflows",
            "Integration challenges",
            "Time-consuming setup"
        ]
        
        journey = discovery._extract_user_journey(
            "test text",
            "Manager",
            activities,
            pain_points
        )
        
        assert "stages" in journey
        assert "awareness" in journey["stages"]
        assert "consideration" in journey["stages"]
        assert "critical_moments" in journey
        assert journey["journey_duration"] == "1-2 months (team evaluation)"
        
    def test_app_concept_generation(self):
        """Test generating app concepts from personas"""
        discovery = PersonaDrivenDiscovery()
        
        # Create test personas
        persona1 = PersonaInsights(
            name="Test User 1",
            role="Manager",
            demographics={},
            daily_activities=["Meetings", "Planning"],
            pain_points=["Communication bottlenecks", "Team coordination"],
            user_journey={"stages": {}},
            goals=["Improve efficiency"],
            tech_proficiency="intermediate",
            decision_drivers=["ROI"],
            budget_range="$1K/month"
        )
        
        persona2 = PersonaInsights(
            name="Test User 2",
            role="Engineer",
            demographics={},
            daily_activities=["Coding", "Reviews"],
            pain_points=["Communication gaps", "Documentation"],
            user_journey={"stages": {}},
            goals=["Better tools"],
            tech_proficiency="expert",
            decision_drivers=["Efficiency"],
            budget_range="$500/month"
        )
        
        discovery.personas = [persona1, persona2]
        
        # Generate concepts
        concepts = discovery.generate_app_concepts([persona1, persona2])
        
        assert len(concepts) > 0
        assert isinstance(concepts[0], AppConcept)
        assert concepts[0].target_personas is not None
        
    def test_perspective_validation(self):
        """Test multi-perspective validation"""
        discovery = PersonaDrivenDiscovery()
        
        # Create test app
        app = AppConcept(
            id="test_app",
            name="TestApp",
            tagline="Test tagline",
            problem_statement="Test problem",
            solution_description="Test solution",
            target_personas=["Test User 1"],
            core_features=[{"name": "Feature 1", "description": "Test feature"}],
            value_proposition="Test value",
            monetization_model="Subscription",
            differentiation="Test differentiation"
        )
        
        # Create test persona
        persona = PersonaInsights(
            name="Test User 1",
            role="Manager",
            demographics={},
            daily_activities=["Meetings"],
            pain_points=["Time management"],
            user_journey={"stages": {}},
            goals=["Efficiency"],
            tech_proficiency="intermediate",
            decision_drivers=["ROI"],
            budget_range="$1K/month"
        )
        
        # Test perspective
        test_result = discovery._test_from_perspective(app, persona, "primary")
        
        assert isinstance(test_result, PerspectiveTest)
        assert test_result.persona_name == "Test User 1"
        assert test_result.perspective_type == "primary"
        assert test_result.would_use == True
        assert test_result.perceived_value >= 0 and test_result.perceived_value <= 10
        
    def test_business_value_analysis(self):
        """Test business value calculation"""
        discovery = PersonaDrivenDiscovery()
        
        app = AppConcept(
            id="test_app",
            name="TestApp",
            tagline="Test",
            problem_statement="Problem",
            solution_description="Solution",
            target_personas=["User1", "User2"],
            core_features=[
                {"name": "Feature1", "description": "Description1"},
                {"name": "Feature2", "description": "Description2"}
            ],
            value_proposition="Value",
            monetization_model="SaaS",
            differentiation="Unique"
        )
        
        tests = [
            PerspectiveTest(
                app_id="test_app",
                persona_name="User1",
                perspective_type="primary",
                reaction="Positive",
                perceived_value=8.0,
                concerns=[],
                suggestions=[],
                would_use=True,
                would_pay=True
            ),
            PerspectiveTest(
                app_id="test_app",
                persona_name="User2",
                perspective_type="adjacent",
                reaction="Interested",
                perceived_value=6.0,
                concerns=["Price"],
                suggestions=["Free trial"],
                would_use=True,
                would_pay=False
            )
        ]
        
        business_case = discovery.analyze_business_value(app, tests)
        
        assert business_case.app_id == "test_app"
        assert business_case.market_size in ["Large ($1B+ TAM)", "Medium ($100M-1B TAM)", "Niche ($10-100M TAM)"]
        assert "conversion_rate" in business_case.revenue_potential
        assert business_case.time_to_market == "3-4 months to MVP"
        
    def test_customer_journey_mapping(self):
        """Test customer journey map creation"""
        discovery = PersonaDrivenDiscovery()
        
        persona = PersonaInsights(
            name="Test User",
            role="Manager",
            demographics={"age": 35},
            daily_activities=["Meetings", "Planning"],
            pain_points=["Time management"],
            user_journey={
                "stages": {
                    "awareness": {
                        "touchpoints": ["Blog"],
                        "emotions": ["curious"],
                        "pain_points": [],
                        "opportunities": ["Education"]
                    },
                    "consideration": {
                        "touchpoints": ["Demo"],
                        "emotions": ["hopeful"],
                        "pain_points": ["Complex pricing"],
                        "opportunities": ["Simplify"]
                    }
                }
            },
            goals=["Efficiency"],
            tech_proficiency="intermediate",
            decision_drivers=["ROI"],
            budget_range="$1K/month"
        )
        
        app = AppConcept(
            id="test_app",
            name="TestApp",
            tagline="Test",
            problem_statement="Problem",
            solution_description="Solution",
            target_personas=["Test User"],
            core_features=[{"name": "Analytics", "description": "Track and analyze data"}],
            value_proposition="Save time",
            monetization_model="SaaS",
            differentiation="AI-powered"
        )
        
        journey_map = discovery.create_customer_journey_map(persona, app)
        
        assert journey_map["persona"] == "Test User"
        assert journey_map["app"] == "TestApp"
        assert "touchpoint_analysis" in journey_map
        assert "emotion_curve" in journey_map
        assert "opportunity_map" in journey_map
        assert "cross_stage_insights" in journey_map


if __name__ == "__main__":
    pytest.main([__file__, "-v"])