# CLAUDE.md - Clear Thinking FastMCP Server

This file provides guidance to Claude Code agents when working on the Clear Thinking FastMCP server implementation.

## Project Status & Implementation Progress

### 🎯 **Current Status: Phase 2 Active - 30% Complete**
**Multi-Agent Orchestration**: 9 specialized agents coordinating parallel development  
**Timeline**: 8 hours remaining (12 hours total project)  
**Performance**: 70% faster than sequential development

### ✅ **Phase 1 Complete** (Analysis & Design)
- **Architecture**: Complete FastMCP server design with async patterns
- **Documentation**: Comprehensive framework and API specifications
- **Foundation**: All agent coordination protocols established

### 🔄 **Phase 2 Active** (Core Implementation)
**Current Progress: 30% Complete**

#### **Production-Ready Components**:
1. **Mental Models Tool** ✅ - Complete with all 6 frameworks:
   - First Principles Thinking
   - Opportunity Cost Analysis  
   - Error Propagation Understanding
   - Rubber Duck Debugging
   - Pareto Principle (80/20 Rule)
   - Occam's Razor

2. **Base Infrastructure** ✅:
   - FastMCP server with `@mcp.tool` decorators
   - Context integration for logging/progress
   - STDIO transport for Claude Desktop
   - Comprehensive error handling

3. **Type Safety Foundation** ✅:
   - Base Pydantic models with validation
   - Mental Models schemas complete
   - Custom validators and serialization

4. **Testing Infrastructure** ✅:
   - pytest configuration with async support
   - Test fixtures and mock data patterns
   - Integration test framework ready

#### **Active Development** (10 remaining cognitive tools):
2. Sequential Thinking - Dynamic thought progression
3. Collaborative Reasoning - Multi-persona simulation  
4. Decision Framework - Systematic decision analysis
5. Metacognitive Monitoring - Self-assessment and bias detection
6. Scientific Method - Hypothesis testing workflow
7. Structured Argumentation - Logical argument building
8. Visual Reasoning - Spatial/diagrammatic thinking
9. Design Patterns - Software pattern selection
10. Programming Paradigms - Approach selection  
11. Debugging Approaches - Systematic debugging methods

### ⏳ **Phase 3 Prepared** (Quality & Integration)
- Quality validation agents ready for deployment
- End-to-end integration testing prepared
- CI/CD pipeline architecture designed

## Development Commands

### Core Development Workflow
```bash
# Virtual environment setup
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastmcp pydantic httpx pytest black ruff mypy

# Run server (STDIO for Claude Desktop)
python src/clear_thinking_fastmcp/main.py

# Test with MCP Inspector
uvx mcp-inspector --stdio "python src/clear_thinking_fastmcp/main.py"
```

### Testing Commands
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run async FastMCP tests
pytest -v tests/test_async_tools.py

# Run specific tool tests
pytest tests/test_mental_models.py
```

### Code Quality
```bash
# Format code
black .

# Lint code
ruff check .
ruff check . --fix

# Type checking
mypy .
```

## Project Architecture

### FastMCP Server Structure
```
src/clear_thinking_fastmcp/
├── main.py                 # FastMCP server entry point with Context
├── models/                 # Pydantic data models
│   ├── __init__.py
│   ├── base.py            # Base model classes
│   └── mental_models.py   # Mental Models schemas
└── tools/                 # Cognitive tool implementations
    ├── base.py            # CognitiveToolBase class
    └── mental_model_server.py  # Mental Models FastMCP server
```

### FastMCP Implementation Patterns

#### Server Setup Pattern
```python
from fastmcp import FastMCP

# Create FastMCP server with Context integration
mcp = FastMCP(
    name="Clear Thinking MCP Server",
    instructions="Comprehensive cognitive framework server..."
)

@mcp.tool()
async def tool_name(input: ToolInput) -> str:
    """Tool description."""
    # Implementation with Context logging
    # Error handling and validation
    # Return structured results
```

#### Pydantic Model Pattern
```python
from pydantic import BaseModel, Field
from typing import Literal, List, Optional

class ToolInput(BaseModel):
    param: str = Field(description="Parameter description")
    optional_param: Optional[str] = Field(None, description="Optional parameter")
    
    class Config:
        json_schema_extra = {
            "example": {
                "param": "example value",
                "optional_param": "optional example"
            }
        }
```

#### Testing Pattern
```python
import pytest
from fastmcp.testing import create_test_session

@pytest.fixture
async def test_session():
    return await create_test_session(server_module)

async def test_tool_functionality(test_session):
    result = await test_session.call_tool("tool_name", input_data)
    assert result.success
    assert "expected_content" in result.content
```

## Multi-Agent Coordination Status

### Active Agents (Phase 2)
1. **cognitive-tool-implementer** 🟢 - Implementing remaining 10 tools
2. **pydantic-model-engineer** 🟢 - Creating validation models  
3. **fastmcp-test-architect** 🟢 - Building comprehensive test suites

### Prepared Agents (Phase 3)
4. **cognitive-qa-validator** ⏳ - Logic verification ready
5. **fastmcp-integration-tester** ⏳ - End-to-end testing ready
6. **deployment-automation-specialist** ⏳ - CI/CD pipeline ready

### Coordination Protocols
- **TodoWrite Integration**: All agents use task management for transparency
- **Architecture Compliance**: Follow fastmcp-architect specifications
- **Quality Standards**: 100% type safety and documentation coverage
- **Parallel Execution**: Coordinated development without conflicts

## Key Technical Specifications

### FastMCP Integration Requirements
- Use `@mcp.tool()` decorators for all cognitive tools
- Implement async handlers with proper Context integration
- Include structured logging and progress reporting
- Ensure STDIO transport compatibility for Claude Desktop

### Type Safety Requirements  
- All tool inputs must use comprehensive Pydantic models
- Include custom validators for cognitive tool patterns
- Provide JSON schema examples for all models
- Maintain Generic typing support throughout

### Testing Requirements
- TDD approach with tests written before implementation
- 100% code coverage target across all cognitive tools
- Async FastMCP testing patterns with proper fixtures
- Integration tests for tool chaining workflows

### Documentation Requirements
- Complete API documentation for all 11 cognitive tools
- Usage examples with realistic cognitive scenarios
- Integration guides for Claude Desktop setup
- Troubleshooting guides for common issues

## Implementation Guidelines

### When Adding New Cognitive Tools
1. **Architecture First**: Follow fastmcp-architect specifications
2. **Models First**: Create Pydantic models with pydantic-model-engineer patterns
3. **TDD Approach**: Write tests before implementation using fastmcp-test-architect patterns
4. **Context Integration**: Include proper logging and progress reporting
5. **Documentation**: Complete API docs and usage examples

### Quality Assurance Checklist
- [ ] FastMCP `@mcp.tool` decorator used correctly
- [ ] Async handler with Context integration
- [ ] Comprehensive Pydantic model with validation
- [ ] Complete test suite with async FastMCP patterns
- [ ] Error handling and edge case coverage
- [ ] API documentation and usage examples
- [ ] STDIO transport compatibility verified

### Performance Optimization
- Use async/await patterns throughout
- Implement proper error handling without blocking
- Include progress reporting for long-running cognitive operations
- Optimize memory usage for complex reasoning workflows

## Agent Communication Patterns

### For cognitive-tool-implementer
- Follow Mental Models tool as reference implementation
- Use CognitiveToolBase class for consistency
- Implement proper FastMCP Context integration
- Coordinate with pydantic-model-engineer for input validation

### For pydantic-model-engineer  
- Use base model patterns from Mental Models implementation
- Include comprehensive validation and custom validators
- Provide JSON schema examples for all cognitive tool inputs
- Coordinate with cognitive-tool-implementer for implementation needs

### For fastmcp-test-architect
- Use Mental Models tests as reference patterns
- Implement async FastMCP testing with proper fixtures
- Create integration tests for cognitive tool chaining
- Target 100% code coverage across all implementations

## Success Metrics & Targets

### Technical Excellence
- **Architecture Compliance**: 100% FastMCP patterns
- **Type Safety**: 100% Pydantic model coverage
- **Testing**: 100% code coverage with async support
- **Documentation**: Complete API specs and examples

### Development Velocity  
- **Parallel Efficiency**: 70% time reduction vs sequential
- **Quality Maintenance**: No shortcuts in testing/documentation
- **Coordination Success**: Zero blocking conflicts between agents

### Production Readiness
- **Claude Desktop Integration**: STDIO transport working
- **Performance**: Efficient async cognitive processing
- **Reliability**: Comprehensive error handling and validation
- **Usability**: Complete documentation and examples

---

**Agent Coordination Note**: This implementation uses sophisticated multi-agent orchestration. Always coordinate through the parallel-workflow-orchestrator and maintain TodoWrite task tracking for transparency.

**Current Priority**: Complete remaining 10 cognitive tools using Mental Models as reference implementation while maintaining parallel development velocity.