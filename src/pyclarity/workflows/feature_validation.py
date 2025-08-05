"""
Feature Validation Pipeline using Multi-Perspective Analysis
==========================================================

Validates product features against different perspectives and user needs
using cognitive tools to ensure features solve real problems.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from pyclarity.tools.multi_perspective.models import (
    MultiPerspectiveContext,
    MultiPerspectiveResult,
    Perspective as MultiPerspective,
    ComplexityLevel
)
from pyclarity.tools.multi_perspective.analyzer import MultiPerspectiveAnalyzer
from pyclarity.tools.decision_framework.models import (
    DecisionFrameworkContext,
    DecisionFrameworkResult,
    DecisionCriterion
)
from pyclarity.tools.decision_framework.analyzer import DecisionFrameworkAnalyzer
from pyclarity.tools.mental_models.models import (
    MentalModelContext,
    MentalModelType
)
from pyclarity.tools.mental_models.analyzer import MentalModelsAnalyzer
from pyclarity.tools.collaborative_reasoning.models import (
    CollaborativeReasoningContext,
    Perspective
)
from pyclarity.tools.collaborative_reasoning.analyzer import CollaborativeReasoningAnalyzer
from pyclarity.tools.structured_argumentation.models import (
    StructuredArgumentationContext,
    ArgumentationType
)
from pyclarity.tools.structured_argumentation.analyzer import StructuredArgumentationAnalyzer


class FeatureDefinition(BaseModel):
    """Definition of a feature to validate"""
    
    name: str = Field(..., description="Feature name")
    description: str = Field(..., description="Detailed description")
    user_story: str = Field(..., description="As a [user], I want [feature] so that [benefit]")
    technical_complexity: str = Field("medium", description="low/medium/high")
    dependencies: List[str] = Field(default_factory=list, description="Other features this depends on")
    success_metrics: List[str] = Field(default_factory=list, description="How to measure success")


class PersonaValidation(BaseModel):
    """Validation results from a specific user perspective"""
    
    perspective_name: str
    perspective_role: str
    relevance_score: float = Field(..., ge=0, le=1, description="How relevant is this feature")
    needs_addressed: List[str] = Field(default_factory=list)
    value_perception: str = Field(..., description="How valuable from this perspective")
    adoption_likelihood: float = Field(..., ge=0, le=1)
    concerns: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)


class MarketValidation(BaseModel):
    """Market analysis for the feature"""
    
    market_fit_score: float = Field(..., ge=0, le=1)
    competitive_advantage: str
    differentiation_factors: List[str] = Field(default_factory=list)
    market_gaps_filled: List[str] = Field(default_factory=list)
    adoption_barriers: List[str] = Field(default_factory=list)
    target_market_size: str


class FeatureValidationResult(BaseModel):
    """Complete validation results for a feature"""
    
    feature: FeatureDefinition
    persona_validations: List[PersonaValidation]
    market_validation: MarketValidation
    overall_score: float = Field(..., ge=0, le=1, description="Overall validation score")
    recommendation: str = Field(..., description="Build/Modify/Reject")
    priority_level: str = Field(..., description="P0/P1/P2/P3")
    implementation_suggestions: List[str] = Field(default_factory=list)
    risk_factors: List[str] = Field(default_factory=list)
    success_probability: float = Field(..., ge=0, le=1)


class FeatureValidationPipeline:
    """Pipeline for validating features using persona and cognitive tools"""
    
    def __init__(self):
        self.persona_analyzer = PersonaSimulatorAnalyzer()
        self.decision_analyzer = DecisionFrameworkAnalyzer()
        self.mental_models_analyzer = MentalModelsAnalyzer()
        self.collaborative_analyzer = CollaborativeReasoningAnalyzer()
    
    async def validate_feature(
        self,
        feature: FeatureDefinition,
        personas: List[Dict[str, Any]],
        market_context: Optional[str] = None
    ) -> FeatureValidationResult:
        """
        Validate a feature against personas and market context
        
        Args:
            feature: Feature to validate
            personas: List of persona definitions
            market_context: Optional market/competitive context
            
        Returns:
            Complete validation results
        """
        # Step 1: Validate with each persona
        persona_validations = await self._validate_with_personas(feature, personas)
        
        # Step 2: Analyze market fit
        market_validation = await self._analyze_market_fit(feature, market_context)
        
        # Step 3: Multi-perspective reasoning
        perspectives = await self._gather_perspectives(feature, persona_validations)
        
        # Step 4: Decision framework analysis
        decision_analysis = await self._analyze_decision(feature, persona_validations, market_validation)
        
        # Step 5: Calculate overall score and recommendation
        overall_score = self._calculate_overall_score(persona_validations, market_validation)
        recommendation = self._determine_recommendation(overall_score, decision_analysis)
        priority = self._determine_priority(overall_score, feature, market_validation)
        
        # Step 6: Generate implementation suggestions
        suggestions = self._generate_suggestions(persona_validations, perspectives)
        risk_factors = self._identify_risks(feature, market_validation, decision_analysis)
        
        return FeatureValidationResult(
            feature=feature,
            persona_validations=persona_validations,
            market_validation=market_validation,
            overall_score=overall_score,
            recommendation=recommendation,
            priority_level=priority,
            implementation_suggestions=suggestions,
            risk_factors=risk_factors,
            success_probability=overall_score * 0.8  # Adjusted for risk
        )
    
    async def _validate_with_personas(
        self,
        feature: FeatureDefinition,
        personas: List[Dict[str, Any]]
    ) -> List[PersonaValidation]:
        """Validate feature with each persona"""
        validations = []
        
        for persona_data in personas:
            # Create persona profile
            profile = PersonaProfile(
                name=persona_data.get("name", "User"),
                role=persona_data.get("role", "General User"),
                background=persona_data.get("background", ""),
                goals=persona_data.get("goals", []),
                pain_points=persona_data.get("pain_points", []),
                preferences=persona_data.get("preferences", {}),
                constraints=persona_data.get("constraints", [])
            )
            
            # Simulate persona response to feature
            context = PersonaSimulatorContext(
                scenario=f"Evaluate this feature: {feature.name}\n{feature.description}\n{feature.user_story}",
                personas=[profile],
                interaction_type="feature_evaluation",
                context_depth="comprehensive"
            )
            
            result = await self.persona_analyzer.analyze(context)
            
            # Extract validation from response
            response = result.persona_responses[0]
            validation = self._extract_persona_validation(profile, response, feature)
            validations.append(validation)
        
        return validations
    
    def _extract_persona_validation(
        self,
        profile: PersonaProfile,
        response: PersonaResponse,
        feature: FeatureDefinition
    ) -> PersonaValidation:
        """Extract validation data from persona response"""
        # Parse response to extract key insights
        response_text = response.response.lower()
        
        # Calculate relevance based on pain points addressed
        pain_points_addressed = [
            pp for pp in profile.pain_points
            if any(word in response_text for word in pp.lower().split())
        ]
        
        relevance_score = len(pain_points_addressed) / max(len(profile.pain_points), 1)
        
        # Extract value perception
        if "essential" in response_text or "critical" in response_text:
            value_perception = "Very High"
            usage_likelihood = 0.9
        elif "useful" in response_text or "helpful" in response_text:
            value_perception = "High"
            usage_likelihood = 0.7
        elif "nice to have" in response_text:
            value_perception = "Medium"
            usage_likelihood = 0.5
        else:
            value_perception = "Low"
            usage_likelihood = 0.3
        
        # Extract concerns and suggestions from reasoning
        concerns = [
            step for step in response.reasoning_steps
            if any(word in step.lower() for word in ["concern", "worry", "issue", "problem"])
        ][:3]
        
        suggestions = [
            step for step in response.reasoning_steps
            if any(word in step.lower() for word in ["suggest", "recommend", "could", "should"])
        ][:3]
        
        return PersonaValidation(
            persona_name=profile.name,
            persona_role=profile.role,
            relevance_score=relevance_score,
            pain_points_addressed=pain_points_addressed,
            value_perception=value_perception,
            usage_likelihood=usage_likelihood,
            concerns=concerns,
            suggestions=suggestions
        )
    
    async def _analyze_market_fit(
        self,
        feature: FeatureDefinition,
        market_context: Optional[str]
    ) -> MarketValidation:
        """Analyze market fit using mental models"""
        context_text = f"""
        Feature: {feature.name}
        Description: {feature.description}
        User Story: {feature.user_story}
        Market Context: {market_context or 'General consumer market'}
        """
        
        # Use multiple mental models for market analysis
        mental_context = MentalModelContext(
            problem=f"Analyze market fit for: {context_text}",
            model_type=MentalModelType.OPPORTUNITY_COST,
            complexity_level=ComplexityLevel.MODERATE,
            focus_areas=["market fit", "competitive advantage", "adoption"]
        )
        
        result = await self.mental_models_analyzer.analyze(mental_context)
        
        # Extract market insights
        market_fit_score = result.confidence_score
        insights = result.framework_applications[0].insights
        
        return MarketValidation(
            market_fit_score=market_fit_score,
            competitive_advantage=insights[0] if insights else "Unique value proposition",
            differentiation_factors=[
                insight for insight in insights
                if "different" in insight.lower() or "unique" in insight.lower()
            ][:3],
            market_gaps_filled=[
                rec for rec in result.framework_applications[0].recommendations
                if "gap" in rec.lower() or "need" in rec.lower()
            ][:2],
            adoption_barriers=[
                step for step in result.framework_applications[0].analysis_steps
                if "barrier" in step.lower() or "challenge" in step.lower()
            ][:2],
            target_market_size="Medium"  # Would need real market data
        )
    
    async def _gather_perspectives(
        self,
        feature: FeatureDefinition,
        persona_validations: List[PersonaValidation]
    ) -> List[Perspective]:
        """Gather multiple perspectives on the feature"""
        # Create perspectives from personas
        perspectives = []
        
        for validation in persona_validations[:3]:  # Top 3 personas
            perspective = Perspective(
                role=validation.persona_role,
                viewpoint=f"As a {validation.persona_role}, this feature is {validation.value_perception} value",
                key_considerations=[
                    f"Addresses: {', '.join(validation.pain_points_addressed[:2])}",
                    f"Usage likelihood: {validation.usage_likelihood:.0%}"
                ],
                potential_conflicts=validation.concerns[:2]
            )
            perspectives.append(perspective)
        
        # Add business perspective
        perspectives.append(Perspective(
            role="Business Stakeholder",
            viewpoint="Feature ROI and strategic alignment",
            key_considerations=[
                f"Technical complexity: {feature.technical_complexity}",
                f"Success metrics: {len(feature.success_metrics)} defined"
            ],
            potential_conflicts=["Resource allocation", "Timeline constraints"]
        ))
        
        return perspectives
    
    async def _analyze_decision(
        self,
        feature: FeatureDefinition,
        persona_validations: List[PersonaValidation],
        market_validation: MarketValidation
    ) -> DecisionFrameworkResult:
        """Use decision framework to analyze feature viability"""
        # Define decision criteria
        criteria = [
            DecisionCriterion(
                name="User Value",
                weight=0.3,
                description="Value delivered to users",
                evaluation_method="persona_validation_scores"
            ),
            DecisionCriterion(
                name="Market Fit",
                weight=0.25,
                description="Alignment with market needs",
                evaluation_method="market_analysis"
            ),
            DecisionCriterion(
                name="Technical Feasibility",
                weight=0.2,
                description="Complexity and dependencies",
                evaluation_method="complexity_assessment"
            ),
            DecisionCriterion(
                name="Business Impact",
                weight=0.25,
                description="Strategic value and ROI",
                evaluation_method="business_metrics"
            )
        ]
        
        decision_context = DecisionFrameworkContext(
            decision_type="feature_prioritization",
            context=f"Should we build: {feature.name}",
            criteria=criteria,
            alternatives=["Build Now", "Build Later", "Don't Build"],
            constraints=[
                f"Complexity: {feature.technical_complexity}",
                f"Dependencies: {len(feature.dependencies)}"
            ],
            complexity_level=ComplexityLevel.MODERATE
        )
        
        return await self.decision_analyzer.analyze(decision_context)
    
    def _calculate_overall_score(
        self,
        persona_validations: List[PersonaValidation],
        market_validation: MarketValidation
    ) -> float:
        """Calculate overall validation score"""
        # Average persona scores
        if persona_validations:
            avg_relevance = sum(v.relevance_score for v in persona_validations) / len(persona_validations)
            avg_usage = sum(v.usage_likelihood for v in persona_validations) / len(persona_validations)
            persona_score = (avg_relevance + avg_usage) / 2
        else:
            persona_score = 0.5
        
        # Combine with market score
        overall = (persona_score * 0.6) + (market_validation.market_fit_score * 0.4)
        return min(max(overall, 0.0), 1.0)
    
    def _determine_recommendation(
        self,
        overall_score: float,
        decision_analysis: DecisionFrameworkResult
    ) -> str:
        """Determine build recommendation"""
        if overall_score >= 0.8:
            return "Build - High Priority"
        elif overall_score >= 0.6:
            return "Build - Normal Priority"
        elif overall_score >= 0.4:
            return "Modify - Needs Refinement"
        else:
            return "Reject - Low Value"
    
    def _determine_priority(
        self,
        overall_score: float,
        feature: FeatureDefinition,
        market_validation: MarketValidation
    ) -> str:
        """Determine implementation priority"""
        if overall_score >= 0.8 and feature.technical_complexity == "low":
            return "P0"  # Immediate
        elif overall_score >= 0.7 or market_validation.market_fit_score >= 0.8:
            return "P1"  # High Priority
        elif overall_score >= 0.5:
            return "P2"  # Medium Priority
        else:
            return "P3"  # Low Priority
    
    def _generate_suggestions(
        self,
        persona_validations: List[PersonaValidation],
        perspectives: List[Perspective]
    ) -> List[str]:
        """Generate implementation suggestions"""
        suggestions = []
        
        # Collect all suggestions from personas
        for validation in persona_validations:
            suggestions.extend(validation.suggestions)
        
        # Add perspective-based suggestions
        for perspective in perspectives:
            if perspective.key_considerations:
                suggestions.append(f"Consider {perspective.role}: {perspective.key_considerations[0]}")
        
        # Deduplicate and limit
        unique_suggestions = list(dict.fromkeys(suggestions))
        return unique_suggestions[:5]
    
    def _identify_risks(
        self,
        feature: FeatureDefinition,
        market_validation: MarketValidation,
        decision_analysis: DecisionFrameworkResult
    ) -> List[str]:
        """Identify risk factors"""
        risks = []
        
        # Technical risks
        if feature.technical_complexity == "high":
            risks.append("High technical complexity may delay delivery")
        
        if len(feature.dependencies) > 2:
            risks.append(f"Depends on {len(feature.dependencies)} other features")
        
        # Market risks
        risks.extend(market_validation.adoption_barriers)
        
        # Add risks from decision analysis
        if hasattr(decision_analysis, "risk_assessment") and decision_analysis.risk_assessment:
            risks.extend([
                risk.description for risk in decision_analysis.risk_assessment.identified_risks[:2]
            ])
        
        return risks[:5]


# Usage example
async def validate_feature_example():
    """Example of validating a feature"""
    pipeline = FeatureValidationPipeline()
    
    # Define a feature
    feature = FeatureDefinition(
        name="Smart Recommendations",
        description="AI-powered product recommendations based on user behavior and preferences",
        user_story="As a shopper, I want personalized recommendations so that I can discover relevant products",
        technical_complexity="high",
        dependencies=["User Profile System", "Analytics Engine"],
        success_metrics=["Click-through rate > 15%", "Conversion rate improvement > 10%"]
    )
    
    # Define personas
    personas = [
        {
            "name": "Sarah",
            "role": "Frequent Shopper",
            "background": "Tech-savvy millennial who shops online weekly",
            "goals": ["Find deals quickly", "Discover new products"],
            "pain_points": ["Too many irrelevant products", "Time wasted browsing"],
            "preferences": {"personalization": "high", "privacy": "medium"}
        },
        {
            "name": "Robert",
            "role": "Occasional Buyer",
            "background": "Busy professional who shops when needed",
            "goals": ["Quick checkout", "Reliable products"],
            "pain_points": ["Complex navigation", "Information overload"],
            "preferences": {"simplicity": "high", "recommendations": "low"}
        }
    ]
    
    # Validate the feature
    result = await pipeline.validate_feature(
        feature=feature,
        personas=personas,
        market_context="E-commerce platform competing with Amazon and eBay"
    )
    
    return result