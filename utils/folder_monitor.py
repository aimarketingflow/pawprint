#!/usr/bin/env python3
"""
Folder Monitor for Pawprinting PyQt6 V2 Automation

Monitors folders for changes (new files, modified files, deleted files)
and triggers automation tasks based on these changes.

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
from typing import Dict, List, Any, Optional, Callable, Set
from datetime import datetime
from pathlib import Path
import hashlib

from PyQt6.QtCore import QObject, pyqtSignal

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.automation.folder_monitor")

class FileChangeType(Enum):
    """Type of file change detected by folder monitor"""
    CREATED = "created"
    MODIFIED = "modified"
    DELETED = "deleted"
    RENAMED = "renamed"
    ATTRIBUTE_CHANGED = "attribute_changed"

class FileInfo:
    """Information about a file for change detection"""
    
    def __init__(self, path: str):
        """Initialize file info from path"""
        self.path = path
        self.update()
    
    def update(self):
        """Update file information from the filesystem"""
        try:
            stat = os.stat(self.path)
            self.exists = True
            self.size = stat.st_size
            self.mtime = stat.st_mtime
            self.ctime = stat.st_ctime
            
            # Calculate hash for small files (optional, can be expensive)
            if self.size < 1024 * 1024 * 10:  # 10 MB limit for hashing
                with open(self.path, 'rb') as f:
                    self.md5 = hashlib.md5(f.read()).hexdigest()
            else:
                self.md5 = None
                
        except FileNotFoundError:
            self.exists = False
            self.size = 0
            self.mtime = 0
            self.ctime = 0
            self.md5 = None
    
    def has_changed(self, other: 'FileInfo') -> bool:
        """Check if file has changed compared to another FileInfo"""
        if self.exists != other.exists:
            return True
        
        if not self.exists:
            return False
            
        if self.size != other.size or self.mtime != other.mtime:
            return True
            
        # If both have MD5 hashes, compare them
        if self.md5 is not None and other.md5 is not None:
            return self.md5 != other.md5
            
        return False

class FolderMonitor(QObject):
    """
    Monitors a folder for file changes and emits signals when changes are detected
    """
    
    # Signals
    file_created = pyqtSignal(str)  # file_path
    file_modified = pyqtSignal(str)  # file_path
    file_deleted = pyqtSignal(str)  # file_path
    file_renamed = pyqtSignal(str, str)  # old_path, new_path
    
    def __init__(self, folder_path: str, parent=None):
        """Initialize folder monitor"""
        super().__init__(parent)
        self.folder_path = os.path.abspath(folder_path)
        
        # Check if folder exists
        if not os.path.isdir(self.folder_path):
            raise ValueError(f"Folder does not exist: {self.folder_path}")
        
        # File tracking
        self.files = {}  # path -> FileInfo
        self.running = False
        self.monitor_thread = None
        self.file_patterns = []  # Patterns to include (empty = all files)
        self.exclude_patterns = []  # Patterns to exclude
        self.check_interval = 2.0  # Seconds between checks
        self.recursive = True  # Monitor subdirectories
        
        logger.debug(f"Folder monitor initialized for {self.folder_path}")
    
    def set_check_interval(self, seconds: float):
        """Set the interval between checks"""
        self.check_interval = max(0.5, float(seconds))
    
    def set_recursive(self, recursive: bool):
        """Set whether to monitor subdirectories"""
        self.recursive = recursive
    
    def set_file_patterns(self, patterns: List[str]):
        """Set patterns for files to monitor (glob format)"""
        self.file_patterns = patterns
    
    def set_exclude_patterns(self, patterns: List[str]):
        """Set patterns for files to exclude (glob format)"""
        self.exclude_patterns = patterns
    
    def _should_monitor_file(self, path: str) -> bool:
        """Check if a file should be monitored based on patterns"""
        from fnmatch import fnmatch
        
        # Convert absolute path to relative path for pattern matching
        rel_path = os.path.relpath(path, self.folder_path)
        
        # Check exclusion patterns first
        for pattern in self.exclude_patterns:
            if fnmatch(rel_path, pattern) or fnmatch(os.path.basename(path), pattern):
                return False
        
        # If no include patterns, include all non-excluded files
        if not self.file_patterns:
            return True
        
        # Check include patterns
        for pattern in self.file_patterns:
            if fnmatch(rel_path, pattern) or fnmatch(os.path.basename(path), pattern):
                return True
        
        return False
    
    def start(self):
        """Start monitoring the folder"""
        if self.running:
            logger.warning("Folder monitor already running")
            return
        
        self.running = True
        
        # Scan for initial file state
        self._scan_folder()
        
        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self._monitor_thread_func, daemon=True)
        self.monitor_thread.start()
        
        logger.info(f"Started monitoring folder: {self.folder_path}")
    
    def stop(self):
        """Stop monitoring the folder"""
        if not self.running:
            logger.warning("Folder monitor not running")
            return
        
        self.running = False
        
        # Wait for monitoring thread to stop
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=2.0)
        
        self.monitor_thread = None
        logger.info(f"Stopped monitoring folder: {self.folder_path}")
    
    def _scan_folder(self):
        """Scan the folder and build initial file state"""
        try:
            new_files = {}
            
            # Walk through the directory tree
            for root, dirs, files in os.walk(self.folder_path):
                # Skip if not recursive and not the top folder
                if not self.recursive and root != self.folder_path:
                    continue
                
                # Process files in this directory
                for filename in files:
                    file_path = os.path.join(root, filename)
                    
                    # Check if this file should be monitored
                    if self._should_monitor_file(file_path):
                        new_files[file_path] = FileInfo(file_path)
            
            # Update file list
            self.files = new_files
            logger.debug(f"Initial scan found {len(self.files)} files to monitor")
            
        except Exception as e:
            logger.error(f"Error scanning folder {self.folder_path}: {str(e)}")
    
    def _monitor_thread_func(self):
        """Thread function to monitor the folder"""
        while self.running:
            try:
                # Sleep first to avoid tight loop
                time.sleep(self.check_interval)
                
                # Check for changes
                self._check_for_changes()
                
            except Exception as e:
                logger.error(f"Error in folder monitor: {str(e)}")
                # If an error occurred, slow down a bit
                time.sleep(1.0)
    
    def _check_for_changes(self):
        """Check for changes in the monitored folder"""
        try:
            # Get current file set
            current_files = {}
            for root, dirs, files in os.walk(self.folder_path):
                # Skip if not recursive and not the top folder
                if not self.recursive and root != self.folder_path:
                    continue
                
                # Process files in this directory
                for filename in files:
                    file_path = os.path.join(root, filename)
                    
                    # Check if this file should be monitored
                    if self._should_monitor_file(file_path):
                        current_files[file_path] = FileInfo(file_path)
            
            # Find new, modified and deleted files
            current_paths = set(current_files.keys())
            previous_paths = set(self.files.keys())
            
            # New files
            for path in current_paths - previous_paths:
                logger.debug(f"New file detected: {path}")
                self.file_created.emit(path)
            
            # Modified files
            for path in current_paths & previous_paths:
                if current_files[path].has_changed(self.files[path]):
                    logger.debug(f"File modified: {path}")
                    self.file_modified.emit(path)
            
            # Deleted files
            for path in previous_paths - current_paths:
                logger.debug(f"File deleted: {path}")
                self.file_deleted.emit(path)
            
            # TODO: Implement renamed file detection (more complex)
            
            # Update file list
            self.files = current_files
            
        except Exception as e:
            logger.error(f"Error checking for changes in {self.folder_path}: {str(e)}")

class FolderMonitorManager(QObject):
    """
    Manages multiple folder monitors for the automation system
    """
    
    # Signals - include all signals from FolderMonitor plus folder info
    file_created = pyqtSignal(str, str)  # folder_id, file_path
    file_modified = pyqtSignal(str, str)  # folder_id, file_path
    file_deleted = pyqtSignal(str, str)  # folder_id, file_path
    file_renamed = pyqtSignal(str, str, str)  # folder_id, old_path, new_path
    
    _instance = None
    
    @classmethod
    def get_instance(cls) -> 'FolderMonitorManager':
        """Get the singleton instance"""
        if cls._instance is None:
            cls._instance = FolderMonitorManager()
        return cls._instance
    
    def __init__(self):
        """Initialize folder monitor manager"""
        super().__init__()
        self.monitors = {}  # folder_id -> FolderMonitor
        logger.info("Folder monitor manager initialized")
    
    def add_monitor(self, folder_id: str, folder_path: str, config: Dict[str, Any] = None) -> bool:
        """
        Add a new folder monitor
        
        Args:
            folder_id: Unique ID for this monitor
            folder_path: Path to the folder to monitor
            config: Optional configuration dictionary
                - check_interval: Seconds between checks (default: 2.0)
                - recursive: Monitor subdirectories (default: True)
                - file_patterns: List of patterns to include (default: [])
                - exclude_patterns: List of patterns to exclude (default: [])
        
        Returns:
            success: True if monitor was added successfully
        """
        try:
            # Check if folder ID already exists
            if folder_id in self.monitors:
                logger.warning(f"Folder monitor with ID {folder_id} already exists")
                return False
            
            # Create monitor
            monitor = FolderMonitor(folder_path)
            
            # Apply configuration
            if config:
                if "check_interval" in config:
                    monitor.set_check_interval(config["check_interval"])
                if "recursive" in config:
                    monitor.set_recursive(config["recursive"])
                if "file_patterns" in config:
                    monitor.set_file_patterns(config["file_patterns"])
                if "exclude_patterns" in config:
                    monitor.set_exclude_patterns(config["exclude_patterns"])
            
            # Connect signals
            monitor.file_created.connect(lambda path: self.file_created.emit(folder_id, path))
            monitor.file_modified.connect(lambda path: self.file_modified.emit(folder_id, path))
            monitor.file_deleted.connect(lambda path: self.file_deleted.emit(folder_id, path))
            monitor.file_renamed.connect(lambda old, new: self.file_renamed.emit(folder_id, old, new))
            
            # Add to monitors dictionary
            self.monitors[folder_id] = monitor
            
            logger.info(f"Added folder monitor {folder_id} for {folder_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding folder monitor for {folder_path}: {str(e)}")
            return False
    
    def remove_monitor(self, folder_id: str) -> bool:
        """
        Remove a folder monitor
        
        Args:
            folder_id: ID of the monitor to remove
        
        Returns:
            success: True if monitor was removed
        """
        if folder_id not in self.monitors:
            logger.warning(f"Folder monitor {folder_id} does not exist")
            return False
        
        # Stop the monitor
        self.stop_monitor(folder_id)
        
        # Remove from monitors
        monitor = self.monitors.pop(folder_id)
        
        # Clean up signals
        try:
            monitor.file_created.disconnect()
            monitor.file_modified.disconnect()
            monitor.file_deleted.disconnect()
            monitor.file_renamed.disconnect()
        except Exception:
            pass
        
        logger.info(f"Removed folder monitor {folder_id}")
        return True
    
    def start_monitor(self, folder_id: str) -> bool:
        """
        Start a folder monitor
        
        Args:
            folder_id: ID of the monitor to start
        
        Returns:
            success: True if monitor was started
        """
        if folder_id not in self.monitors:
            logger.warning(f"Folder monitor {folder_id} does not exist")
            return False
        
        # Start the monitor
        self.monitors[folder_id].start()
        logger.info(f"Started folder monitor {folder_id}")
        return True
    
    def stop_monitor(self, folder_id: str) -> bool:
        """
        Stop a folder monitor
        
        Args:
            folder_id: ID of the monitor to stop
        
        Returns:
            success: True if monitor was stopped
        """
        if folder_id not in self.monitors:
            logger.warning(f"Folder monitor {folder_id} does not exist")
            return False
        
        # Stop the monitor
        self.monitors[folder_id].stop()
        logger.info(f"Stopped folder monitor {folder_id}")
        return True
    
    def stop_all_monitors(self):
        """Stop all folder monitors"""
        for folder_id in list(self.monitors.keys()):
            self.stop_monitor(folder_id)
        logger.info("Stopped all folder monitors")
