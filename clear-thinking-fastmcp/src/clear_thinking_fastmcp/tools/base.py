# Clear Thinking FastMCP Server - Base Tool Server

"""
Base class for all cognitive tool servers with FastMCP Context integration.

This provides common functionality for all cognitive tools including
validation, logging, progress tracking, and error handling.

Agent: cognitive-tool-implementer
Status: ACTIVE - Base tool server implementation complete
"""

from abc import ABC, abstractmethod
from fastmcp.server import Context
from pydantic import BaseModel
from typing import TypeVar, Generic, Dict, Any, Optional
import time
import logging

# Type variables for generic base class
CognitiveInputModel = TypeVar('CognitiveInputModel', bound=BaseModel)
CognitiveOutputModel = TypeVar('CognitiveOutputModel', bound=BaseModel)


class CognitiveToolBase(ABC, Generic[CognitiveInputModel, CognitiveOutputModel]):
    """
    Base class for all cognitive tool servers with FastMCP Context integration.
    
    This abstract base class provides common functionality for all cognitive tools:
    - Input validation with Pydantic models
    - Context logging and progress reporting  
    - Error handling and recovery
    - Performance monitoring
    - Session management
    """
    
    def __init__(self):
        """Initialize the cognitive tool base"""
        self.tool_name: str = "CognitiveTool"
        self.version: str = "2.0.0"
        self.logger = logging.getLogger(f"cognitive_tools.{self.__class__.__name__}")
        
        # Performance tracking
        self._processing_times: list = []
        self._success_count: int = 0
        self._error_count: int = 0
    
    @abstractmethod
    async def process(
        self, 
        data: CognitiveInputModel, 
        ctx: Context
    ) -> CognitiveOutputModel:
        """
        Process the cognitive tool logic.
        
        This method must be implemented by all cognitive tool servers.
        It should use the Context object for logging and progress reporting.
        
        Args:
            data: Validated input data as Pydantic model
            ctx: FastMCP Context for logging and progress
            
        Returns:
            Processed output as Pydantic model
            
        Raises:
            ValueError: For invalid input data
            RuntimeError: For processing errors
        """
        pass
    
    async def validate_input(self, data: CognitiveInputModel) -> bool:
        """
        Validate input data beyond Pydantic model validation.
        
        Override this method to add tool-specific validation logic.
        Base implementation just checks that data exists.
        
        Args:
            data: Input data to validate
            
        Returns:
            True if validation passes, False otherwise
        """
        try:
            # Basic validation - check data exists and is valid Pydantic model
            if data is None:
                return False
            
            # Trigger Pydantic validation by accessing dict
            _ = data.dict()
            return True
            
        except Exception as e:
            self.logger.warning(f"Input validation failed: {e}")
            return False
    
    async def log_processing_start(
        self, 
        data: CognitiveInputModel, 
        ctx: Context
    ) -> None:
        """Log the start of processing with Context integration"""
        ctx.info(f"Starting {self.tool_name} processing")
        ctx.debug(f"Input data type: {type(data).__name__}")
        
        # Log key input parameters (without sensitive data)
        if hasattr(data, 'problem'):
            problem_preview = data.problem[:100] + "..." if len(data.problem) > 100 else data.problem
            ctx.debug(f"Problem: {problem_preview}")
        
        if hasattr(data, 'session_id'):
            ctx.debug(f"Session ID: {data.session_id}")
        
        self.logger.info(f"Processing started for {self.tool_name}")
    
    async def log_processing_complete(
        self, 
        result: CognitiveOutputModel, 
        ctx: Context
    ) -> None:
        """Log the completion of processing with Context integration"""
        ctx.info(f"{self.tool_name} processing completed successfully")
        
        # Log key output metrics
        if hasattr(result, 'confidence_score'):
            ctx.debug(f"Confidence score: {result.confidence_score:.3f}")
        
        if hasattr(result, 'processing_time_ms'):
            ctx.debug(f"Processing time: {result.processing_time_ms:.1f}ms")
        
        # Update success metrics
        self._success_count += 1
        
        if hasattr(result, 'processing_time_ms') and result.processing_time_ms:
            self._processing_times.append(result.processing_time_ms)
            # Keep only last 100 measurements
            if len(self._processing_times) > 100:
                self._processing_times = self._processing_times[-100:]
        
        self.logger.info(f"Processing completed for {self.tool_name}")
    
    async def log_processing_error(
        self, 
        error: Exception, 
        ctx: Context,
        data: Optional[CognitiveInputModel] = None
    ) -> None:
        """Log processing errors with Context integration"""
        error_type = type(error).__name__
        error_message = str(error)
        
        ctx.error(f"{self.tool_name} processing failed: {error_type}: {error_message}")
        
        if data and hasattr(data, 'session_id'):
            ctx.error(f"Failed session ID: {data.session_id}")
        
        # Update error metrics
        self._error_count += 1
        
        self.logger.error(
            f"Processing error in {self.tool_name}: {error_type}: {error_message}",
            exc_info=True
        )
    
    async def progress_update(
        self,
        ctx: Context,
        current: float,
        total: float,
        message: str,
        stage: Optional[str] = None
    ) -> None:
        """
        Update processing progress with Context integration.
        
        Args:
            ctx: FastMCP Context object
            current: Current progress value
            total: Total progress value
            message: Progress message
            stage: Optional processing stage name
        """
        ctx.progress(current, total, message)
        
        if stage:
            ctx.debug(f"Processing stage: {stage}")
        
        # Log significant progress milestones
        progress_percent = (current / total) * 100 if total > 0 else 0
        if progress_percent in [25, 50, 75, 100]:
            self.logger.debug(f"{self.tool_name} progress: {progress_percent:.0f}% - {message}")
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """
        Get performance metrics for this cognitive tool.
        
        Returns:
            Dictionary with performance statistics
        """
        avg_time = (
            sum(self._processing_times) / len(self._processing_times)
            if self._processing_times else 0.0
        )
        
        max_time = max(self._processing_times) if self._processing_times else 0.0
        min_time = min(self._processing_times) if self._processing_times else 0.0
        
        total_requests = self._success_count + self._error_count
        success_rate = (
            (self._success_count / total_requests) * 100
            if total_requests > 0 else 0.0
        )
        
        return {
            "tool_name": self.tool_name,
            "version": self.version,
            "total_requests": total_requests,
            "successful_requests": self._success_count,
            "failed_requests": self._error_count,
            "success_rate_percent": round(success_rate, 2),
            "average_processing_time_ms": round(avg_time, 2),
            "min_processing_time_ms": round(min_time, 2),
            "max_processing_time_ms": round(max_time, 2),
            "recent_measurements": len(self._processing_times)
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Perform health check for this cognitive tool.
        
        Returns:
            Health status dictionary
        """
        try:
            # Basic health checks
            metrics = self.get_performance_metrics()
            
            # Determine health status
            success_rate = metrics["success_rate_percent"]
            avg_time = metrics["average_processing_time_ms"]
            
            if success_rate >= 95 and avg_time < 5000:  # 5 seconds
                status = "healthy"
            elif success_rate >= 90 and avg_time < 10000:  # 10 seconds
                status = "warning"
            else:
                status = "unhealthy"
            
            return {
                "status": status,
                "tool_name": self.tool_name,
                "version": self.version,
                "metrics": metrics,
                "timestamp": time.time()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "tool_name": self.tool_name,
                "version": self.version,
                "error": str(e),
                "timestamp": time.time()
            }
    
    def reset_metrics(self) -> None:
        """Reset performance metrics"""
        self._processing_times.clear()
        self._success_count = 0
        self._error_count = 0
        
        self.logger.info(f"Performance metrics reset for {self.tool_name}")
    
    def __str__(self) -> str:
        """String representation of the cognitive tool"""
        return f"{self.__class__.__name__}(name='{self.tool_name}', version='{self.version}')"
    
    def __repr__(self) -> str:
        """Detailed representation of the cognitive tool"""
        metrics = self.get_performance_metrics()
        return (
            f"{self.__class__.__name__}("
            f"name='{self.tool_name}', "
            f"version='{self.version}', "
            f"requests={metrics['total_requests']}, "
            f"success_rate={metrics['success_rate_percent']}%"
            f")"
        )


class CognitiveToolRegistry:
    """Registry for managing cognitive tool instances"""
    
    def __init__(self):
        """Initialize the tool registry"""
        self._tools: Dict[str, CognitiveToolBase] = {}
        self.logger = logging.getLogger("cognitive_tools.registry")
    
    def register_tool(self, tool: CognitiveToolBase) -> None:
        """Register a cognitive tool instance"""
        tool_name = tool.tool_name.lower().replace(" ", "_")
        self._tools[tool_name] = tool
        self.logger.info(f"Registered cognitive tool: {tool_name}")
    
    def get_tool(self, tool_name: str) -> Optional[CognitiveToolBase]:
        """Get a cognitive tool by name"""
        return self._tools.get(tool_name.lower().replace(" ", "_"))
    
    def list_tools(self) -> Dict[str, str]:
        """List all registered tools with their versions"""
        return {
            name: tool.version 
            for name, tool in self._tools.items()
        }
    
    def get_all_health_status(self) -> Dict[str, Dict[str, Any]]:
        """Get health status for all registered tools"""
        health_status = {}
        
        for name, tool in self._tools.items():
            try:
                health_status[name] = tool.health_check()
            except Exception as e:
                health_status[name] = {
                    "status": "error",
                    "error": str(e),
                    "timestamp": time.time()
                }
        
        return health_status
    
    def get_combined_metrics(self) -> Dict[str, Any]:
        """Get combined performance metrics for all tools"""
        combined = {
            "total_tools": len(self._tools),
            "total_requests": 0,
            "total_successes": 0,
            "total_errors": 0,
            "tool_metrics": {}
        }
        
        for name, tool in self._tools.items():
            metrics = tool.get_performance_metrics()
            combined["total_requests"] += metrics["total_requests"]
            combined["total_successes"] += metrics["successful_requests"]
            combined["total_errors"] += metrics["failed_requests"]
            combined["tool_metrics"][name] = metrics
        
        # Calculate overall success rate
        if combined["total_requests"] > 0:
            combined["overall_success_rate_percent"] = round(
                (combined["total_successes"] / combined["total_requests"]) * 100, 2
            )
        else:
            combined["overall_success_rate_percent"] = 0.0
        
        return combined


# Global tool registry instance
tool_registry = CognitiveToolRegistry()


__all__ = [
    "CognitiveToolBase",
    "CognitiveToolRegistry", 
    "tool_registry"
]