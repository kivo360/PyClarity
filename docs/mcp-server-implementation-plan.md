# MCP Server Implementation Plan

## Overview

Implement a local MCP (Model Context Protocol) server with authentication to provide secure access to PyClarity's cognitive tools.

## Architecture

### Components

1. **MCP Server Core** (`src/pyclarity/server/mcp_server.py`)
   - FastMCP-based server implementation
   - Tool registration and management
   - Request/response handling

2. **Authentication Layer** (`src/pyclarity/auth/`)
   - JWT token-based authentication
   - API key management
   - Role-based access control

3. **Tool Registry** (`src/pyclarity/tools/`)
   - Cognitive tools registration
   - Tool discovery and metadata
   - Tool execution with authentication

4. **Client Interface** (`src/pyclarity/client/`)
   - MCP client implementation
   - Authentication client
   - Tool invocation interface

## Implementation Steps

### Phase 1: Core MCP Server Setup

1. **Basic MCP Server Structure**
   ```python
   # src/pyclarity/server/mcp_server.py
   from fastmcp import FastMCP
   from pyclarity.auth import AuthMiddleware
   from pyclarity.tools import ToolRegistry
   
   class PyClarityMCPServer:
       def __init__(self):
           self.fastmcp = FastMCP()
           self.auth = AuthMiddleware()
           self.tools = ToolRegistry()
   ```

2. **Authentication Middleware**
   ```python
   # src/pyclarity/auth/middleware.py
   import jwt
   from fastapi import HTTPException, Depends
   
   class AuthMiddleware:
       def __init__(self, secret_key: str):
           self.secret_key = secret_key
       
       def verify_token(self, token: str) -> dict:
           # JWT verification logic
           pass
   ```

3. **Tool Registry**
   ```python
   # src/pyclarity/tools/registry.py
   from typing import Dict, Any
   
   class ToolRegistry:
       def __init__(self):
           self.tools: Dict[str, Any] = {}
       
       def register_tool(self, name: str, tool: Any):
           self.tools[name] = tool
   ```

### Phase 2: Authentication Implementation

1. **JWT Token Management**
   - Token generation and validation
   - Refresh token support
   - Token expiration handling

2. **API Key Authentication**
   - API key validation
   - Rate limiting
   - Usage tracking

3. **Role-Based Access Control**
   - User roles (admin, user, read-only)
   - Tool access permissions
   - Resource limits

### Phase 3: Tool Integration

1. **Cognitive Tools Registration**
   ```python
   # Register existing tools
   registry.register_tool("progressive_thinking", ProgressiveSequentialThinkingAnalyzer)
   registry.register_tool("decision_framework", DecisionFrameworkAnalyzer)
   registry.register_tool("mental_models", MentalModelsAnalyzer)
   ```

2. **Tool Execution with Auth**
   ```python
   @app.post("/tools/{tool_name}/execute")
   async def execute_tool(
       tool_name: str,
       request: ToolRequest,
       user: User = Depends(get_current_user)
   ):
       # Check permissions
       # Execute tool
       # Return results
   ```

### Phase 4: Client Implementation

1. **MCP Client**
   ```python
   # src/pyclarity/client/mcp_client.py
   class PyClarityMCPClient:
       def __init__(self, server_url: str, api_key: str):
           self.server_url = server_url
           self.api_key = api_key
       
       async def execute_tool(self, tool_name: str, **kwargs):
           # Make authenticated request
           pass
   ```

2. **CLI Interface**
   ```python
   # src/pyclarity/cli/mcp_cli.py
   @app.command()
   def mcp_server():
       """Start the MCP server"""
       pass
   
   @app.command()
   def mcp_client():
       """Connect to MCP server"""
       pass
   ```

## Security Considerations

### Authentication
- JWT tokens with short expiration
- API key rotation
- Secure token storage
- HTTPS enforcement

### Authorization
- Tool-level permissions
- Resource usage limits
- Rate limiting per user
- Audit logging

### Data Protection
- Input validation
- Output sanitization
- Secure error handling
- No sensitive data in logs

## Configuration

### Environment Variables
```bash
# MCP Server Configuration
MCP_SERVER_HOST=localhost
MCP_SERVER_PORT=8000
MCP_SECRET_KEY=your-secret-key
MCP_JWT_EXPIRY=3600

# Authentication
MCP_AUTH_ENABLED=true
MCP_API_KEY_ROTATION_DAYS=30
MCP_RATE_LIMIT_REQUESTS=100
MCP_RATE_LIMIT_WINDOW=3600

# Database
MCP_DATABASE_URL=postgresql://pyclarity:pyclarity@postgres:5432/pyclarity
```

### Configuration File
```yaml
# mcp_config.yaml
server:
  host: localhost
  port: 8000
  debug: false

auth:
  enabled: true
  jwt_secret: your-secret-key
  jwt_expiry: 3600
  api_key_rotation_days: 30

tools:
  progressive_thinking:
    enabled: true
    rate_limit: 10
    requires_auth: true
  decision_framework:
    enabled: true
    rate_limit: 5
    requires_auth: true
  mental_models:
    enabled: true
    rate_limit: 15
    requires_auth: false
```

## Usage Examples

### Starting the Server
```bash
# Start MCP server
pyclarity mcp-server start

# Start with custom config
pyclarity mcp-server start --config mcp_config.yaml
```

### Client Usage
```python
from pyclarity.client import PyClarityMCPClient

# Connect to server
client = PyClarityMCPClient(
    server_url="http://localhost:8000",
    api_key="your-api-key"
)

# Execute tool
result = await client.execute_tool(
    "progressive_thinking",
    thought="Let me analyze this problem step by step"
)
```

### CLI Usage
```bash
# Execute tool via CLI
pyclarity mcp-client execute progressive_thinking \
  --thought "Let me analyze this problem step by step"

# List available tools
pyclarity mcp-client list-tools

# Get tool info
pyclarity mcp-client tool-info progressive_thinking
```

## Testing Strategy

### Unit Tests
- Authentication middleware tests
- Tool registry tests
- Client connection tests
- Permission validation tests

### Integration Tests
- End-to-end MCP server tests
- Authentication flow tests
- Tool execution tests
- Rate limiting tests

### Security Tests
- Token validation tests
- Permission bypass attempts
- Rate limit enforcement
- Input validation tests

## Deployment

### Docker Configuration
```dockerfile
# Add to existing Dockerfile
RUN pip install fastapi uvicorn python-jose[cryptography] passlib[bcrypt]
```

### Docker Compose
```yaml
# Add to docker-compose.yml
mcp-server:
  build: .
  ports:
    - "8000:8000"
  environment:
    - MCP_SERVER_HOST=0.0.0.0
    - MCP_SERVER_PORT=8000
  depends_on:
    - postgres
```

## Monitoring and Logging

### Metrics
- Request count per tool
- Authentication success/failure rates
- Response times
- Error rates

### Logging
- Authentication events
- Tool execution logs
- Error tracking
- Performance metrics

## Next Steps

1. **Implement Core MCP Server** (Week 1)
   - Basic FastMCP integration
   - Tool registration system
   - Simple request/response handling

2. **Add Authentication** (Week 2)
   - JWT token implementation
   - API key management
   - Basic RBAC

3. **Integrate Existing Tools** (Week 3)
   - Register cognitive tools
   - Add permission controls
   - Implement rate limiting

4. **Client Implementation** (Week 4)
   - MCP client library
   - CLI interface
   - Documentation

5. **Testing and Security** (Week 5)
   - Comprehensive testing
   - Security audit
   - Performance optimization

This implementation will provide a secure, scalable MCP server that can be used both locally and in production environments. 