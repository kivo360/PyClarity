"""SQLAlchemy adapter for PyClarity session state management."""

import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    String,
    Text,
    create_engine,
    select,
    update,
    delete,
)
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from pyclarity.db.base import BaseSessionStore, BaseThoughtStore, SessionData, ThoughtData

logger = logging.getLogger(__name__)

Base = declarative_base()


class SessionTable(Base):
    """SQLAlchemy model for sessions."""
    
    __tablename__ = "pyclarity_sessions"
    
    session_id = Column(String(255), primary_key=True)
    tool_name = Column(String(100), nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    metadata = Column(JSON, default={})
    active = Column(Boolean, default=True, index=True)


class ThoughtTable(Base):
    """SQLAlchemy model for thoughts."""
    
    __tablename__ = "pyclarity_thoughts"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(255), nullable=False, index=True)
    thought_number = Column(Integer, nullable=False)
    total_thoughts = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    thought_type = Column(String(50))
    confidence = Column(Float, default=0.85)
    branch_id = Column(String(255), index=True)
    branch_from_thought = Column(Integer)
    revises_thought = Column(Integer)
    is_revision = Column(Boolean, default=False)
    needs_more_thoughts = Column(Boolean, default=False)
    next_thought_needed = Column(Boolean, default=True)
    supporting_evidence = Column(JSON, default=[])
    assumptions_made = Column(JSON, default=[])
    potential_errors = Column(JSON, default=[])
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    metadata = Column(JSON, default={})
    
    # Create index for common queries
    __table_args__ = (
        {"extend_existing": True},
    )


class SQLAlchemySessionStore(BaseSessionStore):
    """SQLAlchemy implementation of session storage."""
    
    def __init__(self, db_url: str, echo: bool = False):
        """Initialize with database URL."""
        self.engine = create_async_engine(db_url, echo=echo)
        self.async_session = async_sessionmaker(self.engine, class_=AsyncSession)
    
    async def init_db(self):
        """Initialize database tables."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    async def create_session(self, session_data: SessionData) -> SessionData:
        """Create a new session."""
        async with self.async_session() as session:
            db_session = SessionTable(
                session_id=session_data.session_id,
                tool_name=session_data.tool_name,
                created_at=session_data.created_at,
                updated_at=session_data.updated_at,
                metadata=session_data.metadata,
                active=session_data.active,
            )
            session.add(db_session)
            await session.commit()
            return session_data
    
    async def get_session(self, session_id: str) -> Optional[SessionData]:
        """Get session by ID."""
        async with self.async_session() as session:
            result = await session.execute(
                select(SessionTable).where(SessionTable.session_id == session_id)
            )
            db_session = result.scalar_one_or_none()
            
            if db_session:
                return SessionData(
                    session_id=db_session.session_id,
                    tool_name=db_session.tool_name,
                    created_at=db_session.created_at,
                    updated_at=db_session.updated_at,
                    metadata=db_session.metadata or {},
                    active=db_session.active,
                )
            return None
    
    async def update_session(self, session_id: str, updates: Dict[str, Any]) -> Optional[SessionData]:
        """Update session data."""
        async with self.async_session() as session:
            stmt = (
                update(SessionTable)
                .where(SessionTable.session_id == session_id)
                .values(**updates, updated_at=datetime.utcnow())
            )
            await session.execute(stmt)
            await session.commit()
            return await self.get_session(session_id)
    
    async def delete_session(self, session_id: str) -> bool:
        """Delete a session."""
        async with self.async_session() as session:
            stmt = delete(SessionTable).where(SessionTable.session_id == session_id)
            result = await session.execute(stmt)
            await session.commit()
            return result.rowcount > 0
    
    async def list_sessions(
        self,
        tool_name: Optional[str] = None,
        active_only: bool = True,
        limit: int = 100,
        offset: int = 0
    ) -> List[SessionData]:
        """List sessions with optional filtering."""
        async with self.async_session() as session:
            query = select(SessionTable)
            
            if tool_name:
                query = query.where(SessionTable.tool_name == tool_name)
            if active_only:
                query = query.where(SessionTable.active == True)
            
            query = query.order_by(SessionTable.created_at.desc()).limit(limit).offset(offset)
            
            result = await session.execute(query)
            sessions = result.scalars().all()
            
            return [
                SessionData(
                    session_id=s.session_id,
                    tool_name=s.tool_name,
                    created_at=s.created_at,
                    updated_at=s.updated_at,
                    metadata=s.metadata or {},
                    active=s.active,
                )
                for s in sessions
            ]
    
    async def cleanup_old_sessions(self, days_old: int = 7) -> int:
        """Clean up sessions older than specified days."""
        async with self.async_session() as session:
            cutoff = datetime.utcnow() - timedelta(days=days_old)
            stmt = delete(SessionTable).where(SessionTable.created_at < cutoff)
            result = await session.execute(stmt)
            await session.commit()
            return result.rowcount


class SQLAlchemyThoughtStore(BaseThoughtStore):
    """SQLAlchemy implementation of thought storage."""
    
    def __init__(self, db_url: str, echo: bool = False):
        """Initialize with database URL."""
        self.engine = create_async_engine(db_url, echo=echo)
        self.async_session = async_sessionmaker(self.engine, class_=AsyncSession)
    
    async def init_db(self):
        """Initialize database tables."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    async def save_thought(self, thought: ThoughtData) -> ThoughtData:
        """Save a new thought."""
        async with self.async_session() as session:
            db_thought = ThoughtTable(
                session_id=thought.session_id,
                thought_number=thought.thought_number,
                total_thoughts=thought.total_thoughts,
                content=thought.content,
                thought_type=thought.thought_type,
                confidence=thought.confidence,
                branch_id=thought.branch_id,
                branch_from_thought=thought.branch_from_thought,
                revises_thought=thought.revises_thought,
                is_revision=thought.is_revision,
                needs_more_thoughts=thought.needs_more_thoughts,
                next_thought_needed=thought.next_thought_needed,
                supporting_evidence=thought.supporting_evidence,
                assumptions_made=thought.assumptions_made,
                potential_errors=thought.potential_errors,
                created_at=thought.created_at,
                metadata=thought.metadata,
            )
            session.add(db_thought)
            await session.commit()
            await session.refresh(db_thought)
            
            thought.id = db_thought.id
            return thought
    
    async def get_thought(self, thought_id: int) -> Optional[ThoughtData]:
        """Get a thought by ID."""
        async with self.async_session() as session:
            result = await session.execute(
                select(ThoughtTable).where(ThoughtTable.id == thought_id)
            )
            db_thought = result.scalar_one_or_none()
            
            if db_thought:
                return self._to_thought_data(db_thought)
            return None
    
    async def get_session_thoughts(
        self,
        session_id: str,
        branch_id: Optional[str] = None
    ) -> List[ThoughtData]:
        """Get all thoughts for a session, optionally filtered by branch."""
        async with self.async_session() as session:
            query = select(ThoughtTable).where(ThoughtTable.session_id == session_id)
            
            if branch_id is not None:
                if branch_id:
                    query = query.where(ThoughtTable.branch_id == branch_id)
                else:
                    query = query.where(ThoughtTable.branch_id.is_(None))
            
            query = query.order_by(ThoughtTable.thought_number)
            
            result = await session.execute(query)
            thoughts = result.scalars().all()
            
            return [self._to_thought_data(t) for t in thoughts]
    
    async def get_latest_thought(
        self,
        session_id: str,
        branch_id: Optional[str] = None
    ) -> Optional[ThoughtData]:
        """Get the most recent thought for a session/branch."""
        async with self.async_session() as session:
            query = select(ThoughtTable).where(ThoughtTable.session_id == session_id)
            
            if branch_id is not None:
                if branch_id:
                    query = query.where(ThoughtTable.branch_id == branch_id)
                else:
                    query = query.where(ThoughtTable.branch_id.is_(None))
            
            query = query.order_by(ThoughtTable.thought_number.desc()).limit(1)
            
            result = await session.execute(query)
            db_thought = result.scalar_one_or_none()
            
            if db_thought:
                return self._to_thought_data(db_thought)
            return None
    
    async def update_thought(self, thought_id: int, updates: Dict[str, Any]) -> Optional[ThoughtData]:
        """Update an existing thought."""
        async with self.async_session() as session:
            stmt = (
                update(ThoughtTable)
                .where(ThoughtTable.id == thought_id)
                .values(**updates)
            )
            await session.execute(stmt)
            await session.commit()
            return await self.get_thought(thought_id)
    
    async def delete_thought(self, thought_id: int) -> bool:
        """Delete a thought."""
        async with self.async_session() as session:
            stmt = delete(ThoughtTable).where(ThoughtTable.id == thought_id)
            result = await session.execute(stmt)
            await session.commit()
            return result.rowcount > 0
    
    async def count_session_thoughts(self, session_id: str) -> int:
        """Count thoughts in a session."""
        async with self.async_session() as session:
            query = select(ThoughtTable).where(ThoughtTable.session_id == session_id)
            result = await session.execute(query)
            return len(result.scalars().all())
    
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
        async with self.async_session() as session:
            query = select(ThoughtTable)
            
            if session_id:
                query = query.where(ThoughtTable.session_id == session_id)
            if content_query:
                query = query.where(ThoughtTable.content.contains(content_query))
            if thought_type:
                query = query.where(ThoughtTable.thought_type == thought_type)
            if min_confidence is not None:
                query = query.where(ThoughtTable.confidence >= min_confidence)
            
            query = query.order_by(ThoughtTable.created_at.desc()).limit(limit)
            
            result = await session.execute(query)
            thoughts = result.scalars().all()
            
            return [self._to_thought_data(t) for t in thoughts]
    
    def _to_thought_data(self, db_thought: ThoughtTable) -> ThoughtData:
        """Convert database model to Pydantic model."""
        return ThoughtData(
            id=db_thought.id,
            session_id=db_thought.session_id,
            thought_number=db_thought.thought_number,
            total_thoughts=db_thought.total_thoughts,
            content=db_thought.content,
            thought_type=db_thought.thought_type,
            confidence=db_thought.confidence,
            branch_id=db_thought.branch_id,
            branch_from_thought=db_thought.branch_from_thought,
            revises_thought=db_thought.revises_thought,
            is_revision=db_thought.is_revision,
            needs_more_thoughts=db_thought.needs_more_thoughts,
            next_thought_needed=db_thought.next_thought_needed,
            supporting_evidence=db_thought.supporting_evidence or [],
            assumptions_made=db_thought.assumptions_made or [],
            potential_errors=db_thought.potential_errors or [],
            created_at=db_thought.created_at,
            metadata=db_thought.metadata or {},
        )