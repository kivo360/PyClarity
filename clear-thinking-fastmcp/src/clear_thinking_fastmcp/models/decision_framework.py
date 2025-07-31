# Clear Thinking FastMCP Server - Decision Framework

"""
Pydantic models for the Decision Framework cognitive tool.

This tool provides systematic decision analysis including:
- Multi-criteria decision analysis (MCDA)
- Weighted scoring and ranking systems
- Risk assessment and trade-off analysis
- Decision matrices and trees
- Analytical Hierarchy Process (AHP)
- TOPSIS and other decision methods

Agent: pydantic-model-engineer
Status: ACTIVE - Decision Framework implementation complete
"""

from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any, Optional, Literal, Union
from enum import Enum
import uuid

from .base import CognitiveInputBase, CognitiveOutputBase, CognitiveValidators, ComplexityLevel


class DecisionMethodType(str, Enum):
    """Available decision analysis methods"""
    
    WEIGHTED_SCORING = "weighted_scoring"
    AHP = "analytical_hierarchy_process"
    TOPSIS = "topsis"
    COST_BENEFIT = "cost_benefit"
    RISK_ADJUSTED = "risk_adjusted"
    MULTI_OBJECTIVE = "multi_objective"
    
    @property
    def description(self) -> str:
        """Get description of the decision method"""
        descriptions = {
            self.WEIGHTED_SCORING: "Simple weighted sum of criteria scores",
            self.AHP: "Analytical Hierarchy Process with pairwise comparisons",
            self.TOPSIS: "Technique for Order Preference by Similarity to Ideal Solution",
            self.COST_BENEFIT: "Cost-benefit analysis with quantified trade-offs",
            self.RISK_ADJUSTED: "Risk-adjusted decision analysis with uncertainty",
            self.MULTI_OBJECTIVE: "Multi-objective optimization with Pareto analysis"
        }
        return descriptions.get(self, "Unknown decision method")


class CriteriaType(str, Enum):
    """Types of decision criteria"""
    
    BENEFIT = "benefit"        # Higher values are better
    COST = "cost"             # Lower values are better
    CONSTRAINT = "constraint"  # Must meet minimum threshold
    PREFERENCE = "preference"  # Subjective preference ranking


class RiskLevel(str, Enum):
    """Risk assessment levels"""
    
    VERY_LOW = "very_low"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"
    
    @property
    def numeric_value(self) -> float:
        """Get numeric risk multiplier"""
        values = {
            self.VERY_LOW: 0.1,
            self.LOW: 0.3,
            self.MODERATE: 0.5,
            self.HIGH: 0.7,
            self.VERY_HIGH: 0.9
        }
        return values[self]


class DecisionCriteria(BaseModel):
    """Individual decision criterion with weight and type"""
    
    name: str = Field(
        ...,
        description="Name of the criterion",
        min_length=3,
        max_length=100,
        example="Implementation Cost"
    )
    
    description: Optional[str] = Field(
        None,
        description="Detailed description of the criterion",
        max_length=300,
        example="Total cost including development, testing, and deployment"
    )
    
    weight: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Relative weight/importance of this criterion (0-1)",
        example=0.25
    )
    
    criteria_type: CriteriaType = Field(
        CriteriaType.BENEFIT,
        description="Type of criterion (benefit, cost, constraint, preference)",
        example="cost"
    )
    
    measurement_unit: Optional[str] = Field(
        None,
        description="Unit of measurement for this criterion",
        max_length=50,
        example="USD"
    )
    
    minimum_threshold: Optional[float] = Field(
        None,
        description="Minimum acceptable value (for constraint criteria)",
        example=1000.0
    )
    
    maximum_threshold: Optional[float] = Field(
        None,
        description="Maximum acceptable value (for constraint criteria)",
        example=50000.0
    )
    
    @validator('name')
    def validate_name(cls, v):
        """Validate criterion name"""
        return CognitiveValidators.validate_string_not_empty(cls, v, "criterion name")
    
    @validator('weight')
    def validate_weight(cls, v):
        """Validate weight is reasonable"""
        return CognitiveValidators.validate_confidence_score(cls, v)


class DecisionOption(BaseModel):
    """Decision alternative with scores and metadata"""
    
    name: str = Field(
        ...,
        description="Name of the option",
        min_length=3,
        max_length=100,
        example="Cloud-based Solution"
    )
    
    description: Optional[str] = Field(
        None,
        description="Detailed description of the option",
        max_length=500,
        example="Migrate to AWS cloud infrastructure with auto-scaling capabilities"
    )
    
    scores: Dict[str, float] = Field(
        ...,
        description="Scores for each criterion (criterion_name -> score)",
        example={"cost": 0.7, "performance": 0.9, "reliability": 0.8}
    )
    
    raw_values: Optional[Dict[str, Union[float, str]]] = Field(
        None,
        description="Raw values before normalization",
        example={"cost": 25000, "performance": "high", "reliability": 0.99}
    )
    
    confidence_scores: Optional[Dict[str, float]] = Field(
        None,
        description="Confidence in each score (criterion_name -> confidence)",
        example={"cost": 0.9, "performance": 0.7, "reliability": 0.8}
    )
    
    risks: Optional[List[str]] = Field(
        None,
        description="Identified risks for this option",
        max_items=8,
        example=["Vendor lock-in", "Learning curve for team"]
    )
    
    assumptions: Optional[List[str]] = Field(
        None,
        description="Key assumptions for this option",
        max_items=6,
        example=["Team can learn new platform in 3 months", "AWS pricing remains stable"]
    )
    
    @validator('name')
    def validate_name(cls, v):
        """Validate option name"""
        return CognitiveValidators.validate_string_not_empty(cls, v, "option name")
    
    @validator('scores')
    def validate_scores(cls, v):
        """Validate scores are reasonable (supports both 0-1 and 0-10 scales)"""
        if not v:
            raise ValueError("Scores dictionary cannot be empty")
        
        for criterion, score in v.items():
            if not isinstance(score, (int, float)):
                raise ValueError(f"Score for '{criterion}' must be numeric")
            if not 0.0 <= score <= 10.0:
                raise ValueError(f"Score for '{criterion}' must be between 0.0 and 10.0")
        
        return v
    
    @validator('confidence_scores')
    def validate_confidence_scores(cls, v, values):
        """Validate confidence scores match criteria"""
        if v is not None:
            scores = values.get('scores', {})
            for criterion, confidence in v.items():
                if criterion not in scores:
                    raise ValueError(f"Confidence score for unknown criterion: {criterion}")
                if not 0.0 <= confidence <= 1.0:
                    raise ValueError(f"Confidence for '{criterion}' must be between 0.0 and 1.0")
        return v


class DecisionMatrix(BaseModel):
    """Decision matrix with normalized scores and calculations"""
    
    criteria: List[str] = Field(
        ...,
        description="List of criterion names in order",
        min_items=2,
        max_items=20
    )
    
    options: List[str] = Field(
        ...,
        description="List of option names in order",
        min_items=2,
        max_items=15
    )
    
    scores_matrix: List[List[float]] = Field(
        ...,
        description="Normalized scores matrix (options x criteria)",
        example=[[0.8, 0.6, 0.9], [0.7, 0.8, 0.7]]
    )
    
    weights_vector: List[float] = Field(
        ...,
        description="Weights for each criterion",
        example=[0.4, 0.3, 0.3]
    )
    
    weighted_scores: Optional[List[List[float]]] = Field(
        None,
        description="Weighted scores matrix (scores * weights)"
    )
    
    option_totals: Optional[List[float]] = Field(
        None,
        description="Total weighted scores for each option"
    )
    
    rankings: Optional[List[int]] = Field(
        None,
        description="Rankings of options (1 = best)"
    )
    
    @validator('scores_matrix')
    def validate_scores_matrix(cls, v, values):
        """Validate matrix dimensions and values"""
        if not v:
            raise ValueError("Scores matrix cannot be empty")
        
        criteria_count = len(values.get('criteria', []))
        options_count = len(values.get('options', []))
        
        if len(v) != options_count:
            raise ValueError(f"Matrix must have {options_count} rows (one per option)")
        
        for i, row in enumerate(v):
            if len(row) != criteria_count:
                raise ValueError(f"Row {i} must have {criteria_count} columns (one per criterion)")
            
            for j, score in enumerate(row):
                if not isinstance(score, (int, float)):
                    raise ValueError(f"Score at [{i}][{j}] must be numeric")
                if not 0.0 <= score <= 10.0:
                    raise ValueError(f"Score at [{i}][{j}] must be between 0.0 and 10.0")
        
        return v
    
    @validator('weights_vector')
    def validate_weights_vector(cls, v, values):
        """Validate weights sum to 1.0"""
        if not v:
            raise ValueError("Weights vector cannot be empty")
        
        criteria_count = len(values.get('criteria', []))
        if len(v) != criteria_count:
            raise ValueError(f"Weights vector must have {criteria_count} elements")
        
        for weight in v:
            if not isinstance(weight, (int, float)):
                raise ValueError("All weights must be numeric")
            if not 0.0 <= weight <= 1.0:
                raise ValueError("All weights must be between 0.0 and 1.0")
        
        total_weight = sum(v)
        if not 0.95 <= total_weight <= 1.05:  # Allow small rounding errors
            raise ValueError(f"Weights must sum to 1.0 (got {total_weight:.3f})")
        
        return v
    
    def calculate_weighted_scores(self) -> 'DecisionMatrix':
        """Calculate weighted scores and rankings"""
        # Calculate weighted scores
        weighted_scores = []
        for row in self.scores_matrix:
            weighted_row = [score * weight for score, weight in zip(row, self.weights_vector)]
            weighted_scores.append(weighted_row)
        
        # Calculate option totals
        option_totals = [sum(row) for row in weighted_scores]
        
        # Calculate rankings (1 = highest score)
        sorted_indices = sorted(range(len(option_totals)), 
                              key=lambda i: option_totals[i], reverse=True)
        rankings = [0] * len(option_totals)
        for rank, index in enumerate(sorted_indices, 1):
            rankings[index] = rank
        
        # Return updated instance
        return DecisionMatrix(
            criteria=self.criteria,
            options=self.options,
            scores_matrix=self.scores_matrix,
            weights_vector=self.weights_vector,
            weighted_scores=weighted_scores,
            option_totals=option_totals,
            rankings=rankings
        )


class RiskAssessment(BaseModel):
    """Risk evaluation for decision options"""
    
    option_name: str = Field(
        ...,
        description="Name of the option being assessed",
        example="Cloud Migration"
    )
    
    risk_factors: List[Dict[str, Any]] = Field(
        ...,
        description="List of risk factors with details",
        min_items=1,
        max_items=10
    )
    
    overall_risk_level: RiskLevel = Field(
        ...,
        description="Overall risk level for this option"
    )
    
    risk_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Quantified risk score (0 = no risk, 1 = maximum risk)"
    )
    
    mitigation_strategies: Optional[List[str]] = Field(
        None,
        description="Suggested risk mitigation strategies",
        max_items=8
    )
    
    contingency_plans: Optional[List[str]] = Field(
        None,
        description="Contingency plans for high-risk scenarios",
        max_items=5
    )
    
    @validator('risk_factors')
    def validate_risk_factors(cls, v):
        """Validate risk factors structure"""
        if not v:
            raise ValueError("At least one risk factor is required")
        
        required_keys = ['name', 'description', 'probability', 'impact']
        
        for i, factor in enumerate(v):
            if not isinstance(factor, dict):
                raise ValueError(f"Risk factor {i} must be a dictionary")
            
            missing_keys = [key for key in required_keys if key not in factor]
            if missing_keys:
                raise ValueError(f"Risk factor {i} missing keys: {missing_keys}")
            
            # Validate probability and impact are numeric and in range
            for key in ['probability', 'impact']:
                value = factor[key]
                if not isinstance(value, (int, float)):
                    raise ValueError(f"Risk factor {i} '{key}' must be numeric")
                if not 0.0 <= value <= 1.0:
                    raise ValueError(f"Risk factor {i} '{key}' must be between 0.0 and 1.0")
        
        return v


class TradeOffAnalysis(BaseModel):
    """Trade-off comparison between options"""
    
    option_a: str = Field(
        ...,
        description="Name of first option",
        example="On-premise Solution"
    )
    
    option_b: str = Field(
        ...,
        description="Name of second option",
        example="Cloud Solution"
    )
    
    trade_offs: List[Dict[str, str]] = Field(
        ...,
        description="List of trade-off comparisons",
        min_items=1,
        max_items=10
    )
    
    winner_by_criteria: Dict[str, str] = Field(
        ...,
        description="Which option wins for each criterion",
        example={"cost": "option_a", "scalability": "option_b"}
    )
    
    overall_recommendation: Optional[str] = Field(
        None,
        description="Overall recommendation based on trade-offs",
        example="option_b"
    )
    
    rationale: Optional[str] = Field(
        None,
        description="Explanation of the recommendation",
        max_length=500
    )
    
    @validator('trade_offs')
    def validate_trade_offs(cls, v):
        """Validate trade-offs structure"""
        if not v:
            raise ValueError("At least one trade-off is required")
        
        required_keys = ['criterion', 'option_a_value', 'option_b_value', 'analysis']
        
        for i, trade_off in enumerate(v):
            if not isinstance(trade_off, dict):
                raise ValueError(f"Trade-off {i} must be a dictionary")
            
            missing_keys = [key for key in required_keys if key not in trade_off]
            if missing_keys:
                raise ValueError(f"Trade-off {i} missing keys: {missing_keys}")
        
        return v


class SensitivityAnalysis(BaseModel):
    """Sensitivity analysis for decision robustness"""
    
    base_scenario: Dict[str, float] = Field(
        ...,
        description="Base case option scores",
        example={"option_a": 0.75, "option_b": 0.68}
    )
    
    weight_variations: List[Dict[str, Any]] = Field(
        ...,
        description="Results under different weight scenarios",
        min_items=1,
        max_items=20
    )
    
    threshold_analysis: Optional[Dict[str, float]] = Field(
        None,
        description="Weight thresholds where ranking changes"
    )
    
    robustness_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="How robust the decision is to weight changes"
    )
    
    stability_assessment: str = Field(
        ...,
        description="Assessment of decision stability",
        example="Decision is stable across reasonable weight variations"
    )


class DecisionFrameworkInput(CognitiveInputBase):
    """Input model for decision framework cognitive tool"""
    
    decision_method: DecisionMethodType = Field(
        DecisionMethodType.WEIGHTED_SCORING,
        description="Decision analysis method to use",
        example="weighted_scoring"
    )
    
    criteria: List[DecisionCriteria] = Field(
        ...,
        description="Decision criteria with weights",
        min_items=2,
        max_items=20
    )
    
    options: List[DecisionOption] = Field(
        ...,
        description="Decision options to evaluate",
        min_items=2,
        max_items=15
    )
    
    complexity_level: ComplexityLevel = Field(
        ComplexityLevel.MODERATE,
        description="Complexity level of analysis to perform"
    )
    
    include_risk_analysis: bool = Field(
        True,
        description="Whether to include risk assessment"
    )
    
    include_sensitivity_analysis: bool = Field(
        False,
        description="Whether to perform sensitivity analysis"
    )
    
    include_trade_off_analysis: bool = Field(
        True,
        description="Whether to include trade-off analysis"
    )
    
    decision_timeline: Optional[str] = Field(
        None,
        description="Timeline for making the decision",
        max_length=100,
        example="Must decide within 2 weeks"
    )
    
    stakeholders: Optional[List[str]] = Field(
        None,
        description="Key stakeholders in the decision",
        max_items=10,
        example=["Engineering Team", "Product Manager", "CTO"]
    )
    
    constraints: Optional[List[str]] = Field(
        None,
        description="Hard constraints or limitations",
        max_items=8,
        example=["Budget cannot exceed $50k", "Must be implemented by Q4"]
    )
    
    @validator('criteria')
    def validate_criteria_weights(cls, v):
        """Validate criteria weights sum to approximately 1.0"""
        if not v:
            raise ValueError("At least 2 criteria are required")
        
        total_weight = sum(criterion.weight for criterion in v)
        if not 0.95 <= total_weight <= 1.05:  # Allow small rounding errors
            raise ValueError(f"Criteria weights must sum to 1.0 (got {total_weight:.3f})")
        
        # Check for duplicate criterion names
        names = [criterion.name.lower() for criterion in v]
        if len(names) != len(set(names)):
            raise ValueError("Criterion names must be unique")
        
        return v
    
    @validator('options')
    def validate_options_completeness(cls, v, values):
        """Validate options have scores for all criteria"""
        if not v:
            raise ValueError("At least 2 options are required")
        
        criteria = values.get('criteria', [])
        criterion_names = {criterion.name for criterion in criteria}
        
        for i, option in enumerate(v):
            option_criteria = set(option.scores.keys())
            missing_criteria = criterion_names - option_criteria
            if missing_criteria:
                raise ValueError(f"Option '{option.name}' missing scores for: {missing_criteria}")
            
            extra_criteria = option_criteria - criterion_names
            if extra_criteria:
                raise ValueError(f"Option '{option.name}' has scores for unknown criteria: {extra_criteria}")
        
        # Check for duplicate option names
        names = [option.name.lower() for option in v]
        if len(names) != len(set(names)):
            raise ValueError("Option names must be unique")
        
        return v


class DecisionFrameworkOutput(CognitiveOutputBase):
    """Output model for decision framework cognitive tool"""
    
    method_used: DecisionMethodType = Field(
        ...,
        description="Decision method that was applied"
    )
    
    decision_matrix: DecisionMatrix = Field(
        ...,
        description="Complete decision matrix with calculations"
    )
    
    recommended_option: str = Field(
        ...,
        description="Name of the recommended option",
        example="Cloud-based Solution"
    )
    
    option_rankings: List[Dict[str, Any]] = Field(
        ...,
        description="Ranked list of options with scores",
        min_items=2
    )
    
    key_insights: List[str] = Field(
        ...,
        description="Key insights from the analysis",
        min_items=1,
        max_items=8
    )
    
    risk_assessments: Optional[List[RiskAssessment]] = Field(
        None,
        description="Risk assessments for each option"
    )
    
    trade_off_analyses: Optional[List[TradeOffAnalysis]] = Field(
        None,
        description="Trade-off analyses between top options"
    )
    
    sensitivity_analysis: Optional[SensitivityAnalysis] = Field(
        None,
        description="Sensitivity analysis results"
    )
    
    decision_rationale: str = Field(
        ...,
        description="Detailed rationale for the recommendation",
        min_length=100,
        max_length=1000
    )
    
    implementation_considerations: Optional[List[str]] = Field(
        None,
        description="Key considerations for implementing the decision",
        max_items=8
    )
    
    monitoring_metrics: Optional[List[str]] = Field(
        None,
        description="Metrics to monitor after implementation",
        max_items=6
    )
    
    alternative_scenarios: Optional[List[str]] = Field(
        None,
        description="Alternative scenarios to consider",
        max_items=5
    )
    
    confidence_factors: Optional[Dict[str, float]] = Field(
        None,
        description="Confidence scores for different aspects of the analysis"
    )
    
    @validator('option_rankings')
    def validate_option_rankings(cls, v):
        """Validate option rankings structure"""
        if not v:
            raise ValueError("Option rankings cannot be empty")
        
        required_keys = ['option', 'score', 'rank']
        
        for i, ranking in enumerate(v):
            if not isinstance(ranking, dict):
                raise ValueError(f"Ranking {i} must be a dictionary")
            
            missing_keys = [key for key in required_keys if key not in ranking]
            if missing_keys:
                raise ValueError(f"Ranking {i} missing keys: {missing_keys}")
            
            # Validate score is numeric and in range
            score = ranking.get('score')
            if not isinstance(score, (int, float)):
                raise ValueError(f"Ranking {i} score must be numeric")
            if not 0.0 <= score <= 10.0:
                raise ValueError(f"Ranking {i} score must be between 0.0 and 10.0")
            
            # Validate rank is positive integer
            rank = ranking.get('rank')
            if not isinstance(rank, int) or rank < 1:
                raise ValueError(f"Ranking {i} rank must be positive integer")
        
        # Sort by rank
        return sorted(v, key=lambda x: x['rank'])
    
    @validator('decision_rationale')
    def validate_decision_rationale(cls, v):
        """Validate rationale is comprehensive"""
        if not v or not v.strip():
            raise ValueError("Decision rationale cannot be empty")
        
        cleaned = ' '.join(v.split())
        
        if len(cleaned) < 100:
            raise ValueError("Decision rationale must be at least 100 characters")
        
        return cleaned
    
    def get_top_options(self, n: int = 3) -> List[Dict[str, Any]]:
        """Get top N options by ranking"""
        return self.option_rankings[:n]
    
    def get_option_score(self, option_name: str) -> Optional[float]:
        """Get score for a specific option"""
        for ranking in self.option_rankings:
            if ranking['option'] == option_name:
                return ranking['score']
        return None
    
    def get_decision_summary(self) -> Dict[str, Any]:
        """Get concise decision summary"""
        top_option = self.option_rankings[0] if self.option_rankings else None
        
        return {
            'recommended_option': self.recommended_option,
            'method_used': self.method_used.value,
            'confidence_score': self.confidence_score,
            'top_option_score': top_option['score'] if top_option else None,
            'key_insight': self.key_insights[0] if self.key_insights else None,
            'has_risk_analysis': bool(self.risk_assessments),
            'has_sensitivity_analysis': bool(self.sensitivity_analysis)
        }


# Utility functions for decision framework processing
class DecisionFrameworkUtils:
    """Utility functions for decision framework processing"""
    
    @staticmethod
    def normalize_scores(scores: List[float], criteria_type: CriteriaType) -> List[float]:
        """Normalize scores to 0-1 range based on criteria type"""
        if not scores:
            return scores
        
        min_score = min(scores)
        max_score = max(scores)
        
        if min_score == max_score:
            return [0.5] * len(scores)  # All equal
        
        if criteria_type == CriteriaType.COST:
            # For cost criteria, lower is better - invert the normalization
            return [(max_score - score) / (max_score - min_score) for score in scores]
        else:
            # For benefit criteria, higher is better
            return [(score - min_score) / (max_score - min_score) for score in scores]
    
    @staticmethod
    def calculate_topsis_scores(
        decision_matrix: DecisionMatrix,
        criteria_types: List[CriteriaType]
    ) -> List[float]:
        """Calculate TOPSIS scores for options"""
        scores_matrix = decision_matrix.scores_matrix
        weights = decision_matrix.weights_vector
        
        # Weighted normalized matrix
        weighted_matrix = []
        for row in scores_matrix:
            weighted_row = [score * weight for score, weight in zip(row, weights)]
            weighted_matrix.append(weighted_row)
        
        # Ideal and negative ideal solutions
        ideal_solution = []
        negative_ideal_solution = []
        
        for j in range(len(weights)):
            column_values = [weighted_matrix[i][j] for i in range(len(weighted_matrix))]
            
            if criteria_types[j] == CriteriaType.COST:
                ideal_solution.append(min(column_values))
                negative_ideal_solution.append(max(column_values))
            else:
                ideal_solution.append(max(column_values))
                negative_ideal_solution.append(min(column_values))
        
        # Calculate distances and TOPSIS scores
        topsis_scores = []
        for i in range(len(weighted_matrix)):
            # Distance to ideal solution
            dist_ideal = sum((weighted_matrix[i][j] - ideal_solution[j]) ** 2 
                           for j in range(len(weights))) ** 0.5
            
            # Distance to negative ideal solution
            dist_negative = sum((weighted_matrix[i][j] - negative_ideal_solution[j]) ** 2 
                              for j in range(len(weights))) ** 0.5
            
            # TOPSIS score
            if dist_ideal + dist_negative == 0:
                topsis_score = 0.5
            else:
                topsis_score = dist_negative / (dist_ideal + dist_negative)
            
            topsis_scores.append(topsis_score)
        
        return topsis_scores
    
    @staticmethod
    def validate_decision_consistency(
        criteria: List[DecisionCriteria],
        options: List[DecisionOption]
    ) -> List[str]:
        """Validate consistency of decision inputs"""
        issues = []
        
        # Check weight consistency
        total_weight = sum(criterion.weight for criterion in criteria)
        if not 0.95 <= total_weight <= 1.05:
            issues.append(f"Criteria weights sum to {total_weight:.3f}, should be 1.0")
        
        # Check score completeness
        criterion_names = {criterion.name for criterion in criteria}
        for option in options:
            option_criteria = set(option.scores.keys())
            missing = criterion_names - option_criteria
            if missing:
                issues.append(f"Option '{option.name}' missing scores for: {missing}")
        
        # Check for unrealistic confidence combinations
        for option in options:
            if option.confidence_scores:
                low_confidence_count = sum(1 for conf in option.confidence_scores.values() 
                                         if conf < 0.3)
                if low_confidence_count > len(option.confidence_scores) * 0.5:
                    issues.append(f"Option '{option.name}' has low confidence in >50% of scores")
        
        return issues
    
    @staticmethod
    def suggest_decision_method(
        criteria_count: int,
        options_count: int,
        has_uncertainty: bool,
        complexity_level: ComplexityLevel
    ) -> DecisionMethodType:
        """Suggest appropriate decision method based on problem characteristics"""
        
        if complexity_level == ComplexityLevel.SIMPLE and criteria_count <= 5:
            return DecisionMethodType.WEIGHTED_SCORING
        
        if has_uncertainty or any(keyword in str(criteria_count).lower() 
                                for keyword in ['risk', 'uncertain', 'volatile']):
            return DecisionMethodType.RISK_ADJUSTED
        
        if criteria_count > 8 or options_count > 10:
            return DecisionMethodType.TOPSIS
        
        if complexity_level == ComplexityLevel.COMPLEX:
            return DecisionMethodType.AHP
        
        return DecisionMethodType.WEIGHTED_SCORING


__all__ = [
    "DecisionMethodType",
    "CriteriaType", 
    "RiskLevel",
    "DecisionCriteria",
    "DecisionOption",
    "DecisionMatrix",
    "RiskAssessment",
    "TradeOffAnalysis",
    "SensitivityAnalysis",
    "DecisionFrameworkInput",
    "DecisionFrameworkOutput",
    "DecisionFrameworkUtils"
]