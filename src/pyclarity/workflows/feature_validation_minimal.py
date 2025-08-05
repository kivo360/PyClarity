"""
Minimal Feature Validation using Decision Framework
=================================================

Simple feature validation using only decision framework.
"""

from typing import List
from pydantic import BaseModel, Field

from pyclarity.tools.decision_framework.models import (
    DecisionFrameworkContext,
    DecisionCriteria,
    ComplexityLevel
)
from pyclarity.tools.decision_framework.analyzer import DecisionFrameworkAnalyzer


class SimpleFeature(BaseModel):
    """Simple feature definition"""
    name: str
    description: str
    user_benefit: str
    complexity: str = "medium"


class ValidationScore(BaseModel):
    """Simple validation result"""
    feature_name: str
    score: float = Field(..., ge=0, le=1)
    recommendation: str
    reasons: List[str]


async def validate_feature_simple(
    feature: SimpleFeature,
    user_feedback: List[str]
) -> ValidationScore:
    """
    Validate a feature using decision framework
    
    Args:
        feature: Feature to validate
        user_feedback: List of user feedback strings
        
    Returns:
        Simple validation score
    """
    analyzer = DecisionFrameworkAnalyzer()
    
    # Create decision context
    from pyclarity.tools.decision_framework.models import DecisionOption
    
    context = DecisionFrameworkContext(
        problem=f"Should we build this feature: {feature.name}? {feature.description} Benefit: {feature.user_benefit}",
        criteria=[
            DecisionCriteria(name="User Value", weight=0.5),
            DecisionCriteria(name="Feasibility", weight=0.3),
            DecisionCriteria(name="Strategic Fit", weight=0.2)
        ],
        options=[
            DecisionOption(name="Build", description="Build this feature"),
            DecisionOption(name="Don't Build", description="Do not build this feature")
        ],
        complexity_level=ComplexityLevel.SIMPLE
    )
    
    # Add user feedback as constraints
    if user_feedback:
        context.constraints = user_feedback[:3]
    
    # Analyze
    result = await analyzer.analyze(context)
    
    # Extract score and recommendation
    score = result.confidence_score
    
    if score >= 0.7:
        recommendation = "Build"
    elif score >= 0.5:
        recommendation = "Consider with modifications"
    else:
        recommendation = "Don't build"
    
    # Get reasons from top alternative
    reasons = []
    if result.alternatives:
        best_alt = max(result.alternatives, key=lambda a: a.final_score)
        reasons = best_alt.strengths[:3]
    
    return ValidationScore(
        feature_name=feature.name,
        score=score,
        recommendation=recommendation,
        reasons=reasons
    )