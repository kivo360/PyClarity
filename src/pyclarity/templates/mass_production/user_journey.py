"""User journey mapping templates."""

from ..base import PromptTemplate, TemplateCategory

BASIC_USER_JOURNEY = PromptTemplate(
    name="basic_user_journey",
    description="Map user journey from start to end with pain points and solutions",
    template="""Map the user journey for {product_service} from {start_point} to {end_point}.
- Stage format: {stage_format}
- Include: user actions, pain points, emotions, touchpoints, solutions
- Output as: {output_format}""",
    variables=["product_service", "start_point", "end_point", "stage_format", "output_format"],
    category=TemplateCategory.USER_JOURNEY,
    examples=[{
        "product_service": "mobile banking app",
        "start_point": "discovering the app",
        "end_point": "becoming a loyal user",
        "stage_format": "discovery|onboarding|usage|retention|advocacy",
        "output_format": "table"
    }]
)

MULTI_PERSONA_JOURNEY = PromptTemplate(
    name="multi_persona_journey",
    description="Create journey maps for multiple user personas",
    template="""Create 3 user journey maps for {product}:
Persona 1: {persona_1_demographic} - {persona_1_use_case}
Persona 2: {persona_2_demographic} - {persona_2_use_case}
Persona 3: {persona_3_demographic} - {persona_3_use_case}

For each persona, map:
- Discovery channel
- Key decision factors
- Usage patterns
- Success metrics""",
    variables=[
        "product",
        "persona_1_demographic", "persona_1_use_case",
        "persona_2_demographic", "persona_2_use_case",
        "persona_3_demographic", "persona_3_use_case"
    ],
    category=TemplateCategory.USER_JOURNEY,
    examples=[{
        "product": "project management tool",
        "persona_1_demographic": "Tech startup founder",
        "persona_1_use_case": "team coordination",
        "persona_2_demographic": "Enterprise PM",
        "persona_2_use_case": "resource allocation",
        "persona_3_demographic": "Freelance designer",
        "persona_3_use_case": "client collaboration"
    }]
)

TOUCHPOINT_ANALYSIS = PromptTemplate(
    name="touchpoint_analysis",
    description="Analyze all user touchpoints across the customer lifecycle",
    template="""Analyze all touchpoints for {product_service} across the customer lifecycle:
- Pre-purchase touchpoints
- Purchase/onboarding touchpoints
- Usage touchpoints
- Support touchpoints
- Retention touchpoints

For each touchpoint include:
- Channel (web, mobile, email, etc.)
- User goal
- Potential friction points
- Optimization opportunities""",
    variables=["product_service"],
    category=TemplateCategory.USER_JOURNEY,
    examples=[{
        "product_service": "SaaS email marketing platform"
    }]
)

# Collection of all user journey templates
USER_JOURNEY_TEMPLATES = [
    BASIC_USER_JOURNEY,
    MULTI_PERSONA_JOURNEY,
    TOUCHPOINT_ANALYSIS
]
