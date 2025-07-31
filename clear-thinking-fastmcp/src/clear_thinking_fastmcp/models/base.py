# Clear Thinking FastMCP Server - Base Models

"""
Base Pydantic models and utilities for all cognitive tools.

Agent: pydantic-model-engineer
Status: ACTIVE - Base model implementation complete
"""

from pydantic import BaseModel, Field, validator, ConfigDict
from typing import List, Dict, Any, Optional, Union
from enum import Enum
from datetime import datetime
import uuid
import json


class CognitiveToolBase(BaseModel):
    """Base model for all cognitive tools with FastMCP compatibility"""
    
    model_config = ConfigDict(
        # Enable JSON serialization for complex types
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            uuid.UUID: lambda v: str(v),
        },
        # Validate on assignment
        validate_assignment = True,
        # Use enum values in serialization
        use_enum_values = True,
        # Allow population by field name or alias (V2 name)
        populate_by_name = True,
        # Exclude None values by default
        exclude_none = True
    )


class CognitiveInputBase(CognitiveToolBase):
    """Base input model for all cognitive tools"""
    
    problem: str = Field(
        ...,
        description="The problem or question to analyze",
        min_length=10,
        max_length=5000,
        example="How to optimize database performance for a high-traffic web application?"
    )
    
    context: Optional[str] = Field(
        None,
        description="Additional context or background information",
        max_length=2000,
        example="E-commerce platform with 1M+ daily users"
    )
    
    session_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Session identifier for tracking",
        example="550e8400-e29b-41d4-a716-446655440000"
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Request timestamp",
        example="2025-07-29T10:30:00Z"
    )
    
    @validator('problem')
    def validate_problem_content(cls, v):
        """Validate problem description is meaningful"""
        if not v or not v.strip():
            raise ValueError("Problem description cannot be empty")
        
        # Remove excessive whitespace
        cleaned = ' '.join(v.split())
        
        if len(cleaned) < 10:
            raise ValueError("Problem description must be at least 10 characters long")
            
        return cleaned
    
    @validator('context')
    def validate_context_content(cls, v):
        """Validate context if provided"""
        if v is not None:
            cleaned = ' '.join(v.split())
            return cleaned if cleaned else None
        return v


class CognitiveOutputBase(CognitiveToolBase):
    """Base output model for all cognitive tools"""
    
    analysis: str = Field(
        ...,
        description="Primary analysis result",
        min_length=50,
        example="Based on first principles analysis, the core bottleneck appears to be..."
    )
    
    confidence_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score between 0 and 1",
        example=0.85
    )
    
    processing_time_ms: Optional[float] = Field(
        None,
        ge=0.0,
        description="Processing time in milliseconds",
        example=1250.5
    )
    
    session_id: str = Field(
        ...,
        description="Session identifier from request",
        example="550e8400-e29b-41d4-a716-446655440000"
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Response timestamp",
        example="2025-07-29T10:30:02Z"
    )
    
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional metadata about the processing"
    )
    
    @validator('confidence_score')
    def validate_confidence_score(cls, v):
        """Validate and round confidence score"""
        if not 0.0 <= v <= 1.0:
            raise ValueError("Confidence score must be between 0.0 and 1.0")
        return round(v, 3)  # Round to 3 decimal places
    
    @validator('analysis')
    def validate_analysis_content(cls, v):
        """Validate analysis is meaningful"""
        if not v or not v.strip():
            raise ValueError("Analysis cannot be empty")
        
        cleaned = ' '.join(v.split())
        
        if len(cleaned) < 50:
            raise ValueError("Analysis must be at least 50 characters long")
        
        return cleaned


class CognitiveValidators:
    """Custom validators for cognitive tool models"""
    
    @staticmethod
    def validate_confidence_score(cls, v):
        """Validate confidence score is reasonable"""
        if not isinstance(v, (int, float)):
            raise ValueError("Confidence score must be numeric")
        
        if not 0.0 <= v <= 1.0:
            raise ValueError("Confidence score must be between 0.0 and 1.0")
        
        return round(float(v), 3)
    
    @staticmethod
    def validate_problem_complexity(cls, v, values):
        """Validate problem description matches stated complexity"""
        problem = values.get('problem', '') if isinstance(values, dict) else ''
        
        if v == 'complex' and len(problem) < 100:
            raise ValueError("Complex problems require detailed descriptions (min 100 chars)")
        elif v == 'simple' and len(problem) > 500:
            raise ValueError("Simple problems should be concise (max 500 chars)")
        
        return v
    
    @staticmethod
    def validate_list_not_empty(cls, v, field_name="field"):
        """Ensure required lists are not empty"""
        if isinstance(v, list) and len(v) == 0:
            raise ValueError(f"{field_name} list cannot be empty")
        return v
    
    @staticmethod
    def validate_list_max_items(cls, v, max_items=10, field_name="field"):
        """Validate list doesn't exceed maximum items"""
        if isinstance(v, list) and len(v) > max_items:
            raise ValueError(f"{field_name} list cannot exceed {max_items} items")
        return v
    
    @staticmethod
    def validate_string_not_empty(cls, v, field_name="field"):
        """Validate string field is not empty"""
        if isinstance(v, str) and not v.strip():
            raise ValueError(f"{field_name} cannot be empty")
        return v.strip() if isinstance(v, str) else v


class ModelSerializer:
    """Utilities for model serialization and deserialization"""
    
    @staticmethod
    def to_json(model: BaseModel, indent: int = 2) -> str:
        """Serialize model to JSON string"""
        return model.json(indent=indent, ensure_ascii=False)
    
    @staticmethod
    def to_dict(
        model: BaseModel, 
        exclude_none: bool = True,
        exclude_unset: bool = False
    ) -> Dict[str, Any]:
        """Serialize model to dictionary"""
        return model.dict(
            exclude_none=exclude_none,
            exclude_unset=exclude_unset
        )
    
    @staticmethod
    def from_dict(model_class: type, data: Dict[str, Any]) -> BaseModel:  
        """Deserialize dictionary to model"""
        if not issubclass(model_class, BaseModel):
            raise ValueError("model_class must be a Pydantic BaseModel")
        
        return model_class(**data)
    
    @staticmethod
    def from_json(model_class: type, json_str: str) -> BaseModel:
        """Deserialize JSON string to model"""
        if not issubclass(model_class, BaseModel):
            raise ValueError("model_class must be a Pydantic BaseModel")
        
        try:
            data = json.loads(json_str)
            return model_class(**data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")
    
    @staticmethod
    def validate_model(model: BaseModel) -> bool:
        """Validate a model instance"""
        try:
            # Trigger validation by accessing __dict__
            _ = model.dict()
            return True
        except Exception:
            return False
    
    @staticmethod
    def merge_models(base_model: BaseModel, update_data: Dict[str, Any]) -> BaseModel:
        """Merge update data into existing model"""
        base_dict = base_model.dict()
        base_dict.update(update_data)
        
        model_class = type(base_model)
        return model_class(**base_dict)


# Custom field types for common cognitive tool patterns
class ComplexityLevel(str, Enum):
    """Complexity levels for cognitive analysis"""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"


class ProcessingStage(str, Enum):
    """Common processing stages for cognitive tools"""
    INITIALIZATION = "initialization"
    ANALYSIS = "analysis"
    SYNTHESIS = "synthesis"
    VALIDATION = "validation"
    COMPLETION = "completion"


class ConfidenceLevel(str, Enum):
    """Qualitative confidence levels"""
    VERY_LOW = "very_low"      # 0.0 - 0.2
    LOW = "low"                # 0.2 - 0.4
    MODERATE = "moderate"      # 0.4 - 0.6
    HIGH = "high"              # 0.6 - 0.8
    VERY_HIGH = "very_high"    # 0.8 - 1.0
    
    @classmethod
    def from_score(cls, score: float) -> 'ConfidenceLevel':
        """Convert numeric confidence score to qualitative level"""
        if score < 0.2:
            return cls.VERY_LOW
        elif score < 0.4:
            return cls.LOW
        elif score < 0.6:
            return cls.MODERATE
        elif score < 0.8:
            return cls.HIGH
        else:
            return cls.VERY_HIGH


# Export validators for use in specific tool models
__all__ = [
    "CognitiveToolBase",
    "CognitiveInputBase", 
    "CognitiveOutputBase",
    "CognitiveValidators",
    "ModelSerializer",
    "ComplexityLevel",
    "ProcessingStage", 
    "ConfidenceLevel"
]