"""
DeepEval-enhanced reward functions for PyClarity.
Integrates DeepEval's pre-built metrics with reward-kit framework.
"""

import json
import re
from typing import Any, Dict, List, Optional, Union

from deepeval.metrics import (
    AnswerRelevancyMetric,
    BiasMetric,
    FaithfulnessMetric,
    GEval,
    HallucinationMetric,
    ToxicityMetric,
)
from deepeval.test_case import LLMTestCase, LLMTestCaseParams
from reward_kit import EvaluateResult, MetricResult, reward_function
from reward_kit.models import Message


def extract_content(messages: list[Message] | list[dict[str, Any]]) -> tuple[str, str]:
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
    messages: list[Message] | list[dict[str, Any]],
    ground_truth: dict[str, Any] | None = None,
    **kwargs,
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
            score=0.5, reason="No context provided for hallucination check", metrics={}
        )

    # Create DeepEval test case
    test_case = LLMTestCase(
        input=user_input,
        actual_output=assistant_output,
        context=context if isinstance(context, list) else [context],
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
                    score=reward_score, success=reward_score >= 0.7, reason=metric.reason
                )
            },
        )
    except Exception as e:
        return EvaluateResult(score=0.0, reason=f"Error in hallucination check: {e!s}", metrics={})


@reward_function
def factual_consistency_reward(
    messages: list[Message] | list[dict[str, Any]],
    ground_truth: dict[str, Any] | None = None,
    **kwargs,
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
        return EvaluateResult(score=0.5, reason="No retrieval context provided", metrics={})

    test_case = LLMTestCase(
        input=user_input,
        actual_output=assistant_output,
        retrieval_context=retrieval_context
        if isinstance(retrieval_context, list)
        else [retrieval_context],
    )

    metric = FaithfulnessMetric(threshold=0.8)

    try:
        metric.measure(test_case)

        return EvaluateResult(
            score=metric.score,
            reason=f"Faithfulness: {metric.reason}",
            metrics={
                "faithfulness": MetricResult(
                    score=metric.score, success=metric.is_successful(), reason=metric.reason
                )
            },
        )
    except Exception as e:
        return EvaluateResult(score=0.0, reason=f"Error in faithfulness check: {e!s}", metrics={})


@reward_function
def safety_reward(
    messages: list[Message] | list[dict[str, Any]],
    ground_truth: dict[str, Any] | None = None,
    **kwargs,
) -> EvaluateResult:
    """
    Evaluate output safety using toxicity and bias metrics.
    """
    user_input, assistant_output = extract_content(messages)

    test_case = LLMTestCase(input=user_input, actual_output=assistant_output)

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
            reason=f"Toxicity level: {toxicity_metric.score:.2%}",
        )
        reasons.append(f"Toxicity: {toxicity_metric.reason}")
    except (ValueError, RuntimeError, AttributeError) as e:
        scores["toxicity_free"] = MetricResult(score=0.0, success=False, reason=f"Error: {e!s}")

    # Check bias
    try:
        bias_metric.measure(test_case)
        # Invert score (low bias = high reward)
        bias_reward = 1.0 - bias_metric.score
        scores["bias_free"] = MetricResult(
            score=bias_reward,
            success=bias_reward >= 0.9,
            reason=f"Bias level: {bias_metric.score:.2%}",
        )
        reasons.append(f"Bias: {bias_metric.reason}")
    except Exception as e:
        scores["bias_free"] = MetricResult(score=0.0, success=False, reason=f"Error: {e!s}")

    # Combined safety score
    overall_score = sum(m.score for m in scores.values()) / len(scores) if scores else 0.0

    return EvaluateResult(score=overall_score, reason=" | ".join(reasons), metrics=scores)


@reward_function
def answer_quality_reward(
    messages: list[Message] | list[dict[str, Any]],
    ground_truth: dict[str, Any] | None = None,
    **kwargs,
) -> EvaluateResult:
    """
    Evaluate answer quality using relevancy metric.
    """
    user_input, assistant_output = extract_content(messages)

    test_case = LLMTestCase(input=user_input, actual_output=assistant_output)

    metric = AnswerRelevancyMetric(threshold=0.7)

    try:
        metric.measure(test_case)

        return EvaluateResult(
            score=metric.score,
            reason=f"Answer relevancy: {metric.reason}",
            metrics={
                "relevancy": MetricResult(
                    score=metric.score, success=metric.is_successful(), reason=metric.reason
                )
            },
        )
    except Exception as e:
        return EvaluateResult(score=0.0, reason=f"Error in relevancy check: {e!s}", metrics={})


@reward_function
def custom_criteria_reward(
    messages: list[Message] | list[dict[str, Any]],
    ground_truth: dict[str, Any] | None = None,
    criteria: str = "correctness",
    **kwargs,
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
        """,
        "code_correctness": """
            Evaluate the correctness of any code in the response.
            Consider: syntax validity, logic accuracy, best practices, and error handling.
        """,
        "user_experience_quality": """
            Assess how well the solution addresses user experience concerns.
            Consider: ease of use, intuitiveness, accessibility, and user satisfaction.
        """,
    }

    # Get criteria prompt
    criteria_prompt = criteria_prompts.get(criteria, criteria)

    # Create test case
    test_case = LLMTestCase(input=user_input, actual_output=assistant_output)

    # Initialize G-Eval with custom criteria
    g_eval = GEval(
        name=f"custom_{criteria}",
        criteria=criteria_prompt,
        threshold=0.7,
        evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
    )

    try:
        g_eval.measure(test_case)

        return EvaluateResult(
            score=g_eval.score,
            reason=f"{criteria.title()}: {g_eval.reason}",
            metrics={
                criteria: MetricResult(
                    score=g_eval.score, success=g_eval.is_successful(), reason=g_eval.reason
                )
            },
        )
    except Exception as e:
        return EvaluateResult(score=0.0, reason=f"Error in G-Eval: {e!s}", metrics={})


@reward_function
def feature_quality_deepeval_reward(
    messages: list[Message] | list[dict[str, Any]],
    ground_truth: dict[str, Any] | None = None,
    **kwargs,
) -> EvaluateResult:
    """
    Evaluate PyClarity features using DeepEval metrics.
    """
    user_input, assistant_output = extract_content(messages)

    # Parse features from output
    try:
        json_match = re.search(r"\{[\s\S]*\}", assistant_output)
        if json_match:
            features = json.loads(json_match.group())
        else:
            return EvaluateResult(score=0.0, reason="No valid JSON features found", metrics={})
    except Exception as e:
        return EvaluateResult(score=0.0, reason=f"Failed to parse features: {e!s}", metrics={})

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
        actual_output=combined_descriptions,
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
            reason=f"Content safety: {toxicity_score:.2%}",
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
            score=bias_score, success=bias_score >= 0.95, reason=f"Bias-free: {bias_score:.2%}"
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
        threshold=0.7,
    )

    try:
        technical_eval.measure(test_case)
        metrics["technical_quality"] = MetricResult(
            score=technical_eval.score,
            success=technical_eval.is_successful(),
            reason=technical_eval.reason,
        )
        scores.append(technical_eval.score)
    except:
        pass

    # Calculate overall score
    overall_score = sum(scores) / len(scores) if scores else 0.0

    return EvaluateResult(
        score=overall_score, reason="Feature quality evaluation (DeepEval)", metrics=metrics
    )


def create_deepeval_enhanced_evaluator(
    weights: dict[str, float] | None = None,
    include_safety: bool = True,
    custom_criteria: list[str] | None = None,
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
            "custom": 0.25,
        }

    @reward_function
    def deepeval_comprehensive_evaluator(
        messages: list[Message] | list[dict[str, Any]],
        ground_truth: dict[str, Any] | None = None,
        **kwargs,
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
                    criteria, MetricResult(score=criteria_result.score, success=True, reason="")
                )
                custom_scores.append(criteria_result.score)

            # Average custom scores
            if custom_scores:
                avg_custom = sum(custom_scores) / len(custom_scores)
                all_results["custom"] = EvaluateResult(
                    score=avg_custom, reason="Custom criteria evaluation", metrics={}
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
        for criteria in custom_criteria or []:
            if criteria in all_metrics and all_metrics[criteria].score < 0.7:
                suggestions.append(f"Improve {criteria.replace('_', ' ')}")

        return EvaluateResult(
            score=overall_score,
            reason=f"DeepEval comprehensive evaluation: {overall_score:.2%}",
            metrics=all_metrics,
            metadata={
                "suggestions": suggestions,
                "component_scores": {k: v.score for k, v in all_results.items()},
            },
        )

    return deepeval_comprehensive_evaluator


# PyClarity-specific evaluators combining both frameworks
def create_pyclarity_deepeval_evaluator():
    """
    Create an evaluator specifically for PyClarity feature optimization
    that combines DeepEval metrics with PyClarity-specific criteria.
    """

    @reward_function
    def pyclarity_feature_evaluator(
        messages: list[Message] | list[dict[str, Any]],
        ground_truth: dict[str, Any] | None = None,
        **kwargs,
    ) -> EvaluateResult:
        """Evaluate PyClarity features with DeepEval metrics."""
        # Import PyClarity rewards
        from pyclarity_rewards import (
            feature_clarity_reward,
            feature_completeness_reward,
            feature_feasibility_reward,
            feature_innovation_reward,
            feature_user_value_reward,
        )

        # Run PyClarity-specific evaluations
        completeness = feature_completeness_reward(messages, ground_truth, **kwargs)
        clarity = feature_clarity_reward(messages, ground_truth, **kwargs)
        innovation = feature_innovation_reward(messages, ground_truth, **kwargs)
        feasibility = feature_feasibility_reward(messages, ground_truth, **kwargs)
        user_value = feature_user_value_reward(messages, ground_truth, **kwargs)

        # Run DeepEval quality check
        deepeval_quality = feature_quality_deepeval_reward(messages, ground_truth, **kwargs)

        # Combine metrics
        all_metrics = {}
        all_metrics.update(completeness.metrics)
        all_metrics.update(clarity.metrics)
        all_metrics.update(innovation.metrics)
        all_metrics.update(feasibility.metrics)
        all_metrics.update(user_value.metrics)
        all_metrics.update(deepeval_quality.metrics)

        # Weighted combination
        weights = {
            "completeness": 0.15,
            "clarity": 0.15,
            "innovation": 0.15,
            "feasibility": 0.20,
            "user_value": 0.25,
            "deepeval_quality": 0.10,
        }

        overall_score = (
            completeness.score * weights["completeness"]
            + clarity.score * weights["clarity"]
            + innovation.score * weights["innovation"]
            + feasibility.score * weights["feasibility"]
            + user_value.score * weights["user_value"]
            + deepeval_quality.score * weights["deepeval_quality"]
        )

        # Generate comprehensive suggestions
        suggestions = []

        if completeness.score < 0.7:
            suggestions.append("Add more features to under-represented categories")
        if clarity.score < 0.7:
            suggestions.append("Improve feature descriptions with specific use cases")
        if innovation.score < 0.5:
            suggestions.append("Add more AI-powered or innovative features")
        if feasibility.score < 0.6:
            suggestions.append("Reduce technical complexity of high-risk features")
        if user_value.score < 0.7:
            suggestions.append("Focus on features that deliver direct user value")
        if deepeval_quality.score < 0.8:
            suggestions.append("Ensure feature descriptions are safe and technically sound")

        return EvaluateResult(
            score=overall_score,
            reason=f"PyClarity + DeepEval evaluation: {overall_score:.2%}",
            metrics=all_metrics,
            metadata={
                "suggestions": suggestions,
                "framework": "PyClarity + DeepEval",
                "component_scores": {
                    "completeness": completeness.score,
                    "clarity": clarity.score,
                    "innovation": innovation.score,
                    "feasibility": feasibility.score,
                    "user_value": user_value.score,
                    "deepeval_quality": deepeval_quality.score,
                },
            },
        )

    return pyclarity_feature_evaluator
