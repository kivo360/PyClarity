"""
Design Patterns Models for Clear Thinking FastMCP

Provides software architecture patterns, design principle applications,
pattern selection frameworks, and architecture decision support.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Set
from enum import Enum

from .base import BaseClearThinkingModel


class PatternCategory(str, Enum):
    """Categories of design patterns"""
    CREATIONAL = "creational"
    STRUCTURAL = "structural"
    BEHAVIORAL = "behavioral"
    ARCHITECTURAL = "architectural"
    CONCURRENCY = "concurrency"
    ENTERPRISE = "enterprise"


class DesignPrinciple(str, Enum):
    """Core design principles"""
    SINGLE_RESPONSIBILITY = "single_responsibility"
    OPEN_CLOSED = "open_closed"
    LISKOV_SUBSTITUTION = "liskov_substitution"
    INTERFACE_SEGREGATION = "interface_segregation"
    DEPENDENCY_INVERSION = "dependency_inversion"
    DRY = "dont_repeat_yourself"
    KISS = "keep_it_simple_stupid"
    YAGNI = "you_arent_gonna_need_it"
    COMPOSITION_OVER_INHERITANCE = "composition_over_inheritance"
    LOOSE_COUPLING = "loose_coupling"
    HIGH_COHESION = "high_cohesion"


class PatternComplexity(str, Enum):
    """Pattern implementation complexity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


@dataclass
class DesignPattern:
    """Represents a design pattern with its characteristics"""
    pattern_id: str
    name: str
    category: PatternCategory
    description: str
    intent: str
    applicability: List[str]
    structure: Dict[str, Any]
    participants: List[str]
    collaborations: List[str]
    consequences: Dict[str, List[str]]  # benefits and drawbacks
    implementation_notes: List[str]
    related_patterns: List[str]
    complexity: PatternComplexity
    principles_supported: List[DesignPrinciple]


@dataclass
class PatternApplication:
    """Analysis of applying a pattern to a specific context"""
    application_id: str
    pattern: DesignPattern
    context_description: str
    fit_score: float  # 0.0 to 1.0
    benefits: List[str]
    drawbacks: List[str]
    implementation_effort: PatternComplexity
    prerequisites: List[str]
    alternatives: List[str]
    recommendation: str


@dataclass
class ArchitecturalDecision:
    """Represents an architectural decision point"""
    decision_id: str
    title: str
    context: str
    problem_statement: str
    decision: str
    status: str  # proposed, accepted, rejected, superseded
    alternatives_considered: List[str]
    consequences: List[str]
    patterns_involved: List[str]
    principles_applied: List[DesignPrinciple]
    decision_date: str
    stakeholders: List[str]


@dataclass
class PatternCombination:
    """Analysis of combining multiple patterns"""
    combination_id: str
    patterns: List[DesignPattern]
    interaction_type: str  # complementary, conflicting, synergistic
    combined_benefits: List[str]
    potential_conflicts: List[str]
    integration_complexity: PatternComplexity
    usage_scenarios: List[str]
    best_practices: List[str]


@dataclass
class DesignAnalysis:
    """Comprehensive design pattern analysis"""
    analysis_id: str
    system_description: str
    identified_patterns: List[DesignPattern]
    pattern_applications: List[PatternApplication]
    architectural_decisions: List[ArchitecturalDecision]
    pattern_combinations: List[PatternCombination]
    design_quality_score: float
    improvement_suggestions: List[str]
    principle_adherence: Dict[DesignPrinciple, float]


class DesignPatternsModel(BaseClearThinkingModel):
    """
    Design Patterns cognitive model for software architecture and design decisions.
    
    Capabilities:
    - Pattern recognition and recommendation
    - Design principle evaluation
    - Architecture decision analysis
    - Pattern combination assessment
    """
    
    def __init__(self):
        super().__init__()
        self._initialize_pattern_catalog()
    
    def _initialize_pattern_catalog(self):
        """Initialize the catalog of design patterns"""
        self.pattern_catalog = {
            "singleton": DesignPattern(
                pattern_id="singleton",
                name="Singleton",
                category=PatternCategory.CREATIONAL,
                description="Ensures a class has only one instance and provides global access",
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
                description="Defines one-to-many dependency between objects",
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
            )
        }
    
    def get_pattern_by_id(self, pattern_id: str) -> Optional[DesignPattern]:
        """Retrieve a pattern by its ID"""
        return self.pattern_catalog.get(pattern_id)
    
    def find_patterns_by_category(self, category: PatternCategory) -> List[DesignPattern]:
        """Find all patterns in a specific category"""
        return [pattern for pattern in self.pattern_catalog.values() 
                if pattern.category == category]
    
    def find_patterns_by_principle(self, principle: DesignPrinciple) -> List[DesignPattern]:
        """Find patterns that support a specific design principle"""
        return [pattern for pattern in self.pattern_catalog.values()
                if principle in pattern.principles_supported]
    
    def recommend_pattern(
        self,
        problem_description: str,
        context_requirements: List[str],
        constraints: Optional[Dict[str, Any]] = None
    ) -> List[PatternApplication]:
        """Recommend patterns based on problem context"""
        constraints = constraints or {}
        applications = []
        
        for pattern in self.pattern_catalog.values():
            fit_score = self._calculate_pattern_fit(
                pattern, problem_description, context_requirements
            )
            
            if fit_score > 0.3:  # Threshold for consideration
                application = self._create_pattern_application(
                    pattern, problem_description, context_requirements, fit_score
                )
                applications.append(application)
        
        # Sort by fit score
        return sorted(applications, key=lambda x: x.fit_score, reverse=True)
    
    def _calculate_pattern_fit(
        self,
        pattern: DesignPattern,
        problem_description: str,
        requirements: List[str]
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
            PatternCategory.CREATIONAL: ["create", "instantiate", "construct", "build"],
            PatternCategory.STRUCTURAL: ["compose", "structure", "organize", "interface"],
            PatternCategory.BEHAVIORAL: ["behavior", "algorithm", "responsibility", "interaction"]
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
    
    def _create_pattern_application(
        self,
        pattern: DesignPattern,
        context: str,
        requirements: List[str],
        fit_score: float
    ) -> PatternApplication:
        """Create a pattern application analysis"""
        benefits = pattern.consequences.get("benefits", [])
        drawbacks = pattern.consequences.get("drawbacks", [])
        
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
            application_id=f"app_{pattern.pattern_id}_{self._generate_id()}",
            pattern=pattern,
            context_description=context,
            fit_score=fit_score,
            benefits=benefits,
            drawbacks=drawbacks,
            implementation_effort=pattern.complexity,
            prerequisites=[f"Understanding of {pattern.category.value} patterns"],
            alternatives=pattern.related_patterns,
            recommendation=recommendation
        )
    
    def evaluate_design_principles(
        self,
        code_description: str,
        patterns_used: List[str]
    ) -> Dict[DesignPrinciple, float]:
        """Evaluate adherence to design principles"""
        adherence_scores = {}
        
        for principle in DesignPrinciple:
            score = 0.5  # Base neutral score
            
            # Check if patterns supporting this principle are used
            supporting_patterns = self.find_patterns_by_principle(principle)
            used_supporting_patterns = [
                p for p in supporting_patterns 
                if p.pattern_id in patterns_used
            ]
            
            if used_supporting_patterns:
                score += len(used_supporting_patterns) * 0.1
            
            # Specific principle checks based on description
            score += self._evaluate_specific_principle(principle, code_description)
            
            adherence_scores[principle] = min(1.0, score)
        
        return adherence_scores
    
    def _evaluate_specific_principle(
        self,
        principle: DesignPrinciple,
        description: str
    ) -> float:
        """Evaluate specific principle adherence"""
        description_lower = description.lower()
        
        principle_indicators = {
            DesignPrinciple.SINGLE_RESPONSIBILITY: {
                "positive": ["focused", "single purpose", "cohesive"],
                "negative": ["multiple responsibilities", "god class", "kitchen sink"]
            },
            DesignPrinciple.OPEN_CLOSED: {
                "positive": ["extensible", "pluggable", "configurable"],
                "negative": ["hardcoded", "modification required", "brittle"]
            },
            DesignPrinciple.LOOSE_COUPLING: {
                "positive": ["independent", "decoupled", "interface-based"],
                "negative": ["tightly coupled", "dependent", "hardwired"]
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
        
        return score_delta
    
    def create_architectural_decision(
        self,
        title: str,
        context: str,
        problem: str,
        decision: str,
        alternatives: List[str],
        patterns_involved: Optional[List[str]] = None
    ) -> ArchitecturalDecision:
        """Create an architectural decision record"""
        patterns_involved = patterns_involved or []
        
        # Identify principles applied based on decision content
        principles_applied = []
        decision_lower = decision.lower()
        
        for principle in DesignPrinciple:
            if self._principle_mentioned_in_text(principle, decision_lower):
                principles_applied.append(principle)
        
        return ArchitecturalDecision(
            decision_id=f"adr_{self._generate_id()}",
            title=title,
            context=context,
            problem_statement=problem,
            decision=decision,
            status="proposed",
            alternatives_considered=alternatives,
            consequences=[],  # To be filled by analysis
            patterns_involved=patterns_involved,
            principles_applied=principles_applied,
            decision_date=self._get_current_timestamp(),
            stakeholders=[]
        )
    
    def _principle_mentioned_in_text(self, principle: DesignPrinciple, text: str) -> bool:
        """Check if a principle is mentioned in text"""
        principle_keywords = {
            DesignPrinciple.SINGLE_RESPONSIBILITY: ["single responsibility", "one reason to change"],
            DesignPrinciple.OPEN_CLOSED: ["open closed", "open for extension", "closed for modification"],
            DesignPrinciple.LOOSE_COUPLING: ["loose coupling", "decoupled", "independent"],
            DesignPrinciple.DRY: ["don't repeat yourself", "dry", "duplication"],
            DesignPrinciple.KISS: ["keep it simple", "kiss", "simplicity"]
        }
        
        keywords = principle_keywords.get(principle, [])
        return any(keyword in text for keyword in keywords)
    
    def analyze_pattern_combinations(
        self,
        pattern_ids: List[str]
    ) -> List[PatternCombination]:
        """Analyze how multiple patterns work together"""
        combinations = []
        patterns = [self.get_pattern_by_id(pid) for pid in pattern_ids if self.get_pattern_by_id(pid)]
        
        if len(patterns) < 2:
            return combinations
        
        # Analyze pairs of patterns
        for i in range(len(patterns)):
            for j in range(i + 1, len(patterns)):
                combination = self._analyze_pattern_pair(patterns[i], patterns[j])
                if combination:
                    combinations.append(combination)
        
        return combinations
    
    def _analyze_pattern_pair(
        self,
        pattern1: DesignPattern,
        pattern2: DesignPattern
    ) -> Optional[PatternCombination]:
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
            combination_id=f"combo_{pattern1.pattern_id}_{pattern2.pattern_id}",
            patterns=[pattern1, pattern2],
            interaction_type=interaction_type,
            combined_benefits=[
                f"Combines {pattern1.name} and {pattern2.name} benefits",
                "Enhanced design flexibility"
            ],
            potential_conflicts=[
                "Increased complexity",
                "May require careful coordination"
            ],
            integration_complexity=complexity,
            usage_scenarios=[f"When both {pattern1.intent.lower()} and {pattern2.intent.lower()}"],
            best_practices=[
                "Ensure clear separation of concerns",
                "Document pattern interactions",
                "Test integration thoroughly"
            ]
        )
    
    def perform_design_analysis(
        self,
        system_description: str,
        existing_patterns: Optional[List[str]] = None,
        requirements: Optional[List[str]] = None
    ) -> DesignAnalysis:
        """Perform comprehensive design pattern analysis"""
        existing_patterns = existing_patterns or []
        requirements = requirements or []
        
        # Get existing patterns
        identified_patterns = [
            self.get_pattern_by_id(pid) for pid in existing_patterns
            if self.get_pattern_by_id(pid)
        ]
        
        # Get pattern recommendations
        pattern_applications = self.recommend_pattern(
            system_description, requirements
        )
        
        # Analyze pattern combinations
        pattern_combinations = self.analyze_pattern_combinations(existing_patterns)
        
        # Evaluate design principles
        principle_adherence = self.evaluate_design_principles(
            system_description, existing_patterns
        )
        
        # Calculate design quality score
        quality_factors = [
            len(identified_patterns) * 0.1,  # Pattern usage
            sum(principle_adherence.values()) / len(principle_adherence),  # Principle adherence
            len([app for app in pattern_applications if app.fit_score > 0.7]) * 0.05  # Good fits
        ]
        design_quality_score = min(1.0, sum(quality_factors) / len(quality_factors))
        
        # Generate improvement suggestions
        improvement_suggestions = []
        low_scoring_principles = [
            principle for principle, score in principle_adherence.items()
            if score < 0.6
        ]
        
        if low_scoring_principles:
            improvement_suggestions.append(
                f"Consider improving adherence to: {', '.join(p.value for p in low_scoring_principles)}"
            )
        
        if not identified_patterns:
            improvement_suggestions.append("Consider introducing design patterns for better structure")
        
        return DesignAnalysis(
            analysis_id=f"analysis_{self._generate_id()}",
            system_description=system_description,
            identified_patterns=identified_patterns,
            pattern_applications=pattern_applications[:5],  # Top 5 recommendations
            architectural_decisions=[],  # Would be populated in real analysis
            pattern_combinations=pattern_combinations,
            design_quality_score=design_quality_score,
            improvement_suggestions=improvement_suggestions,
            principle_adherence=principle_adherence
        )