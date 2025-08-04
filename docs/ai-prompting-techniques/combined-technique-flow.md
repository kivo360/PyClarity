# Combined Technique Flow: Visual CoT + Self-Consistency + Dynamic Rewriting

## Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        Initial Request                           │
│              "Design a task management app UI"                   │
└─────────────────────────────────────────┬───────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Dynamic Prompt Rewriting                       │
│                                                                  │
│  1. Test initial prompt                                          │
│  2. Evaluate output against criteria                             │
│  3. If inadequate, rewrite for specificity:                     │
│     "Design a task management app UI with 5 specific features,  │
│      visual reasoning steps, responsive design, and HTML/CSS"   │
└─────────────────────────────────────────┬───────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────┐
│              Visual Chain-of-Thought (Multiple Chains)           │
│                                                                  │
│  Chain 1:                          Chain 2:                      │
│  ┌─────────────────┐              ┌─────────────────┐          │
│  │ 1. Top navbar   │              │ 1. Side drawer  │          │
│  │ 2. Task grid    │              │ 2. List view    │          │
│  │ 3. Quick add    │              │ 3. Inline add   │          │
│  │ 4. Filters      │              │ 4. Tab filters  │          │
│  │ 5. Dark mode    │              │ 5. Light theme  │          │
│  └─────────────────┘              └─────────────────┘          │
│                                                                  │
│  Chain 3:                          Chain 4:                      │
│  ┌─────────────────┐              ┌─────────────────┐          │
│  │ 1. Header bar   │              │ 1. Top menu     │          │
│  │ 2. Kanban view  │              │ 2. Card layout  │          │
│  │ 3. Modal add    │              │ 3. FAB button   │          │
│  │ 4. Sidebar      │              │ 4. Breadcrumbs  │          │
│  │ 5. Material UI  │              │ 5. Minimal UI   │          │
│  └─────────────────┘              └─────────────────┘          │
└─────────────────────────────────────────┬───────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Self-Consistency Voting                       │
│                                                                  │
│  Design Features:           Votes:                               │
│  • Top navigation     →     3/4 chains  ✓ SELECTED              │
│  • Grid/Card layout   →     3/4 chains  ✓ SELECTED              │
│  • Quick add button   →     3/4 chains  ✓ SELECTED              │
│  • Filter system      →     4/4 chains  ✓ SELECTED              │
│  • Minimal/Clean UI   →     2/4 chains  ✓ SELECTED              │
│                                                                  │
│  Confidence Score: 85%                                           │
└─────────────────────────────────────────┬───────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Validation Check                            │
│                                                                  │
│  ✓ Meets minimum features (5)                                   │
│  ✓ Has responsive design elements                               │
│  ✓ Includes HTML/CSS prototype                                  │
│  ✓ Reasoning steps are clear                                    │
│  ✓ Confidence > 80%                                             │
└─────────────────────────────────────────┬───────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Final Output                              │
│                                                                  │
│  {                                                               │
│    "reasoning_steps": [                                          │
│      "Fixed top navigation for consistent access",              │
│      "Grid-based task cards for visual organization",           │
│      "Floating action button for quick task creation",          │
│      "Sidebar filters for project/tag organization",            │
│      "Clean minimal design with focus on content"               │
│    ],                                                            │
│    "prototype": {                                                │
│      "html": "<nav>...</nav><main>...</main><button>...</>",   │
│      "css": ".nav { position: fixed; } ..."                     │
│    },                                                            │
│    "confidence": 0.85,                                           │
│    "iterations": 1                                               │
│  }                                                               │
└──────────────────────────────────────────────────────────────────┘
```

## Process Steps

### 1. Dynamic Prompt Rewriting Phase
- **Input**: Initial vague request
- **Process**: Test → Evaluate → Rewrite if needed
- **Output**: Refined, specific prompt with clear criteria

### 2. Visual Chain-of-Thought Phase
- **Input**: Refined prompt
- **Process**: Generate 4-5 independent UI design chains
- **Output**: Multiple design approaches with reasoning

### 3. Self-Consistency Voting Phase
- **Input**: All design chains
- **Process**: Extract features → Count votes → Select majority
- **Output**: Consensus design with confidence score

### 4. Validation Phase
- **Input**: Voted design
- **Process**: Check against original criteria
- **Output**: Final design or trigger another rewrite cycle

## Benefits of Combined Approach

1. **Automatic Quality Control**: Each phase improves the output
2. **Diverse Perspectives**: Multiple chains explore different approaches
3. **Reliable Results**: Voting ensures practical, consensus-based designs
4. **Self-Improving**: Dynamic rewriting learns from failures
5. **Transparent Process**: Every decision is explainable

## Example Implementation

```python
def generate_ui_with_combined_techniques(request, config=None):
    """
    Main orchestrator for combined AI prompting techniques
    """
    config = config or {
        "max_rewrites": 2,
        "num_chains": 5,
        "min_confidence": 0.8,
        "criteria": {
            "min_features": 5,
            "required_elements": ["navigation", "content", "actions"],
            "output_format": "json_with_html_css"
        }
    }
    
    # Phase 1: Dynamic Prompt Rewriting
    refined_prompt = dynamic_prompt_rewriter.refine(
        initial_prompt=request,
        criteria=config["criteria"],
        max_iterations=config["max_rewrites"]
    )
    
    # Phase 2: Visual Chain-of-Thought Generation
    design_chains = []
    for i in range(config["num_chains"]):
        chain = visual_cot_generator.generate(
            prompt=refined_prompt,
            chain_id=i,
            encourage_diversity=True
        )
        design_chains.append(chain)
    
    # Phase 3: Self-Consistency Voting
    voted_result = self_consistency_voter.process(
        chains=design_chains,
        voting_strategy="majority",
        min_votes=3
    )
    
    # Phase 4: Validation and Potential Re-iteration
    if voted_result["confidence"] < config["min_confidence"]:
        # Trigger another cycle with lessons learned
        return generate_ui_with_combined_techniques(
            request=f"{request}\nPrevious attempt confidence: {voted_result['confidence']}",
            config=config
        )
    
    return {
        "success": True,
        "design": voted_result["design"],
        "confidence": voted_result["confidence"],
        "process_metadata": {
            "rewrites": refined_prompt["iterations"],
            "chains_generated": len(design_chains),
            "consensus_features": voted_result["majority_features"]
        }
    }
```

## Integration Points with PyClarity

1. **Strategic Decision Accelerator**
   - Use combined approach for complex strategic UI dashboards
   - Visualize decision matrices with consensus-based layouts

2. **Multi-Perspective Analysis**
   - Generate diverse UI perspectives for analysis tools
   - Vote on most effective visualization approach

3. **Iterative Validation Framework**
   - Continuously refine tool interfaces based on usage
   - Apply dynamic rewriting to improve user prompts

4. **All Cognitive Tools**
   - Generate consistent, high-quality interfaces
   - Ensure accessibility and usability standards
   - Adapt to user preferences through rewriting

## Conclusion

The combination of Visual Chain-of-Thought, Self-Consistency, and Dynamic Prompt Rewriting creates a powerful, self-improving system for UI design generation that:

- Starts with any level of request clarity
- Automatically refines for specificity
- Explores multiple design approaches
- Builds consensus through voting
- Validates against criteria
- Produces reliable, implementable results

This integrated approach transforms AI from a single-shot responder into a thoughtful design partner that iterates, explores, and validates to deliver optimal solutions.