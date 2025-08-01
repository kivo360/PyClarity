"""
Scientific Method Analyzer

Core implementation of the scientific method cognitive tool, providing
hypothesis-driven reasoning through hypothesis formation and testing,
experimental design principles, evidence evaluation and analysis,
theory building and validation, and systematic inquiry processes.
"""

from typing import List, Dict, Any, Optional, Tuple
import asyncio
import time
from datetime import datetime

from .models import (
    ScientificMethodContext,
    ScientificMethodResult,
    Hypothesis,
    Evidence,
    Experiment,
    HypothesisTest,
    TheoryConstruction,
    HypothesisType,
    EvidenceType,
    EvidenceQuality,
    TestResult,
)


class ScientificMethodAnalyzer:
    """Scientific method cognitive tool analyzer"""
    
    def __init__(self):
        """Initialize the scientific method analyzer"""
        self.tool_name = "Scientific Method"
        self.version = "1.0.0"
        
        # Internal state for processing
        self._processing_start_time = 0.0
    
    async def analyze(self, context: ScientificMethodContext) -> ScientificMethodResult:
        """
        Analyze a problem using the scientific method.
        
        Args:
            context: Scientific method context with research question and parameters
            
        Returns:
            ScientificMethodResult with hypotheses, evidence, tests, and conclusions
        """
        self._processing_start_time = time.time()
        
        # Phase 1: Generate hypotheses
        hypotheses = []
        if context.hypothesis_generation_enabled:
            hypotheses = await self._generate_hypotheses(context)
        
        # Phase 2: Collect and evaluate evidence
        evidence_collected = []
        if context.evidence_evaluation_enabled:
            evidence_collected = await self._collect_evidence(context, hypotheses)
        
        # Phase 3: Design experiments
        experiments = []
        if context.experiment_design_enabled:
            experiments = await self._design_experiments(context, hypotheses)
        
        # Phase 4: Test hypotheses
        hypothesis_tests = await self._test_hypotheses(
            hypotheses, evidence_collected, context
        )
        
        # Phase 5: Construct theory if enabled
        theory = None
        if context.theory_construction_enabled:
            theory = await self._construct_theory(
                hypotheses, hypothesis_tests, evidence_collected, context
            )
        
        # Phase 6: Evaluate scientific rigor and generate conclusions
        (
            rigor_score,
            methodology_quality,
            evidence_strength,
            conclusions,
            research_areas,
            recommendations
        ) = await self._evaluate_scientific_process(
            context,
            hypotheses,
            evidence_collected,
            experiments,
            hypothesis_tests,
            theory
        )
        
        # Calculate processing time
        processing_time = time.time() - self._processing_start_time
        
        return ScientificMethodResult(
            hypotheses_generated=hypotheses,
            evidence_collected=evidence_collected,
            experiments_designed=experiments,
            hypothesis_tests=hypothesis_tests,
            theory_construction=theory,
            scientific_rigor_score=rigor_score,
            methodology_quality=methodology_quality,
            evidence_strength=evidence_strength,
            conclusions_supported=conclusions,
            areas_needing_research=research_areas,
            methodological_recommendations=recommendations,
            investigation_duration_minutes=processing_time / 60.0,
            hypotheses_tested=len(hypothesis_tests),
            experiments_feasible=len([e for e in experiments if e.feasibility_score > 0.7]),
            scientific_confidence=self._calculate_scientific_confidence(
                hypothesis_tests, evidence_strength
            ),
            processing_time_ms=round(processing_time * 1000)
        )
    
    async def _generate_hypotheses(
        self, context: ScientificMethodContext
    ) -> List[Hypothesis]:
        """Generate testable hypotheses for the research question"""
        # Simulate processing delay
        await asyncio.sleep(0.1)
        
        hypotheses = []
        
        # Generate different types of hypotheses
        hypothesis_types = [
            HypothesisType.EXPLANATORY,
            HypothesisType.PREDICTIVE,
            HypothesisType.CAUSAL,
            HypothesisType.CORRELATIONAL
        ]
        
        for i, hyp_type in enumerate(hypothesis_types[:context.max_hypotheses]):
            hypothesis = await self._create_hypothesis(
                context.research_question,
                hyp_type,
                context.domain_knowledge
            )
            hypotheses.append(hypothesis)
        
        # Add null hypothesis for statistical testing
        if len(hypotheses) > 0:
            null_hypothesis = await self._create_null_hypothesis(
                hypotheses[0], context
            )
            hypotheses.append(null_hypothesis)
        
        return hypotheses
    
    async def _create_hypothesis(
        self,
        research_question: str,
        hypothesis_type: HypothesisType,
        domain_knowledge: str
    ) -> Hypothesis:
        """Create a specific hypothesis"""
        
        # Generate hypothesis based on type
        if hypothesis_type == HypothesisType.EXPLANATORY:
            statement = f"The observed phenomenon in '{research_question}' is explained by underlying causal mechanisms"
            variables = ["phenomenon", "causal_mechanism", "context_factors"]
            predictions = ["Mechanism should be observable", "Effect should vary with mechanism strength"]
        
        elif hypothesis_type == HypothesisType.PREDICTIVE:
            statement = f"Based on current understanding, '{research_question}' will result in specific measurable outcomes"
            variables = ["current_state", "intervention", "predicted_outcome"]
            predictions = ["Outcome will match prediction", "Relationship will be consistent"]
        
        elif hypothesis_type == HypothesisType.CAUSAL:
            statement = f"There is a direct causal relationship between key factors in '{research_question}'"
            variables = ["cause_variable", "effect_variable", "confounding_variables"]
            predictions = ["Manipulation of cause changes effect", "Temporal precedence observable"]
        
        else:  # CORRELATIONAL
            statement = f"Variables in '{research_question}' show systematic relationships"
            variables = ["variable_a", "variable_b", "relationship_strength"]
            predictions = ["Correlation will be significant", "Relationship will be consistent"]
        
        # Calculate testability and falsifiability
        testability = 0.8 if "measurable" in statement.lower() else 0.6
        falsifiability = 0.9 if "specific" in statement.lower() else 0.7
        
        return Hypothesis(
            statement=statement,
            hypothesis_type=hypothesis_type,
            variables=variables,
            assumptions=["Domain knowledge is accurate", "Measurement is reliable"],
            predictions=predictions,
            testability=testability,
            falsifiability=falsifiability,
            theoretical_foundation=domain_knowledge,
            related_hypotheses=[]
        )
    
    async def _create_null_hypothesis(
        self,
        alternative_hypothesis: Hypothesis,
        context: ScientificMethodContext
    ) -> Hypothesis:
        """Create null hypothesis for statistical testing"""
        
        return Hypothesis(
            statement=f"There is no significant relationship or effect in '{context.research_question}'",
            hypothesis_type=HypothesisType.NULL_HYPOTHESIS,
            variables=alternative_hypothesis.variables,
            assumptions=["No systematic bias", "Random variation only"],
            predictions=["No significant differences", "Results explained by chance"],
            testability=0.9,
            falsifiability=0.9,
            theoretical_foundation="Statistical null hypothesis principle",
            related_hypotheses=[alternative_hypothesis.hypothesis_id]
        )
    
    async def _collect_evidence(
        self,
        context: ScientificMethodContext,
        hypotheses: List[Hypothesis]
    ) -> List[Evidence]:
        """Collect and evaluate evidence for hypotheses"""
        # Simulate processing delay
        await asyncio.sleep(0.1)
        
        evidence_pieces = []
        
        # Generate different types of evidence
        evidence_types = [
            EvidenceType.OBSERVATIONAL,
            EvidenceType.EXPERIMENTAL,
            EvidenceType.STATISTICAL,
            EvidenceType.LITERATURE_REVIEW
        ]
        
        for evidence_type in evidence_types:
            for i, hypothesis in enumerate(hypotheses[:3]):  # Limit evidence per hypothesis
                evidence = await self._create_evidence(
                    hypothesis, evidence_type, context
                )
                evidence_pieces.append(evidence)
        
        # Add evidence from specified sources
        for source in context.evidence_sources:
            source_evidence = Evidence(
                description=f"Evidence from {source} regarding the research question",
                evidence_type=EvidenceType.ARCHIVAL_DATA,
                quality=EvidenceQuality.MEDIUM,
                source=source,
                relevance_score=0.7,
                reliability_score=0.8,
                supporting_strength=0.5,  # Neutral initially
                confidence_level=0.7,
                limitations=["Source-specific limitations", "Potential bias"]
            )
            evidence_pieces.append(source_evidence)
        
        return evidence_pieces
    
    async def _create_evidence(
        self,
        hypothesis: Hypothesis,
        evidence_type: EvidenceType,
        context: ScientificMethodContext
    ) -> Evidence:
        """Create evidence for a specific hypothesis"""
        
        # Simulate evidence quality and strength based on type
        if evidence_type == EvidenceType.EXPERIMENTAL:
            quality = EvidenceQuality.HIGH
            reliability = 0.9
            supporting_strength = 0.7
            confidence = 0.8
            limitations = ["Controlled conditions", "Limited generalizability"]
        
        elif evidence_type == EvidenceType.OBSERVATIONAL:
            quality = EvidenceQuality.MEDIUM
            reliability = 0.7
            supporting_strength = 0.5
            confidence = 0.6
            limitations = ["Correlation not causation", "Confounding variables"]
        
        elif evidence_type == EvidenceType.STATISTICAL:
            quality = EvidenceQuality.HIGH
            reliability = 0.85
            supporting_strength = 0.6
            confidence = 0.75
            limitations = ["Sample size", "Statistical assumptions"]
        
        else:  # LITERATURE_REVIEW
            quality = EvidenceQuality.MEDIUM
            reliability = 0.75
            supporting_strength = 0.4
            confidence = 0.65
            limitations = ["Secondary source", "Publication bias"]
        
        return Evidence(
            description=f"{evidence_type.value.title()} evidence for: {hypothesis.statement[:50]}...",
            evidence_type=evidence_type,
            quality=quality,
            source=f"{evidence_type.value}_source",
            relevance_score=0.8,
            reliability_score=reliability,
            supporting_strength=supporting_strength,
            confidence_level=confidence,
            methodology_notes=f"Standard {evidence_type.value} methodology",
            limitations=limitations
        )
    
    async def _design_experiments(
        self,
        context: ScientificMethodContext,
        hypotheses: List[Hypothesis]
    ) -> List[Experiment]:
        """Design experiments to test hypotheses"""
        # Simulate processing delay
        await asyncio.sleep(0.1)
        
        experiments = []
        
        for hypothesis in hypotheses[:3]:  # Limit experiments
            if hypothesis.hypothesis_type != HypothesisType.NULL_HYPOTHESIS:
                experiment = await self._create_experiment(hypothesis, context)
                experiments.append(experiment)
        
        return experiments
    
    async def _create_experiment(
        self,
        hypothesis: Hypothesis,
        context: ScientificMethodContext
    ) -> Experiment:
        """Create experiment for testing a hypothesis"""
        
        # Determine experiment feasibility based on constraints
        feasibility = 0.8
        for constraint in context.constraints:
            if "time" in constraint.lower() or "budget" in constraint.lower():
                feasibility *= 0.8
        
        return Experiment(
            name=f"Test for {hypothesis.hypothesis_type.value} hypothesis",
            objective=f"Test the hypothesis: {hypothesis.statement}",
            hypothesis_tested=hypothesis.hypothesis_id,
            experimental_design="Controlled experimental design with treatment and control groups",
            variables_controlled=["environmental_factors", "participant_characteristics", "measurement_conditions"],
            variables_measured=hypothesis.variables,
            methodology="Systematic data collection with standardized procedures",
            expected_outcomes=hypothesis.predictions,
            success_criteria=["Statistically significant results", "Effect size > 0.3", "Reproducible findings"],
            potential_confounds=["Selection bias", "Measurement error", "External validity threats"],
            ethical_considerations=["Informed consent", "Risk assessment", "Data privacy"],
            feasibility_score=feasibility
        )
    
    async def _test_hypotheses(
        self,
        hypotheses: List[Hypothesis],
        evidence: List[Evidence],
        context: ScientificMethodContext
    ) -> List[HypothesisTest]:
        """Test hypotheses against collected evidence"""
        # Simulate processing delay
        await asyncio.sleep(0.1)
        
        hypothesis_tests = []
        
        for hypothesis in hypotheses:
            # Find relevant evidence for this hypothesis
            relevant_evidence = [
                e for e in evidence
                if any(var in e.description.lower() for var in hypothesis.variables)
            ]
            
            test_result = await self._conduct_hypothesis_test(
                hypothesis, relevant_evidence, context
            )
            hypothesis_tests.append(test_result)
        
        return hypothesis_tests
    
    async def _conduct_hypothesis_test(
        self,
        hypothesis: Hypothesis,
        evidence: List[Evidence],
        context: ScientificMethodContext
    ) -> HypothesisTest:
        """Conduct test for a single hypothesis"""
        
        if not evidence:
            return HypothesisTest(
                hypothesis_id=hypothesis.hypothesis_id,
                evidence_considered=[],
                test_result=TestResult.INCONCLUSIVE,
                confidence_level=0.1,
                supporting_evidence_count=0,
                opposing_evidence_count=0,
                evidence_quality_score=0.0,
                limitations=["Insufficient evidence"],
                recommendations=["Collect more evidence"]
            )
        
        # Analyze evidence
        supporting_evidence = [e for e in evidence if e.supporting_strength > 0.3]
        opposing_evidence = [e for e in evidence if e.supporting_strength < -0.3]
        
        # Calculate evidence quality
        quality_scores = []
        for e in evidence:
            if e.quality == EvidenceQuality.HIGH:
                quality_scores.append(0.9)
            elif e.quality == EvidenceQuality.MEDIUM:
                quality_scores.append(0.7)
            else:
                quality_scores.append(0.4)
        
        evidence_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0.5
        
        # Determine test result
        support_strength = sum(e.supporting_strength for e in supporting_evidence)
        oppose_strength = abs(sum(e.supporting_strength for e in opposing_evidence))
        
        if support_strength > oppose_strength and support_strength > 1.0:
            test_result = TestResult.SUPPORTED
            confidence = min(0.9, 0.5 + support_strength * 0.2)
        elif oppose_strength > support_strength and oppose_strength > 1.0:
            test_result = TestResult.NOT_SUPPORTED
            confidence = min(0.9, 0.5 + oppose_strength * 0.2)
        elif abs(support_strength - oppose_strength) < 0.5:
            test_result = TestResult.PARTIALLY_SUPPORTED
            confidence = 0.6
        else:
            test_result = TestResult.INCONCLUSIVE
            confidence = 0.3
        
        # Generate statistical significance (simulated)
        statistical_significance = None
        if len(evidence) >= 3 and evidence_quality > 0.6:
            statistical_significance = max(0.001, context.significance_threshold * (1 - confidence))
        
        return HypothesisTest(
            hypothesis_id=hypothesis.hypothesis_id,
            evidence_considered=[e.evidence_id for e in evidence],
            test_result=test_result,
            confidence_level=confidence,
            statistical_significance=statistical_significance,
            effect_size=support_strength * 0.3 if support_strength > 0 else None,
            supporting_evidence_count=len(supporting_evidence),
            opposing_evidence_count=len(opposing_evidence),
            evidence_quality_score=evidence_quality,
            alternative_explanations=self._generate_alternative_explanations(hypothesis),
            limitations=self._identify_test_limitations(evidence),
            recommendations=self._generate_test_recommendations(test_result, confidence)
        )
    
    async def _construct_theory(
        self,
        hypotheses: List[Hypothesis],
        hypothesis_tests: List[HypothesisTest],
        evidence: List[Evidence],
        context: ScientificMethodContext
    ) -> Optional[TheoryConstruction]:
        """Construct theory from supported hypotheses"""
        # Simulate processing delay
        await asyncio.sleep(0.1)
        
        # Find well-supported hypotheses
        supported_tests = [
            test for test in hypothesis_tests
            if test.test_result in [TestResult.SUPPORTED, TestResult.PARTIALLY_SUPPORTED]
            and test.confidence_level > 0.7
        ]
        
        if len(supported_tests) < 2:
            return None
        
        # Get corresponding hypotheses
        supported_hypotheses = [
            h for h in hypotheses
            if any(test.hypothesis_id == h.hypothesis_id for test in supported_tests)
        ]
        
        # Calculate theory metrics
        explanatory_power = sum(test.confidence_level for test in supported_tests) / len(supported_tests)
        predictive_power = min(0.9, explanatory_power * 0.9)  # Slightly lower than explanatory
        parsimony_score = max(0.3, 1.0 - (len(supported_hypotheses) * 0.1))  # Simpler is better
        
        # Generate core principles
        core_principles = [
            "Systematic relationships exist between key variables",
            "Observable patterns can be predicted and explained",
            "Evidence supports theoretical predictions"
        ]
        
        return TheoryConstruction(
            theory_name=f"Integrated Theory for {context.research_question[:30]}...",
            theory_statement=f"A comprehensive explanation integrating {len(supported_hypotheses)} validated hypotheses",
            supporting_hypotheses=[h.hypothesis_id for h in supported_hypotheses],
            core_principles=core_principles,
            explanatory_power=explanatory_power,
            predictive_power=predictive_power,
            parsimony_score=parsimony_score,
            scope=f"Applicable to problems similar to: {context.research_question}",
            testable_predictions=[
                prediction for h in supported_hypotheses for prediction in h.predictions
            ][:10],  # Limit to 10
            competing_theories=["Alternative theoretical frameworks"],
            theory_confidence=min(explanatory_power, predictive_power)
        )
    
    async def _evaluate_scientific_process(
        self,
        context: ScientificMethodContext,
        hypotheses: List[Hypothesis],
        evidence: List[Evidence],
        experiments: List[Experiment],
        hypothesis_tests: List[HypothesisTest],
        theory: Optional[TheoryConstruction]
    ) -> Tuple[float, float, float, List[str], List[str], List[str]]:
        """Evaluate the overall scientific process"""
        
        # Calculate scientific rigor
        rigor_factors = [
            len(hypotheses) / max(1, context.max_hypotheses),  # Hypothesis generation
            len(evidence) / max(1, len(hypotheses) * 2),  # Evidence collection
            len([e for e in experiments if e.feasibility_score > 0.7]) / max(1, len(experiments)),  # Experiment quality
            len([t for t in hypothesis_tests if t.confidence_level > 0.6]) / max(1, len(hypothesis_tests)),  # Test quality
            1.0 if theory else 0.5  # Theory construction
        ]
        rigor_score = sum(rigor_factors) / len(rigor_factors)
        
        # Calculate methodology quality
        methodology_factors = [
            sum(h.testability for h in hypotheses) / max(1, len(hypotheses)),  # Hypothesis testability
            sum(1 for e in evidence if e.quality == EvidenceQuality.HIGH) / max(1, len(evidence)),  # Evidence quality
            sum(e.feasibility_score for e in experiments) / max(1, len(experiments)),  # Experiment feasibility
        ]
        methodology_quality = sum(methodology_factors) / len(methodology_factors)
        
        # Calculate evidence strength
        evidence_strength = 0.0
        if evidence:
            quality_weights = {EvidenceQuality.HIGH: 1.0, EvidenceQuality.MEDIUM: 0.7, EvidenceQuality.LOW: 0.4}
            weighted_strength = sum(
                abs(e.supporting_strength) * quality_weights.get(e.quality, 0.5)
                for e in evidence
            )
            evidence_strength = min(1.0, weighted_strength / len(evidence))
        
        # Generate conclusions
        conclusions = []
        well_supported_tests = [t for t in hypothesis_tests if t.test_result == TestResult.SUPPORTED and t.confidence_level > 0.7]
        for test in well_supported_tests:
            hypothesis = next((h for h in hypotheses if h.hypothesis_id == test.hypothesis_id), None)
            if hypothesis:
                conclusions.append(f"{hypothesis.hypothesis_type.value.title()}: {hypothesis.statement}")
        
        # Identify research areas
        research_areas = []
        inconclusive_tests = [t for t in hypothesis_tests if t.test_result == TestResult.INCONCLUSIVE]
        for test in inconclusive_tests:
            research_areas.append(f"Further investigation needed for hypothesis {test.hypothesis_id}")
        
        if len(evidence) < len(hypotheses) * 2:
            research_areas.append("More comprehensive evidence collection needed")
        
        # Generate recommendations
        recommendations = [
            "Continue systematic hypothesis testing approach",
            "Strengthen evidence collection from multiple sources",
            "Design and conduct feasible experiments",
            "Apply statistical rigor to hypothesis testing"
        ]
        
        if rigor_score < 0.7:
            recommendations.append("Improve overall scientific rigor")
        if methodology_quality < 0.7:
            recommendations.append("Enhance methodological approaches")
        if evidence_strength < 0.6:
            recommendations.append("Collect higher quality evidence")
        
        return rigor_score, methodology_quality, evidence_strength, conclusions, research_areas, recommendations
    
    # Helper methods
    def _calculate_scientific_confidence(
        self, hypothesis_tests: List[HypothesisTest], evidence_strength: float
    ) -> float:
        """Calculate scientific confidence combining tests and evidence"""
        if not hypothesis_tests:
            return evidence_strength * 0.5
        
        test_confidences = [t.confidence_level for t in hypothesis_tests]
        test_confidence = sum(test_confidences) / len(test_confidences)
        return (test_confidence + evidence_strength) / 2.0
    
    def _generate_alternative_explanations(self, hypothesis: Hypothesis) -> List[str]:
        """Generate alternative explanations for a hypothesis"""
        return [
            "Random variation or chance",
            "Confounding variables not accounted for",
            "Alternative causal mechanisms",
            "Measurement artifacts or bias"
        ]
    
    def _identify_test_limitations(self, evidence: List[Evidence]) -> List[str]:
        """Identify limitations in hypothesis testing"""
        limitations = set()
        for e in evidence:
            limitations.update(e.limitations)
        
        common_limitations = [
            "Limited sample size",
            "Potential selection bias",
            "Temporal constraints",
            "Generalizability concerns"
        ]
        
        return list(limitations)[:6]  # Limit to 6
    
    def _generate_test_recommendations(
        self, test_result: TestResult, confidence: float
    ) -> List[str]:
        """Generate recommendations based on test results"""
        recommendations = []
        
        if test_result == TestResult.SUPPORTED:
            recommendations.append("Replicate findings with independent studies")
            recommendations.append("Test boundary conditions and generalizability")
        elif test_result == TestResult.NOT_SUPPORTED:
            recommendations.append("Consider alternative hypotheses")
            recommendations.append("Examine methodology for potential issues")
        elif test_result == TestResult.PARTIALLY_SUPPORTED:
            recommendations.append("Refine hypothesis to better match evidence")
            recommendations.append("Collect additional targeted evidence")
        else:  # INCONCLUSIVE
            recommendations.append("Increase sample size or evidence quality")
            recommendations.append("Improve experimental design")
        
        if confidence < 0.7:
            recommendations.append("Increase confidence through additional validation")
        
        return recommendations[:6]  # Limit to 6