# Technical Stack

> Last Updated: 2025-08-04
> Version: 1.0.0

## Core Technologies

- **Application Framework:** FastMCP v2.10.6+ (MCP server framework)
- **Programming Language:** Python 3.12+
- **Package Manager:** UV (modern Python packaging with lock files)
- **Build Backend:** Hatchling with dynamic versioning

## Data Processing & Validation

- **Data Validation:** Pydantic v2.11.7+ (strict mode enabled)
- **Scientific Computing:** NumPy v2.3.2+
- **Graph Algorithms:** NetworkX v3.0+
- **JSON Processing:** orjson v3.9.0+ (optional performance enhancement)

## Development Tools

- **CLI Framework:** Typer v0.15.1+ with Rich v13.0.0+
- **Testing Framework:** pytest v8.3.4+ with pytest-asyncio
- **Type Checking:** mypy (strict mode)
- **Linting:** Ruff v0.9.2+ (96 rules enabled)
- **Version Control:** Git with Conventional Commits
- **Task Runner:** Poe the Poet v0.32.1+

## AI/ML Integration

- **LLM Libraries:** 
  - anthropic v0.60.0+
  - groq v0.30.0+
  - distilabel[hf-inference-endpoints,litellm] v1.5.3+
- **Chunking:** chonkie[all] v1.1.1+
- **Reward Modeling:** reward-kit[trl] v0.4.1+

## Infrastructure

- **Container Platform:** Docker with Dev Containers
- **Development Environment:** VS Code / PyCharm with Dev Container support
- **Python Environment:** Virtual environments via UV
- **Async Support:** asyncio with optional uvloop v0.19.0+

## Testing & Quality

- **Test Coverage:** 50% minimum (targeting 80%+)
- **Integration Testing:** pytest-xdist for parallel execution
- **Performance Testing:** pytest-testmon for test impact analysis
- **Pre-commit Hooks:** pre-commit v4.0.1+

## Documentation

- **API Documentation:** pdoc v15.0.1+
- **Docstring Format:** NumPy style
- **Changelog:** Automated with Commitizen v4.3.0+

## Deployment

- **Package Distribution:** PyPI via GitHub Actions
- **Containerization:** Multi-stage Docker builds
- **Installation Methods:** pip, uv, or containerized
- **MCP Integration:** FastMCP server with stdio transport

## Optional Enhancements

- **Visualization:** matplotlib v3.8.0+, plotly v5.18.0+, graphviz v0.20.0+
- **Performance:** uvloop for faster async, orjson for faster JSON

## Standards & Conventions

- **Code Style:** 100 character line length, 2-space indentation
- **Import Style:** Absolute imports with pyclarity.* namespace
- **Commit Format:** Conventional Commits for automated versioning
- **File Encoding:** UTF-8 with LF line endings

## Repository Structure

```
src/pyclarity/          # Main package
├── server/            # FastMCP server implementation
├── tools/             # 17 cognitive analyzers
└── cli.py            # CLI interface

experiment/            # Experimental code (isolated)
tests/                # Comprehensive test suite
.agent-os/            # Agent OS documentation
```

## Integration Points

- **MCP Clients:** Compatible with any MCP-compliant client
- **LLM Providers:** Anthropic, Groq, OpenAI (via LiteLLM)
- **Data Sources:** File system, APIs, user input
- **Export Formats:** JSON, Pydantic models, structured text