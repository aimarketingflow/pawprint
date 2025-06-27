#!/usr/bin/env python3
"""
Task Factory for Pawprinting PyQt6 V2 Automation

Creates action instances from configuration data by maintaining
a registry of available action types.

Author: AIMF LLC
Date: June 20, 2025
"""

import logging
import importlib
import inspect
from typing import Dict, List, Any, Optional, Type, Callable

from utils.automation_action_base import Action

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.automation.task_factory")

class ActionRegistry:
    """Registry of available action types"""
    
    def __init__(self):
        """Initialize action registry"""
        self._action_classes = {}  # action_type -> Action class
        
    def register_action_class(self, action_type: str, action_class: Type[Action]) -> None:
        """Register an action class"""
        if not inspect.isclass(action_class) or not issubclass(action_class, Action):
            logger.error(f"Cannot register {action_class} as it is not a subclass of Action")
            return
            
        self._action_classes[action_type] = action_class
        logger.debug(f"Registered action class {action_class.__name__} for type '{action_type}'")
        
    def get_action_class(self, action_type: str) -> Optional[Type[Action]]:
        """Get an action class by type"""
        return self._action_classes.get(action_type)
        
    def get_action_types(self) -> List[str]:
        """Get list of registered action types"""
        return list(self._action_classes.keys())
        
    def create_action(self, action_type: str, action_id: str, config: Dict[str, Any] = None) -> Optional[Action]:
        """Create an action instance"""
        action_class = self.get_action_class(action_type)
        if not action_class:
            logger.error(f"Unknown action type: {action_type}")
            return None
            
        try:
            action = action_class(action_id, config)
            return action
        except Exception as e:
            logger.exception(f"Error creating action of type {action_type}: {str(e)}")
            return None
            
class TaskFactory:
    """Factory for creating task actions"""
    
    def __init__(self):
        """Initialize task factory"""
        self._registry = ActionRegistry()
        self._auto_discovered = False
        
    def get_registry(self) -> ActionRegistry:
        """Get the action registry"""
        return self._registry
        
    def create_action(self, action_type: str, action_id: str, config: Dict[str, Any] = None) -> Optional[Action]:
        """Create an action instance"""
        # Auto-discover action classes if not already done
        if not self._auto_discovered:
            self.discover_action_classes()
            
        return self._registry.create_action(action_type, action_id, config)
        
    def create_action_from_dict(self, data: Dict[str, Any]) -> Optional[Action]:
        """Create an action from a dictionary"""
        if "action_type" not in data or "action_id" not in data:
            logger.error("Invalid action data: missing action_type or action_id")
            return None
            
        action_type = data["action_type"]
        action_id = data["action_id"]
        config = data.get("config", {})
        
        return self.create_action(action_type, action_id, config)
        
    def discover_action_classes(self) -> None:
        """Auto-discover action classes in the utils package"""
        try:
            # Import all the automation action modules
            modules_to_scan = [
                "utils.automation_file_operations",
                "utils.automation_file_analysis_actions",
                "utils.automation_file_content_actions",
                "utils.automation_pawprint_actions",
                "utils.automation_folder_monitor_actions"
            ]
            
            for module_name in modules_to_scan:
                try:
                    module = importlib.import_module(module_name)
                    
                    # Find all Action subclasses in the module
                    for name, obj in inspect.getmembers(module):
                        if inspect.isclass(obj) and issubclass(obj, Action) and obj != Action:
                            # Register with a kebab-case name derived from the class name
                            action_type = self._class_name_to_type(name)
                            self._registry.register_action_class(action_type, obj)
                            
                except ImportError as e:
                    logger.warning(f"Could not import {module_name}: {str(e)}")
                    
            self._auto_discovered = True
            logger.info(f"Discovered {len(self._registry.get_action_types())} action types")
            
        except Exception as e:
            logger.exception(f"Error during action class discovery: {str(e)}")
            
    def _class_name_to_type(self, class_name: str) -> str:
        """Convert a CamelCase class name to kebab-case action type"""
        import re
        
        # Insert hyphen before each capital letter and lowercase
        result = re.sub(r'(?<!^)(?=[A-Z])', '-', class_name).lower()
        
        # Remove 'action' suffix if present
        result = re.sub(r'-action$', '', result)
        
        return result
        
    def register_custom_action(self, action_type: str, action_class: Type[Action]) -> None:
        """Register a custom action class"""
        self._registry.register_action_class(action_type, action_class)

# Singleton instance
_instance = None

def get_task_factory() -> TaskFactory:
    """Get the singleton task factory instance"""
    global _instance
    if _instance is None:
        _instance = TaskFactory()
    return _instance
