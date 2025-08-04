# Technical Notes: Iterative Optimizer Development

## Development Timeline

### Phase 1: Basic Infrastructure
1. Created `optimizer.py` with simulated LLM calls
2. Implemented document chunking and indexing
3. Built basic 5-metric evaluation system
4. Added checkpoint and history tracking

### Phase 2: Advanced Evaluation
1. Created `evaluator.py` with 6 weighted criteria
2. Implemented benchmark-based scoring
3. Added suggestion generation
4. Created quality matrix tracking
5. Integrated evaluator into optimizer

### Phase 3: LLM Integration
1. Created `llm_optimizer.py` using Groq API
2. Initially attempted Anthropic Claude integration
3. Switched to Groq for better availability
4. Implemented JSON extraction from LLM responses
5. Added fallback mechanisms

### Phase 4: Variance Enhancement
1. Identified low variance problem (~3% between iterations)
2. Created `llm_optimizer_enhanced.py` with multiple variance mechanisms
3. Implemented dynamic temperature adjustment
4. Added multi-model rotation
5. Created strategic variation system

## Key Code Patterns

### 1. Dynamic Temperature Calculation
```python
def get_dynamic_temperature(self, base_temp: float = 0.7) -> float:
    iteration_factor = 1.0 - (self.iteration / 20)
    stuck_factor = 1.3 if variance < 0.02 else 1.0
    jitter = random.uniform(0.9, 1.1)
    return max(0.5, min(1.0, base_temp * iteration_factor * stuck_factor * jitter))
```

### 2. Strategic Variation
```python
strategies = {
    "innovation_focus": random.choice(self.innovation_strategies),
    "primary_focus": random.choice(self.focus_areas),
    "model": self.models[self.iteration % len(self.models)],
    "temperature": self.get_dynamic_temperature(),
    "top_p": random.uniform(0.8, 0.95),
    "creativity_boost": random.choice(creative_directions)
}
```

### 3. JSON Extraction Pattern
```python
import re
json_match = re.search(r'\{[\s\S]*\}', content)
if json_match:
    features = json.loads(json_match.group())
```

### 4. Evaluation Integration
```python
evaluation_result = self.evaluator.evaluate(new_features, self.iteration)
self.feature_list = self.optimize_features_with_llm(
    new_features, evaluation_result, strategy
)
```

## Models Configuration

### Initial Models (LLaMA variants)
- llama-3.3-70b-versatile (standard)
- llama-3.1-70b-versatile (alternative)
- mixtral-8x7b-32768 (different architecture)

### Updated Models (per linter changes)
- meta-llama/llama-4-maverick-17b-128e-instruct
- meta-llama/llama-4-scout-17b-16e-instruct
- qwen/qwen3-32b

## Variance Mechanisms Detail

### 1. Temperature Variance
- **Base**: 0.7
- **Iteration Factor**: Decreases over 20 iterations
- **Stuck Factor**: 1.3x boost when variance < 2%
- **Jitter**: ±10% random adjustment
- **Final Range**: 0.5-1.0

### 2. Model Rotation
- Cycles through 3 models
- Each has different training/biases
- Prevents model-specific patterns

### 3. Strategic Dimensions
- **Innovation Styles**: 5 options (revolutionary, incremental, etc.)
- **Focus Areas**: 6 options (UX, tech, business, etc.)
- **Optimization Styles**: 5 options (transformation, refinement, etc.)
- **Creative Directions**: 5 prompts
- **Total Combinations**: 5 × 6 × 5 × 5 = 750 variations

### 4. Prompt Engineering
- Explicit instructions to be different
- Challenge previous assumptions
- Mix unexpected combinations
- Creative interpretation of feedback

## Performance Observations

### Iteration Patterns
1. **Early iterations** (1-3): High exploration, wild ideas
2. **Middle iterations** (4-6): Refinement and consolidation
3. **Late iterations** (7+): Fine-tuning and convergence

### Quality Score Evolution
- Typical start: 65-70%
- Peak performance: 80-85%
- Convergence threshold: <2% improvement over 3 iterations

### Feature Count Growth
- Initial: 15-20 features
- Peak: 30-35 features
- Categories expand from 3 to 6-7

## Debugging Tips

### Common Issues
1. **JSON Parsing Failures**
   - LLM may return markdown formatting
   - Solution: Robust regex extraction

2. **Rate Limits**
   - Multiple models may hit limits
   - Solution: Increase sleep time, reduce models

3. **Low Variance**
   - Temperature too low
   - Solution: Boost base temperature, add more strategies

4. **Convergence Too Early**
   - Minimum iteration check
   - Solution: Require 5+ iterations

## Configuration Tweaks

### For Higher Variance
```python
# Increase temperature range
base_temp = 0.8  # Instead of 0.7

# Boost stuck factor
stuck_factor = 1.5  # Instead of 1.3

# Wider jitter
jitter = random.uniform(0.8, 1.2)  # Instead of 0.9-1.1
```

### For Faster Convergence
```python
# Lower temperature
base_temp = 0.6

# Tighter convergence
convergence_threshold = 0.01  # Instead of 0.02

# Fewer minimum iterations
min_iterations = 3  # Instead of 5
```

## Future Architecture Ideas

### 1. Parallel Evaluation
- Run multiple evaluators with different weights
- Ensemble scoring
- Multi-perspective optimization

### 2. Memory System
- Track successful patterns
- Avoid repeating failed approaches
- Build on proven features

### 3. Domain-Specific Agents
- UI/UX specialist
- Technical architecture expert
- Business value optimizer
- Security reviewer

### 4. Reinforcement Learning
- Reward successful features
- Penalize low-scoring patterns
- Learn optimal strategies

## Metrics to Track

### Current Metrics
- Overall quality score
- Individual criteria scores
- Feature count
- Iteration time
- Improvement rate

### Potential New Metrics
- Feature diversity index
- Innovation quotient
- Implementation complexity
- Market differentiation score
- User story coverage

---

These technical notes capture the implementation details, patterns, and insights gained during development of the iterative optimizer system.