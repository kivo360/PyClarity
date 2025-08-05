"""
Metacognitive Monitoring Analyzer

Core implementation of the metacognitive monitoring cognitive tool, providing
self-reflection and thinking about thinking capabilities through reasoning
process monitoring, bias detection, and strategy evaluation.
"""

import asyncio
import random
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from .models import (
    BiasDetection,
    BiasType,
    ConfidenceAssessment,
    ConfidenceCalibration,
    MetacognitiveMonitoringContext,
    MetacognitiveMonitoringResult,
    MetaLearningInsight,
    MetaStrategies,
    MonitoringDepth,
    MonitoringFrequency,
    ReasoningMonitor,
    StrategyEvaluation,
)


class MetacognitiveMonitoringAnalyzer:
    """Metacognitive monitoring cognitive tool analyzer"""

    def __init__(self):
        """Initialize the metacognitive monitoring analyzer"""
        self.tool_name = "Metacognitive Monitoring"
        self.version = "2.0.0"

        # Internal state for processing
        self._processing_start_time = 0.0
        self._active_monitors: list[ReasoningMonitor] = []
        self._detected_biases: list[BiasDetection] = []
        self._strategy_scores: dict[str, float] = {}

    async def analyze(self, context: MetacognitiveMonitoringContext) -> MetacognitiveMonitoringResult:
        """
        Analyze reasoning process using metacognitive monitoring.

        Args:
            context: Metacognitive monitoring context with target and parameters

        Returns:
            MetacognitiveMonitoringResult with monitoring insights and recommendations
        """
        self._processing_start_time = time.time()

        # Initialize internal state
        self._active_monitors = []
        self._detected_biases = []
        self._strategy_scores = {}

        # Set up reasoning monitors
        reasoning_monitors = await self._setup_reasoning_monitors(context)
        self._active_monitors = reasoning_monitors

        # Detect biases if enabled
        bias_detections = []
        if context.bias_detection_enabled:
            bias_detections = await self._detect_biases(context)
            self._detected_biases = bias_detections

        # Assess confidence calibration if enabled
        confidence_assessment = await self._assess_confidence(context)

        # Evaluate strategies if enabled
        strategy_evaluations = []
        if context.strategy_evaluation_enabled:
            strategy_evaluations = await self._evaluate_strategies(context)

        # Extract meta-learning insights if enabled
        meta_learning_insights = []
        if context.meta_learning_enabled:
            meta_learning_insights = await self._extract_meta_learning_insights(context)

        # Calculate overall metrics
        overall_quality = await self._calculate_overall_quality(
            bias_detections, confidence_assessment, strategy_evaluations
        )

        metacognitive_awareness = await self._calculate_metacognitive_awareness(
            context, reasoning_monitors, bias_detections
        )

        metacognitive_efficiency = await self._calculate_efficiency(
            context, len(reasoning_monitors), len(bias_detections)
        )

        # Generate recommendations and alerts
        improvement_recommendations = await self._generate_recommendations(
            context, bias_detections, confidence_assessment, strategy_evaluations
        )

        intervention_alerts = await self._generate_intervention_alerts(
            context, bias_detections, confidence_assessment
        )

        # Identify reasoning patterns
        reasoning_patterns = await self._identify_reasoning_patterns(
            context, bias_detections, strategy_evaluations
        )

        # Calculate processing time
        monitoring_duration = time.time() - self._processing_start_time

        return MetacognitiveMonitoringResult(
            bias_detections=bias_detections,
            reasoning_monitors=reasoning_monitors,
            confidence_assessment=confidence_assessment,
            strategy_evaluations=strategy_evaluations,
            meta_learning_insights=meta_learning_insights,
            overall_reasoning_quality=overall_quality,
            metacognitive_awareness_level=metacognitive_awareness,
            improvement_recommendations=improvement_recommendations,
            intervention_alerts=intervention_alerts,
            reasoning_patterns_identified=reasoning_patterns,
            monitoring_duration_seconds=monitoring_duration,
            monitors_activated=len(reasoning_monitors),
            biases_corrected=0,  # Will be updated by model validator
            metacognitive_efficiency=metacognitive_efficiency,
            processing_time_ms=round(monitoring_duration * 1000)
        )

    async def _setup_reasoning_monitors(
        self,
        context: MetacognitiveMonitoringContext
    ) -> list[ReasoningMonitor]:
        """Set up monitors for tracking reasoning process"""

        monitors = []

        # Logic consistency monitor
        logic_monitor = ReasoningMonitor(
            monitoring_target="Logical consistency and coherence",
            monitoring_frequency=MonitoringFrequency.CONTINUOUS,
            metrics_tracked=[
                "argument_validity",
                "premise_consistency",
                "conclusion_support",
                "reasoning_gaps"
            ],
            thresholds={
                "argument_validity": 0.8,
                "premise_consistency": 0.85,
                "conclusion_support": 0.75,
                "reasoning_gaps": 0.3
            },
            current_values={
                "argument_validity": random.uniform(0.7, 0.95),
                "premise_consistency": random.uniform(0.75, 0.95),
                "conclusion_support": random.uniform(0.6, 0.9),
                "reasoning_gaps": random.uniform(0.1, 0.4)
            }
        )
        monitors.append(logic_monitor)

        # Progress tracking monitor
        if context.monitoring_depth in [MonitoringDepth.MODERATE, MonitoringDepth.DEEP]:
            progress_monitor = ReasoningMonitor(
                monitoring_target="Reasoning progress and efficiency",
                monitoring_frequency=MonitoringFrequency.PERIODIC,
                metrics_tracked=[
                    "step_completion_rate",
                    "time_efficiency",
                    "backtracking_frequency",
                    "solution_convergence"
                ],
                thresholds={
                    "step_completion_rate": 0.7,
                    "time_efficiency": 0.6,
                    "backtracking_frequency": 0.4,
                    "solution_convergence": 0.65
                },
                current_values={
                    "step_completion_rate": random.uniform(0.6, 0.9),
                    "time_efficiency": random.uniform(0.5, 0.8),
                    "backtracking_frequency": random.uniform(0.2, 0.5),
                    "solution_convergence": random.uniform(0.5, 0.85)
                }
            )
            monitors.append(progress_monitor)

        # Quality assurance monitor
        if context.monitoring_depth == MonitoringDepth.DEEP:
            quality_monitor = ReasoningMonitor(
                monitoring_target="Reasoning quality and depth",
                monitoring_frequency=MonitoringFrequency.MILESTONE,
                metrics_tracked=[
                    "analysis_depth",
                    "evidence_quality",
                    "alternative_consideration",
                    "critical_thinking_level"
                ],
                thresholds={
                    "analysis_depth": 0.75,
                    "evidence_quality": 0.8,
                    "alternative_consideration": 0.7,
                    "critical_thinking_level": 0.75
                },
                current_values={
                    "analysis_depth": random.uniform(0.65, 0.9),
                    "evidence_quality": random.uniform(0.7, 0.95),
                    "alternative_consideration": random.uniform(0.6, 0.85),
                    "critical_thinking_level": random.uniform(0.65, 0.9)
                }
            )
            monitors.append(quality_monitor)

        # Add alerts and interventions based on threshold violations
        for monitor in monitors:
            alerts = []
            interventions = []

            for metric, current_value in monitor.current_values.items():
                threshold = monitor.thresholds.get(metric, 0.5)

                if metric == "reasoning_gaps" or metric == "backtracking_frequency":
                    # For these metrics, lower is better
                    if current_value > threshold:
                        alerts.append(f"{metric} exceeds acceptable threshold")
                        interventions.append(f"Reduce {metric} by improving planning")
                else:
                    # For other metrics, higher is better
                    if current_value < threshold:
                        alerts.append(f"{metric} below minimum threshold")
                        interventions.append(f"Improve {metric} through focused attention")

            monitor.alerts_triggered = alerts
            monitor.interventions_suggested = interventions

        return monitors

    async def _detect_biases(
        self,
        context: MetacognitiveMonitoringContext
    ) -> list[BiasDetection]:
        """Detect cognitive biases in the reasoning process"""

        biases = []
        reasoning_text = context.reasoning_target.lower()

        # Confirmation bias detection
        if any(phrase in reasoning_text for phrase in [
            "as expected", "confirms my", "proves that", "obviously", "clearly shows"
        ]):
            confirmation_bias = BiasDetection(
                bias_type=BiasType.CONFIRMATION_BIAS,
                confidence_level=random.uniform(0.65, 0.85),
                evidence=[
                    "Strong confirmation language detected",
                    "Limited consideration of contradictory evidence",
                    "Selective interpretation of data"
                ],
                manifestation="The reasoning shows a tendency to favor information that confirms existing beliefs while giving less weight to contradictory evidence",
                impact_assessment="This bias may lead to overlooking important alternative explanations and weakening the overall conclusion",
                severity="medium",
                correction_suggestions=[
                    "Actively seek disconfirming evidence",
                    "Consider alternative hypotheses with equal rigor",
                    "Use structured decision frameworks to evaluate all options"
                ]
            )
            biases.append(confirmation_bias)

        # Anchoring bias detection
        if any(phrase in reasoning_text for phrase in [
            "initial", "first impression", "baseline", "starting point", "originally"
        ]):
            anchoring_bias = BiasDetection(
                bias_type=BiasType.ANCHORING_BIAS,
                confidence_level=random.uniform(0.6, 0.8),
                evidence=[
                    "Heavy reliance on initial information",
                    "Insufficient adjustment from starting point",
                    "Limited exploration of alternative anchors"
                ],
                manifestation="The reasoning appears anchored to initial assumptions without sufficient adjustment based on new information",
                impact_assessment="This may result in suboptimal decisions by not fully incorporating all available information",
                severity="low" if context.complexity_level == "simple" else "medium",
                correction_suggestions=[
                    "Question initial assumptions explicitly",
                    "Consider multiple starting points",
                    "Use systematic adjustment techniques"
                ]
            )
            biases.append(anchoring_bias)

        # Availability heuristic detection
        if any(phrase in reasoning_text for phrase in [
            "recent", "memorable", "vivid", "striking example", "comes to mind"
        ]):
            availability_bias = BiasDetection(
                bias_type=BiasType.AVAILABILITY_HEURISTIC,
                confidence_level=random.uniform(0.55, 0.75),
                evidence=[
                    "Overemphasis on recent or memorable events",
                    "Probability judgments based on ease of recall",
                    "Limited use of base rate information"
                ],
                manifestation="The reasoning relies heavily on easily recalled examples rather than systematic analysis of all relevant cases",
                impact_assessment="This could lead to skewed probability assessments and poor risk evaluation",
                severity="medium",
                correction_suggestions=[
                    "Seek comprehensive data rather than relying on memory",
                    "Consider base rates and statistical evidence",
                    "Document and review all relevant cases systematically"
                ]
            )
            biases.append(availability_bias)

        # Overconfidence bias detection
        if any(phrase in reasoning_text for phrase in [
            "certain", "definitely", "no doubt", "guaranteed", "impossible to be wrong"
        ]):
            overconfidence_bias = BiasDetection(
                bias_type=BiasType.OVERCONFIDENCE_BIAS,
                confidence_level=random.uniform(0.7, 0.9),
                evidence=[
                    "Excessive certainty in conclusions",
                    "Underestimation of uncertainty",
                    "Limited acknowledgment of potential errors"
                ],
                manifestation="The reasoning displays excessive confidence without adequate consideration of uncertainty and potential errors",
                impact_assessment="Overconfidence may lead to inadequate risk management and poor decision-making under uncertainty",
                severity="high" if context.complexity_level in ["complex", "very_complex"] else "medium",
                correction_suggestions=[
                    "Explicitly quantify uncertainty ranges",
                    "Conduct pre-mortem analysis",
                    "Seek external calibration of confidence levels",
                    "Consider worst-case scenarios"
                ]
            )
            biases.append(overconfidence_bias)

        return biases

    async def _assess_confidence(
        self,
        context: MetacognitiveMonitoringContext
    ) -> ConfidenceAssessment:
        """Assess and calibrate confidence levels"""

        # Simulate stated confidence based on reasoning language
        reasoning_text = context.reasoning_target.lower()

        # Count confidence indicators
        high_confidence_words = sum(1 for word in [
            "certain", "definitely", "clearly", "obviously", "undoubtedly"
        ] if word in reasoning_text)

        low_confidence_words = sum(1 for word in [
            "maybe", "perhaps", "possibly", "might", "could be"
        ] if word in reasoning_text)

        # Calculate stated confidence
        if high_confidence_words > low_confidence_words:
            stated_confidence = min(0.95, 0.7 + (high_confidence_words * 0.05))
        elif low_confidence_words > high_confidence_words:
            stated_confidence = max(0.3, 0.6 - (low_confidence_words * 0.05))
        else:
            stated_confidence = 0.65

        # Calibrate confidence based on method
        calibration_factors = []

        if context.calibration_method == ConfidenceCalibration.EVIDENCE_BASED:
            # Adjust based on evidence quality
            evidence_adjustment = random.uniform(-0.15, 0.1)
            calibration_factors.append("Quality and quantity of supporting evidence")
            calibration_factors.append("Strength of logical arguments")

        elif context.calibration_method == ConfidenceCalibration.HISTORICAL_PERFORMANCE:
            # Adjust based on past accuracy
            historical_adjustment = random.uniform(-0.1, 0.05)
            evidence_adjustment = historical_adjustment
            calibration_factors.append("Historical accuracy in similar domains")
            calibration_factors.append("Past calibration performance")

        elif context.calibration_method == ConfidenceCalibration.PEER_COMPARISON:
            # Adjust based on peer benchmarks
            peer_adjustment = random.uniform(-0.12, 0.08)
            evidence_adjustment = peer_adjustment
            calibration_factors.append("Comparison with peer assessments")
            calibration_factors.append("Expert consensus levels")

        else:
            evidence_adjustment = random.uniform(-0.1, 0.05)
            calibration_factors.append("General calibration heuristics")

        # Add complexity adjustment
        complexity_adjustment = {
            "simple": 0.05,
            "moderate": 0.0,
            "complex": -0.05,
            "very_complex": -0.1
        }.get(context.complexity_level.value, 0.0)

        calibration_factors.append(f"Complexity level: {context.complexity_level.value}")

        # Calculate calibrated confidence
        calibrated_confidence = max(0.0, min(1.0,
            stated_confidence + evidence_adjustment + complexity_adjustment
        ))

        # Calculate confidence interval
        interval_width = 0.15 if context.complexity_level.value in ["simple", "moderate"] else 0.25
        confidence_interval = {
            "lower": max(0.0, calibrated_confidence - interval_width),
            "upper": min(1.0, calibrated_confidence + interval_width)
        }

        # Calculate reliability score
        reliability_score = 0.8 if abs(stated_confidence - calibrated_confidence) < 0.15 else 0.6

        return ConfidenceAssessment(
            stated_confidence=stated_confidence,
            calibrated_confidence=calibrated_confidence,
            calibration_method=context.calibration_method,
            calibration_factors=calibration_factors,
            overconfidence_detected=False,  # Will be set by model validator
            underconfidence_detected=False,  # Will be set by model validator
            confidence_interval=confidence_interval,
            reliability_score=reliability_score
        )

    async def _evaluate_strategies(
        self,
        context: MetacognitiveMonitoringContext
    ) -> list[StrategyEvaluation]:
        """Evaluate reasoning strategies used"""

        evaluations = []

        # Analyze reasoning text for strategy indicators
        reasoning_text = context.reasoning_target.lower()

        # Analytical strategy evaluation
        if any(phrase in reasoning_text for phrase in [
            "analyze", "break down", "component", "systematic", "step by step"
        ]):
            analytical_eval = StrategyEvaluation(
                strategy_name="Analytical Decomposition",
                strategy_description="Breaking down complex problems into manageable components for systematic analysis",
                effectiveness_score=random.uniform(0.7, 0.9),
                efficiency_score=random.uniform(0.65, 0.85),
                appropriateness_score=0.85 if context.complexity_level.value in ["complex", "very_complex"] else 0.7,
                strengths=[
                    "Systematic approach reduces complexity",
                    "Clear identification of sub-problems",
                    "Thorough analysis of components"
                ],
                weaknesses=[
                    "May miss emergent properties",
                    "Time-intensive process",
                    "Risk of over-analysis"
                ],
                alternative_strategies=[
                    "Holistic synthesis approach",
                    "Pattern recognition strategy",
                    "Intuitive problem-solving"
                ],
                improvement_suggestions=[
                    "Balance decomposition with synthesis phases",
                    "Set time limits for analysis stages",
                    "Include periodic big-picture reviews"
                ],
                context_suitability="Well-suited for complex, multi-faceted problems requiring detailed understanding"
            )
            evaluations.append(analytical_eval)
            self._strategy_scores["analytical"] = analytical_eval.effectiveness_score

        # Creative strategy evaluation
        if any(phrase in reasoning_text for phrase in [
            "creative", "innovative", "novel", "brainstorm", "imagine"
        ]):
            creative_eval = StrategyEvaluation(
                strategy_name="Creative Exploration",
                strategy_description="Using divergent thinking and creative approaches to generate novel solutions",
                effectiveness_score=random.uniform(0.65, 0.85),
                efficiency_score=random.uniform(0.5, 0.75),
                appropriateness_score=0.8 if "novel" in context.reasoning_target else 0.6,
                strengths=[
                    "Generates innovative solutions",
                    "Breaks conventional thinking patterns",
                    "Explores solution space broadly"
                ],
                weaknesses=[
                    "Less predictable outcomes",
                    "May lack systematic validation",
                    "Time efficiency varies greatly"
                ],
                alternative_strategies=[
                    "Structured problem-solving",
                    "Best practices application",
                    "Algorithmic approach"
                ],
                improvement_suggestions=[
                    "Combine with systematic validation",
                    "Set creative exploration boundaries",
                    "Use structured creativity techniques"
                ],
                context_suitability="Effective when conventional approaches have failed or innovation is explicitly required"
            )
            evaluations.append(creative_eval)
            self._strategy_scores["creative"] = creative_eval.effectiveness_score

        # Evidence-based strategy evaluation
        if any(phrase in reasoning_text for phrase in [
            "evidence", "data", "research", "study", "empirical"
        ]):
            evidence_eval = StrategyEvaluation(
                strategy_name="Evidence-Based Reasoning",
                strategy_description="Making decisions based on empirical evidence and data-driven insights",
                effectiveness_score=random.uniform(0.75, 0.95),
                efficiency_score=random.uniform(0.6, 0.8),
                appropriateness_score=0.9,
                strengths=[
                    "High reliability of conclusions",
                    "Objective decision basis",
                    "Verifiable reasoning process",
                    "Reduced bias impact"
                ],
                weaknesses=[
                    "Limited by available evidence",
                    "May miss qualitative factors",
                    "Time needed for evidence gathering"
                ],
                alternative_strategies=[
                    "Intuition-based approach",
                    "Theory-driven reasoning",
                    "Analogical reasoning"
                ],
                improvement_suggestions=[
                    "Expand evidence sources",
                    "Include qualitative evidence",
                    "Develop evidence quality criteria"
                ],
                context_suitability="Ideal for high-stakes decisions requiring justifiable and reliable conclusions"
            )
            evaluations.append(evidence_eval)
            self._strategy_scores["evidence_based"] = evidence_eval.effectiveness_score

        return evaluations

    async def _extract_meta_learning_insights(
        self,
        context: MetacognitiveMonitoringContext
    ) -> list[MetaLearningInsight]:
        """Extract insights from the meta-learning process"""

        insights = []

        # Pattern recognition insight
        if self._detected_biases:
            bias_pattern_insight = MetaLearningInsight(
                insight_type="pattern",
                insight_description=f"Recurring bias patterns detected in reasoning process. Most prominent biases include {', '.join([b.bias_type.value for b in self._detected_biases[:2]])}. This pattern suggests systematic tendencies in information processing that could be addressed through structured decision frameworks.",
                supporting_evidence=[
                    f"{len(self._detected_biases)} distinct biases identified",
                    "Consistent manifestation across reasoning stages",
                    "Correlation between bias types and reasoning complexity"
                ],
                generalizability=0.75,
                actionability=0.85,
                implications=[
                    "Need for bias-aware reasoning protocols",
                    "Value of external perspective in complex decisions",
                    "Importance of structured decision frameworks"
                ],
                related_insights=["cognitive load impacts bias susceptibility"],
                confidence_in_insight=0.8
            )
            insights.append(bias_pattern_insight)

        # Strategy effectiveness insight
        if self._strategy_scores:
            best_strategy = max(self._strategy_scores.items(), key=lambda x: x[1])
            strategy_insight = MetaLearningInsight(
                insight_type="strategy",
                insight_description=f"The {best_strategy[0]} strategy demonstrated highest effectiveness ({best_strategy[1]:.2f}) for this type of reasoning task. This suggests alignment between strategy choice and problem characteristics, indicating good metacognitive strategy selection.",
                supporting_evidence=[
                    "Performance metrics across multiple strategies",
                    "Correlation with problem complexity level",
                    "Consistency with theoretical predictions"
                ],
                generalizability=0.7,
                actionability=0.9,
                implications=[
                    "Continue using this strategy for similar problems",
                    "Develop strategy selection heuristics",
                    "Build strategy repertoire for different contexts"
                ],
                related_insights=["problem type influences optimal strategy choice"],
                confidence_in_insight=0.85
            )
            insights.append(strategy_insight)

        # Performance optimization insight
        if self._active_monitors:
            avg_performance = sum(
                sum(m.current_values.values()) / len(m.current_values)
                for m in self._active_monitors
            ) / len(self._active_monitors)

            performance_insight = MetaLearningInsight(
                insight_type="performance",
                insight_description=f"Overall reasoning performance averages {avg_performance:.2f}, with notable variations across different monitoring dimensions. Key performance drivers include logical consistency and evidence quality. Targeted improvements in lowest-scoring areas could yield significant overall gains.",
                supporting_evidence=[
                    "Multi-dimensional performance tracking",
                    "Identification of performance bottlenecks",
                    "Correlation analysis between dimensions"
                ],
                generalizability=0.65,
                actionability=0.8,
                implications=[
                    "Focus improvement efforts on weak areas",
                    "Maintain strengths while addressing gaps",
                    "Consider performance trade-offs"
                ],
                related_insights=["balanced performance across dimensions improves outcomes"],
                confidence_in_insight=0.75
            )
            insights.append(performance_insight)

        # Context sensitivity insight
        context_insight = MetaLearningInsight(
            insight_type="context",
            insight_description=f"The reasoning process shows high context sensitivity, with {context.complexity_level.value} complexity requiring adapted approaches. Success factors include matching monitoring depth to problem complexity and adjusting confidence calibration methods based on available information.",
            supporting_evidence=[
                "Complexity-appropriate strategy selection",
                "Adaptive monitoring depth",
                "Context-aware bias detection"
            ],
            generalizability=0.85,
            actionability=0.75,
            implications=[
                "Develop context assessment protocols",
                "Build adaptive reasoning frameworks",
                "Create complexity-based heuristics"
            ],
            related_insights=["context assessment is crucial for reasoning success"],
            confidence_in_insight=0.8
        )
        insights.append(context_insight)

        return insights

    async def _calculate_overall_quality(
        self,
        biases: list[BiasDetection],
        confidence: ConfidenceAssessment,
        strategies: list[StrategyEvaluation]
    ) -> float:
        """Calculate overall reasoning quality score"""

        # Base quality from confidence calibration
        confidence_quality = confidence.reliability_score

        # Penalty for biases (weighted by severity)
        bias_penalty = 0.0
        if biases:
            severity_weights = {"low": 0.05, "medium": 0.1, "high": 0.2}
            bias_penalty = sum(
                severity_weights.get(bias.severity, 0.1) * bias.confidence_level
                for bias in biases
            ) / len(biases)

        # Bonus for effective strategies
        strategy_bonus = 0.0
        if strategies:
            avg_effectiveness = sum(s.effectiveness_score for s in strategies) / len(strategies)
            strategy_bonus = avg_effectiveness * 0.15

        # Calculate final quality
        quality = confidence_quality - bias_penalty + strategy_bonus

        # Ensure quality is within bounds
        return max(0.0, min(1.0, quality))

    async def _calculate_metacognitive_awareness(
        self,
        context: MetacognitiveMonitoringContext,
        monitors: list[ReasoningMonitor],
        biases: list[BiasDetection]
    ) -> float:
        """Calculate level of metacognitive awareness"""

        # Base awareness from monitoring setup
        monitoring_score = len(monitors) / 5.0  # Normalize by expected max monitors

        # Awareness from bias recognition
        bias_recognition = len(biases) * 0.1 if biases else 0.0

        # Awareness from monitoring depth
        depth_scores = {
            MonitoringDepth.SURFACE: 0.5,
            MonitoringDepth.MODERATE: 0.75,
            MonitoringDepth.DEEP: 1.0
        }
        depth_score = depth_scores.get(context.monitoring_depth, 0.75)

        # Combine scores
        awareness = (monitoring_score + bias_recognition + depth_score) / 3.0

        return min(1.0, awareness)

    async def _calculate_efficiency(
        self,
        context: MetacognitiveMonitoringContext,
        monitors_count: int,
        biases_count: int
    ) -> float:
        """Calculate metacognitive process efficiency"""

        # Efficiency based on focused monitoring
        focus_efficiency = 1.0 if context.monitoring_focus else 0.8

        # Efficiency based on appropriate depth
        depth_efficiency = {
            MonitoringDepth.SURFACE: 0.9,
            MonitoringDepth.MODERATE: 0.85,
            MonitoringDepth.DEEP: 0.7
        }.get(context.monitoring_depth, 0.85)

        # Efficiency from selective activation
        activation_efficiency = 1.0 - (monitors_count * 0.05)

        # Combine efficiencies
        efficiency = (focus_efficiency + depth_efficiency + activation_efficiency) / 3.0

        return max(0.0, min(1.0, efficiency))

    async def _generate_recommendations(
        self,
        context: MetacognitiveMonitoringContext,
        biases: list[BiasDetection],
        confidence: ConfidenceAssessment,
        strategies: list[StrategyEvaluation]
    ) -> list[str]:
        """Generate improvement recommendations"""

        recommendations = []

        # Bias-related recommendations
        if biases:
            most_severe = max(biases, key=lambda b: (b.severity == "high", b.confidence_level))
            recommendations.append(
                f"Address {most_severe.bias_type.value} through {most_severe.correction_suggestions[0]}"
            )

            if len(biases) > 2:
                recommendations.append(
                    "Implement systematic bias checking protocol for complex decisions"
                )

        # Confidence calibration recommendations
        if confidence.overconfidence_detected:
            recommendations.append(
                "Reduce overconfidence by explicitly considering uncertainty and worst-case scenarios"
            )
        elif confidence.underconfidence_detected:
            recommendations.append(
                "Build confidence through systematic validation of reasoning steps"
            )

        # Strategy recommendations
        if strategies:
            lowest_scoring = min(strategies, key=lambda s: s.effectiveness_score)
            if lowest_scoring.effectiveness_score < 0.7:
                recommendations.append(
                    f"Improve {lowest_scoring.strategy_name} effectiveness through: {lowest_scoring.improvement_suggestions[0]}"
                )

        # General recommendations based on monitoring
        if context.monitoring_depth == MonitoringDepth.SURFACE:
            recommendations.append(
                "Consider deeper monitoring for complex decisions to catch subtle issues"
            )

        # Add recommendations for high complexity problems
        if context.complexity_level.value in ["complex", "very_complex"]:
            recommendations.append(
                "Use structured frameworks and external validation for high-complexity reasoning"
            )
            recommendations.append(
                "Break complex reasoning into verifiable intermediate steps"
            )

        return recommendations[:10]  # Limit to 10 recommendations

    async def _generate_intervention_alerts(
        self,
        context: MetacognitiveMonitoringContext,
        biases: list[BiasDetection],
        confidence: ConfidenceAssessment
    ) -> list[str]:
        """Generate alerts for immediate interventions"""

        alerts = []

        # High severity bias alerts
        high_severity_biases = [b for b in biases if b.severity == "high"]
        for bias in high_severity_biases:
            alerts.append(
                f"HIGH PRIORITY: {bias.bias_type.value} detected with {bias.confidence_level:.0%} confidence"
            )

        # Extreme confidence miscalibration alerts
        confidence_diff = abs(confidence.calibrated_confidence - confidence.stated_confidence)
        if confidence_diff > 0.3:
            alerts.append(
                f"CONFIDENCE MISCALIBRATION: {confidence_diff:.0%} gap between stated and calibrated confidence"
            )

        # Monitor threshold violations
        for monitor in self._active_monitors:
            if monitor.alerts_triggered:
                alerts.append(
                    f"MONITOR ALERT: {monitor.monitoring_target} - {monitor.alerts_triggered[0]}"
                )

        return alerts[:5]  # Limit to 5 most important alerts

    async def _identify_reasoning_patterns(
        self,
        context: MetacognitiveMonitoringContext,
        biases: list[BiasDetection],
        strategies: list[StrategyEvaluation]
    ) -> list[str]:
        """Identify patterns in the reasoning process"""

        patterns = []

        # Bias clustering patterns
        if len(biases) >= 2:
            bias_types = [b.bias_type.value for b in biases]
            if BiasType.CONFIRMATION_BIAS.value in bias_types and BiasType.ANCHORING_BIAS.value in bias_types:
                patterns.append(
                    "Tendency toward fixed thinking: confirmation and anchoring biases reinforce each other"
                )

        # Strategy consistency patterns
        if strategies:
            effectiveness_scores = [s.effectiveness_score for s in strategies]
            if all(score > 0.75 for score in effectiveness_scores):
                patterns.append(
                    "Consistent high-quality strategy selection across reasoning stages"
                )
            elif any(score < 0.6 for score in effectiveness_scores):
                patterns.append(
                    "Inconsistent strategy effectiveness suggesting need for adaptive approach"
                )

        # Complexity handling patterns
        if context.complexity_level.value in ["complex", "very_complex"]:
            patterns.append(
                "Complex problem decomposition pattern with systematic sub-problem analysis"
            )

        # Monitoring adaptation patterns
        if context.monitoring_depth == MonitoringDepth.DEEP and len(self._active_monitors) > 2:
            patterns.append(
                "Comprehensive monitoring pattern indicating high metacognitive engagement"
            )

        # Evidence usage patterns
        if "evidence" in context.reasoning_target.lower():
            patterns.append(
                "Evidence-driven reasoning pattern with emphasis on empirical support"
            )

        return patterns[:8]  # Limit to 8 patterns
