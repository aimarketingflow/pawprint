#!/usr/bin/env python3
"""
Task Types for Pawprinting PyQt6 V2 Automation

Defines the basic types, enums, and status values for the automation system.

Author: AIMF LLC
Date: June 20, 2025
"""

import logging
from enum import Enum
from typing import Dict, Any

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.automation.task_types")

class TaskExecutionStatus(Enum):
    """Enum for task execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"
    
    def is_terminal_state(self) -> bool:
        """Check if this is a terminal state"""
        return self in (
            TaskExecutionStatus.COMPLETED,
            TaskExecutionStatus.FAILED,
            TaskExecutionStatus.CANCELED
        )
    
    def is_successful(self) -> bool:
        """Check if this status represents success"""
        return self == TaskExecutionStatus.COMPLETED

class TaskPriority(Enum):
    """Enum for task priority"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"
    
    def to_numeric(self) -> int:
        """Convert to numeric priority (higher number = higher priority)"""
        if self == TaskPriority.LOW:
            return 0
        elif self == TaskPriority.NORMAL:
            return 1
        elif self == TaskPriority.HIGH:
            return 2
        elif self == TaskPriority.CRITICAL:
            return 3
        return 0

class TaskTriggerType(Enum):
    """Enum for task trigger types"""
    MANUAL = "manual"
    SCHEDULED = "scheduled"
    FILE_CHANGE = "file_change"
    COMPLETION = "completion"  # Triggered on completion of another task
    SYSTEM_EVENT = "system_event"
