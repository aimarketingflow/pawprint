#!/usr/bin/env python3
"""
Base Action Classes for Pawprinting PyQt6 V2 Automation

Defines the base action classes and interfaces for automation task execution.
These form the foundation of the action system that tasks can perform.

Author: AIMF LLC
Date: June 20, 2025
"""

import os
import sys
import json
import logging
import abc
from enum import Enum
from typing import Dict, List, Any, Optional, Callable, Set, Tuple
from datetime import datetime
from pathlib import Path

from PyQt6.QtCore import QObject, pyqtSignal

from utils.automation_logging import TaskLogger, LogLevel

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.automation.actions")

class ActionResult:
    """Result of an automation action execution"""
    
    def __init__(self, success: bool, message: str, data: Optional[Dict[str, Any]] = None):
        """Initialize action result"""
        self.success = success
        self.message = message
        self.data = data or {}
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "success": self.success,
            "message": self.message,
            "data": self.data,
            "timestamp": self.timestamp.isoformat()
        }
    
    @classmethod
    def success(cls, message: str = "Action completed successfully", 
               data: Optional[Dict[str, Any]] = None) -> 'ActionResult':
        """Create a success result"""
        return cls(True, message, data)
    
    @classmethod
    def failure(cls, message: str = "Action failed", 
               data: Optional[Dict[str, Any]] = None) -> 'ActionResult':
        """Create a failure result"""
        return cls(False, message, data)
    
    @classmethod
    def from_exception(cls, e: Exception, message: str = "Action failed with exception") -> 'ActionResult':
        """Create a result from an exception"""
        return cls(False, message, {
            "exception_type": e.__class__.__name__,
            "exception_message": str(e)
        })

class ActionStatus(Enum):
    """Status of an action"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"

class ActionContext:
    """Context for action execution"""
    
    def __init__(self, task_id: str, execution_id: str, params: Dict[str, Any] = None):
        """Initialize action context"""
        self.task_id = task_id
        self.execution_id = execution_id
        self.params = params or {}
        self.results = {}  # Previous action results
        self.logger = None  # Will be set by executor
        self.start_time = None
        self.end_time = None
        self.status = ActionStatus.PENDING
    
    def add_result(self, action_id: str, result: ActionResult):
        """Add result from another action"""
        self.results[action_id] = result
    
    def get_result(self, action_id: str) -> Optional[ActionResult]:
        """Get result from another action"""
        return self.results.get(action_id)
    
    def set_status(self, status: ActionStatus):
        """Set action status"""
        self.status = status
        if status == ActionStatus.RUNNING and not self.start_time:
            self.start_time = datetime.now()
        elif status in (ActionStatus.COMPLETED, ActionStatus.FAILED, ActionStatus.CANCELED):
            self.end_time = datetime.now()

class Action(abc.ABC):
    """Base class for all automation actions"""
    
    def __init__(self, action_id: str, config: Dict[str, Any] = None):
        """Initialize action"""
        self.action_id = action_id
        self.config = config or {}
        self.display_name = self.config.get("display_name", self.action_id)
        self.description = self.config.get("description", "")
    
    @abc.abstractmethod
    def execute(self, context: ActionContext) -> ActionResult:
        """Execute the action"""
        pass
    
    def validate_config(self) -> Tuple[bool, str]:
        """
        Validate action configuration
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        return True, ""
    
    def get_progress(self) -> float:
        """
        Get current progress (0.0 to 1.0)
        
        Default implementation returns indeterminate progress.
        Subclasses should override if they can report progress.
        """
        return 0.0
    
    def cancel(self) -> bool:
        """
        Attempt to cancel the action
        
        Returns:
            True if cancellation was initiated, False if action cannot be canceled
        """
        return False
    
    def cleanup(self):
        """
        Cleanup any resources used by the action
        
        Called after execute() completes, regardless of success/failure
        """
        pass
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert action to dictionary for serialization"""
        return {
            "action_id": self.action_id,
            "type": self.__class__.__name__,
            "config": self.config,
            "display_name": self.display_name,
            "description": self.description
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Action':
        """
        Create action from dictionary
        
        This needs to be implemented by a factory function in the action registry
        """
        raise NotImplementedError("Action.from_dict must be implemented by ActionRegistry")

class CompositeAction(Action):
    """Action that contains multiple sub-actions executed sequentially or in parallel"""
    
    def __init__(self, action_id: str, config: Dict[str, Any] = None):
        """Initialize composite action"""
        super().__init__(action_id, config)
        self.actions = []  # List of sub-actions
        self.parallel = config.get("parallel", False)
        self.stop_on_failure = config.get("stop_on_failure", True)
        self._current_action_index = -1
    
    def add_action(self, action: Action):
        """Add a sub-action"""
        self.actions.append(action)
    
    def execute(self, context: ActionContext) -> ActionResult:
        """Execute all sub-actions"""
        if not self.actions:
            return ActionResult.failure("No sub-actions to execute")
        
        results = []
        
        if self.parallel:
            # TODO: Implement parallel execution
            # This would require threading or async execution
            # For now, just execute sequentially as a fallback
            context.logger.warning("Parallel execution not implemented, falling back to sequential")
        
        # Execute actions sequentially
        for i, action in enumerate(self.actions):
            self._current_action_index = i
            
            try:
                context.logger.info(f"Executing sub-action {i+1}/{len(self.actions)}: {action.action_id}")
                result = action.execute(context)
                results.append(result)
                
                # Add result to context for subsequent actions
                context.add_result(action.action_id, result)
                
                # Stop on failure if configured
                if self.stop_on_failure and not result.success:
                    context.logger.warning(f"Sub-action {action.action_id} failed, stopping")
                    break
                
            except Exception as e:
                context.logger.exception(f"Exception in sub-action {action.action_id}: {str(e)}")
                result = ActionResult.from_exception(e, f"Sub-action {action.action_id} failed with exception")
                results.append(result)
                
                if self.stop_on_failure:
                    break
        
        # Determine overall success
        all_success = all(result.success for result in results)
        
        if all_success:
            return ActionResult.success(
                f"All {len(results)} sub-actions completed successfully",
                {"sub_results": [r.to_dict() for r in results]}
            )
        else:
            success_count = sum(1 for r in results if r.success)
            return ActionResult.failure(
                f"{success_count}/{len(results)} sub-actions completed successfully",
                {"sub_results": [r.to_dict() for r in results]}
            )
    
    def get_progress(self) -> float:
        """Get current progress based on completed sub-actions"""
        if not self.actions:
            return 0.0
        
        if self._current_action_index < 0:
            return 0.0
        
        # Base progress on completed actions
        completed = self._current_action_index
        
        # Add partial progress from current action if available
        if 0 <= self._current_action_index < len(self.actions):
            current_action = self.actions[self._current_action_index]
            current_progress = current_action.get_progress()
            completed += current_progress
        
        return min(1.0, completed / len(self.actions))
    
    def cancel(self) -> bool:
        """Cancel all sub-actions"""
        if self._current_action_index < 0 or self._current_action_index >= len(self.actions):
            return False
        
        # Try to cancel current action
        current_action = self.actions[self._current_action_index]
        return current_action.cancel()
    
    def cleanup(self):
        """Clean up all sub-actions"""
        for action in self.actions:
            try:
                action.cleanup()
            except Exception as e:
                logger.error(f"Error cleaning up action {action.action_id}: {str(e)}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert composite action to dictionary"""
        data = super().to_dict()
        data["parallel"] = self.parallel
        data["stop_on_failure"] = self.stop_on_failure
        data["actions"] = [action.to_dict() for action in self.actions]
        return data
