# Business Strategy Frameworks Library

This document contains business strategy frameworks organized with Jinja2 templates for strategic planning and analysis.

## Strategic Planning Frameworks

### 1. Business Model Canvas

```jinja2
{# Business Model Canvas Template #}

# {{ company_name }} - Business Model Canvas

## 🤝 Key Partners
{% for partner in key_partners %}
- **{{ partner.type }}**: {{ partner.name }}
  - Value: {{ partner.value_provided }}
{% endfor %}

## 🏃 Key Activities
{% for activity in key_activities %}
- {{ activity.name }}: {{ activity.description }}
  - Critical for: {{ activity.critical_for }}
{% endfor %}

## 💎 Value Propositions
{% for segment, props in value_propositions.items() %}
### For {{ segment }}:
{% for prop in props %}
- {{ prop.statement }}
  - Pain solved: {{ prop.pain_solved }}
  - Gain created: {{ prop.gain_created }}
{% endfor %}
{% endfor %}

## 🤝 Customer Relationships
{% for relationship in customer_relationships %}
- **{{ relationship.type }}**: {{ relationship.description }}
  - Stage: {{ relationship.customer_stage }}
{% endfor %}

## 👥 Customer Segments
{% for segment in customer_segments %}
### {{ segment.name }}
- Size: {{ segment.market_size }}
- Characteristics: {{ segment.characteristics }}
- Needs: {{ segment.needs|join(', ') }}
- Revenue potential: {{ segment.revenue_potential }}
{% endfor %}

## 🔑 Key Resources
{% for resource in key_resources %}
- **{{ resource.type }}**: {{ resource.description }}
  - Status: {{ resource.status }}
{% endfor %}

## 📢 Channels
{% for channel in channels %}
### {{ channel.name }}
- Purpose: {{ channel.purpose }}
- Stage: {{ channel.customer_journey_stage }}
- Cost: {{ channel.cost_structure }}
{% endfor %}

## 💰 Cost Structure
### Fixed Costs
{% for cost in cost_structure.fixed %}
- {{ cost.item }}: {{ cost.amount }}/{{ cost.period }}
{% endfor %}

### Variable Costs
{% for cost in cost_structure.variable %}
- {{ cost.item }}: {{ cost.rate }}
{% endfor %}

## 💵 Revenue Streams
{% for stream in revenue_streams %}
### {{ stream.name }}
- Type: {{ stream.type }}
- Pricing: {{ stream.pricing_mechanism }}
- Contribution: {{ stream.percentage }}% of total revenue
- Growth rate: {{ stream.growth_rate }}%
{% endfor %}
```

### 2. Porter's Five Forces Analysis

```jinja2
{# Porter's Five Forces Template #}

# {{ industry_name }} - Five Forces Analysis

## 1️⃣ Threat of New Entrants ({{ new_entrants.rating }}/5)

### Barriers to Entry
{% for barrier in new_entrants.barriers %}
- **{{ barrier.type }}**: {{ barrier.description }}
  - Strength: {{ barrier.strength }}/5
{% endfor %}

### Risk Assessment
- **Overall Threat Level**: {{ new_entrants.threat_level }}
- **Time to Entry**: {{ new_entrants.time_to_entry }}
- **Capital Required**: {{ new_entrants.capital_required }}

### Mitigation Strategies
{% for strategy in new_entrants.mitigation %}
- {{ strategy }}
{% endfor %}

## 2️⃣ Bargaining Power of Suppliers ({{ suppliers.rating }}/5)

### Key Suppliers
{% for supplier in suppliers.key_suppliers %}
- **{{ supplier.name }}**: {{ supplier.product }}
  - Switching cost: {{ supplier.switching_cost }}
  - Alternatives: {{ supplier.alternatives }}
{% endfor %}

### Power Factors
{% for factor in suppliers.power_factors %}
- {{ factor.name }}: {{ factor.impact }}
{% endfor %}

### Strategies to Reduce Supplier Power
{% for strategy in suppliers.strategies %}
- {{ strategy }}
{% endfor %}

## 3️⃣ Bargaining Power of Buyers ({{ buyers.rating }}/5)

### Buyer Segments
{% for segment in buyers.segments %}
- **{{ segment.name }}** ({{ segment.percentage }}% of revenue)
  - Price sensitivity: {{ segment.price_sensitivity }}
  - Switching cost: {{ segment.switching_cost }}
{% endfor %}

### Power Drivers
{% for driver in buyers.power_drivers %}
- {{ driver }}
{% endfor %}

### Customer Retention Strategies
{% for strategy in buyers.retention_strategies %}
- {{ strategy }}
{% endfor %}

## 4️⃣ Threat of Substitutes ({{ substitutes.rating }}/5)

### Direct Substitutes
{% for substitute in substitutes.direct %}
- **{{ substitute.name }}**: {{ substitute.description }}
  - Performance ratio: {{ substitute.performance_ratio }}
  - Price ratio: {{ substitute.price_ratio }}
{% endfor %}

### Indirect Substitutes
{% for substitute in substitutes.indirect %}
- {{ substitute }}
{% endfor %}

### Differentiation Strategies
{% for strategy in substitutes.differentiation %}
- {{ strategy }}
{% endfor %}

## 5️⃣ Industry Rivalry ({{ rivalry.rating }}/5)

### Major Competitors
{% for competitor in rivalry.competitors %}
- **{{ competitor.name }}**: {{ competitor.market_share }}% market share
  - Strengths: {{ competitor.strengths|join(', ') }}
  - Strategy: {{ competitor.strategy }}
{% endfor %}

### Rivalry Intensifiers
{% for factor in rivalry.intensifiers %}
- {{ factor }}
{% endfor %}

### Competitive Advantages
{% for advantage in rivalry.our_advantages %}
- **{{ advantage.type }}**: {{ advantage.description }}
{% endfor %}

## 🎯 Strategic Implications
**Most Critical Force**: {{ most_critical_force }}
**Strategic Priority**: {{ strategic_priority }}
**3-Year Outlook**: {{ three_year_outlook }}
```

### 3. SWOT-TOWS Matrix

```jinja2
{# SWOT-TOWS Strategic Matrix Template #}

# {{ organization_name }} - SWOT-TOWS Analysis

## 📊 SWOT Analysis

### Strengths (Internal +)
{% for strength in strengths %}
S{{ loop.index }}: {{ strength }}
{% endfor %}

### Weaknesses (Internal -)
{% for weakness in weaknesses %}
W{{ loop.index }}: {{ weakness }}
{% endfor %}

### Opportunities (External +)
{% for opportunity in opportunities %}
O{{ loop.index }}: {{ opportunity }}
{% endfor %}

### Threats (External -)
{% for threat in threats %}
T{{ loop.index }}: {{ threat }}
{% endfor %}

## 🎯 TOWS Strategic Matrix

### SO Strategies (Strengths + Opportunities)
**Leverage strengths to capture opportunities**
{% for strategy in so_strategies %}
- {{ strategy.name }}
  - Uses: {{ strategy.strengths_used|join(', ') }}
  - Captures: {{ strategy.opportunities_captured|join(', ') }}
  - Action: {{ strategy.action_plan }}
{% endfor %}

### WO Strategies (Weaknesses + Opportunities)
**Overcome weaknesses by pursuing opportunities**
{% for strategy in wo_strategies %}
- {{ strategy.name }}
  - Addresses: {{ strategy.weaknesses_addressed|join(', ') }}
  - Through: {{ strategy.opportunities_used|join(', ') }}
  - Action: {{ strategy.action_plan }}
{% endfor %}

### ST Strategies (Strengths + Threats)
**Use strengths to avoid threats**
{% for strategy in st_strategies %}
- {{ strategy.name }}
  - Leverages: {{ strategy.strengths_leveraged|join(', ') }}
  - Mitigates: {{ strategy.threats_mitigated|join(', ') }}
  - Action: {{ strategy.action_plan }}
{% endfor %}

### WT Strategies (Weaknesses + Threats)
**Minimize weaknesses and avoid threats**
{% for strategy in wt_strategies %}
- {{ strategy.name }}
  - Reduces: {{ strategy.weaknesses_reduced|join(', ') }}
  - Avoids: {{ strategy.threats_avoided|join(', ') }}
  - Action: {{ strategy.action_plan }}
{% endfor %}

## 🚀 Strategic Priorities
{% for priority in strategic_priorities %}
{{ loop.index }}. **{{ priority.strategy }}**
   - Type: {{ priority.type }}
   - Impact: {{ priority.impact_score }}/10
   - Effort: {{ priority.effort_score }}/10
   - Timeline: {{ priority.timeline }}
{% endfor %}
```

### 4. Blue Ocean Strategy Canvas

```jinja2
{# Blue Ocean Strategy Template #}

# {{ company_name }} - Blue Ocean Strategy

## 🌊 Strategy Canvas

### Industry Factors
{% for factor in industry_factors %}
#### {{ factor.name }}
- Industry Average: {{ factor.industry_avg }}/10
- Our Current: {{ factor.our_current }}/10
- Our Future: {{ factor.our_future }}/10
- Action: {{ factor.action }} {# Eliminate/Reduce/Raise/Create #}
{% endfor %}

## 🔴 Eliminate
**Which factors should be eliminated that the industry takes for granted?**
{% for item in eliminate %}
- **{{ item.factor }}**: {{ item.reason }}
  - Cost savings: {{ item.cost_savings }}
  - Customer impact: {{ item.customer_impact }}
{% endfor %}

## 🟡 Reduce
**Which factors should be reduced well below industry standard?**
{% for item in reduce %}
- **{{ item.factor }}**: {{ item.target_level }}
  - Current: {{ item.current_level }}
  - Reason: {{ item.reason }}
{% endfor %}

## 🟢 Raise
**Which factors should be raised well above industry standard?**
{% for item in raise %}
- **{{ item.factor }}**: {{ item.target_level }}
  - Current: {{ item.current_level }}
  - Investment: {{ item.investment_required }}
{% endfor %}

## 🔵 Create
**Which factors should be created that the industry has never offered?**
{% for item in create %}
- **{{ item.factor }}**: {{ item.description }}
  - Value proposition: {{ item.value_prop }}
  - Implementation: {{ item.implementation }}
  - Differentiation: {{ item.differentiation }}
{% endfor %}

## 🎯 New Value Curve
### Target Customer Profile
- **Who**: {{ target_customer.description }}
- **Current solution**: {{ target_customer.current_solution }}
- **Pain points**: {{ target_customer.pain_points|join(', ') }}
- **Desired gains**: {{ target_customer.desired_gains|join(', ') }}

### Value Innovation
**Simultaneous pursuit of differentiation AND low cost**
- Cost reduction through: {{ value_innovation.cost_reduction }}
- Value increase through: {{ value_innovation.value_increase }}
- Expected margin improvement: {{ value_innovation.margin_improvement }}%

## 📊 Implementation Roadmap
{% for phase in implementation_phases %}
### Phase {{ loop.index }}: {{ phase.name }} ({{ phase.timeline }})
{% for milestone in phase.milestones %}
- {{ milestone }}
{% endfor %}
{% endfor %}
```

### 5. McKinsey 7S Framework

```jinja2
{# McKinsey 7S Framework Template #}

# {{ organization_name }} - 7S Analysis

## 🏗️ Hard Elements

### 1. Strategy
**Current Strategy**: {{ strategy.current }}
**Desired Strategy**: {{ strategy.desired }}
**Gap Analysis**:
{% for gap in strategy.gaps %}
- {{ gap }}
{% endfor %}
**Action Items**:
{% for action in strategy.actions %}
- {{ action.item }} (Owner: {{ action.owner }}, Due: {{ action.due_date }})
{% endfor %}

### 2. Structure
**Organization Type**: {{ structure.type }}
**Reporting Lines**: {{ structure.reporting }}
**Decision Making**: {{ structure.decision_making }}
**Issues**:
{% for issue in structure.issues %}
- {{ issue }}
{% endfor %}
**Proposed Changes**:
{% for change in structure.changes %}
- {{ change }}
{% endfor %}

### 3. Systems
{% for system in systems %}
#### {{ system.name }}
- **Current State**: {{ system.current_state }}
- **Effectiveness**: {{ system.effectiveness }}/10
- **Improvements Needed**: {{ system.improvements|join(', ') }}
{% endfor %}

## 💫 Soft Elements

### 4. Shared Values
**Core Values**:
{% for value in shared_values.core %}
- **{{ value.name }}**: {{ value.description }}
  - Living it?: {{ value.alignment_score }}/10
{% endfor %}
**Cultural Gaps**:
{% for gap in shared_values.gaps %}
- {{ gap }}
{% endfor %}

### 5. Skills
**Core Competencies**:
{% for skill in skills.core %}
- {{ skill.name }}: {{ skill.level }} (Need: {{ skill.needed_level }})
{% endfor %}
**Skill Gaps**:
{% for gap in skills.gaps %}
- **{{ gap.skill }}**: {{ gap.current }} → {{ gap.required }}
  - Training plan: {{ gap.training_plan }}
{% endfor %}

### 6. Style
**Leadership Style**: {{ style.current_leadership }}
**Management Approach**: {{ style.management_approach }}
**Communication Style**: {{ style.communication }}
**Style Evolution Needed**:
{% for evolution in style.evolution %}
- From {{ evolution.from }} to {{ evolution.to }}
{% endfor %}

### 7. Staff
**Headcount**: {{ staff.current_count }} (Optimal: {{ staff.optimal_count }})
**Key Roles**:
{% for role in staff.key_roles %}
- **{{ role.title }}**: {{ role.status }}
  {% if role.action_needed %}Action: {{ role.action_needed }}{% endif %}
{% endfor %}
**Talent Gaps**:
{% for gap in staff.talent_gaps %}
- {{ gap.role }}: {{ gap.requirement }}
{% endfor %}

## 🔄 Alignment Analysis
{% for alignment in alignments %}
### {{ alignment.element1 }} ↔ {{ alignment.element2 }}
- **Current Alignment**: {{ alignment.score }}/10
- **Issues**: {{ alignment.issues|join(', ') }}
- **Actions**: {{ alignment.actions|join('; ') }}
{% endfor %}

## 🎯 Change Priorities
{% for priority in change_priorities %}
{{ loop.index }}. **{{ priority.element }}**: {{ priority.change }}
   - Impact: {{ priority.impact }}
   - Effort: {{ priority.effort }}
   - Timeline: {{ priority.timeline }}
{% endfor %}
```

### 6. Balanced Scorecard

```jinja2
{# Balanced Scorecard Template #}

# {{ company_name }} - Balanced Scorecard

## 🎯 Vision & Strategy
**Vision**: {{ vision }}
**Mission**: {{ mission }}
**Strategic Themes**:
{% for theme in strategic_themes %}
- {{ theme }}
{% endfor %}

## 📊 Four Perspectives

### 💰 Financial Perspective
**Question**: How do we look to shareholders?

{% for objective in financial_objectives %}
#### Objective: {{ objective.name }}
- **Measure**: {{ objective.measure }}
- **Target**: {{ objective.target }}
- **Current**: {{ objective.current }}
- **Initiative**: {{ objective.initiative }}
- **Owner**: {{ objective.owner }}
{% endfor %}

### 👥 Customer Perspective
**Question**: How do customers see us?

{% for objective in customer_objectives %}
#### Objective: {{ objective.name }}
- **Measure**: {{ objective.measure }}
- **Target**: {{ objective.target }}
- **Current**: {{ objective.current }}
- **Initiative**: {{ objective.initiative }}
- **Owner**: {{ objective.owner }}
{% endfor %}

### 🔄 Internal Process Perspective
**Question**: What must we excel at?

{% for objective in process_objectives %}
#### Objective: {{ objective.name }}
- **Measure**: {{ objective.measure }}
- **Target**: {{ objective.target }}
- **Current**: {{ objective.current }}
- **Initiative**: {{ objective.initiative }}
- **Owner**: {{ objective.owner }}
{% endfor %}

### 📚 Learning & Growth Perspective
**Question**: How can we continue to improve?

{% for objective in learning_objectives %}
#### Objective: {{ objective.name }}
- **Measure**: {{ objective.measure }}
- **Target**: {{ objective.target }}
- **Current**: {{ objective.current }}
- **Initiative**: {{ objective.initiative }}
- **Owner**: {{ objective.owner }}
{% endfor %}

## 🔗 Strategy Map
### Cause-and-Effect Relationships

{% for relationship in strategy_map %}
{{ relationship.from_objective }} → {{ relationship.to_objective }}
*{{ relationship.rationale }}*
{% endfor %}

## 📈 Scorecard Summary

| Perspective | # Objectives | On Track | At Risk | Off Track |
|-------------|--------------|----------|---------|-----------|
{% for summary in perspective_summary %}
| {{ summary.perspective }} | {{ summary.total }} | {{ summary.green }} | {{ summary.yellow }} | {{ summary.red }} |
{% endfor %}

## 🚨 Key Risk Areas
{% for risk in key_risks %}
- **{{ risk.area }}**: {{ risk.description }}
  - Mitigation: {{ risk.mitigation }}
{% endfor %}

## 📅 Review Cadence
- **Weekly**: {{ review.weekly|join(', ') }}
- **Monthly**: {{ review.monthly|join(', ') }}
- **Quarterly**: {{ review.quarterly|join(', ') }}
```

### 7. OKR Framework (Objectives and Key Results)

```jinja2
{# OKR Framework Template #}

# {{ period }} OKRs - {{ company_name }}

## 🏢 Company OKRs

{% for objective in company_okrs %}
### Objective {{ loop.index }}: {{ objective.statement }}
*{{ objective.rationale }}*

**Key Results**:
{% for kr in objective.key_results %}
{{ loop.index }}. {{ kr.description }}
   - Baseline: {{ kr.baseline }}
   - Target: {{ kr.target }}
   - Current: {{ kr.current }}
   - Progress: {{ kr.progress }}%
   - Owner: {{ kr.owner }}
{% endfor %}
{% endfor %}

## 🏬 Department OKRs

{% for dept in department_okrs %}
### {{ dept.name }} Department

{% for objective in dept.objectives %}
#### Objective: {{ objective.statement }}
*Supports Company Objective: {{ objective.supports }}*

**Key Results**:
{% for kr in objective.key_results %}
- {{ kr.description }}
  - Target: {{ kr.target }} ({{ kr.progress }}%)
  - Status: {{ kr.status }}
{% endfor %}
{% endfor %}
{% endfor %}

## 👤 Individual OKRs

{% for person in individual_okrs %}
### {{ person.name }} ({{ person.role }})

{% for objective in person.objectives %}
**O**: {{ objective.statement }}
{% for kr in objective.key_results %}
**KR{{ loop.index }}**: {{ kr.description }} ({{ kr.progress }}%)
{% endfor %}
{% endfor %}
{% endfor %}

## 📊 OKR Health Check

### Alignment Score
- Vertical Alignment: {{ alignment.vertical }}%
- Horizontal Alignment: {{ alignment.horizontal }}%
- Cross-functional: {{ alignment.cross_functional }}%

### Quality Metrics
{% for metric in quality_metrics %}
- {{ metric.name }}: {{ metric.score }}/5
  - {{ metric.feedback }}
{% endfor %}

## 🚀 Initiatives & Projects

{% for initiative in initiatives %}
### {{ initiative.name }}
- **Supports OKRs**: {{ initiative.supports_okrs|join(', ') }}
- **Team**: {{ initiative.team|join(', ') }}
- **Timeline**: {{ initiative.timeline }}
- **Status**: {{ initiative.status }}
- **Next Milestone**: {{ initiative.next_milestone }}
{% endfor %}

## 📈 Progress Tracking

### Weekly Check-ins
{% for checkin in weekly_checkins %}
**Week {{ checkin.week }}**:
- Confidence: {{ checkin.confidence }}/10
- Blockers: {{ checkin.blockers|default('None') }}
- Help Needed: {{ checkin.help_needed|default('None') }}
{% endfor %}

### Mid-Period Review
**Overall Progress**: {{ mid_period.overall_progress }}%
**At Risk OKRs**:
{% for risk in mid_period.at_risk %}
- {{ risk.okr }}: {{ risk.issue }}
  - Recovery Plan: {{ risk.recovery_plan }}
{% endfor %}

## 🎯 Lessons & Adjustments
{% for lesson in lessons_learned %}
- **{{ lesson.category }}**: {{ lesson.insight }}
  - Action: {{ lesson.action_item }}
{% endfor %}
```

## Business Analysis Templates

### Financial Analysis Template

```jinja2
{# Financial Analysis Dashboard #}

# {{ company_name }} - Financial Analysis

## 📊 Key Financial Metrics

### Revenue Analysis
- **Total Revenue**: {{ revenue.total|currency }}
- **YoY Growth**: {{ revenue.yoy_growth }}%
- **MRR/ARR**: {{ revenue.recurring|currency }}
- **Revenue per Customer**: {{ revenue.per_customer|currency }}

### Profitability
- **Gross Margin**: {{ profitability.gross_margin }}%
- **Operating Margin**: {{ profitability.operating_margin }}%
- **EBITDA**: {{ profitability.ebitda|currency }}
- **Net Margin**: {{ profitability.net_margin }}%

### Cash Flow
- **Operating Cash Flow**: {{ cash_flow.operating|currency }}
- **Free Cash Flow**: {{ cash_flow.free|currency }}
- **Cash Runway**: {{ cash_flow.runway_months }} months
- **Burn Rate**: {{ cash_flow.burn_rate|currency }}/month

### Unit Economics
- **CAC**: {{ unit_economics.cac|currency }}
- **LTV**: {{ unit_economics.ltv|currency }}
- **LTV:CAC Ratio**: {{ unit_economics.ltv_cac_ratio }}
- **Payback Period**: {{ unit_economics.payback_months }} months

## 📈 Trend Analysis

{% for metric in trend_metrics %}
### {{ metric.name }} Trend
{% for period in metric.periods %}
- {{ period.label }}: {{ period.value }} ({{ period.change }}%)
{% endfor %}
{% endfor %}

## 🎯 Financial Projections

{% for scenario in scenarios %}
### {{ scenario.name }} Scenario
**Assumptions**:
{% for assumption in scenario.assumptions %}
- {{ assumption.factor }}: {{ assumption.value }}
{% endfor %}

**Projected Outcomes**:
- Revenue (Year 1): {{ scenario.year1_revenue|currency }}
- Revenue (Year 3): {{ scenario.year3_revenue|currency }}
- Break-even: {{ scenario.breakeven_month }}
- ROI: {{ scenario.roi }}%
{% endfor %}
```

### Risk Assessment Template

```jinja2
{# Risk Assessment Matrix #}

# {{ project_name }} - Risk Assessment

## 🎯 Risk Matrix

{% for risk in risks %}
### {{ loop.index }}. {{ risk.name }}
- **Category**: {{ risk.category }}
- **Probability**: {{ risk.probability }}/5
- **Impact**: {{ risk.impact }}/5
- **Risk Score**: {{ risk.score }}
- **Status**: {{ risk.status }}

**Description**: {{ risk.description }}

**Mitigation Strategy**: {{ risk.mitigation }}

**Contingency Plan**: {{ risk.contingency }}

**Owner**: {{ risk.owner }}
**Review Date**: {{ risk.review_date }}

---
{% endfor %}

## 📊 Risk Summary

### By Category
{% for category in risk_categories %}
- **{{ category.name }}**: {{ category.count }} risks ({{ category.percentage }}%)
{% endfor %}

### By Severity
- 🔴 Critical: {{ severity.critical }}
- 🟡 High: {{ severity.high }}
- 🟢 Medium: {{ severity.medium }}
- ⚪ Low: {{ severity.low }}

## 🚨 Top Risk Triggers
{% for trigger in risk_triggers %}
- {{ trigger.event }}: Affects {{ trigger.affected_risks|join(', ') }}
{% endfor %}
```

## Summary

This business frameworks library provides:
- 7 comprehensive strategic frameworks
- Financial analysis templates
- Risk assessment tools
- Ready-to-use Jinja2 templates
- Implementation guidance

Each framework serves specific business planning needs and can be combined for comprehensive strategic analysis.