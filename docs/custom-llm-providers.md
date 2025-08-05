# Using Custom LLM Providers with PyClarity

PyClarity supports any OpenAI-compatible API endpoint, allowing you to use cheaper or faster alternatives to OpenAI and Anthropic.

## Quick Start

Set these environment variables in your `.env` file:

```bash
# Use any OpenAI-compatible API
OPENAI_API_KEY=your-api-key
OPENAI_BASE_URL=https://api.together.xyz/v1
OPENAI_MODEL=mistralai/Mixtral-8x7B-Instruct-v0.1
```

That's it! PyClarity will now use your custom provider for schema generation.

## Supported Providers

### 1. Together AI (Recommended for Cost)
- **Free tier**: $25 free credits on signup
- **Pricing**: ~90% cheaper than OpenAI
- **Models**: Mixtral, Llama 2, CodeLlama, and more

```bash
OPENAI_API_KEY=your-together-api-key
OPENAI_BASE_URL=https://api.together.xyz/v1
OPENAI_MODEL=mistralai/Mixtral-8x7B-Instruct-v0.1
```

Get API key: https://api.together.xyz

### 2. Groq (Recommended for Speed)
- **Free tier**: Available
- **Speed**: 10x faster than traditional inference
- **Models**: Mixtral, Llama 2

```bash
OPENAI_API_KEY=your-groq-api-key
OPENAI_BASE_URL=https://api.groq.com/openai/v1
OPENAI_MODEL=mixtral-8x7b-32768
```

Get API key: https://console.groq.com

### 3. Anyscale Endpoints
- **Pricing**: Pay per token
- **Models**: Llama 2, CodeLlama, Mistral

```bash
OPENAI_API_KEY=your-anyscale-api-key
OPENAI_BASE_URL=https://api.endpoints.anyscale.com/v1
OPENAI_MODEL=meta-llama/Llama-2-70b-chat-hf
```

### 4. OpenRouter
- **Feature**: Access to 100+ models with one API
- **Pricing**: Varies by model

```bash
OPENAI_API_KEY=your-openrouter-api-key
OPENAI_BASE_URL=https://openrouter.ai/api/v1
OPENAI_MODEL=anthropic/claude-3-haiku
```

### 5. Local Models (Free!)

#### vLLM Server
```bash
# Start vLLM server
python -m vllm.entrypoints.openai.api_server \
  --model NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO \
  --port 8000

# Configure PyClarity
OPENAI_API_KEY=dummy-key-for-local
OPENAI_BASE_URL=http://localhost:8000/v1
OPENAI_MODEL=NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO
```

#### FastChat
```bash
# Start FastChat controller
python -m fastchat.serve.controller

# Start model worker
python -m fastchat.serve.model_worker --model-path lmsys/vicuna-13b-v1.5

# Start OpenAI API server
python -m fastchat.serve.openai_api_server --host 0.0.0.0 --port 8001

# Configure PyClarity
OPENAI_API_KEY=dummy-key-for-local
OPENAI_BASE_URL=http://localhost:8001/v1
OPENAI_MODEL=vicuna-13b-v1.5
```

#### Ollama (via LiteLLM proxy)
```bash
# Install and start Ollama
ollama serve
ollama pull mixtral

# Start LiteLLM proxy
litellm --model ollama/mixtral --port 8000

# Configure PyClarity
OPENAI_API_KEY=dummy-key-for-local
OPENAI_BASE_URL=http://localhost:8000
OPENAI_MODEL=mixtral
```

## Testing Your Configuration

Run the demo script to test your configuration:

```bash
python demo_custom_llm_providers.py
```

Or test directly:

```python
import os
os.environ["OPENAI_BASE_URL"] = "https://api.together.xyz/v1"
os.environ["OPENAI_MODEL"] = "mistralai/Mixtral-8x7B-Instruct-v0.1"

# Your existing PyClarity code works without changes!
```

## Cost Comparison

| Provider | Model | Cost per 1M tokens | Speed | Quality |
|----------|-------|-------------------|--------|----------|
| OpenAI | GPT-4 | $30-60 | Medium | Excellent |
| OpenAI | GPT-3.5 | $0.50-2.00 | Fast | Good |
| Together | Mixtral 8x7B | $0.60 | Fast | Very Good |
| Together | Llama 2 70B | $0.90 | Medium | Good |
| Groq | Mixtral 8x7B | $0.27 | Ultra Fast | Very Good |
| Local | Any | $0 | Varies | Varies |

## Choosing a Provider

### For Development
- **Local models**: Free, private, no rate limits
- **Together AI**: Generous free tier, good quality

### For Production
- **Groq**: Fastest inference, good pricing
- **Together AI**: Best balance of cost and quality
- **OpenRouter**: Access to many models with one API

### For Quality
- **OpenAI**: Still the gold standard
- **Anthropic**: Excellent for complex tasks

## Troubleshooting

### "API key invalid"
- Some providers require specific key formats
- For local models, use any dummy key like "sk-local"

### "Model not found"
- Check the exact model name for your provider
- Some providers have specific model naming conventions

### Slow responses
- Local models depend on your hardware
- Consider using quantized models for better performance
- Try Groq for fastest cloud inference

## Advanced Configuration

### Multiple Providers

You can configure fallback providers:

```python
# In your code
providers = [
    ("GROQ_API_KEY", "https://api.groq.com/openai/v1", "mixtral-8x7b-32768"),
    ("TOGETHER_API_KEY", "https://api.together.xyz/v1", "mistralai/Mixtral-8x7B-Instruct-v0.1"),
    ("OPENAI_API_KEY", None, "gpt-3.5-turbo"),  # Fallback to OpenAI
]

for key_var, base_url, model in providers:
    if os.getenv(key_var):
        os.environ["OPENAI_API_KEY"] = os.getenv(key_var)
        if base_url:
            os.environ["OPENAI_BASE_URL"] = base_url
        os.environ["OPENAI_MODEL"] = model
        break
```

### Custom Headers

Some providers require custom headers:

```python
# For providers requiring special headers
import openai

client = openai.AsyncOpenAI(
    api_key=api_key,
    base_url=base_url,
    default_headers={
        "HTTP-Referer": "https://yourapp.com",  # OpenRouter
        "X-Title": "PyClarity Schema Generator",  # OpenRouter
    }
)
```

## Privacy & Security

- **Local models**: Complete privacy, no data leaves your machine
- **Together/Groq**: Check their data policies
- **OpenRouter**: Acts as proxy, check both OpenRouter and model provider policies

## Conclusion

Using custom LLM providers with PyClarity is as simple as setting environment variables. This flexibility allows you to:

- Reduce costs by 90%+ compared to OpenAI
- Run models locally for complete privacy
- Use specialized models for specific tasks
- Switch providers without code changes

Start with Together AI's free tier or run models locally to get started without any costs!