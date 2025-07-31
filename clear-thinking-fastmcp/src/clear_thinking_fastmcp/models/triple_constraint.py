# Clear Thinking FastMCP Server - Triple Constraint Thinking Models

"""
Pydantic models for Triple Constraint Thinking cognitive tool.

This model enables analysis of any situation requiring balance between
three competing dimensions (e.g., Quality/Speed/Cost, Scope/Time/Budget).
"""

from typing import List, Dict, Optional, Literal, Any
from pydantic import BaseModel, Field, field_validator, ConfigDict
from enum import Enum

from .base import ClearThinkingBaseModel


class ConstraintDimension(str, Enum):
    """Common constraint dimension types across domains."""
    # Project Management
    SCOPE = "scope"
    TIME = "time" 
    BUDGET = "budget"
    
    # Engineering
    PERFORMANCE = "performance"
    COST = "cost"
    RELIABILITY = "reliability"
    
    # Business
    QUALITY = "quality"
    SPEED = "speed"
    PRICE = "price"
    
    # Generic
    DIMENSION_A = "dimension_a"
    DIMENSION_B = "dimension_b"
    DIMENSION_C = "dimension_c"


class OptimizationStrategy(str, Enum):
    """Strategies for optimizing constraint balance."""
    BALANCED = "balanced"
    PRIORITIZE_A = "prioritize_a"
    PRIORITIZE_B = "prioritize_b"
    PRIORITIZE_C = "prioritize_c"
    MINIMIZE_TRADE_OFFS = "minimize_trade_offs"
    MAXIMIZE_VALUE = "maximize_value"


class ConstraintSet(BaseModel):
    """Represents a set of three competing constraints."""
    model_config = ConfigDict(use_enum_values=True)
    
    dimension_a: str = Field(
        description="First constraint dimension (e.g., Quality, Scope, Performance)"
    )
    dimension_b: str = Field(
        description="Second constraint dimension (e.g., Speed, Time, Cost)"
    )
    dimension_c: str = Field(
        description="Third constraint dimension (e.g., Cost, Budget, Reliability)"
    )
    
    current_values: List[float] = Field(
        description="Current balance values for each dimension (0.0-1.0)",
        min_length=3,
        max_length=3
    )
    
    target_values: Optional[List[float]] = Field(
        None,
        description="Target balance values for optimization",
        min_length=3,
        max_length=3
    )
    
    @field_validator('current_values', 'target_values')
    @classmethod
    def validate_values(cls, v: Optional[List[float]]) -> Optional[List[float]]:
        if v is not None:
            for val in v:
                if not 0.0 <= val <= 1.0:
                    raise ValueError(f"Constraint values must be between 0.0 and 1.0, got {val}")
        return v


class TradeOffAnalysis(BaseModel):
    """Analysis of trade-offs between constraints."""
    model_config = ConfigDict(use_enum_values=True)
    
    relationship: str = Field(
        description="Description of the relationship between constraints"
    )
    impact_score: float = Field(
        description="Strength of the trade-off impact (0.0-1.0)",
        ge=0.0,
        le=1.0
    )
    examples: List[str] = Field(
        description="Concrete examples of this trade-off",
        min_length=1
    )
    mitigation_options: List[str] = Field(
        default_factory=list,
        description="Ways to minimize this trade-off"
    )


class OptimizationRecommendation(BaseModel):
    """Recommendation for optimizing constraint balance."""
    model_config = ConfigDict(use_enum_values=True)
    
    strategy: OptimizationStrategy = Field(
        description="Recommended optimization strategy"
    )
    rationale: str = Field(
        description="Explanation for this recommendation"
    )
    action_steps: List[str] = Field(
        description="Concrete steps to implement the optimization",
        min_length=1
    )
    expected_outcomes: List[str] = Field(
        description="Expected results from this optimization"
    )
    risks: List[str] = Field(
        default_factory=list,
        description="Potential risks or downsides"
    )
    confidence_level: float = Field(
        description="Confidence in this recommendation (0.0-1.0)",
        ge=0.0,
        le=1.0
    )


class TripleConstraintInput(ClearThinkingBaseModel):
    """Input for Triple Constraint Thinking analysis."""
    
    scenario: str = Field(
        description="The scenario or decision requiring constraint analysis"
    )
    
    domain_context: Optional[str] = Field(
        None,
        description="Domain-specific context (e.g., 'software_project', 'business_strategy')"
    )
    
    constraints: Optional[ConstraintSet] = Field(
        None,
        description="Pre-defined constraints if known"
    )
    
    optimization_goal: Optional[str] = Field(
        None,
        description="Specific optimization goal or outcome desired"
    )
    
    known_trade_offs: Optional[List[str]] = Field(
        default_factory=list,
        description="Known trade-offs to consider"
    )
    
    constraints_flexibility: Optional[Dict[str, float]] = Field(
        None,
        description="How flexible each constraint is (0.0=fixed, 1.0=very flexible)"
    )
    
    success_criteria: Optional[List[str]] = Field(
        default_factory=list,
        description="Criteria for successful constraint balance"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "scenario": "Developing a new mobile app with limited resources",
                "domain_context": "software_development",
                "optimization_goal": "Launch MVP within 3 months",
                "known_trade_offs": [
                    "Faster development means fewer features",
                    "Lower cost means less experienced developers"
                ],
                "success_criteria": [
                    "Core features implemented",
                    "Within budget constraints",
                    "Acceptable quality for MVP"
                ]
            }
        }


class TripleConstraintAnalysis(ClearThinkingBaseModel):
    """Complete Triple Constraint Thinking analysis output."""
    
    input_scenario: str = Field(
        description="The analyzed scenario"
    )
    
    identified_constraints: ConstraintSet = Field(
        description="The three competing constraints identified"
    )
    
    current_state_analysis: str = Field(
        description="Analysis of the current constraint balance"
    )
    
    trade_off_analyses: List[TradeOffAnalysis] = Field(
        description="Detailed analysis of trade-offs between constraints"
    )
    
    optimization_recommendations: List[OptimizationRecommendation] = Field(
        description="Recommendations for optimizing constraint balance"
    )
    
    domain_specific_insights: List[str] = Field(
        description="Insights specific to the problem domain"
    )
    
    visual_representation: Optional[Dict[str, Any]] = Field(
        None,
        description="Data for visualizing the constraint triangle"
    )
    
    key_decisions: List[str] = Field(
        description="Key decisions needed to manage constraints"
    )
    
    success_metrics: List[str] = Field(
        description="Metrics to track constraint management success"
    )
    
    overall_assessment: str = Field(
        description="Overall assessment of constraint management approach"
    )
    
    confidence_level: float = Field(
        description="Overall confidence in the analysis (0.0-1.0)",
        ge=0.0,
        le=1.0
    )