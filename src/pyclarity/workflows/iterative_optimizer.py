"""
Iterative Optimizer for PyClarity Workflows

Implements iterative prompting and optimization based on feedback loops.
"""

import asyncio
import logging
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class OptimizationStrategy(str, Enum):
    """Optimization strategies for iterative improvement"""
    CLARITY_ENHANCEMENT = "clarity_enhancement"
    SPECIFICITY_INCREASE = "specificity_increase"
    CONSTRAINT_REFINEMENT = "constraint_refinement"
    EXAMPLE_GENERATION = "example_generation"
    ERROR_CORRECTION = "error_correction"
    CONTEXT_EXPANSION = "context_expansion"


class IterationResult(BaseModel):
    """Result of a single iteration"""
    iteration: int
    input_quality: float
    output_quality: float
    improvements: list[str]
    strategy_used: OptimizationStrategy
    converged: bool = False


class OptimizationConfig(BaseModel):
    """Configuration for iterative optimization"""
    max_iterations: int = Field(default=5, description="Maximum optimization iterations")
    convergence_threshold: float = Field(default=0.85, description="Quality threshold for convergence")
    min_improvement: float = Field(default=0.05, description="Minimum improvement per iteration")
    strategies: list[OptimizationStrategy] = Field(
        default_factory=lambda: list(OptimizationStrategy),
        description="Available optimization strategies"
    )
    enable_parallel_strategies: bool = Field(default=False, description="Try multiple strategies in parallel")


class IterativeOptimizer:
    """
    Implements iterative optimization for prompts and tool inputs.

    Based on the iterative optimizer experiment design, this component:
    - Evaluates input/output quality
    - Applies optimization strategies
    - Iterates until convergence or max iterations
    - Learns from successful patterns
    """

    def __init__(self, config: OptimizationConfig | None = None):
        """
        Initialize the iterative optimizer.

        Args:
            config: Optimization configuration
        """
        self.config = config or OptimizationConfig()
        self.iteration_history: dict[str, list[IterationResult]] = {}
        self.successful_patterns: dict[str, list[dict[str, Any]]] = {}
        self.supported_tools = self._get_supported_tools()

    def _get_supported_tools(self) -> list[str]:
        """Get list of tools that support iterative optimization"""
        return [
            "sequential_thinking",
            "mental_models",
            "decision_framework",
            "scientific_method",
            "structured_argumentation",
            "multi_perspective_analysis",
            "iterative_validation"  # Meta!
        ]

    async def optimize_input(self, tool_name: str, input_data: dict[str, Any],
                           tool_config: dict[str, Any]) -> dict[str, Any]:
        """
        Optimize input data through iterative refinement.

        Args:
            tool_name: Name of the tool
            input_data: Original input data
            tool_config: Tool configuration

        Returns:
            Optimized input data
        """
        if tool_name not in self.supported_tools:
            return input_data

        optimized_input = input_data.copy()
        iteration_results = []

        for iteration in range(self.config.max_iterations):
            # Evaluate current input quality
            input_quality = await self._evaluate_input_quality(optimized_input, tool_name)

            # Check convergence
            if input_quality >= self.config.convergence_threshold:
                logger.info(f"Input optimization converged at iteration {iteration + 1}")
                break

            # Select optimization strategy
            strategy = self._select_strategy(input_quality, iteration_results)

            # Apply optimization
            improved_input = await self._apply_optimization(
                optimized_input, strategy, tool_name, tool_config
            )

            # Evaluate improvement
            new_quality = await self._evaluate_input_quality(improved_input, tool_name)
            improvement = new_quality - input_quality

            # Record iteration
            result = IterationResult(
                iteration=iteration + 1,
                input_quality=input_quality,
                output_quality=new_quality,
                improvements=self._identify_improvements(optimized_input, improved_input),
                strategy_used=strategy,
                converged=new_quality >= self.config.convergence_threshold
            )
            iteration_results.append(result)

            # Update if improved
            if improvement >= self.config.min_improvement:
                optimized_input = improved_input
            else:
                logger.debug(f"Iteration {iteration + 1} didn't meet minimum improvement threshold")
                break

        # Store history
        key = f"{tool_name}_{datetime.utcnow().isoformat()}"
        self.iteration_history[key] = iteration_results

        return optimized_input

    def should_iterate(self, result: dict[str, Any]) -> bool:
        """
        Determine if a result should trigger iteration.

        Args:
            result: Tool execution result

        Returns:
            Whether to iterate on the result
        """
        # Check for error indicators
        if "error" in result or "failed" in str(result).lower():
            return True

        # Check for low confidence
        if "confidence" in result and result["confidence"] < 0.7:
            return True

        # Check for incomplete results
        if "incomplete" in result or "partial" in str(result).lower():
            return True

        return False

    async def iterate_on_result(self, tool_name: str, original_input: dict[str, Any],
                               result: dict[str, Any]) -> dict[str, Any]:
        """
        Iterate on a result to improve quality.

        Args:
            tool_name: Name of the tool
            original_input: Original input that produced the result
            result: Current result to improve

        Returns:
            Improved result
        """
        # Analyze what went wrong
        issues = self._analyze_result_issues(result)

        # Create refined input based on issues
        refined_input = original_input.copy()

        for issue in issues:
            if issue == "low_confidence":
                refined_input["complexity_level"] = "complex"
                refined_input["reasoning_depth"] = refined_input.get("reasoning_depth", 5) + 2

            elif issue == "incomplete":
                refined_input["max_iterations"] = refined_input.get("max_iterations", 3) + 2

            elif issue == "unclear":
                # Add more context
                if "problem" in refined_input:
                    refined_input["problem"] = self._enhance_clarity(refined_input["problem"])
                elif "scenario" in refined_input:
                    refined_input["scenario"] = self._enhance_clarity(refined_input["scenario"])

        # Store successful refinement patterns
        self._store_pattern(tool_name, original_input, refined_input, issues)

        return refined_input

    async def _evaluate_input_quality(self, input_data: dict[str, Any], tool_name: str) -> float:
        """Evaluate the quality of input data"""
        quality_score = 0.0
        max_score = 0.0

        # Check completeness
        max_score += 1.0
        required_fields = self._get_required_fields(tool_name)
        provided_fields = sum(1 for field in required_fields if field in input_data and input_data[field])
        quality_score += provided_fields / len(required_fields) if required_fields else 1.0

        # Check clarity (simple heuristic based on length and structure)
        max_score += 1.0
        problem_text = input_data.get("problem") or input_data.get("scenario", "")
        if len(problem_text) > 50:  # Minimum length for clarity
            quality_score += 0.5
        if len(problem_text.split()) > 10:  # Word count
            quality_score += 0.3
        if any(char in problem_text for char in ["?", ".", ","]):  # Punctuation
            quality_score += 0.2

        # Check specificity
        max_score += 1.0
        specificity_keywords = ["specific", "exactly", "precisely", "must", "should", "require"]
        if any(keyword in problem_text.lower() for keyword in specificity_keywords):
            quality_score += 0.5
        if "constraints" in input_data and input_data["constraints"]:
            quality_score += 0.5

        # Check for examples
        max_score += 1.0
        if "examples" in input_data or "example" in problem_text.lower():
            quality_score += 1.0

        return quality_score / max_score if max_score > 0 else 0.0

    def _select_strategy(self, current_quality: float,
                        history: list[IterationResult]) -> OptimizationStrategy:
        """Select the best optimization strategy"""
        # If quality is very low, start with clarity
        if current_quality < 0.3:
            return OptimizationStrategy.CLARITY_ENHANCEMENT

        # If we've tried clarity, try specificity
        if history and history[-1].strategy_used == OptimizationStrategy.CLARITY_ENHANCEMENT:
            return OptimizationStrategy.SPECIFICITY_INCREASE

        # If moderate quality, add constraints
        if 0.3 <= current_quality < 0.6:
            return OptimizationStrategy.CONSTRAINT_REFINEMENT

        # If good quality, add examples
        if current_quality >= 0.6:
            return OptimizationStrategy.EXAMPLE_GENERATION

        # Default to context expansion
        return OptimizationStrategy.CONTEXT_EXPANSION

    async def _apply_optimization(self, input_data: dict[str, Any],
                                strategy: OptimizationStrategy,
                                tool_name: str, tool_config: dict[str, Any]) -> dict[str, Any]:
        """Apply an optimization strategy to input data"""
        optimized = input_data.copy()

        if strategy == OptimizationStrategy.CLARITY_ENHANCEMENT:
            # Enhance clarity of problem statement
            if "problem" in optimized:
                optimized["problem"] = self._enhance_clarity(optimized["problem"])
            elif "scenario" in optimized:
                optimized["scenario"] = self._enhance_clarity(optimized["scenario"])

        elif strategy == OptimizationStrategy.SPECIFICITY_INCREASE:
            # Add specific requirements
            problem_text = optimized.get("problem", optimized.get("scenario", ""))
            optimized["problem"] = f"{problem_text}\n\nSpecific requirements:\n" + \
                                 f"- Provide {tool_config.get('reasoning_depth', 5)} concrete steps\n" + \
                                 "- Include measurable outcomes\n" + \
                                 "- Consider edge cases"

        elif strategy == OptimizationStrategy.CONSTRAINT_REFINEMENT:
            # Add or refine constraints
            if "constraints" not in optimized:
                optimized["constraints"] = []
            if isinstance(optimized["constraints"], list):
                optimized["constraints"].extend([
                    "Time efficiency is important",
                    "Solution must be practical and implementable",
                    "Consider resource limitations"
                ])

        elif strategy == OptimizationStrategy.EXAMPLE_GENERATION:
            # Add examples to clarify intent
            problem_text = optimized.get("problem", optimized.get("scenario", ""))
            optimized["problem"] = f"{problem_text}\n\nFor example:\n" + \
                                 "- Similar to how [X] works but for [Y]\n" + \
                                 "- Should handle cases like [A], [B], and [C]"

        elif strategy == OptimizationStrategy.CONTEXT_EXPANSION:
            # Add domain context
            if "domain_context" not in optimized:
                optimized["domain_context"] = "software development"
            if "domain_expertise" not in optimized:
                optimized["domain_expertise"] = "intermediate"

        return optimized

    def _enhance_clarity(self, text: str) -> str:
        """Enhance the clarity of a text string"""
        # Simple clarity enhancements
        enhanced = text.strip()

        # Ensure it ends with proper punctuation
        if not enhanced.endswith((".", "?", "!")):
            enhanced += "."

        # Add structure if it's a long block
        if len(enhanced) > 200 and "\n" not in enhanced:
            # Try to add some structure
            sentences = enhanced.split(". ")
            if len(sentences) > 3:
                enhanced = f"{'. '.join(sentences[:2])}.\n\n{'. '.join(sentences[2:])}"

        # Add question clarification if it contains a question
        if "?" in enhanced and not enhanced.startswith(("How", "What", "Why", "When", "Where")):
            enhanced = f"Question: {enhanced}"

        return enhanced

    def _identify_improvements(self, original: dict[str, Any], improved: dict[str, Any]) -> list[str]:
        """Identify what improvements were made"""
        improvements = []

        # Check for new fields
        for key in improved:
            if key not in original:
                improvements.append(f"Added {key}")
            elif improved[key] != original.get(key):
                improvements.append(f"Enhanced {key}")

        # Check for expanded content
        for field in ["problem", "scenario"]:
            if field in original and field in improved:
                if len(str(improved[field])) > len(str(original[field])):
                    improvements.append(f"Expanded {field} content")

        return improvements

    def _analyze_result_issues(self, result: dict[str, Any]) -> list[str]:
        """Analyze issues in a result"""
        issues = []

        if "confidence" in result and result["confidence"] < 0.7:
            issues.append("low_confidence")

        if "error" in result or "failed" in str(result).lower():
            issues.append("error")

        if "incomplete" in result or len(str(result)) < 100:
            issues.append("incomplete")

        if "unclear" in str(result).lower() or "ambiguous" in str(result).lower():
            issues.append("unclear")

        return issues

    def _get_required_fields(self, tool_name: str) -> list[str]:
        """Get required fields for a tool"""
        # Basic required fields by tool
        required_fields = {
            "sequential_thinking": ["problem"],
            "mental_models": ["problem", "model_type"],
            "decision_framework": ["decision_problem"],
            "scientific_method": ["problem"],
            "structured_argumentation": ["problem"],
            "multi_perspective_analysis": ["scenario"],
            "iterative_validation": ["scenario"]
        }

        return required_fields.get(tool_name, ["problem"])

    def _store_pattern(self, tool_name: str, original: dict[str, Any],
                      refined: dict[str, Any], issues: list[str]) -> None:
        """Store successful refinement patterns"""
        if tool_name not in self.successful_patterns:
            self.successful_patterns[tool_name] = []

        pattern = {
            "timestamp": datetime.utcnow().isoformat(),
            "issues": issues,
            "original_fields": list(original.keys()),
            "refined_fields": list(refined.keys()),
            "refinements": self._identify_improvements(original, refined)
        }

        self.successful_patterns[tool_name].append(pattern)

        # Keep only recent patterns
        if len(self.successful_patterns[tool_name]) > 100:
            self.successful_patterns[tool_name] = self.successful_patterns[tool_name][-100:]
