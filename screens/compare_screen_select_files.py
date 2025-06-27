#!/usr/bin/env python3
"""
Compare Screen - Select Files for Comparison

Provides file selection dialog for comparing pawprint files.

Author: AIMF LLC
Date: June 6, 2025
"""

import os
import logging
from PyQt6.QtWidgets import QFileDialog, QMessageBox

logger = logging.getLogger(__name__)

def select_files_for_comparison(self):
    """
    Display a file dialog to select multiple pawprint files for comparison.
    
    Returns:
        list: List of selected file paths, or empty list if canceled
    """
    try:
        # Get the last directory that was used
        last_dir = self.state_manager.get_state("last_directory", os.path.expanduser("~/Documents"))
        
        options = QFileDialog.Option.ReadOnly
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Select Pawprint Files for Comparison")
        file_dialog.setDirectory(last_dir)
        file_dialog.setNameFilter("Pawprint Files (*.json *.pawprint);;All Files (*)")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)
        file_dialog.setOption(QFileDialog.Option.DontUseNativeDialog, False)  # Use native dialog on macOS
        
        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            selected_files = file_dialog.selectedFiles()
            
            # Save the last directory used
            if selected_files:
                last_dir = os.path.dirname(selected_files[0])
                self.state_manager.set_state("last_directory", last_dir)
            
            # Basic validation
            if len(selected_files) < 2:
                logger.warning("At least two files must be selected for comparison")
                QMessageBox.warning(
                    self, 
                    "File Selection", 
                    "Please select at least two files for comparison.",
                    QMessageBox.StandardButton.Ok
                )
                return []
            
            # Log the selected files
            logger.info(f"Selected {len(selected_files)} files for comparison")
            for file_path in selected_files:
                logger.debug(f"Selected file: {file_path}")
                
            return selected_files
        else:
            logger.info("File selection cancelled by user")
            return []
    except Exception as e:
        logger.error(f"Error selecting files for comparison: {str(e)}")
        QMessageBox.critical(
            self, 
            "Error", 
            f"An error occurred while selecting files: {str(e)}",
            QMessageBox.StandardButton.Ok
        )
        return []
