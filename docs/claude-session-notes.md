# Claude Session Notes - Library Documentation Requirements

Date: 2025-08-05

## Key Changes Made

### 1. Updated CLAUDE.md with Mandatory Library Research Rules

Added comprehensive section to `/Users/kevinhill/Coding/Tooling/PyClarity/CLAUDE.md` requiring:
- MANDATORY documentation checks for all non-standard libraries
- Local documentation priority (check `@docs/` first)
- Specific reference to FastMCP local docs
- Programmatic examples of research workflow

### 2. Local Documentation Resources

- **FastMCP Documentation**: Available at `@docs/library-docs/fastmcp/llms-full.txt`
- File contains 23,130 lines of comprehensive FastMCP documentation
- Includes changelog, API references, examples, and more
- Should ALWAYS be checked before using online resources

### 3. Library Research Protocol

Established clear protocol:
1. Check local docs first (`@docs/library-docs/`)
2. Search project test files for examples
3. Verify versions in pyproject.toml
4. Use Context7/DeepWiki only if needed
5. Store findings in memory for future use

### 4. Example Implementation

Added detailed example for "How to use FastMCP client to run tests":
```typescript
// Tool call sequence:
1. mcp__openmemory__search-memories({ query: "FastMCP client testing patterns" })
2. Grep local docs with multiple patterns
3. Glob and Grep project test files
4. Read pyproject.toml for versions
5. Use online resources only if needed
6. mcp__openmemory__add-memory() to store findings
```

### 5. Libraries Requiring Documentation

Identified key libraries that ALWAYS need documentation checks:
- FastMCP (local docs available)
- Pydantic (v2 changes)
- FastAPI
- Typer
- Rich
- Any library < 20 years old or actively evolving

## Next Topics (User Mentioned)

User planning to discuss:
1. **Session storage** - Likely for maintaining state across tool calls
2. **Forcing one step at a time** - Sequential execution for all tools
3. **Sequential thinking specific** - Currently viewing `src/pyclarity/tools/sequential_thinking/analyzer.py`

## Important Files Modified

1. `/Users/kevinhill/Coding/Tooling/PyClarity/CLAUDE.md` - Added External Library Research section
2. (Note: Initially edited wrong file at `/Users/kevinhill/.claude/CLAUDE.md` but user corrected to edit project file instead)

## Key Principles Established

1. **NEVER trust memory for non-standard library APIs** - Always research current documentation
2. **Local docs first** - Faster and more comprehensive than online queries
3. **Version awareness** - Always check pyproject.toml for exact versions
4. **Programmatic approach** - Use systematic search patterns, not random exploration
5. **Knowledge persistence** - Store findings in memory for future queries

## Critical Reminder

For any library that isn't part of the standard library or has been actively developed in the last 20 years, YOU MUST check current documentation before writing code. This is not optional - it's mandatory to ensure accuracy and prevent outdated API usage.