#!/usr/bin/env python3
"""
LLM-Powered Feature Optimizer
Uses real LLM calls to generate and refine feature lists iteratively
"""

import hashlib
import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List
from groq import Groq
from loguru import logger

# Import the advanced evaluator
from evaluator import FeatureEvaluator


class LLMFeatureOptimizer:
    """LLM-powered optimizer for iterative feature generation"""

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

    def run_optimization_loop(self, max_iterations: int = 10, sleep_time: int = 10):
        """Main optimization loop with real LLM calls"""
        logger.info(f"Starting LLM-powered optimization loop (max {max_iterations} iterations)")

        while self.iteration < max_iterations and not self.has_converged():
            start_time = time.time()
            self.iteration += 1

            logger.info(f"\n{'='*60}")
            logger.info(f"Starting iteration {self.iteration}")
            logger.info(f"{'='*60}")

            # Step 1: Load and process documents
            chunks = self.chunk_documents()
            index = self.create_index(chunks)
            summary = self.generate_summary(index)

            # Step 2: Generate/refine features using LLM
            new_features = self.generate_features_with_llm(summary)

            # Step 3: Evaluate quality using advanced evaluator
            evaluation_result = self.evaluator.evaluate(new_features, self.iteration)
            
            # Step 4: Apply improvements based on LLM evaluation
            self.feature_list = self.optimize_features_with_llm(new_features, evaluation_result)

            # Step 5: Log progress with enhanced metrics
            iteration_time = time.time() - start_time
            self.log_iteration_results(evaluation_result, iteration_time)
            
            # Step 5b: Generate and save evaluation report
            self.save_evaluation_report(evaluation_result)

            # Step 6: Save checkpoint
            self.save_checkpoint()
            
            # Show progress
            self.display_iteration_summary(evaluation_result)

            # Sleep to allow observation
            if self.iteration < max_iterations and not self.has_converged():
                logger.info(f"\n💤 Sleeping for {sleep_time} seconds before next iteration...")
                time.sleep(sleep_time)

        logger.info(f"\n{'='*60}")
        logger.info("Optimization complete!")
        logger.info(f"Final quality score: {self.improvement_history[-1]['quality_score']:.2%}")

    def chunk_documents(self) -> List[Dict[str, Any]]:
        """Chunk documents for processing"""
        chunks = []

        # Read all markdown files
        for md_file in self.docs_path.glob("*.md"):
            try:
                with open(md_file, encoding="utf-8") as f:
                    content = f.read()

                # Simple chunking by sections
                sections = content.split("\n## ")
                for i, section in enumerate(sections):
                    if section.strip():
                        chunks.append({
                            "file": md_file.name,
                            "section_index": i,
                            "content": section[:2000],  # Limit chunk size
                            "hash": hashlib.md5(section.encode()).hexdigest(),
                        })
            except Exception as e:
                logger.error(f"Error processing {md_file}: {e}")

        logger.info(f"Created {len(chunks)} chunks from documents")
        return chunks

    def create_index(self, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create searchable index from chunks"""
        index = {
            "total_chunks": len(chunks),
            "files": {},
            "concepts": {"frameworks": []},
            "key_content": []
        }

        # Group by file and extract key content
        for chunk in chunks:
            file_name = chunk["file"]
            if file_name not in index["files"]:
                index["files"][file_name] = []
            index["files"][file_name].append(chunk["hash"])
            
            # Store key content snippets
            if len(index["key_content"]) < 10:  # Keep top 10 chunks
                index["key_content"].append(chunk["content"][:500])

        # Extract framework names from all text
        all_text = " ".join([c["content"] for c in chunks])
        frameworks = [
            "Visual Chain-of-Thought", "Auto-CoT", "Dynamic Prompt Rewriting",
            "AIDA", "PAS", "JTBD", "Business Model Canvas", "SWOT", "SOSTAC",
            "Porter's Five Forces", "Design Thinking", "Lean UX"
        ]
        
        for framework in frameworks:
            if framework.lower() in all_text.lower():
                index["concepts"]["frameworks"].append(framework)

        return index

    def generate_summary(self, index: Dict[str, Any]) -> str:
        """Generate enhanced summary from index"""
        key_content_preview = "\n".join(index["key_content"][:3])
        
        summary = f"""
Documentation Summary:
- Total files: {len(index["files"])}
- Total chunks: {index["total_chunks"]}
- Key frameworks: {", ".join(index["concepts"]["frameworks"])}

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
- Last quality score: {last_result['quality_score']:.2%}
- Total features: {last_result['total_features']}
- Key suggestions: {', '.join(last_result.get('suggestions', [])[:2])}
"""

    def generate_features_with_llm(self, summary: str) -> Dict[str, List[Dict[str, Any]]]:
        """Generate features using Claude API"""
        logger.info("🤖 Generating features with LLM...")
        
        # Build context from previous features
        previous_features_context = ""
        if self.feature_list:
            previous_features_context = f"""
Previous Features (Iteration {self.iteration - 1}):
{json.dumps(self.feature_list, indent=2)}

Previous Evaluation Feedback:
{self._get_last_evaluation_feedback()}
"""

        prompt = f"""You are a product manager designing features for an AI-powered UI generation tool.

Context:
{summary}

{previous_features_context}

Task: Generate a comprehensive feature list organized into categories (core, supporting, integration, analytics, future).

For iteration {self.iteration}, focus on:
1. Addressing previous feedback and suggestions
2. Adding missing feature categories
3. Improving feature descriptions with specific use cases
4. Ensuring technical feasibility
5. Maximizing user value

Generate features in this exact JSON format:
{{
  "core": [
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
  ],
  "supporting": [...],
  "integration": [...],
  "analytics": [...],
  "future": [...]
}}

Requirements:
- Include at least 3-5 features per category
- Ensure all feature IDs are unique
- Dependencies must reference valid feature IDs
- Descriptions should be specific and actionable
- User value 8+ for core features
- Balance innovation with feasibility

Generate the complete feature list:"""

        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                max_tokens=4000,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Extract JSON from response
            content = response.choices[0].message.content
            
            # Find JSON in response
            import re
            json_match = re.search(r'\{[\s\S]*\}', content)
            if json_match:
                features = json.loads(json_match.group())
                logger.info(f"✅ Generated {sum(len(features[cat]) for cat in features)} features")
                return features
            else:
                logger.error("No valid JSON found in LLM response")
                return self._get_fallback_features()
                
        except Exception as e:
            logger.error(f"Error generating features: {e}")
            return self._get_fallback_features()

    def _get_last_evaluation_feedback(self) -> str:
        """Get feedback from last evaluation"""
        if not self.improvement_history:
            return "No previous evaluation"
        
        last = self.improvement_history[-1]
        return f"""
Quality Score: {last['quality_score']:.2%}
Suggestions:
{chr(10).join(f"- {s}" for s in last.get('suggestions', []))}
"""

    def optimize_features_with_llm(self, new_features: Dict[str, List[Dict[str, Any]]], 
                                   evaluation_result: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        """Optimize features based on LLM analysis of evaluation"""
        logger.info("🔧 Optimizing features with LLM based on evaluation...")
        
        prompt = f"""You are a product optimization expert. Analyze the evaluation results and improve the feature list.

Current Features:
{json.dumps(new_features, indent=2)}

Evaluation Results:
- Overall Score: {evaluation_result['overall_score']:.2%}
- Detailed Scores: {json.dumps(evaluation_result['scores'], indent=2)}
- Feedback: {json.dumps(evaluation_result['detailed_feedback'], indent=2)}
- Suggestions: {json.dumps(evaluation_result['suggestions'], indent=2)}

Task: Optimize the feature list by:
1. Adding features to address low-scoring areas
2. Breaking down high-complexity features
3. Improving descriptions for clarity
4. Adding missing categories (especially if completeness score is low)
5. Ensuring all dependencies are valid

Return the optimized features in the same JSON format, with improvements applied.
Focus on actionable changes that will improve the evaluation scores."""

        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                max_tokens=4000,
                temperature=0.5,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.choices[0].message.content
            import re
            json_match = re.search(r'\{[\s\S]*\}', content)
            
            if json_match:
                optimized = json.loads(json_match.group())
                
                # Add metadata
                for category in optimized:
                    for feature in optimized[category]:
                        feature["quality_score"] = evaluation_result["overall_score"]
                        feature["iteration_added"] = feature.get("iteration_added", self.iteration)
                
                logger.info("✅ Features optimized based on evaluation")
                return optimized
            else:
                logger.error("No valid JSON found in optimization response")
                return new_features
                
        except Exception as e:
            logger.error(f"Error optimizing features: {e}")
            return new_features

    def _get_fallback_features(self) -> Dict[str, List[Dict[str, Any]]]:
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
                    "technical_risk": 3
                }
            ],
            "supporting": [],
            "integration": [],
            "analytics": [],
            "future": []
        }

    def has_converged(self) -> bool:
        """Check if optimization has converged"""
        if self.iteration < 3:  # Minimum iterations
            return False

        if len(self.improvement_history) < 3:
            return False

        # Check if improvements are minimal
        recent_scores = [h["quality_score"] for h in self.improvement_history[-3:]]
        improvement_rate = (recent_scores[-1] - recent_scores[0]) / recent_scores[0] if recent_scores[0] > 0 else 0

        converged = improvement_rate < 0.02  # Less than 2% improvement
        
        if converged:
            logger.info(f"🎯 Convergence detected: {improvement_rate:.2%} improvement over last 3 iterations")
        
        return converged

    def log_iteration_results(self, evaluation_result: Dict[str, Any], iteration_time: float):
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
        }

        self.improvement_history.append(result)

        # Save to metrics file
        with open(self.output_path / "metrics.json", "w") as f:
            json.dump({
                "current": result,
                "history": self.improvement_history[-10:],
            }, f, indent=2)

    def save_evaluation_report(self, evaluation_result: Dict[str, Any]):
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

        # Save to history
        history_file = self.history_path / f"iteration_{self.iteration:03d}.json"
        with open(history_file, "w") as f:
            json.dump(features_data, f, indent=2)

    def display_iteration_summary(self, evaluation_result: Dict[str, Any]):
        """Display pretty iteration summary"""
        print(f"\n📊 ITERATION {self.iteration} SUMMARY")
        print("─" * 50)
        print(f"Overall Score: {evaluation_result['overall_score']:.1%} "
              f"({'↑' if evaluation_result['improvement_rate'] > 0 else '↓'} "
              f"{abs(evaluation_result['improvement_rate']):.1%})")
        print(f"Total Features: {sum(len(self.feature_list[cat]) for cat in self.feature_list)}")
        print("\nScores by Criteria:")
        for criterion, score in evaluation_result['scores'].items():
            if criterion != 'overall':
                print(f"  • {criterion.title()}: {score:.1%}")
        print("\n💡 Top Suggestions:")
        for i, suggestion in enumerate(evaluation_result['suggestions'][:3], 1):
            print(f"  {i}. {suggestion}")
        print("─" * 50)


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="LLM-Powered Feature Optimizer")
    parser.add_argument("--iterations", type=int, default=5, help="Maximum iterations")
    parser.add_argument("--sleep", type=int, default=10, help="Sleep time between iterations")
    parser.add_argument("--reset", action="store_true", help="Reset and start fresh")
    args = parser.parse_args()

    # Check for API key
    if not os.environ.get("GROQ_API_KEY"):
        logger.error("Please set GROQ_API_KEY environment variable")
        return

    optimizer = LLMFeatureOptimizer()

    if args.reset:
        # Clear existing state
        for f in ["features.json", "metrics.json", "latest_evaluation.md"]:
            if os.path.exists(f):
                os.remove(f)
        optimizer.iteration = 0
        optimizer.feature_list = {}
        logger.info("Reset complete. Starting fresh.")

    try:
        optimizer.run_optimization_loop(
            max_iterations=args.iterations,
            sleep_time=args.sleep
        )
    except KeyboardInterrupt:
        logger.info("\n⚠️  Optimization stopped by user")
    except Exception as e:
        logger.error(f"Error in optimization: {e}", exc_info=True)


if __name__ == "__main__":
    main()