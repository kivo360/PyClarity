# Marketing Frameworks Library

This document contains marketing frameworks organized with Jinja2 templates for campaign and strategy generation.

## Marketing Campaign Frameworks

### 1. STP Framework (Segmentation-Targeting-Positioning)

```jinja2
{# STP Marketing Strategy Template #}

# {{ campaign_name }} - STP Strategy

## 📊 Market Segmentation
{% for segment in market_segments %}
### Segment {{ loop.index }}: {{ segment.name }}
- **Demographics**: {{ segment.demographics }}
- **Psychographics**: {{ segment.psychographics }}
- **Behaviors**: {{ segment.behaviors }}
- **Size**: {{ segment.market_size }}
- **Growth**: {{ segment.growth_rate }}
{% endfor %}

## 🎯 Target Market Selection
**Primary Target**: {{ primary_target.name }}
- **Why**: {{ primary_target.rationale }}
- **Accessibility**: {{ primary_target.accessibility }}
- **Profitability**: {{ primary_target.profitability }}

{% if secondary_targets %}
**Secondary Targets**:
{% for target in secondary_targets %}
- {{ target.name }}: {{ target.reason }}
{% endfor %}
{% endif %}

## 🏆 Positioning Strategy
**Positioning Statement**: {{ positioning.statement }}

**Key Differentiators**:
{% for diff in positioning.differentiators %}
- {{ diff }}
{% endfor %}

**Value Proposition**: {{ positioning.value_prop }}

**Competitive Frame**: {{ positioning.competitive_frame }}

### Implementation Channels
{% for channel in marketing_channels %}
- {{ channel.name }}: {{ channel.strategy }}
{% endfor %}
```

### 2. SOSTAC Framework (Situation-Objectives-Strategy-Tactics-Action-Control)

```jinja2
{# SOSTAC Marketing Planning Template #}

# {{ project_name }} - SOSTAC Plan

## 📍 Situation Analysis
### Where are we now?

**Market Position**: {{ situation.market_position }}
**SWOT Analysis**:
- **Strengths**: {% for s in situation.strengths %}{{ s }}{% if not loop.last %}, {% endif %}{% endfor %}
- **Weaknesses**: {% for w in situation.weaknesses %}{{ w }}{% if not loop.last %}, {% endif %}{% endfor %}
- **Opportunities**: {% for o in situation.opportunities %}{{ o }}{% if not loop.last %}, {% endif %}{% endfor %}
- **Threats**: {% for t in situation.threats %}{{ t }}{% if not loop.last %}, {% endif %}{% endfor %}

**Customer Insights**: {{ situation.customer_insights }}

## 🎯 Objectives
### Where do we want to be?

{% for objective in objectives %}
{{ loop.index }}. **{{ objective.type }}**: {{ objective.goal }}
   - Metric: {{ objective.metric }}
   - Target: {{ objective.target }}
   - Timeline: {{ objective.timeline }}
{% endfor %}

## 🧭 Strategy
### How do we get there?

**Core Strategy**: {{ strategy.core_approach }}

**Strategic Pillars**:
{% for pillar in strategy.pillars %}
- **{{ pillar.name }}**: {{ pillar.description }}
{% endfor %}

## 🛠️ Tactics
### Specific actions to execute strategy

{% for tactic in tactics %}
### {{ tactic.category }}
{% for action in tactic.actions %}
- {{ action.task }} ({{ action.timeline }})
  - Channel: {{ action.channel }}
  - Budget: {{ action.budget }}
{% endfor %}
{% endfor %}

## 🚀 Action Plan
### Who does what and when?

{% for action in action_plan %}
| Task | Owner | Deadline | Dependencies |
|------|-------|----------|--------------|
| {{ action.task }} | {{ action.owner }} | {{ action.deadline }} | {{ action.dependencies|default('None') }} |
{% endfor %}

## 📊 Control
### How do we monitor and optimize?

**KPIs to Track**:
{% for kpi in control.kpis %}
- {{ kpi.name }}: {{ kpi.target }} (Measured: {{ kpi.frequency }})
{% endfor %}

**Review Schedule**: {{ control.review_schedule }}
**Optimization Process**: {{ control.optimization_process }}
```

### 3. 7Ps Marketing Mix Framework

```jinja2
{# 7Ps Marketing Mix Template #}

# {{ product_name }} - 7Ps Marketing Mix

## 1️⃣ Product
**Core Offering**: {{ product.core }}
**Features**:
{% for feature in product.features %}
- {{ feature.name }}: {{ feature.benefit }}
{% endfor %}
**Lifecycle Stage**: {{ product.lifecycle_stage }}

## 2️⃣ Price
**Pricing Strategy**: {{ price.strategy }}
**Price Points**:
{% for tier in price.tiers %}
- **{{ tier.name }}**: {{ tier.price }} - {{ tier.target_segment }}
{% endfor %}
**Value Justification**: {{ price.value_justification }}

## 3️⃣ Place
**Distribution Channels**:
{% for channel in place.channels %}
- **{{ channel.type }}**: {{ channel.coverage }} ({{ channel.percentage }}% of sales)
{% endfor %}
**Geographic Coverage**: {{ place.geographic_coverage }}

## 4️⃣ Promotion
**Promotional Mix**:
{% for promo in promotion.mix %}
### {{ promo.type }}
- Budget: {{ promo.budget }}
- Channels: {{ promo.channels|join(', ') }}
- Message: "{{ promo.message }}"
{% endfor %}

## 5️⃣ People
**Customer-Facing Roles**:
{% for role in people.roles %}
- **{{ role.title }}**: {{ role.responsibility }}
  - Training: {{ role.training_required }}
{% endfor %}
**Service Standards**: {{ people.service_standards }}

## 6️⃣ Process
**Customer Journey Steps**:
{% for step in process.customer_journey %}
{{ loop.index }}. {{ step.name }} → {{ step.action }}
   - Time: {{ step.duration }}
   - Touchpoint: {{ step.touchpoint }}
{% endfor %}

## 7️⃣ Physical Evidence
**Brand Touchpoints**:
{% for evidence in physical_evidence %}
- **{{ evidence.type }}**: {{ evidence.description }}
  - Impact: {{ evidence.brand_impact }}
{% endfor %}
```

### 4. Growth Hacking Framework (AARRR - Pirate Metrics)

```jinja2
{# AARRR Growth Hacking Template #}

# {{ startup_name }} - Growth Hacking Strategy

## 🚢 AARRR Funnel Overview

{% for stage in aarrr_stages %}
### {{ stage.icon }} {{ stage.name }}
**Definition**: {{ stage.definition }}
**Current Rate**: {{ stage.current_rate }}
**Target Rate**: {{ stage.target_rate }}
**Timeline**: {{ stage.timeline }}
{% endfor %}

## 📈 Growth Experiments

### 1. Acquisition Experiments
{% for exp in acquisition_experiments %}
#### Experiment {{ loop.index }}: {{ exp.name }}
- **Hypothesis**: {{ exp.hypothesis }}
- **Channel**: {{ exp.channel }}
- **Budget**: {{ exp.budget }}
- **Success Metric**: {{ exp.metric }}
- **Test Duration**: {{ exp.duration }}
{% endfor %}

### 2. Activation Experiments
{% for exp in activation_experiments %}
#### {{ exp.name }}
- **Change**: {{ exp.change }}
- **Expected Impact**: {{ exp.expected_impact }}
- **Implementation**: {{ exp.implementation }}
{% endfor %}

### 3. Retention Strategies
{% for strategy in retention_strategies %}
- **{{ strategy.name }}**: {{ strategy.description }}
  - Trigger: {{ strategy.trigger }}
  - Frequency: {{ strategy.frequency }}
{% endfor %}

### 4. Revenue Optimization
{% for tactic in revenue_tactics %}
#### {{ tactic.type }}
- Approach: {{ tactic.approach }}
- Expected Lift: {{ tactic.expected_lift }}
- Risk Level: {{ tactic.risk_level }}
{% endfor %}

### 5. Referral Program
**Program Name**: {{ referral.program_name }}
**Incentive Structure**:
- Referrer Gets: {{ referral.referrer_reward }}
- Referee Gets: {{ referral.referee_reward }}
**Viral Coefficient Target**: {{ referral.viral_coefficient }}

## 🔬 Testing Framework
**Prioritization**: {{ testing.prioritization_method }}
**Test Velocity**: {{ testing.tests_per_sprint }}
**Decision Criteria**: {{ testing.success_criteria }}
```

### 5. Content Marketing Framework

```jinja2
{# Content Marketing Strategy Template #}

# {{ brand_name }} - Content Marketing Strategy

## 🎯 Content Mission
{{ content_mission }}

## 👥 Audience Personas
{% for persona in personas %}
### {{ persona.name }} - {{ persona.title }}
- **Demographics**: {{ persona.demographics }}
- **Goals**: {{ persona.goals|join(', ') }}
- **Challenges**: {{ persona.challenges|join(', ') }}
- **Content Preferences**: {{ persona.content_preferences|join(', ') }}
- **Channels**: {{ persona.preferred_channels|join(', ') }}
{% endfor %}

## 📚 Content Pillars
{% for pillar in content_pillars %}
### {{ loop.index }}. {{ pillar.name }} ({{ pillar.percentage }}%)
**Purpose**: {{ pillar.purpose }}
**Topics**:
{% for topic in pillar.topics %}
- {{ topic }}
{% endfor %}
**Formats**: {{ pillar.formats|join(', ') }}
{% endfor %}

## 📅 Editorial Calendar
### Content Cadence
{% for channel in channels %}
- **{{ channel.name }}**: {{ channel.frequency }}
  - Best Times: {{ channel.best_times }}
  - Content Types: {{ channel.content_types|join(', ') }}
{% endfor %}

## 🔄 Content Workflow
{% for stage in workflow_stages %}
{{ loop.index }}. **{{ stage.name }}** ({{ stage.duration }})
   - Owner: {{ stage.owner }}
   - Deliverables: {{ stage.deliverables|join(', ') }}
{% endfor %}

## 📊 Success Metrics
### Awareness Stage
{% for metric in awareness_metrics %}
- {{ metric.name }}: Target {{ metric.target }}
{% endfor %}

### Consideration Stage
{% for metric in consideration_metrics %}
- {{ metric.name }}: Target {{ metric.target }}
{% endfor %}

### Decision Stage
{% for metric in decision_metrics %}
- {{ metric.name }}: Target {{ metric.target }}
{% endfor %}

## 🔄 Content Repurposing Matrix
{% for content in repurposing_plan %}
**Original**: {{ content.original_format }}
→ Repurpose to:
{% for format in content.repurpose_formats %}
  - {{ format.type }} for {{ format.channel }}
{% endfor %}
{% endfor %}
```

### 6. ABM Framework (Account-Based Marketing)

```jinja2
{# Account-Based Marketing Template #}

# {{ company_name }} - ABM Strategy

## 🎯 Target Account List
### Tier 1 Accounts (1-to-1)
{% for account in tier1_accounts %}
#### {{ account.name }}
- **Industry**: {{ account.industry }}
- **Revenue**: {{ account.revenue }}
- **Decision Makers**: {{ account.decision_makers|join(', ') }}
- **Pain Points**: {{ account.pain_points|join(', ') }}
- **Opportunity Size**: {{ account.opportunity_size }}
- **Personalization Strategy**: {{ account.personalization }}
{% endfor %}

### Tier 2 Accounts (1-to-Few)
{% for segment in tier2_segments %}
**{{ segment.name }}** ({{ segment.account_count }} accounts)
- Common Characteristics: {{ segment.characteristics }}
- Messaging Theme: {{ segment.messaging }}
{% endfor %}

### Tier 3 Accounts (1-to-Many)
**Total Accounts**: {{ tier3.total_accounts }}
**Targeting Criteria**: {{ tier3.criteria|join(', ') }}

## 📊 Account Intelligence
{% for intel_type in account_intelligence %}
### {{ intel_type.category }}
**Data Sources**:
{% for source in intel_type.sources %}
- {{ source.name }}: {{ source.data_points }}
{% endfor %}
**Insights Gathered**: {{ intel_type.insights }}
{% endfor %}

## 🎨 Personalized Campaigns
{% for campaign in campaigns %}
### {{ campaign.name }}
**Target Tier**: {{ campaign.tier }}
**Channels**:
{% for channel in campaign.channels %}
- {{ channel.name }}: {{ channel.content_type }}
{% endfor %}
**Personalization Elements**:
{% for element in campaign.personalization %}
- {{ element }}
{% endfor %}
**Success Metrics**: {{ campaign.metrics|join(', ') }}
{% endfor %}

## 🤝 Sales & Marketing Alignment
**Account Handoff Criteria**: {{ alignment.handoff_criteria }}
**Shared Metrics**:
{% for metric in alignment.shared_metrics %}
- {{ metric.name }}: {{ metric.definition }}
{% endfor %}
**Meeting Cadence**: {{ alignment.meeting_cadence }}

## 📈 Measurement Framework
{% for measure in measurements %}
### {{ measure.stage }}
- **Metrics**: {{ measure.metrics|join(', ') }}
- **Target**: {{ measure.target }}
- **Review Frequency**: {{ measure.frequency }}
{% endfor %}
```

### 7. Influencer Marketing Framework

```jinja2
{# Influencer Marketing Campaign Template #}

# {{ campaign_name }} - Influencer Strategy

## 🎯 Campaign Objectives
**Primary Goal**: {{ primary_goal }}
**Secondary Goals**:
{% for goal in secondary_goals %}
- {{ goal }}
{% endfor %}
**Success Metrics**: {{ success_metrics|join(', ') }}

## 👥 Influencer Tiers
{% for tier in influencer_tiers %}
### {{ tier.name }} ({{ tier.follower_range }})
**Count**: {{ tier.target_count }} influencers
**Budget per Influencer**: {{ tier.budget }}
**Content Requirements**:
{% for req in tier.content_requirements %}
- {{ req }}
{% endfor %}
**Engagement Rate Target**: {{ tier.engagement_target }}
{% endfor %}

## 🔍 Selection Criteria
**Must-Have Criteria**:
{% for criterion in must_have_criteria %}
- {{ criterion }}
{% endfor %}

**Nice-to-Have Criteria**:
{% for criterion in nice_to_have_criteria %}
- {{ criterion }}
{% endfor %}

**Red Flags**:
{% for flag in red_flags %}
- {{ flag }}
{% endfor %}

## 📝 Campaign Brief
**Campaign Theme**: {{ campaign_theme }}
**Key Messages**:
{% for message in key_messages %}
{{ loop.index }}. {{ message }}
{% endfor %}

**Content Guidelines**:
- **Dos**: {{ content_dos|join(', ') }}
- **Don'ts**: {{ content_donts|join(', ') }}

**Hashtags**: {{ hashtags|join(' ') }}

## 📅 Content Calendar
{% for phase in campaign_phases %}
### Phase {{ loop.index }}: {{ phase.name }} ({{ phase.dates }})
{% for activity in phase.activities %}
- {{ activity.date }}: {{ activity.description }}
{% endfor %}
{% endfor %}

## 💰 Compensation Structure
{% for comp_type in compensation_types %}
### {{ comp_type.name }}
- **Description**: {{ comp_type.description }}
- **Rate**: {{ comp_type.rate }}
- **Performance Bonus**: {{ comp_type.bonus_criteria }}
{% endfor %}

## 📊 Performance Tracking
**Real-time Metrics**:
{% for metric in realtime_metrics %}
- {{ metric.name }}: {{ metric.tool }}
{% endfor %}

**Campaign ROI Calculation**:
- Revenue Generated: {{ roi.revenue_formula }}
- Total Investment: {{ roi.investment_formula }}
- ROI Formula: {{ roi.calculation }}

## 📋 Legal & Compliance
**FTC Disclosure Requirements**: {{ legal.ftc_requirements }}
**Contract Terms**:
{% for term in legal.contract_terms %}
- {{ term }}
{% endfor %}
**Content Rights**: {{ legal.content_rights }}
```

## Marketing Framework Processor

```jinja2
{# Framework Processing Configuration #}

## Available Marketing Frameworks

{% for framework in frameworks %}
### {{ framework.name }}
- **Purpose**: {{ framework.purpose }}
- **Best For**: {{ framework.best_for }}
- **Timeline**: {{ framework.typical_timeline }}
- **Team Size**: {{ framework.recommended_team_size }}
{% endfor %}

## Framework Selection Guide

{% if objective == "new_market_entry" %}
Recommended: STP Framework + SOSTAC
{% elif objective == "digital_growth" %}
Recommended: Growth Hacking (AARRR) + Content Marketing
{% elif objective == "b2b_enterprise" %}
Recommended: ABM Framework + 7Ps
{% elif objective == "brand_awareness" %}
Recommended: Influencer Marketing + Content Marketing
{% elif objective == "holistic_planning" %}
Recommended: SOSTAC + 7Ps
{% endif %}

## Integration Points

{% for integration in framework_integrations %}
### {{ integration.framework1 }} ↔ {{ integration.framework2 }}
**Synergy**: {{ integration.synergy_description }}
**Shared Elements**: {{ integration.shared_elements|join(', ') }}
**Implementation Order**: {{ integration.recommended_order }}
{% endfor %}
```

## Marketing Campaign Templates

### Email Campaign Template

```jinja2
{# Email Marketing Campaign #}

Subject: {{ subject_line }}
Preview: {{ preview_text }}

Hi {{ first_name|default('there') }},

{{ opening_hook }}

{% for value_point in value_points %}
{{ value_point.icon }} **{{ value_point.headline }}**
{{ value_point.description }}

{% endfor %}

{{ social_proof }}

{{ cta_button_text }} → {{ cta_link }}

{{ closing_message }}

Best,
{{ sender_name }}
{{ sender_title }}

P.S. {{ ps_message }}

---
{% if footer_links %}
{% for link in footer_links %}
{{ link.text }} | {% endfor %}
{% endif %}
```

### Social Media Campaign Template

```jinja2
{# Social Media Post Generator #}

{% for platform in platforms %}
## {{ platform.name }}

{% if platform.name == "Twitter" %}
{{ hook|truncate(100) }}

{{ main_point }}

{% for point in thread_points %}
{{ loop.index }}/{{ thread_points|length }} {{ point }}

{% endfor %}
{{ cta }} 
{{ link }}
{{ hashtags|join(' ')|truncate(30) }}

{% elif platform.name == "LinkedIn" %}
{{ thought_leader_hook }}

{{ industry_insight }}

Here's what we're seeing:
{% for insight in insights %}
• {{ insight }}
{% endfor %}

{{ call_to_discussion }}

{{ relevant_hashtags|join(' ') }}

{% elif platform.name == "Instagram" %}
[IMAGE: {{ image_description }}]

{{ caption_hook }}

{{ story_or_value }}

{{ engagement_question }}

.
.
.
{{ hashtags|join(' ') }}

{% endif %}
{% endfor %}
```

## Summary

This marketing frameworks library provides:
- 7 comprehensive marketing frameworks
- Ready-to-use Jinja2 templates
- Campaign execution templates
- Framework selection guidance
- Integration strategies

Each framework is designed for specific marketing objectives and can be combined for comprehensive marketing strategies.