# Architecture & Code Quality Tools for PyClarity

This document covers advanced tools for maintaining code quality, architectural integrity, and development velocity in Python projects.

## Tool Overview

### 1. Tach - Architecture Enforcement (Rust-based)

**What it does**: Enforces module boundaries and prevents architectural violations at build time.

**Key Features**:
- Written in Rust for blazing fast performance
- Inspired by modular monolith architecture
- Prevents circular dependencies
- Enforces clean module boundaries
- Integrates with CI/CD pipelines

**Installation & Setup**:
```bash
pip install tach

# Interactive setup
tach mod

# Manual configuration
```

**Configuration Example** (`tach.toml`):
```toml
# Define module boundaries
[modules]
[modules.models]
path = "src/pyclarity/models"
# Models should have no dependencies

[modules.tools]
path = "src/pyclarity/tools"
depends_on = ["models"]  # Tools can use models

[modules.server]
path = "src/pyclarity/server"
depends_on = ["tools", "models"]  # Server can use both

[modules.cli]
path = "src/pyclarity/cli"
depends_on = ["tools"]  # CLI uses tools but not server internals

# Prevent circular dependencies
[modules.tests]
path = "tests"
depends_on = ["models", "tools", "server", "cli"]
```

**Usage**:
```bash
# Check for violations
tach check

# Example output:
# ❌ src/pyclarity/cli/runner.py:12: Cannot import from 'src.pyclarity.server.internal'
# ❌ src/pyclarity/models/user.py:5: Circular dependency with 'src.pyclarity.tools.analyzer'

# Sync configuration with current imports
tach sync

# Run tests for specific module
tach test tools

# Generate dependency graph
tach graph --output deps.svg
```

### 2. Import-Linter - Import Contract Enforcement

**What it does**: Defines and enforces contracts about how modules can import from each other.

**Key Features**:
- More flexible than Tach for complex rules
- Multiple contract types (layers, independence, forbidden)
- Detailed violation reports
- Pre-commit hook integration

**Installation**:
```bash
pip install import-linter
```

**Configuration** (`.importlinter`):
```ini
[importlinter]
root_package = pyclarity
include_external_packages = True

[contracts]
# Contract 1: Enforce layered architecture
name = "Layered architecture"
type = layers
layers =
    pyclarity.models
    pyclarity.tools
    pyclarity.server
    pyclarity.cli
# Lower layers cannot import from higher layers

# Contract 2: Models must be independent
name = "Models are independent"
type = independence
modules =
    pyclarity.models.user
    pyclarity.models.project
    pyclarity.models.analysis

# Contract 3: No internal imports
name = "No internal module imports"
type = forbidden
source_modules =
    pyclarity.cli
    pyclarity.api
forbidden_modules =
    pyclarity.server.internal
    pyclarity.tools.internal

# Contract 4: Utilities are leaf modules
name = "Utils cannot import domain logic"
type = forbidden
source_modules =
    pyclarity.utils
forbidden_modules =
    pyclarity.models
    pyclarity.tools
    pyclarity.server
```

**Usage**:
```bash
# Check all contracts
lint-imports

# Check specific contract
lint-imports --contract "Layered architecture"

# Generate import graph
lint-imports --print-graph
```

### 3. ls-lint - File & Directory Name Linter

**What it does**: Extremely fast linter for file and directory names with configurable rules.

**Key Features**:
- Written in Go for blazing fast performance (lints thousands of files in milliseconds)
- Supports multiple naming conventions (kebab-case, snake_case, PascalCase, etc.)
- Directory-specific rules and patterns
- Full unicode support
- Minimal dependencies

**Installation**:
```bash
# npm/yarn
npm install -g @ls-lint/ls-lint

# Homebrew  
brew install ls-lint

# Download binary
curl -sL -o ls-lint https://github.com/loeffel-io/ls-lint/releases/download/v2.3.0/ls-lint-linux
chmod +x ls-lint
```

**Configuration** (`.ls-lint.yml`):
```yaml
# Python library naming conventions
ls:
  # Root level - package names should be lowercase
  .py: snake_case
  .dir: lowercase | snake_case
  
  # Source code structure
  src:
    .dir: lowercase | snake_case
    .py: snake_case
    
    # PyClarity specific structure
    pyclarity:
      .dir: lowercase | snake_case
      .py: snake_case
      
      # Tools can have more flexible naming
      tools:
        .py: snake_case | lowercase
        .dir: lowercase | snake_case
      
      # Models follow strict conventions
      models:
        .py: snake_case
        .dir: snake_case
      
      # Private modules
      _internal:
        .py: snake_case
  
  # Tests follow test_ prefix convention
  tests:
    .py: regex:^test_.*
    .dir: lowercase | snake_case
    
    # Fixtures and conftest
    conftest.py: lowercase
    fixtures:
      .py: snake_case
  
  # Documentation
  docs:
    .md: kebab-case | lowercase | SCREAMING_SNAKE_CASE # README, LICENSE, etc.
    .rst: lowercase | kebab-case
    .dir: kebab-case | lowercase
  
  # Examples can be more flexible
  examples:
    .py: snake_case | kebab-case
    .dir: kebab-case | snake_case
  
  # Scripts
  scripts:
    .py: snake_case | kebab-case
    .sh: kebab-case | snake_case

ignore:
  - .git
  - node_modules
  - __pycache__
  - .pytest_cache
  - .mypy_cache
  - .ruff_cache
  - "*.egg-info"
  - .venv
  - build
  - dist
```

**Advanced Patterns**:
```yaml
ls:
  # Detect library structure
  "**/models":
    .py: snake_case
    
  "**/tests":
    .py: regex:^test_.*
    
  "**/__pycache__":
    .pyc: snake_case
    
  # Version files
  "**/VERSION": uppercase
  "**/_version.py": snake_case
```

**Usage**:
```bash
# Check all files
ls-lint

# Check specific directory
ls-lint src/

# Show version
ls-lint --version

# Quiet mode (only show errors)
ls-lint --quiet
```

**Integration with Pre-commit**:
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/loeffel-io/ls-lint
    rev: v2.3.0
    hooks:
      - id: ls-lint
        name: Check file/directory names
```

### 4. PEP8-Naming - Naming Convention Enforcement

**What it does**: Enforces Python naming conventions as defined in PEP 8.

**Integration Options**:

#### With Ruff (Recommended - Fast):
```toml
# pyproject.toml
[tool.ruff]
select = ["N"]  # Enable all pep8-naming rules

# Or specific rules:
# N801 - Class names should use CapWords
# N802 - Function names should be lowercase
# N803 - Argument names should be lowercase
# N804 - First argument of classmethod should be 'cls'
# N805 - First argument of method should be 'self'
# N806 - Variable in function should be lowercase
# N807 - Function names should not start/end with '__'

ignore = [
    "N802",  # Allow some mixed case for AI tools
    "N806",  # Allow uppercase in specific modules
]

[tool.ruff.pep8-naming]
# Decorators that create classmethods
classmethod-decorators = ["classmethod", "pydantic.validator", "cached_classmethod"]
# Decorators that create staticmethods  
staticmethod-decorators = ["staticmethod", "cached_staticmethod"]
```

#### With Flake8:
```ini
# .flake8 or setup.cfg
[flake8]
select = N
ignore = N802,N806
pep8-naming-classmethod-decorators = classmethod,validator
```

**Common Violations & Fixes**:
```python
# ❌ N801: Class name should use CapWords convention
class my_analyzer:  # Bad
    pass

class MyAnalyzer:  # ✅ Good
    pass

# ❌ N802: Function name should be lowercase
def ProcessData():  # Bad
    pass

def process_data():  # ✅ Good
    pass

# ❌ N803: Argument name should be lowercase  
def analyze(InputData):  # Bad
    pass

def analyze(input_data):  # ✅ Good
    pass

# ❌ N805: First argument of method should be 'self'
class Tool:
    def process(this, data):  # Bad
        pass
    
    def process(self, data):  # ✅ Good
        pass

# ❌ N806: Variable in function should be lowercase
def calculate():
    Result = 42  # Bad
    return Result

def calculate():
    result = 42  # ✅ Good
    return result
```

### 4. Context7 - Live Documentation MCP Server

**What it does**: Provides up-to-date library documentation directly in your editor via MCP.

**Key Features**:
- Real-time documentation updates
- Works with Claude Code, Cursor, VS Code
- Covers 1000+ libraries
- Context-aware suggestions

**Installation**:

For VS Code:
```bash
npx @context7/context7-mcp
```

For Cursor:
```bash
# Add to .cursorrules or project instructions
```

**Configuration** (`.claude/mcp_settings.json`):
```json
{
  "servers": {
    "context7": {
      "command": "npx",
      "args": ["@context7/context7-mcp"],
      "enabled": true
    }
  }
}
```

**Usage in AI Development**:
```python
# In your CLAUDE.md or .cursorrules:
"""
Always use Context7 to check current documentation for:
- FastMCP (rapidly evolving)
- Pydantic (v2 has major changes)
- Any library updated in last 6 months

Tools available:
- context7.resolveLibraryId(libraryName)
- context7.getLibraryDocs(context7CompatibleLibraryID, topic)
"""
```

## Integration Strategies

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  # Architecture checks
  - repo: local
    hooks:
      - id: tach-check
        name: Check architecture boundaries
        entry: tach check
        language: system
        pass_filenames: false
        always_run: true

      - id: import-linter
        name: Check import contracts
        entry: lint-imports
        language: python
        pass_filenames: false
        always_run: true

  # Naming conventions (via Ruff)
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [--select, "N"]
```

### CI/CD Pipeline

```yaml
# .github/workflows/quality.yml
name: Code Quality

on: [push, pull_request]

jobs:
  architecture:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install dependencies
        run: |
          pip install tach import-linter
      
      - name: Check module boundaries
        run: tach check
        
      - name: Check import contracts
        run: lint-imports
        
      - name: Generate architecture report
        run: |
          tach graph --output architecture.svg
          echo "Architecture diagram saved"
```

### VS Code Settings

```json
// .vscode/settings.json
{
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.linting.flake8Args": [
    "--select=N"
  ],
  "ruff.enable": true,
  "ruff.lint.select": ["N"],
  
  // Run architecture checks on save
  "runOnSave.commands": [
    {
      "match": ".*\\.py$",
      "command": "tach check --quiet",
      "runIn": "terminal"
    }
  ]
}
```

## Best Practices

### 1. Start Simple, Add Gradually

```bash
# Day 1: Basic setup
pip install tach ruff
tach mod  # Interactive setup
ruff check --select N

# Week 1: Add contracts
pip install import-linter
# Create .importlinter with basic contracts

# Month 1: Full integration
# Add pre-commit hooks
# Integrate with CI/CD
# Add Context7 for team
```

### 2. Module Design Principles

```
src/pyclarity/
├── models/        # No dependencies (bottom layer)
├── core/          # Business logic, depends on models
├── tools/         # Features, depends on core + models  
├── server/        # API layer, depends on tools
├── cli/           # UI layer, depends on tools (not server)
└── utils/         # Helpers, no domain dependencies
```

### 3. Contract Evolution

Start with simple contracts:
```ini
# Phase 1: Basic independence
[contracts]
name = "Models are independent"
type = independence
modules = pyclarity.models
```

Evolve to comprehensive rules:
```ini
# Phase 2: Full architecture
[contracts]
name = "Complete architecture"
type = layers
layers =
    pyclarity.utils
    pyclarity.models  
    pyclarity.core
    pyclarity.tools
    pyclarity.server
    pyclarity.cli
```

## Troubleshooting

### Tach Issues

**Problem**: "Module not found" errors
```bash
# Solution: Ensure Python path is correct
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
tach check
```

**Problem**: Configuration drift
```bash
# Solution: Sync with current state
tach sync --update
```

### Import-Linter Issues

**Problem**: Slow on large codebases
```bash
# Solution: Use parallel processing
lint-imports --parallel 4
```

**Problem**: External package issues
```ini
# Solution: Configure external handling
[importlinter]
include_external_packages = False
```

### Context7 Issues

**Problem**: MCP not connecting
```bash
# Solution: Check MCP server status
npx @context7/context7-mcp --test

# Verify in editor
# VS Code: Cmd+Shift+P → "MCP: Show Servers"
```

## Performance Considerations

| Tool | Small Project (<10k LOC) | Medium (10-100k) | Large (>100k) |
|------|-------------------------|------------------|---------------|
| Tach | <100ms | <500ms | <2s |
| Import-linter | <1s | <5s | <20s |
| Ruff (naming) | <100ms | <200ms | <500ms |
| All combined | <2s | <6s | <25s |

## Python Library Naming Conventions

### PEP 8 Standards for Libraries

Based on PEP 8 and Python community best practices, here are the naming conventions for Python libraries:

#### Package and Module Names
- **Packages**: Short, all-lowercase names (e.g., `requests`, `numpy`, `flask`)
- **Modules**: Short, all-lowercase names with underscores if needed (e.g., `os_path.py`, `string_utils.py`)
- **Avoid**: Hyphens in package names (use underscores or no separator)

#### Directory Structure
```
pyclarity/                    # Root package (lowercase)
├── __init__.py              # Package initializer
├── core/                    # Subpackage (lowercase)
│   ├── __init__.py
│   ├── base_classes.py      # Module (snake_case)
│   └── utils.py
├── models/                  # Models subpackage
│   ├── __init__.py
│   ├── user_model.py        # Model files (snake_case)
│   └── data_structures.py
├── tools/                   # Tools subpackage
│   ├── __init__.py
│   ├── analyzer.py
│   └── validator.py
├── _internal/               # Private subpackage (leading underscore)
│   └── helpers.py
└── tests/                   # Tests (outside main package)
    ├── test_core.py         # Test files (test_ prefix)
    └── test_models.py
```

#### Class Names
- Use CapWords (PascalCase) convention
- No underscores between words
```python
class HTTPServerError:  # Acronyms stay uppercase
class JsonParser:       # Not JSONParser
class DataAnalyzer:     # Not Data_Analyzer
```

#### Function and Variable Names
- Use lowercase with underscores (snake_case)
```python
def calculate_average():
    pass

def process_user_data():
    pass

user_count = 0
max_retry_attempts = 3
```

#### Constants
- Use UPPER_CASE_WITH_UNDERSCORES
```python
MAX_BUFFER_SIZE = 1024
DEFAULT_TIMEOUT = 30
API_VERSION = "1.0"
```

#### Private vs Public
- Single leading underscore for internal use
- Double leading underscore for name mangling (rare)
```python
_internal_cache = {}  # Module-private
__private_var = 0     # Name mangling (becomes _ClassName__private_var)

def _helper_function():  # Internal use
    pass

def public_function():   # Part of public API
    pass
```

### ls-lint Configuration for Python Libraries

Here's a comprehensive `.ls-lint.yml` for Python library projects:

```yaml
ls:
  # Package structure
  .py: snake_case
  .pyi: snake_case  # Type stubs
  .pyx: snake_case  # Cython files
  .dir: lowercase | snake_case
  
  # Special Python files
  __init__.py: lowercase
  __main__.py: lowercase
  __version__.py: lowercase
  setup.py: lowercase
  conftest.py: lowercase
  
  # Configuration files
  pyproject.toml: lowercase
  setup.cfg: lowercase
  .flake8: lowercase
  .coveragerc: lowercase
  MANIFEST.in: uppercase
  
  # Documentation
  README.md: uppercase
  README.rst: uppercase
  LICENSE: uppercase
  LICENSE.txt: uppercase
  LICENSE.md: uppercase
  CONTRIBUTING.md: uppercase
  CHANGELOG.md: uppercase
  AUTHORS: uppercase
  
  # Requirements files
  requirements.txt: lowercase
  requirements-dev.txt: kebab-case
  requirements-test.txt: kebab-case
  
  # Directory-specific rules
  tests:
    .py: regex:^test_.*|^conftest$
    
  docs:
    .md: kebab-case | lowercase
    .rst: kebab-case | lowercase
    conf.py: lowercase
    
  examples:
    .py: snake_case | kebab-case
    
  scripts:
    .py: snake_case | kebab-case
    .sh: snake_case | kebab-case

ignore:
  - .git
  - __pycache__
  - "*.egg-info"
  - .pytest_cache
  - .mypy_cache
  - .tox
  - .venv
  - venv
  - build
  - dist
  - htmlcov
  - .coverage
```

### Using ls-lint to Analyze Library Structure

To check naming conventions in existing libraries:

```bash
# Check popular Python libraries
git clone https://github.com/requests/requests.git
cd requests
ls-lint

# Check your own library
cd my-python-library
ls-lint

# Check specific patterns
ls-lint src/  # Just source code
ls-lint tests/  # Just tests
```

### Common Naming Patterns in Popular Libraries

| Library | Package Name | Module Pattern | Class Pattern |
|---------|-------------|----------------|---------------|
| requests | `requests` | `models.py`, `api.py` | `Response`, `Session` |
| flask | `flask` | `app.py`, `blueprints.py` | `Flask`, `Blueprint` |
| django | `django` | `models.py`, `views.py` | `Model`, `View` |
| numpy | `numpy` | `core.py`, `linalg.py` | `ndarray`, `matrix` |
| pandas | `pandas` | `core/frame.py` | `DataFrame`, `Series` |

### Best Practices for Library Naming

1. **Be Descriptive but Concise**
   ```
   ✓ pyclarity  # Clear purpose
   ✓ requests   # Simple and descriptive
   ✗ py-super-awesome-tool  # Too long
   ✗ tool       # Too vague
   ```

2. **Avoid Name Conflicts**
   - Check PyPI for existing names
   - Don't shadow standard library modules
   - Consider namespacing for organization packages

3. **Consistency Within Project**
   - If using `user_model.py`, don't mix with `usercontroller.py`
   - Pick a pattern and stick to it throughout

4. **Version Information**
   ```python
   # pyclarity/__version__.py or pyclarity/_version.py
   __version__ = "1.0.0"
   ```

5. **Public API Definition**
   ```python
   # pyclarity/__init__.py
   __all__ = ["Analyzer", "Validator", "process_data"]
   ```

## Conclusion

These tools form a comprehensive architecture and quality enforcement system:

- **Tach**: Fast, simple module boundaries
- **Import-linter**: Complex import rules and contracts
- **ls-lint**: File and directory name consistency
- **PEP8-naming**: Consistent code naming conventions
- **Context7**: Always-current documentation

Used together, they prevent architectural decay, maintain code quality, and accelerate development through immediate feedback and current documentation. The combination of ls-lint for filesystem structure and PEP8-naming for code structure ensures complete naming consistency throughout your Python projects.