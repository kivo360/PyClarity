# Semantic Behavior Testing Guide

## Overview

This guide outlines approaches for defining application behavior ahead of time to ensure AI-generated code maintains intended functionality rather than just passing tests.

## Core Principles

1. **Define behavior BEFORE implementation** - Makes it harder for AI to game the system
2. **Capture stakeholder intent** - Not just technical requirements
3. **Specify what should NOT happen** - Anti-patterns are as important as patterns
4. **Use multiple specification formats** - Different perspectives catch different issues

## Behavior Definition Approaches

### 1. Behavior Specification Language (BSL)

Create YAML/JSON files that formally specify:
- Invariants that must always hold
- Scenarios with given/when/then structure
- Contracts for security and performance
- State consistency requirements

### 2. Example-Driven Behavior

Define golden paths that must work:
- Real user journeys
- Expected state transitions
- Relationships between operations
- Properties that must hold

### 3. Visual Behavior Modeling

Use state diagrams to show:
- Valid state transitions
- Invariants for each state
- Prohibited transitions
- Temporal requirements

### 4. Formal Contracts

Python/TypeScript decorators that specify:
- Preconditions and postconditions
- Invariants across operations
- Temporal requirements
- Conservation laws (e.g., money, inventory)

### 5. Scenario Tables

Markdown tables that capture:
- Input variations
- Expected behaviors
- Explicitly prohibited behaviors
- Edge cases and their handling

### 6. BDD Specifications

Gherkin features that describe:
- User stories and acceptance criteria
- Concrete scenarios
- Background conditions
- Expected outcomes

### 7. Mathematical Specifications

For algorithmic behavior:
- Mathematical properties
- Formulas and constraints
- Verification functions
- Boundary conditions

### 8. Temporal Specifications

For time-dependent behavior:
- State durations
- Timeout handling
- Sequence requirements
- Deadline constraints

### 9. Interactive Tools

Build tools that help capture:
- User stories → behaviors
- Behaviors → test scenarios
- Visual modeling interfaces
- Collaborative editing

### 10. Workshop Outputs

Document collaborative sessions:
- Stakeholder agreements
- Happy paths
- Edge cases
- Anti-behaviors
- Compliance requirements

## Implementation Strategy

### Team Roles

1. **Behavior Engineer** - Facilitates workshops, creates formal specs
2. **Test Architecture Lead** - Converts behaviors to property tests
3. **Integration Specialist** - Ensures behaviors hold across services
4. **Production Engineer** - Validates behaviors with real data
5. **DX Engineer** - Makes behavior specs accessible in IDE
6. **Review Specialist** - Checks implementation matches behavior

### Workflow

1. **Before Sprint**: Define behaviors for upcoming features
2. **During Development**: Use behaviors as implementation guide
3. **Code Review**: Verify behavior compliance
4. **Testing**: Automated behavior verification
5. **Production**: Monitor behavior adherence

## Best Practices

### DO:
- Involve all stakeholders in behavior definition
- Make behaviors testable and measurable
- Version control behavior specifications
- Update behaviors as understanding evolves
- Test for behavior preservation during refactoring

### DON'T:
- Define behaviors after implementation
- Focus only on happy paths
- Ignore temporal or performance aspects
- Allow implicit behavior assumptions
- Let tests define behavior

## Example: User Authentication Behavior

```yaml
behavior: "User Authentication"
invariants:
  - "Passwords never stored plain text"
  - "Failed logins are rate-limited"
  - "Sessions expire after inactivity"

scenarios:
  successful_login:
    given: "Valid user exists"
    when: "Correct credentials provided"
    then: 
      - "Session token generated"
      - "Login event logged"
    not:
      - "Password logged"
      - "Multiple sessions without config"

  brute_force_protection:
    given: "3 failed attempts"
    when: "4th attempt within 15 min"
    then: "Request rejected without checking"
    not: "Password validation performed"
```

## Tools and Resources

- **Behavior Spec Templates**: `/templates/behavior-specs/`
- **Example Specifications**: `/examples/behaviors/`
- **Validation Tools**: `pyclarity test:behaviors`
- **IDE Integration**: Install "Behavior Spec" extension

## Getting Started

1. Choose a feature to specify
2. Gather stakeholders
3. Use workshop template
4. Document behaviors
5. Create automated tests
6. Review with team

## Measuring Success

- Percentage of features with behavior specs
- AI-generated code rejection rate
- Production incidents from behavior violations
- Time to detect behavior drift
- Developer satisfaction with specs

---

*This guide is part of the PyClarity semantic testing initiative to ensure AI-generated code serves its intended purpose.*