#!/usr/bin/env python3
"""
Pawprint Refresh Action for Pawprinting PyQt6 V2 Automation

Provides actions for refreshing pawprints for previously analyzed folders.

Author: AIMF LLC
Date: June 20, 2025
"""

import os
import sys
import logging
import json
from typing import Dict, List, Any, Optional, Set, Tuple, Callable
from datetime import datetime
from pathlib import Path

from PyQt6.QtCore import QObject, pyqtSignal

from utils.automation_action_base import Action
from utils.automation_pawprint_actions import PawprintAnalysisAction
from utils.automation_task_context import TaskContext

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.automation.pawprint_refresh")

class PawprintHistoryEntry:
    """Represents a previously analyzed folder"""
    
    def __init__(self, folder_path: str, last_analyzed: datetime, 
                 output_path: Optional[str] = None, metadata: Dict[str, Any] = None):
        """Initialize pawprint history entry"""
        self.folder_path = folder_path
        self.last_analyzed = last_analyzed
        self.output_path = output_path
        self.metadata = metadata or {}
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "folder_path": self.folder_path,
            "last_analyzed": self.last_analyzed.isoformat() if self.last_analyzed else None,
            "output_path": self.output_path,
            "metadata": self.metadata
        }
        
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'PawprintHistoryEntry':
        """Create from dictionary"""
        last_analyzed = datetime.fromisoformat(data["last_analyzed"]) if data.get("last_analyzed") else None
        
        return PawprintHistoryEntry(
            folder_path=data["folder_path"],
            last_analyzed=last_analyzed,
            output_path=data.get("output_path"),
            metadata=data.get("metadata", {})
        )

class PawprintHistoryManager:
    """Manages history of analyzed folders for pawprinting"""
    
    def __init__(self, history_file_path: Optional[str] = None):
        """Initialize history manager"""
        self._history: List[PawprintHistoryEntry] = []
        
        if history_file_path:
            self._history_file = history_file_path
        else:
            # Default to user's home directory
            self._history_file = os.path.join(
                os.path.expanduser("~"),
                "Pawprinting_PyQt6_V2",
                "automation",
                "pawprint_history.json"
            )
            
        # Ensure directory exists
        os.makedirs(os.path.dirname(self._history_file), exist_ok=True)
        
        # Load history if file exists
        self.load()
        
    def add_entry(self, entry: PawprintHistoryEntry) -> None:
        """Add a new entry to history"""
        # Check if entry already exists
        for i, existing in enumerate(self._history):
            if existing.folder_path == entry.folder_path:
                # Update existing entry
                self._history[i] = entry
                logger.info(f"Updated history entry for {entry.folder_path}")
                self.save()
                return
                
        # Add new entry
        self._history.append(entry)
        logger.info(f"Added new history entry for {entry.folder_path}")
        self.save()
        
    def get_entries(self, max_entries: int = 0) -> List[PawprintHistoryEntry]:
        """Get history entries, sorted by most recent first"""
        sorted_entries = sorted(
            self._history,
            key=lambda e: e.last_analyzed if e.last_analyzed else datetime.min,
            reverse=True  # Most recent first
        )
        
        if max_entries > 0:
            return sorted_entries[:max_entries]
        return sorted_entries
        
    def get_entry_by_path(self, folder_path: str) -> Optional[PawprintHistoryEntry]:
        """Get entry by folder path"""
        for entry in self._history:
            if entry.folder_path == folder_path:
                return entry
        return None
        
    def remove_entry(self, folder_path: str) -> bool:
        """Remove entry by folder path"""
        for i, entry in enumerate(self._history):
            if entry.folder_path == folder_path:
                del self._history[i]
                logger.info(f"Removed history entry for {folder_path}")
                self.save()
                return True
        return False
        
    def clear(self) -> None:
        """Clear all history"""
        self._history.clear()
        logger.info("Cleared pawprint history")
        self.save()
        
    def save(self) -> bool:
        """Save history to file"""
        try:
            data = {
                "history": [entry.to_dict() for entry in self._history]
            }
            
            with open(self._history_file, 'w') as f:
                json.dump(data, f, indent=2)
                
            logger.info(f"Saved pawprint history to {self._history_file}")
            return True
        except Exception as e:
            logger.exception(f"Error saving pawprint history: {str(e)}")
            return False
            
    def load(self) -> bool:
        """Load history from file"""
        if not os.path.exists(self._history_file):
            logger.info(f"Pawprint history file {self._history_file} does not exist")
            return False
            
        try:
            with open(self._history_file, 'r') as f:
                data = json.load(f)
                
            self._history.clear()
            
            for entry_data in data.get("history", []):
                try:
                    entry = PawprintHistoryEntry.from_dict(entry_data)
                    self._history.append(entry)
                except Exception as e:
                    logger.error(f"Error loading history entry: {str(e)}")
                    
            logger.info(f"Loaded {len(self._history)} entries from pawprint history")
            return True
        except Exception as e:
            logger.exception(f"Error loading pawprint history: {str(e)}")
            return False

# Singleton instance
_history_instance = None

def get_pawprint_history_manager() -> PawprintHistoryManager:
    """Get the singleton history manager instance"""
    global _history_instance
    if _history_instance is None:
        _history_instance = PawprintHistoryManager()
    return _history_instance

class PawprintRefreshAction(Action):
    """Action to refresh pawprints for previously analyzed folders"""
    
    def __init__(self, action_id: str, config: Dict[str, Any] = None):
        """Initialize pawprint refresh action"""
        super().__init__(action_id, config)
        self._history_manager = get_pawprint_history_manager()
        self._subactions = []
        
    def validate(self) -> bool:
        """Validate action configuration"""
        # Refresh options
        # - all: Refresh all known folders
        # - recent: Refresh most recent N folders
        # - specific: Refresh specific folders
        
        refresh_type = self.config.get("refresh_type", "recent")
        
        if refresh_type == "recent":
            # Check if count is specified and valid
            count = self.config.get("count", 5)
            if not isinstance(count, int) or count <= 0:
                self._add_error("Invalid count for recent folders")
                return False
                
        elif refresh_type == "specific":
            # Check if folders are specified
            folders = self.config.get("folders", [])
            if not folders:
                self._add_error("No folders specified for specific refresh")
                return False
                
        elif refresh_type != "all":
            self._add_error(f"Invalid refresh type: {refresh_type}")
            return False
            
        return True
        
    def execute(self, context: TaskContext) -> bool:
        """Execute the action"""
        self._log_info(f"Starting pawprint refresh action")
        
        # Determine folders to refresh
        folders_to_refresh = self._get_folders_to_refresh()
        
        if not folders_to_refresh:
            self._log_warning("No folders to refresh found")
            return True  # Not an error, just nothing to do
            
        total_folders = len(folders_to_refresh)
        self._log_info(f"Found {total_folders} folders to refresh")
        
        # Create sub-actions for each folder
        self._subactions = []
        for i, folder in enumerate(folders_to_refresh):
            # Create pawprint analysis action
            action_id = f"{self.action_id}_sub_{i}"
            
            # Create configuration for the analysis action
            analysis_config = {
                "input_folder": folder,
                "output_folder": self.config.get("output_folder", None),  # Use default if not specified
                "options": self.config.get("analysis_options", {}),  # Pass any analysis options
                "overwrite": self.config.get("overwrite", True)  # Default to overwrite
            }
            
            # Create the action
            analysis_action = PawprintAnalysisAction(action_id, analysis_config)
            self._subactions.append(analysis_action)
            
        # Execute each sub-action
        successful = 0
        for i, action in enumerate(self._subactions):
            folder_path = folders_to_refresh[i]
            self._log_info(f"Processing folder {i+1}/{total_folders}: {folder_path}")
            
            # Update progress
            self.progress = int((i / total_folders) * 100)
            self._emit_progress()
            
            # Create a sub-context for this action
            sub_context = context.create_sub_context(f"subfolder_{i}")
            
            # Execute the action
            if action.execute(sub_context):
                successful += 1
                self._log_info(f"Successfully refreshed pawprint for: {folder_path}")
                
                # Update history
                entry = PawprintHistoryEntry(
                    folder_path=folder_path,
                    last_analyzed=datetime.now(),
                    output_path=action.get_output_path(),
                    metadata={
                        "action_id": self.action_id,
                        "refresh_type": self.config.get("refresh_type"),
                        "success": True
                    }
                )
                self._history_manager.add_entry(entry)
            else:
                self._log_error(f"Failed to refresh pawprint for: {folder_path}")
                # Still update history with failure
                entry = PawprintHistoryEntry(
                    folder_path=folder_path,
                    last_analyzed=datetime.now(),
                    metadata={
                        "action_id": self.action_id,
                        "refresh_type": self.config.get("refresh_type"),
                        "success": False,
                        "errors": action.get_errors()
                    }
                )
                self._history_manager.add_entry(entry)
                
        # Final progress update
        self.progress = 100
        self._emit_progress()
        
        success_rate = (successful / total_folders) * 100 if total_folders > 0 else 0
        self._log_info(f"Pawprint refresh completed. Success: {successful}/{total_folders} ({success_rate:.1f}%)")
        
        return successful > 0 or total_folders == 0
        
    def cancel(self) -> None:
        """Cancel the action"""
        super().cancel()
        
        # Cancel any running sub-actions
        for action in self._subactions:
            if action.is_running():
                action.cancel()
                
    def _get_folders_to_refresh(self) -> List[str]:
        """Get list of folders to refresh based on configuration"""
        refresh_type = self.config.get("refresh_type", "recent")
        
        if refresh_type == "all":
            # Get all known folders
            entries = self._history_manager.get_entries()
            return [entry.folder_path for entry in entries if os.path.exists(entry.folder_path)]
            
        elif refresh_type == "recent":
            # Get most recent N folders
            count = self.config.get("count", 5)
            entries = self._history_manager.get_entries(max_entries=count)
            return [entry.folder_path for entry in entries if os.path.exists(entry.folder_path)]
            
        elif refresh_type == "specific":
            # Get specific folders
            folders = self.config.get("folders", [])
            return [folder for folder in folders if os.path.exists(folder)]
            
        return []

class PawprintBatchRefreshAction(Action):
    """Action to batch refresh multiple pawprint folders"""
    
    def __init__(self, action_id: str, config: Dict[str, Any] = None):
        """Initialize batch refresh action"""
        super().__init__(action_id, config)
        self._refresh_action = None
        
    def validate(self) -> bool:
        """Validate action configuration"""
        # Create and validate the refresh action
        refresh_config = self.config.copy()
        refresh_config["action_id"] = f"{self.action_id}_refresh"
        
        self._refresh_action = PawprintRefreshAction(refresh_config["action_id"], refresh_config)
        return self._refresh_action.validate()
        
    def execute(self, context: TaskContext) -> bool:
        """Execute the action"""
        self._log_info("Starting pawprint batch refresh")
        
        if not self._refresh_action:
            self._refresh_action = PawprintRefreshAction(f"{self.action_id}_refresh", self.config)
            
        # Connect to progress signal
        self._refresh_action.progress_changed.connect(self._on_refresh_progress)
        
        # Execute the refresh action
        success = self._refresh_action.execute(context)
        
        if success:
            self._log_info("Batch refresh completed successfully")
        else:
            self._log_error("Batch refresh failed")
            
        return success
        
    def _on_refresh_progress(self, progress: int) -> None:
        """Handle progress updates from refresh action"""
        self.progress = progress
        self._emit_progress()
        
    def cancel(self) -> None:
        """Cancel the action"""
        super().cancel()
        
        if self._refresh_action and self._refresh_action.is_running():
            self._refresh_action.cancel()
