import os
from typing import Literal

from datasets import load_dataset
from distilabel.models import LiteLLM
from distilabel.pipeline import Pipeline
from distilabel.steps import LoadDataFromHub
from distilabel.steps.tasks import TextGeneration

# Ensure the API key is set
os.environ["FIREWORKS_API_KEY"] = os.getenv("FIREWORKS_API_KEY", "")

# Define different generation types
GENERATION_TYPES = {
    "business_case": {
        "system_prompt": "You are a business strategist. Based on the given persona, create a detailed business case for a product or service that would appeal to them.",
        "template": "Persona: {{ instruction }}\n\nCreate a business case for a product/service targeting this persona:"
    },
    "social_circumstance": {
        "system_prompt": "You are a social scenario designer. Based on the given persona, describe a social situation or circumstance they might encounter.",
        "template": "Persona: {{ instruction }}\n\nDescribe a social situation this persona might face:"
    },
    "emotional_scenario": {
        "system_prompt": "You are an emotional intelligence expert. Based on the given persona, explore their emotional landscape and triggers.",
        "template": "Persona: {{ instruction }}\n\nExplore the emotional world of this persona:"
    },
    "psychometric_insights": {
        "system_prompt": "You are a psychometric analyst. Based on the given persona, provide insights into their personality traits, motivations, and behavioral patterns.",
        "template": "Persona: {{ instruction }}\n\nProvide psychometric insights about this persona:"
    },
    "operational_equation": {
        "system_prompt": "You are a systems analyst. Based on the given persona, create operational frameworks or equations that describe their decision-making process.",
        "template": "Persona: {{ instruction }}\n\nCreate an operational equation/framework for this persona's decision-making:"
    },
    "sales_script": {
        "system_prompt": "You are a sales expert. Based on the given persona, create a sales script that would resonate with them.",
        "template": "Persona: {{ instruction }}\n\nCreate a sales script targeting this persona:"
    },
    "saas_idea": {
        "system_prompt": "You are a SaaS entrepreneur. Based on the given persona, propose a SaaS product idea that would solve their specific pain points.",
        "template": "Persona: {{ instruction }}\n\nPropose a SaaS idea for this persona:"
    }
}

def create_persona_pipeline(generation_type: str = "business_case"):
    """Create a pipeline for a specific generation type."""
    config = GENERATION_TYPES[generation_type]
    
    with Pipeline(name=f"persona-{generation_type}-pipeline") as pipeline:
        text_generation = TextGeneration(
            llm=LiteLLM(
                model="fireworks_ai/accounts/fireworks/models/glm-4p5-air",
                generation_kwargs={"temperature": 0.8, "max_new_tokens": 1024},
            ),
            input_mappings={"persona": "instruction"},
            system_prompt=config["system_prompt"],
            template=config["template"],
            # Add metadata to track generation type
            output_mappings={"generation_type": lambda x: generation_type}
        )
    
    return pipeline

def create_multi_aspect_pipeline():
    """Create a pipeline that generates multiple aspects for each persona."""
    with Pipeline(name="persona-multi-aspect-pipeline") as pipeline:
        # Create tasks for each generation type
        tasks = []
        for gen_type, config in GENERATION_TYPES.items():
            task = TextGeneration(
                name=f"generate_{gen_type}",
                llm=LiteLLM(
                    model="fireworks_ai/accounts/fireworks/models/glm-4p5-air",
                    generation_kwargs={"temperature": 0.8, "max_new_tokens": 1024},
                ),
                input_mappings={"persona": "instruction"},
                output_mappings={
                    "generation": f"{gen_type}_generation",
                    "model_name": f"{gen_type}_model"
                },
                system_prompt=config["system_prompt"],
                template=config["template"],
            )
            tasks.append(task)
    
    return pipeline, tasks

if __name__ == "__main__":
    # Load the PersonaHub dataset
    dataset = load_dataset("proj-persona/PersonaHub", "persona", split="train")
    dataset = dataset.select(range(10))  # Start with 10 personas for testing
    
    # Option 1: Generate a single type of content
    print("Generating business cases for personas...")
    pipeline = create_persona_pipeline("business_case")
    distiset = pipeline.run(dataset=dataset)
    distiset.save_to_disk("persona_business_cases")
    
    # Option 2: Generate all types of content for each persona
    print("\nGenerating multiple aspects for each persona...")
    multi_pipeline, tasks = create_multi_aspect_pipeline()
    
    # Connect all tasks to process the same dataset
    # This will create multiple generations for each persona
    multi_distiset = multi_pipeline.run(dataset=dataset)
    multi_distiset.save_to_disk("persona_multi_aspect")
    
    # Print sample results
    if multi_distiset:
        sample = next(iter(multi_distiset["default"]["train"]))
        print("\nSample persona:", sample["persona"])
        for gen_type in GENERATION_TYPES:
            if f"{gen_type}_generation" in sample:
                print(f"\n{gen_type.upper()}:")
                print(sample[f"{gen_type}_generation"][:200] + "...")