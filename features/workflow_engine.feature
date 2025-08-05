Feature: Workflow Engine Orchestration
  As a developer using PyClarity workflows
  I want to orchestrate multiple cognitive tools
  So that I can solve complex problems requiring multiple analysis approaches

  Background:
    Given the Workflow Engine is initialized
    And the MCP server is accessible
    And all cognitive tools are registered

  Scenario: Simple sequential workflow execution
    Given I have a workflow configuration:
      """
      name: "analyze_technical_debt"
      tools:
        - name: "sequential_thinking"
          config:
            problem: "How to address technical debt"
        - name: "decision_framework"
          depends_on: ["sequential_thinking"]
          config:
            use_previous_output: true
      """
    When I execute the workflow
    Then tools should execute in order: sequential_thinking → decision_framework
    And each tool should receive appropriate inputs
    And the final result should combine both analyses

  Scenario: Parallel tool execution
    Given I have a workflow with independent tools:
      """
      name: "market_analysis"
      parallel_execution: true
      max_parallel: 3
      tools:
        - name: "mental_models"
          config: {model_type: "first_principles"}
        - name: "multi_perspective_analysis"
          config: {perspectives: ["customer", "competitor"]}
        - name: "design_patterns"
          config: {domain: "business_strategy"}
      """
    When I execute the workflow
    Then all three tools should start simultaneously
    And execution time should be less than sequential execution
    And results should be collected from all tools

  Scenario: Complex dependency management
    Given I have a workflow with multiple dependencies:
      """
      tools:
        - name: "A_sequential_thinking"
        - name: "B_mental_models"
        - name: "C_decision_framework"
          depends_on: ["A_sequential_thinking", "B_mental_models"]
        - name: "D_triple_constraint"
          depends_on: ["C_decision_framework"]
        - name: "E_impact_propagation"
          depends_on: ["B_mental_models"]
      """
    When I execute the workflow
    Then execution order should respect all dependencies
    And parallel execution should occur where possible:
      | batch | tools                               |
      | 1     | A_sequential_thinking, B_mental_models |
      | 2     | C_decision_framework, E_impact_propagation |
      | 3     | D_triple_constraint                    |

  Scenario: Tool failure handling
    Given I have a workflow where the second tool will fail:
      """
      tools:
        - name: "sequential_thinking"
        - name: "invalid_tool_config"
          config: {missing_required_field: null}
        - name: "decision_framework"
          depends_on: ["invalid_tool_config"]
      """
    When I execute the workflow
    Then the first tool should complete successfully
    And the second tool should fail with a clear error
    And the third tool should be skipped due to dependency failure
    And workflow status should be "partial"

  Scenario: Retry mechanism for transient failures
    Given I have a workflow with retry configuration:
      """
      tools:
        - name: "scientific_method"
          retry_count: 3
          timeout_seconds: 5
      """
    And the tool will fail twice then succeed
    When I execute the workflow
    Then the tool should be retried up to 3 times
    And the workflow should ultimately succeed
    And retry attempts should be logged

  Scenario: Data flow between tools
    Given I have a data transformation workflow:
      """
      tools:
        - name: "sequential_thinking"
          config:
            problem: "Design a caching strategy"
        - name: "design_patterns"
          depends_on: ["sequential_thinking"]
          config:
            use_insights_from: "sequential_thinking"
        - name: "triple_constraint"
          depends_on: ["design_patterns"]
          config:
            constraints_from: "design_patterns.recommendations"
      """
    When I execute the workflow
    Then each tool should receive data from its dependencies
    And data transformations should preserve essential information
    And the final result should show clear data lineage

  Scenario: Timeout handling
    Given I have a workflow with strict timing:
      """
      timeout_seconds: 30
      tools:
        - name: "collaborative_reasoning"
          timeout_seconds: 10
          config:
            max_dialogue_rounds: 5
      """
    When I execute the workflow
    And a tool exceeds its timeout
    Then the tool execution should be cancelled
    And an appropriate timeout error should be returned
    And other completed tools' results should be preserved

  Scenario: Circular dependency detection
    Given I have a workflow with circular dependencies:
      """
      tools:
        - name: "A"
          depends_on: ["C"]
        - name: "B"
          depends_on: ["A"]
        - name: "C"
          depends_on: ["B"]
      """
    When I try to create an execution plan
    Then the system should detect the circular dependency
    And provide a clear error message indicating the cycle: A→C→B→A
    And the workflow should not execute

  Scenario: Large workflow optimization
    Given I have a workflow with 10+ tools
    And various dependency patterns
    When I execute the workflow
    Then the execution plan should:
      | optimization                                       |
      | Maximize parallelization opportunities            |
      | Minimize total execution time                     |
      | Balance resource usage across parallel batches    |
      | Provide progress updates during execution         |

  Scenario: Conditional tool execution
    Given I have a workflow with conditional logic:
      """
      tools:
        - name: "decision_framework"
          id: "initial_decision"
        - name: "scientific_method"
          condition: "initial_decision.result.confidence < 0.7"
        - name: "mental_models"
          condition: "initial_decision.result.requires_reframing"
      """
    When I execute the workflow
    Then conditional tools should only run if conditions are met
    And skipped tools should be marked as "skipped" not "failed"
    And the execution should adapt based on intermediate results