"""
Programming Paradigms Analyzer

Core implementation of the programming paradigms cognitive tool, providing
analysis of Object-Oriented, Functional, Procedural, and other programming
paradigms with selection criteria, optimization guidance, and paradigm combinations.
"""

from typing import List, Dict, Any, Optional, Tuple
import asyncio
import time
from datetime import datetime

from .models import (
    ProgrammingParadigmsContext,
    ProgrammingParadigmsResult,
    ProgrammingParadigm,
    ParadigmCharacteristic,
    ProblemDomain,
    ParadigmProfile,
    ParadigmAnalysis,
    ParadigmComparison,
    ParadigmMix,
    CodeStructureAnalysis,
)


class ProgrammingParadigmsAnalyzer:
    """Programming paradigms cognitive tool analyzer"""
    
    def __init__(self):
        """Initialize the programming paradigms analyzer"""
        self.tool_name = "Programming Paradigms"
        self.version = "1.0.0"
        
        # Internal state for processing
        self._processing_start_time = 0.0
        
        # Initialize paradigm profiles
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
            ),
            
            ProgrammingParadigm.REACTIVE: ParadigmProfile(
                paradigm=ProgrammingParadigm.REACTIVE,
                description="Focuses on asynchronous data streams and propagation of changes",
                key_characteristics=[
                    ParadigmCharacteristic.COMPOSITION,
                    ParadigmCharacteristic.STATE_MANAGEMENT
                ],
                strengths=[
                    "Excellent for event-driven systems",
                    "Natural handling of asynchronous operations",
                    "Composable stream operations",
                    "Responsive user interfaces"
                ],
                weaknesses=[
                    "Complex debugging of async flows",
                    "Learning curve for reactive thinking",
                    "Memory management challenges",
                    "Potential for callback hell"
                ],
                suitable_domains=[
                    ProblemDomain.USER_INTERFACES,
                    ProblemDomain.WEB_DEVELOPMENT,
                    ProblemDomain.CONCURRENT_SYSTEMS
                ],
                languages=["JavaScript", "Java", "C#", "Scala", "Swift"],
                concepts=["Observables", "Streams", "Event handling", "Asynchronous programming"],
                best_practices=[
                    "Handle errors in reactive streams",
                    "Manage subscription lifecycles",
                    "Use operators for stream transformation",
                    "Avoid blocking operations in streams"
                ],
                antipatterns=[
                    "Unmanaged subscriptions",
                    "Blocking operations in streams",
                    "Complex nested subscriptions",
                    "Ignoring backpressure"
                ],
                learning_curve="steep",
                performance_profile={
                    "memory": "moderate",
                    "cpu": "good",
                    "scalability": "excellent"
                }
            ),
            
            ProgrammingParadigm.CONCURRENT: ParadigmProfile(
                paradigm=ProgrammingParadigm.CONCURRENT,
                description="Handles multiple computations executing simultaneously",
                key_characteristics=[
                    ParadigmCharacteristic.IMMUTABILITY,
                    ParadigmCharacteristic.STATE_MANAGEMENT
                ],
                strengths=[
                    "Utilizes multi-core processors",
                    "Improved system throughput",
                    "Better resource utilization",
                    "Responsive applications"
                ],
                weaknesses=[
                    "Complex synchronization issues",
                    "Race conditions and deadlocks",
                    "Difficult debugging",
                    "Non-deterministic behavior"
                ],
                suitable_domains=[
                    ProblemDomain.SYSTEM_PROGRAMMING,
                    ProblemDomain.CONCURRENT_SYSTEMS,
                    ProblemDomain.WEB_DEVELOPMENT,
                    ProblemDomain.SCIENTIFIC_COMPUTING
                ],
                languages=["Go", "Erlang", "Java", "C++", "Rust"],
                concepts=["Threads", "Locks", "Actors", "Message passing", "Channels"],
                best_practices=[
                    "Minimize shared mutable state",
                    "Use thread-safe data structures",
                    "Prefer message passing over shared memory",
                    "Design for immutability"
                ],
                antipatterns=[
                    "Excessive locking",
                    "Race conditions",
                    "Deadlocks",
                    "Thread leaks"
                ],
                learning_curve="steep",
                performance_profile={
                    "memory": "moderate",
                    "cpu": "excellent",
                    "scalability": "excellent"
                }
            )
        }
    
    async def analyze(self, context: ProgrammingParadigmsContext) -> ProgrammingParadigmsResult:
        """
        Analyze programming paradigms for the given context.
        
        Args:
            context: Programming paradigms context with problem description and requirements
            
        Returns:
            ProgrammingParadigmsResult with paradigm analysis and recommendations
        """
        self._processing_start_time = time.time()
        
        # Phase 1: Analyze paradigm suitability
        paradigm_analyses = await self._analyze_paradigm_suitability(context)
        
        # Phase 2: Compare paradigms
        paradigm_comparisons = []
        if len(paradigm_analyses) > 1:
            paradigm_comparisons = await self._compare_paradigms(
                context, paradigm_analyses[:5]  # Top 5 paradigms
            )
        
        # Phase 3: Analyze paradigm combinations (if enabled)
        paradigm_mixes = []
        if context.include_hybrid_analysis and len(paradigm_analyses) > 1:
            paradigm_mixes = await self._analyze_paradigm_mixes(
                paradigm_analyses[:3]  # Top 3 paradigms
            )
        
        # Phase 4: Code structure analysis (if existing codebase)
        code_structure_analysis = None
        if context.existing_codebase:
            code_structure_analysis = await self._analyze_code_structure(
                context.existing_codebase, context.target_languages
            )
        
        # Phase 5: Generate recommendations and roadmap
        implementation_roadmap = self._generate_implementation_roadmap(
            context, paradigm_analyses
        )
        
        learning_path_recommendations = self._generate_learning_path(
            context, paradigm_analyses
        )
        
        risk_considerations = self._generate_risk_considerations(
            context, paradigm_analyses
        )
        
        success_factors = self._generate_success_factors(
            context, paradigm_analyses
        )
        
        alternatives_analysis = self._analyze_alternatives(paradigm_analyses)
        
        # Calculate processing time
        processing_time = time.time() - self._processing_start_time
        
        return ProgrammingParadigmsResult(
            paradigm_analyses=paradigm_analyses[:context.max_paradigm_recommendations],
            paradigm_comparisons=paradigm_comparisons,
            paradigm_mixes=paradigm_mixes,
            code_structure_analysis=code_structure_analysis,
            top_recommended_paradigm=paradigm_analyses[0].paradigm.value if paradigm_analyses else None,
            paradigm_suitability_scores={
                analysis.paradigm.value: analysis.suitability_score
                for analysis in paradigm_analyses
            },
            implementation_roadmap=implementation_roadmap,
            learning_path_recommendations=learning_path_recommendations,
            risk_considerations=risk_considerations,
            success_factors=success_factors,
            alternatives_analysis=alternatives_analysis,
            processing_time_ms=round(processing_time * 1000)
        )
    
    async def _analyze_paradigm_suitability(
        self, context: ProgrammingParadigmsContext
    ) -> List[ParadigmAnalysis]:
        """Analyze suitability of each paradigm for the context"""
        # Simulate processing delay
        await asyncio.sleep(0.1)
        
        analyses = []
        
        for paradigm, profile in self.paradigm_profiles.items():
            analysis = await self._analyze_single_paradigm(
                paradigm, profile, context
            )
            analyses.append(analysis)
        
        # Sort by suitability score
        return sorted(analyses, key=lambda x: x.suitability_score, reverse=True)
    
    async def _analyze_single_paradigm(
        self,
        paradigm: ProgrammingParadigm,
        profile: ParadigmProfile,
        context: ProgrammingParadigmsContext
    ) -> ParadigmAnalysis:
        """Analyze suitability of a single paradigm"""
        
        problem_lower = context.problem_description.lower()
        project_lower = context.project_type.lower()
        
        # Calculate base suitability score
        score = 0.0
        matching_characteristics = []
        
        # Check domain match
        for domain in profile.suitable_domains:
            domain_keywords = domain.value.replace("_", " ").split()
            if any(keyword in problem_lower or keyword in project_lower 
                   for keyword in domain_keywords):
                score += 0.3
                break
        
        # Check requirements match
        for requirement in context.requirements:
            req_lower = requirement.lower()
            for strength in profile.strengths:
                if any(word in req_lower for word in strength.lower().split()):
                    score += 0.1
                    break
        
        # Check characteristic relevance
        characteristic_keywords = {
            ParadigmCharacteristic.ENCAPSULATION: ["encapsulation", "data hiding", "privacy", "secure"],
            ParadigmCharacteristic.IMMUTABILITY: ["immutable", "thread safe", "concurrent", "parallel"],
            ParadigmCharacteristic.PURE_FUNCTIONS: ["predictable", "testable", "reliable", "deterministic"],
            ParadigmCharacteristic.MODULARITY: ["modular", "reusable", "maintainable", "flexible"],
            ParadigmCharacteristic.INHERITANCE: ["hierarchical", "classification", "is-a", "extends"],
            ParadigmCharacteristic.COMPOSITION: ["has-a", "composable", "building blocks", "components"]
        }
        
        for characteristic in profile.key_characteristics:
            keywords = characteristic_keywords.get(characteristic, [])
            if any(keyword in problem_lower for keyword in keywords):
                matching_characteristics.append(characteristic)
                score += 0.15
        
        # Team experience bonus
        if paradigm in context.team_experience:
            score += 0.2
        
        # Language compatibility
        if context.target_languages:
            for lang in context.target_languages:
                if lang in profile.languages:
                    score += 0.1
                    break
        
        # Performance requirements
        if context.performance_requirements:
            perf_lower = context.performance_requirements.lower()
            if "high performance" in perf_lower or "fast" in perf_lower:
                if profile.performance_profile.get("cpu") == "excellent":
                    score += 0.2
                elif profile.performance_profile.get("cpu") == "poor":
                    score -= 0.1
        
        # Scalability requirements
        if context.scalability_needs:
            scale_lower = context.scalability_needs.lower()
            if "scalable" in scale_lower or "scale" in scale_lower:
                if profile.performance_profile.get("scalability") == "excellent":
                    score += 0.2
                elif profile.performance_profile.get("scalability") == "poor":
                    score -= 0.1
        
        suitability_score = min(1.0, max(0.0, score))
        
        return ParadigmAnalysis(
            paradigm=paradigm,
            context_description=context.problem_description,
            suitability_score=suitability_score,
            matching_characteristics=matching_characteristics,
            benefits_for_context=profile.strengths[:4],  # Top 4 benefits
            challenges_for_context=profile.weaknesses[:3],  # Top 3 challenges
            implementation_guidance=profile.best_practices[:4],
            code_structure_recommendations=[
                f"Organize code using {paradigm.value.replace('_', ' ')} principles",
                f"Apply {', '.join(c.value.replace('_', ' ') for c in profile.key_characteristics[:2])}",
                f"Follow {paradigm.value.replace('_', ' ')} best practices for maintainability"
            ],
            performance_considerations=[
                f"Memory usage: {profile.performance_profile.get('memory', 'moderate')}",
                f"CPU efficiency: {profile.performance_profile.get('cpu', 'moderate')}",
                f"Scalability: {profile.performance_profile.get('scalability', 'good')}"
            ]
        )
    
    async def _compare_paradigms(
        self,
        context: ProgrammingParadigmsContext,
        analyses: List[ParadigmAnalysis]
    ) -> List[ParadigmComparison]:
        """Compare top paradigms across different criteria"""
        # Simulate processing delay
        await asyncio.sleep(0.05)
        
        paradigms = [analysis.paradigm for analysis in analyses]
        criteria = ["performance", "maintainability", "learning_curve", "scalability"]
        
        scores = {}
        for paradigm in paradigms:
            profile = self.paradigm_profiles[paradigm]
            scores[paradigm.value] = {}
            
            for criterion in criteria:
                score = self._evaluate_paradigm_criterion(profile, criterion)
                scores[paradigm.value][criterion] = score
        
        # Generate recommendations
        recommendations = {}
        for criterion in criteria:
            best_paradigm = max(
                paradigms,
                key=lambda p: scores[p.value][criterion]
            )
            recommendations[criterion] = f"Use {best_paradigm.value.replace('_', ' ')} for {criterion}"
        
        # Identify hybrid opportunities
        hybrid_opportunities = self._identify_hybrid_opportunities(paradigms)
        
        # Create decision matrix
        decision_matrix = {}
        for criterion in criteria:
            decision_matrix[criterion] = {}
            for paradigm in paradigms:
                score = scores[paradigm.value][criterion]
                if score >= 0.8:
                    rating = "Excellent"
                elif score >= 0.6:
                    rating = "Good"
                elif score >= 0.4:
                    rating = "Fair"
                else:
                    rating = "Poor"
                decision_matrix[criterion][paradigm.value] = rating
        
        return [ParadigmComparison(
            paradigms=paradigms,
            comparison_criteria=criteria,
            scores=scores,
            recommendations=recommendations,
            hybrid_opportunities=hybrid_opportunities,
            decision_matrix=decision_matrix
        )]
    
    def _evaluate_paradigm_criterion(self, profile: ParadigmProfile, criterion: str) -> float:
        """Evaluate how well a paradigm meets a specific criterion"""
        criterion_lower = criterion.lower()
        
        # Performance-related criteria
        if "performance" in criterion_lower:
            perf_scores = {"excellent": 1.0, "good": 0.8, "moderate": 0.6, "poor": 0.3}
            return perf_scores.get(profile.performance_profile.get("cpu", "moderate"), 0.5)
        
        # Maintainability
        if "maintainability" in criterion_lower:
            if ParadigmCharacteristic.MODULARITY in profile.key_characteristics:
                return 0.9
            if ParadigmCharacteristic.ENCAPSULATION in profile.key_characteristics:
                return 0.8
            return 0.5
        
        # Scalability
        if "scalability" in criterion_lower:
            scale_scores = {"excellent": 1.0, "good": 0.8, "moderate": 0.6, "poor": 0.3}
            return scale_scores.get(profile.performance_profile.get("scalability", "good"), 0.6)
        
        # Learning curve (inverse - easier is better)
        if "learning" in criterion_lower:
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
        
        if (ProgrammingParadigm.REACTIVE in paradigms and
            ProgrammingParadigm.FUNCTIONAL in paradigms):
            opportunities.append("Reactive functional programming: Combine streams with pure functions")
        
        if (ProgrammingParadigm.CONCURRENT in paradigms and
            ProgrammingParadigm.FUNCTIONAL in paradigms):
            opportunities.append("Concurrent functional programming: Leverage immutability for safe concurrency")
        
        if len(paradigms) > 2:
            opportunities.append("Multi-paradigm approach: Different paradigms for different system layers")
        
        return opportunities
    
    async def _analyze_paradigm_mixes(
        self, analyses: List[ParadigmAnalysis]
    ) -> List[ParadigmMix]:
        """Analyze combinations of top paradigms"""
        # Simulate processing delay
        await asyncio.sleep(0.05)
        
        if len(analyses) < 2:
            return []
        
        primary = analyses[0].paradigm
        secondaries = [analysis.paradigm for analysis in analyses[1:3]]
        
        primary_profile = self.paradigm_profiles[primary]
        
        # Analyze synergies and conflicts
        synergies = []
        conflicts = []
        
        for secondary in secondaries:
            secondary_profile = self.paradigm_profiles[secondary]
            
            # Check for characteristic overlaps (synergies)
            common_characteristics = set(primary_profile.key_characteristics) & set(secondary_profile.key_characteristics)
            if common_characteristics:
                synergies.append(f"{primary.value} and {secondary.value} both support {', '.join(c.value.replace('_', ' ') for c in common_characteristics)}")
            
            # Check for conflicts
            if (ParadigmCharacteristic.IMMUTABILITY in primary_profile.key_characteristics and
                ParadigmCharacteristic.SIDE_EFFECTS in secondary_profile.key_characteristics):
                conflicts.append(f"Immutability from {primary.value} conflicts with side effects from {secondary.value}")
        
        return [ParadigmMix(
            primary_paradigm=primary,
            secondary_paradigms=secondaries,
            integration_strategy=f"Use {primary.value.replace('_', ' ')} as main structure with {', '.join(p.value.replace('_', ' ') for p in secondaries)} for specific components",
            synergies=synergies,
            conflicts=conflicts,
            implementation_patterns=[
                f"Layer separation: {primary.value.replace('_', ' ')} for architecture",
                f"Component mixing: Different paradigms for different modules",
                "Interface-based integration between paradigm boundaries"
            ],
            use_cases=[
                f"When {primary_profile.description.lower()} is main need",
                f"But specific components benefit from {', '.join(p.value.replace('_', ' ') for p in secondaries)}",
                "Complex systems requiring multiple problem-solving approaches"
            ],
            complexity_impact="Moderate to High - requires careful integration planning and team training"
        )]
    
    async def _analyze_code_structure(
        self, codebase_description: str, languages: List[str]
    ) -> CodeStructureAnalysis:
        """Analyze existing code structure to identify paradigms"""
        # Simulate processing delay
        await asyncio.sleep(0.05)
        
        description_lower = codebase_description.lower()
        detected_paradigms = []
        paradigm_purity = {}
        
        # Detect paradigms based on description
        paradigm_indicators = {
            ProgrammingParadigm.OBJECT_ORIENTED: [
                "class", "object", "inheritance", "polymorphism", "encapsulation", "method", "interface"
            ],
            ProgrammingParadigm.FUNCTIONAL: [
                "function", "lambda", "map", "filter", "reduce", "immutable", "pure", "compose"
            ],
            ProgrammingParadigm.PROCEDURAL: [
                "procedure", "function", "subroutine", "global", "sequential", "step by step"
            ],
            ProgrammingParadigm.REACTIVE: [
                "observable", "stream", "event", "reactive", "async", "subscription"
            ],
            ProgrammingParadigm.CONCURRENT: [
                "thread", "parallel", "concurrent", "lock", "synchronization", "atomic"
            ]
        }
        
        for paradigm, indicators in paradigm_indicators.items():
            matches = sum(1 for indicator in indicators if indicator in description_lower)
            if matches > 0:
                detected_paradigms.append(paradigm)
                paradigm_purity[paradigm.value] = min(1.0, matches / len(indicators))
        
        # Calculate consistency score
        if paradigm_purity:
            consistency_score = max(paradigm_purity.values())
        else:
            consistency_score = 0.5  # Neutral if no clear paradigm detected
        
        return CodeStructureAnalysis(
            detected_paradigms=detected_paradigms,
            paradigm_purity=paradigm_purity,
            structural_patterns=[
                "Modular organization",
                "Clear separation of concerns",
                "Consistent naming conventions"
            ],
            paradigm_violations=[
                "Mixed paradigm usage without clear boundaries" if len(detected_paradigms) > 2 else None
            ],
            improvement_suggestions=[
                f"Consider strengthening {max(paradigm_purity.keys(), key=paradigm_purity.get).replace('_', ' ')} patterns" if paradigm_purity else "Adopt a clear paradigm structure",
                "Establish coding standards for paradigm consistency",
                "Refactor mixed-paradigm components for clarity"
            ],
            refactoring_opportunities=[
                "Extract common functionality into reusable components",
                "Improve paradigm consistency across modules",
                "Simplify complex inheritance hierarchies" if ProgrammingParadigm.OBJECT_ORIENTED in detected_paradigms else None
            ],
            paradigm_consistency_score=consistency_score
        )
    
    def _generate_implementation_roadmap(
        self,
        context: ProgrammingParadigmsContext,
        analyses: List[ParadigmAnalysis]
    ) -> List[str]:
        """Generate implementation roadmap"""
        if not analyses:
            return ["Define clear requirements and constraints"]
        
        top_paradigm = analyses[0].paradigm
        roadmap = [
            f"1. Establish {top_paradigm.value.replace('_', ' ')} architecture foundation",
            f"2. Set up development environment and tools for {top_paradigm.value.replace('_', ' ')}",
            "3. Create coding standards and best practices documentation",
            "4. Implement core components using chosen paradigm",
            "5. Develop testing strategy aligned with paradigm principles"
        ]
        
        if context.team_experience and top_paradigm not in context.team_experience:
            roadmap.insert(1, "1.5. Provide team training on chosen paradigm")
        
        if len(analyses) > 1 and context.include_hybrid_analysis:
            second_paradigm = analyses[1].paradigm
            roadmap.append(f"6. Integrate {second_paradigm.value.replace('_', ' ')} for specific components")
        
        roadmap.extend([
            "7. Conduct code reviews focusing on paradigm adherence",
            "8. Refactor and optimize based on paradigm best practices",
            "9. Document architectural decisions and paradigm usage",
            "10. Establish continuous improvement process"
        ])
        
        return roadmap
    
    def _generate_learning_path(
        self,
        context: ProgrammingParadigmsContext,
        analyses: List[ParadigmAnalysis]
    ) -> List[str]:
        """Generate learning path recommendations"""
        if not analyses:
            return ["Study fundamental programming concepts"]
        
        top_paradigm = analyses[0].paradigm
        profile = self.paradigm_profiles[top_paradigm]
        
        learning_path = [
            f"1. Study {top_paradigm.value.replace('_', ' ')} theoretical foundations",
            f"2. Learn core concepts: {', '.join(profile.concepts[:3])}",
            f"3. Practice with {profile.languages[0] if profile.languages else 'suitable'} language",
            f"4. Implement small projects using {top_paradigm.value.replace('_', ' ')} principles"
        ]
        
        if profile.learning_curve == "steep":
            learning_path.insert(1, "1.5. Start with simpler paradigms for foundational understanding")
        
        learning_path.extend([
            "5. Study design patterns relevant to the paradigm",
            "6. Analyze existing codebases using the paradigm",
            "7. Participate in code reviews and discussions",
            "8. Mentor others to reinforce understanding"
        ])
        
        return learning_path
    
    def _generate_risk_considerations(
        self,
        context: ProgrammingParadigmsContext,
        analyses: List[ParadigmAnalysis]
    ) -> List[str]:
        """Generate risk considerations"""
        risks = []
        
        if not analyses:
            return ["Risk: Unclear requirements may lead to poor paradigm selection"]
        
        top_paradigm = analyses[0].paradigm
        profile = self.paradigm_profiles[top_paradigm]
        
        # Learning curve risks
        if profile.learning_curve == "steep":
            risks.append("Risk: Steep learning curve may impact development timeline")
        
        # Team experience risks
        if context.team_experience and top_paradigm not in context.team_experience:
            risks.append("Risk: Team lacks experience with recommended paradigm")
        
        # Performance risks
        if profile.performance_profile.get("cpu") == "poor" and context.performance_requirements:
            risks.append("Risk: Paradigm may not meet performance requirements")
        
        # Scalability risks
        if profile.performance_profile.get("scalability") == "poor" and context.scalability_needs:
            risks.append("Risk: Chosen paradigm may limit system scalability")
        
        # General risks
        risks.extend([
            "Risk: Paradigm mismatch with problem domain requirements",
            "Risk: Over-engineering with complex paradigm concepts",
            "Risk: Maintenance challenges if team knowledge is limited",
            "Risk: Integration difficulties with existing systems"
        ])
        
        return risks[:8]  # Limit to 8 risks
    
    def _generate_success_factors(
        self,
        context: ProgrammingParadigmsContext,
        analyses: List[ParadigmAnalysis]
    ) -> List[str]:
        """Generate success factors for paradigm adoption"""
        if not analyses:
            return ["Success factor: Clear requirements definition"]
        
        factors = [
            "Team commitment to learning and following paradigm principles",
            "Proper tooling and development environment setup",
            "Regular code reviews focusing on paradigm adherence",
            "Comprehensive documentation of paradigm usage patterns",
            "Gradual adoption with pilot projects and learning phases",
            "Clear architectural guidelines and coding standards",
            "Continuous education and knowledge sharing within team",
            "Realistic timeline accounting for learning curve"
        ]
        
        return factors
    
    def _analyze_alternatives(
        self, analyses: List[ParadigmAnalysis]
    ) -> Dict[str, str]:
        """Analyze alternative approaches"""
        if len(analyses) < 2:
            return {"alternatives": "Limited analysis due to insufficient paradigm options"}
        
        alternatives = {}
        
        for i, analysis in enumerate(analyses[1:4], 1):  # Top 3 alternatives
            paradigm_name = analysis.paradigm.value.replace('_', ' ')
            alternatives[f"Alternative {i}"] = f"{paradigm_name} (score: {analysis.suitability_score:.2f}) - {analysis.benefits_for_context[0] if analysis.benefits_for_context else 'Good general-purpose option'}"
        
        return alternatives