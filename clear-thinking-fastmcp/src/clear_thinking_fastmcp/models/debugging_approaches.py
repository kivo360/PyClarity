"""
Debugging Approaches Models for Clear Thinking FastMCP

Provides systematic troubleshooting methodologies, error classification and resolution,
debugging strategy selection, and root cause analysis frameworks.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Set
from enum import Enum
from datetime import datetime

from .base import BaseClearThinkingModel


class DebuggingStrategy(str, Enum):
    """Different debugging strategies"""
    PRINT_DEBUGGING = "print_debugging"
    INTERACTIVE_DEBUGGING = "interactive_debugging"
    LOG_ANALYSIS = "log_analysis"
    BINARY_SEARCH = "binary_search"
    RUBBER_DUCK = "rubber_duck"
    UNIT_TESTING = "unit_testing"
    INTEGRATION_TESTING = "integration_testing"
    PROFILING = "profiling"
    STATIC_ANALYSIS = "static_analysis"
    CODE_REVIEW = "code_review"
    DIVIDE_AND_CONQUER = "divide_and_conquer"
    HYPOTHESIS_TESTING = "hypothesis_testing"


class ErrorCategory(str, Enum):
    """Categories of errors"""
    SYNTAX_ERROR = "syntax_error"
    RUNTIME_ERROR = "runtime_error"
    LOGIC_ERROR = "logic_error"
    PERFORMANCE_ERROR = "performance_error"
    MEMORY_ERROR = "memory_error"
    CONCURRENCY_ERROR = "concurrency_error"
    CONFIGURATION_ERROR = "configuration_error"
    INTEGRATION_ERROR = "integration_error"
    USER_INPUT_ERROR = "user_input_error"
    ENVIRONMENT_ERROR = "environment_error"


class Severity(str, Enum):
    """Error severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFORMATIONAL = "informational"


class DebuggingPhase(str, Enum):
    """Phases of the debugging process"""
    PROBLEM_IDENTIFICATION = "problem_identification"
    REPRODUCTION = "reproduction"
    ISOLATION = "isolation"
    ANALYSIS = "analysis"
    HYPOTHESIS_FORMATION = "hypothesis_formation"
    TESTING = "testing"
    RESOLUTION = "resolution"
    VERIFICATION = "verification"
    DOCUMENTATION = "documentation"


@dataclass
class DebugContext:
    """Context information for debugging session"""
    context_id: str
    system_description: str
    environment: Dict[str, str]
    error_symptoms: List[str]
    reproduction_steps: List[str]
    constraints: List[str]
    available_tools: List[str]
    time_constraints: Optional[str]
    impact_assessment: str


@dataclass
class ErrorClassification:
    """Classification of an error or bug"""
    classification_id: str
    error_category: ErrorCategory
    severity: Severity
    error_message: Optional[str]
    stack_trace: Optional[str]
    symptoms: List[str]
    potential_causes: List[str]
    affected_components: List[str]
    frequency: str  # rare, occasional, frequent, constant
    reproducibility: str  # always, sometimes, never
    confidence_level: float


@dataclass
class DebuggingHypothesis:
    """A hypothesis about the cause of a bug"""
    hypothesis_id: str
    description: str
    confidence_level: float
    supporting_evidence: List[str]
    contradicting_evidence: List[str]
    test_plan: List[str]
    estimated_effort: str
    risk_level: str
    alternative_hypotheses: List[str]


@dataclass
class DebuggingStep:
    """A single step in the debugging process"""
    step_id: str
    phase: DebuggingPhase
    description: str
    strategy_used: DebuggingStrategy
    expected_outcome: str
    actual_outcome: Optional[str]
    tools_used: List[str]
    evidence_gathered: List[str]
    time_spent: Optional[str]
    success: Optional[bool]
    next_steps: List[str]


@dataclass
class RootCauseAnalysis:
    """Root cause analysis results"""
    analysis_id: str
    problem_statement: str
    root_causes: List[str]
    contributing_factors: List[str]
    analysis_method: str  # five_whys, fishbone, fault_tree
    evidence_chain: List[str]
    prevention_measures: List[str]
    systemic_issues: List[str]
    confidence_score: float


@dataclass
class DebuggingSession:
    """Complete debugging session record"""
    session_id: str
    context: DebugContext
    error_classification: ErrorClassification
    hypotheses: List[DebuggingHypothesis]
    debugging_steps: List[DebuggingStep]
    root_cause_analysis: Optional[RootCauseAnalysis]
    resolution: Optional[str]
    lessons_learned: List[str]
    prevention_recommendations: List[str]
    session_duration: Optional[str]
    success_rate: float


@dataclass
class DebuggingRecommendation:
    """Recommendation for debugging approach"""
    recommendation_id: str
    recommended_strategy: DebuggingStrategy
    context_match_score: float
    reasoning: str
    expected_effectiveness: float
    estimated_time: str
    required_tools: List[str]
    prerequisites: List[str]
    alternative_strategies: List[DebuggingStrategy]
    risk_factors: List[str]


class DebuggingApproachesModel(BaseClearThinkingModel):
    """
    Debugging Approaches cognitive model for systematic troubleshooting.
    
    Capabilities:
    - Error classification and analysis
    - Debugging strategy selection
    - Root cause analysis
    - Systematic debugging workflows
    """
    
    def __init__(self):
        super().__init__()
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
                "limitations": ["Code pollution", "Performance impact", "Not suitable for production"]
            },
            
            DebuggingStrategy.INTERACTIVE_DEBUGGING: {
                "description": "Using debugger to step through code execution",
                "best_for": ["Complex logic errors", "State inspection", "Runtime behavior"],
                "effectiveness": 0.9,
                "time_cost": "medium",
                "tool_requirements": ["debugger", "IDE", "symbol information"],
                "limitations": ["Setup overhead", "Tool dependency", "May alter timing"]
            },
            
            DebuggingStrategy.BINARY_SEARCH: {
                "description": "Systematically narrowing down error location",
                "best_for": ["Large codebases", "Integration errors", "Regression bugs"],
                "effectiveness": 0.8,
                "time_cost": "medium",
                "tool_requirements": ["version control", "build system"],
                "limitations": ["Requires reproducible error", "May be time-intensive"]
            },
            
            DebuggingStrategy.UNIT_TESTING: {
                "description": "Creating targeted tests to isolate problems",
                "best_for": ["Logic errors", "Regression prevention", "Component validation"],
                "effectiveness": 0.85,
                "time_cost": "medium",
                "tool_requirements": ["testing framework", "test runner"],
                "limitations": ["Requires test writing skills", "Initial setup time"]
            }
        }
    
    def classify_error(
        self,
        error_description: str,
        symptoms: List[str],
        error_message: Optional[str] = None,
        stack_trace: Optional[str] = None
    ) -> ErrorClassification:
        """Classify an error based on available information"""
        
        # Analyze error message and stack trace for category
        category = self._determine_error_category(error_description, error_message, stack_trace)
        
        # Determine severity based on symptoms
        severity = self._assess_severity(symptoms, error_description)
        
        # Generate potential causes
        potential_causes = self._generate_potential_causes(category, symptoms)
        
        # Assess reproducibility and frequency
        reproducibility = self._assess_reproducibility(symptoms)
        frequency = self._assess_frequency(symptoms)
        
        return ErrorClassification(
            classification_id=f"error_class_{self._generate_id()}",
            error_category=category,
            severity=severity,
            error_message=error_message,
            stack_trace=stack_trace,
            symptoms=symptoms,
            potential_causes=potential_causes,
            affected_components=self._identify_affected_components(error_description, stack_trace),
            frequency=frequency,
            reproducibility=reproducibility,
            confidence_level=0.8  # Base confidence, would be refined with more analysis
        )
    
    def _determine_error_category(
        self,
        description: str,
        error_message: Optional[str],
        stack_trace: Optional[str]
    ) -> ErrorCategory:
        """Determine the category of error based on available information"""
        description_lower = description.lower()
        message_lower = (error_message or "").lower()
        trace_lower = (stack_trace or "").lower()
        
        # Check for specific error patterns
        if any(word in description_lower for word in ["syntax", "parse", "compilation"]):
            return ErrorCategory.SYNTAX_ERROR
        
        if any(word in message_lower for word in ["nullpointerexception", "segmentation fault", "access violation"]):
            return ErrorCategory.RUNTIME_ERROR
        
        if any(word in description_lower for word in ["performance", "slow", "timeout", "latency"]):
            return ErrorCategory.PERFORMANCE_ERROR
        
        if any(word in message_lower for word in ["outofmemory", "memory", "heap", "stack overflow"]):
            return ErrorCategory.MEMORY_ERROR
        
        if any(word in description_lower for word in ["deadlock", "race condition", "concurrent", "thread"]):
            return ErrorCategory.CONCURRENCY_ERROR
        
        if any(word in description_lower for word in ["config", "configuration", "setting", "property"]):
            return ErrorCategory.CONFIGURATION_ERROR
        
        if any(word in description_lower for word in ["integration", "api", "service", "connection"]):
            return ErrorCategory.INTEGRATION_ERROR
        
        # Default to logic error if no specific pattern matches
        return ErrorCategory.LOGIC_ERROR
    
    def _assess_severity(self, symptoms: List[str], description: str) -> Severity:
        """Assess the severity of an error"""
        critical_indicators = ["crash", "data loss", "security", "production down", "system failure"]
        high_indicators = ["incorrect results", "performance degradation", "user impact"]
        medium_indicators = ["minor incorrect behavior", "warning messages", "cosmetic issues"]
        
        text = (description + " " + " ".join(symptoms)).lower()
        
        if any(indicator in text for indicator in critical_indicators):
            return Severity.CRITICAL
        elif any(indicator in text for indicator in high_indicators):
            return Severity.HIGH
        elif any(indicator in text for indicator in medium_indicators):
            return Severity.MEDIUM
        else:
            return Severity.LOW
    
    def _generate_potential_causes(self, category: ErrorCategory, symptoms: List[str]) -> List[str]:
        """Generate potential causes based on error category and symptoms"""
        cause_patterns = {
            ErrorCategory.SYNTAX_ERROR: [
                "Missing semicolon or bracket",
                "Incorrect syntax usage",
                "Typo in keyword or identifier"
            ],
            ErrorCategory.RUNTIME_ERROR: [
                "Null pointer dereference",
                "Array index out of bounds",
                "Invalid type casting",
                "Resource not available"
            ],
            ErrorCategory.LOGIC_ERROR: [
                "Incorrect algorithm implementation",
                "Wrong conditional logic",
                "Off-by-one error",
                "Incorrect variable usage"
            ],
            ErrorCategory.PERFORMANCE_ERROR: [
                "Inefficient algorithm",
                "Memory leaks",
                "Excessive database queries",
                "Unoptimized loops"
            ],
            ErrorCategory.MEMORY_ERROR: [
                "Memory leaks",
                "Buffer overflow",
                "Stack overflow from recursion",
                "Insufficient heap space"
            ]
        }
        
        return cause_patterns.get(category, ["Unknown cause pattern"])
    
    def _assess_reproducibility(self, symptoms: List[str]) -> str:
        """Assess how reproducible the error is"""
        symptoms_text = " ".join(symptoms).lower()
        
        if any(word in symptoms_text for word in ["always", "every time", "consistently"]):
            return "always"
        elif any(word in symptoms_text for word in ["sometimes", "intermittent", "occasionally"]):
            return "sometimes"
        elif any(word in symptoms_text for word in ["never", "cannot reproduce", "one time"]):
            return "never"
        else:
            return "sometimes"  # Default assumption
    
    def _assess_frequency(self, symptoms: List[str]) -> str:
        """Assess how frequently the error occurs"""
        symptoms_text = " ".join(symptoms).lower()
        
        if any(word in symptoms_text for word in ["constant", "continuous", "always"]):
            return "constant"
        elif any(word in symptoms_text for word in ["frequent", "often", "regular"]):
            return "frequent"
        elif any(word in symptoms_text for word in ["occasional", "sometimes", "sporadic"]):
            return "occasional"
        else:
            return "rare"
    
    def _identify_affected_components(self, description: str, stack_trace: Optional[str]) -> List[str]:
        """Identify which components are affected by the error"""
        components = []
        text = description.lower()
        
        # Common component patterns
        if "database" in text or "sql" in text:
            components.append("database")
        if "ui" in text or "interface" in text or "frontend" in text:
            components.append("user_interface")
        if "api" in text or "service" in text or "backend" in text:
            components.append("backend_service")
        if "network" in text or "connection" in text:
            components.append("network")
        
        # Extract from stack trace if available
        if stack_trace:
            # Simple extraction of class/module names
            lines = stack_trace.split('\n')
            for line in lines:
                if 'at ' in line or 'in ' in line:
                    # Extract potential component names
                    parts = line.split('.')
                    if len(parts) > 1:
                        components.append(parts[0].strip())
        
        return list(set(components)) if components else ["unknown"]
    
    def recommend_debugging_strategy(
        self,
        error_classification: ErrorClassification,
        context: DebugContext
    ) -> List[DebuggingRecommendation]:
        """Recommend debugging strategies based on error and context"""
        recommendations = []
        
        for strategy, profile in self.strategy_profiles.items():
            match_score = self._calculate_strategy_match(
                strategy, profile, error_classification, context
            )
            
            if match_score > 0.3:  # Threshold for consideration
                recommendation = DebuggingRecommendation(
                    recommendation_id=f"rec_{strategy.value}_{self._generate_id()}",
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
        
        return sorted(recommendations, key=lambda x: x.expected_effectiveness, reverse=True)
    
    def _calculate_strategy_match(
        self,
        strategy: DebuggingStrategy,
        profile: Dict[str, Any],
        classification: ErrorClassification,
        context: DebugContext
    ) -> float:
        """Calculate how well a strategy matches the current situation"""
        score = 0.5  # Base score
        
        # Check if strategy is good for this error category
        category_matches = {
            ErrorCategory.SYNTAX_ERROR: [DebuggingStrategy.STATIC_ANALYSIS, DebuggingStrategy.CODE_REVIEW],
            ErrorCategory.LOGIC_ERROR: [DebuggingStrategy.INTERACTIVE_DEBUGGING, DebuggingStrategy.UNIT_TESTING],
            ErrorCategory.PERFORMANCE_ERROR: [DebuggingStrategy.PROFILING, DebuggingStrategy.LOG_ANALYSIS],
            ErrorCategory.MEMORY_ERROR: [DebuggingStrategy.PROFILING, DebuggingStrategy.STATIC_ANALYSIS]
        }
        
        if strategy in category_matches.get(classification.error_category, []):
            score += 0.3
        
        # Check tool availability
        required_tools = profile.get("tool_requirements", [])
        available_tools = [tool.lower() for tool in context.available_tools]
        
        if all(tool.lower() in " ".join(available_tools) for tool in required_tools):
            score += 0.2
        else:
            score -= 0.1
        
        # Consider time constraints
        if context.time_constraints:
            if "urgent" in context.time_constraints.lower() and profile["time_cost"] == "high":
                score -= 0.2
            elif profile["time_cost"] == "low":
                score += 0.1
        
        return min(1.0, max(0.0, score))
    
    def _generate_strategy_reasoning(
        self,
        strategy: DebuggingStrategy,
        profile: Dict[str, Any],
        classification: ErrorClassification
    ) -> str:
        """Generate reasoning for why a strategy is recommended"""
        return (f"{strategy.value.replace('_', ' ').title()} is recommended because "
                f"it is effective for {classification.error_category.value.replace('_', ' ')} "
                f"and has {profile['effectiveness']*100:.0f}% effectiveness rate. "
                f"{profile['description']}")
    
    def _get_strategy_prerequisites(self, strategy: DebuggingStrategy) -> List[str]:
        """Get prerequisites for a debugging strategy"""
        prerequisites_map = {
            DebuggingStrategy.INTERACTIVE_DEBUGGING: ["Debugger setup", "Symbol information", "Reproducible error"],
            DebuggingStrategy.UNIT_TESTING: ["Testing framework", "Test writing skills", "Isolated test environment"],
            DebuggingStrategy.PROFILING: ["Profiling tools", "Performance baseline", "Representative workload"],
            DebuggingStrategy.STATIC_ANALYSIS: ["Static analysis tools", "Code access", "Tool configuration"]
        }
        
        return prerequisites_map.get(strategy, ["Basic understanding of the codebase"])
    
    def _get_alternative_strategies(self, strategy: DebuggingStrategy) -> List[DebuggingStrategy]:
        """Get alternative strategies for a given strategy"""
        alternatives_map = {
            DebuggingStrategy.PRINT_DEBUGGING: [DebuggingStrategy.INTERACTIVE_DEBUGGING, DebuggingStrategy.LOG_ANALYSIS],
            DebuggingStrategy.INTERACTIVE_DEBUGGING: [DebuggingStrategy.PRINT_DEBUGGING, DebuggingStrategy.UNIT_TESTING],
            DebuggingStrategy.UNIT_TESTING: [DebuggingStrategy.INTEGRATION_TESTING, DebuggingStrategy.INTERACTIVE_DEBUGGING],
            DebuggingStrategy.PROFILING: [DebuggingStrategy.LOG_ANALYSIS, DebuggingStrategy.STATIC_ANALYSIS]
        }
        
        return alternatives_map.get(strategy, [])
    
    def perform_root_cause_analysis(
        self,
        problem_statement: str,
        evidence: List[str],
        method: str = "five_whys"
    ) -> RootCauseAnalysis:
        """Perform root cause analysis using specified method"""
        
        if method == "five_whys":
            return self._five_whys_analysis(problem_statement, evidence)
        elif method == "fishbone":
            return self._fishbone_analysis(problem_statement, evidence)
        else:
            # Default to five whys
            return self._five_whys_analysis(problem_statement, evidence)
    
    def _five_whys_analysis(self, problem_statement: str, evidence: List[str]) -> RootCauseAnalysis:
        """Perform Five Whys root cause analysis"""
        
        # Simulate Five Whys process
        whys = [
            f"Why did the problem occur? {problem_statement}",
            "Why was the immediate cause not prevented?",
            "Why was the prevention mechanism insufficient?",
            "Why was the process design inadequate?",
            "Why was the system design flawed?"
        ]
        
        root_causes = [
            "Insufficient error handling in the code",
            "Lack of proper validation mechanisms",
            "Inadequate testing coverage"
        ]
        
        contributing_factors = [
            "Time pressure during development",
            "Insufficient requirements clarity",
            "Limited code review process"
        ]
        
        prevention_measures = [
            "Implement comprehensive error handling",
            "Add input validation at all entry points",
            "Increase test coverage to 90%+",
            "Establish mandatory code review process"
        ]
        
        return RootCauseAnalysis(
            analysis_id=f"rca_{self._generate_id()}",
            problem_statement=problem_statement,
            root_causes=root_causes,
            contributing_factors=contributing_factors,
            analysis_method="five_whys",
            evidence_chain=evidence,
            prevention_measures=prevention_measures,
            systemic_issues=["Development process gaps", "Quality assurance weaknesses"],
            confidence_score=0.8
        )
    
    def _fishbone_analysis(self, problem_statement: str, evidence: List[str]) -> RootCauseAnalysis:
        """Perform Fishbone (Ishikawa) root cause analysis"""
        
        # Categories: People, Process, Technology, Environment, Materials, Methods
        root_causes = [
            "Insufficient developer training (People)",
            "Inadequate development process (Process)",
            "Outdated development tools (Technology)",
            "High-pressure work environment (Environment)"
        ]
        
        contributing_factors = [
            "Lack of proper documentation",
            "Insufficient testing resources",
            "Unclear requirements",
            "Limited debugging tools"
        ]
        
        prevention_measures = [
            "Provide comprehensive training programs",
            "Establish robust development processes",
            "Upgrade development and testing tools",
            "Improve work environment and reduce pressure"
        ]
        
        return RootCauseAnalysis(
            analysis_id=f"rca_fishbone_{self._generate_id()}",
            problem_statement=problem_statement,
            root_causes=root_causes,
            contributing_factors=contributing_factors,
            analysis_method="fishbone",
            evidence_chain=evidence,
            prevention_measures=prevention_measures,
            systemic_issues=["Organizational capability gaps", "Process maturity issues"],
            confidence_score=0.75
        )
    
    def create_debugging_session(
        self,
        context: DebugContext,
        error_classification: ErrorClassification
    ) -> DebuggingSession:
        """Create a new debugging session"""
        
        # Generate initial hypotheses based on error classification
        hypotheses = self._generate_initial_hypotheses(error_classification)
        
        # Create initial debugging steps
        debugging_steps = self._create_initial_debugging_steps(error_classification, context)
        
        return DebuggingSession(
            session_id=f"debug_session_{self._generate_id()}",
            context=context,
            error_classification=error_classification,
            hypotheses=hypotheses,
            debugging_steps=debugging_steps,
            root_cause_analysis=None,  # To be filled during session
            resolution=None,  # To be filled when resolved
            lessons_learned=[],  # To be filled during session
            prevention_recommendations=[],  # To be filled at end
            session_duration=None,  # To be calculated
            success_rate=0.0  # To be calculated
        )
    
    def _generate_initial_hypotheses(self, classification: ErrorClassification) -> List[DebuggingHypothesis]:
        """Generate initial hypotheses based on error classification"""
        hypotheses = []
        
        for i, cause in enumerate(classification.potential_causes[:3]):  # Top 3 causes
            hypothesis = DebuggingHypothesis(
                hypothesis_id=f"hyp_{i+1}_{self._generate_id()}",
                description=cause,
                confidence_level=0.7 - (i * 0.2),  # Decreasing confidence
                supporting_evidence=classification.symptoms[:2],
                contradicting_evidence=[],
                test_plan=[
                    f"Test scenario related to: {cause}",
                    "Verify hypothesis through targeted testing",
                    "Collect evidence to support or refute hypothesis"
                ],
                estimated_effort="medium",
                risk_level="low",
                alternative_hypotheses=classification.potential_causes[i+1:i+3]
            )
            hypotheses.append(hypothesis)
        
        return hypotheses
    
    def _create_initial_debugging_steps(
        self,
        classification: ErrorClassification,
        context: DebugContext
    ) -> List[DebuggingStep]:
        """Create initial debugging steps for a session"""
        steps = []
        
        # Step 1: Problem verification
        steps.append(DebuggingStep(
            step_id=f"step_1_{self._generate_id()}",
            phase=DebuggingPhase.PROBLEM_IDENTIFICATION,
            description="Verify and document the problem",
            strategy_used=DebuggingStrategy.LOG_ANALYSIS,
            expected_outcome="Clear understanding of the problem symptoms",
            actual_outcome=None,
            tools_used=["logs", "error reports"],
            evidence_gathered=[],
            time_spent=None,
            success=None,
            next_steps=["Attempt to reproduce the problem"]
        ))
        
        # Step 2: Reproduction attempt
        steps.append(DebuggingStep(
            step_id=f"step_2_{self._generate_id()}",
            phase=DebuggingPhase.REPRODUCTION,
            description="Attempt to reproduce the problem consistently",
            strategy_used=DebuggingStrategy.HYPOTHESIS_TESTING,
            expected_outcome="Reproducible error condition",
            actual_outcome=None,
            tools_used=["test environment", "test data"],
            evidence_gathered=[],
            time_spent=None,
            success=None,
            next_steps=["Isolate the problem area"]
        ))
        
        return steps