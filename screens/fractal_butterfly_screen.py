#!/usr/bin/env python3
"""
Fractal Butterfly Screen for Pawprinting PyQt6 Application

Screen for generating and analyzing fractal butterfly patterns.

Author: AIMF LLC
Date: June 2, 2025
"""

import os
import sys
import logging
from datetime import datetime
from typing import Optional, Dict, Any, List, Tuple

from PyQt6.QtCore import Qt, QSize, pyqtSignal, pyqtSlot, QTimer
from PyQt6.QtGui import QIcon, QPixmap, QFont, QColor
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, 
    QGridLayout, QFormLayout, QLineEdit, QFileDialog, QGroupBox,
    QProgressBar, QCheckBox, QComboBox, QFrame, QScrollArea, 
    QRadioButton, QButtonGroup, QSpacerItem, QSizePolicy, QTextEdit,
    QApplication, QTabWidget, QSplitter, QFileDialog
)

# Import utility modules
from utils.notification_manager import NotificationManager
from utils.state_manager import StateManager
from utils.theme_manager import ThemeManager
from utils.file_manager import FileManager
from utils.progress_tracker import ProgressTracker
from components.console_widget import ConsoleWidget

# Import fractal butterfly modules
from fractal_butterfly.fractal_generator import FractalGenerator
from fractal_butterfly.metrics_calculator import MetricsCalculator
from fractal_butterfly.fractal_renderer import FractalRenderer
from fractal_butterfly.export_manager import ExportManager
from fractal_butterfly.pawprint_adapter import PawprintAdapter
from fractal_butterfly.parameter_widget import ParameterWidget
from fractal_butterfly.visualization_widget import VisualizationWidget
from fractal_butterfly.metrics_widget import MetricsWidget
from fractal_butterfly.text_input_widget import TextInputWidget
from fractal_butterfly.text_to_fractal import TextToFractalConverter

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.fractal_butterfly")

class FractalButterflyScreen(QWidget):
    """
    Screen for generating and analyzing fractal butterfly patterns
    """
    def __init__(self, parent=None):
        """Initialize fractal butterfly screen"""
        super().__init__(parent)
        self.main_window = parent
        self.state_manager = StateManager.get_instance()
        self.theme_manager = ThemeManager.get_instance()
        self.file_manager = FileManager(self)
        self.progress_tracker = ProgressTracker(self)
        
        # Initialize fractal butterfly components
        self.fractal_generator = FractalGenerator()
        self.metrics_calculator = MetricsCalculator()
        self.fractal_renderer = FractalRenderer()
        self.export_manager = ExportManager()
        self.pawprint_adapter = PawprintAdapter()
        
        # State variables
        self.current_pawprint_path = ""
        self.current_fractal_data = None
        self.current_metrics = None
        self.current_base_fractal = None
        self.last_export_directory = ""
        self.is_generating = False
        
        # Set up UI
        self.setup_ui()
        
        # Connect signals
        self.connect_signals()
        
        logger.info("Fractal Butterfly screen initialized")
    
    def setup_ui(self):
        """Set up the fractal butterfly screen UI components"""
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)  # Reduced margins from 20 to 10
        layout.setSpacing(10)  # Reduced spacing from 20 to 10
        
        # Title
        title_label = QLabel("Fractal Butterfly Analysis", self)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")  # Reduced font size from 24px to 20px
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # File selection
        file_group = QGroupBox("Pawprint File", self)
        file_layout = QHBoxLayout(file_group)
        file_layout.setContentsMargins(5, 5, 5, 5)  # Reduced internal margins
        
        self.file_input = QLineEdit(self)
        self.file_input.setReadOnly(True)
        self.file_input.setPlaceholderText("Select pawprint file...")
        file_layout.addWidget(self.file_input)
        
        self.browse_button = QPushButton("Browse", self)
        self.browse_button.clicked.connect(self.on_browse_clicked)
        file_layout.addWidget(self.browse_button)
        
        layout.addWidget(file_group)
        
        # Main content area - splitter for adjustable panels
        splitter = QSplitter(Qt.Orientation.Horizontal, self)
        
        # Left panel - controls
        left_panel = QWidget(self)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create a scroll area for controls
        control_scroll = QScrollArea(self)
        control_scroll.setWidgetResizable(True)
        control_scroll.setFrameShape(QFrame.Shape.NoFrame)
        control_scroll.setMinimumWidth(250)  # Set minimum width
        control_scroll.setMaximumWidth(300)  # Set maximum width
        
        # Create a container widget for the scroll area
        control_container = QWidget(control_scroll)
        control_layout = QVBoxLayout(control_container)
        control_layout.setContentsMargins(0, 0, 0, 0)
        control_layout.setSpacing(5)  # Reduced spacing
        
        # Add text input widget
        self.text_input_widget = TextInputWidget(self)
        control_layout.addWidget(self.text_input_widget)
        
        # Add parameter widget
        self.parameter_widget = ParameterWidget(self)
        control_layout.addWidget(self.parameter_widget)
        
        # Add metrics widget
        self.metrics_widget = MetricsWidget(self)
        control_layout.addWidget(self.metrics_widget)
        
        # Add generation button with fixed height
        self.generate_button = QPushButton("Generate Fractal Butterfly", self)
        self.generate_button.clicked.connect(self.on_generate_clicked)
        self.generate_button.setEnabled(False)
        self.generate_button.setMinimumHeight(32)  # Reduced height from 40 to 32
        control_layout.addWidget(self.generate_button)
        
        # Add export options
        export_group = QGroupBox("Export Options", self)
        export_layout = QVBoxLayout(export_group)
        export_layout.setContentsMargins(5, 5, 5, 5)  # Reduced internal margins
        export_layout.setSpacing(5)  # Reduced spacing
        
        # Export buttons
        export_image_button = QPushButton("Export Image", self)
        export_image_button.clicked.connect(self.on_export_image_clicked)
        export_layout.addWidget(export_image_button)
        
        export_data_button = QPushButton("Export Data", self)
        export_data_button.clicked.connect(self.on_export_data_clicked)
        export_layout.addWidget(export_data_button)
        
        export_report_button = QPushButton("Export Report", self)
        export_report_button.clicked.connect(self.on_export_report_clicked)
        export_layout.addWidget(export_report_button)
        
        control_layout.addWidget(export_group)
        
        # Add stretch to prevent widgets from expanding too much
        control_layout.addStretch(1)
        
        # Set the container widget for the scroll area
        control_scroll.setWidget(control_container)
        
        # Add the scroll area to the left panel
        left_layout.addWidget(control_scroll)
        
        # Right panel - visualization
        right_panel = QWidget(self)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add visualization widget
        self.viz_widget = VisualizationWidget(self)
        self.viz_widget.setMinimumHeight(350)  # Set minimum height for visualization
        right_layout.addWidget(self.viz_widget)
        
        # Add progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        self.progress_bar.setMaximumHeight(10)  # Reduced height
        right_layout.addWidget(self.progress_bar)
        
        # Add status label
        self.status_label = QLabel("Ready", self)
        right_layout.addWidget(self.status_label)
        
        # Add panels to splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        
        # Set initial sizes
        splitter.setSizes([300, 700])
        
        layout.addWidget(splitter)
        
        # Add console
        self.console = ConsoleWidget(self)
        self.console.setMaximumHeight(120)  # Reduced height from 150 to 120
        layout.addWidget(self.console)
        
        # Button section
        button_layout = QHBoxLayout()
        
        self.back_button = QPushButton("Back", self)
        self.back_button.clicked.connect(self.on_back_clicked)
        button_layout.addWidget(self.back_button)
        
        layout.addLayout(button_layout)
    
    def connect_signals(self):
        """Connect signals to slots"""
        # Connect progress tracker signals
        self.progress_tracker.progress_updated.connect(self.on_progress_updated)
        self.progress_tracker.operation_completed.connect(self.on_operation_completed)
        
        # Connect parameter widget signals
        self.parameter_widget.parameters_changed.connect(self.on_parameters_changed)
        
        # Connect text input widget signals
        self.text_input_widget.parametersGenerated.connect(self.on_text_parameters_generated)
    
    def on_browse_clicked(self):
        """Handle browse button click"""
        # Show custom dialog with default pawprint option
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Select Pawprint Source")
        msg_box.setText("Would you like to use your own pawprint file or the default demo pawprint?")
        browse_button = msg_box.addButton("Browse for File", QMessageBox.ActionRole)
        default_button = msg_box.addButton("Use Default Pawprint", QMessageBox.ActionRole)
        cancel_button = msg_box.addButton(QMessageBox.Cancel)
        
        msg_box.exec_()
        
        clicked_button = msg_box.clickedButton()
        
        if clicked_button == browse_button:
            # User wants to browse for their own file
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Select Pawprint File",
                os.path.expanduser("~"),
                "Pawprint Files (*.json);;All Files (*.*)"
            )
            
            if file_path:
                # Update UI
                self.file_input.setText(file_path)
                self.file_input.setStyleSheet("")
                
                # Load the pawprint file
                self.load_pawprint_file(file_path)
                
                # Log selection
                logger.info(f"Selected pawprint file: {file_path}")
                NotificationManager.show_info(f"Selected file: {os.path.basename(file_path)}")
                
        elif clicked_button == default_button:
            # User wants to use the default pawprint
            default_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "fractal_butterfly", "default_pawprint.json"
            )
            
            if os.path.exists(default_path):
                # Update UI to indicate this is a demo file
                self.file_input.setStyleSheet("background-color: #E6F7FF; font-style: italic;")
                self.file_input.setText(f"DEMO: {os.path.basename(default_path)}")
                
                # Load the default pawprint file
                self.load_pawprint_file(default_path)
                
                # Inform user
                self.console.info("Loaded default AIMF LLC demo pawprint")
                self.console.info("This pawprint is designed for demonstration purposes")
                NotificationManager.info(
                    "Demo Pawprint Loaded", 
                    "Using AIMF LLC demo pawprint. Generate text parameters to create a visualization."
                )
            else:
                self.console.error(f"Default pawprint file not found at {default_path}")
                QMessageBox.warning(
                    self,
                    "Default File Missing",
                    f"The default pawprint file could not be found at:\n{default_path}"
                )
    
    def load_pawprint_file(self, file_path):
        """
        Load a pawprint file
        
        Args:
            file_path: Path to pawprint file
        """
        try:
            self.console.info(f"Loading pawprint file: {file_path}")
            self.status_label.setText(f"Loading {os.path.basename(file_path)}...")
            
            # Load the file using the adapter
            pawprint_data = self.pawprint_adapter.load_pawprint_file(file_path)
            
            if not pawprint_data:
                raise ValueError("Failed to load pawprint file")
            
            # Extract parameters for fractal generation
            params = self.pawprint_adapter.extract_parameters_from_pawprint(pawprint_data)
            
            # Update parameter widget
            self.parameter_widget.set_parameters(params)
            
            # Enable generate button
            self.generate_button.setEnabled(True)
            
            # Log success
            self.console.info(f"Pawprint file loaded successfully: {file_path}")
            self.status_label.setText("Ready - Click 'Generate Fractal Butterfly' to visualize")
            
        except Exception as e:
            logger.error(f"Error loading pawprint file: {e}")
            self.console.error(f"Error loading file: {e}")
            NotificationManager.show_error(f"Error loading file: {e}")
            self.status_label.setText("Error loading file")
    
    def on_generate_clicked(self):
        """Handle generate button click"""
        if not self.current_pawprint_path:
            NotificationManager.show_error("Please select a pawprint file first")
            return
        
        if self.is_generating:
            NotificationManager.show_info("Generation already in progress")
            return
        
        # Start generation
        self.start_fractal_generation()
    
    def start_fractal_generation(self):
        """Start fractal butterfly generation"""
        # Update UI
        self.is_generating = True
        self.generate_button.setEnabled(False)
        self.browse_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        
        # Get parameters from parameter widget
        params = self.parameter_widget.params
        
        # Update status
        self.status_label.setText("Generating fractal butterfly...")
        
        # Start progress tracker
        self.progress_tracker.start(100, "Fractal Butterfly Generation")
        
        # Log start
        self.console.info("Starting fractal butterfly generation...")
        self.console.info(f"Parameters: {params}")
        
        # Run generation in a timer to keep UI responsive
        QTimer.singleShot(100, lambda: self.run_fractal_generation(params))
    
    def run_fractal_generation(self, params):
        """
        Run fractal generation with parameters
        
        Args:
            params: Dictionary of parameters
        """
        try:
            # Update progress
            self.progress_tracker.update(10, "Initializing fractal generation...")
            
            # Check if we have text-generated parameters
            if hasattr(self, 'text_generated_params') and self.text_generated_params:
                self.console.info("Using text-generated parameters for fractal generation")
                
                # Merge text-generated parameters with current UI parameters
                # Text parameters take precedence for certain values
                merged_params = params.copy()
                for key in ['fractal_dimension', 'wing_ratio', 'symmetry', 'density', 
                            'base_fractal_pattern', 'base_fractal_influence', 'color_scheme']:
                    if key in self.text_generated_params:
                        merged_params[key] = self.text_generated_params[key]
                        self.console.info(f"Using text-generated {key}: {merged_params[key]}")
                
                # Always use base fractal with text parameters
                merged_params['use_base_fractal'] = True
                
                # Set merged parameters
                self.fractal_generator.set_parameters(merged_params)
                params = merged_params
            else:
                # Set parameters without text influence
                self.fractal_generator.set_parameters(params)
                self.console.info("Using standard parameters (no text influence)")
            
            # Check if we're using a base fractal
            base_fractal = None
            if params.get("use_base_fractal", False):
                self.progress_tracker.update(15, f"Generating base fractal: {params['base_fractal_pattern']}...")
                # Get the base fractal pattern
                base_pattern = params["base_fractal_pattern"]
                resolution = params["resolution"]
                # Generate the base fractal directly
                base_fractal = self.fractal_generator._get_base_fractal(base_pattern, resolution)
            
            # Generate fractal data
            self.progress_tracker.update(20, "Generating fractal data...")
            fractal_data, colors = self.fractal_generator.generate_butterfly()
            
            # Calculate metrics
            self.progress_tracker.update(70, "Calculating metrics...")
            metrics = self.metrics_calculator.calculate_all_metrics(fractal_data)
            
            # Add base fractal info to metrics if used
            if params.get("use_base_fractal", False):
                metrics["using_base_fractal"] = True
                metrics["base_pattern"] = params["base_fractal_pattern"]
                metrics["base_influence"] = params["base_fractal_influence"]
            
            # Store results
            self.current_fractal_data = fractal_data
            self.current_metrics = metrics
            self.current_base_fractal = base_fractal
            
            # Configure renderer options
            title = f"Fractal Butterfly Pattern - Dimension {params['fractal_dimension']:.2f}"
            
            # Add text source info to title if text parameters were used
            if hasattr(self, 'text_generated_params') and self.text_generated_params:
                # Get a preview of the text (first 30 chars)
                text_preview = self.text_generated_params.get('text_input', '')
                if len(text_preview) > 30:
                    text_preview = text_preview[:27] + '...'
                title += f" (Text-Influenced: {text_preview})"
            
            renderer_options = {
                "show_base_pattern": params.get("use_base_fractal", False) and base_fractal is not None,
                "title": title
            }
            self.fractal_renderer.set_options(renderer_options)
            
            # Display results
            self.progress_tracker.update(90, "Rendering visualization...")
            if base_fractal is not None and params.get("use_base_fractal", False):
                # Render with base fractal comparison
                fig = self.fractal_renderer.render_fractal(
                    fractal_data, colors, metrics=metrics, base_fractal=base_fractal
                )
                self.viz_widget.render_from_figure(fig)
            else:
                # Standard rendering
                self.viz_widget.render_fractal(fractal_data, colors, metrics)
            
            # Display metrics
            self.metrics_widget.display_metrics(metrics)
            
            # Add text influence information to metrics if used
            if hasattr(self, 'text_generated_params') and self.text_generated_params:
                metrics['text_influenced'] = True
                metrics['text_preview'] = self.text_generated_params.get('text_input', '')[:50] + '...' if len(self.text_generated_params.get('text_input', '')) > 50 else self.text_generated_params.get('text_input', '')
                metrics['text_entropy'] = self.text_generated_params.get('text_entropy', 0.0)
                
                # Log success with text influence
                self.console.info(f"Fractal generated with text influence: Entropy={metrics['text_entropy']:.4f}")
            
            # Complete operation
            self.progress_tracker.complete(True, "Fractal butterfly generation completed successfully")
            
            # Add AIMF LLC branding to visualization
            self.viz_widget.add_watermark("AIMF LLC - Pawprinting Visualization")
            
        except Exception as e:
            # Handle error
            logger.error(f"Error generating fractal butterfly: {e}")
            self.console.error(f"Error generating fractal butterfly: {e}")
            self.progress_tracker.complete(False, f"Error: {e}")
            
            # Show detailed error notification
            NotificationManager.error(
                "Fractal Generation Error", 
                f"Error: {e}\n\nTry adjusting parameters or reloading the pawprint file."
            )
            
            # Save error state for potential recovery
            self.last_error = {
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'params': params.copy() if params else {}
            }
            
            # Create an automatic recovery point
            recovery_file = os.path.join(os.path.expanduser("~"), "Documents", "FolderHackingAnalysis", 
                                        "Pawprinting_PyQt6", "recovery", f"fractal_recovery_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(recovery_file), exist_ok=True)
            
            try:
                with open(recovery_file, 'w') as f:
                    # Save what we can recover from
                    recovery_data = {
                        'timestamp': datetime.now().isoformat(),
                        'parameters': params,
                        'pawprint_file': self.current_pawprint_path,
                        'error': str(e)
                    }
                    
                    # Include text parameters if available
                    if hasattr(self, 'text_generated_params') and self.text_generated_params:
                        recovery_data['text_parameters'] = self.text_generated_params
                    
                    json.dump(recovery_data, f, indent=2)
                    self.console.info(f"Recovery point saved to {recovery_file}")
            except Exception as save_error:
                logger.error(f"Error saving recovery data: {save_error}")
                
        finally:
            # Reset UI
            self.is_generating = False
            self.progress_bar.setVisible(False)
            self.browse_button.setEnabled(True)
            self.generate_button.setEnabled(True)
            
            # Reset button style to normal if there was an error
            if not hasattr(self, 'current_fractal_data') or self.current_fractal_data is None:
                self.generate_button.setStyleSheet("")
            
            # Inform user of completion
            self.status_label.setText("Ready")
            
            # Allow auto-retry with a convenient button if there was an error
            if hasattr(self, 'last_error'):
                retry_button = QPushButton("Retry Generation", self)
                retry_button.clicked.connect(self.retry_last_generation)
                retry_button.setStyleSheet("background-color: #FFA500; color: white; font-weight: bold;")
                
                # Add to layout temporarily
                if hasattr(self, 'retry_button') and self.retry_button is not None:
                    # Remove old retry button if it exists
                    self.control_layout.removeWidget(self.retry_button)
                    self.retry_button.deleteLater()
                
                self.control_layout.addWidget(retry_button)
                self.retry_button = retry_button
    
    def retry_last_generation(self):
        """
        Retry the last failed fractal generation with the same parameters
        """
        if not hasattr(self, 'last_error') or not self.last_error:
            self.console.warning("No previous error found to retry from")
            return
            
        self.console.info("Retrying last generation with the same parameters")
        
        # Get parameters from the last error
        params = self.last_error.get('params', {})
        if not params:
            self.console.error("No parameters found in last error")
            return
            
        # Clear the error state
        delattr(self, 'last_error')
        
        # Remove the retry button
        if hasattr(self, 'retry_button') and self.retry_button is not None:
            self.control_layout.removeWidget(self.retry_button)
            self.retry_button.deleteLater()
            self.retry_button = None
            
        # Start the generation process again
        self.start_fractal_generation()
    
    def on_parameters_changed(self, params):
        """
        Handle parameter changes
        
        Args:
            params: Dictionary of parameters
        """
        # Update local parameters
        logger.debug(f"Parameters changed: {params}")
        
        # If we have a file selected, enable generate button
        if self.file_input.text():
            self.generate_button.setEnabled(True)
    
    def on_text_parameters_generated(self, params):
        """
        Handle parameters generated from text input
        
        Args:
            params: Dictionary of parameters generated from text
        """
        logger.info(f"Text-generated parameters received: {params}")
        
        # Store text-generated parameters (important for fractal generation)
        self.text_generated_params = params.copy()
        
        # Update parameter widget with text-generated parameters
        self.parameter_widget.set_parameters(params)
        
        # Update console with detailed information
        self.console.info(f"Generated parameters from text input: {len(params.get('text_input', ''))} characters")
        self.console.info(f"Fractal dimension: {params.get('fractal_dimension', 1.5)}")
        self.console.info(f"Base fractal pattern: {params.get('base_fractal_pattern', 'unknown')}")
        self.console.info(f"Text entropy: {params.get('text_entropy', 0.0)}")
        
        # If we have a file selected, enable generate button and highlight it
        if self.file_input.text():
            self.generate_button.setEnabled(True)
            self.generate_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
            self.console.info("Ready to generate fractal! Click 'Generate Fractal Butterfly' button.")
        else:
            self.console.info("Please select a pawprint file to generate the fractal.")
            
        # Provide user feedback
        NotificationManager.success(
            "Text Parameters Generated", 
            f"Base fractal pattern: {params.get('base_fractal_pattern', 'unknown').capitalize()}\nClick 'Generate Fractal Butterfly' to visualize"
        )
    
    def on_export_image_clicked(self):
        """Handle export image button click"""
        if self.current_fractal_data is None:
            NotificationManager.show_error("No fractal data to export")
            return
        
        # Get default export directory
        export_dir = self.state_manager.get_value("last_session.last_export_directory", "")
        if not export_dir and self.current_pawprint_path:
            export_dir = os.path.dirname(self.current_pawprint_path)
        
        # Generate default filename
        default_name = "fractal_butterfly.png"
        if self.current_pawprint_path:
            base_name = os.path.splitext(os.path.basename(self.current_pawprint_path))[0]
            default_name = f"{base_name}_fractal.png"
        
        default_path = os.path.join(export_dir, default_name) if export_dir else default_name
        
        # Use QFileDialog directly for better handling of file selection
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Fractal Butterfly Image",
            default_path,
            "PNG Images (*.png);;JPEG Images (*.jpg);;All Files (*)"
        )
        
        if file_path:
            # Update state with selected directory
            self.last_export_directory = os.path.dirname(file_path)
            self.state_manager.set_value("last_session.last_export_directory", self.last_export_directory)
            
            # Export image
            if self.viz_widget.save_figure(file_path, dpi=300):
                self.console.info(f"Exported image to: {file_path}")
                NotificationManager.show_success(f"Image exported to: {file_path}")
                
                # Ask if user wants to open the exported file
                confirm = NotificationManager.show_dialog(
                    "Export Complete",
                    f"Image exported to {file_path}. Do you want to open this file?",
                    "question"
                )
                
                if confirm:
                    # Open the file with the default application
                    if sys.platform == "win32":
                        os.startfile(file_path)
                    elif sys.platform == "darwin":  # macOS
                        os.system(f"open \"{file_path}\"")
                    else:  # Linux
                        os.system(f"xdg-open \"{file_path}\"")
            else:
                NotificationManager.show_error(f"Failed to export image")
    
    def on_export_data_clicked(self):
        """Handle export data button click"""
        if self.current_fractal_data is None or self.current_metrics is None:
            NotificationManager.show_error("No fractal data to export")
            return
        
        # Get default export directory
        export_dir = self.state_manager.get_value("last_session.last_export_directory", "")
        if not export_dir and self.current_pawprint_path:
            export_dir = os.path.dirname(self.current_pawprint_path)
        
        # Generate default filename
        default_name = "fractal_butterfly_data.json"
        if self.current_pawprint_path:
            base_name = os.path.splitext(os.path.basename(self.current_pawprint_path))[0]
            default_name = f"{base_name}_fractal_data.json"
        
        default_path = os.path.join(export_dir, default_name) if export_dir else default_name
        
        # Use QFileDialog directly for better handling of file selection
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Fractal Butterfly Data",
            default_path,
            "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            # Update state with selected directory
            self.last_export_directory = os.path.dirname(file_path)
            self.state_manager.set_value("last_session.last_export_directory", self.last_export_directory)
            
            # Export data
            if self.export_manager.export_data(
                self.current_fractal_data,
                self.current_metrics,
                self.parameter_widget.params,
                file_path
            ):
                self.console.info(f"Exported data to: {file_path}")
                NotificationManager.show_success(f"Data exported to: {file_path}")
            else:
                NotificationManager.show_error(f"Failed to export data")
    
    def on_export_report_clicked(self):
        """Handle export report button click"""
        if self.current_fractal_data is None or self.current_metrics is None:
            NotificationManager.show_error("No fractal data to export")
            return
        
        # Get default export directory
        export_dir = self.state_manager.get_value("last_session.last_export_directory", "")
        if not export_dir and self.current_pawprint_path:
            export_dir = os.path.dirname(self.current_pawprint_path)
        
        # Generate default filename
        default_name = "fractal_butterfly_report.html"
        if self.current_pawprint_path:
            base_name = os.path.splitext(os.path.basename(self.current_pawprint_path))[0]
            default_name = f"{base_name}_fractal_report.html"
        
        default_path = os.path.join(export_dir, default_name) if export_dir else default_name
        
        # Use QFileDialog directly for better handling of file selection
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Fractal Butterfly Report",
            default_path,
            "HTML Files (*.html);;All Files (*)"
        )
        
        if not file_path:
            return
        
        # Update state with selected directory
        self.last_export_directory = os.path.dirname(file_path)
        self.state_manager.set_value("last_session.last_export_directory", self.last_export_directory)
        
        # Export image first
        image_filename = os.path.splitext(os.path.basename(file_path))[0] + ".png"
        image_path = os.path.join(os.path.dirname(file_path), image_filename)
        
        if self.viz_widget.save_figure(image_path, dpi=300):
            # Export HTML report
            if self.export_manager.export_report(
                self.current_fractal_data,
                self.current_metrics,
                self.parameter_widget.params,
                image_path,
                file_path
            ):
                self.console.info(f"Exported report to: {file_path}")
                NotificationManager.show_success(f"Report exported to: {file_path}")
                
                # Ask if user wants to open the exported file
                confirm = NotificationManager.show_dialog(
                    "Export Complete",
                    f"Report exported to {file_path}. Do you want to open this file?",
                    "question"
                )
                
                if confirm:
                    # Open the file with the default application
                    if sys.platform == "win32":
                        os.startfile(file_path)
                    elif sys.platform == "darwin":  # macOS
                        os.system(f"open \"{file_path}\"")
                    else:  # Linux
                        os.system(f"xdg-open \"{file_path}\"")
            else:
                NotificationManager.show_error(f"Failed to export report")
        else:
            NotificationManager.show_error(f"Failed to export image for report")
    
    def on_back_clicked(self):
        """Handle back button click"""
        if self.is_generating:
            # Ask for confirmation if currently generating
            confirm = NotificationManager.show_dialog(
                "Cancel Generation",
                "Fractal generation is in progress. Are you sure you want to cancel and go back?",
                "question"
            )
            
            if not confirm:
                return
        
        # Go back to dashboard
        if hasattr(self.main_window, "show_dashboard_screen") and callable(self.main_window.show_dashboard_screen):
            self.main_window.show_dashboard_screen()
    
    def on_progress_updated(self, percentage, message):
        """
        Handle progress updates from the progress tracker
        
        Args:
            percentage: Progress percentage (0-100)
            message: Status message
        """
        self.progress_bar.setValue(percentage)
        self.status_label.setText(message)
    
    def on_operation_completed(self, success, message):
        """
        Handle operation completion from the progress tracker
        
        Args:
            success: Whether the operation was successful
            message: Completion message
        """
        # Update UI
        self.is_generating = False
        self.generate_button.setEnabled(True)
        self.browse_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        # Update status
        self.status_label.setText(message)
        
        # Show notification
        if success:
            NotificationManager.show_success("Fractal butterfly generated successfully")
            self.console.info("Fractal butterfly generated successfully")
        else:
            NotificationManager.show_error("Error during generation: " + message)
            self.console.error("Error during generation: " + message)
    
    def load_file(self, file_path):
        """
        Public method to load a file from external call
        
        Args:
            file_path: Path to pawprint file to load
        """
        if file_path and os.path.exists(file_path):
            self.current_pawprint_path = file_path
            self.file_input.setText(file_path)
            self.load_pawprint_file(file_path)
            return True
        return False
