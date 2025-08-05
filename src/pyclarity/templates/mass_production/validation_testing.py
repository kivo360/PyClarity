"""Validation and testing templates for product development."""

from ..base import PromptTemplate, TemplateCategory

AB_TEST_HYPOTHESIS = PromptTemplate(
    name="ab_test_hypothesis",
    description="Generate A/B test hypotheses with complete test plans",
    template="""Generate {number} A/B test hypotheses for {website_app}:
- Current metric: {baseline_metric}
- Goal: {improvement_target}
- Test area: {test_area}

For each hypothesis include:
- Hypothesis statement (If we... then we expect...)
- Variable to test (specific element)
- Control vs variant description
- Primary success metric
- Secondary metrics
- Expected impact (percentage)
- Test duration estimate
- Sample size requirement
- Risk assessment""",
    variables=["number", "website_app", "baseline_metric", "improvement_target", "test_area"],
    category=TemplateCategory.VALIDATION_TESTING,
    examples=[{
        "number": "10",
        "website_app": "e-commerce checkout flow",
        "baseline_metric": "68% checkout completion rate",
        "improvement_target": "increase completion by 10%",
        "test_area": "payment and shipping pages"
    }]
)

USER_INTERVIEW_SCRIPT = PromptTemplate(
    name="user_interview_script",
    description="Create structured user interview scripts",
    template="""Create interview script for {product} validation:
- Interview goal: {learning_objective}
- User type: {target_persona}
- Interview duration: {duration} minutes
- Interview format: {format}

Script sections:
1. Introduction and rapport building (2-3 questions)
2. Background and context ({background_questions} questions)
3. Problem exploration ({problem_questions} questions)
4. Solution validation ({solution_questions} questions)
5. Feature prioritization ({feature_questions} questions)
6. Pricing sensitivity (2-3 questions)
7. Closing and next steps

Include follow-up prompts for each question.""",
    variables=["product", "learning_objective", "target_persona", "duration", "format",
               "background_questions", "problem_questions", "solution_questions", "feature_questions"],
    category=TemplateCategory.VALIDATION_TESTING,
    examples=[{
        "product": "AI meeting assistant",
        "learning_objective": "validate need for automated action items",
        "target_persona": "project managers in tech companies",
        "duration": "30",
        "format": "video call",
        "background_questions": "3",
        "problem_questions": "5",
        "solution_questions": "5",
        "feature_questions": "3"
    }]
)

USABILITY_TEST_PLAN = PromptTemplate(
    name="usability_test_plan",
    description="Design comprehensive usability testing scenarios",
    template="""Create usability test plan for {product_feature}:
- Test objective: {objective}
- User profile: {user_profile}
- Number of participants: {participant_count}
- Test environment: {environment}

Include:
1. Pre-test questionnaire (5 questions)
2. Test scenarios ({scenario_count} tasks)
   - Task description
   - Success criteria
   - Time limit
   - Critical path
3. Think-aloud prompts
4. Post-task questions
5. System Usability Scale (SUS) questions
6. Post-test interview questions
7. Metrics to capture
8. Analysis framework""",
    variables=["product_feature", "objective", "user_profile", "participant_count", "environment", "scenario_count"],
    category=TemplateCategory.VALIDATION_TESTING,
    examples=[{
        "product_feature": "mobile app onboarding flow",
        "objective": "identify friction points in first-time user experience",
        "user_profile": "non-technical users aged 35-50",
        "participant_count": "8",
        "environment": "remote moderated testing",
        "scenario_count": "5"
    }]
)

SURVEY_QUESTION_BANK = PromptTemplate(
    name="survey_question_bank",
    description="Generate targeted survey questions for validation",
    template="""Create survey for {validation_goal}:
- Target respondents: {target_audience}
- Survey length: {question_count} questions
- Survey type: {survey_type}
- Incentive: {incentive}

Generate questions for:
1. Screening/qualification (2-3 questions)
2. Current behavior/situation ({behavior_questions} questions)
3. Pain points and challenges ({pain_questions} questions)
4. Solution preferences ({preference_questions} questions)
5. Willingness to pay (2-3 questions)
6. Feature importance ranking
7. Demographics (3-4 questions)

Include question types: multiple choice, scale (1-10), ranking, open-ended.""",
    variables=["validation_goal", "target_audience", "question_count", "survey_type", "incentive",
               "behavior_questions", "pain_questions", "preference_questions"],
    category=TemplateCategory.VALIDATION_TESTING,
    examples=[{
        "validation_goal": "validate demand for AI resume builder",
        "target_audience": "job seekers who changed jobs in last 12 months",
        "question_count": "20",
        "survey_type": "online questionnaire",
        "incentive": "$10 gift card",
        "behavior_questions": "4",
        "pain_questions": "5",
        "preference_questions": "4"
    }]
)

BETA_TEST_FRAMEWORK = PromptTemplate(
    name="beta_test_framework",
    description="Complete beta testing program structure",
    template="""Design beta test program for {product}:
- Beta duration: {duration}
- Target beta users: {user_count}
- User profile: {ideal_tester}
- Success criteria: {success_metric}

Create:
1. Beta tester recruitment criteria
2. Onboarding process and materials
3. Testing tasks/scenarios (weekly)
4. Feedback collection methods
   - Bug reporting template
   - Feature request format
   - Weekly survey questions
5. Communication plan
   - Announcement templates
   - Update frequency
   - Community guidelines
6. Incentive structure
7. Data collection framework
8. Exit survey
9. Beta to customer conversion plan""",
    variables=["product", "duration", "user_count", "ideal_tester", "success_metric"],
    category=TemplateCategory.VALIDATION_TESTING,
    examples=[{
        "product": "B2B analytics dashboard",
        "duration": "8 weeks",
        "user_count": "50",
        "ideal_tester": "data analysts in mid-size companies",
        "success_metric": "80% weekly active usage"
    }]
)

# Collection of all validation testing templates
VALIDATION_TESTING_TEMPLATES = [
    AB_TEST_HYPOTHESIS,
    USER_INTERVIEW_SCRIPT,
    USABILITY_TEST_PLAN,
    SURVEY_QUESTION_BANK,
    BETA_TEST_FRAMEWORK
]
