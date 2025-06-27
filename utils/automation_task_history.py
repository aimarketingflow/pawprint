#!/usr/bin/env python3
"""
Task History for Pawprinting PyQt6 V2 Automation

Maintains a searchable history of task executions including their
results, durations, and other metadata.

Author: AIMF LLC
Date: June 20, 2025
"""

import os
import sys
import logging
import json
import shutil
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Set, Tuple
from pathlib import Path

from PyQt6.QtCore import QObject, pyqtSignal

from utils.automation_task_types import TaskExecutionStatus
from utils.automation_task_result import TaskExecutionResult

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.automation.task_history")

class TaskExecution:
    """Record of a task execution"""
    
    def __init__(self, 
                 execution_id: str,
                 task_id: str,
                 action_id: str,
                 action_type: str,
                 start_time: datetime,
                 end_time: Optional[datetime] = None,
                 status: TaskExecutionStatus = TaskExecutionStatus.RUNNING,
                 result: Dict[str, Any] = None,
                 trigger_info: Dict[str, Any] = None):
        """Initialize task execution record"""
        self.execution_id = execution_id
        self.task_id = task_id
        self.action_id = action_id
        self.action_type = action_type
        self.start_time = start_time
        self.end_time = end_time
        self.status = status
        self.result = result or {}
        self.trigger_info = trigger_info or {}
        
    @property
    def duration_seconds(self) -> Optional[float]:
        """Get duration in seconds"""
        if self.end_time and self.start_time:
            return (self.end_time - self.start_time).total_seconds()
        return None
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "execution_id": self.execution_id,
            "task_id": self.task_id,
            "action_id": self.action_id,
            "action_type": self.action_type,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "status": self.status.value,
            "duration_seconds": self.duration_seconds,
            "result": self.result,
            "trigger_info": self.trigger_info
        }
        
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'TaskExecution':
        """Create from dictionary"""
        start_time = datetime.fromisoformat(data["start_time"]) if data.get("start_time") else None
        end_time = datetime.fromisoformat(data["end_time"]) if data.get("end_time") else None
        
        return TaskExecution(
            execution_id=data["execution_id"],
            task_id=data["task_id"],
            action_id=data["action_id"],
            action_type=data["action_type"],
            start_time=start_time,
            end_time=end_time,
            status=TaskExecutionStatus(data["status"]),
            result=data.get("result", {}),
            trigger_info=data.get("trigger_info", {})
        )
        
    def update_from_result(self, result: TaskExecutionResult) -> None:
        """Update execution record from result"""
        self.end_time = datetime.now()
        self.status = result.status
        self.result = result.to_dict()

class TaskHistoryManager(QObject):
    """Manager for task execution history"""
    
    # Signals
    execution_added = pyqtSignal(str)  # execution_id
    execution_updated = pyqtSignal(str)  # execution_id
    history_cleared = pyqtSignal()
    
    def __init__(self, max_history: int = 1000):
        """Initialize task history manager"""
        super().__init__()
        self._history = {}  # execution_id -> TaskExecution
        self._max_history = max_history
        self._history_by_task = {}  # task_id -> list of execution_id
        
    def add_execution(self, execution: TaskExecution) -> str:
        """Add a task execution to history"""
        self._history[execution.execution_id] = execution
        
        # Add to task index
        if execution.task_id not in self._history_by_task:
            self._history_by_task[execution.task_id] = []
        self._history_by_task[execution.task_id].append(execution.execution_id)
        
        # Trim history if needed
        if len(self._history) > self._max_history:
            self._trim_history()
            
        self.execution_added.emit(execution.execution_id)
        return execution.execution_id
        
    def update_execution(self, execution_id: str, result: TaskExecutionResult) -> bool:
        """Update execution with result"""
        if execution_id not in self._history:
            logger.warning(f"Execution with ID {execution_id} not found in history")
            return False
            
        execution = self._history[execution_id]
        execution.update_from_result(result)
        
        self.execution_updated.emit(execution_id)
        return True
        
    def get_execution(self, execution_id: str) -> Optional[TaskExecution]:
        """Get execution by ID"""
        return self._history.get(execution_id)
        
    def get_executions_for_task(self, task_id: str, limit: int = 100) -> List[TaskExecution]:
        """Get executions for a task"""
        if task_id not in self._history_by_task:
            return []
            
        execution_ids = self._history_by_task[task_id]
        if limit > 0:
            execution_ids = execution_ids[-limit:]  # Get the most recent ones
            
        return [self._history[eid] for eid in execution_ids if eid in self._history]
        
    def search_executions(self, 
                          status: Optional[TaskExecutionStatus] = None,
                          action_type: Optional[str] = None,
                          start_time_from: Optional[datetime] = None,
                          start_time_to: Optional[datetime] = None,
                          limit: int = 100) -> List[TaskExecution]:
        """Search executions by criteria"""
        results = []
        
        for execution in self._history.values():
            # Filter by status
            if status is not None and execution.status != status:
                continue
                
            # Filter by action type
            if action_type is not None and execution.action_type != action_type:
                continue
                
            # Filter by start time range
            if start_time_from is not None and execution.start_time < start_time_from:
                continue
                
            if start_time_to is not None and execution.start_time > start_time_to:
                continue
                
            results.append(execution)
            
            # Check limit
            if limit > 0 and len(results) >= limit:
                break
                
        # Sort by start time descending (newest first)
        results.sort(key=lambda e: e.start_time if e.start_time else datetime.min, reverse=True)
        
        return results[:limit] if limit > 0 else results
        
    def clear_history(self, older_than_days: Optional[int] = None) -> int:
        """Clear history, optionally only entries older than given days"""
        if older_than_days is not None:
            cutoff_date = datetime.now() - timedelta(days=older_than_days)
            
            # Find executions to remove
            to_remove = [
                eid for eid, execution in self._history.items()
                if execution.start_time and execution.start_time < cutoff_date
            ]
            
            # Remove from history
            for eid in to_remove:
                execution = self._history.pop(eid)
                
                # Update task index
                if execution.task_id in self._history_by_task:
                    self._history_by_task[execution.task_id] = [
                        e for e in self._history_by_task[execution.task_id] if e != eid
                    ]
                    
                    # Remove empty lists
                    if not self._history_by_task[execution.task_id]:
                        del self._history_by_task[execution.task_id]
                        
            if to_remove:
                self.history_cleared.emit()
                
            return len(to_remove)
        else:
            # Clear all history
            count = len(self._history)
            self._history.clear()
            self._history_by_task.clear()
            
            if count > 0:
                self.history_cleared.emit()
                
            return count
            
    def to_dict(self) -> Dict[str, Any]:
        """Convert history to dictionary for serialization"""
        return {
            "executions": [execution.to_dict() for execution in self._history.values()]
        }
        
    def load_from_dict(self, data: Dict[str, Any]) -> None:
        """Load history from dictionary"""
        self._history.clear()
        self._history_by_task.clear()
        
        for execution_data in data.get("executions", []):
            try:
                execution = TaskExecution.from_dict(execution_data)
                self._history[execution.execution_id] = execution
                
                # Update task index
                if execution.task_id not in self._history_by_task:
                    self._history_by_task[execution.task_id] = []
                self._history_by_task[execution.task_id].append(execution.execution_id)
            except Exception as e:
                logger.error(f"Error loading execution: {str(e)}")
                
        logger.info(f"Loaded {len(self._history)} execution records into history")
        
    def export_to_file(self, file_path: str) -> bool:
        """Export history to a file"""
        try:
            data = self.to_dict()
            
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
                
            logger.info(f"Exported task history to {file_path}")
            return True
        except Exception as e:
            logger.exception(f"Error exporting task history: {str(e)}")
            return False
            
    def import_from_file(self, file_path: str) -> bool:
        """Import history from a file"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                
            self.load_from_dict(data)
            logger.info(f"Imported task history from {file_path}")
            return True
        except Exception as e:
            logger.exception(f"Error importing task history: {str(e)}")
            return False
            
    def _trim_history(self) -> None:
        """Trim history to maximum size"""
        if len(self._history) <= self._max_history:
            return
            
        # Sort by start time
        sorted_executions = sorted(
            self._history.values(),
            key=lambda e: e.start_time if e.start_time else datetime.min
        )
        
        # Remove oldest entries
        to_remove = sorted_executions[:len(sorted_executions) - self._max_history]
        
        for execution in to_remove:
            eid = execution.execution_id
            
            # Remove from main history
            if eid in self._history:
                del self._history[eid]
                
            # Update task index
            if execution.task_id in self._history_by_task:
                self._history_by_task[execution.task_id] = [
                    e for e in self._history_by_task[execution.task_id] if e != eid
                ]
                
                # Remove empty lists
                if not self._history_by_task[execution.task_id]:
                    del self._history_by_task[execution.task_id]

# Singleton instance
_instance = None

def get_task_history_manager() -> TaskHistoryManager:
    """Get the singleton task history manager instance"""
    global _instance
    if _instance is None:
        _instance = TaskHistoryManager()
    return _instance
