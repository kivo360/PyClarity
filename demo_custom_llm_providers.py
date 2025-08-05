#!/usr/bin/env python3
"""
Demo script showing how to use custom LLM providers with PyClarity.

This demonstrates using OpenAI-compatible APIs from various providers:
- Together AI
- Anyscale
- OpenRouter
- Groq
- Local vLLM/FastChat/etc.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from pyclarity.schema_generator.llm_generator import LLMSchemaGenerator, OpenAIProvider
from pyclarity.tools.sequential_thinking.progressive_analyzer import ProgressiveThoughtRequest

# Example configurations for popular OpenAI-compatible services
PROVIDER_CONFIGS = {
    "together": {
        "base_url": "https://api.together.xyz/v1",
        "model": "moonshotai/Kimi-K2-Instruct",
        "description": "Together AI - Fast inference for open models",
    },
    "anyscale": {
        "base_url": "https://api.endpoints.anyscale.com/v1",
        "model": "meta-llama/Llama-2-70b-chat-hf",
        "description": "Anyscale Endpoints - Scalable model serving",
    },
    "openrouter": {
        "base_url": "https://openrouter.ai/api/v1",
        "model": "anthropic/claude-3-haiku",
        "description": "OpenRouter - Route to any model",
    },
    "groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "description": "Groq - Ultra-fast LPU inference",
    },
}


async def test_custom_provider(provider_name: str, api_key: str):
    """Test a custom LLM provider."""
    config = PROVIDER_CONFIGS.get(provider_name)
    if not config:
        print(f"❌ Unknown provider: {provider_name}")
        return

    print(f"\n🔧 Testing {config['description']}")
    print(f"   Base URL: {config['base_url']}")
    print(f"   Model: {config['model']}")

    # Create custom provider
    provider = OpenAIProvider(api_key=api_key, base_url=config["base_url"])

    if not provider.is_available():
        print("   ❌ API key not provided")
        return

    # Test with a simple prompt
    try:
        # Override the model for this provider
        original_model = os.environ.get("OPENAI_MODEL")
        os.environ["OPENAI_MODEL"] = config["model"]

        response = await provider.generate(
            prompt="Generate a simple JSON example with name and age fields",
            system_prompt="You are a helpful assistant. Respond only with valid JSON.",
        )

        if response:
            print(f"   ✅ Response received: {response[:100]}...")
        else:
            print("   ❌ Empty response")

    except Exception as e:
        print(f"   ❌ Error: {e}")
    finally:
        # Restore original model
        if original_model:
            os.environ["OPENAI_MODEL"] = original_model
        elif "OPENAI_MODEL" in os.environ:
            del os.environ["OPENAI_MODEL"]


async def demo_schema_generation_with_custom_provider():
    """Demo schema generation with a custom provider."""
    print("\n" + "=" * 60)
    print("🎯 Schema Generation with Custom Provider")
    print("=" * 60)

    # Example: Using Together AI for schema generation
    api_key = os.getenv("TOGETHER_API_KEY") or os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("\n⚠️  No API key found. Set TOGETHER_API_KEY or OPENAI_API_KEY")
        print("   Get a free API key from: https://api.together.xyz")
        return

    # Create provider with Together AI base URL
    provider = OpenAIProvider(api_key=api_key, base_url="https://api.together.xyz/v1")

    # Set the model
    os.environ["OPENAI_MODEL"] = "mistralai/Mixtral-8x7B-Instruct-v0.1"

    # Create schema generator
    generator = LLMSchemaGenerator(provider=provider)

    print("\n📝 Generating schema examples using Together AI...")

    try:
        example = await generator.generate_examples(
            tool_name="progressive_sequential_thinking",
            input_model=ProgressiveThoughtRequest,
            description="Process thoughts progressively",
            num_examples=2,
        )

        if example:
            print(f"\n✅ Generated {len(example.examples)} examples")
            for ex in example.examples:
                print(f"   - {ex.get('example_name', 'Example')}")
        else:
            print("\n❌ Failed to generate examples")

    except Exception as e:
        print(f"\n❌ Error: {e}")


def show_configuration_examples():
    """Show example configurations for different providers."""
    print("\n" + "=" * 60)
    print("📋 Example .env Configurations")
    print("=" * 60)

    print("\n1️⃣ Together AI (Recommended - Free tier available):")
    print("   OPENAI_API_KEY=your-together-api-key")
    print("   OPENAI_BASE_URL=https://api.together.xyz/v1")
    print("   OPENAI_MODEL=mistralai/Mixtral-8x7B-Instruct-v0.1")

    print("\n2️⃣ Groq (Fast inference):")
    print("   OPENAI_API_KEY=your-groq-api-key")
    print("   OPENAI_BASE_URL=https://api.groq.com/openai/v1")
    print("   OPENAI_MODEL=mixtral-8x7b-32768")

    print("\n3️⃣ OpenRouter (Access to many models):")
    print("   OPENAI_API_KEY=your-openrouter-api-key")
    print("   OPENAI_BASE_URL=https://openrouter.ai/api/v1")
    print("   OPENAI_MODEL=anthropic/claude-3-haiku")

    print("\n4️⃣ Local vLLM Server:")
    print("   OPENAI_API_KEY=dummy-key-for-local")
    print("   OPENAI_BASE_URL=http://localhost:8000/v1")
    print("   OPENAI_MODEL=NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO")

    print("\n5️⃣ Local Ollama (via OpenAI compatibility layer):")
    print("   # First run: ollama serve")
    print("   # Then run: ollama pull mixtral")
    print("   LOCAL_LLM_BASE_URL=http://localhost:11434")
    print("   LOCAL_LLM_MODEL=mixtral")


async def main():
    """Run the demo."""
    print("\n🚀 PyClarity Custom LLM Providers Demo")
    print("   Use any OpenAI-compatible API!")

    # Show configuration examples
    show_configuration_examples()

    # Test custom providers if API keys are available
    print("\n" + "=" * 60)
    print("🧪 Testing Available Providers")
    print("=" * 60)

    # Check environment for API keys
    providers_to_test = []

    if os.getenv("TOGETHER_API_KEY"):
        providers_to_test.append(("together", os.getenv("TOGETHER_API_KEY")))

    if os.getenv("GROQ_API_KEY"):
        providers_to_test.append(("groq", os.getenv("GROQ_API_KEY")))

    if os.getenv("OPENROUTER_API_KEY"):
        providers_to_test.append(("openrouter", os.getenv("OPENROUTER_API_KEY")))

    # Test OpenAI with custom base URL if set
    if os.getenv("OPENAI_API_KEY") and os.getenv("OPENAI_BASE_URL"):
        print(f"\n🔍 Detected custom OpenAI base URL: {os.getenv('OPENAI_BASE_URL')}")
        await demo_schema_generation_with_custom_provider()
    elif not providers_to_test:
        print("\n⚠️  No API keys found in environment")
        print("   Set one of: TOGETHER_API_KEY, GROQ_API_KEY, OPENROUTER_API_KEY")
        print("   Or set OPENAI_API_KEY with OPENAI_BASE_URL")

    # Test each available provider
    for provider_name, api_key in providers_to_test:
        await test_custom_provider(provider_name, api_key)

    print("\n" + "=" * 60)
    print("✅ Demo complete!")
    print("\n💡 Tips:")
    print("   - Many providers offer free tiers (Together, Groq)")
    print("   - Local models work great for development")
    print("   - Use OPENAI_BASE_URL to override the API endpoint")
    print("   - The same API key variable works for compatible services")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
