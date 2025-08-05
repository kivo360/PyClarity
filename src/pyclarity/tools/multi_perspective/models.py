"""
Models for Multi-Perspective Analysis Cognitive Tool

Analyzes scenarios from multiple stakeholder viewpoints to identify
synergies, conflicts, and create comprehensive integration strategies.
"""

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from ..base import ComplexityLevel


class StakeholderType(str, Enum):
    """Types of stakeholders in multi-perspective analysis."""
    EXECUTIVE = "executive"
    CUSTOMER = "customer"
    EMPLOYEE = "employee"
    PARTNER = "partner"
    TECHNICAL = "technical"
    BUSINESS = "business"
    REGULATORY = "regulatory"
    SECURITY = "security"
    OPERATIONS = "operations"
    END_USER = "end_user"


class ConflictSeverity(str, Enum):
    """Severity levels for conflicts between perspectives."""
    NONE = "none"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class IntegrationApproach(str, Enum):
    """Approaches for integrating multiple perspectives."""
    CONSENSUS = "consensus"
    PRIORITIZATION = "prioritization"
    SYNTHESIS = "synthesis"
    NEGOTIATION = "negotiation"
    COMPROMISE = "compromise"
    PHASED = "phased"


class Perspective(BaseModel):
    """Represents a single stakeholder perspective."""

    perspective_id: str = Field(
        description="Unique identifier for the perspective"
    )
    stakeholder_type: StakeholderType = Field(
        description="Type of stakeholder"
    )
    stakeholder_name: str = Field(
        description="Name or title of the stakeholder group"
    )
    description: str = Field(
        description="Description of this perspective's viewpoint"
    )
    primary_concerns: list[str] = Field(
        description="Main concerns from this perspective",
        min_length=1
    )
    success_criteria: list[str] = Field(
        description="What success looks like from this perspective",
        min_length=1
    )
    influence_level: float = Field(
        description="Level of influence (0.0-1.0)",
        ge=0.0,
        le=1.0
    )
    flexibility: float = Field(
        description="Willingness to compromise (0.0-1.0)",
        ge=0.0,
        le=1.0
    )
    historical_context: str | None = Field(
        None,
        description="Relevant history affecting this perspective"
    )
    cultural_factors: list[str] | None = Field(
        default_factory=list,
        description="Cultural elements influencing this perspective"
    )


class ViewpointAnalysis(BaseModel):
    """Analysis of scenario from a specific perspective."""

    perspective_id: str = Field(
        description="ID of the analyzed perspective"
    )
    priorities: list[str] = Field(
        description="Prioritized objectives from this viewpoint",
        min_length=1
    )
    constraints: list[str] = Field(
        description="Limitations and constraints perceived"
    )
    opportunities: list[str] = Field(
        description="Opportunities seen from this perspective"
    )
    risks: list[str] = Field(
        description="Risks identified from this viewpoint"
    )
    preferred_approach: str = Field(
        description="Preferred solution approach"
    )
    acceptable_compromises: list[str] = Field(
        description="Compromises this perspective would accept"
    )
    deal_breakers: list[str] = Field(
        description="Non-negotiable requirements"
    )
    emotional_factors: list[str] = Field(
        description="Emotional elements affecting decisions"
    )
    communication_preferences: list[str] = Field(
        description="Preferred communication styles and channels"
    )
    influence_dynamics: str = Field(
        description="How this perspective influences others"
    )
    alignment_score: float = Field(
        description="How well the scenario aligns with this perspective (0.0-1.0)",
        ge=0.0,
        le=1.0
    )


class SynergyConflict(BaseModel):
    """Represents either a synergy or conflict between perspectives."""

    item_id: str = Field(
        description="Unique identifier"
    )
    type: str = Field(
        description="Either 'synergy' or 'conflict'"
    )
    perspective_a: str = Field(
        description="First perspective ID"
    )
    perspective_b: str = Field(
        description="Second perspective ID"
    )
    description: str = Field(
        description="Description of the synergy or conflict"
    )
    impact: str = Field(
        description="Impact on overall alignment"
    )
    severity: ConflictSeverity = Field(
        description="Severity level (for conflicts)"
    )
    resolution_difficulty: float = Field(
        description="Difficulty of resolution (0.0-1.0)",
        ge=0.0,
        le=1.0
    )
    mutual_benefit: bool = Field(
        description="Whether this creates mutual benefit"
    )
    exploitation_strategy: str | None = Field(
        None,
        description="How to leverage synergies"
    )
    resolution_options: list[str] | None = Field(
        default_factory=list,
        description="Options for resolving conflicts"
    )


class IntegrationStrategy(BaseModel):
    """Strategy for integrating multiple perspectives."""

    strategy_id: str = Field(
        description="Unique identifier for the strategy"
    )
    name: str = Field(
        description="Name of the integration strategy"
    )
    description: str = Field(
        description="Description of the approach"
    )
    approach_type: IntegrationApproach = Field(
        description="Type of integration approach"
    )
    target_perspectives: list[str] = Field(
        description="Perspectives targeted by this strategy"
    )
    implementation_steps: list[str] = Field(
        description="Steps to implement the strategy",
        min_length=1
    )
    expected_outcomes: list[str] = Field(
        description="Expected results from this approach"
    )
    resource_requirements: list[str] = Field(
        description="Resources needed for implementation"
    )
    timeline: str = Field(
        description="Expected timeline for implementation"
    )
    success_probability: float = Field(
        description="Estimated probability of success (0.0-1.0)",
        ge=0.0,
        le=1.0
    )
    key_risks: list[str] = Field(
        description="Main risks in this approach"
    )
    contingency_plans: list[str] | None = Field(
        default_factory=list,
        description="Backup plans if primary approach fails"
    )


class MultiPerspectiveContext(BaseModel):
    """Input for Multi-Perspective Analysis."""

    scenario: str = Field(
        description="The situation requiring multi-perspective analysis"
    )

    domain_context: str | None = Field(
        None,
        description="Domain or industry context"
    )

    predefined_perspectives: list[Perspective] | None = Field(
        None,
        description="Pre-identified perspectives to analyze"
    )

    focus_areas: list[str] | None = Field(
        default_factory=list,
        description="Specific areas to focus the analysis on"
    )

    known_constraints: list[str] | None = Field(
        default_factory=list,
        description="Known constraints affecting all perspectives"
    )

    desired_outcome: str | None = Field(
        None,
        description="Desired outcome from integration"
    )

    time_horizon: str | None = Field(
        None,
        description="Time frame for implementation"
    )

    cultural_context: str | None = Field(
        None,
        description="Cultural factors to consider"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "scenario": "Implementing a new company-wide remote work policy",
                "domain_context": "technology company",
                "focus_areas": [
                    "productivity impact",
                    "employee satisfaction",
                    "cost implications"
                ],
                "known_constraints": [
                    "Some roles require physical presence",
                    "Existing office lease commitments"
                ],
                "desired_outcome": "Policy that balances flexibility with business needs",
                "time_horizon": "6 months implementation"
            }
        }


class MultiPerspectiveResult(BaseModel):
    """Complete Multi-Perspective Analysis output."""

    input_scenario: str = Field(
        description="The analyzed scenario"
    )

    identified_perspectives: list[Perspective] = Field(
        description="All perspectives analyzed"
    )

    viewpoint_analyses: list[ViewpointAnalysis] = Field(
        description="Detailed analysis from each perspective"
    )

    synergies_conflicts: list[SynergyConflict] = Field(
        description="Identified synergies and conflicts"
    )

    integration_strategies: list[IntegrationStrategy] = Field(
        description="Strategies for integrating perspectives"
    )

    common_ground: list[str] = Field(
        description="Areas of agreement across perspectives"
    )

    critical_divergences: list[str] = Field(
        description="Critical areas of disagreement"
    )

    negotiation_framework: dict[str, Any] = Field(
        description="Framework for negotiating differences"
    )

    communication_strategies: list[str] = Field(
        description="Strategies for communicating with each perspective"
    )

    win_win_opportunities: list[str] = Field(
        description="Opportunities benefiting multiple stakeholders"
    )

    implementation_roadmap: list[str] = Field(
        description="Roadmap for implementing integrated approach"
    )

    feasibility_assessment: str = Field(
        description="Assessment of integration feasibility"
    )

    overall_assessment: str = Field(
        description="Comprehensive assessment of multi-perspective integration"
    )

    confidence_score: float = Field(
        description="Confidence in the analysis (0.0-1.0)",
        ge=0.0,
        le=1.0
    )

    processing_time_ms: float | None = Field(
        None,
        description="Processing time in milliseconds"
    )
