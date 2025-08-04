# Dynamic Prompt Rewriting

Dynamic Prompt Rewriting is a technique where an AI evaluates its initial output, rewrites the prompt for clarity or specificity, and regenerates a better result.

## Core Concept

The technique operates in a cycle:
1. Generate initial output from a prompt
2. Evaluate output against criteria
3. If inadequate, rewrite the prompt with improvements
4. Regenerate with the refined prompt
5. Repeat until criteria are met or limit reached

## Implementation

### Basic Template

```python
def dynamic_prompt_rewriting(initial_prompt, criteria, max_rewrites=2):
    """
    Automatically refine prompts until output meets criteria
    """
    current_prompt = initial_prompt
    
    for iteration in range(max_rewrites + 1):
        # Generate output
        output = generate_output(current_prompt)
        
        # Evaluate against criteria
        if meets_criteria(output, criteria):
            return {
                "final_prompt": current_prompt,
                "output": output,
                "iterations": iteration
            }
        
        # Rewrite prompt if not meeting criteria
        if iteration < max_rewrites:
            current_prompt = rewrite_prompt(current_prompt, output, criteria)
    
    return {
        "final_prompt": current_prompt,
        "output": output,
        "iterations": max_rewrites,
        "criteria_met": False
    }
```

### Rewriting Strategy

```python
def rewrite_prompt(original_prompt, failed_output, criteria):
    rewrite_instruction = f"""
    The following prompt produced inadequate output:
    PROMPT: {original_prompt}
    OUTPUT: {failed_output}
    
    The output failed these criteria:
    {json.dumps(criteria, indent=2)}
    
    Rewrite the prompt to:
    1. Be more specific about requirements
    2. Include concrete examples if helpful
    3. Clarify any ambiguous terms
    4. Add constraints that ensure criteria are met
    
    New prompt:
    """
    
    return generate_improved_prompt(rewrite_instruction)
```

## Use Cases

### 1. Feature List Generation
```python
initial_prompt = "Generate a feature list for a task management app"

criteria = {
    "min_features": 5,
    "required_details": ["name", "description", "use_case"],
    "specificity_level": "high"
}

result = dynamic_prompt_rewriting(initial_prompt, criteria)
```

### 2. Technical Documentation
```python
initial_prompt = "Write API documentation for a user service"

criteria = {
    "sections": ["endpoints", "authentication", "examples", "errors"],
    "detail_level": "comprehensive",
    "code_examples": True
}

result = dynamic_prompt_rewriting(initial_prompt, criteria)
```

### 3. Content Creation
```python
initial_prompt = "Create a blog post about AI trends"

criteria = {
    "word_count": {"min": 800, "max": 1200},
    "sections": ["introduction", "main_points", "conclusion"],
    "tone": "professional",
    "citations": True
}

result = dynamic_prompt_rewriting(initial_prompt, criteria)
```

## Criteria Definition

### 1. Quantitative Criteria
```python
criteria = {
    "min_items": 5,
    "max_length": 1000,
    "required_sections": 3,
    "detail_score": 0.8  # 0-1 scale
}
```

### 2. Qualitative Criteria
```python
criteria = {
    "tone": "professional",
    "clarity": "high",
    "technical_level": "intermediate",
    "audience": "developers"
}
```

### 3. Structural Criteria
```python
criteria = {
    "format": "json",
    "required_fields": ["id", "title", "content"],
    "nested_structure": True,
    "schema": {
        "type": "object",
        "properties": {
            "features": {
                "type": "array",
                "minItems": 5
            }
        }
    }
}
```

## Advanced Techniques

### 1. Multi-Stage Rewriting
```python
def multi_stage_rewriting(initial_prompt, stages):
    """
    Apply different criteria at each stage
    """
    current_prompt = initial_prompt
    
    for stage_name, stage_criteria in stages.items():
        result = dynamic_prompt_rewriting(
            current_prompt, 
            stage_criteria,
            max_rewrites=2
        )
        current_prompt = result["final_prompt"]
        
        if not result.get("criteria_met", True):
            return {
                "failed_at_stage": stage_name,
                "result": result
            }
    
    return {
        "success": True,
        "final_prompt": current_prompt,
        "stages_completed": list(stages.keys())
    }

# Usage
stages = {
    "clarity": {"specificity_score": 0.7},
    "completeness": {"min_sections": 5},
    "quality": {"professional_tone": True}
}
```

### 2. Learning from Rewrites
```python
class AdaptivePromptRewriter:
    def __init__(self):
        self.rewrite_history = []
    
    def learn_from_rewrite(self, original, improved, criteria):
        """
        Track successful rewrites for pattern learning
        """
        self.rewrite_history.append({
            "original": original,
            "improved": improved,
            "criteria": criteria,
            "improvement_patterns": self.extract_patterns(original, improved)
        })
    
    def extract_patterns(self, original, improved):
        """
        Identify what made the improvement successful
        """
        patterns = []
        
        if "specific" not in original and "specific" in improved:
            patterns.append("added_specificity")
        
        if len(improved) > len(original) * 1.5:
            patterns.append("added_detail")
        
        if "example" in improved and "example" not in original:
            patterns.append("added_examples")
        
        return patterns
    
    def suggest_improvements(self, prompt, criteria):
        """
        Use learned patterns to suggest improvements
        """
        relevant_history = [
            h for h in self.rewrite_history 
            if similar_criteria(h["criteria"], criteria)
        ]
        
        common_patterns = self.get_common_patterns(relevant_history)
        return self.apply_patterns(prompt, common_patterns)
```

### 3. Parallel Rewriting Strategies
```python
def parallel_rewriting_strategies(initial_prompt, criteria):
    """
    Try multiple rewriting strategies in parallel
    """
    strategies = {
        "add_specificity": lambda p: f"{p}\nBe specific about each item.",
        "add_constraints": lambda p: f"{p}\nMust include: {criteria}",
        "add_examples": lambda p: f"{p}\nFor example: [relevant example]",
        "restructure": lambda p: restructure_prompt(p)
    }
    
    results = {}
    for strategy_name, strategy_func in strategies.items():
        rewritten = strategy_func(initial_prompt)
        output = generate_output(rewritten)
        score = evaluate_output(output, criteria)
        results[strategy_name] = {
            "prompt": rewritten,
            "output": output,
            "score": score
        }
    
    # Return best performing strategy
    best_strategy = max(results.items(), key=lambda x: x[1]["score"])
    return best_strategy[1]
```

## Common Rewriting Patterns

### 1. Adding Specificity
```python
# Original
"Create a list of features"

# Rewritten
"Create a list of 5-7 specific features with names, descriptions, and use cases"
```

### 2. Adding Structure
```python
# Original
"Describe the product"

# Rewritten
"Describe the product with these sections:
1. Overview (2-3 sentences)
2. Key Features (bullet points)
3. Target Audience
4. Unique Value Proposition"
```

### 3. Adding Constraints
```python
# Original
"Generate user stories"

# Rewritten
"Generate 5 user stories following the format:
'As a [user type], I want to [action] so that [benefit]'
Focus on core functionality only."
```

## Evaluation Functions

### 1. Criteria Checking
```python
def meets_criteria(output, criteria):
    """
    Check if output meets all specified criteria
    """
    for criterion, requirement in criteria.items():
        if not check_single_criterion(output, criterion, requirement):
            return False
    return True

def check_single_criterion(output, criterion, requirement):
    """
    Check individual criterion
    """
    if criterion == "min_items":
        return count_items(output) >= requirement
    elif criterion == "required_fields":
        return all(field in output for field in requirement)
    elif criterion == "word_count":
        word_count = len(output.split())
        return requirement["min"] <= word_count <= requirement["max"]
    # Add more criterion checks
```

### 2. Quality Scoring
```python
def calculate_output_quality(output, criteria):
    """
    Score output quality on 0-1 scale
    """
    scores = []
    
    # Completeness score
    if "required_sections" in criteria:
        present = sum(1 for s in criteria["required_sections"] if s in output)
        scores.append(present / len(criteria["required_sections"]))
    
    # Detail score
    if "min_detail_per_item" in criteria:
        detail_score = calculate_detail_score(output, criteria)
        scores.append(detail_score)
    
    # Specificity score
    specificity = calculate_specificity(output)
    scores.append(specificity)
    
    return sum(scores) / len(scores) if scores else 0
```

## Integration with PyClarity

Dynamic Prompt Rewriting can enhance PyClarity's tools:

### 1. Adaptive Tool Prompts
```python
class AdaptiveToolPrompt:
    def __init__(self, tool_name):
        self.tool_name = tool_name
        self.base_prompt = self.get_base_prompt()
    
    def get_base_prompt(self):
        prompts = {
            "strategic_decision": "Analyze strategic options...",
            "multi_perspective": "Generate perspectives on...",
            "sequential_readiness": "Assess readiness for..."
        }
        return prompts.get(self.tool_name, "")
    
    def refine_for_context(self, context, user_requirements):
        criteria = self.extract_criteria(user_requirements)
        return dynamic_prompt_rewriting(
            self.base_prompt + f"\nContext: {context}",
            criteria
        )
```

### 2. Quality Assurance
```python
def ensure_output_quality(tool_output, quality_criteria):
    """
    Use dynamic rewriting to ensure tool outputs meet quality standards
    """
    if not meets_criteria(tool_output, quality_criteria):
        refined_prompt = create_refinement_prompt(tool_output, quality_criteria)
        return dynamic_prompt_rewriting(refined_prompt, quality_criteria)
    return tool_output
```

## Best Practices

### 1. Set Reasonable Limits
```python
config = {
    "max_rewrites": 3,  # Prevent infinite loops
    "rewrite_timeout": 30,  # Seconds
    "min_improvement": 0.1  # Minimum score increase to continue
}
```

### 2. Track Rewriting Metrics
```python
def track_rewriting_metrics(rewriting_session):
    metrics = {
        "total_rewrites": rewriting_session["iterations"],
        "success_rate": rewriting_session.get("criteria_met", False),
        "improvement_score": calculate_improvement(
            rewriting_session["initial_output"],
            rewriting_session["final_output"]
        ),
        "time_taken": rewriting_session.get("duration", 0)
    }
    return metrics
```

### 3. Graceful Degradation
```python
def dynamic_rewriting_with_fallback(prompt, criteria, max_attempts=3):
    try:
        result = dynamic_prompt_rewriting(prompt, criteria)
        if result.get("criteria_met"):
            return result
    except Exception as e:
        logger.warning(f"Rewriting failed: {e}")
    
    # Fallback to simpler criteria
    simplified_criteria = simplify_criteria(criteria)
    return dynamic_prompt_rewriting(prompt, simplified_criteria, max_rewrites=1)
```

## Performance Optimization

### 1. Caching Successful Rewrites
```python
class RewriteCache:
    def __init__(self):
        self.cache = {}
    
    def get_cached_rewrite(self, prompt_hash, criteria_hash):
        key = f"{prompt_hash}:{criteria_hash}"
        return self.cache.get(key)
    
    def cache_successful_rewrite(self, original, rewritten, criteria):
        key = f"{hash(original)}:{hash(str(criteria))}"
        self.cache[key] = {
            "rewritten": rewritten,
            "timestamp": time.time()
        }
```

### 2. Early Stopping
```python
def dynamic_rewriting_with_early_stopping(prompt, criteria):
    """
    Stop rewriting if improvement plateaus
    """
    previous_score = 0
    
    for iteration in range(MAX_REWRITES):
        output = generate_output(prompt)
        current_score = evaluate_output(output, criteria)
        
        if current_score >= ACCEPTABLE_THRESHOLD:
            return {"success": True, "output": output}
        
        improvement = current_score - previous_score
        if improvement < MIN_IMPROVEMENT:
            return {"success": False, "output": output, "reason": "plateau"}
        
        prompt = rewrite_prompt(prompt, output, criteria)
        previous_score = current_score
```

## Conclusion

Dynamic Prompt Rewriting transforms vague requests into precise, actionable prompts by:
- Automatically identifying output deficiencies
- Iteratively improving prompt clarity
- Learning from successful rewrites
- Ensuring outputs meet specific criteria

When combined with Visual Chain-of-Thought and Self-Consistency, it creates a self-improving system that consistently delivers high-quality results.