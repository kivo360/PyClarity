Feature: Triple Constraint Optimization
  As a project manager or developer
  I want to balance competing constraints in my projects
  So that I can find optimal trade-offs between scope, time, and cost

  Background:
    Given the Triple Constraint Optimization analyzer is available
    And I have defined my project constraints

  Scenario: Basic constraint balancing
    Given I have these constraints for a "software development" project:
      | constraint | current_value | flexibility | priority |
      | scope      | 10 features   | low         | high     |
      | time       | 3 months      | medium      | medium   |
      | cost       | $50,000       | high        | low      |
    When I request constraint optimization
    Then I should receive at least 3 optimization scenarios
    And each scenario should show different trade-offs
    And scenarios should be ranked by success probability

  Scenario: Domain-specific optimization
    Given I am working in the "e-commerce platform" domain
    And I have standard e-commerce constraints
    When I request optimization with domain context
    Then the analysis should apply e-commerce-specific patterns
    And constraints should include domain factors like:
      | factor              | consideration                    |
      | seasonal_traffic    | Black Friday scaling needs      |
      | payment_compliance  | PCI-DSS requirements           |
      | mobile_first        | 60%+ mobile user expectations  |

  Scenario: Trade-off impact analysis
    Given I have identified a critical trade-off:
      | from_constraint | to_constraint | trade_amount    |
      | scope          | time          | -2 features     |
      | time           | cost          | +1 month        |
    When I analyze the trade-off impacts
    Then I should see cascading effects:
      | impact_area      | effect                                |
      | team_morale      | Positive - less rushed development   |
      | market_timing    | Negative - competitor advantage      |
      | quality          | Positive - more testing time         |
      | budget_overrun   | Risk - additional month costs        |

  Scenario: Optimal scenario selection
    Given I have these optimization criteria:
      | criterion           | weight |
      | success_probability | 0.4    |
      | stakeholder_buy_in  | 0.3    |
      | risk_mitigation     | 0.3    |
    When I evaluate 5 different scenarios
    Then the optimal scenario should:
      | requirement                                    |
      | Have the highest weighted score               |
      | Include clear implementation steps            |
      | Show success probability > 0.7                |
      | Address all critical constraints              |

  Scenario: Resource optimization
    Given I have limited resources:
      | resource         | available | required |
      | developers       | 5         | 8        |
      | budget           | $40k      | $50k     |
      | timeline         | 2 months  | 3 months |
    When I request resource-aware optimization
    Then scenarios should only use available resources
    And trade-offs should focus on "doing more with less"
    And each scenario should be achievable within limits

  Scenario: Stakeholder-specific views
    Given I have multiple stakeholders:
      | stakeholder | primary_concern      | flexibility |
      | CEO         | time-to-market      | low         |
      | CTO         | technical quality   | medium      |
      | CFO         | budget control      | low         |
      | Users       | feature completeness| high        |
    When I generate optimization scenarios
    Then each scenario should include stakeholder impact analysis
    And recommendations should address each stakeholder's concerns
    And consensus-building strategies should be provided

  Scenario: Constraint violation detection
    Given I have hard constraints:
      | constraint      | limit        | type |
      | budget          | $100k max    | hard |
      | launch_date     | Q2 2024      | hard |
      | compliance      | GDPR ready   | hard |
    When I analyze proposed changes that violate constraints
    Then the system should:
      | action                                          |
      | Flag constraint violations clearly              |
      | Explain why the constraint cannot be violated   |
      | Suggest alternative approaches                  |
      | Quantify the cost of relaxing each constraint   |

  Scenario: Historical pattern application
    Given I have project type "mobile app development"
    And historical data shows common patterns
    When I request optimization
    Then the analysis should reference relevant patterns:
      | pattern                    | typical_outcome              |
      | scope_creep               | 30% timeline extension       |
      | ios_android_parallel      | 1.5x resource requirement   |
      | app_store_review          | 2-week buffer needed        |

  Scenario: Dynamic constraint adjustment
    Given I am mid-project with these changes:
      | event                    | impact                    |
      | key_developer_left      | -20% velocity            |
      | competitor_launched     | time pressure increased   |
      | budget_approved         | +$20k available          |
    When I request re-optimization
    Then new scenarios should reflect the changed reality
    And recommendations should focus on recovery strategies
    And risk mitigation should be prioritized

  Scenario: Success metrics definition
    Given I select an optimization scenario
    When I request success metrics
    Then I should receive measurable KPIs:
      | metric                 | target      | measurement_method           |
      | on_time_delivery      | 95%         | milestone tracking           |
      | budget_variance       | <5%         | weekly cost reports          |
      | scope_completion      | 90%         | feature acceptance           |
      | quality_score         | >8/10       | defect density + user feedback|