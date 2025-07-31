# PyClarity Tool Naming Conventions Guide

## 1. Tool Definition Criteria

### What Constitutes a "Tool" in PyClarity?

A tool in PyClarity must meet ALL of the following criteria:

1. **Autonomous Capability**: Performs a complete, meaningful task independently
2. **Clear Input/Output Contract**: Well-defined request/response models
3. **Business Value**: Delivers measurable value to users
4. **Composability**: Can be used standalone or composed with other tools
5. **Domain Boundary**: Operates within a clear problem domain

### Tool vs. Component vs. Utility

- **Tool**: Complete solution (e.g., `StrategicDecisionAccelerator`)
- **Component**: Part of a tool (e.g., `DecisionCrystallizer`)
- **Utility**: Shared functionality (e.g., `calculate_weighted_score`)

## 2. Naming Convention Hierarchy

### Level 1: Tool Names (Top-Level Abstractions)
**Pattern**: `[Domain][Action/Purpose][Type]`

**Examples**:
- `StrategicDecisionAccelerator` ✅
- `JourneyOrchestrationIntelligence` ✅
- `ProjectHealthDiagnostic` ✅

**Criteria**:
- 3-4 words maximum
- Business-oriented (not technical)
- Action-oriented when possible
- Avoid generic terms like "Manager" or "Handler"

### Level 2: Component Names (Sub-Tool Abstractions)
**Pattern**: `[Specific Function][Actor/Engine]`

**Examples**:
- `DecisionCrystallizer` ✅
- `ScenarioModeler` ✅
- `StakeholderAligner` ✅
- `MomentumAnalyzer` ✅

**Criteria**:
- 2-3 words maximum
- Specific action verb + noun
- Describes what it does, not how
- Consistent suffix patterns (-er, -or, -izer, -ator)

### Level 3: Model Names (Data Abstractions)
**Pattern**: `[Entity][Qualifier?][State?]`

**Examples**:
- `DecisionContext` ✅
- `QuantumDecisionState` ✅
- `StakeholderAlignment` ✅
- `AccelerationMetrics` ✅

**Criteria**:
- Noun-based
- State-descriptive when relevant
- Avoid verb forms
- Clear data boundary

### Level 4: Method Names (Action Abstractions)
**Pattern**: `[action]_[object]_[qualifier?]`

**Examples**:
- `accelerate_strategic_decision()` ✅
- `crystallize_decision()` ✅
- `model_scenarios()` ✅
- `analyze_complexity()` ✅

**Criteria**:
- Snake_case for Python
- Verb-first
- Clear action and target
- Async prefix when applicable

## 3. Domain-Specific Naming Patterns

### Strategic/Business Tools
**Keywords**: Strategic, Business, Decision, Executive, Enterprise
**Tone**: Professional, outcome-focused
**Examples**: 
- `StrategicDecisionAccelerator`
- `BusinessModelOptimizer`
- `ExecutiveInsightGenerator`

### Journey/Process Tools
**Keywords**: Journey, Process, Workflow, Orchestration, Flow
**Tone**: Dynamic, progressive
**Examples**:
- `JourneyOrchestrationIntelligence`
- `WorkflowVelocityOptimizer`
- `ProcessHealthMonitor`

### Team/Human Tools
**Keywords**: Team, Collaboration, Human, Social, Culture
**Tone**: People-centric, collaborative
**Examples**:
- `TeamDynamicsOptimizer`
- `CollaborationIntelligence`
- `CultureEvolutionFramework`

### Learning/Growth Tools
**Keywords**: Learning, Growth, Evolution, Development, Velocity
**Tone**: Progressive, adaptive
**Examples**:
- `LearningVelocityMaximizer`
- `SkillEvolutionTracker`
- `GrowthAccelerationEngine`

## 4. Anti-Patterns to Avoid

### ❌ Avoid These Patterns:
1. **Generic Managers**: `DataManager`, `ProcessManager`
2. **Vague Actions**: `HandleStuff`, `ProcessThings`
3. **Technical Jargon**: `SQLQueryOptimizer`, `APIGatewayManager`
4. **Redundant Words**: `ToolTool`, `HelperHelper`
5. **Unclear Abbreviations**: `SDAccel`, `JOI`
6. **Mixed Metaphors**: `RocketSurgeryAnalyzer`

### ❌ Bad Examples:
- `Manager` → Too generic
- `StuffDoer` → Unclear purpose
- `BestDecisionMaker` → Subjective qualifier
- `SDMAFWK` → Unclear abbreviation
- `tool_v2_final_final` → Version in name

## 5. Abstraction Level Guidelines

### High-Level (User-Facing Tools)
**Characteristics**:
- Business language
- Outcome-focused
- No implementation details
- Clear value proposition

**Example**: `StrategicDecisionAccelerator`
- ✅ Clear business value
- ✅ No technical details
- ✅ Action-oriented

### Mid-Level (Components)
**Characteristics**:
- Function-specific
- Clear boundaries
- Composable
- Domain-aware

**Example**: `ScenarioModeler`
- ✅ Specific function
- ✅ Clear what it models
- ✅ Reusable component

### Low-Level (Utilities)
**Characteristics**:
- Technical accuracy
- Reusable
- Performance-focused
- Implementation-specific

**Example**: `calculate_monte_carlo_simulation()`
- ✅ Technical but clear
- ✅ Specific algorithm
- ✅ Reusable utility

## 6. Naming Decision Framework

### Step 1: Identify the Abstraction Level
- Is this user-facing? → High-level naming
- Is this a component? → Mid-level naming
- Is this a utility? → Low-level naming

### Step 2: Choose the Domain
- Strategic/Business
- Journey/Process
- Team/Human
- Learning/Growth
- Technical/System

### Step 3: Select Action Words
**High-Impact Verbs**:
- Accelerate, Optimize, Transform, Evolve
- Orchestrate, Synthesize, Crystallize
- Align, Harmonize, Synchronize
- Analyze, Diagnose, Evaluate

### Step 4: Validate the Name
- [ ] Clear purpose?
- [ ] Appropriate abstraction?
- [ ] Consistent with patterns?
- [ ] Avoids anti-patterns?
- [ ] Easy to understand?

## 7. Special Cases

### Cognitive Tools
**Pattern**: `[Cognitive Domain][Intelligence/Framework/Engine]`
**Examples**:
- `SequentialThinkingEngine`
- `MentalModelFramework`
- `CollaborativeReasoningSystem`

### ML/AI Components
**Pattern**: `[Purpose][Model/Predictor/Analyzer]`
**Examples**:
- `OutcomePredictor`
- `PatternAnalyzer`
- `InsightGenerator`

### Integration Points
**Pattern**: `[External System][Adapter/Connector/Bridge]`
**Examples**:
- `MCPServerAdapter`
- `APIConnector`
- `DataBridge`

## 8. Evolution Guidelines

### When to Rename
1. Purpose has significantly changed
2. Scope has expanded/contracted
3. User feedback indicates confusion
4. Better domain term emerges

### Deprecation Pattern
```python
# Old name with deprecation warning
@deprecated("Use StrategicDecisionAccelerator instead")
class DecisionMaker:
    pass

# New name
class StrategicDecisionAccelerator:
    pass
```

## 9. Quick Reference

### Tool Naming Checklist
- [ ] Follows `[Domain][Action][Type]` pattern
- [ ] 3-4 words maximum
- [ ] Business-oriented language
- [ ] Clear value proposition
- [ ] Avoids technical jargon
- [ ] No versions in name
- [ ] Consistent with domain patterns

### Component Naming Checklist
- [ ] Follows `[Function][Actor]` pattern
- [ ] 2-3 words maximum
- [ ] Action-oriented
- [ ] Clear boundaries
- [ ] Consistent suffix
- [ ] Composable name

### Method Naming Checklist
- [ ] Follows `[verb]_[object]` pattern
- [ ] Snake_case
- [ ] Starts with verb
- [ ] Clear target
- [ ] Async-aware
- [ ] Descriptive but concise

## 10. Examples Gallery

### Excellent Names ✅
- `StrategicDecisionAccelerator`: Clear purpose, business value
- `JourneyOrchestrationIntelligence`: Domain-specific, intelligent
- `TeamDynamicsOptimizer`: People-focused, improvement-oriented
- `ProjectHealthDiagnostic`: Medical metaphor, clear function

### Good Names ✅
- `ScenarioModeler`: Specific function, reusable
- `StakeholderAligner`: Clear actor and action
- `VelocityTracker`: Simple, purposeful

### Problematic Names ❌
- `DataProcessor`: Too generic
- `ThingManager`: Unclear purpose
- `SmartAnalyzer`: Vague qualifier
- `tool_v2`: Version in name