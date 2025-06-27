#!/usr/bin/env python3
"""
File Operation Actions for Pawprinting PyQt6 V2 Automation

Provides basic file operation actions (copy, move, delete, etc.) that can be used
in automation tasks.

Author: AIMF LLC
Date: June 20, 2025
"""

import os
import sys
import shutil
import logging
from enum import Enum
from typing import Dict, List, Any, Optional, Callable, Set, Tuple
from datetime import datetime
from pathlib import Path
import json

from utils.automation_action_base import Action, ActionResult, ActionContext

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.automation.file_operations")

class FileCopyAction(Action):
    """Action to copy a file or directory"""
    
    def __init__(self, action_id: str, config: Dict[str, Any] = None):
        """Initialize file copy action"""
        super().__init__(action_id, config or {})
        self.display_name = self.config.get("display_name", "Copy File")
        self.description = self.config.get("description", "Copies a file or directory")
    
    def validate_config(self) -> Tuple[bool, str]:
        """Validate configuration"""
        if "source" not in self.config:
            return False, "Source path is required"
        if "destination" not in self.config:
            return False, "Destination path is required"
        return True, ""
    
    def execute(self, context: ActionContext) -> ActionResult:
        """Execute the file copy action"""
        # Get source and destination
        source = self.config.get("source")
        destination = self.config.get("destination")
        overwrite = self.config.get("overwrite", False)
        preserve_metadata = self.config.get("preserve_metadata", True)
        
        # Check if source exists
        if not os.path.exists(source):
            return ActionResult.failure(f"Source does not exist: {source}")
        
        # Check if destination exists and we're not overwriting
        if os.path.exists(destination) and not overwrite:
            return ActionResult.failure(f"Destination already exists: {destination}")
        
        try:
            context.logger.info(f"Copying {source} to {destination}")
            
            # Create parent directories if needed
            os.makedirs(os.path.dirname(destination), exist_ok=True)
            
            # Copy file or directory
            if os.path.isdir(source):
                if os.path.exists(destination) and overwrite:
                    shutil.rmtree(destination)
                shutil.copytree(source, destination)
                context.logger.info(f"Copied directory {source} to {destination}")
                return ActionResult.success(
                    f"Directory copied successfully",
                    {"source": source, "destination": destination, "is_directory": True}
                )
            else:
                if preserve_metadata:
                    shutil.copy2(source, destination)
                else:
                    shutil.copy(source, destination)
                context.logger.info(f"Copied file {source} to {destination}")
                return ActionResult.success(
                    f"File copied successfully",
                    {"source": source, "destination": destination, "is_directory": False}
                )
                
        except Exception as e:
            context.logger.exception(f"Error copying {source} to {destination}: {str(e)}")
            return ActionResult.from_exception(e, f"Failed to copy {source} to {destination}")

class FileMoveAction(Action):
    """Action to move a file or directory"""
    
    def __init__(self, action_id: str, config: Dict[str, Any] = None):
        """Initialize file move action"""
        super().__init__(action_id, config or {})
        self.display_name = self.config.get("display_name", "Move File")
        self.description = self.config.get("description", "Moves a file or directory")
    
    def validate_config(self) -> Tuple[bool, str]:
        """Validate configuration"""
        if "source" not in self.config:
            return False, "Source path is required"
        if "destination" not in self.config:
            return False, "Destination path is required"
        return True, ""
    
    def execute(self, context: ActionContext) -> ActionResult:
        """Execute the file move action"""
        # Get source and destination
        source = self.config.get("source")
        destination = self.config.get("destination")
        overwrite = self.config.get("overwrite", False)
        
        # Check if source exists
        if not os.path.exists(source):
            return ActionResult.failure(f"Source does not exist: {source}")
        
        # Check if destination exists and we're not overwriting
        if os.path.exists(destination) and not overwrite:
            return ActionResult.failure(f"Destination already exists: {destination}")
        
        try:
            context.logger.info(f"Moving {source} to {destination}")
            
            # Create parent directories if needed
            os.makedirs(os.path.dirname(destination), exist_ok=True)
            
            # Move file or directory
            if os.path.exists(destination) and overwrite:
                if os.path.isdir(destination):
                    shutil.rmtree(destination)
                else:
                    os.remove(destination)
                    
            shutil.move(source, destination)
            context.logger.info(f"Moved {source} to {destination}")
            
            return ActionResult.success(
                f"File/directory moved successfully",
                {"source": source, "destination": destination}
            )
                
        except Exception as e:
            context.logger.exception(f"Error moving {source} to {destination}: {str(e)}")
            return ActionResult.from_exception(e, f"Failed to move {source} to {destination}")

class FileDeleteAction(Action):
    """Action to delete a file or directory"""
    
    def __init__(self, action_id: str, config: Dict[str, Any] = None):
        """Initialize file delete action"""
        super().__init__(action_id, config or {})
        self.display_name = self.config.get("display_name", "Delete File")
        self.description = self.config.get("description", "Deletes a file or directory")
    
    def validate_config(self) -> Tuple[bool, str]:
        """Validate configuration"""
        if "path" not in self.config:
            return False, "Path is required"
        return True, ""
    
    def execute(self, context: ActionContext) -> ActionResult:
        """Execute the file delete action"""
        # Get path
        path = self.config.get("path")
        
        # Check if path exists
        if not os.path.exists(path):
            return ActionResult.failure(f"Path does not exist: {path}")
        
        try:
            context.logger.info(f"Deleting {path}")
            
            # Delete file or directory
            if os.path.isdir(path):
                shutil.rmtree(path)
                context.logger.info(f"Deleted directory {path}")
                return ActionResult.success(
                    f"Directory deleted successfully",
                    {"path": path, "is_directory": True}
                )
            else:
                os.remove(path)
                context.logger.info(f"Deleted file {path}")
                return ActionResult.success(
                    f"File deleted successfully",
                    {"path": path, "is_directory": False}
                )
                
        except Exception as e:
            context.logger.exception(f"Error deleting {path}: {str(e)}")
            return ActionResult.from_exception(e, f"Failed to delete {path}")

class FileMakeDirectoryAction(Action):
    """Action to create a directory"""
    
    def __init__(self, action_id: str, config: Dict[str, Any] = None):
        """Initialize directory creation action"""
        super().__init__(action_id, config or {})
        self.display_name = self.config.get("display_name", "Create Directory")
        self.description = self.config.get("description", "Creates a directory")
    
    def validate_config(self) -> Tuple[bool, str]:
        """Validate configuration"""
        if "path" not in self.config:
            return False, "Path is required"
        return True, ""
    
    def execute(self, context: ActionContext) -> ActionResult:
        """Execute the directory creation action"""
        # Get path
        path = self.config.get("path")
        parents = self.config.get("create_parents", True)
        
        try:
            context.logger.info(f"Creating directory {path}")
            
            # Create directory
            os.makedirs(path, exist_ok=True) if parents else os.mkdir(path)
            context.logger.info(f"Created directory {path}")
            
            return ActionResult.success(
                f"Directory created successfully",
                {"path": path}
            )
                
        except Exception as e:
            context.logger.exception(f"Error creating directory {path}: {str(e)}")
            return ActionResult.from_exception(e, f"Failed to create directory {path}")

class FileArchiveAction(Action):
    """Action to archive a file or directory"""
    
    def __init__(self, action_id: str, config: Dict[str, Any] = None):
        """Initialize file archive action"""
        super().__init__(action_id, config or {})
        self.display_name = self.config.get("display_name", "Archive Files")
        self.description = self.config.get("description", "Creates an archive from files/directories")
    
    def validate_config(self) -> Tuple[bool, str]:
        """Validate configuration"""
        if "source" not in self.config:
            return False, "Source path(s) are required"
        if "destination" not in self.config:
            return False, "Destination archive path is required"
        return True, ""
    
    def execute(self, context: ActionContext) -> ActionResult:
        """Execute the file archive action"""
        import tarfile
        import zipfile
        
        # Get source and destination
        source = self.config.get("source")  # Can be a path or list of paths
        destination = self.config.get("destination")
        format = self.config.get("format", "zip").lower()  # zip, tar, targz
        
        # Convert single path to list
        if isinstance(source, str):
            source = [source]
        
        # Check if all sources exist
        missing = [s for s in source if not os.path.exists(s)]
        if missing:
            return ActionResult.failure(f"Some source paths don't exist: {', '.join(missing)}")
        
        try:
            context.logger.info(f"Creating {format} archive {destination} from {len(source)} sources")
            
            # Create parent directories if needed
            os.makedirs(os.path.dirname(destination), exist_ok=True)
            
            # Create archive based on format
            if format == "zip":
                with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for path in source:
                        if os.path.isdir(path):
                            # Add all files in directory
                            for root, _, files in os.walk(path):
                                for file in files:
                                    file_path = os.path.join(root, file)
                                    arcname = os.path.relpath(file_path, os.path.dirname(path))
                                    zipf.write(file_path, arcname)
                        else:
                            # Add single file
                            arcname = os.path.basename(path)
                            zipf.write(path, arcname)
                            
            elif format in ("tar", "targz"):
                mode = "w:gz" if format == "targz" else "w"
                with tarfile.open(destination, mode) as tarf:
                    for path in source:
                        arcname = os.path.basename(path)
                        tarf.add(path, arcname=arcname)
            else:
                return ActionResult.failure(f"Unsupported archive format: {format}")
            
            context.logger.info(f"Created archive {destination}")
            
            return ActionResult.success(
                f"Archive created successfully",
                {"source": source, "destination": destination, "format": format}
            )
                
        except Exception as e:
            context.logger.exception(f"Error creating archive {destination}: {str(e)}")
            return ActionResult.from_exception(e, f"Failed to create archive {destination}")
