#!/usr/bin/env python3
"""
File Manager for Pawprinting PyQt6 Application

Handles file operations with native macOS dialogs and error handling.

Author: AIMF LLC
Date: June 2, 2025
"""

import os
import sys
import shutil
import logging
import json
from typing import Optional, Tuple, List, Dict, Any
from datetime import datetime

from PyQt6.QtCore import QObject, pyqtSignal, QFileInfo
from PyQt6.QtWidgets import QFileDialog, QApplication, QMessageBox

# Import state manager
from utils.state_manager import StateManager
from utils.notification_manager import NotificationManager

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.file_manager")


class FileManager(QObject):
    """
    Handles file operations with native macOS dialogs
    """
    # Signal emitted when a file is selected
    file_selected = pyqtSignal(str)
    
    # Signal emitted when a directory is selected
    directory_selected = pyqtSignal(str)
    
    def __init__(self, parent=None):
        """Initialize file manager"""
        super().__init__(parent)
        self.state_manager = StateManager.get_instance()
        self.parent_widget = parent
    
    def select_file(self, title: str = "Select File", 
                   directory: str = "", 
                   filter_str: str = "All Files (*)",
                   save_mode: bool = False) -> str:
        """
        Show file selection dialog
        
        Args:
            title: Dialog title
            directory: Initial directory
            filter_str: File filter string
            save_mode: Whether to show save dialog instead of open dialog
            
        Returns:
            Selected file path or empty string if canceled
        """
        # Get parent widget
        parent = self.parent_widget
        if not parent and QApplication.instance():
            parent = QApplication.instance().main_window
        
        # Use last directory from state manager if not specified
        if not directory:
            directory = self.state_manager.get_value("last_session.last_directory")
            if not directory or not os.path.isdir(directory):
                directory = os.path.expanduser("~")
        
        try:
            if save_mode:
                file_path, _ = QFileDialog.getSaveFileName(
                    parent,
                    title,
                    directory,
                    filter_str
                )
            else:
                file_path, _ = QFileDialog.getOpenFileName(
                    parent,
                    title,
                    directory,
                    filter_str
                )
            
            if file_path:
                # Store directory in state manager
                self.state_manager.set_value("last_session.last_directory", 
                                          os.path.dirname(file_path))
                
                # Emit signal
                self.file_selected.emit(file_path)
                
                logger.info(f"Selected file: {file_path}")
                
                return file_path
            else:
                logger.debug("File selection canceled")
                return ""
                
        except Exception as e:
            logger.error(f"Error selecting file: {e}")
            NotificationManager.show_error(f"Error selecting file: {e}")
            return ""
    
    def select_directory(self, title: str = "Select Directory", 
                        directory: str = "") -> str:
        """
        Show directory selection dialog
        
        Args:
            title: Dialog title
            directory: Initial directory
            
        Returns:
            Selected directory path or empty string if canceled
        """
        # Get parent widget
        parent = self.parent_widget
        if not parent and QApplication.instance():
            parent = QApplication.instance().main_window
        
        # Use last directory from state manager if not specified
        if not directory:
            directory = self.state_manager.get_value("last_session.last_directory")
            if not directory or not os.path.isdir(directory):
                directory = os.path.expanduser("~")
        
        try:
            directory_path = QFileDialog.getExistingDirectory(
                parent,
                title,
                directory,
                QFileDialog.Option.ShowDirsOnly | QFileDialog.Option.DontResolveSymlinks
            )
            
            if directory_path:
                # Store in state manager
                self.state_manager.set_value("last_session.last_directory", directory_path)
                
                # Add to recent directories
                self.state_manager.add_recent_directory(directory_path)
                
                # Emit signal
                self.directory_selected.emit(directory_path)
                
                logger.info(f"Selected directory: {directory_path}")
                
                return directory_path
            else:
                logger.debug("Directory selection canceled")
                return ""
                
        except Exception as e:
            logger.error(f"Error selecting directory: {e}")
            NotificationManager.show_error(f"Error selecting directory: {e}")
            return ""
    
    def save_json(self, data: Dict[str, Any], file_path: str) -> bool:
        """
        Save data as JSON file
        
        Args:
            data: Data to save
            file_path: Output file path
            
        Returns:
            Success status
        """
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"Saved JSON data to {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving JSON data to {file_path}: {e}")
            NotificationManager.show_error(f"Error saving data: {e}")
            return False
    
    def load_json(self, file_path: str) -> Optional[Dict[str, Any]]:
        """
        Load data from JSON file
        
        Args:
            file_path: Input file path
            
        Returns:
            Loaded data or None if error
        """
        try:
            if not os.path.isfile(file_path):
                logger.warning(f"File not found: {file_path}")
                return None
            
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            logger.info(f"Loaded JSON data from {file_path}")
            return data
            
        except Exception as e:
            logger.error(f"Error loading JSON data from {file_path}: {e}")
            NotificationManager.show_error(f"Error loading data: {e}")
            return None
    
    def verify_file_exists(self, file_path: str) -> bool:
        """
        Verify that a file exists
        
        Args:
            file_path: File path to verify
            
        Returns:
            True if file exists, False otherwise
        """
        exists = os.path.isfile(file_path)
        if not exists:
            logger.warning(f"File not found: {file_path}")
            NotificationManager.show_warning(f"File not found: {os.path.basename(file_path)}")
        return exists
    
    def verify_directory_exists(self, directory_path: str) -> bool:
        """
        Verify that a directory exists
        
        Args:
            directory_path: Directory path to verify
            
        Returns:
            True if directory exists, False otherwise
        """
        exists = os.path.isdir(directory_path)
        if not exists:
            logger.warning(f"Directory not found: {directory_path}")
            NotificationManager.show_warning(f"Directory not found: {directory_path}")
        return exists
    
    def create_directory(self, directory_path: str) -> bool:
        """
        Create a directory if it doesn't exist
        
        Args:
            directory_path: Directory path to create
            
        Returns:
            True if directory exists or was created, False otherwise
        """
        try:
            os.makedirs(directory_path, exist_ok=True)
            logger.info(f"Created directory: {directory_path}")
            return True
        except Exception as e:
            logger.error(f"Error creating directory {directory_path}: {e}")
            NotificationManager.show_error(f"Error creating directory: {e}")
            return False
    
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """
        Get file information
        
        Args:
            file_path: File path
            
        Returns:
            Dictionary with file information
        """
        try:
            if not os.path.exists(file_path):
                return {
                    "exists": False,
                    "name": os.path.basename(file_path),
                    "path": file_path
                }
            
            info = QFileInfo(file_path)
            return {
                "exists": True,
                "name": info.fileName(),
                "path": info.absoluteFilePath(),
                "size": info.size(),
                "created": datetime.fromtimestamp(info.birthTime().toSecsSinceEpoch()).isoformat(),
                "modified": datetime.fromtimestamp(info.lastModified().toSecsSinceEpoch()).isoformat(),
                "is_dir": info.isDir(),
                "is_file": info.isFile(),
                "extension": info.suffix(),
                "readable": info.isReadable(),
                "writable": info.isWritable(),
                "executable": info.isExecutable()
            }
        except Exception as e:
            logger.error(f"Error getting file info for {file_path}: {e}")
            return {
                "exists": os.path.exists(file_path),
                "name": os.path.basename(file_path),
                "path": file_path,
                "error": str(e)
            }
