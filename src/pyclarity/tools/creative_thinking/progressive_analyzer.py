"""
Progressive Creative Thinking Analyzer

Facilitates creative ideation, brainstorming, and innovation processes
with session-based progression and idea evolution tracking.
"""

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from pyclarity.db.base import BaseSessionStore, SessionData
from pyclarity.db.creative_store import (
    BaseCreativeStore,
    CreativeData,
    Idea,
    CreativeConstraint,
    IdeaCombination,
)
from pyclarity.tools.creative_thinking.models import (
    CreativeMode,
    IdeaCategory,
    CreativeMethod,
    NoveltyLevel,
)


class ProgressiveCreativeRequest(BaseModel):
    """Request for progressive creative thinking."""
    
    session_id: Optional[str] = Field(None, description="Session ID for continuing ideation")
    step_number: int = Field(1, description="Current step in creative process")
    
    # Creative context
    challenge: str = Field(..., description="Creative challenge or problem")
    domain: str = Field("general", description="Domain context")
    creative_mode: CreativeMode = Field(..., description="Mode of creative thinking")
    
    # Current ideation
    ideas: List[Dict[str, Any]] = Field(default_factory=list, description="New ideas generated")
    building_on: List[int] = Field(default_factory=list, description="IDs of ideas to build on")
    
    # Creative parameters
    constraints: List[Dict[str, Any]] = Field(default_factory=list, description="Creative constraints")
    inspiration_sources: List[str] = Field(default_factory=list, description="Sources of inspiration")
    creative_methods: List[CreativeMethod] = Field(default_factory=list, description="Methods to apply")
    
    # Session settings
    divergent_thinking: bool = Field(True, description="Enable divergent thinking")
    combine_ideas: bool = Field(False, description="Combine existing ideas")
    seek_novelty: bool = Field(True, description="Prioritize novel ideas")
    
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ProgressiveCreativeResponse(BaseModel):
    """Response from progressive creative thinking."""
    
    # Core response
    status: str = Field(..., description="Status of creative step")
    session_id: str = Field(..., description="Session identifier")
    step_id: int = Field(..., description="Database ID of this step")
    step_number: int = Field(..., description="Sequential step number")
    
    # Ideas generated
    new_ideas_count: int = Field(0, description="Number of new ideas")
    total_ideas_count: int = Field(0, description="Total ideas in session")
    
    # Idea quality
    novelty_scores: Dict[str, float] = Field(default_factory=dict)
    feasibility_scores: Dict[str, float] = Field(default_factory=dict)
    impact_scores: Dict[str, float] = Field(default_factory=dict)
    
    # Creative insights
    idea_categories: Dict[str, List[str]] = Field(default_factory=dict)
    idea_combinations: List[Dict[str, Any]] = Field(default_factory=list)
    creative_patterns: List[str] = Field(default_factory=list)
    
    # Recommendations
    promising_ideas: List[Dict[str, Any]] = Field(default_factory=list)
    suggested_methods: List[str] = Field(default_factory=list)
    next_directions: List[str] = Field(default_factory=list)
    
    # Creative metrics
    ideation_velocity: float = Field(0.0, description="Ideas per step")
    diversity_score: float = Field(0.0, description="Diversity of ideas")
    innovation_potential: float = Field(0.0, description="Overall innovation score")
    
    # Error handling
    error: Optional[str] = Field(None)
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "session_id": "creative-123",
                "new_ideas_count": 5,
                "total_ideas_count": 12,
                "promising_ideas": [{"title": "Idea 1", "score": 0.85}],
                "innovation_potential": 0.75
            }
        }


class ProgressiveCreativeAnalyzer:
    """Progressive creative thinking with session management."""
    
    def __init__(
        self,
        session_store: BaseSessionStore,
        creative_store: BaseCreativeStore,
    ):
        """Initialize with required stores."""
        self.session_store = session_store
        self.creative_store = creative_store
    
    async def generate_ideas(
        self, request: ProgressiveCreativeRequest
    ) -> ProgressiveCreativeResponse:
        """Process a creative thinking step."""
        try:
            # Get or create session
            session = await self._get_or_create_session(request)
            
            # Process new ideas
            processed_ideas = self._process_ideas(request.ideas)
            
            # Apply creative methods if specified
            if request.creative_methods:
                enhanced_ideas = await self._apply_creative_methods(
                    processed_ideas,
                    request.creative_methods,
                    request.challenge
                )
                processed_ideas.extend(enhanced_ideas)
            
            # Combine ideas if requested
            combinations = []
            if request.combine_ideas and request.building_on:
                combinations = await self._combine_ideas(
                    session.session_id,
                    request.building_on,
                    processed_ideas
                )
            
            # Score ideas
            novelty_scores = self._score_novelty(processed_ideas, session.session_id)
            feasibility_scores = self._score_feasibility(processed_ideas, request.constraints)
            impact_scores = self._score_impact(processed_ideas, request.challenge)
            
            # Categorize ideas
            categories = self._categorize_ideas(processed_ideas)
            
            # Identify patterns
            patterns = await self._identify_creative_patterns(session.session_id)
            
            # Create and save creative data
            creative_data = await self._create_creative_data(
                session.session_id,
                request,
                processed_ideas,
                combinations
            )
            saved_data = await self.creative_store.save_creative_step(creative_data)
            
            # Get session statistics
            total_ideas = await self._count_total_ideas(session.session_id)
            ideation_velocity = total_ideas / request.step_number
            
            # Calculate diversity
            diversity_score = await self._calculate_diversity(session.session_id)
            
            # Identify promising ideas
            promising = self._identify_promising_ideas(
                processed_ideas,
                novelty_scores,
                feasibility_scores,
                impact_scores
            )
            
            # Suggest next methods
            suggested_methods = self._suggest_creative_methods(
                patterns,
                diversity_score,
                request.creative_mode
            )
            
            # Determine next directions
            next_directions = self._suggest_next_directions(
                categories,
                patterns,
                request.seek_novelty
            )
            
            # Calculate innovation potential
            innovation_potential = self._calculate_innovation_potential(
                novelty_scores,
                feasibility_scores,
                diversity_score
            )
            
            return ProgressiveCreativeResponse(
                status="success",
                session_id=session.session_id,
                step_id=saved_data.id,
                step_number=saved_data.step_number,
                new_ideas_count=len(processed_ideas),
                total_ideas_count=total_ideas,
                novelty_scores=novelty_scores,
                feasibility_scores=feasibility_scores,
                impact_scores=impact_scores,
                idea_categories=categories,
                idea_combinations=[self._combination_to_dict(c) for c in combinations],
                creative_patterns=patterns,
                promising_ideas=promising,
                suggested_methods=suggested_methods,
                next_directions=next_directions,
                ideation_velocity=ideation_velocity,
                diversity_score=diversity_score,
                innovation_potential=innovation_potential,
            )
            
        except Exception as e:
            return ProgressiveCreativeResponse(
                status="error",
                session_id=request.session_id or str(uuid.uuid4()),
                step_id=0,
                step_number=request.step_number,
                error=str(e),
            )
    
    async def _get_or_create_session(
        self, request: ProgressiveCreativeRequest
    ) -> SessionData:
        """Get existing session or create new one."""
        if request.session_id:
            session = await self.session_store.get_session(request.session_id)
            if session:
                return session
        
        # Create new session
        session_data = SessionData(
            session_id=request.session_id or str(uuid.uuid4()),
            tool_name="Creative Thinking",
            created_at=datetime.now(timezone.utc),
            metadata={
                "challenge": request.challenge,
                "domain": request.domain,
                "creative_mode": request.creative_mode.value,
            }
        )
        
        return await self.session_store.create_session(session_data)
    
    def _process_ideas(self, idea_dicts: List[Dict[str, Any]]) -> List[Idea]:
        """Process idea dictionaries into Idea objects."""
        ideas = []
        
        for idea_dict in idea_dicts:
            idea = Idea(
                title=idea_dict.get("title", "Untitled Idea"),
                description=idea_dict.get("description", ""),
                category=IdeaCategory(idea_dict.get("category", "concept")),
                tags=idea_dict.get("tags", []),
                inspiration_source=idea_dict.get("inspiration", ""),
                novelty_level=NoveltyLevel(idea_dict.get("novelty", "moderate")),
                feasibility_score=idea_dict.get("feasibility", 0.5),
                impact_score=idea_dict.get("impact", 0.5),
                development_notes=idea_dict.get("notes", ""),
            )
            ideas.append(idea)
        
        return ideas
    
    async def _apply_creative_methods(
        self,
        ideas: List[Idea],
        methods: List[CreativeMethod],
        challenge: str
    ) -> List[Idea]:
        """Apply creative methods to generate new ideas."""
        new_ideas = []
        
        for method in methods:
            if method == CreativeMethod.BRAINSTORMING:
                new_ideas.extend(self._brainstorm_variations(ideas, challenge))
            elif method == CreativeMethod.SCAMPER:
                new_ideas.extend(self._apply_scamper(ideas))
            elif method == CreativeMethod.RANDOM_WORD:
                new_ideas.extend(self._random_word_association(ideas, challenge))
            elif method == CreativeMethod.MORPHOLOGICAL:
                new_ideas.extend(self._morphological_analysis(ideas))
            elif method == CreativeMethod.ANALOGIES:
                new_ideas.extend(self._generate_analogies(ideas, challenge))
        
        return new_ideas
    
    def _brainstorm_variations(self, existing_ideas: List[Idea], challenge: str) -> List[Idea]:
        """Generate variations through brainstorming."""
        variations = []
        
        # Generate opposites
        for idea in existing_ideas[:2]:  # Limit to avoid explosion
            opposite = Idea(
                title=f"Opposite of {idea.title}",
                description=f"What if we did the opposite? {idea.description}",
                category=idea.category,
                tags=idea.tags + ["opposite", "brainstorm"],
                novelty_level=NoveltyLevel.HIGH,
            )
            variations.append(opposite)
        
        # Generate extremes
        if existing_ideas:
            extreme = Idea(
                title="Extreme version",
                description="Taking the concept to its absolute limit",
                category=IdeaCategory.RADICAL,
                tags=["extreme", "brainstorm"],
                novelty_level=NoveltyLevel.VERY_HIGH,
            )
            variations.append(extreme)
        
        return variations
    
    def _apply_scamper(self, ideas: List[Idea]) -> List[Idea]:
        """Apply SCAMPER method."""
        scamper_ideas = []
        
        scamper_prompts = {
            "Substitute": "What can be substituted?",
            "Combine": "What can be combined?",
            "Adapt": "What can be adapted?",
            "Modify": "What can be modified or magnified?",
            "Put to other uses": "How else can this be used?",
            "Eliminate": "What can be eliminated?",
            "Reverse": "What can be reversed or rearranged?",
        }
        
        for idea in ideas[:1]:  # Apply to first idea
            for technique, prompt in scamper_prompts.items():
                new_idea = Idea(
                    title=f"{technique}: {idea.title}",
                    description=f"{prompt} Applied to: {idea.description}",
                    category=IdeaCategory.VARIATION,
                    tags=["scamper", technique.lower()],
                    novelty_level=NoveltyLevel.MODERATE,
                )
                scamper_ideas.append(new_idea)
        
        return scamper_ideas[:3]  # Limit output
    
    def _random_word_association(self, ideas: List[Idea], challenge: str) -> List[Idea]:
        """Generate ideas through random word association."""
        # Simulated random words
        random_words = ["butterfly", "clock", "mirror", "bridge", "seed"]
        associations = []
        
        for word in random_words[:2]:
            association = Idea(
                title=f"{word.capitalize()}-inspired solution",
                description=f"What if the solution worked like a {word}?",
                category=IdeaCategory.METAPHORICAL,
                tags=["random-word", word],
                inspiration_source=word,
                novelty_level=NoveltyLevel.HIGH,
            )
            associations.append(association)
        
        return associations
    
    def _morphological_analysis(self, ideas: List[Idea]) -> List[Idea]:
        """Apply morphological analysis."""
        # Simplified morphological analysis
        parameters = ["Form", "Function", "Material", "Energy"]
        variations = ["A", "B", "C"]
        
        morphological_ideas = []
        
        # Generate one combination
        combination = "-".join([f"{p}{v}" for p, v in zip(parameters[:2], variations[:2])])
        
        new_idea = Idea(
            title=f"Morphological combination: {combination}",
            description="Systematic combination of parameters",
            category=IdeaCategory.SYSTEMATIC,
            tags=["morphological", combination],
            novelty_level=NoveltyLevel.MODERATE,
        )
        morphological_ideas.append(new_idea)
        
        return morphological_ideas
    
    def _generate_analogies(self, ideas: List[Idea], challenge: str) -> List[Idea]:
        """Generate ideas through analogies."""
        analogy_sources = ["nature", "sports", "music", "cooking"]
        analogies = []
        
        for source in analogy_sources[:2]:
            analogy = Idea(
                title=f"{source.capitalize()} analogy",
                description=f"How would {source} solve this problem?",
                category=IdeaCategory.METAPHORICAL,
                tags=["analogy", source],
                inspiration_source=f"{source} systems",
                novelty_level=NoveltyLevel.HIGH,
            )
            analogies.append(analogy)
        
        return analogies
    
    async def _combine_ideas(
        self,
        session_id: str,
        idea_ids: List[int],
        new_ideas: List[Idea]
    ) -> List[IdeaCombination]:
        """Combine existing ideas to create new ones."""
        combinations = []
        
        # Get existing ideas (simplified - would fetch from store)
        existing_ideas = await self.creative_store.get_ideas_by_ids(session_id, idea_ids)
        
        # Combine with new ideas
        for i, existing in enumerate(existing_ideas[:2]):
            for j, new in enumerate(new_ideas[:2]):
                combination = IdeaCombination(
                    idea_a_id=idea_ids[i],
                    idea_b_id=j,  # Would be actual ID
                    combination_type="synthesis",
                    resulting_idea=Idea(
                        title=f"Combined: {existing.title} + {new.title}",
                        description=f"Synthesis of concepts",
                        category=IdeaCategory.HYBRID,
                        tags=["combination", "synthesis"],
                        novelty_level=NoveltyLevel.VERY_HIGH,
                    ),
                    synergy_score=0.8,
                )
                combinations.append(combination)
        
        return combinations
    
    def _score_novelty(self, ideas: List[Idea], session_id: str) -> Dict[str, float]:
        """Score ideas for novelty."""
        scores = {}
        
        for i, idea in enumerate(ideas):
            # Base score from idea's novelty level
            base_score = {
                NoveltyLevel.LOW: 0.2,
                NoveltyLevel.MODERATE: 0.5,
                NoveltyLevel.HIGH: 0.8,
                NoveltyLevel.VERY_HIGH: 0.95,
            }.get(idea.novelty_level, 0.5)
            
            # Adjust based on category
            if idea.category in [IdeaCategory.RADICAL, IdeaCategory.DISRUPTIVE]:
                base_score += 0.1
            
            # Ensure within bounds
            scores[f"idea_{i}"] = min(1.0, base_score)
        
        return scores
    
    def _score_feasibility(
        self, ideas: List[Idea], constraints: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """Score ideas for feasibility."""
        scores = {}
        
        for i, idea in enumerate(ideas):
            # Start with idea's base feasibility
            score = idea.feasibility_score
            
            # Adjust based on constraints
            for constraint in constraints:
                if constraint.get("type") == "resource" and idea.category == IdeaCategory.RADICAL:
                    score -= 0.1  # Radical ideas often need more resources
                elif constraint.get("type") == "time" and idea.novelty_level == NoveltyLevel.VERY_HIGH:
                    score -= 0.1  # Very novel ideas take time
            
            scores[f"idea_{i}"] = max(0.0, min(1.0, score))
        
        return scores
    
    def _score_impact(self, ideas: List[Idea], challenge: str) -> Dict[str, float]:
        """Score ideas for potential impact."""
        scores = {}
        
        for i, idea in enumerate(ideas):
            # Start with idea's base impact
            score = idea.impact_score
            
            # Adjust based on category
            impact_modifiers = {
                IdeaCategory.DISRUPTIVE: 0.2,
                IdeaCategory.TRANSFORMATIVE: 0.15,
                IdeaCategory.RADICAL: 0.1,
                IdeaCategory.SYSTEMATIC: 0.05,
            }
            
            modifier = impact_modifiers.get(idea.category, 0)
            scores[f"idea_{i}"] = min(1.0, score + modifier)
        
        return scores
    
    def _categorize_ideas(self, ideas: List[Idea]) -> Dict[str, List[str]]:
        """Categorize ideas by type."""
        categories = {}
        
        for i, idea in enumerate(ideas):
            category = idea.category.value
            if category not in categories:
                categories[category] = []
            categories[category].append(f"idea_{i}: {idea.title}")
        
        return categories
    
    async def _identify_creative_patterns(self, session_id: str) -> List[str]:
        """Identify patterns in creative process."""
        patterns = []
        
        # Get all ideas from session
        all_ideas = await self.creative_store.get_session_ideas(session_id)
        
        if not all_ideas:
            return patterns
        
        # Category patterns
        category_counts = {}
        for idea in all_ideas:
            category_counts[idea.category.value] = category_counts.get(idea.category.value, 0) + 1
        
        dominant_category = max(category_counts.items(), key=lambda x: x[1])[0]
        patterns.append(f"Tendency toward {dominant_category} ideas")
        
        # Novelty patterns
        high_novelty_count = sum(1 for idea in all_ideas if idea.novelty_level in [NoveltyLevel.HIGH, NoveltyLevel.VERY_HIGH])
        if high_novelty_count > len(all_ideas) * 0.5:
            patterns.append("Strong focus on novel solutions")
        
        # Method patterns
        method_tags = []
        for idea in all_ideas:
            method_tags.extend([tag for tag in idea.tags if tag in ["brainstorm", "scamper", "analogy"]])
        
        if method_tags:
            most_common_method = max(set(method_tags), key=method_tags.count)
            patterns.append(f"{most_common_method.capitalize()} method most effective")
        
        return patterns
    
    async def _count_total_ideas(self, session_id: str) -> int:
        """Count total ideas in session."""
        return await self.creative_store.count_session_ideas(session_id)
    
    async def _calculate_diversity(self, session_id: str) -> float:
        """Calculate diversity of ideas."""
        all_ideas = await self.creative_store.get_session_ideas(session_id)
        
        if len(all_ideas) < 2:
            return 0.0
        
        # Category diversity
        categories = set(idea.category for idea in all_ideas)
        category_diversity = len(categories) / len(IdeaCategory)
        
        # Tag diversity
        all_tags = set()
        for idea in all_ideas:
            all_tags.update(idea.tags)
        
        tag_diversity = min(1.0, len(all_tags) / (len(all_ideas) * 2))
        
        # Novelty diversity
        novelty_levels = set(idea.novelty_level for idea in all_ideas)
        novelty_diversity = len(novelty_levels) / len(NoveltyLevel)
        
        # Combined diversity score
        return (category_diversity + tag_diversity + novelty_diversity) / 3
    
    def _identify_promising_ideas(
        self,
        ideas: List[Idea],
        novelty_scores: Dict[str, float],
        feasibility_scores: Dict[str, float],
        impact_scores: Dict[str, float]
    ) -> List[Dict[str, Any]]:
        """Identify most promising ideas."""
        promising = []
        
        for i, idea in enumerate(ideas):
            idea_key = f"idea_{i}"
            
            # Calculate combined score
            novelty = novelty_scores.get(idea_key, 0)
            feasibility = feasibility_scores.get(idea_key, 0)
            impact = impact_scores.get(idea_key, 0)
            
            # Weighted combination
            combined_score = (novelty * 0.3 + feasibility * 0.3 + impact * 0.4)
            
            if combined_score > 0.6:  # Threshold for promising
                promising.append({
                    "title": idea.title,
                    "category": idea.category.value,
                    "score": round(combined_score, 2),
                    "strengths": self._identify_strengths(novelty, feasibility, impact),
                })
        
        # Sort by score and return top 3
        promising.sort(key=lambda x: x["score"], reverse=True)
        return promising[:3]
    
    def _identify_strengths(
        self, novelty: float, feasibility: float, impact: float
    ) -> List[str]:
        """Identify strengths of an idea."""
        strengths = []
        
        if novelty > 0.7:
            strengths.append("Highly novel")
        if feasibility > 0.7:
            strengths.append("Very feasible")
        if impact > 0.7:
            strengths.append("High impact potential")
        
        return strengths
    
    def _suggest_creative_methods(
        self,
        patterns: List[str],
        diversity_score: float,
        creative_mode: CreativeMode
    ) -> List[str]:
        """Suggest creative methods to try next."""
        suggestions = []
        
        # Based on diversity
        if diversity_score < 0.5:
            suggestions.append("Try SCAMPER for systematic variation")
            suggestions.append("Use random word association for divergent thinking")
        
        # Based on mode
        mode_methods = {
            CreativeMode.DIVERGENT: ["Brainstorming", "Mind mapping", "Free association"],
            CreativeMode.CONVERGENT: ["Morphological analysis", "Systematic combination"],
            CreativeMode.LATERAL: ["Provocations", "Random entry", "Concept extraction"],
            CreativeMode.TRANSFORMATIVE: ["Metaphorical thinking", "Boundary breaking"],
        }
        
        if creative_mode in mode_methods:
            suggestions.extend(mode_methods[creative_mode][:2])
        
        return list(set(suggestions))[:3]
    
    def _suggest_next_directions(
        self,
        categories: Dict[str, List[str]],
        patterns: List[str],
        seek_novelty: bool
    ) -> List[str]:
        """Suggest next directions for ideation."""
        directions = []
        
        # Based on categories
        if len(categories) < 3:
            directions.append("Explore different idea categories")
        
        if IdeaCategory.PRACTICAL.value not in categories and not seek_novelty:
            directions.append("Generate more practical, implementable ideas")
        
        if IdeaCategory.RADICAL.value not in categories and seek_novelty:
            directions.append("Push boundaries with more radical concepts")
        
        # Based on patterns
        if "novel solutions" in str(patterns):
            directions.append("Balance with feasibility considerations")
        
        # General suggestions
        if len(categories) > 5:
            directions.append("Focus on developing top ideas further")
        else:
            directions.append("Continue divergent exploration")
        
        return directions[:3]
    
    def _calculate_innovation_potential(
        self,
        novelty_scores: Dict[str, float],
        feasibility_scores: Dict[str, float],
        diversity_score: float
    ) -> float:
        """Calculate overall innovation potential."""
        if not novelty_scores:
            return 0.0
        
        # Average novelty
        avg_novelty = sum(novelty_scores.values()) / len(novelty_scores)
        
        # Average feasibility
        avg_feasibility = sum(feasibility_scores.values()) / len(feasibility_scores) if feasibility_scores else 0.5
        
        # Innovation = High novelty + Reasonable feasibility + Good diversity
        innovation = (avg_novelty * 0.4 + avg_feasibility * 0.3 + diversity_score * 0.3)
        
        return min(1.0, innovation)
    
    async def _create_creative_data(
        self,
        session_id: str,
        request: ProgressiveCreativeRequest,
        ideas: List[Idea],
        combinations: List[IdeaCombination]
    ) -> CreativeData:
        """Create creative data for storage."""
        # Process constraints
        constraints = []
        for c in request.constraints:
            constraint = CreativeConstraint(
                constraint_type=c.get("type", "general"),
                description=c.get("description", ""),
                importance=c.get("importance", "medium"),
            )
            constraints.append(constraint)
        
        return CreativeData(
            session_id=session_id,
            step_number=request.step_number,
            creative_mode=request.creative_mode,
            challenge=request.challenge,
            domain=request.domain,
            ideas=ideas,
            constraints=constraints,
            idea_combinations=combinations,
            creative_methods_used=[m.value for m in request.creative_methods],
            inspiration_sources=request.inspiration_sources,
            metadata=request.metadata,
            created_at=datetime.now(timezone.utc),
        )
    
    def _combination_to_dict(self, combination: IdeaCombination) -> Dict[str, Any]:
        """Convert combination to dictionary."""
        return {
            "type": combination.combination_type,
            "synergy": combination.synergy_score,
            "result": combination.resulting_idea.title if combination.resulting_idea else "Combined concept",
        }