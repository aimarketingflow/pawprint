#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
test_automation_system.py - Test cases for the Pawprinting PyQt6 V2 automation system

This module contains tests for the automation system components including
TaskManager, TaskScheduler, TaskHistory, and related automation actions.

AIMF LLC - 2025
"""

import os
import sys
import unittest
import tempfile
import json
import logging
from datetime import datetime, timedelta

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import automation components
from utils.automation_system import AutomationSystem
from utils.automation_task_manager import TaskManager, TaskContext
from utils.automation_task_history import TaskHistoryManager
from utils.automation_task_scheduler import TaskScheduler
from utils.automation_task_factory import TaskFactory
from utils.automation_base_action import BaseAutomationAction


class TestAutomationAction(BaseAutomationAction):
    """Test automation action for unit tests"""
    
    def __init__(self, context=None):
        super().__init__(context)
        self.executed = False
        self.progress_reported = False
        self.success = True  # Can be set to False for testing error conditions
        
    def validate(self):
        return True
        
    def execute(self):
        self.executed = True
        # Report progress a few times
        self.report_progress(0.25, "Started execution")
        self.report_progress(0.5, "Halfway through execution")
        self.progress_reported = True
        self.report_progress(1.0, "Completed execution")
        return self.success


class TestTaskManager(unittest.TestCase):
    """Test the TaskManager component"""
    
    def setUp(self):
        self.task_manager = TaskManager()
        
    def test_execute_task(self):
        """Test that a task can be executed successfully"""
        action = TestAutomationAction()
        context = TaskContext()
        
        # Execute task
        result = self.task_manager.execute_task(action, context)
        
        # Verify execution
        self.assertTrue(result.success)
        self.assertTrue(action.executed)
        self.assertTrue(action.progress_reported)
    
    def test_execute_task_failure(self):
        """Test handling of a failed task execution"""
        action = TestAutomationAction()
        action.success = False  # Set to fail
        context = TaskContext()
        
        # Execute task
        result = self.task_manager.execute_task(action, context)
        
        # Verify execution
        self.assertFalse(result.success)
        self.assertTrue(action.executed)


class TestTaskHistory(unittest.TestCase):
    """Test the TaskHistoryManager component"""
    
    def setUp(self):
        # Create a temporary file for history
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        self.history_manager = TaskHistoryManager(self.temp_file.name)
        
    def tearDown(self):
        # Clean up temporary file
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_add_execution(self):
        """Test adding a task execution to history"""
        # Add an execution
        task_id = self.history_manager.add_execution(
            task_type="TestAutomationAction",
            start_time=datetime.now(),
            end_time=datetime.now() + timedelta(seconds=1),
            status="completed",
            params={"test": "value"},
            result={"success": True}
        )
        
        # Verify it was added
        executions = self.history_manager.get_executions()
        self.assertEqual(len(executions), 1)
        self.assertEqual(executions[0]["task_id"], task_id)
        self.assertEqual(executions[0]["task_type"], "TestAutomationAction")
        self.assertEqual(executions[0]["status"], "completed")
        self.assertEqual(executions[0]["params"]["test"], "value")
        self.assertEqual(executions[0]["result"]["success"], True)


class TestAutomationSystem(unittest.TestCase):
    """Test the overall AutomationSystem"""
    
    def setUp(self):
        # Create temporary directory for test files
        self.temp_dir = tempfile.mkdtemp()
        
        # Configure logging for tests
        logging.basicConfig(level=logging.INFO)
        
        # Initialize automation system
        self.automation_system = AutomationSystem(
            data_dir=self.temp_dir,
            log_dir=self.temp_dir
        )
    
    def tearDown(self):
        # Clean up temporary files
        self.automation_system.shutdown()
        if os.path.exists(self.temp_dir):
            for f in os.listdir(self.temp_dir):
                os.unlink(os.path.join(self.temp_dir, f))
            os.rmdir(self.temp_dir)
    
    def test_system_initialization(self):
        """Test that the automation system initializes correctly"""
        self.assertIsNotNone(self.automation_system.task_manager)
        self.assertIsNotNone(self.automation_system.history_manager)
        self.assertIsNotNone(self.automation_system.scheduler)
        self.assertIsNotNone(self.automation_system.trigger_manager)
        
    def test_system_task_execution(self):
        """Test that the automation system can execute tasks"""
        # Register our test action
        self.automation_system.factory.register_action(
            "test", TestAutomationAction
        )
        
        # Create and execute a task
        context = TaskContext()
        action = self.automation_system.factory.create_action("test", context)
        
        # Execute the task
        result = self.automation_system.execute_task(action, context)
        
        # Verify execution
        self.assertTrue(result.success)
        self.assertTrue(action.executed)


if __name__ == '__main__':
    unittest.main()
