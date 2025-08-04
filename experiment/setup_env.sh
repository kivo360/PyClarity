#!/bin/bash

echo "🔧 LLM Optimizer Environment Setup"
echo "=================================="

# Check if GROQ_API_KEY is already set
if [ -n "$GROQ_API_KEY" ]; then
    echo "✅ GROQ_API_KEY is already set"
    echo "Current value: ${GROQ_API_KEY:0:10}..."
else
    echo "❌ GROQ_API_KEY is not set"
    echo ""
    echo "To set up your API key:"
    echo "1. Get a free API key from https://console.groq.com"
    echo "2. Run one of these commands:"
    echo ""
    echo "   # Temporary (for current session):"
    echo "   export GROQ_API_KEY='your-api-key-here'"
    echo ""
    echo "   # Permanent (add to your shell profile):"
    echo "   echo \"export GROQ_API_KEY='your-api-key-here'\" >> ~/.zshrc"
    echo "   source ~/.zshrc"
    echo ""
    echo "3. Then run: ./run_llm_optimizer.sh"
fi

echo ""
echo "📋 Quick test:"
if [ -n "$GROQ_API_KEY" ]; then
    echo "✅ Ready to run optimizer"
else
    echo "❌ Please set GROQ_API_KEY first"
fi 