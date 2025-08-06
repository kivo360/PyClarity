#!/usr/bin/env python3
"""
Demo of enhanced development rules with loguru and validation.

This file demonstrates ALL the key patterns from enhanced-claude-rules.md

Run with: watchexec -e py python examples/demo_enhanced_rules.py
"""
import os
import sys
from datetime import datetime
from loguru import logger
import asyncio

# Clear screen for fresh output
print("\033[2J\033[H")
print(f"{'='*60}")
print(f"🔄 Enhanced Rules Demo | {datetime.now().strftime('%H:%M:%S')}")
print(f"{'='*60}\n")

# Configure logging for development
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{function}:{line}</cyan> - <level>{message}</level>",
    level="DEBUG"
)

# Also log to file for post-mortem
logger.add(
    "logs/demo_{time:YYYY-MM-DD}.log",
    rotation="1 day",
    retention="1 week",
    level="TRACE",
    backtrace=True,
    diagnose=True
)

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# RULE 2: Reference Validation Before Implementation
logger.info("📦 Stage 1: Validating all imports...")
validation_passed = True

try:
    # Test each import individually with helpful errors
    logger.debug("Importing base models...")
    from pyclarity.db.base import SessionData, ThoughtData
    logger.success("✅ Base models imported")
    
    logger.debug("Importing memory stores...")
    from pyclarity.db.memory_stores import MemorySessionStore, MemoryThoughtStore
    logger.success("✅ Memory stores imported")
    
    logger.debug("Importing progressive analyzer...")
    from pyclarity.tools.sequential_thinking.progressive_analyzer import (
        ProgressiveSequentialThinkingAnalyzer,
        ProgressiveThoughtRequest,
        ProgressiveThoughtResponse
    )
    logger.success("✅ Progressive analyzer imported")
    
except ImportError as e:
    validation_passed = False
    logger.exception(e)
    logger.error("❌ Import validation failed")
    logger.info("🔍 Debug hints:")
    logger.info("  1. Check virtual environment: which python")
    logger.info("  2. Check installation: uv pip list | grep pyclarity")
    logger.info("  3. Find the file: find src -name '*.py' | grep -i memory")
    
    # Try to discover what's actually available
    try:
        import pyclarity
        logger.info(f"  4. PyClarity root: {pyclarity.__file__}")
        logger.info(f"  5. Available in pyclarity: {[x for x in dir(pyclarity) if not x.startswith('_')][:5]}")
    except:
        logger.error("  PyClarity not importable at all!")

if not validation_passed:
    logger.error("Cannot continue without valid imports")
    sys.exit(1)

logger.success("✨ All imports validated successfully!\n")

# RULE 1 & 5: Start Small → Validate → Expand
@logger.catch(message="Failed in minimal test", reraise=True)
async def test_minimal_functionality():
    """Stage 1: Test the absolute minimum."""
    logger.info("🧪 Stage 2: Testing minimal functionality")
    
    try:
        # Step 1: Create stores (simplest possible)
        session_store = MemorySessionStore()
        thought_store = MemoryThoughtStore()
        logger.success("✅ Created in-memory stores")
        
        # Step 2: Create a session (one operation)
        session = SessionData(
            session_id="demo-001",
            tool_name="Sequential Thinking Demo"
        )
        saved_session = await session_store.create_session(session)
        logger.success(f"✅ Created session: {saved_session.session_id}")
        
        # Step 3: Verify it worked (validation)
        retrieved = await session_store.get_session("demo-001")
        assert retrieved is not None, "Session not found!"
        logger.success("✅ Session retrieval works")
        
        return session_store, thought_store
        
    except Exception as e:
        logger.exception(e)
        logger.error("Failed at minimal functionality stage")
        raise

@logger.catch(message="Failed in analyzer test", reraise=True)
async def test_analyzer_basic(session_store, thought_store):
    """Stage 2: Test analyzer with one simple operation."""
    logger.info("🧪 Stage 3: Testing analyzer basic operation")
    
    try:
        # Create analyzer
        analyzer = ProgressiveSequentialThinkingAnalyzer(
            session_store=session_store,
            thought_store=thought_store
        )
        logger.success("✅ Created analyzer")
        
        # Single simple request
        request = ProgressiveThoughtRequest(
            session_id="demo-001",
            thought="What is 2+2?",
            thought_number=1,
            total_thoughts=1,
            next_thought_needed=False
        )
        logger.debug(f"Request created: {request.thought}")
        
        # Process it
        response = await analyzer.process_thought(request)
        logger.success(f"✅ Got response: {response.status}")
        logger.info(f"   Message: {response.message}")
        
        return analyzer
        
    except Exception as e:
        logger.exception(e)
        logger.error("Failed at analyzer stage")
        logger.debug(f"Session store state: {session_store._sessions}")
        raise

@logger.catch(message="Failed in multi-thought test", reraise=True)
async def test_multi_thought_chain(analyzer):
    """Stage 3: Test a chain of thoughts."""
    logger.info("🧪 Stage 4: Testing thought chain")
    
    thoughts = [
        "Let's solve a problem step by step",
        "First, identify the key components", 
        "Next, analyze the relationships",
        "Finally, synthesize a solution"
    ]
    
    session_id = "demo-002"
    responses = []
    
    for i, thought_content in enumerate(thoughts, 1):
        try:
            request = ProgressiveThoughtRequest(
                session_id=session_id,
                thought=thought_content,
                thought_number=i,
                total_thoughts=len(thoughts),
                next_thought_needed=(i < len(thoughts))
            )
            
            response = await analyzer.process_thought(request)
            responses.append(response)
            
            logger.success(f"✅ Thought {i}/{len(thoughts)}: {response.status}")
            if response.suggestion:
                logger.info(f"   Suggestion: {response.suggestion[:50]}...")
                
        except Exception as e:
            logger.exception(e)
            logger.error(f"Failed at thought {i}")
            logger.debug(f"Previous responses: {len(responses)}")
            raise
    
    logger.success(f"✅ Completed {len(responses)} thought chain")
    return responses

# RULE 6: Discovery Pattern
def discover_analyzer_methods(analyzer):
    """Discover what methods are available."""
    logger.info("🔍 Stage 5: Discovering analyzer capabilities")
    
    methods = [name for name in dir(analyzer) 
               if not name.startswith('_') and callable(getattr(analyzer, name))]
    
    logger.info("📦 Available methods:")
    for method in sorted(methods):
        logger.info(f"   - {method}")
    
    # Check stores
    logger.info("📦 Session store type: " + type(analyzer.session_store).__name__)
    logger.info("📦 Thought store type: " + type(analyzer.thought_store).__name__)

# Main execution with proper error handling
@logger.catch(reraise=True)
async def main():
    """Main test orchestration following all rules."""
    logger.info("🚀 Starting enhanced rules demonstration")
    
    all_passed = True
    
    try:
        # Stage 1: Minimal test
        session_store, thought_store = await test_minimal_functionality()
        
        # Stage 2: Basic analyzer test  
        analyzer = await test_analyzer_basic(session_store, thought_store)
        
        # Stage 3: Multi-thought test
        responses = await test_multi_thought_chain(analyzer)
        
        # Stage 4: Discovery
        discover_analyzer_methods(analyzer)
        
        # Final validation
        logger.info("📊 Final validation:")
        session_count = len(session_store._sessions)
        thought_count = len(thought_store._thoughts)
        logger.info(f"   Sessions created: {session_count}")
        logger.info(f"   Thoughts processed: {thought_count}")
        
        if session_count >= 2 and thought_count >= 5:
            logger.success("✅ All validations passed!")
        else:
            logger.warning("⚠️  Lower than expected counts")
            all_passed = False
            
    except Exception as e:
        logger.exception(e)
        logger.critical("💥 Unexpected failure in main")
        all_passed = False
    
    return all_passed

# RULE 4: Watchexec-optimized execution
if __name__ == "__main__":
    try:
        # Run async main
        success = asyncio.run(main())
        
        # Summary output
        print(f"\n{'='*60}")
        if success:
            logger.success("✅ ALL TESTS PASSED!")
            print("✅ DEMO COMPLETED SUCCESSFULLY")
        else:
            logger.error("❌ Some tests failed!")
            print("❌ DEMO FAILED")
        print(f"{'='*60}\n")
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        logger.warning("⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.exception(e)
        logger.critical("💥 Fatal error in demo")
        sys.exit(1)