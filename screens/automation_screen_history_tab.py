#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automation Screen - History Tab Implementation
Allows viewing and managing pawprint history records
"""

import os
import sys
import logging
import datetime
from typing import List, Dict, Any, Optional

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QComboBox, QCheckBox, QMessageBox,
    QFileDialog, QGroupBox
)
from PyQt6.QtCore import Qt, QDateTime
from PyQt6.QtGui import QColor, QFont

logger = logging.getLogger(__name__)

# Function to add to AutomationScreen class
def setup_history_tab(self):
    """Setup the History tab UI components"""
    # Create layout for history tab
    history_layout = QVBoxLayout(self.history_tab)
    
    # Create controls at top
    controls_layout = QHBoxLayout()
    
    # Filter group
    filter_group = QGroupBox("Filter Options")
    filter_layout = QHBoxLayout(filter_group)
    
    # Date range filter
    self.date_filter = QComboBox()
    self.date_filter.addItems(["All Time", "Last 7 Days", "Last 30 Days", "Custom..."])
    self.date_filter.currentIndexChanged.connect(self.apply_history_filters)
    
    # Status filter
    self.status_filter = QComboBox()
    self.status_filter.addItems(["All Statuses", "Changed", "Unchanged", "Error"])
    self.status_filter.currentIndexChanged.connect(self.apply_history_filters)
    
    # Add to filter layout
    filter_layout.addWidget(QLabel("Date Range:"))
    filter_layout.addWidget(self.date_filter)
    filter_layout.addWidget(QLabel("Status:"))
    filter_layout.addWidget(self.status_filter)
    
    # Add to controls layout
    controls_layout.addWidget(filter_group)
    
    # Action buttons
    actions_group = QGroupBox("Actions")
    actions_layout = QHBoxLayout(actions_group)
    
    self.refresh_history_button = QPushButton("Refresh List")
    self.refresh_history_button.clicked.connect(self.load_history_data)
    
    self.export_history_button = QPushButton("Export CSV")
    self.export_history_button.clicked.connect(self.export_history)
    
    self.generate_report_button = QPushButton("Generate Report")
    self.generate_report_button.clicked.connect(self.generate_history_report)
    
    # Add to actions layout
    actions_layout.addWidget(self.refresh_history_button)
    actions_layout.addWidget(self.export_history_button)
    actions_layout.addWidget(self.generate_report_button)
    
    # Add to controls layout
    controls_layout.addWidget(actions_group)
    
    # Add controls to main layout
    history_layout.addLayout(controls_layout)
    
    # Create history table
    self.history_table = QTableWidget()
    self.history_table.setColumnCount(7)
    self.history_table.setHorizontalHeaderLabels([
        "Timestamp", "Folder Path", "Status", "Changes", 
        "Last Updated", "Duration (s)", "Actions"
    ])
    
    # Set table properties
    self.history_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
    self.history_table.setAlternatingRowColors(True)
    self.history_table.setStyleSheet(
        "alternate-background-color: #1a1a1a; background-color: #121212;"
    )
    self.history_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
    
    # Add to layout
    history_layout.addWidget(self.history_table)
    
    # Load initial data
    self.load_history_data()

def load_history_data(self):
    """Load pawprint history data into the table"""
    try:
        # Clear existing data
        self.history_table.setRowCount(0)
        
        # Get history data from TaskHistoryManager
        history_items = self.history_manager.get_all_entries()
        
        # Apply filters if needed
        filtered_items = self.apply_history_filters(history_items)
        
        # Populate table
        self.history_table.setRowCount(len(filtered_items))
        for row, item in enumerate(filtered_items):
            # Timestamp
            timestamp = QTableWidgetItem(item.get('timestamp', 'Unknown'))
            self.history_table.setItem(row, 0, timestamp)
            
            # Folder path
            folder_path = QTableWidgetItem(item.get('folder_path', 'Unknown'))
            self.history_table.setItem(row, 1, folder_path)
            
            # Status
            status = QTableWidgetItem(item.get('status', 'Unknown'))
            self.history_table.setItem(row, 2, status)
            
            # Color code by status
            if item.get('status') == 'Changed':
                status.setForeground(QColor('#ffaa00'))  # Orange for changes
            elif item.get('status') == 'Unchanged':
                status.setForeground(QColor('#00cc00'))  # Green for unchanged
            elif item.get('status') == 'Error':
                status.setForeground(QColor('#ff5555'))  # Red for errors
            
            # Changes count
            changes = QTableWidgetItem(str(item.get('changes_count', 0)))
            self.history_table.setItem(row, 3, changes)
            
            # Last updated
            last_updated = QTableWidgetItem(item.get('last_updated', 'Unknown'))
            self.history_table.setItem(row, 4, last_updated)
            
            # Duration
            duration = QTableWidgetItem(f"{item.get('duration_seconds', 0):.2f}")
            self.history_table.setItem(row, 5, duration)
            
            # Create actions button
            actions_cell = QWidget()
            actions_layout = QHBoxLayout(actions_cell)
            actions_layout.setContentsMargins(2, 2, 2, 2)
            
            view_button = QPushButton("View")
            view_button.setProperty('row_id', item.get('id'))
            view_button.clicked.connect(lambda checked, id=item.get('id'): self.view_history_item(id))
            
            refresh_button = QPushButton("Refresh")
            refresh_button.setProperty('row_id', item.get('id'))
            refresh_button.clicked.connect(lambda checked, id=item.get('id'): self.refresh_history_item(id))
            
            actions_layout.addWidget(view_button)
            actions_layout.addWidget(refresh_button)
            
            # Add to table
            self.history_table.setCellWidget(row, 6, actions_cell)
            
        # Auto-adjust column widths
        self.history_table.resizeColumnsToContents()
        
        logger.info(f"Loaded {len(filtered_items)} history entries")
        
    except Exception as e:
        logger.error(f"Error loading history data: {str(e)}")
        QMessageBox.critical(self, "Error", f"Failed to load history data: {str(e)}")

def apply_history_filters(self, history_items=None):
    """Apply filters to history items"""
    if history_items is None:
        # If called by signal from combo box, reload data
        return self.load_history_data()
    
    # Apply date filter
    date_filter = self.date_filter.currentText()
    filtered_by_date = []
    
    now = QDateTime.currentDateTime()
    
    for item in history_items:
        if date_filter == "All Time":
            filtered_by_date.append(item)
        else:
            timestamp = QDateTime.fromString(item.get('timestamp', ''), Qt.DateFormat.ISODate)
            
            if date_filter == "Last 7 Days" and timestamp.daysTo(now) <= 7:
                filtered_by_date.append(item)
            elif date_filter == "Last 30 Days" and timestamp.daysTo(now) <= 30:
                filtered_by_date.append(item)
            # Custom date handling would go here
    
    # Apply status filter
    status_filter = self.status_filter.currentText()
    filtered_by_status = []
    
    for item in filtered_by_date:
        if status_filter == "All Statuses":
            filtered_by_status.append(item)
        else:
            if item.get('status') == status_filter:
                filtered_by_status.append(item)
    
    return filtered_by_status

def view_history_item(self, item_id):
    """View details for a specific history item"""
    try:
        item = self.history_manager.get_entry_by_id(item_id)
        if not item:
            QMessageBox.warning(self, "Not Found", f"History item {item_id} not found")
            return
            
        # Here you would show a detailed view
        # This could be a new dialog or expanding the table row
        QMessageBox.information(self, "History Item Details", 
                               f"Viewing details for {item.get('folder_path')}\n" + 
                               f"Timestamp: {item.get('timestamp')}\n" +
                               f"Status: {item.get('status')}")
        
    except Exception as e:
        logger.error(f"Error viewing history item: {str(e)}")
        QMessageBox.critical(self, "Error", f"Failed to view history item: {str(e)}")

def refresh_history_item(self, item_id):
    """Refresh a specific pawprint from history"""
    try:
        item = self.history_manager.get_entry_by_id(item_id)
        if not item:
            QMessageBox.warning(self, "Not Found", f"History item {item_id} not found")
            return
            
        # Confirm with user
        reply = QMessageBox.question(self, "Confirm Refresh", 
                                    f"Refresh pawprint for:\n{item.get('folder_path')}?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            # Create refresh task
            folder_path = item.get('folder_path')
            task = self.task_factory.create_refresh_task(folder_path)
            self.task_manager.queue_task(task)
            
            QMessageBox.information(self, "Task Queued", 
                                   f"Refresh task for {folder_path} has been queued")
            
            # Switch to Monitor tab to see progress
            self.tab_widget.setCurrentIndex(3)  # Monitor tab index
        
    except Exception as e:
        logger.error(f"Error refreshing history item: {str(e)}")
        QMessageBox.critical(self, "Error", f"Failed to refresh history item: {str(e)}")

def export_history(self):
    """Export history data to CSV file"""
    try:
        # Ask for save location
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save History CSV", "", "CSV Files (*.csv)"
        )
        
        if not file_path:
            return  # User cancelled
            
        # Ensure the file has .csv extension
        if not file_path.endswith('.csv'):
            file_path += '.csv'
            
        # Get data from table
        row_count = self.history_table.rowCount()
        col_count = self.history_table.columnCount() - 1  # Skip Actions column
        
        # Create CSV content
        csv_content = []
        
        # Add headers
        headers = []
        for col in range(col_count):
            headers.append(self.history_table.horizontalHeaderItem(col).text())
        csv_content.append(','.join(headers))
        
        # Add rows
        for row in range(row_count):
            row_data = []
            for col in range(col_count):
                item = self.history_table.item(row, col)
                if item:
                    # Escape commas in field values
                    value = item.text().replace(',', '","')
                    row_data.append(value)
                else:
                    row_data.append('')
            csv_content.append(','.join(row_data))
        
        # Write to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(csv_content))
            
        QMessageBox.information(self, "Export Complete", 
                              f"History data exported to {file_path}")
        
        logger.info(f"Exported history data to {file_path}")
        
    except Exception as e:
        logger.error(f"Error exporting history: {str(e)}")
        QMessageBox.critical(self, "Error", f"Failed to export history: {str(e)}")

def generate_history_report(self):
    """Generate a markdown report of pawprint history"""
    try:
        # Ask for save location
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save History Report", "", "Markdown Files (*.md)"
        )
        
        if not file_path:
            return  # User cancelled
            
        # Ensure the file has .md extension
        if not file_path.endswith('.md'):
            file_path += '.md'
            
        # Get filtered data
        history_items = self.history_manager.get_all_entries()
        filtered_items = self.apply_history_filters(history_items)
        
        # Generate report content
        report = []
        
        # Add header
        report.append("# Pawprint History Report")
        report.append(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Add filters applied
        report.append("## Filters Applied")
        report.append(f"Date Range: {self.date_filter.currentText()}")
        report.append(f"Status: {self.status_filter.currentText()}")
        report.append("")
        
        # Add summary stats
        changed_count = sum(1 for item in filtered_items if item.get('status') == 'Changed')
        unchanged_count = sum(1 for item in filtered_items if item.get('status') == 'Unchanged')
        error_count = sum(1 for item in filtered_items if item.get('status') == 'Error')
        
        report.append("## Summary Statistics")
        report.append(f"Total Pawprints: {len(filtered_items)}")
        report.append(f"Changed: {changed_count}")
        report.append(f"Unchanged: {unchanged_count}")
        report.append(f"Errors: {error_count}")
        report.append("")
        
        # Add table of items
        report.append("## Pawprint History Items")
        report.append("")
        report.append("| Timestamp | Folder Path | Status | Changes | Last Updated | Duration (s) |")
        report.append("| --------- | ----------- | ------ | ------- | ------------ | ------------ |")
        
        for item in filtered_items:
            # Format the row
            report.append(f"| {item.get('timestamp', 'Unknown')} | " +
                         f"{item.get('folder_path', 'Unknown')} | " +
                         f"{item.get('status', 'Unknown')} | " +
                         f"{item.get('changes_count', 0)} | " +
                         f"{item.get('last_updated', 'Unknown')} | " +
                         f"{item.get('duration_seconds', 0):.2f} |")
        
        # Write to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
            
        QMessageBox.information(self, "Report Generated", 
                              f"History report saved to {file_path}")
        
        logger.info(f"Generated history report at {file_path}")
        
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        QMessageBox.critical(self, "Error", f"Failed to generate report: {str(e)}")
