#!/usr/bin/env python3
"""
Compare Screen for Pawprinting PyQt6 Application - Part 4c-3d-8a: Chart Image Export

Implements the chart image export methods for the Compare Screen.

Author: AIMF LLC
Date: June 6, 2025
"""

import os
import logging
from datetime import datetime

# This file contains methods for exporting chart images that would be included in the CompareScreen class

def export_chart_as_image(self, file_path=None, file_format="png", dpi=300):
    """Export current chart as an image file
    
    Args:
        file_path: Path to save the image file (if None, a default path is generated)
        file_format: Image format (png, pdf, jpg, svg)
        dpi: Resolution for raster formats
        
    Returns:
        str: Path to the saved file or None if failed
    """
    if not hasattr(self, 'chart_figure') or self.chart_figure is None:
        logging.error("No chart figure available to export")
        return None
    
    try:
        # Generate default filename if not provided
        if file_path is None:
            # Get timestamp for filename
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            
            # Get chart type
            chart_type = getattr(self, 'current_chart_type', 'chart')
            
            # Create export directory if it doesn't exist
            export_dir = os.path.join(os.path.expanduser("~"), "Documents", "Pawprinting_Exports", "Charts")
            os.makedirs(export_dir, exist_ok=True)
            
            # Generate filename
            file_path = os.path.join(export_dir, f"{chart_type}_{timestamp}.{file_format}")
        
        # Validate file format
        valid_formats = ['png', 'pdf', 'jpg', 'jpeg', 'svg']
        if file_format.lower() not in valid_formats:
            logging.warning(f"Invalid format '{file_format}'. Using png instead.")
            file_format = 'png'
            
            # Ensure file extension matches format
            if not file_path.lower().endswith(f".{file_format}"):
                file_path = f"{os.path.splitext(file_path)[0]}.{file_format}"
        
        # Save figure
        self.chart_figure.savefig(
            file_path,
            format=file_format.lower(),
            dpi=dpi,
            bbox_inches='tight',
            transparent=False
        )
        
        logging.info(f"Chart exported to {file_path}")
        return file_path
        
    except Exception as e:
        logging.error(f"Failed to export chart: {str(e)}")
        return None

def show_export_image_dialog(self):
    """Show dialog to export chart as image
    
    Returns:
        bool: True if export was successful
    """
    try:
        # Only proceed if we have a chart to export
        if not hasattr(self, 'chart_figure') or self.chart_figure is None:
            logging.warning("No chart available to export")
            self.notification_manager.show_message("No chart available to export")
            return False
        
        from PyQt6.QtWidgets import QFileDialog, QMessageBox
        
        # Set up file dialog
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Export Chart as Image")
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        file_dialog.setNameFilter(
            "PNG Image (*.png);;PDF Document (*.pdf);;JPG Image (*.jpg);;SVG Image (*.svg)"
        )
        file_dialog.setDefaultSuffix("png")
        
        # Set initial directory and filename
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        chart_type = getattr(self, 'current_chart_type', 'chart')
        export_dir = os.path.join(os.path.expanduser("~"), "Documents", "Pawprinting_Exports", "Charts")
        os.makedirs(export_dir, exist_ok=True)
        
        file_dialog.setDirectory(export_dir)
        file_dialog.selectFile(f"{chart_type}_{timestamp}.png")
        
        # Execute dialog
        if file_dialog.exec() != QFileDialog.DialogCode.Accepted:
            return False
        
        # Get selected file path and format
        file_path = file_dialog.selectedFiles()[0]
        selected_filter = file_dialog.selectedNameFilter()
        
        # Determine file format from selected filter
        if "PNG" in selected_filter:
            file_format = "png"
        elif "PDF" in selected_filter:
            file_format = "pdf"
        elif "JPG" in selected_filter:
            file_format = "jpg"
        elif "SVG" in selected_filter:
            file_format = "svg"
        else:
            file_format = os.path.splitext(file_path)[1][1:].lower()
            if not file_format:
                file_format = "png"
        
        # Export the chart
        result_path = self.export_chart_as_image(file_path, file_format)
        
        if result_path:
            self.notification_manager.show_message(f"Chart exported successfully to {result_path}")
            return True
        else:
            QMessageBox.warning(self, "Export Failed", "Failed to export chart image. Check the logs for details.")
            return False
            
    except Exception as e:
        logging.error(f"Error in export chart dialog: {str(e)}")
        return False
