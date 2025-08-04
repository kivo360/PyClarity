# Ruff Configuration Summary

## Major Rules Configuration

The PyClarity project has been configured to use only major ruff rules that catch critical issues affecting code functionality, while disabling style-focused rules.

### Enabled Rule Categories

1. **F (Pyflakes)** - Critical errors:
   - F401: Unused imports
   - F811: Redefined functions/variables
   - F821: Undefined names
   - F841: Unused variables
   - Other syntax errors

2. **E (pycodestyle errors)** - Major syntax issues:
   - E722: Bare except clauses
   - Indentation errors
   - Syntax errors
   - Other critical formatting that affects functionality

3. **W (pycodestyle warnings)** - Important warnings:
   - W291: Trailing whitespace
   - W293: Blank line with whitespace
   - Other warnings that could indicate issues

4. **I (isort)** - Import organization:
   - Import sorting and grouping
   - Helps maintain consistent import structure

5. **UP (pyupgrade)** - Python compatibility:
   - UP035: Deprecated imports
   - UP038: Non-PEP604 isinstance usage
   - Ensures code uses modern Python patterns

### Disabled Rules

All style-focused rules have been disabled, including:
- A (flake8-builtins) - Builtin shadowing
- ASYNC (flake8-async) - Async best practices
- B (flake8-bugbear) - Opinionated warnings
- C4 (flake8-comprehensions) - Comprehension suggestions
- C90 (mccabe) - Complexity checking
- D (pydocstyle) - Docstring formatting
- N (pep8-naming) - Naming conventions
- S (flake8-bandit) - Security checks
- And many others...

### Ignored Errors

Even within major categories, some common issues are ignored:
- **E501**: Line too long (handled by formatter)
- **E741**: Ambiguous variable names

### Current Critical Issues

As of this configuration, the codebase has 6 critical errors to fix:
1. **1 undefined name** (F821) - `ImpactPropagationContext` not imported
2. **2 redefined imports** (F811) - Duplicate imports in `__init__.py`
3. **3 bare except clauses** (E722) - Should specify exception types

### Benefits

1. **Faster CI/CD** - Fewer rules to check
2. **Focus on functionality** - Only catch real bugs
3. **Less noise** - No style debates
4. **Easier onboarding** - New contributors don't need to learn 96 style rules

### Running Ruff

```bash
# Check for major issues
ruff check src/

# Fix auto-fixable issues (carefully review changes)
ruff check src/ --fix

# Show statistics
ruff check src/ --statistics

# Check specific rule categories
ruff check src/ --select F,E
```

### Next Steps

1. Fix the 6 critical errors identified
2. Consider adding back specific rules if team needs them
3. Document any project-specific conventions separately