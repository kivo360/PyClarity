"""AsyncPG adapter for PyClarity session state management."""

import json
import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import asyncpg

from pyclarity.db.base import BaseSessionStore, BaseThoughtStore, SessionData, ThoughtData

logger = logging.getLogger(__name__)


class AsyncPGSessionStore(BaseSessionStore):
    """AsyncPG implementation of session storage."""
    
    def __init__(self, dsn: str):
        """Initialize with PostgreSQL connection string."""
        self.dsn = dsn
        self.pool: Optional[asyncpg.Pool] = None
    
    async def init_db(self):
        """Initialize database connection pool and create tables."""
        self.pool = await asyncpg.create_pool(self.dsn)
        
        # Create pgvector extension if not exists (PostgreSQL 17+ with pgvector)
        try:
            await self.pool.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            logger.info("pgvector extension enabled")
        except Exception as e:
            logger.warning(f"Could not enable pgvector: {e}")
        
        # Create sessions table
        await self.pool.execute("""
            CREATE TABLE IF NOT EXISTS pyclarity_sessions (
                session_id VARCHAR(255) PRIMARY KEY,
                tool_name VARCHAR(100) NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
                metadata JSONB DEFAULT '{}',
                active BOOLEAN DEFAULT TRUE
            );
            
            CREATE INDEX IF NOT EXISTS idx_sessions_tool_name ON pyclarity_sessions(tool_name);
            CREATE INDEX IF NOT EXISTS idx_sessions_active ON pyclarity_sessions(active);
        """)
    
    async def close(self):
        """Close the connection pool."""
        if self.pool:
            await self.pool.close()
    
    async def create_session(self, session_data: SessionData) -> SessionData:
        """Create a new session."""
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO pyclarity_sessions 
                (session_id, tool_name, created_at, updated_at, metadata, active)
                VALUES ($1, $2, $3, $4, $5, $6)
            """, 
            session_data.session_id,
            session_data.tool_name,
            session_data.created_at,
            session_data.updated_at,
            json.dumps(session_data.metadata),
            session_data.active
            )
            return session_data
    
    async def get_session(self, session_id: str) -> Optional[SessionData]:
        """Get session by ID."""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM pyclarity_sessions WHERE session_id = $1",
                session_id
            )
            
            if row:
                return SessionData(
                    session_id=row['session_id'],
                    tool_name=row['tool_name'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at'],
                    metadata=json.loads(row['metadata']) if row['metadata'] else {},
                    active=row['active']
                )
            return None
    
    async def update_session(self, session_id: str, updates: Dict[str, Any]) -> Optional[SessionData]:
        """Update session data."""
        # Build update query dynamically
        set_clauses = []
        values = []
        param_count = 1
        
        for key, value in updates.items():
            if key == 'metadata':
                set_clauses.append(f"{key} = ${param_count}")
                values.append(json.dumps(value))
            else:
                set_clauses.append(f"{key} = ${param_count}")
                values.append(value)
            param_count += 1
        
        # Always update updated_at
        set_clauses.append(f"updated_at = ${param_count}")
        values.append(datetime.now(timezone.utc))
        param_count += 1
        
        values.append(session_id)  # For WHERE clause
        
        query = f"""
            UPDATE pyclarity_sessions 
            SET {', '.join(set_clauses)}
            WHERE session_id = ${param_count}
            RETURNING *
        """
        
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, *values)
            if row:
                return SessionData(
                    session_id=row['session_id'],
                    tool_name=row['tool_name'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at'],
                    metadata=json.loads(row['metadata']) if row['metadata'] else {},
                    active=row['active']
                )
            return None
    
    async def delete_session(self, session_id: str) -> bool:
        """Delete a session."""
        async with self.pool.acquire() as conn:
            result = await conn.execute(
                "DELETE FROM pyclarity_sessions WHERE session_id = $1",
                session_id
            )
            return result.split()[-1] != '0'
    
    async def list_sessions(
        self,
        tool_name: Optional[str] = None,
        active_only: bool = True,
        limit: int = 100,
        offset: int = 0
    ) -> List[SessionData]:
        """List sessions with optional filtering."""
        query = "SELECT * FROM pyclarity_sessions WHERE 1=1"
        params = []
        param_count = 1
        
        if tool_name:
            query += f" AND tool_name = ${param_count}"
            params.append(tool_name)
            param_count += 1
        
        if active_only:
            query += f" AND active = ${param_count}"
            params.append(True)
            param_count += 1
        
        query += f" ORDER BY created_at DESC LIMIT ${param_count} OFFSET ${param_count + 1}"
        params.extend([limit, offset])
        
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, *params)
            
            return [
                SessionData(
                    session_id=row['session_id'],
                    tool_name=row['tool_name'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at'],
                    metadata=json.loads(row['metadata']) if row['metadata'] else {},
                    active=row['active']
                )
                for row in rows
            ]
    
    async def cleanup_old_sessions(self, days_old: int = 7) -> int:
        """Clean up sessions older than specified days."""
        cutoff = datetime.now(timezone.utc) - timedelta(days=days_old)
        
        async with self.pool.acquire() as conn:
            result = await conn.execute(
                "DELETE FROM pyclarity_sessions WHERE created_at < $1",
                cutoff
            )
            return int(result.split()[-1])


class AsyncPGThoughtStore(BaseThoughtStore):
    """AsyncPG implementation of thought storage."""
    
    def __init__(self, dsn: str):
        """Initialize with PostgreSQL connection string."""
        self.dsn = dsn
        self.pool: Optional[asyncpg.Pool] = None
    
    async def init_db(self):
        """Initialize database connection pool and create tables."""
        self.pool = await asyncpg.create_pool(self.dsn)
        
        # Create pgvector extension if not exists (PostgreSQL 17+ with pgvector)
        try:
            await self.pool.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            logger.info("pgvector extension enabled")
        except Exception as e:
            logger.warning(f"Could not enable pgvector: {e}")
        
        # Create thoughts table with all necessary columns including vector support
        await self.pool.execute("""
            CREATE TABLE IF NOT EXISTS pyclarity_thoughts (
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
                -- Vector embedding for similarity search (1536 dimensions for OpenAI embeddings)
                embedding vector(1536)
            );
            
            CREATE INDEX IF NOT EXISTS idx_thoughts_session_id ON pyclarity_thoughts(session_id);
            CREATE INDEX IF NOT EXISTS idx_thoughts_branch_id ON pyclarity_thoughts(branch_id);
            CREATE INDEX IF NOT EXISTS idx_thoughts_session_number ON pyclarity_thoughts(session_id, thought_number);
            
            -- Create HNSW index for fast similarity search (if pgvector supports it)
            CREATE INDEX IF NOT EXISTS idx_thoughts_embedding ON pyclarity_thoughts 
            USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
        """)
    
    async def close(self):
        """Close the connection pool."""
        if self.pool:
            await self.pool.close()
    
    async def save_thought(self, thought: ThoughtData) -> ThoughtData:
        """Save a new thought."""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("""
                INSERT INTO pyclarity_thoughts 
                (session_id, thought_number, total_thoughts, content, thought_type,
                 confidence, branch_id, branch_from_thought, revises_thought,
                 is_revision, needs_more_thoughts, next_thought_needed,
                 supporting_evidence, assumptions_made, potential_errors,
                 created_at, metadata)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17)
                RETURNING id
            """,
            thought.session_id,
            thought.thought_number,
            thought.total_thoughts,
            thought.content,
            thought.thought_type,
            thought.confidence,
            thought.branch_id,
            thought.branch_from_thought,
            thought.revises_thought,
            thought.is_revision,
            thought.needs_more_thoughts,
            thought.next_thought_needed,
            json.dumps(thought.supporting_evidence),
            json.dumps(thought.assumptions_made),
            json.dumps(thought.potential_errors),
            thought.created_at,
            json.dumps(thought.metadata)
            )
            
            thought.id = row['id']
            return thought
    
    async def get_thought(self, thought_id: int) -> Optional[ThoughtData]:
        """Get a thought by ID."""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM pyclarity_thoughts WHERE id = $1",
                thought_id
            )
            
            if row:
                return self._row_to_thought(row)
            return None
    
    async def get_session_thoughts(
        self,
        session_id: str,
        branch_id: Optional[str] = None
    ) -> List[ThoughtData]:
        """Get all thoughts for a session, optionally filtered by branch."""
        query = "SELECT * FROM pyclarity_thoughts WHERE session_id = $1"
        params = [session_id]
        
        if branch_id is not None:
            if branch_id:
                query += " AND branch_id = $2"
                params.append(branch_id)
            else:
                query += " AND branch_id IS NULL"
        
        query += " ORDER BY thought_number"
        
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, *params)
            return [self._row_to_thought(row) for row in rows]
    
    async def get_latest_thought(
        self,
        session_id: str,
        branch_id: Optional[str] = None
    ) -> Optional[ThoughtData]:
        """Get the most recent thought for a session/branch."""
        query = "SELECT * FROM pyclarity_thoughts WHERE session_id = $1"
        params = [session_id]
        
        if branch_id is not None:
            if branch_id:
                query += " AND branch_id = $2"
                params.append(branch_id)
            else:
                query += " AND branch_id IS NULL"
        
        query += " ORDER BY thought_number DESC LIMIT 1"
        
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, *params)
            if row:
                return self._row_to_thought(row)
            return None
    
    async def update_thought(self, thought_id: int, updates: Dict[str, Any]) -> Optional[ThoughtData]:
        """Update an existing thought."""
        # Build update query dynamically
        set_clauses = []
        values = []
        param_count = 1
        
        for key, value in updates.items():
            if key in ['supporting_evidence', 'assumptions_made', 'potential_errors', 'metadata']:
                set_clauses.append(f"{key} = ${param_count}")
                values.append(json.dumps(value))
            else:
                set_clauses.append(f"{key} = ${param_count}")
                values.append(value)
            param_count += 1
        
        values.append(thought_id)  # For WHERE clause
        
        query = f"""
            UPDATE pyclarity_thoughts 
            SET {', '.join(set_clauses)}
            WHERE id = ${param_count}
            RETURNING *
        """
        
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, *values)
            if row:
                return self._row_to_thought(row)
            return None
    
    async def delete_thought(self, thought_id: int) -> bool:
        """Delete a thought."""
        async with self.pool.acquire() as conn:
            result = await conn.execute(
                "DELETE FROM pyclarity_thoughts WHERE id = $1",
                thought_id
            )
            return result.split()[-1] != '0'
    
    async def count_session_thoughts(self, session_id: str) -> int:
        """Count thoughts in a session."""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT COUNT(*) as count FROM pyclarity_thoughts WHERE session_id = $1",
                session_id
            )
            return row['count']
    
    async def get_branch_thoughts(self, session_id: str, branch_id: str) -> List[ThoughtData]:
        """Get all thoughts for a specific branch."""
        return await self.get_session_thoughts(session_id, branch_id)
    
    async def search_thoughts(
        self,
        session_id: Optional[str] = None,
        content_query: Optional[str] = None,
        thought_type: Optional[str] = None,
        min_confidence: Optional[float] = None,
        limit: int = 100
    ) -> List[ThoughtData]:
        """Search thoughts with various filters."""
        query = "SELECT * FROM pyclarity_thoughts WHERE 1=1"
        params = []
        param_count = 1
        
        if session_id:
            query += f" AND session_id = ${param_count}"
            params.append(session_id)
            param_count += 1
        
        if content_query:
            query += f" AND content ILIKE ${param_count}"
            params.append(f"%{content_query}%")
            param_count += 1
        
        if thought_type:
            query += f" AND thought_type = ${param_count}"
            params.append(thought_type)
            param_count += 1
        
        if min_confidence is not None:
            query += f" AND confidence >= ${param_count}"
            params.append(min_confidence)
            param_count += 1
        
        query += f" ORDER BY created_at DESC LIMIT ${param_count}"
        params.append(limit)
        
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, *params)
            return [self._row_to_thought(row) for row in rows]
    
    async def search_similar_thoughts(
        self,
        embedding: List[float],
        limit: int = 10,
        threshold: float = 0.8,
        session_id: Optional[str] = None
    ) -> List[ThoughtData]:
        """Search for similar thoughts using vector similarity."""
        query = """
            SELECT *, 1 - (embedding <=> $1::vector) as similarity
            FROM pyclarity_thoughts
            WHERE embedding IS NOT NULL
        """
        params = [embedding]
        param_count = 2
        
        if session_id:
            query += f" AND session_id = ${param_count}"
            params.append(session_id)
            param_count += 1
        
        query += f" AND 1 - (embedding <=> $1::vector) > ${param_count}"
        params.append(threshold)
        param_count += 1
        
        query += f" ORDER BY embedding <=> $1::vector LIMIT ${param_count}"
        params.append(limit)
        
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, *params)
            return [self._row_to_thought(row) for row in rows]
    
    async def save_thought_with_embedding(
        self, 
        thought: ThoughtData,
        embedding: Optional[List[float]] = None
    ) -> ThoughtData:
        """Save thought with optional embedding."""
        async with self.pool.acquire() as conn:
            if embedding:
                # Save with embedding
                row = await conn.fetchrow("""
                    INSERT INTO pyclarity_thoughts 
                    (session_id, thought_number, total_thoughts, content, thought_type,
                     confidence, branch_id, branch_from_thought, revises_thought,
                     is_revision, needs_more_thoughts, next_thought_needed,
                     supporting_evidence, assumptions_made, potential_errors,
                     created_at, metadata, embedding)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18::vector)
                    RETURNING id
                """,
                thought.session_id,
                thought.thought_number,
                thought.total_thoughts,
                thought.content,
                thought.thought_type,
                thought.confidence,
                thought.branch_id,
                thought.branch_from_thought,
                thought.revises_thought,
                thought.is_revision,
                thought.needs_more_thoughts,
                thought.next_thought_needed,
                json.dumps(thought.supporting_evidence),
                json.dumps(thought.assumptions_made),
                json.dumps(thought.potential_errors),
                thought.created_at,
                json.dumps(thought.metadata),
                embedding
                )
            else:
                # Save without embedding (use existing save_thought method)
                return await self.save_thought(thought)
            
            thought.id = row['id']
            return thought
    
    def _row_to_thought(self, row: asyncpg.Record) -> ThoughtData:
        """Convert database row to ThoughtData."""
        return ThoughtData(
            id=row['id'],
            session_id=row['session_id'],
            thought_number=row['thought_number'],
            total_thoughts=row['total_thoughts'],
            content=row['content'],
            thought_type=row['thought_type'],
            confidence=row['confidence'],
            branch_id=row['branch_id'],
            branch_from_thought=row['branch_from_thought'],
            revises_thought=row['revises_thought'],
            is_revision=row['is_revision'],
            needs_more_thoughts=row['needs_more_thoughts'],
            next_thought_needed=row['next_thought_needed'],
            supporting_evidence=json.loads(row['supporting_evidence']) if row['supporting_evidence'] else [],
            assumptions_made=json.loads(row['assumptions_made']) if row['assumptions_made'] else [],
            potential_errors=json.loads(row['potential_errors']) if row['potential_errors'] else [],
            created_at=row['created_at'],
            metadata=json.loads(row['metadata']) if row['metadata'] else {},
        )