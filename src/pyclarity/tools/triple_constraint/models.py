"""
Models for Triple Constraint Optimizer Cognitive Tool

Analyzes situations requiring balance between three competing dimensions
(e.g., Quality/Speed/Cost, Scope/Time/Budget) and identifies optimal trade-offs.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, ClassVar

from pydantic import BaseModel, Field, field_validator, model_validator

from ..base import ComplexityLevel


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
    GROWTH = "growth"
    PROFIT = "profit"
    SUSTAINABILITY = "sustainability"

    # Product Development
    FEATURES = "features"
    USABILITY = "usability"
    MARKET_FIT = "market_fit"

    # Generic
    DIMENSION_A = "dimension_a"
    DIMENSION_B = "dimension_b"
    DIMENSION_C = "dimension_c"

    @classmethod
    def get_dimensions_by_category(cls) -> dict[str, list[ConstraintDimension]]:
        """Get dimensions organized by category."""
        return {
            "project_management": [cls.SCOPE, cls.TIME, cls.BUDGET],
            "engineering": [cls.PERFORMANCE, cls.COST, cls.RELIABILITY],
            "business": [
                cls.QUALITY,
                cls.SPEED,
                cls.PRICE,
                cls.GROWTH,
                cls.PROFIT,
                cls.SUSTAINABILITY,
            ],
            "product_development": [cls.FEATURES, cls.USABILITY, cls.MARKET_FIT],
            "generic": [cls.DIMENSION_A, cls.DIMENSION_B, cls.DIMENSION_C],
        }


class OptimizationStrategy(str, Enum):
    """Strategies for optimizing constraint balance."""

    BALANCED = "balanced"
    PRIORITIZE_A = "prioritize_a"
    PRIORITIZE_B = "prioritize_b"
    PRIORITIZE_C = "prioritize_c"
    MINIMIZE_TRADE_OFFS = "minimize_trade_offs"
    MAXIMIZE_VALUE = "maximize_value"


class ConstraintPriority(str, Enum):
    """Priority levels for constraints."""

    CRITICAL = "critical"  # Must be maintained
    HIGH = "high"  # Very important
    MEDIUM = "medium"  # Important but flexible
    LOW = "low"  # Nice to have
    FLEXIBLE = "flexible"  # Can be traded off


class TradeoffImpact(str, Enum):
    """Impact levels of trade-offs."""

    MINIMAL = "minimal"  # Barely noticeable
    LOW = "low"  # Some impact
    MODERATE = "moderate"  # Noticeable impact
    HIGH = "high"  # Significant impact
    SEVERE = "severe"  # Major consequences


class Constraint(BaseModel):
    """Individual constraint definition."""

    dimension: ConstraintDimension = Field(..., description="The constraint dimension")
    name: str = Field(..., min_length=1, description="Specific name for this constraint")
    current_value: float = Field(..., description="Current state/value")
    target_value: float = Field(..., description="Desired state/value")
    flexibility: float = Field(0.0, ge=0.0, le=1.0, description="How flexible this constraint is")
    priority: ConstraintPriority = Field(ConstraintPriority.MEDIUM)
    unit: str | None = Field(None, description="Unit of measurement")

    @model_validator(mode="after")
    def validate_constraint_values(self) -> Constraint:
        """Validate that constraint values are logical."""
        if self.current_value < 0:
            raise ValueError("Current value cannot be negative")
        if self.target_value < 0:
            raise ValueError("Target value cannot be negative")
        return self

    @property
    def gap(self) -> float:
        """Calculate the gap between current and target values."""
        return self.target_value - self.current_value

    @property
    def is_achieved(self) -> bool:
        """Check if the target value is achieved."""
        return self.current_value >= self.target_value


class Tradeoff(BaseModel):
    """Trade-off between constraints."""

    source: str = Field(..., min_length=1, description="Source constraint name")
    target: str = Field(..., min_length=1, description="Target constraint name")
    impact: float = Field(..., ge=-1.0, le=1.0, description="Impact magnitude (-1 to 1)")
    description: str = Field(..., min_length=1, description="Trade-off description")
    reversible: bool = Field(True, description="Whether trade-off can be reversed")

    @model_validator(mode="after")
    def validate_tradeoff_constraints(self) -> Tradeoff:
        """Validate that source and target constraints are different."""
        if self.source.lower() == self.target.lower():
            raise ValueError("Source and target constraints must be different")
        return self

    @property
    def is_positive(self) -> bool:
        """Check if the trade-off impact is positive."""
        return self.impact > 0

    @property
    def is_negative(self) -> bool:
        """Check if the trade-off impact is negative."""
        return self.impact < 0

    @property
    def impact_magnitude(self) -> float:
        """Get the absolute magnitude of the impact."""
        return abs(self.impact)


class Scenario(BaseModel):
    """Optimization scenario."""

    name: str = Field(..., min_length=1, description="Scenario name")
    strategy: OptimizationStrategy = Field(..., description="Optimization strategy")
    adjustments: dict[str, float] = Field(default_factory=dict, description="Proposed adjustments")
    expected_outcomes: dict[str, Any] = Field(default_factory=dict, description="Expected results")
    risk_level: str = Field("medium", description="Associated risk level")
    implementation_effort: str = Field("medium", description="Implementation effort")

    # Valid risk levels
    VALID_RISK_LEVELS: ClassVar[set[str]] = {"low", "medium", "high", "critical"}
    VALID_EFFORT_LEVELS: ClassVar[set[str]] = {"low", "medium", "high", "very_high"}

    @model_validator(mode="after")
    def validate_scenario_fields(self) -> Scenario:
        """Validate scenario fields."""
        if self.risk_level.lower() not in self.VALID_RISK_LEVELS:
            raise ValueError(f"Risk level must be one of {self.VALID_RISK_LEVELS}")
        if self.implementation_effort.lower() not in self.VALID_EFFORT_LEVELS:
            raise ValueError(f"Implementation effort must be one of {self.VALID_EFFORT_LEVELS}")
        return self


class ConstraintSet(BaseModel):
    """Represents a set of three competing constraints."""

    dimension_a: str = Field(
        min_length=1, description="First constraint dimension (e.g., Quality, Scope, Performance)"
    )
    dimension_b: str = Field(
        min_length=1, description="Second constraint dimension (e.g., Speed, Time, Cost)"
    )
    dimension_c: str = Field(
        min_length=1, description="Third constraint dimension (e.g., Cost, Budget, Reliability)"
    )

    current_values: list[float] = Field(
        description="Current balance values for each dimension (0.0-1.0)",
        min_length=3,
        max_length=3,
    )

    target_values: list[float] | None = Field(
        None, description="Target balance values for optimization", min_length=3, max_length=3
    )

    @field_validator("current_values", "target_values")
    @classmethod
    def validate_values(cls, v: list[float] | None) -> list[float] | None:
        if v is not None:
            for val in v:
                if not 0.0 <= val <= 1.0:
                    raise ValueError(f"Constraint values must be between 0.0 and 1.0, got {val}")
        return v

    @model_validator(mode="after")
    def validate_unique_dimensions(self) -> ConstraintSet:
        """Validate that all dimensions are unique."""
        dimensions = [self.dimension_a.lower(), self.dimension_b.lower(), self.dimension_c.lower()]
        if len(set(dimensions)) != 3:
            raise ValueError("All three dimensions must be unique")
        return self

    @property
    def dimensions(self) -> list[str]:
        """Get all dimensions as a list."""
        return [self.dimension_a, self.dimension_b, self.dimension_c]

    @property
    def current_balance(self) -> dict[str, float]:
        """Get current values mapped to dimensions."""
        return dict(zip(self.dimensions, self.current_values, strict=False))

    @property
    def target_balance(self) -> dict[str, float] | None:
        """Get target values mapped to dimensions, if available."""
        if self.target_values is None:
            return None
        return dict(zip(self.dimensions, self.target_values, strict=False))

    @property
    def balance_score(self) -> float:
        """Calculate a balance score (0.0-1.0) based on how balanced current values are."""
        if not self.current_values:
            return 0.0

        # Calculate standard deviation as a measure of imbalance
        import statistics

        std_dev = statistics.stdev(self.current_values)
        # Convert to balance score (lower std_dev = higher balance)
        return max(0.0, 1.0 - (std_dev * 2.0))


class TradeOffAnalysis(BaseModel):
    """Analysis of trade-offs between constraints."""

    relationship: str = Field(
        min_length=1, description="Description of the relationship between constraints"
    )
    impact_score: float = Field(
        description="Strength of the trade-off impact (0.0-1.0)", ge=0.0, le=1.0
    )
    examples: list[str] = Field(description="Concrete examples of this trade-off", min_length=1)
    mitigation_options: list[str] = Field(
        default_factory=list, description="Ways to minimize this trade-off"
    )

    @property
    def severity(self) -> TradeoffImpact:
        """Get the severity level based on impact score."""
        if self.impact_score >= 0.8:
            return TradeoffImpact.SEVERE
        if self.impact_score >= 0.6:
            return TradeoffImpact.HIGH
        if self.impact_score >= 0.4:
            return TradeoffImpact.MODERATE
        if self.impact_score >= 0.2:
            return TradeoffImpact.LOW
        return TradeoffImpact.MINIMAL

    @property
    def has_mitigation_strategies(self) -> bool:
        """Check if there are any mitigation strategies available."""
        return len(self.mitigation_options) > 0


class OptimizationRecommendation(BaseModel):
    """Recommendation for optimizing constraint balance."""

    strategy: OptimizationStrategy = Field(description="Recommended optimization strategy")
    rationale: str = Field(min_length=1, description="Explanation for this recommendation")
    action_steps: list[str] = Field(
        description="Concrete steps to implement the optimization", min_length=1
    )
    expected_outcomes: list[str] = Field(description="Expected results from this optimization")
    risks: list[str] = Field(default_factory=list, description="Potential risks or downsides")
    confidence_level: float = Field(
        description="Confidence in this recommendation (0.0-1.0)", ge=0.0, le=1.0
    )

    @property
    def risk_count(self) -> int:
        """Get the number of identified risks."""
        return len(self.risks)

    @property
    def complexity_score(self) -> float:
        """Calculate complexity score based on action steps and risks."""
        # More steps and risks = higher complexity
        steps_factor = min(len(self.action_steps) / 10.0, 1.0)
        risk_factor = min(self.risk_count / 5.0, 1.0)
        return (steps_factor + risk_factor) / 2.0

    @property
    def is_high_confidence(self) -> bool:
        """Check if this is a high-confidence recommendation."""
        return self.confidence_level >= 0.8


class TripleConstraintContext(BaseModel):
    """Input for Triple Constraint Thinking analysis."""

    scenario: str = Field(
        min_length=1, description="The scenario or decision requiring constraint analysis"
    )

    domain_context: str | None = Field(
        None, description="Domain-specific context (e.g., 'software_project', 'business_strategy')"
    )

    constraints: ConstraintSet | None = Field(None, description="Pre-defined constraints if known")

    optimization_goal: str | None = Field(
        None, description="Specific optimization goal or outcome desired"
    )

    known_trade_offs: list[str] = Field(
        default_factory=list, description="Known trade-offs to consider"
    )

    constraints_flexibility: dict[str, float] | None = Field(
        None, description="How flexible each constraint is (0.0=fixed, 1.0=very flexible)"
    )

    success_criteria: list[str] = Field(
        default_factory=list, description="Criteria for successful constraint balance"
    )

    @model_validator(mode="after")
    def validate_flexibility_values(self) -> TripleConstraintContext:
        """Validate flexibility values if provided."""
        if self.constraints_flexibility is not None:
            for constraint_name, flexibility in self.constraints_flexibility.items():
                if not 0.0 <= flexibility <= 1.0:
                    raise ValueError(
                        f"Flexibility for constraint '{constraint_name}' must be between 0.0 and 1.0, got {flexibility}"
                    )
        return self

    @property
    def has_constraints(self) -> bool:
        """Check if constraints are defined."""
        return self.constraints is not None

    @property
    def has_flexibility_info(self) -> bool:
        """Check if flexibility information is provided."""
        return self.constraints_flexibility is not None and len(self.constraints_flexibility) > 0

    @property
    def complexity_level(self) -> ComplexityLevel:
        """Determine the complexity level of the analysis."""
        factors = 0

        if self.has_constraints:
            factors += 1
        if self.has_flexibility_info:
            factors += 1
        if len(self.known_trade_offs) > 2:
            factors += 1
        if len(self.success_criteria) > 2:
            factors += 1
        if self.optimization_goal is not None:
            factors += 1

        if factors <= 2:
            return ComplexityLevel.SIMPLE
        if factors <= 4:
            return ComplexityLevel.MODERATE
        return ComplexityLevel.COMPLEX

    class Config:
        json_schema_extra = {
            "example": {
                "scenario": "Developing a new mobile app with limited resources",
                "domain_context": "software_development",
                "optimization_goal": "Launch MVP within 3 months",
                "known_trade_offs": [
                    "Faster development means fewer features",
                    "Lower cost means less experienced developers",
                ],
                "success_criteria": [
                    "Core features implemented",
                    "Within budget constraints",
                    "Acceptable quality for MVP",
                ],
            }
        }


class TripleConstraintResult(BaseModel):
    """Complete Triple Constraint Thinking analysis output."""

    input_scenario: str = Field(min_length=1, description="The analyzed scenario")

    identified_constraints: ConstraintSet = Field(
        description="The three competing constraints identified"
    )

    current_state_analysis: str = Field(
        min_length=1, description="Analysis of the current constraint balance"
    )

    trade_off_analyses: list[TradeOffAnalysis] = Field(
        description="Detailed analysis of trade-offs between constraints"
    )

    optimization_recommendations: list[OptimizationRecommendation] = Field(
        description="Recommendations for optimizing constraint balance"
    )

    domain_specific_insights: list[str] = Field(
        description="Insights specific to the problem domain"
    )

    visual_representation: dict[str, Any] | None = Field(
        None, description="Data for visualizing the constraint triangle"
    )

    key_decisions: list[str] = Field(description="Key decisions needed to manage constraints")

    success_metrics: list[str] = Field(description="Metrics to track constraint management success")

    overall_assessment: str = Field(
        min_length=1, description="Overall assessment of constraint management approach"
    )

    confidence_score: float = Field(
        description="Overall confidence in the analysis (0.0-1.0)", ge=0.0, le=1.0
    )
    processing_time_ms: float | None = Field(
        None, ge=0.0, description="Processing time in milliseconds"
    )

    @property
    def has_high_confidence(self) -> bool:
        """Check if the analysis has high confidence."""
        return self.confidence_score >= 0.8

    @property
    def has_recommendations(self) -> bool:
        """Check if there are any optimization recommendations."""
        return len(self.optimization_recommendations) > 0

    @property
    def has_trade_offs(self) -> bool:
        """Check if there are any trade-off analyses."""
        return len(self.trade_off_analyses) > 0

    @property
    def primary_recommendation(self) -> OptimizationRecommendation | None:
        """Get the highest confidence recommendation."""
        if not self.has_recommendations:
            return None

        return max(self.optimization_recommendations, key=lambda r: r.confidence_level)

    @property
    def most_critical_tradeoff(self) -> TradeOffAnalysis | None:
        """Get the most critical trade-off analysis."""
        if not self.has_trade_offs:
            return None

        return max(self.trade_off_analyses, key=lambda t: t.impact_score)

    def get_recommendations_by_strategy(
        self, strategy: OptimizationStrategy
    ) -> list[OptimizationRecommendation]:
        """Get recommendations filtered by strategy."""
        return [r for r in self.optimization_recommendations if r.strategy == strategy]

    def get_tradeoffs_by_severity(self, severity: TradeoffImpact) -> list[TradeOffAnalysis]:
        """Get trade-offs filtered by severity level."""
        return [t for t in self.trade_off_analyses if t.severity == severity]
