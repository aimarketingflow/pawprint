#!/usr/bin/env python3
"""
Generate Screen for Pawprinting PyQt6 Application

Screen for generating new pawprints from source data.

Author: AIMF LLC
Date: June 2, 2025
"""

import os
import sys
import logging
from datetime import datetime
from typing import Optional, Dict, Any

from PyQt6.QtCore import Qt, QSize, pyqtSignal, pyqtSlot, QTimer
from PyQt6.QtGui import QIcon, QPixmap, QFont, QColor
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, 
    QGridLayout, QFormLayout, QLineEdit, QFileDialog, QGroupBox,
    QProgressBar, QCheckBox, QComboBox, QFrame, QScrollArea, 
    QRadioButton, QButtonGroup, QSpacerItem, QSizePolicy, QTextEdit,
    QApplication
)

# Import utility modules
from utils.notification_manager import NotificationManager
from utils.state_manager import StateManager
from utils.theme_manager import ThemeManager
from utils.file_manager import FileManager
from utils.progress_tracker import ProgressTracker

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.generate")


class GenerateScreen(QWidget):
    """
    Screen for generating new pawprints from source data
    """
    def __init__(self, parent=None):
        """Initialize generate screen"""
        super().__init__(parent)
        self.main_window = parent
        self.state_manager = StateManager.get_instance()
        self.theme_manager = ThemeManager.get_instance()
        self.file_manager = FileManager(self)
        self.progress_tracker = ProgressTracker(self)
        
        # State variables
        self.source_path = ""
        self.output_path = ""
        self.is_generating = False
        
        # Set up UI
        self.setup_ui()
        
        # Connect signals
        self.connect_signals()
        
        logger.info("Generate screen initialized")
    
    def setup_ui(self):
        """Set up the generate screen UI components"""
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 10, 20, 10)  # Reduced margins
        layout.setSpacing(8)  # Reduced spacing
        
        # Title
        title_label = QLabel("Generate Pawprint", self)
        title_label.setStyleSheet("font-size: 22px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFixedHeight(35)  # Fixed height for title
        layout.addWidget(title_label)
        
        # Source section
        source_group = QGroupBox("Source", self)
        source_layout = QVBoxLayout(source_group)
        source_layout.setContentsMargins(10, 8, 10, 8)  # Reduced margins
        source_layout.setSpacing(6)  # Reduced internal spacing
        
        self.source_input = QLineEdit(self)
        self.source_input.setReadOnly(True)
        self.source_input.setPlaceholderText("Select source folder or file...")
        
        source_button_layout = QHBoxLayout()
        self.browse_folder_button = QPushButton("Browse Folder", self)
        self.browse_folder_button.clicked.connect(self.on_browse_folder_clicked)
        source_button_layout.addWidget(self.browse_folder_button)
        
        self.browse_file_button = QPushButton("Browse File", self)
        self.browse_file_button.clicked.connect(self.on_browse_file_clicked)
        source_button_layout.addWidget(self.browse_file_button)
        
        source_layout.addWidget(self.source_input)
        source_layout.addLayout(source_button_layout)
        
        layout.addWidget(source_group)
        
        # Options section
        options_group = QGroupBox("Generation Options", self)
        options_layout = QFormLayout(options_group)
        options_layout.setContentsMargins(10, 8, 10, 8)  # Reduced margins
        options_layout.setVerticalSpacing(6)  # Reduced vertical spacing
        
        # Sampling method
        self.sampling_combo = QComboBox(self)
        self.sampling_combo.addItems(["Standard", "Fractal", "Hybrid", "Advanced"])
        options_layout.addRow("Sampling Method:", self.sampling_combo)
        
        # Resolution
        self.resolution_combo = QComboBox(self)
        self.resolution_combo.addItems(["Low (Faster)", "Medium", "High", "Ultra (Slower)"])
        self.resolution_combo.setCurrentIndex(1)  # Medium by default
        options_layout.addRow("Resolution:", self.resolution_combo)
        
        # Capture options
        self.capture_frame = QFrame(self)
        capture_layout = QVBoxLayout(self.capture_frame)
        capture_layout.setContentsMargins(0, 0, 0, 0)
        
        self.capture_headers = QCheckBox("Capture Headers", self)
        self.capture_headers.setChecked(True)
        capture_layout.addWidget(self.capture_headers)
        
        self.capture_payloads = QCheckBox("Capture Payloads", self)
        self.capture_payloads.setChecked(True)
        capture_layout.addWidget(self.capture_payloads)
        
        self.capture_timestamps = QCheckBox("Include Timestamps", self)
        self.capture_timestamps.setChecked(True)
        capture_layout.addWidget(self.capture_timestamps)
        
        options_layout.addRow("Capture:", self.capture_frame)
        
        # Output format
        self.format_group = QButtonGroup(self)
        self.format_frame = QFrame(self)
        format_layout = QHBoxLayout(self.format_frame)
        format_layout.setContentsMargins(0, 0, 0, 0)
        
        self.format_json = QRadioButton("JSON", self)
        self.format_json.setChecked(True)
        self.format_group.addButton(self.format_json)
        format_layout.addWidget(self.format_json)
        
        self.format_binary = QRadioButton("Binary", self)
        self.format_group.addButton(self.format_binary)
        format_layout.addWidget(self.format_binary)
        
        self.format_text = QRadioButton("Text", self)
        self.format_group.addButton(self.format_text)
        format_layout.addWidget(self.format_text)
        
        options_layout.addRow("Output Format:", self.format_frame)
        
        layout.addWidget(options_group)
        
        # Output file selection
        output_group = QGroupBox("Output", self)
        output_layout = QFormLayout(output_group)
        output_layout.setContentsMargins(10, 8, 10, 8)  # Reduced margins
        output_layout.setVerticalSpacing(6)  # Reduced vertical spacing
        
        self.output_input = QLineEdit(self)
        self.output_input.setPlaceholderText("Select output file...")
        
        self.browse_output_button = QPushButton("Browse", self)
        self.browse_output_button.clicked.connect(self.on_browse_output_clicked)
        
        output_input_layout = QHBoxLayout()
        output_input_layout.addWidget(self.output_input)
        output_input_layout.addWidget(self.browse_output_button)
        
        output_layout.addRow("Output File:", output_input_layout)
        
        layout.addWidget(output_group)
        
        # Progress section
        progress_group = QGroupBox("Progress", self)
        progress_layout = QVBoxLayout(progress_group)
        progress_layout.setContentsMargins(10, 8, 10, 8)  # Reduced margins
        progress_layout.setSpacing(6)  # Reduced vertical spacing
        
        # Add Start button with neon purple styling
        self.start_button = QPushButton("Start", self)
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6; /* Neon purple */
                color: white;
                font-weight: bold;
                font-size: 14px;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #a569bd;
            }
            QPushButton:pressed {
                background-color: #8e44ad;
            }
        """)
        self.start_button.clicked.connect(self.on_generate_clicked)  # Connect to same handler as Generate button
        progress_layout.addWidget(self.start_button)
        
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        progress_layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("Ready to generate", self)
        progress_layout.addWidget(self.status_label)
        
        layout.addWidget(progress_group)
        
        # Button section
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.back_button = QPushButton("Back", self)
        self.back_button.clicked.connect(self.on_back_clicked)
        button_layout.addWidget(self.back_button)
        
        button_layout.addStretch(1)
        
        # Make Generate button more prominent
        self.generate_button = QPushButton("Generate Pawprint", self)
        self.generate_button.setMinimumWidth(200)
        self.generate_button.setMinimumHeight(40)
        self.generate_button.setStyleSheet("""
            QPushButton {
                background-color: #2980b9;
                color: white;
                font-weight: bold;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #3498db;
            }
            QPushButton:pressed {
                background-color: #1c6ea4;
            }
        """)
        self.generate_button.clicked.connect(self.on_generate_clicked)
        button_layout.addWidget(self.generate_button)
        
        # Add button layout to main layout with minimal spacing
        layout.addSpacing(5)  # Reduced space above buttons
        layout.addLayout(button_layout)
    
    def connect_signals(self):
        """Connect signals to slots"""
        # Connect progress tracker signals
        self.progress_tracker.progress_updated.connect(self.on_progress_updated)
        self.progress_tracker.operation_completed.connect(self.on_operation_completed)
        
        # Connect output input changes to update path
        self.output_input.textChanged.connect(self.on_output_text_changed)
        
        # Connect format selection to update output extension
        self.format_json.toggled.connect(self.on_format_changed)
        self.format_binary.toggled.connect(self.on_format_changed)
        self.format_text.toggled.connect(self.on_format_changed)
    
    def on_browse_folder_clicked(self):
        """Handle browse folder button click"""
        # Get last used directory from state
        last_dir = self.state_manager.get_value("last_session.last_directory", "")
        
        # Use QFileDialog directly for better handling of directory selection
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Source Folder",
            last_dir,
            QFileDialog.Option.ShowDirsOnly | QFileDialog.Option.DontResolveSymlinks
        )
        
        if directory:
            # Update state with selected directory
            self.state_manager.set_value("last_session.last_directory", directory)
            self.state_manager.add_recent_directory(directory)
            
            # Update UI
            self.source_path = directory
            self.source_input.setText(directory)
            self.update_default_output_path()
            
            # Log selection
            logger.info(f"Selected source folder: {directory}")
            NotificationManager.show_info(f"Selected folder: {os.path.basename(directory)}")

    def on_browse_file_clicked(self):
        """Handle browse file button click"""
        # Get last used directory from state
        last_dir = self.state_manager.get_value("last_session.last_directory", "")
        
        # Use QFileDialog directly for better handling of file selection
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Source File",
            last_dir,
            "PCAP Files (*.pcap *.pcapng);;All Files (*)"
        )
        
        if file_path:
            # Update state with selected file's directory
            self.state_manager.set_value("last_session.last_directory", os.path.dirname(file_path))
            
            # Update UI
            self.source_path = file_path
            self.source_input.setText(file_path)
            self.update_default_output_path()
            
            # Log selection
            logger.info(f"Selected source file: {file_path}")
            NotificationManager.show_info(f"Selected file: {os.path.basename(file_path)}")
    
    def on_browse_output_clicked(self):
        """Handle browse output button click"""
        # Get default output directory
        default_dir = ""
        if self.output_path:
            default_dir = os.path.dirname(self.output_path)
        elif self.source_path:
            default_dir = os.path.dirname(self.source_path)
        else:
            default_dir = self.state_manager.get_value("last_session.last_export_directory", "")
            if not default_dir:
                default_dir = self.state_manager.get_value("last_session.last_directory", "")
        
        # Generate default filename
        default_name = self.output_input.text()
        if not default_name:
            default_name = self._generate_default_output_filename()
            if default_dir:
                default_name = os.path.join(default_dir, default_name)
        
        # Get default extension based on format selection
        if self.format_json.isChecked():
            filter_str = "JSON Files (*.json);;All Files (*)"
            default_ext = ".json"
        elif self.format_binary.isChecked():
            filter_str = "Binary Files (*.bin);;All Files (*)"
            default_ext = ".bin"
        else:
            filter_str = "Text Files (*.txt);;All Files (*)"
            default_ext = ".txt"
        
        # Ensure default name has the correct extension
        if default_name and not any(default_name.endswith(ext) for ext in [".json", ".bin", ".txt"]):
            default_name += default_ext
        
        # Use QFileDialog directly for better handling of file selection
        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Pawprint File",
            default_name,
            filter_str
        )
        
        if output_path:
            # Update state with selected directory
            export_dir = os.path.dirname(output_path)
            self.state_manager.set_value("last_session.last_export_directory", export_dir)
            
            # Update UI
            self.output_path = output_path
            self.output_input.setText(output_path)
            
            # Log selection
            logger.info(f"Selected output file: {output_path}")
    
    def _generate_default_output_filename(self):
        """Generate default output filename based on source path"""
        if not self.source_path:
            return "pawprint.json"
            
        # Get base name from source
        source_name = os.path.basename(self.source_path)
        
        # Generate output name
        if os.path.isdir(self.source_path):
            output_name = f"{source_name}_pawprint"
        else:
            output_name = f"{os.path.splitext(source_name)[0]}_pawprint"
        
        # Add extension based on format
        if self.format_json.isChecked():
            output_name += ".json"
        elif self.format_binary.isChecked():
            output_name += ".bin"
        else:
            output_name += ".txt"
        
        return output_name
    
    def update_default_output_path(self):
        """Update default output path based on source path"""
        if not self.source_path:
            return
            
        # Generate default output filename
        output_name = self._generate_default_output_filename()
        
        # Use source directory for output
        output_dir = os.path.dirname(self.source_path)
        output_path = os.path.join(output_dir, output_name)
        
        # Update output field
        self.output_path = output_path
        self.output_input.setText(output_path)
    
    def on_back_clicked(self):
        """Handle back button click"""
        if self.is_generating:
            # Ask for confirmation if currently generating
            confirm = NotificationManager.show_dialog(
                "Cancel Generation",
                "A pawprint generation is in progress. Are you sure you want to cancel and go back?",
                "question"
            )
            
            if not confirm:
                return
        
        # Go back to dashboard
        if hasattr(self.main_window, "show_dashboard_screen") and callable(self.main_window.show_dashboard_screen):
            self.main_window.show_dashboard_screen()
    
    def on_generate_clicked(self):
        """Handle generate button click"""
        # Validate inputs
        if not self.validate_inputs():
            return
        
        # Start generation
        self.start_generation()
    
    def validate_inputs(self) -> bool:
        """
        Validate input fields
        
        Returns:
            True if valid, False otherwise
        """
        # Check source path
        if not self.source_path:
            NotificationManager.show_error("Please select a source folder or file.")
            return False
        
        if not os.path.exists(self.source_path):
            NotificationManager.show_error("Source path does not exist.")
            return False
        
        # Check output path
        if not self.output_path:
            NotificationManager.show_error("Please select an output file.")
            return False
        
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(self.output_path)
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir, exist_ok=True)
            except Exception as e:
                NotificationManager.show_error(f"Error creating output directory: {e}")
                return False
        
        return True
    
    def start_generation(self):
        """Start pawprint generation"""
        # Update UI
        self.is_generating = True
        self.generate_button.setEnabled(False)
        self.browse_folder_button.setEnabled(False)
        self.browse_file_button.setEnabled(False)
        self.browse_output_button.setEnabled(False)
        
        # Get options
        options = self.get_generation_options()
        
        # Log generation start
        logger.info(f"Starting pawprint generation with options: {options}")
        
        # Update status
        self.status_label.setText("Initializing generation...")
        
        # Start progress tracker
        self.progress_tracker.start(100, "Pawprint Generation")
        
        # Simulate generation for now
        # In a real app, this would call actual generation code
        QTimer.singleShot(500, self.simulate_generation)
    
    def get_generation_options(self) -> Dict[str, Any]:
        """
        Get generation options from UI
        
        Returns:
            Dictionary of options
        """
        options = {
            "source_path": self.source_path,
            "output_path": self.output_path,
            "sampling_method": self.sampling_combo.currentText(),
            "resolution": self.resolution_combo.currentText(),
            "capture_headers": self.capture_headers.isChecked(),
            "capture_payloads": self.capture_payloads.isChecked(),
            "include_timestamps": self.capture_timestamps.isChecked(),
            "format": "json" if self.format_json.isChecked() else 
                     "binary" if self.format_binary.isChecked() else "text"
        }
        
        return options
    
    def simulate_generation(self):
        """Simulate pawprint generation (for testing UI)"""
        # This would be replaced with actual generation code
        total_steps = 100
        
        # Start simulation
        for i in range(1, total_steps + 1):
            # Simulate processing step
            message = f"Processing {'files' if os.path.isdir(self.source_path) else 'data'}..."
            if i < 20:
                message = "Analyzing source data..."
            elif i < 40:
                message = "Extracting features..."
            elif i < 60:
                message = "Generating pawprint patterns..."
            elif i < 80:
                message = "Optimizing pattern representation..."
            elif i < 95:
                message = "Creating output file..."
            else:
                message = "Finalizing pawprint..."
            
            # Update progress
            self.progress_tracker.update(i, message)
            
            # Process events to keep UI responsive
            QApplication.processEvents()
            
            # Add delay for simulation
            QTimer.singleShot(50, lambda: None)
        
        # Complete generation
        self.progress_tracker.complete(True, "Pawprint generation completed successfully")
        
        # Generate a more realistic pawprint file
        self._generate_realistic_pawprint()
        
        # Add to recent files
        self.state_manager.add_recent_file(self.output_path)

    def _generate_realistic_pawprint(self):
        """Generate a more realistic pawprint file for simulation purposes"""
        import random
        import json
        from datetime import datetime, timedelta
        
        # Get source info
        source_name = os.path.basename(self.source_path)
        is_directory = os.path.isdir(self.source_path)
        
        # Create timestamps
        now = datetime.now()
        start_time = now - timedelta(minutes=random.randint(5, 30))
        
        # Generate basic structure
        pawprint = {
            "metadata": {
                "version": "2.0.0",
                "generated": now.isoformat(),
                "source": self.source_path,
                "source_type": "directory" if is_directory else "file",
                "generation_time_ms": random.randint(1500, 8000),
                "options": self.get_generation_options()
            },
            "summary": {
                "file_count": random.randint(50, 500) if is_directory else 1,
                "total_size_bytes": random.randint(1000000, 100000000),
                "start_time": start_time.isoformat(),
                "end_time": now.isoformat(),
                "complexity_score": round(random.uniform(0.1, 0.95), 2),
                "entropy": round(random.uniform(0.5, 0.9), 3)
            },
            "patterns": []
        }
        
        # Generate pattern data
        pattern_types = ["sequence", "timing", "frequency", "structure", "content"]
        confidence_levels = ["high", "medium", "low"]
        
        # Add random number of patterns
        num_patterns = random.randint(5, 15)
        for i in range(num_patterns):
            pattern = {
                "id": f"pattern_{i+1}",
                "type": random.choice(pattern_types),
                "confidence": random.choice(confidence_levels),
                "score": round(random.uniform(0.1, 1.0), 2),
                "description": f"Detected {random.choice(pattern_types)} pattern in {source_name}",
                "occurrences": random.randint(1, 50),
                "details": {
                    "complexity": round(random.uniform(0.1, 1.0), 2),
                    "periodicity": round(random.uniform(0, 1.0), 2),
                    "uniqueness": round(random.uniform(0.1, 1.0), 2)
                }
            }
            pawprint["patterns"].append(pattern)
        
        # Add fingerprints section
        pawprint["fingerprints"] = {
            "primary": {
                "hash": "".join(random.choice("0123456789abcdef") for _ in range(40)),
                "algorithm": "sha1",
                "confidence": round(random.uniform(0.7, 1.0), 2)
            },
            "secondary": [
                {
                    "hash": "".join(random.choice("0123456789abcdef") for _ in range(32)),
                    "algorithm": "md5",
                    "confidence": round(random.uniform(0.6, 0.9), 2)
                },
                {
                    "hash": "".join(random.choice("0123456789abcdef") for _ in range(64)),
                    "algorithm": "sha256",
                    "confidence": round(random.uniform(0.8, 1.0), 2)
                }
            ]
        }
        
        # Add fractal analysis if that option was selected
        if self.sampling_combo.currentText() == "Fractal":
            pawprint["fractal_analysis"] = {
                "fractal_dimension": round(random.uniform(1.1, 1.9), 3),
                "self_similarity": round(random.uniform(0.5, 0.95), 3),
                "complexity_metrics": {
                    "hurst_exponent": round(random.uniform(0.1, 0.9), 3),
                    "correlation_dimension": round(random.uniform(1.0, 3.0), 3),
                    "lyapunov_exponent": round(random.uniform(0.01, 0.2), 4)
                },
                "butterfly_parameters": {
                    "wing_ratio": round(random.uniform(1.5, 2.5), 2),
                    "symmetry_score": round(random.uniform(0.7, 0.99), 3),
                    "pattern_density": round(random.uniform(0.3, 0.8), 2)
                }
            }
        
        # Add file entries if it's a directory source
        if is_directory:
            pawprint["files"] = []
            # Generate random files
            extensions = [".txt", ".log", ".dat", ".bin", ".cfg", ".json", ".xml"]
            for i in range(min(20, pawprint["summary"]["file_count"])):
                file_entry = {
                    "path": f"{source_name}/{''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(8))}{random.choice(extensions)}",
                    "size_bytes": random.randint(1024, 10485760),
                    "modified": (now - timedelta(days=random.randint(1, 30))).isoformat(),
                    "entropy": round(random.uniform(0.1, 0.9), 3),
                    "hash": "".join(random.choice("0123456789abcdef") for _ in range(32))
                }
                pawprint["files"].append(file_entry)
        
        # Write to output file
        with open(self.output_path, 'w') as f:
            json.dump(pawprint, f, indent=2)
        
        logger.info(f"Generated realistic pawprint file: {self.output_path}")
    
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
        self.browse_folder_button.setEnabled(True)
        self.browse_file_button.setEnabled(True)
        self.browse_output_button.setEnabled(True)
        
        # Update status
        self.status_label.setText(message)
        
        # Show notification
        if success:
            NotificationManager.show_success("Pawprint generated successfully")
            
            # Ask if user wants to analyze the generated pawprint
            confirm = NotificationManager.show_dialog(
                "Pawprint Generated",
                "Would you like to analyze the generated pawprint now?",
                "question"
            )
            
            if confirm and hasattr(self.main_window, "show_analyze_screen") and callable(self.main_window.show_analyze_screen):
                # Open the analyze screen with the generated file
                if hasattr(self.main_window, "analyze_screen") and hasattr(self.main_window.analyze_screen, "load_file"):
                    self.main_window.show_analyze_screen()
                    self.main_window.analyze_screen.load_file(self.output_path)
                else:
                    NotificationManager.show_info("Opening analysis screen (not yet implemented)")
        else:
            NotificationManager.show_error("Error generating pawprint: " + message)

    def on_output_text_changed(self, text):
        """Handle output text field changes"""
        self.output_path = text
    
    def on_format_changed(self, checked):
        """Handle format selection changes"""
        if not checked or not self.output_path:
            return
            
        # Update file extension based on selected format
        base_path = os.path.splitext(self.output_path)[0]
        
        if self.format_json.isChecked():
            new_path = base_path + ".json"
        elif self.format_binary.isChecked():
            new_path = base_path + ".bin"
        else:
            new_path = base_path + ".txt"
        
        # Update path without triggering textChanged signal
        self.output_input.blockSignals(True)
        self.output_input.setText(new_path)
        self.output_input.blockSignals(False)
        self.output_path = new_path
