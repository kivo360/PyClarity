"""Product development and feature planning templates."""

from ..base import PromptTemplate, TemplateCategory

FEATURE_IDEATION = PromptTemplate(
    name="feature_ideation",
    description="Generate feature ideas with implementation details",
    template="""Generate {number} feature ideas for {product_type}:
- User problem: {core_problem}
- Market: {target_market}
- Constraints: {constraints}

For each feature:
- Name
- Description (50 words)
- User benefit
- Implementation complexity (1-5)
- Priority score (1-10)
- Dependencies
- Success metrics""",
    variables=["number", "product_type", "core_problem", "target_market", "constraints"],
    category=TemplateCategory.PRODUCT_DEVELOPMENT,
    examples=[{
        "number": "20",
        "product_type": "task management app",
        "core_problem": "team collaboration across time zones",
        "target_market": "distributed software teams",
        "constraints": "mobile-first, 3-month timeline, $50k budget"
    }]
)

USER_STORY_GENERATOR = PromptTemplate(
    name="user_story_generator",
    description="Mass produce user stories for agile development",
    template="""Create {total_number} user stories for {feature_product}:
Format: As a [USER_TYPE], I want to [ACTION] so that [BENEFIT]

Categories:
- Core functionality ({core_number} stories)
- Edge cases ({edge_number} stories)
- Admin features ({admin_number} stories)
- Mobile experience ({mobile_number} stories)

Include:
- Acceptance criteria for each story
- Story points estimate (1, 2, 3, 5, 8)
- Priority (high, medium, low)""",
    variables=["total_number", "feature_product", "core_number", "edge_number", "admin_number", "mobile_number"],
    category=TemplateCategory.PRODUCT_DEVELOPMENT,
    examples=[{
        "total_number": "40",
        "feature_product": "AI chatbot for customer support",
        "core_number": "15",
        "edge_number": "10",
        "admin_number": "8",
        "mobile_number": "7"
    }]
)

MVP_DEFINITION = PromptTemplate(
    name="mvp_definition",
    description="Define MVP scope and features",
    template="""Define MVP for {product_concept}:
- Target launch: {timeline}
- Budget: {budget}
- Team size: {team_size}
- Primary user: {primary_user}

Create:
1. Core feature list (must-have)
2. Nice-to-have features (phase 2)
3. Out of scope items
4. Technical requirements
5. Success criteria
6. Go-to-market strategy
7. Risk mitigation plan""",
    variables=["product_concept", "timeline", "budget", "team_size", "primary_user"],
    category=TemplateCategory.PRODUCT_DEVELOPMENT,
    examples=[{
        "product_concept": "AI-powered resume builder",
        "timeline": "8 weeks",
        "budget": "$30,000",
        "team_size": "3 developers, 1 designer",
        "primary_user": "job seekers in tech"
    }]
)

TECHNICAL_SPECIFICATION = PromptTemplate(
    name="technical_specification",
    description="Generate technical specs for features",
    template="""Create technical specification for {feature_name}:
- Product: {product}
- Integration points: {integrations}
- Performance requirements: {performance_reqs}
- Security requirements: {security_reqs}

Include:
1. Architecture overview
2. API endpoints needed
3. Data models
4. State management
5. Error handling
6. Testing approach
7. Deployment considerations
8. Monitoring and logging""",
    variables=["feature_name", "product", "integrations", "performance_reqs", "security_reqs"],
    category=TemplateCategory.PRODUCT_DEVELOPMENT,
    examples=[{
        "feature_name": "real-time collaboration",
        "product": "document editor",
        "integrations": "WebSocket, Redis, PostgreSQL",
        "performance_reqs": "sub-100ms latency, support 50 concurrent users",
        "security_reqs": "end-to-end encryption, GDPR compliant"
    }]
)

PRODUCT_ROADMAP = PromptTemplate(
    name="product_roadmap",
    description="Create a comprehensive product roadmap",
    template="""Create a {duration} product roadmap for {product}:
- Vision: {product_vision}
- Current state: {current_state}
- Target market growth: {growth_target}

For each quarter/phase:
1. Theme and objectives
2. Major features/epics
3. Technical debt items
4. Infrastructure improvements
5. Success metrics
6. Resource allocation
7. Dependencies and risks""",
    variables=["duration", "product", "product_vision", "current_state", "growth_target"],
    category=TemplateCategory.PRODUCT_DEVELOPMENT,
    examples=[{
        "duration": "12-month",
        "product": "B2B analytics platform",
        "product_vision": "become the standard for real-time business intelligence",
        "current_state": "MVP with 100 customers",
        "growth_target": "1000 customers, $1M ARR"
    }]
)

# Collection of all product development templates
PRODUCT_DEVELOPMENT_TEMPLATES = [
    FEATURE_IDEATION,
    USER_STORY_GENERATOR,
    MVP_DEFINITION,
    TECHNICAL_SPECIFICATION,
    PRODUCT_ROADMAP
]
