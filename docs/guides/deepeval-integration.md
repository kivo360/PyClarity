# DeepEval + Reward-Kit Integration Guide

## Overview

This guide demonstrates how to integrate DeepEval's pre-built evaluation metrics with reward-kit to create sophisticated reward functions for LLM optimization. By combining DeepEval's research-backed metrics with reward-kit's flexible framework, we can create better rewards that improve both prompts and models.

## Key Benefits of Integration

1. **Research-Backed Metrics**: DeepEval provides metrics based on latest research (G-Eval, RAGAS, etc.)
2. **Hallucination Detection**: Built-in metrics for factual consistency and faithfulness
3. **Safety Evaluation**: Bias and toxicity detection out of the box
4. **Custom Criteria**: G-Eval allows natural language evaluation criteria
5. **Production Ready**: Both frameworks support deployment and scaling

## Installation

```bash
# Install both frameworks
uv add "reward-kit[trl]"
uv add deepeval
```

## Architecture Overview

```
┌─────────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   LLM Optimizer     │────▶│  Reward-Kit      │────▶│    DeepEval     │
│  (PyClarity)        │     │  @reward_function│     │   BaseMetric    │
└─────────────────────┘     └──────────────────┘     └─────────────────┘
         │                           │                         │
         │                           ▼                         ▼
         │                    ┌──────────────┐         ┌─────────────┐
         └───────────────────▶│ EvaluateResult│◀────────│ Metric Score│
                              └──────────────┘         └─────────────┘
```

## Implementation: DeepEval-Enhanced Reward Functions

### 1. Base Integration Pattern

```python
# experiment/deepeval_rewards.py
"""
DeepEval-enhanced reward functions for PyClarity.
"""

from typing import Any, Dict, List, Optional, Union
from reward_kit import reward_function, EvaluateResult, MetricResult
from reward_kit.models import Message
from deepeval.test_case import LLMTestCase
from deepeval.metrics import (
    HallucinationMetric,
    FaithfulnessMetric,
    ToxicityMetric,
    BiasMetric,
    AnswerRelevancyMetric,
    GEval
)
import json
import re


def extract_content(messages: Union[List[Message], List[Dict[str, Any]]]) -> tuple[str, str]:
    """Extract input and output from messages."""
    if not messages:
        return "", ""
    
    # Get the user input (usually first message)
    user_input = ""
    for msg in messages:
        content = msg.get("content", "") if isinstance(msg, dict) else (msg.content or "")
        role = msg.get("role", "") if isinstance(msg, dict) else (msg.role or "")
        if role == "user":
            user_input = content
            break
    
    # Get the assistant output (last assistant message)
    assistant_output = ""
    for msg in reversed(messages):
        content = msg.get("content", "") if isinstance(msg, dict) else (msg.content or "")
        role = msg.get("role", "") if isinstance(msg, dict) else (msg.role or "")
        if role == "assistant":
            assistant_output = content
            break
    
    return user_input, assistant_output


@reward_function
def hallucination_free_reward(
    messages: Union[List[Message], List[Dict[str, Any]]],
    ground_truth: Optional[Dict[str, Any]] = None,
    **kwargs
) -> EvaluateResult:
    """
    Evaluate if the output is free from hallucinations using DeepEval.
    """
    user_input, assistant_output = extract_content(messages)
    
    # Extract context if provided
    context = kwargs.get("context", [])
    if ground_truth and "context" in ground_truth:
        context = ground_truth["context"]
    
    if not context:
        # If no context provided, use faithfulness metric instead
        return EvaluateResult(
            score=0.5,
            reason="No context provided for hallucination check",
            metrics={}
        )
    
    # Create DeepEval test case
    test_case = LLMTestCase(
        input=user_input,
        actual_output=assistant_output,
        context=context if isinstance(context, list) else [context]
    )
    
    # Use DeepEval's HallucinationMetric
    metric = HallucinationMetric(threshold=0.7)
    
    try:
        metric.measure(test_case)
        
        # Convert to reward (higher score = less hallucination)
        reward_score = 1.0 - metric.score  # Invert because hallucination is bad
        
        return EvaluateResult(
            score=reward_score,
            reason=f"Hallucination check: {metric.reason}",
            metrics={
                "hallucination_free": MetricResult(
                    score=reward_score,
                    success=reward_score >= 0.7,
                    reason=metric.reason
                )
            }
        )
    except Exception as e:
        return EvaluateResult(
            score=0.0,
            reason=f"Error in hallucination check: {str(e)}",
            metrics={}
        )


@reward_function
def factual_consistency_reward(
    messages: Union[List[Message], List[Dict[str, Any]]],
    ground_truth: Optional[Dict[str, Any]] = None,
    **kwargs
) -> EvaluateResult:
    """
    Evaluate factual consistency using DeepEval's FaithfulnessMetric.
    Better for RAG systems than HallucinationMetric.
    """
    user_input, assistant_output = extract_content(messages)
    
    # Extract retrieval context
    retrieval_context = kwargs.get("retrieval_context", [])
    if ground_truth and "retrieval_context" in ground_truth:
        retrieval_context = ground_truth["retrieval_context"]
    
    if not retrieval_context:
        return EvaluateResult(
            score=0.5,
            reason="No retrieval context provided",
            metrics={}
        )
    
    test_case = LLMTestCase(
        input=user_input,
        actual_output=assistant_output,
        retrieval_context=retrieval_context if isinstance(retrieval_context, list) else [retrieval_context]
    )
    
    metric = FaithfulnessMetric(threshold=0.8)
    
    try:
        metric.measure(test_case)
        
        return EvaluateResult(
            score=metric.score,
            reason=f"Faithfulness: {metric.reason}",
            metrics={
                "faithfulness": MetricResult(
                    score=metric.score,
                    success=metric.is_successful(),
                    reason=metric.reason
                )
            }
        )
    except Exception as e:
        return EvaluateResult(
            score=0.0,
            reason=f"Error in faithfulness check: {str(e)}",
            metrics={}
        )


@reward_function
def safety_reward(
    messages: Union[List[Message], List[Dict[str, Any]]],
    ground_truth: Optional[Dict[str, Any]] = None,
    **kwargs
) -> EvaluateResult:
    """
    Evaluate output safety using toxicity and bias metrics.
    """
    user_input, assistant_output = extract_content(messages)
    
    test_case = LLMTestCase(
        input=user_input,
        actual_output=assistant_output
    )
    
    # Initialize metrics
    toxicity_metric = ToxicityMetric(threshold=0.1)  # Low threshold for toxicity
    bias_metric = BiasMetric(threshold=0.1)  # Low threshold for bias
    
    scores = {}
    reasons = []
    
    # Check toxicity
    try:
        toxicity_metric.measure(test_case)
        # Invert score (low toxicity = high reward)
        toxicity_reward = 1.0 - toxicity_metric.score
        scores["toxicity_free"] = MetricResult(
            score=toxicity_reward,
            success=toxicity_reward >= 0.9,
            reason=f"Toxicity level: {toxicity_metric.score:.2%}"
        )
        reasons.append(f"Toxicity: {toxicity_metric.reason}")
    except Exception as e:
        scores["toxicity_free"] = MetricResult(
            score=0.0,
            success=False,
            reason=f"Error: {str(e)}"
        )
    
    # Check bias
    try:
        bias_metric.measure(test_case)
        # Invert score (low bias = high reward)
        bias_reward = 1.0 - bias_metric.score
        scores["bias_free"] = MetricResult(
            score=bias_reward,
            success=bias_reward >= 0.9,
            reason=f"Bias level: {bias_metric.score:.2%}"
        )
        reasons.append(f"Bias: {bias_metric.reason}")
    except Exception as e:
        scores["bias_free"] = MetricResult(
            score=0.0,
            success=False,
            reason=f"Error: {str(e)}"
        )
    
    # Combined safety score
    overall_score = sum(m.score for m in scores.values()) / len(scores) if scores else 0.0
    
    return EvaluateResult(
        score=overall_score,
        reason=" | ".join(reasons),
        metrics=scores
    )


@reward_function
def answer_quality_reward(
    messages: Union[List[Message], List[Dict[str, Any]]],
    ground_truth: Optional[Dict[str, Any]] = None,
    **kwargs
) -> EvaluateResult:
    """
    Evaluate answer quality using relevancy metric.
    """
    user_input, assistant_output = extract_content(messages)
    
    test_case = LLMTestCase(
        input=user_input,
        actual_output=assistant_output
    )
    
    metric = AnswerRelevancyMetric(threshold=0.7)
    
    try:
        metric.measure(test_case)
        
        return EvaluateResult(
            score=metric.score,
            reason=f"Answer relevancy: {metric.reason}",
            metrics={
                "relevancy": MetricResult(
                    score=metric.score,
                    success=metric.is_successful(),
                    reason=metric.reason
                )
            }
        )
    except Exception as e:
        return EvaluateResult(
            score=0.0,
            reason=f"Error in relevancy check: {str(e)}",
            metrics={}
        )
```

### 2. Custom G-Eval Integration

```python
@reward_function
def custom_criteria_reward(
    messages: Union[List[Message], List[Dict[str, Any]]],
    ground_truth: Optional[Dict[str, Any]] = None,
    criteria: str = "correctness",
    **kwargs
) -> EvaluateResult:
    """
    Use G-Eval for custom evaluation criteria defined in natural language.
    """
    user_input, assistant_output = extract_content(messages)
    
    # Define custom evaluation criteria
    criteria_prompts = {
        "technical_accuracy": """
            Evaluate if the technical details in the response are accurate and well-explained.
            Consider: code correctness, technical terminology usage, and conceptual accuracy.
        """,
        "innovation": """
            Assess the level of innovation and creativity in the response.
            Consider: novel approaches, creative solutions, and thinking outside the box.
        """,
        "practicality": """
            Evaluate how practical and implementable the suggested solution is.
            Consider: feasibility, resource requirements, and real-world applicability.
        """,
        "completeness": """
            Assess if the response fully addresses all aspects of the query.
            Consider: coverage of edge cases, comprehensive explanation, and thoroughness.
        """
    }
    
    # Get criteria prompt
    criteria_prompt = criteria_prompts.get(criteria, criteria)
    
    # Create test case
    test_case = LLMTestCase(
        input=user_input,
        actual_output=assistant_output
    )
    
    # Initialize G-Eval with custom criteria
    g_eval = GEval(
        name=f"custom_{criteria}",
        criteria=criteria_prompt,
        threshold=0.7,
        evaluation_params=[
            LLMTestCaseParams.INPUT,
            LLMTestCaseParams.ACTUAL_OUTPUT
        ]
    )
    
    try:
        g_eval.measure(test_case)
        
        return EvaluateResult(
            score=g_eval.score,
            reason=f"{criteria.title()}: {g_eval.reason}",
            metrics={
                criteria: MetricResult(
                    score=g_eval.score,
                    success=g_eval.is_successful(),
                    reason=g_eval.reason
                )
            }
        )
    except Exception as e:
        return EvaluateResult(
            score=0.0,
            reason=f"Error in G-Eval: {str(e)}",
            metrics={}
        )
```

### 3. PyClarity Feature Evaluation with DeepEval

```python
@reward_function
def feature_quality_deepeval_reward(
    messages: Union[List[Message], List[Dict[str, Any]]],
    ground_truth: Optional[Dict[str, Any]] = None,
    **kwargs
) -> EvaluateResult:
    """
    Evaluate PyClarity features using DeepEval metrics.
    """
    user_input, assistant_output = extract_content(messages)
    
    # Parse features from output
    try:
        json_match = re.search(r'\{[\s\S]*\}', assistant_output)
        if json_match:
            features = json.loads(json_match.group())
        else:
            return EvaluateResult(
                score=0.0,
                reason="No valid JSON features found",
                metrics={}
            )
    except Exception as e:
        return EvaluateResult(
            score=0.0,
            reason=f"Failed to parse features: {str(e)}",
            metrics={}
        )
    
    # Prepare feature descriptions for evaluation
    all_descriptions = []
    for category, feature_list in features.items():
        for feature in feature_list:
            if isinstance(feature, dict):
                desc = feature.get("description", "")
                if desc:
                    all_descriptions.append(desc)
    
    combined_descriptions = "\n".join(all_descriptions)
    
    # Create test case for evaluation
    test_case = LLMTestCase(
        input="Evaluate the quality of these feature descriptions",
        actual_output=combined_descriptions
    )
    
    metrics = {}
    scores = []
    
    # Check for toxicity in feature descriptions
    toxicity = ToxicityMetric(threshold=0.1)
    try:
        toxicity.measure(test_case)
        toxicity_score = 1.0 - toxicity.score
        metrics["safe_content"] = MetricResult(
            score=toxicity_score,
            success=toxicity_score >= 0.95,
            reason=f"Content safety: {toxicity_score:.2%}"
        )
        scores.append(toxicity_score)
    except:
        pass
    
    # Check for bias
    bias = BiasMetric(threshold=0.1)
    try:
        bias.measure(test_case)
        bias_score = 1.0 - bias.score
        metrics["unbiased"] = MetricResult(
            score=bias_score,
            success=bias_score >= 0.95,
            reason=f"Bias-free: {bias_score:.2%}"
        )
        scores.append(bias_score)
    except:
        pass
    
    # Use G-Eval for technical quality
    technical_eval = GEval(
        name="technical_quality",
        criteria="""
            Evaluate if the feature descriptions are technically sound and well-specified.
            Consider: clarity, specificity, technical accuracy, and implementation feasibility.
        """,
        threshold=0.7
    )
    
    try:
        technical_eval.measure(test_case)
        metrics["technical_quality"] = MetricResult(
            score=technical_eval.score,
            success=technical_eval.is_successful(),
            reason=technical_eval.reason
        )
        scores.append(technical_eval.score)
    except:
        pass
    
    # Calculate overall score
    overall_score = sum(scores) / len(scores) if scores else 0.0
    
    return EvaluateResult(
        score=overall_score,
        reason=f"Feature quality evaluation (DeepEval)",
        metrics=metrics
    )
```

### 4. Combined DeepEval + Reward-Kit Evaluator

```python
def create_deepeval_enhanced_evaluator(
    weights: Optional[Dict[str, float]] = None,
    include_safety: bool = True,
    custom_criteria: Optional[List[str]] = None
):
    """
    Create a comprehensive evaluator combining DeepEval metrics with reward-kit.
    
    Args:
        weights: Weight for each evaluation component
        include_safety: Whether to include safety checks
        custom_criteria: List of custom G-Eval criteria to include
    """
    if weights is None:
        weights = {
            "hallucination_free": 0.25,
            "answer_quality": 0.30,
            "safety": 0.20,
            "custom": 0.25
        }
    
    @reward_function
    def deepeval_comprehensive_evaluator(
        messages: Union[List[Message], List[Dict[str, Any]]],
        ground_truth: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> EvaluateResult:
        """Comprehensive evaluation using DeepEval metrics."""
        
        all_results = {}
        all_metrics = {}
        
        # Run hallucination check if context available
        if kwargs.get("context") or (ground_truth and "context" in ground_truth):
            hallucination_result = hallucination_free_reward(messages, ground_truth, **kwargs)
            all_results["hallucination_free"] = hallucination_result
            all_metrics.update(hallucination_result.metrics)
        
        # Run answer quality check
        quality_result = answer_quality_reward(messages, ground_truth, **kwargs)
        all_results["answer_quality"] = quality_result
        all_metrics.update(quality_result.metrics)
        
        # Run safety checks if enabled
        if include_safety:
            safety_result = safety_reward(messages, ground_truth, **kwargs)
            all_results["safety"] = safety_result
            all_metrics.update(safety_result.metrics)
        
        # Run custom criteria if provided
        if custom_criteria:
            custom_scores = []
            for criteria in custom_criteria:
                criteria_result = custom_criteria_reward(
                    messages, ground_truth, criteria=criteria, **kwargs
                )
                all_metrics[criteria] = criteria_result.metrics.get(
                    criteria, 
                    MetricResult(score=criteria_result.score, success=True, reason="")
                )
                custom_scores.append(criteria_result.score)
            
            # Average custom scores
            if custom_scores:
                avg_custom = sum(custom_scores) / len(custom_scores)
                all_results["custom"] = EvaluateResult(
                    score=avg_custom,
                    reason="Custom criteria evaluation",
                    metrics={}
                )
        
        # Calculate weighted overall score
        total_weight = 0
        weighted_sum = 0
        
        for component, result in all_results.items():
            weight = weights.get(component, 0.0)
            if weight > 0:
                weighted_sum += result.score * weight
                total_weight += weight
        
        overall_score = weighted_sum / total_weight if total_weight > 0 else 0.0
        
        # Generate improvement suggestions
        suggestions = []
        
        # Check each component for improvement areas
        if "hallucination_free" in all_results and all_results["hallucination_free"].score < 0.7:
            suggestions.append("Improve factual accuracy and reduce hallucinations")
        
        if "answer_quality" in all_results and all_results["answer_quality"].score < 0.7:
            suggestions.append("Enhance answer relevancy and completeness")
        
        if "safety" in all_results and all_results["safety"].score < 0.8:
            suggestions.append("Address potential bias or toxicity issues")
        
        # Custom criteria suggestions
        for criteria in (custom_criteria or []):
            if criteria in all_metrics and all_metrics[criteria].score < 0.7:
                suggestions.append(f"Improve {criteria.replace('_', ' ')}")
        
        return EvaluateResult(
            score=overall_score,
            reason=f"DeepEval comprehensive evaluation: {overall_score:.2%}",
            metrics=all_metrics,
            metadata={
                "suggestions": suggestions,
                "component_scores": {k: v.score for k, v in all_results.items()}
            }
        )
    
    return deepeval_comprehensive_evaluator
```

## Integration with PyClarity Optimizer

### 1. Updated Optimizer with DeepEval

```python
# experiment/llm_optimizer_deepeval_enhanced.py
"""
PyClarity optimizer enhanced with DeepEval metrics.
"""

from pathlib import Path
from typing import Any, Dict, List
import json
import time
from datetime import datetime

from groq import Groq
from loguru import logger

# Import both reward-kit and DeepEval enhanced rewards
from pyclarity_rewards import create_combined_evaluator
from deepeval_rewards import create_deepeval_enhanced_evaluator


class DeepEvalEnhancedOptimizer:
    """LLM Optimizer with DeepEval-powered evaluation."""
    
    def __init__(self, use_deepeval: bool = True):
        self.iteration = 0
        self.feature_list = {}
        self.improvement_history = []
        self.client = Groq()
        
        # Choose evaluator
        if use_deepeval:
            # Use DeepEval-enhanced evaluator
            self.evaluator = create_deepeval_enhanced_evaluator(
                weights={
                    "hallucination_free": 0.20,
                    "answer_quality": 0.30,
                    "safety": 0.15,
                    "custom": 0.35
                },
                include_safety=True,
                custom_criteria=["technical_accuracy", "innovation", "completeness"]
            )
            logger.info("Using DeepEval-enhanced evaluator")
        else:
            # Use original reward-kit evaluator
            self.evaluator = create_combined_evaluator()
            logger.info("Using standard reward-kit evaluator")
        
        # Create directories
        Path("history").mkdir(exist_ok=True)
        Path("evaluations").mkdir(exist_ok=True)
    
    def evaluate_features_with_deepeval(
        self, 
        features: Dict[str, List[Dict[str, Any]]],
        context: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Evaluate features using DeepEval metrics.
        """
        # Create comprehensive prompt
        evaluation_prompt = f"""
You are evaluating an AI-powered UI generation tool with the following features:

{json.dumps(features, indent=2)}

Provide a comprehensive analysis of these features considering:
1. Technical feasibility and implementation clarity
2. Innovation and differentiation from existing solutions
3. Practical value to end users
4. Completeness of the feature set

Your evaluation will be used to improve the features in the next iteration.
"""
        
        # Convert to messages format
        messages = [
            {"role": "user", "content": evaluation_prompt},
            {"role": "assistant", "content": json.dumps(features, indent=2)}
        ]
        
        # Add context if available (for hallucination checking)
        kwargs = {}
        if context:
            kwargs["context"] = context
        
        # Run evaluation
        result = self.evaluator(messages, **kwargs)
        
        # Extract component scores for detailed analysis
        component_scores = {}
        if hasattr(result, 'metadata') and 'component_scores' in result.metadata:
            component_scores = result.metadata['component_scores']
        
        # Convert to optimizer format
        evaluation_result = {
            "overall_score": result.score,
            "scores": {
                metric_name: metric_result.score 
                for metric_name, metric_result in result.metrics.items()
            },
            "detailed_feedback": {
                metric_name: metric_result.reason
                for metric_name, metric_result in result.metrics.items()
            },
            "suggestions": result.metadata.get("suggestions", []) if hasattr(result, 'metadata') else [],
            "component_scores": component_scores,
            "deepeval_result": result
        }
        
        return evaluation_result
    
    def generate_improvement_prompt(self, evaluation_result: Dict[str, Any]) -> str:
        """
        Generate targeted improvement prompt based on DeepEval feedback.
        """
        suggestions = evaluation_result.get("suggestions", [])
        component_scores = evaluation_result.get("component_scores", {})
        
        # Identify weakest areas
        weak_areas = []
        if component_scores:
            sorted_components = sorted(
                component_scores.items(), 
                key=lambda x: x[1]
            )
            weak_areas = [comp for comp, score in sorted_components if score < 0.7]
        
        improvement_focus = ""
        if weak_areas:
            improvement_focus = f"""
Priority improvement areas based on DeepEval analysis:
{chr(10).join(f"- {area.replace('_', ' ').title()}: Needs significant improvement" for area in weak_areas)}
"""
        
        return f"""Based on comprehensive DeepEval evaluation, improve the features with focus on:

{improvement_focus}

Specific suggestions:
{chr(10).join(f"- {s}" for s in suggestions)}

DeepEval Scores:
- Overall: {evaluation_result['overall_score']:.2%}
- Component scores: {json.dumps(component_scores, indent=2)}

Generate improved features that address these specific issues while maintaining strengths.
"""
    
    def run_optimization_loop(self, max_iterations: int = 5):
        """
        Run optimization loop with DeepEval metrics.
        """
        logger.info(f"Starting DeepEval-Enhanced Optimization (max {max_iterations} iterations)")
        
        # Load any relevant documentation as context
        context_docs = self._load_context_documents()
        
        while self.iteration < max_iterations:
            start_time = time.time()
            self.iteration += 1
            
            logger.info(f"\n{'=' * 60}")
            logger.info(f"Iteration {self.iteration} - DeepEval Enhanced")
            logger.info(f"{'=' * 60}")
            
            # Generate features
            features = self._generate_features()
            
            # Evaluate with DeepEval
            evaluation_result = self.evaluate_features_with_deepeval(
                features, 
                context=context_docs
            )
            
            # Log detailed DeepEval results
            self._log_deepeval_results(evaluation_result)
            
            # Optimize based on DeepEval feedback
            improvement_prompt = self.generate_improvement_prompt(evaluation_result)
            self.feature_list = self._optimize_features(features, improvement_prompt)
            
            # Save results
            iteration_time = time.time() - start_time
            self._save_iteration_results(evaluation_result, iteration_time)
            
            # Check convergence
            if self._has_converged():
                logger.info("Optimization converged!")
                break
            
            # Sleep between iterations
            if self.iteration < max_iterations:
                logger.info("\n💤 Sleeping for 10 seconds...")
                time.sleep(10)
        
        self._generate_final_report()
    
    def _log_deepeval_results(self, evaluation_result: Dict[str, Any]):
        """Log detailed DeepEval evaluation results."""
        logger.info("\n📊 DeepEval Evaluation Results:")
        logger.info(f"Overall Score: {evaluation_result['overall_score']:.2%}")
        
        if "component_scores" in evaluation_result:
            logger.info("\nComponent Scores:")
            for component, score in evaluation_result["component_scores"].items():
                emoji = "✅" if score >= 0.7 else "⚠️" if score >= 0.5 else "❌"
                logger.info(f"  {emoji} {component}: {score:.2%}")
        
        logger.info("\nDetailed Metrics:")
        for metric, score in evaluation_result["scores"].items():
            logger.info(f"  • {metric}: {score:.2%}")
        
        if evaluation_result.get("suggestions"):
            logger.info("\n💡 Improvement Suggestions:")
            for suggestion in evaluation_result["suggestions"]:
                logger.info(f"  → {suggestion}")
    
    def _load_context_documents(self) -> List[str]:
        """Load documentation for context (hallucination checking)."""
        context = []
        docs_path = Path("../docs/ai-prompting-techniques")
        
        if docs_path.exists():
            for doc_file in docs_path.glob("*.md"):
                try:
                    with open(doc_file, encoding="utf-8") as f:
                        content = f.read()
                        context.append(f"File: {doc_file.name}\n{content[:1000]}")
                except:
                    pass
        
        return context[:5]  # Limit context size
    
    def _generate_final_report(self):
        """Generate comprehensive report with DeepEval insights."""
        report = {
            "optimization_summary": {
                "total_iterations": self.iteration,
                "evaluation_framework": "DeepEval + Reward-Kit",
                "final_score": self.improvement_history[-1]["quality_score"] if self.improvement_history else 0
            },
            "deepeval_insights": {
                "hallucination_free": [],
                "safety_scores": [],
                "quality_progression": []
            },
            "improvement_trajectory": self.improvement_history,
            "final_features": self.feature_list
        }
        
        # Extract DeepEval-specific insights
        for hist in self.improvement_history:
            if "component_scores" in hist:
                scores = hist["component_scores"]
                if "hallucination_free" in scores:
                    report["deepeval_insights"]["hallucination_free"].append({
                        "iteration": hist["iteration"],
                        "score": scores["hallucination_free"]
                    })
                if "safety" in scores:
                    report["deepeval_insights"]["safety_scores"].append({
                        "iteration": hist["iteration"],
                        "score": scores["safety"]
                    })
        
        # Save report
        with open("evaluations/deepeval_optimization_report.json", "w") as f:
            json.dump(report, f, indent=2)
        
        logger.info("\n📝 Final report saved to evaluations/deepeval_optimization_report.json")
    
    # ... (implement other helper methods)
```

## Usage Examples

### 1. Basic DeepEval Reward Function

```python
# Test individual DeepEval reward functions
from deepeval_rewards import hallucination_free_reward, safety_reward

# Test messages
messages = [
    {"role": "user", "content": "What is the capital of France?"},
    {"role": "assistant", "content": "The capital of France is Paris."}
]

# With context for hallucination check
context = ["France is a country in Europe. Its capital city is Paris."]

# Test hallucination reward
result = hallucination_free_reward(messages, context=context)
print(f"Hallucination-free score: {result.score:.2%}")
print(f"Reason: {result.reason}")

# Test safety reward
safety_result = safety_reward(messages)
print(f"Safety score: {safety_result.score:.2%}")
```

### 2. Running the Enhanced Optimizer

```python
# Run optimizer with DeepEval
optimizer = DeepEvalEnhancedOptimizer(use_deepeval=True)
optimizer.run_optimization_loop(max_iterations=5)

# Compare with standard reward-kit
standard_optimizer = DeepEvalEnhancedOptimizer(use_deepeval=False)
standard_optimizer.run_optimization_loop(max_iterations=5)
```

### 3. Custom G-Eval Criteria

```python
# Create custom evaluator for specific use case
custom_evaluator = create_deepeval_enhanced_evaluator(
    custom_criteria=[
        "user_experience_quality",
        "code_generation_accuracy",
        "architectural_soundness"
    ],
    weights={
        "hallucination_free": 0.15,
        "answer_quality": 0.25,
        "safety": 0.10,
        "custom": 0.50  # Emphasize custom criteria
    }
)
```

## Best Practices

### 1. Context Management
- Always provide context for hallucination checking
- Use retrieval_context for RAG systems
- Limit context size to avoid token limits

### 2. Safety First
- Always include safety checks for user-facing applications
- Set low thresholds for toxicity and bias (0.1 or lower)
- Log safety violations for monitoring

### 3. Custom Criteria
- Use G-Eval for domain-specific evaluation
- Write clear, specific criteria in natural language
- Test criteria prompts before deployment

### 4. Performance Optimization
- Cache DeepEval metric instances
- Use async evaluation when possible
- Batch evaluations for efficiency

### 5. Monitoring and Analysis
- Track component scores over iterations
- Identify persistent weak areas
- Use insights to guide model improvements

## Advanced Patterns

### 1. Multi-Stage Evaluation Pipeline

```python
class MultiStageEvaluator:
    """Pipeline with fast filters and detailed evaluation."""
    
    def __init__(self):
        self.safety_filter = safety_reward
        self.quality_evaluator = create_deepeval_enhanced_evaluator()
    
    def evaluate(self, messages):
        # Stage 1: Safety filter (fast)
        safety_result = self.safety_filter(messages)
        if safety_result.score < 0.8:
            return EvaluateResult(
                score=0.0,
                reason="Failed safety check",
                metrics=safety_result.metrics
            )
        
        # Stage 2: Comprehensive evaluation (slower)
        return self.quality_evaluator(messages)
```

### 2. Adaptive Evaluation

```python
def create_adaptive_evaluator():
    """Evaluator that adapts based on content type."""
    
    @reward_function
    def adaptive_evaluator(messages, **kwargs):
        content = extract_content(messages)[1]
        
        # Detect content type
        if "```" in content:  # Code content
            criteria = ["code_correctness", "documentation_quality"]
        elif len(content) > 1000:  # Long-form content
            criteria = ["completeness", "structure", "clarity"]
        else:  # Short response
            criteria = ["conciseness", "accuracy"]
        
        # Create appropriate evaluator
        evaluator = create_deepeval_enhanced_evaluator(
            custom_criteria=criteria
        )
        
        return evaluator(messages, **kwargs)
    
    return adaptive_evaluator
```

## Troubleshooting

### Common Issues

1. **API Key Errors**
   ```python
   # Set DeepEval API key if using cloud features
   import os
   os.environ["DEEPEVAL_API_KEY"] = "your-key"
   ```

2. **Model Compatibility**
   ```python
   # Specify evaluation model
   metric = HallucinationMetric(
       threshold=0.7,
       model="gpt-4"  # or local model
   )
   ```

3. **Context Size Limits**
   ```python
   # Chunk large contexts
   def chunk_context(context, max_tokens=2000):
       # Implementation to split context
       pass
   ```

## Conclusion

By integrating DeepEval with reward-kit, we get:

1. **Research-backed metrics** for reliable evaluation
2. **Safety checks** built into the reward system
3. **Flexible custom criteria** through G-Eval
4. **Production-ready** evaluation pipeline
5. **Better optimization** through targeted feedback

This integration enables PyClarity to optimize not just for feature quality, but also for safety, factual accuracy, and custom business criteria, leading to better prompts and improved model outputs.