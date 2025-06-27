#!/usr/bin/env python3
"""
Compare Screen Example Application

Example demonstrating how to use the Compare Screen component.

Author: AIMF LLC
Date: June 6, 2025
"""

import sys
import os
import logging
from pathlib import Path

# Add parent directory to path to allow importing modules
parent_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(parent_dir))

# Configure Python import paths
import site
site.addsitedir(str(parent_dir))

from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                           QPushButton, QWidget, QFileDialog, QLabel)
from PyQt6.QtCore import Qt
from screens.compare_screen import CompareScreen

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CompareScreenExample(QMainWindow):
    """Example application demonstrating Compare Screen usage"""
    
    def __init__(self):
        """Initialize the example application"""
        super().__init__()
        self.setWindowTitle("Pawprinting Compare Screen Example")
        self.setMinimumSize(1200, 800)
        
        # Create central widget
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)
        
        # Create header
        header_label = QLabel("Pawprinting Compare Screen")
        header_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #bb86fc;")
        main_layout.addWidget(header_label)
        
        # Create instruction label
        instruction_label = QLabel(
            "This example demonstrates the Compare Screen component of the Pawprinting PyQt6 V2 application.\n"
            "Click 'Load Sample Data' to populate with test data, or use the comparison controls in the screen below."
        )
        instruction_label.setStyleSheet("color: #ddd;")
        main_layout.addWidget(instruction_label)
        
        # Create sample data button
        self.load_sample_button = QPushButton("Load Sample Data")
        self.load_sample_button.setStyleSheet("""
            QPushButton { 
                background-color: #333; 
                color: #bb86fc; 
                border: 1px solid #bb86fc; 
                padding: 8px 16px; 
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #444; }
            QPushButton:pressed { background-color: #555; }
        """)
        self.load_sample_button.clicked.connect(self.load_sample_data)
        main_layout.addWidget(self.load_sample_button)
        
        # Create Compare Screen
        self.compare_screen = CompareScreen()
        main_layout.addWidget(self.compare_screen, 1)
        
        # Apply dark theme
        self.apply_dark_theme()
        
        logger.info("Compare Screen Example initialized")
    
    def apply_dark_theme(self):
        """Apply dark theme styling to the application"""
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #222;
                color: #ddd;
            }
            QLabel {
                color: #ddd;
            }
        """)
    
    def load_sample_data(self):
        """Load sample comparison data"""
        try:
            logger.info("Loading sample comparison data")
            
            # Create sample file groups
            sample_directory = os.path.join(parent_dir, "sample_data")
            os.makedirs(sample_directory, exist_ok=True)
            
            # Create sample file references
            self.compare_screen.file_groups = {
                'Original': [
                    {'filename': 'sample_original.json', 'path': os.path.join(sample_directory, 'sample_original.json')}
                ],
                'Modified': [
                    {'filename': 'sample_modified.json', 'path': os.path.join(sample_directory, 'sample_modified.json')}
                ]
            }
            
            # Create sample diff data
            self.compare_screen.diff_cache = {
                'current_diff': {
                    'added': ['pattern_101', 'pattern_202', 'pattern_303'],
                    'removed': ['pattern_404', 'pattern_505'],
                    'changed': {
                        'pattern_606': {'before': 0.3, 'after': 0.8, 'category': 'Network'},
                        'pattern_707': {'before': 0.7, 'after': 0.2, 'category': 'File System'},
                        'pattern_808': {'before': 0.5, 'after': 0.9, 'category': 'Memory'},
                        'pattern_909': {'before': 0.4, 'after': 0.6, 'category': 'Process'},
                        'pattern_010': {'before': 0.8, 'after': 0.3, 'category': 'Registry'}
                    },
                    'unchanged': ['pattern_111', 'pattern_222']
                }
            }
            
            # Create sample top findings
            self.compare_screen.top_findings = {
                'improvements': [
                    'Network pattern 606 improved significantly (+0.5)',
                    'Memory pattern 808 shows better behavior (+0.4)'
                ],
                'regressions': [
                    'Registry pattern 010 shows concerning regression (-0.5)',
                    'File System pattern 707 has regressed (-0.5)'
                ],
                'neutral': [
                    'Process pattern 909 shows minor changes'
                ]
            }
            
            # Extract chart data
            self.compare_screen.extract_chart_data()
            
            # Update UI
            if hasattr(self.compare_screen, 'charts_tab'):
                self.compare_screen.display_chart("radar")
            
            # Show a success message
            logger.info("Sample data loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading sample data: {str(e)}")

def main():
    """Main entry point for the example application"""
    app = QApplication(sys.argv)
    window = CompareScreenExample()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
