"""Business strategy and planning templates."""

from ..base import PromptTemplate, TemplateCategory

BUSINESS_MODEL_CANVAS = PromptTemplate(
    name="business_model_canvas",
    description="Generate complete Business Model Canvas",
    template="""Create a complete Business Model Canvas for {business_idea}:
Industry: {industry}
Target market size: {market_size}

Include:
1. Customer Segments: describe 3 distinct segments
2. Value Propositions: list 5 unique values
3. Channels: identify 4 distribution channels
4. Customer Relationships: define 3 relationship types
5. Revenue Streams: outline 3 revenue models
6. Key Resources: list essential resources
7. Key Activities: identify core activities
8. Key Partnerships: suggest 5 strategic partners
9. Cost Structure: breakdown main costs

Format as structured sections with bullet points.""",
    variables=["business_idea", "industry", "market_size"],
    category=TemplateCategory.BUSINESS_STRATEGY,
    examples=[{
        "business_idea": "AI-powered personal finance coach",
        "industry": "FinTech",
        "market_size": "$10B global personal finance app market"
    }]
)

COMPETITIVE_ANALYSIS = PromptTemplate(
    name="competitive_analysis",
    description="Comprehensive competitive analysis matrix",
    template="""Analyze {number} competitors for {your_product}:
Market: {market_segment}
Geography: {geography}

For each competitor analyze:
- Company name and size
- Target market
- Key features (top 5)
- Pricing model and tiers
- Strengths (3)
- Weaknesses (3)
- Market position
- Technology stack
- Marketing channels
- Differentiation opportunity

Create comparison matrix and strategic recommendations.""",
    variables=["number", "your_product", "market_segment", "geography"],
    category=TemplateCategory.BUSINESS_STRATEGY,
    examples=[{
        "number": "5",
        "your_product": "AI content creation platform",
        "market_segment": "B2B marketing tools",
        "geography": "North America"
    }]
)

GO_TO_MARKET_STRATEGY = PromptTemplate(
    name="go_to_market_strategy",
    description="Comprehensive GTM strategy plan",
    template="""Create go-to-market strategy for {product}:
- Launch timeline: {timeline}
- Budget: {budget}
- Target customer: {target_customer}
- Key differentiator: {differentiator}

Include:
1. Market positioning statement
2. Pricing strategy and tiers
3. Distribution channels (primary and secondary)
4. Marketing campaign ideas (5)
5. Sales strategy and process
6. Partnership opportunities
7. Launch sequence and milestones
8. Success metrics and KPIs
9. Risk mitigation plan""",
    variables=["product", "timeline", "budget", "target_customer", "differentiator"],
    category=TemplateCategory.BUSINESS_STRATEGY,
    examples=[{
        "product": "B2B customer success platform",
        "timeline": "Q2 2025 launch",
        "budget": "$500K marketing budget",
        "target_customer": "SaaS companies with 100-1000 customers",
        "differentiator": "AI-powered churn prediction"
    }]
)

SWOT_ANALYSIS = PromptTemplate(
    name="swot_analysis",
    description="Strategic SWOT analysis with action plans",
    template="""Conduct SWOT analysis for {company_product}:
Context: {business_context}
Market position: {market_position}
Time horizon: {time_horizon}

For each quadrant provide:
- 5 specific points
- Evidence/rationale
- Impact rating (high/medium/low)
- Recommended actions

Additionally create:
1. SO strategies (leverage strengths for opportunities)
2. WO strategies (overcome weaknesses for opportunities)
3. ST strategies (use strengths to avoid threats)
4. WT strategies (minimize weaknesses and avoid threats)""",
    variables=["company_product", "business_context", "market_position", "time_horizon"],
    category=TemplateCategory.BUSINESS_STRATEGY,
    examples=[{
        "company_product": "EdTech mobile learning app",
        "business_context": "post-launch with 10K users",
        "market_position": "emerging player in K-12 market",
        "time_horizon": "next 12 months"
    }]
)

REVENUE_MODEL_DESIGN = PromptTemplate(
    name="revenue_model_design",
    description="Design multiple revenue model options",
    template="""Design {number} revenue models for {product_service}:
- Industry: {industry}
- Target customer: {customer_type}
- Value delivered: {core_value}
- Cost structure: {cost_type}

For each model include:
1. Model type (subscription, transaction, freemium, etc.)
2. Pricing tiers and features
3. Customer acquisition cost estimate
4. Lifetime value projection
5. Break-even analysis
6. Scalability assessment
7. Implementation requirements
8. Competitive comparison""",
    variables=["number", "product_service", "industry", "customer_type", "core_value", "cost_type"],
    category=TemplateCategory.BUSINESS_STRATEGY,
    examples=[{
        "number": "4",
        "product_service": "AI writing assistant",
        "industry": "B2B SaaS",
        "customer_type": "content teams and marketers",
        "core_value": "10x content production speed",
        "cost_type": "high fixed costs, low marginal costs"
    }]
)

# Collection of all business strategy templates
BUSINESS_STRATEGY_TEMPLATES = [
    BUSINESS_MODEL_CANVAS,
    COMPETITIVE_ANALYSIS,
    GO_TO_MARKET_STRATEGY,
    SWOT_ANALYSIS,
    REVENUE_MODEL_DESIGN
]
