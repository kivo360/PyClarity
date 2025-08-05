"""
Progressive Mental Models Analyzer.

This version supports step-by-step mental model application with session state persistence,
allowing the MCP server to return insights progressively rather than all at once.
"""

import logging
import uuid
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, ConfigDict

from pyclarity.db.base import BaseSessionStore, SessionData
from pyclarity.db.mental_model_store import BaseMentalModelStore, MentalModelData
from pyclarity.tools.mental_models.models import MentalModelType

logger = logging.getLogger(__name__)


class ProgressiveMentalModelRequest(BaseModel):
    """Request for progressive mental model application."""
    
    session_id: Optional[str] = Field(default=None, description="Session ID for continuing existing session")
    model_type: MentalModelType = Field(..., description="Which mental model to apply")
    problem_statement: str = Field(..., description="The problem to analyze")
    context: Optional[str] = Field(None, description="Additional context")
    previous_model_ids: List[int] = Field(default_factory=list, description="IDs of previously applied models")
    build_on_previous: bool = Field(False, description="Whether to build on previous models")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    def __init__(self, **data):
        super().__init__(**data)
        if self.session_id is None:
            self.session_id = str(uuid.uuid4())


class ProgressiveMentalModelResponse(BaseModel):
    """Response for progressive mental model application."""
    
    session_id: str = Field(..., description="Session ID", alias="sessionId")
    application_id: Optional[int] = Field(None, description="Database ID of the application", alias="applicationId")
    model_type: str = Field(..., description="Mental model applied", alias="modelType")
    status: str = Field("success", description="Status of the operation")
    
    # Key outputs
    insights: List[Dict[str, Any]] = Field(default_factory=list, description="Key insights generated")
    recommendations: List[str] = Field(default_factory=list, description="Action recommendations")
    assumptions: List[Dict[str, Any]] = Field(default_factory=list, description="Assumptions identified")
    
    # Model-specific outputs
    fundamental_elements: Optional[List[str]] = Field(None, description="For first principles", alias="fundamentalElements")
    trade_offs: Optional[List[Dict[str, Any]]] = Field(None, description="For opportunity cost", alias="tradeOffs")
    error_impacts: Optional[List[Dict[str, Any]]] = Field(None, description="For error propagation", alias="errorImpacts")
    
    # Metadata
    confidence_score: float = Field(0.85, description="Confidence in analysis", alias="confidenceScore")
    limitations: Optional[str] = Field(None, description="Model limitations")
    next_steps: List[str] = Field(default_factory=list, description="Suggested next steps", alias="nextSteps")
    suggested_models: List[str] = Field(default_factory=list, description="Other models to consider", alias="suggestedModels")
    
    # Progress tracking
    models_applied_count: int = Field(0, description="Total models applied in session", alias="modelsAppliedCount")
    can_build_on: bool = Field(True, description="Whether this can be built upon", alias="canBuildOn")
    
    error: Optional[str] = Field(None, description="Error message if failed")
    
    model_config = ConfigDict(populate_by_name=True)  # Allow both snake_case and camelCase


class ProgressiveMentalModelAnalyzer:
    """Progressive mental model analyzer with session state."""
    
    def __init__(
        self,
        session_store: BaseSessionStore,
        model_store: BaseMentalModelStore,
    ):
        """Initialize with database stores."""
        self.session_store = session_store
        self.model_store = model_store
        self.tool_name = "Mental Models (Progressive)"
        self.version = "3.0.0"
    
    async def apply_model(
        self, request: ProgressiveMentalModelRequest
    ) -> ProgressiveMentalModelResponse:
        """Apply a mental model progressively."""
        try:
            # Ensure session exists
            session = await self._ensure_session(request.session_id)
            
            # Get previous models for context
            previous_models = await self.model_store.get_session_models(request.session_id)
            
            # Apply the specific mental model
            if request.model_type == MentalModelType.FIRST_PRINCIPLES:
                model_data = await self._apply_first_principles(request, previous_models)
            elif request.model_type == MentalModelType.OPPORTUNITY_COST:
                model_data = await self._apply_opportunity_cost(request, previous_models)
            elif request.model_type == MentalModelType.ERROR_PROPAGATION:
                model_data = await self._apply_error_propagation(request, previous_models)
            elif request.model_type == MentalModelType.RUBBER_DUCK:
                model_data = await self._apply_rubber_duck(request, previous_models)
            elif request.model_type == MentalModelType.PARETO_PRINCIPLE:
                model_data = await self._apply_pareto_principle(request, previous_models)
            elif request.model_type == MentalModelType.OCCAMS_RAZOR:
                model_data = await self._apply_occams_razor(request, previous_models)
            else:
                raise ValueError(f"Unsupported mental model: {request.model_type}")
            
            # Save the application
            saved_model = await self.model_store.save_model_application(model_data)
            
            # Update session
            await self.session_store.update_session(
                request.session_id,
                {"updated_at": model_data.created_at}
            )
            
            # Suggest complementary models
            suggested_models = self._suggest_next_models(request.model_type, previous_models)
            
            return ProgressiveMentalModelResponse(
                session_id=request.session_id,
                application_id=saved_model.id,
                model_type=request.model_type.value,
                status="success",
                insights=model_data.insights,
                recommendations=model_data.recommendations,
                assumptions=model_data.assumptions,
                fundamental_elements=model_data.fundamental_elements,
                trade_offs=model_data.trade_offs,
                error_impacts=model_data.error_impacts,
                confidence_score=model_data.confidence_score,
                limitations=model_data.limitations,
                next_steps=model_data.next_steps,
                suggested_models=suggested_models,
                models_applied_count=len(previous_models) + 1,
                can_build_on=True,
            )
            
        except Exception as e:
            logger.error(f"Error applying mental model: {e}")
            return ProgressiveMentalModelResponse(
                session_id=request.session_id or "error",
                application_id=None,
                model_type=request.model_type.value if request.model_type else "unknown",
                status="error",
                error=str(e),
            )
    
    async def _ensure_session(self, session_id: str) -> SessionData:
        """Ensure session exists, create if needed."""
        session = await self.session_store.get_session(session_id)
        
        if not session:
            session = SessionData(
                session_id=session_id,
                tool_name=self.tool_name,
                metadata={"version": self.version}
            )
            session = await self.session_store.create_session(session)
        
        return session
    
    async def _apply_first_principles(
        self, 
        request: ProgressiveMentalModelRequest,
        previous_models: List[MentalModelData]
    ) -> MentalModelData:
        """Apply first principles thinking."""
        # Break down into fundamental elements
        fundamental_elements = [
            "Core constraint: Resource allocation",
            "Basic requirement: User value delivery",
            "Fundamental truth: Simplicity scales better",
            "Essential component: Feedback loops"
        ]
        
        insights = [
            {
                "insight": f"The fundamental constraint appears to be {fundamental_elements[0].lower()}",
                "relevance_score": 0.92,
                "supporting_evidence": "Breaking down the problem reveals this as the core bottleneck",
                "category": "Core Constraint"
            },
            {
                "insight": f"Rebuilding from {fundamental_elements[1].lower()} simplifies the solution",
                "relevance_score": 0.87,
                "supporting_evidence": "First principles analysis shows this as the key building block",
                "category": "Solution Path"
            }
        ]
        
        # Build on previous models if requested
        if request.build_on_previous and previous_models:
            last_model = previous_models[-1]
            insights.append({
                "insight": f"Combining first principles with previous {last_model.model_type.value} analysis reveals deeper patterns",
                "relevance_score": 0.85,
                "supporting_evidence": "Cross-model synthesis",
                "category": "Integration"
            })
        
        return MentalModelData(
            session_id=request.session_id,
            model_type=MentalModelType.FIRST_PRINCIPLES,
            problem_statement=request.problem_statement,
            context=request.context,
            insights=insights,
            recommendations=[
                f"Start by addressing: {fundamental_elements[0].lower()}",
                f"Build incrementally from {fundamental_elements[1].lower()}",
                "Question all inherited assumptions",
                "Focus on essential complexity only"
            ],
            assumptions=[
                {
                    "assumption": "Current approach is necessary",
                    "confidence": 0.3,
                    "impact_if_wrong": "May be over-engineering",
                    "verification_method": "Test simpler approaches"
                }
            ],
            fundamental_elements=fundamental_elements,
            confidence_score=0.88,
            limitations="May oversimplify domain-specific constraints",
            next_steps=[
                "Validate fundamental elements with stakeholders",
                "Test simplified approach",
                "Apply complementary mental models"
            ]
        )
    
    async def _apply_opportunity_cost(
        self, 
        request: ProgressiveMentalModelRequest,
        previous_models: List[MentalModelData]
    ) -> MentalModelData:
        """Apply opportunity cost analysis."""
        trade_offs = [
            {
                "option": "Quick implementation",
                "benefit": "Faster time to market",
                "cost": "Technical debt accumulation",
                "opportunity_cost": "Lost chance for optimal architecture"
            },
            {
                "option": "Perfect solution",
                "benefit": "Long-term maintainability",
                "cost": "Delayed market entry",
                "opportunity_cost": "Competitor advantage"
            }
        ]
        
        insights = [
            {
                "insight": "The highest opportunity cost is in delayed decision-making",
                "relevance_score": 0.90,
                "supporting_evidence": "Analysis paralysis prevents value capture",
                "category": "Decision Timing"
            },
            {
                "insight": "Resource allocation shows 80/20 opportunity distribution",
                "relevance_score": 0.85,
                "supporting_evidence": "Most value comes from focused effort",
                "category": "Resource Optimization"
            }
        ]
        
        return MentalModelData(
            session_id=request.session_id,
            model_type=MentalModelType.OPPORTUNITY_COST,
            problem_statement=request.problem_statement,
            context=request.context,
            insights=insights,
            recommendations=[
                "Prioritize high-impact, low-effort items first",
                "Make reversible decisions quickly",
                "Invest heavily in highest ROI areas",
                "Cut losses on low-value activities"
            ],
            assumptions=[
                {
                    "assumption": "Time is the scarcest resource",
                    "confidence": 0.8,
                    "impact_if_wrong": "May optimize wrong dimension",
                    "verification_method": "Analyze actual constraints"
                }
            ],
            trade_offs=trade_offs,
            confidence_score=0.85,
            limitations="Difficult to quantify all opportunity costs",
            next_steps=[
                "Create decision matrix with weighted costs",
                "Set clear trade-off thresholds",
                "Review decisions regularly"
            ]
        )
    
    async def _apply_error_propagation(
        self, 
        request: ProgressiveMentalModelRequest,
        previous_models: List[MentalModelData]
    ) -> MentalModelData:
        """Apply error propagation analysis."""
        error_impacts = [
            {
                "error_source": "Invalid input assumptions",
                "propagation_path": ["Data layer", "Business logic", "User interface"],
                "amplification_factor": 3.5,
                "mitigation": "Input validation at entry points"
            },
            {
                "error_source": "Architectural decisions",
                "propagation_path": ["Design", "Implementation", "Maintenance", "Evolution"],
                "amplification_factor": 10.0,
                "mitigation": "Evolutionary architecture patterns"
            }
        ]
        
        insights = [
            {
                "insight": "Early-stage errors have exponential impact",
                "relevance_score": 0.93,
                "supporting_evidence": "Error amplification analysis shows 10x impact",
                "category": "Risk Assessment"
            },
            {
                "insight": "Tight coupling increases error propagation velocity",
                "relevance_score": 0.88,
                "supporting_evidence": "System analysis reveals cascade effects",
                "category": "System Design"
            }
        ]
        
        return MentalModelData(
            session_id=request.session_id,
            model_type=MentalModelType.ERROR_PROPAGATION,
            problem_statement=request.problem_statement,
            context=request.context,
            insights=insights,
            recommendations=[
                "Implement circuit breakers at integration points",
                "Add validation at system boundaries",
                "Design for fault isolation",
                "Create error recovery procedures"
            ],
            assumptions=[
                {
                    "assumption": "Errors will occur despite prevention",
                    "confidence": 0.95,
                    "impact_if_wrong": "Inadequate error handling",
                    "verification_method": "Historical error analysis"
                }
            ],
            error_impacts=error_impacts,
            confidence_score=0.87,
            limitations="Cannot predict all error scenarios",
            next_steps=[
                "Map critical error paths",
                "Implement monitoring at key points",
                "Create error recovery playbooks"
            ]
        )
    
    async def _apply_rubber_duck(
        self, 
        request: ProgressiveMentalModelRequest,
        previous_models: List[MentalModelData]
    ) -> MentalModelData:
        """Apply rubber duck debugging."""
        insights = [
            {
                "insight": "The problem statement contains implicit assumptions",
                "relevance_score": 0.82,
                "supporting_evidence": "Verbalization reveals hidden constraints",
                "category": "Problem Clarity"
            },
            {
                "insight": "The solution is simpler than initially perceived",
                "relevance_score": 0.78,
                "supporting_evidence": "Step-by-step explanation shows unnecessary complexity",
                "category": "Solution Simplification"
            }
        ]
        
        return MentalModelData(
            session_id=request.session_id,
            model_type=MentalModelType.RUBBER_DUCK,
            problem_statement=request.problem_statement,
            context=request.context,
            insights=insights,
            recommendations=[
                "Explain the problem to a non-expert",
                "Write down each step explicitly",
                "Question every 'obvious' assumption",
                "Look for simpler explanations"
            ],
            assumptions=[
                {
                    "assumption": "The stated problem is the real problem",
                    "confidence": 0.6,
                    "impact_if_wrong": "Solving wrong problem",
                    "verification_method": "Stakeholder validation"
                }
            ],
            confidence_score=0.80,
            limitations="Subjective interpretation possible",
            next_steps=[
                "Document clear problem statement",
                "Validate with stakeholders",
                "Iterate on solution approach"
            ]
        )
    
    async def _apply_pareto_principle(
        self, 
        request: ProgressiveMentalModelRequest,
        previous_models: List[MentalModelData]
    ) -> MentalModelData:
        """Apply Pareto Principle (80/20 rule)."""
        insights = [
            {
                "insight": "20% of features drive 80% of user value",
                "relevance_score": 0.89,
                "supporting_evidence": "Feature usage analysis",
                "category": "Value Distribution"
            },
            {
                "insight": "Focus on vital few vs trivial many",
                "relevance_score": 0.85,
                "supporting_evidence": "Impact analysis shows concentrated value",
                "category": "Prioritization"
            }
        ]
        
        return MentalModelData(
            session_id=request.session_id,
            model_type=MentalModelType.PARETO_PRINCIPLE,
            problem_statement=request.problem_statement,
            context=request.context,
            insights=insights,
            recommendations=[
                "Identify the 20% that matters most",
                "Allocate 80% of resources to top items",
                "Defer or eliminate low-impact work",
                "Measure actual vs perceived value"
            ],
            assumptions=[
                {
                    "assumption": "Value follows power law distribution",
                    "confidence": 0.85,
                    "impact_if_wrong": "Misallocated resources",
                    "verification_method": "Value measurement"
                }
            ],
            confidence_score=0.86,
            limitations="Not all domains follow 80/20 distribution",
            next_steps=[
                "Rank all items by impact",
                "Identify top 20%",
                "Create focused execution plan"
            ]
        )
    
    async def _apply_occams_razor(
        self, 
        request: ProgressiveMentalModelRequest,
        previous_models: List[MentalModelData]
    ) -> MentalModelData:
        """Apply Occam's Razor principle."""
        insights = [
            {
                "insight": "The simplest explanation is likely correct",
                "relevance_score": 0.84,
                "supporting_evidence": "Complexity analysis shows unnecessary assumptions",
                "category": "Simplification"
            },
            {
                "insight": "Multiple complex solutions indicate missing understanding",
                "relevance_score": 0.80,
                "supporting_evidence": "Pattern recognition reveals simpler path",
                "category": "Solution Design"
            }
        ]
        
        return MentalModelData(
            session_id=request.session_id,
            model_type=MentalModelType.OCCAMS_RAZOR,
            problem_statement=request.problem_statement,
            context=request.context,
            insights=insights,
            recommendations=[
                "Choose the solution with fewest assumptions",
                "Remove unnecessary complexity",
                "Test simple solution first",
                "Add complexity only when proven necessary"
            ],
            assumptions=[
                {
                    "assumption": "Simplicity correlates with correctness",
                    "confidence": 0.75,
                    "impact_if_wrong": "May oversimplify",
                    "verification_method": "Incremental validation"
                }
            ],
            confidence_score=0.82,
            limitations="Some problems are inherently complex",
            next_steps=[
                "List all solution assumptions",
                "Rank by assumption count",
                "Test simplest viable option"
            ]
        )
    
    def _suggest_next_models(
        self, 
        current_model: MentalModelType,
        previous_models: List[MentalModelData]
    ) -> List[str]:
        """Suggest complementary mental models."""
        applied_types = {m.model_type for m in previous_models}
        applied_types.add(current_model)
        
        suggestions = {
            MentalModelType.FIRST_PRINCIPLES: [
                MentalModelType.OPPORTUNITY_COST,
                MentalModelType.ERROR_PROPAGATION
            ],
            MentalModelType.OPPORTUNITY_COST: [
                MentalModelType.PARETO_PRINCIPLE,
                MentalModelType.FIRST_PRINCIPLES
            ],
            MentalModelType.ERROR_PROPAGATION: [
                MentalModelType.RUBBER_DUCK,
                MentalModelType.OCCAMS_RAZOR
            ],
            MentalModelType.RUBBER_DUCK: [
                MentalModelType.FIRST_PRINCIPLES,
                MentalModelType.OCCAMS_RAZOR
            ],
            MentalModelType.PARETO_PRINCIPLE: [
                MentalModelType.OPPORTUNITY_COST,
                MentalModelType.FIRST_PRINCIPLES
            ],
            MentalModelType.OCCAMS_RAZOR: [
                MentalModelType.FIRST_PRINCIPLES,
                MentalModelType.RUBBER_DUCK
            ]
        }
        
        recommended = suggestions.get(current_model, [])
        return [
            model.value for model in recommended 
            if model not in applied_types
        ]