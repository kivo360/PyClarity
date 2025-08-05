"""
Example: Progressive Sequential Thinking with Session State

This example demonstrates how to use the progressive Sequential Thinking tool
that maintains state between calls, allowing for true step-by-step reasoning.
"""

import asyncio
import json
import os
from typing import Any, Dict

# For demonstration, we'll simulate MCP client calls
# In real usage, this would be called through an MCP client


class ProgressiveThinkingExample:
    """Example client for progressive sequential thinking."""

    def __init__(self):
        self.session_id = None
        self.thought_history = []

    async def start_thinking_session(self, problem: str) -> dict[str, Any]:
        """Start a new progressive thinking session."""
        # Initial thought - problem decomposition
        response = await self.call_tool(
            "progressive_sequential_thinking",
            {
                "thought": f"Let me break down this problem: {problem}. The key components appear to be the need for systematic analysis, identification of core issues, and development of actionable solutions.",
                "thought_number": 1,
                "total_thoughts": 5,
                "next_thought_needed": True,
            },
        )

        if response["success"]:
            self.session_id = response["response"]["sessionId"]
            self.thought_history.append(response["response"])

        return response

    async def continue_thinking(self, thought_content: str, thought_number: int) -> dict[str, Any]:
        """Continue the thinking session with the next thought."""
        response = await self.call_tool(
            "progressive_sequential_thinking",
            {
                "session_id": self.session_id,
                "thought": thought_content,
                "thought_number": thought_number,
                "total_thoughts": 5,
                "next_thought_needed": thought_number < 5,
            },
        )

        if response["success"]:
            self.thought_history.append(response["response"])

        return response

    async def branch_thinking(self, thought_content: str, branch_from: int) -> dict[str, Any]:
        """Create a branch in the thinking process."""
        response = await self.call_tool(
            "progressive_sequential_thinking",
            {
                "session_id": self.session_id,
                "thought": thought_content,
                "thought_number": len(self.thought_history) + 1,
                "total_thoughts": 7,  # Extended for branch
                "next_thought_needed": True,
                "branch_from_thought": branch_from,
                "branch_id": "alternative_hypothesis",
            },
        )

        if response["success"]:
            self.thought_history.append(response["response"])

        return response

    async def revise_thought(self, thought_content: str, revises: int) -> dict[str, Any]:
        """Revise a previous thought."""
        response = await self.call_tool(
            "progressive_sequential_thinking",
            {
                "session_id": self.session_id,
                "thought": thought_content,
                "thought_number": len(self.thought_history) + 1,
                "total_thoughts": 6,  # Extended for revision
                "next_thought_needed": True,
                "is_revision": True,
                "revises_thought": revises,
            },
        )

        if response["success"]:
            self.thought_history.append(response["response"])

        return response

    async def get_all_thoughts(self) -> dict[str, Any]:
        """Retrieve all thoughts from the session."""
        return await self.call_tool("get_session_thoughts", {"session_id": self.session_id})

    async def call_tool(self, tool_name: str, args: dict[str, Any]) -> dict[str, Any]:
        """Simulate calling an MCP tool."""
        # In real usage, this would call the actual MCP server
        # For this example, we'll simulate the response
        print(f"\n🔧 Calling tool: {tool_name}")
        print(f"   Args: {json.dumps(args, indent=2)}")

        # Simulate successful response
        if tool_name == "progressive_sequential_thinking":
            thought_number = args.get("thought_number", 1)
            suggestion = self._get_suggestion_for_thought(thought_number)

            return {
                "success": True,
                "response": {
                    "sessionId": self.session_id or "example-session-123",
                    "thoughtId": len(self.thought_history) + 1,
                    "thoughtNumber": thought_number,
                    "totalThoughts": args.get("total_thoughts", 5),
                    "status": "success",
                    "nextThoughtNeeded": args.get("next_thought_needed", True),
                    "isRevision": args.get("is_revision", False),
                    "branchId": args.get("branch_id"),
                    "message": f"Processed thought {thought_number}",
                    "suggestion": suggestion,
                    "confidence": 0.85,
                    "thoughtType": self._get_thought_type(thought_number),
                    "progress": {
                        "currentChainLength": len(self.thought_history) + 1,
                        "percentComplete": (thought_number / args.get("total_thoughts", 5)) * 100,
                        "thoughtsRemaining": max(0, args.get("total_thoughts", 5) - thought_number),
                        "onTrack": True,
                        "branch": args.get("branch_id") is not None,
                    },
                },
            }

        elif tool_name == "get_session_thoughts":
            return {
                "success": True,
                "thoughts": self.thought_history,
                "count": len(self.thought_history),
            }

        return {"success": False, "error": "Unknown tool"}

    def _get_suggestion_for_thought(self, thought_number: int) -> str:
        """Get suggestion for next thought based on current position."""
        suggestions = {
            1: "Now identify the key hypotheses or potential causes",
            2: "Gather evidence to support or refute these hypotheses",
            3: "Apply logical reasoning to analyze the evidence",
            4: "Look for patterns and synthesize insights",
            5: "Formulate conclusions and recommendations",
        }
        return suggestions.get(thought_number, "Continue developing the reasoning chain")

    def _get_thought_type(self, thought_number: int) -> str:
        """Get thought type based on position in sequence."""
        types = {
            1: "problem_decomposition",
            2: "hypothesis_formation",
            3: "evidence_gathering",
            4: "logical_deduction",
            5: "conclusion",
        }
        return types.get(thought_number, "synthesis")


async def run_example():
    """Run the progressive thinking example."""
    print("🧠 Progressive Sequential Thinking Example")
    print("=" * 50)

    example = ProgressiveThinkingExample()

    # Start with a problem
    problem = "How can we improve user engagement on our platform?"

    print(f"\n📋 Problem: {problem}")
    print("\n🔄 Starting progressive thinking session...\n")

    # Step 1: Initial problem decomposition
    response = await example.start_thinking_session(problem)
    print(f"\n✅ Step 1 Complete - Session ID: {response['response']['sessionId']}")
    print(f"   Suggestion: {response['response']['suggestion']}")

    # Step 2: Hypothesis formation
    await asyncio.sleep(1)  # Simulate thinking time
    response = await example.continue_thinking(
        "Based on the decomposition, I hypothesize that user engagement is primarily affected by three factors: content relevance, user interface complexity, and social features. The lack of personalization might be the key issue.",
        2,
    )
    print(f"\n✅ Step 2 Complete - Thought Type: {response['response']['thoughtType']}")
    print(f"   Confidence: {response['response']['confidence']}")

    # Step 3: Evidence gathering
    await asyncio.sleep(1)
    response = await example.continue_thinking(
        "Evidence from user analytics shows: 1) 60% of users leave within 2 minutes, 2) Only 15% use social features, 3) Content recommendations have a 25% click-through rate. User surveys indicate confusion with navigation.",
        3,
    )
    print(
        f"\n✅ Step 3 Complete - Progress: {response['response']['progress']['percentComplete']}%"
    )

    # Step 3.5: Branch to explore alternative hypothesis
    await asyncio.sleep(1)
    print("\n🌿 Creating branch to explore alternative hypothesis...")
    response = await example.branch_thinking(
        "Alternative hypothesis: The issue might not be the platform itself but the onboarding process. New users might not understand the value proposition clearly.",
        2,  # Branching from thought 2
    )
    print(f"   Branch created: {response['response']['branchId']}")

    # Step 4: Logical deduction (main branch)
    await asyncio.sleep(1)
    response = await example.continue_thinking(
        "Logical analysis reveals that UI complexity correlates strongly with early user departure. The evidence suggests simplifying navigation and improving content personalization would have the highest impact.",
        4,
    )
    print(
        f"\n✅ Step 4 Complete - Remaining thoughts: {response['response']['progress']['thoughtsRemaining']}"
    )

    # Step 4.5: Revise earlier thought based on new insights
    await asyncio.sleep(1)
    print("\n📝 Revising thought 2 based on new evidence...")
    response = await example.revise_thought(
        "Revised hypothesis: User engagement is affected by both platform complexity AND onboarding effectiveness. The combination of poor initial experience and complex UI creates a compounding negative effect.",
        2,  # Revising thought 2
    )
    print(f"   Revision complete - Is revision: {response['response']['isRevision']}")

    # Step 5: Final conclusion
    await asyncio.sleep(1)
    response = await example.continue_thinking(
        "Conclusion: To improve user engagement, we should: 1) Simplify the UI with focus on core features, 2) Implement progressive disclosure for advanced features, 3) Create an interactive onboarding tutorial, 4) Enhance content personalization algorithms. Expected improvement: 40-50% in user retention.",
        5,
    )
    print("\n✅ Step 5 Complete - Thinking session finished!")
    print(f"   Final confidence: {response['response']['confidence']}")

    # Retrieve all thoughts
    print("\n📚 Retrieving complete thought history...")
    all_thoughts = await example.get_all_thoughts()
    print(f"\nTotal thoughts generated: {all_thoughts['count']}")

    # Display summary
    print("\n" + "=" * 50)
    print("📊 Session Summary:")
    print(f"   • Total thoughts: {len(example.thought_history)}")
    print("   • Branches created: 1")
    print("   • Revisions made: 1")
    print("   • Final status: Complete")

    print("\n💡 Key Insights:")
    print("   1. UI complexity is the primary barrier to engagement")
    print("   2. Onboarding process needs significant improvement")
    print("   3. Personalization can increase content relevance")
    print("   4. Progressive disclosure can reduce initial complexity")


if __name__ == "__main__":
    # Run the example
    asyncio.run(run_example())
