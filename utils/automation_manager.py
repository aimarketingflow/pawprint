#!/usr/bin/env python3
"""
Automation Manager for Pawprinting PyQt6 V2

Provides core functionality for automating Pawprinting tasks including
scheduling, folder monitoring, and task execution.

Author: AIMF LLC
Date: June 20, 2025
"""

import os
import sys
import time
import json
import logging
import threading
from enum import Enum
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime, timedelta
from pathlib import Path

from PyQt6.QtCore import QObject, pyqtSignal, QTimer

from utils.state_manager import StateManager

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.automation")

class AutomationStatus(Enum):
    """Status of an automation task"""
    IDLE = "idle"
    SCHEDULED = "scheduled"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class AutomationManager(QObject):
    """
    Manages automation tasks for the Pawprinting application.
    Implemented as a Singleton.
    """
    
    # Signals
    task_started = pyqtSignal(str)  # task_id
    task_completed = pyqtSignal(str)  # task_id
    task_failed = pyqtSignal(str, str)  # task_id, error_message
    task_status_changed = pyqtSignal(str, object)  # task_id, new_status
    
    _instance = None
    
    @classmethod
    def get_instance(cls) -> 'AutomationManager':
        """Get the singleton instance"""
        if cls._instance is None:
            cls._instance = AutomationManager()
        return cls._instance
    
    def __init__(self):
        """Initialize automation manager"""
        super().__init__()
        self.state_manager = StateManager.get_instance()
        
        # Task information
        self.tasks = {}  # Dictionary of tasks
        self.active_timers = {}  # Task timers for scheduled tasks
        self.folder_monitors = {}  # Dictionary of folder monitoring threads
        
        # Load existing tasks
        self._load_tasks()
        
        logger.info("Automation Manager initialized")
    
    def _load_tasks(self):
        """Load tasks from state manager"""
        tasks = self.state_manager.get_settings().get("automation", {}).get("tasks", {})
        self.tasks = tasks
        
        # Validate and update task status
        for task_id, task in self.tasks.items():
            # Set tasks to idle if they were previously running
            if task.get("status") == AutomationStatus.RUNNING.value:
                task["status"] = AutomationStatus.IDLE.value
        
        logger.debug(f"Loaded {len(self.tasks)} automation tasks")
    
    def save_tasks(self):
        """Save tasks to state manager"""
        automation_settings = self.state_manager.get_settings().get("automation", {})
        automation_settings["tasks"] = self.tasks
        self.state_manager.update_settings("automation", automation_settings)
        self.state_manager.save_state()
        logger.debug(f"Saved {len(self.tasks)} automation tasks")
    
    def create_task(self, task_config: Dict[str, Any]) -> str:
        """
        Create a new automation task
        
        Args:
            task_config: Dictionary containing task configuration
                Required keys:
                - name: Task name
                - type: Task type (scheduled, folder_monitor)
                - actions: List of actions to perform
                
                For scheduled tasks:
                - schedule: Dictionary with schedule information
                    - type: one-time, daily, weekly, monthly
                    - time: ISO format time string
                    - days: List of days (for weekly)
                    
                For folder monitor tasks:
                - folder_path: Path to monitor
                - monitor_interval: Seconds between checks
                - trigger_on: List of triggers (new_file, modified_file, deleted_file)
        
        Returns:
            task_id: ID of the created task
        """
        # Validate required fields
        required_fields = ["name", "type", "actions"]
        for field in required_fields:
            if field not in task_config:
                raise ValueError(f"Missing required field: {field}")
        
        # Create task ID
        task_id = f"task_{int(time.time())}_{task_config['name'].lower().replace(' ', '_')}"
        
        # Add status
        task_config["status"] = AutomationStatus.IDLE.value
        task_config["created"] = datetime.now().isoformat()
        task_config["last_run"] = None
        task_config["last_result"] = None
        
        # Add to tasks dictionary
        self.tasks[task_id] = task_config
        
        # Save tasks
        self.save_tasks()
        
        logger.info(f"Created automation task: {task_config['name']} ({task_id})")
        return task_id
    
    def update_task(self, task_id: str, task_config: Dict[str, Any]) -> bool:
        """
        Update an existing task
        
        Args:
            task_id: ID of the task to update
            task_config: New task configuration
            
        Returns:
            success: True if task was updated successfully
        """
        if task_id not in self.tasks:
            logger.warning(f"Attempted to update non-existent task: {task_id}")
            return False
        
        # Preserve certain fields
        original_task = self.tasks[task_id]
        for preserve_field in ["created", "last_run", "last_result"]:
            if preserve_field in original_task and preserve_field not in task_config:
                task_config[preserve_field] = original_task[preserve_field]
        
        # Update task
        self.tasks[task_id] = task_config
        
        # Save tasks
        self.save_tasks()
        
        logger.info(f"Updated automation task: {task_config['name']} ({task_id})")
        return True
    
    def delete_task(self, task_id: str) -> bool:
        """
        Delete an automation task
        
        Args:
            task_id: ID of the task to delete
            
        Returns:
            success: True if task was deleted successfully
        """
        if task_id not in self.tasks:
            logger.warning(f"Attempted to delete non-existent task: {task_id}")
            return False
        
        # Stop task if it's running
        self.stop_task(task_id)
        
        # Delete task
        del self.tasks[task_id]
        
        # Save tasks
        self.save_tasks()
        
        logger.info(f"Deleted automation task: {task_id}")
        return True
    
    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task configuration by ID"""
        return self.tasks.get(task_id)
    
    def get_all_tasks(self) -> Dict[str, Dict[str, Any]]:
        """Get all tasks"""
        return self.tasks
    
    def start_task(self, task_id: str) -> bool:
        """
        Start an automation task
        
        Args:
            task_id: ID of the task to start
            
        Returns:
            success: True if task was started successfully
        """
        if task_id not in self.tasks:
            logger.warning(f"Attempted to start non-existent task: {task_id}")
            return False
        
        task = self.tasks[task_id]
        
        # Check if task is already running
        if task["status"] == AutomationStatus.RUNNING.value:
            logger.warning(f"Task {task_id} is already running")
            return False
        
        # Set task status to running
        task["status"] = AutomationStatus.RUNNING.value
        task["last_run"] = datetime.now().isoformat()
        self.task_status_changed.emit(task_id, AutomationStatus.RUNNING)
        
        # Save tasks
        self.save_tasks()
        
        # Start the task based on its type
        if task["type"] == "scheduled":
            self._setup_scheduled_task(task_id, task)
        elif task["type"] == "folder_monitor":
            self._start_folder_monitor(task_id, task)
        else:
            logger.error(f"Unknown task type: {task['type']}")
            task["status"] = AutomationStatus.FAILED.value
            task["last_result"] = f"Unknown task type: {task['type']}"
            self.task_status_changed.emit(task_id, AutomationStatus.FAILED)
            self.save_tasks()
            return False
        
        self.task_started.emit(task_id)
        logger.info(f"Started automation task: {task['name']} ({task_id})")
        return True
    
    def stop_task(self, task_id: str) -> bool:
        """
        Stop an automation task
        
        Args:
            task_id: ID of the task to stop
            
        Returns:
            success: True if task was stopped successfully
        """
        if task_id not in self.tasks:
            logger.warning(f"Attempted to stop non-existent task: {task_id}")
            return False
        
        task = self.tasks[task_id]
        
        # Check if task is running
        if task["status"] != AutomationStatus.RUNNING.value:
            logger.warning(f"Task {task_id} is not running")
            return False
        
        # Stop scheduled timer if it exists
        if task_id in self.active_timers:
            timer = self.active_timers[task_id]
            timer.stop()
            del self.active_timers[task_id]
        
        # Stop folder monitor if it exists
        if task_id in self.folder_monitors:
            monitor = self.folder_monitors[task_id]
            monitor["running"] = False
            if "thread" in monitor and monitor["thread"].is_alive():
                # Wait for monitor thread to stop
                monitor["thread"].join(1.0)  # Wait up to 1 second
            del self.folder_monitors[task_id]
        
        # Set task status to idle
        task["status"] = AutomationStatus.IDLE.value
        self.task_status_changed.emit(task_id, AutomationStatus.IDLE)
        
        # Save tasks
        self.save_tasks()
        
        logger.info(f"Stopped automation task: {task['name']} ({task_id})")
        return True
    
    def _setup_scheduled_task(self, task_id: str, task: Dict[str, Any]):
        """Set up a scheduled task"""
        # Get schedule information
        schedule = task.get("schedule", {})
        schedule_type = schedule.get("type", "one-time")
        
        if schedule_type == "one-time":
            # Schedule task to run once
            self._schedule_one_time_task(task_id, task)
        elif schedule_type in ["daily", "weekly", "monthly"]:
            # Schedule recurring task
            self._schedule_recurring_task(task_id, task)
        else:
            logger.error(f"Unknown schedule type: {schedule_type}")
            task["status"] = AutomationStatus.FAILED.value
            task["last_result"] = f"Unknown schedule type: {schedule_type}"
            self.task_status_changed.emit(task_id, AutomationStatus.FAILED)
            self.save_tasks()
    
    def _schedule_one_time_task(self, task_id: str, task: Dict[str, Any]):
        """Schedule a one-time task"""
        # Implementation will be expanded in subsequent components
        pass
    
    def _schedule_recurring_task(self, task_id: str, task: Dict[str, Any]):
        """Schedule a recurring task"""
        # Implementation will be expanded in subsequent components
        pass
    
    def _start_folder_monitor(self, task_id: str, task: Dict[str, Any]):
        """Start a folder monitor task"""
        # Implementation will be expanded in subsequent components
        pass
    
    def _execute_task_actions(self, task_id: str, task: Dict[str, Any]):
        """Execute the actions defined for a task"""
        # Implementation will be expanded in subsequent components
        pass
