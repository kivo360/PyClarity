Feature: Mental Models Framework
  As a problem solver
  I want to apply different mental models to my challenges
  So that I can gain deeper insights through structured thinking

  Background:
    Given the Mental Models analyzer is available
    And I understand the available mental model types

  Scenario: First Principles thinking
    Given I have a complex problem "Reduce cloud infrastructure costs by 50%"
    And I select the "first_principles" mental model
    When I apply the mental model
    Then the analysis should:
      | step                    | example                                    |
      | Question assumptions    | Why do we need all these servers?         |
      | Break to fundamentals   | Core need: Compute, Storage, Network       |
      | Identify root truths    | Users active 8 hours/day, 5 days/week     |
      | Rebuild from basics     | Serverless for variable load              |
    And provide actionable insights based on fundamental truths

  Scenario: Opportunity Cost analysis
    Given I need to decide "Hire 2 senior devs vs 4 junior devs"
    And I select the "opportunity_cost" mental model
    When analyzing the opportunity costs
    Then I should see:
      | choice              | gives_up                            | gains                          |
      | 2 senior devs      | Larger team size, training culture  | Immediate productivity         |
      | 4 junior devs      | Quick expertise, less mentoring     | Growth potential, fresh ideas  |
    And hidden opportunity costs should be revealed
    And long-term vs short-term trade-offs clarified

  Scenario: Error Propagation understanding
    Given I have a system issue "One microservice is returning slow responses"
    And I select the "error_propagation" mental model
    When I trace the error propagation
    Then the analysis should show:
      | propagation_level | impact                                   |
      | Direct           | API gateway timeout                       |
      | First-order      | Client retries overwhelming system        |
      | Second-order     | Cache invalidation cascade                |
      | System-wide      | Overall degraded user experience          |
    And suggest intervention points to break the chain

  Scenario: Pareto Principle application
    Given I want to optimize "Customer support ticket resolution"
    And I select the "pareto_principle" mental model
    When analyzing with 80/20 rule
    Then the system should identify:
      | finding                                        |
      | 20% of issue types causing 80% of tickets     |
      | 20% of customers generating 80% of workload   |
      | 20% of features causing 80% of confusion      |
    And prioritize improvements based on impact
    And quantify expected results from focusing on vital few

  Scenario: Occam's Razor for solution selection
    Given multiple explanations for "Website conversion dropped 30%"
    And theories include:
      | theory                | complexity | assumptions |
      | Payment bug          | Simple     | 1           |
      | Market shift         | Complex    | 5           |
      | Competitor actions   | Medium     | 3           |
      | UI/UX issues        | Medium     | 4           |
    When applying "occams_razor" mental model
    Then the analysis should:
      | action                                         |
      | Rank theories by simplicity                   |
      | Highlight testable predictions                |
      | Suggest verification order                    |
      | Warn against premature complexity            |

  Scenario: Combining multiple mental models
    Given a strategic problem "Enter new market segment"
    When I request multi-model analysis
    Then the system should apply relevant models:
      | model              | insight_type                          |
      | first_principles   | Core market needs                     |
      | opportunity_cost   | Resource allocation trade-offs        |
      | pareto_principle   | Focus areas for maximum impact        |
    And show how different models complement each other
    And synthesize insights into cohesive strategy