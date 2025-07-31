# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

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