# UX/UI Design Frameworks Library

This document contains UX/UI design frameworks with TypeDict definitions for structured design generation and Jinja2 templates.

## Base Type Definitions

```python
from typing import TypedDict, List, Optional, Dict, Any, Literal

class UXUIFrameworkInput(TypedDict, total=False):
    """Base input structure for all UX/UI frameworks"""
    project_name: str
    target_users: List[str]
    primary_goal: str
    brand_attributes: List[str]
    platform: Literal["web", "mobile", "desktop", "cross-platform"]
    accessibility_level: Literal["WCAG-A", "WCAG-AA", "WCAG-AAA"]
    design_system: Optional[str]  # Material, Bootstrap, custom, etc.

class UXUIFrameworkOutput(TypedDict):
    """Standard output structure"""
    framework_name: str
    design_specification: str
    components: Dict[str, Any]
    design_tokens: Dict[str, str]
    accessibility_notes: List[str]
    implementation_guide: str
```

## UX/UI Design Frameworks

### 1. Double Diamond Framework (Discover-Define-Develop-Deliver)

```python
class DoubleDiamondInput(UXUIFrameworkInput):
    """Input for Double Diamond design process"""
    discover_insights: List[str]  # User research findings
    problem_definition: str  # Clear problem statement
    solution_concepts: List[str]  # Multiple solution ideas
    final_solution: str  # Chosen solution
    success_metrics: List[str]  # How to measure success

DOUBLE_DIAMOND_TEMPLATE = """
{# Double Diamond UX Process #}

# {{ project_name }} Design Process

## 🔍 Discover Phase
Understanding the problem space for {{ target_users|join(', ') }}:

### Key Insights
{% for insight in discover_insights %}
• {{ insight }}
{% endfor %}

## 🎯 Define Phase
### Problem Statement
{{ problem_definition }}

### Design Challenge
How might we {{ primary_goal }} while maintaining {{ brand_attributes|join(' and ') }}?

## 💡 Develop Phase
### Solution Concepts Explored
{% for concept in solution_concepts %}
{{ loop.index }}. {{ concept }}
{% endfor %}

## 🚀 Deliver Phase
### Final Solution
{{ final_solution }}

### Success Metrics
{% for metric in success_metrics %}
- {{ metric }}
{% endfor %}

### Platform: {{ platform }}
### Accessibility: {{ accessibility_level }}
"""

double_diamond_example = DoubleDiamondInput(
    project_name="HealthTrack App",
    target_users=["chronic patients", "caregivers", "healthcare providers"],
    primary_goal="simplify medication tracking and health monitoring",
    brand_attributes=["trustworthy", "simple", "caring"],
    platform="mobile",
    accessibility_level="WCAG-AA",
    discover_insights=[
        "Users forget medications 3x per week on average",
        "Caregivers need remote monitoring capabilities",
        "Current apps are too complex for elderly users"
    ],
    problem_definition="Patients struggle to maintain medication adherence due to complex schedules and lack of caregiver visibility",
    solution_concepts=[
        "Voice-activated reminder system",
        "Visual medication calendar with photos",
        "Gamified adherence tracking",
        "Simplified one-tap logging"
    ],
    final_solution="A voice-first medication app with visual aids and automatic caregiver notifications",
    success_metrics=[
        "95% medication adherence rate",
        "< 3 taps to log medication",
        "4.5+ app store rating"
    ]
)
```

### 2. Jobs-to-be-Done (JTBD) Framework

```python
class JTBDInput(UXUIFrameworkInput):
    """Input for Jobs-to-be-Done framework"""
    main_job: str  # Primary job user is trying to accomplish
    job_context: Dict[str, str]  # When/where/why
    current_solutions: List[str]  # What they use now
    pain_points: List[str]  # Problems with current solutions
    desired_outcomes: List[str]  # What success looks like
    ui_implications: List[str]  # How this affects UI design

JTBD_TEMPLATE = """
{# Jobs-to-be-Done UI Framework #}

# {{ project_name }} - JTBD Analysis

## The Main Job
**When** {{ job_context.when }}
**Where** {{ job_context.where }}
**Users want to** {{ main_job }}
**So they can** {{ job_context.outcome }}

## Current Solutions & Pain Points
### What Users Do Now:
{% for solution in current_solutions %}
- {{ solution }}
{% endfor %}

### Why Current Solutions Fail:
{% for pain in pain_points %}
❌ {{ pain }}
{% endfor %}

## Desired Outcomes
Users will know they're successful when:
{% for outcome in desired_outcomes %}
✓ {{ outcome }}
{% endfor %}

## UI Design Implications
Based on the job analysis, our {{ platform }} interface must:
{% for implication in ui_implications %}
🎨 {{ implication }}
{% endfor %}

### Design Principles
- **Platform**: {{ platform }}
- **Users**: {{ target_users|join(', ') }}
- **Brand**: {{ brand_attributes|join(', ') }}
"""

jtbd_example = JTBDInput(
    project_name="QuickExpense",
    target_users=["freelancers", "small business owners"],
    primary_goal="track expenses for tax deductions",
    main_job="capture and categorize business expenses quickly",
    job_context={
        "when": "immediately after making a purchase",
        "where": "on-the-go, often in stores or restaurants",
        "outcome": "maximize tax deductions without manual bookkeeping"
    },
    current_solutions=[
        "Save paper receipts in shoebox",
        "Email themselves receipt photos",
        "Manual spreadsheet entry later"
    ],
    pain_points=[
        "Receipts get lost or fade",
        "Bulk data entry is time-consuming",
        "Missing receipts mean lost deductions",
        "No real-time expense visibility"
    ],
    desired_outcomes=[
        "Every business expense is captured",
        "Expenses auto-categorize correctly",
        "Tax-ready reports in seconds",
        "Real-time spending insights"
    ],
    ui_implications=[
        "One-tap receipt capture from lock screen",
        "AI-powered auto-categorization",
        "Voice input for quick notes",
        "Offline-first architecture",
        "Dashboard shows YTD tax savings"
    ],
    platform="mobile",
    brand_attributes=["efficient", "smart", "reliable"]
)
```

### 3. Atomic Design Framework

```python
class AtomicDesignInput(UXUIFrameworkInput):
    """Input for Atomic Design system"""
    atoms: Dict[str, List[str]]  # Basic elements
    molecules: Dict[str, str]  # Simple components
    organisms: Dict[str, str]  # Complex components
    templates: List[str]  # Page templates
    pages: Dict[str, str]  # Actual pages
    design_tokens: Dict[str, Any]  # Colors, fonts, spacing

ATOMIC_DESIGN_TEMPLATE = """
{# Atomic Design System #}

# {{ project_name }} Component Library

## ⚛️ Atoms (Basic Building Blocks)
{% for category, items in atoms.items() %}
### {{ category }}
{% for item in items %}
- {{ item }}
{% endfor %}
{% endfor %}

## 🧬 Molecules (Simple Components)
{% for name, description in molecules.items() %}
### {{ name }}
{{ description }}
{% endfor %}

## 🦠 Organisms (Complex Components)
{% for name, description in organisms.items() %}
### {{ name }}
{{ description }}
{% endfor %}

## 📄 Templates
{% for template in templates %}
- {{ template }}
{% endfor %}

## 📱 Pages
{% for page, description in pages.items() %}
### {{ page }}
{{ description }}
{% endfor %}

## 🎨 Design Tokens
```json
{
  "colors": {{ design_tokens.colors | tojson }},
  "typography": {{ design_tokens.typography | tojson }},
  "spacing": {{ design_tokens.spacing | tojson }},
  "shadows": {{ design_tokens.shadows | tojson }}
}
```

### Implementation for {{ platform }}
Target Users: {{ target_users|join(', ') }}
Accessibility: {{ accessibility_level }}
"""

atomic_example = AtomicDesignInput(
    project_name="EduLearn Platform",
    target_users=["students", "teachers", "parents"],
    platform="web",
    atoms={
        "Buttons": ["Primary CTA", "Secondary", "Text button", "Icon button"],
        "Inputs": ["Text field", "Search bar", "Dropdown", "Checkbox"],
        "Typography": ["H1-H6", "Body text", "Caption", "Label"],
        "Icons": ["Navigation", "Actions", "Status", "Social"]
    },
    molecules={
        "SearchBar": "Icon + Input + Clear button",
        "CourseCard": "Image + Title + Progress + CTA",
        "UserAvatar": "Image + Status indicator + Name",
        "FormField": "Label + Input + Error message"
    },
    organisms={
        "Header": "Logo + Navigation + Search + User menu",
        "CourseGrid": "Filter bar + Grid of CourseCards + Pagination",
        "LessonPlayer": "Video player + Transcript + Notes + Quiz",
        "Dashboard": "Stats cards + Progress chart + Recent activity"
    },
    templates=[
        "Landing page template",
        "Course catalog template",
        "Lesson view template",
        "User dashboard template",
        "Admin panel template"
    ],
    pages={
        "Homepage": "Hero + Featured courses + Testimonials + CTA",
        "Browse": "Filters + Course grid + Load more",
        "Learn": "Video + Interactive exercises + Progress tracking",
        "Profile": "User info + Achievements + Course history"
    },
    design_tokens={
        "colors": {
            "primary": "#2563EB",
            "secondary": "#7C3AED",
            "success": "#10B981",
            "surface": "#FFFFFF",
            "text": "#1F2937"
        },
        "typography": {
            "fontFamily": "Inter, system-ui",
            "scale": [12, 14, 16, 20, 24, 32, 48]
        },
        "spacing": {
            "unit": 8,
            "scale": [0, 8, 16, 24, 32, 48, 64]
        },
        "shadows": {
            "sm": "0 1px 2px rgba(0,0,0,0.05)",
            "md": "0 4px 6px rgba(0,0,0,0.1)",
            "lg": "0 10px 15px rgba(0,0,0,0.15)"
        }
    },
    brand_attributes=["modern", "friendly", "educational"],
    accessibility_level="WCAG-AA"
)
```

### 4. User Journey Mapping Framework

```python
class UserJourneyInput(UXUIFrameworkInput):
    """Input for User Journey Mapping"""
    persona: Dict[str, str]  # User details
    journey_stages: List[str]  # Stages of journey
    touchpoints: Dict[str, List[str]]  # Stage: touchpoints
    emotions: Dict[str, str]  # Stage: emotion
    pain_points: Dict[str, List[str]]  # Stage: issues
    opportunities: Dict[str, List[str]]  # Stage: improvements
    ui_solutions: Dict[str, str]  # Stage: UI solution

USER_JOURNEY_TEMPLATE = """
{# User Journey Mapping #}

# {{ project_name }} - User Journey

## 👤 Persona
**Name**: {{ persona.name }}
**Role**: {{ persona.role }}
**Goal**: {{ persona.goal }}
**Tech Level**: {{ persona.tech_level }}

## 🗺️ Journey Map

{% for stage in journey_stages %}
### {{ loop.index }}. {{ stage }}

**Touchpoints**: {{ touchpoints[stage]|join(' → ') }}
**Emotion**: {{ emotions[stage] }}

**Pain Points**:
{% for pain in pain_points[stage] %}
- 😣 {{ pain }}
{% endfor %}

**Opportunities**:
{% for opp in opportunities[stage] %}
- 💡 {{ opp }}
{% endfor %}

**UI Solution**: {{ ui_solutions[stage] }}

---
{% endfor %}

## 🎨 Design Requirements
- **Platform**: {{ platform }}
- **Accessibility**: {{ accessibility_level }}
- **Brand**: {{ brand_attributes|join(', ') }}
"""

journey_example = UserJourneyInput(
    project_name="HomeFinder App",
    target_users=["first-time homebuyers", "real estate agents"],
    platform="cross-platform",
    persona={
        "name": "Sarah Chen",
        "role": "First-time homebuyer",
        "goal": "Find affordable starter home in good school district",
        "tech_level": "Intermediate"
    },
    journey_stages=["Awareness", "Research", "Viewing", "Decision", "Purchase"],
    touchpoints={
        "Awareness": ["Social media ad", "Friend recommendation", "App download"],
        "Research": ["Browse listings", "Save favorites", "Compare homes"],
        "Viewing": ["Schedule tour", "Virtual walkthrough", "Neighborhood info"],
        "Decision": ["Review saved homes", "Calculate mortgage", "Share with partner"],
        "Purchase": ["Make offer", "Track progress", "Complete paperwork"]
    },
    emotions={
        "Awareness": "😊 Excited but overwhelmed",
        "Research": "🤔 Curious but confused",
        "Viewing": "😃 Hopeful yet anxious",
        "Decision": "😰 Stressed about choosing",
        "Purchase": "😅 Relieved but nervous"
    },
    pain_points={
        "Awareness": ["Too many app options", "Unclear value propositions"],
        "Research": ["Information overload", "Inconsistent listing data", "No price history"],
        "Viewing": ["Scheduling conflicts", "Limited tour slots", "Travel time"],
        "Decision": ["Comparison paralysis", "Missing cost calculations", "No decision framework"],
        "Purchase": ["Complex paperwork", "Unclear process", "Communication gaps"]
    },
    opportunities={
        "Awareness": ["Clear onboarding", "Personalized setup", "Value demonstration"],
        "Research": ["Smart filters", "Saved searches", "AI recommendations"],
        "Viewing": ["Instant booking", "AR previews", "Neighborhood tours"],
        "Decision": ["Comparison tools", "Decision matrix", "Cost calculator"],
        "Purchase": ["Digital documents", "Progress tracker", "In-app messaging"]
    },
    ui_solutions={
        "Awareness": "Guided onboarding with preference quiz and instant value demo",
        "Research": "Card-based browsing with swipe actions and smart filters",
        "Viewing": "Calendar integration with one-tap booking and AR mode",
        "Decision": "Split-screen comparison with weighted scoring matrix",
        "Purchase": "Step-by-step wizard with document upload and status tracking"
    },
    brand_attributes=["trustworthy", "simple", "empowering"],
    accessibility_level="WCAG-AA"
)
```

### 5. Design Thinking Framework

```python
class DesignThinkingInput(UXUIFrameworkInput):
    """Input for Design Thinking process"""
    empathize_findings: List[str]  # User research insights
    define_statement: str  # Problem statement
    ideate_concepts: List[Dict[str, str]]  # Ideas with descriptions
    prototype_features: List[str]  # What to build
    test_metrics: Dict[str, str]  # What to measure

DESIGN_THINKING_TEMPLATE = """
{# Design Thinking Process #}

# {{ project_name }} - Design Thinking

## 💗 Empathize
Understanding {{ target_users|join(' and ') }}:

### Key Findings
{% for finding in empathize_findings %}
🔍 {{ finding }}
{% endfor %}

## 📍 Define
### Problem Statement
{{ define_statement }}

### Design Goal
{{ primary_goal }}

## 💡 Ideate
### Concept Exploration
{% for concept in ideate_concepts %}
#### {{ concept.name }}
{{ concept.description }}
- **Pros**: {{ concept.pros }}
- **Cons**: {{ concept.cons }}
{% endfor %}

## 🛠️ Prototype
### Features to Build
{% for feature in prototype_features %}
- [ ] {{ feature }}
{% endfor %}

### Technical Specs
- Platform: {{ platform }}
- Design System: {{ design_system|default('Custom') }}
- Accessibility: {{ accessibility_level }}

## 🧪 Test
### Success Metrics
{% for metric, target in test_metrics.items() %}
- **{{ metric }}**: {{ target }}
{% endfor %}

### Brand Alignment
Ensuring {{ brand_attributes|join(', ') }} throughout the experience.
"""

design_thinking_example = DesignThinkingInput(
    project_name="MindfulWork",
    target_users=["remote workers", "digital nomads"],
    primary_goal="reduce digital burnout through mindful breaks",
    platform="desktop",
    design_system="Material Design 3",
    empathize_findings=[
        "Users work 9+ hours without proper breaks",
        "Zoom fatigue is real - 67% report exhaustion",
        "Current reminder apps are too intrusive",
        "Users want gentle, context-aware nudges"
    ],
    define_statement="Remote workers need a non-intrusive way to maintain work-life balance and prevent burnout while staying productive",
    ideate_concepts=[
        {
            "name": "Ambient Awareness",
            "description": "Subtle visual cues in menu bar that change based on work patterns",
            "pros": "Non-intrusive, always visible, beautiful",
            "cons": "Might be too subtle, platform limitations"
        },
        {
            "name": "Smart Scheduling",
            "description": "AI that learns patterns and suggests breaks between meetings",
            "pros": "Personalized, integrates with calendar, proactive",
            "cons": "Privacy concerns, complex implementation"
        },
        {
            "name": "Pomodoro Plus",
            "description": "Enhanced Pomodoro with biometric integration",
            "pros": "Proven technique, health-aware, customizable",
            "cons": "Requires wearables, might feel rigid"
        }
    ],
    prototype_features=[
        "Menu bar app with customizable ambient indicators",
        "Calendar integration for smart break scheduling",
        "Quick meditation/stretch guides (30s-5min)",
        "Focus mode with app blocking",
        "Daily wellness dashboard",
        "Team sync for collective breaks"
    ],
    test_metrics={
        "Break Compliance": "85% of suggested breaks taken",
        "Burnout Score": "30% reduction in self-reported burnout",
        "Productivity": "No decrease in work output",
        "Retention": "80% still using after 30 days",
        "NPS": "50+ Net Promoter Score"
    },
    brand_attributes=["calm", "intelligent", "supportive"],
    accessibility_level="WCAG-AAA"
)
```

### 6. Lean UX Framework

```python
class LeanUXInput(UXUIFrameworkInput):
    """Input for Lean UX process"""
    assumptions: List[str]  # What we believe
    hypotheses: List[Dict[str, str]]  # If/then statements
    mvp_features: List[str]  # Minimum viable product
    success_signals: List[str]  # How we know it works
    pivot_triggers: List[str]  # When to change direction

LEAN_UX_TEMPLATE = """
{# Lean UX Canvas #}

# {{ project_name }} - Lean UX

## 🎯 Business Goal
{{ primary_goal }}

## 👥 Target Users
{{ target_users|join(', ') }}

## 💭 Assumptions
We believe that:
{% for assumption in assumptions %}
- {{ assumption }}
{% endfor %}

## 🧪 Hypotheses
{% for hyp in hypotheses %}
### Hypothesis {{ loop.index }}
**We believe**: {{ hyp.belief }}
**To verify**: {{ hyp.test }}
**We'll know when**: {{ hyp.metric }}
{% endfor %}

## 🚀 MVP Features
Essential features for {{ platform }}:
{% for feature in mvp_features %}
1. {{ feature }}
{% endfor %}

## ✅ Success Signals
We're succeeding when:
{% for signal in success_signals %}
- {{ signal }}
{% endfor %}

## 🔄 Pivot Triggers
Consider pivoting if:
{% for trigger in pivot_triggers %}
⚠️ {{ trigger }}
{% endfor %}

### Design Constraints
- Brand: {{ brand_attributes|join(', ') }}
- Accessibility: {{ accessibility_level }}
"""

lean_ux_example = LeanUXInput(
    project_name="FitBuddy",
    target_users=["fitness beginners", "gym-intimidated adults"],
    primary_goal="make fitness accessible through AI coaching",
    platform="mobile",
    assumptions=[
        "Beginners quit due to lack of guidance, not motivation",
        "AI can provide personalized coaching at scale",
        "Video form-checks can prevent injuries",
        "Social features increase accountability"
    ],
    hypotheses=[
        {
            "belief": "AI form-checking will increase user confidence",
            "test": "we provide real-time exercise feedback",
            "metric": "70% report feeling more confident after 2 weeks"
        },
        {
            "belief": "Micro-workouts (5-10min) improve adherence",
            "test": "we offer bite-sized workout options",
            "metric": "80% completion rate for micro vs 40% for 30min"
        },
        {
            "belief": "Buddy matching increases retention",
            "test": "we pair users with similar fitness levels",
            "metric": "2x retention for matched vs solo users"
        }
    ],
    mvp_features=[
        "AI form-check using phone camera",
        "5-minute starter workouts",
        "Progress photos with privacy",
        "Simple buddy matching",
        "Daily check-in notifications"
    ],
    success_signals=[
        "1000 DAU within first month",
        "4.5+ app store rating",
        "50% week-2 retention",
        "Users complete 3+ workouts/week",
        "Injury rate < 1%"
    ],
    pivot_triggers=[
        "Week-2 retention below 30%",
        "AI accuracy below 80%",
        "CAC exceeds $50",
        "Users prefer human coaches (>60%)",
        "Technical limitations prevent core features"
    ],
    brand_attributes=["encouraging", "smart", "accessible"],
    accessibility_level="WCAG-AA"
)
```

## UX/UI Framework Processor

```python
class UXUIFrameworkProcessor:
    """Processes UX/UI frameworks with design system integration"""
    
    def __init__(self):
        self.templates = {
            "DOUBLE_DIAMOND": DOUBLE_DIAMOND_TEMPLATE,
            "JTBD": JTBD_TEMPLATE,
            "ATOMIC_DESIGN": ATOMIC_DESIGN_TEMPLATE,
            "USER_JOURNEY": USER_JOURNEY_TEMPLATE,
            "DESIGN_THINKING": DESIGN_THINKING_TEMPLATE,
            "LEAN_UX": LEAN_UX_TEMPLATE
        }
        self.design_systems = self._load_design_systems()
        
    def process_framework(
        self,
        framework_name: str,
        input_data: UXUIFrameworkInput,
        output_format: str = "specification"
    ) -> UXUIFrameworkOutput:
        """
        Process UX/UI framework and generate design artifacts
        """
        template = self.jinja_env.get_template(framework_name)
        specification = template.render(**input_data)
        
        # Extract components based on framework
        components = self._extract_components(framework_name, input_data)
        
        # Generate design tokens
        design_tokens = self._generate_design_tokens(input_data)
        
        # Create implementation guide
        implementation = self._create_implementation_guide(
            framework_name, 
            input_data["platform"], 
            components
        )
        
        return UXUIFrameworkOutput(
            framework_name=framework_name,
            design_specification=specification,
            components=components,
            design_tokens=design_tokens,
            accessibility_notes=self._generate_a11y_notes(input_data),
            implementation_guide=implementation
        )
    
    def generate_design_system(
        self,
        framework_outputs: List[UXUIFrameworkOutput],
        brand_guidelines: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate complete design system from framework outputs
        """
        # Merge components from all frameworks
        # Extract common patterns
        # Generate style guide
        # Create component library
        # Return design system package
        pass
```

## Framework Selection Matrix

| Framework | Best For | Output | Time Required |
|-----------|----------|--------|---------------|
| Double Diamond | Complete design process | Full design spec | 2-4 weeks |
| JTBD | Feature prioritization | UI requirements | 1 week |
| Atomic Design | Design system creation | Component library | 2-3 weeks |
| User Journey | Experience mapping | Touchpoint designs | 1-2 weeks |
| Design Thinking | Innovation projects | Prototype designs | 2-3 weeks |
| Lean UX | Rapid validation | MVP designs | 1 week |

## Integration Benefits

1. **Systematic Approach**: Each framework provides structured thinking
2. **Reusable Components**: Atomic Design creates lasting design systems
3. **User-Centered**: All frameworks prioritize user needs
4. **Measurable Outcomes**: Built-in success metrics
5. **Platform Agnostic**: Works for web, mobile, and desktop

This UX/UI frameworks library provides structured approaches for creating user-centered designs with clear documentation and measurable outcomes.