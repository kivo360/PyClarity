# Claude Code: Comprehensive Best Practices & Features Guide

## Overview

Claude Code is an agentic coding tool that lives in your terminal, understands your codebase, and helps you code faster through natural language commands. It integrates directly with your development environment and can execute routine tasks, explain complex code, and handle git workflows.

## Core Features

### 1. **Natural Language Commands**
- Execute coding tasks through conversational commands
- Understand context from your codebase
- Handle complex multi-step operations

### 2. **Available Tools**
```bash
# Core Tools (No Permission Required)
Agent      # Runs sub-agents for complex tasks
Glob       # Find files based on pattern matching
Grep       # Search for patterns in file contents
LS         # List files and directories
Read       # Read file contents
TodoRead   # Read current session's task list
TodoWrite  # Create and manage structured task lists

# File Operations (Permission Required)
Edit       # Make targeted edits to specific files
MultiEdit  # Perform multiple edits atomically
Write      # Create or overwrites files
NotebookEdit   # Modify Jupyter notebook cells
NotebookRead   # Read Jupyter notebook contents

# System Operations (Permission Required)
Bash       # Execute shell commands
WebFetch   # Fetch content from URLs
WebSearch  # Perform web searches with domain filtering
```

### 3. **MCP (Model Context Protocol) Integration**
- Connect to remote MCP servers
- Extend functionality with custom tools
- Support for STDIO, SSE, and HTTP transport methods

### 4. **Git Workflow Integration**
- Handle git operations through natural language
- Understand repository context
- Manage branches, commits, and merges

## Best Practices

### 1. **Customize Your Setup with CLAUDE.md Files**

Create `CLAUDE.md` files to provide project-specific context:

```markdown
# CLAUDE.md
# Bash commands
- npm run build: Build the project
- npm run typecheck: Run the typechecker

# Code style
- Use ES modules (import/export) syntax, not CommonJS (require)
- Destructure imports when possible (eg. import { foo } from 'bar')

# Workflow
- Be sure to typecheck when you're done making a series of code changes
- Prefer running single tests, and not the whole test suite, for performance
```

**Placement Options:**
- **Root of repo** (most common) - `CLAUDE.md` or `CLAUDE.local.md`
- **Parent directories** - Useful for monorepos
- **Child directories** - On-demand context
- **Home folder** - `~/.claude/CLAUDE.md` for global settings

### 2. **Curate Claude's Tool Allowlist**

Manage permissions strategically:

```bash
# Use /permissions command to manage tools
/permissions

# Examples of safe tools to always allow:
- Edit (file editing)
- Bash(git commit:*) (git commits)
- mcp__puppeteer__puppeteer_navigate (MCP tools)
```

### 3. **Use Custom Slash Commands**

Create reusable workflows in `.claude/commands/`:

```markdown
# .claude/commands/fix-github-issue.md
Please analyze and fix the GitHub issue: $ARGUMENTS.

Follow these steps:
1. Use `gh issue view` to get the issue details
2. Understand the problem described in the issue
3. Search the codebase for relevant files
4. Implement the necessary changes to fix the issue
5. Write and run tests to verify the fix
6. Ensure code passes linting and type checking
7. Create a descriptive commit message
8. Push and create a PR
```

### 4. **Leverage MCP (Model Context Protocol)**

Configure MCP servers for extended functionality:

```json
// .mcp.json
{
  "mcpServers": {
    "puppeteer": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-puppeteer"]
    },
    "sentry": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-sentry"]
    }
  }
}
```

### 5. **Use Headless Mode for Automation**

```bash
# For CI/CD and automation
claude -p "your prompt" --output-format stream-json

# For issue triage
claude -p "Analyze this issue and assign appropriate labels" --allowedTools Edit Bash
```

### 6. **Multi-Claude Workflows**

**Parallel Development:**
```bash
# Create multiple git checkouts
git worktree add ../project-feature-a feature-a
git worktree add ../project-feature-b feature-b

# Run Claude in each worktree
cd ../project-feature-a && claude
cd ../project-feature-b && claude
```

**Code Review Workflow:**
1. Have one Claude write code
2. Use `/clear` or start second Claude
3. Have second Claude review the work
4. Start third Claude to read both code and review
5. Have third Claude edit based on feedback

### 7. **Use Checklists and Scratchpads**

For complex workflows, use Markdown files as working scratchpads:

```markdown
# Migration Checklist
- [ ] Analyze current codebase structure
- [ ] Identify deprecated patterns
- [ ] Create migration plan
- [ ] Implement changes incrementally
- [ ] Test each change
- [ ] Update documentation
```

### 8. **Optimize Context Management**

```bash
# Use /clear frequently to keep context focused
/clear

# Pass data efficiently
cat logfile.txt | claude
claude -p "Analyze this data" < data.json
```

### 9. **Use Correction Tools**

When Claude makes mistakes, use correction tools:
- **`/edit`** - Make targeted fixes
- **`/multi-edit`** - Multiple atomic changes
- **`/clear` + retry** - Fresh context for complex issues

### 10. **Git Worktree Strategy**

For multiple independent tasks:

```bash
# Create worktrees for parallel development
git worktree add ../auth-refactor auth-refactor
git worktree add ../ui-components ui-components
git worktree add ../api-optimization api-optimization

# Each worktree gets its own Claude session
cd ../auth-refactor && claude
cd ../ui-components && claude  
cd ../api-optimization && claude

# Clean up when done
git worktree remove ../auth-refactor
git worktree remove ../ui-components
git worktree remove ../api-optimization
```

### 11. **Advanced Prompting Techniques**

**For Maximum Efficiency:**
```
For maximum efficiency, whenever you need to perform multiple independent operations, invoke all relevant tools simultaneously rather than sequentially.
```

**For Complex Tasks:**
```
After receiving tool results, carefully reflect on their quality and determine optimal next steps before proceeding. Use your thinking to plan and iterate based on this new information, and then take the best next action.
```

**For Code Quality:**
```
Please write a high quality, general purpose solution. Implement a solution that works correctly for all valid inputs, not just the test cases. Do not hard-code values or create solutions that only work for specific test inputs.
```

### 12. **Environment-Specific Configurations**

**Development Environment:**
```bash
# Enable all tools for development
claude --allowedTools Edit Bash MultiEdit Write

# Use debug mode for troubleshooting
claude --mcp-debug
```

**Production/CI Environment:**
```bash
# Restrictive permissions for safety
claude -p "your task" --allowedTools Read Grep

# JSON output for automation
claude -p "analyze code" --output-format json
```

### 13. **Testing-First Approach**

```bash
# Always test before committing
python -m pytest tests/test_new_feature.py -xvs  # Write test first!
python -m pytest -xvs                             # Run all tests
poe test                                          # Full test suite
```

### 14. **TDD Workflow (Preferred)**
1. **Write the test first** - Define expected behavior
2. **Run test and watch it fail** - Verify test is testing the right thing
3. **Write minimal code** - Just enough to make test pass
4. **Run test and watch it pass** - Verify implementation
5. **Refactor** - Improve code while keeping tests green
6. **Run tests again** - Ensure refactoring didn't break anything

### 15. **Start Small → Validate → Expand → Scale**
```python
# ❌ WRONG: Writing 200 lines without testing
class ComplexAnalyzer:
    def __init__(self, db, cache, config, logger):
        # 50 lines of setup...
    
    def analyze(self, data):
        # 100 lines of logic...

# ✅ RIGHT: Start with minimal working code
def analyze_simple(text: str) -> str:
    """Minimal working version."""
    return f"Analyzed: {text}"

# Test immediately:
print(analyze_simple("test"))  # Works? Continue.
```

## Slash Commands

### Core Commands
```bash
/release-notes      # View release notes
/approved-tools     # Manage tool permissions
/config             # Toggle conversation compaction
/vim                # Enable Vim bindings
/bug                # Report bugs
/clear              # Clear conversation context
/init               # Generate CLAUDE.md automatically
/permissions        # Manage tool allowlist
```

### MCP Commands
```bash
claude mcp add                    # Interactive setup wizard
claude mcp add-from-claude-desktop # Import from Desktop
claude mcp add-json <n> <json>    # Add JSON configuration
```

### Debug Commands
```bash
claude --mcp-debug                # Enable debug mode
claude --mcp-config <path>        # Run one-off MCP servers
```

## Conversation Management

### Resume Conversations
```bash
claude --continue
claude --resume
```

### Import Files
```bash
@path/to/file.md                  # Import markdown files
```

### Configuration Management
```bash
# Add/remove multiple values
claude config add <value1>,<value2>
claude config remove <value1> <value2>

# Stream JSON output
claude -p --output-format=stream-json
```

## Common Workflows

### 1. **Code Understanding**
```bash
> find the files that handle user authentication
> how do these authentication files work together?
> trace the login process from front-end to database
```

### 2. **Bug Fixing**
```bash
> there's a bug where users can submit empty forms - fix it
> add input validation to the user registration form
```

### 3. **Refactoring**
```bash
> find deprecated API usage in our codebase
> suggest how to refactor utils.js to use modern JavaScript features
> refactor utils.js to use ES2024 features while maintaining behavior
> run tests for the refactored code
```

### 4. **Documentation**
```bash
> explain this code at a beginner level
> generate documentation for this function
> create a tutorial for this feature
```

## Integration with PyClarity

### 1. **Install PyClarity as MCP Server**
```bash
# Install PyClarity
pip install pyclarity

# Start as MCP server
pyclarity server
```

### 2. **Configure in Claude Code**
```json
// .mcp.json
{
  "mcpServers": {
    "pyclarity": {
      "command": "uv",
      "args": ["run", "pyclarity", "server"],
      "cwd": "/path/to/your/PyClarity",
      "env": {
        "PYTHONPATH": "/path/to/your/PyClarity/src"
      }
    }
  }
}
```

### 3. **Use Cognitive Tools**
```bash
> Use the mental models tool to analyze this architecture decision
> Apply the decision framework to evaluate these feature options
> Use sequential thinking to break down this complex refactoring
```

### 4. **Enhanced Development Workflow**
```bash
# Combine Claude Code with PyClarity tools
> Use the debugging approaches tool to analyze this error
> Apply mental models to understand this complex algorithm
> Use collaborative reasoning to design this API
```

## Advanced Features

### 1. **Extended Thinking**
- Available in Claude Opus 4 and Sonnet 4
- Must set temperature to 1 when enabled
- Provides transparency into step-by-step reasoning

### 2. **Tool Use Optimization**
```bash
# For maximum efficiency, invoke multiple tools simultaneously
# rather than sequentially when operations are independent
```

### 3. **Code Quality Practices**
- Write high-quality, general-purpose solutions
- Avoid hard-coding values
- Focus on understanding problem requirements
- Implement correct algorithms, not just test cases

### 4. **File Management**
```python
def backup_file(file_path):
    """Create a backup before editing."""
    backup_path = f"{file_path}.backup"
    if os.path.exists(file_path):
        with open(file_path, 'r') as src, open(backup_path, 'w') as dst:
            dst.write(src.read())
```

## Security & Safety

### 1. **Permission Management**
- Claude Code requests permission for potentially unsafe actions
- Use `/permissions` to manage tool allowlist
- Configure session-specific permissions with `--allowedTools`

### 2. **Safe Defaults**
- Conservative approach prioritizes safety
- File edits and git commits require explicit permission
- MCP tools require allowlist configuration

### 3. **Environment Isolation**
- Use different configurations for development vs production
- Restrict permissions in CI/CD environments
- Use headless mode for automation with limited permissions

## Performance Optimization

### 1. **Context Management**
- Use `/clear` frequently to maintain focused context
- Avoid long conversations that fill context window
- Use scratchpads for complex multi-step tasks

### 2. **Tool Efficiency**
- Invoke multiple independent tools simultaneously
- Use appropriate tools for specific tasks
- Leverage MCP servers for specialized functionality

### 3. **Parallel Development**
- Use git worktrees for independent tasks
- Run multiple Claude sessions simultaneously
- Cycle through sessions to check progress

## Troubleshooting

### 1. **MCP Issues**
```bash
# Enable debug mode
claude --mcp-debug

# Check MCP server configuration
claude mcp list

# Test MCP server connection
claude mcp test <server-name>
```

### 2. **Permission Issues**
```bash
# Check current permissions
/permissions

# Add specific tools
/permissions add Edit
/permissions add Bash(git commit:*)
```

### 3. **Context Issues**
```bash
# Clear conversation
/clear

# Start fresh session
claude --clear-context
```

## Best Practices Summary

### 1. **Setup & Configuration**
- Create comprehensive `CLAUDE.md` files
- Configure tool allowlist appropriately
- Set up MCP servers for extended functionality
- Use custom slash commands for repeated workflows

### 2. **Development Workflow**
- Start small and validate incrementally
- Use TDD approach when possible
- Test code before committing
- Use git worktrees for parallel development

### 3. **Context Management**
- Use `/clear` frequently
- Use scratchpads for complex tasks
- Pass data efficiently (pipes, files)
- Manage conversation length

### 4. **Quality Assurance**
- Use multiple Claude instances for review
- Leverage correction tools when needed
- Use headless mode for automation
- Monitor and optimize performance

### 5. **Integration**
- Combine with PyClarity for enhanced reasoning
- Use MCP servers for specialized tools
- Configure environment-specific settings
- Maintain security and safety practices

## Conclusion

Claude Code represents a powerful evolution in AI-assisted development, providing direct integration with your development environment while maintaining safety and flexibility. By following these best practices and leveraging the integration with PyClarity's cognitive tools, developers can achieve significantly improved productivity and code quality.

The key is to start with the basics (CLAUDE.md files, proper permissions), gradually add complexity (MCP servers, custom commands), and optimize for your specific workflow (parallel development, context management). This creates a comprehensive AI-assisted development environment that enhances rather than replaces human capabilities. 