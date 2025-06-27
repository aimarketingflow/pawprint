#!/usr/bin/env python3
"""
Task Executor Base for Pawprinting PyQt6 V2 Automation

Provides the core execution engine for running automation tasks
and handling their lifecycle, including execution, cancellation,
and progress reporting.

Author: AIMF LLC
Date: June 20, 2025
"""

import os
import sys
import logging
import traceback
import threading
from enum import Enum
from typing import Dict, List, Any, Optional, Set, Tuple
from datetime import datetime
from pathlib import Path

from PyQt6.QtCore import QObject, pyqtSignal, QThread, QMutex, QMutexLocker

from utils.automation_action_base import Action, ActionResult, ActionContext, ActionStatus
from utils.automation_logging import AutomationLogManager, TaskLogger

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.automation.task_executor_base")

class TaskExecutionStatus(Enum):
    """Enum for task execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"

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

class TaskExecutor(QObject):
    """Base task executor class"""
    
    # Signals
    task_started = pyqtSignal(str)  # task_id
    task_completed = pyqtSignal(str, object)  # task_id, result
    task_failed = pyqtSignal(str, object)  # task_id, result
    task_canceled = pyqtSignal(str)  # task_id
    task_progress = pyqtSignal(str, float)  # task_id, progress (0-1)
    
    def __init__(self):
        """Initialize task executor"""
        super().__init__()
        self._active_tasks = {}  # task_id -> Action
        self._task_threads = {}  # task_id -> QThread
        self._task_loggers = {}  # task_id -> TaskLogger
        self._mutex = QMutex()
        self._log_manager = AutomationLogManager.get_instance()
    
    def execute_task(self, task_id: str, action: Action, task_config: Dict[str, Any] = None) -> bool:
        """Execute a task"""
        task_config = task_config or {}
        
        with QMutexLocker(self._mutex):
            if task_id in self._active_tasks:
                logger.warning(f"Task with ID {task_id} is already running")
                return False
            
            # Create task logger
            task_logger = self._log_manager.create_logger(task_id)
            self._task_loggers[task_id] = task_logger
            
            # Set up execution context
            context = ActionContext(
                task_id=task_id,
                variables=task_config.get("variables", {}),
                logger=task_logger
            )
            
            # Store action
            self._active_tasks[task_id] = action
            
            # Create and start thread
            thread = QThread()
            self._task_threads[task_id] = thread
            
            # Create worker
            worker = TaskExecutorWorker(task_id, action, context)
            worker.moveToThread(thread)
            
            # Connect signals
            thread.started.connect(worker.run)
            worker.finished.connect(lambda result: self._on_task_finished(task_id, result))
            worker.progress.connect(lambda p: self.task_progress.emit(task_id, p))
            
            # Start the thread
            thread.start()
            
            # Log and emit signal
            task_logger.info(f"Task {task_id} started")
            logger.info(f"Task {task_id} started")
            self.task_started.emit(task_id)
            
            return True
    
    def cancel_task(self, task_id: str) -> bool:
        """Cancel a running task"""
        with QMutexLocker(self._mutex):
            if task_id not in self._active_tasks:
                logger.warning(f"Task with ID {task_id} is not running")
                return False
            
            action = self._active_tasks[task_id]
            logger.info(f"Canceling task {task_id}")
            
            # Log cancellation
            if task_id in self._task_loggers:
                self._task_loggers[task_id].warning(f"Task cancellation requested")
            
            # Cancel the action
            return action.cancel()
    
    def get_task_progress(self, task_id: str) -> Optional[float]:
        """Get task progress"""
        with QMutexLocker(self._mutex):
            if task_id not in self._active_tasks:
                return None
            
            action = self._active_tasks[task_id]
            return action.get_progress()
    
    def is_task_running(self, task_id: str) -> bool:
        """Check if task is running"""
        with QMutexLocker(self._mutex):
            return task_id in self._active_tasks
    
    def get_active_tasks(self) -> List[str]:
        """Get list of active task IDs"""
        with QMutexLocker(self._mutex):
            return list(self._active_tasks.keys())
    
    def _on_task_finished(self, task_id: str, result: TaskExecutionResult):
        """Handle task finished"""
        thread = None
        action = None
        
        with QMutexLocker(self._mutex):
            if task_id in self._active_tasks:
                action = self._active_tasks.pop(task_id)
            
            if task_id in self._task_threads:
                thread = self._task_threads.pop(task_id)
            
            # Get logger
            if task_id in self._task_loggers:
                task_logger = self._task_loggers[task_id]
                
                # Log result
                if result.status == TaskExecutionStatus.COMPLETED:
                    task_logger.info(f"Task completed: {result.message}")
                    task_logger.complete()  # Mark as complete in logger
                elif result.status == TaskExecutionStatus.FAILED:
                    task_logger.error(f"Task failed: {result.message}")
                    if result.exception:
                        task_logger.exception(result.exception)
                    task_logger.fail()  # Mark as failed in logger
                elif result.status == TaskExecutionStatus.CANCELED:
                    task_logger.warning(f"Task canceled: {result.message}")
                    task_logger.cancel()  # Mark as canceled in logger
                
                # Close logger
                self._log_manager.close_logger(task_id)
                self._task_loggers.pop(task_id)
        
        # Emit appropriate signal
        if result.status == TaskExecutionStatus.COMPLETED:
            self.task_completed.emit(task_id, result)
            logger.info(f"Task {task_id} completed: {result.message}")
        elif result.status == TaskExecutionStatus.FAILED:
            self.task_failed.emit(task_id, result)
            logger.error(f"Task {task_id} failed: {result.message}")
        elif result.status == TaskExecutionStatus.CANCELED:
            self.task_canceled.emit(task_id)
            logger.info(f"Task {task_id} canceled")
        
        # Clean up thread
        if thread:
            thread.quit()
            thread.wait()
            thread.deleteLater()

class TaskExecutorWorker(QObject):
    """Worker for executing tasks in a separate thread"""
    
    # Signals
    finished = pyqtSignal(object)  # TaskExecutionResult
    progress = pyqtSignal(float)  # 0-1
    
    def __init__(self, task_id: str, action: Action, context: ActionContext):
        """Initialize worker"""
        super().__init__()
        self.task_id = task_id
        self.action = action
        self.context = context
    
    def run(self):
        """Run the task"""
        try:
            # Validate action config
            valid, message = self.action.validate_config()
            if not valid:
                self.finished.emit(TaskExecutionResult.failure(
                    f"Invalid action configuration: {message}"
                ))
                return
            
            # Execute action
            result = self.action.execute(self.context)
            
            # Convert to task result
            task_result = TaskExecutionResult.from_action_result(result)
            
            # Emit result
            self.finished.emit(task_result)
            
        except Exception as e:
            # Handle exceptions
            logger.exception(f"Unhandled exception in task {self.task_id}")
            
            self.finished.emit(TaskExecutionResult.failure(
                f"Task failed with unhandled exception: {str(e)}",
                exception=e
            ))
    
    def report_progress(self, progress: float):
        """Report progress"""
        # Ensure progress is between 0 and 1
        progress = max(0.0, min(1.0, progress))
        self.progress.emit(progress)


# Singleton instance
_instance = None

def get_task_executor() -> TaskExecutor:
    """Get the singleton task executor instance"""
    global _instance
    if _instance is None:
        _instance = TaskExecutor()
    return _instance
