#!/usr/bin/env python3
"""
Task Worker for Pawprinting PyQt6 V2 Automation

Handles the actual execution of tasks in separate threads.

Author: AIMF LLC
Date: June 20, 2025
"""

import logging
from typing import Dict, Any

from PyQt6.QtCore import QObject, pyqtSignal

from utils.automation_action_base import Action
from utils.automation_task_context import TaskContext
from utils.automation_task_result import TaskExecutionResult

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.automation.task_worker")

class TaskExecutorWorker(QObject):
    """Worker for executing tasks in a separate thread"""
    
    # Signals
    finished = pyqtSignal(object)  # TaskExecutionResult
    progress = pyqtSignal(float)  # 0-1
    
    def __init__(self, task_id: str, action: Action, context: TaskContext):
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
