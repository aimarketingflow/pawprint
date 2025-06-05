#!/usr/bin/env python3
"""
State Manager for Pawprinting PyQt6 Application

Manages application state, including recent files, settings, and other
persistent data.

Author: AIMF LLC
Date: June 2, 2025
"""

import os
import sys
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from PyQt6.QtCore import QObject, pyqtSignal, QSettings

# Import configuration paths
script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from config_paths import CONFIG_DIR

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.state_manager")


class StateManager(QObject):
    """
    Manages application state, including recent files and settings
    """
    # Signal emitted when state changes
    state_changed = pyqtSignal(dict)  # Full state dictionary
    
    # Singleton instance
    _instance = None
    
    @classmethod
    def get_instance(cls) -> 'StateManager':
        """Get or create the singleton instance"""
        if cls._instance is None:
            cls._instance = StateManager()
        return cls._instance
    
    def __init__(self):
        """Initialize state manager"""
        super().__init__()
        
        if StateManager._instance is not None:
            raise RuntimeError("StateManager is a singleton. Use get_instance() instead")
        
        # Initialize QSettings
        self._settings = QSettings("AIMF LLC", "Pawprinting PyQt6")
        
        # Initialize state
        self._state = {
            "recent_files": [],
            "recent_directories": [],
            "last_session": {
                "last_open_file": None,
                "last_directory": None,
                "last_export_directory": None,
                "last_screen": "dashboard"
            },
            "settings": {
                "theme": "auto",
                "max_recent_files": 10,
                "auto_save": True,
                "auto_load_last_file": False,
                "console_log_level": "INFO",
                "file_log_level": "DEBUG",
                "show_tooltips": True,
                "confirm_on_exit": True
            },
            "analysis": {
                "default_parameters": {}
            },
            "fractal": {
                "default_parameters": {}
            }
        }
        
        # Load state from settings
        self._load_state()
        
        logger.info("State manager initialized")
    
    def _load_state(self) -> None:
        """Load state from QSettings"""
        # Load from QSettings first (faster, but less detail)
        if self._settings.contains("recent_files"):
            self._state["recent_files"] = self._settings.value("recent_files", [])
        
        if self._settings.contains("recent_directories"):
            self._state["recent_directories"] = self._settings.value("recent_directories", [])
        
        if self._settings.contains("last_open_file"):
            self._state["last_session"]["last_open_file"] = self._settings.value("last_open_file", None)
        
        if self._settings.contains("last_directory"):
            self._state["last_session"]["last_directory"] = self._settings.value("last_directory", None)
        
        if self._settings.contains("last_export_directory"):
            self._state["last_session"]["last_export_directory"] = self._settings.value("last_export_directory", None)
        
        if self._settings.contains("last_screen"):
            self._state["last_session"]["last_screen"] = self._settings.value("last_screen", "dashboard")
        
        # Check if settings file exists for full state
        settings_file = os.path.join(CONFIG_DIR, "app_state.json")
        if os.path.exists(settings_file):
            try:
                with open(settings_file, "r") as f:
                    state_data = json.load(f)
                    # Update state with loaded data
                    for key, value in state_data.items():
                        if key in self._state:
                            if isinstance(value, dict) and isinstance(self._state[key], dict):
                                # Merge dictionaries
                                self._state[key].update(value)
                            else:
                                # Replace value
                                self._state[key] = value
                logger.info(f"Loaded application state from {settings_file}")
            except Exception as e:
                logger.error(f"Error loading state from {settings_file}: {e}")
    
    def _save_state(self) -> None:
        """Save state to QSettings and JSON file"""
        # Save critical items to QSettings for quick access
        self._settings.setValue("recent_files", self._state["recent_files"])
        self._settings.setValue("recent_directories", self._state["recent_directories"])
        self._settings.setValue("last_open_file", self._state["last_session"]["last_open_file"])
        self._settings.setValue("last_directory", self._state["last_session"]["last_directory"])
        self._settings.setValue("last_export_directory", self._state["last_session"]["last_export_directory"])
        self._settings.setValue("last_screen", self._state["last_session"]["last_screen"])
        
        # Save full state to JSON file
        settings_file = os.path.join(CONFIG_DIR, "app_state.json")
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(settings_file), exist_ok=True)
            
            with open(settings_file, "w") as f:
                json.dump(self._state, f, indent=2)
            logger.debug(f"Saved application state to {settings_file}")
        except Exception as e:
            logger.error(f"Error saving state to {settings_file}: {e}")
    
    def get_state(self) -> Dict[str, Any]:
        """Get the full application state"""
        return self._state
    
    def get_value(self, key_path: str, default: Any = None) -> Any:
        """
        Get a value from the state by key path
        
        Args:
            key_path: Dot-separated path to the value (e.g., "settings.theme")
            default: Default value to return if key not found
            
        Returns:
            Value from state or default if not found
        """
        keys = key_path.split(".")
        value = self._state
        
        try:
            for key in keys:
                if isinstance(value, dict) and key in value:
                    value = value[key]
                else:
                    return default
            return value
        except Exception:
            return default
    
    def set_value(self, key_path: str, value: Any) -> None:
        """
        Set a value in the state by key path
        
        Args:
            key_path: Dot-separated path to the value (e.g., "settings.theme")
            value: Value to set
        """
        keys = key_path.split(".")
        if not keys:
            return
        
        # Navigate to the right part of the state
        target = self._state
        for key in keys[:-1]:
            if key not in target:
                target[key] = {}
            target = target[key]
        
        # Set the value
        target[keys[-1]] = value
        
        # Save state
        self._save_state()
        
        # Emit signal
        self.state_changed.emit(self._state)
        
        logger.debug(f"Set state value {key_path} = {value}")
    
    def add_recent_file(self, file_path: str) -> None:
        """
        Add a file to the recent files list
        
        Args:
            file_path: Path to file
        """
        if not file_path or not os.path.exists(file_path):
            return
        
        # Get the absolute path
        file_path = os.path.abspath(file_path)
        
        # Get current list
        recent_files = self._state["recent_files"]
        
        # Remove if already in list
        if file_path in recent_files:
            recent_files.remove(file_path)
        
        # Add to beginning of list
        recent_files.insert(0, file_path)
        
        # Limit list size
        max_recent = self._state["settings"]["max_recent_files"]
        if len(recent_files) > max_recent:
            recent_files = recent_files[:max_recent]
        
        # Update state
        self._state["recent_files"] = recent_files
        self._state["last_session"]["last_open_file"] = file_path
        
        # Save state
        self._save_state()
        
        # Emit signal
        self.state_changed.emit(self._state)
        
        logger.debug(f"Added recent file: {file_path}")
    
    def add_recent_directory(self, directory_path: str) -> None:
        """
        Add a directory to the recent directories list
        
        Args:
            directory_path: Path to directory
        """
        if not directory_path or not os.path.isdir(directory_path):
            return
        
        # Get the absolute path
        directory_path = os.path.abspath(directory_path)
        
        # Get current list
        recent_dirs = self._state["recent_directories"]
        
        # Remove if already in list
        if directory_path in recent_dirs:
            recent_dirs.remove(directory_path)
        
        # Add to beginning of list
        recent_dirs.insert(0, directory_path)
        
        # Limit list size
        max_recent = self._state["settings"]["max_recent_files"]
        if len(recent_dirs) > max_recent:
            recent_dirs = recent_dirs[:max_recent]
        
        # Update state
        self._state["recent_directories"] = recent_dirs
        self._state["last_session"]["last_directory"] = directory_path
        
        # Save state
        self._save_state()
        
        # Emit signal
        self.state_changed.emit(self._state)
        
        logger.debug(f"Added recent directory: {directory_path}")
    
    def set_last_screen(self, screen_name: str) -> None:
        """
        Set the last active screen
        
        Args:
            screen_name: Name of the screen
        """
        self._state["last_session"]["last_screen"] = screen_name
        self._save_state()
        logger.debug(f"Set last screen: {screen_name}")
    
    def clear_recent_files(self) -> None:
        """Clear the recent files list"""
        self._state["recent_files"] = []
        self._save_state()
        self.state_changed.emit(self._state)
        logger.info("Cleared recent files list")
    
    def clear_recent_directories(self) -> None:
        """Clear the recent directories list"""
        self._state["recent_directories"] = []
        self._save_state()
        self.state_changed.emit(self._state)
        logger.info("Cleared recent directories list")
    
    def reset_to_defaults(self) -> None:
        """Reset all settings to defaults"""
        # Only reset settings, keep recent files and last session
        self._state["settings"] = {
            "theme": "auto",
            "max_recent_files": 10,
            "auto_save": True,
            "auto_load_last_file": False,
            "console_log_level": "INFO",
            "file_log_level": "DEBUG",
            "show_tooltips": True,
            "confirm_on_exit": True
        }
        self._save_state()
        self.state_changed.emit(self._state)
        logger.info("Reset settings to defaults")
