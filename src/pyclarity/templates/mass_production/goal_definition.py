"""Goal definition and objective setting templates."""

from ..base import PromptTemplate, TemplateCategory

SMART_GOAL_GENERATOR = PromptTemplate(
    name="smart_goal_generator",
    description="Generate SMART goals for projects or products",
    template="""Generate {number} SMART goals for {project_product}:
Context: {business_context}
Timeframe: {duration}
Resources: {available_resources}

For each goal include:
- Specific objective
- Measurable metrics
- Achievable milestones
- Relevant business impact
- Time-bound deadline""",
    variables=["number", "project_product", "business_context", "duration", "available_resources"],
    category=TemplateCategory.GOAL_DEFINITION,
    examples=[{
        "number": "5",
        "project_product": "customer retention initiative",
        "business_context": "B2B SaaS with 20% annual churn",
        "duration": "Q1 2025",
        "available_resources": "2 developers, 1 designer, $50k budget"
    }]
)

OKR_FRAMEWORK = PromptTemplate(
    name="okr_framework",
    description="Create Objectives and Key Results for strategic planning",
    template="""Create OKRs for {company_product} for {time_period}:
Mission: {company_mission}
Focus areas: {focus_areas}

Structure:
- Objective: Inspirational goal
- Key Result 1: Quantifiable outcome
- Key Result 2: Quantifiable outcome
- Key Result 3: Quantifiable outcome

Generate {number_of_objectives} objectives with 3 key results each.""",
    variables=["company_product", "time_period", "company_mission", "focus_areas", "number_of_objectives"],
    category=TemplateCategory.GOAL_DEFINITION,
    examples=[{
        "company_product": "AI writing assistant",
        "time_period": "Q2 2025",
        "company_mission": "Democratize high-quality content creation",
        "focus_areas": "user growth, product quality, revenue",
        "number_of_objectives": "3"
    }]
)

VALIDATION_METRICS = PromptTemplate(
    name="validation_metrics",
    description="Define success metrics and validation criteria",
    template="""Define validation metrics for {product_feature}:
- Primary success metric: {primary_metric}
- Target audience: {target_audience}
- Baseline performance: {baseline}

Create:
1. Leading indicators (3-5)
2. Lagging indicators (3-5)
3. Qualitative success criteria
4. Risk metrics to monitor
5. A/B test success thresholds""",
    variables=["product_feature", "primary_metric", "target_audience", "baseline"],
    category=TemplateCategory.GOAL_DEFINITION,
    examples=[{
        "product_feature": "AI-powered recommendation engine",
        "primary_metric": "click-through rate",
        "target_audience": "e-commerce shoppers",
        "baseline": "2.5% CTR"
    }]
)

MILESTONE_ROADMAP = PromptTemplate(
    name="milestone_roadmap",
    description="Create a milestone-based roadmap with clear deliverables",
    template="""Create a milestone roadmap for {project}:
Duration: {total_duration}
Team size: {team_size}
Budget: {budget}

For each milestone include:
- Name and description
- Deliverables
- Success criteria
- Dependencies
- Resource requirements
- Risk factors

Generate {number_of_milestones} milestones.""",
    variables=["project", "total_duration", "team_size", "budget", "number_of_milestones"],
    category=TemplateCategory.GOAL_DEFINITION,
    examples=[{
        "project": "mobile app MVP",
        "total_duration": "3 months",
        "team_size": "5 people",
        "budget": "$100,000",
        "number_of_milestones": "6"
    }]
)

# Collection of all goal definition templates
GOAL_DEFINITION_TEMPLATES = [
    SMART_GOAL_GENERATOR,
    OKR_FRAMEWORK,
    VALIDATION_METRICS,
    MILESTONE_ROADMAP
]
