# Persona-Based Content Generation with Distilabel

This directory contains various approaches to generate persona-based modifications using the Distilabel framework and LiteLLM.

## Overview

These scripts demonstrate how to:
- Load personas from the PersonaHub dataset
- Generate various types of content tailored to each persona
- Use dynamic system prompts based on persona analysis
- Create business cases, social scenarios, emotional journeys, and more

## Scripts

### 1. `llm_persona_gen.py` - Basic Persona Generation
Simple example that generates creative content based on personas.

```bash
python llm_persona_gen.py
```

**Features:**
- Basic TextGeneration task with persona mapping
- Fixed system prompt for all personas
- Saves results to `persona_distiset/`

### 2. `llm_persona_advanced.py` - Multi-Aspect Generation
Generates multiple types of content for each persona.

```bash
python llm_persona_advanced.py
```

**Features:**
- 7 different generation types (business cases, social scenarios, etc.)
- Can generate single type or all types for each persona
- Organized output structure

### 3. `persona_modifier_task.py` - Custom Task Implementation
Implements a custom Distilabel task for persona modifications.

```bash
python persona_modifier_task.py
```

**Features:**
- Custom `PersonaModifier` task class
- Batch processing support
- Multiple export formats (JSON, CSV, HuggingFace)
- Detailed prompts for each modification type

### 4. `dynamic_persona_generator.py` - Dynamic Prompt Generation
Most advanced approach with two-stage generation.

```bash
python dynamic_persona_generator.py
```

**Features:**
- Stage 1: Analyzes personas to understand characteristics
- Stage 2: Generates content with persona-specific system prompts
- Creates contextual and relevant modifications
- JSON output with full analysis

## Generation Types

All scripts support various generation types:

1. **Business Case** - Product/service ideas for the persona
2. **Social Scenario** - Social situations they might encounter
3. **Emotional Journey** - Emotional experiences and growth
4. **Psychometric Profile** - Personality and behavioral analysis
5. **Decision Framework** - How they make decisions
6. **Sales Strategy** - How to sell to them effectively
7. **SaaS Solution** - Software solutions for their needs

## Setup

1. Ensure you have your Fireworks API key:
```bash
export FIREWORKS_API_KEY="your-api-key-here"
```

2. Install dependencies (from project root):
```bash
uv sync
```

## Output Examples

### Basic Generation Output
```json
{
  "persona": "A high school environmental science teacher...",
  "generation": "Based on this persona, I would create a SaaS platform...",
  "model_name": "fireworks_ai/accounts/fireworks/models/glm-4p5-air"
}
```

### Dynamic Generation Output
```json
{
  "persona": "A high school environmental science teacher...",
  "system_prompt": "You are a business strategist specializing in education technology...",
  "generated_content": "EcoClassroom: A comprehensive environmental education platform...",
  "generation_type": "business_case"
}
```

## Best Practices

1. **Start Small**: Test with 5-10 personas before scaling up
2. **Monitor API Usage**: Each persona generates multiple API calls
3. **Use Batching**: The `persona_modifier_task.py` supports batch processing
4. **Save Checkpoints**: For large datasets, save intermediate results
5. **Dynamic Prompts**: Use `dynamic_persona_generator.py` for best results

## Customization

### Adding New Generation Types

In any script, add to the generation types dictionary:

```python
GENERATION_TYPES["new_type"] = {
    "system_prompt": "You are an expert in...",
    "template": "Based on persona: {{ instruction }}\n\nGenerate..."
}
```

### Changing Models

Update the model in LiteLLM initialization:

```python
llm=LiteLLM(
    model="your-preferred-model",
    generation_kwargs={"temperature": 0.8, "max_new_tokens": 1000}
)
```

## Troubleshooting

1. **API Key Issues**: Ensure `FIREWORKS_API_KEY` is set
2. **Import Errors**: Run from project root with proper Python path
3. **Memory Issues**: Reduce batch size or number of personas
4. **JSON Parse Errors**: The dynamic generator has fallback handling

## Data Flow

```
PersonaHub Dataset
    ↓
Persona Selection (e.g., 100 personas)
    ↓
[Optional] Persona Analysis (dynamic_persona_generator.py)
    ↓
System Prompt Generation (fixed or dynamic)
    ↓
LLM Generation (Fireworks API)
    ↓
Output Processing
    ↓
Save Results (disk, JSON, CSV, or HuggingFace)
```

## Performance Tips

- **Parallel Processing**: Advanced scripts can process multiple personas simultaneously
- **Caching**: Distilabel caches results by default
- **Batch Size**: Adjust `input_batch_size` for optimal throughput
- **Temperature**: Lower (0.6-0.7) for consistency, higher (0.8-0.9) for creativity