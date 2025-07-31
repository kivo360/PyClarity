# Tool Migration Plan: Consolidating PyClarity Tools

## Current State

We have tools in two locations:

### 1. FastMCP Cognitive Tools (14 tools)
Location: `/clear-thinking-fastmcp/src/clear_thinking_fastmcp/tools/`

**MCP Server Tools:**
- `sequential_thinking_server.py`
- `mental_model_server.py`
- `decision_framework_server.py`
- `collaborative_reasoning_server.py`
- `scientific_method_server.py`
- `design_patterns_server.py`
- `impact_propagation_server.py`
- `iterative_validation_server.py`
- `metacognitive_monitoring_server.py`
- `multi_perspective_server.py`
- `programming_paradigms_server.py`
- `sequential_readiness_server.py`
- `triple_constraint_server.py`
- `visual_reasoning_server.py`

### 2. New PSM-Based Tools (6 planned, 1 implemented)
Location: `/src/pyclarity/tools/`

**Business Tools:**
- ✅ `strategic_decision/` - Strategic Decision Accelerator (implemented)
- 🔄 Journey Orchestration Intelligence (pending)
- 🔄 Project Health Diagnostic (pending)
- 🔄 Team Dynamics Optimizer (tests written)
- 🔄 Mentorship Evolution Framework (tests written)
- 🔄 Learning Velocity Maximizer (tests written)

## Migration Strategy

### Option 1: Full Consolidation
Move everything to `/src/pyclarity/tools/` with proper categorization:

```
/src/pyclarity/tools/
├── cognitive/                    # FastMCP cognitive tools
│   ├── sequential_thinking/
│   ├── mental_models/
│   ├── decision_framework/
│   └── ...
├── business/                     # PSM-based business tools
│   ├── strategic_decision/
│   ├── journey_orchestration/
│   ├── project_health/
│   └── ...
└── __init__.py
```

### Option 2: Type-Based Organization
Organize by tool type/purpose:

```
/src/pyclarity/tools/
├── reasoning/                    # Reasoning tools
│   ├── sequential_thinking/
│   ├── collaborative_reasoning/
│   └── mental_models/
├── decision/                     # Decision-making tools
│   ├── strategic_decision/
│   ├── decision_framework/
│   └── multi_perspective/
├── project/                      # Project management tools
│   ├── journey_orchestration/
│   ├── project_health/
│   └── triple_constraint/
├── team/                         # Team & people tools
│   ├── team_dynamics/
│   ├── mentorship_evolution/
│   └── ...
└── __init__.py
```

### Option 3: Abstraction-Level Organization
Based on our abstraction levels guide:

```
/src/pyclarity/tools/
├── level1_business/              # User-facing business tools
│   ├── strategic_decision/
│   ├── journey_orchestration/
│   └── project_health/
├── level2_cognitive/             # Domain engines
│   ├── sequential_thinking/
│   ├── mental_models/
│   └── decision_framework/
├── level3_technical/             # Technical services
│   ├── impact_propagation/
│   ├── design_patterns/
│   └── ...
└── __init__.py
```

## Recommended Approach: Hybrid Organization

```
/src/pyclarity/tools/
├── strategic/                    # Strategic & decision tools
│   ├── decision_accelerator/     # From PSM
│   ├── decision_framework/       # From FastMCP
│   └── multi_perspective/        # From FastMCP
├── execution/                    # Execution & project tools
│   ├── journey_orchestration/    # From PSM
│   ├── project_health/          # From PSM
│   ├── triple_constraint/       # From FastMCP
│   └── iterative_validation/    # From FastMCP
├── cognitive/                    # Pure cognitive tools
│   ├── sequential_thinking/     # From FastMCP
│   ├── mental_models/          # From FastMCP
│   ├── scientific_method/      # From FastMCP
│   └── metacognitive/          # From FastMCP
├── collaboration/               # Team & collaboration tools
│   ├── team_dynamics/          # From PSM
│   ├── mentorship_evolution/   # From PSM
│   ├── collaborative_reasoning/ # From FastMCP
│   └── multi_perspective/      # From FastMCP (duplicate?)
├── learning/                    # Learning & improvement tools
│   ├── learning_velocity/      # From PSM
│   ├── programming_paradigms/  # From FastMCP
│   └── design_patterns/        # From FastMCP
└── analysis/                    # Analysis & monitoring tools
    ├── impact_propagation/     # From FastMCP
    ├── visual_reasoning/       # From FastMCP
    └── sequential_readiness/   # From FastMCP
```

## Migration Steps

### Phase 1: Structure Setup
1. Create the new directory structure in `/src/pyclarity/tools/`
2. Update `__init__.py` files for proper imports
3. Create category READMEs explaining each category

### Phase 2: FastMCP Tool Migration
For each FastMCP tool:
1. Create new directory under appropriate category
2. Refactor from MCP server pattern to PyClarity pattern:
   - Extract core logic from server classes
   - Create proper models using Pydantic
   - Implement async methods
   - Follow naming conventions
3. Create/update tests
4. Update imports

### Phase 3: PSM Tool Completion
1. Complete remaining PSM tools in their categories
2. Ensure consistent patterns across all tools
3. Update documentation

### Phase 4: Integration
1. Create cross-tool integration patterns
2. Build tool composition examples
3. Update main PyClarity CLI

## Tool Transformation Example

### Before (FastMCP pattern):
```python
# mental_model_server.py
@server.tool()
async def analyze_with_mental_model(task_description: str, ...) -> MentalModelAnalysis:
    # Server implementation
```

### After (PyClarity pattern):
```python
# cognitive/mental_models/analyzer.py
class MentalModelAnalyzer:
    async def analyze_mental_model(self, context: MentalModelContext) -> MentalModelResult:
        # Core business logic
```

## Benefits of Migration

1. **Consistency**: All tools follow same patterns
2. **Discoverability**: Clear categorization
3. **Reusability**: Shared components and models
4. **Maintainability**: Single location for all tools
5. **Testing**: Unified testing approach
6. **Documentation**: Consistent docs structure

## Considerations

1. **Backward Compatibility**: Keep FastMCP servers as thin wrappers?
2. **Import Paths**: Will change - need to update all references
3. **Testing**: Need to migrate/update all tests
4. **Documentation**: Update all tool references
5. **Dependencies**: Ensure all deps are in pyproject.toml

## Next Steps

1. Choose organization structure (recommend Hybrid)
2. Create migration script to automate repetitive tasks
3. Start with one category as proof of concept
4. Iterate based on learnings