# PyClarity Development Guide

This guide outlines the development patterns, code structure, and conventions for contributing to the PyClarity cognitive tools library.

## Table of Contents
1. [Project Structure](#project-structure)
2. [Tool Development Patterns](#tool-development-patterns)
3. [Naming Conventions](#naming-conventions)
4. [Code Organization Rules](#code-organization-rules)
5. [Migration Guidelines](#migration-guidelines)
6. [Testing Standards](#testing-standards)
7. [Documentation Requirements](#documentation-requirements)

## Project Structure

### Directory Layout
```
src/pyclarity/
├── tools/                           # All cognitive tools
│   ├── sequential_thinking/         # Each tool in its own directory
│   │   ├── __init__.py             # Package exports
│   │   ├── models.py               # Pydantic data models
│   │   └── analyzer.py             # Core implementation
│   ├── metacognitive_monitoring/    # Another cognitive tool
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── analyzer.py
│   └── __init__.py                 # Main tools package exports
```

### Key Principles
1. **One Tool, One Directory**: Each cognitive tool gets its own dedicated directory
2. **Consistent Internal Structure**: Every tool follows the same file organization
3. **Clear Separation of Concerns**: Models separate from implementation logic
4. **Comprehensive Exports**: All public interfaces exported through `__init__.py`

## Tool Development Patterns

### Standard Tool Structure

Each cognitive tool MUST follow this structure:

#### 1. Models File (`models.py`)
```python
"""
{Tool Name} Models

Data structures for {tool description}, including
{key features and capabilities}.
"""

from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List, Dict, Any, Optional
from enum import Enum
from datetime import datetime
import uuid

# Enums first
class ComplexityLevel(str, Enum):
    """Problem complexity levels"""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    VERY_COMPLEX = "very_complex"

# Specific enums for the tool
class ToolSpecificEnum(str, Enum):
    # Tool-specific enumeration values
    pass

# Supporting models (building blocks)
class SupportingModel(BaseModel):
    """Description of what this model represents"""
    
    field_name: str = Field(
        ...,
        description="Clear description of the field",
        min_length=10,
        max_length=200
    )
    
    @field_validator('field_name')
    @classmethod
    def validate_field_name(cls, v):
        """Validate field is meaningful"""
        if not v or v.strip() == "":
            raise ValueError("Field cannot be empty")
        return v.strip()

# Main context/input model
class ToolNameContext(BaseModel):
    """Context for {tool name} analysis"""
    
    problem: str = Field(
        ...,
        description="The problem or question to analyze",
        min_length=10,
        max_length=2000
    )
    
    complexity_level: ComplexityLevel = Field(
        ComplexityLevel.MODERATE,
        description="Complexity level of the problem"
    )
    
    # Tool-specific configuration fields
    
    @model_validator(mode='after')
    def validate_consistency(self):
        """Validate consistency across fields"""
        # Cross-field validation logic
        return self

# Main result/output model
class ToolNameResult(BaseModel):
    """Result of {tool name} analysis"""
    
    # Core result fields
    
    processing_time_ms: int = Field(
        0,
        description="Time taken to process in milliseconds"
    )
    
    # Helper methods
    def get_summary(self) -> str:
        """Get a summary of the results"""
        pass
```

#### 2. Analyzer File (`analyzer.py`)
```python
"""
{Tool Name} Analyzer

Core implementation of the {tool name} cognitive tool, providing
{key capabilities and features}.
"""

from typing import List, Dict, Any, Optional
import asyncio
import time

from .models import (
    ToolNameContext,
    ToolNameResult,
    # Import all needed models
)


class ToolNameAnalyzer:
    """{Tool name} cognitive tool analyzer"""
    
    def __init__(self):
        """Initialize the {tool name} analyzer"""
        self.tool_name = "{Tool Name}"
        self.version = "1.0.0"
        
        # Internal state if needed
        self._processing_start_time = 0.0
    
    async def analyze(self, context: ToolNameContext) -> ToolNameResult:
        """
        Analyze {problem type} using {tool methodology}.
        
        Args:
            context: {Tool name} context with problem and parameters
            
        Returns:
            ToolNameResult with {key outputs}
        """
        self._processing_start_time = time.time()
        
        # Core processing logic
        # Break into smaller private methods
        
        # Calculate processing time
        processing_time = time.time() - self._processing_start_time
        
        return ToolNameResult(
            # Populate all required fields
            processing_time_ms=round(processing_time * 1000)
        )
    
    # Private helper methods
    async def _process_step(self, data: Any) -> Any:
        """Process a specific step"""
        pass
```

#### 3. Package Init File (`__init__.py`)
```python
"""
{Tool Name} Cognitive Tool

{Brief description of what this tool does and its key capabilities}.
"""

from .models import (
    # Export all enums first
    ComplexityLevel,
    ToolSpecificEnum,
    # Export all models
    SupportingModel,
    ToolNameContext,
    ToolNameResult,
)

from .analyzer import ToolNameAnalyzer

__all__ = [
    # Enums
    "ComplexityLevel",
    "ToolSpecificEnum",
    # Models
    "SupportingModel",
    "ToolNameContext", 
    "ToolNameResult",
    # Main class
    "ToolNameAnalyzer",
]
```

### Async Pattern Requirements

All analyzers MUST:
1. Use `async def analyze()` as the main entry point
2. Use `async def` for all internal methods that might do I/O
3. Return results wrapped in proper Pydantic models
4. Track processing time in milliseconds

### Error Handling Pattern

```python
async def analyze(self, context: ToolContext) -> ToolResult:
    """Main analysis method"""
    try:
        # Validate context first
        if not self._validate_context(context):
            raise ValueError("Invalid context provided")
        
        # Process
        result = await self._process(context)
        
        return result
        
    except Exception as e:
        # Log error appropriately
        # Return error result or re-raise
        raise
```

## Naming Conventions

### Tool Names
- **Keep Original Cognitive Names**: Sequential Thinking, Metacognitive Monitoring, etc.
- **No Abbreviations**: Use full, descriptive names
- **Cognitive Focus**: Names should reflect the cognitive process, not technical implementation

### File Names
- **Snake Case**: `sequential_thinking`, `metacognitive_monitoring`
- **Descriptive**: `models.py`, `analyzer.py` (not `core.py` or `main.py`)
- **Consistent**: Same file names across all tools

### Class Names
- **PascalCase**: `SequentialThinkingAnalyzer`, `MetacognitiveMonitoringContext`
- **Suffix Pattern**:
  - Analyzers: `{ToolName}Analyzer`
  - Contexts: `{ToolName}Context`
  - Results: `{ToolName}Result`

### Model Field Names
- **Snake Case**: `reasoning_chain`, `confidence_level`
- **Descriptive**: Avoid abbreviations
- **Consistent**: Use same field names across tools for similar concepts

## Code Organization Rules

### Model Organization

1. **Order of Definitions**:
   ```python
   # 1. Imports
   # 2. Constants
   # 3. Enums
   # 4. Supporting Models (smallest to largest)
   # 5. Main Context Model
   # 6. Main Result Model
   # 7. Utility classes/functions
   ```

2. **Field Definitions**:
   ```python
   field_name: Type = Field(
       default_value,  # or ... for required
       description="Clear description",
       # Constraints in logical order
       min_length=10,
       max_length=100,
       ge=0,
       le=1
   )
   ```

3. **Validation Pattern**:
   ```python
   @field_validator('field_name')
   @classmethod
   def validate_field_name(cls, v):
       """Validate field meets requirements"""
       # Validation logic
       return processed_value
   ```

### Analyzer Organization

1. **Method Order**:
   ```python
   class Analyzer:
       def __init__(self)
       async def analyze()  # Main public method
       # Private helper methods in logical order
       async def _step_one()
       async def _step_two()
       # Utility methods last
       def _calculate_metric()
   ```

2. **State Management**:
   - Use instance variables for processing state
   - Reset state at the beginning of `analyze()`
   - Don't leak state between analyze calls

### Import Organization

```python
"""
Module docstring
"""

# Standard library imports
from typing import List, Dict, Any, Optional
import asyncio
import time
from datetime import datetime
from enum import Enum

# Third-party imports
from pydantic import BaseModel, Field, field_validator

# Local imports
from .models import (
    ModelOne,
    ModelTwo,
)
```

## Migration Guidelines

When migrating tools from FastMCP to PyClarity:

### 1. Preserve Cognitive Identity
- **Keep Original Names**: Don't rename "Sequential Thinking" to "Step Processor"
- **Maintain Concepts**: Keep cognitive concepts like "bias detection", "mental models"
- **Preserve Descriptions**: Adapt descriptions but keep cognitive focus

### 2. Adapt Technical Patterns
```python
# FastMCP pattern
@mcp.tool()
async def tool_name(input: ToolInput) -> str:
    """Tool description."""
    # Implementation with Context logging
    
# PyClarity pattern
class ToolNameAnalyzer:
    async def analyze(self, context: ToolContext) -> ToolResult:
        """Tool description."""
        # Implementation with result model
```

### 3. Model Migration
- Convert FastMCP input models to PyClarity Context models
- Convert string outputs to structured Result models
- Preserve all validation logic
- Keep field descriptions and constraints

### 4. Remove FastMCP Dependencies
- Remove `@mcp.tool()` decorators
- Remove Context parameter from methods
- Remove progress reporting (or make it optional)
- Convert string returns to model returns

## Testing Standards

### Test Structure
```
tests/tools/
├── test_sequential_thinking.py
├── test_metacognitive_monitoring.py
└── fixtures/
    └── cognitive_fixtures.py
```

### Test Requirements
1. **Async Tests**: Use `pytest-asyncio`
2. **Model Validation**: Test all validators
3. **Edge Cases**: Test complexity boundaries
4. **Integration**: Test full analyze() flow

### Test Pattern
```python
import pytest
from pyclarity.tools.sequential_thinking import (
    SequentialThinkingAnalyzer,
    SequentialThinkingContext,
    ComplexityLevel,
)

@pytest.mark.asyncio
async def test_analyze_simple_problem():
    """Test analyzing a simple problem"""
    analyzer = SequentialThinkingAnalyzer()
    
    context = SequentialThinkingContext(
        problem="Test problem",
        complexity_level=ComplexityLevel.SIMPLE
    )
    
    result = await analyzer.analyze(context)
    
    assert result.reasoning_chain
    assert len(result.reasoning_chain) >= 3
    assert result.processing_time_ms > 0
```

## Documentation Requirements

### Module Docstrings
Every file must start with:
```python
"""
{Module Name}

{Description of what this module provides, its purpose,
and key capabilities. Should be 2-4 lines.}
"""
```

### Class Docstrings
```python
class ToolNameAnalyzer:
    """{Tool name} cognitive tool analyzer
    
    Provides {key capability 1}, {key capability 2}, and
    {key capability 3} for {problem domain}.
    """
```

### Method Docstrings
```python
async def analyze(self, context: ToolContext) -> ToolResult:
    """
    Analyze {problem type} using {methodology}.
    
    Args:
        context: {Tool name} context containing {key inputs}
        
    Returns:
        ToolResult containing {key outputs}
        
    Raises:
        ValueError: If context validation fails
    """
```

### Field Descriptions
Every Pydantic field MUST have a description:
```python
field_name: str = Field(
    ...,
    description="Clear, concise description of what this field represents"
)
```

## Best Practices

### 1. Cognitive Clarity
- Keep the cognitive purpose clear in all code
- Use domain language from cognitive science
- Avoid over-technical naming

### 2. Consistency
- Follow the same patterns across all tools
- Use consistent field names for similar concepts
- Maintain similar validation approaches

### 3. Modularity
- Each tool should be independent
- Shared concepts go in base models
- No cross-tool dependencies

### 4. Performance
- Use async for potential I/O operations
- Track processing time consistently
- Avoid blocking operations

### 5. Validation
- Validate early and clearly
- Provide helpful error messages
- Use Pydantic validators effectively

## Adding a New Tool

1. Create directory: `src/pyclarity/tools/{tool_name}/`
2. Create `__init__.py` with proper exports
3. Create `models.py` following the pattern
4. Create `analyzer.py` with async analyze method
5. Update `src/pyclarity/tools/__init__.py` to export the tool
6. Create tests in `tests/tools/test_{tool_name}.py`
7. Update documentation

## Code Review Checklist

- [ ] Follows directory structure pattern
- [ ] Uses consistent naming conventions
- [ ] Has complete model validation
- [ ] Implements async analyze() method
- [ ] Includes processing time tracking
- [ ] Has comprehensive docstrings
- [ ] Exports all public interfaces
- [ ] Includes field descriptions
- [ ] Follows import organization
- [ ] Preserves cognitive focus