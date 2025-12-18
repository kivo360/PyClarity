#!/usr/bin/env python3
"""
PyClarity MCP Server
Production-ready FastMCP server with PyClarity cognitive tools.
"""

from fastmcp import FastMCP

# Import cognitive analyzers
from pyclarity.tools.sequential_thinking.analyzer import SequentialThinkingAnalyzer
from pyclarity.tools.sequential_thinking.models import SequentialThinkingContext, ComplexityLevel
from pyclarity.tools.mental_models.analyzer import MentalModelsAnalyzer  
from pyclarity.tools.mental_models.models import MentalModelContext, MentalModelType
from pyclarity.tools.decision_framework.analyzer import DecisionFrameworkAnalyzer
from pyclarity.tools.decision_framework.models import DecisionFrameworkContext, DecisionCriteria, DecisionOption

# Create the FastMCP server instance
app = FastMCP("PyClarity")

# Initialize cognitive analyzers
sequential_analyzer = SequentialThinkingAnalyzer()
mental_models_analyzer = MentalModelsAnalyzer()
decision_analyzer = DecisionFrameworkAnalyzer()


@app.tool
async def sequential_thinking(problem: str, complexity_level: str = "moderate", reasoning_depth: int = 5) -> dict:
    """
    Analyze a problem using sequential thinking methodology with step-by-step reasoning.
    
    Args:
        problem: The problem or question to analyze
        complexity_level: One of 'simple', 'moderate', 'complex', 'very_complex'
        reasoning_depth: Maximum number of reasoning steps (3-20)
        
    Returns:
        Structured analysis with reasoning chain, branches, and revisions
    """
    try:
        context = SequentialThinkingContext(
            problem=problem,
            complexity_level=ComplexityLevel(complexity_level),
            reasoning_depth=max(3, min(20, reasoning_depth))
        )
        result = await sequential_analyzer.analyze(context)
        return result.model_dump()
    except Exception as e:
        return {"error": f"Sequential thinking analysis failed: {str(e)}"}


@app.tool 
async def mental_models(problem: str, complexity_level: str = "moderate", model_type: str = "first_principles") -> dict:
    """
    Apply mental models framework to analyze a problem from multiple cognitive perspectives.
    
    Args:
        problem: The problem or situation to analyze
        complexity_level: One of 'simple', 'moderate', 'complex', 'very_complex'
        model_type: One of 'first_principles', 'opportunity_cost', 'error_propagation', 'rubber_duck', 'pareto_principle'
        
    Returns:
        Analysis using different mental models and cognitive frameworks
    """
    try:
        context = MentalModelContext(
            problem=problem,
            complexity_level=ComplexityLevel(complexity_level),
            model_type=MentalModelType(model_type)
        )
        result = await mental_models_analyzer.analyze(context)
        return result.model_dump()
    except Exception as e:
        return {"error": f"Mental models analysis failed: {str(e)}"}


@app.tool
async def decision_framework(
    problem: str, 
    complexity_level: str = "moderate",
    criteria_names: list[str] = ["cost", "time", "quality"], 
    option_names: list[str] = ["option_a", "option_b", "option_c"]
) -> dict:
    """
    Analyze a decision using structured decision-making framework.
    
    Args:
        problem: The decision or problem to analyze
        complexity_level: One of 'simple', 'moderate', 'complex', 'very_complex'
        criteria_names: List of decision criteria (default: cost, time, quality)
        option_names: List of options to evaluate (default: option_a, option_b, option_c)
        
    Returns:
        Structured decision analysis with criteria, alternatives, and recommendations
    """
    try:
        # Create criteria with default weights
        criteria = []
        for i, name in enumerate(criteria_names):
            criteria.append(DecisionCriteria(
                name=name,
                weight=1.0 / len(criteria_names),  # Equal weights by default
                description=f"Analysis of {name} for this decision"
            ))
        
        # Create options with default scores
        options = []
        for name in option_names:
            # Generate default scores for each criterion (random values for demonstration)
            scores = {criteria_name: 0.5 for criteria_name in criteria_names}  # Neutral scores
            options.append(DecisionOption(
                name=name,
                description=f"Analysis of {name} option",
                scores=scores
            ))
        
        context = DecisionFrameworkContext(
            problem=problem,
            complexity_level=ComplexityLevel(complexity_level),
            criteria=criteria,
            options=options,
            include_risk_analysis=False  # Disable risk analysis for simplicity
        )
        result = await decision_analyzer.analyze(context)
        return result.model_dump()
    except Exception as e:
        return {"error": f"Decision framework analysis failed: {str(e)}"}


@app.tool
def server_info() -> dict:
    """Get information about the PyClarity server and available tools."""
    return {
        "server": "PyClarity MCP Server",
        "version": "2.0.0",
        "description": "Cognitive tools for enhanced reasoning and decision-making",
        "tools": [
            {
                "name": "sequential_thinking",
                "description": "Step-by-step problem analysis with branching and revision",
                "complexity_levels": ["simple", "moderate", "complex", "very_complex"]
            },
            {
                "name": "mental_models", 
                "description": "Multi-perspective analysis using cognitive frameworks",
                "complexity_levels": ["simple", "moderate", "complex", "very_complex"]
            },
            {
                "name": "decision_framework",
                "description": "Structured decision-making with criteria and alternatives",
                "complexity_levels": ["simple", "moderate", "complex", "very_complex"]
            }
        ]
    }


if __name__ == "__main__":
    print("🧠 Starting PyClarity MCP Server...")
    print("Available cognitive tools:")
    print("  • sequential_thinking - Step-by-step reasoning")
    print("  • mental_models - Multi-perspective analysis") 
    print("  • decision_framework - Structured decision-making")
    print("  • server_info - Server information")
    app.run()