# Test Behavior Validation Strategy

## 🎭 The Problem: Tests That Lie

AI agents (and developers) can make tests pass without implementing correct behavior. This document outlines strategies to ensure tests validate **intended behavior**, not just syntactic correctness.

## 🔍 Behavior Validation Techniques

### 1. **Triangulation Testing**
Test the same behavior from multiple angles to ensure consistency.

```python
def test_mental_model_triangulation():
    """Validate first principles from multiple perspectives."""
    problem = "System performance is degrading"
    
    # Approach 1: Direct analysis
    result1 = analyzer.analyze(MentalModelContext(
        problem=problem,
        model_type=MentalModelType.FIRST_PRINCIPLES
    ))
    
    # Approach 2: Step-by-step breakdown
    components = analyzer.decompose_to_fundamentals(problem)
    result2 = analyzer.reconstruct_from_components(components)
    
    # Approach 3: Constraint validation
    result3 = analyzer.analyze_with_constraints(
        problem=problem,
        constraints=["must identify root cause", "no assumptions"]
    )
    
    # All approaches should converge on same fundamental truths
    assert result1.root_causes == result2.root_causes == result3.root_causes
```

### 2. **Metamorphic Testing**
Test relationships between inputs and outputs that must hold.

```python
def test_metamorphic_relations():
    """Test properties that must hold across transformations."""
    
    # Property 1: Adding detail shouldn't change fundamental analysis
    simple = "System is slow"
    detailed = "System is slow during peak hours with high user load"
    
    result_simple = analyzer.analyze(simple)
    result_detailed = analyzer.analyze(detailed)
    
    # Core insights should be consistent
    assert set(result_simple.core_insights).issubset(result_detailed.core_insights)
    
    # Property 2: Inverse operations
    original = "Complex nested problem"
    decomposed = analyzer.decompose(original)
    recomposed = analyzer.recompose(decomposed)
    
    assert analyzer.semantic_similarity(original, recomposed) > 0.9
```

### 3. **Invariant Testing**
Identify properties that must ALWAYS be true.

```python
class AnalyzerInvariants:
    """Invariants that must hold for ANY valid analysis."""
    
    @staticmethod
    def confidence_bounds(result):
        """Confidence must be in valid range."""
        return 0.0 <= result.confidence_score <= 1.0
    
    @staticmethod
    def non_empty_insights(result):
        """Analysis must produce insights."""
        return len(result.insights) > 0
    
    @staticmethod
    def model_consistency(result, context):
        """Result must match requested model type."""
        return result.model_type == context.model_type
    
    @staticmethod
    def temporal_consistency(result):
        """Timestamps must be logical."""
        return result.started_at <= result.completed_at

def test_invariants_hold():
    """Test that ALL invariants hold for ANY input."""
    # Generate random test cases
    for _ in range(100):
        context = generate_random_context()
        result = analyzer.analyze(context)
        
        # Check all invariants
        assert AnalyzerInvariants.confidence_bounds(result)
        assert AnalyzerInvariants.non_empty_insights(result)
        assert AnalyzerInvariants.model_consistency(result, context)
        assert AnalyzerInvariants.temporal_consistency(result)
```

### 4. **Behavioral Mutation Testing**
Verify tests catch incorrect implementations.

```python
def test_detects_incorrect_behavior():
    """Ensure test fails with wrong implementation."""
    
    # Create intentionally broken analyzer
    class BrokenAnalyzer:
        def analyze(self, context):
            # Always returns same result (wrong!)
            return MentalModelResult(
                insights=["Generic insight"],
                confidence_score=0.5
            )
    
    broken = BrokenAnalyzer()
    
    # Our test should detect this is wrong
    with pytest.raises(AssertionError):
        validate_analyzer_behavior(broken)
```

### 5. **Contract-Based Testing**
Define and verify contracts between components.

```python
class AnalyzerContract:
    """Formal contract for analyzer behavior."""
    
    @precondition
    def valid_input(self, context):
        assert context.problem is not None
        assert context.model_type in MentalModelType
        assert len(context.problem) > 0
    
    @postcondition
    def valid_output(self, result, context):
        assert result is not None
        assert result.model_type == context.model_type
        assert len(result.insights) >= 1
        assert all(len(insight) > 0 for insight in result.insights)
    
    @invariant
    def consistency(self, analyzer):
        # Same input should give similar results
        context = MentalModelContext("Test problem", MentalModelType.FIRST_PRINCIPLES)
        result1 = analyzer.analyze(context)
        result2 = analyzer.analyze(context)
        assert similarity(result1, result2) > 0.9
```

### 6. **Semantic Behavior Testing**
Test meaning, not just structure.

```python
def test_semantic_behavior():
    """Test that output has correct meaning."""
    
    # Test first principles actually breaks down to fundamentals
    result = analyzer.analyze(MentalModelContext(
        problem="Website loads slowly",
        model_type=MentalModelType.FIRST_PRINCIPLES
    ))
    
    # Semantic checks
    fundamentals = extract_fundamentals(result.insights)
    assert "network latency" in fundamentals or "server processing" in fundamentals
    assert "data transfer" in fundamentals or "computational complexity" in fundamentals
    
    # Should NOT contain high-level assumptions
    assert "user experience" not in fundamentals
    assert "business impact" not in fundamentals
```

### 7. **Oracle Testing**
Compare against known good results.

```python
class TestOracles:
    """Known good results for comparison."""
    
    FIRST_PRINCIPLES_ORACLE = {
        "slow system": {
            "must_contain": ["hardware", "software", "network"],
            "must_decompose_to": ["CPU", "memory", "I/O", "algorithms"],
            "abstraction_level": "fundamental"
        }
    }
    
    def validate_against_oracle(self, problem, result):
        oracle = self.FIRST_PRINCIPLES_ORACLE.get(problem.lower())
        if oracle:
            # Check required elements
            insights_text = " ".join(result.insights).lower()
            for required in oracle["must_contain"]:
                assert required in insights_text
```

### 8. **Differential Testing**
Compare multiple implementations.

```python
def test_differential_behavior():
    """Compare against reference implementation."""
    
    # Our implementation
    our_result = our_analyzer.analyze(context)
    
    # Reference implementation (could be simple but correct)
    reference_result = reference_analyzer.analyze(context)
    
    # Results should be semantically equivalent
    assert semantic_similarity(our_result, reference_result) > 0.85
    
    # But our implementation might be more detailed
    assert len(our_result.insights) >= len(reference_result.insights)
```

## 🛡️ Defense Against Test Gaming

### 1. **Randomized Test Cases**
```python
@given(
    problem=text(min_size=10, max_size=200),
    model_type=sampled_from(MentalModelType)
)
def test_random_inputs(problem, model_type):
    """Prevent hardcoded responses."""
    result = analyzer.analyze(MentalModelContext(problem, model_type))
    
    # Result should be specific to input
    assert problem.split()[0] in str(result.insights)
    assert len(set(result.insights)) > 1  # Not all same
```

### 2. **Time-Based Validation**
```python
def test_processing_time_realistic():
    """Ensure actual processing happens."""
    start = time.time()
    result = analyzer.analyze(complex_context)
    duration = time.time() - start
    
    # Should take some minimum time for real analysis
    assert duration > 0.01  # Not just returning cached/hardcoded
    assert duration < 5.0   # Not hanging
```

### 3. **State Independence**
```python
def test_no_hidden_state():
    """Ensure analyzer doesn't 'remember' test patterns."""
    results = []
    for i in range(10):
        result = analyzer.analyze(MentalModelContext(
            f"Problem variation {i}",
            MentalModelType.FIRST_PRINCIPLES
        ))
        results.append(result)
    
    # Each result should be independent
    for i in range(1, 10):
        assert results[i].insights != results[i-1].insights
```

## 📊 Behavior Coverage Metrics

### 1. **Behavior Coverage Matrix**
```python
BEHAVIOR_MATRIX = {
    "MentalModelAnalyzer": {
        "first_principles": [
            "decomposes_to_fundamentals",
            "identifies_base_constraints", 
            "removes_assumptions",
            "builds_from_basics"
        ],
        "opportunity_cost": [
            "identifies_alternatives",
            "quantifies_tradeoffs",
            "ranks_options",
            "calculates_foregone_value"
        ]
    }
}

def measure_behavior_coverage(test_suite):
    """Calculate what percentage of behaviors are tested."""
    tested_behaviors = extract_tested_behaviors(test_suite)
    total_behaviors = count_all_behaviors(BEHAVIOR_MATRIX)
    return len(tested_behaviors) / total_behaviors
```

### 2. **Assertion Quality Score**
```python
def score_assertion_quality(test_function):
    """Rate the quality of assertions in a test."""
    assertions = extract_assertions(test_function)
    
    score = 0
    for assertion in assertions:
        if is_behavioral_assertion(assertion):
            score += 2  # Checks behavior
        elif is_semantic_assertion(assertion):
            score += 1.5  # Checks meaning
        elif is_structural_assertion(assertion):
            score += 1  # Checks structure
        elif is_existence_assertion(assertion):
            score += 0.5  # Just checks not None
    
    return score / len(assertions)
```

## 🚨 Red Flags in Tests

### Tests to Refactor:
1. **Tests without assertions** - Just running code
2. **Tests that only check types** - `assert isinstance(result, dict)`
3. **Tests with only positive cases** - No error handling
4. **Tests that mock core behavior** - Testing mocks, not code
5. **Tests with hardcoded expectations** - Brittle and gameable

### Good Test Patterns:
1. **Tests with semantic assertions** - Check meaning
2. **Tests with multiple angles** - Triangulation
3. **Tests with invariant checking** - Universal truths
4. **Tests with error cases** - Negative testing
5. **Tests with property validation** - Mathematical properties

## 🎯 Implementation Checklist

For each test being fixed:

- [ ] Verify it tests behavior, not implementation
- [ ] Add semantic assertions
- [ ] Include negative test cases  
- [ ] Check invariants hold
- [ ] Validate against oracles/examples
- [ ] Ensure it catches wrong implementations
- [ ] Add property-based test cases
- [ ] Document expected behavior clearly