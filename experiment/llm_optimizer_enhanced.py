#!/usr/bin/env python3
"""
Enhanced LLM-Powered Feature Optimizer with Increased Variance
Uses multiple strategies to ensure diverse iterations and continuous improvement
"""

import hashlib
import json
import os
import random
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

# Import the advanced evaluator
from evaluator import FeatureEvaluator
from groq import Groq
from loguru import logger


class EnhancedLLMOptimizer:
    """Enhanced LLM optimizer with variance mechanisms"""

    def __init__(self):
        self.iteration = 0
        self.feature_list = {}
        self.improvement_history = []
        self.convergence_threshold = 0.95
        self.docs_path = Path("../docs/ai-prompting-techniques")
        self.output_path = Path()
        self.history_path = Path("history")
        self.logs_path = Path("logs")

        # Initialize the advanced evaluator
        self.evaluator = FeatureEvaluator()

        # Initialize Groq client
        self.client = Groq()

        # Variance mechanisms
        self.innovation_strategies = [
            "revolutionary",
            "incremental",
            "disruptive",
            "experimental",
            "conservative",
        ]
        self.focus_areas = [
            "user experience",
            "technical innovation",
            "business value",
            "scalability",
            "integration",
            "automation",
        ]
        self.models = [
            "meta-llama/llama-4-maverick-17b-128e-instruct",
            "meta-llama/llama-4-scout-17b-16e-instruct",
            "qwen/qwen3-32b",
        ]

        # Create necessary directories
        self.history_path.mkdir(exist_ok=True)
        self.logs_path.mkdir(exist_ok=True)

        # Load existing state if available
        self._load_state()

    def _load_state(self):
        """Load previous state if exists"""
        features_file = self.output_path / "features.json"
        if features_file.exists():
            with open(features_file) as f:
                data = json.load(f)
                self.feature_list = data.get("features", {})
                self.iteration = data.get("last_iteration", 0)
                logger.info(f"Loaded state from iteration {self.iteration}")

    def get_dynamic_temperature(self, base_temp: float = 0.7) -> float:
        """Calculate dynamic temperature based on iteration and performance"""
        # Start higher, decrease as we converge
        iteration_factor = 1.0 - (self.iteration / 20)  # Decreases over 20 iterations

        # Increase if stuck
        stuck_factor = 1.0
        if len(self.improvement_history) >= 3:
            recent_scores = [h["quality_score"] for h in self.improvement_history[-3:]]
            if max(recent_scores) - min(recent_scores) < 0.02:  # Less than 2% variance
                stuck_factor = 1.3  # Boost temperature by 30%
                logger.info("🔥 Boosting temperature - low variance detected")

        # Random jitter
        jitter = random.uniform(0.9, 1.1)

        final_temp = base_temp * iteration_factor * stuck_factor * jitter
        return max(0.5, min(1.0, final_temp))  # Clamp between 0.5 and 1.0

    def get_iteration_strategy(self) -> dict[str, Any]:
        """Get varying strategy for each iteration"""
        # Cycle through different approaches
        strategies = {
            "innovation_focus": random.choice(self.innovation_strategies),
            "primary_focus": random.choice(self.focus_areas),
            "model": self.models[self.iteration % len(self.models)],
            "temperature": self.get_dynamic_temperature(),
            "top_p": random.uniform(0.8, 0.95),  # nosec B311
            "creativity_boost": random.choice(
                [
                    "Think outside the box",
                    "Challenge conventional approaches",
                    "Combine unrelated concepts",
                    "Question every assumption",
                    "Explore edge cases",
                ]
            ),
        }

        logger.info(f"🎲 Iteration {self.iteration} strategy: {strategies}")
        return strategies

    def run_optimization_loop(self, max_iterations: int = 10, sleep_time: int = 10):
        """Main optimization loop with enhanced variance"""
        logger.info(f"Starting Enhanced LLM Optimizer (max {max_iterations} iterations)")

        while self.iteration < max_iterations and not self.has_converged():
            start_time = time.time()
            self.iteration += 1

            logger.info(f"\n{'=' * 60}")
            logger.info(f"Starting iteration {self.iteration}")
            logger.info(f"{'=' * 60}")

            # Get varying strategy for this iteration
            strategy = self.get_iteration_strategy()

            # Step 1: Load and process documents
            chunks = self.chunk_documents()
            index = self.create_index(chunks)
            summary = self.generate_summary(index, strategy)

            # Step 2: Generate/refine features using LLM with variance
            new_features = self.generate_features_with_llm(summary, strategy)

            # Step 3: Evaluate quality with some randomness
            evaluation_result = self.evaluate_with_variance(new_features)

            # Step 4: Apply improvements with creative optimization
            self.feature_list = self.optimize_features_with_llm(
                new_features, evaluation_result, strategy
            )

            # Step 5: Log progress
            iteration_time = time.time() - start_time
            self.log_iteration_results(evaluation_result, iteration_time, strategy)

            # Step 5b: Generate and save evaluation report
            self.save_evaluation_report(evaluation_result)

            # Step 6: Save checkpoint
            self.save_checkpoint()

            # Show progress
            self.display_iteration_summary(evaluation_result, strategy)

            # Sleep to allow observation
            if self.iteration < max_iterations and not self.has_converged():
                logger.info(f"\n💤 Sleeping for {sleep_time} seconds before next iteration...")
                time.sleep(sleep_time)

        logger.info(f"\n{'=' * 60}")
        logger.info("Optimization complete!")
        logger.info(f"Final quality score: {self.improvement_history[-1]['quality_score']:.2%}")

    def chunk_documents(self) -> list[dict[str, Any]]:
        """Chunk documents for processing"""
        chunks = []

        for md_file in self.docs_path.glob("*.md"):
            try:
                with open(md_file, encoding="utf-8") as f:
                    content = f.read()

                sections = content.split("\n## ")
                for i, section in enumerate(sections):
                    if section.strip():
                        chunks.append(
                            {
                                "file": md_file.name,
                                "section_index": i,
                                "content": section[:2000],
                                "hash": hashlib.md5(section.encode()).hexdigest(),
                            }
                        )
            except Exception as e:
                logger.error(f"Error processing {md_file}: {e}")
                logger.exception(e)

        logger.info(f"Created {len(chunks)} chunks from documents")
        return chunks

    def create_index(self, chunks: list[dict[str, Any]]) -> dict[str, Any]:
        """Create searchable index from chunks"""
        index = {
            "total_chunks": len(chunks),
            "files": {},
            "concepts": {"frameworks": []},
            "key_content": [],
        }

        for chunk in chunks:
            file_name = chunk["file"]
            if file_name not in index["files"]:
                index["files"][file_name] = []
            index["files"][file_name].append(chunk["hash"])

            if len(index["key_content"]) < 10:
                index["key_content"].append(chunk["content"][:500])

        all_text = " ".join([c["content"] for c in chunks])
        frameworks = [
            "Visual Chain-of-Thought",
            "Auto-CoT",
            "Dynamic Prompt Rewriting",
            "AIDA",
            "PAS",
            "JTBD",
            "Business Model Canvas",
            "SWOT",
            "SOSTAC",
            "Porter's Five Forces",
            "Design Thinking",
            "Lean UX",
        ]

        for framework in frameworks:
            if framework.lower() in all_text.lower():
                index["concepts"]["frameworks"].append(framework)

        return index

    def generate_summary(self, index: dict[str, Any], strategy: dict[str, Any]) -> str:
        """Generate enhanced summary with strategic focus"""
        key_content_preview = "\n".join(index["key_content"][:3])

        summary = f"""
Documentation Summary:
- Total files: {len(index["files"])}
- Total chunks: {index["total_chunks"]}
- Key frameworks: {", ".join(index["concepts"]["frameworks"])}

Strategic Focus for This Iteration:
- Innovation Style: {strategy["innovation_focus"]}
- Primary Focus: {strategy["primary_focus"]}
- Creative Direction: {strategy["creativity_boost"]}

The documentation covers AI prompting techniques including:
1. Visual Chain-of-Thought: Breaking UI design into logical visual reasoning steps
2. Auto-CoT with Self-Consistency: Multiple reasoning chains with majority voting
3. Dynamic Prompt Rewriting: AI evaluating and rewriting its own prompts
4. Business/Marketing Frameworks: {len(index["concepts"]["frameworks"])} frameworks for AI-powered tools

Key Content Preview:
{key_content_preview}

Previous Iteration Results:
{self._get_previous_results_summary()}
"""
        return summary

    def _get_previous_results_summary(self) -> str:
        """Get summary of previous iteration results"""
        if not self.improvement_history:
            return "No previous iterations"

        last_result = self.improvement_history[-1]
        return f"""
- Last quality score: {last_result["quality_score"]:.2%}
- Total features: {last_result["total_features"]}
- Key suggestions: {", ".join(last_result.get("suggestions", [])[:2])}
"""

    def generate_features_with_llm(
        self, summary: str, strategy: dict[str, Any]
    ) -> dict[str, list[dict[str, Any]]]:
        """Generate features using LLM with strategic variance"""
        logger.info(
            f"🤖 Generating features with {strategy['model']} (temp={strategy['temperature']:.2f})..."
        )

        # Build context from previous features
        previous_features_context = ""
        if self.feature_list:
            previous_features_context = f"""
Previous Features (Iteration {self.iteration - 1}):
{json.dumps(self.feature_list, indent=2)}

Previous Evaluation Feedback:
{self._get_last_evaluation_feedback()}
"""

        # Add creative constraints based on strategy
        creative_direction = f"""
For this iteration, adopt a {strategy["innovation_focus"]} approach with focus on {strategy["primary_focus"]}.
{strategy["creativity_boost"]}!

Special Instructions:
- If previous iterations were conservative, be bold
- If previous iterations were complex, simplify
- Challenge assumptions from previous iterations
- Introduce at least 2-3 completely new concepts
- Mix features from different domains unexpectedly
"""

        prompt = f"""You are a {strategy["innovation_focus"]} product innovator designing features for an AI-powered UI generation tool.

Context:
{summary}

{previous_features_context}

{creative_direction}

Task: Generate a comprehensive feature list organized into categories (core, supporting, integration, analytics, future).

For iteration {self.iteration}, you MUST:
1. Be creative and introduce NEW ideas not seen before
2. Challenge conventional thinking
3. Mix unexpected combinations
4. Think beyond typical boundaries
5. Surprise with innovative approaches

Generate features in this exact JSON format:
{{
  "core": [...],
  "supporting": [...],
  "integration": [...],
  "analytics": [...],
  "future": [...]
}}

Each feature should follow this structure:
{{
  "id": "F001",
  "name": "Feature Name",
  "description": "Clear description with specific use case (50-150 chars)",
  "priority": "high|medium|low",
  "complexity": "low|medium|high|very_high",
  "dependencies": ["F002"],
  "user_value": 8,  // 1-10
  "technical_risk": 2  // 1-5
}}

Be bold! Be creative! Think differently from previous iterations!"""

        try:
            response = self.client.chat.completions.create(
                model=strategy["model"],
                max_tokens=4000,
                temperature=strategy["temperature"],
                top_p=strategy["top_p"],
                messages=[{"role": "user", "content": prompt}],
            )

            content = response.choices[0].message.content

            import re

            json_match = re.search(r"\{[\s\S]*\}", content)
            if json_match:
                features = json.loads(json_match.group())
                logger.info(f"✅ Generated {sum(len(features[cat]) for cat in features)} features")
                return features
            logger.error("No valid JSON found in LLM response")
            return self._get_fallback_features()

        except Exception as e:
            logger.error(f"Error generating features: {e}")
            return self._get_fallback_features()

    def evaluate_with_variance(self, features: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
        """Evaluate with some randomness to avoid local optima"""
        base_result = self.evaluator.evaluate(features, self.iteration)

        # Add some variance to scores to encourage exploration
        variance_factor = random.uniform(0.95, 1.05)
        base_result["overall_score"] *= variance_factor

        # Randomly emphasize different criteria
        emphasized_criterion = random.choice(list(base_result["scores"].keys()))
        logger.info(f"🎯 Emphasizing {emphasized_criterion} this iteration")

        return base_result

    def _get_last_evaluation_feedback(self) -> str:
        """Get feedback from last evaluation"""
        if not self.improvement_history:
            return "No previous evaluation"

        last = self.improvement_history[-1]
        return f"""
Quality Score: {last["quality_score"]:.2%}
Suggestions:
{chr(10).join(f"- {s}" for s in last.get("suggestions", []))}
"""

    def optimize_features_with_llm(
        self,
        new_features: dict[str, list[dict[str, Any]]],
        evaluation_result: dict[str, Any],
        strategy: dict[str, Any],
    ) -> dict[str, list[dict[str, Any]]]:
        """Optimize features with creative approaches"""
        logger.info(f"🔧 Optimizing with {strategy['innovation_focus']} approach...")

        optimization_style = random.choice(
            [
                "radical transformation",
                "incremental refinement",
                "cross-pollination",
                "simplification",
                "feature fusion",
            ]
        )

        prompt = f"""You are a {strategy["innovation_focus"]} optimization expert using {optimization_style} approach.

Current Features:
{json.dumps(new_features, indent=2)}

Evaluation Results:
- Overall Score: {evaluation_result["overall_score"]:.2%}
- Scores: {json.dumps(evaluation_result["scores"], indent=2)}
- Suggestions: {json.dumps(evaluation_result["suggestions"], indent=2)}

Optimization Style: {optimization_style}
Focus Area: {strategy["primary_focus"]}

Task: Transform the feature list using {optimization_style}:
{"- Completely reimagine low-scoring features" if optimization_style == "radical transformation" else ""}
{"- Make small but impactful improvements" if optimization_style == "incremental refinement" else ""}
{"- Combine features from different categories creatively" if optimization_style == "cross-pollination" else ""}
{"- Remove complexity while maintaining value" if optimization_style == "simplification" else ""}
{"- Merge related features into super-features" if optimization_style == "feature fusion" else ""}

Be creative! Don't just follow suggestions literally - interpret them innovatively!

Return the optimized features in the same JSON format."""

        try:
            response = self.client.chat.completions.create(
                model=strategy["model"],
                max_tokens=4000,
                temperature=strategy["temperature"] * 1.1,  # Slightly higher for optimization
                messages=[{"role": "user", "content": prompt}],
            )

            content = response.choices[0].message.content
            import re

            json_match = re.search(r"\{[\s\S]*\}", content)

            if json_match:
                optimized = json.loads(json_match.group())

                for category in optimized:
                    for feature in optimized[category]:
                        feature["quality_score"] = evaluation_result["overall_score"]
                        feature["iteration_added"] = feature.get("iteration_added", self.iteration)
                        feature["optimization_style"] = optimization_style

                logger.info(f"✅ Features optimized using {optimization_style}")
                return optimized
            logger.error("No valid JSON found in optimization response")
            return new_features

        except Exception as e:
            logger.error(f"Error optimizing features: {e}")
            return new_features

    def _get_fallback_features(self) -> dict[str, list[dict[str, Any]]]:
        """Fallback features if LLM fails"""
        return {
            "core": [
                {
                    "id": "F001",
                    "name": "Visual Chain-of-Thought Designer",
                    "description": "Drag-and-drop interface for creating visual reasoning chains",
                    "priority": "high",
                    "complexity": "medium",
                    "dependencies": [],
                    "user_value": 9,
                    "technical_risk": 3,
                }
            ],
            "supporting": [],
            "integration": [],
            "analytics": [],
            "future": [],
        }

    def has_converged(self) -> bool:
        """Check if optimization has converged"""
        if self.iteration < 3:
            return False

        if len(self.improvement_history) < 3:
            return False

        recent_scores = [h["quality_score"] for h in self.improvement_history[-3:]]
        improvement_rate = (
            (recent_scores[-1] - recent_scores[0]) / recent_scores[0] if recent_scores[0] > 0 else 0
        )

        # Don't converge too early if variance is being introduced
        if self.iteration < 5 and improvement_rate > -0.05:  # Allow some decrease
            return False

        converged = improvement_rate < 0.02 and self.iteration >= 5

        if converged:
            logger.info(
                f"🎯 Convergence detected: {improvement_rate:.2%} improvement over last 3 iterations"
            )

        return converged

    def log_iteration_results(
        self, evaluation_result: dict[str, Any], iteration_time: float, strategy: dict[str, Any]
    ):
        """Log results of current iteration"""
        total_features = sum(len(self.feature_list[cat]) for cat in self.feature_list)

        result = {
            "iteration": self.iteration,
            "timestamp": datetime.now().isoformat(),
            "quality_score": evaluation_result["overall_score"],
            "total_features": total_features,
            "iteration_time": round(iteration_time, 2),
            "metrics": evaluation_result["scores"],
            "improvement_rate": evaluation_result["improvement_rate"],
            "suggestions": evaluation_result["suggestions"][:3],
            "strategy": {
                "model": strategy["model"],
                "temperature": strategy["temperature"],
                "innovation_focus": strategy["innovation_focus"],
            },
        }

        self.improvement_history.append(result)

        with open(self.output_path / "metrics.json", "w") as f:
            json.dump(
                {
                    "current": result,
                    "history": self.improvement_history[-10:],
                },
                f,
                indent=2,
            )

    def save_evaluation_report(self, evaluation_result: dict[str, Any]):
        """Save detailed evaluation report"""
        report = self.evaluator.generate_report(evaluation_result)

        eval_dir = Path("evaluation_reports")
        eval_dir.mkdir(exist_ok=True)

        report_file = eval_dir / f"iteration_{self.iteration:03d}_report.md"
        with open(report_file, "w") as f:
            f.write(report)

        with open("latest_evaluation.md", "w") as f:
            f.write(report)

    def save_checkpoint(self):
        """Save current state"""
        features_data = {
            "iteration": self.iteration,
            "timestamp": datetime.now().isoformat(),
            "features": self.feature_list,
            "last_iteration": self.iteration,
        }

        with open(self.output_path / "features.json", "w") as f:
            json.dump(features_data, f, indent=2)

        history_file = self.history_path / f"iteration_{self.iteration:03d}.json"
        with open(history_file, "w") as f:
            json.dump(features_data, f, indent=2)

    def display_iteration_summary(
        self, evaluation_result: dict[str, Any], strategy: dict[str, Any]
    ):
        """Display pretty iteration summary"""
        print(f"\n📊 ITERATION {self.iteration} SUMMARY")
        print("─" * 50)
        print(f"Strategy: {strategy['innovation_focus']} | Focus: {strategy['primary_focus']}")
        print(f"Model: {strategy['model'].split('-')[0]} | Temp: {strategy['temperature']:.2f}")
        print(
            f"\nOverall Score: {evaluation_result['overall_score']:.1%} "
            f"({'↑' if evaluation_result['improvement_rate'] > 0 else '↓'} "
            f"{abs(evaluation_result['improvement_rate']):.1%})"
        )
        print(f"Total Features: {sum(len(self.feature_list[cat]) for cat in self.feature_list)}")
        print("\nScores by Criteria:")
        for criterion, score in evaluation_result["scores"].items():
            if criterion != "overall":
                print(f"  • {criterion.title()}: {score:.1%}")
        print("\n💡 Top Suggestions:")
        for i, suggestion in enumerate(evaluation_result["suggestions"][:3], 1):
            print(f"  {i}. {suggestion}")
        print("─" * 50)


def main():
    """Run the enhanced LLM optimizer."""
    import argparse

    parser = argparse.ArgumentParser(description="Enhanced LLM Feature Optimizer")
    parser.add_argument("--iterations", type=int, default=8, help="Maximum iterations")
    parser.add_argument("--sleep", type=int, default=10, help="Sleep time between iterations")
    parser.add_argument("--reset", action="store_true", help="Reset and start fresh")
    args = parser.parse_args()

    if not os.environ.get("GROQ_API_KEY"):
        logger.error("Please set GROQ_API_KEY environment variable")
        return

    optimizer = EnhancedLLMOptimizer()

    if args.reset:
        for f in ["features.json", "metrics.json", "latest_evaluation.md"]:
            if os.path.exists(f):
                os.remove(f)
        optimizer.iteration = 0
        optimizer.feature_list = {}
        logger.info("Reset complete. Starting fresh.")

    try:
        optimizer.run_optimization_loop(max_iterations=args.iterations, sleep_time=args.sleep)
    except KeyboardInterrupt:
        logger.info("\n⚠️  Optimization stopped by user")
    except Exception as e:
        logger.error(f"Error in optimization: {e}", exc_info=True)
        logger.exception(e)


if __name__ == "__main__":
    main()
