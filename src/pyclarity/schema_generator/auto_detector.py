"""Automatic LLM detection and schema generation wrapper for PyClarity."""

import json
import logging
import os
from pathlib import Path
from typing import Dict, Optional, Type

from pydantic import BaseModel

from pyclarity.schema_generator.llm_generator import (
    LLMSchemaGenerator,
    SchemaExample,
    detect_available_llm,
)

logger = logging.getLogger(__name__)


class SchemaGenerationConfig:
    """Configuration for automatic schema generation."""
    
    def __init__(self):
        """Initialize from environment variables."""
        self.enabled = os.getenv("ENABLE_SCHEMA_GENERATION", "true").lower() == "true"
        self.num_examples = int(os.getenv("SCHEMA_GENERATION_EXAMPLES", "3"))
        self.cache_dir = os.getenv("SCHEMA_CACHE_DIR", "cache/schemas")
        self.auto_save = os.getenv("SCHEMA_AUTO_SAVE", "true").lower() == "true"


class AutoSchemaGenerator:
    """Automatic schema generator that detects LLM availability."""
    
    def __init__(self, config: Optional[SchemaGenerationConfig] = None):
        """Initialize the auto generator."""
        self.config = config or SchemaGenerationConfig()
        self.generator: Optional[LLMSchemaGenerator] = None
        self._initialized = False
        self._examples_cache: Dict[str, SchemaExample] = {}
        
    async def initialize(self) -> bool:
        """Initialize the schema generator if LLM is available."""
        if not self.config.enabled:
            logger.info("Schema generation is disabled")
            return False
            
        if self._initialized:
            return self.generator is not None
            
        # Detect available LLM
        llm_type = detect_available_llm()
        if not llm_type:
            logger.warning(
                "No LLM provider detected. Schema generation will be unavailable. "
                "Set OPENAI_API_KEY, ANTHROPIC_API_KEY, or LOCAL_LLM_BASE_URL in .env"
            )
            return False
            
        # Create generator
        self.generator = LLMSchemaGenerator()
        self._initialized = True
        
        logger.info(f"Schema generator initialized with {llm_type} provider")
        
        # Load cached examples if available
        self._load_cache()
        
        return True
    
    def _load_cache(self):
        """Load cached examples from disk."""
        cache_path = Path(self.config.cache_dir)
        if not cache_path.exists():
            return
            
        for json_file in cache_path.glob("*_examples.json"):
            try:
                with open(json_file, "r") as f:
                    data = json.load(f)
                    example = SchemaExample(
                        tool_name=data["tool_name"],
                        input_schema=data["input_schema"],
                        output_schema=data.get("output_schema"),
                        examples=data["examples"],
                        description=data.get("description", "")
                    )
                    self._examples_cache[example.tool_name] = example
                    logger.debug(f"Loaded cached examples for {example.tool_name}")
            except Exception as e:
                logger.error(f"Failed to load cache file {json_file}: {e}")
    
    async def generate_if_needed(
        self,
        tool_name: str,
        input_model: Type[BaseModel],
        output_model: Optional[Type[BaseModel]] = None,
        description: str = "",
        force: bool = False
    ) -> Optional[SchemaExample]:
        """Generate examples only if needed (not cached or forced)."""
        if not await self.initialize():
            return None
            
        # Check cache first
        if not force and tool_name in self._examples_cache:
            logger.debug(f"Using cached examples for {tool_name}")
            return self._examples_cache[tool_name]
            
        # Generate new examples
        logger.info(f"Generating examples for {tool_name}")
        try:
            example = await self.generator.generate_examples(
                tool_name=tool_name,
                input_model=input_model,
                output_model=output_model,
                description=description,
                num_examples=self.config.num_examples
            )
            
            if example:
                # Cache in memory
                self._examples_cache[tool_name] = example
                
                # Save to disk if auto-save enabled
                if self.config.auto_save:
                    self._save_example(example)
                    
                logger.info(f"Generated {len(example.examples)} examples for {tool_name}")
            
            return example
            
        except Exception as e:
            logger.error(f"Failed to generate examples for {tool_name}: {e}")
            return None
    
    def _save_example(self, example: SchemaExample):
        """Save example to disk cache."""
        cache_path = Path(self.config.cache_dir)
        cache_path.mkdir(parents=True, exist_ok=True)
        
        output_file = cache_path / f"{example.tool_name}_examples.json"
        
        data = {
            "tool_name": example.tool_name,
            "description": example.description,
            "input_schema": example.input_schema,
            "output_schema": example.output_schema,
            "examples": example.examples
        }
        
        try:
            with open(output_file, "w") as f:
                json.dump(data, f, indent=2)
            logger.debug(f"Saved examples for {example.tool_name} to {output_file}")
        except Exception as e:
            logger.error(f"Failed to save examples for {example.tool_name}: {e}")
    
    async def generate_for_tools(
        self,
        tools: Dict[str, Dict[str, any]],
        force: bool = False
    ) -> Dict[str, SchemaExample]:
        """Generate examples for multiple tools."""
        if not await self.initialize():
            return {}
            
        results = {}
        
        for tool_name, tool_info in tools.items():
            input_model = tool_info.get("input_model")
            if not input_model:
                continue
                
            example = await self.generate_if_needed(
                tool_name=tool_name,
                input_model=input_model,
                output_model=tool_info.get("output_model"),
                description=tool_info.get("description", ""),
                force=force
            )
            
            if example:
                results[tool_name] = example
        
        return results
    
    def get_example(self, tool_name: str) -> Optional[SchemaExample]:
        """Get cached example for a tool."""
        return self._examples_cache.get(tool_name)
    
    def clear_cache(self):
        """Clear in-memory cache."""
        self._examples_cache.clear()
        logger.info("Cleared schema examples cache")


# Global instance for easy access
_auto_generator: Optional[AutoSchemaGenerator] = None


def get_auto_generator() -> AutoSchemaGenerator:
    """Get or create the global auto generator instance."""
    global _auto_generator
    if _auto_generator is None:
        _auto_generator = AutoSchemaGenerator()
    return _auto_generator


async def ensure_schema_examples(
    tool_name: str,
    input_model: Type[BaseModel],
    output_model: Optional[Type[BaseModel]] = None,
    description: str = ""
) -> Optional[SchemaExample]:
    """Convenience function to ensure schema examples exist for a tool."""
    generator = get_auto_generator()
    return await generator.generate_if_needed(
        tool_name=tool_name,
        input_model=input_model,
        output_model=output_model,
        description=description
    )


# Example usage in tool registration
async def register_tool_with_examples(
    tool_registry: dict,
    tool_name: str,
    handler: callable,
    input_model: Type[BaseModel],
    output_model: Optional[Type[BaseModel]] = None,
    description: str = ""
):
    """Register a tool and generate examples if LLM is available."""
    # Register the tool
    tool_registry[tool_name] = {
        "handler": handler,
        "input_model": input_model,
        "output_model": output_model,
        "description": description
    }
    
    # Generate examples if possible
    example = await ensure_schema_examples(
        tool_name=tool_name,
        input_model=input_model,
        output_model=output_model,
        description=description
    )
    
    if example:
        tool_registry[tool_name]["examples"] = example.examples
        logger.info(f"Registered {tool_name} with {len(example.examples)} generated examples")
    else:
        logger.info(f"Registered {tool_name} without examples (no LLM available)")