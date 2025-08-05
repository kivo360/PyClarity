# Session Management Implementation Plan for PyClarity Tools

Based on the progressive sequential thinking implementation, here's a comprehensive plan to add session management to all remaining cognitive tools.

## Pattern Analysis from Sequential Thinking

The Sequential Thinking tool implements session management with:
1. **Progressive Analyzer** pattern with request/response models
2. **Base Store Classes** (BaseSessionStore, BaseThoughtStore)
3. **Tool-specific Data Models** (ThoughtData extends base patterns)
4. **Session lifecycle management** (create, update, retrieve)
5. **Branching and revision support**

## Implementation Plan by Tool

### 1. Mental Models Tool

**New Classes/Files:**
- `src/pyclarity/tools/mental_models/progressive_analyzer.py`
- `src/pyclarity/db/mental_model_store.py`

**Functions to Add:**
```python
# In progressive_analyzer.py
class ProgressiveMentalModelAnalyzer:
    def __init__(self, session_store: BaseSessionStore, model_store: BaseMentalModelStore)
    async def apply_model(self, request: ProgressiveMentalModelRequest) -> ProgressiveMentalModelResponse
    async def _ensure_session(self, session_id: str) -> SessionData
    async def _get_previous_applications(self, session_id: str) -> List[MentalModelData]
    async def _save_model_application(self, model_data: MentalModelData) -> MentalModelData

# In mental_model_store.py
class BaseMentalModelStore(ABC):
    async def save_model_application(self, model_data: MentalModelData) -> MentalModelData
    async def get_session_models(self, session_id: str) -> List[MentalModelData]
    async def get_model_by_type(self, session_id: str, model_type: str) -> Optional[MentalModelData]
    async def update_model_insights(self, model_id: int, insights: List[dict]) -> Optional[MentalModelData]
```

**Data Models:**
```python
class MentalModelData(BaseModel):
    id: Optional[int]
    session_id: str
    model_type: MentalModelType
    problem_statement: str
    insights: List[dict]
    recommendations: List[str]
    assumptions: List[dict]
    confidence_score: float
    created_at: datetime
```

### 2. Debugging Approaches Tool

**New Classes/Files:**
- `src/pyclarity/tools/debugging_approaches/progressive_analyzer.py`
- `src/pyclarity/db/debugging_store.py`

**Functions to Add:**
```python
# In progressive_analyzer.py
class ProgressiveDebuggingAnalyzer:
    def __init__(self, session_store: BaseSessionStore, debug_store: BaseDebuggingStore)
    async def analyze_issue(self, request: ProgressiveDebuggingRequest) -> ProgressiveDebuggingResponse
    async def add_hypothesis(self, session_id: str, hypothesis: DebuggingHypothesis) -> DebuggingData
    async def validate_hypothesis(self, session_id: str, hypothesis_id: int, validation_result: dict)
    async def get_debugging_history(self, session_id: str) -> List[DebuggingData]

# In debugging_store.py
class BaseDebuggingStore(ABC):
    async def save_debugging_step(self, debug_data: DebuggingData) -> DebuggingData
    async def get_session_steps(self, session_id: str) -> List[DebuggingData]
    async def get_hypotheses(self, session_id: str, status: Optional[str]) -> List[DebuggingHypothesis]
    async def update_hypothesis_status(self, hypothesis_id: int, status: str, evidence: dict)
```

**Data Models:**
```python
class DebuggingData(BaseModel):
    id: Optional[int]
    session_id: str
    step_number: int
    debugging_type: str  # systematic, rubber_duck, bisection, etc.
    hypothesis: Optional[DebuggingHypothesis]
    evidence_gathered: List[str]
    validation_result: Optional[dict]
    next_steps: List[str]
    confidence: float
    created_at: datetime
```

### 3. Collaborative Reasoning Tool

**New Classes/Files:**
- `src/pyclarity/tools/collaborative_reasoning/progressive_analyzer.py`
- `src/pyclarity/db/collaborative_store.py`

**Functions to Add:**
```python
# In progressive_analyzer.py
class ProgressiveCollaborativeAnalyzer:
    def __init__(self, session_store: BaseSessionStore, collab_store: BaseCollaborativeStore)
    async def add_perspective(self, request: CollaborativePerspectiveRequest) -> CollaborativePerspectiveResponse
    async def synthesize_perspectives(self, session_id: str) -> CollaborativeSynthesis
    async def resolve_conflict(self, session_id: str, conflict_id: int, resolution: dict)
    async def get_consensus_level(self, session_id: str) -> float

# In collaborative_store.py
class BaseCollaborativeStore(ABC):
    async def save_perspective(self, perspective_data: PerspectiveData) -> PerspectiveData
    async def get_session_perspectives(self, session_id: str) -> List[PerspectiveData]
    async def save_synthesis(self, synthesis: CollaborativeSynthesis) -> CollaborativeSynthesis
    async def get_conflicts(self, session_id: str, resolved: Optional[bool]) -> List[ConflictData]
```

**Data Models:**
```python
class PerspectiveData(BaseModel):
    id: Optional[int]
    session_id: str
    persona_name: str
    perspective_type: str  # technical, business, user, etc.
    viewpoint: str
    supporting_arguments: List[str]
    concerns: List[str]
    confidence: float
    conflicts_with: List[int]  # IDs of conflicting perspectives
    created_at: datetime
```

### 4. Decision Framework Tool

**New Classes/Files:**
- `src/pyclarity/tools/decision_framework/progressive_analyzer.py`
- `src/pyclarity/db/decision_store.py`

**Functions to Add:**
```python
# In progressive_analyzer.py
class ProgressiveDecisionAnalyzer:
    def __init__(self, session_store: BaseSessionStore, decision_store: BaseDecisionStore)
    async def analyze_decision(self, request: ProgressiveDecisionRequest) -> ProgressiveDecisionResponse
    async def add_criterion(self, session_id: str, criterion: DecisionCriterion) -> DecisionData
    async def evaluate_option(self, session_id: str, option_id: int, scores: dict)
    async def get_recommendation(self, session_id: str) -> DecisionRecommendation

# In decision_store.py (from provided example)
class BaseDecisionStore(BaseStore):
    async def add_decision(self, decision_data: DecisionData) -> DecisionData
    async def get_decision_sessions(self, analysis_type: str) -> List[DecisionData]
    async def search_decisions(self, keywords: str) -> List[DecisionData]
    async def get_decision_quality(self, decision_id: str) -> dict
    async def update_scores(self, decision_id: int, option_id: int, scores: dict)
```

**Data Models:**
```python
class DecisionData(BaseModel):
    id: Optional[int]
    session_id: str
    decision_statement: str
    analysis_type: str  # pros_cons, multi_criteria, etc.
    options: List[DecisionOption]
    criteria: List[DecisionCriterion]
    scores: Dict[str, Dict[str, float]]  # option_id -> criterion_id -> score
    recommendation: Optional[DecisionRecommendation]
    confidence: float
    created_at: datetime
```

### 5. Metacognitive Monitoring Tool

**New Classes/Files:**
- `src/pyclarity/tools/metacognitive_monitoring/progressive_analyzer.py`
- `src/pyclarity/db/metacognitive_store.py`

**Functions to Add:**
```python
# In progressive_analyzer.py
class ProgressiveMetacognitiveAnalyzer:
    def __init__(self, session_store: BaseSessionStore, meta_store: BaseMetacognitiveStore)
    async def monitor_thinking(self, request: MetacognitiveMonitorRequest) -> MetacognitiveMonitorResponse
    async def identify_bias(self, session_id: str, thinking_pattern: str) -> List[BiasIdentification]
    async def suggest_improvement(self, session_id: str) -> List[ImprovementSuggestion]
    async def track_progress(self, session_id: str) -> MetacognitiveProgress

# In metacognitive_store.py
class BaseMetacognitiveStore(ABC):
    async def save_monitoring_data(self, monitor_data: MetacognitiveData) -> MetacognitiveData
    async def get_session_monitoring(self, session_id: str) -> List[MetacognitiveData]
    async def get_biases_identified(self, session_id: str) -> List[BiasIdentification]
    async def track_improvement_metrics(self, session_id: str) -> dict
```

**Data Models:**
```python
class MetacognitiveData(BaseModel):
    id: Optional[int]
    session_id: str
    monitoring_type: str  # self_assessment, bias_check, quality_review
    thinking_pattern_observed: str
    biases_identified: List[BiasIdentification]
    quality_indicators: dict
    improvement_areas: List[str]
    confidence_in_assessment: float
    created_at: datetime
```

### 6. Scientific Method Tool

**New Classes/Files:**
- `src/pyclarity/tools/scientific_method/progressive_analyzer.py`
- `src/pyclarity/db/scientific_store.py`

**Functions to Add:**
```python
# In progressive_analyzer.py
class ProgressiveScientificAnalyzer:
    def __init__(self, session_store: BaseSessionStore, scientific_store: BaseScientificStore)
    async def formulate_hypothesis(self, request: HypothesisRequest) -> HypothesisResponse
    async def design_experiment(self, session_id: str, hypothesis_id: int) -> ExperimentDesign
    async def record_observation(self, session_id: str, experiment_id: int, observation: dict)
    async def analyze_results(self, session_id: str) -> ScientificConclusion

# In scientific_store.py
class BaseScientificStore(ABC):
    async def save_hypothesis(self, hypothesis_data: HypothesisData) -> HypothesisData
    async def save_experiment(self, experiment_data: ExperimentData) -> ExperimentData
    async def get_session_hypotheses(self, session_id: str) -> List[HypothesisData]
    async def get_experiment_results(self, experiment_id: int) -> ExperimentResults
```

**Data Models:**
```python
class HypothesisData(BaseModel):
    id: Optional[int]
    session_id: str
    hypothesis_statement: str
    variables: Dict[str, str]  # independent, dependent, controlled
    predictions: List[str]
    experiment_designs: List[ExperimentDesign]
    test_results: Optional[dict]
    confidence: float
    status: str  # proposed, testing, validated, refuted
    created_at: datetime
```

### 7. Visual Reasoning Tool

**New Classes/Files:**
- `src/pyclarity/tools/visual_reasoning/progressive_analyzer.py`
- `src/pyclarity/db/visual_store.py`

**Functions to Add:**
```python
# In progressive_analyzer.py
class ProgressiveVisualAnalyzer:
    def __init__(self, session_store: BaseSessionStore, visual_store: BaseVisualStore)
    async def create_diagram(self, request: DiagramRequest) -> DiagramResponse
    async def add_element(self, session_id: str, diagram_id: int, element: VisualElement)
    async def connect_elements(self, session_id: str, connection: ElementConnection)
    async def analyze_patterns(self, session_id: str) -> List[VisualPattern]

# In visual_store.py
class BaseVisualStore(ABC):
    async def save_diagram(self, diagram_data: DiagramData) -> DiagramData
    async def save_element(self, element_data: VisualElementData) -> VisualElementData
    async def get_session_diagrams(self, session_id: str) -> List[DiagramData]
    async def get_diagram_elements(self, diagram_id: int) -> List[VisualElementData]
```

**Data Models:**
```python
class DiagramData(BaseModel):
    id: Optional[int]
    session_id: str
    diagram_type: str  # flowchart, mind_map, sequence, etc.
    title: str
    elements: List[VisualElementData]
    connections: List[ElementConnection]
    patterns_identified: List[VisualPattern]
    insights: List[str]
    created_at: datetime
```

### 8. Creative Thinking Tool (if missing)

**New Classes/Files:**
- `src/pyclarity/tools/creative_thinking/analyzer.py`
- `src/pyclarity/tools/creative_thinking/progressive_analyzer.py`
- `src/pyclarity/db/creative_store.py`

**Functions to Add:**
```python
# In progressive_analyzer.py
class ProgressiveCreativeAnalyzer:
    def __init__(self, session_store: BaseSessionStore, creative_store: BaseCreativeStore)
    async def generate_idea(self, request: IdeaGenerationRequest) -> IdeaGenerationResponse
    async def combine_ideas(self, session_id: str, idea_ids: List[int]) -> CombinedIdea
    async def evaluate_creativity(self, session_id: str, idea_id: int) -> CreativityScore
    async def get_inspiration_sources(self, session_id: str) -> List[InspirationSource]
```

### 9. Systems Thinking Tool (if missing)

**New Classes/Files:**
- `src/pyclarity/tools/systems_thinking/analyzer.py`
- `src/pyclarity/tools/systems_thinking/progressive_analyzer.py`
- `src/pyclarity/db/systems_store.py`

**Functions to Add:**
```python
# In progressive_analyzer.py
class ProgressiveSystemsAnalyzer:
    def __init__(self, session_store: BaseSessionStore, systems_store: BaseSystemsStore)
    async def map_system(self, request: SystemMappingRequest) -> SystemMappingResponse
    async def identify_feedback_loops(self, session_id: str) -> List[FeedbackLoop]
    async def analyze_emergent_properties(self, session_id: str) -> List[EmergentProperty]
    async def simulate_intervention(self, session_id: str, intervention: SystemIntervention) -> SimulationResult
```

## Common Implementation Patterns

### 1. Progressive Request/Response Pattern
Each tool should implement:
- Request model with optional `session_id`
- Response model with session tracking
- Progressive analysis methods

### 2. Session Lifecycle
- Auto-generate session_id if not provided
- Ensure session exists before operations
- Update session timestamp on each operation

### 3. Store Interface Pattern
Each store should implement:
- `save_*` methods for creating data
- `get_session_*` methods for retrieval
- `update_*` methods for modifications
- `search_*` methods for querying

### 4. Error Handling
- Graceful handling of missing sessions
- Validation of session ownership
- Recovery from partial failures

## Implementation Order

1. **Phase 1**: Create base store classes in `src/pyclarity/db/`
2. **Phase 2**: Implement stores for each tool type
3. **Phase 3**: Add progressive analyzers to existing tools
4. **Phase 4**: Update MCP server to use progressive analyzers
5. **Phase 5**: Add tests for session management

## Testing Requirements

Each tool should have tests for:
- Session creation and retrieval
- Progressive analysis flow
- State persistence across calls
- Concurrent session handling
- Error recovery scenarios

This plan ensures consistent session management across all cognitive tools while maintaining the flexibility for tool-specific requirements.