# Clear Thinking FastMCP Server - Architecture Design

**Agent**: fastmcp-architect  
**Status**: ANALYSIS COMPLETE - ARCHITECTURE DESIGNED  
**Date**: 2025-07-29

## Executive Summary

This document presents the comprehensive architecture design for rebuilding the Clear Thought MCP Server using Python FastMCP framework. The design maintains full compatibility with the original 11 cognitive tools while leveraging FastMCP's modern async patterns, Context objects, and enhanced developer experience.

## Original Architecture Analysis

### TypeScript Original Server Structure
- **Core**: `@modelcontextprotocol/sdk` with `StdioServerTransport`
- **Tools**: 11 dedicated server classes (MentalModelServer, DesignPatternServer, etc.)
- **Protocol**: JSON-RPC over stdio with structured request/response handling
- **Validation**: Zod runtime validation with TypeScript interfaces
- **Output**: Structured JSON responses with chalk-styled console output

### Key Findings
1. Each cognitive tool has dedicated server class with process method
2. Input validation occurs at multiple layers (JSON Schema + TypeScript + Zod)
3. Request dispatching based on tool name to appropriate server instance
4. Consistent response structure: `{content: [{type: "text", text: JSON.stringify(result)}]}`

## FastMCP Architecture Design

### Core Server Architecture

```python
# main.py - Primary server implementation
from fastmcp import FastMCP
from fastmcp.server import Context
from pydantic import BaseModel
import asyncio
from typing import Dict, Any

# Initialize FastMCP server
mcp = FastMCP(
    name="ClearThinkingServer",
    version="2.0.0",
    description="Advanced cognitive reasoning tools via FastMCP"
)

class CognitiveToolBase:
    """Base class for all cognitive tools"""
    
    async def validate_input(self, data: Dict[str, Any]) -> BaseModel:
        """Validate input using Pydantic models"""
        pass
    
    async def process(self, validated_data: BaseModel, ctx: Context) -> Dict[str, Any]:
        """Process the cognitive tool logic"""
        pass

# Tool registration pattern
@mcp.tool
async def mental_model_tool(
    model_data: MentalModelInput, 
    ctx: Context
) -> MentalModelOutput:
    """Apply structured mental models to problem-solving"""
    ctx.info(f"Processing mental model: {model_data.model_type}")
    
    server = MentalModelServer()
    result = await server.process(model_data, ctx)
    
    ctx.progress(1.0, 1.0, "Mental model analysis complete")
    return result

if __name__ == "__main__":
    mcp.run(transport="stdio")  # Compatible with Claude Desktop
```

### Cognitive Tool Server Classes

Each cognitive tool will be implemented as an async class following this pattern:

```python
# src/tools/mental_model_server.py
from fastmcp.server import Context
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Literal
import asyncio

class MentalModelInput(BaseModel):
    """Input schema for mental model tool"""
    problem: str = Field(..., description="The problem to analyze")
    model_type: Literal[
        "first_principles", 
        "opportunity_cost", 
        "error_propagation",
        "rubber_duck",
        "pareto_principle", 
        "occams_razor"
    ] = Field(..., description="Mental model to apply")
    context: str = Field("", description="Additional context")

class MentalModelOutput(BaseModel):
    """Output schema for mental model tool"""
    analysis: str
    key_insights: List[str]
    recommendations: List[str]
    model_applied: str
    confidence_score: float = Field(ge=0.0, le=1.0)

class MentalModelServer:
    """Mental model cognitive tool server"""
    
    async def process(
        self, 
        data: MentalModelInput, 
        ctx: Context
    ) -> MentalModelOutput:
        """Process mental model analysis"""
        
        ctx.info(f"Applying {data.model_type} to problem analysis")
        
        # Model-specific processing logic
        if data.model_type == "first_principles":
            result = await self._apply_first_principles(data, ctx)
        elif data.model_type == "opportunity_cost":
            result = await self._apply_opportunity_cost(data, ctx)
        # ... additional model types
        
        ctx.info("Mental model analysis completed")
        return result
    
    async def _apply_first_principles(
        self, 
        data: MentalModelInput, 
        ctx: Context
    ) -> MentalModelOutput:
        """Apply first principles thinking"""
        ctx.progress(0.3, 1.0, "Breaking down to fundamental truths")
        
        # Implementation logic here
        analysis = f"First principles analysis of: {data.problem}"
        insights = ["Fundamental truth 1", "Fundamental truth 2"]
        recommendations = ["Build from basics", "Question assumptions"]
        
        ctx.progress(1.0, 1.0, "First principles analysis complete")
        
        return MentalModelOutput(
            analysis=analysis,
            key_insights=insights,
            recommendations=recommendations,
            model_applied="first_principles",
            confidence_score=0.85
        )
```

### All 11 Cognitive Tools Architecture

| Tool | FastMCP Handler | Server Class | Input Model | Output Model |
|------|----------------|--------------|-------------|--------------|
| Mental Models | `@mcp.tool async def mental_model_tool` | `MentalModelServer` | `MentalModelInput` | `MentalModelOutput` |
| Sequential Thinking | `@mcp.tool async def sequential_thinking_tool` | `SequentialThinkingServer` | `SequentialThinkingInput` | `SequentialThinkingOutput` |
| Collaborative Reasoning | `@mcp.tool async def collaborative_reasoning_tool` | `CollaborativeReasoningServer` | `CollaborativeReasoningInput` | `CollaborativeReasoningOutput` |
| Decision Framework | `@mcp.tool async def decision_framework_tool` | `DecisionFrameworkServer` | `DecisionFrameworkInput` | `DecisionFrameworkOutput` |
| Metacognitive Monitoring | `@mcp.tool async def metacognitive_monitoring_tool` | `MetacognitiveMonitoringServer` | `MetacognitiveMonitoringInput` | `MetacognitiveMonitoringOutput` |
| Scientific Method | `@mcp.tool async def scientific_method_tool` | `ScientificMethodServer` | `ScientificMethodInput` | `ScientificMethodOutput` |
| Structured Argumentation | `@mcp.tool async def structured_argumentation_tool` | `StructuredArgumentationServer` | `StructuredArgumentationInput` | `StructuredArgumentationOutput` |
| Visual Reasoning | `@mcp.tool async def visual_reasoning_tool` | `VisualReasoningServer` | `VisualReasoningInput` | `VisualReasoningOutput` |
| Design Patterns | `@mcp.tool async def design_patterns_tool` | `DesignPatternsServer` | `DesignPatternsInput` | `DesignPatternsOutput` |
| Programming Paradigms | `@mcp.tool async def programming_paradigms_tool` | `ProgrammingParadigmsServer` | `ProgrammingParadigmsInput` | `ProgrammingParadigmsOutput` |
| Debugging Approaches | `@mcp.tool async def debugging_approaches_tool` | `DebuggingApproachesServer` | `DebuggingApproachesInput` | `DebuggingApproachesOutput` |

### Directory Structure

```
clear-thinking-fastmcp/
├── src/
│   ├── clear_thinking_fastmcp/
│   │   ├── __init__.py
│   │   ├── main.py                 # Main FastMCP server
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── base.py            # Base Pydantic models
│   │   │   ├── mental_models.py   # Mental model schemas
│   │   │   ├── sequential_thinking.py
│   │   │   ├── collaborative_reasoning.py
│   │   │   ├── decision_framework.py
│   │   │   ├── metacognitive_monitoring.py
│   │   │   ├── scientific_method.py
│   │   │   ├── structured_argumentation.py
│   │   │   ├── visual_reasoning.py
│   │   │   ├── design_patterns.py
│   │   │   ├── programming_paradigms.py
│   │   │   └── debugging_approaches.py
│   │   ├── tools/
│   │   │   ├── __init__.py
│   │   │   ├── base.py            # Base tool server class
│   │   │   ├── mental_model_server.py
│   │   │   ├── sequential_thinking_server.py
│   │   │   ├── collaborative_reasoning_server.py
│   │   │   ├── decision_framework_server.py
│   │   │   ├── metacognitive_monitoring_server.py
│   │   │   ├── scientific_method_server.py
│   │   │   ├── structured_argumentation_server.py
│   │   │   ├── visual_reasoning_server.py
│   │   │   ├── design_patterns_server.py
│   │   │   ├── programming_paradigms_server.py
│   │   │   └── debugging_approaches_server.py
│   │   ├── middleware/
│   │   │   ├── __init__.py
│   │   │   ├── logging.py         # Enhanced logging middleware
│   │   │   ├── validation.py      # Input validation middleware
│   │   │   └── error_handling.py  # Error handling middleware
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── validation.py      # Validation utilities
│   │       └── formatting.py      # Output formatting utilities
├── tests/
│   ├── __init__.py
│   ├── conftest.py               # pytest fixtures
│   ├── test_main.py             # Main server tests
│   ├── test_models/             # Pydantic model tests
│   ├── test_tools/              # Tool server tests
│   └── integration/             # Integration tests
├── docs/
│   ├── README.md
│   ├── API.md                   # API documentation
│   ├── DEVELOPMENT.md           # Development guide
│   └── DEPLOYMENT.md           # Deployment guide
├── pyproject.toml              # Project configuration
└── README.md
```

### Context Integration Pattern

```python
from fastmcp.server import Context

async def process_cognitive_tool(data: InputModel, ctx: Context) -> OutputModel:
    """Standard pattern for cognitive tool processing"""
    
    # Logging
    ctx.info(f"Starting {tool_name} processing")
    ctx.debug(f"Input data: {data}")
    
    # Progress reporting for long-running operations
    ctx.progress(0.0, 1.0, "Initializing analysis")
    
    # Processing steps with progress updates
    ctx.progress(0.3, 1.0, "Analyzing input")
    result = await perform_analysis(data)
    
    ctx.progress(0.6, 1.0, "Generating insights")
    insights = await generate_insights(result)
    
    ctx.progress(0.9, 1.0, "Formatting output")
    output = format_output(result, insights)
    
    ctx.progress(1.0, 1.0, "Processing complete")
    ctx.info(f"{tool_name} processing completed successfully")
    
    return output
```

### Transport Configuration

```python
# Development configuration (STDIO)
if __name__ == "__main__":
    mcp.run(transport="stdio")  # Compatible with Claude Desktop

# Production configuration (HTTP)
if __name__ == "__main__":
    mcp.run(
        transport="http", 
        host="0.0.0.0", 
        port=8000,
        middleware=[
            AuthenticationMiddleware(),
            LoggingMiddleware(),
            ValidationMiddleware()
        ]
    )
```

## Integration Framework

### Client-Server Integration

```python
# Integration testing pattern
from fastmcp import Client
import asyncio

async def test_integration():
    """Test client-server integration"""
    
    client = Client("src/clear_thinking_fastmcp/main.py")
    
    async with client:
        # Test connection
        await client.ping()
        
        # List available tools
        tools = await client.list_tools()
        assert len(tools) == 11
        
        # Test cognitive tool
        result = await client.call_tool(
            "mental_model_tool",
            {
                "problem": "How to optimize database queries?",
                "model_type": "first_principles",
                "context": "High-traffic web application"
            }
        )
        
        assert result.model_applied == "first_principles"
        assert result.confidence_score > 0.0

if __name__ == "__main__":
    asyncio.run(test_integration())
```

### Middleware Architecture

```python
# src/middleware/logging.py
from fastmcp.server.middleware import Middleware, MiddlewareContext
import structlog

class CognitiveLoggingMiddleware(Middleware):
    """Enhanced logging for cognitive tools"""
    
    def __init__(self):
        self.logger = structlog.get_logger()
    
    async def on_request(self, context: MiddlewareContext, call_next):
        """Log cognitive tool requests"""
        
        self.logger.info(
            "cognitive_tool_request",
            tool=context.method,
            timestamp=context.timestamp
        )
        
        try:
            result = await call_next(context)
            
            self.logger.info(
                "cognitive_tool_success",
                tool=context.method,
                duration=context.duration
            )
            
            return result
            
        except Exception as e:
            self.logger.error(
                "cognitive_tool_error",
                tool=context.method,
                error=str(e)
            )
            raise
```

## Deployment Strategy

### Development Environment
```python
# dev_server.py
from fastmcp import FastMCP
from src.clear_thinking_fastmcp.main import mcp

if __name__ == "__main__":
    # Development with hot reload
    mcp.run(
        transport="stdio",
        debug=True,
        reload=True
    )
```

### Production Environment
```python
# production_server.py
from fastmcp import FastMCP
from src.clear_thinking_fastmcp.main import mcp
from src.middleware import CognitiveLoggingMiddleware, ValidationMiddleware

if __name__ == "__main__":
    # Production configuration
    mcp.add_middleware(CognitiveLoggingMiddleware())
    mcp.add_middleware(ValidationMiddleware())
    
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=8000,
        workers=4
    )
```

## API Specifications

### Standard Request/Response Pattern

All cognitive tools follow this API pattern:

```json
// Request
{
  "method": "tools/call",
  "params": {
    "name": "mental_model_tool",
    "arguments": {
      "problem": "How to scale microservices architecture?",
      "model_type": "first_principles",
      "context": "E-commerce platform with 1M+ users"
    }
  }
}

// Response
{
  "content": [
    {
      "type": "text",
      "text": {
        "analysis": "First principles analysis of microservices scaling...",
        "key_insights": [
          "Service boundaries must align with business domains",
          "Data consistency patterns determine scaling approach"
        ],
        "recommendations": [
          "Implement event-driven architecture",
          "Use distributed caching strategies"
        ],
        "model_applied": "first_principles",
        "confidence_score": 0.87
      }
    }
  ]
}
```

## Success Metrics

1. **Functionality**: All 11 cognitive tools implemented with equivalent functionality
2. **Performance**: Response times under 500ms for typical requests
3. **Reliability**: 99.9% uptime with comprehensive error handling
4. **Developer Experience**: Clear APIs, comprehensive documentation, easy testing
5. **Compatibility**: Full MCP protocol compliance for Claude Desktop integration

## Next Phase Handoffs

### To Phase 2 Teams:

1. **cognitive-tool-implementer**: Complete architecture specifications and tool patterns
2. **pydantic-model-engineer**: Detailed schema requirements for all 11 tools
3. **fastmcp-test-architect**: Testing patterns and integration specifications

### To Phase 3 Teams:

1. **cognitive-qa-validator**: Logic verification requirements and test cases
2. **fastmcp-integration-tester**: End-to-end testing specifications
3. **deployment-automation-specialist**: Production deployment architecture

---

**Architecture Status**: COMPLETE ✅  
**Ready for Phase 2**: YES ✅  
**Next Agent**: cognitive-tool-implementer, pydantic-model-engineer, fastmcp-test-architect