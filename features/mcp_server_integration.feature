Feature: MCP Server Integration
  As a client of the PyClarity MCP server
  I want to call cognitive tools through the MCP protocol
  So that I can integrate cognitive analysis into any MCP-compatible system

  Background:
    Given the PyClarity MCP server is running
    And all 16 cognitive tools are registered
    And I have an MCP client connected

  Scenario: Basic tool invocation
    Given I want to analyze a problem with sequential thinking
    When I call the MCP tool "sequential_thinking" with parameters:
      """
      {
        "problem": "How to improve code review process",
        "complexity_level": "moderate",
        "enable_branching": false
      }
      """
    Then I should receive a successful MCP response
    And the response should contain:
      | field                | type        | description                        |
      | reasoning_chain      | array       | Steps of logical reasoning         |
      | key_insights         | array       | Main discoveries                   |
      | confidence_score     | number      | Overall confidence (0-1)           |
      | processing_time_ms   | number      | Execution time                     |

  Scenario: Parameter validation
    Given I want to use the decision framework tool
    When I call "decision_framework" with invalid parameters:
      """
      {
        "decision": "Which database to use",
        "criteria": "not_an_array",
        "options": []
      }
      """
    Then I should receive an MCP error response
    And the error should indicate "criteria must be an array"
    And the error should include parameter requirements

  Scenario: Tool discovery
    When I request the list of available tools
    Then I should receive 16 tool descriptions including:
      | tool_name                    | category          | complexity_support |
      | sequential_thinking          | reasoning         | all levels         |
      | mental_models               | frameworks        | all levels         |
      | decision_framework          | decision_making   | all levels         |
      | triple_constraint          | optimization      | moderate+          |
      | collaborative_reasoning    | multi_perspective | complex+           |

  Scenario: Complex object handling
    Given I want to use collaborative reasoning with multiple personas
    When I call "collaborative_reasoning" with:
      """
      {
        "problem": "Should we adopt microservices?",
        "personas": [
          {
            "name": "DevOps Engineer",
            "persona_type": "implementer",
            "reasoning_style": "practical",
            "background": "10 years managing distributed systems"
          },
          {
            "name": "Product Manager",
            "persona_type": "decision_maker",
            "reasoning_style": "analytical",
            "background": "Focused on time-to-market"
          }
        ],
        "consensus_strategy": "weighted_consensus"
      }
      """
    Then the tool should process all personas correctly
    And return perspectives from each persona
    And attempt consensus building

  Scenario: Async execution handling
    Given I call a long-running tool like "scientific_method"
    With a complex experiment design
    When the tool takes more than 1 second to execute
    Then the MCP server should handle it asynchronously
    And not block other tool calls
    And return results when complete

  Scenario: Error propagation
    Given a tool encounters an internal error
    When I call "design_patterns" with valid parameters
    But the analyzer throws an exception
    Then the MCP response should:
      | requirement                                    |
      | Have error status                             |
      | Include a user-friendly error message         |
      | Not expose internal stack traces              |
      | Suggest corrective actions if possible        |

  Scenario: Result size handling
    Given I use "iterative_validation" with many cycles
    When the tool generates a large result set
    Then the MCP server should:
      | action                                        |
      | Successfully serialize large results          |
      | Maintain result structure integrity           |
      | Not truncate important data                   |
      | Include summary if result is very large       |

  Scenario: Concurrent tool calls
    Given I have multiple MCP clients
    When 5 clients simultaneously call different tools:
      | client | tool                    |
      | 1      | sequential_thinking     |
      | 2      | mental_models          |
      | 3      | decision_framework     |
      | 4      | triple_constraint      |
      | 5      | design_patterns        |
    Then all calls should be processed concurrently
    And each client should receive correct results
    And no cross-contamination should occur

  Scenario: Tool chaining through MCP
    Given I want to chain multiple tools
    When I call "sequential_thinking" first
    And use its output to call "decision_framework"
    And use that output to call "triple_constraint"
    Then each tool should build on previous results
    And maintain context throughout the chain
    And produce progressively refined analysis

  Scenario: MCP protocol compliance
    When I interact with any PyClarity tool
    Then all responses should comply with MCP protocol:
      | requirement                                    |
      | Valid JSON-RPC 2.0 format                     |
      | Correct method names                          |
      | Proper error codes (when applicable)          |
      | Consistent parameter naming                   |
      | Type-safe responses                           |

  Scenario: Graceful degradation
    Given some tools might be temporarily unavailable
    When I call a tool that's currently disabled
    Then I should receive an informative error
    And suggestions for alternative tools
    And the server should remain operational
    And other tools should work normally