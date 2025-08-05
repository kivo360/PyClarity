"""Base classes for the PyClarity template system."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class TemplateCategory(Enum):
    """Categories for organizing templates."""
    USER_JOURNEY = "user_journey"
    GOAL_DEFINITION = "goal_definition"
    COPYWRITING = "copywriting"
    PRODUCT_DEVELOPMENT = "product_development"
    BUSINESS_STRATEGY = "business_strategy"
    CONTENT_PRODUCTION = "content_production"
    VALIDATION_TESTING = "validation_testing"
    RAPID_IDEATION = "rapid_ideation"


@dataclass
class PromptTemplate:
    """Base class for all prompt templates."""

    name: str
    description: str
    template: str
    variables: list[str]
    category: TemplateCategory
    examples: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def render(self, **kwargs) -> str:
        """Render the template with provided variables."""
        # Check all required variables are provided
        missing_vars = set(self.variables) - set(kwargs.keys())
        if missing_vars:
            raise ValueError(f"Missing required variables: {missing_vars}")

        # Render the template
        return self.template.format(**kwargs)

    def validate(self, **kwargs) -> bool:
        """Validate that all required variables are provided."""
        return all(var in kwargs for var in self.variables)

    def get_example(self, index: int = 0) -> dict[str, Any] | None:
        """Get an example usage of this template."""
        if index < len(self.examples):
            return self.examples[index]
        return None

    def to_dict(self) -> dict[str, Any]:
        """Convert template to dictionary format."""
        return {
            "name": self.name,
            "description": self.description,
            "template": self.template,
            "variables": self.variables,
            "category": self.category.value,
            "examples": self.examples,
            "metadata": self.metadata
        }
