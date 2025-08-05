import asyncio

from pyclarity.config import MCPConfig
from pyclarity.server.mcp_server import PyClarityMCPServer


def create_server():
    """Create and return a PyClarity MCP server instance"""
    config = MCPConfig()
    return PyClarityMCPServer(config)


app = create_server()


if __name__ == "__main__":
    asyncio.run(app.start(host="0.0.0.0", port=9020))
