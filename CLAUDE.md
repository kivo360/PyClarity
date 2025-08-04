# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## CRITICAL: Testing Requirements

### Always Test Your Code
- **NEVER** commit or present code without testing it first
- **RUN** all code you write to verify it works
- **TEST** edge cases and error conditions
- **PREFER** Test-Driven Development (TDD) approach

### TDD Workflow (Preferred)
1. **Write the test first** - Define expected behavior
2. **Run test and watch it fail** - Verify test is testing the right thing
3. **Write minimal code** - Just enough to make test pass
4. **Run test and watch it pass** - Verify implementation
5. **Refactor** - Improve code while keeping tests green
6. **Run tests again** - Ensure refactoring didn't break anything

### Testing Commands
```bash
# Before writing any feature code
python -m pytest tests/test_new_feature.py -xvs  # Write this test first!

# During development
python -m pytest -xvs                             # Run all tests verbosely
python -m pytest tests/specific_test.py::test_function  # Run specific test
python -m pytest --lf                             # Run last failed tests

# Before committing
poe test                                          # Full test suite with coverage
poe lint                                          # Ensure code quality
```

## Development Commands

### Core Development Workflow
```bash
# Setup development environment
uv sync --python 3.12 --all-extras
source .venv/bin/activate
pre-commit install --install-hooks

# Primary development tasks
poe                    # List all available tasks
poe lint              # Run all code quality checks (ruff, mypy, pre-commit)
poe test              # Run test suite with coverage reporting
poe docs              # Generate documentation with pdoc

# Package management
uv add {package}                       # Add runtime dependency
uv add {package} --dev                 # Add dev dependency
uv sync --upgrade                      # Upgrade all dependencies
uv build                               # Build package for distribution
```

### Testing Commands
```bash
# Run specific tests
python -m pytest tests/test_cli.py                    # Test CLI functionality
python -m pytest tests/test_import.py                 # Test package imports
python -m pytest -k "test_name"                       # Run specific test
python -m pytest --cov-report=html                    # Generate HTML coverage report
```

### CLI Testing
```bash
# Test the CLI directly
pyclarity --help
pyclarity fire --name "test"
```

### Version Management
```bash
cz bump                               # Bump version, update CHANGELOG.md, create git tag
git push origin main --tags           # Push changes and tags to trigger publishing
```

## Project Architecture

### Package Structure
- **src/pyclarity/**: Main package code with CLI implementation in `cli.py`
- **tests/**: Test suite with CLI tests and import validation
- **Entry Point**: `pyclarity` command via Typer CLI framework

### Build System
- **Package Manager**: UV (modern Python packaging with lock files)
- **Build Backend**: Hatchling with dynamic versioning
- **Python Target**: 3.12+ (CI tests 3.10 and 3.12)

### Code Quality Stack
- **Formatting/Linting**: Ruff with comprehensive rule set (96 rules enabled)
- **Type Checking**: mypy in strict mode
- **Testing**: pytest with coverage reporting (50% minimum threshold)
- **Pre-commit**: Automated code quality enforcement
- **Line Length**: 100 characters maximum

### CLI Architecture Pattern
The CLI uses Typer framework with Rich for formatting:
```python
# Standard CLI command pattern used in cli.py
@app.command()
def command_name(
    param: str = typer.Option(..., help="Parameter description")
) -> None:
    """Command description."""
    # Implementation with Rich console output
```

### Development Environment
- **Primary**: Dev Containers (VS Code/PyCharm) with full tooling pre-configured
- **Docker**: Multi-stage builds with non-root user setup
- **Task Runner**: Poe the Poet for common development tasks

### CI/CD Pipeline
- **Testing**: Matrix testing across Python 3.10/3.12 in Dev Containers
- **Publishing**: Automated PyPI publishing on GitHub releases
- **Dependencies**: Monthly Dependabot updates

### Commit Convention
Project uses Conventional Commits with Commitizen for automated versioning and changelog generation. All commits must follow the conventional commit format.

#### Conventional Commit Format
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

#### Types
- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **perf**: A code change that improves performance
- **test**: Adding missing tests or correcting existing tests
- **build**: Changes that affect the build system or external dependencies
- **ci**: Changes to CI configuration files and scripts
- **chore**: Other changes that don't modify src or test files
- **revert**: Reverts a previous commit

#### Examples
```
feat(auth): add OAuth2 authentication
fix(cli): resolve argument parsing issue
docs: update installation instructions
test(models): add unit tests for validation logic
```

### Key Configuration Files
- `pyproject.toml`: Central configuration for all tools (dependencies, build, testing, linting)
- `.pre-commit-config.yaml`: Code quality automation rules
- `.devcontainer/devcontainer.json`: Development environment specification

## Testing Guidelines for Experiments

### Experiment Code Testing
When creating experimental code (e.g., in `experiment/` directory):
1. **Create a test file** even for experiments
2. **Run the code** to verify basic functionality
3. **Test with sample data** before using real data
4. **Handle errors gracefully** - experiments often reveal edge cases

### Example Experiment Testing
```bash
# For experiment code
cd experiment/personas
python persona_driven_discovery.py  # Run to test basic execution
python -m pytest test_discovery.py  # Run tests if available

# Quick validation
python -c "from persona_driven_discovery import PersonaDrivenDiscovery; print('Import successful')"
```

## CRITICAL: Import Patterns & Module Resolution

### Always Verify Imports Before Using
```bash
# ALWAYS test imports first
python -c "from pyclarity.tools.mental_models import MentalModelsAnalyzer; print('✓ Import works')"

# Check what's actually exported
python -c "import pyclarity; print(dir(pyclarity))"

# Verify module structure
python -c "from pyclarity import tools; print(dir(tools))"
```

### Correct Import Patterns
```python
# ✅ From external code/experiments (PREFERRED)
from pyclarity.tools.mental_models import MentalModelsAnalyzer
from pyclarity import MentalModelsAnalyzer  # If exported in __init__.py

# ✅ From within src/pyclarity package
from .tools.mental_models import MentalModelsAnalyzer
from ..base import CognitiveToolBase

# ❌ NEVER assume relative paths from outside package
from ...src.pyclarity.tools import SomeTool  # WILL FAIL
```

### Common Import Errors to Check
1. **Class name mismatches**: `Constraint` vs `ConstraintSet`
2. **Module not found**: Missing `__init__.py` files
3. **Circular imports**: Check dependency order
4. **Typos in names**: `Tradeoff` vs `TradeOffAnalysis`

### Testing Import Integrity
```bash
# Before ANY feature development
python -m pytest tests/test_import.py -xvs  # Verify all imports work

# Test specific module imports
python -c "from pyclarity.tools import *; print('All tools imported')"

# Check for broken references
grep -r "from.*import" src/ | grep -v "__pycache__" | sort | uniq
```

## High Coverage Requirements

### Why High Coverage Matters
- **AI-generated code often has non-existent references**
- **Import errors are the #1 failure mode**
- **Type mismatches are common**
- **Edge cases reveal integration issues**

### Coverage Standards
```bash
# Minimum 80% coverage required
poe test  # Runs with coverage report

# Check specific module coverage
python -m pytest tests/tools/test_mental_models.py --cov=pyclarity.tools.mental_models --cov-report=term-missing

# Generate detailed HTML report
python -m pytest --cov=pyclarity --cov-report=html
```

### Testing Checklist for Every Change
- [ ] Import test passes
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Coverage >= 80%
- [ ] No broken imports
- [ ] All class/function names verified
- [ ] Edge cases tested

## Verification Protocol

### Before Committing ANY Code
1. **Verify imports work**
   ```bash
   python -c "from module import Class; print('✓')"
   ```

2. **Run the code**
   ```bash
   python experiment/my_code.py  # Actually execute it
   ```

3. **Test with real data**
   ```bash
   python -m pytest tests/ -xvs  # Stop on first failure
   ```

4. **Check for warnings**
   ```bash
   python -W all -m pytest tests/
   ```

### Common Verification Commands
```bash
# Verify package structure
find src -name "*.py" -exec python -m py_compile {} \;

# Check all imports
python -c "import pyclarity; from pyclarity.tools import *"

# Lint for undefined names
ruff check src/ --select F821  # undefined name
ruff check src/ --select F401  # unused import

# Type check
mypy src/pyclarity --strict
```

## Development Best Practices

### For Experiments
1. **Always use virtual environment**
2. **Install package in editable mode**: `uv pip install -e .`
3. **Use absolute imports**: `from pyclarity.tools.x import Y`
4. **Test imports before writing features**
5. **Create minimal test case first**

### Error Prevention
- **Never assume a class exists** - check the actual file
- **Never copy imports** - verify each one
- **Never skip testing** - even for "simple" changes
- **Never trust AI-generated imports** - always verify

### Quick Import Debug
```python
# When import fails, debug systematically:
import sys
print(sys.path)  # Check Python path

import pyclarity
print(pyclarity.__file__)  # Check package location
print(dir(pyclarity))  # Check exports

from pyclarity import tools
print(dir(tools))  # Check submodule exports
```

## Agent OS Documentation

### Product Context
- **Mission & Vision:** @.agent-os/product/mission.md
- **Technical Architecture:** @.agent-os/product/tech-stack.md
- **Development Roadmap:** @.agent-os/product/roadmap.md
- **Decision History:** @.agent-os/product/decisions.md

### Development Standards
- **Code Style:** @~/.agent-os/standards/code-style.md
- **Best Practices:** @~/.agent-os/standards/best-practices.md

### Project Management
- **Active Specs:** @.agent-os/specs/
- **Spec Planning:** Use `@~/.agent-os/instructions/create-spec.md`
- **Tasks Execution:** Use `@~/.agent-os/instructions/execute-tasks.md`

## Workflow Instructions

When asked to work on this codebase:

1. **First**, check @.agent-os/product/roadmap.md for current priorities
2. **Then**, follow the appropriate instruction file:
   - For new features: @.agent-os/instructions/create-spec.md
   - For tasks execution: @.agent-os/instructions/execute-tasks.md
3. **Always**, adhere to the standards in the files listed above

## Important Notes

- Product-specific files in `.agent-os/product/` override any global standards
- User's specific instructions override (or amend) instructions found in `.agent-os/specs/...`
- Always adhere to established patterns, code style, and best practices documented above.