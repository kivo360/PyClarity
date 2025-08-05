#!/usr/bin/env python3
"""
Test script for PyClarity MCP Server
"""

import asyncio
import logging

from pyclarity.config import MCPConfig
from pyclarity.server.mcp_server import PyClarityMCPServer

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_mcp_server():
    """Test the MCP server functionality"""
    print("🧪 Testing PyClarity MCP Server")
    print("=" * 50)

    # Create configuration
    config = MCPConfig()
    config.server.host = "localhost"
    config.server.port = 8000
    config.auth.enabled = False  # Disable auth for testing

    # Create server
    server = PyClarityMCPServer(config)

    print("✅ Server created successfully")
    print(f"📋 Available tools: {list(server.tools.list_tools().keys())}")
    print(f"🔧 Auth enabled: {config.auth.enabled}")
    print(f"🌐 Server host: {config.server.host}")
    print(f"🔌 Server port: {config.server.port}")

    # Test server start
    print("\n🚀 Starting server...")
    await server.start(host=config.server.host, port=config.server.port)

    print("\n✅ MCP Server test completed successfully!")
    print("\n💡 Next steps:")
    print("   1. Implement FastMCP integration")
    print("   2. Add tool registration for existing analyzers")
    print("   3. Implement authentication endpoints")
    print("   4. Add client library")
    print("   5. Create comprehensive tests")


if __name__ == "__main__":
    asyncio.run(test_mcp_server())
