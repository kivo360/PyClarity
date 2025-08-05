Feature: Cognitive Tool Orchestration
  As a PyClarity power user
  I want to seamlessly combine multiple cognitive tools
  So that I can tackle complex, multi-faceted problems effectively

  Background:
    Given all cognitive tools are available
    And the workflow engine is configured
    And I understand tool capabilities

  Scenario: Startup validation workflow
    Given I have a startup idea "AI-powered code review assistant"
    When I orchestrate a comprehensive validation:
      """
      1. Sequential Thinking → Break down the problem space
      2. Mental Models → Apply first principles to core value
      3. Collaborative Reasoning → Gather stakeholder perspectives
      4. Decision Framework → Evaluate build vs buy vs partner
      5. Triple Constraint → Balance features, time, budget
      6. Market Analysis → Assess market opportunity
      7. Competitive Intelligence → Understand competition
      """
    Then each tool should build on previous insights
    And the final output should include:
      | component                | description                          |
      | Problem validation      | Is this a real problem worth solving |
      | Solution approach       | How to build it effectively          |
      | Market opportunity      | Size and growth potential            |
      | Competitive advantage   | How to differentiate                 |
      | Implementation plan     | Concrete next steps                  |

  Scenario: Technical architecture decision
    Given I need to design "Microservices vs Monolith for e-commerce"
    When I create a technical decision workflow:
      | sequence | tool                    | purpose                              |
      | 1       | scientific_method       | Form hypotheses about each approach   |
      | 2       | design_patterns        | Identify relevant patterns            |
      | 3       | programming_paradigms  | Consider paradigm implications        |
      | 4       | impact_propagation     | Analyze failure modes                 |
      | 5       | decision_framework     | Make final recommendation             |
    Then tools should share context effectively
    And technical constraints should flow through analysis
    And decision should be traceable to evidence

  Scenario: Problem debugging orchestration
    Given I have a production issue "Memory leak in payment service"
    When I orchestrate debugging workflow:
      | tool                  | contribution                            |
      | debugging_approaches  | Systematic investigation strategy       |
      | visual_reasoning     | Visualize memory allocation patterns    |
      | scientific_method    | Test hypotheses about leak source       |
      | impact_propagation   | Understand system-wide effects          |
    Then the orchestration should:
      | outcome                                        |
      | Identify root cause systematically            |
      | Understand full impact scope                  |
      | Provide fix verification strategy             |
      | Suggest prevention measures                   |

  Scenario: Strategic planning cascade
    Given quarterly planning for "Platform modernization initiative"
    When I cascade through strategic tools:
      """
      Phase 1 - Understanding:
        - Mental Models (first principles)
        - Multi-perspective Analysis (stakeholder views)
      
      Phase 2 - Planning:
        - Sequential Thinking (roadmap steps)
        - Triple Constraint (resource optimization)
        
      Phase 3 - Validation:
        - Iterative Validation (test assumptions)
        - Decision Framework (go/no-go points)
      """
    Then each phase should inform the next
    And outputs should progressively refine
    And final plan should be actionable

  Scenario: Cross-functional tool collaboration
    Given a complex challenge requiring diverse thinking
    When tools from different categories collaborate:
      | category          | tool                      | contributes              |
      | Analytical       | sequential_thinking        | Logical structure        |
      | Creative         | design_patterns           | Solution patterns        |
      | Critical         | structured_argumentation  | Challenge assumptions    |
      | Collaborative    | collaborative_reasoning   | Multiple viewpoints      |
      | Evaluative       | decision_framework        | Final assessment         |
    Then diverse perspectives should be integrated
    And conflicts should be explicitly addressed
    And synthesis should be richer than individual analyses

  Scenario: Adaptive workflow based on complexity
    Given problems of varying complexity:
      | problem                        | complexity |
      | "Fix typo in documentation"   | simple     |
      | "Optimize API performance"    | moderate   |
      | "Redesign system architecture"| complex    |
      | "Company pivot strategy"      | very_complex |
    When the system selects appropriate tool combinations
    Then tool selection should match complexity:
      | complexity    | recommended_tools                                    |
      | simple       | sequential_thinking only                             |
      | moderate     | sequential_thinking + mental_models                  |
      | complex      | + design_patterns + decision_framework               |
      | very_complex | + collaborative_reasoning + triple_constraint + more |

  Scenario: Failure recovery in orchestration
    Given a multi-tool workflow where tool 3 of 5 fails
    When the orchestration handles the failure
    Then it should:
      | recovery_action                                |
      | Preserve results from tools 1 and 2          |
      | Attempt alternate approaches for tool 3       |
      | Adjust tools 4 and 5 to work with partial data |
      | Provide meaningful results despite failure    |
      | Document what was missed due to failure       |

  Scenario: Real-time orchestration adaptation
    Given an ongoing analysis that reveals new information
    When intermediate results suggest different approach needed
    Then the orchestration should:
      | adaptation                                     |
      | Dynamically add relevant tools               |
      | Skip tools that are no longer applicable     |
      | Adjust parameters based on discoveries        |
      | Maintain coherent narrative throughout        |

  Scenario: Performance optimization
    Given a workflow with 8+ tools
    When executing the orchestration
    Then performance optimizations should include:
      | optimization                                   |
      | Parallel execution where possible             |
      | Caching of intermediate results               |
      | Progressive output streaming                  |
      | Total time < sum of individual tool times     |
      | Memory usage within reasonable bounds         |