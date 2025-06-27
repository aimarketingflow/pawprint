#!/usr/bin/env python3
"""
Compare Screen - Save Chart Image

Saves the current chart as an image file.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
import os
from datetime import datetime
from PyQt6.QtWidgets import QFileDialog, QMessageBox

logger = logging.getLogger(__name__)

def save_chart_image(self):
    """Save current chart as an image file
    
    Returns:
        bool: Success status
    """
    try:
        # Check if matplotlib is available
        if not self.MATPLOTLIB_AVAILABLE or not hasattr(self, 'chart_figure'):
            logger.warning("Cannot save chart - matplotlib not available or no chart drawn")
            self.show_error_dialog("Chart Not Available", 
                                  "There is no chart available to save.")
            return False
            
        # Generate default filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        chart_type = self.chart_selector.currentText() if hasattr(self, 'chart_selector') else "chart"
        default_filename = f"pawprinting_{chart_type.lower().replace(' ', '_')}_{timestamp}.png"
        
        # Get user's Documents folder as default location
        default_dir = os.path.join(os.path.expanduser("~"), "Documents", "Pawprinting_Exports", "images")
        os.makedirs(default_dir, exist_ok=True)
        
        # Open file dialog for save location
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Chart Image",
            os.path.join(default_dir, default_filename),
            "PNG Images (*.png);;All Files (*)"
        )
        
        if not file_path:
            logger.debug("Chart image save cancelled by user")
            return False
            
        # Save chart as image
        self.chart_figure.savefig(
            file_path, 
            format='png', 
            dpi=300, 
            bbox_inches='tight',
            facecolor=self.chart_figure.get_facecolor()
        )
        
        logger.info(f"Chart image saved to {file_path}")
        
        # Show success notification
        msg = QMessageBox(self)
        msg.setWindowTitle("Image Saved")
        msg.setText("Chart image saved successfully!")
        msg.setInformativeText(f"The image has been saved to:\n{file_path}")
        msg.setIcon(QMessageBox.Icon.Information)
        
        # Apply dark theme styling
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #121212;
                color: #ffffff;
            }
            QPushButton {
                background-color: #bb86fc;
                color: #000000;
                padding: 5px 15px;
                border-radius: 4px;
            }
        """)
        
        msg.exec()
        return True
    except Exception as e:
        logger.error(f"Error saving chart image: {str(e)}")
        self.show_error_dialog("Save Error", f"Failed to save chart image: {str(e)}")
        return False
