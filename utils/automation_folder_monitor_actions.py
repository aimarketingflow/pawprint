#!/usr/bin/env python3
"""
Folder Monitoring Actions for Pawprinting PyQt6 V2 Automation

Provides actions for monitoring folders and responding to file changes
for use in the automation system.

Author: AIMF LLC
Date: June 20, 2025
"""

import os
import sys
import logging
from enum import Enum
from typing import Dict, List, Any, Optional, Set, Tuple
from datetime import datetime
from pathlib import Path

from PyQt6.QtCore import QObject, pyqtSignal, QTimer

from utils.automation_action_base import Action, ActionResult, ActionContext
from utils.folder_monitor import FolderMonitor, FolderMonitorManager, FileChangeType

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.automation.folder_monitor_actions")

class StartMonitorAction(Action):
    """Action to start monitoring a folder"""
    
    def __init__(self, action_id: str, config: Dict[str, Any] = None):
        """Initialize start monitor action"""
        super().__init__(action_id, config or {})
        self.display_name = self.config.get("display_name", "Start Folder Monitor")
        self.description = self.config.get("description", "Starts monitoring a folder for changes")
    
    def validate_config(self) -> Tuple[bool, str]:
        """Validate configuration"""
        if "folder_path" not in self.config:
            return False, "Folder path is required"
        if "monitor_id" not in self.config:
            return False, "Monitor ID is required"
        return True, ""
    
    def execute(self, context: ActionContext) -> ActionResult:
        """Execute the start monitor action"""
        folder_path = self.config.get("folder_path")
        monitor_id = self.config.get("monitor_id")
        recursive = self.config.get("recursive", True)
        file_patterns = self.config.get("file_patterns", [])
        exclude_patterns = self.config.get("exclude_patterns", [])
        check_interval = self.config.get("check_interval", 2.0)
        
        # Check if folder exists
        if not os.path.exists(folder_path):
            return ActionResult.failure(f"Folder does not exist: {folder_path}")
        
        # Check if it's a directory
        if not os.path.isdir(folder_path):
            return ActionResult.failure(f"Path is not a directory: {folder_path}")
        
        try:
            context.logger.info(f"Starting folder monitor for {folder_path} with ID {monitor_id}")
            
            # Get monitor manager
            monitor_manager = FolderMonitorManager.get_instance()
            
            # Check if monitor with this ID already exists
            existing_monitors = monitor_manager.monitors
            if monitor_id in existing_monitors:
                context.logger.warning(f"Monitor with ID {monitor_id} already exists")
                
                # If monitor exists, stop it first to reset configuration
                monitor_manager.stop_monitor(monitor_id)
                monitor_manager.remove_monitor(monitor_id)
                context.logger.info(f"Removed existing monitor with ID {monitor_id}")
            
            # Create monitor configuration
            monitor_config = {
                "check_interval": check_interval,
                "recursive": recursive,
                "file_patterns": file_patterns,
                "exclude_patterns": exclude_patterns
            }
            
            # Add the monitor
            success = monitor_manager.add_monitor(monitor_id, folder_path, monitor_config)
            if not success:
                return ActionResult.failure(f"Failed to add folder monitor for {folder_path}")
            
            # Start the monitor
            success = monitor_manager.start_monitor(monitor_id)
            if not success:
                return ActionResult.failure(f"Failed to start folder monitor for {folder_path}")
            
            context.logger.info(f"Successfully started monitoring folder: {folder_path}")
            
            return ActionResult.success(
                f"Folder monitoring started successfully",
                {
                    "folder_path": folder_path,
                    "monitor_id": monitor_id,
                    "recursive": recursive,
                    "file_patterns": file_patterns,
                    "exclude_patterns": exclude_patterns
                }
            )
            
        except Exception as e:
            context.logger.exception(f"Error starting folder monitor for {folder_path}: {str(e)}")
            return ActionResult.from_exception(e, f"Failed to start folder monitor for {folder_path}")

class StopMonitorAction(Action):
    """Action to stop monitoring a folder"""
    
    def __init__(self, action_id: str, config: Dict[str, Any] = None):
        """Initialize stop monitor action"""
        super().__init__(action_id, config or {})
        self.display_name = self.config.get("display_name", "Stop Folder Monitor")
        self.description = self.config.get("description", "Stops monitoring a folder")
    
    def validate_config(self) -> Tuple[bool, str]:
        """Validate configuration"""
        if "monitor_id" not in self.config:
            return False, "Monitor ID is required"
        return True, ""
    
    def execute(self, context: ActionContext) -> ActionResult:
        """Execute the stop monitor action"""
        monitor_id = self.config.get("monitor_id")
        
        try:
            context.logger.info(f"Stopping folder monitor with ID {monitor_id}")
            
            # Get monitor manager
            monitor_manager = FolderMonitorManager.get_instance()
            
            # Check if monitor exists
            if monitor_id not in monitor_manager.monitors:
                return ActionResult.failure(f"Monitor with ID {monitor_id} does not exist")
            
            # Get the folder path for the monitor (for reporting)
            folder_path = monitor_manager.monitors[monitor_id].folder_path
            
            # Stop the monitor
            success = monitor_manager.stop_monitor(monitor_id)
            if not success:
                return ActionResult.failure(f"Failed to stop folder monitor with ID {monitor_id}")
            
            context.logger.info(f"Successfully stopped monitoring folder: {folder_path}")
            
            return ActionResult.success(
                f"Folder monitoring stopped successfully",
                {
                    "monitor_id": monitor_id,
                    "folder_path": folder_path
                }
            )
            
        except Exception as e:
            context.logger.exception(f"Error stopping folder monitor: {str(e)}")
            return ActionResult.from_exception(e, f"Failed to stop folder monitor")

class RemoveMonitorAction(Action):
    """Action to remove a folder monitor"""
    
    def __init__(self, action_id: str, config: Dict[str, Any] = None):
        """Initialize remove monitor action"""
        super().__init__(action_id, config or {})
        self.display_name = self.config.get("display_name", "Remove Folder Monitor")
        self.description = self.config.get("description", "Removes a folder monitor")
    
    def validate_config(self) -> Tuple[bool, str]:
        """Validate configuration"""
        if "monitor_id" not in self.config:
            return False, "Monitor ID is required"
        return True, ""
    
    def execute(self, context: ActionContext) -> ActionResult:
        """Execute the remove monitor action"""
        monitor_id = self.config.get("monitor_id")
        
        try:
            context.logger.info(f"Removing folder monitor with ID {monitor_id}")
            
            # Get monitor manager
            monitor_manager = FolderMonitorManager.get_instance()
            
            # Check if monitor exists
            if monitor_id not in monitor_manager.monitors:
                return ActionResult.failure(f"Monitor with ID {monitor_id} does not exist")
            
            # Get the folder path for the monitor (for reporting)
            folder_path = monitor_manager.monitors[monitor_id].folder_path
            
            # Remove the monitor (this also stops it)
            success = monitor_manager.remove_monitor(monitor_id)
            if not success:
                return ActionResult.failure(f"Failed to remove folder monitor with ID {monitor_id}")
            
            context.logger.info(f"Successfully removed monitor for folder: {folder_path}")
            
            return ActionResult.success(
                f"Folder monitor removed successfully",
                {
                    "monitor_id": monitor_id,
                    "folder_path": folder_path
                }
            )
            
        except Exception as e:
            context.logger.exception(f"Error removing folder monitor: {str(e)}")
            return ActionResult.from_exception(e, f"Failed to remove folder monitor")

class MonitorWaitAction(Action):
    """Action to wait for file changes in a monitored folder"""
    
    def __init__(self, action_id: str, config: Dict[str, Any] = None):
        """Initialize monitor wait action"""
        super().__init__(action_id, config or {})
        self.display_name = self.config.get("display_name", "Wait for File Changes")
        self.description = self.config.get("description", "Waits for file changes in a monitored folder")
        self._timer = None
        self._changes_detected = False
        self._canceled = False
        self._monitor_id = None
        self._detected_changes = []
    
    def validate_config(self) -> Tuple[bool, str]:
        """Validate configuration"""
        if "monitor_id" not in self.config:
            return False, "Monitor ID is required"
        if "timeout_seconds" not in self.config:
            return False, "Timeout is required"
        return True, ""
    
    def _on_file_created(self, folder_id: str, file_path: str):
        """Handler for file created event"""
        if folder_id != self._monitor_id:
            return
        
        self._changes_detected = True
        self._detected_changes.append({
            "type": "created",
            "path": file_path,
            "timestamp": datetime.now().isoformat()
        })
    
    def _on_file_modified(self, folder_id: str, file_path: str):
        """Handler for file modified event"""
        if folder_id != self._monitor_id:
            return
        
        self._changes_detected = True
        self._detected_changes.append({
            "type": "modified",
            "path": file_path,
            "timestamp": datetime.now().isoformat()
        })
    
    def _on_file_deleted(self, folder_id: str, file_path: str):
        """Handler for file deleted event"""
        if folder_id != self._monitor_id:
            return
        
        self._changes_detected = True
        self._detected_changes.append({
            "type": "deleted",
            "path": file_path,
            "timestamp": datetime.now().isoformat()
        })
    
    def execute(self, context: ActionContext) -> ActionResult:
        """Execute the monitor wait action"""
        from PyQt6.QtCore import QEventLoop, QTimer
        
        monitor_id = self.config.get("monitor_id")
        timeout_seconds = self.config.get("timeout_seconds")
        change_types = self.config.get("change_types", ["created", "modified", "deleted"])
        min_changes = self.config.get("min_changes", 1)
        
        self._monitor_id = monitor_id
        
        try:
            context.logger.info(f"Waiting for changes in monitor {monitor_id} (timeout: {timeout_seconds}s)")
            
            # Get monitor manager
            monitor_manager = FolderMonitorManager.get_instance()
            
            # Check if monitor exists
            if monitor_id not in monitor_manager.monitors:
                return ActionResult.failure(f"Monitor with ID {monitor_id} does not exist")
            
            # Reset state
            self._changes_detected = False
            self._canceled = False
            self._detected_changes = []
            
            # Connect to monitor signals
            if "created" in change_types:
                monitor_manager.file_created.connect(self._on_file_created)
            if "modified" in change_types:
                monitor_manager.file_modified.connect(self._on_file_modified)
            if "deleted" in change_types:
                monitor_manager.file_deleted.connect(self._on_file_deleted)
            
            # Create event loop for waiting
            loop = QEventLoop()
            
            # Create timer for timeout
            timer = QTimer()
            timer.setSingleShot(True)
            timer.timeout.connect(loop.quit)
            
            # Create timer to check for changes
            check_timer = QTimer()
            check_timer.setInterval(100)  # Check every 100ms
            
            # Define check function
            def check_changes():
                if self._changes_detected and len(self._detected_changes) >= min_changes:
                    loop.quit()
                if self._canceled:
                    loop.quit()
            
            check_timer.timeout.connect(check_changes)
            
            # Start timers
            timer.start(timeout_seconds * 1000)  # Convert to milliseconds
            check_timer.start()
            
            # Wait for changes or timeout
            context.logger.info(f"Waiting for file changes...")
            loop.exec()  # This blocks until the loop is exited
            
            # Clean up
            if "created" in change_types:
                try: monitor_manager.file_created.disconnect(self._on_file_created)
                except: pass
            if "modified" in change_types:
                try: monitor_manager.file_modified.disconnect(self._on_file_modified)
                except: pass
            if "deleted" in change_types:
                try: monitor_manager.file_deleted.disconnect(self._on_file_deleted)
                except: pass
            
            # Check why we exited
            if self._canceled:
                return ActionResult.failure(
                    "Wait for file changes was canceled",
                    {"monitor_id": monitor_id}
                )
            
            if not self._changes_detected or len(self._detected_changes) < min_changes:
                return ActionResult.failure(
                    f"Timed out waiting for file changes after {timeout_seconds} seconds",
                    {
                        "monitor_id": monitor_id,
                        "timeout_seconds": timeout_seconds,
                        "detected_changes": len(self._detected_changes),
                        "changes": self._detected_changes
                    }
                )
            
            context.logger.info(f"Detected {len(self._detected_changes)} file changes")
            
            return ActionResult.success(
                f"Detected {len(self._detected_changes)} file changes",
                {
                    "monitor_id": monitor_id,
                    "detected_changes": len(self._detected_changes),
                    "changes": self._detected_changes
                }
            )
            
        except Exception as e:
            context.logger.exception(f"Error waiting for file changes: {str(e)}")
            return ActionResult.from_exception(e, f"Failed to wait for file changes")
    
    def cancel(self) -> bool:
        """Cancel waiting for file changes"""
        self._canceled = True
        return True
