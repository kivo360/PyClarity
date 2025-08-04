#!/usr/bin/env python3
"""
Test script for reward-kit integration.
"""

import json
from pyclarity_rewards import (
    feature_completeness_reward,
    feature_clarity_reward,
    feature_innovation_reward,
    feature_feasibility_reward,
    feature_user_value_reward,
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
    
    # Test feasibility
    feasibility_result = feature_feasibility_reward(messages)
    print(f"\nFeasibility Score: {feasibility_result.score:.2%}")
    print(f"Reason: {feasibility_result.reason}")
    
    # Test user value
    user_value_result = feature_user_value_reward(messages)
    print(f"\nUser Value Score: {user_value_result.score:.2%}")
    print(f"Reason: {user_value_result.reason}")


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
        "completeness": 0.30,
        "clarity": 0.10,
        "innovation": 0.20,
        "feasibility": 0.15,
        "user_value": 0.25
    })
    custom_result = custom_evaluator(messages)
    print(f"\nCustom Weighted Score: {custom_result.score:.2%}")


def test_edge_cases():
    """Test edge cases and error handling."""
    
    print("\n\nTesting Edge Cases")
    print("=" * 50)
    
    # Test empty messages
    evaluator = create_combined_evaluator()
    result = evaluator([])
    print(f"\nEmpty messages score: {result.score}")
    print(f"Reason: {result.reason}")
    
    # Test invalid JSON
    result = evaluator([{"role": "assistant", "content": "This is not JSON"}])
    print(f"\nInvalid JSON score: {result.score}")
    print(f"Reason: {result.reason}")
    
    # Test minimal features
    minimal_features = {
        "core": [
            {
                "id": "F001",
                "name": "Basic Feature",
                "description": "Simple feature",
                "priority": "low",
                "complexity": "low",
                "user_value": 5,
                "technical_risk": 1
            }
        ]
    }
    result = evaluator([{"role": "assistant", "content": json.dumps(minimal_features)}])
    print(f"\nMinimal features score: {result.score:.2%}")
    print(f"Reason: {result.reason}")


def test_optimization_scenario():
    """Test a realistic optimization scenario."""
    
    print("\n\nTesting Optimization Scenario")
    print("=" * 50)
    
    # Initial features (poor quality)
    initial_features = {
        "core": [
            {
                "id": "F001",
                "name": "Feature 1",
                "description": "Does something",
                "priority": "medium",
                "complexity": "high",
                "user_value": 3,
                "technical_risk": 4
            }
        ],
        "supporting": [],
        "integration": [],
        "analytics": [],
        "future": []
    }
    
    # Improved features
    improved_features = {
        "core": [
            {
                "id": "F001",
                "name": "AI-Powered UI Generator",
                "description": "Intelligent system that generates UI components using machine learning for adaptive interfaces",
                "priority": "high",
                "complexity": "high",
                "user_value": 9,
                "technical_risk": 3
            },
            {
                "id": "F002",
                "name": "Real-time Preview Engine",
                "description": "Live preview of generated UI with instant updates and hot-reload functionality",
                "priority": "high",
                "complexity": "medium",
                "user_value": 8,
                "technical_risk": 2
            },
            {
                "id": "F003",
                "name": "Component Validator",
                "description": "Automated validation system ensuring generated components meet accessibility standards",
                "priority": "high",
                "complexity": "medium",
                "user_value": 8,
                "technical_risk": 2
            }
        ],
        "supporting": [
            {
                "id": "F004",
                "name": "Template Marketplace",
                "description": "Community-driven marketplace for sharing and selling UI templates",
                "priority": "medium",
                "complexity": "medium",
                "user_value": 7,
                "technical_risk": 2
            },
            {
                "id": "F005",
                "name": "Version Control System",
                "description": "Built-in version control for tracking UI component changes over time",
                "priority": "medium",
                "complexity": "medium",
                "user_value": 7,
                "technical_risk": 2
            }
        ],
        "integration": [
            {
                "id": "F006",
                "name": "Design Tool Bridge",
                "description": "Seamless integration with Figma, Sketch, and Adobe XD for design imports",
                "priority": "high",
                "complexity": "high",
                "user_value": 8,
                "technical_risk": 3
            }
        ],
        "analytics": [
            {
                "id": "F007",
                "name": "Performance Dashboard",
                "description": "Real-time analytics showing component performance and usage patterns",
                "priority": "medium",
                "complexity": "low",
                "user_value": 6,
                "technical_risk": 1
            }
        ],
        "future": [
            {
                "id": "F008",
                "name": "Predictive Design AI",
                "description": "AI system that predicts and suggests next design elements based on context",
                "priority": "low",
                "complexity": "very_high",
                "user_value": 9,
                "technical_risk": 5
            }
        ]
    }
    
    evaluator = create_combined_evaluator()
    
    # Evaluate initial features
    initial_result = evaluator([{"role": "assistant", "content": json.dumps(initial_features)}])
    print(f"\nInitial Features Score: {initial_result.score:.2%}")
    print("Initial Suggestions:")
    if hasattr(initial_result, 'metadata') and 'suggestions' in initial_result.metadata:
        for suggestion in initial_result.metadata['suggestions']:
            print(f"  • {suggestion}")
    
    # Evaluate improved features
    improved_result = evaluator([{"role": "assistant", "content": json.dumps(improved_features)}])
    print(f"\nImproved Features Score: {improved_result.score:.2%}")
    print("Improved Suggestions:")
    if hasattr(improved_result, 'metadata') and 'suggestions' in improved_result.metadata:
        for suggestion in improved_result.metadata['suggestions']:
            print(f"  • {suggestion}")
    
    # Calculate improvement
    improvement = (improved_result.score - initial_result.score) / initial_result.score * 100
    print(f"\nImprovement: {improvement:.1f}%")


def main():
    """Run all tests."""
    test_individual_rewards()
    test_combined_evaluator()
    test_edge_cases()
    test_optimization_scenario()
    
    print("\n\n✅ All tests completed!")


if __name__ == "__main__":
    main()