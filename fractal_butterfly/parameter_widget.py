#!/usr/bin/env python3
"""
Parameter Widget Module

UI widget for controlling fractal butterfly parameters.

Author: AIMF LLC
Date: June 2, 2025
"""

import logging
from typing import Dict, Any, Callable

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, 
    QSlider, QComboBox, QDoubleSpinBox, QSpinBox, QPushButton,
    QGroupBox, QCheckBox, QSizePolicy
)

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.fractal_butterfly.param_widget")

class ParameterWidget(QWidget):
    """
    Widget for controlling fractal butterfly parameters
    """
    
    # Signal emitted when parameters change
    parameters_changed = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        """Initialize the parameter widget"""
        super().__init__(parent)
        
        # Default parameters
        self.params = {
            "fractal_dimension": 1.5,
            "iterations": 500,
            "resolution": (800, 800),
            "wing_ratio": 2.0,
            "symmetry": 0.9,
            "density": 0.5,
            "color_scheme": "rainbow",
            "use_base_fractal": False,
            "base_fractal_influence": 0.5,
            "base_fractal_pattern": "mandelbrot"
        }
        
        # Available color schemes
        self.color_schemes = [
            "rainbow", "bluescale", "heatmap", "grayscale", "cosmic"
        ]
        
        # Available base fractal patterns
        self.base_fractal_patterns = [
            "mandelbrot", "julia", "burning_ship", "tricorn", "multibrot"
        ]
        
        # Auto-update flag
        self.auto_update = True
        
        # Set size policy
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        
        # Set up UI
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the UI components"""
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create parameter groups
        basic_group = self.create_basic_params_group()
        advanced_group = self.create_advanced_params_group()
        display_group = self.create_display_params_group()
        base_group = self.create_base_fractal_group()
        
        # Add groups to layout
        layout.addWidget(basic_group)
        layout.addWidget(advanced_group)
        layout.addWidget(display_group)
        layout.addWidget(base_group)
        
        # Add buttons
        button_layout = QHBoxLayout()
        
        # Reset button
        reset_button = QPushButton("Reset Parameters", self)
        reset_button.clicked.connect(self.reset_parameters)
        button_layout.addWidget(reset_button)
        
        # Apply button
        self.apply_button = QPushButton("Apply Changes", self)
        self.apply_button.clicked.connect(self.apply_parameters)
        self.apply_button.setEnabled(False)  # Initially disabled until changes are made
        button_layout.addWidget(self.apply_button)
        
        layout.addLayout(button_layout)
        
        # Add auto-update checkbox
        auto_update_check = QCheckBox("Auto-update on parameter change", self)
        auto_update_check.setChecked(self.auto_update)
        auto_update_check.stateChanged.connect(self.on_auto_update_changed)
        layout.addWidget(auto_update_check)
        
        # Add stretch to push everything to the top
        layout.addStretch(1)
    
    def create_basic_params_group(self) -> QGroupBox:
        """Create group for basic parameters"""
        group = QGroupBox("Basic Parameters", self)
        layout = QFormLayout(group)
        layout.setContentsMargins(5, 5, 5, 5)  # Reduced margins
        layout.setVerticalSpacing(3)  # Reduced spacing
        
        # Fractal dimension
        self.dimension_spin = QDoubleSpinBox(self)
        self.dimension_spin.setRange(1.0, 2.0)
        self.dimension_spin.setSingleStep(0.05)
        self.dimension_spin.setValue(self.params["fractal_dimension"])
        self.dimension_spin.setDecimals(2)
        self.dimension_spin.valueChanged.connect(
            lambda v: self.on_parameter_changed("fractal_dimension", v))
        layout.addRow("Fractal Dimension:", self.dimension_spin)
        
        # Wing ratio
        self.wing_ratio_spin = QDoubleSpinBox(self)
        self.wing_ratio_spin.setRange(1.0, 4.0)
        self.wing_ratio_spin.setSingleStep(0.1)
        self.wing_ratio_spin.setValue(self.params["wing_ratio"])
        self.wing_ratio_spin.setDecimals(1)
        self.wing_ratio_spin.valueChanged.connect(
            lambda v: self.on_parameter_changed("wing_ratio", v))
        layout.addRow("Wing Ratio:", self.wing_ratio_spin)
        
        # Symmetry
        self.symmetry_spin = QDoubleSpinBox(self)
        self.symmetry_spin.setRange(0.0, 1.0)
        self.symmetry_spin.setSingleStep(0.05)
        self.symmetry_spin.setValue(self.params["symmetry"])
        self.symmetry_spin.setDecimals(2)
        self.symmetry_spin.valueChanged.connect(
            lambda v: self.on_parameter_changed("symmetry", v))
        layout.addRow("Symmetry:", self.symmetry_spin)
        
        # Density
        self.density_spin = QDoubleSpinBox(self)
        self.density_spin.setRange(0.0, 1.0)
        self.density_spin.setSingleStep(0.05)
        self.density_spin.setValue(self.params["density"])
        self.density_spin.setDecimals(2)
        self.density_spin.valueChanged.connect(
            lambda v: self.on_parameter_changed("density", v))
        layout.addRow("Density:", self.density_spin)
        
        return group
    
    def create_advanced_params_group(self) -> QGroupBox:
        """Create group for advanced parameters"""
        group = QGroupBox("Advanced Parameters", self)
        layout = QFormLayout(group)
        layout.setContentsMargins(5, 5, 5, 5)  # Reduced margins
        layout.setVerticalSpacing(3)  # Reduced spacing
        
        # Iterations
        self.iterations_spin = QSpinBox(self)
        self.iterations_spin.setRange(100, 2000)
        self.iterations_spin.setSingleStep(50)
        self.iterations_spin.setValue(self.params["iterations"])
        self.iterations_spin.valueChanged.connect(
            lambda v: self.on_parameter_changed("iterations", v))
        layout.addRow("Iterations:", self.iterations_spin)
        
        # Resolution width
        self.width_spin = QSpinBox(self)
        self.width_spin.setRange(200, 2000)
        self.width_spin.setSingleStep(100)
        self.width_spin.setValue(self.params["resolution"][0])
        self.width_spin.valueChanged.connect(self.on_resolution_changed)
        layout.addRow("Width:", self.width_spin)
        
        # Resolution height
        self.height_spin = QSpinBox(self)
        self.height_spin.setRange(200, 2000)
        self.height_spin.setSingleStep(100)
        self.height_spin.setValue(self.params["resolution"][1])
        self.height_spin.valueChanged.connect(self.on_resolution_changed)
        layout.addRow("Height:", self.height_spin)
        
        return group
    
    def create_display_params_group(self) -> QGroupBox:
        """Create group for display parameters"""
        group = QGroupBox("Display Parameters", self)
        layout = QFormLayout(group)
        layout.setContentsMargins(5, 5, 5, 5)  # Reduced margins
        layout.setVerticalSpacing(3)  # Reduced spacing
        
        # Color scheme
        self.color_combo = QComboBox(self)
        for scheme in self.color_schemes:
            self.color_combo.addItem(scheme.capitalize())
        self.color_combo.setCurrentText(self.params["color_scheme"].capitalize())
        self.color_combo.currentTextChanged.connect(self.on_color_scheme_changed)
        layout.addRow("Color Scheme:", self.color_combo)
        
        return group
    
    def create_base_fractal_group(self) -> QGroupBox:
        """Create group for base fractal parameters"""
        group = QGroupBox("Base Fractal", self)
        layout = QFormLayout(group)
        layout.setContentsMargins(5, 5, 5, 5)  # Reduced margins
        layout.setVerticalSpacing(3)  # Reduced spacing
        
        # Use base fractal
        self.use_base_check = QCheckBox("Use Base Fractal Pattern", self)
        self.use_base_check.setChecked(self.params["use_base_fractal"])
        self.use_base_check.stateChanged.connect(self.on_use_base_changed)
        layout.addRow(self.use_base_check)
        
        # Base fractal pattern
        self.base_pattern_combo = QComboBox(self)
        for pattern in self.base_fractal_patterns:
            self.base_pattern_combo.addItem(pattern.capitalize())
        self.base_pattern_combo.setCurrentText(self.params["base_fractal_pattern"].capitalize())
        self.base_pattern_combo.currentTextChanged.connect(self.on_base_pattern_changed)
        self.base_pattern_combo.setEnabled(self.params["use_base_fractal"])
        layout.addRow("Pattern:", self.base_pattern_combo)
        
        # Base fractal influence
        self.base_influence_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.base_influence_slider.setRange(0, 100)
        self.base_influence_slider.setValue(int(self.params["base_fractal_influence"] * 100))
        self.base_influence_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.base_influence_slider.setTickInterval(10)
        self.base_influence_slider.valueChanged.connect(self.on_base_influence_changed)
        self.base_influence_slider.setEnabled(self.params["use_base_fractal"])
        layout.addRow("Influence:", self.base_influence_slider)
        self.base_influence_label = QLabel(f"{self.params['base_fractal_influence']:.2f}", self)
        layout.addRow("", self.base_influence_label)
        
        return group
    
    def on_parameter_changed(self, param_name: str, value: Any) -> None:
        """
        Handle parameter change
        
        Args:
            param_name: Name of the parameter
            value: New value for the parameter
        """
        # Update parameter
        self.params[param_name] = value
        logger.debug(f"Parameter changed: {param_name} = {value}")
        
        # Enable apply button if not auto-updating
        if not self.auto_update:
            self.apply_button.setEnabled(True)
        else:
            # Emit signal for automatic update
            self.parameters_changed.emit(self.params)
    
    def on_resolution_changed(self) -> None:
        """Handle resolution change"""
        width = self.width_spin.value()
        height = self.height_spin.value()
        self.params["resolution"] = (width, height)
        logger.debug(f"Resolution changed: {width}x{height}")
        
        # Enable apply button if not auto-updating
        if not self.auto_update:
            self.apply_button.setEnabled(True)
        else:
            # Emit signal for automatic update
            self.parameters_changed.emit(self.params)
    
    def on_color_scheme_changed(self, scheme_text: str) -> None:
        """
        Handle color scheme change
        
        Args:
            scheme_text: Name of the color scheme (capitalized)
        """
        # Convert to lowercase for internal use
        scheme = scheme_text.lower()
        self.params["color_scheme"] = scheme
        logger.debug(f"Color scheme changed: {scheme}")
        
        # Enable apply button if not auto-updating
        if not self.auto_update:
            self.apply_button.setEnabled(True)
        else:
            # Emit signal for automatic update
            self.parameters_changed.emit(self.params)
    
    def on_use_base_changed(self, state: int) -> None:
        """
        Handle use base fractal change
        
        Args:
            state: Checkbox state
        """
        use_base = state == Qt.CheckState.Checked.value
        self.params["use_base_fractal"] = use_base
        
        # Enable/disable related controls
        self.base_pattern_combo.setEnabled(use_base)
        self.base_influence_slider.setEnabled(use_base)
        
        if not self.auto_update:
            self.apply_button.setEnabled(True)
        else:
            # Emit signal for automatic update
            self.parameters_changed.emit(self.params)
    
    def on_base_pattern_changed(self, pattern: str) -> None:
        """
        Handle base pattern change
        
        Args:
            pattern: Base pattern name
        """
        # Convert to lowercase for internal use
        self.params["base_fractal_pattern"] = pattern.lower()
        logger.debug(f"Base pattern changed: {pattern}")
        
        if not self.auto_update:
            self.apply_button.setEnabled(True)
        else:
            # Emit signal for automatic update
            self.parameters_changed.emit(self.params)
    
    def on_base_influence_changed(self, value: int) -> None:
        """
        Handle base influence change
        
        Args:
            value: Slider value (0-100)
        """
        influence = value / 100.0
        self.params["base_fractal_influence"] = influence
        self.base_influence_label.setText(f"{influence:.2f}")
        logger.debug(f"Base influence changed: {influence}")
        
        if not self.auto_update:
            self.apply_button.setEnabled(True)
        else:
            # Emit signal for automatic update
            self.parameters_changed.emit(self.params)
    
    def on_auto_update_changed(self, state: int) -> None:
        """
        Handle auto-update checkbox change
        
        Args:
            state: Checkbox state
        """
        self.auto_update = state == Qt.CheckState.Checked.value
        logger.debug(f"Auto-update set to {self.auto_update}")
        
        # Enable/disable apply button
        self.apply_button.setEnabled(not self.auto_update)
    
    def apply_parameters(self) -> None:
        """Apply parameter changes"""
        logger.debug("Applying parameter changes")
        
        # Emit signal with current parameters
        self.parameters_changed.emit(self.params)
        
        # Disable apply button
        self.apply_button.setEnabled(False)
    
    def reset_parameters(self) -> None:
        """Reset parameters to defaults"""
        logger.debug("Resetting parameters to defaults")
        
        # Default parameters
        self.params = {
            "fractal_dimension": 1.5,
            "iterations": 500,
            "resolution": (800, 800),
            "wing_ratio": 2.0,
            "symmetry": 0.9,
            "density": 0.5,
            "color_scheme": "rainbow",
            "use_base_fractal": False,
            "base_fractal_influence": 0.5,
            "base_fractal_pattern": "mandelbrot"
        }
        
        # Update UI
        self.dimension_spin.setValue(self.params["fractal_dimension"])
        self.wing_ratio_spin.setValue(self.params["wing_ratio"])
        self.symmetry_spin.setValue(self.params["symmetry"])
        self.density_spin.setValue(self.params["density"])
        self.iterations_spin.setValue(self.params["iterations"])
        self.width_spin.setValue(self.params["resolution"][0])
        self.height_spin.setValue(self.params["resolution"][1])
        self.color_combo.setCurrentText(self.params["color_scheme"].capitalize())
        self.use_base_check.setChecked(self.params["use_base_fractal"])
        self.base_pattern_combo.setCurrentText(self.params["base_fractal_pattern"].capitalize())
        self.base_pattern_combo.setEnabled(self.params["use_base_fractal"])
        self.base_influence_slider.setValue(int(self.params["base_fractal_influence"] * 100))
        self.base_influence_slider.setEnabled(self.params["use_base_fractal"])
        self.base_influence_label.setText(f"{self.params['base_fractal_influence']:.2f}")
        
        # Emit signal with reset parameters
        self.parameters_changed.emit(self.params)
        
        # Disable apply button
        self.apply_button.setEnabled(False)
    
    def set_parameters(self, params: Dict[str, Any]) -> None:
        """
        Set parameters from external source
        
        Args:
            params: Dictionary of parameters
        """
        logger.debug(f"Setting parameters: {params}")
        
        # Update internal parameters
        for key, value in params.items():
            if key in self.params:
                self.params[key] = value
        
        # Update UI without triggering signals
        self.blockSignals(True)
        
        if "fractal_dimension" in params:
            self.dimension_spin.setValue(params["fractal_dimension"])
        
        if "wing_ratio" in params:
            self.wing_ratio_spin.setValue(params["wing_ratio"])
        
        if "symmetry" in params:
            self.symmetry_spin.setValue(params["symmetry"])
        
        if "density" in params:
            self.density_spin.setValue(params["density"])
        
        if "iterations" in params:
            self.iterations_spin.setValue(params["iterations"])
        
        if "resolution" in params:
            self.width_spin.setValue(params["resolution"][0])
            self.height_spin.setValue(params["resolution"][1])
        
        if "color_scheme" in params:
            self.color_combo.setCurrentText(params["color_scheme"].capitalize())
        
        if "use_base_fractal" in params:
            self.use_base_check.setChecked(params["use_base_fractal"])
            self.base_pattern_combo.setEnabled(params["use_base_fractal"])
            self.base_influence_slider.setEnabled(params["use_base_fractal"])
        
        if "base_fractal_pattern" in params:
            self.base_pattern_combo.setCurrentText(params["base_fractal_pattern"].capitalize())
        
        if "base_fractal_influence" in params:
            self.base_influence_slider.setValue(int(params["base_fractal_influence"] * 100))
            self.base_influence_label.setText(f"{params['base_fractal_influence']:.2f}")
        
        self.blockSignals(False)
        
        # Disable apply button
        self.apply_button.setEnabled(False)
