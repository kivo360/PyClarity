# Reference Validation and Logging Rules for Python Development

## Overview

This document outlines best practices for validating Python references and using loguru for comprehensive error tracking. Based on research, the most effective tools for reference validation are:

1. **pyright/pylance** - Fast type checker with excellent undefined name detection
2. **mypy** - Comprehensive type checking with configurable strictness
3. **pyflakes** - Lightweight and fast for basic undefined name detection
4. **ruff** - Modern, fast linter written in Rust

## 1. Loguru Setup and Configuration

### Basic Setup
```python
# examples/active_test.py
from loguru import logger
import sys

# Configure loguru for watchexec development
logger.remove()  # Remove default handler
logger.add(
    sys.stderr,
    format="<green>{time:HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="DEBUG"
)

# For production, also log to file
logger.add(
    "logs/debug.log",
    rotation="10 MB",
    retention="1 week",
    level="DEBUG",
    backtrace=True,
    diagnose=True  # Include variable values in tracebacks
)
```

### Exception Handling Pattern
```python
def safe_import(module_path: str, class_name: str):
    """Import with comprehensive error logging"""
    logger.debug(f"Attempting import: from {module_path} import {class_name}")
    
    try:
        module = __import__(module_path, fromlist=[class_name])
        cls = getattr(module, class_name)
        logger.success(f"✅ Imported {class_name} from {module_path}")
        return cls
    except ImportError as e:
        logger.exception(e)  # This captures the full traceback
        logger.error(f"❌ Failed to import module: {module_path}")
        logger.error(f"   Looking for: {class_name}")
        
        # Provide helpful debugging info
        logger.info("🔍 Debug suggestions:")
        logger.info(f"   1. Check file exists: ls src/{module_path.replace('.', '/')}.py")
        logger.info(f"   2. Verify class name: grep '^class' src/{module_path.replace('.', '/')}.py")
        raise
    except AttributeError as e:
        logger.exception(e)
        logger.error(f"❌ Module {module_path} exists but doesn't contain {class_name}")
        
        # Show what's actually available
        available = [x for x in dir(module) if not x.startswith('_')]
        logger.info(f"📦 Available in {module_path}:")
        for item in available[:10]:
            logger.info(f"   - {item}")
        raise
```

## 2. Static Reference Validation

### Using pyright for Comprehensive Validation

Create `pyrightconfig.json` in project root:
```json
{
  "include": ["src", "examples", "tests"],
  "exclude": ["**/node_modules", "**/__pycache__", "venv", ".venv"],
  "reportMissingImports": true,
  "reportMissingTypeStubs": false,
  "reportUnusedImport": true,
  "reportUnusedVariable": true,
  "reportUndefinedVariable": true,
  "reportUnknownMemberType": true,
  "reportUnknownVariableType": true,
  "reportUnknownParameterType": true,
  "pythonVersion": "3.12",
  "pythonPlatform": "All",
  "typeCheckingMode": "strict",
  "useLibraryCodeForTypes": true
}
```

### Validation Script
```python
#!/usr/bin/env python3
"""
validate_references.py - Comprehensive reference validation
"""
import subprocess
import sys
from loguru import logger

def run_validation_tool(tool_name: str, command: list[str]) -> bool:
    """Run a validation tool and report results"""
    logger.info(f"🔍 Running {tool_name}...")
    
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            logger.success(f"✅ {tool_name}: No issues found")
            return True
        else:
            logger.error(f"❌ {tool_name}: Found issues")
            logger.error(result.stdout)
            if result.stderr:
                logger.error(result.stderr)
            return False
            
    except FileNotFoundError:
        logger.warning(f"⚠️  {tool_name} not installed")
        return True  # Don't fail if tool not available
    except Exception as e:
        logger.exception(e)
        return False

def validate_all_references():
    """Run all reference validation tools"""
    all_passed = True
    
    # 1. Pyright - Best for undefined names and imports
    if not run_validation_tool("pyright", ["pyright", "--warnings"]):
        all_passed = False
    
    # 2. Mypy - Good for type checking
    if not run_validation_tool("mypy", ["mypy", "src", "--strict", "--show-error-codes"]):
        all_passed = False
    
    # 3. Pyflakes - Fast basic checks
    if not run_validation_tool("pyflakes", ["pyflakes", "src", "examples"]):
        all_passed = False
    
    # 4. Ruff - Modern and fast
    if not run_validation_tool("ruff", ["ruff", "check", "src", "--select", "F821,F822,F401"]):
        # F821: undefined name
        # F822: undefined name in __all__
        # F401: imported but unused
        all_passed = False
    
    return all_passed

if __name__ == "__main__":
    logger.info("🚀 Starting reference validation")
    
    if validate_all_references():
        logger.success("✨ All reference validations passed!")
        sys.exit(0)
    else:
        logger.error("💥 Reference validation failed")
        sys.exit(1)
```

## 3. Runtime Reference Validation

### Import Validator Class
```python
from loguru import logger
import importlib
import inspect
from typing import Dict, List, Tuple, Any

class ImportValidator:
    """Validate imports and references at runtime"""
    
    def __init__(self):
        self.validated: Dict[str, bool] = {}
        self.errors: List[str] = []
    
    def validate_module_imports(self, module_path: str) -> bool:
        """Validate all imports in a module"""
        logger.info(f"🔍 Validating imports in {module_path}")
        
        try:
            module = importlib.import_module(module_path)
            logger.success(f"✅ Module {module_path} imports successfully")
            
            # Check all attributes
            for name in dir(module):
                if not name.startswith('_'):
                    try:
                        attr = getattr(module, name)
                        if inspect.isclass(attr) or inspect.isfunction(attr):
                            logger.debug(f"   ✓ {name}: {type(attr).__name__}")
                    except Exception as e:
                        logger.exception(e)
                        self.errors.append(f"{module_path}.{name}")
                        
            return len(self.errors) == 0
            
        except ImportError as e:
            logger.exception(e)
            logger.error(f"❌ Failed to import {module_path}")
            self.errors.append(module_path)
            return False
    
    def validate_import_chain(self, import_chain: List[Tuple[str, str]]) -> bool:
        """Validate a chain of imports"""
        logger.info("🔗 Validating import chain")
        
        for module_path, item_name in import_chain:
            try:
                module = importlib.import_module(module_path)
                if hasattr(module, item_name):
                    logger.success(f"✅ from {module_path} import {item_name}")
                else:
                    logger.error(f"❌ {item_name} not found in {module_path}")
                    self.errors.append(f"{module_path}.{item_name}")
            except ImportError as e:
                logger.exception(e)
                self.errors.append(module_path)
        
        return len(self.errors) == 0
```

## 4. Watchexec-Optimized Test Pattern

### Test File with Comprehensive Logging
```python
#!/usr/bin/env python3
"""
examples/test_with_validation.py - Test with full validation and logging
"""
import sys
import os
from datetime import datetime
from loguru import logger

# Configure logging
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="DEBUG"
)

# Add file logging for post-mortem analysis
logger.add(
    "logs/test_run_{time:YYYY-MM-DD}.log",
    rotation="1 day",
    retention="1 week",
    level="TRACE",
    backtrace=True,
    diagnose=True
)

# Clear screen for fresh run
print("\033[2J\033[H")
logger.info(f"🔄 Test run started at {datetime.now().strftime('%H:%M:%S')}")

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestRunner:
    """Run tests with comprehensive error tracking"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        
    @logger.catch(reraise=True)  # Decorator to catch and log any exception
    def test_imports(self):
        """Test all required imports"""
        logger.info("📦 Testing imports...")
        
        imports_to_test = [
            ("pyclarity.db.memory_stores", "MemorySessionStore"),
            ("pyclarity.db.memory_stores", "MemoryThoughtStore"),
            ("pyclarity.tools.sequential_thinking.progressive_analyzer", "ProgressiveSequentialThinkingAnalyzer"),
        ]
        
        for module_path, class_name in imports_to_test:
            try:
                logger.debug(f"Importing {class_name} from {module_path}")
                module = __import__(module_path, fromlist=[class_name])
                cls = getattr(module, class_name)
                logger.success(f"✅ {class_name}")
                self.passed += 1
            except Exception as e:
                logger.exception(e)
                logger.error(f"❌ Failed to import {class_name}")
                self.failed += 1
                
                # Detailed debugging info
                self._debug_import_failure(module_path, class_name)
    
    def _debug_import_failure(self, module_path: str, class_name: str):
        """Provide detailed debugging for import failures"""
        logger.info("🔍 Debugging import failure:")
        
        # Check if module file exists
        module_file = os.path.join("src", module_path.replace(".", "/") + ".py")
        if os.path.exists(module_file):
            logger.info(f"   ✓ Module file exists: {module_file}")
            
            # Try to read and search for class
            try:
                with open(module_file, 'r') as f:
                    content = f.read()
                    if f"class {class_name}" in content:
                        logger.info(f"   ✓ Class {class_name} found in file")
                    else:
                        logger.error(f"   ✗ Class {class_name} NOT found in file")
                        
                        # Find what classes are actually there
                        import re
                        classes = re.findall(r'^class\s+(\w+)', content, re.MULTILINE)
                        if classes:
                            logger.info(f"   📋 Available classes: {', '.join(classes)}")
            except Exception as e:
                logger.exception(e)
        else:
            logger.error(f"   ✗ Module file NOT found: {module_file}")
            
            # Check parent directory
            parent_dir = os.path.dirname(module_file)
            if os.path.exists(parent_dir):
                logger.info(f"   📁 Files in {parent_dir}:")
                for file in os.listdir(parent_dir)[:10]:
                    logger.info(f"      - {file}")
    
    def run_all_tests(self):
        """Run all tests and report results"""
        logger.info("🚀 Starting all tests")
        
        self.test_imports()
        # Add more test methods here
        
        # Summary
        total = self.passed + self.failed
        logger.info("="*50)
        logger.info(f"📊 Test Summary: {self.passed}/{total} passed")
        
        if self.failed > 0:
            logger.error(f"❌ {self.failed} tests failed")
            return False
        else:
            logger.success("✅ All tests passed!")
            return True

if __name__ == "__main__":
    runner = TestRunner()
    
    try:
        success = runner.run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.warning("⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.exception(e)
        logger.critical("💥 Unexpected error in test runner")
        sys.exit(1)
```

## 5. Pre-commit Validation Hook

### .pre-commit-config.yaml
```yaml
repos:
  - repo: https://github.com/microsoft/pyright
    rev: v1.1.350
    hooks:
      - id: pyright
        name: pyright reference validation
        entry: pyright
        language: node
        types: [python]
        args: ["--warnings"]
        
  - repo: https://github.com/PyCQA/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
        args: ['--select=F821,F822,F401', '--ignore=E501']
        # Only check for undefined names and unused imports
```

## 6. VSCode Integration

### .vscode/settings.json
```json
{
    "python.analysis.typeCheckingMode": "strict",
    "python.analysis.autoImportCompletions": true,
    "python.analysis.diagnosticMode": "workspace",
    "python.analysis.inlayHints.functionReturnTypes": true,
    "python.analysis.inlayHints.variableTypes": true,
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "python.linting.flake8Args": [
        "--select=F821,F822,F401",
        "--ignore=E501"
    ],
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false
}
```

## 7. Continuous Validation Script for Watchexec

### watch_validate.py
```python
#!/usr/bin/env python3
"""
Run continuous validation - perfect companion for watchexec
"""
from loguru import logger
import subprocess
import time

# Configure for continuous output
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:HH:mm:ss}</green> | <level>{message}</level>",
    level="INFO"
)

def quick_validate():
    """Quick validation that runs on every file save"""
    start = time.time()
    
    # Run pyflakes (fastest)
    result = subprocess.run(
        ["pyflakes", "src", "examples"],
        capture_output=True,
        text=True
    )
    
    elapsed = time.time() - start
    
    if result.returncode == 0:
        logger.success(f"✅ No undefined references ({elapsed:.2f}s)")
    else:
        logger.error("❌ Found undefined references:")
        for line in result.stdout.splitlines():
            logger.error(f"   {line}")
    
    return result.returncode == 0

if __name__ == "__main__":
    quick_validate()
```

## Usage with watchexec

```bash
# Terminal 1: Run tests on save
watchexec -e py python examples/test_with_validation.py

# Terminal 2: Run quick validation on save
watchexec -e py python watch_validate.py

# Terminal 3: Run full validation periodically
watch -n 30 python validate_references.py
```

## Key Benefits

1. **Immediate Feedback**: Errors show exact file, function, and line number
2. **Full Tracebacks**: logger.exception() captures complete stack traces
3. **Contextual Information**: Variable values included in error logs
4. **Static + Runtime**: Catches errors before and during execution
5. **Progressive Validation**: Quick checks on every save, deep checks periodically
6. **Historical Data**: Log files for post-mortem analysis

## Summary

This approach combines:
- **loguru** for comprehensive runtime error tracking with exact locations
- **pyright/mypy** for static validation of undefined names and imports
- **watchexec-friendly** patterns for continuous feedback
- **Progressive validation** from fast (pyflakes) to comprehensive (pyright --strict)