-- Initialize PostgreSQL extensions for PyClarity
-- This script runs automatically when the container is first created

-- Create pgvector extension for vector similarity search
CREATE EXTENSION IF NOT EXISTS vector;

-- Create UUID extension for generating unique IDs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create pg_trgm for text similarity search (optional but useful)
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Grant necessary permissions
GRANT ALL PRIVILEGES ON DATABASE pyclarity TO pyclarity;