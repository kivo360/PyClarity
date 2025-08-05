"""
Mental Models Models

Data structures for applying structured mental model frameworks including
First Principles Thinking, Opportunity Cost Analysis, Error Propagation,
Rubber Duck Debugging, Pareto Principle, and Occam's Razor.
"""

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


class ComplexityLevel(str, Enum):
    """Problem complexity levels"""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    VERY_COMPLEX = "very_complex"


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
        max_length=500
    )

    relevance_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="How relevant this insight is to the problem"
    )

    supporting_evidence: str | None = Field(
        None,
        description="Evidence or reasoning supporting this insight",
        max_length=300
    )

    category: str | None = Field(
        None,
        description="Category or theme of the insight",
        max_length=50
    )

    @field_validator('insight')
    @classmethod
    def validate_insight_content(cls, v):
        """Validate insight is meaningful"""
        if not v or v.strip() == "":
            raise ValueError("Insight cannot be empty")
        return v.strip()


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

    verification_method: str | None = Field(
        None,
        description="How to verify or test this assumption",
        max_length=200
    )

    @field_validator('assumption', 'impact_if_wrong')
    @classmethod
    def validate_string_fields(cls, v):
        """Validate string fields are meaningful"""
        if not v or v.strip() == "":
            raise ValueError("Field cannot be empty")
        return v.strip()


class MentalModelContext(BaseModel):
    """Context for mental model analysis"""

    problem: str = Field(
        ...,
        description="The problem or question to analyze",
        min_length=20,
        max_length=2000
    )

    model_type: MentalModelType = Field(
        ...,
        description="Type of mental model to apply"
    )

    complexity_level: ComplexityLevel = Field(
        ComplexityLevel.MODERATE,
        description="Complexity level of analysis to perform"
    )

    focus_areas: list[str] | None = Field(
        None,
        description="Specific areas to focus the analysis on",
        max_length=5
    )

    constraints: list[str] | None = Field(
        None,
        description="Known constraints or limitations",
        max_length=8
    )

    domain_expertise: str | None = Field(
        None,
        description="Relevant domain expertise level to apply",
        max_length=100
    )

    @field_validator('problem')
    @classmethod
    def validate_problem_for_mental_model(cls, v):
        """Enhanced validation for mental model problems"""
        v = v.strip()
        if len(v) < 20:
            raise ValueError("Mental model analysis requires detailed problem descriptions (min 20 chars)")
        return v

    @field_validator('focus_areas')
    @classmethod
    def validate_focus_areas(cls, v):
        """Validate focus areas if provided"""
        if v is not None:
            # Remove empty strings and duplicates
            cleaned = list(set(area.strip() for area in v if area.strip()))
            if not cleaned:
                return None
            return cleaned[:5]  # Limit to 5 items
        return v

    @field_validator('constraints')
    @classmethod
    def validate_constraints(cls, v):
        """Validate constraints if provided"""
        if v is not None:
            cleaned = [constraint.strip() for constraint in v if constraint.strip()]
            return cleaned[:8] if cleaned else None
        return v


class MentalModelResult(BaseModel):
    """Result of mental model analysis"""

    model_applied: MentalModelType = Field(
        ...,
        description="Mental model that was applied"
    )

    key_insights: list[MentalModelInsight] = Field(
        ...,
        description="List of key insights from the analysis",
        min_length=1,
        max_length=10
    )

    recommendations: list[str] = Field(
        ...,
        description="Actionable recommendations based on the analysis",
        min_length=1,
        max_length=8
    )

    assumptions_identified: list[MentalModelAssumption] = Field(
        default_factory=list,
        description="Assumptions identified during analysis",
        max_length=6
    )

    fundamental_elements: list[str] | None = Field(
        None,
        description="Fundamental elements identified (for first principles)",
        max_length=8
    )

    trade_offs: list[dict[str, str]] | None = Field(
        None,
        description="Trade-offs identified (for opportunity cost)",
        max_length=5
    )

    error_paths: list[str] | None = Field(
        None,
        description="Error propagation paths identified",
        max_length=6
    )

    critical_factors: list[str] | None = Field(
        None,
        description="Critical 20% factors (for Pareto analysis)",
        max_length=5
    )

    simplified_explanation: str | None = Field(
        None,
        description="Simplified explanation (for Occam's Razor)",
        max_length=500
    )

    limitations: str | None = Field(
        None,
        description="Limitations of this analysis",
        max_length=300
    )

    next_steps: list[str] | None = Field(
        None,
        description="Suggested next steps based on analysis",
        max_length=5
    )

    processing_time_ms: int = Field(
        0,
        description="Time taken to process in milliseconds"
    )

    @field_validator('key_insights')
    @classmethod
    def validate_key_insights(cls, v):
        """Validate key insights list"""
        if not v:
            raise ValueError("At least one key insight is required")

        # Sort by relevance score (highest first)
        return sorted(v, key=lambda x: x.relevance_score, reverse=True)

    @field_validator('recommendations')
    @classmethod
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

    @field_validator('trade_offs')
    @classmethod
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

    @field_validator('fundamental_elements', 'error_paths', 'critical_factors', 'next_steps')
    @classmethod
    def validate_string_lists(cls, v):
        """Validate string lists are non-empty when provided"""
        if v is not None:
            cleaned = [item.strip() for item in v if item.strip()]
            return cleaned if cleaned else None
        return v

    def get_model_description(self) -> str:
        """Get description of the applied mental model"""
        return self.model_applied.description

    def get_top_insights(self, n: int = 3) -> list[MentalModelInsight]:
        """Get top N insights by relevance score"""
        return sorted(self.key_insights, key=lambda x: x.relevance_score, reverse=True)[:n]

    def get_high_confidence_assumptions(self, threshold: float = 0.7) -> list[MentalModelAssumption]:
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
    def suggest_mental_model(problem: str) -> list[MentalModelType]:
        """Suggest appropriate mental models for a problem"""
        suggestions = []

        for model_type in MentalModelType:
            if MentalModelUtils.validate_model_compatibility(problem, model_type):
                suggestions.append(model_type)

        # If no specific matches, suggest first principles as default
        if not suggestions:
            suggestions.append(MentalModelType.FIRST_PRINCIPLES)

        return suggestions
