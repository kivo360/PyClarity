# Clear Thinking FastMCP Server - Multi-Perspective Analysis Models

"""
Pydantic models for Multi-Perspective Analysis cognitive tool.

This model enables comprehensive analysis from multiple stakeholder viewpoints,
revealing blind spots, conflicts, and opportunities for alignment across
different perspectives and interests.
"""

from typing import List, Dict, Optional, Literal, Any
from pydantic import BaseModel, Field, field_validator, ConfigDict
from enum import Enum

from .base import CognitiveInputBase, CognitiveOutputBase, ComplexityLevel


class PerspectiveType(str, Enum):
    """Types of perspectives for analysis."""
    STAKEHOLDER = "stakeholder"      # Direct stakeholder view
    FUNCTIONAL = "functional"         # Department/function view
    TEMPORAL = "temporal"            # Time-based view (short/long term)
    CULTURAL = "cultural"            # Cultural/values view
    ECONOMIC = "economic"            # Financial/economic view
    TECHNICAL = "technical"          # Technical/implementation view
    STRATEGIC = "strategic"          # Strategic/competitive view
    CUSTOMER = "customer"            # End-user/customer view
    REGULATORY = "regulatory"        # Compliance/legal view
    ETHICAL = "ethical"              # Ethical/moral view


class AlignmentLevel(str, Enum):
    """Level of alignment between perspectives."""
    STRONG_CONFLICT = "strong_conflict"
    MODERATE_CONFLICT = "moderate_conflict"
    NEUTRAL = "neutral"
    MODERATE_ALIGNMENT = "moderate_alignment"
    STRONG_ALIGNMENT = "strong_alignment"


class ConflictResolutionStrategy(str, Enum):
    """Strategies for resolving perspective conflicts."""
    COMPROMISE = "compromise"              # Find middle ground
    PRIORITIZATION = "prioritization"      # Prioritize one view
    INTEGRATION = "integration"            # Integrate multiple views
    SEQUENCING = "sequencing"             # Address in sequence
    REFRAMING = "reframing"               # Reframe the problem
    NEGOTIATION = "negotiation"           # Negotiate trade-offs
    CONSENSUS_BUILDING = "consensus_building"  # Build consensus


class Perspective(BaseModel):
    """Represents a single perspective or viewpoint."""
    model_config = ConfigDict(use_enum_values=True)
    
    name: str = Field(
        description="Name of the perspective holder or viewpoint"
    )
    
    perspective_type: PerspectiveType = Field(
        description="Type of perspective"
    )
    
    key_interests: List[str] = Field(
        description="Primary interests or concerns from this perspective",
        min_length=1
    )
    
    priorities: List[str] = Field(
        description="Top priorities from this viewpoint",
        min_length=1
    )
    
    concerns: List[str] = Field(
        default_factory=list,
        description="Major concerns or risks perceived"
    )
    
    success_criteria: List[str] = Field(
        description="What success looks like from this perspective",
        min_length=1
    )
    
    constraints: List[str] = Field(
        default_factory=list,
        description="Constraints or limitations from this viewpoint"
    )
    
    influence_level: float = Field(
        default=0.5,
        description="Level of influence (0.0-1.0)",
        ge=0.0,
        le=1.0
    )
    
    emotional_stance: Optional[str] = Field(
        None,
        description="Emotional position (supportive, resistant, neutral, etc.)"
    )


class PerspectiveComparison(BaseModel):
    """Comparison between two perspectives."""
    model_config = ConfigDict(use_enum_values=True)
    
    perspective_a: str = Field(
        description="First perspective name"
    )
    
    perspective_b: str = Field(
        description="Second perspective name"
    )
    
    alignment_level: AlignmentLevel = Field(
        description="Level of alignment between perspectives"
    )
    
    common_ground: List[str] = Field(
        default_factory=list,
        description="Areas of agreement or shared interest"
    )
    
    conflicts: List[str] = Field(
        default_factory=list,
        description="Areas of disagreement or conflict"
    )
    
    complementary_aspects: List[str] = Field(
        default_factory=list,
        description="Ways perspectives complement each other"
    )
    
    tension_points: List[str] = Field(
        default_factory=list,
        description="Specific points of tension"
    )
    
    potential_synergies: List[str] = Field(
        default_factory=list,
        description="Opportunities for synergy"
    )


class BlindSpot(BaseModel):
    """Represents a blind spot identified through multi-perspective analysis."""
    model_config = ConfigDict(use_enum_values=True)
    
    description: str = Field(
        description="Description of the blind spot"
    )
    
    affected_perspectives: List[str] = Field(
        description="Perspectives that miss this aspect",
        min_length=1
    )
    
    revealing_perspectives: List[str] = Field(
        description="Perspectives that highlight this aspect",
        min_length=1
    )
    
    impact: str = Field(
        description="Potential impact of this blind spot"
    )
    
    mitigation_strategies: List[str] = Field(
        default_factory=list,
        description="Ways to address the blind spot"
    )


class ConflictResolution(BaseModel):
    """Resolution approach for perspective conflicts."""
    model_config = ConfigDict(use_enum_values=True)
    
    conflict_description: str = Field(
        description="Description of the conflict"
    )
    
    involved_perspectives: List[str] = Field(
        description="Perspectives involved in the conflict",
        min_length=2
    )
    
    resolution_strategy: ConflictResolutionStrategy = Field(
        description="Recommended resolution strategy"
    )
    
    action_steps: List[str] = Field(
        description="Steps to resolve the conflict",
        min_length=1
    )
    
    expected_outcomes: List[str] = Field(
        description="Expected results of resolution"
    )
    
    success_probability: float = Field(
        description="Likelihood of successful resolution (0.0-1.0)",
        ge=0.0,
        le=1.0
    )
    
    risks: List[str] = Field(
        default_factory=list,
        description="Risks in the resolution approach"
    )


class IntegrationOpportunity(BaseModel):
    """Opportunity to integrate multiple perspectives."""
    model_config = ConfigDict(use_enum_values=True)
    
    opportunity_description: str = Field(
        description="Description of the integration opportunity"
    )
    
    perspectives_to_integrate: List[str] = Field(
        description="Perspectives that can be integrated",
        min_length=2
    )
    
    integration_approach: str = Field(
        description="How to integrate these perspectives"
    )
    
    expected_benefits: List[str] = Field(
        description="Benefits of integration",
        min_length=1
    )
    
    implementation_steps: List[str] = Field(
        description="Steps to achieve integration"
    )
    
    complexity_level: str = Field(
        description="Complexity of integration (low, medium, high)"
    )


class MultiPerspectiveInput(CognitiveInputBase):
    """Input for Multi-Perspective Analysis."""
    
    scenario: str = Field(
        default="",
        description="The situation or decision requiring multi-perspective analysis"
    )
    
    domain_context: Optional[str] = Field(
        None,
        description="Domain context (e.g., 'organizational_change', 'product_development', 'policy_making')"
    )
    
    predefined_perspectives: Optional[List[Perspective]] = Field(
        None,
        description="Pre-defined perspectives if known"
    )
    
    primary_decision: Optional[str] = Field(
        None,
        description="The main decision or question to analyze"
    )
    
    stakeholder_map: Optional[Dict[str, str]] = Field(
        None,
        description="Map of stakeholders and their roles"
    )
    
    analysis_depth: Optional[Literal["quick", "standard", "comprehensive"]] = Field(
        "standard",
        description="Depth of perspective analysis"
    )
    
    conflict_tolerance: Optional[str] = Field(
        None,
        description="Organization's tolerance for conflict (low, medium, high)"
    )
    
    time_horizon: Optional[str] = Field(
        None,
        description="Time horizon for considering impacts"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "scenario": "Implementing AI automation in customer service department",
                "domain_context": "organizational_change",
                "primary_decision": "How to implement AI while maintaining service quality and employee morale",
                "stakeholder_map": {
                    "Customer Service Reps": "Directly affected employees",
                    "Customers": "End users of the service",
                    "Management": "Decision makers and budget holders",
                    "IT Department": "Implementation team",
                    "HR Department": "Employee relations and training"
                },
                "analysis_depth": "comprehensive",
                "conflict_tolerance": "medium",
                "time_horizon": "2 years"
            }
        }


class MultiPerspectiveAnalysis(CognitiveOutputBase):
    """Complete Multi-Perspective Analysis output."""
    
    input_scenario: str = Field(
        description="The analyzed scenario"
    )
    
    identified_perspectives: List[Perspective] = Field(
        description="All perspectives identified and analyzed"
    )
    
    perspective_comparisons: List[PerspectiveComparison] = Field(
        description="Comparisons between different perspectives"
    )
    
    blind_spots: List[BlindSpot] = Field(
        description="Blind spots revealed through multi-perspective analysis"
    )
    
    conflict_resolutions: List[ConflictResolution] = Field(
        description="Approaches to resolve identified conflicts"
    )
    
    integration_opportunities: List[IntegrationOpportunity] = Field(
        description="Opportunities to integrate perspectives"
    )
    
    alignment_matrix: Dict[str, Dict[str, AlignmentLevel]] = Field(
        description="Matrix showing alignment between all perspective pairs"
    )
    
    influence_analysis: Dict[str, float] = Field(
        description="Influence level of each perspective"
    )
    
    consensus_areas: List[str] = Field(
        description="Areas where most perspectives agree"
    )
    
    divergence_areas: List[str] = Field(
        description="Areas of significant divergence"
    )
    
    synthesis_insights: List[str] = Field(
        description="Insights from synthesizing all perspectives"
    )
    
    recommended_approach: str = Field(
        description="Recommended approach considering all perspectives"
    )
    
    implementation_considerations: List[str] = Field(
        description="Key considerations for implementation"
    )
    
    communication_strategy: List[str] = Field(
        description="How to communicate with different perspectives"
    )
    
    visual_representation: Optional[Dict[str, Any]] = Field(
        None,
        description="Data for visualizing perspective relationships"
    )
    
    overall_assessment: str = Field(
        description="Overall assessment of the multi-perspective landscape"
    )
    
    confidence_level: float = Field(
        description="Confidence in the analysis (0.0-1.0)",
        ge=0.0,
        le=1.0
    )