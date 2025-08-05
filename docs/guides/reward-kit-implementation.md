# Reward-Kit Implementation Guide for PyClarity Optimizer

## Quick Start Implementation

This guide shows how to modify PyClarity's existing `llm_optimizer_enhanced.py` to use reward-kit for evaluation.

## Step 1: Create Reward Functions Module

First, create a dedicated module for PyClarity reward functions:

```python
# experiment/pyclarity_rewards.py
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
            "completeness": 0.4,
            "clarity": 0.3,
            "innovation": 0.3
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
        
        # Calculate weighted score
        combined_score = (
            completeness_result.score * weights["completeness"] +
            clarity_result.score * weights["clarity"] +
            innovation_result.score * weights["innovation"]
        )
        
        # Combine metrics
        all_metrics = {
            "completeness": completeness_result.metrics.get("category_coverage", MetricResult(score=completeness_result.score, success=True, reason="")),
            "clarity": clarity_result.metrics.get("clarity", MetricResult(score=clarity_result.score, success=True, reason="")),
            "innovation": innovation_result.metrics.get("innovation", MetricResult(score=innovation_result.score, success=True, reason=""))
        }
        
        # Generate improvement suggestions based on lowest scores
        suggestions = []
        if completeness_result.score < 0.7:
            suggestions.append("Add more features to under-represented categories")
        if clarity_result.score < 0.7:
            suggestions.append("Improve feature descriptions with specific use cases")
        if innovation_result.score < 0.7:
            suggestions.append("Add more AI-powered or automated capabilities")
        
        return EvaluateResult(
            score=combined_score,
            reason=f"Combined score: {combined_score:.1%}",
            metrics=all_metrics,
            metadata={"suggestions": suggestions}
        )
    
    return combined_feature_evaluator
```

## Step 2: Modified Optimizer Implementation

Create a new optimizer that uses reward-kit:

```python
# experiment/llm_optimizer_reward_kit.py
"""
Enhanced LLM Optimizer using Reward-Kit for evaluation.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from groq import Groq
from loguru import logger

# Import reward-kit components
from pyclarity_rewards import create_combined_evaluator


class RewardKitLLMOptimizer:
    """LLM Optimizer enhanced with reward-kit evaluation."""
    
    def __init__(self):
        self.iteration = 0
        self.feature_list = {}
        self.improvement_history = []
        self.convergence_threshold = 0.95
        self.docs_path = Path("../docs/ai-prompting-techniques")
        self.output_path = Path()
        self.history_path = Path("history")
        
        # Initialize Groq client
        self.client = Groq()
        
        # Initialize reward-kit evaluator
        self.evaluator = create_combined_evaluator()
        
        # Create necessary directories
        self.history_path.mkdir(exist_ok=True)
        
        # Load existing state if available
        self._load_state()
    
    def _load_state(self):
        """Load previous state if exists."""
        features_file = self.output_path / "features.json"
        if features_file.exists():
            with open(features_file) as f:
                data = json.load(f)
                self.feature_list = data.get("features", {})
                self.iteration = data.get("last_iteration", 0)
                logger.info(f"Loaded state from iteration {self.iteration}")
    
    def evaluate_features_with_reward_kit(self, features: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """
        Evaluate features using reward-kit framework.
        
        Args:
            features: Dictionary of feature categories and their features
            
        Returns:
            Evaluation result in optimizer format
        """
        # Convert to message format for reward function
        messages = [
            {"role": "system", "content": "Feature generation and evaluation system"},
            {"role": "assistant", "content": json.dumps(features, indent=2)}
        ]
        
        # Run reward function
        result = self.evaluator(messages)
        
        # Extract suggestions from metadata if available
        suggestions = result.metadata.get("suggestions", []) if hasattr(result, 'metadata') else []
        
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
            "suggestions": suggestions,
            "improvement_rate": self._calculate_improvement_rate(result.score),
            "reward_kit_result": result  # Keep original for debugging
        }
        
        return evaluation_result
    
    def _calculate_improvement_rate(self, current_score: float) -> float:
        """Calculate improvement rate from history."""
        if not self.improvement_history:
            return 0.0
        
        previous_score = self.improvement_history[-1]["quality_score"]
        return (current_score - previous_score) / previous_score if previous_score > 0 else 0
    
    def generate_features_with_llm(self, summary: str, strategy: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        """Generate features using LLM."""
        prompt = f"""You are a product innovator designing features for an AI-powered UI generation tool.

Context:
{summary}

Task: Generate a comprehensive feature list organized into categories (core, supporting, integration, analytics, future).

Generate features in this exact JSON format:
{{
  "core": [...],
  "supporting": [...],
  "integration": [...],
  "analytics": [...],
  "future": [...]
}}

Each feature should follow this structure:
{{
  "id": "F001",
  "name": "Feature Name",
  "description": "Clear description with specific use case (50-150 chars)",
  "priority": "high|medium|low",
  "complexity": "low|medium|high|very_high",
  "dependencies": ["F002"],
  "user_value": 8,  // 1-10
  "technical_risk": 2  // 1-5
}}"""
        
        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                max_tokens=4000,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.choices[0].message.content
            
            import re
            json_match = re.search(r'\{[\s\S]*\}', content)
            if json_match:
                features = json.loads(json_match.group())
                logger.info(f"✅ Generated {sum(len(features[cat]) for cat in features)} features")
                return features
        except Exception as e:
            logger.error(f"Error generating features: {e}")
        
        return self._get_fallback_features()
    
    def optimize_features_with_llm(
        self,
        features: Dict[str, List[Dict[str, Any]]],
        evaluation_result: Dict[str, Any]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Optimize features based on reward-kit evaluation."""
        
        suggestions_text = "\n".join(f"- {s}" for s in evaluation_result["suggestions"])
        
        prompt = f"""You are an optimization expert improving features based on evaluation feedback.

Current Features:
{json.dumps(features, indent=2)}

Evaluation Results:
- Overall Score: {evaluation_result["overall_score"]:.2%}
- Scores: {json.dumps(evaluation_result["scores"], indent=2)}
- Suggestions:
{suggestions_text}

Task: Improve the feature list addressing the suggestions while maintaining what works well.
Return the optimized features in the same JSON format."""
        
        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                max_tokens=4000,
                temperature=0.8,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.choices[0].message.content
            import re
            json_match = re.search(r'\{[\s\S]*\}', content)
            
            if json_match:
                optimized = json.loads(json_match.group())
                logger.info("✅ Features optimized based on reward-kit evaluation")
                return optimized
        except Exception as e:
            logger.error(f"Error optimizing features: {e}")
        
        return features
    
    def run_optimization_loop(self, max_iterations: int = 10):
        """Main optimization loop using reward-kit."""
        logger.info(f"Starting Reward-Kit Enhanced Optimizer (max {max_iterations} iterations)")
        
        while self.iteration < max_iterations and not self.has_converged():
            start_time = time.time()
            self.iteration += 1
            
            logger.info(f"\n{'=' * 60}")
            logger.info(f"Starting iteration {self.iteration}")
            logger.info(f"{'=' * 60}")
            
            # Step 1: Generate initial summary
            summary = self._generate_summary()
            
            # Step 2: Generate features
            strategy = {"model": "llama-3.1-70b-versatile", "temperature": 0.7}
            new_features = self.generate_features_with_llm(summary, strategy)
            
            # Step 3: Evaluate with reward-kit
            evaluation_result = self.evaluate_features_with_reward_kit(new_features)
            
            # Step 4: Optimize based on evaluation
            self.feature_list = self.optimize_features_with_llm(new_features, evaluation_result)
            
            # Step 5: Log results
            iteration_time = time.time() - start_time
            self.log_iteration_results(evaluation_result, iteration_time)
            
            # Step 6: Save checkpoint
            self.save_checkpoint()
            
            # Display summary
            self.display_iteration_summary(evaluation_result)
            
            # Sleep between iterations
            if self.iteration < max_iterations and not self.has_converged():
                logger.info("\n💤 Sleeping for 10 seconds...")
                time.sleep(10)
        
        logger.info("\n" + "=" * 60)
        logger.info("Optimization complete!")
        logger.info(f"Final score: {self.improvement_history[-1]['quality_score']:.2%}")
    
    def _generate_summary(self) -> str:
        """Generate summary of documentation and context."""
        return f"""
Documentation Summary:
- AI prompting techniques for UI generation
- Visual Chain-of-Thought methodology
- Auto-CoT with self-consistency
- Dynamic prompt rewriting
- Business and marketing frameworks

Current Iteration: {self.iteration}
Previous Score: {self.improvement_history[-1]['quality_score'] if self.improvement_history else 'N/A'}
"""
    
    def has_converged(self) -> bool:
        """Check if optimization has converged."""
        if len(self.improvement_history) < 3:
            return False
        
        recent_scores = [h["quality_score"] for h in self.improvement_history[-3:]]
        improvement = (recent_scores[-1] - recent_scores[0]) / recent_scores[0]
        
        return improvement < 0.02 and self.iteration >= 5
    
    def log_iteration_results(self, evaluation_result: Dict[str, Any], iteration_time: float):
        """Log results of current iteration."""
        result = {
            "iteration": self.iteration,
            "timestamp": datetime.now().isoformat(),
            "quality_score": evaluation_result["overall_score"],
            "total_features": sum(len(self.feature_list[cat]) for cat in self.feature_list),
            "iteration_time": round(iteration_time, 2),
            "metrics": evaluation_result["scores"],
            "improvement_rate": evaluation_result["improvement_rate"],
            "suggestions": evaluation_result["suggestions"]
        }
        
        self.improvement_history.append(result)
        
        # Save metrics
        with open(self.output_path / "metrics.json", "w") as f:
            json.dump({
                "current": result,
                "history": self.improvement_history[-10:]
            }, f, indent=2)
    
    def save_checkpoint(self):
        """Save current state."""
        features_data = {
            "iteration": self.iteration,
            "timestamp": datetime.now().isoformat(),
            "features": self.feature_list,
            "last_iteration": self.iteration
        }
        
        with open(self.output_path / "features.json", "w") as f:
            json.dump(features_data, f, indent=2)
        
        # Save to history
        history_file = self.history_path / f"iteration_{self.iteration:03d}.json"
        with open(history_file, "w") as f:
            json.dump(features_data, f, indent=2)
    
    def display_iteration_summary(self, evaluation_result: Dict[str, Any]):
        """Display iteration summary."""
        print(f"\n📊 ITERATION {self.iteration} SUMMARY")
        print("─" * 50)
        print(f"Overall Score: {evaluation_result['overall_score']:.1%}")
        print("\nScores by Criteria:")
        for criterion, score in evaluation_result["scores"].items():
            print(f"  • {criterion.title()}: {score:.1%}")
        print("\n💡 Suggestions:")
        for i, suggestion in enumerate(evaluation_result["suggestions"][:3], 1):
            print(f"  {i}. {suggestion}")
        print("─" * 50)
    
    def _get_fallback_features(self) -> Dict[str, List[Dict[str, Any]]]:
        """Fallback features if generation fails."""
        return {
            "core": [
                {
                    "id": "F001",
                    "name": "AI-Powered UI Generator",
                    "description": "Generates UI components using advanced AI models",
                    "priority": "high",
                    "complexity": "high",
                    "dependencies": [],
                    "user_value": 9,
                    "technical_risk": 3
                }
            ],
            "supporting": [],
            "integration": [],
            "analytics": [],
            "future": []
        }


def main():
    """Main entry point."""
    import argparse
    import os
    
    parser = argparse.ArgumentParser(description="Reward-Kit Enhanced LLM Optimizer")
    parser.add_argument("--iterations", type=int, default=5, help="Maximum iterations")
    parser.add_argument("--reset", action="store_true", help="Reset and start fresh")
    args = parser.parse_args()
    
    if not os.environ.get("GROQ_API_KEY"):
        logger.error("Please set GROQ_API_KEY environment variable")
        return
    
    optimizer = RewardKitLLMOptimizer()
    
    if args.reset:
        for f in ["features.json", "metrics.json"]:
            if os.path.exists(f):
                os.remove(f)
        optimizer.iteration = 0
        optimizer.feature_list = {}
        logger.info("Reset complete. Starting fresh.")
    
    try:
        optimizer.run_optimization_loop(max_iterations=args.iterations)
    except KeyboardInterrupt:
        logger.info("\n⚠️ Optimization stopped by user")
    except Exception as e:
        logger.error(f"Error in optimization: {e}", exc_info=True)


if __name__ == "__main__":
    main()
```

## Step 3: Testing the Implementation

Create test scripts to verify the reward functions:

```python
# experiment/test_reward_kit_integration.py
"""
Test script for reward-kit integration.
"""

import json
from pyclarity_rewards import (
    feature_completeness_reward,
    feature_clarity_reward,
    feature_innovation_reward,
    create_combined_evaluator
)


def test_individual_rewards():
    """Test individual reward functions."""
    
    # Test data
    test_features = {
        "core": [
            {
                "id": "F001",
                "name": "AI-Powered UI Generator",
                "description": "Intelligent system that generates complete UI components using advanced machine learning",
                "priority": "high",
                "complexity": "high",
                "user_value": 9,
                "technical_risk": 3
            },
            {
                "id": "F002",
                "name": "Real-time Preview",
                "description": "Live preview of generated UI with instant updates",
                "priority": "high",
                "complexity": "medium",
                "user_value": 8,
                "technical_risk": 2
            }
        ],
        "supporting": [
            {
                "id": "F003",
                "name": "Template Library",
                "description": "Pre-built templates for common UI patterns",
                "priority": "medium",
                "complexity": "low",
                "user_value": 7,
                "technical_risk": 1
            }
        ],
        "integration": [],
        "analytics": [],
        "future": []
    }
    
    messages = [
        {"role": "assistant", "content": json.dumps(test_features, indent=2)}
    ]
    
    print("Testing Individual Reward Functions")
    print("=" * 50)
    
    # Test completeness
    completeness_result = feature_completeness_reward(messages)
    print(f"\nCompleteness Score: {completeness_result.score:.2%}")
    print(f"Reason: {completeness_result.reason}")
    for metric_name, metric in completeness_result.metrics.items():
        print(f"  - {metric_name}: {metric.score:.2%} - {metric.reason}")
    
    # Test clarity
    clarity_result = feature_clarity_reward(messages)
    print(f"\nClarity Score: {clarity_result.score:.2%}")
    print(f"Reason: {clarity_result.reason}")
    
    # Test innovation
    innovation_result = feature_innovation_reward(messages)
    print(f"\nInnovation Score: {innovation_result.score:.2%}")
    print(f"Reason: {innovation_result.reason}")


def test_combined_evaluator():
    """Test combined evaluator."""
    
    # Create test data with more features
    test_features = {
        "core": [
            {
                "id": "F001",
                "name": "AI-Powered UI Generator",
                "description": "Intelligent system with neural networks for adaptive UI generation",
                "priority": "high",
                "complexity": "high",
                "user_value": 9,
                "technical_risk": 3
            },
            {
                "id": "F002",
                "name": "Real-time Collaboration",
                "description": "Multi-user real-time editing with conflict resolution",
                "priority": "high",
                "complexity": "high",
                "user_value": 8,
                "technical_risk": 4
            },
            {
                "id": "F003",
                "name": "Visual Debugger",
                "description": "Interactive debugging tools for generated components",
                "priority": "medium",
                "complexity": "medium",
                "user_value": 7,
                "technical_risk": 2
            }
        ],
        "supporting": [
            {
                "id": "F004",
                "name": "Component Library",
                "description": "Extensive library of reusable UI components",
                "priority": "medium",
                "complexity": "low",
                "user_value": 7,
                "technical_risk": 1
            },
            {
                "id": "F005",
                "name": "Theme Engine",
                "description": "Advanced theming with dynamic color generation",
                "priority": "medium",
                "complexity": "medium",
                "user_value": 6,
                "technical_risk": 2
            }
        ],
        "integration": [
            {
                "id": "F006",
                "name": "API Gateway",
                "description": "RESTful API for external integrations",
                "priority": "high",
                "complexity": "medium",
                "user_value": 8,
                "technical_risk": 2
            }
        ],
        "analytics": [
            {
                "id": "F007",
                "name": "Usage Analytics",
                "description": "Track component usage and performance metrics",
                "priority": "low",
                "complexity": "low",
                "user_value": 5,
                "technical_risk": 1
            }
        ],
        "future": [
            {
                "id": "F008",
                "name": "AI Design Assistant",
                "description": "Predictive design suggestions using machine learning",
                "priority": "low",
                "complexity": "very_high",
                "user_value": 9,
                "technical_risk": 5
            }
        ]
    }
    
    messages = [
        {"role": "assistant", "content": json.dumps(test_features, indent=2)}
    ]
    
    print("\n\nTesting Combined Evaluator")
    print("=" * 50)
    
    # Test with default weights
    evaluator = create_combined_evaluator()
    result = evaluator(messages)
    
    print(f"\nCombined Score: {result.score:.2%}")
    print(f"Reason: {result.reason}")
    print("\nDetailed Metrics:")
    for metric_name, metric in result.metrics.items():
        print(f"  - {metric_name}: {metric.score:.2%} - {metric.reason}")
    
    if hasattr(result, 'metadata') and 'suggestions' in result.metadata:
        print("\nSuggestions:")
        for suggestion in result.metadata['suggestions']:
            print(f"  • {suggestion}")
    
    # Test with custom weights
    custom_evaluator = create_combined_evaluator({
        "completeness": 0.5,
        "clarity": 0.2,
        "innovation": 0.3
    })
    custom_result = custom_evaluator(messages)
    print(f"\nCustom Weighted Score: {custom_result.score:.2%}")


if __name__ == "__main__":
    test_individual_rewards()
    test_combined_evaluator()
```

## Step 4: Running the Enhanced Optimizer

```bash
# Set up environment
export GROQ_API_KEY="your-groq-api-key"

# Run the optimizer
python experiment/llm_optimizer_reward_kit.py --iterations 5

# Run with reset
python experiment/llm_optimizer_reward_kit.py --iterations 5 --reset

# Test reward functions
python experiment/test_reward_kit_integration.py
```

## Step 5: Monitoring and Analysis

Create a script to analyze optimization results:

```python
# experiment/analyze_reward_kit_results.py
"""
Analyze results from reward-kit optimization.
"""

import json
import matplotlib.pyplot as plt
from pathlib import Path


def analyze_optimization_history():
    """Analyze and visualize optimization history."""
    
    # Load metrics
    metrics_file = Path("metrics.json")
    if not metrics_file.exists():
        print("No metrics file found. Run optimization first.")
        return
    
    with open(metrics_file) as f:
        data = json.load(f)
    
    history = data.get("history", [])
    if not history:
        print("No history data available.")
        return
    
    # Extract data
    iterations = [h["iteration"] for h in history]
    overall_scores = [h["quality_score"] for h in history]
    
    # Extract individual metric scores
    metric_names = list(history[0]["metrics"].keys()) if history else []
    metric_scores = {name: [] for name in metric_names}
    
    for h in history:
        for name in metric_names:
            metric_scores[name].append(h["metrics"].get(name, 0))
    
    # Create plots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Overall score plot
    ax1.plot(iterations, overall_scores, 'b-o', linewidth=2, markersize=8)
    ax1.set_xlabel('Iteration')
    ax1.set_ylabel('Overall Score')
    ax1.set_title('Optimization Progress - Overall Score')
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 1)
    
    # Individual metrics plot
    for name, scores in metric_scores.items():
        ax2.plot(iterations, scores, '-o', label=name.title(), linewidth=1.5)
    
    ax2.set_xlabel('Iteration')
    ax2.set_ylabel('Score')
    ax2.set_title('Individual Metric Scores')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0, 1)
    
    plt.tight_layout()
    plt.savefig('reward_kit_optimization_progress.png', dpi=150)
    plt.show()
    
    # Print summary
    print("\nOptimization Summary")
    print("=" * 50)
    print(f"Total Iterations: {len(history)}")
    print(f"Initial Score: {history[0]['quality_score']:.2%}")
    print(f"Final Score: {history[-1]['quality_score']:.2%}")
    improvement = (history[-1]['quality_score'] - history[0]['quality_score']) / history[0]['quality_score']
    print(f"Total Improvement: {improvement:.2%}")
    
    print("\nFinal Metrics:")
    for name, score in history[-1]["metrics"].items():
        print(f"  - {name.title()}: {score:.2%}")
    
    print("\nLatest Suggestions:")
    for suggestion in history[-1].get("suggestions", []):
        print(f"  • {suggestion}")


if __name__ == "__main__":
    analyze_optimization_history()
```

## Key Benefits of This Implementation

1. **Modular Evaluation**: Separate reward functions for different aspects
2. **Flexible Weighting**: Easy to adjust importance of different metrics
3. **Clear Feedback**: Detailed reasons and suggestions for improvement
4. **Easy Testing**: Individual reward functions can be tested in isolation
5. **Production Ready**: Can be deployed to Fireworks AI or other platforms
6. **Extensible**: Easy to add new evaluation criteria

## Next Steps

1. Fine-tune the reward function weights based on results
2. Add more sophisticated evaluation metrics
3. Integrate with TRL for reinforcement learning
4. Deploy to production for continuous evaluation
5. Create dataset-specific reward functions

This implementation provides a solid foundation for using reward-kit in PyClarity's optimization loop while maintaining compatibility with the existing architecture.