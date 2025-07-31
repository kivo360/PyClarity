"""
Design Patterns FastMCP Server

Provides software architecture patterns and design principle guidance through FastMCP tools.
Supports pattern selection, architectural decisions, and design quality analysis.
"""

import json
from typing import Any, Dict, List, Optional
from fastmcp import FastMCP

from ..models.design_patterns import (
    DesignPatternsModel,
    PatternCategory,
    DesignPrinciple,
    PatternComplexity
)

# Initialize the FastMCP app and model
app = FastMCP("Design Patterns")
model = DesignPatternsModel()


@app.tool()
def get_pattern_by_id(pattern_id: str) -> str:
    """
    Retrieve detailed information about a specific design pattern.
    
    Args:
        pattern_id: Unique identifier for the design pattern
    
    Returns:
        JSON string with pattern details or error if not found
    """
    try:
        pattern = model.get_pattern_by_id(pattern_id)
        
        if not pattern:
            return json.dumps({"error": f"Pattern '{pattern_id}' not found"})
        
        return json.dumps({
            "pattern_id": pattern.pattern_id,
            "name": pattern.name,
            "category": pattern.category.value,
            "description": pattern.description,
            "intent": pattern.intent,
            "applicability": pattern.applicability,
            "structure": pattern.structure,
            "participants": pattern.participants,
            "collaborations": pattern.collaborations,
            "benefits": pattern.consequences.get("benefits", []),
            "drawbacks": pattern.consequences.get("drawbacks", []),
            "implementation_notes": pattern.implementation_notes,
            "related_patterns": pattern.related_patterns,
            "complexity": pattern.complexity.value,
            "principles_supported": [p.value for p in pattern.principles_supported]
        }, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Failed to retrieve pattern: {str(e)}"})


@app.tool()
def find_patterns_by_category(category: str) -> str:
    """
    Find all design patterns in a specific category.
    
    Args:
        category: Pattern category (creational, structural, behavioral, etc.)
    
    Returns:
        JSON string with list of patterns in the category
    """
    try:
        try:
            cat = PatternCategory(category.lower())
        except ValueError:
            return json.dumps({"error": f"Invalid category: {category}. Valid categories: {[c.value for c in PatternCategory]}"})
        
        patterns = model.find_patterns_by_category(cat)
        
        patterns_data = []
        for pattern in patterns:
            patterns_data.append({
                "pattern_id": pattern.pattern_id,
                "name": pattern.name,
                "description": pattern.description,
                "complexity": pattern.complexity.value,
                "principles_supported": [p.value for p in pattern.principles_supported]
            })
        
        return json.dumps({
            "category": category,
            "pattern_count": len(patterns),
            "patterns": patterns_data
        }, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Failed to find patterns by category: {str(e)}"})


@app.tool()
def recommend_pattern(
    problem_description: str,
    requirements: str,
    constraints: Optional[str] = None
) -> str:
    """
    Recommend design patterns based on problem context and requirements.
    
    Args:
        problem_description: Description of the problem to solve
        requirements: Comma-separated list of requirements
        constraints: Optional JSON string of constraints (performance, complexity, etc.)
    
    Returns:
        JSON string with pattern recommendations ranked by suitability
    """
    try:
        req_list = [req.strip() for req in requirements.split(",")]
        constraint_dict = json.loads(constraints) if constraints else {}
        
        recommendations = model.recommend_pattern(
            problem_description, req_list, constraint_dict
        )
        
        recommendations_data = []
        for rec in recommendations:
            recommendations_data.append({
                "pattern_id": rec.pattern.pattern_id,
                "pattern_name": rec.pattern.name,
                "fit_score": rec.fit_score,
                "recommendation": rec.recommendation,
                "benefits": rec.benefits,
                "drawbacks": rec.drawbacks,
                "implementation_effort": rec.implementation_effort.value,
                "required_tools": rec.required_tools,
                "prerequisites": rec.prerequisites,
                "alternatives": rec.alternatives
            })
        
        return json.dumps({
            "problem_description": problem_description,
            "requirements": req_list,
            "recommendations": recommendations_data,
            "top_recommendation": recommendations_data[0] if recommendations_data else None
        }, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Failed to recommend patterns: {str(e)}"})


@app.tool()
def evaluate_design_principles(
    code_description: str,
    patterns_used: str
) -> str:
    """
    Evaluate adherence to design principles in code or design.
    
    Args:
        code_description: Description of the code or design
        patterns_used: Comma-separated list of pattern IDs used
    
    Returns:
        JSON string with principle adherence scores and analysis
    """
    try:
        pattern_list = [p.strip() for p in patterns_used.split(",") if p.strip()]
        
        adherence = model.evaluate_design_principles(code_description, pattern_list)
        
        principle_scores = []
        total_score = 0
        for principle, score in adherence.items():
            principle_scores.append({
                "principle": principle.value,
                "score": score,
                "rating": "Excellent" if score >= 0.8 else "Good" if score >= 0.6 else "Fair" if score >= 0.4 else "Poor"
            })
            total_score += score
        
        average_score = total_score / len(adherence) if adherence else 0
        
        return json.dumps({
            "code_description": code_description,
            "patterns_used": pattern_list,
            "principle_adherence": principle_scores,
            "average_score": average_score,
            "overall_rating": "Excellent" if average_score >= 0.8 else "Good" if average_score >= 0.6 else "Fair" if average_score >= 0.4 else "Poor",
            "recommendations": [
                f"Focus on improving {p['principle']}" 
                for p in principle_scores if p['score'] < 0.6
            ]
        }, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Failed to evaluate design principles: {str(e)}"})


@app.tool()
def create_architectural_decision(
    title: str,
    context: str,
    problem: str,
    decision: str,
    alternatives: str,
    patterns_involved: Optional[str] = None
) -> str:
    """
    Create an architectural decision record (ADR).
    
    Args:
        title: Title of the architectural decision
        context: Context and background information
        problem: Problem statement being addressed
        decision: The decision that was made
        alternatives: Comma-separated list of alternatives considered
        patterns_involved: Optional comma-separated list of patterns involved
    
    Returns:
        JSON string with the created architectural decision record
    """
    try:
        alt_list = [alt.strip() for alt in alternatives.split(",")]
        pattern_list = [p.strip() for p in patterns_involved.split(",")] if patterns_involved else []
        
        adr = model.create_architectural_decision(
            title, context, problem, decision, alt_list, pattern_list
        )
        
        return json.dumps({
            "decision_id": adr.decision_id,
            "title": adr.title,
            "context": adr.context,
            "problem_statement": adr.problem_statement,
            "decision": adr.decision,
            "status": adr.status,
            "alternatives_considered": adr.alternatives_considered,
            "patterns_involved": adr.patterns_involved,
            "principles_applied": [p.value for p in adr.principles_applied],
            "decision_date": adr.decision_date,
            "stakeholders": adr.stakeholders,
            "next_steps": [
                "Review and approve the decision",
                "Communicate to all stakeholders",
                "Begin implementation planning"
            ]
        }, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Failed to create architectural decision: {str(e)}"})


@app.tool()
def analyze_pattern_combinations(
    pattern_ids: str
) -> str:
    """
    Analyze how multiple design patterns work together.
    
    Args:
        pattern_ids: Comma-separated list of pattern IDs to analyze
    
    Returns:
        JSON string with pattern combination analysis
    """
    try:
        pattern_list = [p.strip() for p in pattern_ids.split(",")]
        
        if len(pattern_list) < 2:
            return json.dumps({"error": "At least 2 patterns required for combination analysis"})
        
        combinations = model.analyze_pattern_combinations(pattern_list)
        
        combinations_data = []
        for combo in combinations:
            combinations_data.append({
                "combination_id": combo.combination_id,
                "patterns": [p.name for p in combo.patterns],
                "interaction_type": combo.interaction_type,
                "combined_benefits": combo.combined_benefits,
                "potential_conflicts": combo.potential_conflicts,
                "integration_complexity": combo.integration_complexity.value,
                "usage_scenarios": combo.usage_scenarios,
                "best_practices": combo.best_practices
            })
        
        return json.dumps({
            "patterns_analyzed": pattern_list,
            "combinations_found": len(combinations),
            "combinations": combinations_data,
            "analysis_summary": f"Analyzed {len(combinations)} pattern combinations"
        }, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Failed to analyze pattern combinations: {str(e)}"})


@app.tool()
def perform_design_analysis(
    system_description: str,
    existing_patterns: Optional[str] = None,
    requirements: Optional[str] = None
) -> str:
    """
    Perform comprehensive design pattern analysis of a system.
    
    Args:
        system_description: Description of the system or codebase
        existing_patterns: Optional comma-separated list of existing patterns
        requirements: Optional comma-separated list of requirements
    
    Returns:
        JSON string with comprehensive design analysis
    """
    try:
        existing_list = [p.strip() for p in existing_patterns.split(",")] if existing_patterns else []
        req_list = [r.strip() for r in requirements.split(",")] if requirements else []
        
        analysis = model.perform_design_analysis(system_description, existing_list, req_list)
        
        # Prepare pattern applications data
        applications_data = []
        for app in analysis.pattern_applications:
            applications_data.append({
                "pattern_name": app.pattern.name,
                "fit_score": app.fit_score,
                "recommendation": app.recommendation,
                "benefits": app.benefits[:3],  # Top 3 benefits
                "implementation_effort": app.implementation_effort.value
            })
        
        # Prepare pattern combinations data
        combinations_data = []
        for combo in analysis.pattern_combinations:
            combinations_data.append({
                "patterns": [p.name for p in combo.patterns],
                "interaction_type": combo.interaction_type,
                "complexity": combo.integration_complexity.value
            })
        
        return json.dumps({
            "analysis_id": analysis.analysis_id,
            "system_description": system_description,
            "identified_patterns": [p.name for p in analysis.identified_patterns],
            "design_quality_score": analysis.design_quality_score,
            "quality_rating": "Excellent" if analysis.design_quality_score >= 0.8 else "Good" if analysis.design_quality_score >= 0.6 else "Fair" if analysis.design_quality_score >= 0.4 else "Poor",
            "pattern_recommendations": applications_data,
            "pattern_combinations": combinations_data,
            "principle_adherence": {
                principle.value: score for principle, score in analysis.principle_adherence.items()
            },
            "improvement_suggestions": analysis.improvement_suggestions,
            "summary": {
                "patterns_identified": len(analysis.identified_patterns),
                "recommendations_count": len(analysis.pattern_applications),
                "combinations_analyzed": len(analysis.pattern_combinations),
                "overall_health": "Good" if analysis.design_quality_score > 0.6 else "Needs Improvement"
            }
        }, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Failed to perform design analysis: {str(e)}"})


# Export the FastMCP app
def get_app():
    """Get the FastMCP application instance"""
    return app


if __name__ == "__main__":
    app.run()