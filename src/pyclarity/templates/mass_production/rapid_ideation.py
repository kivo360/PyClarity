"""Rapid ideation and zero-to-product templates."""

from ..base import PromptTemplate, TemplateCategory

ZERO_TO_PRODUCT_SPRINT = PromptTemplate(
    name="zero_to_product_sprint",
    description="Complete product concept from scratch in 60 minutes",
    template="""Generate a complete product concept in 60 minutes for {industry}:
Budget: {budget_range}
Timeline: {launch_timeline}
Team size: {team_size}

Create in this sequence:
1. Problem identification (10 min)
   - Target user pain points
   - Market gap analysis
   - Urgency/importance matrix

2. Solution brainstorm (10 min)
   - Core value proposition
   - Unique differentiators
   - Technical approach

3. Target market definition (10 min)
   - Primary persona
   - Market size (TAM/SAM/SOM)
   - Early adopter profile

4. MVP feature list (10 min)
   - Must-have features (3-5)
   - Nice-to-have features
   - Explicitly out of scope

5. Go-to-market strategy (10 min)
   - Launch channels
   - Pricing model
   - First 100 customers plan

6. Success metrics (10 min)
   - KPIs and targets
   - Validation milestones
   - Pivot triggers""",
    variables=["industry", "budget_range", "launch_timeline", "team_size"],
    category=TemplateCategory.RAPID_IDEATION,
    examples=[{
        "industry": "EdTech",
        "budget_range": "$50-100k",
        "launch_timeline": "3 months",
        "team_size": "3-person team"
    }]
)

STARTUP_IDEA_VALIDATOR = PromptTemplate(
    name="startup_idea_validator",
    description="Validate startup ideas across multiple dimensions",
    template="""Validate {startup_idea} comprehensively:
Founder background: {founder_profile}
Available resources: {resources}
Risk tolerance: {risk_level}

Analyze:
1. Market validation
   - Size estimation (with sources)
   - Growth trajectory
   - Competitive landscape

2. Technical feasibility
   - Required technology stack
   - Development complexity
   - Technical risks

3. Business model viability
   - Revenue streams
   - Unit economics
   - Path to profitability

4. Customer validation
   - Target customer profile
   - Value proposition fit
   - Acquisition channels

5. Execution risk assessment
   - Key assumptions
   - Major risks
   - Mitigation strategies

6. MVP definition
   - Core features
   - Build timeline
   - Launch strategy

7. 90-day action plan
   - Week-by-week milestones
   - Resource allocation
   - Success criteria""",
    variables=["startup_idea", "founder_profile", "resources", "risk_level"],
    category=TemplateCategory.RAPID_IDEATION,
    examples=[{
        "startup_idea": "AI-powered personal shopping assistant",
        "founder_profile": "technical founder with e-commerce experience",
        "resources": "$25k budget, 6 months runway",
        "risk_level": "moderate - willing to pivot"
    }]
)

RAPID_PROTOTYPE_GENERATOR = PromptTemplate(
    name="rapid_prototype_generator",
    description="Create testable prototypes in 1 hour",
    template="""Create rapid prototype for {product_idea}:
- Prototype format: {format}
- Testing goal: {test_goal}
- Target users: {test_users}
- Time limit: 1 hour

Generate:
1. Core concept visualization
   - Main screen/interface mockup
   - Key user flow (3-5 steps)
   - Visual hierarchy

2. Feature specifications
   - Primary feature details
   - User interactions
   - Data requirements

3. Testing script
   - Introduction to testers
   - Tasks to complete
   - Questions to ask

4. Feedback collection plan
   - Metrics to track
   - Qualitative feedback areas
   - Success criteria

5. Iteration roadmap
   - Priority improvements
   - Next prototype version
   - Timeline to MVP""",
    variables=["product_idea", "format", "test_goal", "test_users"],
    category=TemplateCategory.RAPID_IDEATION,
    examples=[{
        "product_idea": "voice-controlled task manager",
        "format": "interactive wireframe",
        "test_goal": "validate voice command usability",
        "test_users": "busy professionals"
    }],
    metadata={"formats": ["wireframe", "landing page", "pitch deck", "demo video", "clickable prototype"]}
)

IDEA_PIVOT_MATRIX = PromptTemplate(
    name="idea_pivot_matrix",
    description="Generate pivot options when original idea needs adjustment",
    template="""Generate {number} pivot options for {original_idea}:
- Current challenge: {main_problem}
- Assets to preserve: {existing_assets}
- Constraints: {constraints}

For each pivot option:
1. Pivot type (zoom-in, zoom-out, platform, segment, etc.)
2. New value proposition
3. Target market adjustment
4. Required changes
5. Preserved elements
6. Risk assessment
7. Validation approach
8. 30-day test plan
9. Success indicators
10. Resource requirements""",
    variables=["number", "original_idea", "main_problem", "existing_assets", "constraints"],
    category=TemplateCategory.RAPID_IDEATION,
    examples=[{
        "number": "5",
        "original_idea": "B2C fitness tracking app",
        "main_problem": "high customer acquisition cost",
        "existing_assets": "AI algorithm, mobile app codebase",
        "constraints": "limited marketing budget, 2-person team"
    }]
)

WEEKEND_PROJECT_PLANNER = PromptTemplate(
    name="weekend_project_planner",
    description="Plan executable weekend projects for quick validation",
    template="""Plan weekend project for {project_idea}:
- Available time: {hours} hours
- Skills available: {skills}
- Budget: {budget}
- Success metric: {metric}

Create hour-by-hour plan:

Saturday:
- Hours 1-2: {task}
- Hours 3-4: {task}
- Hours 5-6: {task}
- Hours 7-8: {task}

Sunday:
- Hours 1-2: {task}
- Hours 3-4: {task}
- Hours 5-6: {task}
- Hours 7-8: {task}

Include:
- Tool/resource list
- Potential blockers
- Minimum viable outcome
- Stretch goals
- Monday morning next steps""",
    variables=["project_idea", "hours", "skills", "budget", "metric"],
    category=TemplateCategory.RAPID_IDEATION,
    examples=[{
        "project_idea": "landing page for new SaaS idea",
        "hours": "16",
        "skills": "basic coding, design, copywriting",
        "budget": "$100",
        "metric": "50 email signups"
    }]
)

MICRO_SAAS_GENERATOR = PromptTemplate(
    name="micro_saas_generator",
    description="Generate micro-SaaS ideas that can be built quickly",
    template="""Generate {number} micro-SaaS ideas for {target_market}:
- Development time: {dev_time}
- Price range: {price_range}
- Required skills: {skill_level}
- Market characteristics: {market_traits}

For each idea include:
1. Product name and tagline
2. Specific problem solved
3. Target user (very specific)
4. Core features (3 maximum)
5. Tech stack required
6. MVP development steps
7. Pricing model
8. Marketing channels
9. First 10 customers strategy
10. Monthly revenue potential""",
    variables=["number", "target_market", "dev_time", "price_range", "skill_level", "market_traits"],
    category=TemplateCategory.RAPID_IDEATION,
    examples=[{
        "number": "20",
        "target_market": "solopreneurs and freelancers",
        "dev_time": "under 30 days",
        "price_range": "$19-49/month",
        "skill_level": "no-code or basic coding",
        "market_traits": "underserved niches with clear pain points"
    }]
)

# Collection of all rapid ideation templates
RAPID_IDEATION_TEMPLATES = [
    ZERO_TO_PRODUCT_SPRINT,
    STARTUP_IDEA_VALIDATOR,
    RAPID_PROTOTYPE_GENERATOR,
    IDEA_PIVOT_MATRIX,
    WEEKEND_PROJECT_PLANNER,
    MICRO_SAAS_GENERATOR
]
