# Session State Management for PyClarity

This document describes the session state management system implemented for PyClarity's Progressive Sequential Thinking tool and the automatic schema generation with LLM integration.

## Overview

The session state management system enables:
1. **Progressive Thinking**: Process thoughts one at a time with full session persistence
2. **Database Agnostic**: Support for multiple database backends (AsyncPG, SQLAlchemy, Supabase, etc.)
3. **Automatic Schema Generation**: Generate test examples using available LLMs
4. **Vector Search Ready**: PostgreSQL 17 with pgvector for future similarity search

## Architecture

### Database Abstraction Layer

```
src/pyclarity/db/
├── base.py                 # Abstract base classes and Pydantic models
├── asyncpg_adapter.py      # PostgreSQL implementation with pgvector
└── __init__.py
```

### Schema Generation

```
src/pyclarity/schema_generator/
├── llm_generator.py        # Core LLM integration (OpenAI, Anthropic, Local)
├── auto_detector.py        # Automatic detection and caching
└── __init__.py
```

### Progressive Sequential Thinking

```
src/pyclarity/tools/sequential_thinking/
├── progressive_analyzer.py  # Progressive thought processing
└── models.py               # Thought step types and models
```

## Database Setup

### Using Docker Compose

The easiest way to get started is with the provided Docker Compose configuration:

```bash
# Start PostgreSQL 17 with pgvector
docker-compose up -d postgres

# The database will be available at:
# postgresql://pyclarity:pyclarity@localhost:5432/pyclarity
```

### Manual Setup

If you prefer to use an existing PostgreSQL instance:

1. Ensure PostgreSQL 17+ is installed
2. Install pgvector extension
3. Create database and user:

```sql
CREATE DATABASE pyclarity;
CREATE USER pyclarity WITH PASSWORD 'your-secure-password';
GRANT ALL PRIVILEGES ON DATABASE pyclarity TO pyclarity;

-- Connect to pyclarity database
\c pyclarity

-- Enable pgvector
CREATE EXTENSION IF NOT EXISTS vector;
```

## Environment Configuration

Copy `.env.example` to `.env` and configure:

```bash
# Database
DATABASE_URL=postgresql://pyclarity:pyclarity@localhost:5432/pyclarity

# LLM Provider (choose one or more)
OPENAI_API_KEY=your-key-here
ANTHROPIC_API_KEY=your-key-here
LOCAL_LLM_BASE_URL=http://localhost:11434

# Schema Generation
ENABLE_SCHEMA_GENERATION=true
SCHEMA_GENERATION_EXAMPLES=3
```

## Using Progressive Sequential Thinking

### Basic Usage

```python
from pyclarity.db.asyncpg_adapter import AsyncPGSessionStore, AsyncPGThoughtStore
from pyclarity.tools.sequential_thinking.progressive_analyzer import (
    ProgressiveSequentialThinkingAnalyzer,
    ProgressiveThoughtRequest
)

# Initialize stores
session_store = AsyncPGSessionStore(database_url)
thought_store = AsyncPGThoughtStore(database_url)

# Initialize analyzer
analyzer = ProgressiveSequentialThinkingAnalyzer(
    session_store=session_store,
    thought_store=thought_store
)

# Process first thought
request = ProgressiveThoughtRequest(
    thought="Let me analyze this problem step by step",
    thought_number=1,
    total_thoughts=5,
    next_thought_needed=True
)

response = await analyzer.process_thought(request)
session_id = response.session_id

# Continue with next thought
request = ProgressiveThoughtRequest(
    session_id=session_id,
    thought="Building on the previous analysis...",
    thought_number=2,
    total_thoughts=5,
    next_thought_needed=True
)

response = await analyzer.process_thought(request)
```

### Advanced Features

#### Branching

Create alternative reasoning paths:

```python
response = await analyzer.process_thought(
    ProgressiveThoughtRequest(
        session_id=session_id,
        thought="Alternative hypothesis to explore",
        thought_number=3,
        total_thoughts=7,
        branch_from_thought=2,
        branch_id="alt-hypothesis",
        next_thought_needed=True
    )
)
```

#### Revisions

Revise previous thoughts with new insights:

```python
response = await analyzer.process_thought(
    ProgressiveThoughtRequest(
        session_id=session_id,
        thought="Revised analysis based on new evidence",
        thought_number=4,
        total_thoughts=6,
        is_revision=True,
        revises_thought=2,
        next_thought_needed=True
    )
)
```

## Automatic Schema Generation

### How It Works

1. **Detection**: Automatically detects available LLM providers in order:
   - OpenAI (via OPENAI_API_KEY)
   - Anthropic (via ANTHROPIC_API_KEY)
   - Local LLMs (via LOCAL_LLM_BASE_URL)

2. **Generation**: When a tool is registered, generates realistic test examples

3. **Caching**: Caches generated examples to disk and memory

### Using the Auto Generator

```python
from pyclarity.schema_generator.auto_detector import ensure_schema_examples

# Generate examples for a tool
example = await ensure_schema_examples(
    tool_name="my_tool",
    input_model=MyInputModel,
    output_model=MyOutputModel,
    description="Tool that does X"
)

if example:
    print(f"Generated {len(example.examples)} examples")
    for ex in example.examples:
        print(f"- {ex['example_name']}: {ex['description']}")
```

### Manual Schema Generation

```python
from pyclarity.schema_generator import LLMSchemaGenerator

# Create generator (auto-detects provider)
generator = LLMSchemaGenerator()

# Generate examples
example = await generator.generate_examples(
    tool_name="mental_models",
    input_model=MentalModelsRequest,
    output_model=MentalModelsResponse,
    description="Apply mental models to analyze situations",
    num_examples=5
)
```

## Vector Search (Future)

The database is prepared for vector similarity search:

```python
# Save thought with embedding
embedding = await generate_embedding(thought.content)  # Your embedding function
await thought_store.save_thought_with_embedding(thought, embedding)

# Search similar thoughts
similar = await thought_store.search_similar_thoughts(
    embedding=query_embedding,
    limit=10,
    threshold=0.8,
    session_id=session_id  # Optional: limit to session
)
```

## Database Schema

### Sessions Table

```sql
CREATE TABLE pyclarity_sessions (
    session_id VARCHAR(255) PRIMARY KEY,
    tool_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    metadata JSONB DEFAULT '{}',
    active BOOLEAN DEFAULT TRUE
);
```

### Thoughts Table

```sql
CREATE TABLE pyclarity_thoughts (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,
    thought_number INTEGER NOT NULL,
    total_thoughts INTEGER NOT NULL,
    content TEXT NOT NULL,
    thought_type VARCHAR(50),
    confidence FLOAT DEFAULT 0.85,
    branch_id VARCHAR(255),
    branch_from_thought INTEGER,
    revises_thought INTEGER,
    is_revision BOOLEAN DEFAULT FALSE,
    needs_more_thoughts BOOLEAN DEFAULT FALSE,
    next_thought_needed BOOLEAN DEFAULT TRUE,
    supporting_evidence JSONB DEFAULT '[]',
    assumptions_made JSONB DEFAULT '[]',
    potential_errors JSONB DEFAULT '[]',
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    metadata JSONB DEFAULT '{}',
    embedding vector(1536)  -- For OpenAI embeddings
);
```

## Performance Considerations

1. **Connection Pooling**: AsyncPG uses connection pools by default
2. **Indexes**: Created on frequently queried columns
3. **pgvector Index**: Uses IVFFlat for fast similarity search
4. **Caching**: Schema examples are cached in memory and disk

## Error Handling

The system includes comprehensive error handling:

- Database connection errors
- LLM API failures  
- Invalid thought sequences
- Schema validation errors

All errors are logged and returned with appropriate error messages.

## Testing

Run the test suite:

```bash
# Test progressive thinking
pytest tests/test_progressive_sequential_thinking.py -v

# Test with real database (requires PostgreSQL)
DATABASE_URL=postgresql://test:test@localhost:5432/test pytest tests/integration/
```

## Future Enhancements

1. **Additional Database Adapters**
   - SQLAlchemy for broader database support
   - Supabase native integration
   - Redis for high-performance caching

2. **Enhanced Vector Search**
   - Multiple embedding models
   - Hybrid search (vector + keyword)
   - Clustering and visualization

3. **Advanced Schema Generation**
   - Domain-specific examples
   - Multi-language support
   - Interactive refinement

4. **Session Analytics**
   - Thinking pattern analysis
   - Performance metrics
   - Usage insights