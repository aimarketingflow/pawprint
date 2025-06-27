#!/usr/bin/env python3
"""
Fractal Settings Main Panel for Pawprinting PyQt6 V2

Main container for fractal butterfly settings that loads and organizes
the visualization and generation subcomponents.

Author: AIMF LLC
Date: June 20, 2025
"""

import os
import sys
import json
import logging
from typing import Dict, Any, List

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QPushButton, QLabel, QScrollArea
)

from utils.state_manager import StateManager

# Import subcomponents
from screens.settings_components.settings_fractal_visualization import FractalVisualizationSettings
from screens.settings_components.settings_fractal_generation import FractalGenerationSettings

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.settings.fractal.main")

class FractalSettingsPanel(QWidget):
    """Main container for fractal settings that combines visualization and generation settings"""
    
    # Signal when settings are modified
    settings_modified = pyqtSignal()
    
    def __init__(self, parent=None):
        """Initialize fractal settings panel with subcomponents"""
        super().__init__(parent)
        self.parent_screen = parent
        self.state_manager = StateManager.get_instance()
        
        # Setup UI
        self.setup_ui()
        
        logger.debug("Fractal settings main panel initialized")
    
    def setup_ui(self):
        """Set up the fractal settings UI with subcomponents"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Header
        header_label = QLabel("FractalButterfly Settings")
        header_label.setStyleSheet("font-size: 14pt; font-weight: bold;")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header_label)
        
        # Description
        description = QLabel(
            "Configure how the FractalButterfly visualizations look and behave. "
            "These settings affect both the generation algorithms and the visual display."
        )
        description.setWordWrap(True)
        description.setStyleSheet("font-size: 10pt;")
        main_layout.addWidget(description)
        
        # Add visualization settings subcomponent
        self.viz_settings = FractalVisualizationSettings(self)
        self.viz_settings.settings_modified.connect(self.on_subcomponent_modified)
        main_layout.addWidget(self.viz_settings)
        
        # Add generation settings subcomponent
        self.gen_settings = FractalGenerationSettings(self)
        self.gen_settings.settings_modified.connect(self.on_subcomponent_modified)
        main_layout.addWidget(self.gen_settings)
        
        # Add a stretch at the end to push everything up
        main_layout.addStretch(1)
    
    def on_subcomponent_modified(self):
        """Forward modification signal from subcomponents"""
        self.mark_as_modified()
    
    def mark_as_modified(self):
        """Mark settings as modified"""
        if self.parent_screen:
            self.parent_screen.mark_as_modified()
        self.settings_modified.emit()
    
    def save_settings(self) -> Dict[str, Any]:
        """Save settings from all subcomponents"""
        # Collect settings from subcomponents
        viz_settings = self.viz_settings.save_settings()
        gen_settings = self.gen_settings.save_settings()
        
        # This method returns the combined settings, but each subcomponent
        # has already saved its settings to the state_manager
        logger.info("All fractal settings saved")
        return {
            "visualization": viz_settings,
            "generation": gen_settings
        }
    
    def restore_defaults(self):
        """Restore defaults in all subcomponents"""
        self.viz_settings.restore_defaults()
        self.gen_settings.restore_defaults()
        self.mark_as_modified()
        logger.info("All fractal settings restored to defaults")
