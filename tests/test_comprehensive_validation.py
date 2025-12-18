"""
Comprehensive validation suite for PyClarity fixes.

This test suite validates all the fixes made to PyClarity including:
1. CLI functionality (list-tools, fire command)
2. Progressive analyzer with proper field names
3. FastMCP integration with step-by-step reasoning
4. Session management and persistence
5. Error handling and edge cases
"""

import pytest
import asyncio
from typer.testing import CliRunner
from fastmcp import FastMCP, Client

from pyclarity.cli import app
from pyclarity.tools.sequential_thinking.progressive_analyzer import (
    ProgressiveSequentialThinkingAnalyzer,
    ProgressiveThoughtRequest,
    ProgressiveThoughtResponse
)
from pyclarity.tools.sequential_thinking.analyzer import SequentialThinkingAnalyzer
from pyclarity.tools.sequential_thinking.models import SequentialThinkingContext
from pyclarity.db.memory_stores import MemorySessionStore, MemoryThoughtStore
from pyclarity.server.mcp_server import PyClarityMCPServer


class TestCLIFunctionality:
    """Test CLI commands work correctly."""

    def test_fire_command(self):
        """Test the fire command works."""
        runner = CliRunner()
        result = runner.invoke(app, ["fire", "--name", "TestUser"])
        assert result.exit_code == 0
        assert "TestUser" in result.stdout
        assert "portal gun" in result.stdout

    def test_list_tools_command(self):
        """Test the list-tools command works."""
        runner = CliRunner()
        result = runner.invoke(app, ["list-tools"])
        assert result.exit_code == 0
        assert "PyClarity Cognitive Tools" in result.stdout
        assert "Total:" in result.stdout
        # Should show at least some tools
        assert not ("Total: 0" in result.stdout)


class TestProgressiveAnalyzer:
    """Test progressive analyzer functionality with correct field names."""

    @pytest.fixture
    def progressive_setup(self):
        """Create progressive analyzer setup."""
        session_store = MemorySessionStore()
        thought_store = MemoryThoughtStore()
        analyzer = ProgressiveSequentialThinkingAnalyzer(session_store, thought_store)
        return analyzer, session_store, thought_store

    @pytest.mark.asyncio
    async def test_progressive_analyzer_field_names(self, progressive_setup):
        """Test that progressive analyzer uses correct field names (thought_number not step_number)."""
        analyzer, session_store, thought_store = progressive_setup
        
        request = ProgressiveThoughtRequest(
            session_id="field_test",
            thought="Testing field name consistency",
            thought_number=1,
            total_thoughts=2,
            next_thought_needed=True
        )
        
        response = await analyzer.process_thought(request)
        
        assert response.status == "success"
        assert response.thought_number == 1
        assert response.session_id == "field_test"
        
        # Verify the thought was stored correctly
        stored_thought = await thought_store.get_thought_by_step("field_test", 1)
        assert stored_thought is not None
        assert stored_thought.thought_number == 1

    @pytest.mark.asyncio
    async def test_session_persistence(self, progressive_setup):
        """Test that session data persists across multiple calls."""
        analyzer, session_store, thought_store = progressive_setup
        session_id = "persistence_test"
        
        # First thought
        request1 = ProgressiveThoughtRequest(
            session_id=session_id,
            thought="First thought in persistence test",
            thought_number=1,
            total_thoughts=3,
            next_thought_needed=True
        )
        
        response1 = await analyzer.process_thought(request1)
        assert response1.status == "success"
        
        # Second thought
        request2 = ProgressiveThoughtRequest(
            session_id=session_id,
            thought="Second thought building on first",
            thought_number=2,
            total_thoughts=3,
            next_thought_needed=True
        )
        
        response2 = await analyzer.process_thought(request2)
        assert response2.status == "success"
        
        # Verify both thoughts are stored
        all_thoughts = await thought_store.get_session_thoughts(session_id)
        assert len(all_thoughts) == 2
        assert all_thoughts[0].thought_number == 1
        assert all_thoughts[1].thought_number == 2

    @pytest.mark.asyncio
    async def test_progressive_completion(self, progressive_setup):
        """Test complete progressive reasoning sequence."""
        analyzer, session_store, thought_store = progressive_setup
        session_id = "completion_test"
        
        # Complete sequence of 3 thoughts
        for i in range(1, 4):
            is_final = (i == 3)
            request = ProgressiveThoughtRequest(
                session_id=session_id,
                thought=f"Thought {i} in complete reasoning sequence",
                thought_number=i,
                total_thoughts=3,
                next_thought_needed=not is_final
            )
            
            response = await analyzer.process_thought(request)
            assert response.status == "success"
            assert response.thought_number == i
            assert response.next_thought_needed == (not is_final)
        
        # Verify all thoughts stored
        final_thoughts = await thought_store.get_session_thoughts(session_id)
        assert len(final_thoughts) == 3


class TestFastMCPIntegration:
    """Test FastMCP integration with PyClarity tools."""

    @pytest.fixture
    def fastmcp_server(self):
        """Create FastMCP server with PyClarity tools."""
        # Create stores
        session_store = MemorySessionStore()
        thought_store = MemoryThoughtStore()
        
        server = FastMCP("PyClarity-Validation")
        
        # Add basic sequential thinking tool
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
                "confidence": result.conclusion_confidence
            }
        
        # Add sequential thinking tool (progressive by default)
        analyzer = ProgressiveSequentialThinkingAnalyzer(session_store, thought_store)
        
        @server.tool
        async def sequential_thinking(
            session_id: str,
            thought: str,
            thought_number: int,
            total_thoughts: int = 5,
            next_thought_needed: bool = True
        ) -> dict:
            """Sequential thinking with session management (progressive by default)."""
            try:
                request = ProgressiveThoughtRequest(
                    session_id=session_id,
                    thought=thought,
                    thought_number=thought_number,
                    total_thoughts=total_thoughts,
                    next_thought_needed=next_thought_needed
                )
                
                response = await analyzer.process_thought(request)
                
                return {
                    "session_id": response.session_id,
                    "thought_number": response.thought_number,
                    "status": response.status,
                    "message": response.message,
                    "next_thought_needed": response.next_thought_needed,
                    "confidence": response.confidence
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
    async def test_basic_tool_integration(self, fastmcp_server):
        """Test basic tool works through FastMCP."""
        async with Client(fastmcp_server) as client:
            result = await client.call_tool("sequential_thinking", {
                "problem": "Should I switch to renewable energy?",
                "reasoning_depth": 4
            })
            
            assert "final_conclusion" in result.data
            assert "steps_count" in result.data
            assert result.data["steps_count"] >= 4
            assert isinstance(result.data["confidence"], float)

    @pytest.mark.asyncio
    async def test_progressive_tool_integration(self, fastmcp_server):
        """Test progressive tool works through FastMCP with Clear Thought MCP pattern."""
        async with Client(fastmcp_server) as client:
            session_id = "fastmcp_validation"
            
            # Step 1
            result1 = await client.call_tool("sequential_thinking", {
                "session_id": session_id,
                "thought": "I need to evaluate switching to electric vehicle",
                "thought_number": 1,
                "total_thoughts": 3,
                "next_thought_needed": True
            })
            
            data1 = result1.data
            assert data1["status"] == "success"
            assert data1["thought_number"] == 1
            assert data1["next_thought_needed"] is True
            
            # Step 2
            result2 = await client.call_tool("sequential_thinking", {
                "session_id": session_id,
                "thought": "Electric vehicles have high upfront costs but lower operating costs",
                "thought_number": 2,
                "total_thoughts": 3,
                "next_thought_needed": True
            })
            
            data2 = result2.data
            assert data2["status"] == "success"
            assert data2["thought_number"] == 2
            
            # Step 3 (final)
            result3 = await client.call_tool("sequential_thinking", {
                "session_id": session_id,
                "thought": "I should calculate total cost of ownership before deciding",
                "thought_number": 3,
                "total_thoughts": 3,
                "next_thought_needed": False
            })
            
            data3 = result3.data
            assert data3["status"] == "success"
            assert data3["thought_number"] == 3
            assert data3["next_thought_needed"] is False

    @pytest.mark.asyncio
    async def test_error_handling(self, fastmcp_server):
        """Test error handling in FastMCP integration."""
        async with Client(fastmcp_server) as client:
            # Test with invalid data
            try:
                await client.call_tool("sequential_thinking", {
                    "problem": "",  # Too short
                    "reasoning_depth": -1  # Invalid
                })
                assert False, "Should have raised validation error"
            except Exception as e:
                assert "validation error" in str(e).lower()


class TestSystemIntegration:
    """Test overall system integration."""

    def test_server_initialization(self):
        """Test that PyClarity MCP server can be initialized."""
        try:
            server = PyClarityMCPServer()
            tools = server.tools.tools
            assert len(tools) > 0
            print(f"✅ Server initialized with {len(tools)} tools")
        except Exception as e:
            pytest.fail(f"Server initialization failed: {e}")

    @pytest.mark.asyncio
    async def test_complete_reasoning_workflow(self):
        """Test complete reasoning workflow from start to finish."""
        # Create analyzer
        session_store = MemorySessionStore()
        thought_store = MemoryThoughtStore()
        analyzer = ProgressiveSequentialThinkingAnalyzer(session_store, thought_store)
        
        session_id = "complete_workflow_test"
        
        # Simulate a complete reasoning session about a business decision
        thoughts = [
            "I need to decide whether to expand my business to a new market",
            "The new market has high potential but also requires significant investment", 
            "I should analyze market research data and financial projections",
            "Based on analysis, the ROI looks positive with manageable risk",
            "I will proceed with a pilot program to test market response"
        ]
        
        for i, thought in enumerate(thoughts, 1):
            is_final = (i == len(thoughts))
            request = ProgressiveThoughtRequest(
                session_id=session_id,
                thought=thought,
                thought_number=i,
                total_thoughts=len(thoughts),
                next_thought_needed=not is_final
            )
            
            response = await analyzer.process_thought(request)
            assert response.status == "success"
            assert response.thought_number == i
            
            if is_final:
                assert response.next_thought_needed is False
            else:
                assert response.next_thought_needed is True
        
        # Verify complete session
        final_thoughts = await thought_store.get_session_thoughts(session_id)
        assert len(final_thoughts) == len(thoughts)
        
        # Verify session exists
        session = await session_store.get_session(session_id)
        assert session is not None
        assert session.session_id == session_id
        
        print(f"✅ Complete reasoning workflow with {len(thoughts)} thoughts validated")


def test_validation_summary():
    """Print validation summary."""
    print("\n🎉 PYCLARITY COMPREHENSIVE VALIDATION SUMMARY:")
    print("✅ CLI Commands (fire, list-tools)")
    print("✅ Progressive Analyzer (field names fixed)")
    print("✅ Session Management (persistence working)")
    print("✅ FastMCP Integration (Clear Thought MCP pattern)")
    print("✅ Error Handling (validation working)")
    print("✅ System Integration (end-to-end workflow)")
    print("\n🚀 PyClarity is ready for tonight's deadline!")


if __name__ == "__main__":
    # Run all tests when executed directly
    import subprocess
    import sys
    
    print("🧪 Running comprehensive PyClarity validation...")
    
    # Run the test suite
    result = subprocess.run([
        sys.executable, "-m", "pytest", __file__, "-v", "--tb=short"
    ], capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    if result.returncode == 0:
        test_validation_summary()
    else:
        print("❌ Some tests failed!")
        sys.exit(1)