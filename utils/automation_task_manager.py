#!/usr/bin/env python3
"""
Task Manager for Pawprinting PyQt6 V2 Automation

Core component that manages task execution, including starting, stopping,
and tracking the status of tasks.

Author: AIMF LLC
Date: June 20, 2025
"""

import logging
from typing import Dict, List, Any, Optional

from PyQt6.QtCore import QObject, pyqtSignal, QThread, QMutex, QMutexLocker

from utils.automation_action_base import Action
from utils.automation_task_context import TaskContext
from utils.automation_task_result import TaskExecutionResult
from utils.automation_task_types import TaskExecutionStatus
from utils.automation_task_worker import TaskExecutorWorker
from utils.automation_logging import AutomationLogManager, TaskLogger

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.automation.task_manager")

class TaskManager(QObject):
    """Manager for task execution"""
    
    # Signals
    task_started = pyqtSignal(str)  # task_id
    task_completed = pyqtSignal(str, object)  # task_id, result
    task_failed = pyqtSignal(str, object)  # task_id, result
    task_canceled = pyqtSignal(str)  # task_id
    task_progress = pyqtSignal(str, float)  # task_id, progress (0-1)
    
    def __init__(self):
        """Initialize task manager"""
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
            context = TaskContext(
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

# Singleton instance
_instance = None

def get_task_manager() -> TaskManager:
    """Get the singleton task manager instance"""
    global _instance
    if _instance is None:
        _instance = TaskManager()
    return _instance
