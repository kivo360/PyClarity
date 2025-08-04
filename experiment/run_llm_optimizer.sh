#!/bin/bash

# LLM-Powered Feature Optimizer Launcher

echo "🚀 Starting LLM-Powered Feature Optimizer"
echo "========================================="

# Check if GROQ_API_KEY is set
if [ -z "$GROQ_API_KEY" ]; then
    echo "❌ Error: GROQ_API_KEY not set"
    echo "Please export your API key:"
    echo "  export GROQ_API_KEY='your-key-here'"
    exit 1
fi

# Default values
ITERATIONS=5
SLEEP=15
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
            echo "  --iterations N   Number of iterations (default: 5)"
            echo "  --sleep N       Seconds between iterations (default: 15)"
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

# Run the optimizer from the script's directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ "$RESET" = true ]; then
    python "$SCRIPT_DIR/llm_optimizer.py" --reset --iterations "$ITERATIONS" --sleep "$SLEEP"
else
    python "$SCRIPT_DIR/llm_optimizer.py" --iterations "$ITERATIONS" --sleep "$SLEEP"
fi