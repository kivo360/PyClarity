#!/bin/bash

# Enhanced LLM Optimizer with High Variance

echo "🚀 Starting Enhanced LLM Optimizer (High Variance Mode)"
echo "======================================================"

# Check if GROQ_API_KEY is set
if [ -z "$GROQ_API_KEY" ]; then
    echo "❌ Error: GROQ_API_KEY not set"
    echo "Please export your API key:"
    echo "  export GROQ_API_KEY='your-key-here'"
    exit 1
fi

# Default values
ITERATIONS=8
SLEEP=12
RESET=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --iterations)
            ITERATIONS="$2"
            shift 2
            ;;
        --sleep)
            SLEEP="$2"
            shift 2
            ;;
        --reset)
            RESET=true
            shift
            ;;
        --help)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  --iterations N   Number of iterations (default: 8)"
            echo "  --sleep N       Seconds between iterations (default: 12)"
            echo "  --reset         Start fresh (delete previous results)"
            echo "  --help          Show this help"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

echo "Configuration:"
echo "  Iterations: $ITERATIONS"
echo "  Sleep time: ${SLEEP}s"
echo "  Reset: $RESET"
echo ""
echo "Features:"
echo "  ✨ Dynamic temperature adjustment"
echo "  🎲 Multiple model rotation"
echo "  🎯 Strategic variation per iteration"
echo "  🔥 Anti-stuck mechanisms"
echo ""

# Run the enhanced optimizer
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ "$RESET" = true ]; then
    python "$SCRIPT_DIR/llm_optimizer_enhanced.py" --reset --iterations "$ITERATIONS" --sleep "$SLEEP"
else
    python "$SCRIPT_DIR/llm_optimizer_enhanced.py" --iterations "$ITERATIONS" --sleep "$SLEEP"
fi