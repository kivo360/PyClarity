"""
Persona-Driven Product Discovery System
======================================

A practical implementation that demonstrates how to:
1. Extract insights from personas
2. Generate app ideas from pain points
3. Test with multiple perspectives
4. Map business value and features
5. Create actionable roadmaps
"""

import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple

from loguru import logger


@dataclass
class PersonaInsights:
    """Extracted insights from a persona"""

    name: str
    role: str
    demographics: dict[str, Any]
    daily_activities: list[str]
    pain_points: list[str]
    user_journey: dict[str, Any]  # Maps journey stages to experiences
    goals: list[str]
    tech_proficiency: str
    decision_drivers: list[str]
    budget_range: str


@dataclass
class AppConcept:
    """App idea with full context"""

    id: str
    name: str
    tagline: str
    problem_statement: str
    solution_description: str
    target_personas: list[str]
    core_features: list[dict[str, str]]
    value_proposition: str
    monetization_model: str
    differentiation: str


@dataclass
class PerspectiveTest:
    """Testing from different viewpoints"""

    app_id: str
    persona_name: str
    perspective_type: str  # primary, adjacent, skeptical
    reaction: str
    perceived_value: float  # 0-10
    concerns: list[str]
    suggestions: list[str]
    would_use: bool
    would_pay: bool


@dataclass
class BusinessCase:
    """Business value analysis"""

    app_id: str
    market_size: str
    revenue_potential: dict[str, Any]
    cost_estimate: dict[str, Any]
    time_to_market: str
    competitive_landscape: list[str]
    risks: list[dict[str, str]]
    success_metrics: list[str]


@dataclass
class FeatureBehavior:
    """Feature to behavior mapping"""

    feature_name: str
    user_stories: list[str]
    expected_behaviors: list[str]
    system_requirements: list[str]
    success_criteria: list[str]
    edge_cases: list[str]


class PersonaDrivenDiscovery:
    """Main discovery system"""

    def __init__(self):
        self.personas: list[PersonaInsights] = []
        self.app_concepts: list[AppConcept] = []
        self.perspective_tests: list[PerspectiveTest] = []
        self.business_cases: list[BusinessCase] = []
        self.feature_behaviors: list[FeatureBehavior] = []

    def extract_persona_insights(self, persona_text: str) -> PersonaInsights:
        """Extract structured insights from persona text"""
        # Extract name (stop at newline or next field)
        name_match = re.search(r"Name:?\s*([A-Za-z\s]+?)(?:\n|Age:|$)", persona_text)
        name = name_match.group(1).strip() if name_match else "Unknown"

        # Extract role/profession
        role_patterns = [
            r"Role:?\s*([^\.]+)",
            r"Current Role:?\s*([^\.]+)",
            r"profession[^:]*:?\s*([^\.]+)",
            r"works? as (?:a |an )?([^\.]+)",
        ]
        role = "Professional"
        for pattern in role_patterns:
            match = re.search(pattern, persona_text, re.IGNORECASE)
            if match:
                role = match.group(1).strip()
                break

        # Extract demographics
        age_match = re.search(r"Age:?\s*(\d+)", persona_text)
        location_match = re.search(r"Location:?\s*([^,\n]+)", persona_text)

        demographics = {
            "age": int(age_match.group(1)) if age_match else 35,
            "location": location_match.group(1).strip() if location_match else "Urban",
            "education": self._extract_education(persona_text),
            "family": self._extract_family_status(persona_text),
        }

        # Extract activities from context
        activities = self._extract_activities(persona_text, role)

        # Extract pain points
        pain_points = self._extract_pain_points(persona_text, role)

        # Extract user journey based on activities and pain points
        user_journey = self._extract_user_journey(persona_text, role, activities, pain_points)

        # Extract goals
        goals = self._extract_goals(persona_text)

        # Determine tech proficiency
        tech_proficiency = self._assess_tech_proficiency(persona_text, role)

        # Extract decision drivers
        decision_drivers = self._extract_decision_drivers(persona_text, role)

        # Estimate budget range
        budget_range = self._estimate_budget(persona_text, role)

        return PersonaInsights(
            name=name,
            role=role,
            demographics=demographics,
            daily_activities=activities,
            pain_points=pain_points,
            user_journey=user_journey,
            goals=goals,
            tech_proficiency=tech_proficiency,
            decision_drivers=decision_drivers,
            budget_range=budget_range,
        )

    def generate_app_concepts(self, personas: list[PersonaInsights]) -> list[AppConcept]:
        """Generate app ideas from persona pain points"""
        # Analyze pain point patterns
        pain_point_clusters = self._cluster_pain_points(personas)

        app_concepts = []

        for cluster_theme, affected_personas in pain_point_clusters.items():
            # Generate app concept for this cluster
            concept = self._create_app_concept(cluster_theme, affected_personas, personas)
            app_concepts.append(concept)

        return app_concepts

    def test_with_perspectives(
        self, app: AppConcept, personas: list[PersonaInsights]
    ) -> list[PerspectiveTest]:
        """Test app concept with multiple persona perspectives"""
        tests = []

        # Primary perspective - target personas
        for persona_name in app.target_personas[:3]:
            persona = next((p for p in personas if p.name == persona_name), None)
            if persona:
                test = self._test_from_perspective(app, persona, "primary")
                tests.append(test)

        # Adjacent perspective - similar but not exact match
        adjacent_personas = self._find_adjacent_personas(app.target_personas, personas)
        for persona in adjacent_personas[:2]:
            test = self._test_from_perspective(app, persona, "adjacent")
            tests.append(test)

        # Skeptical perspective - those who might resist
        skeptical_personas = self._find_skeptical_personas(app.target_personas, personas)
        for persona in skeptical_personas[:1]:
            test = self._test_from_perspective(app, persona, "skeptical")
            tests.append(test)

        return tests

    def analyze_business_value(self, app: AppConcept, tests: list[PerspectiveTest]) -> BusinessCase:
        """Analyze business value based on app concept and testing"""
        # Calculate market size based on persona representation
        market_size = self._estimate_market_size(app, tests)

        # Revenue potential
        revenue_potential = self._calculate_revenue_potential(app, tests)

        # Cost estimation
        cost_estimate = self._estimate_costs(app)

        # Time to market
        time_to_market = self._estimate_timeline(app)

        # Competitive analysis
        competitive_landscape = self._analyze_competition(app)

        # Risk assessment
        risks = self._assess_risks(app, tests)

        # Success metrics
        success_metrics = self._define_success_metrics(app)

        return BusinessCase(
            app_id=app.id,
            market_size=market_size,
            revenue_potential=revenue_potential,
            cost_estimate=cost_estimate,
            time_to_market=time_to_market,
            competitive_landscape=competitive_landscape,
            risks=risks,
            success_metrics=success_metrics,
        )

    def map_feature_behaviors(
        self, app: AppConcept, personas: list[PersonaInsights]
    ) -> list[FeatureBehavior]:
        """Map features to expected behaviors"""
        feature_behaviors = []

        for feature in app.core_features:
            # Create user stories
            user_stories = self._create_user_stories(feature, app.target_personas, personas)

            # Define expected behaviors
            expected_behaviors = self._define_expected_behaviors(feature, personas)

            # System requirements
            system_requirements = self._define_system_requirements(feature)

            # Success criteria
            success_criteria = self._define_success_criteria(feature)

            # Edge cases
            edge_cases = self._identify_edge_cases(feature, personas)

            feature_behavior = FeatureBehavior(
                feature_name=feature["name"],
                user_stories=user_stories,
                expected_behaviors=expected_behaviors,
                system_requirements=system_requirements,
                success_criteria=success_criteria,
                edge_cases=edge_cases,
            )

            feature_behaviors.append(feature_behavior)

        return feature_behaviors

    def create_customer_journey_map(
        self, persona: PersonaInsights, app: AppConcept
    ) -> dict[str, Any]:
        """Create a detailed customer journey map for a persona using an app"""
        journey_map = {
            "persona": persona.name,
            "app": app.name,
            "journey_overview": persona.user_journey,
            "touchpoint_analysis": {},
            "emotion_curve": {},
            "opportunity_map": {},
        }

        # Analyze each journey stage
        for stage_name, stage_data in persona.user_journey["stages"].items():
            # Touchpoint analysis
            journey_map["touchpoint_analysis"][stage_name] = {
                "channels": self._identify_channels(stage_name, persona.role),
                "interactions": stage_data["touchpoints"],
                "duration": self._estimate_stage_duration(stage_name, persona.role),
                "friction_points": stage_data["pain_points"],
                "support_needs": self._identify_support_needs(
                    stage_name, stage_data["pain_points"]
                ),
            }

            # Emotion tracking
            journey_map["emotion_curve"][stage_name] = {
                "emotions": stage_data["emotions"],
                "satisfaction_level": self._calculate_satisfaction(stage_data),
                "anxiety_level": self._calculate_anxiety(stage_data),
                "confidence_level": self._calculate_confidence(
                    stage_name, persona.tech_proficiency
                ),
            }

            # Opportunity mapping
            journey_map["opportunity_map"][stage_name] = {
                "quick_wins": self._identify_quick_wins(stage_data),
                "feature_ideas": self._map_features_to_stage(app.core_features, stage_name),
                "messaging": self._create_stage_messaging(stage_name, persona.decision_drivers),
                "metrics": self._define_stage_metrics(stage_name),
            }

        # Add cross-stage insights
        journey_map["cross_stage_insights"] = {
            "drop_off_risks": self._identify_dropoff_risks(journey_map),
            "acceleration_opportunities": self._find_acceleration_points(journey_map),
            "personalization_points": self._identify_personalization_opportunities(persona),
            "competitive_differentiators": self._map_differentiators_to_journey(app, journey_map),
        }

        return journey_map

    def _identify_channels(self, stage: str, role: str) -> list[str]:
        """Identify communication channels for each stage"""
        channels = {
            "awareness": [
                "Search engines",
                "Social media",
                "Industry publications",
                "Word of mouth",
            ],
            "consideration": ["Website", "Documentation", "Demo videos", "Case studies"],
            "decision": ["Sales calls", "Free trial", "Pricing page", "Comparison tools"],
            "onboarding": ["Email", "In-app guides", "Video tutorials", "Support chat"],
            "usage": ["Product dashboard", "Email notifications", "Help center", "Community"],
            "advocacy": ["Review platforms", "Social media", "Referral program", "User community"],
        }

        # Adjust based on role
        if "enterprise" in role.lower():
            channels["decision"].extend(["RFP process", "Security review"])
        elif "developer" in role.lower():
            channels["consideration"].extend(["API docs", "GitHub"])

        return channels.get(stage, ["Website", "Email"])

    def _estimate_stage_duration(self, stage: str, role: str) -> str:
        """Estimate how long each stage takes"""
        base_durations = {
            "awareness": "1-2 weeks",
            "consideration": "2-4 weeks",
            "decision": "1-2 weeks",
            "onboarding": "1 week",
            "usage": "Ongoing",
            "advocacy": "After 3+ months",
        }

        # Adjust for role
        if "executive" in role.lower() and stage in ["consideration", "decision"]:
            return "4-8 weeks"
        if "freelance" in role.lower():
            return "1-3 days" if stage != "usage" else "Ongoing"

        return base_durations.get(stage, "Variable")

    def _identify_support_needs(self, stage: str, pain_points: list[str]) -> list[str]:
        """Identify support requirements by stage"""
        support_needs = []

        if stage == "awareness":
            support_needs = ["Educational content", "Problem validation resources"]
        elif stage == "consideration":
            support_needs = ["Comparison guides", "Technical specs", "Use case examples"]
        elif stage == "decision":
            support_needs = ["ROI calculator", "Implementation timeline", "Security documentation"]
        elif stage == "onboarding":
            support_needs = ["Setup wizard", "Migration tools", "1-on-1 onboarding"]
        elif stage == "usage":
            support_needs = ["Help documentation", "Community support", "Feature tutorials"]

        # Add based on pain points
        if any("integration" in p.lower() for p in pain_points):
            support_needs.append("Integration specialists")

        return support_needs

    def _calculate_satisfaction(self, stage_data: dict[str, Any]) -> float:
        """Calculate satisfaction level for a stage"""
        # Simple heuristic: more opportunities than pain points = higher satisfaction
        opportunities = len(stage_data.get("opportunities", []))
        pain_points = len(stage_data.get("pain_points", []))

        if pain_points == 0:
            return 8.0

        ratio = opportunities / (pain_points + opportunities)
        return round(3 + (ratio * 7), 1)  # Scale from 3 to 10

    def _calculate_anxiety(self, stage_data: dict[str, Any]) -> float:
        """Calculate anxiety level for a stage"""
        anxiety_triggers = ["overwhelmed", "confused", "frustrated", "uncertain", "worried"]
        emotions = stage_data.get("emotions", [])

        anxiety_count = sum(1 for emotion in emotions if emotion in anxiety_triggers)
        return min(10, anxiety_count * 2.5)

    def _calculate_confidence(self, stage: str, tech_proficiency: str) -> float:
        """Calculate confidence level for a stage"""
        base_confidence = {"expert": 9.0, "advanced": 7.5, "intermediate": 6.0, "basic": 4.0}

        confidence = base_confidence.get(tech_proficiency, 5.0)

        # Adjust by stage
        if stage == "onboarding":
            confidence -= 1.5  # Everyone less confident during onboarding
        elif stage == "advocacy":
            confidence += 1.0  # More confident by advocacy stage

        return max(1, min(10, confidence))

    def _identify_quick_wins(self, stage_data: dict[str, Any]) -> list[str]:
        """Identify quick wins for each stage"""
        quick_wins = []

        for opportunity in stage_data.get("opportunities", []):
            if any(word in opportunity.lower() for word in ["simplify", "automate", "streamline"]):
                quick_wins.append(opportunity)

        return quick_wins[:3]

    def _map_features_to_stage(self, features: list[dict[str, str]], stage: str) -> list[str]:
        """Map app features to journey stages"""
        stage_features = []

        for feature in features:
            feature_desc = feature.get("description", "").lower()

            if (
                (
                    stage == "consideration"
                    and any(word in feature_desc for word in ["demo", "preview", "try"])
                )
                or (
                    stage == "onboarding"
                    and any(word in feature_desc for word in ["setup", "import", "configure"])
                )
                or (
                    stage == "usage"
                    and any(word in feature_desc for word in ["automate", "analyze", "track"])
                )
            ):
                stage_features.append(feature["name"])

        return stage_features

    def _create_stage_messaging(self, stage: str, decision_drivers: list[str]) -> dict[str, str]:
        """Create messaging for each stage based on decision drivers"""
        messaging = {
            "awareness": {
                "headline": "Discover a better way",
                "focus": "Problem recognition",
                "cta": "Learn more",
            },
            "consideration": {
                "headline": "See how it works",
                "focus": "Solution capabilities",
                "cta": "Watch demo",
            },
            "decision": {
                "headline": "Join thousands who switched",
                "focus": "Social proof and ROI",
                "cta": "Start free trial",
            },
            "onboarding": {
                "headline": "Welcome! Let's get started",
                "focus": "Quick wins",
                "cta": "Complete setup",
            },
            "usage": {
                "headline": "You're doing great",
                "focus": "Continuous value",
                "cta": "Explore more features",
            },
            "advocacy": {
                "headline": "Share the success",
                "focus": "Community building",
                "cta": "Invite teammates",
            },
        }

        # Customize based on decision drivers
        if "ROI" in decision_drivers:
            messaging["decision"]["focus"] = "Measurable returns"
        if "ease of use" in str(decision_drivers).lower():
            messaging["consideration"]["focus"] = "Simplicity and efficiency"

        return messaging.get(stage, messaging["awareness"])

    def _define_stage_metrics(self, stage: str) -> list[str]:
        """Define metrics to track for each stage"""
        metrics = {
            "awareness": ["Page views", "Time on site", "Bounce rate", "Content downloads"],
            "consideration": ["Demo requests", "Feature page views", "Comparison tool usage"],
            "decision": ["Trial starts", "Pricing page views", "Sales inquiries"],
            "onboarding": ["Setup completion rate", "Time to first value", "Feature adoption"],
            "usage": ["Daily active users", "Feature usage", "Task completion rate"],
            "advocacy": ["NPS score", "Referrals", "Reviews", "Case study participation"],
        }

        return metrics.get(stage, ["Engagement rate"])

    def _identify_dropoff_risks(self, journey_map: dict[str, Any]) -> list[dict[str, str]]:
        """Identify where users might drop off"""
        risks = []

        for stage, data in journey_map["touchpoint_analysis"].items():
            if data["friction_points"]:
                risks.append(
                    {
                        "stage": stage,
                        "risk": f"High friction: {data['friction_points'][0]}",
                        "mitigation": f"Provide {data['support_needs'][0] if data['support_needs'] else 'guidance'}",
                    }
                )

        return risks

    def _find_acceleration_points(self, journey_map: dict[str, Any]) -> list[str]:
        """Find opportunities to accelerate the journey"""
        acceleration_points = []

        # Look for stages that could be combined or shortened
        if journey_map["emotion_curve"]["consideration"]["anxiety_level"] < 3:
            acceleration_points.append("Combine consideration and decision with free trial")

        if journey_map["touchpoint_analysis"]["onboarding"]["duration"] != "1 week":
            acceleration_points.append("Streamline onboarding to under 1 hour")

        return acceleration_points

    def _identify_personalization_opportunities(self, persona: PersonaInsights) -> list[str]:
        """Identify where to personalize the experience"""
        opportunities = []

        # Based on role
        opportunities.append(f"Role-based onboarding for {persona.role}")

        # Based on tech proficiency
        if persona.tech_proficiency == "basic":
            opportunities.append("Simplified UI mode option")
        elif persona.tech_proficiency == "expert":
            opportunities.append("Advanced features and API access")

        # Based on goals
        for goal in persona.goals[:2]:
            opportunities.append(f"Templates for '{goal}'")

        return opportunities

    def _map_differentiators_to_journey(
        self, app: AppConcept, journey_map: dict[str, Any]
    ) -> dict[str, str]:
        """Map competitive differentiators to journey stages"""
        differentiators = {}

        # Use app's differentiation at key stages
        differentiators["consideration"] = app.differentiation
        differentiators["decision"] = app.value_proposition
        differentiators["usage"] = f"Unique approach to {app.problem_statement}"

        return differentiators

    def create_strategic_roadmap(
        self,
        apps: list[AppConcept],
        business_cases: list[BusinessCase],
        feature_behaviors: list[FeatureBehavior],
    ) -> dict[str, Any]:
        """Create long-term strategic roadmap"""
        # Prioritize apps based on business value
        prioritized_apps = self._prioritize_apps(apps, business_cases)

        roadmap = {
            "vision": "Transform pain points into valuable solutions through persona-driven development",
            "phases": [],
            "success_factors": [],
            "risk_mitigation": [],
        }

        # Phase 1: MVP (0-3 months)
        roadmap["phases"].append(
            {
                "name": "MVP Launch",
                "duration": "0-3 months",
                "focus": prioritized_apps[0] if prioritized_apps else None,
                "objectives": [
                    "Validate core problem-solution fit",
                    "Build minimal feature set",
                    "Acquire first 100 users",
                    "Establish feedback loops",
                ],
                "deliverables": [
                    "Core app functionality",
                    "User onboarding flow",
                    "Basic analytics",
                    "Feedback collection system",
                ],
            }
        )

        # Phase 2: Growth (3-6 months)
        roadmap["phases"].append(
            {
                "name": "Growth & Refinement",
                "duration": "3-6 months",
                "objectives": [
                    "Scale to 1000+ users",
                    "Implement key requested features",
                    "Optimize user experience",
                    "Establish revenue streams",
                ],
            }
        )

        # Phase 3: Expansion (6-12 months)
        roadmap["phases"].append(
            {
                "name": "Market Expansion",
                "duration": "6-12 months",
                "objectives": [
                    "Enter adjacent markets",
                    "Build platform ecosystem",
                    "Achieve profitability",
                    "Prepare for next product",
                ],
            }
        )

        # Success factors
        roadmap["success_factors"] = [
            "Strong persona-problem fit",
            "Iterative development with user feedback",
            "Clear differentiation from competitors",
            "Sustainable unit economics",
            "Engaged user community",
        ]

        # Risk mitigation
        roadmap["risk_mitigation"] = [
            {"risk": "Market adoption", "mitigation": "Start with most passionate persona segment"},
            {
                "risk": "Technical complexity",
                "mitigation": "Build incrementally with proven technologies",
            },
            {"risk": "Competition", "mitigation": "Focus on unique insights from persona research"},
            {
                "risk": "Resource constraints",
                "mitigation": "Prioritize features with highest impact/effort ratio",
            },
        ]

        return roadmap

    # Helper methods
    def _extract_education(self, text: str) -> str:
        """Extract education level from persona text"""
        education_patterns = [
            r"MBA",
            r"PhD",
            r"Master",
            r"Bachelor",
            r"degree",
            r"university",
            r"college",
            r"graduate",
            r"diploma",
        ]
        for pattern in education_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return "Higher Education"
        return "Professional Training"

    def _extract_family_status(self, text: str) -> str:
        """Extract family status"""
        if re.search(r"married|spouse|husband|wife", text, re.IGNORECASE):
            if re.search(r"child|children|kids|parent", text, re.IGNORECASE):
                return "Married with children"
            return "Married"
        if re.search(r"single|divorced", text, re.IGNORECASE):
            return "Single"
        return "Not specified"

    def _extract_activities(self, text: str, role: str) -> list[str]:
        """Extract daily activities based on role and context"""
        activities = []

        # Common professional activities
        if "manager" in role.lower():
            activities.extend(
                [
                    "Team meetings and 1-on-1s",
                    "Strategic planning",
                    "Performance reviews",
                    "Stakeholder communication",
                ]
            )
        elif "engineer" in role.lower() or "developer" in role.lower():
            activities.extend(
                [
                    "Code development and reviews",
                    "Technical documentation",
                    "Debugging and testing",
                    "Architecture planning",
                ]
            )
        elif "designer" in role.lower():
            activities.extend(
                [
                    "Design iterations",
                    "Client presentations",
                    "User research",
                    "Portfolio development",
                ]
            )

        # Extract specific activities mentioned
        activity_patterns = [
            r"spends? time ([^\.]+)",
            r"daily ([^\.]+)",
            r"regularly ([^\.]+)",
            r"focuses? on ([^\.]+)",
        ]

        for pattern in activity_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            activities.extend([m.strip() for m in matches])

        return list(set(activities))[:8]  # Limit to 8 activities

    def _extract_pain_points(self, text: str, role: str) -> list[str]:
        """Extract pain points from persona context"""
        pain_points = []

        # Role-specific common pain points
        role_pain_points = {
            "manager": [
                "Team coordination challenges",
                "Resource allocation conflicts",
                "Communication bottlenecks",
            ],
            "engineer": ["Technical debt management", "Documentation gaps", "Tool fragmentation"],
            "designer": [
                "Client feedback loops",
                "Version control for designs",
                "Collaboration with developers",
            ],
            "founder": ["Cash flow management", "Talent acquisition", "Market validation"],
        }

        # Add role-specific pain points
        for key, points in role_pain_points.items():
            if key in role.lower():
                pain_points.extend(points)

        # Extract mentioned challenges
        challenge_patterns = [
            r"struggles? with ([^\.]+)",
            r"challenges? include ([^\.]+)",
            r"difficult(?:y|ies) ([^\.]+)",
            r"frustrated by ([^\.]+)",
            r"problems? with ([^\.]+)",
        ]

        for pattern in challenge_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            pain_points.extend([m.strip() for m in matches])

        return list(set(pain_points))[:6]  # Limit to 6 pain points

    def _extract_goals(self, text: str) -> list[str]:
        """Extract goals from persona text"""
        goals = []

        goal_patterns = [
            r"goals? (?:include|are) ([^\.]+)",
            r"aims? to ([^\.]+)",
            r"wants? to ([^\.]+)",
            r"aspir\w+ to ([^\.]+)",
            r"objectives? (?:include|are) ([^\.]+)",
        ]

        for pattern in goal_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            goals.extend([m.strip() for m in matches])

        # Add common professional goals if none found
        if not goals:
            goals = [
                "Career advancement",
                "Work-life balance",
                "Skill development",
                "Financial security",
            ]

        return list(set(goals))[:5]

    def _assess_tech_proficiency(self, text: str, role: str) -> str:
        """Assess technology proficiency level"""
        tech_indicators = {
            "expert": ["engineer", "developer", "architect", "data scientist", "DevOps"],
            "advanced": ["designer", "analyst", "manager", "consultant"],
            "intermediate": ["coordinator", "specialist", "administrator"],
            "basic": ["traditional", "non-technical", "beginner"],
        }

        for level, indicators in tech_indicators.items():
            for indicator in indicators:
                if indicator.lower() in role.lower() or indicator.lower() in text.lower():
                    return level

        return "intermediate"

    def _extract_decision_drivers(self, text: str, role: str) -> list[str]:
        """Extract what drives decision making"""
        drivers = []

        # Common decision drivers by role type
        if "executive" in role.lower() or "founder" in role.lower():
            drivers.extend(["ROI", "Strategic alignment", "Competitive advantage"])
        elif "manager" in role.lower():
            drivers.extend(["Team productivity", "Budget efficiency", "Risk mitigation"])
        else:
            drivers.extend(["Ease of use", "Time savings", "Cost effectiveness"])

        # Look for specific mentions
        if re.search(r"data[- ]driven", text, re.IGNORECASE):
            drivers.append("Data-driven insights")
        if re.search(r"user experience|UX", text, re.IGNORECASE):
            drivers.append("User experience")
        if re.search(r"security|privacy", text, re.IGNORECASE):
            drivers.append("Security and privacy")

        return list(set(drivers))[:4]

    def _estimate_budget(self, text: str, role: str) -> str:
        """Estimate budget range based on role and context"""
        if "enterprise" in text.lower() or "fortune" in text.lower():
            return "$10K-100K/year"
        if "startup" in text.lower() or "small business" in text.lower():
            return "$100-1K/month"
        if "freelance" in text.lower() or "individual" in text.lower():
            return "$10-100/month"
        if "executive" in role.lower() or "director" in role.lower():
            return "$1K-10K/month"
        return "$50-500/month"

    def _extract_user_journey(
        self, text: str, role: str, activities: list[str], pain_points: list[str]
    ) -> dict[str, Any]:
        """Extract user journey mapping stages to experiences and pain points"""
        # Define standard customer journey stages
        journey_stages = {
            "awareness": {
                "description": "Discovering the problem exists",
                "touchpoints": [],
                "emotions": [],
                "pain_points": [],
                "opportunities": [],
            },
            "consideration": {
                "description": "Researching potential solutions",
                "touchpoints": [],
                "emotions": [],
                "pain_points": [],
                "opportunities": [],
            },
            "decision": {
                "description": "Evaluating and choosing solution",
                "touchpoints": [],
                "emotions": [],
                "pain_points": [],
                "opportunities": [],
            },
            "onboarding": {
                "description": "Getting started with solution",
                "touchpoints": [],
                "emotions": [],
                "pain_points": [],
                "opportunities": [],
            },
            "usage": {
                "description": "Day-to-day interaction",
                "touchpoints": [],
                "emotions": [],
                "pain_points": [],
                "opportunities": [],
            },
            "advocacy": {
                "description": "Recommending to others",
                "touchpoints": [],
                "emotions": [],
                "pain_points": [],
                "opportunities": [],
            },
        }

        # Map activities and pain points to journey stages
        for activity in activities:
            activity_lower = activity.lower()

            # Awareness stage activities
            if any(
                word in activity_lower for word in ["research", "discover", "identify", "realize"]
            ):
                journey_stages["awareness"]["touchpoints"].append(activity)
                journey_stages["awareness"]["emotions"].append("curious")

            # Consideration stage activities
            elif any(
                word in activity_lower for word in ["evaluate", "compare", "review", "analyze"]
            ):
                journey_stages["consideration"]["touchpoints"].append(activity)
                journey_stages["consideration"]["emotions"].append("analytical")

            # Decision stage activities
            elif any(word in activity_lower for word in ["choose", "select", "decide", "budget"]):
                journey_stages["decision"]["touchpoints"].append(activity)
                journey_stages["decision"]["emotions"].append("cautious")

            # Usage stage activities (most daily activities)
            else:
                journey_stages["usage"]["touchpoints"].append(activity)
                journey_stages["usage"]["emotions"].append("focused")

        # Map pain points to journey stages
        for pain_point in pain_points:
            pain_lower = pain_point.lower()

            # Awareness pain points
            if any(word in pain_lower for word in ["don't know", "unaware", "hidden", "invisible"]):
                journey_stages["awareness"]["pain_points"].append(pain_point)
                journey_stages["awareness"]["opportunities"].append(f"Educate about {pain_point}")

            # Consideration pain points
            elif any(
                word in pain_lower for word in ["complex", "overwhelming", "confusing", "unclear"]
            ):
                journey_stages["consideration"]["pain_points"].append(pain_point)
                journey_stages["consideration"]["opportunities"].append(f"Simplify {pain_point}")

            # Onboarding pain points
            elif any(word in pain_lower for word in ["setup", "learn", "integrate", "migrate"]):
                journey_stages["onboarding"]["pain_points"].append(pain_point)
                journey_stages["onboarding"]["opportunities"].append(f"Streamline {pain_point}")

            # Usage pain points (most common)
            else:
                journey_stages["usage"]["pain_points"].append(pain_point)
                journey_stages["usage"]["opportunities"].append(f"Automate {pain_point}")

        # Add role-specific journey characteristics
        if "manager" in role.lower():
            journey_stages["decision"]["touchpoints"].append("ROI analysis")
            journey_stages["advocacy"]["touchpoints"].append("Team adoption metrics")
        elif "engineer" in role.lower():
            journey_stages["consideration"]["touchpoints"].append("Technical documentation review")
            journey_stages["onboarding"]["touchpoints"].append("API integration")
        elif "designer" in role.lower():
            journey_stages["consideration"]["touchpoints"].append("Visual examples review")
            journey_stages["usage"]["touchpoints"].append("Design system integration")

        # Add emotional journey based on role
        journey_stages["awareness"]["emotions"].extend(["frustrated", "seeking"])
        journey_stages["consideration"]["emotions"].extend(["hopeful", "skeptical"])
        journey_stages["decision"]["emotions"].extend(
            ["confident" if "senior" in role.lower() else "uncertain"]
        )
        journey_stages["onboarding"]["emotions"].extend(["excited", "overwhelmed"])
        journey_stages["usage"]["emotions"].extend(["productive", "efficient"])
        journey_stages["advocacy"]["emotions"].extend(["proud", "helpful"])

        # Create journey summary
        journey_summary = {
            "stages": journey_stages,
            "critical_moments": self._identify_critical_moments(journey_stages),
            "journey_duration": self._estimate_journey_duration(role),
            "key_decisions": self._extract_key_decisions(journey_stages),
            "success_factors": self._identify_success_factors(role, journey_stages),
        }

        return journey_summary

    def _identify_critical_moments(self, stages: dict[str, Any]) -> list[dict[str, str]]:
        """Identify critical moments in the user journey"""
        critical_moments = []

        # First pain point encounter
        for stage_name, stage_data in stages.items():
            if stage_data["pain_points"]:
                critical_moments.append(
                    {
                        "moment": f"First encounter with {stage_data['pain_points'][0]}",
                        "stage": stage_name,
                        "impact": "high",
                        "action_needed": "Provide immediate value demonstration",
                    }
                )
                break

        # Decision point
        if stages["decision"]["touchpoints"]:
            critical_moments.append(
                {
                    "moment": "Final purchase/adoption decision",
                    "stage": "decision",
                    "impact": "critical",
                    "action_needed": "Clear value proposition and social proof",
                }
            )

        # First success
        critical_moments.append(
            {
                "moment": "First successful outcome achieved",
                "stage": "usage",
                "impact": "high",
                "action_needed": "Celebrate and reinforce value",
            }
        )

        return critical_moments

    def _estimate_journey_duration(self, role: str) -> str:
        """Estimate typical journey duration by role"""
        if "executive" in role.lower() or "director" in role.lower():
            return "2-3 months (strategic decision)"
        if "manager" in role.lower():
            return "1-2 months (team evaluation)"
        if "freelance" in role.lower() or "individual" in role.lower():
            return "1-2 weeks (quick decision)"
        return "3-4 weeks (standard evaluation)"

    def _extract_key_decisions(self, stages: dict[str, Any]) -> list[str]:
        """Extract key decision points in the journey"""
        decisions = []

        if stages["consideration"]["touchpoints"]:
            decisions.append("Whether to invest time in evaluation")
        if stages["decision"]["touchpoints"]:
            decisions.append("Which solution best fits needs and budget")
        if stages["onboarding"]["touchpoints"]:
            decisions.append("How deeply to integrate into workflow")
        if stages["usage"]["pain_points"]:
            decisions.append("Whether to continue or seek alternatives")

        return decisions

    def _identify_success_factors(self, role: str, stages: dict[str, Any]) -> list[str]:
        """Identify what determines journey success"""
        factors = []

        # Role-based success factors
        if "manager" in role.lower():
            factors.extend(["Team adoption rate", "Measurable productivity gains"])
        elif "engineer" in role.lower():
            factors.extend(["Clean API integration", "Performance metrics"])
        elif "designer" in role.lower():
            factors.extend(["Visual quality", "Workflow integration"])

        # Stage-based success factors
        if stages["onboarding"]["pain_points"]:
            factors.append("Smooth onboarding experience")
        if stages["usage"]["opportunities"]:
            factors.append("Continuous value delivery")

        return factors[:5]  # Limit to top 5

    def _cluster_pain_points(self, personas: list[PersonaInsights]) -> dict[str, list[str]]:
        """Group similar pain points across personas"""
        clusters = defaultdict(list)

        # Categorize pain points
        categories = {
            "workflow_efficiency": [
                "coordination",
                "bottleneck",
                "fragmentation",
                "management",
                "allocation",
            ],
            "communication": ["feedback", "collaboration", "communication", "alignment", "updates"],
            "data_insights": ["analytics", "insights", "reporting", "visibility", "tracking"],
            "automation": ["manual", "repetitive", "automation", "time-consuming", "tedious"],
            "integration": ["integration", "compatibility", "sync", "connection", "siloed"],
        }

        for persona in personas:
            for pain_point in persona.pain_points:
                for category, keywords in categories.items():
                    if any(keyword in pain_point.lower() for keyword in keywords):
                        clusters[category].append(persona.name)
                        break

        return dict(clusters)

    def _create_app_concept(
        self, theme: str, affected_personas: list[str], all_personas: list[PersonaInsights]
    ) -> AppConcept:
        """Create app concept for a pain point cluster"""
        # Map themes to app concepts
        app_templates = {
            "workflow_efficiency": {
                "name": "FlowSync",
                "tagline": "Seamless workflow orchestration for modern teams",
                "problem": "Teams waste 30% of time on coordination and context switching",
                "solution": "AI-powered workflow automation that learns team patterns",
                "features": [
                    {
                        "name": "Smart Task Routing",
                        "description": "AI assigns tasks to optimal team members",
                    },
                    {
                        "name": "Context Preservation",
                        "description": "Maintains work context across tools",
                    },
                    {
                        "name": "Predictive Scheduling",
                        "description": "Anticipates bottlenecks and suggests solutions",
                    },
                ],
                "monetization": "Subscription per team member",
                "differentiation": "Only solution that learns from team behavior patterns",
            },
            "communication": {
                "name": "ClarityHub",
                "tagline": "Transform team communication into actionable insights",
                "problem": "Important decisions get lost in communication overload",
                "solution": "Intelligent communication platform that surfaces key decisions and actions",
                "features": [
                    {
                        "name": "Decision Tracking",
                        "description": "Automatically identifies and tracks decisions",
                    },
                    {
                        "name": "Action Extraction",
                        "description": "Pulls action items from any conversation",
                    },
                    {
                        "name": "Stakeholder Alignment",
                        "description": "Ensures right people see right information",
                    },
                ],
                "monetization": "Tiered pricing based on team size",
                "differentiation": "Focus on decision intelligence, not just messaging",
            },
            "data_insights": {
                "name": "InsightLens",
                "tagline": "See your business clearly with zero-effort analytics",
                "problem": "Data is everywhere but insights are nowhere",
                "solution": "Automated insight generation from all your business tools",
                "features": [
                    {
                        "name": "One-Click Integrations",
                        "description": "Connect all tools in minutes",
                    },
                    {
                        "name": "Natural Language Queries",
                        "description": "Ask questions in plain English",
                    },
                    {"name": "Proactive Alerts", "description": "Get notified of important trends"},
                ],
                "monetization": "Usage-based pricing",
                "differentiation": "No dashboard building - insights come to you",
            },
        }

        template = app_templates.get(theme, app_templates["workflow_efficiency"])

        return AppConcept(
            id=f"app_{theme}",
            name=template["name"],
            tagline=template["tagline"],
            problem_statement=template["problem"],
            solution_description=template["solution"],
            target_personas=affected_personas[:5],
            core_features=template["features"],
            value_proposition=f"Save 10+ hours/week for {len(affected_personas)} user types",
            monetization_model=template["monetization"],
            differentiation=template["differentiation"],
        )

    def _find_adjacent_personas(
        self, target_names: list[str], all_personas: list[PersonaInsights]
    ) -> list[PersonaInsights]:
        """Find personas similar but not identical to targets"""
        adjacent = []
        target_personas = [p for p in all_personas if p.name in target_names]

        for persona in all_personas:
            if persona.name not in target_names:
                # Check for similarity
                similarity_score = 0
                for target in target_personas:
                    if persona.tech_proficiency == target.tech_proficiency:
                        similarity_score += 1
                    if any(goal in persona.goals for goal in target.goals):
                        similarity_score += 1
                    if persona.budget_range == target.budget_range:
                        similarity_score += 1

                if similarity_score >= 2:
                    adjacent.append(persona)

        return adjacent[:3]

    def _find_skeptical_personas(
        self, target_names: list[str], all_personas: list[PersonaInsights]
    ) -> list[PersonaInsights]:
        """Find personas likely to be skeptical"""
        skeptical = []

        for persona in all_personas:
            if persona.name not in target_names:
                # Look for skeptical indicators
                if (
                    persona.tech_proficiency == "basic"
                    or "traditional" in str(persona.demographics).lower()
                    or persona.budget_range == "$10-100/month"
                ):
                    skeptical.append(persona)

        return skeptical[:2]

    def _test_from_perspective(
        self, app: AppConcept, persona: PersonaInsights, perspective_type: str
    ) -> PerspectiveTest:
        """Simulate testing from a persona's perspective"""
        # Base scores on perspective type and persona match
        if perspective_type == "primary":
            base_value = 7.5
            would_use = True
            would_pay = True
        elif perspective_type == "adjacent":
            base_value = 6.0
            would_use = True
            would_pay = False
        else:  # skeptical
            base_value = 4.0
            would_use = False
            would_pay = False

        # Adjust based on persona characteristics
        if persona.tech_proficiency in ["expert", "advanced"]:
            base_value += 0.5
        elif persona.tech_proficiency == "basic":
            base_value -= 1.0

        # Generate realistic feedback
        reactions = {
            "primary": f"This directly addresses my {persona.pain_points[0] if persona.pain_points else 'needs'}",
            "adjacent": f"Interesting, though designed for {app.target_personas[0] if app.target_personas else 'others'}",
            "skeptical": f"Not sure this fits my workflow as a {persona.role}",
        }

        concerns = []
        if persona.tech_proficiency == "basic":
            concerns.append("Learning curve might be steep")
        if "$10K" in persona.budget_range:
            concerns.append("Need to justify ROI to stakeholders")
        else:
            concerns.append("Pricing might be too high for my budget")

        suggestions = []
        if perspective_type == "adjacent":
            suggestions.append(f"Add features for {persona.role} use cases")
        if perspective_type == "skeptical":
            suggestions.append("Provide free trial or freemium option")

        return PerspectiveTest(
            app_id=app.id,
            persona_name=persona.name,
            perspective_type=perspective_type,
            reaction=reactions[perspective_type],
            perceived_value=min(10, max(0, base_value)),
            concerns=concerns,
            suggestions=suggestions,
            would_use=would_use,
            would_pay=would_pay,
        )

    def _estimate_market_size(self, app: AppConcept, tests: list[PerspectiveTest]) -> str:
        """Estimate market size based on persona representation"""
        positive_tests = [t for t in tests if t.would_use]
        ratio = len(positive_tests) / len(tests) if tests else 0

        if ratio > 0.7:
            return "Large ($1B+ TAM)"
        if ratio > 0.5:
            return "Medium ($100M-1B TAM)"
        return "Niche ($10-100M TAM)"

    def _calculate_revenue_potential(
        self, app: AppConcept, tests: list[PerspectiveTest]
    ) -> dict[str, Any]:
        """Calculate potential revenue"""
        paying_users = [t for t in tests if t.would_pay]
        pay_ratio = len(paying_users) / len(tests) if tests else 0

        return {
            "conversion_rate": f"{pay_ratio * 100:.0f}%",
            "arpu": "$50-200/month",
            "year_1_revenue": "$100K-1M",
            "year_3_revenue": "$1M-10M",
            "break_even": "Month 12-18",
        }

    def _estimate_costs(self, app: AppConcept) -> dict[str, Any]:
        """Estimate development and operational costs"""
        return {
            "development": {
                "mvp": "$50-100K",
                "full_product": "$200-500K",
                "timeline": "3-6 months MVP, 12 months full",
            },
            "operational": {
                "monthly": "$10-30K",
                "team_size": "5-10 people",
                "infrastructure": "$1-5K/month",
            },
        }

    def _estimate_timeline(self, app: AppConcept) -> str:
        """Estimate time to market"""
        complexity = len(app.core_features)
        if complexity <= 3:
            return "3-4 months to MVP"
        if complexity <= 5:
            return "4-6 months to MVP"
        return "6-9 months to MVP"

    def _analyze_competition(self, app: AppConcept) -> list[str]:
        """Identify potential competitors"""
        theme_competitors = {
            "workflow": ["Monday.com", "Asana", "Notion"],
            "communication": ["Slack", "Microsoft Teams", "Discord"],
            "data": ["Tableau", "Looker", "PowerBI"],
            "automation": ["Zapier", "Make", "n8n"],
        }

        # Find relevant competitors
        competitors = []
        for theme, comps in theme_competitors.items():
            if theme in app.name.lower() or theme in app.solution_description.lower():
                competitors.extend(comps)

        return competitors[:3] if competitors else ["No direct competitors identified"]

    def _assess_risks(self, app: AppConcept, tests: list[PerspectiveTest]) -> list[dict[str, str]]:
        """Assess key risks"""
        risks = []

        # Market risk
        skeptical_ratio = (
            len([t for t in tests if t.perspective_type == "skeptical" and not t.would_use])
            / len(tests)
            if tests
            else 0
        )
        if skeptical_ratio > 0.3:
            risks.append(
                {
                    "type": "Market Adoption",
                    "level": "High",
                    "mitigation": "Extended beta period with early adopter incentives",
                }
            )

        # Technical risk
        if len(app.core_features) > 5:
            risks.append(
                {
                    "type": "Technical Complexity",
                    "level": "Medium",
                    "mitigation": "Phased feature rollout with continuous testing",
                }
            )

        # Competition risk
        risks.append(
            {
                "type": "Competition",
                "level": "Medium",
                "mitigation": "Focus on unique persona insights and rapid iteration",
            }
        )

        return risks

    def _define_success_metrics(self, app: AppConcept) -> list[str]:
        """Define success metrics"""
        return [
            "Monthly Active Users (MAU) > 1,000 in 6 months",
            "User retention > 60% after 3 months",
            "NPS score > 50",
            "Customer Acquisition Cost < $100",
            "Monthly Recurring Revenue > $50K by month 12",
            "Feature adoption rate > 70% for core features",
        ]

    def _create_user_stories(
        self, feature: dict[str, str], target_personas: list[str], personas: list[PersonaInsights]
    ) -> list[str]:
        """Create user stories for a feature"""
        stories = []

        for persona_name in target_personas[:2]:
            persona = next((p for p in personas if p.name == persona_name), None)
            if persona:
                stories.append(
                    f"As {persona.name} ({persona.role}), I want to {feature['description'].lower()} "
                    f"so that I can {persona.goals[0].lower() if persona.goals else 'achieve my goals'}"
                )

        return stories

    def _define_expected_behaviors(
        self, feature: dict[str, str], personas: list[PersonaInsights]
    ) -> list[str]:
        """Define expected user behaviors"""
        behaviors = [
            f"Users will interact with {feature['name']} 3-5 times per day",
            f"Average session duration with {feature['name']}: 2-5 minutes",
            f"Users will share results from {feature['name']} with team members",
            f"Power users will customize {feature['name']} within first week",
        ]
        return behaviors

    def _define_system_requirements(self, feature: dict[str, str]) -> list[str]:
        """Define system requirements"""
        return [
            f"{feature['name']} must respond within 200ms",
            "Support 1000+ concurrent users",
            "Maintain 99.9% uptime",
            "Integrate with 10+ third-party APIs",
            "Support offline mode with sync",
        ]

    def _define_success_criteria(self, feature: dict[str, str]) -> list[str]:
        """Define success criteria"""
        return [
            f"80% of users successfully complete first use of {feature['name']}",
            "Feature adoption rate > 70% within 30 days",
            "User satisfaction score > 4.5/5",
            "Support tickets < 5% of active users",
            "Performance meets all system requirements",
        ]

    def _identify_edge_cases(
        self, feature: dict[str, str], personas: list[PersonaInsights]
    ) -> list[str]:
        """Identify edge cases"""
        edge_cases = [
            "User has no internet connectivity",
            "User inputs exceed system limits",
            "Concurrent editing by multiple users",
            "Integration API is down",
            "User has accessibility needs",
        ]

        # Add persona-specific edge cases
        for persona in personas:
            if persona.tech_proficiency == "basic":
                edge_cases.append(f"User ({persona.role}) needs extra guidance")

        return edge_cases[:6]

    def _prioritize_apps(
        self, apps: list[AppConcept], business_cases: list[BusinessCase]
    ) -> list[AppConcept]:
        """Prioritize apps based on business value"""
        # Simple prioritization based on market size
        # In reality, this would use a more sophisticated scoring system
        return apps  # Return as-is for this example

    def generate_report(self):
        """Generate comprehensive discovery report"""
        report = {
            "executive_summary": {
                "personas_analyzed": len(self.personas),
                "pain_points_identified": sum(len(p.pain_points) for p in self.personas),
                "app_concepts_generated": len(self.app_concepts),
                "perspectives_tested": len(self.perspective_tests),
                "top_opportunity": self.app_concepts[0].name if self.app_concepts else "None",
            },
            "key_insights": {
                "common_pain_points": self._get_top_pain_points(),
                "underserved_segments": self._identify_underserved_segments(),
                "market_gaps": self._identify_market_gaps(),
            },
            "recommendations": {
                "immediate_actions": [
                    "Validate top app concept with 10 real users",
                    "Build clickable prototype for user testing",
                    "Conduct competitive analysis deep dive",
                    "Secure initial funding/resources",
                ],
                "next_90_days": [
                    "Complete MVP development",
                    "Launch beta with 100 early adopters",
                    "Iterate based on feedback",
                    "Prepare for public launch",
                ],
            },
        }

        # Save report
        with open("persona_discovery_report.json", "w") as f:
            json.dump(report, f, indent=2, default=str)

        return report

    def _get_top_pain_points(self) -> list[str]:
        """Get most common pain points"""
        all_pain_points = []
        for persona in self.personas:
            all_pain_points.extend(persona.pain_points)

        counter = Counter(all_pain_points)
        return [point for point, count in counter.most_common(5)]

    def _identify_underserved_segments(self) -> list[str]:
        """Identify underserved market segments"""
        segments = []

        for persona in self.personas:
            if persona.tech_proficiency == "basic":
                segments.append(f"Non-technical {persona.role}s")
            elif "$10-100/month" in persona.budget_range:
                segments.append(f"Budget-conscious {persona.role}s")

        return list(set(segments))[:3]

    def _identify_market_gaps(self) -> list[str]:
        """Identify gaps in current market"""
        return [
            "Solutions designed for non-technical users",
            "Affordable options for small businesses",
            "Industry-specific workflow tools",
            "AI-powered automation for repetitive tasks",
        ]


def run_discovery_demo():
    """Run a demonstration of the discovery system"""
    logger.info("🚀 Persona-Driven Product Discovery Demo\n")

    discovery = PersonaDrivenDiscovery()

    # Load sample personas
    logger.info("📊 Loading personas...")
    with open("generated_personas_readable.txt") as f:
        content = f.read()

    # Split into individual personas
    persona_blocks = content.split("=" * 80)

    # Process first 5 personas for demo
    for block in persona_blocks[:5]:
        if block.strip() and "Generated Persona:" in block:
            insights = discovery.extract_persona_insights(block)
            discovery.personas.append(insights)
            logger.info(f"✓ Loaded {insights.name} - {insights.role}")

    # Generate app concepts
    logger.info(f"\n💡 Generating app concepts from {len(discovery.personas)} personas...")
    discovery.app_concepts = discovery.generate_app_concepts(discovery.personas)

    for app in discovery.app_concepts:
        logger.info(f"✓ {app.name}: {app.tagline}")

    # Test with perspectives
    logger.info("\n🔄 Testing with multiple perspectives...")
    for app in discovery.app_concepts[:2]:  # Test first 2 apps
        tests = discovery.test_with_perspectives(app, discovery.personas)
        discovery.perspective_tests.extend(tests)

        positive = len([t for t in tests if t.would_use])
        logger.info(f"✓ {app.name}: {positive}/{len(tests)} positive responses")

    # Analyze business value
    logger.info("\n💰 Analyzing business value...")
    for app in discovery.app_concepts[:2]:
        app_tests = [t for t in discovery.perspective_tests if t.app_id == app.id]
        business_case = discovery.analyze_business_value(app, app_tests)
        discovery.business_cases.append(business_case)
        logger.info(f"✓ {app.name}: {business_case.market_size}, {business_case.time_to_market}")

    # Map features to behaviors
    logger.info("\n🎯 Mapping features to behaviors...")
    for app in discovery.app_concepts[:1]:  # Just the top app
        behaviors = discovery.map_feature_behaviors(app, discovery.personas)
        discovery.feature_behaviors.extend(behaviors)
        logger.info(f"✓ Mapped {len(behaviors)} features for {app.name}")

    # Create strategic roadmap
    logger.info("\n📈 Creating strategic roadmap...")
    roadmap = discovery.create_strategic_roadmap(
        discovery.app_concepts, discovery.business_cases, discovery.feature_behaviors
    )

    logger.info(f"✓ Roadmap created with {len(roadmap['phases'])} phases")

    # Generate report
    logger.info("\n📄 Generating final report...")
    report = discovery.generate_report()

    logger.info("\n✅ Discovery process complete!")
    logger.info(
        f"\nTop recommendation: Build '{discovery.app_concepts[0].name if discovery.app_concepts else 'No concepts generated'}'"
    )
    logger.info(
        f"Target market: {discovery.app_concepts[0].target_personas[:3] if discovery.app_concepts else 'No targets'}"
    )
    logger.info("\nFull report saved to: persona_discovery_report.json")

    return discovery


if __name__ == "__main__":
    discovery: PersonaDrivenDiscovery = run_discovery_demo()
