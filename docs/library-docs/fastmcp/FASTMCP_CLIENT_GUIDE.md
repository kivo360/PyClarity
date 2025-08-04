# FastMCP Client Usage Guide for PyClarity

This guide documents the correct usage patterns for FastMCP client integration based on the official documentation.

## Key Concepts

1. **FastMCP uses `Client` (not `FastMCP`) for client operations**
2. **Tools are called via `client.call_tool()` within an async context**
3. **The client must be used within an `async with` context manager**
4. **For local servers, use stdio transport (default for .py files)**
5. **For testing, use in-memory transport by passing FastMCP instance directly**

## Client Creation Patterns

### 1. In-Memory Client (Best for Testing)
```python
from fastmcp import FastMCP, Client

# Create server
mcp = FastMCP("TestServer")

@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"

# Create client with in-memory transport
client = Client(mcp)

async with client:
    result = await client.call_tool("greet", {"name": "World"})
```

### 2. Local Python Script Client (stdio)
```python
from fastmcp import Client

# Automatically uses stdio transport
client = Client("my_server.py")

# Or with explicit environment variables
client = Client(
    "my_server.py",
    env={"API_KEY": "secret", "DEBUG": "true"}
)

async with client:
    result = await client.call_tool("tool_name", {"param": "value"})
```

### 3. Configuration-Based Client
```python
from fastmcp import Client

config = {
    "mcpServers": {
        "pyclarity": {
            "command": "python",
            "args": ["-m", "pyclarity.server"],
            "env": {"LOG_LEVEL": "INFO"}
        }
    }
}

client = Client(config)

async with client:
    # For single server, tools are called directly
    result = await client.call_tool("mental_models_analysis", {
        "problem": "Analyze this",
        "model_type": "first_principles"
    })
```

### 4. Multi-Server Configuration
```python
config = {
    "mcpServers": {
        "pyclarity": {
            "command": "python",
            "args": ["-m", "pyclarity.server"],
        },
        "weather": {
            "url": "https://weather.example.com/mcp",
            "transport": "http"
        }
    }
}

client = Client(config)

async with client:
    # Tools are prefixed with server name
    cognitive_result = await client.call_tool("pyclarity_mental_models_analysis", {...})
    weather_result = await client.call_tool("weather_get_forecast", {"city": "NYC"})
```

## Tool Calling Patterns

### Basic Tool Call
```python
async with client:
    result = await client.call_tool(
        "tool_name",
        {
            "param1": "value1",
            "param2": "value2"
        }
    )
    
    # Access result data
    print(result.data)  # For tools that return data
    print(result)       # For tools that return structured results
```

### Tool Call with Timeout
```python
async with client:
    # Override default timeout for specific call
    result = await client.call_tool(
        "long_running_tool",
        {"param": "value"},
        timeout=30.0  # seconds
    )
```

### Tool Call with Progress Handler
```python
async def progress_handler(progress: float, total: float | None, message: str | None):
    if total:
        percentage = (progress / total) * 100
        print(f"Progress: {percentage:.1f}% - {message or ''}")

client = Client("server.py", progress_handler=progress_handler)

async with client:
    result = await client.call_tool("process_data", {"file": "large.csv"})
```

## Error Handling

```python
from fastmcp.client import ClientError, McpError

async with client:
    try:
        result = await client.call_tool("risky_tool", {"param": "value"})
    except ClientError as e:
        print(f"Tool execution failed: {e}")
    except McpError as e:
        print(f"MCP protocol error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
```

## Client Configuration Options

```python
from fastmcp import Client

client = Client(
    "server.py",
    # Handlers
    log_handler=my_log_handler,          # Handle server logs
    progress_handler=my_progress_handler, # Track long operations
    sampling_handler=my_llm_handler,     # Handle LLM requests
    
    # Roots (for file access)
    roots=["/path/to/data", "/path/to/config"],
    
    # Timeouts
    timeout=30.0,        # Default request timeout
    init_timeout=10.0    # Connection initialization timeout
)
```

## PyClarity-Specific Integration

### Correct Pattern for WorkflowEngine
```python
from fastmcp import Client

class WorkflowEngine:
    def __init__(self, server_config=None):
        self.server_config = server_config or {
            "mcpServers": {
                "pyclarity": {
                    "command": "python",
                    "args": ["-m", "pyclarity.server"],
                    "transport": "stdio"
                }
            }
        }
        self._client = None
    
    async def initialize(self):
        """Initialize the FastMCP client"""
        self._client = Client(self.server_config)
    
    async def close(self):
        """Close client connection"""
        if self._client and self._client.is_connected():
            # Client closes automatically when exiting context
            pass
    
    async def _call_mcp_tool(self, tool_name: str, input_data: Dict[str, Any]):
        """Call an MCP tool via FastMCP client"""
        if not self._client:
            raise RuntimeError("Client not initialized")
        
        async with self._client:
            # For single server config, tool names are not prefixed
            result = await self._client.call_tool(tool_name, input_data)
            return result
```

### For Testing with In-Memory Server
```python
from fastmcp import FastMCP, Client
from pyclarity.server import create_server

async def test_workflow():
    # Create the PyClarity server
    server = create_server()
    
    # Create client with in-memory transport
    client = Client(server)
    
    async with client:
        # Call cognitive tools directly
        result = await client.call_tool("sequential_thinking", {
            "problem": "Test problem",
            "complexity_level": "moderate"
        })
        
        assert "reasoning_steps" in result
```

## Common Mistakes to Avoid

1. **DON'T use `FastMCP` for client operations** - Use `Client`
2. **DON'T forget the async context** - Always use `async with client:`
3. **DON'T call tools outside the context** - The connection must be active
4. **DON'T use prefixes for single-server configs** - Only multi-server needs prefixes
5. **DON'T forget to handle exceptions** - Use try/except for robust error handling

## Session Management

### Default Behavior (keep_alive=True)
```python
client = Client("server.py")  # keep_alive=True by default

async def multiple_operations():
    # First operation
    async with client:
        await client.ping()
    
    # Second operation - reuses same subprocess
    async with client:
        await client.call_tool("tool", {})
```

### Isolated Sessions
```python
from fastmcp.client.transports import StdioTransport

transport = StdioTransport(
    command="python",
    args=["server.py"],
    keep_alive=False  # New process for each session
)
client = Client(transport)
```

## References

- FastMCP Documentation: https://gofastmcp.com
- MCP Protocol: https://github.com/modelcontextprotocol
- PyClarity Server: src/pyclarity/server/mcp_server.py