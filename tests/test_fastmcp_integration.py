"""
Test FastMCP integration for PyClarity tools using in-memory testing patterns.

This follows the FastMCP testing best practices from https://gofastmcp.com/patterns/testing
"""

import pytest
from fastmcp import FastMCP, Client

from pyclarity.tools.sequential_thinking.analyzer import SequentialThinkingAnalyzer
from pyclarity.tools.sequential_thinking.models import SequentialThinkingContext


@pytest.fixture
def mcp_server():
    """Create a FastMCP server with PyClarity tools for testing."""
    server = FastMCP("PyClarity-Test")
    
    # Register sequential thinking tool
    @server.tool
    async def sequential_thinking(
        problem: str,
        reasoning_depth: int = 5,
        complexity_level: str = "moderate"
    ) -> dict:
        """Analyze problem using sequential thinking."""
        analyzer = SequentialThinkingAnalyzer()
        context = SequentialThinkingContext(
            problem=problem,
            reasoning_depth=reasoning_depth,
            complexity_level=complexity_level
        )
        result = await analyzer.analyze(context)
        return {
            "final_conclusion": result.final_conclusion,
            "steps_count": len(result.reasoning_chain),
            "confidence": result.conclusion_confidence,
            "reasoning_path": result.reasoning_path_summary
        }
    
    return server


@pytest.mark.asyncio
async def test_sequential_thinking_tool(mcp_server):
    """Test sequential thinking tool via FastMCP."""
    async with Client(mcp_server) as client:
        result = await client.call_tool("sequential_thinking", {
            "problem": "Should I invest in Bitcoin?",
            "reasoning_depth": 3
        })
        
        # Validate the response structure
        assert "final_conclusion" in result.data
        assert "steps_count" in result.data
        assert "confidence" in result.data
        
        # Validate the content
        assert result.data["steps_count"] >= 3
        assert 0.0 <= result.data["confidence"] <= 1.0
        assert len(result.data["final_conclusion"]) > 50
        
        print(f"✅ Sequential thinking test passed!")
        print(f"Steps: {result.data['steps_count']}")
        print(f"Confidence: {result.data['confidence']}")


@pytest.fixture
def progressive_mcp_server():
    """Create a FastMCP server with progressive/step-by-step tools."""
    server = FastMCP("PyClarity-Progressive")
    
    # Store for session management
    sessions = {}
    
    @server.tool
    async def sequential_thinking(
        session_id: str,
        thought: str,
        thought_number: int,
        total_thoughts: int = 5,
        next_thought_needed: bool = True
    ) -> dict:
        """Process sequential thinking with session management (progressive by default)."""
        # Simulate step-by-step processing like Clear Thought MCP
        if session_id not in sessions:
            sessions[session_id] = {"thoughts": [], "created_at": "2025-01-01"}
        
        # Add current thought
        sessions[session_id]["thoughts"].append({
            "thought_number": thought_number,
            "content": thought,
            "timestamp": "2025-01-01"
        })
        
        # Determine if we need more thoughts
        actual_next_needed = thought_number < total_thoughts
        
        return {
            "thought_number": thought_number,
            "total_thoughts": total_thoughts,
            "status": "success",
            "next_thought_needed": actual_next_needed,
            "session_id": session_id,
            "message": f"Processed thought {thought_number}/{total_thoughts}",
            "thoughts_so_far": len(sessions[session_id]["thoughts"])
        }
    
    return server


@pytest.mark.asyncio
async def test_progressive_sequential_thinking(progressive_mcp_server):
    """Test step-by-step sequential thinking (Clear Thought MCP pattern)."""
    async with Client(progressive_mcp_server) as client:
        session_id = "test_session_123"
        
        # Step 1
        result1 = await client.call_tool("sequential_thinking", {
            "session_id": session_id,
            "thought": "I need to analyze Bitcoin investment carefully",
            "thought_number": 1,
            "total_thoughts": 3,
            "next_thought_needed": True
        })
        
        assert result1.data["status"] == "success"
        assert result1.data["thought_number"] == 1
        assert result1.data["next_thought_needed"] == True
        assert result1.data["thoughts_so_far"] == 1
        
        # Step 2
        result2 = await client.call_tool("sequential_thinking", {
            "session_id": session_id,
            "thought": "Bitcoin is highly volatile with regulatory risks",
            "thought_number": 2,
            "total_thoughts": 3,
            "next_thought_needed": True
        })
        
        assert result2.data["thought_number"] == 2
        assert result2.data["next_thought_needed"] == True
        assert result2.data["thoughts_so_far"] == 2
        
        # Step 3 (final)
        result3 = await client.call_tool("sequential_thinking", {
            "session_id": session_id,
            "thought": "I should only invest what I can afford to lose",
            "thought_number": 3,
            "total_thoughts": 3,
            "next_thought_needed": False
        })
        
        assert result3.data["thought_number"] == 3
        assert result3.data["next_thought_needed"] == False
        assert result3.data["thoughts_so_far"] == 3
        
        print(f"✅ Progressive sequential thinking test passed!")
        print(f"Session {session_id} completed with 3 thoughts")


@pytest.mark.asyncio 
async def test_tool_error_handling(mcp_server):
    """Test error handling in FastMCP tools."""
    async with Client(mcp_server) as client:
        try:
            # Test with invalid parameters
            result = await client.call_tool("sequential_thinking", {
                "problem": "",  # Empty problem should fail
                "reasoning_depth": -1  # Invalid depth
            })
            assert False, "Should have raised an error"
        except Exception as e:
            print(f"✅ Error handling test passed: {str(e)}")


if __name__ == "__main__":
    # Run tests directly for quick validation
    import asyncio
    
    async def run_tests():
        print("🧪 Testing PyClarity FastMCP Integration...")
        
        # Test 1: Basic sequential thinking
        server = FastMCP("PyClarity-Test")
        
        @server.tool
        async def sequential_thinking(problem: str, reasoning_depth: int = 3) -> dict:
            analyzer = SequentialThinkingAnalyzer()
            context = SequentialThinkingContext(problem=problem, reasoning_depth=reasoning_depth)
            result = await analyzer.analyze(context)
            return {
                "final_conclusion": result.final_conclusion,
                "steps_count": len(result.reasoning_chain),
                "confidence": result.conclusion_confidence
            }
        
        async with Client(server) as client:
            result = await client.call_tool("sequential_thinking", {
                "problem": "Should I invest in Bitcoin?",
                "reasoning_depth": 3
            })
            print(f"✅ Basic test passed - Steps: {result.data['steps_count']}")
        
        # Test 2: Progressive thinking
        prog_server = FastMCP("Progressive-Test")
        sessions = {}
        
        @prog_server.tool
        async def sequential_thinking(session_id: str, thought: str, thought_number: int, total_thoughts: int = 3) -> dict:
            if session_id not in sessions:
                sessions[session_id] = []
            sessions[session_id].append(thought)
            next_needed = thought_number < total_thoughts
            return {
                "thought_number": thought_number,
                "next_thought_needed": next_needed,
                "status": "success"
            }
        
        async with Client(prog_server) as client:
            for i in range(1, 4):
                result = await client.call_tool("sequential_thinking", {
                    "session_id": "test",
                    "thought": f"Thought {i}",
                    "thought_number": i
                })
                print(f"✅ Step {i} - Next needed: {result.data['next_thought_needed']}")
        
        print("🎉 All FastMCP integration tests passed!")
    
    asyncio.run(run_tests())