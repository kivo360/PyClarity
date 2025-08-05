"""
In-memory store implementations for testing and single-use cases.

These stores don't persist data and are perfect for demos and testing.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from pyclarity.db.base import BaseSessionStore, BaseThoughtStore, SessionData, ThoughtData


class MemorySessionStore(BaseSessionStore):
    """In-memory session store."""
    
    def __init__(self):
        self._sessions: Dict[str, SessionData] = {}
        self._next_id = 1
    
    async def create_session(self, session_data: SessionData) -> SessionData:
        """Create a new session."""
        # No id field in SessionData - use session_id as key
        self._sessions[session_data.session_id] = session_data
        return session_data
    
    async def get_session(self, session_id: str) -> Optional[SessionData]:
        """Get a session by ID."""
        return self._sessions.get(session_id)
    
    async def update_session(self, session_id: str, updates: Dict[str, Any]) -> Optional[SessionData]:
        """Update an existing session."""
        if session_id in self._sessions:
            session = self._sessions[session_id]
            for field, value in updates.items():
                if hasattr(session, field):
                    setattr(session, field, value)
            session.updated_at = datetime.now(timezone.utc)
            return session
        return None
    
    async def list_sessions(
        self,
        tool_name: Optional[str] = None,
        user_id: Optional[str] = None,
        active_only: bool = False,
        limit: int = 100,
        offset: int = 0
    ) -> List[SessionData]:
        """List sessions with optional filtering."""
        sessions = list(self._sessions.values())
        
        # Apply filters
        if tool_name:
            sessions = [s for s in sessions if s.tool_name == tool_name]
        if user_id:
            sessions = [s for s in sessions if s.user_id == user_id]
        if active_only:
            sessions = [s for s in sessions if s.is_active]
        
        # Sort by created_at descending
        sessions.sort(key=lambda s: s.created_at, reverse=True)
        
        # Apply pagination
        return sessions[offset:offset + limit]
    
    async def delete_session(self, session_id: str) -> bool:
        """Delete a session."""
        if session_id in self._sessions:
            del self._sessions[session_id]
            return True
        return False
    
    async def cleanup_old_sessions(self, days_old: int = 7) -> int:
        """Clean up sessions older than specified days."""
        from datetime import timedelta
        cutoff = datetime.now(timezone.utc) - timedelta(days=days_old)
        
        to_delete = [
            session_id for session_id, session in self._sessions.items()
            if session.created_at < cutoff
        ]
        
        for session_id in to_delete:
            del self._sessions[session_id]
        
        return len(to_delete)


class MemoryThoughtStore(BaseThoughtStore):
    """In-memory thought store."""
    
    def __init__(self):
        self._thoughts: Dict[str, ThoughtData] = {}
        self._next_id = 1
    
    async def save_thought(self, thought_data: ThoughtData) -> ThoughtData:
        """Save a new thought."""
        thought_data.id = self._next_id
        self._next_id += 1
        key = f"{thought_data.session_id}:{thought_data.step_number}"
        self._thoughts[key] = thought_data
        return thought_data
    
    async def get_thought(self, thought_id: int) -> Optional[ThoughtData]:
        """Get a specific thought by ID."""
        for thought in self._thoughts.values():
            if thought.id == thought_id:
                return thought
        return None
    
    async def get_thought_by_step(self, session_id: str, step_number: int) -> Optional[ThoughtData]:
        """Get a specific thought by session and step."""
        key = f"{session_id}:{step_number}"
        return self._thoughts.get(key)
    
    async def get_session_thoughts(self, session_id: str, branch_id: Optional[str] = None) -> List[ThoughtData]:
        """Get all thoughts for a session."""
        thoughts = [
            t for t in self._thoughts.values()
            if t.session_id == session_id and (branch_id is None or t.branch_id == branch_id)
        ]
        thoughts.sort(key=lambda t: t.thought_number)
        return thoughts
    
    async def get_latest_thought(self, session_id: str) -> Optional[ThoughtData]:
        """Get the latest thought for a session."""
        thoughts = await self.get_session_thoughts(session_id)
        return thoughts[-1] if thoughts else None
    
    async def search_thoughts(
        self,
        query: str,
        session_id: Optional[str] = None,
        limit: int = 100
    ) -> List[ThoughtData]:
        """Search thoughts containing query text."""
        thoughts = list(self._thoughts.values())
        
        # Filter by session if specified
        if session_id:
            thoughts = [t for t in thoughts if t.session_id == session_id]
        
        # Simple text search
        query_lower = query.lower()
        thoughts = [
            t for t in thoughts
            if query_lower in t.thought_content.lower() or
               query_lower in t.initial_query.lower()
        ]
        
        # Sort by timestamp descending
        thoughts.sort(key=lambda t: t.timestamp, reverse=True)
        
        return thoughts[:limit]
    
    async def delete_session_thoughts(self, session_id: str) -> int:
        """Delete all thoughts for a session."""
        to_delete = [
            key for key, thought in self._thoughts.items()
            if thought.session_id == session_id
        ]
        for key in to_delete:
            del self._thoughts[key]
        return len(to_delete)
    
    async def update_thought(self, thought_id: int, updates: Dict[str, Any]) -> Optional[ThoughtData]:
        """Update a thought by ID."""
        # Find thought by ID
        for key, thought in self._thoughts.items():
            if thought.id == thought_id:
                # Apply updates
                for field, value in updates.items():
                    if hasattr(thought, field):
                        setattr(thought, field, value)
                return thought
        return None
    
    async def delete_thought(self, thought_id: int) -> bool:
        """Delete a thought by ID."""
        for key, thought in list(self._thoughts.items()):
            if thought.id == thought_id:
                del self._thoughts[key]
                return True
        return False
    
    async def count_session_thoughts(self, session_id: str) -> int:
        """Count thoughts in a session."""
        return len([t for t in self._thoughts.values() if t.session_id == session_id])
    
    async def get_branch_thoughts(self, session_id: str, branch_id: str) -> List[ThoughtData]:
        """Get thoughts for a specific branch."""
        thoughts = [
            t for t in self._thoughts.values()
            if t.session_id == session_id and t.branch_id == branch_id
        ]
        thoughts.sort(key=lambda t: t.step_number)
        return thoughts