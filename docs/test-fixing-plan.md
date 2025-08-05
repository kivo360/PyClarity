# Test Import Error Fixing Plan

## 🎯 Objective
Fix all test import errors while ensuring tests validate intended behavior, not just pass syntactically.

## 📋 Current Known Issues

1. **test_mental_models.py**
   - Error: `ImportError: cannot import name 'MentalModelsContext' from 'pyclarity.tools.mental_models.models'`
   - Likely cause: Wrong import name or missing model

2. **Potential other test files** (need to scan)
   - Similar import errors may exist in other test files
   - Deprecated imports using old model names

## 🔍 Phase 1: Discovery & Analysis

### Step 1.1: Comprehensive Test Scan
```bash
# Find all test files with import errors
python -m pytest tests/ -v --tb=short | grep ImportError

# Run individual test files to identify specific errors
find tests/ -name "test_*.py" -exec python -m pytest {} -xvs \;
```

### Step 1.2: Import Verification
```python
# For each failing import, verify:
1. Check actual exports in source module
2. Compare test expectations vs. actual implementation
3. Document mismatches in import names
```

### Step 1.3: Behavior Mapping
Create a matrix mapping:
- Test file → What behavior it should validate
- Current test → Actual behavior being tested
- Gap analysis → Missing behavioral tests

## 🛠️ Phase 2: Fix Strategy

### Step 2.1: Import Resolution Patterns

**Pattern A: Wrong Import Name**
```python
# Before (test expects)
from pyclarity.tools.mental_models.models import MentalModelsContext

# After (actual export)
from pyclarity.tools.mental_models.models import MentalModelContext  # No 's'
```

**Pattern B: Missing Model**
```python
# If model doesn't exist, check:
1. Is it in a different module?
2. Was it renamed?
3. Should we create it?
```

**Pattern C: Structural Changes**
```python
# Model might have moved or been refactored
from pyclarity.tools.mental_models import MentalModelContext  # Direct import
```

### Step 2.2: Fix Priority Order
1. Fix imports that block the most tests
2. Fix imports for core functionality tests
3. Fix imports for integration tests
4. Fix imports for edge case tests

## 🧪 Phase 3: Behavior Validation Strategy

### 3.1: Test Quality Checks

**A. Semantic Test Validation**
```python
def validate_test_quality(test_function):
    """Ensure test validates behavior, not just syntax."""
    checks = {
        'has_assertions': True,  # Not just running code
        'tests_behavior': True,  # Validates outcomes
        'has_edge_cases': True,  # Tests boundaries
        'validates_contracts': True,  # Checks invariants
    }
    return all(checks.values())
```

**B. Behavior-Driven Test Pattern**
```python
def test_mental_model_analyzer_behavior():
    """Test WHAT the analyzer does, not HOW."""
    # GIVEN: A problem requiring first principles thinking
    context = MentalModelContext(
        problem="Why is the system slow?",
        model_type=MentalModelType.FIRST_PRINCIPLES
    )
    
    # WHEN: We analyze using the mental model
    result = analyzer.analyze(context)
    
    # THEN: We get fundamental decomposition
    assert result.contains_fundamental_truths()
    assert result.identifies_root_causes()
    assert not result.makes_assumptions()
```

### 3.2: Behavior Validation Techniques

**1. Property-Based Testing**
```python
# Test invariants that must always hold
@given(problem=text(), model_type=sampled_from(MentalModelType))
def test_analyzer_properties(problem, model_type):
    result = analyzer.analyze(MentalModelContext(problem, model_type))
    
    # Properties that must ALWAYS be true
    assert len(result.insights) > 0
    assert result.confidence_score between 0 and 1
    assert result.model_type == model_type
```

**2. Contract Testing**
```python
# Verify pre/post conditions
def test_analyzer_contracts():
    # Precondition: Valid input
    assert context.is_valid()
    
    result = analyzer.analyze(context)
    
    # Postcondition: Valid output
    assert result.satisfies_output_contract()
```

**3. Behavioral Scenarios**
```python
# Test specific behavioral scenarios
scenarios = [
    ("technical problem", "expects technical decomposition"),
    ("business problem", "expects business analysis"),
    ("ambiguous problem", "handles uncertainty gracefully"),
]
```

### 3.3: Anti-Pattern Detection

**Red Flags in Tests:**
1. ❌ Tests that only check for no exceptions
2. ❌ Tests that mock everything (no real behavior)
3. ❌ Tests that check implementation details
4. ❌ Tests without clear Given/When/Then structure

**Good Test Patterns:**
1. ✅ Tests that verify outcomes match expectations
2. ✅ Tests that check behavior under different conditions
3. ✅ Tests that validate business rules
4. ✅ Tests that ensure error handling works correctly

## 📊 Phase 4: Validation Metrics

### 4.1: Test Coverage Metrics
- **Import Coverage**: All imports resolve correctly
- **Behavior Coverage**: All documented behaviors have tests
- **Edge Case Coverage**: Boundary conditions tested
- **Error Path Coverage**: Failure modes tested

### 4.2: Quality Metrics
```python
# For each test file, measure:
quality_metrics = {
    'assertion_density': assertions_per_test,
    'behavior_focus': behavior_tests / total_tests,
    'edge_case_ratio': edge_tests / total_tests,
    'mock_usage': real_tests / mocked_tests,
}
```

## 🚀 Phase 5: Implementation Plan

### Day 1: Discovery
1. [ ] Run comprehensive test scan
2. [ ] Document all import errors
3. [ ] Create behavior mapping matrix
4. [ ] Identify fix patterns

### Day 2: Core Fixes
1. [ ] Fix mental_models test imports
2. [ ] Fix collaborative_reasoning test imports
3. [ ] Validate behavior coverage
4. [ ] Add missing behavior tests

### Day 3: Validation
1. [ ] Run full test suite
2. [ ] Measure quality metrics
3. [ ] Add integration tests
4. [ ] Document test patterns

## 🔒 Phase 6: Prevention Strategy

### 6.1: Import Validation CI Check
```yaml
# Add to CI pipeline
- name: Validate Test Imports
  run: |
    python -m pytest tests/ --collect-only
    python scripts/validate_test_behavior.py
```

### 6.2: Test Template
Create standard test template ensuring:
- Correct import patterns
- Behavior-focused structure
- Property validation
- Contract verification

### 6.3: Documentation
- Document common import patterns
- Create test writing guide
- Maintain import mapping reference

## ✅ Success Criteria

1. **All tests run successfully** (no import errors)
2. **Tests validate behavior**, not just syntax
3. **Clear Given/When/Then** structure in tests
4. **Comprehensive edge case** coverage
5. **Meaningful assertions** that check outcomes
6. **No test gaming** - tests can't be fooled by incorrect implementations

## 🎯 Expected Outcomes

- Zero import errors in test suite
- Increased confidence in code behavior
- Better documentation of expected behavior
- Foundation for BDD test generation
- Protection against AI gaming tests