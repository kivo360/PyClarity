# Progressive Analyzers as Default

As of the latest version, PyClarity uses progressive analyzers as the default implementation for all cognitive tools when a database is configured. This provides powerful session management and multi-step analysis capabilities while maintaining backward compatibility.

## How It Works

### With Database (Progressive Mode - Default)

When you run the MCP server with a database URL, all tools automatically use progressive analyzers:

```python
# Server initialization with database
server = await create_progressive_server_v2("postgresql://user:pass@localhost/pyclarity")
```

In this mode, all standard tool names map to progressive implementations:
- `sequential_thinking` → Progressive Sequential Thinking Analyzer
- `mental_models` → Progressive Mental Model Analyzer
- `debugging_approaches` → Progressive Debugging Analyzer
- `collaborative_reasoning` → Progressive Collaborative Analyzer
- `decision_framework` → Progressive Decision Analyzer
- `metacognitive_monitoring` → Progressive Metacognitive Analyzer
- `scientific_method` → Progressive Scientific Analyzer
- `visual_reasoning` → Progressive Visual Analyzer
- `creative_thinking` → Progressive Creative Analyzer
- `systems_thinking` → Progressive Systems Analyzer

### Without Database (Standard Mode - Fallback)

When no database is configured, tools fall back to standard implementations without session management:

```python
# Server initialization without database
server = await create_progressive_server_v2()  # No database URL
```

## Tool Usage

### Single-Use Analysis

Even with progressive analyzers, you can use tools for simple, one-off analysis:

```json
{
  "tool": "mental_models",
  "arguments": {
    "problem_statement": "How to scale a web application?",
    "model_type": "first_principles",
    "context": "Growing startup with 1000 daily users"
  }
}
```

The tool will automatically create a session but you don't need to manage it.

### Multi-Step Sessions

For complex analysis, use the `session_id` to continue across steps:

```json
// Step 1
{
  "tool": "debugging_approaches",
  "arguments": {
    "issue_description": "Memory leak in production",
    "debugging_type": "systematic"
  }
}

// Returns: { "session_id": "debug-123", ... }

// Step 2 - Continue same session
{
  "tool": "debugging_approaches",
  "arguments": {
    "session_id": "debug-123",
    "step_number": 2,
    "hypothesis": "Connection pool issue",
    "evidence": ["Memory grows with connections"]
  }
}
```

## Benefits

1. **Automatic Session Management** - No need to explicitly create sessions
2. **Progress Tracking** - Each step is numbered and tracked
3. **State Persistence** - Previous insights inform future analysis
4. **Rich Responses** - Detailed insights, recommendations, and next steps
5. **Cross-Tool Integration** - Share sessions between different tools
6. **Backward Compatible** - Works with existing tool interfaces

## Migration Guide

### For Tool Users

No changes needed! Tools work the same way but now have additional capabilities:
- Optional `session_id` parameter for multi-step workflows
- Richer response data with insights and recommendations
- Automatic progress tracking

### For Developers

To leverage progressive features:

1. **Check for session_id in responses** - Save it for multi-step workflows
2. **Use step_number** - Track progress through analysis
3. **Build on previous results** - Use `build_on_previous` flags
4. **Monitor evolution** - Track how analysis improves over steps

## Examples

### Simple Use Case
```python
# Single-use creative thinking
result = await toolkit.generate_ideas(
    challenge="Improve code review process",
    creative_mode="divergent"
)
print(f"Generated {result['new_ideas_count']} ideas")
```

### Advanced Use Case
```python
# Multi-step scientific investigation
# Step 1: Observation
result1 = await toolkit.conduct_research(
    research_question="Why is the API slow?",
    domain="Performance optimization",
    research_phase="observation",
    observations=["Response times over 2s", "High CPU usage"]
)
session_id = result1['session_id']

# Step 2: Hypothesis
result2 = await toolkit.conduct_research(
    session_id=session_id,
    step_number=2,
    research_phase="hypothesis",
    hypothesis="N+1 query problem in ORM"
)

# Step 3: Experimentation
result3 = await toolkit.conduct_research(
    session_id=session_id,
    step_number=3,
    research_phase="experimentation",
    experiment_design={"method": "Query profiling"}
)
```

## Configuration

### Environment Variables

- `DATABASE_URL` - PostgreSQL connection string (enables progressive mode)
- `PYCLARITY_MODE` - Set to "standard" to force standard mode even with database

### Server Options

```python
# Force standard mode
server = await create_progressive_server_v2(
    db_url=None  # Explicitly disable progressive mode
)

# Custom stores
server = await create_progressive_server_v2(
    db_url="postgresql://...",
    custom_stores={
        "mental_model_store": MyCustomMentalModelStore(),
        # ... other custom stores
    }
)
```