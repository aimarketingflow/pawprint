#!/usr/bin/env python3
"""
Task Context for Pawprinting PyQt6 V2 Automation

Provides the execution context for automation tasks, including
variables, logger access, and execution state.

Author: AIMF LLC
Date: June 20, 2025
"""

import os
import sys
import logging
from datetime import datetime
from typing import Dict, Any, Optional

from utils.automation_logging import TaskLogger

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.automation.task_context")

class TaskContext:
    """Task execution context"""
    
    def __init__(self, 
                 task_id: str,
                 variables: Dict[str, Any] = None,
                 logger: TaskLogger = None):
        """Initialize task context"""
        self.task_id = task_id
        self.variables = variables or {}
        self.logger = logger
        self.start_time = datetime.now()
        self._temp_dir = None
        
    def get_variable(self, name: str, default=None) -> Any:
        """Get a context variable"""
        return self.variables.get(name, default)
    
    def set_variable(self, name: str, value: Any) -> None:
        """Set a context variable"""
        self.variables[name] = value
        
    def has_variable(self, name: str) -> bool:
        """Check if a variable exists"""
        return name in self.variables
        
    def get_temp_dir(self) -> str:
        """Get a temporary directory for this task"""
        if not self._temp_dir:
            import tempfile
            self._temp_dir = tempfile.mkdtemp(prefix=f"pawprint_task_{self.task_id}_")
            
        return self._temp_dir
        
    def get_elapsed_time(self) -> float:
        """Get elapsed time in seconds"""
        return (datetime.now() - self.start_time).total_seconds()
        
    def get_task_data(self) -> Dict[str, Any]:
        """Get dictionary of task context data"""
        return {
            "task_id": self.task_id,
            "variables": self.variables,
            "start_time": self.start_time.isoformat(),
            "elapsed_seconds": self.get_elapsed_time()
        }
    
    def cleanup(self):
        """Clean up any resources"""
        # Remove temp directory if it exists
        if self._temp_dir and os.path.exists(self._temp_dir):
            try:
                import shutil
                shutil.rmtree(self._temp_dir)
                self._temp_dir = None
            except Exception as e:
                if self.logger:
                    self.logger.warning(f"Failed to clean up temp dir: {str(e)}")
                else:
                    logger.warning(f"Failed to clean up temp dir: {str(e)}")
                    
    def __enter__(self):
        """Context manager enter"""
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.cleanup()
