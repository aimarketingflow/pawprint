#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automation Screen - Batch Operations Tab (Part 3c)
Task execution and task manager integration
"""

import os
import sys
import logging
import datetime
import json
import threading
from typing import List, Dict, Any, Optional

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QMessageBox, QApplication
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QObject

logger = logging.getLogger(__name__)

# BatchTaskWorker class for threaded execution
class BatchTaskWorker(QObject):
    """Worker class for executing batch tasks in a separate thread"""
    # Define signals
    taskStarted = pyqtSignal(str, int)  # folder_path, row_index
    taskProgress = pyqtSignal(str, int, int)  # folder_path, progress_percent, row_index
    taskCompleted = pyqtSignal(str, str, str, int)  # folder_path, result, time_str, row_index
    taskError = pyqtSignal(str, str, int)  # folder_path, error_message, row_index
    
    batchProgress = pyqtSignal(int, int, str, str)  # overall_percent, file_percent, status, current_task
    batchCompleted = pyqtSignal(dict)  # summary_dict
    
    def __init__(self, task_manager, task_factory, history_manager, folders, operation, settings):
        super().__init__()
        self.task_manager = task_manager
        self.task_factory = task_factory
        self.history_manager = history_manager
        self.folders = folders
        self.operation = operation
        self.settings = settings
        self.is_running = False
        self.should_cancel = False
    
    def run(self):
        """Execute the batch operation on all selected folders"""
        self.is_running = True
        self.should_cancel = False
        start_time = datetime.datetime.now()
        
        # Initialize task tracking
        completed = 0
        total = len(self.folders)
        results = {
            'completed': 0,
            'failed': 0,
            'unchanged': 0,
            'changed': 0,
            'duration': 0,
            'details': []
        }
        
        try:
            # Process each folder
            for i, folder in enumerate(self.folders):
                if self.should_cancel:
                    break
                
                folder_basename = os.path.basename(folder)
                row_index = i  # Corresponds to the row in the table
                
                self.taskStarted.emit(folder, row_index)
                self.batchProgress.emit(
                    int(i * 100 / total), 0, 
                    f"Processing {i+1} of {total}",
                    f"Starting task for {folder_basename}"
                )
                
                # Create appropriate task based on operation type
                task = self.create_task(folder)
                
                if not task:
                    self.taskError.emit(
                        folder, 
                        f"Failed to create task for operation: {self.operation['type']}", 
                        row_index
                    )
                    results['failed'] += 1
                    continue
                
                # Execute the task
                try:
                    # Process task with progress updates
                    result = self.execute_task(task, folder, row_index)
                    
                    # Track completion time
                    task_time = datetime.datetime.now() - start_time
                    time_str = str(datetime.timedelta(seconds=int(task_time.total_seconds())))
                    
                    # Update task status
                    self.taskCompleted.emit(folder, result['status'], time_str, row_index)
                    
                    # Update result statistics
                    if result['success']:
                        results['completed'] += 1
                        if result['changes']:
                            results['changed'] += 1
                        else:
                            results['unchanged'] += 1
                    else:
                        results['failed'] += 1
                        
                    # Store task details
                    results['details'].append({
                        'folder': folder,
                        'success': result['success'],
                        'status': result['status'],
                        'time': time_str,
                        'output': result.get('output', ''),
                    })
                    
                    completed += 1
                    
                except Exception as e:
                    logger.error(f"Error processing folder {folder}: {str(e)}")
                    self.taskError.emit(folder, str(e), row_index)
                    results['failed'] += 1
                
                # Update overall progress
                self.batchProgress.emit(
                    int(completed * 100 / total), 100,
                    f"Completed {completed} of {total}",
                    f"Finished task for {folder_basename}"
                )
                
                # Small delay to prevent UI freezing
                QThread.msleep(50)
        
        except Exception as e:
            logger.error(f"Batch operation failed: {str(e)}")
            self.batchProgress.emit(
                int(completed * 100 / total), 0,
                f"Error: {str(e)}",
                "Batch operation failed"
            )
        
        finally:
            # Calculate total duration
            total_time = datetime.datetime.now() - start_time
            results['duration'] = int(total_time.total_seconds())
            
            # Emit batch completion signal with results
            self.batchCompleted.emit(results)
            self.is_running = False
    
    def create_task(self, folder):
        """Create appropriate task object based on operation type"""
        try:
            op_type = self.operation['type']
            
            if op_type == "generate":
                # Create new pawprint task
                return self.task_factory.create_pawprint_task(
                    folder,
                    recursion_depth=self.settings.get('depth', 5),
                    include_hidden=self.settings.get('include_hidden', False),
                    output_dir=self.settings.get('output_dir', None),
                )
                
            elif op_type == "refresh":
                # Create refresh task
                return self.task_factory.create_refresh_task(
                    folder,
                    auto_detect=self.settings.get('auto_detect', True),
                    force_refresh=self.settings.get('force_refresh', False),
                    update_timestamp=self.settings.get('update_timestamp', False),
                )
                
            elif op_type == "compare":
                # Create comparison task
                compare_method = self.settings.get('compare_method', 'latest_with_previous')
                detail_level = self.settings.get('compare_detail', 'changed_only')
                visualization = self.settings.get('visualization', 'simple')
                
                return self.task_factory.create_comparison_task(
                    folder,
                    compare_method=compare_method,
                    detail_level=detail_level,
                    visualization=visualization,
                )
                
            elif op_type == "report":
                # Create report generation task
                report_format = self.settings.get('report_format', 'markdown')
                include_options = {
                    'summary': self.settings.get('include_summary', True),
                    'changes': self.settings.get('include_changes', True),
                    'charts': self.settings.get('include_charts', True),
                }
                output_dir = self.settings.get('report_output_dir', None)
                
                return self.task_factory.create_report_task(
                    folder,
                    report_format=report_format,
                    include_options=include_options,
                    output_dir=output_dir,
                )
                
        except Exception as e:
            logger.error(f"Failed to create task: {str(e)}")
            return None
    
    def execute_task(self, task, folder, row_index):
        """Execute a task with progress tracking"""
        result = {
            'success': False,
            'changes': False,
            'status': 'Failed',
            'output': ''
        }
        
        try:
            # Register progress callback if task supports it
            if hasattr(task, 'register_progress_callback'):
                def progress_callback(progress_pct, status_msg):
                    self.taskProgress.emit(folder, progress_pct, row_index)
                    self.batchProgress.emit(
                        -1,  # Don't update overall progress
                        progress_pct,
                        status_msg,
                        f"Processing {os.path.basename(folder)}: {progress_pct}%"
                    )
                
                task.register_progress_callback(progress_callback)
            
            # Execute the task
            task_result = self.task_manager.execute_task(task)
            
            # Process result
            result['success'] = task_result.get('success', False)
            result['output'] = task_result.get('output', '')
            
            if result['success']:
                # Check for changes
                if 'changes' in task_result:
                    result['changes'] = task_result['changes']
                    if result['changes']:
                        result['status'] = f"Changes: {task_result.get('change_count', 'Some')}"
                    else:
                        result['status'] = "Unchanged"
                else:
                    result['status'] = "Completed"
            else:
                result['status'] = f"Error: {task_result.get('error', 'Unknown')}"
            
            # Add to history
            self.history_manager.add_entry({
                'timestamp': datetime.datetime.now().isoformat(),
                'folder_path': folder,
                'operation': self.operation['type'],
                'success': result['success'],
                'status': result['status'],
                'details': task_result,
            })
            
        except Exception as e:
            logger.error(f"Task execution error: {str(e)}")
            result['status'] = f"Error: {str(e)}"
        
        return result
    
    def cancel(self):
        """Cancel the batch operation"""
        self.should_cancel = True

# Methods to be added to the AutomationScreen class
def execute_batch_operation(self):
    """Execute the batch operation with selected folders and options"""
    # Validate configuration first
    if not self.validate_batch_config():
        return
    
    # Get selected folders
    folders = self.get_selected_folders()
    if not folders:
        QMessageBox.warning(self, "No Folders", "No folders selected for batch processing")
        return
    
    # Get operation type and settings
    operation = self.get_operation_settings()
    settings = self.get_batch_settings()
    
    # Confirm with user
    msg = (f"You are about to run <b>{operation['name']}</b> on "
           f"<b>{len(folders)}</b> folder(s).\n\n"
           f"This operation cannot be undone. Proceed?")
    
    reply = QMessageBox.question(
        self, "Confirm Batch Operation", 
        msg, 
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    )
    
    if reply != QMessageBox.StandardButton.Yes:
        return
    
    # Set up tasks table
    self.tasks_table.setRowCount(0)
    for folder in folders:
        self.add_task_to_table(folder)
    
    # Set UI to running state
    self.is_batch_running = True
    self.batch_start_time = datetime.datetime.now()
    self.batch_timer.start(1000)  # Update time every second
    
    self.batch_status_label.setText("Starting...")
    self.execute_button.setEnabled(False)
    self.cancel_button.setEnabled(True)
    
    # Create worker in a new thread
    self.batch_worker = BatchTaskWorker(
        self.task_manager,
        self.task_factory,
        self.history_manager,
        folders,
        operation,
        settings
    )
    
    # Connect signals
    self.batch_worker.taskStarted.connect(self.on_task_started)
    self.batch_worker.taskProgress.connect(self.on_task_progress)
    self.batch_worker.taskCompleted.connect(self.on_task_completed)
    self.batch_worker.taskError.connect(self.on_task_error)
    
    self.batch_worker.batchProgress.connect(self.on_batch_progress)
    self.batch_worker.batchCompleted.connect(self.on_batch_completed)
    
    # Create thread
    self.batch_thread = QThread()
    self.batch_worker.moveToThread(self.batch_thread)
    self.batch_thread.started.connect(self.batch_worker.run)
    
    # Start thread
    self.batch_thread.start()

def cancel_batch_operation(self):
    """Cancel the currently running batch operation"""
    if not self.is_batch_running:
        return
    
    reply = QMessageBox.question(
        self, "Cancel Operation", 
        "Are you sure you want to cancel the current batch operation?",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    )
    
    if reply != QMessageBox.StandardButton.Yes:
        return
    
    # Cancel the worker
    if hasattr(self, 'batch_worker') and self.batch_worker.is_running:
        self.batch_worker.cancel()
        self.batch_status_label.setText("Cancelling...")
        self.cancel_button.setEnabled(False)

def get_operation_settings(self):
    """Get the current operation settings"""
    op_index = self.operation_type.currentIndex()
    op_types = ["generate", "refresh", "compare", "report"]
    op_names = [
        "Generate New Pawprints", 
        "Refresh Existing Pawprints",
        "Compare with Previous",
        "Generate & Export Report"
    ]
    
    return {
        'type': op_types[op_index] if op_index < len(op_types) else "generate",
        'name': op_names[op_index] if op_index < len(op_names) else "Generate New Pawprints",
    }

def get_batch_settings(self):
    """Get all the current batch settings based on operation type"""
    settings = {
        # Common settings
        'parallel': self.parallel_processing.isChecked(),
        'threads': self.thread_count.value(),
        'priority': self.process_priority.currentText().lower(),
    }
    
    # Get operation-specific settings
    op_type = self.get_operation_settings()['type']
    
    if op_type == "generate":
        settings.update({
            'depth': self.depth_spinner.value(),
            'include_hidden': self.include_hidden.isChecked(),
            'output_dir': self.output_dir.text() if self.output_dir.text() else None,
        })
        
    elif op_type == "refresh":
        settings.update({
            'auto_detect': self.auto_detect.isChecked(),
            'update_timestamp': self.update_timestamp.isChecked(),
            'force_refresh': self.force_refresh.isChecked(),
        })
        
    elif op_type == "compare":
        settings.update({
            'compare_method': self.compare_method.currentText().lower().replace(' ', '_'),
            'compare_detail': self.compare_detail.currentText().lower().replace(' ', '_'),
            'visualization': self.visualization.currentText().lower(),
        })
        
    elif op_type == "report":
        settings.update({
            'report_format': self.report_format.currentText().lower(),
            'include_summary': self.include_summary.isChecked(),
            'include_changes': self.include_changes.isChecked(),
            'include_charts': self.include_charts.isChecked(),
            'report_output_dir': self.report_output_dir.text() if self.report_output_dir.text() else None,
        })
    
    return settings
