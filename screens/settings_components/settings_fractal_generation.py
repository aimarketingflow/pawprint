#!/usr/bin/env python3
"""
Fractal Generation Settings Component for Pawprinting PyQt6 V2

Manages settings related to fractal pattern generation algorithms,
complexity, seed values, and other generation parameters.

Author: AIMF LLC
Date: June 20, 2025
"""

import os
import sys
import json
import logging
import random
from typing import Dict, Any, List

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QComboBox, QSlider, QCheckBox, QGroupBox,
    QPushButton, QSpinBox, QDoubleSpinBox, QLineEdit
)

from utils.state_manager import StateManager

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.settings.fractal.generation")

class FractalGenerationSettings(QWidget):
    """Settings panel for fractal generation options"""
    
    # Signal when settings are modified
    settings_modified = pyqtSignal()
    
    def __init__(self, parent=None):
        """Initialize fractal generation settings panel"""
        super().__init__(parent)
        self.parent_widget = parent
        self.state_manager = StateManager.get_instance()
        
        # Load current settings
        self.current_settings = self.state_manager.get_settings().get("fractal", {}).get("generation", {})
        if not self.current_settings:
            self.current_settings = self.get_default_settings()
        
        # Setup UI
        self.setup_ui()
        
        # Load settings into UI
        self.load_settings()
        
        logger.debug("Fractal generation settings panel initialized")
    
    def setup_ui(self):
        """Set up the fractal generation settings UI"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(15)
        
        # Algorithm Settings group
        self.algorithm_group = QGroupBox("Generation Algorithm")
        algorithm_layout = QFormLayout(self.algorithm_group)
        algorithm_layout.setContentsMargins(15, 15, 15, 15)
        algorithm_layout.setSpacing(10)
        
        # Algorithm type
        self.algorithm_type = QComboBox()
        self.algorithm_type.addItem("Julia Set (Default)", "julia")
        self.algorithm_type.addItem("Mandelbrot", "mandelbrot")
        self.algorithm_type.addItem("IFS (Iterated Function System)", "ifs")
        self.algorithm_type.addItem("L-System", "lsystem")
        self.algorithm_type.addItem("Pawprint-Derived", "pawprint")
        self.algorithm_type.currentIndexChanged.connect(self.on_setting_changed)
        algorithm_layout.addRow("Algorithm type:", self.algorithm_type)
        
        # Iteration depth
        iteration_layout = QHBoxLayout()
        self.iteration_depth = QSpinBox()
        self.iteration_depth.setRange(10, 5000)
        self.iteration_depth.setSingleStep(10)
        self.iteration_depth.valueChanged.connect(self.on_setting_changed)
        
        iteration_layout.addWidget(self.iteration_depth)
        iteration_layout.addStretch(1)
        algorithm_layout.addRow("Iteration depth:", iteration_layout)
        
        # Complexity Settings group
        self.complexity_group = QGroupBox("Complexity Settings")
        complexity_layout = QVBoxLayout(self.complexity_group)
        complexity_layout.setContentsMargins(15, 15, 15, 15)
        complexity_layout.setSpacing(15)
        
        # Complexity level
        complexity_slider_layout = QVBoxLayout()
        complexity_label = QLabel("Complexity level:")
        self.complexity_level = QSlider(Qt.Orientation.Horizontal)
        self.complexity_level.setRange(1, 10)
        self.complexity_level.setSingleStep(1)
        self.complexity_level.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.complexity_level.setTickInterval(1)
        self.complexity_level.valueChanged.connect(self.on_complexity_changed)
        
        self.complexity_value_label = QLabel("5 (Medium)")
        self.complexity_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        complexity_slider_layout.addWidget(complexity_label)
        complexity_slider_layout.addWidget(self.complexity_level)
        complexity_slider_layout.addWidget(self.complexity_value_label)
        complexity_layout.addLayout(complexity_slider_layout)
        
        # Detail level
        detail_slider_layout = QVBoxLayout()
        detail_label = QLabel("Detail level:")
        self.detail_level = QSlider(Qt.Orientation.Horizontal)
        self.detail_level.setRange(1, 10)
        self.detail_level.setSingleStep(1)
        self.detail_level.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.detail_level.setTickInterval(1)
        self.detail_level.valueChanged.connect(self.on_detail_changed)
        
        self.detail_value_label = QLabel("5 (Medium)")
        self.detail_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        detail_slider_layout.addWidget(detail_label)
        detail_slider_layout.addWidget(self.detail_level)
        detail_slider_layout.addWidget(self.detail_value_label)
        complexity_layout.addLayout(detail_slider_layout)
        
        # Seeds group
        self.seeds_group = QGroupBox("Generation Seeds")
        seeds_layout = QFormLayout(self.seeds_group)
        seeds_layout.setContentsMargins(15, 15, 15, 15)
        seeds_layout.setSpacing(10)
        
        # Use random seed
        self.use_random_seed = QCheckBox("Use random seed")
        self.use_random_seed.stateChanged.connect(self.on_random_seed_toggled)
        seeds_layout.addRow("", self.use_random_seed)
        
        # Seed value
        seed_layout = QHBoxLayout()
        self.seed_value = QSpinBox()
        self.seed_value.setRange(0, 999999999)
        self.seed_value.valueChanged.connect(self.on_setting_changed)
        
        self.randomize_btn = QPushButton("Randomize")
        self.randomize_btn.clicked.connect(self.randomize_seed)
        
        seed_layout.addWidget(self.seed_value)
        seed_layout.addWidget(self.randomize_btn)
        seeds_layout.addRow("Seed value:", seed_layout)
        
        # Pattern source checkbox
        self.derive_from_pawprint = QCheckBox("Derive patterns from pawprint data")
        self.derive_from_pawprint.stateChanged.connect(self.on_setting_changed)
        seeds_layout.addRow("", self.derive_from_pawprint)
        
        # Advanced Options group
        self.advanced_group = QGroupBox("Advanced Options")
        advanced_layout = QFormLayout(self.advanced_group)
        advanced_layout.setContentsMargins(15, 15, 15, 15)
        advanced_layout.setSpacing(10)
        
        # Algorithm-specific parameter 1 (example for complex number in Julia set)
        param1_layout = QHBoxLayout()
        self.param1 = QDoubleSpinBox()
        self.param1.setRange(-2.0, 2.0)
        self.param1.setSingleStep(0.01)
        self.param1.setDecimals(3)
        self.param1.valueChanged.connect(self.on_setting_changed)
        param1_layout.addWidget(self.param1)
        advanced_layout.addRow("Complex parameter real:", param1_layout)
        
        # Algorithm-specific parameter 2
        param2_layout = QHBoxLayout()
        self.param2 = QDoubleSpinBox()
        self.param2.setRange(-2.0, 2.0)
        self.param2.setSingleStep(0.01)
        self.param2.setDecimals(3)
        self.param2.valueChanged.connect(self.on_setting_changed)
        param2_layout.addWidget(self.param2)
        advanced_layout.addRow("Complex parameter imag:", param2_layout)
        
        # Pattern Preference
        self.pattern_preference = QComboBox()
        self.pattern_preference.addItem("Balanced (Default)", "balanced")
        self.pattern_preference.addItem("Organic", "organic")
        self.pattern_preference.addItem("Geometric", "geometric")
        self.pattern_preference.addItem("Abstract", "abstract")
        self.pattern_preference.currentIndexChanged.connect(self.on_setting_changed)
        advanced_layout.addRow("Pattern preference:", self.pattern_preference)
        
        # Add all groups to main layout
        main_layout.addWidget(self.algorithm_group)
        main_layout.addWidget(self.complexity_group)
        main_layout.addWidget(self.seeds_group)
        main_layout.addWidget(self.advanced_group)
    
    def on_complexity_changed(self, value):
        """Update complexity value label and notify about setting change"""
        if value <= 3:
            label = f"{value} (Low)"
        elif value <= 7:
            label = f"{value} (Medium)"
        else:
            label = f"{value} (High)"
        
        self.complexity_value_label.setText(label)
        self.on_setting_changed()
    
    def on_detail_changed(self, value):
        """Update detail value label and notify about setting change"""
        if value <= 3:
            label = f"{value} (Low)"
        elif value <= 7:
            label = f"{value} (Medium)"
        else:
            label = f"{value} (High)"
        
        self.detail_value_label.setText(label)
        self.on_setting_changed()
    
    def on_random_seed_toggled(self, state):
        """Handle random seed checkbox toggle"""
        use_random = state == Qt.CheckState.Checked.value
        self.seed_value.setEnabled(not use_random)
        self.randomize_btn.setEnabled(not use_random)
        self.on_setting_changed()
    
    def randomize_seed(self):
        """Generate a random seed value"""
        new_seed = random.randint(0, 999999999)
        self.seed_value.setValue(new_seed)
        logger.debug(f"Generated new random seed: {new_seed}")
    
    def on_setting_changed(self):
        """Handle when any setting is changed"""
        if self.parent_widget:
            self.parent_widget.mark_as_modified()
        self.settings_modified.emit()
    
    def load_settings(self):
        """Load current settings into UI components"""
        # Algorithm settings
        algorithm = self.current_settings.get("algorithm_type", "julia")
        index = self.algorithm_type.findData(algorithm)
        if index >= 0:
            self.algorithm_type.setCurrentIndex(index)
        
        self.iteration_depth.setValue(self.current_settings.get("iteration_depth", 100))
        
        # Complexity settings
        self.complexity_level.setValue(self.current_settings.get("complexity_level", 5))
        self.on_complexity_changed(self.complexity_level.value())
        
        self.detail_level.setValue(self.current_settings.get("detail_level", 5))
        self.on_detail_changed(self.detail_level.value())
        
        # Seeds
        use_random = self.current_settings.get("use_random_seed", False)
        self.use_random_seed.setChecked(use_random)
        self.seed_value.setEnabled(not use_random)
        self.randomize_btn.setEnabled(not use_random)
        self.seed_value.setValue(self.current_settings.get("seed_value", 42))
        
        self.derive_from_pawprint.setChecked(self.current_settings.get("derive_from_pawprint", True))
        
        # Advanced options
        self.param1.setValue(self.current_settings.get("param1", -0.7))
        self.param2.setValue(self.current_settings.get("param2", 0.27))
        
        preference = self.current_settings.get("pattern_preference", "balanced")
        index = self.pattern_preference.findData(preference)
        if index >= 0:
            self.pattern_preference.setCurrentIndex(index)
    
    def get_default_settings(self) -> Dict[str, Any]:
        """Get default fractal generation settings"""
        return {
            "algorithm_type": "julia",
            "iteration_depth": 100,
            "complexity_level": 5,
            "detail_level": 5,
            "use_random_seed": False,
            "seed_value": 42,
            "derive_from_pawprint": True,
            "param1": -0.7,
            "param2": 0.27,
            "pattern_preference": "balanced"
        }
    
    def save_settings(self) -> Dict[str, Any]:
        """Save current settings to state manager"""
        settings = {
            "algorithm_type": self.algorithm_type.currentData(),
            "iteration_depth": self.iteration_depth.value(),
            "complexity_level": self.complexity_level.value(),
            "detail_level": self.detail_level.value(),
            "use_random_seed": self.use_random_seed.isChecked(),
            "seed_value": self.seed_value.value(),
            "derive_from_pawprint": self.derive_from_pawprint.isChecked(),
            "param1": self.param1.value(),
            "param2": self.param2.value(),
            "pattern_preference": self.pattern_preference.currentData()
        }
        
        # Save to state manager under fractal.generation
        fractal_settings = self.state_manager.get_settings().get("fractal", {})
        fractal_settings["generation"] = settings
        self.state_manager.update_settings("fractal", fractal_settings)
        
        logger.info("Fractal generation settings saved")
        
        return settings
    
    def restore_defaults(self):
        """Restore default settings"""
        self.current_settings = self.get_default_settings()
        self.load_settings()
        self.on_setting_changed()
