---
size_categories: n<1K
tags:
- synthetic
- distilabel
- rlaif
---

<p align="left">
  <a href="https://github.com/argilla-io/distilabel">
    <img src="https://raw.githubusercontent.com/argilla-io/distilabel/main/docs/assets/distilabel-badge-light.png" alt="Built with Distilabel" width="200" height="32"/>
  </a>
</p>

# Dataset Card for generated_personas

This dataset has been created with [distilabel](https://distilabel.argilla.io/).



## Dataset Summary

This dataset contains a `pipeline.yaml` which can be used to reproduce the pipeline that generated it in distilabel using the `distilabel` CLI:

```console
distilabel pipeline run --config "https://huggingface.co/datasets/generated_personas/raw/main/pipeline.yaml"
```

or explore the configuration:

```console
distilabel pipeline info --config "https://huggingface.co/datasets/generated_personas/raw/main/pipeline.yaml"
```

## Dataset structure

The examples have the following structure per configuration:


<details><summary> Configuration: default </summary><hr>

```json
{
    "distilabel_metadata": {
        "raw_input_text_generation_0": [
            {
                "content": "You are an expert persona designer who creates detailed, realistic personas for various purposes. Each persona should include demographic details, personality traits, goals, challenges, professional background, personal interests, and behavioral patterns. Make each persona unique, diverse, and believable.",
                "role": "system"
            },
            {
                "content": "Create a persona for a startup founder in the sustainable technology sector",
                "role": "user"
            }
        ],
        "raw_output_text_generation_0": "\n# Persona: Elena Rodriguez - Sustainable Tech Founder\n\n## Demographic Details\n- **Name:** Elena Rodriguez\n- **Age:** 34\n- **Gender:** Female\n- **Ethnicity:** Hispanic-American (second-generation, parents immigrated from Mexico)\n- **Location:**",
        "statistics_text_generation_0": {
            "input_tokens": 73,
            "output_tokens": 58
        }
    },
    "generation": "\n# Persona: Elena Rodriguez - Sustainable Tech Founder\n\n## Demographic Details\n- **Name:** Elena Rodriguez\n- **Age:** 34\n- **Gender:** Female\n- **Ethnicity:** Hispanic-American (second-generation, parents immigrated from Mexico)\n- **Location:**",
    "instruction": "Create a persona for a startup founder in the sustainable technology sector",
    "model_name": "fireworks_ai/accounts/fireworks/models/glm-4p5-air"
}
```

This subset can be loaded as:

```python
from datasets import load_dataset

ds = load_dataset("generated_personas", "default")
```

Or simply as it follows, since there's only one configuration and is named `default`: 

```python
from datasets import load_dataset

ds = load_dataset("generated_personas")
```


</details>




