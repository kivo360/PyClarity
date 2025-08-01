"""
Structured Argumentation Analyzer

Provides logic chain construction, argument validity assessment, evidence evaluation,
and reasoning quality validation for structured arguments.
"""

import asyncio
import time
import re
from typing import List, Dict, Any, Optional, Set, Tuple
from collections import defaultdict

from .models import (
    StructuredArgumentationContext,
    StructuredArgumentationResult,
    ArgumentStructure,
    ArgumentAnalysis,
    CounterargumentAnalysis,
    DebateStructure,
    LogicChain,
    Premise,
    Evidence,
    FallacyDetection,
    ArgumentType,
    LogicalFallacy,
    EvidenceType,
    StrengthLevel
)


class StructuredArgumentationAnalyzer:
    """
    Structured Argumentation Analyzer for logic analysis and construction.
    
    Capabilities:
    - Argument structure analysis
    - Logic chain validation
    - Fallacy detection
    - Evidence evaluation
    - Counterargument analysis
    """
    
    def __init__(self):
        """Initialize the Structured Argumentation Analyzer"""
        self._initialize_fallacy_patterns()
        self._initialize_argument_templates()
        self._initialize_evidence_patterns()
    
    def _initialize_fallacy_patterns(self):
        """Initialize patterns for detecting logical fallacies"""
        self.fallacy_patterns = {
            LogicalFallacy.AD_HOMINEM: {
                "keywords": ["you're wrong because you", "can't trust them because", "coming from someone who", "you people"],
                "pattern": r"(?:you|they|he|she).{0,30}(?:wrong|can't trust|bad|stupid|evil)",
                "severity": "high"
            },
            LogicalFallacy.STRAW_MAN: {
                "keywords": ["so you're saying", "your position is that", "you want to", "you believe"],
                "pattern": r"so you(?:'re| are) saying.{10,100}",
                "severity": "high"
            },
            LogicalFallacy.FALSE_DICHOTOMY: {
                "keywords": ["either...or", "only two options", "you must choose", "it's either"],
                "pattern": r"(?:either|only).{0,50}(?:or|two|choice)",
                "severity": "medium"
            },
            LogicalFallacy.SLIPPERY_SLOPE: {
                "keywords": ["if we allow this", "this will lead to", "slippery slope", "next thing you know"],
                "pattern": r"if.{0,20}(?:then|will lead|result in).{20,100}",
                "severity": "medium"
            },
            LogicalFallacy.CIRCULAR_REASONING: {
                "keywords": ["because it is", "by definition", "obviously", "it's true because"],
                "pattern": r"(?:because|since|as).{10,50}(?:it is|obviously|by definition)",
                "severity": "high"
            },
            LogicalFallacy.APPEAL_TO_AUTHORITY: {
                "keywords": ["expert says", "according to", "famous person", "studies show"],
                "pattern": r"(?:expert|authority|famous).{0,30}says?",
                "severity": "medium"
            },
            LogicalFallacy.APPEAL_TO_EMOTION: {
                "keywords": ["think of the children", "imagine if", "how would you feel", "heartbreaking"],
                "pattern": r"(?:think|imagine|feel|heart).{0,30}(?:children|family|tragic|sad)",
                "severity": "medium"
            },
            LogicalFallacy.HASTY_GENERALIZATION: {
                "keywords": ["all", "every", "always", "never", "everyone"],
                "pattern": r"(?:all|every|always|never|everyone).{10,100}",
                "severity": "medium"
            }
        }
    
    def _initialize_argument_templates(self):
        """Initialize templates for different argument types"""
        self.argument_templates = {
            ArgumentType.DEDUCTIVE: {
                "structure": ["Major premise", "Minor premise", "Conclusion"],
                "validity_criteria": ["Logical form", "Premise truth", "Valid inference"],
                "strength_indicators": ["necessary conclusion", "follows logically", "must be true"]
            },
            ArgumentType.INDUCTIVE: {
                "structure": ["Observations", "Pattern", "Generalization"],
                "validity_criteria": ["Sample size", "Representativeness", "Pattern strength"],
                "strength_indicators": ["likely", "probably", "strong evidence suggests"]
            },
            ArgumentType.CAUSAL: {
                "structure": ["Cause identification", "Mechanism", "Effect demonstration"],
                "validity_criteria": ["Temporal sequence", "Correlation strength", "Alternative causes"],
                "strength_indicators": ["causes", "leads to", "results in", "because of"]
            },
            ArgumentType.ANALOGICAL: {
                "structure": ["Source analogy", "Similarity mapping", "Target conclusion"],
                "validity_criteria": ["Relevant similarities", "Significant differences", "Analogy strength"],
                "strength_indicators": ["like", "similar to", "analogous", "just as"]
            }
        }
    
    def _initialize_evidence_patterns(self):
        """Initialize patterns for identifying evidence types"""
        self.evidence_patterns = {
            EvidenceType.STATISTICAL: {
                "keywords": ["study shows", "research indicates", "data suggests", "statistics", "survey"],
                "pattern": r"(?:\d+%|\d+\.\d+|statistics?|study|research|survey)",
                "quality_indicators": ["peer-reviewed", "large sample", "controlled"]
            },
            EvidenceType.EXPERT_TESTIMONY: {
                "keywords": ["expert", "professor", "doctor", "scientist", "authority"],
                "pattern": r"(?:expert|professor|dr\.|scientist|authority).{0,50}(?:says|states|claims)",
                "quality_indicators": ["recognized", "leading", "published"]
            },
            EvidenceType.EMPIRICAL: {
                "keywords": ["observed", "measured", "tested", "experiment", "trial"],
                "pattern": r"(?:observed|measured|tested|experiment|trial|empirical)",
                "quality_indicators": ["controlled", "replicated", "verified"]
            },
            EvidenceType.ANECDOTAL: {
                "keywords": ["I know someone", "personal experience", "story", "example"],
                "pattern": r"(?:I know|personal|story|example|anecdote)",
                "quality_indicators": ["representative", "multiple cases", "documented"]
            }
        }
    
    async def analyze(self, context: StructuredArgumentationContext) -> StructuredArgumentationResult:
        """
        Perform comprehensive structured argumentation analysis
        
        Args:
            context: Argumentation context with text and analysis parameters
            
        Returns:
            StructuredArgumentationResult with complete analysis
        """
        start_time = time.time()
        
        # Phase 1: Parse argument structure
        argument_structure = await self._parse_argument_structure(
            context.argument_text, context.argument_type
        )
        
        # Phase 2: Analyze argument quality
        argument_analysis = await self._analyze_argument_quality(
            argument_structure, context.include_fallacy_detection, 
            context.include_evidence_evaluation
        )
        
        # Phase 3: Generate counterarguments if requested
        counterargument_analysis = None
        if context.include_counterargument_analysis:
            counterargument_analysis = await self._analyze_counterarguments(
                argument_structure, context.max_counterarguments
            )
        
        # Phase 4: Detect debate structure if multiple positions
        debate_structure = await self._analyze_debate_structure(
            context.argument_text, argument_structure
        )
        
        # Phase 5: Calculate quality scores
        logic_quality_scores = await self._calculate_logic_quality_scores(
            argument_analysis, counterargument_analysis
        )
        
        # Phase 6: Generate improvement roadmap
        improvement_roadmap = await self._generate_improvement_roadmap(
            argument_analysis, counterargument_analysis
        )
        
        # Phase 7: Generate reports and assessments
        logical_consistency_report = await self._generate_consistency_report(
            argument_structure, argument_analysis
        )
        
        evidence_assessment = await self._assess_evidence_quality(
            argument_structure.supporting_evidence
        )
        
        recommended_strengthening = await self._recommend_strengthening(
            argument_analysis, counterargument_analysis
        )
        
        fallacy_summary = await self._summarize_fallacies(
            argument_analysis.detected_fallacies
        )
        
        processing_time = int((time.time() - start_time) * 1000)
        
        processing_metrics = {
            'premises_analyzed': sum(len(chain.premises) for chain in argument_structure.logic_chains),
            'logic_chains_evaluated': len(argument_structure.logic_chains),
            'evidence_pieces_assessed': len(argument_structure.supporting_evidence),
            'fallacies_detected': len(argument_analysis.detected_fallacies),
            'processing_phases': 7
        }
        
        return StructuredArgumentationResult(
            argument_structure=argument_structure,
            argument_analysis=argument_analysis,
            counterargument_analysis=counterargument_analysis,
            debate_structure=debate_structure,
            logic_quality_scores=logic_quality_scores,
            improvement_roadmap=improvement_roadmap,
            logical_consistency_report=logical_consistency_report,
            evidence_assessment=evidence_assessment,
            recommended_strengthening=recommended_strengthening,
            fallacy_summary=fallacy_summary,
            processing_metrics=processing_metrics,
            processing_time_ms=processing_time
        )
    
    async def _parse_argument_structure(
        self, 
        argument_text: str, 
        expected_type: ArgumentType
    ) -> ArgumentStructure:
        """Parse the argument text into structured components"""
        
        # Split text into sentences
        sentences = self._split_into_sentences(argument_text)
        
        # Identify main claim (usually first or last sentence)
        main_claim = await self._identify_main_claim(sentences)
        
        # Extract premises
        premises = await self._extract_premises(sentences, main_claim)
        
        # Extract evidence
        evidence = await self._extract_evidence(argument_text)
        
        # Build logic chain
        logic_chain = await self._build_logic_chain(premises, main_claim, expected_type)
        
        # Identify assumptions
        assumptions = await self._identify_assumptions(argument_text, premises)
        
        # Determine argument strength
        argument_strength = await self._assess_argument_strength(logic_chain, evidence)
        
        return ArgumentStructure(
            claim=main_claim,
            logic_chains=[logic_chain],
            supporting_evidence=evidence,
            counterarguments=[],  # Will be filled later if requested
            rebuttals=[],
            assumptions=assumptions,
            context="",
            argument_strength=argument_strength,
            confidence_level=0.7  # Base confidence
        )
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        # Simple sentence splitting
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    async def _identify_main_claim(self, sentences: List[str]) -> str:
        """Identify the main claim in the argument"""
        if not sentences:
            return "No clear claim identified"
        
        # Look for claim indicators
        claim_indicators = [
            "therefore", "thus", "consequently", "in conclusion", 
            "I argue that", "I believe that", "the point is"
        ]
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(indicator in sentence_lower for indicator in claim_indicators):
                return sentence
        
        # If no clear indicators, use the first substantive sentence
        for sentence in sentences:
            if len(sentence) > 20:  # Substantive sentence
                return sentence
        
        return sentences[0] if sentences else "No claim identified"
    
    async def _extract_premises(self, sentences: List[str], main_claim: str) -> List[Premise]:
        """Extract premises from sentences"""
        premises = []
        premise_indicators = ["because", "since", "given that", "as", "due to", "for the reason that"]
        
        for i, sentence in enumerate(sentences):
            if sentence == main_claim:
                continue
            
            # Determine premise type
            sentence_lower = sentence.lower()
            premise_type = "supporting"  # Default
            
            if any(indicator in sentence_lower for indicator in premise_indicators):
                premise_type = "major" if i < len(sentences) // 2 else "minor"
            
            # Estimate certainty level based on language
            certainty = await self._estimate_certainty(sentence)
            
            premise = Premise(
                statement=sentence,
                premise_type=premise_type,
                certainty_level=certainty,
                supporting_evidence=[],
                is_implicit=False
            )
            premises.append(premise)
        
        return premises
    
    async def _estimate_certainty(self, text: str) -> float:
        """Estimate certainty level of a statement"""
        text_lower = text.lower()
        
        # High certainty indicators
        if any(word in text_lower for word in ["always", "never", "definitely", "certainly", "absolutely"]):
            return 0.9
        
        # Medium certainty indicators
        if any(word in text_lower for word in ["probably", "likely", "usually", "often"]):
            return 0.7
        
        # Low certainty indicators
        if any(word in text_lower for word in ["maybe", "perhaps", "might", "could", "possibly"]):
            return 0.4
        
        # Default moderate certainty
        return 0.6
    
    async def _extract_evidence(self, text: str) -> List[Evidence]:
        """Extract evidence from the argument text"""
        evidence_list = []
        
        for evidence_type, pattern_info in self.evidence_patterns.items():
            pattern = pattern_info["pattern"]
            matches = re.finditer(pattern, text, re.IGNORECASE)
            
            for match in matches:
                context_start = max(0, match.start() - 50)
                context_end = min(len(text), match.end() + 50)
                context = text[context_start:context_end]
                
                # Assess quality based on quality indicators
                quality_score = 0.5  # Base quality
                for indicator in pattern_info["quality_indicators"]:
                    if indicator.lower() in text.lower():
                        quality_score += 0.15
                
                quality_score = min(1.0, quality_score)
                
                evidence = Evidence(
                    description=context.strip(),
                    evidence_type=evidence_type,
                    source="argument text",
                    quality_score=quality_score,
                    relevance_score=0.8,  # Assume high relevance within argument
                    reliability_assessment=self._assess_reliability_level(quality_score),
                    supporting_premises=[],
                    contradicting_evidence=[],
                    context=context.strip(),
                    limitations=[]
                )
                evidence_list.append(evidence)
        
        return evidence_list[:10]  # Limit to prevent overcrowding
    
    def _assess_reliability_level(self, quality_score: float) -> str:
        """Assess reliability level based on quality score"""
        if quality_score >= 0.8:
            return "high"
        elif quality_score >= 0.6:
            return "moderate"
        elif quality_score >= 0.4:
            return "low"
        else:
            return "unknown"
    
    async def _build_logic_chain(
        self, 
        premises: List[Premise], 
        conclusion: str, 
        argument_type: ArgumentType
    ) -> LogicChain:
        """Build logic chain from premises to conclusion"""
        
        # Generate inference rules based on argument type
        inference_rules = self._get_inference_rules(argument_type)
        
        # Generate intermediate conclusions for complex chains
        intermediate_conclusions = []
        if len(premises) > 2:
            intermediate_conclusions = [
                f"Intermediate conclusion from premises 1-{i+1}"
                for i in range(1, min(len(premises), 4))
            ]
        
        # Assess validity
        validity = await self._assess_chain_validity(premises, conclusion, argument_type)
        
        # Assess soundness
        soundness = await self._assess_chain_soundness(premises, validity)
        
        # Identify logical gaps
        logical_gaps = await self._identify_logical_gaps(premises, conclusion, argument_type)
        
        # Determine strength rating
        strength_rating = await self._determine_chain_strength(validity, soundness, logical_gaps)
        
        return LogicChain(
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
    
    def _get_inference_rules(self, argument_type: ArgumentType) -> List[str]:
        """Get appropriate inference rules for argument type"""
        rules_map = {
            ArgumentType.DEDUCTIVE: ["Modus ponens", "Universal instantiation", "Hypothetical syllogism"],
            ArgumentType.INDUCTIVE: ["Generalization", "Statistical inference", "Pattern recognition"],
            ArgumentType.CAUSAL: ["Causal inference", "Mill's methods", "Temporal precedence"],
            ArgumentType.ANALOGICAL: ["Analogical reasoning", "Similarity mapping", "Proportional inference"],
            ArgumentType.STATISTICAL: ["Statistical inference", "Probability assessment", "Confidence intervals"],
            ArgumentType.ABDUCTIVE: ["Inference to best explanation", "Hypothesis formation", "Explanatory coherence"]
        }
        return rules_map.get(argument_type, ["Standard logical inference"])
    
    async def _assess_chain_validity(
        self, 
        premises: List[Premise], 
        conclusion: str, 
        argument_type: ArgumentType
    ) -> str:
        """Assess the logical validity of the chain"""
        if len(premises) < 1:
            return "insufficient_premises"
        
        if argument_type == ArgumentType.DEDUCTIVE:
            # For deductive arguments, check if conclusion follows necessarily
            if len(premises) >= 2:
                return "valid"
            else:
                return "insufficient_premises"
        elif argument_type == ArgumentType.INDUCTIVE:
            # For inductive arguments, assess strength
            return "strong" if len(premises) >= 3 else "weak"
        else:
            return "plausible"
    
    async def _assess_chain_soundness(self, premises: List[Premise], validity: str) -> str:
        """Assess the soundness of the logic chain"""
        if validity not in ["valid", "strong"]:
            return "unsound"
        
        # Check premise truth levels
        high_certainty_premises = sum(1 for p in premises if p.certainty_level > 0.7)
        
        if high_certainty_premises == len(premises):
            return "sound"
        elif high_certainty_premises > len(premises) / 2:
            return "partially_sound"
        else:
            return "unsound"
    
    async def _identify_logical_gaps(
        self, 
        premises: List[Premise], 
        conclusion: str, 
        argument_type: ArgumentType
    ) -> List[str]:
        """Identify gaps in logical reasoning"""
        gaps = []
        
        # Check for insufficient premises
        if len(premises) < 2 and argument_type == ArgumentType.DEDUCTIVE:
            gaps.append("Insufficient premises for deductive argument")
        
        # Check for low-certainty premises
        weak_premises = [p for p in premises if p.certainty_level < 0.5]
        if weak_premises:
            gaps.append(f"{len(weak_premises)} premises have low certainty levels")
        
        # Check for implicit assumptions
        implicit_premises = [p for p in premises if p.is_implicit]
        if implicit_premises:
            gaps.append("Contains unstated assumptions")
        
        # Check for missing connecting logic
        if argument_type == ArgumentType.CAUSAL and len(premises) < 3:
            gaps.append("Causal argument may lack mechanism explanation")
        
        return gaps
    
    async def _determine_chain_strength(
        self, 
        validity: str, 
        soundness: str, 
        gaps: List[str]
    ) -> StrengthLevel:
        """Determine overall strength of the logic chain"""
        gap_count = len(gaps)
        
        if validity == "valid" and soundness == "sound" and gap_count == 0:
            return StrengthLevel.VERY_STRONG
        elif validity in ["valid", "strong"] and soundness in ["sound", "partially_sound"] and gap_count <= 1:
            return StrengthLevel.STRONG
        elif validity in ["valid", "strong", "plausible"] and gap_count <= 2:
            return StrengthLevel.MODERATE
        elif gap_count <= 3:
            return StrengthLevel.WEAK
        else:
            return StrengthLevel.VERY_WEAK
    
    async def _identify_assumptions(self, text: str, premises: List[Premise]) -> List[str]:
        """Identify underlying assumptions in the argument"""
        assumptions = []
        text_lower = text.lower()
        
        # Common assumption indicators
        assumption_patterns = [
            "of course", "obviously", "naturally", "clearly", "it goes without saying",
            "everyone knows", "it's common knowledge", "by definition"
        ]
        
        for pattern in assumption_patterns:
            if pattern in text_lower:
                # Extract context around the pattern
                index = text_lower.find(pattern)
                context_start = max(0, index - 30)
                context_end = min(len(text), index + len(pattern) + 30)
                context = text[context_start:context_end].strip()
                assumptions.append(f"Assumption: {context}")
        
        return assumptions[:5]  # Limit assumptions
    
    async def _assess_argument_strength(self, logic_chain: LogicChain, evidence: List[Evidence]) -> StrengthLevel:
        """Assess overall argument strength"""
        chain_strength = logic_chain.strength_rating
        
        # Adjust based on evidence quality
        if evidence:
            avg_evidence_quality = sum(e.quality_score for e in evidence) / len(evidence)
            if avg_evidence_quality > 0.8:
                # Upgrade strength if evidence is very strong
                strength_levels = list(StrengthLevel)
                current_index = strength_levels.index(chain_strength)
                if current_index > 0:
                    return strength_levels[current_index - 1]  # Upgrade
        
        return chain_strength
    
    async def _analyze_argument_quality(
        self, 
        argument: ArgumentStructure, 
        detect_fallacies: bool, 
        evaluate_evidence: bool
    ) -> ArgumentAnalysis:
        """Analyze the quality of the argument structure"""
        
        # Calculate validity score
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
        evidence_quality = 0.5
        if evaluate_evidence and argument.supporting_evidence:
            evidence_quality = sum(e.quality_score for e in argument.supporting_evidence) / len(argument.supporting_evidence)
        
        # Calculate logical consistency
        total_gaps = sum(len(chain.logical_gaps) for chain in argument.logic_chains)
        logical_consistency = max(0.0, 1.0 - (total_gaps * 0.1))
        
        # Calculate persuasiveness
        persuasiveness_score = (validity_score * 0.3 + soundness_score * 0.3 + 
                              evidence_quality * 0.2 + logical_consistency * 0.2)
        
        # Detect fallacies
        detected_fallacies = []
        if detect_fallacies:
            argument_text = f"{argument.claim} {' '.join(argument.assumptions)}"
            detected_fallacies = await self._detect_fallacies(argument_text)
        
        # Identify strengths and weaknesses
        strengths, weaknesses = await self._identify_strengths_weaknesses(
            validity_score, soundness_score, evidence_quality, logical_consistency, detected_fallacies
        )
        
        # Generate improvement suggestions
        improvement_suggestions = await self._generate_improvement_suggestions(
            validity_score, soundness_score, evidence_quality, logical_consistency, detected_fallacies
        )
        
        # Determine overall quality
        overall_score = (validity_score + soundness_score + evidence_quality + logical_consistency) / 4
        overall_quality = await self._score_to_strength_level(overall_score)
        
        return ArgumentAnalysis(
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
    
    async def _detect_fallacies(self, text: str) -> List[FallacyDetection]:
        """Detect logical fallacies in the argument text"""
        detections = []
        text_lower = text.lower()
        
        for fallacy_type, pattern_info in self.fallacy_patterns.items():
            # Check keywords
            for keyword in pattern_info["keywords"]:
                if keyword in text_lower:
                    detection = FallacyDetection(
                        fallacy_type=fallacy_type,
                        location=f"Near keyword: '{keyword}'",
                        description=f"Potential {fallacy_type.value.replace('_', ' ')} fallacy detected",
                        severity=StrengthLevel.HIGH if pattern_info["severity"] == "high" else StrengthLevel.MEDIUM,
                        correction_suggestion=self._get_fallacy_correction(fallacy_type),
                        impact_on_argument="May weaken logical validity",
                        confidence=0.7
                    )
                    detections.append(detection)
                    break  # Only detect once per fallacy type
            
            # Check regex pattern
            if "pattern" in pattern_info:
                matches = re.finditer(pattern_info["pattern"], text, re.IGNORECASE)
                for match in matches:
                    if not any(d.fallacy_type == fallacy_type for d in detections):
                        detection = FallacyDetection(
                            fallacy_type=fallacy_type,
                            location=f"Text pattern match: '{match.group()}'",
                            description=f"Pattern-based {fallacy_type.value.replace('_', ' ')} fallacy detected",
                            severity=StrengthLevel.HIGH if pattern_info["severity"] == "high" else StrengthLevel.MEDIUM,
                            correction_suggestion=self._get_fallacy_correction(fallacy_type),
                            impact_on_argument="May weaken logical validity",
                            confidence=0.6
                        )
                        detections.append(detection)
                        break
        
        return detections
    
    def _get_fallacy_correction(self, fallacy_type: LogicalFallacy) -> str:
        """Get correction suggestion for a specific fallacy"""
        corrections = {
            LogicalFallacy.AD_HOMINEM: "Focus on the argument itself, not the person making it",
            LogicalFallacy.STRAW_MAN: "Represent the opponent's position accurately and completely",
            LogicalFallacy.FALSE_DICHOTOMY: "Consider additional alternatives beyond the two presented",
            LogicalFallacy.SLIPPERY_SLOPE: "Provide evidence for each step in the claimed chain of events",
            LogicalFallacy.CIRCULAR_REASONING: "Provide independent evidence for the conclusion",
            LogicalFallacy.APPEAL_TO_AUTHORITY: "Evaluate the authority's expertise and the strength of their argument",
            LogicalFallacy.APPEAL_TO_EMOTION: "Support emotional appeals with logical reasoning and evidence",
            LogicalFallacy.HASTY_GENERALIZATION: "Ensure sufficient and representative examples before generalizing"
        }
        return corrections.get(fallacy_type, "Review the logical structure for validity")
    
    async def _identify_strengths_weaknesses(
        self, 
        validity_score: float, 
        soundness_score: float, 
        evidence_quality: float, 
        logical_consistency: float, 
        fallacies: List[FallacyDetection]
    ) -> Tuple[List[str], List[str]]:
        """Identify argument strengths and weaknesses"""
        strengths = []
        weaknesses = []
        
        # Validity assessment
        if validity_score > 0.8:
            strengths.append("Strong logical validity - conclusions follow well from premises")
        elif validity_score < 0.5:
            weaknesses.append("Weak logical structure - conclusions don't clearly follow from premises")
        
        # Soundness assessment
        if soundness_score > 0.8:
            strengths.append("Sound argument - valid structure with likely true premises")
        elif soundness_score < 0.5:
            weaknesses.append("Unsound argument - either invalid structure or questionable premises")
        
        # Evidence assessment
        if evidence_quality > 0.8:
            strengths.append("High-quality supporting evidence from reliable sources")
        elif evidence_quality < 0.5:
            weaknesses.append("Poor quality or insufficient supporting evidence")
        
        # Consistency assessment
        if logical_consistency > 0.8:
            strengths.append("Logically consistent with minimal gaps or contradictions")
        elif logical_consistency < 0.5:
            weaknesses.append("Contains logical gaps or inconsistencies")
        
        # Fallacy assessment
        if not fallacies:
            strengths.append("No obvious logical fallacies detected")
        else:
            high_severity_fallacies = [f for f in fallacies if f.severity == StrengthLevel.HIGH]
            if high_severity_fallacies:
                weaknesses.append(f"Contains {len(high_severity_fallacies)} high-severity logical fallacies")
            else:
                weaknesses.append(f"Contains {len(fallacies)} potential logical fallacies")
        
        return strengths, weaknesses
    
    async def _generate_improvement_suggestions(
        self, 
        validity_score: float, 
        soundness_score: float, 
        evidence_quality: float, 
        logical_consistency: float, 
        fallacies: List[FallacyDetection]
    ) -> List[str]:
        """Generate suggestions for improving the argument"""
        suggestions = []
        
        if validity_score < 0.7:
            suggestions.append("Strengthen logical connections between premises and conclusions")
            suggestions.append("Ensure conclusions follow necessarily or probably from premises")
        
        if soundness_score < 0.7:
            suggestions.append("Verify the truth of premises with additional evidence")
            suggestions.append("Consider alternative explanations for the premises")
        
        if evidence_quality < 0.7:
            suggestions.append("Add higher-quality evidence from reliable sources")
            suggestions.append("Include multiple types of evidence (statistical, expert, empirical)")
        
        if logical_consistency < 0.7:
            suggestions.append("Address identified logical gaps and inconsistencies")
            suggestions.append("Make implicit assumptions explicit")
        
        if fallacies:
            suggestions.append("Remove or correct identified logical fallacies")
            suggestions.append("Restructure arguments to avoid fallacious reasoning")
        
        # General suggestions
        suggestions.extend([
            "Consider potential counterarguments and address them",
            "Provide more specific examples to support general claims",
            "Clarify the scope and limitations of the argument"
        ])
        
        return suggestions[:15]  # Limit suggestions
    
    async def _score_to_strength_level(self, score: float) -> StrengthLevel:
        """Convert numeric score to strength level"""
        if score >= 0.8:
            return StrengthLevel.VERY_STRONG
        elif score >= 0.6:
            return StrengthLevel.STRONG
        elif score >= 0.4:
            return StrengthLevel.MODERATE
        elif score >= 0.2:
            return StrengthLevel.WEAK
        else:
            return StrengthLevel.VERY_WEAK
    
    async def _analyze_counterarguments(
        self, 
        argument: ArgumentStructure, 
        max_counterarguments: int
    ) -> CounterargumentAnalysis:
        """Generate and analyze potential counterarguments"""
        counterarguments = []
        
        # Challenge premises
        for chain in argument.logic_chains:
            for premise in chain.premises:
                if premise.certainty_level < 0.8:
                    counterarguments.append(f"Challenge the validity of: '{premise.statement[:100]}...'")
        
        # Challenge evidence
        for evidence in argument.supporting_evidence:
            if evidence.quality_score < 0.7:
                counterarguments.append(f"Question the reliability of evidence: '{evidence.description[:100]}...'")
        
        # Challenge logical connections
        for chain in argument.logic_chains:
            if chain.logical_gaps:
                counterarguments.append(f"Identify logical gap: {chain.logical_gaps[0]}")
        
        # General counterargument strategies
        counterarguments.extend([
            "Propose alternative explanations for the same evidence",
            "Question the representativeness of examples used",
            "Challenge unstated assumptions underlying the argument",
            "Present contradictory evidence or examples",
            "Question the relevance of evidence to the conclusion"
        ])
        
        # Limit to requested maximum
        counterarguments = counterarguments[:max_counterarguments]
        
        # Assess counterargument strength
        counterargument_strength = {}
        for counter in counterarguments:
            if "challenge" in counter.lower() and "premise" in counter.lower():
                counterargument_strength[counter] = StrengthLevel.STRONG.value
            elif "evidence" in counter.lower():
                counterargument_strength[counter] = StrengthLevel.MODERATE.value
            else:
                counterargument_strength[counter] = StrengthLevel.WEAK.value
        
        # Generate potential rebuttals
        potential_rebuttals = {}
        for counter in counterarguments:
            potential_rebuttals[counter] = [
                "Provide additional supporting evidence",
                "Clarify the logical connection",
                "Address the specific concern raised",
                "Acknowledge limitations while maintaining core argument"
            ]
        
        # Calculate vulnerability
        strong_counters = [c for c, s in counterargument_strength.items() if s == StrengthLevel.STRONG.value]
        vulnerability = len(strong_counters) / max(1, len(counterarguments))
        
        return CounterargumentAnalysis(
            original_argument=argument.claim,
            counterarguments=counterarguments,
            counterargument_strength=counterargument_strength,
            potential_rebuttals=potential_rebuttals,
            argument_vulnerability=vulnerability,
            defensive_strategies=[
                "Strengthen weak premises with additional evidence",
                "Address potential counterarguments proactively",
                "Acknowledge limitations while maintaining core argument",
                "Provide multiple lines of evidence for key claims"
            ],
            strengthening_recommendations=[
                "Add more diverse evidence sources",
                "Make implicit assumptions explicit",
                "Consider and address alternative explanations",
                "Strengthen logical connections between premises and conclusion"
            ]
        )
    
    async def _analyze_debate_structure(
        self, 
        text: str, 
        argument: ArgumentStructure
    ) -> Optional[DebateStructure]:
        """Analyze if the text contains debate structure with multiple positions"""
        # Simple heuristic: look for opposing viewpoints
        opposing_indicators = [
            "however", "but", "on the other hand", "conversely", "nevertheless",
            "critics argue", "opponents claim", "some believe", "others contend"
        ]
        
        text_lower = text.lower()
        opposition_count = sum(1 for indicator in opposing_indicators if indicator in text_lower)
        
        if opposition_count < 2:
            return None  # Not enough evidence of debate structure
        
        # If debate structure detected, create basic analysis
        return DebateStructure(
            topic=argument.claim[:200],  # Use main claim as topic
            positions=["Primary argument", "Counter-position"],
            arguments_by_position={
                "Primary argument": [argument.claim],
                "Counter-position": argument.counterarguments
            },
            cross_references={},
            consensus_points=[],
            contentious_points=argument.counterarguments,
            resolution_pathways=[
                "Address counterarguments systematically",
                "Find common ground where possible",
                "Strengthen evidence for disputed claims"
            ],
            quality_assessment={
                "Primary argument": 0.7,  # Base assessment
                "Counter-position": 0.5
            }
        )
    
    async def _calculate_logic_quality_scores(
        self, 
        analysis: ArgumentAnalysis, 
        counter_analysis: Optional[CounterargumentAnalysis]
    ) -> Dict[str, float]:
        """Calculate quality scores for different logic aspects"""
        scores = {
            'validity': analysis.validity_score,
            'soundness': analysis.soundness_score,
            'persuasiveness': analysis.persuasiveness_score,
            'consistency': analysis.logical_consistency,
            'evidence_quality': analysis.evidence_quality,
            'overall': (analysis.validity_score + analysis.soundness_score + 
                       analysis.logical_consistency + analysis.evidence_quality) / 4
        }
        
        # Add vulnerability score if counterargument analysis available
        if counter_analysis:
            scores['resilience'] = 1.0 - counter_analysis.argument_vulnerability
        
        return scores
    
    async def _generate_improvement_roadmap(
        self, 
        analysis: ArgumentAnalysis, 
        counter_analysis: Optional[CounterargumentAnalysis]
    ) -> List[str]:
        """Generate step-by-step improvement roadmap"""
        roadmap = []
        
        # Phase 1: Fix critical issues
        if analysis.detected_fallacies:
            high_severity = [f for f in analysis.detected_fallacies if f.severity == StrengthLevel.HIGH]
            if high_severity:
                roadmap.append("Phase 1: Remove high-severity logical fallacies")
                for fallacy in high_severity[:3]:  # Limit to top 3
                    roadmap.append(f"  - Fix {fallacy.fallacy_type.value.replace('_', ' ')}: {fallacy.correction_suggestion}")
        
        # Phase 2: Strengthen structure
        if analysis.validity_score < 0.7:
            roadmap.append("Phase 2: Strengthen logical structure")
            roadmap.append("  - Clarify connections between premises and conclusions")
            roadmap.append("  - Ensure logical flow from premises to conclusion")
        
        # Phase 3: Improve evidence
        if analysis.evidence_quality < 0.7:
            roadmap.append("Phase 3: Enhance evidence quality")
            roadmap.append("  - Add high-quality sources and citations")
            roadmap.append("  - Include multiple types of evidence")
            roadmap.append("  - Verify evidence reliability and relevance")
        
        # Phase 4: Address counterarguments
        if counter_analysis and counter_analysis.argument_vulnerability > 0.5:
            roadmap.append("Phase 4: Address argument vulnerabilities")
            roadmap.append("  - Proactively address strongest counterarguments")
            roadmap.append("  - Provide rebuttals for main objections")
        
        # Phase 5: Polish and refine
        roadmap.extend([
            "Phase 5: Final refinement",
            "  - Review overall coherence and flow",
            "  - Ensure clarity of expression",
            "  - Verify all claims are properly supported"
        ])
        
        return roadmap
    
    async def _generate_consistency_report(
        self, 
        argument: ArgumentStructure, 
        analysis: ArgumentAnalysis
    ) -> List[str]:
        """Generate report on logical consistency issues"""
        report = []
        
        # Check for contradictions
        premises_text = " ".join([p.statement for chain in argument.logic_chains for p in chain.premises])
        contradiction_indicators = ["not", "never", "opposite", "contrary", "but", "however"]
        
        for indicator in contradiction_indicators:
            if indicator in premises_text.lower():
                report.append(f"Potential contradiction detected near '{indicator}'")
        
        # Check logical gaps from chains
        for chain in argument.logic_chains:
            if chain.logical_gaps:
                report.extend([f"Logical gap: {gap}" for gap in chain.logical_gaps])
        
        # Check assumption consistency
        if len(argument.assumptions) > 3:
            report.append("Large number of assumptions may indicate complexity or gaps in reasoning")
        
        if not report:
            report.append("No major logical consistency issues detected")
        
        return report
    
    async def _assess_evidence_quality(self, evidence: List[Evidence]) -> List[str]:
        """Assess the quality of evidence provided"""
        if not evidence:
            return ["No evidence provided to assess"]
        
        assessment = []
        
        # Overall quality assessment
        avg_quality = sum(e.quality_score for e in evidence) / len(evidence)
        avg_relevance = sum(e.relevance_score for e in evidence) / len(evidence)
        
        assessment.append(f"Average evidence quality: {avg_quality:.2f}/1.0")
        assessment.append(f"Average evidence relevance: {avg_relevance:.2f}/1.0")
        
        # Evidence type diversity
        evidence_types = set(e.evidence_type for e in evidence)
        assessment.append(f"Evidence type diversity: {len(evidence_types)} different types")
        
        # Quality distribution
        high_quality = [e for e in evidence if e.quality_score > 0.7]
        low_quality = [e for e in evidence if e.quality_score < 0.4]
        
        if high_quality:
            assessment.append(f"{len(high_quality)} pieces of high-quality evidence")
        if low_quality:
            assessment.append(f"{len(low_quality)} pieces of low-quality evidence need improvement")
        
        # Reliability assessment
        reliability_counts = {}
        for e in evidence:
            reliability_counts[e.reliability_assessment] = reliability_counts.get(e.reliability_assessment, 0) + 1
        
        for reliability, count in reliability_counts.items():
            assessment.append(f"{count} pieces of {reliability} reliability evidence")
        
        return assessment
    
    async def _recommend_strengthening(
        self, 
        analysis: ArgumentAnalysis, 
        counter_analysis: Optional[CounterargumentAnalysis]
    ) -> List[str]:
        """Recommend specific strengthening strategies"""
        recommendations = []
        
        # Based on analysis weaknesses
        if analysis.validity_score < 0.6:
            recommendations.extend([
                "Add intermediate steps to clarify logical progression",
                "Use formal logical structures (if-then, cause-effect)",
                "Ensure each conclusion follows clearly from its premises"
            ])
        
        if analysis.evidence_quality < 0.6:
            recommendations.extend([
                "Seek peer-reviewed sources for key claims",
                "Include quantitative data where appropriate",
                "Cite recognized experts in the relevant field"
            ])
        
        if analysis.detected_fallacies:
            recommendations.extend([
                "Remove ad hominem attacks and focus on arguments",
                "Avoid overgeneralization and hasty conclusions",
                "Present opponent positions fairly and completely"
            ])
        
        # Based on counterargument vulnerability
        if counter_analysis and counter_analysis.argument_vulnerability > 0.4:
            recommendations.extend([
                "Acknowledge and address the strongest counterarguments",
                "Provide multiple independent lines of evidence",
                "Consider and discuss alternative explanations"
            ])
        
        # General strengthening
        recommendations.extend([
            "Use specific, concrete examples to illustrate abstract points",
            "Define key terms clearly to avoid ambiguity",
            "Structure the argument with clear introduction, body, and conclusion"
        ])
        
        return recommendations[:12]  # Limit recommendations
    
    async def _summarize_fallacies(self, fallacies: List[FallacyDetection]) -> Dict[str, int]:
        """Summarize detected fallacies by type"""
        if not fallacies:
            return {"none_detected": 1}
        
        summary = {}
        for fallacy in fallacies:
            fallacy_name = fallacy.fallacy_type.value
            summary[fallacy_name] = summary.get(fallacy_name, 0) + 1
        
        return summary