"""
Visual Reasoning FastMCP Server

Provides spatial and diagrammatic thinking capabilities through FastMCP tools.
Supports visual problem-solving, pattern recognition, and diagram analysis.
"""

import json
from typing import Any, Dict, List, Optional
from fastmcp import FastMCP

from ..models.visual_reasoning import (
    VisualReasoningModel,
    VisualElement,
    VisualRepresentationType,
    SpatialRelationship,
    PatternType
)

# Initialize the FastMCP app and model
app = FastMCP("Visual Reasoning")
model = VisualReasoningModel()


@app.tool()
def create_visual_element(
    element_id: str,
    element_type: str,
    position_x: float,
    position_y: float,
    width: float,
    height: float,
    properties: Optional[str] = None
) -> str:
    """
    Create a visual element with spatial properties for diagram analysis.
    
    Args:
        element_id: Unique identifier for the element
        element_type: Type of visual element (rectangle, circle, text, etc.)
        position_x: X coordinate position
        position_y: Y coordinate position  
        width: Width of the element
        height: Height of the element
        properties: Optional JSON string of additional properties
    
    Returns:
        JSON string describing the created visual element
    """
    try:
        props = json.loads(properties) if properties else {}
        
        element = model.create_visual_element(
            element_id=element_id,
            element_type=element_type,
            position=(position_x, position_y),
            size=(width, height),
            properties=props
        )
        
        return json.dumps({
            "element_id": element.element_id,
            "type": element.element_type,
            "position": element.position,
            "size": element.size,
            "area": element.metadata.get("area", 0),
            "center": element.metadata.get("center", (0, 0)),
            "properties": element.properties,
            "status": "created"
        }, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Failed to create visual element: {str(e)}"})


@app.tool()
def analyze_spatial_relationships(
    elements_json: str
) -> str:
    """
    Analyze spatial relationships between visual elements.
    
    Args:
        elements_json: JSON string containing array of visual elements
    
    Returns:
        JSON string with spatial relationship analysis
    """
    try:
        elements_data = json.loads(elements_json)
        elements = []
        
        for elem_data in elements_data:
            element = VisualElement(
                element_id=elem_data["element_id"],
                element_type=elem_data["element_type"],
                position=tuple(elem_data["position"]),
                size=tuple(elem_data["size"]),
                properties=elem_data.get("properties", {}),
                relationships=elem_data.get("relationships", []),
                metadata=elem_data.get("metadata", {})
            )
            elements.append(element)
        
        relationships = model.analyze_spatial_relationships(elements)
        
        return json.dumps({
            "relationships": {
                elem_id: [rel.value for rel in rels] 
                for elem_id, rels in relationships.items()
            },
            "summary": f"Analyzed relationships for {len(elements)} elements",
            "total_relationships": sum(len(rels) for rels in relationships.values())
        }, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Failed to analyze spatial relationships: {str(e)}"})


@app.tool()
def recognize_visual_patterns(
    elements_json: str
) -> str:
    """
    Recognize patterns in visual elements arrangement.
    
    Args:
        elements_json: JSON string containing array of visual elements
    
    Returns:
        JSON string with identified patterns
    """
    try:
        elements_data = json.loads(elements_json)
        elements = []
        
        for elem_data in elements_data:
            element = VisualElement(
                element_id=elem_data["element_id"],
                element_type=elem_data["element_type"],
                position=tuple(elem_data["position"]),
                size=tuple(elem_data["size"]),
                properties=elem_data.get("properties", {}),
                relationships=elem_data.get("relationships", []),
                metadata=elem_data.get("metadata", {})
            )
            elements.append(element)
        
        patterns = model.recognize_visual_patterns(elements)
        
        patterns_data = []
        for pattern in patterns:
            patterns_data.append({
                "pattern_id": pattern.pattern_id,
                "pattern_type": pattern.pattern_type.value,
                "confidence": pattern.confidence_level,
                "description": pattern.pattern_description,
                "elements_involved": pattern.pattern_elements,
                "rules": pattern.pattern_rules,
                "similarity_score": pattern.similarity_score
            })
        
        return json.dumps({
            "patterns_found": patterns_data,
            "pattern_count": len(patterns),
            "analysis_summary": f"Identified {len(patterns)} visual patterns"
        }, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Failed to recognize patterns: {str(e)}"})


@app.tool()
def analyze_diagram(
    elements_json: str,
    representation_type: str
) -> str:
    """
    Analyze diagram structure and extract insights.
    
    Args:
        elements_json: JSON string containing array of visual elements
        representation_type: Type of visual representation (diagram, chart, flowchart, etc.)
    
    Returns:
        JSON string with diagram analysis results
    """
    try:
        # Parse representation type
        try:
            rep_type = VisualRepresentationType(representation_type.lower())
        except ValueError:
            rep_type = VisualRepresentationType.DIAGRAM
        
        elements_data = json.loads(elements_json)
        elements = []
        
        for elem_data in elements_data:
            element = VisualElement(
                element_id=elem_data["element_id"],
                element_type=elem_data["element_type"],
                position=tuple(elem_data["position"]),
                size=tuple(elem_data["size"]),
                properties=elem_data.get("properties", {}),
                relationships=elem_data.get("relationships", []),
                metadata=elem_data.get("metadata", {})
            )
            elements.append(element)
        
        analysis = model.analyze_diagram(elements, rep_type)
        
        return json.dumps({
            "diagram_id": analysis.diagram_id,
            "representation_type": analysis.representation_type.value,
            "element_count": len(analysis.elements),
            "patterns_identified": [
                {
                    "type": p.pattern_type.value,
                    "confidence": p.confidence_level,
                    "description": p.pattern_description
                }
                for p in analysis.patterns_identified
            ],
            "key_insights": analysis.key_insights,
            "interpretation": analysis.interpretation,
            "confidence_score": analysis.confidence_score,
            "spatial_mapping": {
                "mapping_id": analysis.spatial_mapping.mapping_id,
                "coordinate_system": analysis.spatial_mapping.coordinate_system,
                "constraint_count": len(analysis.spatial_mapping.spatial_constraints)
            }
        }, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Failed to analyze diagram: {str(e)}"})


@app.tool()
def solve_visually(
    problem_description: str,
    elements_json: str,
    representation_type: str
) -> str:
    """
    Apply visual reasoning to problem solving.
    
    Args:
        problem_description: Description of the problem to solve
        elements_json: JSON string containing visual elements
        representation_type: Type of visual representation being used
    
    Returns:
        JSON string with visual problem-solving approach and solution
    """
    try:
        # Parse representation type
        try:
            rep_type = VisualRepresentationType(representation_type.lower())
        except ValueError:
            rep_type = VisualRepresentationType.DIAGRAM
        
        elements_data = json.loads(elements_json)
        elements = []
        
        for elem_data in elements_data:
            element = VisualElement(
                element_id=elem_data["element_id"],
                element_type=elem_data["element_type"],
                position=tuple(elem_data["position"]),
                size=tuple(elem_data["size"]),
                properties=elem_data.get("properties", {}),
                relationships=elem_data.get("relationships", []),
                metadata=elem_data.get("metadata", {})
            )
            elements.append(element)
        
        solution = model.solve_visually(problem_description, elements, rep_type)
        
        return json.dumps({
            "problem_id": solution.problem_id,
            "problem_description": solution.problem_description,
            "solution_steps": solution.solution_steps,
            "visual_aids_used": solution.visual_aids_used,
            "spatial_reasoning_applied": solution.spatial_reasoning_applied,
            "patterns_used": [
                {
                    "type": p.pattern_type.value,
                    "confidence": p.confidence_level,
                    "elements": p.pattern_elements
                }
                for p in solution.pattern_matching_used
            ],
            "solution_confidence": solution.solution_confidence,
            "visual_representation": {
                "diagram_id": solution.visual_representation.diagram_id,
                "interpretation": solution.visual_representation.interpretation,
                "insights": solution.visual_representation.key_insights
            }
        }, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Failed to solve visually: {str(e)}"})


@app.tool()
def create_spatial_mapping(
    elements_json: str,
    coordinate_system: str = "cartesian"
) -> str:
    """
    Create spatial mapping of visual elements with relationship analysis.
    
    Args:
        elements_json: JSON string containing array of visual elements
        coordinate_system: Coordinate system to use (cartesian, polar, etc.)
    
    Returns:
        JSON string with spatial mapping results
    """
    try:
        elements_data = json.loads(elements_json)
        elements = []
        
        for elem_data in elements_data:
            element = VisualElement(
                element_id=elem_data["element_id"],
                element_type=elem_data["element_type"],
                position=tuple(elem_data["position"]),
                size=tuple(elem_data["size"]),
                properties=elem_data.get("properties", {}),
                relationships=elem_data.get("relationships", []),
                metadata=elem_data.get("metadata", {})
            )
            elements.append(element)
        
        mapping = model.create_spatial_mapping(elements, coordinate_system)
        
        return json.dumps({
            "mapping_id": mapping.mapping_id,
            "coordinate_system": mapping.coordinate_system,
            "scale_factor": mapping.scale_factor,
            "element_count": len(mapping.elements),
            "relationships": {
                elem_id: [rel.value for rel in rels]
                for elem_id, rels in mapping.relationships.items()
            },
            "spatial_constraints": mapping.spatial_constraints,
            "mapping_summary": f"Created spatial mapping for {len(elements)} elements"
        }, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Failed to create spatial mapping: {str(e)}"})


# Export the FastMCP app
def get_app():
    """Get the FastMCP application instance"""
    return app


if __name__ == "__main__":
    app.run()