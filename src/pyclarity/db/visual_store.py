"""Base store for Visual Reasoning tool session management."""

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel, Field


class VisualElement(BaseModel):
    """Model for a visual element in a diagram."""
    
    element_id: str = Field(..., description="Unique element identifier")
    element_type: str = Field(..., description="Type: node, box, circle, arrow, label, etc.")
    position: Dict[str, float] = Field(..., description="Position coordinates {x, y}")
    size: Optional[Dict[str, float]] = Field(None, description="Size {width, height}")
    label: Optional[str] = Field(None, description="Element label or text")
    style: Dict[str, Any] = Field(default_factory=dict, description="Visual style properties")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class ElementConnection(BaseModel):
    """Model for connections between visual elements."""
    
    connection_id: str = Field(..., description="Unique connection identifier")
    source_id: str = Field(..., description="Source element ID")
    target_id: str = Field(..., description="Target element ID")
    connection_type: str = Field(..., description="Type: arrow, line, association, etc.")
    label: Optional[str] = Field(None, description="Connection label")
    style: Dict[str, Any] = Field(default_factory=dict, description="Connection style")
    bidirectional: bool = Field(False, description="Whether connection is bidirectional")


class VisualPattern(BaseModel):
    """Model for identified visual patterns."""
    
    pattern_type: str = Field(..., description="Type: hierarchy, cycle, cluster, flow, etc.")
    description: str = Field(..., description="Pattern description")
    elements_involved: List[str] = Field(default_factory=list, description="Element IDs in pattern")
    confidence: float = Field(0.85, description="Confidence in pattern identification")
    implications: List[str] = Field(default_factory=list, description="What this pattern suggests")


class DiagramData(BaseModel):
    """Data model for diagram storage."""
    
    id: Optional[int] = Field(None, description="Database ID")
    session_id: str = Field(..., description="Session this diagram belongs to")
    
    # Diagram properties
    diagram_type: str = Field(..., description="Type: flowchart, mind_map, sequence, network, etc.")
    title: str = Field(..., description="Diagram title")
    description: Optional[str] = Field(None, description="Diagram description")
    purpose: str = Field(..., description="Purpose of the diagram")
    
    # Visual elements
    elements: List[VisualElement] = Field(default_factory=list, description="All visual elements")
    connections: List[ElementConnection] = Field(default_factory=list, description="All connections")
    
    # Layout and structure
    layout_algorithm: Optional[str] = Field(None, description="Layout algorithm used")
    hierarchical_levels: Optional[Dict[int, List[str]]] = Field(None, description="Elements by level")
    clusters: Optional[List[List[str]]] = Field(None, description="Element clusters")
    
    # Analysis
    patterns_identified: List[VisualPattern] = Field(default_factory=list, description="Patterns found")
    insights: List[str] = Field(default_factory=list, description="Insights from visualization")
    
    # Metrics
    complexity_score: float = Field(0.0, description="Visual complexity (0-1)")
    clarity_score: float = Field(0.0, description="Visual clarity (0-1)")
    completeness: float = Field(0.0, description="How complete the diagram is (0-1)")
    
    # Versioning
    version: int = Field(1, description="Diagram version")
    parent_diagram_id: Optional[int] = Field(None, description="Parent diagram if this is a revision")
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)


class VisualAnalysis(BaseModel):
    """Model for visual analysis results."""
    
    diagram_id: int = Field(..., description="Analyzed diagram ID")
    analysis_type: str = Field(..., description="Type: structural, semantic, aesthetic")
    
    # Structural analysis
    node_count: int = Field(0, description="Number of nodes")
    edge_count: int = Field(0, description="Number of edges")
    connected_components: int = Field(1, description="Number of connected components")
    max_path_length: Optional[int] = Field(None, description="Longest path in diagram")
    
    # Pattern analysis
    patterns: List[VisualPattern] = Field(default_factory=list, description="Patterns found")
    symmetries: List[str] = Field(default_factory=list, description="Symmetries identified")
    
    # Cognitive load
    cognitive_load_score: float = Field(0.5, description="Estimated cognitive load (0-1)")
    visual_balance: float = Field(0.5, description="Visual balance score (0-1)")
    
    recommendations: List[str] = Field(default_factory=list, description="Improvement recommendations")


class BaseVisualStore(ABC):
    """Abstract base class for visual reasoning storage operations."""
    
    @abstractmethod
    async def save_diagram(self, diagram_data: DiagramData) -> DiagramData:
        """Save a new diagram."""
        pass
    
    @abstractmethod
    async def get_diagram(self, diagram_id: int) -> Optional[DiagramData]:
        """Get a specific diagram by ID."""
        pass
    
    @abstractmethod
    async def get_session_diagrams(self, session_id: str) -> List[DiagramData]:
        """Get all diagrams for a session."""
        pass
    
    @abstractmethod
    async def add_element(
        self,
        diagram_id: int,
        element: VisualElement
    ) -> Optional[DiagramData]:
        """Add an element to a diagram."""
        pass
    
    @abstractmethod
    async def add_connection(
        self,
        diagram_id: int,
        connection: ElementConnection
    ) -> Optional[DiagramData]:
        """Add a connection between elements."""
        pass
    
    @abstractmethod
    async def update_element(
        self,
        diagram_id: int,
        element_id: str,
        updates: Dict[str, Any]
    ) -> Optional[DiagramData]:
        """Update an element's properties."""
        pass
    
    @abstractmethod
    async def remove_element(
        self,
        diagram_id: int,
        element_id: str
    ) -> Optional[DiagramData]:
        """Remove an element and its connections."""
        pass
    
    @abstractmethod
    async def identify_patterns(
        self,
        diagram_id: int
    ) -> List[VisualPattern]:
        """Identify visual patterns in a diagram."""
        pass
    
    @abstractmethod
    async def save_analysis(
        self,
        analysis: VisualAnalysis
    ) -> VisualAnalysis:
        """Save visual analysis results."""
        pass
    
    @abstractmethod
    async def get_diagram_versions(
        self,
        diagram_id: int
    ) -> List[DiagramData]:
        """Get all versions of a diagram."""
        pass
    
    @abstractmethod
    async def clone_diagram(
        self,
        diagram_id: int,
        new_session_id: str,
        new_title: str
    ) -> DiagramData:
        """Clone a diagram to a new session."""
        pass
    
    @abstractmethod
    async def export_diagram(
        self,
        diagram_id: int,
        format: str = "json"
    ) -> Dict[str, Any]:
        """Export diagram in specified format."""
        pass
    
    @abstractmethod
    async def search_diagrams(
        self,
        keywords: Optional[str] = None,
        diagram_type: Optional[str] = None,
        min_elements: Optional[int] = None,
        has_patterns: Optional[bool] = None,
        limit: int = 100
    ) -> List[DiagramData]:
        """Search diagrams with various filters."""
        pass