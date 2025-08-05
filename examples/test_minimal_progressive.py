#!/usr/bin/env python3
"""
Minimal test of progressive analyzers - starting with just Sequential Thinking
"""

import asyncio
import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

async def test_sequential_thinking():
    """Test just Sequential Thinking progressive analyzer"""
    print("Testing Sequential Thinking Progressive Analyzer...")
    
    try:
        # Import only what we need for Sequential Thinking
        from pyclarity.db.memory_stores import MemorySessionStore, MemoryThoughtStore
        from pyclarity.tools.sequential_thinking.progressive_analyzer import (
            ProgressiveSequentialThinkingAnalyzer,
            ProgressiveThoughtRequest
        )
        
        print("✓ Imports successful")
        
        # Create stores
        session_store = MemorySessionStore()
        thought_store = MemoryThoughtStore()
        
        print("✓ Stores created")
        
        # Create analyzer
        analyzer = ProgressiveSequentialThinkingAnalyzer(session_store, thought_store)
        
        print("✓ Analyzer created")
        
        # Create request
        request = ProgressiveThoughtRequest(
            thought="How to make a cup of tea?",
            thought_number=1,
            total_thoughts=5
        )
        
        print("✓ Request created")
        
        # Run analysis
        response = await analyzer.process_thought(request)
        
        print("✓ Analysis complete!")
        print(f"Session ID: {response.session_id}")
        print(f"Step: {response.thought_number}")
        print(f"Current thought: {response.thought_content}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(test_sequential_thinking())
    sys.exit(0 if success else 1)