# PyClarity MCP Server Setup

PyClarity can be run as an MCP (Model Context Protocol) server, allowing integration with Claude Desktop and other MCP-compatible clients. This provides direct access to all cognitive tools through natural language interactions.

## Quick Start

### 1. Start the MCP Server

```bash
# Start server on default port (8000)
pyclarity server

# Start on custom port with debug mode
pyclarity server --port 8080 --debug

# Start on specific host/port
pyclarity server --host 0.0.0.0 --port 8000
```

### 2. Claude Desktop Integration

To use PyClarity with Claude Desktop, add the following to your Claude Desktop MCP configuration:

**Location**: `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)

```json
{
  "mcpServers": {
    "pyclarity": {
      "command": "uv",
      "args": [
        "run", 
        "pyclarity",
        "server"
      ],
      "cwd": "/path/to/your/PyClarity",
      "env": {
        "PYTHONPATH": "/path/to/your/PyClarity/src"
      }
    }
  }
}
```

**Replace `/path/to/your/PyClarity`** with the actual path to your PyClarity installation.

### 3. Verify Connection

After restarting Claude Desktop, you should see the PyClarity tools available. You can test with:

```
"Use the mental models tool to analyze this problem using first principles thinking: How should we architect a scalable web application?"
```

## Available Tools

PyClarity provides 12 cognitive analysis tools through MCP:

### 🧠 Mental Models Analysis
Apply structured thinking frameworks:
- **First Principles**: Break down to fundamental truths
- **Opportunity Cost**: Analyze trade-offs and alternatives  
- **Error Propagation**: Understand how errors compound
- **Rubber Duck**: Step-by-step explanation methodology
- **Pareto Principle**: Focus on highest-impact factors
- **Occam's Razor**: Find simplest viable solutions

### 🔄 Sequential Thinking
Step-by-step logical reasoning with branching and revision capabilities.

### ⚖️ Decision Framework  
Systematic decision-making using multi-criteria analysis and stakeholder weighting.

### 🔬 Scientific Method
Hypothesis-driven problem solving with evidence gathering and validation.

### 🏗️ Design Patterns
Architectural pattern analysis and recommendation for software design problems.

### 💻 Programming Paradigms
Analysis of programming paradigm selection and application strategies.

### 🐛 Debugging Approaches
Systematic debugging methodology and troubleshooting approach selection.

### 👁️ Visual Reasoning
Visual problem representation and spatial reasoning analysis.

### 💬 Structured Argumentation
Logical argumentation structure analysis and fallacy detection.

### 🎯 Metacognitive Monitoring
Self-awareness and reasoning quality monitoring during problem-solving.

### 🤝 Collaborative Reasoning
Multi-perspective collaborative problem-solving and consensus building.

### 🌊 Impact Propagation
Analysis of cascading effects and system-wide impact assessment.

## Usage Examples

### Mental Models Analysis
```
"Analyze the decision to migrate from microservices back to a monolith using opportunity cost analysis"
```

### Sequential Thinking
```
"Walk me through the reasoning for choosing between React and Vue for our new project, with branching to explore different scenarios"
```

### Decision Framework
```
"Help me make a systematic decision about cloud providers, considering cost, performance, and vendor lock-in with appropriate weightings"
```

### Scientific Method
```
"Apply scientific method to investigate why our API response times increased by 200ms after the latest deployment"
```

## Configuration Options

### Server Configuration
```bash
# Environment variables
export PYCLARITY_HOST=localhost
export PYCLARITY_PORT=8000
export PYCLARITY_DEBUG=false

# Command line options
pyclarity server \
  --host localhost \
  --port 8000 \
  --debug
```

### Tool Parameters

Each tool accepts various parameters for customization:

#### Mental Models
- `model_type`: first_principles, opportunity_cost, error_propagation, rubber_duck, pareto_principle, occams_razor
- `complexity_level`: simple, moderate, complex
- `focus_areas`: List of specific areas to focus on
- `constraints`: Known limitations or constraints
- `domain_expertise`: Relevant domain expertise level

#### Sequential Thinking
- `reasoning_depth`: Number of reasoning steps (1-10)
- `enable_branching`: Allow exploration of alternative paths
- `enable_revision`: Enable revision of earlier steps
- `branch_strategy`: linear, adaptive, exhaustive

#### Decision Framework
- `criteria`: Decision criteria with weights and types
- `options`: Available options with scores
- `decision_methods`: weighted_sum, ahp, consensus
- `stakeholder_weights`: Importance by stakeholder group

## Troubleshooting

### Connection Issues
1. **Server not starting**: Check that all dependencies are installed with `uv sync`
2. **Claude Desktop not connecting**: Verify the path in `claude_desktop_config.json` is correct
3. **Tools not appearing**: Restart Claude Desktop after configuration changes

### Common Errors
```bash
# Check if server is running
curl http://localhost:8000/health

# View server logs
pyclarity server --debug

# Test tool availability
pyclarity list-tools
```

### Performance Optimization
- Use `complexity_level: "simple"` for faster responses
- Limit `reasoning_depth` for sequential thinking
- Set appropriate `max_hypotheses` for scientific method

## Development

### Adding Custom Tools
1. Create analyzer in `src/pyclarity/tools/your_tool/`
2. Add to `tool_handlers.py`
3. Register in `mcp_server.py`
4. Update `__init__.py` exports

### Testing MCP Integration
```bash
# Run integration tests
pytest tests/mcp/ -v

# Test specific tool
pytest tests/mcp/test_mental_models_mcp.py -v
```

## Advanced Usage

### Batch Analysis
```python
# Use multiple tools in sequence through natural language
"First analyze this with mental models using first principles, then apply sequential thinking to the insights, finally use the decision framework to recommend next steps"
```

### Custom Configurations
```json
{
  "mcpServers": {
    "pyclarity-dev": {
      "command": "uv",
      "args": ["run", "pyclarity", "server", "--debug", "--port", "8001"],
      "cwd": "/path/to/PyClarity",
      "env": {
        "PYCLARITY_DEBUG": "true",
        "PYTHONPATH": "/path/to/PyClarity/src"
      }
    }
  }
}
```

## Support

- **Issues**: [GitHub Issues](https://github.com/kevinhill/PyClarity/issues)
- **Documentation**: [GitHub Wiki](https://github.com/kevinhill/PyClarity/wiki)
- **Examples**: See `examples/mcp/` directory