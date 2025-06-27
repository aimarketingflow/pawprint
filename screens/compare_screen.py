#!/usr/bin/env python3
"""
Compare Screen - Main Class

Integrates all modular components for the Compare Screen.

Author: AIMF LLC
Date: June 6, 2025
"""

import os
import logging
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, 
                           QPushButton, QLabel, QSplitter, QFileDialog)
from PyQt6.QtCore import Qt, pyqtSignal

# Import structure components - base class is already CompareScreen
# Instead of inheritance, we'll use composition
from .compare_screen_part1_structure import CompareScreen as BaseCompareScreen

# Import UI setup components
from .compare_screen_part2_ui_setup import setup_ui_components

# Import comparison tab components
from .compare_screen_part3_comparison_tab import setup_comparison_tab

# Import charts setup components
from .compare_screen_part4a_charts_setup import setup_charts
from .compare_screen_part4b_chart_generation import generate_charts

# Import tab components
from .compare_screen_part4c1_raw_data_tab import setup_raw_data_tab
from .compare_screen_part4c2_summary_tab import setup_summary_tab

# Import data processing components
from .compare_screen_part4c3a_data_loading import load_pawprint_data
from .compare_screen_part4c3b_diff_generation import generate_diff
from .compare_screen_part4c3c_pattern_analysis import analyze_patterns

# Import chart tab integration
from .compare_screen_part4c3d_11_integration import integrate_charts_tab_into_compare_screen

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CompareScreen(QWidget):
    """Main Compare Screen class that integrates all modular components"""
    
    # Define signals
    comparison_completed = pyqtSignal(dict)
    loading_progress = pyqtSignal(int, str)
    
    def __init__(self, parent=None):
        """Initialize the Compare Screen
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        logger.info("Initializing Compare Screen")
        
        # Create main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Set up UI components
        self.setup_ui_components()
        
        # Initialize tabs
        self.tab_widget = QTabWidget(self)
        self.main_layout.addWidget(self.tab_widget)
        
        # Set up comparison tab
        self.setup_comparison_tab()
        
        # Set up summary tab
        self.setup_summary_tab()
        
        # Set up raw data tab
        self.setup_raw_data_tab()
        
        # Initialize charts tab
        self.initialize_charts_tab()
        
        # Initialize default values
        self.file_groups = {}
        self.diff_cache = {}
        self.results_ready = False
        self.current_view = "side_by_side"
        
        # Apply dark theme styling to tab widget
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane { 
                border: 1px solid #555; 
                background-color: #333;
            }
            QTabBar::tab { 
                background-color: #333; 
                color: #ddd;
                padding: 8px 16px;
                border: 1px solid #555;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected { 
                background-color: #424242; 
                color: #bb86fc;
            }
            QTabBar::tab:hover:!selected { 
                background-color: #3a3a3a; 
            }
        """)
        
        logger.info("Compare Screen initialized")
    
    # Include core methods
    setup_ui_components = setup_ui_components
    setup_comparison_tab = setup_comparison_tab
    setup_summary_tab = setup_summary_tab
    setup_raw_data_tab = setup_raw_data_tab
    setup_charts = setup_charts
    generate_charts = generate_charts
    load_pawprint_data = load_pawprint_data
    generate_diff = generate_diff
    analyze_patterns = analyze_patterns
    
    def on_compare_files(self):
        """Handler for compare files button"""
        try:
            logger.info("Starting file comparison")
            
            # Load data
            self.load_pawprint_data()
            
            if not self.file_groups or len(self.file_groups) < 2:
                logger.warning("Not enough files selected for comparison")
                return False
            
            # Generate diff
            self.generate_diff()
            
            # Analyze patterns
            self.analyze_patterns()
            
            # Extract chart data
            self.extract_chart_data()
            
            # Set results ready flag
            self.results_ready = True
            
            # Emit completion signal
            self.comparison_completed.emit(self.diff_cache)
            
            # Update UI to show results
            self.tab_widget.setCurrentIndex(0)  # Switch to summary tab
            
            logger.info("Comparison completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error during comparison: {str(e)}")
            return False

# Integrate charts tab functionality
integrate_charts_tab_into_compare_screen(CompareScreen)
