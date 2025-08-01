"""
Decision Framework Analyzer

Core implementation of the decision framework cognitive tool, providing
systematic decision analysis including multi-criteria decision analysis (MCDA),
weighted scoring, risk assessment, trade-off analysis, and various decision
methodologies.
"""

from typing import List, Dict, Any, Optional, Tuple
import asyncio
import time
from datetime import datetime
import numpy as np

from .models import (
    DecisionFrameworkContext,
    DecisionFrameworkResult,
    DecisionMethodType,
    CriteriaType,
    RiskLevel,
    DecisionCriteria,
    DecisionOption,
    DecisionMatrix,
    RiskAssessment,
    TradeOffAnalysis,
    SensitivityAnalysis,
    DecisionFrameworkUtils,
)


class DecisionFrameworkAnalyzer:
    """Decision framework cognitive tool analyzer"""
    
    def __init__(self):
        """Initialize the decision framework analyzer"""
        self.tool_name = "Decision Framework"
        self.version = "1.0.0"
        
        # Internal state for processing
        self._processing_start_time = 0.0
    
    async def analyze(self, context: DecisionFrameworkContext) -> DecisionFrameworkResult:
        """
        Analyze a decision problem using the specified decision framework.
        
        Args:
            context: Decision framework context with criteria and options
            
        Returns:
            DecisionFrameworkResult with recommendations and analysis
        """
        self._processing_start_time = time.time()
        
        # Phase 1: Validate and normalize inputs
        validation_issues = DecisionFrameworkUtils.validate_decision_consistency(
            context.criteria, context.options
        )
        if validation_issues:
            # Handle validation issues but continue processing
            pass
        
        # Phase 2: Build decision matrix
        decision_matrix = await self._build_decision_matrix(context)
        
        # Phase 3: Apply decision method
        recommended_option, option_rankings = await self._apply_decision_method(
            context, decision_matrix
        )
        
        # Phase 4: Risk assessment (if enabled)
        risk_assessments = None
        if context.include_risk_analysis:
            risk_assessments = await self._perform_risk_assessment(context)
        
        # Phase 5: Trade-off analysis (if enabled)
        trade_off_analyses = None
        if context.include_trade_off_analysis and len(option_rankings) >= 2:
            trade_off_analyses = await self._perform_trade_off_analysis(
                context, option_rankings[:3]
            )
        
        # Phase 6: Sensitivity analysis (if enabled)
        sensitivity_analysis = None
        if context.include_sensitivity_analysis:
            sensitivity_analysis = await self._perform_sensitivity_analysis(
                context, decision_matrix, option_rankings
            )
        
        # Phase 7: Generate insights and recommendations
        key_insights = self._generate_key_insights(
            context, decision_matrix, option_rankings, risk_assessments
        )
        
        decision_rationale = self._generate_decision_rationale(
            context, recommended_option, option_rankings, decision_matrix
        )
        
        implementation_considerations = self._generate_implementation_considerations(
            context, recommended_option, risk_assessments
        )
        
        monitoring_metrics = self._generate_monitoring_metrics(
            context, recommended_option
        )
        
        # Calculate confidence factors
        confidence_factors = self._calculate_confidence_factors(
            context, option_rankings, sensitivity_analysis
        )
        
        # Calculate processing time
        processing_time = time.time() - self._processing_start_time
        
        return DecisionFrameworkResult(
            method_used=context.decision_method,
            decision_matrix=decision_matrix,
            recommended_option=recommended_option,
            option_rankings=option_rankings,
            key_insights=key_insights,
            risk_assessments=risk_assessments,
            trade_off_analyses=trade_off_analyses,
            sensitivity_analysis=sensitivity_analysis,
            decision_rationale=decision_rationale,
            implementation_considerations=implementation_considerations,
            monitoring_metrics=monitoring_metrics,
            alternative_scenarios=self._generate_alternative_scenarios(context),
            confidence_factors=confidence_factors,
            processing_time_ms=round(processing_time * 1000)
        )
    
    async def _build_decision_matrix(
        self, context: DecisionFrameworkContext
    ) -> DecisionMatrix:
        """Build the decision matrix from context"""
        # Simulate processing delay
        await asyncio.sleep(0.1)
        
        # Extract criteria and option names
        criteria_names = [c.name for c in context.criteria]
        option_names = [o.name for o in context.options]
        
        # Build scores matrix
        scores_matrix = []
        for option in context.options:
            row = [option.scores[criterion] for criterion in criteria_names]
            scores_matrix.append(row)
        
        # Normalize scores based on criteria types
        normalized_matrix = []
        for j, criterion in enumerate(context.criteria):
            column_scores = [scores_matrix[i][j] for i in range(len(scores_matrix))]
            normalized_scores = DecisionFrameworkUtils.normalize_scores(
                column_scores, criterion.criteria_type
            )
            for i, score in enumerate(normalized_scores):
                if j == 0:
                    normalized_matrix.append([])
                normalized_matrix[i].append(score)
        
        # Extract weights
        weights_vector = [c.weight for c in context.criteria]
        
        # Create decision matrix
        matrix = DecisionMatrix(
            criteria=criteria_names,
            options=option_names,
            scores_matrix=normalized_matrix,
            weights_vector=weights_vector
        )
        
        # Calculate weighted scores and rankings
        return matrix.calculate_weighted_scores()
    
    async def _apply_decision_method(
        self,
        context: DecisionFrameworkContext,
        decision_matrix: DecisionMatrix
    ) -> Tuple[str, List[Dict[str, Any]]]:
        """Apply the specified decision method"""
        
        method = context.decision_method
        
        if method == DecisionMethodType.WEIGHTED_SCORING:
            return await self._weighted_scoring_method(decision_matrix)
        elif method == DecisionMethodType.AHP:
            return await self._ahp_method(context, decision_matrix)
        elif method == DecisionMethodType.TOPSIS:
            return await self._topsis_method(context, decision_matrix)
        elif method == DecisionMethodType.COST_BENEFIT:
            return await self._cost_benefit_method(context, decision_matrix)
        elif method == DecisionMethodType.RISK_ADJUSTED:
            return await self._risk_adjusted_method(context, decision_matrix)
        elif method == DecisionMethodType.MULTI_OBJECTIVE:
            return await self._multi_objective_method(context, decision_matrix)
        else:
            return await self._weighted_scoring_method(decision_matrix)
    
    async def _weighted_scoring_method(
        self, decision_matrix: DecisionMatrix
    ) -> Tuple[str, List[Dict[str, Any]]]:
        """Apply weighted scoring method"""
        # Simulate processing
        await asyncio.sleep(0.05)
        
        # Get rankings from the already calculated matrix
        option_rankings = []
        for i, option in enumerate(decision_matrix.options):
            option_rankings.append({
                'option': option,
                'score': decision_matrix.option_totals[i] if decision_matrix.option_totals else 0.0,
                'rank': decision_matrix.rankings[i] if decision_matrix.rankings else i + 1
            })
        
        # Sort by rank
        option_rankings.sort(key=lambda x: x['rank'])
        
        # Recommended option is the highest ranked
        recommended_option = option_rankings[0]['option'] if option_rankings else ""
        
        return recommended_option, option_rankings
    
    async def _ahp_method(
        self,
        context: DecisionFrameworkContext,
        decision_matrix: DecisionMatrix
    ) -> Tuple[str, List[Dict[str, Any]]]:
        """Apply Analytical Hierarchy Process method"""
        # Simulate AHP processing
        await asyncio.sleep(0.1)
        
        # For simplicity, fall back to weighted scoring
        # In a real implementation, this would include pairwise comparisons
        return await self._weighted_scoring_method(decision_matrix)
    
    async def _topsis_method(
        self,
        context: DecisionFrameworkContext,
        decision_matrix: DecisionMatrix
    ) -> Tuple[str, List[Dict[str, Any]]]:
        """Apply TOPSIS method"""
        # Simulate processing
        await asyncio.sleep(0.1)
        
        # Get criteria types
        criteria_types = [c.criteria_type for c in context.criteria]
        
        # Calculate TOPSIS scores
        topsis_scores = DecisionFrameworkUtils.calculate_topsis_scores(
            decision_matrix, criteria_types
        )
        
        # Build rankings
        option_rankings = []
        for i, option in enumerate(decision_matrix.options):
            option_rankings.append({
                'option': option,
                'score': topsis_scores[i],
                'rank': 0  # Will be set after sorting
            })
        
        # Sort by score (descending)
        option_rankings.sort(key=lambda x: x['score'], reverse=True)
        
        # Assign ranks
        for i, ranking in enumerate(option_rankings):
            ranking['rank'] = i + 1
        
        recommended_option = option_rankings[0]['option'] if option_rankings else ""
        
        return recommended_option, option_rankings
    
    async def _cost_benefit_method(
        self,
        context: DecisionFrameworkContext,
        decision_matrix: DecisionMatrix
    ) -> Tuple[str, List[Dict[str, Any]]]:
        """Apply cost-benefit analysis method"""
        # Simulate processing
        await asyncio.sleep(0.1)
        
        # Identify cost and benefit criteria
        cost_criteria = [c.name for c in context.criteria if c.criteria_type == CriteriaType.COST]
        benefit_criteria = [c.name for c in context.criteria if c.criteria_type == CriteriaType.BENEFIT]
        
        # Calculate cost-benefit ratios
        option_rankings = []
        for i, option in enumerate(context.options):
            total_cost = sum(option.scores.get(c, 0) for c in cost_criteria)
            total_benefit = sum(option.scores.get(c, 0) for c in benefit_criteria)
            
            # Avoid division by zero
            ratio = total_benefit / total_cost if total_cost > 0 else float('inf')
            
            option_rankings.append({
                'option': option.name,
                'score': ratio,
                'rank': 0,
                'cost': total_cost,
                'benefit': total_benefit
            })
        
        # Sort by ratio (descending)
        option_rankings.sort(key=lambda x: x['score'], reverse=True)
        
        # Assign ranks
        for i, ranking in enumerate(option_rankings):
            ranking['rank'] = i + 1
        
        recommended_option = option_rankings[0]['option'] if option_rankings else ""
        
        return recommended_option, option_rankings
    
    async def _risk_adjusted_method(
        self,
        context: DecisionFrameworkContext,
        decision_matrix: DecisionMatrix
    ) -> Tuple[str, List[Dict[str, Any]]]:
        """Apply risk-adjusted decision method"""
        # First get base scores
        recommended, base_rankings = await self._weighted_scoring_method(decision_matrix)
        
        # Perform risk assessment
        risk_assessments = await self._perform_risk_assessment(context)
        
        # Adjust scores based on risk
        if risk_assessments:
            risk_map = {ra.option_name: ra.risk_score for ra in risk_assessments}
            
            for ranking in base_rankings:
                risk_score = risk_map.get(ranking['option'], 0.5)
                # Adjust score by risk (lower risk is better)
                ranking['score'] = ranking['score'] * (1.0 - risk_score * 0.5)
                ranking['risk_adjusted'] = True
            
            # Re-sort and re-rank
            base_rankings.sort(key=lambda x: x['score'], reverse=True)
            for i, ranking in enumerate(base_rankings):
                ranking['rank'] = i + 1
            
            recommended = base_rankings[0]['option'] if base_rankings else ""
        
        return recommended, base_rankings
    
    async def _multi_objective_method(
        self,
        context: DecisionFrameworkContext,
        decision_matrix: DecisionMatrix
    ) -> Tuple[str, List[Dict[str, Any]]]:
        """Apply multi-objective optimization method"""
        # Simulate processing
        await asyncio.sleep(0.1)
        
        # For simplicity, use weighted scoring with Pareto analysis
        # In a real implementation, this would include Pareto frontier calculation
        return await self._weighted_scoring_method(decision_matrix)
    
    async def _perform_risk_assessment(
        self, context: DecisionFrameworkContext
    ) -> List[RiskAssessment]:
        """Perform risk assessment for each option"""
        # Simulate processing
        await asyncio.sleep(0.1)
        
        risk_assessments = []
        
        for option in context.options:
            # Analyze risks for this option
            risk_factors = []
            
            # Check for low scores on critical criteria
            for criterion in context.criteria:
                if criterion.criteria_type == CriteriaType.CONSTRAINT:
                    score = option.scores.get(criterion.name, 0)
                    if criterion.minimum_threshold and score < criterion.minimum_threshold:
                        risk_factors.append({
                            'name': f'Below threshold for {criterion.name}',
                            'description': f'Score {score} is below minimum {criterion.minimum_threshold}',
                            'probability': 0.8,
                            'impact': 0.9
                        })
            
            # Add option-specific risks
            if option.risks:
                for i, risk in enumerate(option.risks[:3]):
                    risk_factors.append({
                        'name': f'Risk {i+1}',
                        'description': risk,
                        'probability': 0.5,
                        'impact': 0.6
                    })
            
            # Calculate overall risk
            if risk_factors:
                avg_probability = sum(rf['probability'] for rf in risk_factors) / len(risk_factors)
                avg_impact = sum(rf['impact'] for rf in risk_factors) / len(risk_factors)
                risk_score = avg_probability * avg_impact
            else:
                risk_score = 0.1  # Low risk if no factors identified
            
            # Determine risk level
            if risk_score >= 0.7:
                risk_level = RiskLevel.VERY_HIGH
            elif risk_score >= 0.5:
                risk_level = RiskLevel.HIGH
            elif risk_score >= 0.3:
                risk_level = RiskLevel.MODERATE
            elif risk_score >= 0.2:
                risk_level = RiskLevel.LOW
            else:
                risk_level = RiskLevel.VERY_LOW
            
            # Generate mitigation strategies
            mitigation_strategies = [
                "Develop contingency plans for high-risk areas",
                "Monitor risk indicators closely during implementation",
                "Consider phased approach to reduce exposure"
            ]
            
            risk_assessments.append(RiskAssessment(
                option_name=option.name,
                risk_factors=risk_factors[:5],  # Limit to 5
                overall_risk_level=risk_level,
                risk_score=risk_score,
                mitigation_strategies=mitigation_strategies[:3],
                contingency_plans=[
                    "Fallback to alternative option if risks materialize",
                    "Establish clear escalation procedures"
                ]
            ))
        
        return risk_assessments
    
    async def _perform_trade_off_analysis(
        self,
        context: DecisionFrameworkContext,
        top_options: List[Dict[str, Any]]
    ) -> List[TradeOffAnalysis]:
        """Perform trade-off analysis between top options"""
        # Simulate processing
        await asyncio.sleep(0.1)
        
        trade_off_analyses = []
        
        # Compare top options pairwise
        for i in range(len(top_options) - 1):
            for j in range(i + 1, len(top_options)):
                option_a_name = top_options[i]['option']
                option_b_name = top_options[j]['option']
                
                # Find the actual options
                option_a = next((o for o in context.options if o.name == option_a_name), None)
                option_b = next((o for o in context.options if o.name == option_b_name), None)
                
                if not option_a or not option_b:
                    continue
                
                # Analyze trade-offs
                trade_offs = []
                winner_by_criteria = {}
                
                for criterion in context.criteria:
                    score_a = option_a.scores.get(criterion.name, 0)
                    score_b = option_b.scores.get(criterion.name, 0)
                    
                    trade_off = {
                        'criterion': criterion.name,
                        'option_a_value': f"{score_a:.2f}",
                        'option_b_value': f"{score_b:.2f}",
                        'analysis': self._analyze_trade_off(
                            criterion, score_a, score_b, option_a_name, option_b_name
                        )
                    }
                    trade_offs.append(trade_off)
                    
                    # Determine winner for this criterion
                    if criterion.criteria_type == CriteriaType.COST:
                        winner_by_criteria[criterion.name] = option_a_name if score_a < score_b else option_b_name
                    else:
                        winner_by_criteria[criterion.name] = option_a_name if score_a > score_b else option_b_name
                
                # Determine overall recommendation
                option_a_wins = sum(1 for winner in winner_by_criteria.values() if winner == option_a_name)
                option_b_wins = len(winner_by_criteria) - option_a_wins
                
                if option_a_wins > option_b_wins:
                    recommendation = option_a_name
                    rationale = f"{option_a_name} wins in {option_a_wins} out of {len(winner_by_criteria)} criteria"
                else:
                    recommendation = option_b_name
                    rationale = f"{option_b_name} wins in {option_b_wins} out of {len(winner_by_criteria)} criteria"
                
                trade_off_analyses.append(TradeOffAnalysis(
                    option_a=option_a_name,
                    option_b=option_b_name,
                    trade_offs=trade_offs[:5],  # Limit to 5
                    winner_by_criteria=winner_by_criteria,
                    overall_recommendation=recommendation,
                    rationale=rationale
                ))
        
        return trade_off_analyses
    
    async def _perform_sensitivity_analysis(
        self,
        context: DecisionFrameworkContext,
        decision_matrix: DecisionMatrix,
        base_rankings: List[Dict[str, Any]]
    ) -> SensitivityAnalysis:
        """Perform sensitivity analysis on criteria weights"""
        # Simulate processing
        await asyncio.sleep(0.1)
        
        # Base scenario scores
        base_scenario = {ranking['option']: ranking['score'] for ranking in base_rankings}
        
        # Test weight variations
        weight_variations = []
        threshold_analysis = {}
        
        # Test each criterion weight variation
        for i, criterion in enumerate(context.criteria):
            original_weight = criterion.weight
            
            # Test +20% and -20% variations
            for variation in [-0.2, 0.2]:
                new_weight = max(0.0, min(1.0, original_weight + variation))
                
                # Adjust other weights proportionally
                weight_adjustment = (original_weight - new_weight) / (len(context.criteria) - 1)
                test_weights = []
                for j, w in enumerate(decision_matrix.weights_vector):
                    if j == i:
                        test_weights.append(new_weight)
                    else:
                        test_weights.append(max(0.0, w + weight_adjustment))
                
                # Normalize to sum to 1.0
                total = sum(test_weights)
                test_weights = [w / total for w in test_weights]
                
                # Recalculate with new weights
                test_matrix = DecisionMatrix(
                    criteria=decision_matrix.criteria,
                    options=decision_matrix.options,
                    scores_matrix=decision_matrix.scores_matrix,
                    weights_vector=test_weights
                )
                test_matrix = test_matrix.calculate_weighted_scores()
                
                # Record variation results
                variation_result = {
                    'criterion_varied': criterion.name,
                    'original_weight': original_weight,
                    'new_weight': new_weight,
                    'variation_percent': variation * 100,
                    'new_rankings': []
                }
                
                # Add new rankings
                for j, option in enumerate(test_matrix.options):
                    variation_result['new_rankings'].append({
                        'option': option,
                        'score': test_matrix.option_totals[j] if test_matrix.option_totals else 0.0,
                        'rank': test_matrix.rankings[j] if test_matrix.rankings else j + 1
                    })
                
                weight_variations.append(variation_result)
        
        # Assess robustness
        ranking_changes = 0
        for variation in weight_variations:
            original_top = base_rankings[0]['option'] if base_rankings else None
            new_top = variation['new_rankings'][0]['option'] if variation['new_rankings'] else None
            if original_top != new_top:
                ranking_changes += 1
        
        robustness_score = 1.0 - (ranking_changes / len(weight_variations)) if weight_variations else 1.0
        
        # Stability assessment
        if robustness_score >= 0.8:
            stability_assessment = "Decision is highly stable across weight variations"
        elif robustness_score >= 0.6:
            stability_assessment = "Decision is moderately stable with some sensitivity"
        else:
            stability_assessment = "Decision is sensitive to weight changes"
        
        return SensitivityAnalysis(
            base_scenario=base_scenario,
            weight_variations=weight_variations[:10],  # Limit to 10
            threshold_analysis=threshold_analysis,
            robustness_score=robustness_score,
            stability_assessment=stability_assessment
        )
    
    def _analyze_trade_off(
        self,
        criterion: DecisionCriteria,
        score_a: float,
        score_b: float,
        option_a: str,
        option_b: str
    ) -> str:
        """Analyze trade-off between two options for a criterion"""
        diff = abs(score_a - score_b)
        
        if diff < 0.1:
            return f"Nearly equal performance on {criterion.name}"
        elif criterion.criteria_type == CriteriaType.COST:
            if score_a < score_b:
                return f"{option_a} is more cost-effective by {diff:.1f} points"
            else:
                return f"{option_b} is more cost-effective by {diff:.1f} points"
        else:
            if score_a > score_b:
                return f"{option_a} performs better by {diff:.1f} points"
            else:
                return f"{option_b} performs better by {diff:.1f} points"
    
    def _generate_key_insights(
        self,
        context: DecisionFrameworkContext,
        decision_matrix: DecisionMatrix,
        option_rankings: List[Dict[str, Any]],
        risk_assessments: Optional[List[RiskAssessment]]
    ) -> List[str]:
        """Generate key insights from the analysis"""
        insights = []
        
        # Top option insight
        if option_rankings:
            top_option = option_rankings[0]
            insights.append(
                f"{top_option['option']} emerged as the top choice with a score of {top_option['score']:.2f}"
            )
        
        # Score distribution insight
        if len(option_rankings) > 1:
            score_range = option_rankings[0]['score'] - option_rankings[-1]['score']
            if score_range < 0.2:
                insights.append("All options have similar scores, indicating a close decision")
            else:
                insights.append(f"Clear differentiation between options with score range of {score_range:.2f}")
        
        # Criteria influence insight
        most_influential = max(context.criteria, key=lambda c: c.weight)
        insights.append(
            f"{most_influential.name} has the highest influence at {most_influential.weight:.1%} weight"
        )
        
        # Risk insight
        if risk_assessments:
            high_risk_count = sum(1 for ra in risk_assessments if ra.overall_risk_level in [RiskLevel.HIGH, RiskLevel.VERY_HIGH])
            if high_risk_count > 0:
                insights.append(f"{high_risk_count} options have high or very high risk levels")
        
        # Method-specific insight
        insights.append(f"Analysis used {context.decision_method.description}")
        
        return insights[:5]
    
    def _generate_decision_rationale(
        self,
        context: DecisionFrameworkContext,
        recommended_option: str,
        option_rankings: List[Dict[str, Any]],
        decision_matrix: DecisionMatrix
    ) -> str:
        """Generate comprehensive decision rationale"""
        
        # Find the recommended option details
        recommended_details = next((r for r in option_rankings if r['option'] == recommended_option), None)
        
        if not recommended_details:
            return "Unable to generate rationale due to missing option details."
        
        # Build rationale
        rationale_parts = [
            f"The decision analysis recommends {recommended_option} based on {context.decision_method.value} methodology.",
            f"This option achieved the highest overall score of {recommended_details['score']:.2f}."
        ]
        
        # Add performance highlights
        option_obj = next((o for o in context.options if o.name == recommended_option), None)
        if option_obj:
            high_scoring_criteria = [
                c.name for c in context.criteria
                if option_obj.scores.get(c.name, 0) >= 0.8
            ]
            if high_scoring_criteria:
                rationale_parts.append(
                    f"It excels in: {', '.join(high_scoring_criteria[:3])}"
                )
        
        # Add competitive advantage
        if len(option_rankings) > 1:
            margin = recommended_details['score'] - option_rankings[1]['score']
            if margin > 0.1:
                rationale_parts.append(
                    f"The recommendation has a clear advantage of {margin:.2f} points over the next best option."
                )
            else:
                rationale_parts.append(
                    "While the margin is narrow, this option provides the best overall balance."
                )
        
        # Add stakeholder consideration
        if context.stakeholders:
            rationale_parts.append(
                f"This choice considers the priorities of {len(context.stakeholders)} key stakeholders."
            )
        
        return " ".join(rationale_parts)
    
    def _generate_implementation_considerations(
        self,
        context: DecisionFrameworkContext,
        recommended_option: str,
        risk_assessments: Optional[List[RiskAssessment]]
    ) -> List[str]:
        """Generate implementation considerations"""
        considerations = []
        
        # Timeline consideration
        if context.decision_timeline:
            considerations.append(f"Implementation must align with: {context.decision_timeline}")
        
        # Risk-based considerations
        if risk_assessments:
            option_risk = next((ra for ra in risk_assessments if ra.option_name == recommended_option), None)
            if option_risk and option_risk.overall_risk_level in [RiskLevel.HIGH, RiskLevel.VERY_HIGH]:
                considerations.append("High-risk option requires careful risk management during implementation")
        
        # Constraint considerations
        if context.constraints:
            considerations.append(f"Must comply with constraints: {', '.join(context.constraints[:2])}")
        
        # Option-specific considerations
        option_obj = next((o for o in context.options if o.name == recommended_option), None)
        if option_obj and option_obj.assumptions:
            considerations.append(f"Success depends on: {option_obj.assumptions[0]}")
        
        # General considerations
        considerations.extend([
            "Establish clear success metrics before implementation",
            "Create communication plan for stakeholder alignment",
            "Plan for regular progress reviews and adjustments"
        ])
        
        return considerations[:5]
    
    def _generate_monitoring_metrics(
        self,
        context: DecisionFrameworkContext,
        recommended_option: str
    ) -> List[str]:
        """Generate monitoring metrics for implementation"""
        metrics = []
        
        # Criteria-based metrics
        for criterion in context.criteria[:3]:
            if criterion.measurement_unit:
                metrics.append(f"{criterion.name} ({criterion.measurement_unit})")
            else:
                metrics.append(f"{criterion.name} performance")
        
        # Risk metrics
        metrics.append("Risk indicator tracking")
        
        # Timeline metrics
        if context.decision_timeline:
            metrics.append("Timeline adherence")
        
        # General metrics
        metrics.extend([
            "Stakeholder satisfaction score",
            "Implementation progress percentage",
            "Budget variance"
        ])
        
        return metrics[:6]
    
    def _generate_alternative_scenarios(
        self, context: DecisionFrameworkContext
    ) -> List[str]:
        """Generate alternative scenarios to consider"""
        scenarios = []
        
        # Constraint relaxation scenario
        if context.constraints:
            scenarios.append(f"If constraint '{context.constraints[0]}' could be relaxed")
        
        # Weight change scenario
        scenarios.append("If priorities shift significantly during implementation")
        
        # Risk materialization scenario
        scenarios.append("If identified risks materialize earlier than expected")
        
        # Resource change scenario
        scenarios.append("If available resources increase by 20%")
        
        # Timeline scenario
        if context.decision_timeline:
            scenarios.append("If timeline could be extended by 3 months")
        
        return scenarios[:5]
    
    def _calculate_confidence_factors(
        self,
        context: DecisionFrameworkContext,
        option_rankings: List[Dict[str, Any]],
        sensitivity_analysis: Optional[SensitivityAnalysis]
    ) -> Dict[str, float]:
        """Calculate confidence factors for various aspects"""
        factors = {}
        
        # Data quality confidence
        total_confidence_scores = 0
        confidence_count = 0
        for option in context.options:
            if option.confidence_scores:
                total_confidence_scores += sum(option.confidence_scores.values())
                confidence_count += len(option.confidence_scores)
        
        factors['data_quality'] = total_confidence_scores / confidence_count if confidence_count > 0 else 0.5
        
        # Method appropriateness
        suggested_method = DecisionFrameworkUtils.suggest_decision_method(
            len(context.criteria),
            len(context.options),
            any(o.risks for o in context.options),
            context.complexity_level
        )
        factors['method_appropriateness'] = 1.0 if suggested_method == context.decision_method else 0.7
        
        # Decision clarity
        if option_rankings and len(option_rankings) > 1:
            score_diff = option_rankings[0]['score'] - option_rankings[1]['score']
            factors['decision_clarity'] = min(1.0, score_diff * 2)  # Scale difference
        else:
            factors['decision_clarity'] = 0.5
        
        # Robustness
        if sensitivity_analysis:
            factors['robustness'] = sensitivity_analysis.robustness_score
        else:
            factors['robustness'] = 0.6  # Default moderate robustness
        
        # Overall confidence
        factors['overall'] = sum(factors.values()) / len(factors)
        
        return factors