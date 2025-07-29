# Clear Thinking FastMCP Server - Mental Models

"""
Pydantic models for the Mental Models cognitive tool.

This tool applies structured mental model frameworks including:
- First Principles Thinking
- Opportunity Cost Analysis  
- Error Propagation Understanding
- Rubber Duck Debugging
- Pareto Principle (80/20 Rule)
- Occam's Razor

Agent: pydantic-model-engineer
Status: ACTIVE - Mental Models implementation complete
"""

from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any, Optional, Literal
from enum import Enum

from .base import CognitiveInputBase, CognitiveOutputBase, CognitiveValidators, ComplexityLevel


class MentalModelType(str, Enum):
    """Available mental model frameworks"""
    
    FIRST_PRINCIPLES = "first_principles"
    OPPORTUNITY_COST = "opportunity_cost"
    ERROR_PROPAGATION = "error_propagation"
    RUBBER_DUCK = "rubber_duck"
    PARETO_PRINCIPLE = "pareto_principle"
    OCCAMS_RAZOR = "occams_razor"
    
    @property
    def description(self) -> str:
        """Get description of the mental model"""
        descriptions = {
            self.FIRST_PRINCIPLES: "Break down complex problems to fundamental truths and build up from there",
            self.OPPORTUNITY_COST: "Analyze what you give up when making a choice",
            self.ERROR_PROPAGATION: "Understand how errors compound and propagate through systems",
            self.RUBBER_DUCK: "Explain the problem step-by-step to identify solutions",
            self.PARETO_PRINCIPLE: "Focus on the 20% of causes that create 80% of effects",
            self.OCCAMS_RAZOR: "Prefer the simplest explanation or solution that fits the facts"
        }
        return descriptions.get(self, "Unknown mental model")


class MentalModelInsight(BaseModel):
    """Individual insight from mental model analysis"""
    
    insight: str = Field(
        ...,
        description="The insight description",
        min_length=20,
        max_length=500,
        example="The fundamental constraint is database connection pooling, not query optimization"
    )
    
    relevance_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="How relevant this insight is to the problem",
        example=0.92
    )
    
    supporting_evidence: Optional[str] = Field(
        None,
        description="Evidence or reasoning supporting this insight",
        max_length=300,
        example="Connection pool analysis shows 95% utilization during peak hours"
    )
    
    category: Optional[str] = Field(
        None,
        description="Category or theme of the insight",
        max_length=50,
        example="Performance Bottleneck"
    )
    
    # Apply validators
    _validate_relevance = validator('relevance_score', allow_reuse=True)(
        CognitiveValidators.validate_confidence_score
    )
    
    @validator('insight')
    def validate_insight_content(cls, v):
        """Validate insight is meaningful"""
        return CognitiveValidators.validate_string_not_empty(cls, v, "insight")


class MentalModelAssumption(BaseModel):
    """Assumption identified during analysis"""
    
    assumption: str = Field(
        ...,
        description="The assumption being made",
        min_length=10,
        max_length=300
    )
    
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence that this assumption is valid"
    )
    
    impact_if_wrong: str = Field(
        ...,
        description="What happens if this assumption is incorrect",
        min_length=10,
        max_length=200
    )
    
    verification_method: Optional[str] = Field(
        None,
        description="How to verify or test this assumption",
        max_length=200
    )


class MentalModelInput(CognitiveInputBase):
    """Input model for mental model cognitive tool"""
    
    model_type: MentalModelType = Field(
        ...,
        description="Type of mental model to apply",
        example="first_principles"
    )
    
    complexity_level: ComplexityLevel = Field(
        ComplexityLevel.MODERATE,
        description="Complexity level of analysis to perform",
        example="moderate"
    )
    
    focus_areas: Optional[List[str]] = Field(
        None,
        description="Specific areas to focus the analysis on",
        max_items=5,
        example=["performance", "scalability", "cost"]
    )
    
    constraints: Optional[List[str]] = Field(
        None,
        description="Known constraints or limitations",
        max_items=8,
        example=["budget under $10k", "must complete in 3 months"]
    )
    
    domain_expertise: Optional[str] = Field(
        None,
        description="Relevant domain expertise level to apply",
        max_length=100,
        example="Senior software architect with database specialization"
    )
    
    @validator('problem')
    def validate_problem_for_mental_model(cls, v):
        """Enhanced validation for mental model problems"""
        if len(v.strip()) < 20:
            raise ValueError("Mental model analysis requires detailed problem descriptions (min 20 chars)")
        return v
    
    @validator('focus_areas')
    def validate_focus_areas(cls, v):
        """Validate focus areas if provided"""
        if v is not None:
            # Remove empty strings and duplicates
            cleaned = list(set(area.strip() for area in v if area.strip()))
            if not cleaned:
                return None
            return cleaned[:5]  # Limit to 5 items
        return v
    
    @validator('constraints')
    def validate_constraints(cls, v):
        """Validate constraints if provided"""
        if v is not None:
            cleaned = [constraint.strip() for constraint in v if constraint.strip()]
            return cleaned[:8] if cleaned else None
        return v


class MentalModelOutput(CognitiveOutputBase):
    """Output model for mental model cognitive tool"""
    
    model_applied: MentalModelType = Field(
        ...,
        description="Mental model that was applied",
        example="first_principles"
    )
    
    key_insights: List[MentalModelInsight] = Field(
        ...,
        description="List of key insights from the analysis",
        min_items=1,
        max_items=10
    )
    
    recommendations: List[str] = Field(
        ...,
        description="Actionable recommendations based on the analysis",
        min_items=1,
        max_items=8
    )
    
    assumptions_identified: List[MentalModelAssumption] = Field(
        default_factory=list,
        description="Assumptions identified during analysis",
        max_items=6
    )
    
    fundamental_elements: Optional[List[str]] = Field(
        None,
        description="Fundamental elements identified (for first principles)",
        max_items=8
    )
    
    trade_offs: Optional[List[Dict[str, str]]] = Field(
        None,
        description="Trade-offs identified (for opportunity cost)",
        max_items=5
    )
    
    error_paths: Optional[List[str]] = Field(
        None,
        description="Error propagation paths identified",
        max_items=6
    )
    
    critical_factors: Optional[List[str]] = Field(
        None,
        description="Critical 20% factors (for Pareto analysis)",
        max_items=5
    )
    
    simplified_explanation: Optional[str] = Field(
        None,
        description="Simplified explanation (for Occam's Razor)",
        max_length=500
    )
    
    limitations: Optional[str] = Field(
        None,
        description="Limitations of this analysis",
        max_length=300
    )
    
    next_steps: Optional[List[str]] = Field(
        None,
        description="Suggested next steps based on analysis",
        max_items=5
    )
    
    @validator('key_insights')
    def validate_key_insights(cls, v):
        """Validate key insights list"""
        if not v:
            raise ValueError("At least one key insight is required")
        
        # Sort by relevance score (highest first)
        return sorted(v, key=lambda x: x.relevance_score, reverse=True)
    
    @validator('recommendations')
    def validate_recommendations(cls, v):
        """Validate recommendations list"""
        if not v:
            raise ValueError("At least one recommendation is required")
        
        # Clean and validate each recommendation
        cleaned = []
        for rec in v:
            if isinstance(rec, str) and rec.strip():
                cleaned_rec = ' '.join(rec.split())
                if len(cleaned_rec) >= 10:  # Minimum meaningful length
                    cleaned.append(cleaned_rec)
        
        if not cleaned:
            raise ValueError("All recommendations must be meaningful (min 10 chars)")
        
        return cleaned
    
    @validator('trade_offs')
    def validate_trade_offs(cls, v):
        """Validate trade-offs structure"""
        if v is not None:
            for trade_off in v:
                if not isinstance(trade_off, dict):
                    raise ValueError("Trade-offs must be dictionaries")
                
                required_keys = ['option', 'benefit', 'cost']
                if not all(key in trade_off for key in required_keys):
                    raise ValueError(f"Trade-offs must contain keys: {required_keys}")
        
        return v

    def get_model_description(self) -> str:
        """Get description of the applied mental model"""
        return self.model_applied.description
    
    def get_top_insights(self, n: int = 3) -> List[MentalModelInsight]:
        """Get top N insights by relevance score"""
        return sorted(self.key_insights, key=lambda x: x.relevance_score, reverse=True)[:n]
    
    def get_high_confidence_assumptions(self, threshold: float = 0.7) -> List[MentalModelAssumption]:
        """Get assumptions with confidence above threshold"""
        return [
            assumption for assumption in self.assumptions_identified
            if assumption.confidence >= threshold
        ]


# Utility functions for mental model processing
class MentalModelUtils:
    """Utility functions for mental model processing"""
    
    @staticmethod
    def validate_model_compatibility(problem: str, model_type: MentalModelType) -> bool:
        """Check if problem is suitable for the mental model"""
        problem_lower = problem.lower()
        
        compatibility = {
            MentalModelType.FIRST_PRINCIPLES: [
                'how', 'why', 'fundamental', 'basic', 'core', 'foundation'
            ],
            MentalModelType.OPPORTUNITY_COST: [
                'choose', 'decision', 'alternative', 'option', 'trade-off', 'versus'
            ],
            MentalModelType.ERROR_PROPAGATION: [
                'error', 'fail', 'break', 'cascade', 'propagate', 'reliability'
            ],
            MentalModelType.RUBBER_DUCK: [
                'stuck', 'confused', 'debug', 'explain', 'understand', 'clarify'
            ],
            MentalModelType.PARETO_PRINCIPLE: [
                'optimize', 'prioritize', 'focus', 'critical', 'important', 'impact'
            ],
            MentalModelType.OCCAMS_RAZOR: [
                'complex', 'simple', 'elegant', 'straightforward', 'multiple solutions'
            ]
        }
        
        keywords = compatibility.get(model_type, [])
        return any(keyword in problem_lower for keyword in keywords)
    
    @staticmethod
    def suggest_mental_model(problem: str) -> List[MentalModelType]:
        """Suggest appropriate mental models for a problem"""
        suggestions = []
        
        for model_type in MentalModelType:
            if MentalModelUtils.validate_model_compatibility(problem, model_type):
                suggestions.append(model_type)
        
        # If no specific matches, suggest first principles as default
        if not suggestions:
            suggestions.append(MentalModelType.FIRST_PRINCIPLES)
        
        return suggestions


__all__ = [
    "MentalModelType",
    "MentalModelInput", 
    "MentalModelOutput",
    "MentalModelInsight",
    "MentalModelAssumption",
    "MentalModelUtils"
]