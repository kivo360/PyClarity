"""
Programming Paradigms FastMCP Server

Provides analysis of programming paradigms and paradigm selection guidance.
Supports OOP, functional, procedural, and multi-paradigm analysis.
"""

import json
from typing import Any, Dict, List, Optional
from fastmcp import FastMCP

from ..models.programming_paradigms import (
    ProgrammingParadigmsModel,
    ProgrammingParadigm,
    ProblemDomain,
    ParadigmCharacteristic
)

# Initialize the FastMCP app and model
app = FastMCP("Programming Paradigms")
model = ProgrammingParadigmsModel()


@app.tool()
def get_paradigm_profile(paradigm: str) -> str:
    """
    Get comprehensive profile information for a programming paradigm.
    
    Args:
        paradigm: Programming paradigm name (object_oriented, functional, procedural, etc.)
    
    Returns:
        JSON string with detailed paradigm profile
    """
    try:
        try:
            paradigm_enum = ProgrammingParadigm(paradigm.lower())
        except ValueError:
            return json.dumps({
                "error": f"Invalid paradigm: {paradigm}",
                "valid_paradigms": [p.value for p in ProgrammingParadigm]
            })
        
        profile = model.get_paradigm_profile(paradigm_enum)
        
        if not profile:
            return json.dumps({"error": f"Profile not found for paradigm: {paradigm}"})
        
        return json.dumps({
            "paradigm": profile.paradigm.value,
            "description": profile.description,
            "key_characteristics": [c.value for c in profile.key_characteristics],
            "strengths": profile.strengths,
            "weaknesses": profile.weaknesses,
            "suitable_domains": [d.value for d in profile.suitable_domains],
            "languages": profile.languages,
            "concepts": profile.concepts,
            "best_practices": profile.best_practices,
            "antipatterns": profile.antipatterns,
            "learning_curve": profile.learning_curve,
            "performance_profile": profile.performance_profile
        }, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Failed to get paradigm profile: {str(e)}"})


@app.tool()
def analyze_paradigm_suitability(
    context_description: str,
    requirements: str,
    constraints: Optional[str] = None
) -> str:
    """
    Analyze which programming paradigms are most suitable for a given context.
    
    Args:
        context_description: Description of the programming context or problem
        requirements: Comma-separated list of requirements
        constraints: Optional JSON string of constraints (performance, team_skills, etc.)
    
    Returns:
        JSON string with paradigm suitability analysis
    """
    try:
        req_list = [req.strip() for req in requirements.split(",")]
        constraint_dict = json.loads(constraints) if constraints else {}
        
        analyses = model.analyze_paradigm_suitability(
            context_description, req_list, constraint_dict
        )
        
        analyses_data = []
        for analysis in analyses:
            analyses_data.append({
                "paradigm": analysis.paradigm.value,
                "suitability_score": analysis.suitability_score,
                "suitability_rating": "Excellent" if analysis.suitability_score >= 0.8 else 
                                   "Good" if analysis.suitability_score >= 0.6 else 
                                   "Fair" if analysis.suitability_score >= 0.4 else "Poor",
                "matching_characteristics": [c.value for c in analysis.matching_characteristics],
                "benefits_for_context": analysis.benefits_for_context,
                "challenges_for_context": analysis.challenges_for_context,
                "implementation_guidance": analysis.implementation_guidance,
                "code_structure_recommendations": analysis.code_structure_recommendations,
                "performance_considerations": analysis.performance_considerations
            })
        
        return json.dumps({
            "context": context_description,
            "requirements": req_list,
            "constraints": constraint_dict,
            "paradigm_analyses": analyses_data,
            "top_recommendation": analyses_data[0] if analyses_data else None,
            "analysis_summary": f"Analyzed {len(analyses)} paradigms for suitability"
        }, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Failed to analyze paradigm suitability: {str(e)}"})


@app.tool()
def compare_paradigms(
    paradigms: str,
    comparison_criteria: str
) -> str:
    """
    Compare multiple programming paradigms across specified criteria.
    
    Args:
        paradigms: Comma-separated list of paradigms to compare
        comparison_criteria: Comma-separated list of criteria (performance, maintainability, etc.)
    
    Returns:
        JSON string with paradigm comparison results
    """
    try:
        paradigm_list = []
        for p in paradigms.split(","):
            try:
                paradigm_list.append(ProgrammingParadigm(p.strip().lower()))
            except ValueError:
                return json.dumps({
                    "error": f"Invalid paradigm: {p.strip()}",
                    "valid_paradigms": [p.value for p in ProgrammingParadigm]
                })
        
        criteria_list = [c.strip() for c in comparison_criteria.split(",")]
        
        comparison = model.compare_paradigms(paradigm_list, criteria_list)
        
        # Prepare scores data
        scores_data = {}
        for paradigm, criteria_scores in comparison.scores.items():
            scores_data[paradigm.value] = criteria_scores
        
        # Prepare decision matrix
        matrix_data = {}
        for criterion, paradigm_ratings in comparison.decision_matrix.items():
            matrix_data[criterion] = {
                p.value: rating for p, rating in paradigm_ratings.items()
            }
        
        return json.dumps({
            "comparison_id": comparison.comparison_id,
            "paradigms_compared": [p.value for p in comparison.paradigms],
            "comparison_criteria": comparison.comparison_criteria,
            "scores": scores_data,
            "recommendations": comparison.recommendations,
            "hybrid_opportunities": comparison.hybrid_opportunities,
            "decision_matrix": matrix_data,
            "summary": {
                "paradigms_count": len(comparison.paradigms),
                "criteria_count": len(comparison.comparison_criteria),
                "hybrid_options": len(comparison.hybrid_opportunities)
            }
        }, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Failed to compare paradigms: {str(e)}"})


@app.tool()
def analyze_paradigm_mix(
    primary_paradigm: str,
    secondary_paradigms: str
) -> str:
    """
    Analyze combining multiple programming paradigms in a single system.
    
    Args:
        primary_paradigm: The main paradigm to use
        secondary_paradigms: Comma-separated list of secondary paradigms
    
    Returns:
        JSON string with paradigm mix analysis
    """
    try:
        try:
            primary = ProgrammingParadigm(primary_paradigm.lower())
        except ValueError:
            return json.dumps({
                "error": f"Invalid primary paradigm: {primary_paradigm}",
                "valid_paradigms": [p.value for p in ProgrammingParadigm]
            })
        
        secondary_list = []
        for p in secondary_paradigms.split(","):
            try:
                secondary_list.append(ProgrammingParadigm(p.strip().lower()))
            except ValueError:
                return json.dumps({
                    "error": f"Invalid secondary paradigm: {p.strip()}",
                    "valid_paradigms": [p.value for p in ProgrammingParadigm]
                })
        
        mix_analysis = model.analyze_paradigm_mix(primary, secondary_list)
        
        return json.dumps({
            "mix_id": mix_analysis.mix_id,
            "primary_paradigm": mix_analysis.primary_paradigm.value,
            "secondary_paradigms": [p.value for p in mix_analysis.secondary_paradigms],
            "integration_strategy": mix_analysis.integration_strategy,
            "synergies": mix_analysis.synergies,
            "conflicts": mix_analysis.conflicts,
            "implementation_patterns": mix_analysis.implementation_patterns,
            "use_cases": mix_analysis.use_cases,
            "complexity_impact": mix_analysis.complexity_impact,
            "recommendations": [
                "Start with primary paradigm as foundation",
                "Introduce secondary paradigms gradually",
                "Establish clear boundaries between paradigm usage",
                "Document paradigm decisions and rationale"
            ]
        }, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Failed to analyze paradigm mix: {str(e)}"})


@app.tool()
def analyze_code_structure(
    code_description: str,
    language_hints: Optional[str] = None
) -> str:
    """
    Analyze code structure to identify programming paradigms in use.
    
    Args:
        code_description: Description of the code structure and organization
        language_hints: Optional comma-separated list of programming languages used
    
    Returns:
        JSON string with code structure analysis
    """
    try:
        lang_list = [lang.strip() for lang in language_hints.split(",")] if language_hints else []
        
        analysis = model.analyze_code_structure(code_description, lang_list)
        
        return json.dumps({
            "analysis_id": analysis.analysis_id,
            "detected_paradigms": [p.value for p in analysis.detected_paradigms],
            "paradigm_purity": {
                p.value: purity for p, purity in analysis.paradigm_purity.items()
            },
            "structural_patterns": analysis.structural_patterns,
            "paradigm_violations": analysis.paradigm_violations,
            "improvement_suggestions": analysis.improvement_suggestions,
            "refactoring_opportunities": analysis.refactoring_opportunities,
            "paradigm_consistency_score": analysis.paradigm_consistency_score,
            "consistency_rating": "Excellent" if analysis.paradigm_consistency_score >= 0.8 else
                                "Good" if analysis.paradigm_consistency_score >= 0.6 else
                                "Fair" if analysis.paradigm_consistency_score >= 0.4 else "Poor",
            "recommendations": [
                f"Primary paradigm appears to be: {max(analysis.paradigm_purity.keys(), key=analysis.paradigm_purity.get).value}" if analysis.paradigm_purity else "Consider adopting a clear paradigm structure",
                "Focus on improving paradigm consistency" if analysis.paradigm_consistency_score < 0.7 else "Maintain current paradigm structure"
            ]
        }, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Failed to analyze code structure: {str(e)}"})


@app.tool()
def get_paradigm_best_practices(
    paradigm: str,
    context: Optional[str] = None
) -> str:
    """
    Get best practices and guidelines for a specific programming paradigm.
    
    Args:
        paradigm: Programming paradigm name
        context: Optional context to tailor recommendations
    
    Returns:
        JSON string with best practices and guidelines
    """
    try:
        try:
            paradigm_enum = ProgrammingParadigm(paradigm.lower())
        except ValueError:
            return json.dumps({
                "error": f"Invalid paradigm: {paradigm}",
                "valid_paradigms": [p.value for p in ProgrammingParadigm]
            })
        
        profile = model.get_paradigm_profile(paradigm_enum)
        
        if not profile:
            return json.dumps({"error": f"Profile not found for paradigm: {paradigm}"})
        
        # Generate context-specific recommendations
        context_recommendations = []
        if context:
            context_lower = context.lower()
            if "beginner" in context_lower:
                context_recommendations.extend([
                    "Start with simple examples",
                    "Focus on understanding core concepts first",
                    "Practice with guided tutorials"
                ])
            elif "enterprise" in context_lower:
                context_recommendations.extend([
                    "Emphasize maintainability and scalability",
                    "Follow industry-standard patterns",
                    "Implement comprehensive testing"
                ])
            elif "performance" in context_lower:
                context_recommendations.extend([
                    "Consider performance implications of paradigm choices",
                    "Profile and optimize critical paths",
                    "Balance readability with efficiency"
                ])
        
        return json.dumps({
            "paradigm": profile.paradigm.value,
            "core_principles": [c.value for c in profile.key_characteristics],
            "best_practices": profile.best_practices,
            "antipatterns_to_avoid": profile.antipatterns,
            "context_specific_recommendations": context_recommendations,
            "learning_resources": [
                "Study the paradigm's theoretical foundations",
                "Practice with paradigm-specific languages",
                "Read code written by experts in the paradigm",
                "Implement design patterns relevant to the paradigm"
            ],
            "implementation_guidelines": [
                f"Apply {profile.paradigm.value.replace('_', ' ')} principles consistently",
                "Start simple and gradually introduce complexity",
                "Regular code reviews focusing on paradigm adherence",
                "Refactor code that violates paradigm principles"
            ]
        }, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Failed to get paradigm best practices: {str(e)}"})


# Export the FastMCP app
def get_app():
    """Get the FastMCP application instance"""
    return app


if __name__ == "__main__":
    app.run()