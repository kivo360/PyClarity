#!/usr/bin/env python3
"""
Demo script showing schema generation without requiring real API keys.
This mocks the LLM responses to demonstrate the functionality.
"""

import asyncio
import json
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from pyclarity.schema_generator.llm_generator import LLMProvider, LLMSchemaGenerator, SchemaExample
from pyclarity.tools.sequential_thinking.progressive_analyzer import (
    ProgressiveThoughtRequest,
    ProgressiveThoughtResponse,
)


class MockLLMProvider(LLMProvider):
    """Mock LLM provider for demonstration."""
    
    def is_available(self) -> bool:
        """Always available for demo."""
        return True
    
    async def generate(self, prompt: str, system_prompt: str = None) -> str:
        """Generate mock responses based on the prompt."""
        # Detect what we're generating examples for
        if "progressive_sequential_thinking" in prompt.lower():
            return json.dumps({
                "examples": [
                    {
                        "example_name": "simple_problem_solving",
                        "description": "Basic problem decomposition and analysis",
                        "input": {
                            "thought": "Let me analyze this step-by-step problem about improving user engagement",
                            "thought_number": 1,
                            "total_thoughts": 5,
                            "next_thought_needed": True
                        }
                    },
                    {
                        "example_name": "branching_analysis",
                        "description": "Creating alternative hypothesis branches",
                        "input": {
                            "session_id": "example-session-123",
                            "thought": "I need to explore an alternative approach to this problem",
                            "thought_number": 3,
                            "total_thoughts": 7,
                            "branch_from_thought": 2,
                            "branch_id": "alternative-approach",
                            "next_thought_needed": True
                        }
                    },
                    {
                        "example_name": "thought_revision",
                        "description": "Revising a previous thought with new insights",
                        "input": {
                            "session_id": "example-session-456",
                            "thought": "Based on new evidence, I need to revise my earlier hypothesis",
                            "thought_number": 4,
                            "total_thoughts": 6,
                            "is_revision": True,
                            "revises_thought": 2,
                            "next_thought_needed": True
                        }
                    }
                ]
            })
        else:
            # Generic response
            return json.dumps({
                "examples": [
                    {"example_name": "example_1", "input": {}, "description": "Generic example"}
                ]
            })


async def demo_schema_generation():
    """Demonstrate schema generation with mock LLM."""
    print("\n" + "="*60)
    print("🎭 DEMO: Schema Generation with Mock LLM")
    print("="*60)
    
    # Create schema generator with mock provider
    mock_provider = MockLLMProvider()
    generator = LLMSchemaGenerator(provider=mock_provider)
    
    print("\n1️⃣ Generating schema for ProgressiveThoughtRequest...")
    print("\n📋 Input Schema:")
    schema = ProgressiveThoughtRequest.model_json_schema()
    print(json.dumps(schema, indent=2))
    
    print("\n2️⃣ Generating examples using mock LLM...")
    
    example = await generator.generate_examples(
        tool_name="progressive_sequential_thinking",
        input_model=ProgressiveThoughtRequest,
        output_model=ProgressiveThoughtResponse,
        description="Process thoughts one at a time with session state",
        num_examples=3
    )
    
    if example:
        print(f"\n✅ Generated {len(example.examples)} examples:")
        for i, ex in enumerate(example.examples, 1):
            print(f"\n   Example {i}: {ex.get('example_name', 'Unnamed')}")
            print(f"   Description: {ex.get('description', 'No description')}")
            print(f"   Input:")
            for key, value in ex.get('input', {}).items():
                print(f"      {key}: {value}")
    
    print("\n3️⃣ Validating examples against Pydantic model...")
    
    for i, ex in enumerate(example.examples, 1):
        try:
            # Create instance from example input
            request = ProgressiveThoughtRequest(**ex['input'])
            print(f"\n   ✅ Example {i} is valid!")
            print(f"      Session ID: {request.session_id}")
            print(f"      Thought #{request.thought_number}: {request.thought[:50]}...")
        except Exception as e:
            print(f"\n   ❌ Example {i} failed validation: {e}")
    
    print("\n4️⃣ Saving examples to file...")
    
    generator.save_examples(
        {"progressive_sequential_thinking": example},
        output_dir="examples"
    )
    
    print("\n✅ Examples saved to examples/")
    
    # Show the output schema too
    print("\n5️⃣ Output Schema (ProgressiveThoughtResponse):")
    output_schema = ProgressiveThoughtResponse.model_json_schema()
    print(json.dumps(output_schema, indent=2)[:500] + "...")


async def demo_without_database():
    """Demonstrate the concept without requiring a database."""
    print("\n" + "="*60)
    print("🧠 DEMO: Progressive Thinking Concept (No Database)")
    print("="*60)
    
    # Simulate a thinking session
    thoughts = []
    session_id = "demo-session-789"
    
    print(f"\n📝 Starting thinking session: {session_id}")
    
    # Step 1
    request1 = ProgressiveThoughtRequest(
        session_id=session_id,
        thought="Let me break down this problem into key components. First, I need to understand the user's core needs.",
        thought_number=1,
        total_thoughts=5,
        next_thought_needed=True
    )
    
    print(f"\n1️⃣ Thought #{request1.thought_number}:")
    print(f"   {request1.thought}")
    thoughts.append(request1)
    
    # Step 2
    request2 = ProgressiveThoughtRequest(
        session_id=session_id,
        thought="Based on the components, I can see three main factors: usability, performance, and cost.",
        thought_number=2,
        total_thoughts=5,
        next_thought_needed=True
    )
    
    print(f"\n2️⃣ Thought #{request2.thought_number}:")
    print(f"   {request2.thought}")
    thoughts.append(request2)
    
    # Step 3 - Branch
    request3 = ProgressiveThoughtRequest(
        session_id=session_id,
        thought="Alternative hypothesis: What if cost isn't actually a primary concern for this user segment?",
        thought_number=3,
        total_thoughts=6,  # Extended for branch
        branch_from_thought=2,
        branch_id="cost-hypothesis",
        next_thought_needed=True
    )
    
    print(f"\n3️⃣ Thought #{request3.thought_number} (Branch: {request3.branch_id}):")
    print(f"   {request3.thought}")
    thoughts.append(request3)
    
    print(f"\n📊 Session Summary:")
    print(f"   Total thoughts: {len(thoughts)}")
    print(f"   Branches created: 1")
    print(f"   Session complete: No (3/6 thoughts)")


async def main():
    """Run all demos."""
    print("\n🚀 PyClarity Schema Generation Demo")
    print("   This demo uses mock LLM to show functionality")
    print("   No API keys or database required!")
    
    # Demo 1: Schema generation with mock LLM
    await demo_schema_generation()
    
    # Demo 2: Progressive thinking concept
    await demo_without_database()
    
    print("\n" + "="*60)
    print("✅ Demo complete!")
    print("\n💡 Key Takeaways:")
    print("   1. Pydantic models auto-generate JSON schemas")
    print("   2. LLM integration can generate realistic test examples")
    print("   3. Progressive thinking processes one thought at a time")
    print("   4. Session state enables branching and revisions")
    print("="*60)


if __name__ == "__main__":
    # Check if running in PyClarity directory
    if not Path("src/pyclarity").exists():
        print("❌ Error: Run this script from the PyClarity root directory")
        sys.exit(1)
    
    # Run demos
    asyncio.run(main())