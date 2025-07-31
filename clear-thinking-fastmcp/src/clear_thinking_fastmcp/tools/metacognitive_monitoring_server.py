# Clear Thinking FastMCP Server - Metacognitive Monitoring Server

"""
FastMCP server implementation for Metacognitive Monitoring cognitive tool.

This server provides self-reflection and thinking about thinking through:
- Reasoning process monitoring
- Bias detection and correction
- Confidence calibration
- Strategy evaluation and adjustment
- Meta-learning from reasoning patterns

Agent: AGENT D - Metacognitive Monitoring Implementation
Status: ACTIVE - Phase 2C Parallel Expansion
"""

import asyncio
import time
from typing import List, Dict, Any, Optional
from fastmcp.server import Context

from ..models.metacognitive_monitoring import (
    MetacognitiveMonitoringInput,
    MetacognitiveMonitoringOutput,
    BiasDetection,
    ReasoningMonitor,
    ConfidenceAssessment,
    StrategyEvaluation,
    MetaLearningInsight,
    BiasType,
    MetaStrategies,
    ConfidenceCalibration
)
from .base import CognitiveToolBase


class MetacognitiveMonitoringServer(CognitiveToolBase):
    """Server implementation for Metacognitive Monitoring tool"""
    
    def __init__(self):
        super().__init__()
        self.tool_name = "Metacognitive Monitoring"
        self.version = "1.0.0"
        self.description = "Self-reflection and thinking about thinking processes"
    
    async def process(
        self, 
        input_data: MetacognitiveMonitoringInput, 
        context: Context
    ) -> MetacognitiveMonitoringOutput:
        """Process metacognitive monitoring of reasoning"""
        
        start_time = time.time()
        
        try:
            await context.info(f"🧠 Starting Metacognitive Monitoring of: {input_data.reasoning_target}")
            await context.progress("Initializing metacognitive monitoring", 0.0)
            
            # Phase 1: Set up monitoring systems
            await context.info("Phase 1: Setting up reasoning monitors")
            reasoning_monitors = await self._setup_monitoring_systems(
                input_data, context
            )
            await context.progress("Set up monitoring systems", 0.2)
            
            # Phase 2: Detect cognitive biases
            bias_detections = []
            if input_data.bias_detection_enabled:
                await context.info("Phase 2: Detecting cognitive biases")
                bias_detections = await self._detect_biases(
                    input_data, context
                )
                await context.progress("Detected cognitive biases", 0.4)
            
            # Phase 3: Calibrate confidence
            confidence_assessment = None
            if input_data.confidence_calibration_enabled:
                await context.info("Phase 3: Calibrating confidence levels")
                confidence_assessment = await self._calibrate_confidence(
                    input_data, context
                )
                await context.progress("Calibrated confidence", 0.6)
            
            # Phase 4: Evaluate strategies
            strategy_evaluations = []
            if input_data.strategy_evaluation_enabled:
                await context.info("Phase 4: Evaluating reasoning strategies")
                strategy_evaluations = await self._evaluate_strategies(
                    input_data, reasoning_monitors, context
                )
                await context.progress("Evaluated strategies", 0.8)
            
            # Phase 5: Generate meta-learning insights
            meta_insights = []
            if input_data.meta_learning_enabled:
                await context.info("Phase 5: Generating meta-learning insights")
                meta_insights = await self._generate_meta_insights(
                    input_data, bias_detections, strategy_evaluations, context
                )
                await context.progress("Generated meta-learning insights", 0.9)
            
            # Phase 6: Synthesize results and recommendations
            await context.info("Phase 6: Synthesizing monitoring results")
            (
                reasoning_quality,
                awareness_level,
                recommendations,
                alerts,
                patterns
            ) = await self._synthesize_results(
                input_data,
                reasoning_monitors,
                bias_detections,
                confidence_assessment,
                strategy_evaluations,
                meta_insights,
                context
            )
            
            processing_time = time.time() - start_time
            
            # Create output
            output = MetacognitiveMonitoringOutput(
                problem=input_data.problem,
                complexity_level=input_data.complexity_level,
                confidence_score=confidence_assessment.calibrated_confidence if confidence_assessment else 0.5,
                analysis=f"Metacognitive monitoring completed with {len(reasoning_monitors)} monitors, {len(bias_detections)} biases detected",
                session_id=input_data.session_id,
                bias_detections=bias_detections,
                reasoning_monitors=reasoning_monitors,
                confidence_assessment=confidence_assessment or self._default_confidence_assessment(),
                strategy_evaluations=strategy_evaluations,
                meta_learning_insights=meta_insights,
                overall_reasoning_quality=reasoning_quality,
                metacognitive_awareness_level=awareness_level,
                improvement_recommendations=recommendations,
                intervention_alerts=alerts,
                reasoning_patterns_identified=patterns,
                monitoring_duration_seconds=processing_time,
                monitors_activated=len(reasoning_monitors),
                biases_corrected=len([b for b in bias_detections if b.correction_suggestions]),
                metacognitive_efficiency=min(1.0, awareness_level * reasoning_quality)
            )
            
            await context.progress("Metacognitive monitoring completed", 1.0)
            await context.info(f"✅ Metacognitive Monitoring completed in {processing_time:.2f}s")
            
            return output
            
        except Exception as e:
            await context.error(f"Metacognitive Monitoring failed: {str(e)}")
            raise
    
    async def _setup_monitoring_systems(
        self,
        input_data: MetacognitiveMonitoringInput,
        context: Context
    ) -> List[ReasoningMonitor]:
        """Set up monitoring systems for reasoning process"""
        
        monitors = []
        
        # Core reasoning quality monitor
        quality_monitor = ReasoningMonitor(
            monitoring_target="reasoning_quality",
            monitoring_frequency="continuous",
            metrics_tracked=["logical_consistency", "evidence_support", "conclusion_validity"],
            thresholds={"logical_consistency": 0.7, "evidence_support": 0.6, "conclusion_validity": 0.8},
            current_values={"logical_consistency": 0.8, "evidence_support": 0.7, "conclusion_validity": 0.75}
        )
        monitors.append(quality_monitor)
        
        # Confidence tracking monitor
        confidence_monitor = ReasoningMonitor(
            monitoring_target="confidence_calibration",
            monitoring_frequency="periodic",
            metrics_tracked=["stated_confidence", "actual_accuracy", "overconfidence_bias"],
            thresholds={"overconfidence_bias": 0.3, "calibration_error": 0.2},
            current_values={"stated_confidence": 0.8, "calibration_error": 0.15}
        )
        monitors.append(confidence_monitor)
        
        # Strategy effectiveness monitor
        strategy_monitor = ReasoningMonitor(
            monitoring_target="strategy_effectiveness",
            monitoring_frequency="milestone",
            metrics_tracked=["efficiency", "accuracy", "appropriateness"],
            thresholds={"efficiency": 0.6, "accuracy": 0.7, "appropriateness": 0.8},
            current_values={"efficiency": 0.75, "accuracy": 0.8, "appropriateness": 0.85}
        )
        monitors.append(strategy_monitor)
        
        # Add focus-specific monitors
        for focus_area in input_data.monitoring_focus:
            focus_monitor = ReasoningMonitor(
                monitoring_target=focus_area,
                monitoring_frequency="periodic",
                metrics_tracked=[f"{focus_area}_quality", f"{focus_area}_consistency"],
                thresholds={f"{focus_area}_quality": input_data.intervention_threshold},
                current_values={f"{focus_area}_quality": 0.7}
            )
            monitors.append(focus_monitor)
        
        # Check for threshold violations and generate alerts
        for monitor in monitors:
            for metric, threshold in monitor.thresholds.items():
                current_value = monitor.current_values.get(metric, 0.5)
                if current_value < threshold:
                    alert = f"Monitor '{monitor.monitoring_target}': {metric} below threshold ({current_value:.2f} < {threshold:.2f})"
                    monitor.alerts_triggered.append(alert)
                    monitor.interventions_suggested.append(f"Improve {metric} in {monitor.monitoring_target}")
        
        await context.debug(f"Set up {len(monitors)} reasoning monitors")
        return monitors
    
    async def _detect_biases(
        self,
        input_data: MetacognitiveMonitoringInput,
        context: Context
    ) -> List[BiasDetection]:
        """Detect cognitive biases in reasoning process"""
        
        bias_detections = []
        
        # Check for common biases based on reasoning patterns
        potential_biases = [
            BiasType.CONFIRMATION_BIAS,
            BiasType.ANCHORING_BIAS,
            BiasType.OVERCONFIDENCE_BIAS,
            BiasType.AVAILABILITY_HEURISTIC
        ]
        
        for bias_type in potential_biases:
            detection = await self._analyze_bias(bias_type, input_data, context)
            if detection.confidence_level > 0.3:  # Only include likely biases
                bias_detections.append(detection)
        
        await context.debug(f"Detected {len(bias_detections)} potential biases")
        return bias_detections
    
    async def _analyze_bias(
        self,
        bias_type: BiasType,
        input_data: MetacognitiveMonitoringInput,
        context: Context
    ) -> BiasDetection:
        """Analyze for a specific type of bias"""
        
        # Simulate bias detection logic
        if bias_type == BiasType.CONFIRMATION_BIAS:
            confidence = 0.4  # Moderate likelihood
            evidence = ["Selective evidence consideration", "Limited alternative exploration"]
            manifestation = "Tendency to favor information that confirms initial assessment"
            impact = "May lead to overlooking contradictory evidence"
            corrections = ["Actively seek disconfirming evidence", "Consider alternative interpretations"]
            severity = "medium"
        
        elif bias_type == BiasType.OVERCONFIDENCE_BIAS:
            confidence = 0.6  # Higher likelihood
            evidence = ["High confidence without proportional evidence", "Limited uncertainty acknowledgment"]
            manifestation = "Confidence levels exceed accuracy levels"
            impact = "May lead to insufficient preparation for alternatives"
            corrections = ["Calibrate confidence against historical accuracy", "Seek external validation"]
            severity = "high"
        
        elif bias_type == BiasType.ANCHORING_BIAS:
            confidence = 0.3  # Lower likelihood
            evidence = ["Heavy reliance on initial information"]
            manifestation = "Insufficient adjustment from starting point"
            impact = "May limit exploration of full solution space"
            corrections = ["Consider multiple starting points", "Delay initial judgments"]
            severity = "low"
        
        else:
            confidence = 0.2
            evidence = ["General bias indicators"]
            manifestation = f"Potential {bias_type.value} patterns"
            impact = "Minimal impact detected"
            corrections = ["General bias awareness"]
            severity = "low"
        
        return BiasDetection(
            bias_type=bias_type,
            confidence_level=confidence,
            evidence=evidence,
            manifestation=manifestation,
            impact_assessment=impact,
            severity=severity,
            correction_suggestions=corrections
        )
    
    async def _calibrate_confidence(
        self,
        input_data: MetacognitiveMonitoringInput,
        context: Context
    ) -> ConfidenceAssessment:
        """Calibrate confidence levels"""
        
        # Simulate confidence calibration
        stated_confidence = 0.8  # Typically high initial confidence
        
        # Apply calibration based on method
        if input_data.calibration_method == ConfidenceCalibration.EVIDENCE_BASED:
            calibrated_confidence = stated_confidence * 0.85  # Slight reduction
            factors = ["Evidence quality", "Evidence completeness", "Alternative considerations"] 
        elif input_data.calibration_method == ConfidenceCalibration.HISTORICAL_PERFORMANCE:
            calibrated_confidence = stated_confidence * 0.75  # More conservative
            factors = ["Past accuracy", "Similar problem performance", "Context familiarity"]
        else:
            calibrated_confidence = stated_confidence * 0.9  # Minimal adjustment
            factors = ["General calibration", "Uncertainty acknowledgment"]
        
        # Detect over/under confidence
        overconfidence = stated_confidence - calibrated_confidence > 0.1
        underconfidence = calibrated_confidence - stated_confidence > 0.1
        
        return ConfidenceAssessment(
            stated_confidence=stated_confidence,
            calibrated_confidence=calibrated_confidence,
            calibration_method=input_data.calibration_method,
            calibration_factors=factors,
            overconfidence_detected=overconfidence,
            underconfidence_detected=underconfidence,
            confidence_interval={"lower": calibrated_confidence - 0.1, "upper": calibrated_confidence + 0.1},
            reliability_score=0.8
        )
    
    async def _evaluate_strategies(
        self,
        input_data: MetacognitiveMonitoringInput,
        monitors: List[ReasoningMonitor],
        context: Context
    ) -> List[StrategyEvaluation]:
        """Evaluate reasoning strategies"""
        
        evaluations = []
        
        # Evaluate current reasoning strategy
        current_strategy = StrategyEvaluation(
            strategy_name="Systematic Analysis",
            strategy_description="Step-by-step systematic approach to problem analysis",
            effectiveness_score=0.8,
            efficiency_score=0.7,
            appropriateness_score=0.85,
            strengths=["Thorough coverage", "Logical progression", "Evidence-based"],
            weaknesses=["Time-intensive", "May miss creative solutions"],
            alternative_strategies=["Intuitive approach", "Collaborative reasoning", "Creative problem solving"],
            improvement_suggestions=["Incorporate creative elements", "Add time management", "Include stakeholder perspectives"],
            context_suitability="Well-suited for complex analytical problems"
        )
        evaluations.append(current_strategy)
        
        # Evaluate metacognitive strategy
        meta_strategy = StrategyEvaluation(
            strategy_name="Metacognitive Monitoring",
            strategy_description="Self-monitoring and regulation of thinking processes",
            effectiveness_score=0.75,
            efficiency_score=0.6,
            appropriateness_score=0.9,
            strengths=["Bias awareness", "Confidence calibration", "Self-correction"],
            weaknesses=["Overhead cost", "Potential overthinking"],
            alternative_strategies=["Expert consultation", "Peer review", "Automated checking"],
            improvement_suggestions=["Balance monitoring with action", "Focus on high-impact areas"],
            context_suitability="Excellent for high-stakes decisions requiring accuracy"
        )
        evaluations.append(meta_strategy)
        
        await context.debug(f"Evaluated {len(evaluations)} reasoning strategies")
        return evaluations
    
    async def _generate_meta_insights(
        self,
        input_data: MetacognitiveMonitoringInput,
        bias_detections: List[BiasDetection],
        strategy_evaluations: List[StrategyEvaluation],
        context: Context
    ) -> List[MetaLearningInsight]:
        """Generate meta-learning insights"""
        
        insights = []
        
        # Pattern insight
        pattern_insight = MetaLearningInsight(
            insight_type="pattern",
            insight_description="Tendency to start with high confidence that gets calibrated down through systematic analysis",
            supporting_evidence=["Initial confidence: 0.8", "Calibrated confidence: 0.68", "Consistent overconfidence pattern"],
            generalizability=0.7,
            actionability=0.8,
            implications=["Need for earlier confidence calibration", "Value of systematic doubt"],
            related_insights=["Overconfidence bias detection"],
            confidence_in_insight=0.75
        )
        insights.append(pattern_insight)
        
        # Strategy insight
        if strategy_evaluations:
            best_strategy = max(strategy_evaluations, key=lambda s: s.effectiveness_score)
            strategy_insight = MetaLearningInsight(
                insight_type="strategy",
                insight_description=f"'{best_strategy.strategy_name}' most effective with {best_strategy.effectiveness_score:.1%} success rate",
                supporting_evidence=[f"Effectiveness: {best_strategy.effectiveness_score:.1%}", f"Appropriateness: {best_strategy.appropriateness_score:.1%}"],
                generalizability=0.6,
                actionability=0.9,
                implications=["Prioritize systematic approaches", "Balance thoroughness with efficiency"],
                related_insights=["Efficiency vs effectiveness tradeoff"],
                confidence_in_insight=0.8
            )
            insights.append(strategy_insight)
        
        # Bias insight
        if bias_detections:
            high_confidence_biases = [b for b in bias_detections if b.confidence_level > 0.5]
            if high_confidence_biases:
                bias_insight = MetaLearningInsight(
                    insight_type="bias",
                    insight_description=f"Detected {len(high_confidence_biases)} high-confidence biases requiring attention",
                    supporting_evidence=[f"{b.bias_type.value}: {b.confidence_level:.1%}" for b in high_confidence_biases],
                    generalizability=0.8,
                    actionability=0.9,
                    implications=["Implement bias checking procedures", "Seek external perspectives"],
                    related_insights=["Systematic bias patterns"],
                    confidence_in_insight=0.85
                )
                insights.append(bias_insight)
        
        await context.debug(f"Generated {len(insights)} meta-learning insights")
        return insights
    
    async def _synthesize_results(
        self,
        input_data: MetacognitiveMonitoringInput,
        monitors: List[ReasoningMonitor],
        bias_detections: List[BiasDetection],
        confidence_assessment: Optional[ConfidenceAssessment],
        strategy_evaluations: List[StrategyEvaluation],
        meta_insights: List[MetaLearningInsight],
        context: Context
    ) -> tuple[float, float, List[str], List[str], List[str]]:
        """Synthesize all monitoring results"""
        
        # Calculate overall reasoning quality
        quality_scores = []
        for monitor in monitors:
            monitor_quality = sum(monitor.current_values.values()) / len(monitor.current_values) if monitor.current_values else 0.5
            quality_scores.append(monitor_quality)
        
        overall_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0.5
        
        # Calculate metacognitive awareness level
        awareness_factors = [
            len(bias_detections) * 0.1,  # Bias awareness
            (confidence_assessment.reliability_score if confidence_assessment else 0.5) * 0.3,  # Confidence calibration
            (sum(s.effectiveness_score for s in strategy_evaluations) / len(strategy_evaluations) if strategy_evaluations else 0.5) * 0.3,  # Strategy awareness
            len(meta_insights) * 0.1  # Meta-learning
        ]
        awareness_level = min(1.0, sum(awareness_factors))
        
        # Generate recommendations
        recommendations = [
            "Continue systematic monitoring of reasoning processes",
            "Address detected biases through corrective actions",
            "Calibrate confidence more frequently during reasoning",
            "Apply meta-learning insights to future reasoning tasks"
        ]
        
        # Add specific recommendations based on findings
        high_severity_biases = [b for b in bias_detections if b.severity == "high"]
        if high_severity_biases:
            recommendations.append(f"Immediately address {len(high_severity_biases)} high-severity biases")
        
        if confidence_assessment and confidence_assessment.overconfidence_detected:
            recommendations.append("Implement confidence debiasing techniques")
        
        # Generate intervention alerts
        alerts = []
        for monitor in monitors:
            alerts.extend(monitor.alerts_triggered)
        
        for bias in bias_detections:
            if bias.severity == "high":
                alerts.append(f"High-severity {bias.bias_type.value} detected - immediate intervention needed")
        
        # Identify reasoning patterns
        patterns = [
            "Systematic approach preference",
            "High initial confidence with subsequent calibration",
            "Evidence-based reasoning style",
            "Active monitoring and self-correction"
        ]
        
        if bias_detections:
            patterns.append(f"Bias susceptibility: {', '.join([b.bias_type.value for b in bias_detections[:3]])}")
        
        return overall_quality, awareness_level, recommendations, alerts, patterns
    
    def _default_confidence_assessment(self) -> ConfidenceAssessment:
        """Create default confidence assessment when calibration is disabled"""
        return ConfidenceAssessment(
            stated_confidence=0.5,
            calibrated_confidence=0.5,
            calibration_method=ConfidenceCalibration.EVIDENCE_BASED,
            calibration_factors=["Default calibration"],
            overconfidence_detected=False,
            underconfidence_detected=False,
            confidence_interval={"lower": 0.4, "upper": 0.6},
            reliability_score=0.5
        )
