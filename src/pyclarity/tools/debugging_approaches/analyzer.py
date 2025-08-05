"""
Debugging Approaches Analyzer

Core implementation of the debugging approaches cognitive tool, providing
systematic troubleshooting methodologies, error classification and resolution,
debugging strategy selection, and root cause analysis frameworks.
"""

import asyncio
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from .models import (
    DebugContext,
    DebuggingApproachesContext,
    DebuggingApproachesResult,
    DebuggingHypothesis,
    DebuggingPhase,
    DebuggingRecommendation,
    DebuggingSession,
    DebuggingStep,
    DebuggingStrategy,
    ErrorCategory,
    ErrorClassification,
    RootCauseAnalysis,
    Severity,
)


class DebuggingApproachesAnalyzer:
    """Debugging approaches cognitive tool analyzer"""

    def __init__(self):
        """Initialize the debugging approaches analyzer"""
        self.tool_name = "Debugging Approaches"
        self.version = "1.0.0"

        # Internal state for processing
        self._processing_start_time = 0.0

        # Initialize strategy profiles
        self._initialize_strategy_profiles()

    def _initialize_strategy_profiles(self):
        """Initialize profiles for different debugging strategies"""
        self.strategy_profiles = {
            DebuggingStrategy.PRINT_DEBUGGING: {
                "description": "Adding print statements to trace program execution",
                "best_for": ["Simple logic errors", "Value tracking", "Flow verification"],
                "effectiveness": 0.7,
                "time_cost": "low",
                "tool_requirements": ["text editor", "console output"],
                "limitations": ["Code pollution", "Performance impact", "Not suitable for production"],
                "error_categories": [ErrorCategory.LOGIC_ERROR, ErrorCategory.RUNTIME_ERROR]
            },

            DebuggingStrategy.INTERACTIVE_DEBUGGING: {
                "description": "Using debugger to step through code execution",
                "best_for": ["Complex logic errors", "State inspection", "Runtime behavior"],
                "effectiveness": 0.9,
                "time_cost": "medium",
                "tool_requirements": ["debugger", "IDE", "symbol information"],
                "limitations": ["Setup overhead", "Tool dependency", "May alter timing"],
                "error_categories": [ErrorCategory.LOGIC_ERROR, ErrorCategory.RUNTIME_ERROR, ErrorCategory.MEMORY_ERROR]
            },

            DebuggingStrategy.LOG_ANALYSIS: {
                "description": "Analyzing application logs to identify issues",
                "best_for": ["Production issues", "Historical analysis", "Pattern identification"],
                "effectiveness": 0.75,
                "time_cost": "low",
                "tool_requirements": ["log viewer", "grep/search tools", "log aggregation"],
                "limitations": ["Depends on log quality", "May miss context", "Large data volumes"],
                "error_categories": [ErrorCategory.INTEGRATION_ERROR, ErrorCategory.CONFIGURATION_ERROR, ErrorCategory.PERFORMANCE_ERROR]
            },

            DebuggingStrategy.BINARY_SEARCH: {
                "description": "Systematically narrowing down error location",
                "best_for": ["Large codebases", "Integration errors", "Regression bugs"],
                "effectiveness": 0.8,
                "time_cost": "medium",
                "tool_requirements": ["version control", "build system"],
                "limitations": ["Requires reproducible error", "May be time-intensive"],
                "error_categories": [ErrorCategory.INTEGRATION_ERROR, ErrorCategory.LOGIC_ERROR]
            },

            DebuggingStrategy.RUBBER_DUCK: {
                "description": "Explaining the problem aloud to identify solutions",
                "best_for": ["Logic errors", "Design issues", "Conceptual problems"],
                "effectiveness": 0.6,
                "time_cost": "low",
                "tool_requirements": ["none"],
                "limitations": ["Depends on explanation skills", "May not work for complex issues"],
                "error_categories": [ErrorCategory.LOGIC_ERROR, ErrorCategory.SYNTAX_ERROR]
            },

            DebuggingStrategy.UNIT_TESTING: {
                "description": "Creating targeted tests to isolate problems",
                "best_for": ["Logic errors", "Regression prevention", "Component validation"],
                "effectiveness": 0.85,
                "time_cost": "medium",
                "tool_requirements": ["testing framework", "test runner"],
                "limitations": ["Requires test writing skills", "Initial setup time"],
                "error_categories": [ErrorCategory.LOGIC_ERROR, ErrorCategory.RUNTIME_ERROR]
            },

            DebuggingStrategy.INTEGRATION_TESTING: {
                "description": "Testing interactions between system components",
                "best_for": ["Integration errors", "API issues", "System-level problems"],
                "effectiveness": 0.8,
                "time_cost": "high",
                "tool_requirements": ["test environment", "integration tools", "monitoring"],
                "limitations": ["Complex setup", "Environment dependencies", "Time intensive"],
                "error_categories": [ErrorCategory.INTEGRATION_ERROR, ErrorCategory.CONFIGURATION_ERROR]
            },

            DebuggingStrategy.PROFILING: {
                "description": "Analyzing performance characteristics and resource usage",
                "best_for": ["Performance issues", "Memory problems", "Resource bottlenecks"],
                "effectiveness": 0.9,
                "time_cost": "medium",
                "tool_requirements": ["profiler", "performance tools", "monitoring"],
                "limitations": ["Tool overhead", "May alter behavior", "Complex analysis"],
                "error_categories": [ErrorCategory.PERFORMANCE_ERROR, ErrorCategory.MEMORY_ERROR]
            },

            DebuggingStrategy.STATIC_ANALYSIS: {
                "description": "Analyzing code without executing it",
                "best_for": ["Code quality", "Potential bugs", "Security issues"],
                "effectiveness": 0.7,
                "time_cost": "low",
                "tool_requirements": ["static analysis tools", "linters", "code scanners"],
                "limitations": ["False positives", "Limited runtime context", "Tool configuration"],
                "error_categories": [ErrorCategory.SYNTAX_ERROR, ErrorCategory.LOGIC_ERROR, ErrorCategory.MEMORY_ERROR]
            },

            DebuggingStrategy.CODE_REVIEW: {
                "description": "Systematic examination of code by peers",
                "best_for": ["Code quality", "Logic errors", "Best practices"],
                "effectiveness": 0.75,
                "time_cost": "medium",
                "tool_requirements": ["code review tools", "team collaboration"],
                "limitations": ["Requires team expertise", "Time coordinating", "Subjective"],
                "error_categories": [ErrorCategory.LOGIC_ERROR, ErrorCategory.SYNTAX_ERROR]
            },

            DebuggingStrategy.DIVIDE_AND_CONQUER: {
                "description": "Breaking down complex problems into smaller parts",
                "best_for": ["Complex systems", "Multiple symptoms", "System-wide issues"],
                "effectiveness": 0.8,
                "time_cost": "medium",
                "tool_requirements": ["modular architecture", "isolation capabilities"],
                "limitations": ["Requires good system design", "May miss interactions"],
                "error_categories": [ErrorCategory.INTEGRATION_ERROR, ErrorCategory.LOGIC_ERROR, ErrorCategory.PERFORMANCE_ERROR]
            },

            DebuggingStrategy.HYPOTHESIS_TESTING: {
                "description": "Forming and testing specific hypotheses about the problem",
                "best_for": ["Complex issues", "Multiple possible causes", "Scientific approach"],
                "effectiveness": 0.85,
                "time_cost": "medium",
                "tool_requirements": ["testing capabilities", "measurement tools"],
                "limitations": ["Requires hypothesis formation skills", "Time intensive"],
                "error_categories": [ErrorCategory.LOGIC_ERROR, ErrorCategory.PERFORMANCE_ERROR, ErrorCategory.INTEGRATION_ERROR]
            }
        }

    async def analyze(self, context: DebuggingApproachesContext) -> DebuggingApproachesResult:
        """
        Analyze debugging approaches for the given context.

        Args:
            context: Debugging approaches context with problem description and constraints

        Returns:
            DebuggingApproachesResult with debugging analysis and recommendations
        """
        self._processing_start_time = time.time()

        # Phase 1: Classify the error
        error_classification = await self._classify_error(context)

        # Phase 2: Generate debugging recommendations
        debugging_recommendations = await self._generate_debugging_recommendations(
            error_classification, context
        )

        # Phase 3: Create debugging session structure
        debugging_session = await self._create_debugging_session(
            error_classification, context
        )

        # Phase 4: Root cause analysis (if enabled)
        root_cause_analysis = None
        if context.include_root_cause_analysis:
            root_cause_analysis = await self._perform_root_cause_analysis(
                context.problem_description, context.error_symptoms
            )

        # Phase 5: Generate debugging roadmap
        debugging_roadmap = self._generate_debugging_roadmap(
            error_classification, debugging_recommendations
        )

        # Phase 6: Generate prevention measures (if enabled)
        prevention_measures = []
        if context.include_prevention_measures:
            prevention_measures = self._generate_prevention_measures(
                error_classification, root_cause_analysis
            )

        # Phase 7: Generate additional recommendations
        risk_assessment = self._generate_risk_assessment(
            error_classification, debugging_recommendations
        )

        tool_recommendations = self._generate_tool_recommendations(
            debugging_recommendations, context.available_tools
        )

        best_practices = self._generate_best_practices(error_classification)

        learning_opportunities = self._generate_learning_opportunities(
            error_classification, debugging_recommendations
        )

        # Calculate processing time
        processing_time = time.time() - self._processing_start_time

        return DebuggingApproachesResult(
            error_classification=error_classification,
            debugging_recommendations=debugging_recommendations[:context.max_strategy_recommendations],
            debugging_session=debugging_session,
            root_cause_analysis=root_cause_analysis,
            top_recommended_strategy=debugging_recommendations[0].recommended_strategy.value if debugging_recommendations else None,
            strategy_effectiveness_scores={
                rec.recommended_strategy.value: rec.expected_effectiveness
                for rec in debugging_recommendations
            },
            debugging_roadmap=debugging_roadmap,
            prevention_measures=prevention_measures,
            risk_assessment=risk_assessment,
            tool_recommendations=tool_recommendations,
            best_practices=best_practices,
            learning_opportunities=learning_opportunities,
            processing_time_ms=round(processing_time * 1000)
        )

    async def _classify_error(self, context: DebuggingApproachesContext) -> ErrorClassification:
        """Classify the error based on context information"""
        # Simulate processing delay
        await asyncio.sleep(0.05)

        # Determine error category
        category = self._determine_error_category(
            context.problem_description,
            context.error_symptoms,
            context.environment_details
        )

        # Assess severity
        severity = context.impact_level

        # Generate potential causes
        potential_causes = self._generate_potential_causes(category, context.error_symptoms)

        # Assess reproducibility and frequency
        reproducibility = self._assess_reproducibility(context.error_symptoms, context.reproduction_steps)
        frequency = self._assess_frequency(context.error_symptoms)

        # Identify affected components
        affected_components = self._identify_affected_components(
            context.problem_description, context.system_context
        )

        return ErrorClassification(
            error_category=category,
            severity=severity,
            error_message=None,  # Would be extracted from context if available
            stack_trace=None,    # Would be extracted from context if available
            symptoms=context.error_symptoms,
            potential_causes=potential_causes,
            affected_components=affected_components,
            frequency=frequency,
            reproducibility=reproducibility,
            confidence_level=0.8  # Base confidence
        )

    def _determine_error_category(
        self,
        description: str,
        symptoms: list[str],
        environment: dict[str, str]
    ) -> ErrorCategory:
        """Determine the category of error based on available information"""
        description_lower = description.lower()
        symptoms_text = " ".join(symptoms).lower()
        combined_text = f"{description_lower} {symptoms_text}"

        # Check for specific error patterns
        if any(word in combined_text for word in ["syntax", "parse", "compilation", "compiler error"]):
            return ErrorCategory.SYNTAX_ERROR

        if any(word in combined_text for word in ["null pointer", "segmentation fault", "access violation", "crash", "exception"]):
            return ErrorCategory.RUNTIME_ERROR

        if any(word in combined_text for word in ["performance", "slow", "timeout", "latency", "bottleneck"]):
            return ErrorCategory.PERFORMANCE_ERROR

        if any(word in combined_text for word in ["memory", "heap", "stack overflow", "out of memory", "leak"]):
            return ErrorCategory.MEMORY_ERROR

        if any(word in combined_text for word in ["deadlock", "race condition", "concurrent", "thread", "synchronization"]):
            return ErrorCategory.CONCURRENCY_ERROR

        if any(word in combined_text for word in ["config", "configuration", "setting", "property", "environment"]):
            return ErrorCategory.CONFIGURATION_ERROR

        if any(word in combined_text for word in ["integration", "api", "service", "connection", "network"]):
            return ErrorCategory.INTEGRATION_ERROR

        if any(word in combined_text for word in ["user input", "validation", "form", "input error"]):
            return ErrorCategory.USER_INPUT_ERROR

        if any(word in combined_text for word in ["environment", "deployment", "system", "platform"]):
            return ErrorCategory.ENVIRONMENT_ERROR

        # Default to logic error if no specific pattern matches
        return ErrorCategory.LOGIC_ERROR

    def _generate_potential_causes(self, category: ErrorCategory, symptoms: list[str]) -> list[str]:
        """Generate potential causes based on error category and symptoms"""
        cause_patterns = {
            ErrorCategory.SYNTAX_ERROR: [
                "Missing semicolon or bracket",
                "Incorrect syntax usage",
                "Typo in keyword or identifier",
                "Wrong indentation or formatting"
            ],
            ErrorCategory.RUNTIME_ERROR: [
                "Null pointer dereference",
                "Array index out of bounds",
                "Invalid type casting",
                "Resource not available",
                "Unhandled exception"
            ],
            ErrorCategory.LOGIC_ERROR: [
                "Incorrect algorithm implementation",
                "Wrong conditional logic",
                "Off-by-one error",
                "Incorrect variable usage",
                "Missing edge case handling"
            ],
            ErrorCategory.PERFORMANCE_ERROR: [
                "Inefficient algorithm",
                "Memory leaks",
                "Excessive database queries",
                "Unoptimized loops",
                "Resource contention"
            ],
            ErrorCategory.MEMORY_ERROR: [
                "Memory leaks",
                "Buffer overflow",
                "Stack overflow from recursion",
                "Insufficient heap space",
                "Double free or use after free"
            ],
            ErrorCategory.CONCURRENCY_ERROR: [
                "Race conditions",
                "Deadlocks",
                "Thread safety violations",
                "Improper synchronization",
                "Resource sharing conflicts"
            ],
            ErrorCategory.CONFIGURATION_ERROR: [
                "Incorrect configuration values",
                "Missing configuration files",
                "Environment variable issues",
                "Path or dependency problems",
                "Version mismatches"
            ],
            ErrorCategory.INTEGRATION_ERROR: [
                "API version mismatches",
                "Network connectivity issues",
                "Authentication/authorization problems",
                "Data format incompatibilities",
                "Service unavailability"
            ],
            ErrorCategory.USER_INPUT_ERROR: [
                "Invalid input format",
                "Missing input validation",
                "Boundary condition violations",
                "Encoding issues",
                "Input sanitization problems"
            ],
            ErrorCategory.ENVIRONMENT_ERROR: [
                "Operating system differences",
                "Missing dependencies",
                "Permission issues",
                "Resource limitations",
                "Platform-specific behaviors"
            ]
        }

        return cause_patterns.get(category, ["Unknown cause pattern"])

    def _assess_reproducibility(self, symptoms: list[str], reproduction_steps: list[str]) -> str:
        """Assess how reproducible the error is"""
        symptoms_text = " ".join(symptoms).lower()
        steps_text = " ".join(reproduction_steps).lower()
        combined_text = f"{symptoms_text} {steps_text}"

        if any(word in combined_text for word in ["always", "every time", "consistently", "reproducible"]):
            return "always"
        elif any(word in combined_text for word in ["sometimes", "intermittent", "occasionally", "sporadic"]):
            return "sometimes"
        elif any(word in combined_text for word in ["never", "cannot reproduce", "one time", "random"]):
            return "never"
        elif reproduction_steps:
            return "always"  # If steps are provided, assume reproducible
        else:
            return "sometimes"  # Default assumption

    def _assess_frequency(self, symptoms: list[str]) -> str:
        """Assess how frequently the error occurs"""
        symptoms_text = " ".join(symptoms).lower()

        if any(word in symptoms_text for word in ["constant", "continuous", "always", "every time"]):
            return "constant"
        elif any(word in symptoms_text for word in ["frequent", "often", "regular", "common"]):
            return "frequent"
        elif any(word in symptoms_text for word in ["occasional", "sometimes", "sporadic", "intermittent"]):
            return "occasional"
        else:
            return "rare"

    def _identify_affected_components(self, description: str, system_context: str) -> list[str]:
        """Identify which components are affected by the error"""
        components = []
        text = f"{description} {system_context}".lower()

        # Common component patterns
        component_keywords = {
            "database": ["database", "sql", "query", "table", "db"],
            "user_interface": ["ui", "interface", "frontend", "view", "form", "screen"],
            "backend_service": ["api", "service", "backend", "server", "endpoint"],
            "network": ["network", "connection", "http", "tcp", "socket"],
            "authentication": ["auth", "login", "security", "token", "session"],
            "file_system": ["file", "disk", "storage", "path", "directory"],
            "memory": ["memory", "ram", "heap", "stack", "cache"],
            "configuration": ["config", "settings", "properties", "environment"]
        }

        for component, keywords in component_keywords.items():
            if any(keyword in text for keyword in keywords):
                components.append(component)

        return components if components else ["unknown"]

    async def _generate_debugging_recommendations(
        self,
        error_classification: ErrorClassification,
        context: DebuggingApproachesContext
    ) -> list[DebuggingRecommendation]:
        """Generate debugging strategy recommendations"""
        # Simulate processing delay
        await asyncio.sleep(0.1)

        recommendations = []

        for strategy, profile in self.strategy_profiles.items():
            match_score = self._calculate_strategy_match(
                strategy, profile, error_classification, context
            )

            if match_score > 0.3:  # Threshold for consideration
                recommendation = DebuggingRecommendation(
                    recommended_strategy=strategy,
                    context_match_score=match_score,
                    reasoning=self._generate_strategy_reasoning(strategy, profile, error_classification),
                    expected_effectiveness=profile["effectiveness"] * match_score,
                    estimated_time=profile["time_cost"],
                    required_tools=profile["tool_requirements"],
                    prerequisites=self._get_strategy_prerequisites(strategy),
                    alternative_strategies=self._get_alternative_strategies(strategy),
                    risk_factors=profile.get("limitations", [])
                )
                recommendations.append(recommendation)

        # Sort by expected effectiveness
        return sorted(recommendations, key=lambda x: x.expected_effectiveness, reverse=True)

    def _calculate_strategy_match(
        self,
        strategy: DebuggingStrategy,
        profile: dict[str, Any],
        classification: ErrorClassification,
        context: DebuggingApproachesContext
    ) -> float:
        """Calculate how well a strategy matches the current situation"""
        score = 0.5  # Base score

        # Check if strategy is good for this error category
        if classification.error_category in profile.get("error_categories", []):
            score += 0.3

        # Check tool availability
        required_tools = profile.get("tool_requirements", [])
        available_tools_lower = [tool.lower() for tool in context.available_tools]

        if required_tools:
            available_count = sum(
                1 for tool in required_tools
                if any(tool.lower() in available_tool for available_tool in available_tools_lower)
            )
            tool_availability = available_count / len(required_tools)
            score += tool_availability * 0.2
        else:
            score += 0.2  # No tools required

        # Consider time constraints
        if context.time_constraints:
            if "urgent" in context.time_constraints.lower():
                if profile["time_cost"] == "low":
                    score += 0.2
                elif profile["time_cost"] == "high":
                    score -= 0.2

        # Consider team expertise
        strategy_name = strategy.value.replace('_', ' ')
        if any(strategy_name in expertise.lower() for expertise in context.team_expertise):
            score += 0.1

        # Consider previous attempts
        if any(strategy_name in attempt.lower() for attempt in context.previous_attempts):
            score -= 0.1  # Penalize already tried strategies

        return min(1.0, max(0.0, score))

    def _generate_strategy_reasoning(
        self,
        strategy: DebuggingStrategy,
        profile: dict[str, Any],
        classification: ErrorClassification
    ) -> str:
        """Generate reasoning for why a strategy is recommended"""
        strategy_name = strategy.value.replace('_', ' ').title()
        category_name = classification.error_category.value.replace('_', ' ')
        effectiveness = profile['effectiveness'] * 100

        return (f"{strategy_name} is recommended because it is highly effective for "
                f"{category_name} issues ({effectiveness:.0f}% success rate). "
                f"{profile['description']}. This approach is particularly suitable "
                f"when you need {', '.join(profile['best_for'][:2]).lower()}.")

    def _get_strategy_prerequisites(self, strategy: DebuggingStrategy) -> list[str]:
        """Get prerequisites for a debugging strategy"""
        prerequisites_map = {
            DebuggingStrategy.INTERACTIVE_DEBUGGING: [
                "Debugger setup and configuration",
                "Symbol information available",
                "Reproducible error condition",
                "Understanding of debugging commands"
            ],
            DebuggingStrategy.UNIT_TESTING: [
                "Testing framework setup",
                "Test writing skills",
                "Isolated test environment",
                "Understanding of test patterns"
            ],
            DebuggingStrategy.PROFILING: [
                "Profiling tools installation",
                "Performance baseline established",
                "Representative workload available",
                "Profiler interpretation skills"
            ],
            DebuggingStrategy.STATIC_ANALYSIS: [
                "Static analysis tools configured",
                "Code access and build setup",
                "Rule configuration understanding",
                "False positive filtering skills"
            ],
            DebuggingStrategy.LOG_ANALYSIS: [
                "Access to relevant logs",
                "Log analysis tools",
                "Understanding of log formats",
                "Pattern recognition skills"
            ],
            DebuggingStrategy.CODE_REVIEW: [
                "Team coordination",
                "Code review process established",
                "Domain expertise available",
                "Collaborative review tools"
            ]
        }

        return prerequisites_map.get(strategy, ["Basic understanding of the system and codebase"])

    def _get_alternative_strategies(self, strategy: DebuggingStrategy) -> list[DebuggingStrategy]:
        """Get alternative strategies for a given strategy"""
        alternatives_map = {
            DebuggingStrategy.PRINT_DEBUGGING: [
                DebuggingStrategy.INTERACTIVE_DEBUGGING,
                DebuggingStrategy.LOG_ANALYSIS,
                DebuggingStrategy.UNIT_TESTING
            ],
            DebuggingStrategy.INTERACTIVE_DEBUGGING: [
                DebuggingStrategy.PRINT_DEBUGGING,
                DebuggingStrategy.UNIT_TESTING,
                DebuggingStrategy.LOG_ANALYSIS
            ],
            DebuggingStrategy.UNIT_TESTING: [
                DebuggingStrategy.INTEGRATION_TESTING,
                DebuggingStrategy.INTERACTIVE_DEBUGGING,
                DebuggingStrategy.STATIC_ANALYSIS
            ],
            DebuggingStrategy.PROFILING: [
                DebuggingStrategy.LOG_ANALYSIS,
                DebuggingStrategy.STATIC_ANALYSIS,
                DebuggingStrategy.HYPOTHESIS_TESTING
            ],
            DebuggingStrategy.LOG_ANALYSIS: [
                DebuggingStrategy.PROFILING,
                DebuggingStrategy.STATIC_ANALYSIS,
                DebuggingStrategy.BINARY_SEARCH
            ]
        }

        return alternatives_map.get(strategy, [])

    async def _create_debugging_session(
        self,
        error_classification: ErrorClassification,
        context: DebuggingApproachesContext
    ) -> DebuggingSession:
        """Create a structured debugging session"""
        # Simulate processing delay
        await asyncio.sleep(0.05)

        # Create debug context
        debug_context = DebugContext(
            system_description=context.system_context,
            environment=context.environment_details,
            error_symptoms=context.error_symptoms,
            reproduction_steps=context.reproduction_steps,
            constraints=context.available_tools,
            available_tools=context.available_tools,
            time_constraints=context.time_constraints,
            impact_assessment=f"Impact level: {context.impact_level.value}"
        )

        # Generate initial hypotheses
        hypotheses = self._generate_initial_hypotheses(error_classification)

        # Create debugging steps
        debugging_steps = self._create_debugging_steps(error_classification, context)

        return DebuggingSession(
            context=debug_context,
            error_classification=error_classification,
            hypotheses=hypotheses,
            debugging_steps=debugging_steps,
            root_cause_analysis=None,
            resolution=None,
            lessons_learned=[],
            prevention_recommendations=[],
            session_duration=None,
            success_rate=0.0
        )

    def _generate_initial_hypotheses(self, classification: ErrorClassification) -> list[DebuggingHypothesis]:
        """Generate initial hypotheses based on error classification"""
        hypotheses = []

        for i, cause in enumerate(classification.potential_causes[:3]):  # Top 3 causes
            confidence = 0.8 - (i * 0.15)  # Decreasing confidence

            hypothesis = DebuggingHypothesis(
                description=f"The error is caused by: {cause}",
                confidence_level=confidence,
                supporting_evidence=classification.symptoms[:2],
                contradicting_evidence=[],
                test_plan=[
                    f"Test hypothesis: {cause}",
                    "Collect evidence through targeted investigation",
                    "Verify or refute through systematic testing",
                    "Document findings and adjust confidence"
                ],
                estimated_effort="medium" if i == 0 else "low",
                risk_level="low",
                alternative_hypotheses=classification.potential_causes[i+1:i+3] if i < 2 else []
            )
            hypotheses.append(hypothesis)

        return hypotheses

    def _create_debugging_steps(
        self,
        classification: ErrorClassification,
        context: DebuggingApproachesContext
    ) -> list[DebuggingStep]:
        """Create initial debugging steps"""
        steps = []

        # Step 1: Problem verification
        steps.append(DebuggingStep(
            phase=DebuggingPhase.PROBLEM_IDENTIFICATION,
            description="Verify and document the problem thoroughly",
            strategy_used=DebuggingStrategy.LOG_ANALYSIS,
            expected_outcome="Clear understanding of problem scope and symptoms",
            actual_outcome=None,
            tools_used=["logs", "error reports", "monitoring"],
            evidence_gathered=[],
            time_spent=None,
            success=None,
            next_steps=["Attempt to reproduce the problem", "Gather additional context"]
        ))

        # Step 2: Reproduction
        if context.reproduction_steps:
            steps.append(DebuggingStep(
                phase=DebuggingPhase.REPRODUCTION,
                description="Reproduce the problem using known steps",
                strategy_used=DebuggingStrategy.HYPOTHESIS_TESTING,
                expected_outcome="Consistent reproduction of the error",
                actual_outcome=None,
                tools_used=["test environment", "reproduction scripts"],
                evidence_gathered=[],
                time_spent=None,
                success=None,
                next_steps=["Isolate the problem area", "Analyze error patterns"]
            ))

        # Step 3: Isolation
        steps.append(DebuggingStep(
            phase=DebuggingPhase.ISOLATION,
            description="Isolate the problem to specific components or code areas",
            strategy_used=DebuggingStrategy.DIVIDE_AND_CONQUER,
            expected_outcome="Narrowed down problem location",
            actual_outcome=None,
            tools_used=["debugging tools", "component testing"],
            evidence_gathered=[],
            time_spent=None,
            success=None,
            next_steps=["Analyze isolated components", "Form specific hypotheses"]
        ))

        return steps

    async def _perform_root_cause_analysis(
        self,
        problem_statement: str,
        evidence: list[str]
    ) -> RootCauseAnalysis:
        """Perform root cause analysis using Five Whys method"""
        # Simulate processing delay
        await asyncio.sleep(0.05)

        # Generate root causes based on evidence
        root_causes = [
            "Insufficient error handling and validation",
            "Lack of proper testing coverage",
            "Design assumptions that don't hold in production"
        ]

        contributing_factors = [
            "Time pressure during development",
            "Incomplete understanding of requirements",
            "Limited testing in production-like environments",
            "Insufficient code review processes"
        ]

        prevention_measures = [
            "Implement comprehensive error handling at all levels",
            "Increase test coverage including edge cases",
            "Establish thorough code review processes",
            "Improve requirements gathering and validation",
            "Create better testing environments that mirror production"
        ]

        systemic_issues = [
            "Development process maturity gaps",
            "Quality assurance methodology weaknesses",
            "Communication and collaboration improvements needed"
        ]

        return RootCauseAnalysis(
            problem_statement=problem_statement,
            root_causes=root_causes,
            contributing_factors=contributing_factors,
            analysis_method="five_whys",
            evidence_chain=evidence,
            prevention_measures=prevention_measures,
            systemic_issues=systemic_issues,
            confidence_score=0.75
        )

    def _generate_debugging_roadmap(
        self,
        classification: ErrorClassification,
        recommendations: list[DebuggingRecommendation]
    ) -> list[str]:
        """Generate a step-by-step debugging roadmap"""
        roadmap = [
            "1. Document and verify the problem symptoms",
            "2. Gather all available error information and context",
            "3. Classify the error type and assess severity"
        ]

        if recommendations:
            top_strategy = recommendations[0].recommended_strategy.value.replace('_', ' ')
            roadmap.extend([
                f"4. Set up {top_strategy} debugging approach",
                f"5. Execute {top_strategy} to gather evidence",
                "6. Analyze findings and form hypotheses"
            ])

        roadmap.extend([
            "7. Test hypotheses systematically",
            "8. Isolate the root cause",
            "9. Implement and verify the fix",
            "10. Document lessons learned and prevention measures"
        ])

        # Add category-specific steps
        if classification.error_category == ErrorCategory.PERFORMANCE_ERROR:
            roadmap.insert(4, "4a. Establish performance baseline and metrics")
        elif classification.error_category == ErrorCategory.INTEGRATION_ERROR:
            roadmap.insert(4, "4a. Verify all integration points and dependencies")
        elif classification.error_category == ErrorCategory.CONCURRENCY_ERROR:
            roadmap.insert(4, "4a. Analyze threading and synchronization patterns")

        return roadmap

    def _generate_prevention_measures(
        self,
        classification: ErrorClassification,
        root_cause_analysis: RootCauseAnalysis | None
    ) -> list[str]:
        """Generate prevention measures based on error type and root cause"""
        measures = []

        # Generic prevention measures
        measures.extend([
            "Implement comprehensive error handling and logging",
            "Increase test coverage including edge cases and error paths",
            "Establish regular code review processes",
            "Improve documentation and knowledge sharing"
        ])

        # Category-specific measures
        category_measures = {
            ErrorCategory.SYNTAX_ERROR: [
                "Use linters and static analysis tools",
                "Implement pre-commit hooks for code quality",
                "Provide IDE configurations with syntax checking"
            ],
            ErrorCategory.LOGIC_ERROR: [
                "Implement unit tests for all business logic",
                "Use test-driven development practices",
                "Establish clear specifications and requirements"
            ],
            ErrorCategory.PERFORMANCE_ERROR: [
                "Implement performance monitoring and alerting",
                "Establish performance budgets and thresholds",
                "Conduct regular performance testing"
            ],
            ErrorCategory.MEMORY_ERROR: [
                "Use memory profiling tools regularly",
                "Implement memory leak detection",
                "Follow memory management best practices"
            ],
            ErrorCategory.CONCURRENCY_ERROR: [
                "Use thread-safe data structures",
                "Implement proper synchronization mechanisms",
                "Test with stress and load testing tools"
            ]
        }

        measures.extend(category_measures.get(classification.error_category, []))

        # Add root cause analysis measures if available
        if root_cause_analysis:
            measures.extend(root_cause_analysis.prevention_measures[:3])

        return measures[:10]  # Limit to 10 measures

    def _generate_risk_assessment(
        self,
        classification: ErrorClassification,
        recommendations: list[DebuggingRecommendation]
    ) -> list[str]:
        """Generate risk assessment for the debugging process"""
        risks = []

        # Severity-based risks
        if classification.severity == Severity.CRITICAL:
            risks.append("High risk: Critical error may cause system instability")
        elif classification.severity == Severity.HIGH:
            risks.append("Medium risk: Error significantly impacts functionality")

        # Reproducibility risks
        if classification.reproducibility == "never":
            risks.append("High risk: Non-reproducible errors are difficult to debug")
        elif classification.reproducibility == "sometimes":
            risks.append("Medium risk: Intermittent errors may be timing-dependent")

        # Strategy-specific risks
        if recommendations:
            for rec in recommendations[:2]:  # Top 2 recommendations
                if rec.risk_factors:
                    risks.extend([f"Strategy risk: {risk}" for risk in rec.risk_factors[:2]])

        # General debugging risks
        risks.extend([
            "Risk: Debugging changes may introduce new issues",
            "Risk: Time pressure may lead to incomplete analysis",
            "Risk: Complex systems may have cascading effects"
        ])

        return risks[:8]  # Limit to 8 risks

    def _generate_tool_recommendations(
        self,
        recommendations: list[DebuggingRecommendation],
        available_tools: list[str]
    ) -> list[str]:
        """Generate tool recommendations based on strategies"""
        recommended_tools = set()

        # Collect tools from recommendations
        for rec in recommendations[:3]:  # Top 3 recommendations
            recommended_tools.update(rec.required_tools)

        # Filter out already available tools and add explanations
        tool_explanations = []
        for tool in recommended_tools:
            if not any(tool.lower() in available.lower() for available in available_tools):
                tool_explanations.append(f"{tool}: Essential for recommended debugging strategies")

        # Add general purpose tools
        general_tools = [
            "Log aggregation tool: For centralized log analysis",
            "Version control: For tracking changes and bisecting",
            "Monitoring system: For real-time system observation",
            "Testing framework: For creating reproducible test cases"
        ]

        tool_explanations.extend(general_tools)
        return tool_explanations[:10]

    def _generate_best_practices(self, classification: ErrorClassification) -> list[str]:
        """Generate best practices based on error category"""
        general_practices = [
            "Document all debugging steps and findings",
            "Create reproducible test cases before fixing",
            "Verify fixes don't introduce new issues",
            "Share knowledge with team members"
        ]

        category_practices = {
            ErrorCategory.PERFORMANCE_ERROR: [
                "Profile before and after optimization",
                "Focus on algorithmic improvements first",
                "Consider caching strategies appropriately"
            ],
            ErrorCategory.MEMORY_ERROR: [
                "Use memory debugging tools consistently",
                "Check for resource cleanup in all paths",
                "Monitor memory usage patterns over time"
            ],
            ErrorCategory.CONCURRENCY_ERROR: [
                "Test with multiple thread configurations",
                "Use race condition detection tools",
                "Design for thread safety from the start"
            ],
            ErrorCategory.INTEGRATION_ERROR: [
                "Test integration points independently",
                "Implement circuit breaker patterns",
                "Monitor service dependencies closely"
            ]
        }

        practices = general_practices + category_practices.get(classification.error_category, [])
        return practices[:10]

    def _generate_learning_opportunities(
        self,
        classification: ErrorClassification,
        recommendations: list[DebuggingRecommendation]
    ) -> list[str]:
        """Generate learning opportunities from this debugging scenario"""
        opportunities = []

        # Category-specific learning
        category_name = classification.error_category.value.replace('_', ' ')
        opportunities.append(f"Learn more about {category_name} debugging techniques")

        # Strategy-specific learning
        if recommendations:
            top_strategy = recommendations[0].recommended_strategy.value.replace('_', ' ')
            opportunities.append(f"Improve skills in {top_strategy} debugging")

        # General learning opportunities
        opportunities.extend([
            "Study systematic debugging methodologies",
            "Learn about error prevention techniques",
            "Understand root cause analysis methods",
            "Develop better error reproduction skills",
            "Practice hypothesis-driven debugging",
            "Improve debugging tool proficiency"
        ])

        return opportunities[:8]
