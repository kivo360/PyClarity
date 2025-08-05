"""Mass production templates for PyClarity."""

from .business_strategy import BUSINESS_STRATEGY_TEMPLATES
from .content_production import CONTENT_PRODUCTION_TEMPLATES
from .copywriting import COPYWRITING_TEMPLATES
from .goal_definition import GOAL_DEFINITION_TEMPLATES
from .product_development import PRODUCT_DEVELOPMENT_TEMPLATES
from .rapid_ideation import RAPID_IDEATION_TEMPLATES
from .user_journey import USER_JOURNEY_TEMPLATES
from .validation_testing import VALIDATION_TESTING_TEMPLATES

# Aggregate all templates
ALL_TEMPLATES = {
    "user_journey": USER_JOURNEY_TEMPLATES,
    "goal_definition": GOAL_DEFINITION_TEMPLATES,
    "copywriting": COPYWRITING_TEMPLATES,
    "product_development": PRODUCT_DEVELOPMENT_TEMPLATES,
    "business_strategy": BUSINESS_STRATEGY_TEMPLATES,
    "content_production": CONTENT_PRODUCTION_TEMPLATES,
    "validation_testing": VALIDATION_TESTING_TEMPLATES,
    "rapid_ideation": RAPID_IDEATION_TEMPLATES,
}

__all__ = [
    "USER_JOURNEY_TEMPLATES",
    "GOAL_DEFINITION_TEMPLATES",
    "COPYWRITING_TEMPLATES",
    "PRODUCT_DEVELOPMENT_TEMPLATES",
    "BUSINESS_STRATEGY_TEMPLATES",
    "CONTENT_PRODUCTION_TEMPLATES",
    "VALIDATION_TESTING_TEMPLATES",
    "RAPID_IDEATION_TEMPLATES",
    "ALL_TEMPLATES",
]
