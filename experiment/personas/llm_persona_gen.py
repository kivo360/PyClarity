import os

from datasets import Dataset
from distilabel.models import LiteLLM
from distilabel.pipeline import Pipeline
from distilabel.steps.tasks import TextGeneration

# Ensure the API key is set as an environment variable
os.environ["FIREWORKS_API_KEY"] = os.getenv("FIREWORKS_API_KEY", "")

with Pipeline() as pipeline:
    TextGeneration(
        llm=LiteLLM(
            model="fireworks_ai/accounts/fireworks/models/glm-4p5-air",
            generation_kwargs={"temperature": 0.8, "max_tokens": 1024},
        ),
        # System prompt for generating diverse personas
        system_prompt=(
            "You are an expert persona designer who creates detailed, realistic personas for various purposes. "
            "Each persona should include demographic details, personality traits, goals, challenges, "
            "professional background, personal interests, and behavioral patterns. "
            "Make each persona unique, diverse, and believable."
        ),
    )

if __name__ == "__main__":
    # Create a dataset with instructions for generating different types of personas
    persona_instructions = [
        # Business personas
        "Create a persona for a startup founder in the sustainable technology sector",
        "Create a persona for a mid-level marketing manager at a Fortune 500 company",
        "Create a persona for a freelance graphic designer specializing in brand identity",
        "Create a persona for a small business owner running a local bakery",
        "Create a persona for a venture capitalist focused on AI investments",
        # Technical personas
        "Create a persona for a senior backend engineer at a fintech company",
        "Create a persona for a data scientist working in healthcare analytics",
        "Create a persona for a DevOps engineer transitioning to cloud architecture",
        "Create a persona for a cybersecurity consultant for government contracts",
        "Create a persona for a mobile app developer focused on accessibility",
        # Creative personas
        "Create a persona for a content creator on social media platforms",
        "Create a persona for a novelist writing their third mystery book",
        "Create a persona for a documentary filmmaker focused on social issues",
        "Create a persona for a UX designer in the gaming industry",
        "Create a persona for a music producer working with emerging artists",
        # Healthcare personas
        "Create a persona for a nurse practitioner in rural healthcare",
        "Create a persona for a mental health counselor specializing in adolescents",
        "Create a persona for a medical researcher studying rare diseases",
        "Create a persona for a physical therapist with a sports medicine focus",
        "Create a persona for a healthcare administrator managing multiple clinics",
        # Education personas
        "Create a persona for a high school STEM teacher in an urban school",
        "Create a persona for a university professor researching climate change",
        "Create a persona for an instructional designer for corporate training",
        "Create a persona for a special education coordinator",
        "Create a persona for an edtech startup product manager",
        # Diverse backgrounds
        "Create a persona for a recent immigrant starting their first US-based business",
        "Create a persona for a military veteran transitioning to civilian tech career",
        "Create a persona for a single parent returning to workforce after 5 years",
        "Create a persona for a Gen Z environmental activist and influencer",
        "Create a persona for a retired executive becoming a nonprofit consultant",
    ]

    # Create dataset from instructions
    dataset = Dataset.from_dict({"instruction": persona_instructions})

    # Run the pipeline
    distiset = pipeline.run(dataset=dataset)
    distiset.save_to_disk("generated_personas")
