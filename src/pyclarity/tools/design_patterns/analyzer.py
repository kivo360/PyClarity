"""
Design Patterns Analyzer

Core implementation of the design patterns cognitive tool, providing
software architecture patterns, design principle applications,
pattern selection frameworks, and architecture decision support.
"""

import asyncio
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from .models import (
    ArchitecturalDecision,
    DesignAnalysis,
    DesignPattern,
    DesignPatternsContext,
    DesignPatternsResult,
    DesignPrinciple,
    PatternApplication,
    PatternCategory,
    PatternCombination,
    PatternComplexity,
)


class DesignPatternsAnalyzer:
    """Design patterns cognitive tool analyzer"""

    def __init__(self):
        """Initialize the design patterns analyzer"""
        self.tool_name = "Design Patterns"
        self.version = "1.0.0"

        # Internal state for processing
        self._processing_start_time = 0.0

        # Initialize pattern catalog
        self._initialize_pattern_catalog()

    def _initialize_pattern_catalog(self):
        """Initialize the catalog of design patterns"""
        self.pattern_catalog = {
            "singleton": DesignPattern(
                pattern_id="singleton",
                name="Singleton",
                category=PatternCategory.CREATIONAL,
                description="Ensures a class has only one instance and provides global access to it",
                intent="Ensure a class only has one instance, and provide a global point of access to it",
                applicability=["Need exactly one instance", "Global access required", "Lazy initialization needed"],
                structure={"class": "Singleton", "method": "getInstance()"},
                participants=["Singleton"],
                collaborations=["Clients access singleton through getInstance()"],
                consequences={
                    "benefits": ["Controlled access", "Reduced namespace", "Permits refinement of operations"],
                    "drawbacks": ["Global state", "Testing difficulties", "Hidden dependencies"]
                },
                implementation_notes=["Thread safety considerations", "Lazy vs eager initialization"],
                related_patterns=["Factory Method", "Abstract Factory"],
                complexity=PatternComplexity.LOW,
                principles_supported=[DesignPrinciple.SINGLE_RESPONSIBILITY]
            ),

            "observer": DesignPattern(
                pattern_id="observer",
                name="Observer",
                category=PatternCategory.BEHAVIORAL,
                description="Defines one-to-many dependency between objects for automatic notification",
                intent="Define a one-to-many dependency between objects so that when one object changes state, all dependents are notified",
                applicability=["Loose coupling needed", "Dynamic relationships", "Event notification"],
                structure={"subject": "Subject", "observer": "Observer", "concrete": "ConcreteObserver"},
                participants=["Subject", "Observer", "ConcreteSubject", "ConcreteObserver"],
                collaborations=["Subject notifies observers", "Observers register/unregister"],
                consequences={
                    "benefits": ["Loose coupling", "Dynamic relationships", "Broadcast communication"],
                    "drawbacks": ["Unexpected updates", "Complex update semantics", "Memory leaks potential"]
                },
                implementation_notes=["Push vs pull model", "Subject state consistency"],
                related_patterns=["Mediator", "Model-View-Controller"],
                complexity=PatternComplexity.MEDIUM,
                principles_supported=[DesignPrinciple.LOOSE_COUPLING, DesignPrinciple.OPEN_CLOSED]
            ),

            "strategy": DesignPattern(
                pattern_id="strategy",
                name="Strategy",
                category=PatternCategory.BEHAVIORAL,
                description="Defines family of algorithms and makes them interchangeable",
                intent="Define a family of algorithms, encapsulate each one, and make them interchangeable",
                applicability=["Multiple algorithms", "Runtime algorithm selection", "Avoid conditionals"],
                structure={"context": "Context", "strategy": "Strategy", "concrete": "ConcreteStrategy"},
                participants=["Strategy", "ConcreteStrategy", "Context"],
                collaborations=["Context delegates to Strategy", "Strategy implements algorithm"],
                consequences={
                    "benefits": ["Algorithm family", "Eliminates conditionals", "Runtime choice"],
                    "drawbacks": ["Clients must know strategies", "Communication overhead", "Increased objects"]
                },
                implementation_notes=["Strategy interface design", "Context-strategy communication"],
                related_patterns=["State", "Template Method"],
                complexity=PatternComplexity.MEDIUM,
                principles_supported=[DesignPrinciple.OPEN_CLOSED, DesignPrinciple.SINGLE_RESPONSIBILITY]
            ),

            "factory_method": DesignPattern(
                pattern_id="factory_method",
                name="Factory Method",
                category=PatternCategory.CREATIONAL,
                description="Creates objects without specifying their concrete classes",
                intent="Define an interface for creating an object, but let subclasses decide which class to instantiate",
                applicability=["Class can't anticipate objects to create", "Subclasses specify objects", "Delegate creation"],
                structure={"creator": "Creator", "product": "Product", "concrete": "ConcreteCreator"},
                participants=["Product", "ConcreteProduct", "Creator", "ConcreteCreator"],
                collaborations=["Creator relies on subclasses", "ConcreteCreator creates ConcreteProduct"],
                consequences={
                    "benefits": ["Eliminates concrete classes", "Provides hooks", "Connects parallel hierarchies"],
                    "drawbacks": ["Complex class hierarchy", "Subclass required for creation"]
                },
                implementation_notes=["Creator can provide default implementation", "Parameterized factory methods"],
                related_patterns=["Abstract Factory", "Template Method", "Prototype"],
                complexity=PatternComplexity.MEDIUM,
                principles_supported=[DesignPrinciple.OPEN_CLOSED, DesignPrinciple.DEPENDENCY_INVERSION]
            ),

            "adapter": DesignPattern(
                pattern_id="adapter",
                name="Adapter",
                category=PatternCategory.STRUCTURAL,
                description="Allows incompatible interfaces to work together",
                intent="Convert the interface of a class into another interface clients expect",
                applicability=["Use existing class with incompatible interface", "Create reusable class", "Interface mismatch"],
                structure={"target": "Target", "adapter": "Adapter", "adaptee": "Adaptee"},
                participants=["Target", "Client", "Adaptee", "Adapter"],
                collaborations=["Client calls Adapter", "Adapter translates to Adaptee"],
                consequences={
                    "benefits": ["Allows incompatible classes to work", "Increases reusability", "Separates interface from implementation"],
                    "drawbacks": ["Increases complexity", "All requests forwarded", "May limit functionality"]
                },
                implementation_notes=["Object vs class adapter", "Two-way adapters", "Pluggable adapters"],
                related_patterns=["Bridge", "Decorator", "Proxy"],
                complexity=PatternComplexity.LOW,
                principles_supported=[DesignPrinciple.OPEN_CLOSED, DesignPrinciple.SINGLE_RESPONSIBILITY]
            ),

            "decorator": DesignPattern(
                pattern_id="decorator",
                name="Decorator",
                category=PatternCategory.STRUCTURAL,
                description="Adds behavior to objects dynamically without altering their structure",
                intent="Attach additional responsibilities to an object dynamically",
                applicability=["Add responsibilities dynamically", "Responsibilities can be withdrawn", "Extension by subclassing impractical"],
                structure={"component": "Component", "decorator": "Decorator", "concrete": "ConcreteDecorator"},
                participants=["Component", "ConcreteComponent", "Decorator", "ConcreteDecorator"],
                collaborations=["Decorator forwards requests to Component", "May perform additional actions"],
                consequences={
                    "benefits": ["More flexibility than inheritance", "Avoids feature-laden classes", "Pay-as-you-go approach"],
                    "drawbacks": ["Lots of little objects", "Identity problems", "Complex configuration"]
                },
                implementation_notes=["Interface conformance", "Omitting abstract Decorator", "Changing object skin vs guts"],
                related_patterns=["Adapter", "Composite", "Strategy"],
                complexity=PatternComplexity.MEDIUM,
                principles_supported=[DesignPrinciple.OPEN_CLOSED, DesignPrinciple.COMPOSITION_OVER_INHERITANCE]
            )
        }

    async def analyze(self, context: DesignPatternsContext) -> DesignPatternsResult:
        """
        Analyze a system using design patterns.

        Args:
            context: Design patterns context with system description and requirements

        Returns:
            DesignPatternsResult with pattern recommendations and analysis
        """
        self._processing_start_time = time.time()

        # Phase 1: Identify existing patterns
        identified_patterns = await self._identify_existing_patterns(
            context.existing_patterns
        )

        # Phase 2: Generate pattern recommendations
        pattern_recommendations = await self._recommend_patterns(context)

        # Phase 3: Analyze architectural decisions (if enabled)
        architectural_decisions = []
        if context.include_architectural_decisions:
            architectural_decisions = await self._analyze_architectural_decisions(
                context, pattern_recommendations
            )

        # Phase 4: Analyze pattern combinations (if enabled)
        pattern_combinations = []
        if context.include_pattern_combinations and len(identified_patterns) > 1:
            pattern_combinations = await self._analyze_pattern_combinations(
                identified_patterns
            )

        # Phase 5: Evaluate design principles
        principle_adherence = await self._evaluate_design_principles(
            context, identified_patterns
        )

        # Phase 6: Calculate quality scores
        design_quality_score = self._calculate_design_quality_score(
            identified_patterns, principle_adherence, pattern_recommendations
        )

        maintainability_score = self._calculate_maintainability_score(
            identified_patterns, principle_adherence
        )

        extensibility_score = self._calculate_extensibility_score(
            pattern_recommendations, principle_adherence
        )

        # Phase 7: Generate improvement suggestions
        improvement_suggestions = self._generate_improvement_suggestions(
            context, principle_adherence, pattern_recommendations
        )

        # Calculate processing time
        processing_time = time.time() - self._processing_start_time

        return DesignPatternsResult(
            identified_patterns=identified_patterns,
            pattern_recommendations=pattern_recommendations[:context.max_recommendations],
            architectural_decisions=architectural_decisions,
            pattern_combinations=pattern_combinations,
            design_quality_score=design_quality_score,
            principle_adherence={p.value: score for p, score in principle_adherence.items()},
            improvement_suggestions=improvement_suggestions,
            pattern_catalog_size=len(self.pattern_catalog),
            top_recommended_pattern=pattern_recommendations[0].pattern.name if pattern_recommendations else None,
            complexity_assessment=self._assess_complexity(context, identified_patterns),
            maintainability_score=maintainability_score,
            extensibility_score=extensibility_score,
            processing_time_ms=round(processing_time * 1000)
        )

    async def _identify_existing_patterns(
        self, existing_pattern_ids: list[str]
    ) -> list[DesignPattern]:
        """Identify existing patterns from their IDs"""
        # Simulate processing delay
        await asyncio.sleep(0.05)

        identified = []
        for pattern_id in existing_pattern_ids:
            pattern = self.pattern_catalog.get(pattern_id.lower())
            if pattern:
                identified.append(pattern)

        return identified

    async def _recommend_patterns(
        self, context: DesignPatternsContext
    ) -> list[PatternApplication]:
        """Recommend patterns based on context"""
        # Simulate processing delay
        await asyncio.sleep(0.1)

        recommendations = []

        for pattern in self.pattern_catalog.values():
            fit_score = self._calculate_pattern_fit(
                pattern, context.problem, context.requirements
            )

            if fit_score > 0.3:  # Threshold for consideration
                application = await self._create_pattern_application(
                    pattern, context, fit_score
                )
                recommendations.append(application)

        # Sort by fit score
        return sorted(recommendations, key=lambda x: x.fit_score, reverse=True)

    def _calculate_pattern_fit(
        self,
        pattern: DesignPattern,
        problem_description: str,
        requirements: list[str]
    ) -> float:
        """Calculate how well a pattern fits the given context"""
        score = 0.0
        factors = 0

        # Check applicability match
        for applicability in pattern.applicability:
            for requirement in requirements:
                if applicability.lower() in requirement.lower():
                    score += 0.3
                    factors += 1

        # Check problem description relevance
        problem_lower = problem_description.lower()
        if pattern.intent.lower() in problem_lower:
            score += 0.4
            factors += 1

        # Check category relevance based on keywords
        category_keywords = {
            PatternCategory.CREATIONAL: ["create", "instantiate", "construct", "build", "factory"],
            PatternCategory.STRUCTURAL: ["compose", "structure", "organize", "interface", "adapter", "wrapper"],
            PatternCategory.BEHAVIORAL: ["behavior", "algorithm", "responsibility", "interaction", "communication"],
            PatternCategory.ARCHITECTURAL: ["architecture", "system", "component", "layer", "module"],
            PatternCategory.CONCURRENCY: ["thread", "concurrent", "parallel", "synchronization", "lock"],
            PatternCategory.ENTERPRISE: ["enterprise", "business", "service", "transaction", "persistence"]
        }

        keywords = category_keywords.get(pattern.category, [])
        for keyword in keywords:
            if keyword in problem_lower:
                score += 0.2
                factors += 1
                break

        # Base score for having the pattern available
        if factors == 0:
            return 0.1  # Minimal relevance

        return min(1.0, score / max(1, factors))

    async def _create_pattern_application(
        self,
        pattern: DesignPattern,
        context: DesignPatternsContext,
        fit_score: float
    ) -> PatternApplication:
        """Create a pattern application analysis"""

        benefits = pattern.consequences.get("benefits", [])
        drawbacks = pattern.consequences.get("drawbacks", [])

        # Adjust complexity based on team experience
        implementation_effort = pattern.complexity
        if context.team_experience_level == "beginner":
            if pattern.complexity == PatternComplexity.LOW:
                implementation_effort = PatternComplexity.MEDIUM
            elif pattern.complexity == PatternComplexity.MEDIUM:
                implementation_effort = PatternComplexity.HIGH
        elif context.team_experience_level == "expert":
            if pattern.complexity == PatternComplexity.HIGH:
                implementation_effort = PatternComplexity.MEDIUM
            elif pattern.complexity == PatternComplexity.MEDIUM:
                implementation_effort = PatternComplexity.LOW

        # Generate recommendation based on fit score
        if fit_score > 0.8:
            recommendation = "Highly recommended - excellent fit for requirements"
        elif fit_score > 0.6:
            recommendation = "Recommended - good fit with minor considerations"
        elif fit_score > 0.4:
            recommendation = "Consider with caution - moderate fit"
        else:
            recommendation = "Not recommended - poor fit for requirements"

        return PatternApplication(
            pattern=pattern,
            context_description=context.system_description,
            fit_score=fit_score,
            benefits=benefits,
            drawbacks=drawbacks,
            implementation_effort=implementation_effort,
            prerequisites=[f"Understanding of {pattern.category.value} patterns"],
            alternatives=pattern.related_patterns,
            recommendation=recommendation
        )

    async def _analyze_architectural_decisions(
        self,
        context: DesignPatternsContext,
        recommendations: list[PatternApplication]
    ) -> list[ArchitecturalDecision]:
        """Analyze architectural decisions based on patterns"""
        # Simulate processing delay
        await asyncio.sleep(0.1)

        decisions = []

        # Create decisions for top recommendations
        for i, rec in enumerate(recommendations[:3]):
            if rec.fit_score > 0.6:
                decision = ArchitecturalDecision(
                    title=f"Adopt {rec.pattern.name} Pattern",
                    context=context.system_description,
                    problem_statement=f"Need to address: {context.problem}",
                    decision=f"Implement the {rec.pattern.name} pattern to {rec.pattern.intent.lower()}",
                    status="proposed",
                    alternatives_considered=rec.alternatives,
                    consequences=rec.benefits + [f"Drawback: {d}" for d in rec.drawbacks],
                    patterns_involved=[rec.pattern.pattern_id],
                    principles_applied=rec.pattern.principles_supported,
                    stakeholders=["Development Team", "Architecture Team"]
                )
                decisions.append(decision)

        return decisions

    async def _analyze_pattern_combinations(
        self, patterns: list[DesignPattern]
    ) -> list[PatternCombination]:
        """Analyze how multiple patterns work together"""
        # Simulate processing delay
        await asyncio.sleep(0.1)

        combinations = []

        # Analyze pairs of patterns
        for i in range(len(patterns)):
            for j in range(i + 1, len(patterns)):
                combination = await self._analyze_pattern_pair(patterns[i], patterns[j])
                if combination:
                    combinations.append(combination)

        return combinations

    async def _analyze_pattern_pair(
        self,
        pattern1: DesignPattern,
        pattern2: DesignPattern
    ) -> PatternCombination | None:
        """Analyze interaction between two patterns"""

        # Check if patterns are related
        is_related = (pattern1.pattern_id in pattern2.related_patterns or
                     pattern2.pattern_id in pattern1.related_patterns)

        if not is_related and pattern1.category != pattern2.category:
            # Different categories might be complementary
            interaction_type = "complementary"
            complexity = PatternComplexity.MEDIUM
        elif is_related:
            interaction_type = "synergistic"
            complexity = PatternComplexity.HIGH
        else:
            interaction_type = "neutral"
            complexity = PatternComplexity.LOW

        return PatternCombination(
            patterns=[pattern1, pattern2],
            interaction_type=interaction_type,
            combined_benefits=[
                f"Combines {pattern1.name} and {pattern2.name} benefits",
                "Enhanced design flexibility",
                "Better separation of concerns"
            ],
            potential_conflicts=[
                "Increased complexity",
                "May require careful coordination",
                "Potential performance overhead"
            ],
            integration_complexity=complexity,
            usage_scenarios=[f"When both {pattern1.intent.lower()} and {pattern2.intent.lower()}"],
            best_practices=[
                "Ensure clear separation of concerns",
                "Document pattern interactions",
                "Test integration thoroughly"
            ]
        )

    async def _evaluate_design_principles(
        self,
        context: DesignPatternsContext,
        identified_patterns: list[DesignPattern]
    ) -> dict[DesignPrinciple, float]:
        """Evaluate adherence to design principles"""
        # Simulate processing delay
        await asyncio.sleep(0.1)

        adherence_scores = {}

        for principle in DesignPrinciple:
            score = 0.5  # Base neutral score

            # Check if patterns supporting this principle are used
            supporting_patterns = [
                p for p in identified_patterns
                if principle in p.principles_supported
            ]

            if supporting_patterns:
                score += len(supporting_patterns) * 0.1

            # Specific principle checks based on description
            score += self._evaluate_specific_principle(
                principle, context.system_description
            )

            # Bonus for explicitly targeting this principle
            if principle in context.target_principles:
                score += 0.2

            adherence_scores[principle] = min(1.0, score)

        return adherence_scores

    def _evaluate_specific_principle(
        self, principle: DesignPrinciple, description: str
    ) -> float:
        """Evaluate specific principle adherence"""
        description_lower = description.lower()

        principle_indicators = {
            DesignPrinciple.SINGLE_RESPONSIBILITY: {
                "positive": ["focused", "single purpose", "cohesive", "one responsibility"],
                "negative": ["multiple responsibilities", "god class", "kitchen sink", "does everything"]
            },
            DesignPrinciple.OPEN_CLOSED: {
                "positive": ["extensible", "pluggable", "configurable", "modular"],
                "negative": ["hardcoded", "modification required", "brittle", "rigid"]
            },
            DesignPrinciple.LOOSE_COUPLING: {
                "positive": ["independent", "decoupled", "interface-based", "loosely coupled"],
                "negative": ["tightly coupled", "dependent", "hardwired", "monolithic"]
            },
            DesignPrinciple.DRY: {
                "positive": ["reusable", "shared", "common", "abstracted"],
                "negative": ["duplicated", "repeated", "copy-paste", "redundant"]
            },
            DesignPrinciple.KISS: {
                "positive": ["simple", "straightforward", "clear", "minimal"],
                "negative": ["complex", "complicated", "convoluted", "over-engineered"]
            }
        }

        indicators = principle_indicators.get(principle, {"positive": [], "negative": []})
        score_delta = 0.0

        for positive in indicators["positive"]:
            if positive in description_lower:
                score_delta += 0.1

        for negative in indicators["negative"]:
            if negative in description_lower:
                score_delta -= 0.1

        return max(-0.3, min(0.3, score_delta))  # Limit impact

    def _calculate_design_quality_score(
        self,
        patterns: list[DesignPattern],
        principle_adherence: dict[DesignPrinciple, float],
        recommendations: list[PatternApplication]
    ) -> float:
        """Calculate overall design quality score"""

        factors = []

        # Pattern usage factor
        if patterns:
            pattern_factor = min(1.0, len(patterns) * 0.2)
            factors.append(pattern_factor)

        # Principle adherence factor
        if principle_adherence:
            principle_factor = sum(principle_adherence.values()) / len(principle_adherence)
            factors.append(principle_factor)

        # Recommendation quality factor
        if recommendations:
            good_recommendations = [r for r in recommendations if r.fit_score > 0.7]
            rec_factor = len(good_recommendations) / max(1, len(recommendations))
            factors.append(rec_factor)

        # Overall score
        if factors:
            return sum(factors) / len(factors)
        else:
            return 0.5  # Neutral if no factors

    def _calculate_maintainability_score(
        self,
        patterns: list[DesignPattern],
        principle_adherence: dict[DesignPrinciple, float]
    ) -> float:
        """Calculate maintainability score"""

        # Key principles for maintainability
        key_principles = [
            DesignPrinciple.SINGLE_RESPONSIBILITY,
            DesignPrinciple.LOOSE_COUPLING,
            DesignPrinciple.DRY,
            DesignPrinciple.KISS
        ]

        maintainability_factors = []

        for principle in key_principles:
            if principle in principle_adherence:
                maintainability_factors.append(principle_adherence[principle])

        # Pattern complexity factor
        if patterns:
            avg_complexity = sum(
                0.9 if p.complexity == PatternComplexity.LOW else
                0.7 if p.complexity == PatternComplexity.MEDIUM else
                0.5 if p.complexity == PatternComplexity.HIGH else 0.3
                for p in patterns
            ) / len(patterns)
            maintainability_factors.append(avg_complexity)

        return sum(maintainability_factors) / len(maintainability_factors) if maintainability_factors else 0.5

    def _calculate_extensibility_score(
        self,
        recommendations: list[PatternApplication],
        principle_adherence: dict[DesignPrinciple, float]
    ) -> float:
        """Calculate extensibility score"""

        # Key principles for extensibility
        key_principles = [
            DesignPrinciple.OPEN_CLOSED,
            DesignPrinciple.DEPENDENCY_INVERSION,
            DesignPrinciple.COMPOSITION_OVER_INHERITANCE
        ]

        extensibility_factors = []

        for principle in key_principles:
            if principle in principle_adherence:
                extensibility_factors.append(principle_adherence[principle])

        # Pattern extensibility factor
        if recommendations:
            extensible_patterns = [
                r for r in recommendations
                if DesignPrinciple.OPEN_CLOSED in r.pattern.principles_supported
            ]
            pattern_factor = len(extensible_patterns) / len(recommendations)
            extensibility_factors.append(pattern_factor)

        return sum(extensibility_factors) / len(extensibility_factors) if extensibility_factors else 0.5

    def _generate_improvement_suggestions(
        self,
        context: DesignPatternsContext,
        principle_adherence: dict[DesignPrinciple, float],
        recommendations: list[PatternApplication]
    ) -> list[str]:
        """Generate improvement suggestions"""

        suggestions = []

        # Principle-based suggestions
        low_scoring_principles = [
            principle for principle, score in principle_adherence.items()
            if score < 0.6
        ]

        if low_scoring_principles:
            suggestions.append(
                f"Consider improving adherence to: {', '.join(p.value.replace('_', ' ').title() for p in low_scoring_principles)}"
            )

        # Pattern-based suggestions
        if not context.existing_patterns:
            suggestions.append("Consider introducing design patterns for better structure and maintainability")

        if recommendations and recommendations[0].fit_score > 0.8:
            suggestions.append(f"Strongly consider implementing the {recommendations[0].pattern.name} pattern")

        # Complexity-based suggestions
        if context.complexity_level.value in ["complex", "very_complex"]:
            suggestions.append("Break down complex components using appropriate structural patterns")

        # Team experience suggestions
        if context.team_experience_level == "beginner":
            suggestions.append("Start with simpler patterns like Strategy or Observer before tackling complex ones")

        # Performance suggestions
        if context.performance_requirements:
            suggestions.append("Consider performance implications when selecting patterns")

        return suggestions[:10]  # Limit to 10 suggestions

    def _assess_complexity(
        self, context: DesignPatternsContext, patterns: list[DesignPattern]
    ) -> str:
        """Assess the complexity of the system"""

        base_complexity = context.complexity_level.value

        if not patterns:
            return f"System complexity: {base_complexity} - No design patterns identified"

        pattern_complexity_avg = sum(
            1 if p.complexity == PatternComplexity.LOW else
            2 if p.complexity == PatternComplexity.MEDIUM else
            3 if p.complexity == PatternComplexity.HIGH else 4
            for p in patterns
        ) / len(patterns)

        if pattern_complexity_avg < 1.5:
            complexity_assessment = "low pattern complexity"
        elif pattern_complexity_avg < 2.5:
            complexity_assessment = "moderate pattern complexity"
        else:
            complexity_assessment = "high pattern complexity"

        return f"System complexity: {base_complexity} with {complexity_assessment}"
