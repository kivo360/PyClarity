"""
Prompt Template Manager for PyClarity Workflows

Manages prompt templates, dynamic rewriting, and prompt optimization.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class PromptTemplate(BaseModel):
    """A reusable prompt template"""
    name: str
    description: str
    template: str
    variables: list[str] = Field(default_factory=list)
    examples: list[dict[str, Any]] = Field(default_factory=list)
    version: str = "1.0.0"
    tags: list[str] = Field(default_factory=list)

    def apply(self, variables: dict[str, Any]) -> str:
        """Apply variables to the template"""
        # Use safe substitution that leaves missing variables as placeholders
        from string import Template

        # Convert Python format string to Template format
        template_str = self.template.replace('{', '${')
        template = Template(template_str)

        try:
            result = template.safe_substitute(**variables)
            # Convert back to Python format for any remaining placeholders
            return result.replace('${', '{')
        except Exception as e:
            logger.warning(f"Error applying template {self.name}: {e}")
            return self.template


class PromptLibrary(BaseModel):
    """Collection of prompt templates organized by category"""
    business_frameworks: dict[str, PromptTemplate] = Field(default_factory=dict)
    technical_analysis: dict[str, PromptTemplate] = Field(default_factory=dict)
    copywriting_formulas: dict[str, PromptTemplate] = Field(default_factory=dict)
    ux_ui_patterns: dict[str, PromptTemplate] = Field(default_factory=dict)
    cognitive_tools: dict[str, PromptTemplate] = Field(default_factory=dict)
    custom: dict[str, PromptTemplate] = Field(default_factory=dict)


class PromptManager:
    """
    Manages prompt templates and dynamic prompt optimization.

    Integrates with the workflow engine to provide:
    - Prompt template library management
    - Dynamic prompt rewriting
    - Context-aware prompt selection
    - Prompt performance tracking
    """

    def __init__(self, templates_dir: Path | None = None):
        """
        Initialize prompt manager.

        Args:
            templates_dir: Directory containing prompt template files
        """
        self.templates_dir = templates_dir or Path("prompts")
        self.library = PromptLibrary()
        self.performance_metrics: dict[str, dict[str, Any]] = {}
        self._builtin_templates = self._initialize_builtin_templates()

    async def load_templates(self) -> None:
        """Load prompt templates from disk and builtins"""
        # Load built-in templates
        for category, templates in self._builtin_templates.items():
            category_dict = getattr(self.library, category, {})
            category_dict.update(templates)
            setattr(self.library, category, category_dict)

        # Load custom templates from disk if directory exists
        if self.templates_dir.exists():
            await self._load_custom_templates()

        logger.info(f"Loaded {self._count_templates()} prompt templates")

    def has_template(self, tool_name: str) -> bool:
        """Check if a template exists for a tool"""
        # Check cognitive tools first
        if tool_name in self.library.cognitive_tools:
            return True

        # Check other categories
        for category in ["business_frameworks", "technical_analysis", "custom"]:
            category_dict = getattr(self.library, category, {})
            if tool_name in category_dict:
                return True

        return False

    async def apply_template(self, tool_name: str, input_data: dict[str, Any]) -> dict[str, Any]:
        """
        Apply a prompt template to enhance input data.

        Args:
            tool_name: Name of the tool
            input_data: Original input data

        Returns:
            Enhanced input data with applied templates
        """
        template = self._find_template(tool_name)
        if not template:
            return input_data

        # Create a copy to avoid modifying the original
        enhanced_data = input_data.copy()

        # Apply template to problem/scenario field
        if "problem" in enhanced_data:
            enhanced_problem = template.apply({
                "original_problem": enhanced_data["problem"],
                **enhanced_data
            })
            enhanced_data["problem"] = enhanced_problem

        elif "scenario" in enhanced_data:
            enhanced_scenario = template.apply({
                "original_scenario": enhanced_data["scenario"],
                **enhanced_data
            })
            enhanced_data["scenario"] = enhanced_scenario

        # Track template usage
        self._track_usage(tool_name, template.name)

        return enhanced_data

    def get_template_suggestions(self, context: dict[str, Any]) -> list[str]:
        """Get suggested templates based on context"""
        suggestions = []

        # Analyze context for relevant templates
        if "product" in str(context).lower():
            suggestions.extend(["lean_startup", "jobs_to_be_done", "value_proposition"])

        if "technical" in str(context).lower():
            suggestions.extend(["first_principles", "system_design", "debugging_systematic"])

        if "decision" in str(context).lower():
            suggestions.extend(["decision_matrix", "pros_cons", "impact_effort"])

        return suggestions

    def _initialize_builtin_templates(self) -> dict[str, dict[str, PromptTemplate]]:
        """Initialize built-in prompt templates"""
        return {
            "cognitive_tools": {
                "sequential_thinking": PromptTemplate(
                    name="sequential_thinking_enhanced",
                    description="Enhanced sequential thinking with chain-of-thought",
                    template="""
{original_problem}

Please approach this step-by-step with the following structure:
1. **Initial Analysis**: Break down the core components
2. **Step-by-Step Reasoning**: Show each logical step clearly
3. **Branch Points**: Identify where alternative paths exist
4. **Validation**: Check reasoning at each step
5. **Synthesis**: Combine insights into actionable conclusions

Focus on clarity and logical flow throughout.
""",
                    variables=["original_problem"],
                    tags=["cognitive", "reasoning", "step-by-step"]
                ),

                "mental_models": PromptTemplate(
                    name="mental_models_structured",
                    description="Structured mental models analysis",
                    template="""
Analyze the following using the {model_type} mental model:

{original_problem}

Apply the model with these considerations:
- Core principles of {model_type}
- Domain context: {domain_expertise}
- Known constraints: {constraints}
- Expected depth: {complexity_level}

Provide concrete insights and actionable recommendations.
""",
                    variables=["original_problem", "model_type", "domain_expertise", "constraints", "complexity_level"],
                    tags=["cognitive", "mental-models", "analysis"]
                ),
            },

            "business_frameworks": {
                "lean_startup": PromptTemplate(
                    name="lean_startup_validation",
                    description="Lean Startup methodology for rapid validation",
                    template="""
Apply Lean Startup methodology to: {original_problem}

Structure your analysis around:
1. **Assumptions to Test**: What must be true for success?
2. **MVP Definition**: Minimal viable solution
3. **Validation Metrics**: How to measure success
4. **Pivot Triggers**: When to change direction
5. **Resource Efficiency**: Maximum learning, minimum waste

Focus on rapid iteration and validated learning.
""",
                    variables=["original_problem"],
                    tags=["business", "startup", "validation"]
                ),

                "jobs_to_be_done": PromptTemplate(
                    name="jtbd_analysis",
                    description="Jobs-to-be-Done framework analysis",
                    template="""
Analyze using Jobs-to-be-Done framework: {original_problem}

Consider:
- **Functional Job**: What task needs completion?
- **Emotional Job**: How should users feel?
- **Social Job**: How do users want to be perceived?
- **Current Solutions**: What exists today?
- **Unmet Needs**: Where do current solutions fall short?

Identify the core job and innovation opportunities.
""",
                    variables=["original_problem"],
                    tags=["business", "product", "innovation"]
                ),
            },

            "technical_analysis": {
                "system_design": PromptTemplate(
                    name="system_design_approach",
                    description="Systematic approach to system design",
                    template="""
Design a system for: {original_problem}

Follow this structure:
1. **Requirements**: Functional and non-functional
2. **Scale Estimates**: Users, data, requests
3. **Architecture**: High-level components
4. **Data Model**: Core entities and relationships
5. **API Design**: Key interfaces
6. **Trade-offs**: Design decisions and alternatives

Consider: {constraints}
Target scale: {system_scale}
""",
                    variables=["original_problem", "constraints", "system_scale"],
                    tags=["technical", "architecture", "design"]
                ),
            }
        }

    async def _load_custom_templates(self) -> None:
        """Load custom templates from disk"""
        for file_path in self.templates_dir.glob("*.yaml"):
            try:
                with open(file_path) as f:
                    data = yaml.safe_load(f)

                if "templates" in data:
                    for template_data in data["templates"]:
                        template = PromptTemplate(**template_data)
                        self.library.custom[template.name] = template

            except Exception as e:
                logger.error(f"Failed to load template from {file_path}: {e}")

    def _find_template(self, tool_name: str) -> PromptTemplate | None:
        """Find a template by tool name"""
        # Check each category
        for category in ["cognitive_tools", "business_frameworks", "technical_analysis", "custom"]:
            category_dict = getattr(self.library, category, {})
            if tool_name in category_dict:
                return category_dict[tool_name]

        return None

    def _count_templates(self) -> int:
        """Count total number of loaded templates"""
        total = 0
        for category in ["cognitive_tools", "business_frameworks", "technical_analysis",
                        "copywriting_formulas", "ux_ui_patterns", "custom"]:
            category_dict = getattr(self.library, category, {})
            total += len(category_dict)
        return total

    def _track_usage(self, tool_name: str, template_name: str) -> None:
        """Track template usage for performance metrics"""
        if tool_name not in self.performance_metrics:
            self.performance_metrics[tool_name] = {
                "usage_count": 0,
                "templates_used": {},
                "last_used": None
            }

        metrics = self.performance_metrics[tool_name]
        metrics["usage_count"] += 1
        metrics["last_used"] = datetime.utcnow().isoformat()

        if template_name not in metrics["templates_used"]:
            metrics["templates_used"][template_name] = 0
        metrics["templates_used"][template_name] += 1
