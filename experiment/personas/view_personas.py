"""View the generated personas from the Distilabel output."""

from pathlib import Path

from distilabel.distiset import Distiset
from loguru import logger

# Get the project root directory
project_root = Path(__file__).parent.parent.parent
personas_path = project_root / "generated_personas"

# Load the generated personas using Distilabel
distiset = Distiset.load_from_disk(personas_path)

# Access the dataset
dataset = distiset["default"]["train"]

# Log summary
logger.info(f"Total personas generated: {len(dataset)}")
logger.info(f"Columns: {dataset.column_names}")
logger.info("\n" + "=" * 80 + "\n")

# Display first 3 personas
for i, example in enumerate(dataset.select(range(3))):
    logger.info(f"PERSONA {i + 1}:")
    logger.info(f"Instruction: {example['instruction']}")
    logger.info("\nGenerated Persona:")
    logger.info(example["generation"])
    logger.info("\n" + "-" * 80 + "\n")

# Optionally save to a more readable format
if __name__ == "__main__":
    # Save all personas to a text file for easy reading
    output_file = Path("generated_personas_readable.txt")
    with output_file.open("w") as f:
        for i, example in enumerate(dataset):
            f.write(f"PERSONA {i + 1}:\n")
            f.write(f"Instruction: {example['instruction']}\n\n")
            f.write(f"Generated Persona:\n{example['generation']}\n")
            f.write("\n" + "=" * 80 + "\n\n")

    logger.info("All personas saved to 'generated_personas_readable.txt'")
