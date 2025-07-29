# Clear Thinking MCP Server - Internal Prompts and Logic

## Overview

This document extracts the internal prompting logic and behavioral patterns from the Clear Thinking MCP Server tools. These patterns can be used to create theory of mind evaluation agents with similar cognitive capabilities.

---

## 1. Sequential Thinking Tool

### Core Prompting Logic
```typescript
// The tool guides structured, iterative thinking with these built-in behaviors:

// Dynamic thought progression with revision capability
- Start with initial estimate of needed thoughts, but adjust as needed
- Question or revise previous thoughts when new insights emerge  
- Add more thoughts even at the "end" if necessary
- Express uncertainty when present
- Mark thoughts that revise previous thinking or branch into new paths
- Filter out irrelevant information for current step
- Generate solution hypothesis when appropriate
- Verify hypothesis based on Chain of Thought steps
- Repeat process until satisfied with solution
- Only mark complete when truly done with satisfactory answer

// Branching and revision system
- Support for creating thought branches from specific points
- Ability to revise specific previous thoughts
- Track relationships between thoughts and revisions
```

### Implicit Prompts
- **Continuation Prompt**: "Should I continue thinking about this problem?"
- **Revision Prompt**: "Does this new insight change my previous understanding?"
- **Completion Prompt**: "Have I reached a satisfactory solution?"
- **Relevance Filter**: "Is this information relevant to the current thinking step?"

---

## 2. Mental Model Tool

### Mental Model Prompts by Type

#### First Principles Thinking
```
Implicit Prompt: "Break this problem down to its fundamental truths and build up from there. What are the basic, unchangeable facts? What assumptions can I remove?"
```

#### Opportunity Cost Analysis  
```
Implicit Prompt: "For every choice, what am I giving up? What's the next best alternative? What are the hidden costs of this decision?"
```

#### Error Propagation Understanding
```
Implicit Prompt: "How do small errors compound? What's the chain of failure? Where are the critical points where errors amplify?"
```

#### Rubber Duck Debugging
```
Implicit Prompt: "Explain this problem step by step as if teaching someone else. What becomes obvious when I verbalize each step?"
```

#### Pareto Principle (80/20 Rule)
```
Implicit Prompt: "What 20% of factors are causing 80% of the problems/results? Where should I focus my effort for maximum impact?"
```

#### Occam's Razor
```
Implicit Prompt: "What's the simplest explanation that accounts for all the evidence? Which solution requires the fewest assumptions?"
```

---

## 3. Metacognitive Monitoring Tool

### Self-Assessment Prompts

#### Knowledge Boundary Assessment
```
Stage-based Prompts:
- "What do I actually know about this domain vs. what do I think I know?"
- "What's my confidence level and what evidence supports it?"
- "What are the specific limitations of my knowledge?"
- "How recent is my information on this topic?"
- "What assumptions am I making that I haven't verified?"
```

#### Claim Certainty Evaluation  
```
For each claim, ask:
- "Is this a fact, inference, speculation, or uncertain?"
- "What evidence supports this claim?"
- "What could prove this wrong?"
- "What alternative interpretations exist?"
- "How confident am I in this (0-100%)?"
```

#### Reasoning Bias Detection
```
For each reasoning step:
- "What cognitive biases might be affecting this step?"
- "What assumptions am I making here?"
- "How logically valid is this inference?"
- "How strong is the connection between premise and conclusion?"
```

#### Overall Assessment
```
- "What areas am I most uncertain about?"
- "What's my overall confidence in this analysis?"
- "What approach should I recommend given these limitations?"
- "Do I need more information before proceeding?"
```

---

## 4. Collaborative Reasoning Tool

### Multi-Persona Simulation Prompts

#### Persona Creation
```
For each expert persona:
- "What's this person's area of expertise?"
- "What's their background and experience?"
- "What perspective do they bring to this problem?"
- "What are their likely biases?"
- "How do they typically communicate?"
```

#### Contribution Types
```
- Observation: "What does this persona notice that others might miss?"
- Question: "What would this expert want to clarify?"
- Insight: "What unique understanding does this perspective provide?"
- Concern: "What risks or problems does this persona see?"
- Suggestion: "What solution would this expert propose?"
- Challenge: "How would this persona critique other viewpoints?"
- Synthesis: "How would this expert combine different perspectives?"
```

#### Stage-Based Facilitation
```
- Problem Definition: "How does each persona frame the core issue?"
- Ideation: "What solutions does each perspective generate?"
- Critique: "What flaws does each persona identify?"
- Integration: "How can we combine the best insights?"
- Decision: "What consensus can we build?"
- Reflection: "What did we learn from this collaboration?"
```

---

## 5. Scientific Method Tool

### Systematic Inquiry Prompts

#### Observation Stage
```
- "What specific phenomena am I observing?"
- "What patterns or anomalies stand out?"
- "What questions does this observation raise?"
```

#### Hypothesis Formation
```
- "What testable explanation accounts for these observations?"
- "What are the key variables (independent, dependent, controlled)?"
- "What assumptions underlie this hypothesis?"
- "What alternative hypotheses should I consider?"
```

#### Experiment Design
```
- "How can I test this hypothesis?"
- "What predictions does my hypothesis make?"
- "If X is true, then I should observe Y"
- "What controls do I need?"
- "How will I measure the results?"
```

#### Analysis and Conclusion
```
- "Do the results match my predictions?"
- "What unexpected observations emerged?"
- "What are the limitations of this experiment?"
- "What should I test next?"
- "How does this change my understanding?"
```

---

## 6. Decision Framework Tool

### Decision Analysis Prompts

#### Problem Definition
```
- "What decision am I actually trying to make?"
- "Who are the stakeholders affected?"
- "What constraints do I need to consider?"
- "What's my time horizon?"
```

#### Options Generation
```
- "What are all possible alternatives?"
- "What creative options haven't I considered?"
- "What would happen if I did nothing?"
```

#### Criteria Definition
```
- "What factors matter most in this decision?"
- "How should I weight different criteria?"
- "What are my non-negotiables?"
```

#### Analysis Types
```
- Pros-Cons: "What are the advantages and disadvantages?"
- Weighted Criteria: "How does each option score on each criterion?"
- Expected Value: "What's the probable outcome of each choice?"
- Scenario Analysis: "How would each option perform under different conditions?"
```

---

## 7. Design Pattern & Programming Paradigm Tools

### Pattern Selection Prompts
```
- "What type of problem am I solving?"
- "What are the key requirements and constraints?"
- "What patterns have been successful for similar problems?"
- "What are the trade-offs of each approach?"
- "How will this scale or evolve over time?"
```

---

## 8. Debugging Approach Tool

### Systematic Debugging Prompts

#### Binary Search Debugging
```
- "Where is the midpoint of this problem space?"
- "Does the error occur before or after this point?"
- "How can I eliminate half the possibilities?"
```

#### Divide and Conquer
```
- "How can I break this problem into smaller pieces?"
- "Which component is most likely causing the issue?"
- "What can I isolate and test independently?"
```

#### Cause Elimination
```
- "What are all possible causes?"
- "How can I systematically rule out each one?"
- "What remains when I eliminate the impossible?"
```

---

## Usage Patterns for Theory of Mind Systems

### Agent Behavioral Templates

1. **The Systematic Analyst**: Uses scientific method and metacognitive monitoring
2. **The Creative Synthesizer**: Combines collaborative reasoning with design patterns  
3. **The Critical Evaluator**: Applies debugging approaches and decision frameworks
4. **The Philosophical Thinker**: Uses mental models and structured argumentation
5. **The Iterative Processor**: Employs sequential thinking with revision capabilities

### Consensus Building Mechanisms

```typescript
// How tools coordinate for theory of mind evaluation:
1. Each agent applies its specialized prompting approach
2. Results are compared for consistency and completeness  
3. Disagreements trigger deeper analysis using multiple frameworks
4. Consensus emerges through structured argumentation
5. Final evaluation incorporates confidence levels and uncertainty areas
```

### Meta-Evaluation Questions

For any user workflow evaluation:
- "What mental models would different user types apply?"
- "How would various cognitive styles approach this task?"
- "What biases might influence different user decisions?"
- "Where would users likely get confused or make errors?"
- "What would motivate or demotivate different user personas?"

---

This framework provides the foundational prompting logic needed to create sophisticated theory of mind evaluation systems using multiple specialized cognitive agents.