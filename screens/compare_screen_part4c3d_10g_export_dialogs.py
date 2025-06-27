#!/usr/bin/env python3
"""
Compare Screen - Part 4c-3d-10g: Export Dialog Handlers

Implements the export dialog pop-ups and export action handlers.

Author: AIMF LLC
Date: June 6, 2025
"""

import os
import logging
from datetime import datetime
from PyQt6.QtWidgets import QFileDialog, QMessageBox

def show_export_image_dialog(self):
    """Show dialog to export current chart as image"""
    try:
        if not hasattr(self, 'current_chart_type') or not hasattr(self, 'chart_figure'):
            QMessageBox.warning(self, "Export Error", "No chart available to export.")
            return
            
        # Create file dialog
        formats = "PNG (*.png);;PDF (*.pdf);;JPG (*.jpg);;SVG (*.svg)"
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        default_dir = os.path.join(os.path.expanduser("~"), "Documents", "Pawprinting_Exports", "Images")
        os.makedirs(default_dir, exist_ok=True)
        default_name = f"{self.current_chart_type}_chart_{timestamp}.png"
        
        file_path, selected_filter = QFileDialog.getSaveFileName(
            self, "Export Chart Image", 
            os.path.join(default_dir, default_name),
            formats
        )
        
        if file_path:
            # Call the appropriate export method based on the chart type
            if self.current_chart_type == "radar":
                self.export_radar_chart_image(file_path)
            elif self.current_chart_type == "bar":
                self.export_bar_chart_image(file_path)
            elif self.current_chart_type == "line":
                self.export_line_chart_image(file_path)
            elif self.current_chart_type == "pie":
                self.export_pie_chart_image(file_path)
            elif self.current_chart_type == "heatmap":
                self.export_heatmap_chart_image(file_path)
                
            QMessageBox.information(self, "Export Complete", f"Chart exported to {file_path}")
            
    except Exception as e:
        logging.error(f"Error showing export image dialog: {str(e)}")
        QMessageBox.critical(self, "Export Error", f"Failed to export chart: {str(e)}")
