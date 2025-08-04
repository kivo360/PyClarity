"""Copywriting and marketing content templates."""

from ..base import PromptTemplate, TemplateCategory

MARKETING_COPY_FACTORY = PromptTemplate(
    name="marketing_copy_factory",
    description="Generate multiple variations of marketing copy",
    template="""Generate {number} variations of {copy_type} for {product}:
- Target audience: {demographics}
- Tone: {tone}
- Length: {length}
- Key benefits: {benefits}

For each variation:
- Use different angles/hooks
- Maintain brand voice
- Include emotional triggers
- End with clear value proposition""",
    variables=["number", "copy_type", "product", "demographics", "tone", "length", "benefits"],
    category=TemplateCategory.COPYWRITING,
    examples=[{
        "number": "10",
        "copy_type": "headline",
        "product": "AI scheduling assistant",
        "demographics": "busy professionals aged 25-45",
        "tone": "professional yet friendly",
        "length": "short (under 10 words)",
        "benefits": "saves time, reduces stress, never miss meetings"
    }],
    metadata={"copy_types": ["headline", "tagline", "email_subject", "ad_copy", "cta_button"]}
)

SALES_EMAIL_SEQUENCE = PromptTemplate(
    name="sales_email_sequence",
    description="Create a complete email nurture sequence",
    template="""Create a {number}-email sequence for {product_service}:
- Audience: {target_persona}
- Pain point: {main_problem}
- Solution: {your_solution}
- Call to action: {desired_action}

Email structure:
1. Attention grabber
2. Problem agitation
3. Solution introduction
4. Social proof
5. Clear CTA

Include subject lines and preview text for each email.""",
    variables=["number", "product_service", "target_persona", "main_problem", "your_solution", "desired_action"],
    category=TemplateCategory.COPYWRITING,
    examples=[{
        "number": "5",
        "product_service": "project management software",
        "target_persona": "startup founders",
        "main_problem": "team chaos and missed deadlines",
        "your_solution": "intuitive task tracking with AI prioritization",
        "desired_action": "start free trial"
    }]
)

LANDING_PAGE_COPY = PromptTemplate(
    name="landing_page_copy",
    description="Complete landing page copy blueprint",
    template="""Generate landing page copy for {product}:
- Hero headline: {value_proposition}
- Subheadline: {supporting_statement}
- Target audience: {audience}
- Primary CTA: {main_cta}

Include:
1. Hero section (headline, subheadline, CTA)
2. Problem statement section
3. Solution overview with 3 key benefits
4. Feature highlights (5 features with descriptions)
5. Social proof section (3 testimonials)
6. FAQ section (5 questions)
7. Final CTA section
8. Trust indicators""",
    variables=["product", "value_proposition", "supporting_statement", "audience", "main_cta"],
    category=TemplateCategory.COPYWRITING,
    examples=[{
        "product": "AI content generator",
        "value_proposition": "Create months of content in minutes",
        "supporting_statement": "Powered by advanced AI that understands your brand voice",
        "audience": "content marketers and social media managers",
        "main_cta": "Start creating for free"
    }]
)

SOCIAL_MEDIA_CAPTIONS = PromptTemplate(
    name="social_media_captions",
    description="Generate platform-specific social media captions",
    template="""Create {number} social media captions for {product_campaign}:
- Platform: {platform}
- Campaign goal: {goal}
- Brand voice: {voice}
- Include hashtags: {hashtag_count}
- Content theme: {theme}

For each caption:
- Hook in first line
- Platform-appropriate length
- Engagement prompt
- Relevant hashtags
- Optional emoji usage: {emoji_style}""",
    variables=["number", "product_campaign", "platform", "goal", "voice", "hashtag_count", "theme", "emoji_style"],
    category=TemplateCategory.COPYWRITING,
    examples=[{
        "number": "20",
        "product_campaign": "new feature launch",
        "platform": "LinkedIn",
        "goal": "drive feature adoption",
        "voice": "professional and insightful",
        "hashtag_count": "3-5",
        "theme": "productivity and innovation",
        "emoji_style": "minimal"
    }],
    metadata={"platforms": ["LinkedIn", "Twitter", "Instagram", "Facebook", "TikTok"]}
)

AD_COPY_VARIATIONS = PromptTemplate(
    name="ad_copy_variations",
    description="Create multiple ad copy variations for A/B testing",
    template="""Generate {number} ad copy variations for {product}:
- Ad platform: {platform}
- Budget: {budget_range}
- Objective: {campaign_objective}
- Target audience: {audience_segment}

For each variation include:
- Headline (character limit: {headline_limit})
- Description (character limit: {description_limit})
- CTA button text
- Display URL
- Unique angle/hook""",
    variables=["number", "product", "platform", "budget_range", "campaign_objective", "audience_segment", "headline_limit", "description_limit"],
    category=TemplateCategory.COPYWRITING,
    examples=[{
        "number": "15",
        "product": "online course platform",
        "platform": "Google Ads",
        "budget_range": "$1000-5000/month",
        "campaign_objective": "lead generation",
        "audience_segment": "professionals seeking career change",
        "headline_limit": "30",
        "description_limit": "90"
    }]
)

# Collection of all copywriting templates
COPYWRITING_TEMPLATES = [
    MARKETING_COPY_FACTORY,
    SALES_EMAIL_SEQUENCE,
    LANDING_PAGE_COPY,
    SOCIAL_MEDIA_CAPTIONS,
    AD_COPY_VARIATIONS
]
