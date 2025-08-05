"""
Simple Feature Validation using Existing Tools
=============================================

Validates features using multi-perspective analysis and decision framework.
"""

from typing import Dict, List
from pydantic import BaseModel, Field

from pyclarity.tools.multi_perspective.models import (
    MultiPerspectiveContext,
    Perspective,
    ComplexityLevel
)
from pyclarity.tools.multi_perspective.analyzer import MultiPerspectiveAnalyzer
from pyclarity.tools.decision_framework.models import (
    DecisionFrameworkContext,
    DecisionCriteria
)
from pyclarity.tools.decision_framework.analyzer import DecisionFrameworkAnalyzer


class FeatureToValidate(BaseModel):
    """Feature definition"""
    name: str
    description: str
    user_story: str
    complexity: str = "medium"  # low/medium/high


class ValidationResult(BaseModel):
    """Validation results"""
    feature_name: str
    overall_score: float = Field(..., ge=0, le=1)
    recommendation: str  # Build/Modify/Reject
    key_insights: List[str]
    risks: List[str]
    priority: str  # P0/P1/P2/P3


class SimpleFeatureValidator:
    """Validates features using cognitive tools"""
    
    def __init__(self):
        self.multi_perspective = MultiPerspectiveAnalyzer()
        self.decision_framework = DecisionFrameworkAnalyzer()
    
    async def validate_feature(
        self,
        feature: FeatureToValidate,
        user_personas: List[Dict[str, str]]
    ) -> ValidationResult:
        """
        Validate a feature from multiple perspectives
        
        Args:
            feature: Feature to validate
            user_personas: List of user types with name and description
            
        Returns:
            Validation results
        """
        # Create perspectives from personas
        perspectives = []
        for persona in user_personas:
            perspectives.append(Perspective(
                role=persona["name"],
                viewpoint=persona.get("viewpoint", f"As a {persona['name']}"),
                key_considerations=persona.get("needs", []),
                potential_conflicts=persona.get("concerns", [])
            ))
        
        # Add business perspective
        perspectives.append(Perspective(
            role="Business",
            viewpoint="ROI and strategic alignment",
            key_considerations=[
                f"Feature complexity: {feature.complexity}",
                "Resource requirements",
                "Market differentiation"
            ]
        ))
        
        # Multi-perspective analysis
        mp_context = MultiPerspectiveContext(
            topic=f"Validate feature: {feature.name}",
            description=f"{feature.description}\n{feature.user_story}",
            perspectives=perspectives,
            complexity_level=ComplexityLevel.MODERATE,
            synthesis_required=True
        )
        
        mp_result = await self.multi_perspective.analyze(mp_context)
        
        # Decision framework analysis
        criteria = [
            DecisionCriteria(
                name="User Value",
                weight=0.4,
                description="Value to end users"
            ),
            DecisionCriteria(
                name="Business Impact",
                weight=0.3,
                description="Strategic value"
            ),
            DecisionCriteria(
                name="Technical Feasibility",
                weight=0.3,
                description="Implementation complexity"
            )
        ]
        
        decision_context = DecisionFrameworkContext(
            decision_type="feature_prioritization",
            context=f"Should we build: {feature.name}",
            criteria=criteria,
            alternatives=["Build Now", "Build Later", "Don't Build"],
            complexity_level=ComplexityLevel.MODERATE
        )
        
        decision_result = await self.decision_framework.analyze(decision_context)
        
        # Calculate overall score
        overall_score = decision_result.confidence_score
        
        # Determine recommendation
        if overall_score >= 0.7:
            recommendation = "Build"
            priority = "P0" if feature.complexity == "low" else "P1"
        elif overall_score >= 0.5:
            recommendation = "Modify"
            priority = "P2"
        else:
            recommendation = "Reject"
            priority = "P3"
        
        # Extract insights and risks
        key_insights = mp_result.synthesis.split(".")[:3]
        risks = [
            alt.risks[0] if alt.risks else "No major risks"
            for alt in decision_result.alternatives
            if alt.name == "Build Now"
        ][:2]
        
        return ValidationResult(
            feature_name=feature.name,
            overall_score=overall_score,
            recommendation=recommendation,
            key_insights=[i.strip() for i in key_insights if i.strip()],
            risks=risks,
            priority=priority
        )


# Example usage
async def example_validation():
    validator = SimpleFeatureValidator()
    
    feature = FeatureToValidate(
        name="AI Recommendations",
        description="Personalized product recommendations using AI",
        user_story="As a shopper, I want recommendations so I can find relevant products",
        complexity="high"
    )
    
    personas = [
        {
            "name": "Frequent Shopper",
            "viewpoint": "I shop weekly and want to save time",
            "needs": ["Quick discovery", "Relevant suggestions"],
            "concerns": ["Privacy", "Too many notifications"]
        },
        {
            "name": "Budget Buyer",
            "viewpoint": "I look for deals and compare prices",
            "needs": ["Price comparisons", "Deal alerts"],
            "concerns": ["Upselling", "Hidden costs"]
        }
    ]
    
    result = await validator.validate_feature(feature, personas)
    print(f"Feature: {result.feature_name}")
    print(f"Score: {result.overall_score:.2f}")
    print(f"Recommendation: {result.recommendation} ({result.priority})")
    print(f"Insights: {result.key_insights}")
    print(f"Risks: {result.risks}")
    
    return result