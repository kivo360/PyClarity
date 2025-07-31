# PyClarity Tool Abstraction Levels Guide

## Overview

This guide defines the abstraction levels for PyClarity tools, helping developers understand where their code fits in the architecture and how to properly structure new tools.

## Abstraction Pyramid

```
┌─────────────────────────────────┐
│   Level 1: Business Tools       │  User-facing, complete solutions
├─────────────────────────────────┤
│   Level 2: Domain Engines       │  Core processing components  
├─────────────────────────────────┤
│   Level 3: Technical Services   │  Shared capabilities
├─────────────────────────────────┤
│   Level 4: Infrastructure       │  Foundation utilities
└─────────────────────────────────┘
```

## Level 1: Business Tools (User-Facing)

### Definition
Complete, autonomous tools that deliver direct business value. These are the primary interfaces users interact with.

### Characteristics
- **Complete Solutions**: Solve entire business problems
- **Self-Contained**: Include all necessary components
- **Business Language**: Use domain terminology
- **High-Level API**: Simple request/response models
- **Value-Oriented**: Clear ROI and outcomes

### Structure Pattern
```python
class [BusinessDomain][ValueProposition]:
    """High-level tool delivering complete business value."""
    
    async def [primary_action](self, context: BusinessContext) -> BusinessResult:
        """Main entry point with business-oriented parameters."""
        # Orchestrates multiple components
        # Returns comprehensive results
```

### Examples
```python
# Strategic Decision Making
class StrategicDecisionAccelerator:
    async def accelerate_strategic_decision(self, context: DecisionContext) -> StrategicDecisionResult:
        pass

# Journey Management  
class JourneyOrchestrationIntelligence:
    async def orchestrate_journey(self, journey: JourneyContext) -> JourneyOrchestrationResult:
        pass

# Project Health
class ProjectHealthDiagnostic:
    async def diagnose_project_health(self, project: ProjectContext) -> HealthDiagnosticResult:
        pass
```

### Naming Rules
- Start with business domain (Strategic, Project, Team)
- Include value proposition (Accelerator, Optimizer, Intelligence)
- End with tool type (Diagnostic, Framework, System)

## Level 2: Domain Engines (Core Components)

### Definition
Specialized components that handle specific aspects of a business tool. These are the "engines" that power the tools.

### Characteristics
- **Domain Experts**: Deep expertise in specific area
- **Reusable**: Can be used by multiple tools
- **Focused**: Single responsibility principle
- **Stateless**: No persistent state between calls
- **Composable**: Work well with other engines

### Structure Pattern
```python
class [SpecificFunction][EngineType]:
    """Specialized engine for specific domain logic."""
    
    async def [core_action](self, input_data: DomainModel) -> DomainResult:
        """Focused processing method."""
        # Implements specific algorithm
        # Returns focused results
```

### Examples
```python
# Decision Components
class DecisionCrystallizer:
    async def crystallize_decision(self, context: DecisionContext) -> DecisionCrystallization:
        pass

class ScenarioModeler:
    async def model_scenarios(self, context: DecisionContext) -> ScenarioModeling:
        pass

# Journey Components
class JourneyDecomposer:
    async def decompose_journey(self, journey: Journey) -> DecomposedJourney:
        pass

class MomentumAnalyzer:
    async def analyze_momentum(self, metrics: JourneyMetrics) -> MomentumAnalysis:
        pass
```

### Naming Rules
- Action-oriented (Crystallizer, Modeler, Analyzer)
- Specific function (Decision, Scenario, Journey)
- Consistent suffixes (-er, -or, -izer, -ator)

## Level 3: Technical Services (Shared Capabilities)

### Definition
Technical services that provide common functionality across multiple domain engines.

### Characteristics
- **Technical Focus**: Implementation-specific
- **Highly Reusable**: Used across domains
- **Performance-Oriented**: Optimized for efficiency
- **Well-Tested**: High test coverage
- **Stable APIs**: Rarely change

### Structure Pattern
```python
class [TechnicalCapability]Service:
    """Technical service providing shared capability."""
    
    async def [technical_operation](self, params: TechnicalParams) -> TechnicalResult:
        """Performs specific technical operation."""
        # Implements technical algorithm
        # Returns technical results
```

### Examples
```python
# Analysis Services
class MonteCarloSimulationService:
    async def run_simulation(self, parameters: SimulationParams) -> SimulationResults:
        pass

class SentimentAnalysisService:
    async def analyze_sentiment(self, text: str) -> SentimentScore:
        pass

# Data Services
class TimeSeriesAnalysisService:
    async def analyze_trends(self, data: TimeSeriesData) -> TrendAnalysis:
        pass

class GraphAnalysisService:
    async def analyze_network(self, graph: NetworkGraph) -> NetworkMetrics:
        pass
```

### Naming Rules
- Technical terminology acceptable
- Service suffix for clarity
- Implementation-specific names OK
- Focus on capability, not domain

## Level 4: Infrastructure (Foundation Utilities)

### Definition
Low-level utilities and infrastructure that support all higher levels.

### Characteristics
- **Pure Functions**: No side effects
- **Highly Optimized**: Performance critical
- **Generic**: Domain-agnostic
- **Minimal Dependencies**: Self-contained
- **Extensively Tested**: Edge cases covered

### Structure Pattern
```python
def [operation]_[target]_[qualifier](input: BaseType) -> BaseType:
    """Pure function for specific operation."""
    # Implements algorithm
    # Returns transformed result

class [Infrastructure]Utility:
    """Utility class for infrastructure needs."""
    
    @staticmethod
    def [utility_method](param: BaseType) -> BaseType:
        """Static utility method."""
        pass
```

### Examples
```python
# Calculation Utilities
def calculate_weighted_score(scores: Dict[str, float], weights: Dict[str, float]) -> float:
    pass

def normalize_distribution(values: List[float]) -> List[float]:
    pass

# Data Utilities
class DataTransformer:
    @staticmethod
    def flatten_nested_dict(nested: Dict[str, Any]) -> Dict[str, Any]:
        pass

# Time Utilities
class TimeWindowCalculator:
    @staticmethod
    def calculate_time_windows(start: datetime, end: datetime, window_size: timedelta) -> List[TimeWindow]:
        pass
```

### Naming Rules
- Function names: verb_object_qualifier
- Utility classes: [Purpose]Utility or [Purpose]Helper
- Clear, technical names
- No business domain language

## Cross-Level Guidelines

### Dependency Rules
```
Level 1 → Level 2 → Level 3 → Level 4
  ↓         ↓         ↓         ↓
Business → Domain → Technical → Pure
```

- Higher levels can depend on lower levels
- Lower levels should NOT depend on higher levels
- Same-level dependencies should be minimal
- Circular dependencies are forbidden

### Data Flow Patterns

#### Top-Down Request Flow
```python
# Level 1: Business Tool
result = await accelerator.accelerate_decision(business_context)
    ↓
# Level 2: Domain Engine  
crystallization = await crystallizer.crystallize(domain_context)
    ↓
# Level 3: Technical Service
simulation = await monte_carlo.simulate(parameters)
    ↓
# Level 4: Infrastructure
score = calculate_weighted_score(values, weights)
```

#### Bottom-Up Result Flow
```python
# Level 4: Pure calculation
score = 8.5
    ↑
# Level 3: Technical result
SimulationResult(score=score, confidence=0.9)
    ↑
# Level 2: Domain result  
DecisionCrystallization(readiness=score, state="ready")
    ↑
# Level 1: Business result
StrategicDecisionResult(recommendation="proceed", confidence="high")
```

### Interface Design by Level

#### Level 1 Interfaces (Business)
```python
@dataclass
class BusinessRequest:
    business_context: str
    stakeholders: List[str]
    constraints: List[str]
    timeline: str

@dataclass  
class BusinessResult:
    recommendation: str
    confidence: str
    next_steps: List[str]
    executive_summary: str
```

#### Level 2 Interfaces (Domain)
```python
@dataclass
class DomainInput:
    entities: List[DomainEntity]
    relationships: List[Relationship]
    rules: List[DomainRule]

@dataclass
class DomainOutput:
    analysis: DomainAnalysis
    metrics: DomainMetrics
    insights: List[DomainInsight]
```

#### Level 3 Interfaces (Technical)
```python
@dataclass
class TechnicalParams:
    algorithm: str
    parameters: Dict[str, float]
    options: TechnicalOptions

@dataclass
class TechnicalResult:
    values: np.ndarray
    statistics: Statistics
    metadata: Dict[str, Any]
```

#### Level 4 Interfaces (Infrastructure)
```python
# Simple types preferred
def utility_function(
    data: List[float],
    param: float
) -> float:
    pass

# Or basic dataclasses
@dataclass
class Point:
    x: float
    y: float
```

## Abstraction Level Decision Tree

```
Is this user-facing and complete?
├─ Yes → Level 1: Business Tool
└─ No → Does it implement domain logic?
    ├─ Yes → Level 2: Domain Engine
    └─ No → Is it a reusable technical service?
        ├─ Yes → Level 3: Technical Service
        └─ No → Level 4: Infrastructure Utility
```

## Examples of Proper Abstraction

### Good Abstraction ✅
```python
# Level 1: Clear business value
class StrategicDecisionAccelerator:
    def __init__(self):
        # Uses Level 2 components
        self.crystallizer = DecisionCrystallizer()
        self.modeler = ScenarioModeler()

# Level 2: Domain-specific logic
class DecisionCrystallizer:
    def __init__(self):
        # Uses Level 3 services
        self.analyzer = ComplexityAnalysisService()

# Level 3: Technical capability  
class ComplexityAnalysisService:
    def analyze(self, data):
        # Uses Level 4 utilities
        return calculate_complexity_score(data)

# Level 4: Pure function
def calculate_complexity_score(factors: List[float]) -> float:
    return sum(factors) / len(factors)
```

### Poor Abstraction ❌
```python
# Bad: Mixes abstraction levels
class DecisionMaker:  # Vague name
    def make_decision(self, sql_query):  # Technical in business tool
        db_results = self.execute_sql(sql_query)  # Infrastructure in business
        return "good" if db_results else "bad"  # Poor abstraction

# Bad: Circular dependency
class BusinessTool:
    def __init__(self, infra_util):
        self.util = infra_util
        infra_util.business_tool = self  # Infrastructure depends on business!
```

## Testing Strategy by Level

### Level 1: Integration Tests
- Test complete workflows
- Mock external dependencies
- Focus on business outcomes
- Use realistic scenarios

### Level 2: Unit Tests  
- Test domain logic
- Mock Level 3 services
- Focus on correctness
- Cover edge cases

### Level 3: Performance Tests
- Test efficiency
- Benchmark algorithms
- Mock Level 4 calls
- Measure resource usage

### Level 4: Property Tests
- Test mathematical properties
- Use property-based testing
- Focus on correctness proofs
- Test edge cases extensively

## Migration Guide

### Moving Between Levels

#### Promoting to Higher Level
When infrastructure becomes domain-specific:
```python
# Before (Level 4)
def calculate_score(values: List[float]) -> float:
    return sum(values) / len(values)

# After (Level 3)  
class DecisionScoringService:
    def score_decision(self, decision: Decision) -> DecisionScore:
        # Domain-aware scoring
        base_score = sum(decision.values) / len(decision.values)
        return DecisionScore(
            value=base_score,
            confidence=self._calculate_confidence(decision)
        )
```

#### Extracting to Lower Level
When domain logic becomes generic:
```python
# Before (Level 2)
class JourneyAnalyzer:
    def calculate_momentum(self, velocities):
        # Generic calculation
        return sum(v * w for v, w in zip(velocities, weights))

# After (Level 4)
def calculate_weighted_sum(values: List[float], weights: List[float]) -> float:
    return sum(v * w for v, w in zip(values, weights))
```

## Conclusion

Proper abstraction levels ensure:
- Clear separation of concerns
- Appropriate reusability
- Maintainable architecture
- Testable components
- Scalable design

Always consider the abstraction level when:
- Creating new components
- Refactoring existing code
- Designing interfaces
- Planning dependencies
- Writing tests