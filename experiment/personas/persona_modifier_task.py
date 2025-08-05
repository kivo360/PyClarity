import os
from typing import Any, Dict, List, Union

from datasets import load_dataset
from distilabel.models import LiteLLM
from distilabel.pipeline import Pipeline
from distilabel.steps.tasks import Task

# Define ChatType for chat message format
ChatType = list[dict[str, str]]

# Set API key
os.environ["FIREWORKS_API_KEY"] = os.getenv("FIREWORKS_API_KEY", "")


class PersonaModifier(Task):
    """
    A custom task that generates modifications based on personas.

    This task takes a persona and generates various types of content
    that would resonate with or be relevant to that persona.
    """

    modification_type: str = "business_case"
    """The type of modification to generate."""

    @property
    def inputs(self) -> list[str]:
        """The inputs for the task are the persona descriptions."""
        return ["persona"]

    @property
    def outputs(self) -> list[str]:
        """The outputs include the generated content and metadata."""
        return ["modification", "modification_type", "reasoning"]

    def format_input(self, input: dict[str, Any]) -> "ChatType":
        """Format the input for the LLM."""
        persona = input["persona"]

        prompts = {
            "business_case": f"""Given this persona: {persona}
            
Create a detailed business case for a product or service that would appeal to them. Include:
1. Problem statement
2. Proposed solution
3. Value proposition
4. Revenue model
5. Target market analysis""",
            "social_scenario": f"""Given this persona: {persona}
            
Describe a complex social situation they might encounter. Include:
1. Setting and context
2. Other people involved
3. Potential conflicts or challenges
4. How their persona traits would influence their behavior""",
            "emotional_journey": f"""Given this persona: {persona}
            
Map out an emotional journey they might experience. Include:
1. Triggering event
2. Initial emotional response
3. Internal conflict
4. Resolution or growth
5. Long-term impact""",
            "psychometric_profile": f"""Given this persona: {persona}
            
Create a psychometric profile including:
1. Big Five personality traits scores
2. Cognitive preferences
3. Motivational drivers
4. Stress responses
5. Communication style""",
            "decision_framework": f"""Given this persona: {persona}
            
Design a decision-making framework they would use:
1. Key decision criteria
2. Information gathering approach
3. Risk tolerance
4. Time preferences
5. Influence factors""",
            "sales_approach": f"""Given this persona: {persona}
            
Develop a sales approach tailored to them:
1. Opening hook
2. Pain point identification
3. Solution presentation
4. Objection handling
5. Closing strategy""",
            "saas_solution": f"""Given this persona: {persona}
            
Design a SaaS solution for their needs:
1. Core problem to solve
2. Key features
3. User experience priorities
4. Pricing model
5. Success metrics""",
        }

        system_prompt = f"You are an expert at creating {self.modification_type.replace('_', ' ')} content based on personas."

        return [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": prompts.get(self.modification_type, prompts["business_case"]),
            },
        ]

    def process(self, inputs: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Process the inputs and generate modifications."""
        outputs = []

        for input_dict in inputs:
            # Format input for LLM
            formatted_input = self.format_input(input_dict)

            # Generate using LLM
            result = self.llm.generate(
                inputs=[formatted_input], num_generations=1, **self.llm.generation_kwargs
            )

            # Extract generation
            generation = result[0]["generations"][0] if result else ""

            # Create output
            output = {
                "persona": input_dict["persona"],
                "modification": generation,
                "modification_type": self.modification_type,
                "reasoning": f"Generated {self.modification_type} based on persona characteristics",
            }

            outputs.append(output)

        return outputs


# Example: Create a comprehensive persona analysis pipeline
def create_comprehensive_pipeline():
    """Create a pipeline that analyzes personas from multiple angles."""
    modification_types = [
        "business_case",
        "social_scenario",
        "emotional_journey",
        "psychometric_profile",
        "decision_framework",
        "sales_approach",
        "saas_solution",
    ]

    with Pipeline(name="comprehensive-persona-analysis") as pipeline:
        # Create a task for each modification type
        for mod_type in modification_types:
            PersonaModifier(
                name=f"analyze_{mod_type}",
                llm=LiteLLM(
                    model="fireworks_ai/accounts/fireworks/models/glm-4p5-air",
                    generation_kwargs={"temperature": 0.8, "max_new_tokens": 1500, "top_p": 0.9},
                ),
                modification_type=mod_type,
                output_mappings={
                    "modification": f"{mod_type}_content",
                    "reasoning": f"{mod_type}_reasoning",
                },
            )

    return pipeline


# Example usage with batch processing
def process_personas_in_batches():
    """Process personas in batches for efficiency."""
    # Load dataset
    dataset = load_dataset("proj-persona/PersonaHub", "persona", split="train")

    # Select a subset for demonstration
    dataset = dataset.select(range(50))

    # Create pipeline for business cases with batching
    with Pipeline(name="batch-persona-processing") as pipeline:
        PersonaModifier(
            llm=LiteLLM(
                model="fireworks_ai/accounts/fireworks/models/glm-4p5-air",
                generation_kwargs={
                    "temperature": 0.7,
                    "max_tokens": 1000,
                },
            ),
            modification_type="business_case",
            input_batch_size=5,  # Process 5 personas at a time
        )

    # Run pipeline
    distiset = pipeline.run(dataset=dataset)

    # Save results
    distiset.save_to_disk("persona_business_cases_batch")

    # Export to different formats
    if distiset:
        # Save as JSON
        distiset["default"]["train"].to_json("persona_modifications.json")

        # Save as CSV
        distiset["default"]["train"].to_csv("persona_modifications.csv")

        # Push to Hugging Face Hub (optional)
        # distiset.push_to_hub("your-username/persona-modifications")

    return distiset


if __name__ == "__main__":
    # Example 1: Simple single modification
    print("Running simple persona modification...")
    dataset = load_dataset("proj-persona/PersonaHub", "persona", split="train").select(range(5))

    with Pipeline() as simple_pipeline:
        PersonaModifier(
            llm=LiteLLM(
                model="fireworks_ai/accounts/fireworks/models/glm-4p5-air",
                generation_kwargs={"temperature": 0.7, "max_new_tokens": 800},
            ),
            modification_type="saas_solution",
        )

    result = simple_pipeline.run(dataset=dataset)

    # Print sample output
    if result:
        sample = next(iter(result["default"]["train"]))
        print(f"\nPersona: {sample['persona'][:100]}...")
        print(f"\nSaaS Solution: {sample['modification'][:300]}...")

    # Example 2: Batch processing
    print("\n\nRunning batch processing...")
    batch_results = process_personas_in_batches()

    print("\nProcessing complete!")
