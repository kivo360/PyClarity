#!/usr/bin/env python3
"""
Feature Evaluator Module
Provides advanced evaluation capabilities for the feature optimizer
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from collections import defaultdict
import numpy as np


@dataclass
class EvaluationCriteria:
    """Structured evaluation criteria"""
    name: str
    weight: float
    description: str
    eval_function: callable
    

class FeatureEvaluator:
    """Advanced evaluator for feature lists"""
    
    def __init__(self):
        self.criteria = self._initialize_criteria()
        self.evaluation_history = []
        self.benchmark_features = self._load_benchmark_features()
        
    def _initialize_criteria(self) -> List[EvaluationCriteria]:
        """Initialize evaluation criteria with specific functions"""
        return [
            EvaluationCriteria(
                name="completeness",
                weight=0.25,
                description="Coverage of all necessary feature categories",
                eval_function=self._evaluate_completeness
            ),
            EvaluationCriteria(
                name="clarity",
                weight=0.15,
                description="Clear, unambiguous feature descriptions",
                eval_function=self._evaluate_clarity
            ),
            EvaluationCriteria(
                name="feasibility",
                weight=0.20,
                description="Technical feasibility and resource requirements",
                eval_function=self._evaluate_feasibility
            ),
            EvaluationCriteria(
                name="user_value",
                weight=0.20,
                description="Value delivered to end users",
                eval_function=self._evaluate_user_value
            ),
            EvaluationCriteria(
                name="technical_coherence",
                weight=0.10,
                description="Dependencies and integration consistency",
                eval_function=self._evaluate_coherence
            ),
            EvaluationCriteria(
                name="innovation",
                weight=0.10,
                description="Novel approaches and differentiation",
                eval_function=self._evaluate_innovation
            )
        ]
        
    def _load_benchmark_features(self) -> Dict[str, Any]:
        """Load benchmark features from successful products"""
        # In real implementation, this would load from a curated dataset
        return {
            "essential_categories": ["core", "supporting", "integration", "analytics"],
            "min_features_per_category": {
                "core": 3,
                "supporting": 2,
                "integration": 1,
                "analytics": 1
            },
            "required_capabilities": [
                "visual_design",
                "validation",
                "export",
                "api",
                "monitoring"
            ],
            "quality_keywords": [
                "intuitive", "automated", "real-time", "scalable",
                "secure", "customizable", "integrated"
            ]
        }
    
    def evaluate(self, features: Dict[str, List[Dict[str, Any]]], 
                 iteration: int = 0) -> Dict[str, Any]:
        """Comprehensive feature evaluation"""
        
        # Run all evaluation criteria
        scores = {}
        detailed_feedback = {}
        
        for criterion in self.criteria:
            score, feedback = criterion.eval_function(features)
            scores[criterion.name] = score
            detailed_feedback[criterion.name] = feedback
            
        # Calculate weighted overall score
        overall_score = sum(
            scores[c.name] * c.weight 
            for c in self.criteria
        )
        
        # Generate improvement suggestions
        suggestions = self._generate_suggestions(features, scores, detailed_feedback)
        
        # Compare with previous iterations
        improvement_rate = self._calculate_improvement_rate(overall_score)
        
        evaluation_result = {
            "iteration": iteration,
            "scores": scores,
            "overall_score": overall_score,
            "detailed_feedback": detailed_feedback,
            "suggestions": suggestions,
            "improvement_rate": improvement_rate,
            "feature_quality_matrix": self._generate_quality_matrix(features)
        }
        
        self.evaluation_history.append(evaluation_result)
        
        return evaluation_result
    
    def _evaluate_completeness(self, features: Dict[str, List[Dict[str, Any]]]) -> Tuple[float, str]:
        """Evaluate feature completeness"""
        score = 0.0
        feedback_items = []
        
        # Check category coverage
        required_categories = self.benchmark_features["essential_categories"]
        existing_categories = set(features.keys())
        missing_categories = set(required_categories) - existing_categories
        
        category_score = len(existing_categories & set(required_categories)) / len(required_categories)
        score += category_score * 0.3
        
        if missing_categories:
            feedback_items.append(f"Missing categories: {', '.join(missing_categories)}")
        
        # Check feature count per category
        for category, min_count in self.benchmark_features["min_features_per_category"].items():
            if category in features:
                actual_count = len(features[category])
                if actual_count >= min_count:
                    score += 0.1
                else:
                    feedback_items.append(f"{category} needs {min_count - actual_count} more features")
        
        # Check required capabilities coverage
        all_feature_names = []
        for category in features.values():
            all_feature_names.extend([f["name"].lower() for f in category])
        
        capability_coverage = 0
        for capability in self.benchmark_features["required_capabilities"]:
            if any(capability in name for name in all_feature_names):
                capability_coverage += 1
                
        capability_score = capability_coverage / len(self.benchmark_features["required_capabilities"])
        score += capability_score * 0.3
        
        feedback = " | ".join(feedback_items) if feedback_items else "Good coverage"
        
        return min(score, 1.0), feedback
    
    def _evaluate_clarity(self, features: Dict[str, List[Dict[str, Any]]]) -> Tuple[float, str]:
        """Evaluate description clarity"""
        total_features = 0
        clarity_scores = []
        unclear_features = []
        
        for category, feature_list in features.items():
            for feature in feature_list:
                total_features += 1
                desc = feature.get("description", "")
                
                # Check description length
                if len(desc) < 20:
                    clarity_scores.append(0.3)
                    unclear_features.append(f"{feature['name']}: too brief")
                elif len(desc) > 200:
                    clarity_scores.append(0.7)
                    unclear_features.append(f"{feature['name']}: too verbose")
                else:
                    clarity_scores.append(1.0)
                    
                # Check for quality keywords
                quality_keyword_count = sum(
                    1 for keyword in self.benchmark_features["quality_keywords"]
                    if keyword in desc.lower()
                )
                if quality_keyword_count > 0:
                    clarity_scores[-1] = min(clarity_scores[-1] + 0.1 * quality_keyword_count, 1.0)
        
        avg_clarity = np.mean(clarity_scores) if clarity_scores else 0.0
        
        feedback = "Clear descriptions overall"
        if unclear_features:
            feedback = f"Unclear: {'; '.join(unclear_features[:3])}"
            if len(unclear_features) > 3:
                feedback += f" and {len(unclear_features) - 3} more"
                
        return avg_clarity, feedback
    
    def _evaluate_feasibility(self, features: Dict[str, List[Dict[str, Any]]]) -> Tuple[float, str]:
        """Evaluate technical feasibility"""
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
                complexity = feature.get("complexity", "medium")
                risk = feature.get("technical_risk", 3)
                
                complexity_score = complexity_scores.get(complexity, 0.5)
                risk_score = risk_scores.get(risk, 0.5)
                
                feature_feasibility = (complexity_score + risk_score) / 2
                feasibility_scores.append(feature_feasibility)
                
                if feature_feasibility < 0.5:
                    high_risk_features.append(f"{feature['name']} (risk: {risk}, complexity: {complexity})")
        
        avg_feasibility = np.mean(feasibility_scores) if feasibility_scores else 0.0
        
        feedback = "Good technical feasibility"
        if high_risk_features:
            feedback = f"High risk: {', '.join(high_risk_features[:2])}"
            
        return avg_feasibility, feedback
    
    def _evaluate_user_value(self, features: Dict[str, List[Dict[str, Any]]]) -> Tuple[float, str]:
        """Evaluate user value delivery"""
        value_scores = []
        high_value_features = []
        low_value_features = []
        
        for category, feature_list in features.items():
            for feature in feature_list:
                user_value = feature.get("user_value", 5)
                normalized_value = user_value / 10.0
                value_scores.append(normalized_value)
                
                if user_value >= 8:
                    high_value_features.append(feature["name"])
                elif user_value <= 4:
                    low_value_features.append(feature["name"])
        
        avg_value = np.mean(value_scores) if value_scores else 0.0
        
        # Bonus for having multiple high-value features
        if len(high_value_features) >= 3:
            avg_value = min(avg_value + 0.1, 1.0)
            
        feedback_parts = []
        if high_value_features:
            feedback_parts.append(f"High value: {', '.join(high_value_features[:2])}")
        if low_value_features:
            feedback_parts.append(f"Low value: {', '.join(low_value_features[:2])}")
            
        feedback = " | ".join(feedback_parts) if feedback_parts else "Balanced value distribution"
        
        return avg_value, feedback
    
    def _evaluate_coherence(self, features: Dict[str, List[Dict[str, Any]]]) -> Tuple[float, str]:
        """Evaluate technical coherence and dependencies"""
        all_feature_ids = set()
        dependency_issues = []
        
        # Collect all feature IDs
        for category, feature_list in features.items():
            for feature in feature_list:
                all_feature_ids.add(feature["id"])
        
        # Check dependencies
        valid_dependencies = 0
        total_dependencies = 0
        
        for category, feature_list in features.items():
            for feature in feature_list:
                deps = feature.get("dependencies", [])
                total_dependencies += len(deps)
                
                for dep in deps:
                    if dep in all_feature_ids:
                        valid_dependencies += 1
                    else:
                        dependency_issues.append(f"{feature['id']} depends on missing {dep}")
        
        coherence_score = valid_dependencies / total_dependencies if total_dependencies > 0 else 1.0
        
        # Check for circular dependencies (simplified)
        if self._has_circular_dependencies(features):
            coherence_score *= 0.8
            dependency_issues.append("Potential circular dependencies detected")
            
        feedback = "Good dependency structure"
        if dependency_issues:
            feedback = f"Issues: {'; '.join(dependency_issues[:2])}"
            
        return coherence_score, feedback
    
    def _evaluate_innovation(self, features: Dict[str, List[Dict[str, Any]]]) -> Tuple[float, str]:
        """Evaluate innovation and differentiation"""
        innovative_keywords = [
            "ai-powered", "intelligent", "automated", "predictive",
            "adaptive", "self-", "machine learning", "neural",
            "revolutionary", "breakthrough", "novel", "unique"
        ]
        
        innovation_count = 0
        innovative_features = []
        
        for category, feature_list in features.items():
            for feature in feature_list:
                name = feature.get("name", "").lower()
                desc = feature.get("description", "").lower()
                
                if any(keyword in name + desc for keyword in innovative_keywords):
                    innovation_count += 1
                    innovative_features.append(feature["name"])
        
        total_features = sum(len(features[cat]) for cat in features)
        innovation_ratio = innovation_count / total_features if total_features > 0 else 0
        
        # Target 30-50% innovative features
        if innovation_ratio < 0.3:
            score = innovation_ratio / 0.3
            feedback = "Needs more innovative features"
        elif innovation_ratio > 0.5:
            score = 1.0 - (innovation_ratio - 0.5) * 0.5
            feedback = "Good balance of innovation"
        else:
            score = 1.0
            feedback = f"Innovative: {', '.join(innovative_features[:3])}"
            
        return score, feedback
    
    def _has_circular_dependencies(self, features: Dict[str, List[Dict[str, Any]]]) -> bool:
        """Check for circular dependencies (simplified)"""
        # Build dependency graph
        graph = defaultdict(list)
        
        for category, feature_list in features.items():
            for feature in feature_list:
                feature_id = feature["id"]
                deps = feature.get("dependencies", [])
                graph[feature_id].extend(deps)
        
        # Convert to regular dict to avoid modification during iteration
        graph = dict(graph)
        
        # Simple cycle detection (DFS)
        visited = set()
        rec_stack = set()
        
        def has_cycle(node):
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    if has_cycle(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
                    
            rec_stack.remove(node)
            return False
        
        # Get all nodes to check
        all_nodes = set(graph.keys())
        for deps in graph.values():
            all_nodes.update(deps)
        
        for node in all_nodes:
            if node not in visited:
                if has_cycle(node):
                    return True
                    
        return False
    
    def _generate_suggestions(self, features: Dict[str, List[Dict[str, Any]]], 
                             scores: Dict[str, float], 
                             feedback: Dict[str, str]) -> List[str]:
        """Generate actionable improvement suggestions"""
        suggestions = []
        
        # Priority 1: Address lowest scoring areas
        sorted_scores = sorted(scores.items(), key=lambda x: x[1])
        
        for criterion, score in sorted_scores[:2]:  # Focus on 2 worst areas
            if score < 0.7:
                if criterion == "completeness":
                    suggestions.append("Add more features to under-represented categories")
                elif criterion == "clarity":
                    suggestions.append("Improve feature descriptions with specific use cases")
                elif criterion == "feasibility":
                    suggestions.append("Reduce technical complexity or break down high-risk features")
                elif criterion == "user_value":
                    suggestions.append("Focus on features that directly solve user pain points")
                elif criterion == "coherence":
                    suggestions.append("Review and fix dependency relationships")
                elif criterion == "innovation":
                    suggestions.append("Add AI-powered or automated capabilities")
        
        # Priority 2: Specific improvements based on analysis
        total_features = sum(len(features[cat]) for cat in features)
        if total_features < 15:
            suggestions.append(f"Add {15 - total_features} more features for comprehensive coverage")
            
        if "core" in features and len(features["core"]) < 5:
            suggestions.append("Expand core features - these are your main value drivers")
            
        return suggestions
    
    def _calculate_improvement_rate(self, current_score: float) -> float:
        """Calculate improvement rate from history"""
        if len(self.evaluation_history) < 2:
            return 0.0
            
        previous_score = self.evaluation_history[-1]["overall_score"]
        improvement = (current_score - previous_score) / previous_score if previous_score > 0 else 0
        
        return improvement
    
    def _generate_quality_matrix(self, features: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Generate a quality matrix for all features"""
        matrix = {}
        
        for category, feature_list in features.items():
            matrix[category] = {}
            for feature in feature_list:
                quality_indicators = {
                    "description_quality": len(feature.get("description", "")) / 100,  # Normalized
                    "dependency_count": len(feature.get("dependencies", [])),
                    "user_value": feature.get("user_value", 5) / 10,
                    "risk_level": (6 - feature.get("technical_risk", 3)) / 5,  # Inverted
                    "priority_score": {"high": 1.0, "medium": 0.6, "low": 0.3}.get(feature.get("priority", "medium"), 0.5)
                }
                matrix[category][feature["id"]] = quality_indicators
                
        return matrix
    
    def generate_report(self, evaluation_result: Dict[str, Any]) -> str:
        """Generate human-readable evaluation report"""
        report = f"""
# Feature Evaluation Report - Iteration {evaluation_result['iteration']}

## Overall Score: {evaluation_result['overall_score']:.2%}
Improvement Rate: {evaluation_result['improvement_rate']:+.2%}

## Detailed Scores:
"""
        for criterion in self.criteria:
            score = evaluation_result['scores'][criterion.name]
            feedback = evaluation_result['detailed_feedback'][criterion.name]
            report += f"- **{criterion.name.title()}** ({criterion.weight:.0%} weight): {score:.2%}\n"
            report += f"  - {feedback}\n"
            
        report += "\n## Top Suggestions:\n"
        for i, suggestion in enumerate(evaluation_result['suggestions'], 1):
            report += f"{i}. {suggestion}\n"
            
        return report


if __name__ == "__main__":
    # Test the evaluator
    evaluator = FeatureEvaluator()
    
    # Load current features
    with open("features.json", "r") as f:
        data = json.load(f)
        features = data.get("features", {})
        iteration = data.get("iteration", 0)
    
    # Evaluate
    result = evaluator.evaluate(features, iteration)
    
    # Print report
    print(evaluator.generate_report(result))
    
    # Save detailed results
    with open("evaluation_report.json", "w") as f:
        json.dump(result, f, indent=2)