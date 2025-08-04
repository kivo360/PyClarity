"""
PyClarity-specific reward functions using reward-kit framework.
"""

import json
import re
from typing import Any, Dict, List, Optional, Union

from reward_kit import reward_function, EvaluateResult, MetricResult
from reward_kit.models import Message


@reward_function
def feature_completeness_reward(
    messages: Union[List[Message], List[Dict[str, Any]]],
    ground_truth: Optional[Dict[str, Any]] = None,
    **kwargs
) -> EvaluateResult:
    """
    Evaluate feature completeness based on PyClarity criteria.
    """
    # Extract features from the last message
    if not messages:
        return EvaluateResult(
            score=0.0,
            reason="No messages provided",
            metrics={}
        )
    
    last_message = messages[-1]
    if isinstance(last_message, dict):
        content = last_message.get("content", "")
    else:
        content = last_message.content or ""
    
    # Parse features
    try:
        json_match = re.search(r'\{[\s\S]*\}', content)
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
    
    # Evaluation metrics
    metrics = {}
    
    # Check category coverage
    required_categories = ["core", "supporting", "integration", "analytics", "future"]
    present_categories = [cat for cat in required_categories if cat in features and features[cat]]
    category_score = len(present_categories) / len(required_categories)
    
    metrics["category_coverage"] = MetricResult(
        score=category_score,
        success=category_score >= 0.8,
        reason=f"Present: {', '.join(present_categories)}"
    )
    
    # Check feature counts
    min_features_per_category = {
        "core": 3,
        "supporting": 2,
        "integration": 1,
        "analytics": 1,
        "future": 1
    }
    
    feature_count_score = 0.0
    for category, min_count in min_features_per_category.items():
        if category in features:
            actual_count = len(features[category])
            if actual_count >= min_count:
                feature_count_score += 0.2
    
    metrics["feature_density"] = MetricResult(
        score=feature_count_score,
        success=feature_count_score >= 0.8,
        reason=f"Feature distribution score: {feature_count_score:.1%}"
    )
    
    # Overall score
    overall_score = (category_score * 0.6 + feature_count_score * 0.4)
    
    return EvaluateResult(
        score=overall_score,
        reason=f"Completeness: {overall_score:.1%}",
        metrics=metrics
    )


@reward_function
def feature_clarity_reward(
    messages: Union[List[Message], List[Dict[str, Any]]],
    ground_truth: Optional[Dict[str, Any]] = None,
    **kwargs
) -> EvaluateResult:
    """
    Evaluate clarity and quality of feature descriptions.
    """
    # Extract features
    last_message = messages[-1] if messages else None
    if not last_message:
        return EvaluateResult(score=0.0, reason="No messages", metrics={})
    
    content = last_message.get("content", "") if isinstance(last_message, dict) else (last_message.content or "")
    
    try:
        json_match = re.search(r'\{[\s\S]*\}', content)
        if json_match:
            features = json.loads(json_match.group())
        else:
            return EvaluateResult(score=0.0, reason="No features found", metrics={})
    except:
        return EvaluateResult(score=0.0, reason="Parse error", metrics={})
    
    # Evaluate clarity
    clarity_scores = []
    unclear_features = []
    
    for category, feature_list in features.items():
        for feature in feature_list:
            if not isinstance(feature, dict):
                continue
                
            desc = feature.get("description", "")
            name = feature.get("name", "Unknown")
            
            # Check description quality
            desc_score = 0.0
            if 20 <= len(desc) <= 200:
                desc_score += 0.5
            if any(word in desc.lower() for word in ["specific", "automated", "intelligent", "real-time"]):
                desc_score += 0.3
            if feature.get("user_value", 0) >= 7:
                desc_score += 0.2
                
            clarity_scores.append(desc_score)
            if desc_score < 0.7:
                unclear_features.append(name)
    
    avg_clarity = sum(clarity_scores) / len(clarity_scores) if clarity_scores else 0.0
    
    return EvaluateResult(
        score=avg_clarity,
        reason=f"Average clarity: {avg_clarity:.1%}",
        metrics={
            "clarity": MetricResult(
                score=avg_clarity,
                success=avg_clarity >= 0.7,
                reason=f"Unclear features: {', '.join(unclear_features[:3]) if unclear_features else 'None'}"
            )
        }
    )


@reward_function
def feature_innovation_reward(
    messages: Union[List[Message], List[Dict[str, Any]]],
    ground_truth: Optional[Dict[str, Any]] = None,
    **kwargs
) -> EvaluateResult:
    """
    Evaluate innovation and differentiation in features.
    """
    # Extract features
    last_message = messages[-1] if messages else None
    if not last_message:
        return EvaluateResult(score=0.0, reason="No messages", metrics={})
    
    content = last_message.get("content", "") if isinstance(last_message, dict) else (last_message.content or "")
    
    try:
        json_match = re.search(r'\{[\s\S]*\}', content)
        if json_match:
            features = json.loads(json_match.group())
        else:
            return EvaluateResult(score=0.0, reason="No features found", metrics={})
    except:
        return EvaluateResult(score=0.0, reason="Parse error", metrics={})
    
    # Innovation keywords
    innovative_keywords = [
        "ai-powered", "intelligent", "automated", "predictive",
        "adaptive", "self-", "machine learning", "neural",
        "revolutionary", "breakthrough", "novel", "unique",
        "real-time", "dynamic", "context-aware"
    ]
    
    innovation_count = 0
    innovative_features = []
    total_features = 0
    
    for category, feature_list in features.items():
        for feature in feature_list:
            if not isinstance(feature, dict):
                continue
                
            total_features += 1
            name = feature.get("name", "")
            desc = feature.get("description", "")
            combined_text = f"{name} {desc}".lower()
            
            if any(keyword in combined_text for keyword in innovative_keywords):
                innovation_count += 1
                innovative_features.append(name)
    
    innovation_ratio = innovation_count / total_features if total_features > 0 else 0
    
    # Target 30-50% innovative features
    if innovation_ratio < 0.3:
        score = innovation_ratio / 0.3
    elif innovation_ratio > 0.5:
        score = 1.0 - (innovation_ratio - 0.5) * 0.5
    else:
        score = 1.0
    
    return EvaluateResult(
        score=score,
        reason=f"Innovation ratio: {innovation_ratio:.1%}",
        metrics={
            "innovation": MetricResult(
                score=score,
                success=0.3 <= innovation_ratio <= 0.5,
                reason=f"Innovative features: {', '.join(innovative_features[:3]) if innovative_features else 'None'}"
            )
        }
    )


@reward_function
def feature_feasibility_reward(
    messages: Union[List[Message], List[Dict[str, Any]]],
    ground_truth: Optional[Dict[str, Any]] = None,
    **kwargs
) -> EvaluateResult:
    """
    Evaluate technical feasibility of features.
    """
    # Extract features
    last_message = messages[-1] if messages else None
    if not last_message:
        return EvaluateResult(score=0.0, reason="No messages", metrics={})
    
    content = last_message.get("content", "") if isinstance(last_message, dict) else (last_message.content or "")
    
    try:
        json_match = re.search(r'\{[\s\S]*\}', content)
        if json_match:
            features = json.loads(json_match.group())
        else:
            return EvaluateResult(score=0.0, reason="No features found", metrics={})
    except:
        return EvaluateResult(score=0.0, reason="Parse error", metrics={})
    
    # Complexity and risk scoring
    complexity_scores = {
        "low": 1.0,
        "medium": 0.7,
        "high": 0.4,
        "very_high": 0.1
    }
    
    risk_scores = {
        1: 1.0,
        2: 0.8,
        3: 0.6,
        4: 0.4,
        5: 0.2
    }
    
    feasibility_scores = []
    high_risk_features = []
    
    for category, feature_list in features.items():
        for feature in feature_list:
            if not isinstance(feature, dict):
                continue
                
            complexity = feature.get("complexity", "medium")
            risk = feature.get("technical_risk", 3)
            name = feature.get("name", "Unknown")
            
            complexity_score = complexity_scores.get(complexity, 0.5)
            risk_score = risk_scores.get(risk, 0.5)
            
            feature_feasibility = (complexity_score + risk_score) / 2
            feasibility_scores.append(feature_feasibility)
            
            if feature_feasibility < 0.5:
                high_risk_features.append(f"{name} (risk: {risk}, complexity: {complexity})")
    
    avg_feasibility = sum(feasibility_scores) / len(feasibility_scores) if feasibility_scores else 0.0
    
    return EvaluateResult(
        score=avg_feasibility,
        reason=f"Average feasibility: {avg_feasibility:.1%}",
        metrics={
            "feasibility": MetricResult(
                score=avg_feasibility,
                success=avg_feasibility >= 0.6,
                reason=f"High risk: {', '.join(high_risk_features[:2]) if high_risk_features else 'All feasible'}"
            )
        }
    )


@reward_function
def feature_user_value_reward(
    messages: Union[List[Message], List[Dict[str, Any]]],
    ground_truth: Optional[Dict[str, Any]] = None,
    **kwargs
) -> EvaluateResult:
    """
    Evaluate user value delivery of features.
    """
    # Extract features
    last_message = messages[-1] if messages else None
    if not last_message:
        return EvaluateResult(score=0.0, reason="No messages", metrics={})
    
    content = last_message.get("content", "") if isinstance(last_message, dict) else (last_message.content or "")
    
    try:
        json_match = re.search(r'\{[\s\S]*\}', content)
        if json_match:
            features = json.loads(json_match.group())
        else:
            return EvaluateResult(score=0.0, reason="No features found", metrics={})
    except:
        return EvaluateResult(score=0.0, reason="Parse error", metrics={})
    
    value_scores = []
    high_value_features = []
    low_value_features = []
    
    for category, feature_list in features.items():
        for feature in feature_list:
            if not isinstance(feature, dict):
                continue
                
            user_value = feature.get("user_value", 5)
            name = feature.get("name", "Unknown")
            normalized_value = user_value / 10.0
            value_scores.append(normalized_value)
            
            if user_value >= 8:
                high_value_features.append(name)
            elif user_value <= 4:
                low_value_features.append(name)
    
    avg_value = sum(value_scores) / len(value_scores) if value_scores else 0.0
    
    # Bonus for having multiple high-value features
    if len(high_value_features) >= 3:
        avg_value = min(avg_value + 0.1, 1.0)
    
    feedback_parts = []
    if high_value_features:
        feedback_parts.append(f"High value: {', '.join(high_value_features[:2])}")
    if low_value_features:
        feedback_parts.append(f"Low value: {', '.join(low_value_features[:2])}")
    
    feedback = " | ".join(feedback_parts) if feedback_parts else "Balanced value distribution"
    
    return EvaluateResult(
        score=avg_value,
        reason=f"Average user value: {avg_value:.1%}",
        metrics={
            "user_value": MetricResult(
                score=avg_value,
                success=avg_value >= 0.7,
                reason=feedback
            )
        }
    )


def create_combined_evaluator(weights: Optional[Dict[str, float]] = None):
    """
    Create a combined evaluator using multiple reward functions.
    
    Args:
        weights: Dictionary of weights for each evaluator
    
    Returns:
        A combined reward function
    """
    if weights is None:
        weights = {
            "completeness": 0.25,
            "clarity": 0.15,
            "innovation": 0.10,
            "feasibility": 0.20,
            "user_value": 0.30
        }
    
    @reward_function
    def combined_feature_evaluator(
        messages: Union[List[Message], List[Dict[str, Any]]],
        ground_truth: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> EvaluateResult:
        """Combined evaluation of features."""
        
        # Run individual evaluators
        completeness_result = feature_completeness_reward(messages, ground_truth, **kwargs)
        clarity_result = feature_clarity_reward(messages, ground_truth, **kwargs)
        innovation_result = feature_innovation_reward(messages, ground_truth, **kwargs)
        feasibility_result = feature_feasibility_reward(messages, ground_truth, **kwargs)
        user_value_result = feature_user_value_reward(messages, ground_truth, **kwargs)
        
        # Calculate weighted score
        combined_score = (
            completeness_result.score * weights["completeness"] +
            clarity_result.score * weights["clarity"] +
            innovation_result.score * weights["innovation"] +
            feasibility_result.score * weights["feasibility"] +
            user_value_result.score * weights["user_value"]
        )
        
        # Combine metrics
        all_metrics = {
            "completeness": completeness_result.metrics.get("category_coverage", 
                MetricResult(score=completeness_result.score, success=True, reason="")),
            "clarity": clarity_result.metrics.get("clarity", 
                MetricResult(score=clarity_result.score, success=True, reason="")),
            "innovation": innovation_result.metrics.get("innovation", 
                MetricResult(score=innovation_result.score, success=True, reason="")),
            "feasibility": feasibility_result.metrics.get("feasibility",
                MetricResult(score=feasibility_result.score, success=True, reason="")),
            "user_value": user_value_result.metrics.get("user_value",
                MetricResult(score=user_value_result.score, success=True, reason=""))
        }
        
        # Generate improvement suggestions based on lowest scores
        suggestions = []
        score_results = [
            ("completeness", completeness_result.score, "Add more features to under-represented categories"),
            ("clarity", clarity_result.score, "Improve feature descriptions with specific use cases"),
            ("innovation", innovation_result.score, "Add more AI-powered or automated capabilities"),
            ("feasibility", feasibility_result.score, "Reduce technical complexity or break down high-risk features"),
            ("user_value", user_value_result.score, "Focus on features that directly solve user pain points")
        ]
        
        # Sort by score and suggest improvements for lowest scoring areas
        score_results.sort(key=lambda x: x[1])
        for name, score, suggestion in score_results[:2]:  # Top 2 areas needing improvement
            if score < 0.7:
                suggestions.append(suggestion)
        
        return EvaluateResult(
            score=combined_score,
            reason=f"Combined score: {combined_score:.1%}",
            metrics=all_metrics,
            metadata={"suggestions": suggestions}
        )
    
    return combined_feature_evaluator