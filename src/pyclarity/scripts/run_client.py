import asyncio

from fastmcp import Client, FastMCP
from mcp.types import Tool
from rich import print

from pyclarity.server.mcp_server import create_server

# In-memory server (ideal for testing)
# server = FastMCP("TestServer")
server = create_server()


@server.tool
def example_tool(param: str) -> str:
    return f"Hello, {param}!"


client = Client(server)

# # HTTP server
# client = Client("https://example.com/mcp")

# # Local Python script
# client = Client("my_mcp_server.py")


async def main():
    async with client:
        # Basic server interaction
        await client.ping()

        # List available operations
        tools: list[Tool] = await client.list_tools()

        for tool in tools:
            print(tool.name)
            print(tool.description)
            # print(tool.parameters)
            # print(tool.result)
            # print(tool.tags)
            # print(tool.deprecated)

        resources = await client.list_resources()
        prompts = await client.list_prompts()
        # print(tools)
        # print(resources)
        # print(prompts)
        # Execute operations
        sequential_thinking_input = {
            "problem": "How should we design a scalable microservices architecture for an e-commerce platform?",
            "complexity_level": "complex",
            "reasoning_depth": 8,
            "enable_branching": True,
            "enable_revision": True,
            "branch_strategy": "parallel_exploration",
        }
        result = await client.call_tool("sequential_thinking", sequential_thinking_input)
        print(result)


asyncio.run(main())
