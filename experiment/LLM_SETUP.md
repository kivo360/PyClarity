# LLM-Powered Feature Optimizer Setup

This optimizer uses Groq's LLaMA 3.3 70B model to iteratively generate and improve feature lists.

## Prerequisites

1. **Get a Groq API Key**
   - Sign up at https://console.groq.com
   - Create an API key in the dashboard
   - It's free with generous rate limits!

2. **Set Environment Variable**
   ```bash
   export GROQ_API_KEY='your-groq-api-key-here'
   ```

## Running the Optimizer

### Quick Start (5 iterations, 15s sleep)
```bash
./run_llm_optimizer.sh
```

### Custom Configuration
```bash
# More iterations with shorter sleep
./run_llm_optimizer.sh --iterations 10 --sleep 10

# Start fresh (delete previous results)
./run_llm_optimizer.sh --reset

# Help
./run_llm_optimizer.sh --help
```

### Direct Python Usage
```bash
# Basic run
python llm_optimizer.py

# With options
python llm_optimizer.py --iterations 8 --sleep 20 --reset
```

## What to Expect

1. **Iteration 1**: Generates initial feature set based on documentation
2. **Evaluation**: Advanced evaluator scores features on 6 criteria
3. **Optimization**: LLM analyzes scores and improves features
4. **Progress**: Watch quality scores improve each iteration
5. **Convergence**: Stops when improvements plateau (<2%)

## Monitor Progress

Open multiple terminals:

```bash
# Terminal 1: Run optimizer
./run_llm_optimizer.sh

# Terminal 2: Watch features evolve
watch -n 2 'cat features.json | python -m json.tool | head -50'

# Terminal 3: Monitor metrics
watch -n 2 'cat metrics.json | python -m json.tool'

# Terminal 4: View latest evaluation
watch -n 2 'cat latest_evaluation.md'
```

## Output Files

- `features.json` - Current optimized feature list
- `metrics.json` - Quality scores and improvement tracking
- `latest_evaluation.md` - Detailed evaluation report
- `evaluation_reports/` - History of all evaluations
- `history/` - Checkpoint of each iteration

## Why Groq?

- **Fast**: LLaMA 3.3 70B with ultra-low latency
- **Free Tier**: Generous rate limits for experimentation
- **Quality**: Excellent at structured JSON generation
- **Reliable**: Consistent outputs for iterative improvement

## Troubleshooting

1. **No API Key**: Export `GROQ_API_KEY` before running
2. **Rate Limits**: Increase sleep time between iterations
3. **JSON Parsing**: The optimizer handles malformed JSON gracefully
4. **Convergence**: Adjust minimum iterations if needed

## Example Session

```
🚀 Starting LLM-Powered Feature Optimizer
=========================================
Configuration:
  Iterations: 5
  Sleep time: 15s
  Reset: false

2024-01-20 10:30:45.123 | INFO | Starting LLM-powered optimization loop (max 5 iterations)

============================================================
Starting iteration 1
============================================================
🤖 Generating features with LLM...
✅ Generated 25 features
🔧 Optimizing features with LLM based on evaluation...
✅ Features optimized based on evaluation

📊 ITERATION 1 SUMMARY
──────────────────────────────────────────────────
Overall Score: 65.2% (↑ 0.0%)
Total Features: 25

Scores by Criteria:
  • Completeness: 75.0%
  • Clarity: 85.0%
  • Feasibility: 60.0%
  • User_Value: 70.0%
  • Technical_Coherence: 90.0%
  • Innovation: 45.0%

💡 Top Suggestions:
  1. Add more innovative AI-powered features
  2. Reduce complexity of high-risk features
  3. Improve feature descriptions with use cases
──────────────────────────────────────────────────

💤 Sleeping for 15 seconds before next iteration...
```