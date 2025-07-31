"""
Programming Paradigms Models for Clear Thinking FastMCP

Provides analysis of Object-Oriented, Functional, Procedural, and other programming
paradigms with selection criteria, optimization guidance, and paradigm combinations.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Set
from enum import Enum

from .base import CognitiveToolBase, CognitiveInputBase, CognitiveOutputBase, ComplexityLevel


class ProgrammingParadigm(str, Enum):
    """Programming paradigm types"""
    OBJECT_ORIENTED = "object_oriented"
    FUNCTIONAL = "functional"
    PROCEDURAL = "procedural"
    DECLARATIVE = "declarative"
    IMPERATIVE = "imperative"
    LOGIC = "logic"
    CONCURRENT = "concurrent"
    REACTIVE = "reactive"
    EVENT_DRIVEN = "event_driven"
    ASPECT_ORIENTED = "aspect_oriented"


class ParadigmCharacteristic(str, Enum):
    """Key characteristics of programming paradigms"""
    ENCAPSULATION = "encapsulation"
    INHERITANCE = "inheritance"
    POLYMORPHISM = "polymorphism"
    IMMUTABILITY = "immutability"
    HIGHER_ORDER_FUNCTIONS = "higher_order_functions"
    PURE_FUNCTIONS = "pure_functions"
    SIDE_EFFECTS = "side_effects"
    STATE_MANAGEMENT = "state_management"
    MODULARITY = "modularity"
    ABSTRACTION = "abstraction"
    COMPOSITION = "composition"


class ProblemDomain(str, Enum):
    """Problem domains suitable for different paradigms"""
    WEB_DEVELOPMENT = "web_development"
    DATA_PROCESSING = "data_processing"
    SYSTEM_PROGRAMMING = "system_programming"
    SCIENTIFIC_COMPUTING = "scientific_computing"
    GAME_DEVELOPMENT = "game_development"
    ENTERPRISE_SOFTWARE = "enterprise_software"
    EMBEDDED_SYSTEMS = "embedded_systems"
    MACHINE_LEARNING = "machine_learning"
    CONCURRENT_SYSTEMS = "concurrent_systems"
    USER_INTERFACES = "user_interfaces"


@dataclass
class ParadigmProfile:
    """Comprehensive profile of a programming paradigm"""
    paradigm: ProgrammingParadigm
    description: str
    key_characteristics: List[ParadigmCharacteristic]
    strengths: List[str]
    weaknesses: List[str]
    suitable_domains: List[ProblemDomain]
    languages: List[str]
    concepts: List[str]
    best_practices: List[str]
    antipatterns: List[str]
    learning_curve: str  # easy, moderate, steep
    performance_profile: Dict[str, str]  # memory, cpu, scalability


@dataclass
class ParadigmAnalysis:
    """Analysis of paradigm suitability for a specific context"""
    analysis_id: str
    paradigm: ProgrammingParadigm
    context_description: str
    suitability_score: float  # 0.0 to 1.0
    matching_characteristics: List[ParadigmCharacteristic]
    benefits_for_context: List[str]
    challenges_for_context: List[str]
    implementation_guidance: List[str]
    code_structure_recommendations: List[str]
    performance_considerations: List[str]


@dataclass
class ParadigmComparison:
    """Comparison between multiple paradigms"""
    comparison_id: str
    paradigms: List[ProgrammingParadigm]
    comparison_criteria: List[str]
    scores: Dict[ProgrammingParadigm, Dict[str, float]]
    recommendations: Dict[str, str]  # context -> recommended paradigm
    hybrid_opportunities: List[str]
    decision_matrix: Dict[str, Dict[ProgrammingParadigm, str]]


@dataclass
class ParadigmMix:
    """Analysis of combining multiple paradigms"""
    mix_id: str
    primary_paradigm: ProgrammingParadigm
    secondary_paradigms: List[ProgrammingParadigm]
    integration_strategy: str
    synergies: List[str]
    conflicts: List[str]
    implementation_patterns: List[str]
    use_cases: List[str]
    complexity_impact: str


@dataclass
class CodeStructureAnalysis:
    """Analysis of code structure from paradigm perspective"""
    analysis_id: str
    detected_paradigms: List[ProgrammingParadigm]
    paradigm_purity: Dict[ProgrammingParadigm, float]
    structural_patterns: List[str]
    paradigm_violations: List[str]
    improvement_suggestions: List[str]
    refactoring_opportunities: List[str]
    paradigm_consistency_score: float


class ProgrammingParadigmsModel(CognitiveToolBase):
    """
    Programming Paradigms cognitive model for paradigm analysis and selection.
    
    Capabilities:
    - Paradigm suitability analysis
    - Multi-paradigm combination strategies
    - Code structure optimization
    - Paradigm-specific best practices
    """
    
    def __init__(self):
        super().__init__()
        self._initialize_paradigm_profiles()
    
    def _initialize_paradigm_profiles(self):
        """Initialize profiles for different programming paradigms"""
        self.paradigm_profiles = {
            ProgrammingParadigm.OBJECT_ORIENTED: ParadigmProfile(
                paradigm=ProgrammingParadigm.OBJECT_ORIENTED,
                description="Organizes code around objects that contain data and methods",
                key_characteristics=[
                    ParadigmCharacteristic.ENCAPSULATION,
                    ParadigmCharacteristic.INHERITANCE,
                    ParadigmCharacteristic.POLYMORPHISM,
                    ParadigmCharacteristic.ABSTRACTION
                ],
                strengths=[
                    "Code reusability through inheritance",
                    "Natural modeling of real-world entities",
                    "Encapsulation provides data protection",
                    "Polymorphism enables flexible interfaces"
                ],
                weaknesses=[
                    "Can lead to complex inheritance hierarchies",
                    "Potential for tight coupling",
                    "May have performance overhead",
                    "Learning curve for proper design"
                ],
                suitable_domains=[
                    ProblemDomain.ENTERPRISE_SOFTWARE,
                    ProblemDomain.WEB_DEVELOPMENT,
                    ProblemDomain.GAME_DEVELOPMENT,
                    ProblemDomain.USER_INTERFACES
                ],
                languages=["Java", "C++", "C#", "Python", "JavaScript", "Ruby"],
                concepts=["Classes", "Objects", "Inheritance", "Polymorphism", "Encapsulation"],
                best_practices=[
                    "Favor composition over inheritance",
                    "Use interfaces for loose coupling",
                    "Apply SOLID principles",
                    "Keep classes focused and cohesive"
                ],
                antipatterns=[
                    "God objects",
                    "Deep inheritance hierarchies",
                    "Circular dependencies",
                    "Feature envy"
                ],
                learning_curve="moderate",
                performance_profile={
                    "memory": "moderate",
                    "cpu": "moderate",
                    "scalability": "good"
                }
            ),
            
            ProgrammingParadigm.FUNCTIONAL: ParadigmProfile(
                paradigm=ProgrammingParadigm.FUNCTIONAL,
                description="Treats computation as evaluation of mathematical functions",
                key_characteristics=[
                    ParadigmCharacteristic.IMMUTABILITY,
                    ParadigmCharacteristic.PURE_FUNCTIONS,
                    ParadigmCharacteristic.HIGHER_ORDER_FUNCTIONS,
                    ParadigmCharacteristic.COMPOSITION
                ],
                strengths=[
                    "Easier reasoning about code behavior",
                    "Better support for concurrency",
                    "Reduced side effects",
                    "Mathematical foundations"
                ],
                weaknesses=[
                    "Learning curve for imperative programmers",
                    "Can be less intuitive for some problems",
                    "Potential performance overhead",
                    "Limited by language support"
                ],
                suitable_domains=[
                    ProblemDomain.DATA_PROCESSING,
                    ProblemDomain.SCIENTIFIC_COMPUTING,
                    ProblemDomain.CONCURRENT_SYSTEMS,
                    ProblemDomain.MACHINE_LEARNING
                ],
                languages=["Haskell", "Lisp", "Clojure", "F#", "Scala", "JavaScript"],
                concepts=["Pure functions", "Immutability", "Higher-order functions", "Recursion"],
                best_practices=[
                    "Avoid side effects in pure functions",
                    "Use immutable data structures",
                    "Compose functions for complex operations",
                    "Prefer recursion over iteration"
                ],
                antipatterns=[
                    "Hidden side effects",
                    "Excessive mutation",
                    "Deeply nested function calls",
                    "Ignoring tail recursion optimization"
                ],
                learning_curve="steep",
                performance_profile={
                    "memory": "high",
                    "cpu": "variable",
                    "scalability": "excellent"
                }
            ),
            
            ProgrammingParadigm.PROCEDURAL: ParadigmProfile(
                paradigm=ProgrammingParadigm.PROCEDURAL,
                description="Organizes code as a sequence of procedures or functions",
                key_characteristics=[
                    ParadigmCharacteristic.MODULARITY,
                    ParadigmCharacteristic.STATE_MANAGEMENT,
                    ParadigmCharacteristic.SIDE_EFFECTS
                ],
                strengths=[
                    "Simple and straightforward approach",
                    "Easy to understand and debug",
                    "Direct control over program flow",
                    "Efficient execution"
                ],
                weaknesses=[
                    "Can lead to code duplication",
                    "Global state management issues",
                    "Limited reusability",
                    "Difficult to maintain large codebases"
                ],
                suitable_domains=[
                    ProblemDomain.SYSTEM_PROGRAMMING,
                    ProblemDomain.EMBEDDED_SYSTEMS,
                    ProblemDomain.SCIENTIFIC_COMPUTING
                ],
                languages=["C", "Pascal", "FORTRAN", "COBOL"],
                concepts=["Functions", "Procedures", "Global variables", "Local scope"],
                best_practices=[
                    "Keep functions small and focused",
                    "Minimize global variables",
                    "Use meaningful function names",
                    "Document function interfaces"
                ],
                antipatterns=[
                    "Spaghetti code",
                    "Excessive global state",
                    "Monolithic functions",
                    "Copy-paste programming"
                ],
                learning_curve="easy",
                performance_profile={
                    "memory": "low",
                    "cpu": "excellent",
                    "scalability": "poor"
                }
            )
        }
    
    def get_paradigm_profile(self, paradigm: ProgrammingParadigm) -> Optional[ParadigmProfile]:
        """Get the profile for a specific paradigm"""
        return self.paradigm_profiles.get(paradigm)
    
    def analyze_paradigm_suitability(
        self,
        context_description: str,
        requirements: List[str],
        constraints: Optional[Dict[str, Any]] = None
    ) -> List[ParadigmAnalysis]:
        """Analyze which paradigms are most suitable for the given context"""
        constraints = constraints or {}
        analyses = []
        
        for paradigm, profile in self.paradigm_profiles.items():
            analysis = self._analyze_single_paradigm(
                paradigm, profile, context_description, requirements, constraints
            )
            analyses.append(analysis)
        
        # Sort by suitability score
        return sorted(analyses, key=lambda x: x.suitability_score, reverse=True)
    
    def _analyze_single_paradigm(
        self,
        paradigm: ProgrammingParadigm,
        profile: ParadigmProfile,
        context: str,
        requirements: List[str],
        constraints: Dict[str, Any]
    ) -> ParadigmAnalysis:
        """Analyze suitability of a single paradigm"""
        context_lower = context.lower()
        
        # Calculate base suitability score
        score = 0.0
        matching_characteristics = []
        
        # Check domain match
        for domain in profile.suitable_domains:
            if domain.value.replace("_", " ") in context_lower:
                score += 0.3
                break
        
        # Check requirements match
        for requirement in requirements:
            req_lower = requirement.lower()
            for strength in profile.strengths:
                if any(word in req_lower for word in strength.lower().split()):
                    score += 0.1
                    break
        
        # Check characteristic relevance
        characteristic_keywords = {
            ParadigmCharacteristic.ENCAPSULATION: ["encapsulation", "data hiding", "privacy"],
            ParadigmCharacteristic.IMMUTABILITY: ["immutable", "thread safe", "concurrent"],
            ParadigmCharacteristic.PURE_FUNCTIONS: ["predictable", "testable", "reliable"],
            ParadigmCharacteristic.MODULARITY: ["modular", "reusable", "maintainable"]
        }
        
        for characteristic in profile.key_characteristics:
            keywords = characteristic_keywords.get(characteristic, [])
            if any(keyword in context_lower for keyword in keywords):
                matching_characteristics.append(characteristic)
                score += 0.1
        
        # Apply constraints
        if "performance" in constraints and constraints["performance"] == "critical":
            if profile.performance_profile["cpu"] == "excellent":
                score += 0.2
            elif profile.performance_profile["cpu"] == "poor":
                score -= 0.2
        
        suitability_score = min(1.0, score)
        
        return ParadigmAnalysis(
            analysis_id=f"paradigm_analysis_{paradigm.value}_{self._generate_id()}",
            paradigm=paradigm,
            context_description=context,
            suitability_score=suitability_score,
            matching_characteristics=matching_characteristics,
            benefits_for_context=profile.strengths[:3],  # Top 3 benefits
            challenges_for_context=profile.weaknesses[:2],  # Top 2 challenges
            implementation_guidance=profile.best_practices[:3],
            code_structure_recommendations=[
                f"Organize code using {paradigm.value.replace('_', ' ')} principles",
                f"Apply {', '.join(c.value for c in profile.key_characteristics[:2])}"
            ],
            performance_considerations=[
                f"Memory usage: {profile.performance_profile['memory']}",
                f"CPU efficiency: {profile.performance_profile['cpu']}"
            ]
        )
    
    def compare_paradigms(
        self,
        paradigms: List[ProgrammingParadigm],
        comparison_criteria: List[str]
    ) -> ParadigmComparison:
        """Compare multiple paradigms across specified criteria"""
        scores = {}
        
        for paradigm in paradigms:
            profile = self.get_paradigm_profile(paradigm)
            if not profile:
                continue
                
            scores[paradigm] = {}
            for criterion in comparison_criteria:
                score = self._evaluate_paradigm_criterion(profile, criterion)
                scores[paradigm][criterion] = score
        
        # Generate recommendations based on scores
        recommendations = {}
        for criterion in comparison_criteria:
            best_paradigm = max(
                paradigms,
                key=lambda p: scores.get(p, {}).get(criterion, 0.0)
            )
            recommendations[criterion] = f"Use {best_paradigm.value} for {criterion}"
        
        # Identify hybrid opportunities
        hybrid_opportunities = self._identify_hybrid_opportunities(paradigms)
        
        return ParadigmComparison(
            comparison_id=f"comparison_{self._generate_id()}",
            paradigms=paradigms,
            comparison_criteria=comparison_criteria,
            scores=scores,
            recommendations=recommendations,
            hybrid_opportunities=hybrid_opportunities,
            decision_matrix=self._create_decision_matrix(paradigms, comparison_criteria, scores)
        )
    
    def _evaluate_paradigm_criterion(self, profile: ParadigmProfile, criterion: str) -> float:
        """Evaluate how well a paradigm meets a specific criterion"""
        criterion_lower = criterion.lower()
        
        # Performance-related criteria
        if "performance" in criterion_lower:
            perf_scores = {"excellent": 1.0, "good": 0.8, "moderate": 0.6, "poor": 0.3}
            return perf_scores.get(profile.performance_profile.get("cpu", "moderate"), 0.5)
        
        # Maintainability
        if "maintainability" in criterion_lower or "maintenance" in criterion_lower:
            if ParadigmCharacteristic.MODULARITY in profile.key_characteristics:
                return 0.9
            if ParadigmCharacteristic.ENCAPSULATION in profile.key_characteristics:
                return 0.8
            return 0.5
        
        # Concurrency
        if "concurrency" in criterion_lower or "parallel" in criterion_lower:
            if ParadigmCharacteristic.IMMUTABILITY in profile.key_characteristics:
                return 0.9
            if ParadigmCharacteristic.PURE_FUNCTIONS in profile.key_characteristics:
                return 0.8
            return 0.4
        
        # Learning curve (inverse - easier is better)
        if "learning" in criterion_lower or "easy" in criterion_lower:
            learning_scores = {"easy": 1.0, "moderate": 0.7, "steep": 0.3}
            return learning_scores.get(profile.learning_curve, 0.5)
        
        return 0.5  # Default neutral score
    
    def _identify_hybrid_opportunities(self, paradigms: List[ProgrammingParadigm]) -> List[str]:
        """Identify opportunities for combining paradigms"""
        opportunities = []
        
        if (ProgrammingParadigm.OBJECT_ORIENTED in paradigms and 
            ProgrammingParadigm.FUNCTIONAL in paradigms):
            opportunities.append("Functional programming with OOP: Use functional concepts within object methods")
        
        if (ProgrammingParadigm.PROCEDURAL in paradigms and 
            ProgrammingParadigm.OBJECT_ORIENTED in paradigms):
            opportunities.append("Procedural core with OOP wrapper: Procedural algorithms within object interfaces")
        
        if len(paradigms) > 2:
            opportunities.append("Multi-paradigm approach: Different paradigms for different system layers")
        
        return opportunities
    
    def _create_decision_matrix(
        self,
        paradigms: List[ProgrammingParadigm],
        criteria: List[str],
        scores: Dict[ProgrammingParadigm, Dict[str, float]]
    ) -> Dict[str, Dict[ProgrammingParadigm, str]]:
        """Create a decision matrix for paradigm selection"""
        matrix = {}
        
        for criterion in criteria:
            matrix[criterion] = {}
            for paradigm in paradigms:
                score = scores.get(paradigm, {}).get(criterion, 0.0)
                if score >= 0.8:
                    rating = "Excellent"
                elif score >= 0.6:
                    rating = "Good"
                elif score >= 0.4:
                    rating = "Fair"
                else:
                    rating = "Poor"
                matrix[criterion][paradigm] = rating
        
        return matrix
    
    def analyze_paradigm_mix(
        self,
        primary_paradigm: ProgrammingParadigm,
        secondary_paradigms: List[ProgrammingParadigm]
    ) -> ParadigmMix:
        """Analyze combining multiple paradigms in a single system"""
        primary_profile = self.get_paradigm_profile(primary_paradigm)
        if not primary_profile:
            raise ValueError(f"Unknown primary paradigm: {primary_paradigm}")
        
        # Analyze synergies and conflicts
        synergies = []
        conflicts = []
        
        for secondary in secondary_paradigms:
            secondary_profile = self.get_paradigm_profile(secondary)
            if not secondary_profile:
                continue
            
            # Check for characteristic overlaps (synergies)
            common_characteristics = set(primary_profile.key_characteristics) & set(secondary_profile.key_characteristics)
            if common_characteristics:
                synergies.append(f"{primary_paradigm.value} and {secondary.value} both support {', '.join(c.value for c in common_characteristics)}")
            
            # Check for conflicts
            if (ParadigmCharacteristic.IMMUTABILITY in primary_profile.key_characteristics and
                ParadigmCharacteristic.SIDE_EFFECTS in secondary_profile.key_characteristics):
                conflicts.append(f"Immutability from {primary_paradigm.value} conflicts with side effects from {secondary.value}")
        
        return ParadigmMix(
            mix_id=f"mix_{primary_paradigm.value}_{self._generate_id()}",
            primary_paradigm=primary_paradigm,
            secondary_paradigms=secondary_paradigms,
            integration_strategy=f"Use {primary_paradigm.value} as main structure with {', '.join(p.value for p in secondary_paradigms)} for specific components",
            synergies=synergies,
            conflicts=conflicts,
            implementation_patterns=[
                f"Layer separation: {primary_paradigm.value} for architecture",
                f"Component mixing: Different paradigms for different modules"
            ],
            use_cases=[
                f"When {primary_profile.description.lower()} is main need",
                f"But specific components benefit from {', '.join(p.value for p in secondary_paradigms)}"
            ],
            complexity_impact="Moderate to High - requires careful integration planning"
        )
    
    def analyze_code_structure(
        self,
        code_description: str,
        language_hints: Optional[List[str]] = None
    ) -> CodeStructureAnalysis:
        """Analyze code structure to identify paradigms in use"""
        language_hints = language_hints or []
        detected_paradigms = []
        paradigm_purity = {}
        
        description_lower = code_description.lower()
        
        # Detect paradigms based on description
        paradigm_indicators = {
            ProgrammingParadigm.OBJECT_ORIENTED: [
                "class", "object", "inheritance", "polymorphism", "encapsulation", "method"
            ],
            ProgrammingParadigm.FUNCTIONAL: [
                "function", "lambda", "map", "filter", "reduce", "immutable", "pure"
            ],
            ProgrammingParadigm.PROCEDURAL: [
                "procedure", "function", "subroutine", "global", "sequential"
            ]
        }
        
        for paradigm, indicators in paradigm_indicators.items():
            matches = sum(1 for indicator in indicators if indicator in description_lower)
            if matches > 0:
                detected_paradigms.append(paradigm)
                paradigm_purity[paradigm] = min(1.0, matches / len(indicators))
        
        # Calculate consistency score
        if detected_paradigms:
            consistency_score = max(paradigm_purity.values())
        else:
            consistency_score = 0.5  # Neutral if no clear paradigm detected
        
        return CodeStructureAnalysis(
            analysis_id=f"structure_{self._generate_id()}",
            detected_paradigms=detected_paradigms,
            paradigm_purity=paradigm_purity,
            structural_patterns=["Modular organization", "Clear separation of concerns"],
            paradigm_violations=[],  # Would be populated with real analysis
            improvement_suggestions=[
                f"Consider strengthening {max(paradigm_purity.keys(), key=paradigm_purity.get).value} patterns" if paradigm_purity else "Adopt a clear paradigm structure"
            ],
            refactoring_opportunities=[
                "Extract common functionality",
                "Improve paradigm consistency"
            ],
            paradigm_consistency_score=consistency_score
        )