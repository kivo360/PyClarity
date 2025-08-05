"""
Product Discovery Pipeline using Cognitive Tools
==============================================

This module implements the ProductDiscoveryPipeline that orchestrates
cognitive tools for comprehensive product analysis and validation.

Pipeline Stages:
1. Persona Analysis - Extract insights from user personas
2. Pain Point Identification - Group and prioritize problems
3. Idea Generation - Create product concepts addressing pain points
4. Multi-Perspective Validation - Validate from different viewpoints
5. Market Analysis - Assess market opportunity and competition
6. Feature Validation - Validate features with personas
7. USP Generation - Create unique selling propositions
8. Model Optimization - Generate optimized product models

The pipeline uses the WorkflowEngine to coordinate cognitive tools
and produces structured outputs ready for BDD scenario generation.
"""

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from ..workflows.engine import WorkflowEngine
from ..workflows.models import ToolConfig, ToolType, WorkflowConfig, WorkflowStatus


class AnalysisStage(str, Enum):
    """Stages of the product discovery pipeline"""
    PERSONA_ANALYSIS = "persona_analysis"
    PAIN_POINT_EXTRACTION = "pain_point_extraction"
    IDEA_GENERATION = "idea_generation"
    MULTI_PERSPECTIVE_VALIDATION = "multi_perspective_validation"
    MARKET_ANALYSIS = "market_analysis"
    COMPETITIVE_INTELLIGENCE = "competitive_intelligence"
    FEATURE_VALIDATION = "feature_validation"
    USP_GENERATION = "usp_generation"
    MODEL_OPTIMIZATION = "model_optimization"


class PersonaInsight(BaseModel):
    """Extracted insights from a persona"""
    persona_id: str
    demographics: dict[str, Any] = Field(default_factory=dict)
    activities: list[str] = Field(default_factory=list)
    pain_points: list[str] = Field(default_factory=list)
    goals: list[str] = Field(default_factory=list)
    tech_comfort_level: float = Field(default=0.5, ge=0, le=1)
    decision_factors: list[str] = Field(default_factory=list)


class PainPointCluster(BaseModel):
    """Grouped pain points with affected personas"""
    cluster_id: str
    pain_points: list[str]
    affected_personas: list[str]
    severity_score: float = Field(ge=0, le=1)
    frequency_score: float = Field(ge=0, le=1)
    opportunity_size: str = "medium"


class ProductIdea(BaseModel):
    """Generated product idea"""
    idea_id: str
    title: str
    description: str
    problem_solved: str
    unique_value: str
    target_clusters: list[str] = Field(default_factory=list)
    feasibility_score: float = Field(ge=0, le=1)
    innovation_score: float = Field(ge=0, le=1)


class ValidationResult(BaseModel):
    """Multi-perspective validation result"""
    idea_id: str
    perspective_type: str  # primary, adjacent, contrarian
    feedback: str
    concerns: list[str] = Field(default_factory=list)
    opportunities: list[str] = Field(default_factory=list)
    validation_score: float = Field(ge=0, le=1)


class MarketAnalysis(BaseModel):
    """Market analysis results"""
    idea_id: str
    market_size: str
    growth_rate: str
    competitive_intensity: str
    entry_barriers: list[str] = Field(default_factory=list)
    regulatory_concerns: list[str] = Field(default_factory=list)
    market_fit_score: float = Field(ge=0, le=1)


class CompetitiveIntelligence(BaseModel):
    """Competitive analysis results"""
    idea_id: str
    direct_competitors: list[dict[str, Any]] = Field(default_factory=list)
    indirect_competitors: list[dict[str, Any]] = Field(default_factory=list)
    competitive_advantages: list[str] = Field(default_factory=list)
    market_gaps: list[str] = Field(default_factory=list)
    positioning_strategy: str = ""


class FeatureValidation(BaseModel):
    """Feature validation results"""
    feature_name: str
    importance_scores: dict[str, float] = Field(default_factory=dict)  # persona_id -> score
    adoption_likelihood: float = Field(ge=0, le=1)
    complexity_score: float = Field(ge=0, le=1)
    mvp_priority: str = "medium"  # high, medium, low


class USPOption(BaseModel):
    """Unique Selling Proposition option"""
    usp_id: str
    statement: str
    target_audience: str
    key_differentiators: list[str] = Field(default_factory=list)
    messaging_tone: str = "professional"
    effectiveness_score: float = Field(ge=0, le=1)


class OptimizedProductModel(BaseModel):
    """Final optimized product model"""
    model_id: str
    product_name: str
    description: str
    target_personas: list[PersonaInsight]
    core_features: list[FeatureValidation]
    unique_selling_proposition: USPOption
    business_model: str
    go_to_market_strategy: str
    success_metrics: list[str] = Field(default_factory=list)
    risk_factors: list[str] = Field(default_factory=list)
    confidence_score: float = Field(ge=0, le=1)


class ProductDiscoveryPipeline:
    """
    Orchestrates cognitive tools for product discovery and validation.

    This pipeline coordinates multiple cognitive tools to analyze personas,
    identify opportunities, generate ideas, and create optimized product models.
    """

    def __init__(self, mcp_server_url: str = "stdio://pyclarity"):
        """
        Initialize the product discovery pipeline.

        Args:
            mcp_server_url: URL of the MCP server with cognitive tools
        """
        self.mcp_server_url = mcp_server_url
        self.workflow_engine = WorkflowEngine()

        # Storage for pipeline results
        self.persona_insights: list[PersonaInsight] = []
        self.pain_point_clusters: list[PainPointCluster] = []
        self.product_ideas: list[ProductIdea] = []
        self.validations: list[ValidationResult] = []
        self.market_analyses: list[MarketAnalysis] = []
        self.competitive_intelligence: list[CompetitiveIntelligence] = []
        self.feature_validations: dict[str, list[FeatureValidation]] = {}
        self.usp_options: list[USPOption] = []
        self.optimized_models: list[OptimizedProductModel] = []

        self.current_stage: AnalysisStage | None = None

    async def execute_pipeline(self, persona_data: list[str]) -> list[OptimizedProductModel]:
        """
        Execute the complete product discovery pipeline.

        Args:
            persona_data: List of persona descriptions

        Returns:
            List of optimized product models ready for BDD generation
        """
        print("🚀 Starting Product Discovery Pipeline")

        # Stage 1: Analyze personas
        self.current_stage = AnalysisStage.PERSONA_ANALYSIS
        await self._analyze_personas(persona_data)

        # Stage 2: Extract and cluster pain points
        self.current_stage = AnalysisStage.PAIN_POINT_EXTRACTION
        await self._extract_pain_points()

        # Stage 3: Generate product ideas
        self.current_stage = AnalysisStage.IDEA_GENERATION
        await self._generate_ideas()

        # Stage 4: Multi-perspective validation
        self.current_stage = AnalysisStage.MULTI_PERSPECTIVE_VALIDATION
        await self._validate_ideas()

        # Stage 5: Market analysis
        self.current_stage = AnalysisStage.MARKET_ANALYSIS
        await self._analyze_market()

        # Stage 6: Competitive intelligence
        self.current_stage = AnalysisStage.COMPETITIVE_INTELLIGENCE
        await self._analyze_competition()

        # Stage 7: Feature validation
        self.current_stage = AnalysisStage.FEATURE_VALIDATION
        await self._validate_features()

        # Stage 8: USP generation
        self.current_stage = AnalysisStage.USP_GENERATION
        await self._generate_usps()

        # Stage 9: Model optimization
        self.current_stage = AnalysisStage.MODEL_OPTIMIZATION
        await self._optimize_models()

        print(f"✅ Pipeline complete. Generated {len(self.optimized_models)} optimized models.")
        return self.optimized_models

    async def _analyze_personas(self, persona_data: list[str]):
        """Stage 1: Analyze personas using cognitive tools"""
        self.current_stage = AnalysisStage.PERSONA_ANALYSIS
        print(f"\n📊 Stage 1: {self.current_stage.value}")

        # Create workflow for persona analysis
        workflow_config = WorkflowConfig(
            name="persona_analysis",
            tools=[
                ToolConfig(
                    name="sequential_thinking",
                    tool_type=ToolType.COGNITIVE,
                    config={
                        "analysis_type": "persona_extraction",
                        "output_format": "structured"
                    }
                ),
                ToolConfig(
                    name="collaborative_reasoning",
                    tool_type=ToolType.COGNITIVE,
                    config={
                        "personas": [
                            {"role": "UX Researcher", "focus": "user behaviors"},
                            {"role": "Product Manager", "focus": "user needs"},
                            {"role": "Data Analyst", "focus": "user patterns"}
                        ]
                    }
                )
            ],
            dependencies=[]  # Both tools can run in parallel
        )

        # Execute persona analysis for each persona
        for i, persona_text in enumerate(persona_data):
            inputs = {
                "sequential_thinking": {
                    "prompt": f"Extract structured insights from this persona: {persona_text[:1000]}",
                    "context": {"task": "persona_analysis"}
                },
                "collaborative_reasoning": {
                    "prompt": f"Analyze this persona from multiple perspectives: {persona_text[:1000]}",
                    "context": {"task": "deep_persona_insights"}
                }
            }

            state = await self.workflow_engine.execute_workflow(
                self.mcp_server_url,
                workflow_config,
                inputs
            )

            # Check for errors
            if state.status == WorkflowStatus.FAILED:
                raise Exception(f"Workflow failed: {state.errors}")

            # Extract and combine results
            persona_insight = self._process_persona_results(
                f"persona_{i}",
                state.tool_results
            )
            self.persona_insights.append(persona_insight)

        print(f"✅ Analyzed {len(self.persona_insights)} personas")

    async def _extract_pain_points(self):
        """Stage 2: Extract and cluster pain points"""
        self.current_stage = AnalysisStage.PAIN_POINT_EXTRACTION
        print(f"\n🔍 Stage 2: {self.current_stage.value}")

        # Aggregate all pain points
        all_pain_points = []
        for persona in self.persona_insights:
            for pain_point in persona.pain_points:
                all_pain_points.append({
                    "pain_point": pain_point,
                    "persona_id": persona.persona_id
                })

        # Use Impact Propagation to understand pain point relationships
        workflow_config = WorkflowConfig(
            name="pain_point_clustering",
            tools=[
                {
                    "name": "impact_propagation",
                    "tool_type": ToolType.COGNITIVE,
                    "config": {
                        "analysis_depth": 3,
                        "consider_indirect_effects": True
                    }
                }
            ],
            dependencies=[]
        )

        # Analyze pain point relationships
        inputs = {
            "impact_propagation": {
                "prompt": f"Analyze relationships between these pain points: {all_pain_points}",
                "context": {"task": "pain_point_clustering"}
            }
        }

        state = await self.workflow_engine.execute_workflow(
            self.mcp_server_url,
            workflow_config,
            inputs
        )

        # Create pain point clusters
        self.pain_point_clusters = self._create_pain_point_clusters(
            all_pain_points,
            state.tool_results.get("impact_propagation", {})
        )

        print(f"✅ Created {len(self.pain_point_clusters)} pain point clusters")

    async def _generate_ideas(self):
        """Stage 3: Generate product ideas"""
        self.current_stage = AnalysisStage.IDEA_GENERATION
        print(f"\n💡 Stage 3: {self.current_stage.value}")

        workflow_config = WorkflowConfig(
            name="idea_generation",
            tools=[
                {
                    "name": "decision_framework",
                    "tool_type": ToolType.COGNITIVE,
                    "config": {
                        "decision_type": "product_ideation",
                        "innovation_level": "high"
                    }
                },
                {
                    "name": "design_patterns",
                    "tool_type": ToolType.COGNITIVE,
                    "config": {
                        "pattern_type": "product_solutions"
                    }
                }
            ],
            dependencies=[]
        )

        # Generate ideas for each pain point cluster
        for cluster in self.pain_point_clusters:
            inputs = {
                "strategic_decision": {
                    "prompt": f"Generate innovative product ideas for: {cluster.pain_points}",
                    "context": {
                        "affected_users": len(cluster.affected_personas),
                        "severity": cluster.severity_score
                    }
                },
                "design_patterns": {
                    "prompt": f"Identify solution patterns for: {cluster.pain_points}",
                    "context": {"domain": "product_development"}
                }
            }

            state = await self.workflow_engine.execute_workflow(
                self.mcp_server_url,
                workflow_config,
                inputs
            )

            # Process generated ideas
            ideas = self._process_idea_generation_results(
                cluster.cluster_id,
                state.tool_results
            )
            self.product_ideas.extend(ideas)

        print(f"✅ Generated {len(self.product_ideas)} product ideas")

    async def _validate_ideas(self):
        """Stage 4: Multi-perspective validation"""
        self.current_stage = AnalysisStage.MULTI_PERSPECTIVE_VALIDATION
        print(f"\n🔄 Stage 4: {self.current_stage.value}")

        workflow_config = WorkflowConfig(
            name="idea_validation",
            tools=[
                {
                    "name": "multi_perspective_analysis",
                    "tool_type": ToolType.COGNITIVE,
                    "config": {
                        "perspectives": ["primary", "adjacent", "contrarian"]
                    }
                }
            ],
            dependencies=[]
        )

        # Validate top ideas
        for idea in self.product_ideas[:10]:  # Limit to top 10 for efficiency
            # Validate with different persona perspectives
            for perspective_type in ["primary", "adjacent", "contrarian"]:
                personas = self._select_personas_for_perspective(
                    idea,
                    perspective_type
                )

                for persona in personas[:3]:  # Limit personas per perspective
                    inputs = {
                        "multi_perspective_analysis": {
                            "prompt": f"Validate this idea: {idea.title} - {idea.description}",
                            "context": {
                                "persona": persona.model_dump(),
                                "perspective_type": perspective_type
                            }
                        }
                    }

                    state = await self.workflow_engine.execute_workflow(
                        self.mcp_server_url,
                        workflow_config,
                        inputs
                    )

                    validation = self._process_validation_results(
                        idea.idea_id,
                        perspective_type,
                        state.tool_results.get("multi_perspective_analysis", {})
                    )
                    self.validations.append(validation)

        print(f"✅ Completed {len(self.validations)} validations")

    async def _analyze_market(self):
        """Stage 5: Market analysis"""
        self.current_stage = AnalysisStage.MARKET_ANALYSIS
        print(f"\n📈 Stage 5: {self.current_stage.value}")

        workflow_config = WorkflowConfig(
            name="market_analysis",
            tools=[
                {
                    "name": "mental_models",
                    "tool_type": ToolType.COGNITIVE,
                    "config": {
                        "models": ["TAM-SAM-SOM", "Porter's Five Forces", "Blue Ocean"]
                    }
                },
                {
                    "name": "decision_framework",
                    "tool_type": ToolType.COGNITIVE,
                    "config": {
                        "criteria": ["market_size", "growth_potential", "competition", "barriers"]
                    }
                }
            ],
            dependencies=[]
        )

        # Analyze market for validated ideas
        validated_ideas = self._get_validated_ideas()

        for idea in validated_ideas:
            inputs = {
                "mental_models": {
                    "prompt": f"Analyze market opportunity for: {idea.title}",
                    "context": {"product_description": idea.description}
                },
                "decision_framework": {
                    "prompt": f"Evaluate market viability for: {idea.title}",
                    "context": {"unique_value": idea.unique_value}
                }
            }

            state = await self.workflow_engine.execute_workflow(
                self.mcp_server_url,
                workflow_config,
                inputs
            )

            market_analysis = self._process_market_analysis_results(
                idea.idea_id,
                state.tool_results
            )
            self.market_analyses.append(market_analysis)

        print(f"✅ Completed market analysis for {len(self.market_analyses)} ideas")

    async def _analyze_competition(self):
        """Stage 6: Competitive intelligence"""
        self.current_stage = AnalysisStage.COMPETITIVE_INTELLIGENCE
        print(f"\n🎯 Stage 6: {self.current_stage.value}")

        workflow_config = WorkflowConfig(
            name="competitive_analysis",
            tools=[
                {
                    "name": "impact_propagation",
                    "tool_type": ToolType.COGNITIVE,
                    "config": {
                        "system_type": "market_ecosystem"
                    }
                },
                {
                    "name": "decision_framework",
                    "tool_type": ToolType.COGNITIVE,
                    "config": {
                        "decision_type": "competitive_positioning"
                    }
                }
            ],
            dependencies=[
                {"from": "impact_propagation", "to": "strategic_decision"}
            ]
        )

        # Analyze competition for market-validated ideas
        for analysis in self.market_analyses:
            if analysis.market_fit_score > 0.6:  # Focus on viable ideas
                idea = next(i for i in self.product_ideas if i.idea_id == analysis.idea_id)

                inputs = {
                    "impact_propagation": {
                        "prompt": f"Analyze competitive landscape for: {idea.title}",
                        "context": {"market": analysis.market_size}
                    },
                    "strategic_decision": {
                        "prompt": f"Develop positioning strategy for: {idea.title}",
                        "context": {"unique_value": idea.unique_value}
                    }
                }

                state = await self.workflow_engine.execute_workflow(
                    self.mcp_server_url,
                    workflow_config,
                    inputs
                )

                competitive_intel = self._process_competitive_analysis_results(
                    idea.idea_id,
                    state.tool_results
                )
                self.competitive_intelligence.append(competitive_intel)

        print(f"✅ Completed competitive analysis for {len(self.competitive_intelligence)} ideas")

    async def _validate_features(self):
        """Stage 7: Feature validation with personas"""
        self.current_stage = AnalysisStage.FEATURE_VALIDATION
        print(f"\n✅ Stage 7: {self.current_stage.value}")

        workflow_config = WorkflowConfig(
            name="feature_validation",
            tools=[
                {
                    "name": "iterative_validation",
                    "tool_type": ToolType.COGNITIVE,
                    "config": {
                        "validation_rounds": 3,
                        "refinement_enabled": True
                    }
                }
            ],
            dependencies=[]
        )

        # Define features for top ideas
        for idea in self._get_top_ideas():
            features = self._define_features_for_idea(idea)
            self.feature_validations[idea.idea_id] = []

            for feature in features:
                # Validate with representative personas
                validation_results = []
                for persona in self.persona_insights[:5]:
                    inputs = {
                        "iterative_validation": {
                            "prompt": f"Validate feature '{feature}' for user",
                            "context": {
                                "persona": persona.model_dump(),
                                "product": idea.title
                            }
                        }
                    }

                    state = await self.workflow_engine.execute_workflow(
                        self.mcp_server_url,
                        workflow_config,
                        inputs
                    )

                    validation_results.append({
                        "persona_id": persona.persona_id,
                        "result": state.tool_results.get("iterative_validation", {})
                    })

                feature_validation = self._process_feature_validation_results(
                    feature,
                    validation_results
                )
                self.feature_validations[idea.idea_id].append(feature_validation)

        total_features = sum(len(features) for features in self.feature_validations.values())
        print(f"✅ Validated {total_features} features across {len(self.feature_validations)} products")

    async def _generate_usps(self):
        """Stage 8: Generate unique selling propositions"""
        self.current_stage = AnalysisStage.USP_GENERATION
        print(f"\n🎨 Stage 8: {self.current_stage.value}")

        workflow_config = WorkflowConfig(
            name="usp_generation",
            tools=[
                {
                    "name": "sequential_thinking",
                    "tool_type": ToolType.COGNITIVE,
                    "config": {
                        "thinking_style": "creative",
                        "depth": 5
                    }
                },
                {
                    "name": "multi_perspective_analysis",
                    "tool_type": ToolType.COGNITIVE,
                    "config": {
                        "perspectives": ["customer", "business", "technical"]
                    }
                }
            ],
            dependencies=[]
        )

        # Generate USPs for top ideas
        for idea in self._get_top_ideas():
            competitive_intel = next(
                (ci for ci in self.competitive_intelligence if ci.idea_id == idea.idea_id),
                None
            )

            inputs = {
                "sequential_thinking": {
                    "prompt": f"Generate compelling USP for: {idea.title}",
                    "context": {
                        "unique_value": idea.unique_value,
                        "differentiators": competitive_intel.competitive_advantages if competitive_intel else []
                    }
                },
                "multi_perspective_analysis": {
                    "prompt": f"Refine USP from multiple viewpoints: {idea.title}",
                    "context": {"target_market": self._get_target_market(idea)}
                }
            }

            state = await self.workflow_engine.execute_workflow(
                self.mcp_server_url,
                workflow_config,
                inputs
            )

            usp_options = self._process_usp_generation_results(
                idea.idea_id,
                state.tool_results
            )
            self.usp_options.extend(usp_options)

        print(f"✅ Generated {len(self.usp_options)} USP options")

    async def _optimize_models(self):
        """Stage 9: Create optimized product models"""
        self.current_stage = AnalysisStage.MODEL_OPTIMIZATION
        print(f"\n🎯 Stage 9: {self.current_stage.value}")

        workflow_config = WorkflowConfig(
            name="model_optimization",
            tools=[
                {
                    "name": "triple_constraint_optimization",
                    "tool_type": ToolType.COGNITIVE,
                    "config": {
                        "optimization_goal": "balanced"
                    }
                },
                {
                    "name": "decision_framework",
                    "tool_type": ToolType.COGNITIVE,
                    "config": {
                        "decision_type": "final_optimization"
                    }
                }
            ],
            dependencies=[]
        )

        # Create optimized models for top ideas
        for idea in self._get_top_ideas():
            # Gather all related data
            validations = [v for v in self.validations if v.idea_id == idea.idea_id]
            market_analysis = next((ma for ma in self.market_analyses if ma.idea_id == idea.idea_id), None)
            competitive_intel = next((ci for ci in self.competitive_intelligence if ci.idea_id == idea.idea_id), None)
            features = self.feature_validations.get(idea.idea_id, [])
            usp = self._select_best_usp(idea.idea_id)

            inputs = {
                "triple_constraint_optimization": {
                    "prompt": f"Optimize product model for: {idea.title}",
                    "context": {
                        "features": [f.model_dump() for f in features],
                        "market_size": market_analysis.market_size if market_analysis else "unknown"
                    }
                },
                "decision_framework": {
                    "prompt": f"Finalize product strategy for: {idea.title}",
                    "context": {
                        "validations": [v.model_dump() for v in validations],
                        "competitive_position": competitive_intel.positioning_strategy if competitive_intel else ""
                    }
                }
            }

            state = await self.workflow_engine.execute_workflow(
                self.mcp_server_url,
                workflow_config,
                inputs
            )

            optimized_model = self._create_optimized_model(
                idea,
                state.tool_results,
                validations,
                market_analysis,
                competitive_intel,
                features,
                usp
            )
            self.optimized_models.append(optimized_model)

        print(f"✅ Created {len(self.optimized_models)} optimized product models")

    # Helper methods
    def _process_persona_results(self, persona_id: str, results: dict[str, Any]) -> PersonaInsight:
        """Process cognitive tool results into PersonaInsight"""
        sequential_result = results.get("sequential_thinking", {})
        collaborative_result = results.get("collaborative_reasoning", {})

        # Combine insights from both tools
        activities = sequential_result.get("activities", [])
        pain_points = sequential_result.get("pain_points", [])

        # Add insights from collaborative reasoning
        for perspective in collaborative_result.get("perspectives", []):
            activities.extend(perspective.get("activities", []))
            pain_points.extend(perspective.get("pain_points", []))

        return PersonaInsight(
            persona_id=persona_id,
            demographics=sequential_result.get("demographics", {}),
            activities=list(set(activities)),  # Remove duplicates
            pain_points=list(set(pain_points)),
            goals=sequential_result.get("goals", []),
            tech_comfort_level=sequential_result.get("tech_comfort", 0.5),
            decision_factors=sequential_result.get("decision_factors", [])
        )

    def _create_pain_point_clusters(self, all_pain_points: list[dict], impact_results: dict) -> list[PainPointCluster]:
        """Create clusters from pain point analysis"""
        # Simplified clustering logic
        clusters = []
        clustered_points = set()

        relationships = impact_results.get("relationships", [])

        for i, point_data in enumerate(all_pain_points):
            if point_data["pain_point"] in clustered_points:
                continue

            cluster = PainPointCluster(
                cluster_id=f"cluster_{i}",
                pain_points=[point_data["pain_point"]],
                affected_personas=[point_data["persona_id"]],
                severity_score=0.7,  # Would be calculated from analysis
                frequency_score=0.6   # Would be calculated from analysis
            )

            # Add related pain points to cluster
            for rel in relationships:
                if point_data["pain_point"] in rel.get("points", []):
                    for related_point in rel.get("points", []):
                        if related_point not in clustered_points:
                            cluster.pain_points.append(related_point)
                            clustered_points.add(related_point)

            clusters.append(cluster)

        return clusters

    def _process_idea_generation_results(self, cluster_id: str, results: dict) -> list[ProductIdea]:
        """Process idea generation results"""
        ideas = []

        strategic_ideas = results.get("decision_framework", {}).get("recommendations", [])
        # TODO: Integrate pattern solutions from design patterns
        # pattern_solutions = results.get("design_patterns", {}).get("patterns", [])

        # Process strategic ideas
        for i, idea_data in enumerate(strategic_ideas):
            idea = ProductIdea(
                idea_id=f"idea_{cluster_id}_{i}",
                title=idea_data.get("title", ""),
                description=idea_data.get("description", ""),
                problem_solved=idea_data.get("problem", ""),
                unique_value=idea_data.get("value_proposition", ""),
                target_clusters=[cluster_id],
                feasibility_score=idea_data.get("feasibility", 0.7),
                innovation_score=idea_data.get("innovation", 0.6)
            )
            ideas.append(idea)

        return ideas

    def _select_personas_for_perspective(self, idea: ProductIdea, perspective_type: str) -> list[PersonaInsight]:
        """Select appropriate personas for validation perspective"""
        if perspective_type == "primary":
            # Get personas from target clusters
            target_persona_ids = set()
            for cluster_id in idea.target_clusters:
                cluster = next(c for c in self.pain_point_clusters if c.cluster_id == cluster_id)
                target_persona_ids.update(cluster.affected_personas)
            return [p for p in self.persona_insights if p.persona_id in target_persona_ids]

        elif perspective_type == "adjacent":
            # Get similar but not directly targeted personas
            # Simplified logic - would use similarity metrics
            return self.persona_insights[3:6]

        else:  # contrarian
            # Get personas with different characteristics
            # Simplified logic - would use contrast metrics
            return self.persona_insights[-2:]

    def _process_validation_results(self, idea_id: str, perspective_type: str, results: dict) -> ValidationResult:
        """Process validation results from multi-perspective analysis"""
        return ValidationResult(
            idea_id=idea_id,
            perspective_type=perspective_type,
            feedback=results.get("feedback", ""),
            concerns=results.get("concerns", []),
            opportunities=results.get("opportunities", []),
            validation_score=results.get("score", 0.5)
        )

    def _get_validated_ideas(self) -> list[ProductIdea]:
        """Get ideas with positive validation scores"""
        validated_ids = set()
        for validation in self.validations:
            if validation.validation_score > 0.6:
                validated_ids.add(validation.idea_id)

        return [idea for idea in self.product_ideas if idea.idea_id in validated_ids]

    def _process_market_analysis_results(self, idea_id: str, results: dict) -> MarketAnalysis:
        """Process market analysis results"""
        mental_models_result = results.get("mental_models", {})
        decision_result = results.get("decision_framework", {})

        return MarketAnalysis(
            idea_id=idea_id,
            market_size=mental_models_result.get("tam", "unknown"),
            growth_rate=mental_models_result.get("growth_rate", "moderate"),
            competitive_intensity=mental_models_result.get("competition", "medium"),
            entry_barriers=mental_models_result.get("barriers", []),
            regulatory_concerns=decision_result.get("regulations", []),
            market_fit_score=decision_result.get("viability_score", 0.5)
        )

    def _process_competitive_analysis_results(self, idea_id: str, results: dict) -> CompetitiveIntelligence:
        """Process competitive analysis results"""
        impact_result = results.get("impact_propagation", {})
        strategic_result = results.get("strategic_decision", {})

        return CompetitiveIntelligence(
            idea_id=idea_id,
            direct_competitors=impact_result.get("direct_competitors", []),
            indirect_competitors=impact_result.get("indirect_competitors", []),
            competitive_advantages=strategic_result.get("advantages", []),
            market_gaps=impact_result.get("gaps", []),
            positioning_strategy=strategic_result.get("positioning", "")
        )

    def _get_top_ideas(self) -> list[ProductIdea]:
        """Get top performing ideas based on validation and market analysis"""
        # Score ideas based on multiple factors
        idea_scores = {}

        for idea in self.product_ideas:
            score = idea.feasibility_score * 0.3 + idea.innovation_score * 0.2

            # Add validation scores
            validations = [v for v in self.validations if v.idea_id == idea.idea_id]
            if validations:
                avg_validation = sum(v.validation_score for v in validations) / len(validations)
                score += avg_validation * 0.3

            # Add market fit score
            market_analysis = next((ma for ma in self.market_analyses if ma.idea_id == idea.idea_id), None)
            if market_analysis:
                score += market_analysis.market_fit_score * 0.2

            idea_scores[idea.idea_id] = score

        # Sort by score and return top 5
        sorted_ideas = sorted(idea_scores.items(), key=lambda x: x[1], reverse=True)
        top_idea_ids = [idea_id for idea_id, _ in sorted_ideas[:5]]

        return [idea for idea in self.product_ideas if idea.idea_id in top_idea_ids]

    def _define_features_for_idea(self, idea: ProductIdea) -> list[str]:
        """Define features based on idea and pain points"""
        # In a real implementation, this would use cognitive tools
        # For now, return example features
        return [
            f"Core functionality for {idea.problem_solved}",
            "User authentication and profiles",
            "Data synchronization",
            "Analytics dashboard",
            "Mobile app support"
        ]

    def _process_feature_validation_results(self, feature_name: str, validation_results: list[dict]) -> FeatureValidation:
        """Process feature validation results from multiple personas"""
        importance_scores = {}
        adoption_scores = []

        for result in validation_results:
            persona_id = result["persona_id"]
            validation_data = result["result"]

            importance_scores[persona_id] = validation_data.get("importance", 0.5)
            adoption_scores.append(validation_data.get("adoption_likelihood", 0.5))

        avg_adoption = sum(adoption_scores) / len(adoption_scores) if adoption_scores else 0.5

        # Determine MVP priority based on scores
        avg_importance = sum(importance_scores.values()) / len(importance_scores) if importance_scores else 0.5

        if avg_importance > 0.8 and avg_adoption > 0.7:
            mvp_priority = "high"
        elif avg_importance > 0.6 or avg_adoption > 0.6:
            mvp_priority = "medium"
        else:
            mvp_priority = "low"

        return FeatureValidation(
            feature_name=feature_name,
            importance_scores=importance_scores,
            adoption_likelihood=avg_adoption,
            complexity_score=0.5,  # Would be calculated based on technical analysis
            mvp_priority=mvp_priority
        )

    def _get_target_market(self, idea: ProductIdea) -> str:
        """Get target market description for an idea"""
        # Aggregate persona demographics from target clusters
        target_personas = []
        for cluster_id in idea.target_clusters:
            cluster = next(c for c in self.pain_point_clusters if c.cluster_id == cluster_id)
            for persona_id in cluster.affected_personas:
                persona = next(p for p in self.persona_insights if p.persona_id == persona_id)
                target_personas.append(persona)

        # Create market description (simplified)
        return f"Users experiencing: {idea.problem_solved}"

    def _process_usp_generation_results(self, idea_id: str, results: dict) -> list[USPOption]:
        """Process USP generation results"""
        usp_options = []

        sequential_result = results.get("sequential_thinking", {})
        perspective_result = results.get("multi_perspective_analysis", {})

        # Get USP variations
        usp_statements = sequential_result.get("usp_options", [])

        for i, statement in enumerate(usp_statements[:3]):  # Limit to 3 options
            usp = USPOption(
                usp_id=f"usp_{idea_id}_{i}",
                statement=statement,
                target_audience=perspective_result.get("target_audience", ""),
                key_differentiators=sequential_result.get("differentiators", []),
                messaging_tone=perspective_result.get("tone", "professional"),
                effectiveness_score=perspective_result.get("effectiveness", 0.7)
            )
            usp_options.append(usp)

        return usp_options

    def _select_best_usp(self, idea_id: str) -> USPOption | None:
        """Select the best USP option for an idea"""
        idea_usps = [usp for usp in self.usp_options if usp.usp_id.startswith(f"usp_{idea_id}")]
        if not idea_usps:
            return None

        # Return highest scoring USP
        return max(idea_usps, key=lambda x: x.effectiveness_score)

    def _create_optimized_model(
        self,
        idea: ProductIdea,
        optimization_results: dict,
        validations: list[ValidationResult],
        market_analysis: MarketAnalysis | None,
        competitive_intel: CompetitiveIntelligence | None,
        features: list[FeatureValidation],
        usp: USPOption | None
    ) -> OptimizedProductModel:
        """Create final optimized product model"""

        # Get target personas
        target_personas = []
        for cluster_id in idea.target_clusters:
            cluster = next(c for c in self.pain_point_clusters if c.cluster_id == cluster_id)
            for persona_id in cluster.affected_personas:
                persona = next(p for p in self.persona_insights if p.persona_id == persona_id)
                if persona not in target_personas:
                    target_personas.append(persona)

        # Filter to MVP features
        mvp_features = [f for f in features if f.mvp_priority in ["high", "medium"]]

        # Extract optimization insights
        triple_result = optimization_results.get("triple_constraint_optimization", {})
        decision_result = optimization_results.get("decision_framework", {})

        return OptimizedProductModel(
            model_id=f"model_{idea.idea_id}",
            product_name=idea.title,
            description=idea.description,
            target_personas=target_personas[:5],  # Limit for model size
            core_features=mvp_features,
            unique_selling_proposition=usp or USPOption(
                usp_id="default",
                statement=idea.unique_value,
                target_audience="General users",
                key_differentiators=[],
                effectiveness_score=0.5
            ),
            business_model=triple_result.get("business_model", "Freemium"),
            go_to_market_strategy=decision_result.get("gtm_strategy", "Digital marketing focus"),
            success_metrics=decision_result.get("metrics", [
                "User acquisition rate",
                "Feature adoption rate",
                "Customer satisfaction score"
            ]),
            risk_factors=triple_result.get("risks", []),
            confidence_score=decision_result.get("confidence", 0.7)
        )
