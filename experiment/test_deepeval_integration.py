#!/usr/bin/env python3
"""
Test script for DeepEval + Reward-Kit integration.
"""

import json
import os
from deepeval_rewards import (
    hallucination_free_reward,
    factual_consistency_reward,
    safety_reward,
    answer_quality_reward,
    custom_criteria_reward,
    feature_quality_deepeval_reward,
    create_deepeval_enhanced_evaluator,
    create_pyclarity_deepeval_evaluator
)


def test_individual_deepeval_rewards():
    """Test individual DeepEval reward functions."""
    
    print("Testing Individual DeepEval Reward Functions")
    print("=" * 60)
    
    # Test messages
    messages = [
        {"role": "user", "content": "What is the capital of France?"},
        {"role": "assistant", "content": "The capital of France is Paris, a beautiful city known for the Eiffel Tower."}
    ]
    
    # Test with context (for hallucination check)
    context = ["France is a country in Europe. Its capital city is Paris, home to the Eiffel Tower."]
    
    print("\n1. Hallucination-Free Reward")
    print("-" * 30)
    try:
        result = hallucination_free_reward(messages, context=context)
        print(f"Score: {result.score:.2%}")
        print(f"Reason: {result.reason}")
        for metric_name, metric in result.metrics.items():
            print(f"  - {metric_name}: {metric.score:.2%} (Success: {metric.success})")
    except Exception as e:
        print(f"Error: {e}")
        print("Note: DeepEval requires API key or local model setup")
    
    print("\n2. Safety Reward")
    print("-" * 30)
    try:
        result = safety_reward(messages)
        print(f"Score: {result.score:.2%}")
        print(f"Reason: {result.reason}")
        for metric_name, metric in result.metrics.items():
            print(f"  - {metric_name}: {metric.score:.2%} (Success: {metric.success})")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n3. Answer Quality Reward")
    print("-" * 30)
    try:
        result = answer_quality_reward(messages)
        print(f"Score: {result.score:.2%}")
        print(f"Reason: {result.reason}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test custom criteria
    print("\n4. Custom Criteria (Technical Accuracy)")
    print("-" * 30)
    tech_messages = [
        {"role": "user", "content": "How do I implement a binary search in Python?"},
        {"role": "assistant", "content": """def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1  # Target not found"""}
    ]
    
    try:
        result = custom_criteria_reward(tech_messages, criteria="technical_accuracy")
        print(f"Score: {result.score:.2%}")
        print(f"Reason: {result.reason}")
    except Exception as e:
        print(f"Error: {e}")


def test_pyclarity_features_with_deepeval():
    """Test PyClarity feature evaluation with DeepEval."""
    
    print("\n\nTesting PyClarity Features with DeepEval")
    print("=" * 60)
    
    # Sample PyClarity features
    features = {
        "core": [
            {
                "id": "F001",
                "name": "AI-Powered UI Generator",
                "description": "Intelligent system using neural networks to generate adaptive UI components in real-time",
                "priority": "high",
                "complexity": "high",
                "user_value": 9,
                "technical_risk": 3
            },
            {
                "id": "F002",
                "name": "Real-time Collaboration Engine",
                "description": "Multi-user collaborative editing with conflict resolution and live updates",
                "priority": "high",
                "complexity": "high",
                "user_value": 8,
                "technical_risk": 4
            }
        ],
        "supporting": [
            {
                "id": "F003",
                "name": "Component Template Library",
                "description": "Extensive library of customizable UI component templates",
                "priority": "medium",
                "complexity": "low",
                "user_value": 7,
                "technical_risk": 1
            }
        ],
        "integration": [
            {
                "id": "F004",
                "name": "Design Tool Bridge",
                "description": "Seamless integration with Figma, Sketch, and Adobe XD",
                "priority": "high",
                "complexity": "medium",
                "user_value": 8,
                "technical_risk": 3
            }
        ],
        "analytics": [
            {
                "id": "F005",
                "name": "Performance Analytics Dashboard",
                "description": "Real-time metrics for component performance and usage patterns",
                "priority": "medium",
                "complexity": "medium",
                "user_value": 6,
                "technical_risk": 2
            }
        ],
        "future": []
    }
    
    messages = [
        {"role": "user", "content": "Evaluate these features for an AI-powered UI generation tool"},
        {"role": "assistant", "content": json.dumps(features, indent=2)}
    ]
    
    print("\n1. Feature Quality with DeepEval")
    print("-" * 30)
    try:
        result = feature_quality_deepeval_reward(messages)
        print(f"Score: {result.score:.2%}")
        print(f"Reason: {result.reason}")
        for metric_name, metric in result.metrics.items():
            print(f"  - {metric_name}: {metric.score:.2%}")
    except Exception as e:
        print(f"Error: {e}")


def test_comprehensive_evaluator():
    """Test comprehensive DeepEval evaluator."""
    
    print("\n\nTesting Comprehensive DeepEval Evaluator")
    print("=" * 60)
    
    # Create evaluator with custom criteria
    evaluator = create_deepeval_enhanced_evaluator(
        weights={
            "hallucination_free": 0.20,
            "answer_quality": 0.30,
            "safety": 0.20,
            "custom": 0.30
        },
        include_safety=True,
        custom_criteria=["technical_accuracy", "innovation", "completeness"]
    )
    
    # Test with a comprehensive response
    messages = [
        {"role": "user", "content": "How can I build a scalable microservices architecture?"},
        {"role": "assistant", "content": """To build a scalable microservices architecture, follow these key principles:

1. **Service Decomposition**: Break down your application into small, independent services based on business capabilities. Each service should have a single responsibility.

2. **API Gateway**: Implement an API gateway (like Kong or AWS API Gateway) as a single entry point for all client requests.

3. **Service Discovery**: Use tools like Consul or Eureka for dynamic service discovery and registration.

4. **Communication**: 
   - Synchronous: REST APIs or gRPC for real-time communication
   - Asynchronous: Message queues (RabbitMQ, Kafka) for decoupled communication

5. **Data Management**: Each service should own its data. Use the Database per Service pattern to ensure loose coupling.

6. **Containerization**: Package services in Docker containers for consistency and portability.

7. **Orchestration**: Use Kubernetes for container orchestration, providing automatic scaling, healing, and deployment.

8. **Monitoring**: Implement distributed tracing (Jaeger), logging (ELK stack), and metrics (Prometheus + Grafana).

9. **Resilience**: Add circuit breakers (Hystrix), retries, and timeouts to handle failures gracefully.

10. **CI/CD**: Automate deployment pipelines for each service independently.

This architecture enables horizontal scaling, technology diversity, and independent deployment of services."""}
    ]
    
    # Add context for better evaluation
    context = [
        "Microservices architecture is an approach to building applications as a collection of small, independent services.",
        "Key patterns include API Gateway, Service Discovery, Circuit Breaker, and Event Sourcing.",
        "Popular tools include Docker, Kubernetes, Istio, and various message brokers."
    ]
    
    print("\nComprehensive Evaluation Results:")
    print("-" * 30)
    try:
        result = evaluator(messages, context=context)
        print(f"Overall Score: {result.score:.2%}")
        print(f"Reason: {result.reason}")
        
        print("\nDetailed Metrics:")
        for metric_name, metric in result.metrics.items():
            print(f"  - {metric_name}: {metric.score:.2%}")
            if metric.reason:
                print(f"    Reason: {metric.reason}")
        
        if hasattr(result, 'metadata') and 'suggestions' in result.metadata:
            print("\nImprovement Suggestions:")
            for suggestion in result.metadata['suggestions']:
                print(f"  • {suggestion}")
        
        if hasattr(result, 'metadata') and 'component_scores' in result.metadata:
            print("\nComponent Scores:")
            for component, score in result.metadata['component_scores'].items():
                print(f"  - {component}: {score:.2%}")
    except Exception as e:
        print(f"Error: {e}")
        print("\nNote: Some DeepEval metrics require API keys or model setup.")


def test_pyclarity_deepeval_combined():
    """Test PyClarity + DeepEval combined evaluator."""
    
    print("\n\nTesting PyClarity + DeepEval Combined Evaluator")
    print("=" * 60)
    
    # Create combined evaluator
    evaluator = create_pyclarity_deepeval_evaluator()
    
    # Test with PyClarity features
    features = {
        "core": [
            {
                "id": "F001",
                "name": "AI-Powered UI Generator",
                "description": "Revolutionary system using GPT-4 and DALL-E to create complete UI designs from natural language",
                "priority": "high",
                "complexity": "very_high",
                "user_value": 10,
                "technical_risk": 4
            },
            {
                "id": "F002",
                "name": "Intelligent Code Generation",
                "description": "Automatically generates React/Vue/Angular components with best practices and accessibility",
                "priority": "high",
                "complexity": "high",
                "user_value": 9,
                "technical_risk": 3
            },
            {
                "id": "F003",
                "name": "Real-time Design Iteration",
                "description": "Live preview with hot-reload as AI generates and refines UI components",
                "priority": "high",
                "complexity": "medium",
                "user_value": 8,
                "technical_risk": 2
            }
        ],
        "supporting": [
            {
                "id": "F004",
                "name": "Smart Component Library",
                "description": "AI-curated library that learns from usage patterns and suggests optimal components",
                "priority": "medium",
                "complexity": "medium",
                "user_value": 7,
                "technical_risk": 2
            },
            {
                "id": "F005",
                "name": "Automated Testing Suite",
                "description": "AI-generated unit and integration tests for all generated components",
                "priority": "high",
                "complexity": "high",
                "user_value": 8,
                "technical_risk": 3
            }
        ],
        "integration": [
            {
                "id": "F006",
                "name": "Multi-Framework Export",
                "description": "Export generated UI to React, Vue, Angular, or vanilla JavaScript",
                "priority": "high",
                "complexity": "medium",
                "user_value": 9,
                "technical_risk": 2
            }
        ],
        "analytics": [
            {
                "id": "F007",
                "name": "AI Performance Insights",
                "description": "Track AI generation accuracy, user satisfaction, and component performance",
                "priority": "medium",
                "complexity": "medium",
                "user_value": 6,
                "technical_risk": 2
            }
        ],
        "future": [
            {
                "id": "F008",
                "name": "Voice-Controlled UI Design",
                "description": "Design interfaces using voice commands with real-time visual feedback",
                "priority": "low",
                "complexity": "very_high",
                "user_value": 7,
                "technical_risk": 5
            }
        ]
    }
    
    messages = [
        {"role": "user", "content": "Generate and evaluate features for an AI-powered UI generation tool"},
        {"role": "assistant", "content": json.dumps(features, indent=2)}
    ]
    
    print("\nPyClarity + DeepEval Combined Results:")
    print("-" * 30)
    try:
        result = evaluator(messages)
        print(f"Overall Score: {result.score:.2%}")
        print(f"Framework: {result.metadata.get('framework', 'Unknown')}")
        
        print("\nComponent Scores:")
        if hasattr(result, 'metadata') and 'component_scores' in result.metadata:
            for component, score in result.metadata['component_scores'].items():
                emoji = "✅" if score >= 0.7 else "⚠️" if score >= 0.5 else "❌"
                print(f"  {emoji} {component}: {score:.2%}")
        
        print("\nKey Metrics:")
        important_metrics = ["completeness", "innovation", "feasibility", "user_value", "safe_content", "technical_quality"]
        for metric_name in important_metrics:
            if metric_name in result.metrics:
                metric = result.metrics[metric_name]
                print(f"  - {metric_name}: {metric.score:.2%}")
        
        if hasattr(result, 'metadata') and 'suggestions' in result.metadata:
            print("\nActionable Suggestions:")
            for i, suggestion in enumerate(result.metadata['suggestions'], 1):
                print(f"  {i}. {suggestion}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Run all tests."""
    
    print("\n🚀 DeepEval + Reward-Kit Integration Test Suite")
    print("=" * 80)
    
    # Note about requirements
    print("\n⚠️  Note: DeepEval metrics may require:")
    print("   - API keys (OPENAI_API_KEY or DEEPEVAL_API_KEY)")
    print("   - Or local model setup")
    print("   - Install with: pip install deepeval")
    print("=" * 80)
    
    # Run tests
    test_individual_deepeval_rewards()
    test_pyclarity_features_with_deepeval()
    test_comprehensive_evaluator()
    test_pyclarity_deepeval_combined()
    
    print("\n\n✅ All tests completed!")
    print("\n💡 Next Steps:")
    print("1. Set up API keys for full DeepEval functionality")
    print("2. Integrate with PyClarity optimizer")
    print("3. Fine-tune weights based on your specific needs")
    print("4. Deploy to production with monitoring")


if __name__ == "__main__":
    main()