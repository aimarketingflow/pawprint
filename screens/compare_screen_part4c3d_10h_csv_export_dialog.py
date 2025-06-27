#!/usr/bin/env python3
"""
Compare Screen - Part 4c-3d-10h: CSV Export Dialog Handler

Implements the CSV export dialog and data export actions.

Author: AIMF LLC
Date: June 6, 2025
"""

import os
import logging
from datetime import datetime
from PyQt6.QtWidgets import QFileDialog, QMessageBox

def show_export_csv_dialog(self):
    """Show dialog to export current chart data as CSV"""
    try:
        if not hasattr(self, 'current_chart_type') or not hasattr(self, 'current_chart_data'):
            QMessageBox.warning(self, "Export Error", "No chart data available to export.")
            return
            
        # Create file dialog
        formats = "CSV Files (*.csv)"
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        default_dir = os.path.join(os.path.expanduser("~"), "Documents", "Pawprinting_Exports", "Data")
        os.makedirs(default_dir, exist_ok=True)
        default_name = f"{self.current_chart_type}_data_{timestamp}.csv"
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Chart Data", 
            os.path.join(default_dir, default_name),
            formats
        )
        
        if file_path:
            # Call the appropriate export method based on the chart type
            if self.current_chart_type == "radar":
                self.export_radar_chart_csv(file_path)
            elif self.current_chart_type == "bar":
                self.export_bar_chart_csv(file_path)
            elif self.current_chart_type == "line":
                self.export_line_chart_csv(file_path)
            elif self.current_chart_type == "pie":
                self.export_pie_chart_csv(file_path)
            elif self.current_chart_type == "heatmap":
                self.export_heatmap_chart_csv(file_path)
                
            QMessageBox.information(self, "Export Complete", f"Chart data exported to {file_path}")
            
    except Exception as e:
        logging.error(f"Error showing export CSV dialog: {str(e)}")
        QMessageBox.critical(self, "Export Error", f"Failed to export chart data: {str(e)}")

def _handle_report_export(self):
    """Handle export of complete comparison report"""
    try:
        # Create file dialog
        formats = "HTML Files (*.html);;Text Files (*.txt)"
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        default_dir = os.path.join(os.path.expanduser("~"), "Documents", "Pawprinting_Exports", "Reports")
        os.makedirs(default_dir, exist_ok=True)
        default_name = f"comparison_report_{timestamp}.html"
        
        file_path, selected_filter = QFileDialog.getSaveFileName(
            self, "Export Comparison Report", 
            os.path.join(default_dir, default_name),
            formats
        )
        
        if file_path:
            if selected_filter == "HTML Files (*.html)":
                result = self.export_html_report(file_path)
            else:
                result = self.export_comparison_summary(file_path)
                
            if result:
                QMessageBox.information(self, "Export Complete", f"Report exported to {file_path}")
            else:
                QMessageBox.warning(self, "Export Warning", "Report may not have exported correctly.")
                
    except Exception as e:
        logging.error(f"Error exporting report: {str(e)}")
        QMessageBox.critical(self, "Export Error", f"Failed to export report: {str(e)}")
