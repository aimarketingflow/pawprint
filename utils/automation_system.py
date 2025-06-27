#!/usr/bin/env python3
"""
Automation System Integration for Pawprinting PyQt6 V2

Main entry point for the automation system that initializes and
connects all components.

Author: AIMF LLC
Date: June 20, 2025
"""

import os
import sys
import logging
import json
from typing import Dict, List, Any, Optional
from pathlib import Path

from PyQt6.QtCore import QObject, pyqtSignal

from utils.automation_task_types import TaskExecutionStatus, TaskPriority, TaskTriggerType
from utils.automation_task_result import TaskExecutionResult
from utils.automation_task_context import TaskContext
from utils.automation_task_worker import TaskExecutorWorker
from utils.automation_task_manager import TaskManager, get_task_manager
from utils.automation_task_scheduler import TaskScheduler, get_task_scheduler
from utils.automation_task_trigger import TaskTriggerManager, get_task_trigger_manager
from utils.automation_task_factory import TaskFactory, get_task_factory
from utils.automation_task_history import TaskHistoryManager, get_task_history_manager
from utils.automation_state import AutomationState
from utils.automation_logging import AutomationLogManager, get_log_manager
from utils.folder_monitor import FolderMonitorManager

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.automation.system")

class AutomationSystem(QObject):
    """
    Central integration point for the Pawprinting PyQt6 V2 automation system.
    
    This class initializes and connects all automation components:
    - Task Manager: Executes and tracks tasks
    - Task Scheduler: Schedules tasks to run at specific times
    - Task Trigger Manager: Triggers tasks on events (file changes, etc.)
    - Task Factory: Creates action instances from configurations
    - Task History: Maintains a history of task executions
    - Automation State: Persists configurations and state
    - Log Manager: Centralized logging for tasks
    - Folder Monitor: Watches folders for changes
    """
    
    # Signals
    system_initialized = pyqtSignal()
    system_started = pyqtSignal()
    system_stopped = pyqtSignal()
    system_error = pyqtSignal(str)
    
    def __init__(self, app_data_dir: Optional[str] = None):
        """Initialize automation system"""
        super().__init__()
        
        # Set up data directory
        self._app_data_dir = app_data_dir
        if not self._app_data_dir:
            # Default to user's home directory
            self._app_data_dir = os.path.join(
                os.path.expanduser("~"),
                "Pawprinting_PyQt6_V2",
                "automation"
            )
            
        # Create data directories if they don't exist
        self._ensure_directories()
        
        # Get component managers
        self._task_manager = get_task_manager()
        self._scheduler = get_task_scheduler()
        self._trigger_manager = get_task_trigger_manager()
        self._task_factory = get_task_factory()
        self._history_manager = get_task_history_manager()
        self._log_manager = get_log_manager()
        
        # Get state manager
        self._state = AutomationState.get_instance()
        
        # Get folder monitor manager
        self._folder_monitor = FolderMonitorManager.get_instance()
        
        # Initialization flag
        self._initialized = False
        self._running = False
        
    def initialize(self) -> bool:
        """Initialize the automation system"""
        try:
            logger.info("Initializing automation system...")
            
            # Set up directory for state
            self._state.set_data_directory(os.path.join(self._app_data_dir, "state"))
            
            # Set up directory for logs
            self._log_manager.set_log_directory(os.path.join(self._app_data_dir, "logs"))
            
            # Connect task completion to history
            self._connect_signals()
            
            # Auto-discover action classes
            self._task_factory.discover_action_classes()
            
            # Load persisted state if it exists
            self._load_state()
            
            self._initialized = True
            self.system_initialized.emit()
            logger.info("Automation system initialized successfully")
            return True
            
        except Exception as e:
            logger.exception("Failed to initialize automation system")
            self.system_error.emit(f"Initialization error: {str(e)}")
            return False
            
    def start(self) -> bool:
        """Start the automation system"""
        if not self._initialized:
            logger.error("Cannot start: automation system not initialized")
            self.system_error.emit("Cannot start: automation system not initialized")
            return False
            
        if self._running:
            logger.info("Automation system already running")
            return True
            
        try:
            logger.info("Starting automation system...")
            
            # Start folder monitoring
            self._folder_monitor.start_all_monitors()
            
            # Start task scheduler
            self._scheduler.start()
            
            self._running = True
            self.system_started.emit()
            logger.info("Automation system started successfully")
            return True
            
        except Exception as e:
            logger.exception("Failed to start automation system")
            self.system_error.emit(f"Start error: {str(e)}")
            return False
            
    def stop(self) -> bool:
        """Stop the automation system"""
        if not self._running:
            logger.info("Automation system already stopped")
            return True
            
        try:
            logger.info("Stopping automation system...")
            
            # Stop task scheduler
            self._scheduler.stop()
            
            # Stop folder monitoring
            self._folder_monitor.stop_all_monitors()
            
            # Cancel any running tasks
            self._task_manager.cancel_all_tasks()
            
            # Save state
            self._save_state()
            
            self._running = False
            self.system_stopped.emit()
            logger.info("Automation system stopped successfully")
            return True
            
        except Exception as e:
            logger.exception("Failed to stop automation system")
            self.system_error.emit(f"Stop error: {str(e)}")
            return False
            
    def is_running(self) -> bool:
        """Check if system is running"""
        return self._running
        
    def is_initialized(self) -> bool:
        """Check if system is initialized"""
        return self._initialized
        
    def _ensure_directories(self) -> None:
        """Ensure required directories exist"""
        directories = [
            self._app_data_dir,
            os.path.join(self._app_data_dir, "state"),
            os.path.join(self._app_data_dir, "logs"),
            os.path.join(self._app_data_dir, "configs"),
            os.path.join(self._app_data_dir, "temp")
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
            
    def _connect_signals(self) -> None:
        """Connect component signals"""
        # When task is completed, update history
        self._task_manager.task_completed.connect(self._on_task_completed)
        
        # Connect log signals
        self._log_manager.log_added.connect(self._on_log_added)
        
        # Connect scheduler signals
        self._scheduler.schedule_triggered.connect(self._on_schedule_triggered)
        
        # Connect trigger signals
        self._trigger_manager.trigger_fired.connect(self._on_trigger_fired)
        
    def _on_task_completed(self, task_id: str, result: TaskExecutionResult) -> None:
        """Handle task completion"""
        # Update execution history
        from utils.automation_task_history import TaskExecution
        import uuid
        from datetime import datetime
        
        # Find task details from manager
        task_info = self._task_manager.get_task_info(task_id)
        if not task_info:
            logger.warning(f"Task {task_id} completed but not found in manager")
            return
            
        # Create execution record
        execution = TaskExecution(
            execution_id=f"exec_{uuid.uuid4().hex[:8]}",
            task_id=task_id,
            action_id=task_info.get("action_id", "unknown"),
            action_type=task_info.get("action_type", "unknown"),
            start_time=task_info.get("start_time", datetime.now()),
            end_time=datetime.now(),
            status=result.status,
            result=result.to_dict()
        )
        
        # Add to history
        self._history_manager.add_execution(execution)
        
    def _on_log_added(self, task_id: str, level: int, message: str) -> None:
        """Handle log added"""
        # Could be used to show log notifications in UI
        pass
        
    def _on_schedule_triggered(self, schedule_id: str, task_id: str) -> None:
        """Handle schedule triggered"""
        logger.info(f"Schedule {schedule_id} triggered task {task_id}")
        
    def _on_trigger_fired(self, trigger_id: str, task_id: str) -> None:
        """Handle trigger fired"""
        logger.info(f"Trigger {trigger_id} fired task {task_id}")
        
    def _load_state(self) -> None:
        """Load persisted state"""
        if self._state.load():
            logger.info("Loaded automation state")
            
            # Load items from state
            # TODO: Implement state loading
            
    def _save_state(self) -> None:
        """Save current state"""
        # TODO: Save current configurations to state
        
        if self._state.save():
            logger.info("Saved automation state")

# Singleton instance
_instance = None

def get_automation_system(app_data_dir: Optional[str] = None) -> AutomationSystem:
    """Get the singleton automation system instance"""
    global _instance
    if _instance is None:
        _instance = AutomationSystem(app_data_dir)
    return _instance
