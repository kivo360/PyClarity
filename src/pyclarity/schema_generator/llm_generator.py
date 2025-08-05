"""LLM-based schema example generator for PyClarity tools."""

import json
import logging
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Type

from pydantic import BaseModel

logger = logging.getLogger(__name__)


@dataclass
class SchemaExample:
    """Container for generated schema examples."""
    
    tool_name: str
    input_schema: Dict[str, Any]
    output_schema: Optional[Dict[str, Any]]
    examples: List[Dict[str, Any]]
    description: str


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate text from prompt."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if this provider is available."""
        pass


class OpenAIProvider(LLMProvider):
    """OpenAI API provider (or compatible APIs)."""
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL")  # Custom base URL
        self._client = None
    
    def is_available(self) -> bool:
        """Check if OpenAI is available."""
        return bool(self.api_key)
    
    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate using OpenAI or compatible API."""
        if not self._client:
            try:
                import openai
                # Support custom base URLs for OpenAI-compatible APIs
                if self.base_url:
                    self._client = openai.AsyncOpenAI(
                        api_key=self.api_key,
                        base_url=self.base_url
                    )
                    logger.info(f"Using custom OpenAI-compatible API at: {self.base_url}")
                else:
                    self._client = openai.AsyncOpenAI(api_key=self.api_key)
            except ImportError:
                logger.error("OpenAI library not installed. Run: pip install openai")
                return ""
        
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = await self._client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4"),
                messages=messages,
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI generation failed: {e}")
            return ""


class AnthropicProvider(LLMProvider):
    """Anthropic Claude API provider."""
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.base_url = base_url or os.getenv("ANTHROPIC_BASE_URL")  # Custom base URL
        self._client = None
    
    def is_available(self) -> bool:
        """Check if Anthropic is available."""
        return bool(self.api_key)
    
    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate using Anthropic."""
        if not self._client:
            try:
                import anthropic
                # Support custom base URLs for Anthropic-compatible APIs
                if self.base_url:
                    self._client = anthropic.AsyncAnthropic(
                        api_key=self.api_key,
                        base_url=self.base_url
                    )
                    logger.info(f"Using custom Anthropic-compatible API at: {self.base_url}")
                else:
                    self._client = anthropic.AsyncAnthropic(api_key=self.api_key)
            except ImportError:
                logger.error("Anthropic library not installed. Run: pip install anthropic")
                return ""
        
        try:
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"
            
            response = await self._client.messages.create(
                model=os.getenv("ANTHROPIC_MODEL", "claude-3-sonnet-20240229"),
                max_tokens=4000,
                temperature=0.7,
                messages=[{
                    "role": "user",
                    "content": f"{full_prompt}\n\nProvide your response as valid JSON."
                }]
            )
            
            return response.content[0].text
        except Exception as e:
            logger.error(f"Anthropic generation failed: {e}")
            return ""


class LocalLLMProvider(LLMProvider):
    """Local LLM provider (e.g., Ollama, LM Studio)."""
    
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or os.getenv("LOCAL_LLM_BASE_URL", "http://localhost:11434")
        self.model = os.getenv("LOCAL_LLM_MODEL", "llama2")
    
    def is_available(self) -> bool:
        """Check if local LLM is available."""
        try:
            import requests
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate using local LLM."""
        try:
            import aiohttp
            
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": f"{full_prompt}\n\nProvide your response as valid JSON.",
                        "stream": False,
                        "format": "json"
                    }
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("response", "")
                    return ""
        except Exception as e:
            logger.error(f"Local LLM generation failed: {e}")
            return ""


class LLMSchemaGenerator:
    """Generate schema examples using available LLMs."""
    
    def __init__(self, provider: Optional[LLMProvider] = None):
        """Initialize with optional provider."""
        self.provider = provider or self._detect_provider()
        self._cache: Dict[str, SchemaExample] = {}
    
    def _detect_provider(self) -> Optional[LLMProvider]:
        """Detect available LLM provider."""
        # Check in order of preference
        providers = [
            OpenAIProvider(),
            AnthropicProvider(),
            LocalLLMProvider(),
        ]
        
        for provider in providers:
            if provider.is_available():
                logger.info(f"Detected LLM provider: {provider.__class__.__name__}")
                return provider
        
        logger.warning("No LLM provider available for schema generation")
        return None
    
    async def generate_examples(
        self,
        tool_name: str,
        input_model: Type[BaseModel],
        output_model: Optional[Type[BaseModel]] = None,
        description: str = "",
        num_examples: int = 3
    ) -> Optional[SchemaExample]:
        """Generate examples for a tool's input/output schemas."""
        if not self.provider:
            return None
        
        # Check cache
        cache_key = f"{tool_name}:{input_model.__name__}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        # Build prompt
        system_prompt = """You are an expert at generating realistic test examples for API schemas.
        Generate diverse, realistic examples that cover different use cases.
        Always respond with valid JSON in the format requested."""
        
        input_schema = input_model.model_json_schema()
        prompt = f"""Generate {num_examples} realistic example inputs for the following tool:

Tool Name: {tool_name}
Description: {description or 'A cognitive analysis tool'}

Input Schema:
{json.dumps(input_schema, indent=2)}

Required Output Format:
{{
    "examples": [
        {{"example_name": "descriptive_name", "input": {{"field1": "value1", ...}}, "description": "what this example tests"}}
    ]
}}

Generate diverse examples that:
1. Cover different use cases
2. Include edge cases
3. Use realistic values
4. Test optional parameters"""

        try:
            response = await self.provider.generate(prompt, system_prompt)
            data = json.loads(response)
            
            # Validate examples against schema
            validated_examples = []
            for ex in data.get("examples", []):
                try:
                    # Validate input against model
                    input_model(**ex["input"])
                    validated_examples.append(ex)
                except Exception as e:
                    logger.warning(f"Invalid example generated for {tool_name}: {e}")
            
            result = SchemaExample(
                tool_name=tool_name,
                input_schema=input_schema,
                output_schema=output_model.model_json_schema() if output_model else None,
                examples=validated_examples,
                description=description
            )
            
            # Cache result
            self._cache[cache_key] = result
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to generate examples for {tool_name}: {e}")
            return None
    
    async def generate_for_all_tools(
        self,
        tools: Dict[str, Dict[str, Any]]
    ) -> Dict[str, SchemaExample]:
        """Generate examples for all tools in a registry."""
        results = {}
        
        for tool_name, tool_info in tools.items():
            input_model = tool_info.get("input_model")
            output_model = tool_info.get("output_model")
            description = tool_info.get("description", "")
            
            if input_model:
                example = await self.generate_examples(
                    tool_name,
                    input_model,
                    output_model,
                    description
                )
                if example:
                    results[tool_name] = example
        
        return results
    
    def save_examples(self, examples: Dict[str, SchemaExample], output_dir: str = "examples"):
        """Save generated examples to files."""
        os.makedirs(output_dir, exist_ok=True)
        
        for tool_name, schema_example in examples.items():
            output_file = os.path.join(output_dir, f"{tool_name}_examples.json")
            
            # Focus on input examples only
            data = {
                "tool_name": schema_example.tool_name,
                "description": schema_example.description,
                "input_schema": schema_example.input_schema,
                "input_examples": [ex.get("input", {}) for ex in schema_example.examples],
                "example_descriptions": [
                    {
                        "name": ex.get("example_name", f"example_{i}"),
                        "description": ex.get("description", "")
                    }
                    for i, ex in enumerate(schema_example.examples)
                ]
            }
            
            with open(output_file, "w") as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"Saved examples for {tool_name} to {output_file}")


def detect_available_llm() -> Optional[str]:
    """Detect which LLM is available."""
    if os.getenv("OPENAI_API_KEY"):
        return "openai"
    elif os.getenv("ANTHROPIC_API_KEY"):
        return "anthropic"
    elif os.getenv("LOCAL_LLM_BASE_URL"):
        return "local"
    return None