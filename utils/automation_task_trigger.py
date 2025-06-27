#!/usr/bin/env python3
"""
Task Trigger System for Pawprinting PyQt6 V2 Automation

Manages triggers that can start tasks based on events such as file changes,
task completions, and system events.

Author: AIMF LLC
Date: June 20, 2025
"""

import os
import sys
import logging
import uuid
from enum import Enum
from typing import Dict, List, Any, Optional, Set, Tuple, Callable

from PyQt6.QtCore import QObject, pyqtSignal

from utils.automation_action_base import Action
from utils.automation_task_types import TaskTriggerType
from utils.automation_task_manager import get_task_manager
from utils.folder_monitor import FolderMonitorManager, FileChangeType

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.automation.task_trigger")

class TriggerConditionOperator(Enum):
    """Operators for trigger conditions"""
    EQUALS = "equals"
    NOT_EQUALS = "not_equals"
    CONTAINS = "contains"
    NOT_CONTAINS = "not_contains"
    STARTS_WITH = "starts_with"
    ENDS_WITH = "ends_with"
    GREATER_THAN = "greater_than"
    LESS_THAN = "less_than"
    MATCHES_REGEX = "matches_regex"

class TaskTrigger:
    """Base class for task triggers"""
    
    def __init__(self, 
                 trigger_id: str,
                 task_id: str,
                 action: Action,
                 trigger_type: TaskTriggerType,
                 config: Dict[str, Any] = None):
        """Initialize task trigger"""
        self.trigger_id = trigger_id
        self.task_id = task_id
        self.action = action
        self.trigger_type = trigger_type
        self.config = config or {}
        self.enabled = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "trigger_id": self.trigger_id,
            "task_id": self.task_id,
            "action_id": self.action.action_id,
            "action_config": self.action.config,
            "trigger_type": self.trigger_type.value,
            "config": self.config,
            "enabled": self.enabled
        }
        
    @staticmethod
    def from_dict(data: Dict[str, Any], action_factory: Callable[[str, Dict[str, Any]], Action]) -> 'TaskTrigger':
        """Create from dictionary"""
        action = action_factory(data["action_id"], data["action_config"])
        
        trigger = TaskTrigger(
            trigger_id=data["trigger_id"],
            task_id=data["task_id"],
            action=action,
            trigger_type=TaskTriggerType(data["trigger_type"]),
            config=data["config"]
        )
        
        trigger.enabled = data.get("enabled", True)
        return trigger
    
    def evaluate_condition(self, data: Dict[str, Any]) -> bool:
        """
        Evaluate trigger condition based on data
        
        This uses a simple condition system where each condition has:
        - field: the field in the data to check
        - operator: the comparison operator
        - value: the value to compare against
        """
        if "conditions" not in self.config:
            return True  # No conditions, always trigger
            
        conditions = self.config["conditions"]
        if not conditions:
            return True  # Empty conditions, always trigger
            
        # Check if we need ALL conditions to match or just ANY
        require_all = self.config.get("require_all_conditions", True)
        
        result = True if require_all else False
        
        for condition in conditions:
            field = condition.get("field", "")
            operator_str = condition.get("operator", "equals")
            expected_value = condition.get("value", None)
            
            # Skip if no field specified
            if not field:
                continue
                
            # Get actual value from data, using nested field path
            path_parts = field.split(".")
            actual_value = data
            
            try:
                for part in path_parts:
                    actual_value = actual_value[part]
            except (KeyError, TypeError):
                # Field doesn't exist
                condition_result = False
            else:
                # Field exists, compare values
                operator = TriggerConditionOperator(operator_str)
                
                if operator == TriggerConditionOperator.EQUALS:
                    condition_result = actual_value == expected_value
                    
                elif operator == TriggerConditionOperator.NOT_EQUALS:
                    condition_result = actual_value != expected_value
                    
                elif operator == TriggerConditionOperator.CONTAINS:
                    if isinstance(actual_value, str) and isinstance(expected_value, str):
                        condition_result = expected_value in actual_value
                    elif isinstance(actual_value, (list, tuple, set)):
                        condition_result = expected_value in actual_value
                    else:
                        condition_result = False
                        
                elif operator == TriggerConditionOperator.NOT_CONTAINS:
                    if isinstance(actual_value, str) and isinstance(expected_value, str):
                        condition_result = expected_value not in actual_value
                    elif isinstance(actual_value, (list, tuple, set)):
                        condition_result = expected_value not in actual_value
                    else:
                        condition_result = False
                        
                elif operator == TriggerConditionOperator.STARTS_WITH:
                    if isinstance(actual_value, str) and isinstance(expected_value, str):
                        condition_result = actual_value.startswith(expected_value)
                    else:
                        condition_result = False
                        
                elif operator == TriggerConditionOperator.ENDS_WITH:
                    if isinstance(actual_value, str) and isinstance(expected_value, str):
                        condition_result = actual_value.endswith(expected_value)
                    else:
                        condition_result = False
                        
                elif operator == TriggerConditionOperator.GREATER_THAN:
                    try:
                        condition_result = float(actual_value) > float(expected_value)
                    except (ValueError, TypeError):
                        condition_result = False
                        
                elif operator == TriggerConditionOperator.LESS_THAN:
                    try:
                        condition_result = float(actual_value) < float(expected_value)
                    except (ValueError, TypeError):
                        condition_result = False
                        
                elif operator == TriggerConditionOperator.MATCHES_REGEX:
                    if isinstance(actual_value, str) and isinstance(expected_value, str):
                        import re
                        try:
                            pattern = re.compile(expected_value)
                            condition_result = bool(pattern.search(actual_value))
                        except re.error:
                            condition_result = False
                    else:
                        condition_result = False
                
                else:
                    # Unknown operator
                    condition_result = False
            
            if require_all:
                result = result and condition_result
                if not result:
                    break  # Short-circuit for AND logic
            else:
                result = result or condition_result
                if result:
                    break  # Short-circuit for OR logic
                    
        return result

class TaskTriggerManager(QObject):
    """Manages task triggers"""
    
    # Signals
    trigger_added = pyqtSignal(str)  # trigger_id
    trigger_updated = pyqtSignal(str)  # trigger_id
    trigger_removed = pyqtSignal(str)  # trigger_id
    trigger_fired = pyqtSignal(str, str)  # trigger_id, task_id
    
    def __init__(self):
        """Initialize trigger manager"""
        super().__init__()
        self._triggers = {}  # trigger_id -> TaskTrigger
        self._task_manager = get_task_manager()
        self._setup_file_change_triggers()
        self._setup_task_completion_triggers()
    
    def add_trigger(self, trigger: TaskTrigger) -> bool:
        """Add a new trigger"""
        if trigger.trigger_id in self._triggers:
            logger.warning(f"Trigger with ID {trigger.trigger_id} already exists")
            return False
            
        self._triggers[trigger.trigger_id] = trigger
        self.trigger_added.emit(trigger.trigger_id)
        logger.info(f"Added trigger {trigger.trigger_id} for task {trigger.task_id}")
        return True
    
    def update_trigger(self, trigger_id: str, updates: Dict[str, Any]) -> bool:
        """Update an existing trigger"""
        if trigger_id not in self._triggers:
            logger.warning(f"Trigger with ID {trigger_id} does not exist")
            return False
            
        trigger = self._triggers[trigger_id]
        
        # Apply updates
        for key, value in updates.items():
            if key == "enabled":
                trigger.enabled = value
            elif key == "config":
                trigger.config = value
            elif key == "trigger_type" and isinstance(value, str):
                trigger.trigger_type = TaskTriggerType(value)
        
        self.trigger_updated.emit(trigger_id)
        logger.info(f"Updated trigger {trigger_id}")
        return True
    
    def remove_trigger(self, trigger_id: str) -> bool:
        """Remove a trigger"""
        if trigger_id not in self._triggers:
            logger.warning(f"Trigger with ID {trigger_id} does not exist")
            return False
            
        del self._triggers[trigger_id]
        self.trigger_removed.emit(trigger_id)
        logger.info(f"Removed trigger {trigger_id}")
        return True
    
    def get_trigger(self, trigger_id: str) -> Optional[TaskTrigger]:
        """Get a trigger by ID"""
        return self._triggers.get(trigger_id)
    
    def get_all_triggers(self) -> List[TaskTrigger]:
        """Get all triggers"""
        return list(self._triggers.values())
    
    def get_triggers_by_type(self, trigger_type: TaskTriggerType) -> List[TaskTrigger]:
        """Get triggers by type"""
        return [t for t in self._triggers.values() if t.trigger_type == trigger_type]
    
    def _setup_file_change_triggers(self) -> None:
        """Set up handlers for file change triggers"""
        # Get the folder monitor manager
        monitor_manager = FolderMonitorManager.get_instance()
        
        # Connect to signals
        monitor_manager.file_created.connect(self._on_file_created)
        monitor_manager.file_modified.connect(self._on_file_modified)
        monitor_manager.file_deleted.connect(self._on_file_deleted)
        
    def _setup_task_completion_triggers(self) -> None:
        """Set up handlers for task completion triggers"""
        self._task_manager.task_completed.connect(self._on_task_completed)
    
    def _on_file_created(self, monitor_id: str, file_path: str) -> None:
        """Handle file created event"""
        self._process_file_event(FileChangeType.CREATED, monitor_id, file_path)
    
    def _on_file_modified(self, monitor_id: str, file_path: str) -> None:
        """Handle file modified event"""
        self._process_file_event(FileChangeType.MODIFIED, monitor_id, file_path)
    
    def _on_file_deleted(self, monitor_id: str, file_path: str) -> None:
        """Handle file deleted event"""
        self._process_file_event(FileChangeType.DELETED, monitor_id, file_path)
    
    def _process_file_event(self, change_type: FileChangeType, monitor_id: str, file_path: str) -> None:
        """Process a file change event for triggers"""
        # Get all file change triggers
        file_triggers = self.get_triggers_by_type(TaskTriggerType.FILE_CHANGE)
        
        # Create event data
        event_data = {
            "change_type": change_type.value,
            "monitor_id": monitor_id,
            "file_path": file_path,
            "file_name": os.path.basename(file_path),
            "directory": os.path.dirname(file_path),
            "extension": os.path.splitext(file_path)[1].lower()[1:] if os.path.splitext(file_path)[1] else ""
        }
        
        # Check each trigger
        for trigger in file_triggers:
            if not trigger.enabled:
                continue
                
            # Check if this trigger is for this monitor
            if "monitor_id" in trigger.config and trigger.config["monitor_id"] != monitor_id:
                continue
                
            # Check if this trigger is for this change type
            if "change_types" in trigger.config:
                change_types = trigger.config["change_types"]
                if change_types and change_type.value not in change_types:
                    continue
            
            # Evaluate conditions
            if trigger.evaluate_condition(event_data):
                # Trigger matches, execute task
                self._execute_triggered_task(trigger, event_data)
    
    def _on_task_completed(self, completed_task_id: str, result) -> None:
        """Handle task completion event for triggers"""
        # Get all completion triggers
        completion_triggers = self.get_triggers_by_type(TaskTriggerType.COMPLETION)
        
        # Create event data
        event_data = {
            "completed_task_id": completed_task_id,
            "result": result.to_dict() if hasattr(result, "to_dict") else {"success": True, "message": str(result)}
        }
        
        # Check each trigger
        for trigger in completion_triggers:
            if not trigger.enabled:
                continue
                
            # Check if this trigger is for this task
            if "parent_task_id" in trigger.config and trigger.config["parent_task_id"] != completed_task_id:
                continue
            
            # Evaluate conditions
            if trigger.evaluate_condition(event_data):
                # Trigger matches, execute task
                self._execute_triggered_task(trigger, event_data)
    
    def _execute_triggered_task(self, trigger: TaskTrigger, event_data: Dict[str, Any]) -> None:
        """Execute a task when a trigger fires"""
        # Generate a unique task ID
        task_id = f"{trigger.task_id}_triggered_{uuid.uuid4().hex[:8]}"
        
        # Set up task variables
        variables = {
            "trigger_id": trigger.trigger_id,
            "trigger_type": trigger.trigger_type.value,
            "event_data": event_data
        }
        
        # Execute the task
        success = self._task_manager.execute_task(
            task_id,
            trigger.action,
            {"variables": variables}
        )
        
        if success:
            self.trigger_fired.emit(trigger.trigger_id, task_id)
            logger.info(f"Trigger {trigger.trigger_id} fired, executing task {task_id}")
        else:
            logger.error(f"Failed to execute task for trigger {trigger.trigger_id}")

# Singleton instance
_instance = None

def get_task_trigger_manager() -> TaskTriggerManager:
    """Get the singleton task trigger manager instance"""
    global _instance
    if _instance is None:
        _instance = TaskTriggerManager()
    return _instance
