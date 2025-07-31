"""
Structured Argumentation Models for Clear Thinking FastMCP

Provides logic chain construction, argument validity assessment, evidence evaluation
frameworks, and reasoning quality validation for structured arguments.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Set, Tuple
from enum import Enum

from .base import CognitiveToolBase, CognitiveInputBase, CognitiveOutputBase, ComplexityLevel


class ArgumentType(str, Enum):
    """Types of arguments"""
    DEDUCTIVE = "deductive"
    INDUCTIVE = "inductive"
    ABDUCTIVE = "abductive"
    ANALOGICAL = "analogical"
    CAUSAL = "causal"
    STATISTICAL = "statistical"
    AUTHORITATIVE = "authoritative"
    MORAL = "moral"
    PRAGMATIC = "pragmatic"


class LogicalFallacy(str, Enum):
    """Common logical fallacies"""
    AD_HOMINEM = "ad_hominem"
    STRAW_MAN = "straw_man"
    FALSE_DICHOTOMY = "false_dichotomy"
    SLIPPERY_SLOPE = "slippery_slope"
    CIRCULAR_REASONING = "circular_reasoning"
    APPEAL_TO_AUTHORITY = "appeal_to_authority"
    APPEAL_TO_EMOTION = "appeal_to_emotion"
    HASTY_GENERALIZATION = "hasty_generalization"
    FALSE_CAUSE = "false_cause"
    BANDWAGON = "bandwagon"
    RED_HERRING = "red_herring"
    BEGGING_THE_QUESTION = "begging_the_question"


class EvidenceType(str, Enum):
    """Types of evidence"""
    EMPIRICAL = "empirical"
    STATISTICAL = "statistical"
    ANECDOTAL = "anecdotal"
    EXPERT_TESTIMONY = "expert_testimony"
    DOCUMENTARY = "documentary"
    EXPERIMENTAL = "experimental"
    OBSERVATIONAL = "observational"
    THEORETICAL = "theoretical"
    HISTORICAL = "historical"
    COMPARATIVE = "comparative"


class StrengthLevel(str, Enum):
    """Strength levels for arguments and evidence"""
    VERY_STRONG = "very_strong"
    STRONG = "strong"
    MODERATE = "moderate"
    WEAK = "weak"
    VERY_WEAK = "very_weak"


@dataclass
class Premise:
    """A premise in an argument"""
    premise_id: str
    statement: str
    premise_type: str  # major, minor, supporting, assumption
    truth_value: Optional[bool]
    certainty_level: float  # 0.0 to 1.0
    supporting_evidence: List[str]
    source: Optional[str]
    is_implicit: bool


@dataclass
class Evidence:
    """Evidence supporting a premise or conclusion"""
    evidence_id: str
    description: str
    evidence_type: EvidenceType
    source: str
    quality_score: float  # 0.0 to 1.0
    relevance_score: float  # 0.0 to 1.0
    reliability_assessment: str
    supporting_premises: List[str]
    contradicting_evidence: List[str]
    context: str
    limitations: List[str]


@dataclass
class LogicChain:
    """A chain of logical reasoning"""
    chain_id: str
    premises: List[Premise]
    inference_rules: List[str]
    intermediate_conclusions: List[str]
    final_conclusion: str
    argument_type: ArgumentType
    validity_assessment: str
    soundness_assessment: str
    logical_gaps: List[str]
    strength_rating: StrengthLevel


@dataclass
class ArgumentStructure:
    """Complete structure of an argument"""
    argument_id: str
    claim: str
    logic_chains: List[LogicChain]
    supporting_evidence: List[Evidence]
    counterarguments: List[str]
    rebuttals: List[str]
    assumptions: List[str]
    context: str
    argument_strength: StrengthLevel
    confidence_level: float


@dataclass
class FallacyDetection:
    """Detection of logical fallacies"""
    detection_id: str
    fallacy_type: LogicalFallacy
    location: str  # where in the argument
    description: str
    severity: StrengthLevel
    correction_suggestion: str
    impact_on_argument: str
    confidence: float


@dataclass
class ArgumentAnalysis:
    """Analysis of argument quality and structure"""
    analysis_id: str
    argument: ArgumentStructure
    validity_score: float
    soundness_score: float
    persuasiveness_score: float
    logical_consistency: float
    evidence_quality: float
    detected_fallacies: List[FallacyDetection]
    strengths: List[str]
    weaknesses: List[str]
    improvement_suggestions: List[str]
    overall_quality: StrengthLevel


@dataclass
class CounterargumentAnalysis:
    """Analysis of counterarguments and responses"""
    analysis_id: str
    original_argument: str
    counterarguments: List[str]
    counterargument_strength: Dict[str, StrengthLevel]
    potential_rebuttals: Dict[str, List[str]]
    argument_vulnerability: float
    defensive_strategies: List[str]
    strengthening_recommendations: List[str]


@dataclass
class DebateStructure:
    """Structure for analyzing debates and discussions"""
    debate_id: str
    topic: str
    positions: List[str]
    arguments_by_position: Dict[str, List[ArgumentStructure]]
    cross_references: Dict[str, List[str]]  # argument -> related arguments
    consensus_points: List[str]
    contentious_points: List[str]
    resolution_pathways: List[str]
    quality_assessment: Dict[str, float]


class StructuredArgumentationModel(CognitiveToolBase):
    """
    Structured Argumentation cognitive model for logic analysis and construction.
    
    Capabilities:
    - Argument structure analysis
    - Logic chain validation
    - Fallacy detection
    - Evidence evaluation
    - Counterargument analysis
    """
    
    def __init__(self):
        super().__init__()
        self._initialize_fallacy_patterns()
        self._initialize_argument_templates()
    
    def _initialize_fallacy_patterns(self):
        """Initialize patterns for detecting logical fallacies"""
        self.fallacy_patterns = {
            LogicalFallacy.AD_HOMINEM: {
                "keywords": ["you're wrong because you", "can't trust them because", "coming from someone who"],
                "pattern": "Attacking the person rather than the argument",
                "severity": "high"
            },
            LogicalFallacy.STRAW_MAN: {
                "keywords": ["so you're saying", "your position is that", "you want to"],
                "pattern": "Misrepresenting opponent's position",
                "severity": "high"
            },
            LogicalFallacy.FALSE_DICHOTOMY: {
                "keywords": ["either...or", "only two options", "you must choose"],
                "pattern": "Presenting only two options when more exist",
                "severity": "medium"
            },
            LogicalFallacy.SLIPPERY_SLOPE: {
                "keywords": ["if we allow this", "this will lead to", "slippery slope"],
                "pattern": "Assuming one event will lead to extreme consequences",
                "severity": "medium"
            },
            LogicalFallacy.CIRCULAR_REASONING: {
                "keywords": ["because it is", "by definition", "obviously"],
                "pattern": "Conclusion assumes the premise",
                "severity": "high"
            }
        }
    
    def _initialize_argument_templates(self):
        """Initialize templates for different argument types"""
        self.argument_templates = {
            ArgumentType.DEDUCTIVE: {
                "structure": ["Major premise", "Minor premise", "Conclusion"],
                "validity_criteria": ["Logical form", "Premise truth", "Valid inference"],
                "example": "All humans are mortal (major) → Socrates is human (minor) → Socrates is mortal (conclusion)"
            },
            ArgumentType.INDUCTIVE: {
                "structure": ["Observations", "Pattern", "Generalization"],
                "validity_criteria": ["Sample size", "Representativeness", "Pattern strength"],
                "example": "Multiple observations → Pattern identification → General principle"
            },
            ArgumentType.CAUSAL: {
                "structure": ["Cause identification", "Mechanism", "Effect demonstration"],
                "validity_criteria": ["Temporal sequence", "Correlation strength", "Alternative causes"],
                "example": "X causes Y through mechanism Z"
            }
        }
    
    def create_premise(
        self,
        statement: str,
        premise_type: str = "supporting",
        certainty_level: float = 0.8,
        supporting_evidence: Optional[List[str]] = None
    ) -> Premise:
        """Create a premise for an argument"""
        return Premise(
            premise_id=f"premise_{self._generate_id()}",
            statement=statement,
            premise_type=premise_type,
            truth_value=None,  # To be determined through analysis
            certainty_level=certainty_level,
            supporting_evidence=supporting_evidence or [],
            source=None,
            is_implicit=False
        )
    
    def create_evidence(
        self,
        description: str,
        evidence_type: EvidenceType,
        source: str,
        quality_score: float = 0.7,
        relevance_score: float = 0.8
    ) -> Evidence:
        """Create evidence to support premises or conclusions"""
        return Evidence(
            evidence_id=f"evidence_{self._generate_id()}",
            description=description,
            evidence_type=evidence_type,
            source=source,
            quality_score=quality_score,
            relevance_score=relevance_score,
            reliability_assessment=self._assess_reliability(source, evidence_type),
            supporting_premises=[],
            contradicting_evidence=[],
            context="",
            limitations=[]
        )
    
    def _assess_reliability(self, source: str, evidence_type: EvidenceType) -> str:
        """Assess the reliability of evidence based on source and type"""
        source_lower = source.lower()
        
        # High reliability sources
        if any(indicator in source_lower for indicator in ["peer reviewed", "scientific journal", "expert study"]):
            if evidence_type in [EvidenceType.EMPIRICAL, EvidenceType.EXPERIMENTAL]:
                return "high"
            else:
                return "moderate"
        
        # Medium reliability sources
        elif any(indicator in source_lower for indicator in ["government report", "professional organization"]):
            return "moderate"
        
        # Lower reliability sources
        elif any(indicator in source_lower for indicator in ["blog", "social media", "opinion piece"]):
            return "low"
        
        return "unknown"
    
    def construct_logic_chain(
        self,
        premises: List[Premise],
        conclusion: str,
        argument_type: ArgumentType
    ) -> LogicChain:
        """Construct a logic chain from premises to conclusion"""
        
        # Generate inference rules based on argument type
        inference_rules = self._generate_inference_rules(argument_type, premises)
        
        # Create intermediate conclusions if needed
        intermediate_conclusions = self._generate_intermediate_conclusions(premises, conclusion)
        
        # Assess validity and soundness
        validity = self._assess_validity(premises, conclusion, argument_type)
        soundness = self._assess_soundness(premises, conclusion, validity)
        
        # Identify logical gaps
        logical_gaps = self._identify_logical_gaps(premises, conclusion, argument_type)
        
        # Determine strength rating
        strength_rating = self._determine_strength_rating(validity, soundness, logical_gaps)
        
        return LogicChain(
            chain_id=f"chain_{self._generate_id()}",
            premises=premises,
            inference_rules=inference_rules,
            intermediate_conclusions=intermediate_conclusions,
            final_conclusion=conclusion,
            argument_type=argument_type,
            validity_assessment=validity,
            soundness_assessment=soundness,
            logical_gaps=logical_gaps,
            strength_rating=strength_rating
        )
    
    def _generate_inference_rules(self, argument_type: ArgumentType, premises: List[Premise]) -> List[str]:
        """Generate appropriate inference rules for the argument type"""
        if argument_type == ArgumentType.DEDUCTIVE:
            return ["Modus ponens", "Universal instantiation", "Hypothetical syllogism"]
        elif argument_type == ArgumentType.INDUCTIVE:
            return ["Generalization", "Statistical inference", "Pattern recognition"]
        elif argument_type == ArgumentType.CAUSAL:
            return ["Causal inference", "Mill's methods", "Temporal precedence"]
        else:
            return ["Standard logical inference"]
    
    def _generate_intermediate_conclusions(self, premises: List[Premise], final_conclusion: str) -> List[str]:
        """Generate intermediate conclusions in the reasoning chain"""
        if len(premises) <= 2:
            return []
        
        # Generate intermediate steps based on premise structure
        intermediate = []
        for i in range(1, len(premises)):
            intermediate.append(f"Intermediate conclusion from premises 1-{i+1}")
        
        return intermediate
    
    def _assess_validity(self, premises: List[Premise], conclusion: str, argument_type: ArgumentType) -> str:
        """Assess the logical validity of the argument"""
        # Simplified validity assessment
        if argument_type == ArgumentType.DEDUCTIVE:
            # Check if conclusion follows necessarily from premises
            if len(premises) >= 2:
                return "valid"
            else:
                return "insufficient_premises"
        elif argument_type == ArgumentType.INDUCTIVE:
            # Check strength of inductive inference
            return "strong" if len(premises) >= 3 else "weak"
        else:
            return "plausible"
    
    def _assess_soundness(self, premises: List[Premise], conclusion: str, validity: str) -> str:
        """Assess the soundness of the argument (validity + true premises)"""
        if validity not in ["valid", "strong"]:
            return "unsound"
        
        # Check premise truth (simplified)
        true_premises = sum(1 for p in premises if p.certainty_level > 0.7)
        if true_premises == len(premises):
            return "sound"
        elif true_premises > len(premises) / 2:
            return "partially_sound"
        else:
            return "unsound"
    
    def _identify_logical_gaps(self, premises: List[Premise], conclusion: str, argument_type: ArgumentType) -> List[str]:
        """Identify gaps in the logical reasoning"""
        gaps = []
        
        # Check for missing premises
        if len(premises) < 2:
            gaps.append("Insufficient premises for complete argument")
        
        # Check for unstated assumptions
        implicit_premises = [p for p in premises if p.is_implicit]
        if len(implicit_premises) > 0:
            gaps.append("Contains implicit assumptions that should be stated")
        
        # Check for weak evidence
        weak_premises = [p for p in premises if p.certainty_level < 0.5]
        if weak_premises:
            gaps.append("Some premises have low certainty levels")
        
        return gaps
    
    def _determine_strength_rating(self, validity: str, soundness: str, gaps: List[str]) -> StrengthLevel:
        """Determine overall strength rating for the logic chain"""
        if validity == "valid" and soundness == "sound" and len(gaps) == 0:
            return StrengthLevel.VERY_STRONG
        elif validity in ["valid", "strong"] and soundness in ["sound", "partially_sound"] and len(gaps) <= 1:
            return StrengthLevel.STRONG
        elif validity in ["valid", "strong", "plausible"] and len(gaps) <= 2:
            return StrengthLevel.MODERATE
        elif len(gaps) <= 3:
            return StrengthLevel.WEAK
        else:
            return StrengthLevel.VERY_WEAK
    
    def detect_fallacies(self, argument_text: str) -> List[FallacyDetection]:
        """Detect logical fallacies in argument text"""
        detections = []
        text_lower = argument_text.lower()
        
        for fallacy_type, pattern_info in self.fallacy_patterns.items():
            for keyword in pattern_info["keywords"]:
                if keyword in text_lower:
                    detection = FallacyDetection(
                        detection_id=f"fallacy_{fallacy_type.value}_{self._generate_id()}",
                        fallacy_type=fallacy_type,
                        location=f"Near keyword: '{keyword}'",
                        description=pattern_info["pattern"],
                        severity=StrengthLevel.HIGH if pattern_info["severity"] == "high" else StrengthLevel.MEDIUM,
                        correction_suggestion=self._get_fallacy_correction(fallacy_type),
                        impact_on_argument="Weakens logical validity",
                        confidence=0.7  # Pattern matching confidence
                    )
                    detections.append(detection)
                    break  # Only detect once per fallacy type
        
        return detections
    
    def _get_fallacy_correction(self, fallacy_type: LogicalFallacy) -> str:
        """Get correction suggestion for a specific fallacy"""
        corrections = {
            LogicalFallacy.AD_HOMINEM: "Focus on the argument itself, not the person making it",
            LogicalFallacy.STRAW_MAN: "Represent the opponent's position accurately and completely",
            LogicalFallacy.FALSE_DICHOTOMY: "Consider additional alternatives beyond the two presented",
            LogicalFallacy.SLIPPERY_SLOPE: "Provide evidence for each step in the claimed chain of events",
            LogicalFallacy.CIRCULAR_REASONING: "Provide independent evidence for the conclusion"
        }
        return corrections.get(fallacy_type, "Review the logical structure for validity")
    
    def analyze_argument_structure(self, argument: ArgumentStructure) -> ArgumentAnalysis:
        """Perform comprehensive analysis of argument structure"""
        
        # Calculate validity score based on logic chains
        validity_scores = []
        for chain in argument.logic_chains:
            if chain.validity_assessment == "valid":
                validity_scores.append(1.0)
            elif chain.validity_assessment == "strong":
                validity_scores.append(0.8)
            elif chain.validity_assessment == "plausible":
                validity_scores.append(0.6)
            else:
                validity_scores.append(0.3)
        
        validity_score = sum(validity_scores) / len(validity_scores) if validity_scores else 0.5
        
        # Calculate soundness score
        soundness_scores = []
        for chain in argument.logic_chains:
            if chain.soundness_assessment == "sound":
                soundness_scores.append(1.0)
            elif chain.soundness_assessment == "partially_sound":
                soundness_scores.append(0.7)
            else:
                soundness_scores.append(0.3)
        
        soundness_score = sum(soundness_scores) / len(soundness_scores) if soundness_scores else 0.5
        
        # Calculate evidence quality
        if argument.supporting_evidence:
            evidence_quality = sum(e.quality_score for e in argument.supporting_evidence) / len(argument.supporting_evidence)
        else:
            evidence_quality = 0.5
        
        # Detect fallacies in the argument
        argument_text = f"{argument.claim} {' '.join(argument.counterarguments)} {' '.join(argument.rebuttals)}"
        detected_fallacies = self.detect_fallacies(argument_text)
        
        # Calculate logical consistency
        gaps_count = sum(len(chain.logical_gaps) for chain in argument.logic_chains)
        logical_consistency = max(0.0, 1.0 - (gaps_count * 0.1))
        
        # Calculate persuasiveness (combination of factors)
        persuasiveness_score = (validity_score * 0.3 + soundness_score * 0.3 + 
                              evidence_quality * 0.2 + logical_consistency * 0.2)
        
        # Identify strengths and weaknesses
        strengths = []
        weaknesses = []
        
        if validity_score > 0.8:
            strengths.append("Strong logical validity")
        elif validity_score < 0.5:
            weaknesses.append("Weak logical structure")
        
        if evidence_quality > 0.8:
            strengths.append("High-quality supporting evidence")
        elif evidence_quality < 0.5:
            weaknesses.append("Poor quality or insufficient evidence")
        
        if detected_fallacies:
            weaknesses.append(f"Contains {len(detected_fallacies)} logical fallacies")
        else:
            strengths.append("No obvious logical fallacies detected")
        
        # Determine overall quality
        overall_score = (validity_score + soundness_score + evidence_quality + logical_consistency) / 4
        if overall_score > 0.8:
            overall_quality = StrengthLevel.VERY_STRONG
        elif overall_score > 0.6:
            overall_quality = StrengthLevel.STRONG
        elif overall_score > 0.4:
            overall_quality = StrengthLevel.MODERATE
        elif overall_score > 0.2:
            overall_quality = StrengthLevel.WEAK
        else:
            overall_quality = StrengthLevel.VERY_WEAK
        
        # Generate improvement suggestions
        improvement_suggestions = []
        if validity_score < 0.7:
            improvement_suggestions.append("Strengthen logical connections between premises and conclusion")
        if evidence_quality < 0.7:
            improvement_suggestions.append("Add higher-quality supporting evidence")
        if logical_consistency < 0.7:
            improvement_suggestions.append("Address logical gaps and unstated assumptions")
        if detected_fallacies:
            improvement_suggestions.append("Remove or correct logical fallacies")
        
        return ArgumentAnalysis(
            analysis_id=f"analysis_{self._generate_id()}",
            argument=argument,
            validity_score=validity_score,
            soundness_score=soundness_score,
            persuasiveness_score=persuasiveness_score,
            logical_consistency=logical_consistency,
            evidence_quality=evidence_quality,
            detected_fallacies=detected_fallacies,
            strengths=strengths,
            weaknesses=weaknesses,
            improvement_suggestions=improvement_suggestions,
            overall_quality=overall_quality
        )
    
    def generate_counterarguments(self, argument: ArgumentStructure) -> CounterargumentAnalysis:
        """Generate and analyze potential counterarguments"""
        
        # Generate counterarguments based on premises and evidence
        counterarguments = []
        
        # Challenge premises
        for chain in argument.logic_chains:
            for premise in chain.premises:
                if premise.certainty_level < 0.8:
                    counterarguments.append(f"Challenge premise: {premise.statement}")
        
        # Challenge evidence quality
        for evidence in argument.supporting_evidence:
            if evidence.quality_score < 0.7:
                counterarguments.append(f"Question evidence reliability: {evidence.description}")
        
        # Challenge logical connections
        for chain in argument.logic_chains:
            if chain.logical_gaps:
                counterarguments.append(f"Identify logical gap: {chain.logical_gaps[0]}")
        
        # Alternative explanations
        counterarguments.append("Propose alternative explanation for the same evidence")
        
        # Assess counterargument strength
        counterargument_strength = {}
        for counter in counterarguments:
            if "challenge premise" in counter.lower():
                counterargument_strength[counter] = StrengthLevel.STRONG
            elif "question evidence" in counter.lower():
                counterargument_strength[counter] = StrengthLevel.MODERATE
            else:
                counterargument_strength[counter] = StrengthLevel.WEAK
        
        # Generate potential rebuttals
        potential_rebuttals = {}
        for counter in counterarguments:
            potential_rebuttals[counter] = [
                "Provide additional supporting evidence",
                "Clarify the logical connection",
                "Address the specific concern raised"
            ]
        
        # Calculate argument vulnerability
        strong_counters = [c for c, s in counterargument_strength.items() if s == StrengthLevel.STRONG]
        vulnerability = len(strong_counters) / max(1, len(counterarguments))
        
        return CounterargumentAnalysis(
            analysis_id=f"counter_analysis_{self._generate_id()}",
            original_argument=argument.claim,
            counterarguments=counterarguments,
            counterargument_strength=counterargument_strength,
            potential_rebuttals=potential_rebuttals,
            argument_vulnerability=vulnerability,
            defensive_strategies=[
                "Strengthen weak premises with additional evidence",
                "Address potential counterarguments proactively",
                "Acknowledge limitations while maintaining core argument"
            ],
            strengthening_recommendations=[
                "Add more diverse evidence sources",
                "Make implicit assumptions explicit",
                "Consider and address alternative explanations"
            ]
        )