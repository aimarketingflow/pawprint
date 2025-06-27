#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automation Screen - Batch Operations Tab (Part 3d)
Event handlers for task events and batch completion
"""

import os
import sys
import logging
import datetime
import json
from typing import List, Dict, Any, Optional

from PyQt6.QtWidgets import (
    QMessageBox, QFileDialog
)
from PyQt6.QtCore import Qt, QThread, pyqtSlot
from PyQt6.QtGui import QColor, QFont

logger = logging.getLogger(__name__)

# Event handlers for the AutomationScreen class

@pyqtSlot(str, int)
def on_task_started(self, folder_path, row_index):
    """Handle task started signal"""
    try:
        folder_name = os.path.basename(folder_path)
        # Update status in table
        self.update_task_in_table(
            row_index, 
            status="Running",
            progress=0
        )
        
        # Log event
        logger.info(f"Started batch task for folder: {folder_path}")
        
    except Exception as e:
        logger.error(f"Error handling task start: {str(e)}")

@pyqtSlot(str, int, int)
def on_task_progress(self, folder_path, progress_percent, row_index):
    """Handle task progress signal"""
    try:
        # Update progress in table
        self.update_task_in_table(
            row_index, 
            progress=progress_percent
        )
        
    except Exception as e:
        logger.error(f"Error handling task progress: {str(e)}")

@pyqtSlot(str, str, str, int)
def on_task_completed(self, folder_path, result, time_str, row_index):
    """Handle task completed signal"""
    try:
        folder_name = os.path.basename(folder_path)
        
        # Update status in table
        self.update_task_in_table(
            row_index, 
            status="Completed",
            progress=100,
            time_str=time_str,
            result=result
        )
        
        # Update progress count
        completed = 0
        total = self.tasks_table.rowCount()
        
        for i in range(total):
            status = self.tasks_table.item(i, 1).text()
            if status in ["Completed", "Failed"]:
                completed += 1
        
        self.progress_count_label.setText(f"{completed} / {total} completed")
        
        # Log completion
        logger.info(f"Completed batch task for folder: {folder_path}, result: {result}")
        
    except Exception as e:
        logger.error(f"Error handling task completion: {str(e)}")

@pyqtSlot(str, str, int)
def on_task_error(self, folder_path, error_message, row_index):
    """Handle task error signal"""
    try:
        folder_name = os.path.basename(folder_path)
        
        # Update status in table
        self.update_task_in_table(
            row_index, 
            status="Failed",
            result=f"Error: {error_message}",
            time_str="--"
        )
        
        # Update progress count
        completed = 0
        total = self.tasks_table.rowCount()
        
        for i in range(total):
            status = self.tasks_table.item(i, 1).text()
            if status in ["Completed", "Failed"]:
                completed += 1
        
        self.progress_count_label.setText(f"{completed} / {total} completed")
        
        # Log error
        logger.error(f"Error in batch task for folder: {folder_path}, error: {error_message}")
        
    except Exception as e:
        logger.error(f"Error handling task error event: {str(e)}")

@pyqtSlot(int, int, str, str)
def on_batch_progress(self, overall_percent, file_percent, status, current_task):
    """Handle batch progress update signal"""
    try:
        # Only update overall progress if value is valid
        if overall_percent >= 0:
            self.overall_progress.setValue(overall_percent)
        
        # Update file progress if provided
        if file_percent >= 0:
            self.file_progress.setValue(file_percent)
        
        # Update status text
        if status:
            self.batch_status_label.setText(status)
        
        # Update current task text
        if current_task:
            self.current_task_label.setText(current_task)
        
    except Exception as e:
        logger.error(f"Error handling batch progress: {str(e)}")

@pyqtSlot(dict)
def on_batch_completed(self, results):
    """Handle batch operation completion signal"""
    try:
        # Stop the timer
        self.batch_timer.stop()
        
        # Format completion time
        duration = results.get('duration', 0)
        duration_str = str(datetime.timedelta(seconds=duration))
        
        # Update UI state
        self.is_batch_running = False
        self.execute_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        
        # Set final status
        total = len(results.get('details', []))
        completed = results.get('completed', 0)
        failed = results.get('failed', 0)
        
        status_text = f"Completed: {completed}, Failed: {failed}, Total time: {duration_str}"
        self.batch_status_label.setText(status_text)
        self.progress_count_label.setText(f"{completed} / {total} completed")
        self.current_task_label.setText("Operation completed")
        
        # Ensure progress bar is at 100% if all succeeded
        if failed == 0 and completed == total:
            self.overall_progress.setValue(100)
        
        # Clean up thread
        if hasattr(self, 'batch_thread') and self.batch_thread.isRunning():
            self.batch_thread.quit()
            self.batch_thread.wait()
        
        # Show completion dialog
        if failed > 0:
            message_text = (f"Batch operation completed with some failures.\n"
                          f"Completed: {completed}, Failed: {failed}\n"
                          f"Total time: {duration_str}")
            
            QMessageBox.warning(self, "Batch Operation Completed", message_text)
        else:
            message_text = (f"Batch operation completed successfully!\n"
                          f"Total folders processed: {completed}\n"
                          f"Changed: {results.get('changed', 0)}, Unchanged: {results.get('unchanged', 0)}\n"
                          f"Total time: {duration_str}")
            
            QMessageBox.information(self, "Batch Operation Completed", message_text)
        
        # Ask if user wants to export results
        self.prompt_export_results(results)
        
        # Log completion
        logger.info(f"Batch operation completed: {status_text}")
        
    except Exception as e:
        logger.error(f"Error handling batch completion: {str(e)}")

def prompt_export_results(self, results):
    """Ask user if they want to export batch results"""
    reply = QMessageBox.question(
        self, "Export Results", 
        "Do you want to export the batch operation results?",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    )
    
    if reply != QMessageBox.StandardButton.Yes:
        return
    
    # Get export format preference
    formats = ["JSON", "CSV", "Markdown Report"]
    format_dialog = QMessageBox(self)
    format_dialog.setWindowTitle("Select Export Format")
    format_dialog.setText("Choose the export format:")
    format_dialog.setIcon(QMessageBox.Icon.Question)
    
    # Add format buttons
    for fmt in formats:
        format_dialog.addButton(fmt, QMessageBox.ButtonRole.AcceptRole)
    format_dialog.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)
    
    # Show dialog and get result
    choice = format_dialog.exec()
    
    if choice == QMessageBox.DialogCode.Rejected:
        return
    
    selected_format = format_dialog.clickedButton().text()
    
    try:
        # Get export file path
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        default_name = f"batch_results_{timestamp}"
        
        file_extension = ".json"
        filter_string = "JSON Files (*.json)"
        
        if selected_format == "CSV":
            file_extension = ".csv"
            filter_string = "CSV Files (*.csv)"
        elif selected_format == "Markdown Report":
            file_extension = ".md"
            filter_string = "Markdown Files (*.md)"
        
        # Ask for save location
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Batch Results",
            os.path.join(os.path.expanduser("~"), default_name + file_extension),
            filter_string
        )
        
        if not file_path:
            return
        
        # Export the results
        if selected_format == "JSON":
            self.export_results_json(results, file_path)
        elif selected_format == "CSV":
            self.export_results_csv(results, file_path)
        elif selected_format == "Markdown Report":
            self.export_results_markdown(results, file_path)
        
        # Confirm export
        QMessageBox.information(
            self,
            "Export Complete",
            f"Results exported successfully to:\n{file_path}"
        )
        
    except Exception as e:
        logger.error(f"Error exporting results: {str(e)}")
        QMessageBox.critical(
            self,
            "Export Error",
            f"Failed to export results: {str(e)}"
        )

def export_results_json(self, results, file_path):
    """Export batch results to JSON file"""
    # Add timestamp and metadata
    export_data = results.copy()
    export_data['export_timestamp'] = datetime.datetime.now().isoformat()
    export_data['operation_type'] = self.get_operation_settings()['name']
    
    # Write to file
    with open(file_path, 'w') as f:
        json.dump(export_data, f, indent=2)

def export_results_csv(self, results, file_path):
    """Export batch results to CSV file"""
    import csv
    
    # Prepare CSV headers and rows
    headers = ['Folder', 'Status', 'Success', 'Time', 'Output']
    rows = []
    
    for detail in results.get('details', []):
        rows.append([
            detail.get('folder', ''),
            detail.get('status', ''),
            'Yes' if detail.get('success', False) else 'No',
            detail.get('time', ''),
            detail.get('output', '')
        ])
    
    # Write to CSV
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def export_results_markdown(self, results, file_path):
    """Export batch results to Markdown report"""
    # Get operation details
    op_type = self.get_operation_settings()['name']
    
    # Format timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Calculate duration
    duration = results.get('duration', 0)
    duration_str = str(datetime.timedelta(seconds=duration))
    
    # Prepare markdown content
    md_content = [
        f"# Batch Operation Results - {op_type}",
        f"*Generated on: {timestamp}*",
        "",
        "## Summary",
        f"- **Total folders processed:** {len(results.get('details', []))}",
        f"- **Successfully completed:** {results.get('completed', 0)}",
        f"- **Failed:** {results.get('failed', 0)}",
        f"- **Changed:** {results.get('changed', 0)}",
        f"- **Unchanged:** {results.get('unchanged', 0)}",
        f"- **Total duration:** {duration_str}",
        "",
        "## Detailed Results",
        "",
        "| Folder | Status | Time | Result |",
        "| ------ | ------ | ---- | ------ |",
    ]
    
    # Add rows for each folder
    for detail in results.get('details', []):
        folder = os.path.basename(detail.get('folder', ''))
        status = "✅ Success" if detail.get('success', False) else "❌ Failed"
        time = detail.get('time', '--')
        output = detail.get('output', '').replace('|', '\\|')  # Escape any pipe characters
        
        md_content.append(f"| {folder} | {status} | {time} | {output} |")
    
    # Join all lines and write to file
    with open(file_path, 'w') as f:
        f.write('\n'.join(md_content))
