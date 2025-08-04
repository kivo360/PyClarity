Feature: Decision Framework Analyzer
  As a decision maker
  I want to evaluate options against multiple criteria
  So that I can make informed decisions with clear rationale

  Background:
    Given the Decision Framework analyzer is available
    And I have a decision to make with multiple options

  Scenario: Multi-criteria decision analysis
    Given I need to decide "Which cloud provider to use"
    And I have these options:
      | option | description                    |
      | AWS    | Amazon Web Services           |
      | Azure  | Microsoft Azure               |
      | GCP    | Google Cloud Platform         |
    And I have these criteria:
      | criterion        | weight | measurement_type |
      | Cost            | 0.3    | quantitative     |
      | Reliability     | 0.25   | qualitative      |
      | Features        | 0.25   | qualitative      |
      | Support         | 0.2    | qualitative      |
    When I analyze the decision
    Then each option should be scored against each criterion
    And weighted scores should be calculated correctly
    And a clear recommendation should be provided
    And rationale should explain the scoring

  Scenario: Sensitivity analysis
    Given I have completed a decision analysis
    When I request sensitivity analysis
    Then I should see:
      | analysis_type           | insight                                |
      | Weight sensitivity      | How changing weights affects outcome   |
      | Score sensitivity       | Which scores most impact the decision  |
      | Break-even points      | When rankings would change             |
      | Robustness measure     | How stable the decision is             |

  Scenario: AHP method for complex decisions
    Given I select the AHP (Analytic Hierarchy Process) method
    And I have criteria that need pairwise comparison
    When I provide comparison matrices
    Then the system should:
      | action                                          |
      | Calculate eigenvectors for weights             |
      | Check consistency ratio < 0.1                  |
      | Flag inconsistent comparisons                  |
      | Derive criteria weights mathematically         |

  Scenario: Consensus building among stakeholders
    Given multiple stakeholders with different preferences:
      | stakeholder | role        | top_priority    | veto_power |
      | CTO        | Technical   | Reliability     | Yes        |
      | CFO        | Financial   | Cost           | Yes        |
      | Dev Team   | Users       | Features       | No         |
    When building consensus
    Then the analysis should:
      | requirement                                    |
      | Weight opinions by stakeholder influence      |
      | Identify potential conflicts                  |
      | Suggest compromise solutions                  |
      | Respect veto power constraints               |

  Scenario: Handling incomplete information
    Given I have options with missing data:
      | option | cost | reliability | features | support |
      | A      | $100 | High       | ?        | Good    |
      | B      | ?    | Medium     | Good     | ?       |
      | C      | $150 | ?          | Excellent| Fair    |
    When analyzing with incomplete information
    Then the system should:
      | action                                         |
      | Use ranges or estimates for missing data      |
      | Calculate confidence intervals                |
      | Highlight uncertainty in recommendations      |
      | Suggest what information to gather            |