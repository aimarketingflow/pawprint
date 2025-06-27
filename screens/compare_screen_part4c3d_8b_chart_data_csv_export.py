#!/usr/bin/env python3
"""
Compare Screen for Pawprinting PyQt6 Application - Part 4c-3d-8b: Chart Data CSV Export

Implements the chart data CSV export methods for the Compare Screen.

Author: AIMF LLC
Date: June 6, 2025
"""

import os
import csv
import logging
from datetime import datetime

# This file contains methods for exporting chart data as CSV that would be included in the CompareScreen class

def export_chart_data_as_csv(self, file_path=None):
    """Export current chart data as a CSV file
    
    Args:
        file_path: Path to save the CSV file (if None, a default path is generated)
        
    Returns:
        str: Path to the saved file or None if failed
    """
    if not hasattr(self, 'current_chart_data') or not self.current_chart_data:
        logging.error("No chart data available to export")
        return None
    
    try:
        # Get current chart data
        chart_data = self.current_chart_data
        chart_type = getattr(self, 'current_chart_type', 'unknown')
        
        # Generate default filename if not provided
        if file_path is None:
            # Get timestamp for filename
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            
            # Create export directory if it doesn't exist
            export_dir = os.path.join(os.path.expanduser("~"), "Documents", "Pawprinting_Exports", "Data")
            os.makedirs(export_dir, exist_ok=True)
            
            # Generate filename
            file_path = os.path.join(export_dir, f"{chart_type}_data_{timestamp}.csv")
        
        # Format data based on chart type
        csv_data = self._format_chart_data_for_csv(chart_data, chart_type)
        
        # Write to CSV
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(csv_data)
        
        logging.info(f"Chart data exported to {file_path}")
        return file_path
        
    except Exception as e:
        logging.error(f"Failed to export chart data as CSV: {str(e)}")
        return None

def _format_chart_data_for_csv(self, chart_data, chart_type):
    """Format chart data for CSV export based on chart type
    
    Args:
        chart_data: Chart data dictionary
        chart_type: Type of chart
        
    Returns:
        list: List of rows for CSV export
    """
    csv_data = []
    
    # Add metadata header
    csv_data.append(["Pawprinting Chart Data Export"])
    csv_data.append([f"Chart Type: {chart_type.capitalize()}"])
    csv_data.append([f"Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"])
    csv_data.append([])  # Empty row as separator
    
    # Format based on chart type
    if chart_type == "radar":
        return self._format_radar_data_for_csv(csv_data, chart_data)
    elif chart_type == "bar":
        return self._format_bar_data_for_csv(csv_data, chart_data)
    elif chart_type == "line":
        return self._format_line_data_for_csv(csv_data, chart_data)
    elif chart_type == "pie":
        return self._format_pie_data_for_csv(csv_data, chart_data)
    elif chart_type == "heatmap":
        return self._format_heatmap_data_for_csv(csv_data, chart_data)
    else:
        # Generic format for unknown chart types
        return self._format_generic_data_for_csv(csv_data, chart_data)

def _format_radar_data_for_csv(self, csv_data, chart_data):
    """Format radar chart data for CSV export
    
    Args:
        csv_data: Initial CSV data with metadata
        chart_data: Radar chart data dictionary
        
    Returns:
        list: List of rows for CSV export
    """
    # Extract radar chart data
    categories = chart_data.get("categories", [])
    before_values = chart_data.get("before_values", [])
    after_values = chart_data.get("after_values", [])
    
    # Add header row
    csv_data.append(["Category", "Before Value", "After Value", "Change"])
    
    # Add data rows
    for i, category in enumerate(categories):
        if i < len(before_values) and i < len(after_values):
            before_val = before_values[i]
            after_val = after_values[i]
            change = after_val - before_val
            csv_data.append([category, before_val, after_val, change])
    
    return csv_data

def _format_bar_data_for_csv(self, csv_data, chart_data):
    """Format bar chart data for CSV export
    
    Args:
        csv_data: Initial CSV data with metadata
        chart_data: Bar chart data dictionary
        
    Returns:
        list: List of rows for CSV export
    """
    # Extract bar chart data
    patterns = chart_data.get("patterns", [])
    changes = chart_data.get("changes", [])
    categories = chart_data.get("categories", [])
    before_values = chart_data.get("before_values", [])
    after_values = chart_data.get("after_values", [])
    
    # Add header row
    csv_data.append(["Pattern", "Category", "Before Value", "After Value", "Change"])
    
    # Add data rows
    for i, pattern in enumerate(patterns):
        if i < len(changes) and i < len(categories):
            category = categories[i]
            
            # Get before/after values if available
            before_val = before_values[i] if i < len(before_values) else None
            after_val = after_values[i] if i < len(after_values) else None
            change = changes[i]
            
            csv_data.append([pattern, category, before_val, after_val, change])
    
    return csv_data

def _format_line_data_for_csv(self, csv_data, chart_data):
    """Format line chart data for CSV export
    
    Args:
        csv_data: Initial CSV data with metadata
        chart_data: Line chart data dictionary
        
    Returns:
        list: List of rows for CSV export
    """
    # Extract line chart data
    x_values = chart_data.get("x_values", [])
    y_values = chart_data.get("y_values", [])
    series_names = chart_data.get("series_names", [])
    
    if not series_names and y_values:
        # Default series name if not provided
        series_names = ["Series 1"]
    
    # Add header row with x-axis label and series names
    header = ["X Value"]
    for name in series_names:
        header.append(name)
    csv_data.append(header)
    
    # Add data rows
    if len(series_names) == 1:
        # Single series
        for i, x in enumerate(x_values):
            if i < len(y_values):
                csv_data.append([x, y_values[i]])
    else:
        # Multiple series
        for i, x in enumerate(x_values):
            row = [x]
            for series_idx, _ in enumerate(series_names):
                if series_idx < len(y_values) and i < len(y_values[series_idx]):
                    row.append(y_values[series_idx][i])
                else:
                    row.append("")
            csv_data.append(row)
    
    return csv_data

def _format_pie_data_for_csv(self, csv_data, chart_data):
    """Format pie chart data for CSV export
    
    Args:
        csv_data: Initial CSV data with metadata
        chart_data: Pie chart data dictionary
        
    Returns:
        list: List of rows for CSV export
    """
    # Determine which data set to use
    if chart_data.get("chart_mode", "change_distribution") == "change_distribution":
        # Use change distribution data
        labels = chart_data.get("labels", [])
        values = chart_data.get("values", [])
    else:
        # Use category distribution data
        labels = chart_data.get("category_labels", [])
        values = chart_data.get("category_values", [])
    
    # Add header row
    csv_data.append(["Label", "Value", "Percentage"])
    
    # Calculate total for percentages
    total = sum(values) if values else 0
    
    # Add data rows
    for i, label in enumerate(labels):
        if i < len(values):
            value = values[i]
            percentage = (value / total) * 100 if total > 0 else 0
            csv_data.append([label, value, f"{percentage:.1f}%"])
    
    # Add total row
    csv_data.append(["Total", total, "100.0%"])
    
    return csv_data

def _format_heatmap_data_for_csv(self, csv_data, chart_data):
    """Format heatmap chart data for CSV export
    
    Args:
        csv_data: Initial CSV data with metadata
        chart_data: Heatmap chart data dictionary
        
    Returns:
        list: List of rows for CSV export
    """
    # Determine which data set to use
    if chart_data.get("chart_mode", "category_changes") == "category_changes":
        # Use category-change distribution data
        x_labels = chart_data.get("x_labels", [])
        y_labels = chart_data.get("y_labels", [])
        z_values = chart_data.get("z_values", [])
    else:
        # Use origin-category distribution data
        x_labels = chart_data.get("alt_x_labels", [])
        y_labels = chart_data.get("alt_y_labels", [])
        z_values = chart_data.get("alt_z_values", [])
    
    # Add header row with x-axis labels
    header = [""]  # Empty cell for y-axis label column
    header.extend(x_labels)
    csv_data.append(header)
    
    # Add data rows with y-axis labels
    for i, y_label in enumerate(y_labels):
        if i < len(z_values):
            row = [y_label]  # Y-axis label
            
            # Add z-values for this row
            for j in range(len(x_labels)):
                if j < len(z_values[i]):
                    row.append(z_values[i][j])
                else:
                    row.append("")
                    
            csv_data.append(row)
    
    return csv_data

def _format_generic_data_for_csv(self, csv_data, chart_data):
    """Format generic chart data for CSV export
    
    Args:
        csv_data: Initial CSV data with metadata
        chart_data: Chart data dictionary
        
    Returns:
        list: List of rows for CSV export
    """
    # Extract basic pattern data
    patterns = chart_data.get("patterns", [])
    changes = chart_data.get("changes", [])
    categories = chart_data.get("categories", [])
    
    # Add header row
    csv_data.append(["Pattern", "Category", "Change"])
    
    # Add data rows
    for i, pattern in enumerate(patterns):
        if i < len(changes):
            category = categories[i] if i < len(categories) else ""
            change = changes[i]
            csv_data.append([pattern, category, change])
    
    return csv_data

def show_export_csv_dialog(self):
    """Show dialog to export chart data as CSV
    
    Returns:
        bool: True if export was successful
    """
    try:
        # Only proceed if we have chart data to export
        if not hasattr(self, 'current_chart_data') or not self.current_chart_data:
            logging.warning("No chart data available to export")
            self.notification_manager.show_message("No chart data available to export")
            return False
        
        from PyQt6.QtWidgets import QFileDialog, QMessageBox
        
        # Set up file dialog
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Export Chart Data as CSV")
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        file_dialog.setNameFilter("CSV Files (*.csv)")
        file_dialog.setDefaultSuffix("csv")
        
        # Set initial directory and filename
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        chart_type = getattr(self, 'current_chart_type', 'chart')
        export_dir = os.path.join(os.path.expanduser("~"), "Documents", "Pawprinting_Exports", "Data")
        os.makedirs(export_dir, exist_ok=True)
        
        file_dialog.setDirectory(export_dir)
        file_dialog.selectFile(f"{chart_type}_data_{timestamp}.csv")
        
        # Execute dialog
        if file_dialog.exec() != QFileDialog.DialogCode.Accepted:
            return False
        
        # Get selected file path
        file_path = file_dialog.selectedFiles()[0]
        
        # Export the chart data
        result_path = self.export_chart_data_as_csv(file_path)
        
        if result_path:
            self.notification_manager.show_message(f"Chart data exported successfully to {result_path}")
            return True
        else:
            QMessageBox.warning(self, "Export Failed", "Failed to export chart data. Check the logs for details.")
            return False
            
    except Exception as e:
        logging.error(f"Error in export chart data dialog: {str(e)}")
        return False
