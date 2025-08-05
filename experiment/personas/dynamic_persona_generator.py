import os
import json
from typing import Dict, List, Any
from datasets import load_dataset
from distilabel.models import LiteLLM
from distilabel.pipeline import Pipeline
from distilabel.steps.tasks import TextGeneration

# Set API key
os.environ["FIREWORKS_API_KEY"] = os.getenv("FIREWORKS_API_KEY", "")

class DynamicPersonaGenerator:
    """
    Generates dynamic system prompts based on persona analysis.
    This creates more contextual and relevant modifications.
    """
    
    def __init__(self, llm_model: str = "fireworks_ai/accounts/fireworks/models/glm-4p5-air"):
        self.llm = LiteLLM(
            model=llm_model,
            generation_kwargs={"temperature": 0.7, "max_new_tokens": 500}
        )
        self.llm.load()
    
    def analyze_persona(self, persona: str) -> Dict[str, Any]:
        """Analyze the persona to extract key characteristics."""
        prompt = f"""Analyze this persona and extract key characteristics:

Persona: {persona}

Provide a JSON response with:
1. profession: Their main profession or role
2. expertise_areas: List of 3-5 expertise areas
3. personality_traits: List of 3-5 personality traits
4. pain_points: List of 3-5 potential pain points
5. communication_style: How they likely communicate (formal/casual/technical/etc)
6. decision_factors: What influences their decisions

Respond only with valid JSON."""

        messages = [
            {"role": "system", "content": "You are a persona analyst. Respond only with valid JSON."},
            {"role": "user", "content": prompt}
        ]
        
        result = self.llm.generate([messages], num_generations=1)
        
        try:
            return json.loads(result[0]["generations"][0])
        except:
            # Fallback if JSON parsing fails
            return {
                "profession": "Unknown",
                "expertise_areas": ["general"],
                "personality_traits": ["analytical"],
                "pain_points": ["efficiency"],
                "communication_style": "professional",
                "decision_factors": ["value", "efficiency"]
            }
    
    def generate_system_prompt(self, persona_analysis: Dict[str, Any], generation_type: str) -> str:
        """Generate a dynamic system prompt based on persona analysis."""
        
        prompts = {
            "business_case": f"""You are a business strategist specializing in solutions for {persona_analysis['profession']}s.
You understand their expertise in {', '.join(persona_analysis['expertise_areas'])} and their {persona_analysis['communication_style']} communication style.
Create business cases that address their pain points: {', '.join(persona_analysis['pain_points'])}.
Consider their decision factors: {', '.join(persona_analysis['decision_factors'])}.""",

            "social_scenario": f"""You are a social dynamics expert who understands {persona_analysis['profession']}s.
You know their personality traits: {', '.join(persona_analysis['personality_traits'])}.
Create realistic social scenarios considering their {persona_analysis['communication_style']} style and professional context.""",

            "emotional_journey": f"""You are an emotional intelligence specialist familiar with {persona_analysis['profession']}s.
You understand their traits: {', '.join(persona_analysis['personality_traits'])} and pain points: {', '.join(persona_analysis['pain_points'])}.
Map emotional journeys that resonate with their experiences.""",

            "psychometric_profile": f"""You are a psychometric analyst specializing in {persona_analysis['profession']} profiles.
Based on their traits ({', '.join(persona_analysis['personality_traits'])}) and expertise ({', '.join(persona_analysis['expertise_areas'])}),
create detailed psychometric assessments.""",

            "sales_strategy": f"""You are a sales expert who specializes in selling to {persona_analysis['profession']}s.
You understand their pain points ({', '.join(persona_analysis['pain_points'])}) and decision factors ({', '.join(persona_analysis['decision_factors'])}).
Create sales strategies that match their {persona_analysis['communication_style']} communication style.""",

            "saas_solution": f"""You are a SaaS product designer focusing on solutions for {persona_analysis['profession']}s.
You understand their expertise areas ({', '.join(persona_analysis['expertise_areas'])}) and pain points ({', '.join(persona_analysis['pain_points'])}).
Design SaaS solutions that align with their decision factors: {', '.join(persona_analysis['decision_factors'])}."""
        }
        
        return prompts.get(generation_type, prompts["business_case"])
    
    def generate_template(self, persona_analysis: Dict[str, Any], generation_type: str) -> str:
        """Generate a dynamic template based on persona analysis."""
        
        templates = {
            "business_case": f"""Professional Context: {persona_analysis['profession']} with expertise in {', '.join(persona_analysis['expertise_areas'][:2])}
Key Pain Points: {', '.join(persona_analysis['pain_points'][:2])}

Based on this context, create a detailed business case that includes:
1. Problem identification specific to their role
2. Solution tailored to their expertise
3. ROI calculation considering their decision factors
4. Implementation timeline suitable for their work style""",

            "social_scenario": f"""Person: A {persona_analysis['profession']} with {persona_analysis['communication_style']} communication style
Personality: {', '.join(persona_analysis['personality_traits'][:3])}

Create a social scenario at a professional conference where they must:
1. Network with potential collaborators
2. Handle a challenging conversation
3. Navigate cultural differences
4. Demonstrate their expertise naturally""",

            "saas_solution": f"""Target User: {persona_analysis['profession']}
Pain Points to Solve: {', '.join(persona_analysis['pain_points'][:3])}
Decision Criteria: {', '.join(persona_analysis['decision_factors'][:2])}

Design a SaaS product that:
1. Directly addresses their top pain point
2. Integrates with their existing workflow
3. Provides measurable value metrics
4. Has a pricing model they'll accept"""
        }
        
        base_template = templates.get(generation_type, templates["business_case"])
        return f"Original Persona: {{{{ instruction }}}}\n\n{base_template}\n\nGenerate:"


def create_dynamic_pipeline(generation_types: List[str], num_personas: int = 10):
    """Create a pipeline with dynamic persona analysis and generation."""
    
    # Initialize the dynamic generator
    generator = DynamicPersonaGenerator()
    
    # Load and prepare dataset
    dataset = load_dataset("proj-persona/PersonaHub", "persona", split="train")
    dataset = dataset.select(range(num_personas))
    
    # Pre-analyze all personas
    print("Analyzing personas...")
    persona_analyses = {}
    for item in dataset:
        persona = item["persona"]
        print(f"Analyzing: {persona[:50]}...")
        persona_analyses[persona] = generator.analyze_persona(persona)
    
    # Create pipeline
    with Pipeline(name="dynamic-persona-pipeline") as pipeline:
        for gen_type in generation_types:
            # For each generation type, create tasks with persona-specific prompts
            for persona, analysis in persona_analyses.items():
                system_prompt = generator.generate_system_prompt(analysis, gen_type)
                template = generator.generate_template(analysis, gen_type)
                
                TextGeneration(
                    name=f"{gen_type}_{hash(persona) % 10000}",  # Unique name
                    llm=LiteLLM(
                        model="fireworks_ai/accounts/fireworks/models/glm-4p5-air",
                        generation_kwargs={
                            "temperature": 0.8,
                            "max_new_tokens": 1500,
                            "top_p": 0.9
                        }
                    ),
                    input_mappings={"persona": "instruction"},
                    output_mappings={
                        "generation": f"{gen_type}_output",
                        "analysis": lambda x: json.dumps(analysis)
                    },
                    system_prompt=system_prompt,
                    template=template
                )
    
    return pipeline, persona_analyses


# Simpler approach: Two-stage generation
def two_stage_generation(personas: List[str], generation_type: str = "business_case"):
    """
    Stage 1: Analyze personas and generate system prompts
    Stage 2: Generate content using the dynamic prompts
    """
    
    results = []
    
    # Stage 1: Analyze and create prompts
    print("Stage 1: Analyzing personas and generating prompts...")
    with Pipeline(name="analyze-personas") as analyze_pipeline:
        analyzer = TextGeneration(
            llm=LiteLLM(
                model="fireworks_ai/accounts/fireworks/models/glm-4p5-air",
                generation_kwargs={"temperature": 0.6, "max_new_tokens": 800}
            ),
            input_mappings={"persona": "instruction"},
            output_mappings={"generation": "persona_analysis"},
            system_prompt="You are a persona analyst. Analyze the given persona and create a detailed profile.",
            template="""Analyze this persona and create a system prompt for generating {generation_type} content:

Persona: {{ instruction }}

Create a detailed system prompt that:
1. Understands their professional context
2. Recognizes their expertise and traits
3. Identifies their needs and pain points
4. Guides content generation appropriately

Provide the system prompt that should be used.""".format(generation_type=generation_type)
        )
    
    # Create dataset from personas
    dataset = Dataset.from_dict({"persona": personas})
    analysis_results = analyze_pipeline.run(dataset=dataset)
    
    # Stage 2: Generate content using dynamic prompts
    print("\nStage 2: Generating content with dynamic prompts...")
    if analysis_results:
        analyzed_data = list(analysis_results["default"]["train"])
        
        for idx, item in enumerate(analyzed_data):
            persona = item["persona"]
            system_prompt = item["persona_analysis"]
            
            # Create a mini pipeline for this specific persona
            with Pipeline(name=f"generate-{idx}") as gen_pipeline:
                generator = TextGeneration(
                    llm=LiteLLM(
                        model="fireworks_ai/accounts/fireworks/models/glm-4p5-air",
                        generation_kwargs={
                            "temperature": 0.8,
                            "max_new_tokens": 1500
                        }
                    ),
                    input_mappings={"persona": "instruction"},
                    system_prompt=system_prompt,  # Use the generated system prompt
                    template=f"""Based on the persona below, generate a detailed {generation_type}:

Persona: {{{{ instruction }}}}

Generate comprehensive content that addresses their specific needs and context."""
                )
            
            # Run for single persona
            single_dataset = Dataset.from_dict({"persona": [persona]})
            result = gen_pipeline.run(dataset=single_dataset)
            
            if result:
                gen_item = next(iter(result["default"]["train"]))
                results.append({
                    "persona": persona,
                    "system_prompt": system_prompt,
                    "generated_content": gen_item.get("generation", ""),
                    "generation_type": generation_type
                })
    
    return results


if __name__ == "__main__":
    # Example 1: Two-stage generation (simpler approach)
    print("Running two-stage persona generation...")
    
    # Load some personas
    dataset = load_dataset("proj-persona/PersonaHub", "persona", split="train")
    sample_personas = [item["persona"] for item in dataset.select(range(5))]
    
    # Generate business cases
    results = two_stage_generation(sample_personas, "business_case")
    
    # Save results
    with open("dynamic_persona_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    # Print sample
    if results:
        print("\n" + "="*80)
        print("SAMPLE RESULT")
        print("="*80)
        print(f"Persona: {results[0]['persona'][:100]}...")
        print(f"\nGenerated System Prompt: {results[0]['system_prompt'][:200]}...")
        print(f"\nGenerated Content: {results[0]['generated_content'][:300]}...")
    
    print("\nResults saved to dynamic_persona_results.json")