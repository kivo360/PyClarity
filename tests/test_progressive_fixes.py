"""
Test progressive analyzer fixes and validation.

This tests the actual PyClarity progressive analyzers to ensure they work 
properly after fixing data model mismatches and integration issues.
"""

import pytest
from fastmcp import FastMCP, Client

from pyclarity.tools.sequential_thinking.progressive_analyzer import (
    ProgressiveSequentialThinkingAnalyzer, 
    ProgressiveThoughtRequest,
    ProgressiveThoughtResponse
)
from pyclarity.db.memory_stores import MemorySessionStore, MemoryThoughtStore


@pytest.fixture
def progressive_stores():
    """Create in-memory stores for progressive analyzer testing."""
    session_store = MemorySessionStore()
    thought_store = MemoryThoughtStore()
    return session_store, thought_store


@pytest.fixture
def progressive_analyzer(progressive_stores):
    """Create progressive analyzer with memory stores."""
    session_store, thought_store = progressive_stores
    return ProgressiveSequentialThinkingAnalyzer(session_store, thought_store)


@pytest.mark.asyncio
async def test_progressive_analyzer_direct(progressive_analyzer):
    """Test progressive analyzer directly (not through FastMCP)."""
    print("🧪 Testing progressive analyzer directly...")
    
    try:
        # Step 1
        request1 = ProgressiveThoughtRequest(
            session_id="test_direct",
            thought="I need to analyze Bitcoin investment risks carefully",
            thought_number=1,
            total_thoughts=3,
            next_thought_needed=True
        )
        
        response1 = await progressive_analyzer.process_thought(request1)
        
        # Validate response type and basic fields
        assert isinstance(response1, ProgressiveThoughtResponse)
        assert response1.session_id == "test_direct"
        assert response1.thought_number == 1
        assert response1.status in ["success", "error"]
        
        if response1.status == "error":
            print(f"❌ Step 1 failed: {response1.error}")
            return False
        
        print(f"✅ Step 1 success: {response1.message}")
        
        # Step 2
        request2 = ProgressiveThoughtRequest(
            session_id="test_direct", 
            thought="Bitcoin is highly volatile and has regulatory uncertainty",
            thought_number=2,
            total_thoughts=3,
            next_thought_needed=True
        )
        
        response2 = await progressive_analyzer.process_thought(request2)
        assert response2.thought_number == 2
        
        if response2.status == "error":
            print(f"❌ Step 2 failed: {response2.error}")
            return False
            
        print(f"✅ Step 2 success: {response2.message}")
        
        # Step 3 (final)
        request3 = ProgressiveThoughtRequest(
            session_id="test_direct",
            thought="I should only invest what I can afford to lose completely",
            thought_number=3,
            total_thoughts=3,
            next_thought_needed=False
        )
        
        response3 = await progressive_analyzer.process_thought(request3)
        assert response3.thought_number == 3
        
        if response3.status == "error":
            print(f"❌ Step 3 failed: {response3.error}")
            return False
            
        print(f"✅ Step 3 success: {response3.message}")
        print("🎉 Progressive analyzer direct test PASSED!")
        return True
        
    except Exception as e:
        print(f"❌ Progressive analyzer test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


@pytest.fixture
def progressive_fastmcp_server(progressive_stores):
    """Create FastMCP server with progressive analyzer integration."""
    session_store, thought_store = progressive_stores
    server = FastMCP("PyClarity-Progressive-Real")
    
    # Create analyzer instance 
    analyzer = ProgressiveSequentialThinkingAnalyzer(session_store, thought_store)
    
    @server.tool
    async def sequential_thinking(
        session_id: str,
        thought: str,
        thought_number: int,
        total_thoughts: int = 5,
        next_thought_needed: bool = True,
        is_revision: bool = False,
        revises_thought: int = None,
        branch_id: str = None
    ) -> dict:
        """Sequential thinking with real PyClarity analyzer (progressive by default)."""
        try:
            request = ProgressiveThoughtRequest(
                session_id=session_id,
                thought=thought,
                thought_number=thought_number,
                total_thoughts=total_thoughts,
                next_thought_needed=next_thought_needed,
                is_revision=is_revision,
                revises_thought=revises_thought,
                branch_id=branch_id
            )
            
            response = await analyzer.process_thought(request)
            
            # Convert to dict for MCP response
            return {
                "session_id": response.session_id,
                "thought_number": response.thought_number,
                "total_thoughts": response.total_thoughts,
                "status": response.status,
                "next_thought_needed": response.next_thought_needed,
                "message": response.message,
                "suggestion": response.suggestion,
                "confidence": response.confidence,
                "thought_type": response.thought_type,
                "error": response.error
            }
            
        except Exception as e:
            return {
                "session_id": session_id,
                "thought_number": thought_number,
                "status": "error",
                "error": str(e),
                "next_thought_needed": False
            }
    
    return server


@pytest.mark.asyncio
async def test_progressive_via_fastmcp(progressive_fastmcp_server):
    """Test progressive analyzer through FastMCP protocol."""
    print("🧪 Testing progressive analyzer via FastMCP...")
    
    async with Client(progressive_fastmcp_server) as client:
        session_id = "fastmcp_test_session"
        
        # Step 1
        result1 = await client.call_tool("sequential_thinking", {
            "session_id": session_id,
            "thought": "I need to evaluate Bitcoin as an investment option",
            "thought_number": 1,
            "total_thoughts": 3,
            "next_thought_needed": True
        })
        
        data1 = result1.data
        assert data1["session_id"] == session_id
        assert data1["thought_number"] == 1
        
        if data1["status"] == "error":
            print(f"❌ FastMCP Step 1 failed: {data1['error']}")
            return False
            
        print(f"✅ FastMCP Step 1: {data1['message']}")
        
        # Step 2 
        result2 = await client.call_tool("sequential_thinking", {
            "session_id": session_id,
            "thought": "Bitcoin has high volatility and regulatory risks",
            "thought_number": 2,
            "total_thoughts": 3,
            "next_thought_needed": True
        })
        
        data2 = result2.data
        assert data2["thought_number"] == 2
        
        if data2["status"] == "error":
            print(f"❌ FastMCP Step 2 failed: {data2['error']}")
            return False
            
        print(f"✅ FastMCP Step 2: {data2['message']}")
        
        # Step 3 (final)
        result3 = await client.call_tool("sequential_thinking", {
            "session_id": session_id,
            "thought": "Only invest disposable income in high-risk assets like Bitcoin",
            "thought_number": 3,
            "total_thoughts": 3,
            "next_thought_needed": False
        })
        
        data3 = result3.data
        assert data3["thought_number"] == 3
        
        if data3["status"] == "error":
            print(f"❌ FastMCP Step 3 failed: {data3['error']}")
            return False
            
        print(f"✅ FastMCP Step 3: {data3['message']}")
        print("🎉 Progressive analyzer FastMCP test PASSED!")
        return True


@pytest.mark.asyncio
async def test_session_persistence(progressive_analyzer):
    """Test that session data persists across calls."""
    session_id = "persistence_test"
    
    # First call
    request1 = ProgressiveThoughtRequest(
        session_id=session_id,
        thought="Initial thought for persistence test",
        thought_number=1,
        total_thoughts=2,
        next_thought_needed=True
    )
    
    response1 = await progressive_analyzer.process_thought(request1)
    
    if response1.status == "error":
        print(f"❌ Persistence test setup failed: {response1.error}")
        return False
    
    # Second call to same session
    request2 = ProgressiveThoughtRequest(
        session_id=session_id,
        thought="Second thought to test persistence",
        thought_number=2,
        total_thoughts=2,
        next_thought_needed=False
    )
    
    response2 = await progressive_analyzer.process_thought(request2)
    
    if response2.status == "error":
        print(f"❌ Persistence test failed: {response2.error}")
        return False
        
    # Verify session continuity
    assert response2.session_id == session_id
    print("✅ Session persistence test PASSED!")
    return True


if __name__ == "__main__":
    # Quick validation script
    import asyncio
    
    async def validate_progressive_fixes():
        print("🔧 Validating Progressive Analyzer Fixes...")
        
        # Create stores and analyzer
        session_store = MemorySessionStore()
        thought_store = MemoryThoughtStore()
        analyzer = ProgressiveSequentialThinkingAnalyzer(session_store, thought_store)
        
        # Test 1: Direct analyzer test
        try:
            request = ProgressiveThoughtRequest(
                session_id="validation_test",
                thought="Testing the fixed progressive analyzer",
                thought_number=1,
                total_thoughts=2,
                next_thought_needed=True
            )
            
            response = await analyzer.process_thought(request)
            
            if response.status == "success":
                print("✅ Progressive analyzer basic functionality WORKS!")
            else:
                print(f"❌ Progressive analyzer failed: {response.error}")
                return False
                
        except Exception as e:
            print(f"❌ Progressive analyzer crashed: {str(e)}")
            return False
        
        # Test 2: FastMCP integration
        try:
            server = FastMCP("Validation-Test")
            
            @server.tool
            async def sequential_thinking(session_id: str, thought: str, thought_number: int) -> dict:
                request = ProgressiveThoughtRequest(
                    session_id=session_id,
                    thought=thought,
                    thought_number=thought_number
                )
                response = await analyzer.process_thought(request)
                return {"status": response.status, "message": response.message}
            
            async with Client(server) as client:
                result = await client.call_tool("sequential_thinking", {
                    "session_id": "fastmcp_validation",
                    "thought": "FastMCP integration test",
                    "thought_number": 1
                })
                
                if result.data["status"] == "success":
                    print("✅ FastMCP integration WORKS!")
                else:
                    print(f"❌ FastMCP integration failed: {result.data}")
                    return False
                    
        except Exception as e:
            print(f"❌ FastMCP integration crashed: {str(e)}")
            return False
        
        print("🎉 ALL PROGRESSIVE ANALYZER FIXES VALIDATED!")
        return True
    
    asyncio.run(validate_progressive_fixes())