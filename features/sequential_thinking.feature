Feature: Sequential Thinking Analyzer
  As a developer using PyClarity
  I want to analyze problems step-by-step with logical reasoning
  So that I can understand complex problems through decomposition

  Background:
    Given the Sequential Thinking analyzer is available
    And the MCP server is running

  Scenario: Basic problem decomposition
    Given I have a complex problem "How to build a scalable microservices architecture"
    And the complexity level is "complex"
    When I analyze the problem with sequential thinking
    Then I should receive a reasoning chain with at least 5 steps
    And each step should have a type from the valid step types
    And the confidence score for each step should be between 0 and 1
    And the final conclusion should synthesize the key insights

  Scenario: Branching logic exploration
    Given I have a problem with multiple solution paths "Should we migrate to cloud or on-premise?"
    And branching is enabled with max branches of 3
    When I analyze the problem with sequential thinking
    Then I should receive multiple reasoning branches
    And each branch should explore a different approach
    And branches should have labels like "cloud-first", "hybrid", "on-premise"
    And each branch should reach its own conclusion

  Scenario: Low confidence revision
    Given I have a problem "Optimize database performance"
    And revision is enabled with confidence threshold 0.7
    When I analyze the problem with sequential thinking
    And some reasoning steps have confidence below 0.7
    Then those steps should be marked for revision
    And revised steps should show improvement attempts
    And the revision explanation should justify the changes

  Scenario: Step type progression
    Given I have a scientific problem "Why do unit tests fail intermittently?"
    When I analyze the problem with sequential thinking
    Then the reasoning chain should follow logical progression:
      | step_number | expected_type        | description                           |
      | 1          | problem_decomposition | Break down the problem components     |
      | 2          | hypothesis_formation  | Form hypotheses about causes          |
      | 3          | evidence_gathering    | Identify what evidence to collect     |
      | 4          | logical_deduction     | Deduce likely causes from evidence    |
      | 5          | validation           | Validate the conclusions              |

  Scenario: Handling simple problems efficiently
    Given I have a simple problem "What is 2 + 2?"
    And the complexity level is "simple"
    When I analyze the problem with sequential thinking
    Then I should receive a concise reasoning chain with 2-3 steps
    And the analysis should not overcomplicate the solution
    And the confidence scores should be high (above 0.9)

  Scenario: Error handling for invalid input
    Given I have an empty problem description ""
    When I try to analyze with sequential thinking
    Then I should receive an error indicating "Problem description cannot be empty"
    And the analysis should not proceed

  Scenario: Maximum depth control
    Given I have a recursive problem "Explain recursion by using recursion"
    And max depth is set to 10
    When I analyze the problem with sequential thinking
    Then the reasoning chain should not exceed 10 steps
    And if truncated, it should indicate "Maximum depth reached"

  Scenario: Integration with other tools
    Given I have a problem requiring multiple perspectives "Design a fault-tolerant payment system"
    When I analyze with sequential thinking
    And the result suggests using other cognitive tools
    Then the recommendations should include relevant tools like:
      | tool_name                  | reason                                    |
      | design_patterns           | For architectural patterns                 |
      | triple_constraint         | For balancing security, speed, cost       |
      | impact_propagation        | For failure cascade analysis              |