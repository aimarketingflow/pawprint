#!/usr/bin/env python3
"""
Automation State Manager for Pawprinting PyQt6 V2

Manages persistent storage and retrieval of automation tasks, configurations,
and execution history.

Author: AIMF LLC
Date: June 20, 2025
"""

import os
import json
import logging
import threading
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import shutil

from PyQt6.QtCore import QObject, pyqtSignal

from utils.state_manager import StateManager

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.automation.state")

class AutomationState(QObject):
    """
    Manages persistent state for automation tasks and configurations
    """
    
    # Signals
    state_loaded = pyqtSignal()
    state_saved = pyqtSignal()
    tasks_updated = pyqtSignal()
    
    _instance = None
    
    @classmethod
    def get_instance(cls) -> 'AutomationState':
        """Get the singleton instance"""
        if cls._instance is None:
            cls._instance = AutomationState()
        return cls._instance
    
    def __init__(self):
        """Initialize automation state manager"""
        super().__init__()
        self.state_manager = StateManager.get_instance()
        
        # Automation data
        self.tasks = {}
        self.monitors = {}
        self.schedules = {}
        self.history = []
        
        # State file locations
        self.base_data_dir = Path(os.path.expanduser("~")) / "Documents" / "Pawprinting_PyQt6_V2" / "automation"
        self.tasks_file = self.base_data_dir / "tasks.json"
        self.history_file = self.base_data_dir / "history.json"
        self.backup_dir = self.base_data_dir / "backups"
        
        # Create necessary directories
        self._ensure_directories()
        
        # Load state
        self._load_state()
        
        logger.info("Automation State Manager initialized")
    
    def _ensure_directories(self):
        """Ensure necessary directories exist"""
        try:
            self.base_data_dir.mkdir(parents=True, exist_ok=True)
            self.backup_dir.mkdir(exist_ok=True)
            logger.debug(f"Ensured directories exist: {self.base_data_dir}")
        except Exception as e:
            logger.error(f"Error creating directories: {str(e)}")
    
    def _load_state(self):
        """Load automation state from files"""
        try:
            # Load tasks
            if self.tasks_file.exists():
                with open(self.tasks_file, 'r') as f:
                    self.tasks = json.load(f)
                logger.info(f"Loaded {len(self.tasks)} automation tasks")
            
            # Load history
            if self.history_file.exists():
                with open(self.history_file, 'r') as f:
                    self.history = json.load(f)
                logger.info(f"Loaded {len(self.history)} history entries")
            
            # Emit signal
            self.state_loaded.emit()
            
        except Exception as e:
            logger.error(f"Error loading automation state: {str(e)}")
            
            # Try to recover from backups if loading failed
            self._try_recover_from_backup()
    
    def save_state(self):
        """Save automation state to files"""
        try:
            # Create backup first
            self._create_backup()
            
            # Save tasks
            with open(self.tasks_file, 'w') as f:
                json.dump(self.tasks, f, indent=2)
            
            # Save history
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=2)
            
            logger.info("Saved automation state")
            
            # Emit signal
            self.state_saved.emit()
            
            return True
            
        except Exception as e:
            logger.error(f"Error saving automation state: {str(e)}")
            return False
    
    def _create_backup(self):
        """Create a backup of the current state"""
        try:
            # Use timestamp for backup name
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            backup_dir = self.backup_dir / timestamp
            backup_dir.mkdir(exist_ok=True)
            
            # Copy files to backup
            if self.tasks_file.exists():
                shutil.copy2(self.tasks_file, backup_dir / "tasks.json")
            
            if self.history_file.exists():
                shutil.copy2(self.history_file, backup_dir / "history.json")
            
            logger.debug(f"Created automation state backup: {backup_dir}")
            
            # Clean up old backups (keep last 10)
            self._cleanup_old_backups(10)
            
        except Exception as e:
            logger.error(f"Error creating backup: {str(e)}")
    
    def _cleanup_old_backups(self, keep_count: int):
        """Clean up old backups, keeping only the specified number"""
        try:
            # Get list of backup directories sorted by name (timestamp)
            backup_dirs = [d for d in self.backup_dir.iterdir() if d.is_dir()]
            backup_dirs.sort()
            
            # Remove oldest if we have more than the keep count
            if len(backup_dirs) > keep_count:
                for old_dir in backup_dirs[:-keep_count]:
                    shutil.rmtree(old_dir)
                    logger.debug(f"Removed old backup: {old_dir}")
                    
        except Exception as e:
            logger.error(f"Error cleaning up old backups: {str(e)}")
    
    def _try_recover_from_backup(self):
        """Try to recover state from the most recent backup"""
        try:
            # Get list of backup directories sorted by name (timestamp)
            backup_dirs = [d for d in self.backup_dir.iterdir() if d.is_dir()]
            backup_dirs.sort()
            
            if not backup_dirs:
                logger.warning("No backups found for recovery")
                return False
            
            # Get most recent backup
            latest_backup = backup_dirs[-1]
            
            # Copy backup files to main location
            backup_tasks = latest_backup / "tasks.json"
            if backup_tasks.exists():
                shutil.copy2(backup_tasks, self.tasks_file)
            
            backup_history = latest_backup / "history.json"
            if backup_history.exists():
                shutil.copy2(backup_history, self.history_file)
            
            logger.info(f"Recovered automation state from backup: {latest_backup}")
            
            # Try loading again
            self._load_state()
            return True
            
        except Exception as e:
            logger.error(f"Error recovering from backup: {str(e)}")
            return False
    
    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get a task by ID"""
        return self.tasks.get(task_id)
    
    def get_all_tasks(self) -> Dict[str, Dict[str, Any]]:
        """Get all tasks"""
        return self.tasks.copy()
    
    def add_task(self, task_id: str, task_data: Dict[str, Any]) -> bool:
        """Add a new task to the state"""
        if task_id in self.tasks:
            logger.warning(f"Task {task_id} already exists, use update_task instead")
            return False
        
        self.tasks[task_id] = task_data
        self.save_state()
        self.tasks_updated.emit()
        logger.info(f"Added task: {task_id}")
        return True
    
    def update_task(self, task_id: str, task_data: Dict[str, Any]) -> bool:
        """Update an existing task"""
        if task_id not in self.tasks:
            logger.warning(f"Task {task_id} does not exist, use add_task instead")
            return False
        
        self.tasks[task_id] = task_data
        self.save_state()
        self.tasks_updated.emit()
        logger.info(f"Updated task: {task_id}")
        return True
    
    def delete_task(self, task_id: str) -> bool:
        """Delete a task"""
        if task_id not in self.tasks:
            logger.warning(f"Task {task_id} does not exist")
            return False
        
        del self.tasks[task_id]
        self.save_state()
        self.tasks_updated.emit()
        logger.info(f"Deleted task: {task_id}")
        return True
    
    def add_history_entry(self, event_type: str, task_id: Optional[str], 
                         details: Dict[str, Any]) -> str:
        """
        Add an entry to the task execution history
        
        Args:
            event_type: Type of event (e.g., task_started, task_completed)
            task_id: ID of the related task (or None if not associated with a task)
            details: Additional event details
            
        Returns:
            event_id: ID of the created history entry
        """
        timestamp = datetime.now().isoformat()
        event_id = f"event_{int(datetime.now().timestamp())}"
        
        # Create history entry
        entry = {
            "id": event_id,
            "timestamp": timestamp,
            "type": event_type,
            "task_id": task_id,
            "details": details
        }
        
        # Add to history
        self.history.append(entry)
        
        # Limit history size
        max_history = 1000  # Configurable
        if len(self.history) > max_history:
            self.history = self.history[-max_history:]
        
        # Save periodically (not every time to improve performance)
        # Currently saving every time, could optimize later
        self.save_state()
        
        logger.debug(f"Added history entry: {event_type} for task {task_id}")
        return event_id
    
    def get_history(self, limit: int = 100, 
                   task_id: Optional[str] = None,
                   event_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get history entries with optional filtering
        
        Args:
            limit: Maximum number of entries to return
            task_id: Filter by task ID
            event_type: Filter by event type
            
        Returns:
            entries: List of matching history entries
        """
        # Apply filters
        filtered = self.history
        
        if task_id is not None:
            filtered = [e for e in filtered if e.get("task_id") == task_id]
        
        if event_type is not None:
            filtered = [e for e in filtered if e.get("type") == event_type]
        
        # Sort by timestamp (newest first)
        filtered.sort(key=lambda e: e.get("timestamp", ""), reverse=True)
        
        # Apply limit
        return filtered[:limit]
    
    def clear_history(self) -> bool:
        """Clear all history entries"""
        self.history = []
        self.save_state()
        logger.info("Cleared automation history")
        return True
    
    def export_tasks(self, file_path: str) -> bool:
        """Export tasks to a JSON file"""
        try:
            with open(file_path, 'w') as f:
                json.dump({"tasks": self.tasks}, f, indent=2)
            logger.info(f"Exported {len(self.tasks)} tasks to {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error exporting tasks: {str(e)}")
            return False
    
    def import_tasks(self, file_path: str, overwrite: bool = False) -> Tuple[int, int]:
        """
        Import tasks from a JSON file
        
        Args:
            file_path: Path to JSON file
            overwrite: Whether to overwrite existing tasks
            
        Returns:
            tuple: (number of imported tasks, number of skipped tasks)
        """
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            if "tasks" not in data:
                logger.error("Invalid task import file format")
                return 0, 0
            
            import_tasks = data["tasks"]
            imported = 0
            skipped = 0
            
            for task_id, task_data in import_tasks.items():
                if task_id in self.tasks and not overwrite:
                    skipped += 1
                    continue
                
                self.tasks[task_id] = task_data
                imported += 1
            
            if imported > 0:
                self.save_state()
                self.tasks_updated.emit()
                
            logger.info(f"Imported {imported} tasks, skipped {skipped} tasks from {file_path}")
            return imported, skipped
            
        except Exception as e:
            logger.error(f"Error importing tasks: {str(e)}")
            return 0, 0
