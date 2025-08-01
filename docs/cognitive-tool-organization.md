# PyClarity Cognitive Tool Organization

## Core Purpose
PyClarity is a collection of **cognitive tools** designed to help think through problems strategically and achieve objectives. Each tool represents a different way of thinking or reasoning about problems.

## Organizational Structure

```
/src/pyclarity/tools/
├── sequential_thinking/         # Step-by-step problem decomposition
├── mental_models/              # Framework switching for different contexts  
├── decision_framework/         # Structured decision evaluation
├── collaborative_reasoning/    # Multi-stakeholder perspective integration
├── scientific_method/          # Hypothesis-driven exploration
├── design_patterns/           # Reusable solution templates
├── impact_propagation/        # Ripple effect analysis
├── iterative_validation/      # Continuous refinement cycles
├── metacognitive_monitoring/  # Thinking about thinking
├── multi_perspective/         # Viewing problems from multiple angles
├── programming_paradigms/     # Different coding thought models
├── sequential_readiness/      # Prerequisite checking
├── triple_constraint/         # Balancing competing constraints
├── visual_reasoning/          # Spatial and diagrammatic thinking
├── strategic_decision/        # Strategic decision acceleration (NEW)
├── journey_orchestration/     # Complex journey navigation (NEW)
├── project_health/           # Holistic project assessment (NEW)
├── team_dynamics/            # Team optimization (NEW)
├── mentorship_evolution/     # Growth facilitation (NEW)
└── learning_velocity/        # Learning acceleration (NEW)
```

## Tool Categories by Cognitive Function

### 1. Analytical Thinking Tools
Tools that break down and analyze problems:
- **sequential_thinking**: Decomposes problems into ordered steps
- **impact_propagation**: Analyzes cause-and-effect chains
- **triple_constraint**: Balances time, cost, and scope

### 2. Synthetic Thinking Tools  
Tools that combine and create:
- **mental_models**: Synthesizes different thinking frameworks
- **collaborative_reasoning**: Integrates multiple perspectives
- **multi_perspective**: Combines diverse viewpoints

### 3. Evaluative Thinking Tools
Tools that assess and validate:
- **decision_framework**: Evaluates options systematically
- **iterative_validation**: Refines through cycles
- **sequential_readiness**: Assesses prerequisites
- **project_health**: Diagnoses project status

### 4. Creative Thinking Tools
Tools that generate new approaches:
- **design_patterns**: Applies proven templates creatively
- **programming_paradigms**: Explores different coding philosophies
- **visual_reasoning**: Uses spatial thinking

### 5. Metacognitive Tools
Tools for thinking about thinking:
- **metacognitive_monitoring**: Self-awareness in problem-solving
- **learning_velocity**: Optimizes learning processes
- **mentorship_evolution**: Develops thinking in others

### 6. Strategic Thinking Tools
Tools for long-term planning:
- **strategic_decision**: Accelerates strategic choices
- **journey_orchestration**: Plans complex initiatives
- **scientific_method**: Structures exploration

### 7. Social Thinking Tools
Tools for group cognition:
- **team_dynamics**: Optimizes collective thinking
- **collaborative_reasoning**: Facilitates group reasoning

## Key Principles

1. **Cognitive First**: Each tool represents a way of thinking
2. **Problem-Solving Focus**: Tools help achieve objectives
3. **Clear Names**: Tool names describe the thinking approach
4. **Composable**: Tools can be combined for complex problems
5. **Strategic**: Aimed at achieving meaningful outcomes

## Tool Naming Patterns

Keep original cognitive names from FastMCP:
- `sequential_thinking` ✅ (clear cognitive process)
- `mental_models` ✅ (established cognitive concept)
- `decision_framework` ✅ (clear purpose)

New tools follow same pattern:
- `strategic_decision` ✅ (type of thinking + domain)
- `journey_orchestration` ✅ (metaphor + process)
- `learning_velocity` ✅ (goal + measure)

## Why This Organization Works

1. **Preserves Cognitive Identity**: Maintains the clear-thinking focus
2. **Flat Structure**: Easy to find tools without deep nesting
3. **Self-Documenting**: Tool names explain their purpose
4. **Academically Grounded**: Based on cognitive science concepts
5. **Practically Oriented**: Each tool solves real problems

## Migration Approach

1. **Keep Names**: Maintain the cognitive tool names from FastMCP
2. **Remove Suffixes**: Drop "_server" from all names
3. **Flat Directory**: Each tool gets its own directory at tools/ level
4. **Consistent Structure**: Each tool directory has:
   ```
   tool_name/
   ├── __init__.py
   ├── models.py      # Data structures
   ├── core.py        # Main logic
   └── README.md      # Tool documentation
   ```

## Next Steps

1. Create directories for each cognitive tool
2. Migrate FastMCP tools preserving their cognitive names
3. Implement remaining PSM tools with cognitive-focused names
4. Create unified documentation explaining the cognitive approach