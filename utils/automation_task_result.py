#!/usr/bin/env python3
"""
Task Result for Pawprinting PyQt6 V2 Automation

Handles the results of task execution, including success/failure status,
data, and error information.

Author: AIMF LLC
Date: June 20, 2025
"""

import logging
import traceback
from datetime import datetime
from typing import Dict, Any, Optional

from utils.automation_action_base import ActionResult
from utils.automation_task_types import TaskExecutionStatus

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.automation.task_result")

class TaskExecutionResult:
    """Result of a task execution"""
    
    def __init__(
        self, 
        status: TaskExecutionStatus, 
        message: str, 
        data: Dict[str, Any] = None, 
        exception: Exception = None
    ):
        """Initialize task execution result"""
        self.status = status
        self.message = message
        self.data = data or {}
        self.exception = exception
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        result = {
            "status": self.status.value,
            "message": self.message,
            "data": self.data,
            "timestamp": self.timestamp.isoformat()
        }
        
        if self.exception:
            result["exception"] = {
                "type": type(self.exception).__name__,
                "message": str(self.exception),
                "traceback": traceback.format_exc()
            }
        
        return result
    
    @staticmethod
    def from_action_result(result: ActionResult) -> 'TaskExecutionResult':
        """Create task execution result from action result"""
        if result.success:
            return TaskExecutionResult(
                TaskExecutionStatus.COMPLETED,
                result.message,
                result.data
            )
        else:
            return TaskExecutionResult(
                TaskExecutionStatus.FAILED,
                result.message,
                result.data,
                result.exception
            )
    
    @staticmethod
    def success(message: str, data: Dict[str, Any] = None) -> 'TaskExecutionResult':
        """Create a success result"""
        return TaskExecutionResult(TaskExecutionStatus.COMPLETED, message, data)
    
    @staticmethod
    def failure(message: str, data: Dict[str, Any] = None, exception: Exception = None) -> 'TaskExecutionResult':
        """Create a failure result"""
        return TaskExecutionResult(TaskExecutionStatus.FAILED, message, data, exception)
    
    @staticmethod
    def canceled(message: str = "Task was canceled", data: Dict[str, Any] = None) -> 'TaskExecutionResult':
        """Create a canceled result"""
        return TaskExecutionResult(TaskExecutionStatus.CANCELED, message, data)
        
    def is_success(self) -> bool:
        """Check if this result represents success"""
        return self.status == TaskExecutionStatus.COMPLETED
        
    def get_duration(self, start_time: datetime) -> float:
        """Get task duration in seconds"""
        return (self.timestamp - start_time).total_seconds()
