# Reward-Kit Quick Reference

## Essential Imports

```python
from reward_kit import reward_function, EvaluateResult, MetricResult
from reward_kit.models import Message
from reward_kit.integrations.trl import create_trl_adapter
from reward_kit.evaluation import create_evaluation
```

## Basic Reward Function Template

```python
@reward_function
def my_evaluator(
    messages: Union[List[Message], List[Dict[str, Any]]],
    ground_truth: Optional[Dict[str, Any]] = None,
    **kwargs
) -> EvaluateResult:
    """Evaluate something specific."""
    
    # Extract content from last message
    if not messages:
        return EvaluateResult(score=0.0, reason="No messages", metrics={})
    
    last_msg = messages[-1]
    content = last_msg.get("content", "") if isinstance(last_msg, dict) else last_msg.content
    
    # Your evaluation logic
    score = evaluate_content(content)
    
    # Return result
    return EvaluateResult(
        score=score,
        reason=f"Score: {score:.2%}",
        metrics={
            "metric_name": MetricResult(
                score=score,
                success=score > 0.7,
                reason="Detailed explanation"
            )
        }
    )
```

## Common Patterns

### 1. JSON Parsing Pattern

```python
import json
import re

def extract_json_from_content(content: str) -> Optional[dict]:
    """Extract JSON from LLM response."""
    try:
        # Try direct parsing first
        return json.loads(content)
    except:
        # Try to find JSON in the content
        json_match = re.search(r'\{[\s\S]*\}', content)
        if json_match:
            try:
                return json.loads(json_match.group())
            except:
                pass
    return None
```

### 2. Multi-Metric Pattern

```python
@reward_function
def multi_metric_evaluator(messages, **kwargs) -> EvaluateResult:
    """Evaluate with multiple metrics."""
    
    metrics = {}
    scores = []
    
    # Metric 1
    metric1_score = calculate_metric1(messages)
    metrics["metric1"] = MetricResult(
        score=metric1_score,
        success=metric1_score > 0.8,
        reason="Metric 1 evaluation"
    )
    scores.append(metric1_score)
    
    # Metric 2
    metric2_score = calculate_metric2(messages)
    metrics["metric2"] = MetricResult(
        score=metric2_score,
        success=metric2_score > 0.7,
        reason="Metric 2 evaluation"
    )
    scores.append(metric2_score)
    
    # Combined score
    overall_score = sum(scores) / len(scores)
    
    return EvaluateResult(
        score=overall_score,
        reason=f"Average of {len(metrics)} metrics",
        metrics=metrics
    )
```

### 3. Error Handling Pattern

```python
@reward_function
def robust_evaluator(messages, **kwargs) -> EvaluateResult:
    """Evaluator with comprehensive error handling."""
    
    try:
        # Main evaluation logic
        result = perform_evaluation(messages)
        return EvaluateResult(
            score=result['score'],
            reason=result['reason'],
            metrics=result.get('metrics', {})
        )
    
    except json.JSONDecodeError as e:
        return EvaluateResult(
            score=0.0,
            reason=f"JSON parsing error: {str(e)}",
            metrics={"error": MetricResult(score=0.0, success=False, reason="Invalid JSON")}
        )
    
    except KeyError as e:
        return EvaluateResult(
            score=0.0,
            reason=f"Missing required field: {str(e)}",
            metrics={"error": MetricResult(score=0.0, success=False, reason=f"Missing {e}")}
        )
    
    except Exception as e:
        return EvaluateResult(
            score=0.0,
            reason=f"Unexpected error: {type(e).__name__}",
            metrics={"error": MetricResult(score=0.0, success=False, reason=str(e))}
        )
```

### 4. Ground Truth Comparison Pattern

```python
@reward_function
def comparison_evaluator(
    messages: List[Dict[str, Any]],
    ground_truth: Optional[Dict[str, Any]] = None,
    **kwargs
) -> EvaluateResult:
    """Compare output with ground truth."""
    
    if not ground_truth:
        return EvaluateResult(
            score=0.5,
            reason="No ground truth provided, using default score",
            metrics={}
        )
    
    # Extract generated output
    generated = extract_output(messages)
    expected = ground_truth.get("expected_output")
    
    # Calculate similarity
    similarity = calculate_similarity(generated, expected)
    
    return EvaluateResult(
        score=similarity,
        reason=f"Similarity to ground truth: {similarity:.2%}",
        metrics={
            "accuracy": MetricResult(
                score=similarity,
                success=similarity > 0.9,
                reason=f"Matched {similarity:.0%} of expected output"
            )
        }
    )
```

## CLI Commands

### Preview Evaluation

```bash
# Test reward function with sample data
reward-kit preview \
  --metrics-folders "my_metric=./path/to/metric" \
  --samples ./samples.jsonl

# With multiple metrics
reward-kit preview \
  --metrics-folders "metric1=./metrics/metric1" "metric2=./metrics/metric2" \
  --samples ./samples.jsonl
```

### Run Full Evaluation

```bash
# Run with configuration
reward-kit run --config-name my_eval --config-path ./conf

# Override parameters
reward-kit run --config-name my_eval --config-path ./conf \
  generation.model_name="llama-3.1-70b" \
  evaluation_params.limit_samples=100
```

### Deploy Reward Function

```bash
# Deploy to Fireworks
reward-kit deploy \
  --id my-evaluator \
  --metrics-folders "metric=./metrics" \
  --display-name "My Evaluator" \
  --description "Evaluates specific criteria" \
  --force

# Deploy as local server
reward-kit deploy \
  --id local-evaluator \
  --target local-serve \
  --function-ref my_module.my_reward_function \
  --verbose
```

## Configuration Examples

### Basic Evaluation Config (YAML)

```yaml
# conf/my_eval.yaml
defaults:
  - _self_

dataset:
  source_type: "jsonl"
  path: "./data/evaluation_data.jsonl"
  
generation:
  enabled: true
  model_name: "accounts/fireworks/models/llama-v3p1-70b-instruct"
  max_tokens: 2000
  temperature: 0.7
  
evaluation:
  metrics:
    - name: "quality"
      module: "my_metrics"
      function: "quality_evaluator"
      
output:
  results_file: "evaluation_results.jsonl"
  save_preview: true
```

### Dataset with Column Mapping

```yaml
dataset:
  source_type: "huggingface"
  path_or_name: "my-org/my-dataset"
  split: "test"
  column_mapping:
    input: "messages"
    output: "ground_truth_for_eval"
  limit_samples: 1000
```

## TRL Integration

### Basic TRL Adapter

```python
from reward_kit.integrations.trl import create_trl_adapter

# Create adapter for TRL
trl_reward = create_trl_adapter(
    reward_fn=my_evaluator,
    dataset_to_reward_kwargs_map={
        "expected": "ground_truth"  # Map dataset column to kwarg
    },
    static_reward_kwargs={
        "threshold": 0.8
    }
)

# Use with TRL trainer
from trl import GRPOTrainer, GRPOConfig

trainer = GRPOTrainer(
    model=model,
    reward_funcs=[trl_reward],
    args=training_args,
    train_dataset=dataset
)
```

### Combined Rewards for TRL

```python
def combine_rewards_for_trl(reward_configs, weights=None):
    """Combine multiple rewards with weights."""
    
    adapters = []
    for config in reward_configs:
        adapter = create_trl_adapter(
            reward_fn=config["func"],
            dataset_to_reward_kwargs_map=config.get("map", {}),
            static_reward_kwargs=config.get("kwargs", {})
        )
        adapters.append(adapter)
    
    if weights is None:
        weights = [1.0 / len(adapters)] * len(adapters)
    
    def combined_adapter(prompts, completions, **kwargs):
        all_scores = []
        for adapter in adapters:
            scores = adapter(prompts, completions, **kwargs)
            all_scores.append(scores)
        
        # Weighted combination
        combined = []
        for i in range(len(completions)):
            score = sum(
                all_scores[j][i] * weights[j] 
                for j in range(len(adapters))
            )
            combined.append(score)
        
        return combined
    
    return combined_adapter
```

## Testing Patterns

### Unit Test Template

```python
import pytest
from my_rewards import my_evaluator

def test_evaluator_basic():
    """Test basic functionality."""
    messages = [
        {"role": "user", "content": "Test input"},
        {"role": "assistant", "content": "Test output"}
    ]
    
    result = my_evaluator(messages)
    
    assert isinstance(result.score, float)
    assert 0 <= result.score <= 1
    assert isinstance(result.reason, str)
    assert isinstance(result.metrics, dict)

def test_evaluator_edge_cases():
    """Test edge cases."""
    # Empty messages
    result = my_evaluator([])
    assert result.score == 0.0
    
    # Invalid format
    result = my_evaluator([{"role": "user"}])
    assert result.score == 0.0
```

### Integration Test

```python
def test_reward_function_integration():
    """Test full integration."""
    
    # Load test dataset
    with open("test_data.jsonl") as f:
        test_samples = [json.loads(line) for line in f]
    
    # Run evaluation
    results = []
    for sample in test_samples:
        result = my_evaluator(
            messages=sample["messages"],
            ground_truth=sample.get("ground_truth")
        )
        results.append(result)
    
    # Verify results
    avg_score = sum(r.score for r in results) / len(results)
    assert avg_score > 0.5  # Expect reasonable performance
    
    # Check metrics
    for result in results:
        assert all(
            isinstance(m, MetricResult) 
            for m in result.metrics.values()
        )
```

## Common Issues and Solutions

### Issue: JSON Parsing Failures

```python
# Solution: Robust JSON extraction
def safe_json_parse(content: str) -> dict:
    """Safely parse JSON with fallbacks."""
    # Remove markdown code blocks
    content = re.sub(r'```json\n(.*?)\n```', r'\1', content, flags=re.DOTALL)
    content = re.sub(r'```\n(.*?)\n```', r'\1', content, flags=re.DOTALL)
    
    # Try multiple parsing strategies
    strategies = [
        lambda: json.loads(content),
        lambda: json.loads(re.search(r'\{[\s\S]*\}', content).group()),
        lambda: eval(content),  # Last resort, be careful!
    ]
    
    for strategy in strategies:
        try:
            return strategy()
        except:
            continue
    
    return {}
```

### Issue: Message Format Variations

```python
# Solution: Flexible message handling
def get_message_content(message):
    """Extract content from various message formats."""
    if isinstance(message, dict):
        return message.get("content", "")
    elif hasattr(message, "content"):
        return message.content or ""
    elif isinstance(message, str):
        return message
    else:
        return str(message)
```

### Issue: Metric Aggregation

```python
# Solution: Weighted metric aggregation
def aggregate_metrics(metrics: Dict[str, MetricResult], weights: Dict[str, float] = None) -> float:
    """Aggregate multiple metrics with optional weights."""
    if not metrics:
        return 0.0
    
    if weights is None:
        # Equal weights
        return sum(m.score for m in metrics.values()) / len(metrics)
    
    # Weighted average
    total_weight = sum(weights.values())
    weighted_sum = sum(
        metrics[name].score * weights.get(name, 0)
        for name in metrics
    )
    
    return weighted_sum / total_weight if total_weight > 0 else 0.0
```

## Performance Tips

1. **Cache Expensive Operations**
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=128)
   def expensive_calculation(input_hash):
       # Expensive operation
       return result
   ```

2. **Batch Processing**
   ```python
   def batch_evaluate(all_messages, batch_size=10):
       results = []
       for i in range(0, len(all_messages), batch_size):
           batch = all_messages[i:i+batch_size]
           batch_results = [evaluator(msg) for msg in batch]
           results.extend(batch_results)
       return results
   ```

3. **Async Evaluation**
   ```python
   import asyncio
   
   async def async_evaluator(messages):
       # Async operations
       result = await async_operation(messages)
       return EvaluateResult(score=result, reason="Async evaluation", metrics={})
   ```

This quick reference provides the most common patterns and usage examples for reward-kit integration.