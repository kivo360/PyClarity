#!/usr/bin/env python3
"""
Example: Using PyClarity FastMCP Server

This example demonstrates how to test the PyClarity cognitive tools
through the FastMCP server interface.
"""

import asyncio
import sys
from pathlib import Path

# Add src to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fastmcp import Client
from pyclarity.mcp_app import app


async def demonstrate_cognitive_tools():
    """Demonstrate PyClarity cognitive tools via FastMCP."""
    client = Client(app)
    
    async with client:
        print("🧠 PyClarity Cognitive Tools Demonstration")
        print("=" * 50)
        
        # 1. Sequential Thinking
        print("\n1. 🔄 Sequential Thinking Analysis")
        result = await client.call_tool("sequential_thinking", {
            "problem": "How to increase customer retention for a SaaS product",
            "complexity_level": "moderate",
            "reasoning_depth": 3
        })
        
        if "error" not in result.data:
            print(f"   Generated {len(result.data.get('reasoning_chain', []))} reasoning steps")
            print(f"   Final conclusion confidence: {result.data.get('conclusion_confidence', 0):.2f}")
        else:
            print(f"   Error: {result.data['error']}")
        
        # 2. Mental Models
        print("\n2. 🧩 Mental Models Analysis")
        result = await client.call_tool("mental_models", {
            "problem": "Should we launch our product now or wait 3 months for more features?",
            "model_type": "opportunity_cost",
            "complexity_level": "moderate"
        })
        
        if "error" not in result.data:
            print("   Applied opportunity cost mental model")
            print("   Analysis completed successfully")
        else:
            print(f"   Error: {result.data['error']}")
        
        # 3. Decision Framework  
        print("\n3. ⚖️  Decision Framework Analysis")
        result = await client.call_tool("decision_framework", {
            "problem": "Choose marketing strategy for Q4",
            "criteria_names": ["cost", "reach", "conversion"],
            "option_names": ["social_media", "paid_ads", "content_marketing"]
        })
        
        if "error" not in result.data:
            print("   Evaluated 3 marketing options against 3 criteria")
            print("   Generated structured decision analysis")
        else:
            print(f"   Error: {result.data['error']}")
        
        # 4. Server Info
        print("\n4. ℹ️  Server Information")
        result = await client.call_tool("server_info", {})
        info = result.data
        print(f"   Server: {info['server']} v{info['version']}")
        print(f"   Available tools: {len(info['tools'])}")
        
        print("\n✅ Demonstration completed!")
        print("\nTo start the server: python src/pyclarity/mcp_app.py")


if __name__ == "__main__":
    asyncio.run(demonstrate_cognitive_tools())