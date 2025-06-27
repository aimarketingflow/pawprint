#!/usr/bin/env python3
"""
Automation Logging Utilities for Pawprinting PyQt6 V2

Provides specialized logging facilities for the automation system,
including task execution logs, error reporting, and diagnostic information.

Author: AIMF LLC
Date: June 20, 2025
"""

import os
import sys
import logging
import threading
import traceback
from enum import Enum
from typing import Dict, List, Any, Optional, Set, Tuple
from datetime import datetime
from pathlib import Path
import json
import io
import shutil

from PyQt6.QtCore import QObject, pyqtSignal

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.automation.logging")

class LogLevel(Enum):
    """Log levels for automation logs"""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class TaskLogEntry:
    """Represents a single log entry for a task execution"""
    
    def __init__(self, level: LogLevel, message: str, context: Optional[Dict[str, Any]] = None):
        """Initialize log entry"""
        self.timestamp = datetime.now().isoformat()
        self.level = level
        self.message = message
        self.context = context or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "timestamp": self.timestamp,
            "level": self.level.value,
            "message": self.message,
            "context": self.context
        }
    
    def __str__(self) -> str:
        """String representation"""
        return f"[{self.timestamp}] {self.level.value.upper()}: {self.message}"

class TaskLogger:
    """Logger for an individual task execution"""
    
    def __init__(self, task_id: str, task_name: str, execution_id: str = None):
        """Initialize task logger"""
        self.task_id = task_id
        self.task_name = task_name
        
        # If no execution ID provided, generate one based on timestamp
        self.execution_id = execution_id or f"exec_{task_id}_{int(datetime.now().timestamp())}"
        
        self.logs = []
        self.start_time = datetime.now()
        self.end_time = None
        self.success = None
        self.progress = 0.0
        
        # Base path for log files
        base_path = Path(os.path.expanduser("~")) / "Documents" / "Pawprinting_PyQt6_V2" / "automation" / "logs"
        
        # Create log directory
        os.makedirs(base_path, exist_ok=True)
        
        # Log file path: automation/logs/TASK_ID/EXECUTION_ID.log
        task_dir = base_path / self.task_id
        os.makedirs(task_dir, exist_ok=True)
        
        self.log_file = task_dir / f"{self.execution_id}.log"
        self.json_log_file = task_dir / f"{self.execution_id}.json"
        
        # Log start
        self.log(LogLevel.INFO, f"Started task execution: {self.task_name}")
    
    def log(self, level: LogLevel, message: str, context: Optional[Dict[str, Any]] = None) -> TaskLogEntry:
        """Add a log entry"""
        entry = TaskLogEntry(level, message, context)
        self.logs.append(entry)
        
        # Write to log file
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(f"{str(entry)}\n")
        except Exception as e:
            logging.error(f"Error writing to task log file: {str(e)}")
        
        return entry
    
    def debug(self, message: str, context: Optional[Dict[str, Any]] = None) -> TaskLogEntry:
        """Add a debug log entry"""
        return self.log(LogLevel.DEBUG, message, context)
    
    def info(self, message: str, context: Optional[Dict[str, Any]] = None) -> TaskLogEntry:
        """Add an info log entry"""
        return self.log(LogLevel.INFO, message, context)
    
    def warning(self, message: str, context: Optional[Dict[str, Any]] = None) -> TaskLogEntry:
        """Add a warning log entry"""
        return self.log(LogLevel.WARNING, message, context)
    
    def error(self, message: str, context: Optional[Dict[str, Any]] = None) -> TaskLogEntry:
        """Add an error log entry"""
        return self.log(LogLevel.ERROR, message, context)
    
    def critical(self, message: str, context: Optional[Dict[str, Any]] = None) -> TaskLogEntry:
        """Add a critical log entry"""
        return self.log(LogLevel.CRITICAL, message, context)
    
    def exception(self, message: str, exc_info=None, context: Optional[Dict[str, Any]] = None) -> TaskLogEntry:
        """Log an exception with traceback"""
        if exc_info is None:
            exc_info = sys.exc_info()
        
        # Get exception details
        exc_type, exc_value, exc_tb = exc_info
        tb_str = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        
        # Add traceback to context
        ctx = context.copy() if context else {}
        ctx["traceback"] = tb_str
        ctx["exception_type"] = exc_type.__name__ if exc_type else "Unknown"
        ctx["exception_value"] = str(exc_value) if exc_value else ""
        
        return self.error(message, ctx)
    
    def set_progress(self, progress: float):
        """Update task progress (0.0 to 1.0)"""
        self.progress = min(1.0, max(0.0, progress))
        self.info(f"Progress: {self.progress * 100:.1f}%", {"progress": self.progress})
    
    def complete(self, success: bool = True, message: Optional[str] = None):
        """Mark task execution as complete"""
        self.end_time = datetime.now()
        self.success = success
        
        duration = (self.end_time - self.start_time).total_seconds()
        
        if message:
            if success:
                self.info(message, {"duration": duration})
            else:
                self.error(message, {"duration": duration})
        
        status = "successfully" if success else "with failure"
        self.log(
            LogLevel.INFO if success else LogLevel.ERROR,
            f"Task execution completed {status} (duration: {duration:.1f} seconds)",
            {"duration": duration, "success": success}
        )
        
        # Write complete log as JSON
        self.save_json_log()
    
    def save_json_log(self):
        """Save the complete log as JSON"""
        try:
            log_data = {
                "task_id": self.task_id,
                "task_name": self.task_name,
                "execution_id": self.execution_id,
                "start_time": self.start_time.isoformat(),
                "end_time": self.end_time.isoformat() if self.end_time else None,
                "success": self.success,
                "progress": self.progress,
                "logs": [entry.to_dict() for entry in self.logs]
            }
            
            with open(self.json_log_file, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, indent=2)
                
        except Exception as e:
            logging.error(f"Error saving JSON task log: {str(e)}")

class AutomationLogManager(QObject):
    """
    Manages logging for the automation system
    """
    
    # Signals
    log_added = pyqtSignal(str, object)  # task_id, log_entry
    task_started = pyqtSignal(str, str)  # task_id, execution_id
    task_completed = pyqtSignal(str, str, bool)  # task_id, execution_id, success
    
    _instance = None
    
    @classmethod
    def get_instance(cls) -> 'AutomationLogManager':
        """Get the singleton instance"""
        if cls._instance is None:
            cls._instance = AutomationLogManager()
        return cls._instance
    
    def __init__(self):
        """Initialize automation log manager"""
        super().__init__()
        
        # Active task loggers
        self.active_loggers = {}  # (task_id, execution_id) -> TaskLogger
        
        # Maximum number of log files to keep per task
        self.max_logs_per_task = 50
        
        # Base path for logs
        self.logs_dir = Path(os.path.expanduser("~")) / "Documents" / "Pawprinting_PyQt6_V2" / "automation" / "logs"
        os.makedirs(self.logs_dir, exist_ok=True)
        
        logger.info("Automation Log Manager initialized")
    
    def create_task_logger(self, task_id: str, task_name: str, 
                          execution_id: Optional[str] = None) -> TaskLogger:
        """
        Create a new task logger
        
        Args:
            task_id: ID of the task
            task_name: Name of the task
            execution_id: Optional execution ID
            
        Returns:
            task_logger: New task logger
        """
        # Create logger
        task_logger = TaskLogger(task_id, task_name, execution_id)
        
        # Store in active loggers
        self.active_loggers[(task_id, task_logger.execution_id)] = task_logger
        
        # Emit signal
        self.task_started.emit(task_id, task_logger.execution_id)
        
        # Cleanup old logs for this task
        self._cleanup_old_logs(task_id)
        
        return task_logger
    
    def get_task_logger(self, task_id: str, execution_id: str) -> Optional[TaskLogger]:
        """Get an existing task logger"""
        return self.active_loggers.get((task_id, execution_id))
    
    def get_active_task_loggers(self, task_id: Optional[str] = None) -> List[TaskLogger]:
        """Get all active task loggers for a task or all tasks"""
        if task_id:
            return [logger for (tid, _), logger in self.active_loggers.items() if tid == task_id]
        else:
            return list(self.active_loggers.values())
    
    def complete_task_logger(self, task_id: str, execution_id: str, success: bool = True, 
                            message: Optional[str] = None):
        """Mark a task logger as complete"""
        key = (task_id, execution_id)
        if key in self.active_loggers:
            task_logger = self.active_loggers[key]
            task_logger.complete(success, message)
            
            # Remove from active loggers
            del self.active_loggers[key]
            
            # Emit signal
            self.task_completed.emit(task_id, execution_id, success)
            
            return True
        else:
            logger.warning(f"Attempted to complete non-existent task logger: {task_id}/{execution_id}")
            return False
    
    def get_task_execution_logs(self, task_id: str) -> List[Dict[str, Any]]:
        """
        Get all execution logs for a task
        
        Args:
            task_id: ID of the task
            
        Returns:
            logs: List of execution log summaries
        """
        logs = []
        
        # Directory for this task's logs
        task_dir = self.logs_dir / task_id
        
        if not task_dir.exists():
            return []
        
        # Find all JSON log files
        json_files = list(task_dir.glob("*.json"))
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    log_data = json.load(f)
                
                # Extract summary info
                summary = {
                    "task_id": log_data.get("task_id"),
                    "task_name": log_data.get("task_name"),
                    "execution_id": log_data.get("execution_id"),
                    "start_time": log_data.get("start_time"),
                    "end_time": log_data.get("end_time"),
                    "success": log_data.get("success"),
                    "log_file": str(json_file)
                }
                
                logs.append(summary)
                
            except Exception as e:
                logger.error(f"Error reading log file {json_file}: {str(e)}")
        
        # Sort by start time (newest first)
        logs.sort(key=lambda x: x.get("start_time", ""), reverse=True)
        
        return logs
    
    def get_execution_log_details(self, task_id: str, execution_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed log for a specific task execution
        
        Args:
            task_id: ID of the task
            execution_id: ID of the execution
            
        Returns:
            log_data: Complete log data or None if not found
        """
        # Check if this is an active logger
        key = (task_id, execution_id)
        if key in self.active_loggers:
            task_logger = self.active_loggers[key]
            
            # Create log data from active logger
            log_data = {
                "task_id": task_logger.task_id,
                "task_name": task_logger.task_name,
                "execution_id": task_logger.execution_id,
                "start_time": task_logger.start_time.isoformat(),
                "end_time": task_logger.end_time.isoformat() if task_logger.end_time else None,
                "success": task_logger.success,
                "progress": task_logger.progress,
                "logs": [entry.to_dict() for entry in task_logger.logs]
            }
            
            return log_data
        
        # Otherwise look for JSON log file
        json_file = self.logs_dir / task_id / f"{execution_id}.json"
        
        if not json_file.exists():
            return None
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                log_data = json.load(f)
            
            return log_data
            
        except Exception as e:
            logger.error(f"Error reading log file {json_file}: {str(e)}")
            return None
    
    def _cleanup_old_logs(self, task_id: str):
        """Clean up old log files for a task"""
        try:
            task_dir = self.logs_dir / task_id
            
            if not task_dir.exists():
                return
            
            # Get all JSON log files
            json_files = list(task_dir.glob("*.json"))
            
            # If we have more files than the limit, delete the oldest ones
            if len(json_files) > self.max_logs_per_task:
                # Sort by modification time (oldest first)
                json_files.sort(key=lambda x: x.stat().st_mtime)
                
                # Delete oldest files
                for old_file in json_files[:-self.max_logs_per_task]:
                    # Also delete corresponding .log file
                    log_file = old_file.with_suffix(".log")
                    
                    try:
                        if old_file.exists():
                            old_file.unlink()
                        
                        if log_file.exists():
                            log_file.unlink()
                    except Exception as e:
                        logger.error(f"Error deleting old log file {old_file}: {str(e)}")
        
        except Exception as e:
            logger.error(f"Error cleaning up old logs for task {task_id}: {str(e)}")
    
    def export_logs(self, task_id: str, target_dir: str) -> Tuple[int, str]:
        """
        Export all logs for a task to a directory
        
        Args:
            task_id: ID of the task
            target_dir: Target directory
            
        Returns:
            tuple: (number of exported files, target directory)
        """
        try:
            # Source directory
            source_dir = self.logs_dir / task_id
            
            if not source_dir.exists():
                return 0, target_dir
            
            # Create target directory
            os.makedirs(target_dir, exist_ok=True)
            
            # Copy all log files
            count = 0
            for log_file in source_dir.glob("*.*"):
                target_file = os.path.join(target_dir, log_file.name)
                shutil.copy2(log_file, target_file)
                count += 1
            
            logger.info(f"Exported {count} log files for task {task_id} to {target_dir}")
            return count, target_dir
            
        except Exception as e:
            logger.error(f"Error exporting logs for task {task_id}: {str(e)}")
            return 0, target_dir
    
    def delete_task_logs(self, task_id: str) -> int:
        """
        Delete all logs for a task
        
        Args:
            task_id: ID of the task
            
        Returns:
            count: Number of deleted files
        """
        try:
            # Directory for this task's logs
            task_dir = self.logs_dir / task_id
            
            if not task_dir.exists():
                return 0
            
            # Count files to delete
            count = len(list(task_dir.glob("*.*")))
            
            # Remove the directory and all its contents
            shutil.rmtree(task_dir)
            
            logger.info(f"Deleted {count} log files for task {task_id}")
            return count
            
        except Exception as e:
            logger.error(f"Error deleting logs for task {task_id}: {str(e)}")
            return 0
