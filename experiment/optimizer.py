#!/usr/bin/env python3
"""
Iterative Feature Optimizer
Continuously generates and refines feature lists from documentation
"""

import hashlib
import json
import logging
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Any

from loguru import logger

# Import the advanced evaluator
from evaluator import FeatureEvaluator

# Set up logging


class FeatureOptimizer:
    """Main optimizer class for iterative feature generation"""

    def __init__(self, config_path: str = "optimizer_config.yaml"):
        self.iteration = 0
        self.feature_list = []
        self.improvement_history = []
        self.convergence_threshold = 0.95
        self.docs_path = Path("../docs/ai-prompting-techniques")
        self.output_path = Path()
        self.history_path = Path("history")
        self.logs_path = Path("logs")
        
        # Initialize the advanced evaluator
        self.evaluator = FeatureEvaluator()

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

    def run_optimization_loop(self, watch_mode: bool = False):
        """Main optimization loop"""
        logger.info("Starting optimization loop")

        while not self.has_converged():
            start_time = time.time()
            self.iteration += 1

            logger.info(f"Starting iteration {self.iteration}")

            # Step 1: Load and process documents
            chunks = self.chunk_documents()
            index = self.create_index(chunks)
            summary = self.generate_summary(index)

            # Step 2: Generate/refine features
            new_features = self.generate_features(summary)

            # Step 3: Evaluate quality using advanced evaluator
            evaluation_result = self.evaluator.evaluate(new_features, self.iteration)
            
            # Extract quality scores for compatibility
            quality_score = evaluation_result["scores"]
            quality_score["overall"] = evaluation_result["overall_score"]

            # Step 4: Apply improvements based on evaluator suggestions
            old_features = self.feature_list.copy() if isinstance(self.feature_list, list) else {}
            self.feature_list = self.optimize_features(old_features, new_features, evaluation_result)

            # Step 5: Log progress with enhanced metrics
            iteration_time = time.time() - start_time
            self.log_iteration_results(evaluation_result, iteration_time)
            
            # Step 5b: Generate and save evaluation report
            self.save_evaluation_report(evaluation_result)

            # Step 6: Save checkpoint
            self.save_checkpoint()

            # Check if we should continue
            if not watch_mode and self.iteration >= 1:
                break

            if watch_mode:
                time.sleep(5)  # Wait 5 seconds between iterations in watch mode

    def chunk_documents(self) -> list[dict[str, Any]]:
        """Chunk documents for processing"""
        chunks = []

        # Read all markdown files
        for md_file in self.docs_path.glob("*.md"):
            try:
                with open(md_file, encoding="utf-8") as f:
                    content = f.read()

                # Simple chunking by sections (would use chonkie in real implementation)
                sections = content.split("\n## ")
                for i, section in enumerate(sections):
                    if section.strip():
                        chunks.append(
                            {
                                "file": md_file.name,
                                "section_index": i,
                                "content": section[:1000],  # Limit chunk size
                                "hash": hashlib.md5(section.encode()).hexdigest(),
                            }
                        )
            except Exception as e:
                logger.error(f"Error processing {md_file}: {e}")

        logger.info(f"Created {len(chunks)} chunks from documents")
        return chunks

    def create_index(self, chunks: list[dict[str, Any]]) -> dict[str, Any]:
        """Create searchable index from chunks"""
        index = {"total_chunks": len(chunks), "files": {}, "concepts": {}, "keywords": []}

        # Group by file
        for chunk in chunks:
            file_name = chunk["file"]
            if file_name not in index["files"]:
                index["files"][file_name] = []
            index["files"][file_name].append(chunk["hash"])

        # Extract key concepts (simplified)
        all_text = " ".join([c["content"] for c in chunks])

        # Look for framework names
        frameworks = [
            "Visual Chain-of-Thought",
            "Auto-CoT",
            "Dynamic Prompt Rewriting",
            "AIDA",
            "PAS",
            "JTBD",
            "Business Model Canvas",
            "SWOT",
        ]

        for framework in frameworks:
            if framework.lower() in all_text.lower():
                if "frameworks" not in index["concepts"]:
                    index["concepts"]["frameworks"] = []
                index["concepts"]["frameworks"].append(framework)

        return index

    def generate_summary(self, index: dict[str, Any]) -> str:
        """Generate summary from index"""
        summary = f"""
        Documentation Summary:
        - Total files: {len(index["files"])}
        - Total chunks: {index["total_chunks"]}
        - Key frameworks: {", ".join(index["concepts"].get("frameworks", []))}
        
        The documentation covers AI prompting techniques including visual reasoning,
        self-consistency validation, dynamic rewriting, and multiple business/marketing
        frameworks for building AI-powered tools.
        """
        return summary

    def generate_features(self, summary: str) -> dict[str, list[dict[str, Any]]]:
        """Generate features based on current knowledge"""
        # In real implementation, this would call an LLM
        # For now, we'll simulate with progressive improvements

        base_features = {
            "core": [
                {
                    "id": "F001",
                    "name": "Visual Chain-of-Thought Designer",
                    "description": "Drag-and-drop interface for creating visual reasoning chains",
                    "priority": "high",
                    "complexity": "medium",
                    "dependencies": ["F002", "F003"],
                    "user_value": 9,
                    "technical_risk": 3,
                },
                {
                    "id": "F002",
                    "name": "Dynamic Prompt Rewriter",
                    "description": "AI-powered prompt optimization engine",
                    "priority": "high",
                    "complexity": "high",
                    "dependencies": [],
                    "user_value": 8,
                    "technical_risk": 4,
                },
                {
                    "id": "F003",
                    "name": "Self-Consistency Validator",
                    "description": "Multi-chain validation with voting mechanism",
                    "priority": "high",
                    "complexity": "medium",
                    "dependencies": [],
                    "user_value": 8,
                    "technical_risk": 2,
                },
            ],
            "supporting": [
                {
                    "id": "F004",
                    "name": "Framework Template Library",
                    "description": "Pre-built templates for 50+ frameworks",
                    "priority": "medium",
                    "complexity": "low",
                    "dependencies": [],
                    "user_value": 7,
                    "technical_risk": 1,
                },
                {
                    "id": "F005",
                    "name": "Export API",
                    "description": "RESTful API for integrations",
                    "priority": "medium",
                    "complexity": "medium",
                    "dependencies": ["F001", "F002", "F003"],
                    "user_value": 6,
                    "technical_risk": 2,
                },
            ],
            "future": [
                {
                    "id": "F006",
                    "name": "Collaborative Editing",
                    "description": "Real-time multi-user editing",
                    "priority": "low",
                    "complexity": "high",
                    "dependencies": ["F001"],
                    "user_value": 5,
                    "technical_risk": 5,
                }
            ],
        }

        # Simulate improvements based on iteration
        if self.iteration > 1:
            # Add more detailed descriptions
            for category in base_features:
                for feature in base_features[category]:
                    feature["description"] += f" (Refined in iteration {self.iteration})"

        if self.iteration > 3:
            # Add new features discovered
            base_features["core"].append(
                {
                    "id": f"F00{6 + self.iteration}",
                    "name": "Intelligent Caching System",
                    "description": "Cache successful patterns for reuse",
                    "priority": "high",
                    "complexity": "medium",
                    "dependencies": ["F002"],
                    "user_value": 7,
                    "technical_risk": 2,
                }
            )

        return base_features

    def optimize_features(
        self, current: Any, new: dict[str, list[dict[str, Any]]], evaluation_result: dict[str, Any]
    ) -> dict[str, list[dict[str, Any]]]:
        """Merge and optimize feature lists based on evaluation"""
        optimized = new.copy()
        
        # Apply suggestions from evaluator
        suggestions = evaluation_result.get("suggestions", [])
        
        # Add optimization history and quality indicators
        for category in optimized:
            for feature in optimized[category]:
                feature["quality_score"] = evaluation_result["overall_score"]
                feature["iteration_added"] = feature.get("iteration_added", self.iteration)
                
                # Mark features that need improvement based on feedback
                feedback = evaluation_result["detailed_feedback"]
                if "High risk" in feedback.get("feasibility", "") and feature["name"] in feedback["feasibility"]:
                    feature["needs_improvement"] = "feasibility"
                elif "Low value" in feedback.get("user_value", "") and feature["name"] in feedback["user_value"]:
                    feature["needs_improvement"] = "user_value"
        
        # Log suggestions for next iteration
        if suggestions:
            logger.info(f"Evaluator suggestions: {suggestions}")

        return optimized

    def has_converged(self) -> bool:
        """Check if optimization has converged"""
        if self.iteration < 5:  # Minimum iterations
            return False

        if len(self.improvement_history) < 3:
            return False

        # Check if improvements are minimal
        recent_scores = [h["quality_score"] for h in self.improvement_history[-3:]]
        improvement_rate = (recent_scores[-1] - recent_scores[0]) / recent_scores[0] if recent_scores[0] > 0 else 0

        converged = improvement_rate < 0.01  # Less than 1% improvement
        
        if converged:
            logger.info(f"Convergence detected: {improvement_rate:.2%} improvement over last 3 iterations")
        
        return converged

    def log_iteration_results(self, evaluation_result: dict[str, Any], iteration_time: float):
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
            "suggestions": evaluation_result["suggestions"][:3],  # Top 3 suggestions
        }

        self.improvement_history.append(result)

        # Save to metrics file
        with open(self.output_path / "metrics.json", "w") as f:
            json.dump(
                {
                    "current": result,
                    "history": self.improvement_history[-10:],  # Keep last 10
                },
                f,
                indent=2,
            )

        logger.info(f"Iteration {self.iteration} complete. Quality: {evaluation_result['overall_score']:.3f} ({evaluation_result['improvement_rate']:+.2%} improvement)")
    
    def save_evaluation_report(self, evaluation_result: dict[str, Any]):
        """Save detailed evaluation report"""
        report = self.evaluator.generate_report(evaluation_result)
        
        # Save to evaluation reports directory
        eval_dir = Path("evaluation_reports")
        eval_dir.mkdir(exist_ok=True)
        
        report_file = eval_dir / f"iteration_{self.iteration:03d}_report.md"
        with open(report_file, "w") as f:
            f.write(report)
            
        # Also save the latest report for easy access
        with open("latest_evaluation.md", "w") as f:
            f.write(report)
            
        logger.info(f"Evaluation report saved to {report_file}")

    def save_checkpoint(self):
        """Save current state"""
        # Save features
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

        logger.info(f"Checkpoint saved for iteration {self.iteration}")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Feature Optimizer")
    parser.add_argument("--watch", action="store_true", help="Run in watch mode")
    parser.add_argument("--reset", action="store_true", help="Reset and start fresh")
    args = parser.parse_args()

    optimizer = FeatureOptimizer()

    if args.reset:
        # Clear existing state
        for f in ["features.json", "metrics.json"]:
            if os.path.exists(f):
                os.remove(f)
        optimizer.iteration = 0
        optimizer.feature_list = []
        logger.info("Reset complete. Starting fresh.")

    try:
        optimizer.run_optimization_loop(watch_mode=args.watch)
    except KeyboardInterrupt:
        logger.info("Optimization stopped by user")
    except Exception as e:
        logger.error(f"Error in optimization: {e}", exc_info=True)


if __name__ == "__main__":
    main()
