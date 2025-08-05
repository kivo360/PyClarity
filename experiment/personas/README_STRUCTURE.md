# PyClarity Repository Structure Guide

## Repository Organization

```
PyClarity/
├── src/pyclarity/              # Main package (installed via pip/uv)
│   ├── __init__.py            # Exports all tools
│   ├── cli.py                 # CLI interface
│   ├── server/                # MCP server
│   └── tools/                 # 17 cognitive tools
│       ├── base.py           # Base classes
│       ├── collaborative_reasoning/
│       ├── decision_framework/
│       ├── mental_models/
│       └── ... (14 more tools)
│
├── tests/                     # Test suite
│   └── tools/                # Tool-specific tests
│
├── experiment/               # Experimental code
│   └── personas/            # Persona experiments
│
├── docs/                     # Documentation
├── pyproject.toml           # Project configuration
└── uv.lock                  # Dependency lock
```

## Import Patterns

### ✅ From Within src/pyclarity/
```python
# Internal imports use relative paths
from .tools.mental_models import MentalModelsAnalyzer
from .tools.base import CognitiveToolBase
```

### ✅ From Tests or External Code
```python
# External imports use absolute pyclarity paths
from pyclarity.tools.mental_models import MentalModelsAnalyzer
from pyclarity.tools.decision_framework import DecisionFrameworkAnalyzer
```

### ✅ From Experiments (Recommended Approaches)

#### Option 1: Install PyClarity in Development Mode
```bash
# From project root
uv pip install -e .
# or
pip install -e .
```

Then use normal imports:
```python
from pyclarity.tools.mental_models import MentalModelsAnalyzer
```

#### Option 2: Add to Python Path (for quick experiments)
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from pyclarity.tools.mental_models import MentalModelsAnalyzer
```

#### Option 3: Move Experiments Inside Package
```
src/pyclarity/experiments/personas/
```

### ❌ Common Import Mistakes

```python
# Don't use relative imports from outside the package
from ...src.pyclarity.tools import MentalModelsAnalyzer  # Won't work

# Don't assume current directory
from tools.mental_models import MentalModelsAnalyzer  # Fragile
```

## Why This Structure?

1. **Package Isolation**: `src/pyclarity` is a proper Python package
2. **Clean Imports**: Everything under `pyclarity.*` namespace
3. **Easy Testing**: Tests can import `pyclarity` directly
4. **Experiments**: Kept separate to avoid polluting main package
5. **Distribution**: Only `src/pyclarity` gets packaged for PyPI

## Best Practices for Experiments

1. **Create a virtual environment**
   ```bash
   uv venv
   source .venv/bin/activate
   ```

2. **Install PyClarity in development mode**
   ```bash
   uv pip install -e .
   ```

3. **Use absolute imports**
   ```python
   from pyclarity.tools.mental_models import MentalModelsAnalyzer
   ```

4. **Keep experiments organized**
   ```
   experiment/
   ├── personas/          # Persona-related experiments
   ├── benchmarks/        # Performance testing
   └── integrations/      # Integration experiments
   ```

## Module Discovery

PyClarity uses `__init__.py` files to make modules discoverable:

```python
# src/pyclarity/__init__.py exports everything
from .tools import (
    MentalModelsAnalyzer,
    DecisionFrameworkAnalyzer,
    # ... all other analyzers
)

# So users can do:
from pyclarity import MentalModelsAnalyzer
```

This is why `pyclarity.*` imports work from anywhere once the package is installed!