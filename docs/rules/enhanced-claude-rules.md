# Enhanced CLAUDE.md Rules for PyClarity

## Core Development Principles

### 1. Start Small → Validate → Expand → Scale (MANDATORY)

**CRITICAL: This is the #1 rule that overrides all others.**

```python
# ❌ WRONG: Writing 200 lines without testing
class ComplexAnalyzer:
    def __init__(self, db, cache, config, logger):
        # 50 lines of setup...
    
    def analyze(self, data):
        # 100 lines of logic...
    
    def process_results(self, results):
        # 50 lines of processing...

# ✅ RIGHT: Start with minimal working code
# Step 1: Simplest possible version (5 minutes)
def analyze_simple(text: str) -> str:
    """Minimal working version."""
    return f"Analyzed: {text}"

# Test immediately:
print(analyze_simple("test"))  # Works? Continue.

# Step 2: Add one feature (5 minutes)
def analyze_with_logging(text: str) -> str:
    """Add logging."""
    logger.info(f"Analyzing: {text}")
    result = f"Analyzed: {text}"
    logger.success(f"Result: {result}")
    return result

# Test again:
print(analyze_with_logging("test"))  # Works? Continue.

# Step 3: Only NOW add complexity
```

### 2. Reference Validation Before Implementation

**Every import and class reference must be validated BEFORE use:**

```python
# ALWAYS start new files with import validation block
#!/usr/bin/env python3
"""
Validate all imports before implementing features.
"""
from loguru import logger
import sys

# Configure logging first
logger.remove()
logger.add(sys.stderr, format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}:{line}</cyan> - <level>{message}</level>")

# Validation block - ALWAYS include this
try:
    logger.info("🔍 Validating imports...")
    
    # Test each import individually
    from pyclarity.db.memory_stores import MemorySessionStore
    logger.success("✅ MemorySessionStore")
    
    from pyclarity.db.memory_stores import MemoryThoughtStore  
    logger.success("✅ MemoryThoughtStore")
    
    from pyclarity.tools.sequential_thinking.progressive_analyzer import (
        ProgressiveSequentialThinkingAnalyzer,
        ProgressiveThoughtRequest,
        ProgressiveThoughtResponse
    )
    logger.success("✅ Sequential thinking imports")
    
except ImportError as e:
    logger.exception(e)
    logger.error("❌ Import validation failed")
    logger.info("Debug hints:")
    logger.info("  1. Check file exists: find src -name '*.py' | grep memory_stores")
    logger.info("  2. Check class names: grep -n '^class' src/pyclarity/db/memory_stores.py")
    sys.exit(1)

logger.success("✨ All imports validated!")

# NOW you can write implementation code
```

### 3. Loguru Exception Handling Pattern

**Every function that could fail MUST use this pattern:**

```python
from loguru import logger

@logger.catch(message="Failed to process data", reraise=True)
async def process_data(data: dict) -> dict:
    """Process with comprehensive error tracking."""
    logger.debug(f"Processing data with keys: {list(data.keys())}")
    
    try:
        # Step 1: Validate input
        if not data:
            raise ValueError("Empty data provided")
        logger.debug("✓ Input validated")
        
        # Step 2: Process
        result = await actual_processing(data)
        logger.debug(f"✓ Processing complete: {len(result)} items")
        
        # Step 3: Validate output
        if not result:
            logger.warning("Processing returned empty result")
        
        logger.success(f"Successfully processed {len(result)} items")
        return result
        
    except KeyError as e:
        logger.exception(e)
        logger.error(f"Missing required key: {e}")
        logger.info("Available keys: " + ", ".join(data.keys()))
        raise
        
    except Exception as e:
        logger.exception(e)  # Full traceback with context
        logger.error(f"Unexpected error in {__name__}")
        logger.debug(f"Data that caused error: {data}")
        raise
```

### 4. Watchexec-Optimized Test Structure

**Every example/test file MUST follow this structure:**

```python
#!/usr/bin/env python3
"""
examples/test_feature.py - Watchexec-optimized test file

Run with: watchexec -e py python examples/test_feature.py
"""
import os
import sys
from datetime import datetime
from loguru import logger

# Clear screen for fresh output
print("\033[2J\033[H")
print(f"{'='*60}")
print(f"🔄 Run started: {datetime.now().strftime('%H:%M:%S')}")
print(f"{'='*60}\n")

# Configure logging for development
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{function}:{line}</cyan> - <level>{message}</level>",
    level="DEBUG"
)

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import validation block (MANDATORY)
logger.info("📦 Validating imports...")
try:
    # Your imports here, one at a time
    from module import Class
    logger.success("✅ Class imported")
except ImportError as e:
    logger.exception(e)
    sys.exit(1)

# Test implementation
@logger.catch(reraise=True)
def main():
    """Main test function."""
    logger.info("🚀 Starting tests")
    
    # Test 1: Simplest case
    logger.info("Test 1: Basic functionality")
    try:
        result = simple_test()
        logger.success(f"✅ Test 1 passed: {result}")
    except Exception as e:
        logger.exception(e)
        return False
    
    # Test 2: Add complexity
    logger.info("Test 2: With options")
    try:
        result = test_with_options()
        logger.success(f"✅ Test 2 passed: {result}")
    except Exception as e:
        logger.exception(e)
        return False
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        
        # Summary
        print(f"\n{'='*60}")
        if success:
            logger.success("✅ All tests passed!")
            print("✅ ALL TESTS PASSED")
        else:
            logger.error("❌ Tests failed!")
            print("❌ TESTS FAILED")
        print(f"{'='*60}\n")
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        logger.warning("⚠️ Interrupted by user")
        sys.exit(1)
```

### 5. Progressive Implementation Pattern

**Build features incrementally with validation at each step:**

```python
# Stage 1: Define minimal interface (2 minutes)
class ProgressiveAnalyzer:
    """Minimal analyzer interface."""
    
    def __init__(self):
        logger.info("Analyzer initialized")
    
    def analyze(self, text: str) -> str:
        logger.debug(f"Analyzing: {text[:50]}...")
        return f"Result: {text}"

# TEST IMMEDIATELY
analyzer = ProgressiveAnalyzer()
print(analyzer.analyze("test"))  # Works? Continue.

# Stage 2: Add ONE feature (2 minutes)
class ProgressiveAnalyzer:
    """Analyzer with session support."""
    
    def __init__(self, session_id: str = None):
        self.session_id = session_id or str(uuid.uuid4())
        logger.info(f"Analyzer initialized with session: {self.session_id}")
    
    def analyze(self, text: str) -> dict:
        logger.debug(f"Session {self.session_id}: {text[:50]}...")
        return {
            "session_id": self.session_id,
            "result": f"Result: {text}"
        }

# TEST AGAIN
analyzer = ProgressiveAnalyzer()
print(analyzer.analyze("test"))  # Works? Continue.

# Stage 3: Add stores ONLY after basic functionality works
```

### 6. Import Discovery Pattern

**When you don't know exact class names:**

```python
#!/usr/bin/env python3
"""
discover_imports.py - Find available classes in modules
"""
from loguru import logger
import importlib
import inspect

def discover_module_contents(module_path: str):
    """Discover what's available in a module."""
    logger.info(f"🔍 Discovering contents of {module_path}")
    
    try:
        module = importlib.import_module(module_path)
        logger.success(f"✅ Module loaded: {module_path}")
        
        # Find all classes
        classes = []
        functions = []
        
        for name, obj in inspect.getmembers(module):
            if not name.startswith('_'):
                if inspect.isclass(obj):
                    classes.append(name)
                elif inspect.isfunction(obj):
                    functions.append(name)
        
        if classes:
            logger.info("📦 Available classes:")
            for cls in sorted(classes):
                logger.info(f"   - {cls}")
        
        if functions:
            logger.info("🔧 Available functions:")
            for func in sorted(functions)[:10]:  # First 10
                logger.info(f"   - {func}")
                
        return classes, functions
        
    except ImportError as e:
        logger.exception(e)
        
        # Try to find the file
        import os
        possible_path = module_path.replace('.', '/') + '.py'
        search_path = os.path.join('src', possible_path)
        
        if os.path.exists(search_path):
            logger.info(f"📄 File exists at: {search_path}")
            # Try to read it
            with open(search_path, 'r') as f:
                import re
                content = f.read()
                classes = re.findall(r'^class\s+(\w+)', content, re.MULTILINE)
                if classes:
                    logger.info("📦 Classes found in file:")
                    for cls in classes:
                        logger.info(f"   - {cls}")
        else:
            logger.error(f"❌ File not found: {search_path}")

# Usage
if __name__ == "__main__":
    modules_to_check = [
        "pyclarity.db.memory_stores",
        "pyclarity.tools.sequential_thinking.progressive_analyzer",
        "pyclarity.db.base",
    ]
    
    for module in modules_to_check:
        print(f"\n{'='*60}")
        discover_module_contents(module)
```

### 7. Database Store Testing Pattern

**Always test with in-memory stores first:**

```python
async def test_with_memory_stores():
    """Test pattern using in-memory stores."""
    logger.info("🧪 Testing with in-memory stores")
    
    # Stage 1: Create stores
    try:
        from pyclarity.db.memory_stores import MemorySessionStore, MemoryThoughtStore
        
        session_store = MemorySessionStore()
        thought_store = MemoryThoughtStore()
        logger.success("✅ Stores created")
        
    except Exception as e:
        logger.exception(e)
        return False
    
    # Stage 2: Test basic operations
    try:
        from pyclarity.db.base import SessionData
        
        # Create session
        session = SessionData(
            session_id="test-123",
            tool_name="test-tool"
        )
        saved = await session_store.create_session(session)
        logger.success(f"✅ Session created: {saved.session_id}")
        
        # Retrieve session
        retrieved = await session_store.get_session("test-123")
        assert retrieved is not None
        logger.success("✅ Session retrieved")
        
    except Exception as e:
        logger.exception(e)
        return False
    
    # Stage 3: Only now test your analyzer
    try:
        from your_module import YourAnalyzer
        
        analyzer = YourAnalyzer(
            session_store=session_store,
            thought_store=thought_store
        )
        
        # Test minimal case first
        result = await analyzer.process_simple("test")
        logger.success(f"✅ Analyzer works: {result}")
        
    except Exception as e:
        logger.exception(e)
        return False
    
    return True
```

### 8. Continuous Validation Setup

**Project-wide validation configuration:**

```json
// pyrightconfig.json
{
  "include": ["src", "examples", "tests"],
  "exclude": ["**/__pycache__", ".venv"],
  "reportMissingImports": true,
  "reportUndefinedVariable": true,
  "reportUnknownMemberType": true,
  "pythonVersion": "3.12",
  "typeCheckingMode": "strict"
}
```

```yaml
# .pre-commit-config.yaml addition
repos:
  - repo: local
    hooks:
      - id: validate-imports
        name: Validate Python imports
        entry: python scripts/validate_imports.py
        language: python
        types: [python]
        pass_filenames: false
```

### 9. Error Context Pattern

**Always provide context in errors:**

```python
def process_complex_data(data: dict, config: dict) -> dict:
    """Process with rich error context."""
    context = {
        "function": "process_complex_data",
        "data_keys": list(data.keys()),
        "config_keys": list(config.keys()),
        "timestamp": datetime.now().isoformat()
    }
    
    try:
        # Processing logic
        result = transform_data(data, config)
        return result
        
    except KeyError as e:
        logger.exception(e)
        logger.error(f"Missing key: {e}")
        logger.error(f"Context: {context}")
        logger.info("Debug suggestions:")
        logger.info(f"  - Available data keys: {list(data.keys())}")
        logger.info(f"  - Available config keys: {list(config.keys())}")
        logger.info(f"  - Required keys: ['input', 'output', 'format']")
        raise
        
    except Exception as e:
        logger.exception(e)
        logger.error(f"Unexpected error: {type(e).__name__}")
        logger.error(f"Context: {context}")
        logger.debug(f"Full data: {data}")
        logger.debug(f"Full config: {config}")
        raise
```

### 10. Development Command Reference

**Essential commands for the PyClarity workflow:**

```bash
# Before ANY coding
uv sync --python 3.12 --all-extras
source .venv/bin/activate

# Validation commands (run frequently)
pyright --warnings                    # Full type checking
python scripts/validate_imports.py    # Import validation
ruff check src --select F821,F822    # Undefined names
python -m pytest tests/test_import.py # Import tests

# Development workflow
watchexec -e py python examples/active_test.py  # Auto-run on save
python discover_imports.py            # Find available classes

# Before committing
poe lint                             # All linting checks
poe test                            # Full test suite
python validate_references.py        # Comprehensive validation
```

## Summary of Key Rules

1. **Start Small**: Maximum 10 lines before first test
2. **Validate Imports**: Every import must be tested before use
3. **Use Loguru**: All exceptions must use logger.exception()
4. **Test Incrementally**: Run code every 2-3 changes
5. **Provide Context**: Every error must include debugging hints
6. **Clear Output**: Start test files with screen clear
7. **Progress Indicators**: Show visual progress (✅/❌)
8. **Memory First**: Always test with in-memory stores
9. **Discover Don't Assume**: Use discovery scripts for unknown imports
10. **Watchexec Friendly**: Design for continuous execution

## Critical Reminders

- **NEVER** write more than 20 lines without testing
- **NEVER** assume a class name - always verify
- **NEVER** skip import validation
- **ALWAYS** use logger.exception() in except blocks
- **ALWAYS** provide debug hints in errors
- **ALWAYS** test with minimal data first

## 11. Architecture Quality Tools

### Module Boundaries with Tach
```bash
# Before adding any cross-module import
tach check  # Verify no violations

# Initial setup for new modules
tach mod  # Interactive configuration
```

### Import Contracts
```ini
# .importlinter - Define and enforce rules
[contracts]
name = "No circular dependencies"
type = independence
modules = pyclarity.models, pyclarity.tools
```

### Naming Conventions
```bash
# Run before every commit
ruff check --select N  # PEP8 naming rules
```

### Live Documentation
```python
# For any non-standard library, check current docs
# 1. Local docs first
if exists("@docs/library-docs/{library}/"):
    read_local_docs()

# 2. Context7 MCP for live docs
lib_id = await context7.resolveLibraryId({"libraryName": "fastmcp"})
docs = await context7.getLibraryDocs({
    "context7CompatibleLibraryID": lib_id,
    "topic": "testing"
})
```