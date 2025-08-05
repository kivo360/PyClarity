"""Content production and editorial templates."""

from ..base import PromptTemplate, TemplateCategory

BLOG_POST_OUTLINE = PromptTemplate(
    name="blog_post_outline",
    description="Generate detailed blog post outlines",
    template="""Generate {number} blog post outlines for {topic_industry}:
- Target audience: {reader_persona}
- Content goal: {content_goal}
- Word count target: {word_count}
- SEO focus keyword: {focus_keyword}

For each outline include:
1. Compelling title (with keyword)
2. Meta description (155 chars)
3. Hook/introduction approach
4. 3-5 main sections with subpoints
5. Practical examples/case studies
6. Key takeaways
7. Call-to-action
8. Internal linking opportunities""",
    variables=["number", "topic_industry", "reader_persona", "content_goal", "word_count", "focus_keyword"],
    category=TemplateCategory.CONTENT_PRODUCTION,
    examples=[{
        "number": "10",
        "topic_industry": "AI in healthcare",
        "reader_persona": "healthcare IT decision makers",
        "content_goal": "educate and build thought leadership",
        "word_count": "1500",
        "focus_keyword": "AI healthcare solutions"
    }],
    metadata={"content_goals": ["educate", "inspire", "convert", "engage"]}
)

SOCIAL_MEDIA_CALENDAR = PromptTemplate(
    name="social_media_calendar",
    description="Create comprehensive social media content calendar",
    template="""Create a {duration} social media content plan for {brand}:
- Platforms: {platforms}
- Posting frequency: {posting_frequency}
- Content pillars: {content_pillars}
- Brand voice: {brand_voice}

For each post include:
- Date/time (optimal for platform)
- Platform
- Content type (image, video, carousel, etc.)
- Caption with hashtags
- Visual description
- Engagement hook
- Link/CTA if applicable
- Content pillar category""",
    variables=["duration", "brand", "platforms", "posting_frequency", "content_pillars", "brand_voice"],
    category=TemplateCategory.CONTENT_PRODUCTION,
    examples=[{
        "duration": "30-day",
        "brand": "B2B SaaS productivity tool",
        "platforms": "LinkedIn, Twitter, Instagram",
        "posting_frequency": "daily on Twitter, 3x/week others",
        "content_pillars": "tips, features, success stories, industry news",
        "brand_voice": "helpful, professional, slightly witty"
    }]
)

EMAIL_NEWSLETTER_SERIES = PromptTemplate(
    name="email_newsletter_series",
    description="Design email newsletter content series",
    template="""Create {number} email newsletters for {company_product}:
- Audience: {subscriber_type}
- Newsletter goal: {primary_goal}
- Frequency: {send_frequency}
- Average length: {email_length}

For each newsletter:
1. Subject line (3 variations)
2. Preview text
3. Opening hook
4. Main content sections (3-4)
5. Secondary content/resources
6. Call-to-action
7. P.S. section
8. Suggested visuals""",
    variables=["number", "company_product", "subscriber_type", "primary_goal", "send_frequency", "email_length"],
    category=TemplateCategory.CONTENT_PRODUCTION,
    examples=[{
        "number": "12",
        "company_product": "project management software",
        "subscriber_type": "product users and trials",
        "primary_goal": "increase feature adoption",
        "send_frequency": "weekly",
        "email_length": "3-5 minute read"
    }]
)

VIDEO_SCRIPT_OUTLINE = PromptTemplate(
    name="video_script_outline",
    description="Create video content scripts and outlines",
    template="""Create {number} video script outlines for {channel_platform}:
- Video topic: {topic}
- Video length: {duration}
- Video style: {style}
- Target viewer: {viewer_persona}

For each script include:
1. Hook (first 5 seconds)
2. Introduction (context setting)
3. Main content points (3-5)
4. Visual cues and B-roll notes
5. Transitions between sections
6. Call-to-action
7. End screen elements
8. Thumbnail concept""",
    variables=["number", "channel_platform", "topic", "duration", "style", "viewer_persona"],
    category=TemplateCategory.CONTENT_PRODUCTION,
    examples=[{
        "number": "8",
        "channel_platform": "YouTube",
        "topic": "productivity tips for remote workers",
        "duration": "8-10 minutes",
        "style": "educational with motion graphics",
        "viewer_persona": "25-40 year old professionals"
    }]
)

CONTENT_REPURPOSING_PLAN = PromptTemplate(
    name="content_repurposing_plan",
    description="Transform one piece of content into multiple formats",
    template="""Create a content repurposing plan for {original_content}:
- Original format: {original_format}
- Content topic: {topic}
- Key message: {core_message}

Generate ideas for:
1. Blog post adaptation
2. Social media posts (5 platforms)
3. Email newsletter feature
4. Infographic concepts (3)
5. Video/podcast outline
6. Slide deck structure
7. Quick reference guide
8. Interactive tool/calculator
9. Case study angle
10. FAQ compilation""",
    variables=["original_content", "original_format", "topic", "core_message"],
    category=TemplateCategory.CONTENT_PRODUCTION,
    examples=[{
        "original_content": "comprehensive industry report on AI adoption",
        "original_format": "20-page PDF report",
        "topic": "AI adoption in retail",
        "core_message": "AI is transforming retail customer experience"
    }]
)

# Collection of all content production templates
CONTENT_PRODUCTION_TEMPLATES = [
    BLOG_POST_OUTLINE,
    SOCIAL_MEDIA_CALENDAR,
    EMAIL_NEWSLETTER_SERIES,
    VIDEO_SCRIPT_OUTLINE,
    CONTENT_REPURPOSING_PLAN
]
