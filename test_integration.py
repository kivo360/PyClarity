#!/usr/bin/env python3
"""
Integration test script to demonstrate all features working together.

Run this to see:
1. LLM detection and schema generation
2. Progressive sequential thinking with database persistence
3. Vector embedding support (if OpenAI is available)
"""

import asyncio
import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from pyclarity.db.asyncpg_adapter import AsyncPGSessionStore, AsyncPGThoughtStore
from pyclarity.schema_generator import detect_available_llm
from pyclarity.schema_generator.auto_detector import get_auto_generator
from pyclarity.tools.sequential_thinking.progressive_analyzer import (
    ProgressiveSequentialThinkingAnalyzer,
    ProgressiveThoughtRequest,
)


async def test_llm_detection():
    """Test LLM detection and show what's available."""
    print("\n" + "=" * 60)
    print("🔍 TESTING LLM DETECTION")
    print("=" * 60)

    # Check environment variables
    print("\n📋 Environment Variables:")
    print(f"   OPENAI_API_KEY: {'✅ Set' if os.getenv('OPENAI_API_KEY') else '❌ Not set'}")
    print(f"   ANTHROPIC_API_KEY: {'✅ Set' if os.getenv('ANTHROPIC_API_KEY') else '❌ Not set'}")
    print(f"   LOCAL_LLM_BASE_URL: {'✅ Set' if os.getenv('LOCAL_LLM_BASE_URL') else '❌ Not set'}")

    # Detect available LLM
    llm_type = detect_available_llm()
    if llm_type:
        print(f"\n✅ Detected LLM Provider: {llm_type}")
    else:
        print("\n❌ No LLM provider detected")
        print("   To enable schema generation, set one of:")
        print("   - OPENAI_API_KEY")
        print("   - ANTHROPIC_API_KEY")
        print("   - LOCAL_LLM_BASE_URL (for Ollama, etc.)")

    return llm_type is not None


async def test_schema_generation():
    """Test automatic schema generation."""
    print("\n" + "=" * 60)
    print("🧪 TESTING SCHEMA GENERATION")
    print("=" * 60)

    generator = get_auto_generator()

    if not await generator.initialize():
        print("\n⚠️  Schema generation unavailable (no LLM)")
        return False

    print("\n✅ Schema generator initialized")

    # Generate examples for progressive thinking
    print("\n📝 Generating examples for Progressive Sequential Thinking...")

    example = await generator.generate_if_needed(
        tool_name="progressive_sequential_thinking",
        input_model=ProgressiveThoughtRequest,
        description="Process thoughts one at a time with session state",
    )

    if example:
        print(f"\n✅ Generated {len(example.examples)} examples:")
        for i, ex in enumerate(example.examples, 1):
            print(f"\n   Example {i}: {ex.get('example_name', 'Unnamed')}")
            print(f"   Description: {ex.get('description', 'No description')}")
            if "input" in ex:
                print(f"   Input thought: {ex['input'].get('thought', '')[:80]}...")
    else:
        print("\n❌ Failed to generate examples")
        return False

    return True


async def test_database_connection():
    """Test database connection and initialization."""
    print("\n" + "=" * 60)
    print("🗄️  TESTING DATABASE CONNECTION")
    print("=" * 60)

    db_url = os.getenv("DATABASE_URL", "postgresql://pyclarity:pyclarity@localhost:5432/pyclarity")
    print(f"\n📍 Database URL: {db_url}")

    try:
        # Initialize stores
        session_store = AsyncPGSessionStore(db_url)
        thought_store = AsyncPGThoughtStore(db_url)

        # Initialize database
        print("\n🔄 Initializing database tables...")
        await session_store.init_db()
        await thought_store.init_db()

        print("✅ Database initialized successfully")

        # Test pgvector support
        async with thought_store.pool.acquire() as conn:
            result = await conn.fetchval(
                "SELECT EXISTS(SELECT 1 FROM pg_extension WHERE extname = 'vector')"
            )
            if result:
                print("✅ pgvector extension is installed")
            else:
                print("⚠️  pgvector extension not found (vector search unavailable)")

        return session_store, thought_store

    except Exception as e:
        print(f"\n❌ Database connection failed: {e}")
        print("\n💡 Make sure PostgreSQL is running:")
        print("   docker-compose up -d postgres")
        return None, None


async def test_progressive_thinking(session_store, thought_store):
    """Test progressive sequential thinking with database."""
    print("\n" + "=" * 60)
    print("🧠 TESTING PROGRESSIVE SEQUENTIAL THINKING")
    print("=" * 60)

    if not session_store or not thought_store:
        print("\n⚠️  Skipping (no database connection)")
        return

    # Create analyzer
    analyzer = ProgressiveSequentialThinkingAnalyzer(
        session_store=session_store, thought_store=thought_store
    )

    print("\n📝 Starting new thinking session...")

    # Step 1: Initial thought
    print("\n1️⃣ Processing first thought...")
    request = ProgressiveThoughtRequest(
        thought="Let me analyze the problem of improving user engagement on a platform. First, I need to understand the key factors.",
        thought_number=1,
        total_thoughts=5,
        next_thought_needed=True,
    )

    response = await analyzer.process_thought(request)
    session_id = response.session_id

    print(f"   Session ID: {session_id}")
    print(f"   Status: {response.status}")
    print(f"   Thought Type: {response.thought_type}")
    print(f"   Confidence: {response.confidence}")
    print(f"   Suggestion: {response.suggestion}")

    # Step 2: Continue thinking
    await asyncio.sleep(0.5)  # Small delay for demo
    print("\n2️⃣ Processing second thought...")

    request = ProgressiveThoughtRequest(
        session_id=session_id,
        thought="Based on my analysis, the key factors are: content relevance, UI complexity, and social features. Let me form a hypothesis.",
        thought_number=2,
        total_thoughts=5,
        next_thought_needed=True,
    )

    response = await analyzer.process_thought(request)
    print(f"   Thought Type: {response.thought_type}")
    print(f"   Progress: {response.progress['percentComplete']}%")

    # Step 3: Branch thinking
    await asyncio.sleep(0.5)
    print("\n3️⃣ Creating a branch to explore alternative...")

    request = ProgressiveThoughtRequest(
        session_id=session_id,
        thought="Alternative hypothesis: The onboarding process might be the real issue, not the platform features.",
        thought_number=3,
        total_thoughts=6,
        branch_from_thought=2,
        branch_id="onboarding-hypothesis",
        next_thought_needed=True,
    )

    response = await analyzer.process_thought(request)
    print(f"   Branch ID: {response.branch_id}")
    print(f"   Status: {response.status}")

    # Retrieve all thoughts
    print("\n📚 Retrieving all thoughts from session...")
    thoughts = await thought_store.get_session_thoughts(session_id)

    print(f"\n✅ Total thoughts saved: {len(thoughts)}")
    for thought in thoughts:
        print(f"\n   Thought #{thought.thought_number}:")
        print(f"   Content: {thought.content[:80]}...")
        print(f"   Type: {thought.thought_type}")
        if thought.branch_id:
            print(f"   Branch: {thought.branch_id}")

    # Clean up
    await session_store.close()
    await thought_store.close()


async def test_vector_embedding():
    """Test vector embedding support (if OpenAI is available)."""
    print("\n" + "=" * 60)
    print("🔮 TESTING VECTOR EMBEDDING SUPPORT")
    print("=" * 60)

    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  Skipping (OpenAI API key not set)")
        print("   Vector embeddings require OpenAI for this demo")
        return

    try:
        import openai

        client = openai.OpenAI()

        # Test embedding generation
        text = "This is a test thought about improving user engagement"
        print(f"\n📝 Generating embedding for: '{text}'")

        response = client.embeddings.create(model="text-embedding-ada-002", input=text)

        embedding = response.data[0].embedding
        print(f"\n✅ Generated embedding with {len(embedding)} dimensions")
        print(f"   First 5 values: {embedding[:5]}")

    except Exception as e:
        print(f"\n❌ Embedding generation failed: {e}")


async def main():
    """Run all integration tests."""
    print("\n🚀 PyClarity Integration Test Suite")
    print("   Testing all components together...")

    # Test 1: LLM Detection
    has_llm = await test_llm_detection()

    # Test 2: Schema Generation (if LLM available)
    if has_llm:
        await test_schema_generation()

    # Test 3: Database Connection
    session_store, thought_store = await test_database_connection()

    # Test 4: Progressive Thinking (if database available)
    if session_store and thought_store:
        await test_progressive_thinking(session_store, thought_store)

    # Test 5: Vector Embeddings (if OpenAI available)
    await test_vector_embedding()

    print("\n" + "=" * 60)
    print("✅ Integration tests complete!")
    print("=" * 60)

    # Summary
    print("\n📊 Summary:")
    print(f"   LLM Available: {'Yes' if has_llm else 'No'}")
    print(f"   Database Connected: {'Yes' if session_store else 'No'}")
    print(f"   pgvector Support: {'Check above' if thought_store else 'N/A'}")
    print(f"   OpenAI Embeddings: {'Yes' if os.getenv('OPENAI_API_KEY') else 'No'}")

    print("\n💡 To enable all features:")
    print("   1. Set LLM API keys in .env file")
    print("   2. Run: docker-compose up -d postgres")
    print("   3. Install OpenAI: pip install openai")


if __name__ == "__main__":
    # Check if running in PyClarity directory
    if not Path("src/pyclarity").exists():
        print("❌ Error: Run this script from the PyClarity root directory")
        sys.exit(1)

    # Run tests
    asyncio.run(main())
