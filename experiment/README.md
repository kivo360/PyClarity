# Feature Optimizer Experiment

This is a self-improving loop that generates and refines feature lists for our AI prompting framework.

## LLM-Powered Optimizer

For advanced optimization using Groq's LLMs, we offer two versions:

### Standard LLM Optimizer
Uses consistent temperature and single model:
```bash
# Set your Groq API key (get one at https://console.groq.com)
export GROQ_API_KEY='your-api-key-here'

# Run the standard optimizer
./run_llm_optimizer.sh
```

### Enhanced Optimizer (Recommended)
Features dynamic variance mechanisms for better exploration:
```bash
# Run the enhanced optimizer with high variance
./run_enhanced.sh

# Custom settings
./run_enhanced.sh --iterations 10 --sleep 12 --reset
```

**Enhanced Features:**
- 🌡️ Dynamic temperature (0.5-1.0)
- 🎲 Multi-model rotation (3 models)
- 🎯 Strategic variation per iteration
- 🔥 Anti-stuck mechanisms
- 📈 15-25% variance between iterations

See `LLM_SETUP.md` for setup and `VARIANCE_GUIDE.md` for variance mechanisms.

## Quick Start

### 1. Run a single iteration
```bash
python optimizer.py
```

### 2. Run in watch mode (continuous)
```bash
python optimizer.py --watch
```

### 3. Reset and start fresh
```bash
python optimizer.py --reset
```

## Development Dependencies

This project requires YAML processing for reading configuration files. You can satisfy this requirement in **one** of the following ways:

1. Install the standalone [`yq`](https://github.com/mikefarah/yq) CLI:
   ```bash
   uv add --dev yq
   ```
2. Install the [`PyYAML`](https://pyyaml.org/) Python package (used when invoking the optimizer from Python):
   ```bash
   uv add --dev pyyaml
   ```

Both commands add the dependency to the *development* group following uv’s recommended workflow, keeping production builds lean.

## Monitoring

Open multiple terminals to watch the optimization in real-time:

### Terminal 1: Run the optimizer
```bash
python optimizer.py --watch
```

### Terminal 2: Watch features evolve
```bash
watch -n 1 'cat features.json | python -m json.tool'
```

### Terminal 3: Monitor metrics
```bash
watch -n 1 'cat metrics.json | python -m json.tool'
```

### Terminal 4: Tail logs
```bash
tail -f logs/optimizer.log
```

## File Structure

```
experiment/
├── optimizer.py          # Main optimization loop
├── evaluator.py          # Advanced feature evaluator
├── features.json         # Current feature list
├── metrics.json          # Real-time metrics
├── optimizer_config.yaml # Configuration
├── latest_evaluation.md  # Most recent evaluation report
├── evaluation_reports/   # Detailed evaluation reports
│   ├── iteration_012_report.md
│   └── ...
├── history/              # Iteration checkpoints
│   ├── iteration_001.json
│   ├── iteration_002.json
│   └── ...
└── logs/                 # Detailed logs
    └── optimizer.log
```

## How It Works

1. **Loads documentation** from `../docs/ai-prompting-techniques/`
2. **Chunks documents** into processable pieces
3. **Generates features** based on documentation content
4. **Evaluates quality** using advanced evaluator with 6 criteria:
   - **Completeness** (25% weight): Coverage of all necessary feature categories
   - **Clarity** (15% weight): Clear, unambiguous feature descriptions
   - **Feasibility** (20% weight): Technical feasibility and resource requirements
   - **User Value** (20% weight): Value delivered to end users
   - **Technical Coherence** (10% weight): Dependencies and integration consistency
   - **Innovation** (10% weight): Novel approaches and differentiation
5. **Optimizes** the feature list based on evaluator suggestions
6. **Saves checkpoint** and generates detailed evaluation reports

## Output Format

### features.json
```json
{
  "iteration": 5,
  "timestamp": "2024-01-20T10:30:00",
  "features": {
    "core": [...],
    "supporting": [...],
    "future": [...]
  }
}
```

### metrics.json
```json
{
  "current": {
    "iteration": 5,
    "quality_score": 0.87,
    "total_features": 15,
    "iteration_time": 12.5
  },
  "history": [...]
}
```

## Advanced Evaluator

The integrated evaluator (`evaluator.py`) provides:

- **Weighted Multi-Criteria Evaluation**: 6 criteria with specific weights
- **Detailed Feedback**: Specific issues identified for each criterion
- **Actionable Suggestions**: Prioritized improvement recommendations
- **Quality Matrix**: Comprehensive quality indicators for all features
- **Progress Tracking**: Improvement rate calculation across iterations
- **Human-Readable Reports**: Markdown reports for each iteration

### Running the Evaluator Standalone

```bash
python evaluator.py  # Evaluates current features.json
```

## Notes

- The optimizer simulates LLM calls for now (replace `generate_features()` with actual LLM integration)
- Features improve with each iteration based on evaluator suggestions
- Convergence is detected when improvement rate < 1%
- Minimum 5 iterations before convergence check
- Each iteration generates a detailed evaluation report with specific improvement areas