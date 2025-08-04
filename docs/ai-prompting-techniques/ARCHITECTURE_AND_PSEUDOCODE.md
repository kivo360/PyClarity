# AI Prompting Techniques: Architecture and Pseudocode

This document provides the complete architecture and pseudocode for implementing the combined AI prompting techniques system. No implementation details - just structure and logic flow.

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     Orchestrator Agent                           │
│                    (Temperature: 0.3)                            │
│  - Manages overall workflow                                      │
│  - Coordinates specialist agents                                 │
│  - Validates final outputs                                       │
└──────────────────────────┬──────────────────────────────────────┘
                           │
       ┌───────────────────┴───────────────────┐
       │                                       │
       ▼                                       ▼
┌──────────────────────┐            ┌──────────────────────┐
│  Rewriter Agent      │            │  Generator Agent     │
│  (Temperature: 0.7)  │            │  (Temperature: 0.9)  │
│  - Refines prompts   │            │  - Creates designs   │
│  - Evaluates quality │            │  - Visual reasoning  │
└──────────────────────┘            └──────┬───────────────┘
                                           │
                                           ▼
                                 ┌──────────────────────┐
                                 │   Voter Agent        │
                                 │  (Temperature: 0.2)  │
                                 │  - Analyzes chains   │
                                 │  - Applies voting    │
                                 └──────────────────────┘
```

## Agent Definitions

### 1. Orchestrator Agent (Temperature: 0.3)
**Purpose**: Main coordinator ensuring workflow consistency
**Characteristics**: 
- Low temperature for reliable orchestration
- Manages state between agents
- Handles error recovery

### 2. Rewriter Agent (Temperature: 0.7)
**Purpose**: Creative prompt refinement
**Characteristics**:
- Medium temperature for balanced creativity
- Identifies prompt weaknesses
- Suggests improvements

### 3. Generator Agent (Temperature: 0.9)
**Purpose**: Diverse design generation
**Characteristics**:
- High temperature for creative diversity
- Generates unique approaches
- Explores design space

### 4. Voter Agent (Temperature: 0.2)
**Purpose**: Analytical consensus building
**Characteristics**:
- Very low temperature for consistency
- Objective analysis
- Deterministic voting

## Pseudocode Structure

```python
# ============================================================
# MAIN ORCHESTRATOR
# ============================================================

class AIPromptingOrchestrator:
    """
    Main orchestrator combining all three techniques.
    Manages workflow and coordinates specialist agents.
    """
    
    def __init__(self):
        """Initialize all specialist agents with appropriate temperatures"""
        self.rewriter_agent = None     # Temperature: 0.7
        self.generator_agent = None     # Temperature: 0.9
        self.voter_agent = None         # Temperature: 0.2
        self.logger = None              # Logging framework
        
    def generate_ui_design(self, request, config):
        """
        Main entry point for UI design generation.
        Orchestrates the complete workflow.
        
        Args:
            request: Initial user request (may be vague)
            config: Configuration including criteria, chains, thresholds
            
        Returns:
            Final design with metadata
        """
        # Log workflow start
        # Phase 1: Dynamic Prompt Rewriting
        # Phase 2: Multi-chain Generation
        # Phase 3: Self-consistency Voting
        # Phase 4: Validation
        # Log workflow completion
        pass


# ============================================================
# DYNAMIC PROMPT REWRITER WITH LEARNING LOOP
# ============================================================

class DynamicPromptRewriter:
    """
    Handles automatic prompt refinement with continuous learning.
    Uses medium temperature for creative improvements.
    Implements a training loop that learns from successful rewrites.
    """
    
    def __init__(self):
        """Initialize with learning components"""
        self.rewrite_history = []       # Track all rewrites
        self.success_patterns = {}      # Successful rewrite patterns
        self.failure_patterns = {}      # Common failure patterns
        self.learning_rate = 0.1        # How much to weight new patterns
        
    def refine_prompt(self, initial_prompt, criteria, max_iterations):
        """
        Iteratively refines prompt until criteria are met.
        
        Process:
        1. Test current prompt
        2. Evaluate against criteria
        3. Rewrite if needed (using learned patterns)
        4. Repeat until success or max iterations
        5. Update learning patterns based on outcome
        """
        # Log refinement start
        # Check if we have successful patterns for similar criteria
        # Test prompt loop:
        #   - Generate output
        #   - Evaluate against criteria
        #   - If success: record pattern
        #   - If failure: apply learned rewrite strategies
        # Update success/failure patterns
        # Log refinement result with learning metrics
        pass
    
    def evaluate_output(self, output, criteria):
        """
        Checks if output meets all specified criteria.
        Records evaluation patterns for learning.
        
        Criteria types:
        - Quantitative (min_features, word_count)
        - Qualitative (tone, clarity)
        - Structural (format, required_fields)
        """
        # Log evaluation start
        # Check each criterion
        # Record which criteria passed/failed
        # Calculate evaluation score
        # Store evaluation pattern
        # Return detailed results with scores
        pass
    
    def generate_rewrite(self, original_prompt, failed_output, criteria):
        """
        Creates improved prompt based on failure analysis and learned patterns.
        
        Improvement strategies (ordered by success rate):
        1. Apply previously successful patterns
        2. Add specificity based on failure type
        3. Include examples from successful outputs
        4. Clarify requirements using learned language
        5. Add constraints that prevented past failures
        """
        # Log rewrite generation
        # Analyze failure patterns
        # Check rewrite history for similar failures
        # Apply most successful improvement strategy
        # If no history, use default strategies
        # Track which strategy was used
        # Return refined prompt with strategy metadata
        pass
    
    def update_learning_patterns(self, prompt_pair, outcome, criteria):
        """
        Updates the learning model based on rewrite outcomes.
        This is the core of the training loop.
        
        Args:
            prompt_pair: (original_prompt, rewritten_prompt)
            outcome: Success/failure and quality metrics
            criteria: The criteria that were being optimized for
        """
        # Extract rewrite patterns (what changed)
        # If successful:
        #   - Increase pattern weight in success_patterns
        #   - Store criteria-pattern mapping
        #   - Calculate pattern effectiveness score
        # If failed:
        #   - Add to failure_patterns
        #   - Identify what didn't work
        # Update pattern rankings
        # Decay old patterns (forgetting mechanism)
        pass
    
    def get_best_rewrite_strategy(self, criteria_fingerprint):
        """
        Returns the most successful rewrite strategy for given criteria.
        This implements the learning application.
        
        Returns:
            Strategy function that can transform prompts
        """
        # Generate criteria fingerprint (hash of requirements)
        # Look up most successful patterns for this fingerprint
        # If found, return pattern-based strategy
        # If not found, return closest match strategy
        # Include confidence score in strategy
        pass
    
    def export_learned_patterns(self):
        """
        Exports successful patterns for persistence or sharing.
        Enables transfer learning across sessions.
        """
        # Compile top patterns by success rate
        # Include metadata: use count, success rate, criteria types
        # Format for easy import/merge
        # Return exportable pattern library
        pass


# ============================================================
# VISUAL CHAIN-OF-THOUGHT GENERATOR
# ============================================================

class VisualChainOfThoughtGenerator:
    """
    Generates multiple UI design chains with visual reasoning.
    Uses high temperature for diverse approaches.
    """
    
    def generate_design_chains(self, prompt, num_chains, diversity_hints):
        """
        Creates multiple independent design approaches.
        
        Each chain includes:
        - Visual reasoning steps
        - Design decisions
        - HTML/CSS prototype
        - Confidence score
        """
        # Log generation start
        # For each chain:
        #   Apply diversity hint
        #   Generate reasoning steps
        #   Create prototype
        #   Calculate confidence
        # Log all chains generated
        pass
    
    def generate_single_chain(self, prompt, chain_id, diversity_hint):
        """
        Generates one complete design chain.
        
        Steps:
        1. Visual layout reasoning
        2. Component selection
        3. Interaction patterns
        4. Style decisions
        5. Code generation
        """
        # Log chain generation
        # Generate visual reasoning
        # Create design decisions
        # Generate prototype code
        # Return complete chain
        pass
    
    def apply_diversity_strategy(self, base_prompt, strategy):
        """
        Modifies prompt to encourage diverse approaches.
        
        Strategies:
        - Platform focus (mobile, desktop, tablet)
        - User type (power user, casual, enterprise)
        - Design philosophy (minimal, rich, playful)
        - Technical constraints (performance, accessibility)
        """
        # Log diversity application
        # Modify prompt based on strategy
        # Return enhanced prompt
        pass


# ============================================================
# SELF-CONSISTENCY VOTER
# ============================================================

class SelfConsistencyVoter:
    """
    Analyzes multiple chains and builds consensus.
    Uses low temperature for objective analysis.
    """
    
    def vote_on_designs(self, design_chains):
        """
        Applies majority voting to select best design.
        
        Process:
        1. Extract features from all chains
        2. Count feature occurrences
        3. Identify majority patterns
        4. Select representative design
        5. Calculate confidence
        """
        # Log voting start
        # Extract all features
        # Apply voting algorithm
        # Select winning design
        # Log voting results
        pass
    
    def extract_design_features(self, chain):
        """
        Identifies key features from a design chain.
        
        Feature categories:
        - Layout patterns (grid, flex, etc.)
        - Navigation types
        - Component choices
        - Interaction patterns
        - Visual style
        """
        # Log feature extraction
        # Parse reasoning steps
        # Identify features
        # Return feature list
        pass
    
    def calculate_consensus_confidence(self, vote_distribution, total_chains):
        """
        Calculates confidence based on voting patterns.
        
        Factors:
        - Majority strength
        - Vote distribution
        - Feature agreement
        - Chain quality scores
        """
        # Log confidence calculation
        # Analyze vote patterns
        # Calculate confidence score
        # Return confidence metrics
        pass


# ============================================================
# VALIDATION AND QUALITY ASSURANCE
# ============================================================

class DesignValidator:
    """
    Validates final designs against criteria.
    Ensures quality and completeness.
    """
    
    def validate_design(self, design, original_criteria):
        """
        Comprehensive validation of generated design.
        
        Checks:
        - Criteria satisfaction
        - Code validity
        - Design coherence
        - Accessibility compliance
        - Performance considerations
        """
        # Log validation start
        # Check all criteria
        # Validate code structure
        # Verify design coherence
        # Return validation report
        pass
    
    def suggest_improvements(self, design, validation_report):
        """
        Generates improvement suggestions for failed validations.
        
        Improvement areas:
        - Missing features
        - Code quality
        - Design consistency
        - User experience
        """
        # Log improvement analysis
        # Identify weaknesses
        # Generate suggestions
        # Return improvement plan
        pass


# ============================================================
# SUPPORTING COMPONENTS
# ============================================================

class PromptTemplateManager:
    """Manages and optimizes prompt templates"""
    
    def get_template(self, technique, context):
        """Retrieves appropriate prompt template"""
        pass
    
    def optimize_template(self, template, success_metrics):
        """Learns from successful prompts"""
        pass


class DesignPatternLibrary:
    """Stores and retrieves successful design patterns"""
    
    def store_pattern(self, pattern, metadata):
        """Saves successful design patterns"""
        pass
    
    def retrieve_similar_patterns(self, context):
        """Finds relevant past patterns"""
        pass


class MetricsCollector:
    """Tracks system performance and quality metrics"""
    
    def track_generation_metrics(self, workflow_data):
        """Records metrics for analysis"""
        pass
    
    def generate_quality_report(self):
        """Produces quality assessment"""
        pass


# ============================================================
# COPYWRITING META-LIBRARY INTEGRATION
# ============================================================

class CopywritingMetaLibrary:
    """
    Mass production factory for copywriting frameworks.
    Integrates with main system for content generation at scale.
    """
    
    def __init__(self):
        """Initialize with all copywriting frameworks"""
        self.frameworks = {
            "AIDA": None,           # Attention-Interest-Desire-Action
            "PAS": None,            # Problem-Agitate-Solve
            "FAB": None,            # Features-Advantages-Benefits
            "PASTOR": None,         # Problem-Amplify-Story-Testimonial-Offer-Response
            "BAB": None,            # Before-After-Bridge
            "4Ps": None,            # Picture-Promise-Prove-Push
            "ACCA": None,           # Awareness-Comprehension-Conviction-Action
            "5_Objections": None,   # Time/Money/Trust/Need/Work objections
            "SSS": None,            # Story-Solve-Sell
            "Emotion_Logic": None,  # Emotional and logical appeals
            # ... 24+ frameworks total
        }
        self.batch_processor = None
        self.quality_checker = None
        
    def mass_produce_copy(self, framework_name, parameter_sets, count=10):
        """
        Mass produce copy variations using specified framework.
        
        Process:
        1. Select framework template
        2. Generate parameter combinations
        3. Produce variations in parallel
        4. Quality check each output
        5. Return batch results
        """
        # Log mass production start
        # Validate framework exists
        # Generate all parameter combinations
        # Parallel process variations
        # Quality check results
        # Return successful outputs
        pass
    
    def adaptive_framework_selection(self, context, goal):
        """
        Automatically selects best framework based on context.
        Uses learning from past performance.
        
        Selection criteria:
        - Industry type
        - Audience characteristics
        - Desired outcome
        - Historical performance
        """
        # Analyze context
        # Check historical performance
        # Select optimal framework
        # Return with confidence score
        pass
    
    def hybrid_framework_generation(self, frameworks, blend_weights):
        """
        Creates new frameworks by blending existing ones.
        Enables innovation in copy structures.
        """
        # Validate frameworks
        # Apply blend weights
        # Generate hybrid structure
        # Test with sample data
        # Return new framework
        pass


# ============================================================
# TRAINING LOOP IMPLEMENTATION
# ============================================================

class PromptRewritingTrainingLoop:
    """
    Implements the continuous learning loop for Dynamic Prompt Rewriting.
    This is how the system improves over time.
    """
    
    def __init__(self):
        """Initialize training components"""
        self.rewriter = None                    # DynamicPromptRewriter instance
        self.training_buffer = []               # Recent interactions
        self.batch_size = 10                    # Process in batches
        self.success_threshold = 0.8            # What counts as success
        
    def run_training_iteration(self, user_requests):
        """
        Single iteration of the training loop.
        Processes multiple requests and learns from outcomes.
        
        This is the "on-the-fly" learning mechanism.
        """
        # For each user request:
        #   1. Try current best strategy
        #   2. If fails, try rewriting with different patterns
        #   3. Track what worked/didn't work
        #   4. Update pattern weights
        # Batch update learned patterns
        # Export improved patterns
        pass
    
    def online_learning_step(self, request, outcome):
        """
        Real-time learning from a single interaction.
        Updates patterns immediately based on success/failure.
        
        This enables "on-the-fly" adaptation.
        """
        # Extract features from request
        # Identify which patterns were used
        # Calculate success metrics
        # Update pattern weights immediately
        # Adjust strategy for next request
        pass
    
    def pattern_discovery_loop(self):
        """
        Discovers new rewrite patterns through experimentation.
        Runs in background to find novel strategies.
        """
        # Generate pattern variations
        # Test on historical difficult cases
        # Measure improvement
        # Add successful discoveries to pattern library
        # Remove unsuccessful patterns
        pass
    
    def cross_domain_transfer(self, source_domain, target_domain):
        """
        Transfers learned patterns between different domains.
        Enables faster learning in new areas.
        """
        # Identify transferable patterns
        # Adapt patterns to new domain
        # Test adapted patterns
        # Integrate successful transfers
        pass


# ============================================================
# WORKFLOW EXAMPLE WITH TRAINING LOOP
# ============================================================

def example_workflow_with_learning():
    """
    Demonstrates the complete workflow with continuous learning.
    
    Flow:
    1. User provides vague request
    2. Orchestrator initiates workflow
    3. Rewriter refines prompt (using learned patterns)
    4. Generator creates multiple chains
    5. Voter selects best design
    6. Validator ensures quality
    7. Training loop updates patterns based on outcome
    8. Return final design
    9. System is now smarter for next request
    """
    # Initialize orchestrator with learning enabled
    # Configure agents
    # Process request:
    #   - Apply best known rewrite strategy
    #   - Generate designs
    #   - Vote and validate
    # Update learning patterns:
    #   - Record what worked
    #   - Adjust strategies
    #   - Export improvements
    # Log learning metrics
    # Return results
    pass

def continuous_improvement_example():
    """
    Shows how the system improves over multiple requests.
    
    Example sequence:
    Request 1: "Make a task app" (vague)
    - System struggles, takes 3 rewrites
    - Learns: task apps need specific feature lists
    
    Request 2: "Make another task app" (vague)
    - System immediately adds feature requirements
    - Success in 1 rewrite
    
    Request 3: "Make a project tool" (vague, similar domain)
    - System transfers learning from task apps
    - Adds feature lists, UI components
    - Success in 1 rewrite
    
    The system has learned to handle vague productivity app requests!
    """
    # Show progression of learning
    # Demonstrate pattern transfer
    # Visualize improvement metrics
    pass


# ============================================================
# CONFIGURATION STRUCTURE
# ============================================================

DEFAULT_CONFIG = {
    "agents": {
        "orchestrator": {"temperature": 0.3},
        "rewriter": {"temperature": 0.7, "max_rewrites": 3},
        "generator": {"temperature": 0.9, "num_chains": 5},
        "voter": {"temperature": 0.2, "min_confidence": 0.7}
    },
    "criteria": {
        "min_features": 5,
        "required_elements": ["navigation", "content", "actions"],
        "output_format": "json_with_html_css"
    },
    "diversity_strategies": [
        "mobile_first",
        "desktop_power_user", 
        "accessibility_focused",
        "performance_optimized",
        "collaboration_centric"
    ],
    "validation": {
        "strict_mode": True,
        "accessibility_check": True,
        "performance_budget": {"css_size": "50kb", "load_time": "3s"}
    }
}


# ============================================================
# LOGGING FRAMEWORK
# ============================================================

class WorkflowLogger:
    """
    Comprehensive logging for debugging and monitoring.
    All functions include logging placeholders.
    """
    
    def log_phase_start(self, phase_name, context):
        """Log the start of a major phase"""
        # timestamp, phase, context details
        pass
    
    def log_phase_complete(self, phase_name, results):
        """Log phase completion with results"""
        # timestamp, phase, results summary
        pass
    
    def log_agent_action(self, agent_name, action, details):
        """Log individual agent actions"""
        # timestamp, agent, action, details
        pass
    
    def log_error(self, error_type, details, recovery_action):
        """Log errors and recovery attempts"""
        # timestamp, error, details, recovery
        pass
    
    def generate_workflow_summary(self, workflow_id):
        """Generate complete workflow summary"""
        # Full workflow trace
        # Performance metrics
        # Quality scores
        # Recommendations
        pass
```

## Integration Points with PyClarity

### 1. Cognitive Tool Enhancement
- Generate UIs for each cognitive tool
- Adapt interfaces based on tool requirements
- Maintain consistency across tool suite

### 2. Shared Components
- Reuse validation logic
- Common design patterns
- Unified logging framework

### 3. Performance Optimization
- Cache successful patterns
- Reuse refined prompts
- Share agent instances

## Future Extensibility

### 1. Additional Agents
- **Accessibility Agent** (Temperature: 0.4): Ensures WCAG compliance
- **Performance Agent** (Temperature: 0.3): Optimizes for speed
- **Localization Agent** (Temperature: 0.6): Adapts for different regions

### 2. Advanced Techniques
- Reinforcement learning from user feedback
- Pattern evolution over time
- Cross-project learning

### 3. Integration APIs
- REST endpoints for external access
- Event-driven architecture
- Plugin system for custom agents

## Learning Pattern Examples

### Pattern Library Structure
```python
LEARNED_PATTERNS = {
    "vague_to_specific": {
        "task_app": {
            "original": "Make a task app",
            "improved": "Design a task management app with at least 5 features including task creation, categorization, due dates, collaboration, and progress tracking. Include responsive design and output as JSON with HTML/CSS.",
            "success_rate": 0.92,
            "use_count": 47
        },
        "dashboard": {
            "original": "Create a dashboard",
            "improved": "Design an analytics dashboard with data visualization, real-time updates, filtering options, export functionality, and responsive grid layout. Include specific metrics and KPIs.",
            "success_rate": 0.88,
            "use_count": 23
        }
    },
    "missing_criteria_fixes": {
        "no_feature_count": "Explicitly specify 'include at least X features'",
        "no_format": "Add 'output as JSON with structure: {...}'",
        "no_platform": "Specify 'for desktop/mobile/responsive design'"
    },
    "domain_specific_improvements": {
        "e_commerce": ["product grid", "cart", "checkout", "search", "filters"],
        "productivity": ["task management", "collaboration", "timeline", "reports"],
        "analytics": ["charts", "metrics", "filters", "exports", "real-time"]
    }
}
```

### How Learning Happens On-The-Fly

1. **Pattern Recognition**: System identifies request type
2. **Strategy Selection**: Chooses best known rewrite pattern
3. **Application**: Applies pattern to current request
4. **Evaluation**: Measures success against criteria
5. **Weight Update**: Adjusts pattern confidence
6. **Pattern Evolution**: Modifies patterns based on outcomes

### Training Loop Visualization
```
Request → Rewrite → Generate → Evaluate → Learn
   ↑                                          ↓
   ←──────── Apply Learned Patterns ←─────────┘
```

## Summary

This architecture provides:
- Clear separation of concerns
- Modular agent design
- **Continuous learning through pattern recognition**
- **On-the-fly prompt improvement**
- **Cross-domain pattern transfer**
- Comprehensive logging framework
- Extensible configuration
- No scattered implementation files
- Single source of truth for the system

The Dynamic Prompt Rewriting with training loop enables the system to:
- Learn from every interaction
- Improve prompt quality automatically
- Transfer knowledge between domains
- Reduce rewrite iterations over time
- Build a library of successful patterns

All components are defined as pseudocode with clear purposes and logic flow, ready for future implementation when needed.

## Framework Libraries

The system now includes comprehensive framework libraries across multiple domains:

### Copywriting Frameworks
- **Core Library**: 24+ copywriting frameworks (AIDA, PAS, FAB, PASTOR, etc.)
- **Extended Library**: 15+ additional frameworks with TypeDict and Jinja2 templates
- **Mass Production**: Scaling capabilities for generating variations
- See: `copywriting-meta-library.md` and `extended-copywriting-frameworks.md`

### UX/UI Design Frameworks
- **Design Process**: Double Diamond, Design Thinking, Lean UX
- **Analysis**: JTBD, User Journey Mapping, Atomic Design
- **Implementation**: Component libraries, design tokens, accessibility
- See: `ux-ui-frameworks.md`

### Marketing Frameworks
- **Strategic**: STP, SOSTAC, 7Ps Marketing Mix
- **Growth**: AARRR (Pirate Metrics), Growth Hacking
- **Campaigns**: Content Marketing, ABM, Influencer Marketing
- **Templates**: Email campaigns, social media, multi-channel
- See: `marketing-frameworks.md`

### Business Strategy Frameworks
- **Planning**: Business Model Canvas, OKRs, Balanced Scorecard
- **Analysis**: Porter's Five Forces, SWOT-TOWS, McKinsey 7S
- **Innovation**: Blue Ocean Strategy, Value Innovation
- **Financial**: Unit economics, projections, risk assessment
- See: `business-frameworks.md`

All frameworks use Jinja2 templates for consistent, scalable generation and can be integrated with the Visual Chain-of-Thought and Dynamic Prompt Rewriting systems.