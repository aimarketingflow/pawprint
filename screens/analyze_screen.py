#!/usr/bin/env python3
"""
Analyze Screen for Pawprinting PyQt6 Application

Screen for analyzing pawprints and visualizing data patterns.

Author: AIMF LLC
Date: June 2, 2025
"""

import os
import sys
import json
import logging
import re
from datetime import datetime
from typing import Optional, Dict, Any, List

from PyQt6.QtCore import Qt, QSize, pyqtSignal, pyqtSlot, QTimer
from PyQt6.QtGui import QIcon, QPixmap, QFont, QColor, QPainter, QPen, QBrush, QTextCharFormat, QTextCursor
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, 
    QGridLayout, QFormLayout, QLineEdit, QFileDialog, QGroupBox,
    QProgressBar, QCheckBox, QComboBox, QFrame, QScrollArea, 
    QRadioButton, QButtonGroup, QSpacerItem, QSizePolicy, QTextEdit,
    QApplication, QTabWidget, QSplitter
)

try:
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
    import numpy as np
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

# Import utility modules
from utils.notification_manager import NotificationManager
from utils.state_manager import StateManager
from utils.theme_manager import ThemeManager
from utils.file_manager import FileManager
from utils.progress_tracker import ProgressTracker
from components.console_widget import ConsoleWidget

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.analyze")


class MatplotlibCanvas(FigureCanvas):
    """Matplotlib canvas for plotting"""
    
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        """Initialize matplotlib canvas"""
        if not MATPLOTLIB_AVAILABLE:
            raise ImportError("Matplotlib is required for plotting")
            
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        
        FigureCanvas.setSizePolicy(
            self,
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        FigureCanvas.updateGeometry(self)


class PawprintVisualizerWidget(QWidget):
    """Widget for visualizing pawprints with various chart types"""
    
    def __init__(self, parent=None):
        """Initialize visualizer widget"""
        super().__init__(parent)
        self.theme_manager = ThemeManager.get_instance()
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 20)  # Extra bottom margin
        
        # Chart type selection and comparison controls
        top_controls = QHBoxLayout()
        
        # Chart type selection
        chart_type_layout = QHBoxLayout()
        chart_type_label = QLabel("Chart Type:", self)
        chart_type_layout.addWidget(chart_type_label)
        
        self.chart_type_combo = QComboBox(self)
        self.chart_type_combo.addItems([
            "Time Series", "Distribution", "Heatmap", "Network Graph", "Fractal View"
        ])
        self.chart_type_combo.currentIndexChanged.connect(self.on_chart_type_changed)
        chart_type_layout.addWidget(self.chart_type_combo)
        chart_type_layout.addStretch(1)
        
        # Chart options
        options_button = QPushButton("Chart Options", self)
        options_button.clicked.connect(self.on_options_clicked)
        chart_type_layout.addWidget(options_button)
        

        
        top_controls.addLayout(chart_type_layout)
        layout.addLayout(top_controls)
        
        # Plot area
        if MATPLOTLIB_AVAILABLE:
            self.canvas = MatplotlibCanvas(self)
            self.toolbar = NavigationToolbar(self.canvas, self)
            layout.addWidget(self.toolbar)
            layout.addWidget(self.canvas)
            
            # Add chart description box
            description_group = QGroupBox("Chart Description", self)
            description_layout = QVBoxLayout(description_group)
            
            self.chart_description = QTextEdit(self)
            self.chart_description.setReadOnly(True)
            self.chart_description.setFixedHeight(100)  # Fixed height to save space
            self.chart_description.setStyleSheet("""
                QTextEdit {
                    background-color: #f8f9fa;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    padding: 5px;
                }
            """)
            description_layout.addWidget(self.chart_description)
            
            layout.addWidget(description_group)
        else:
            # Fallback if matplotlib not available
            fallback_widget = QLabel(
                "Matplotlib is required for visualization. Please install matplotlib.",
                self
            )
            fallback_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
            fallback_widget.setStyleSheet("color: red; font-weight: bold;")
            layout.addWidget(fallback_widget)
    
    def on_chart_type_changed(self, index):
        """Handle chart type selection change"""
        if MATPLOTLIB_AVAILABLE:
            self.update_plot()
    
    def on_options_clicked(self):
        """Handle options button click"""
        # To be implemented: options dialog for plot customization
        NotificationManager.show_info("Chart options dialog will be implemented")
    
    def update_plot(self):
        """Update the current plot"""
        if not MATPLOTLIB_AVAILABLE:
            return
        
        # Clear the plot
        self.canvas.axes.clear()
        
        # Get selected chart type
        chart_type = self.chart_type_combo.currentText()
        
        # Create a placeholder plot based on chart type
        if chart_type == "Time Series":
            self._create_time_series_plot()
            self._set_description("Time Series shows patterns over time. Higher values indicate stronger pattern detection. Look for peaks and trends that may indicate significant events or patterns.")
        elif chart_type == "Distribution":
            self._create_distribution_plot()
            self._set_description("Distribution shows the frequency of different values. Look for unusual peaks or gaps which may indicate anomalies or patterns in the data.")
        elif chart_type == "Heatmap":
            self._create_heatmap_plot()
            self._set_description("Heatmap displays relationships between different data points. Darker colors indicate stronger correlations. Look for clusters that might identify related components.")
        elif chart_type == "Network Graph":
            self._create_network_plot()
            self._set_description("Network Graph shows connections between entities. Larger nodes indicate more connections. Look for central nodes and dense connection clusters that may reveal key interaction points.")
        elif chart_type == "Fractal View":
            self._create_fractal_view()
            self._set_description("Fractal View visualizes self-similar patterns in the data. Similar colors and patterns indicate related behaviors. Look for repeating structures that might indicate recursive or nested behaviors.")
        
        # Update the canvas
        self.canvas.draw()
        
    def _set_description(self, text):
        """Set the chart description text"""
        if hasattr(self, 'chart_description'):
            self.chart_description.setText(text)
    
    def set_data(self, data):
        """Set data for visualization"""
        self.data = data
        self.update_plot()
    
    def _create_time_series_plot(self):
        """Create a time series plot"""
        if not hasattr(self, 'data') or not self.data:
            # Example plot - would use real data in production
            x = np.linspace(0, 10, 100)
            y = np.sin(x)
            self.canvas.axes.plot(x, y)
            self.canvas.axes.set_title("Pawprint Time Series Analysis (Sample Data)")
            self.canvas.axes.set_xlabel("Time")
            self.canvas.axes.set_ylabel("Signal Value")
            self.canvas.axes.grid(True)
            return
            
        # Try to extract pattern data for time series
        try:
            # Create x values based on number of patterns
            if 'patterns' in self.data and isinstance(self.data['patterns'], list):
                patterns = self.data['patterns']
                x = np.arange(len(patterns))
                
                # Get scores from patterns
                y = [p.get('score', 0) for p in patterns]
                
                # Create the plot
                self.canvas.axes.plot(x, y, 'o-', label='Pattern Scores')
                self.canvas.axes.set_title("Pawprint Pattern Scores Analysis")
                self.canvas.axes.set_xlabel("Pattern Index")
                self.canvas.axes.set_ylabel("Confidence Score")
                self.canvas.axes.grid(True)
                
                # Add labels for pattern types
                for i, pattern in enumerate(patterns):
                    self.canvas.axes.annotate(
                        pattern.get('type', ''),
                        (i, y[i]),
                        textcoords="offset points",
                        xytext=(0, 10),
                        ha='center'
                    )
                
                # Set y-axis limits
                self.canvas.axes.set_ylim(0, 1.1)
                return
        except Exception as e:
            logger.error(f"Error creating time series plot: {e}")
            
        # Fallback to example plot
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        self.canvas.axes.plot(x, y)
        self.canvas.axes.set_title("Pawprint Time Series Analysis")
        self.canvas.axes.set_xlabel("Time")
        self.canvas.axes.set_ylabel("Signal Value")
        self.canvas.axes.grid(True)
    
    def _create_distribution_plot(self):
        """Create a distribution plot"""
        if not hasattr(self, 'data') or not self.data:
            # Example plot - would use real data in production
            x = np.random.normal(size=1000)
            self.canvas.axes.hist(x, bins=30, alpha=0.7)
            self.canvas.axes.set_title("Pawprint Distribution Analysis (Sample Data)")
            self.canvas.axes.set_xlabel("Value")
            self.canvas.axes.set_ylabel("Frequency")
            self.canvas.axes.grid(True)
            return
            
        # Try to extract pattern data for distribution
        try:
            # Extract various metrics for distribution
            metrics = []
            
            # Add pattern scores
            if 'patterns' in self.data and isinstance(self.data['patterns'], list):
                metrics.extend([p.get('score', 0) for p in self.data['patterns']])
                
                # Add complexity values if available
                for pattern in self.data['patterns']:
                    if 'details' in pattern and isinstance(pattern['details'], dict):
                        details = pattern['details']
                        metrics.extend([
                            details.get('complexity', 0),
                            details.get('uniqueness', 0),
                            details.get('periodicity', 0)
                        ])
            
            # Add fractal metrics if available
            if 'fractal_analysis' in self.data:
                fractal = self.data['fractal_analysis']
                if isinstance(fractal, dict):
                    metrics.extend([
                        fractal.get('fractal_dimension', 0),
                        fractal.get('self_similarity', 0)
                    ])
                    
                    # Add complexity metrics
                    if 'complexity_metrics' in fractal and isinstance(fractal['complexity_metrics'], dict):
                        complexity = fractal['complexity_metrics']
                        metrics.extend([
                            complexity.get('hurst_exponent', 0),
                            complexity.get('correlation_dimension', 0),
                            complexity.get('lyapunov_exponent', 0)
                        ])
            
            # Create histogram if we have metrics
            if metrics:
                self.canvas.axes.hist(metrics, bins=20, alpha=0.7, color='blue')
                self.canvas.axes.set_title("Pawprint Metrics Distribution")
                self.canvas.axes.set_xlabel("Metric Value")
                self.canvas.axes.set_ylabel("Frequency")
                self.canvas.axes.grid(True)
                return
        except Exception as e:
            logger.error(f"Error creating distribution plot: {e}")
            
        # Fallback to example plot
        x = np.random.normal(size=1000)
        self.canvas.axes.hist(x, bins=30, alpha=0.7)
        self.canvas.axes.set_title("Pawprint Distribution Analysis")
        self.canvas.axes.set_xlabel("Value")
        self.canvas.axes.set_ylabel("Frequency")
        self.canvas.axes.grid(True)
    
    def _create_heatmap_plot(self):
        """Create a heatmap plot"""
        # Example plot - would use real data in production
        data = np.random.rand(10, 10)
        im = self.canvas.axes.imshow(data, cmap='hot')
        self.canvas.axes.set_title("Pawprint Heatmap Analysis")
        self.canvas.fig.colorbar(im)
    
    def _create_network_plot(self):
        """Create a network graph plot"""
        # Example plot - would use real data in production
        # This is a simplified network plot
        nodes_x = np.random.rand(20)
        nodes_y = np.random.rand(20)
        self.canvas.axes.scatter(nodes_x, nodes_y, s=100)
        
        # Draw random edges
        for i in range(30):
            idx1 = np.random.randint(0, 20)
            idx2 = np.random.randint(0, 20)
            self.canvas.axes.plot([nodes_x[idx1], nodes_x[idx2]], 
                                 [nodes_y[idx1], nodes_y[idx2]], 'k-', alpha=0.2)
        
        self.canvas.axes.set_title("Pawprint Network Analysis")
        self.canvas.axes.set_xticks([])
        self.canvas.axes.set_yticks([])
    
    def _create_fractal_view(self):
        """Create a fractal visualization"""
        from matplotlib.colors import LinearSegmentedColormap
        
        # Create a custom colormap
        colors = [(0, 0, 0), (0, 0, 1), (0, 1, 0), (1, 0, 0)]
        cmap_name = 'fractal'
        cmap = LinearSegmentedColormap.from_list(cmap_name, colors, N=256)
        
        # Check if we have fractal data
        if hasattr(self, 'data') and self.data and 'fractal_analysis' in self.data:
            try:
                fractal = self.data['fractal_analysis']
                
                # Use butterfly parameters if available
                wing_ratio = 2.0
                symmetry = 0.9
                density = 0.5
                
                if 'butterfly_parameters' in fractal:
                    butterfly = fractal['butterfly_parameters']
                    wing_ratio = butterfly.get('wing_ratio', wing_ratio)
                    symmetry = butterfly.get('symmetry_score', symmetry)
                    density = butterfly.get('pattern_density', density)
                
                fractal_dim = fractal.get('fractal_dimension', 1.5)
                
                # Generate a more interesting fractal based on parameters
                x, y = np.meshgrid(np.linspace(-2, 1, 500), np.linspace(-1.5, 1.5, 500))
                c = x + 1j * y
                z = c.copy()
                fractal_data = np.zeros_like(z, dtype=float)
                
                # Adjust parameters based on fractal data
                max_iter = int(20 + fractal_dim * 10)
                escape_radius = 4.0 + symmetry * 6.0
                
                # Generate fractal
                for n in range(max_iter):
                    mask = (np.abs(z) <= escape_radius)
                    fractal_data[mask] = n + np.abs(z[mask]) / escape_radius
                    z[mask] = z[mask]**2 + c[mask] * wing_ratio
                
                # Apply density adjustment
                fractal_data = fractal_data ** (1.0 - density * 0.5)
                
                # Plot the fractal
                im = self.canvas.axes.imshow(fractal_data, cmap=cmap, origin='lower', 
                                           extent=[-2, 1, -1.5, 1.5])
                self.canvas.axes.set_title(f"Pawprint Fractal Analysis (Dimension: {fractal_dim:.3f})")
                self.canvas.axes.set_xlabel("Real")
                self.canvas.axes.set_ylabel("Imaginary")
                self.canvas.fig.colorbar(im)
                return
                
            except Exception as e:
                logger.error(f"Error creating fractal view: {e}")
        
        # Fallback to default fractal
        # Generate fractal-like data (simplified Mandelbrot set)
        x, y = np.meshgrid(np.linspace(-2, 1, 500), np.linspace(-1.5, 1.5, 500))
        c = x + 1j * y
        z = c.copy()
        fractal = np.zeros_like(z, dtype=float)
        
        max_iter = 20
        for n in range(max_iter):
            mask = (np.abs(z) <= 10)
            fractal[mask] = n
            z[mask] = z[mask]**2 + c[mask]
        
        im = self.canvas.axes.imshow(fractal, cmap=cmap, origin='lower', 
                                    extent=[-2, 1, -1.5, 1.5])
        self.canvas.axes.set_title("Pawprint Fractal Analysis (Sample Data)")
        self.canvas.axes.set_xlabel("Real")
        self.canvas.axes.set_ylabel("Imaginary")
        self.canvas.fig.colorbar(im)


class JsonViewerWidget(QWidget):
    """Widget for viewing JSON data"""
    
    def __init__(self, parent=None):
        """Initialize JSON viewer widget"""
        super().__init__(parent)
        self.theme_manager = ThemeManager.get_instance()
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the UI components"""
        layout = QVBoxLayout(self)
        
        # Controls
        controls_layout = QHBoxLayout()
        
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Search JSON...")
        self.search_input.textChanged.connect(self.on_search_changed)
        controls_layout.addWidget(self.search_input)
        
        self.format_button = QPushButton("Format JSON", self)
        self.format_button.clicked.connect(self.format_json)
        controls_layout.addWidget(self.format_button)
        
        self.expand_button = QPushButton("Expand All", self)
        self.expand_button.clicked.connect(self.expand_all)
        controls_layout.addWidget(self.expand_button)
        
        self.collapse_button = QPushButton("Collapse All", self)
        self.collapse_button.clicked.connect(self.collapse_all)
        controls_layout.addWidget(self.collapse_button)
        
        layout.addLayout(controls_layout)
        
        # JSON text area
        self.json_text = QTextEdit(self)
        self.json_text.setReadOnly(True)
        font = QFont("Menlo", 10)
        if not font.exactMatch():
            font = QFont("Courier New", 10)
            if not font.exactMatch():
                font = QFont("Monospace", 10)
        font.setFixedPitch(True)
        self.json_text.setFont(font)
        
        layout.addWidget(self.json_text)
    
    def on_search_changed(self, text):
        """Handle search text change"""
        if not text:
            # Reset search
            self.format_json()
            return
            
        # Find matches
        cursor = self.json_text.textCursor()
        cursor.setPosition(0)
        self.json_text.setTextCursor(cursor)
        
        # Clear previous formatting
        format_json = self.json_data
        self.json_text.setText(json.dumps(format_json, indent=2))
        
        # Search and highlight
        search_text = text.lower()
        json_text = self.json_text.toPlainText().lower()
        
        index = json_text.find(search_text)
        while index != -1:
            cursor = self.json_text.textCursor()
            cursor.setPosition(index)
            cursor.setPosition(index + len(search_text), QTextCursor.MoveMode.KeepAnchor)
            format = QTextCharFormat()
            format.setBackground(QColor("yellow"))
            format.setForeground(QColor("black"))
            cursor.mergeCharFormat(format)
            index = json_text.find(search_text, index + 1)
    
    def format_json(self):
        """Format JSON with proper indentation"""
        if hasattr(self, 'json_data'):
            formatted_json = json.dumps(self.json_data, indent=2)
            self.json_text.setText(formatted_json)
    
    def expand_all(self):
        """Expand all JSON nodes (placeholder)"""
        self.format_json()
        # Note: Full tree-based expansion would require a more complex widget
    
    def collapse_all(self):
        """Collapse all JSON nodes (placeholder)"""
        if hasattr(self, 'json_data'):
            # Just show first level for now
            collapsed = {}
            for key, value in self.json_data.items():
                if isinstance(value, dict) or isinstance(value, list):
                    collapsed[key] = "..."
                else:
                    collapsed[key] = value
            self.json_text.setText(json.dumps(collapsed, indent=2))
    
    def set_data(self, data):
        """Set JSON data for display"""
        self.json_data = data
        # Ensure we actually have data
        if data is None:
            self.json_text.setText("No data available")
            return
            
        try:
            # Try to format the JSON
            formatted_json = json.dumps(data, indent=2, sort_keys=False)
            self.json_text.setText(formatted_json)
            # Set cursor to beginning
            cursor = self.json_text.textCursor()
            cursor.setPosition(0)
            self.json_text.setTextCursor(cursor)
        except Exception as e:
            # If there's an error, display that
            self.json_text.setText(f"Error formatting JSON: {str(e)}\n\nRaw data: {str(data)}")
        
        # Highlight the syntax (basic version)
        self._highlight_json()
        
    def _highlight_json(self):
        """Apply syntax highlighting to the JSON text"""
        # Get the current text
        text = self.json_text.toPlainText()
        
        # Don't process if empty
        if not text:
            return
            
        # Create a cursor to apply formatting
        cursor = self.json_text.textCursor()
        cursor.setPosition(0)
        
        # Define colors for different JSON elements
        colors = {
            'key': QColor("#881280"),    # Purple for keys
            'string': QColor("#1A1AA6"), # Blue for string values
            'number': QColor("#1C00CF"), # Dark blue for numbers
            'boolean': QColor("#008000"), # Green for true/false
            'null': QColor("#808080"),    # Gray for null
            'bracket': QColor("#000000") # Black for brackets and braces
        }
        
        # Simple regex patterns for different elements
        patterns = [
            # Keys (with quotes and colon)
            (r'"[^"]*"(?=\s*:)', colors['key']),
            # String values
            (r'"[^"]*"(?!\s*:)', colors['string']),
            # Numbers
            (r'\b-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?\b', colors['number']),
            # Booleans
            (r'\b(true|false)\b', colors['boolean']),
            # Null
            (r'\bnull\b', colors['null']),
            # Brackets and braces
            (r'[\[\]{},:]+', colors['bracket'])
        ]
        
        # Store the original cursor position
        orig_position = self.json_text.textCursor().position()
        
        # Apply formatting
        for pattern, color in patterns:
            regex = re.compile(pattern)
            matches = regex.finditer(text)
            
            for match in matches:
                start, end = match.span()
                format = QTextCharFormat()
                format.setForeground(color)
                
                cursor = self.json_text.textCursor()
                cursor.setPosition(start)
                cursor.setPosition(end, QTextCursor.MoveMode.KeepAnchor)
                cursor.mergeCharFormat(format)
        
        # Restore cursor position
        cursor = self.json_text.textCursor()
        cursor.setPosition(orig_position)
        self.json_text.setTextCursor(cursor)


class AnalyzeScreen(QWidget):
    """
    Screen for analyzing pawprints and visualizing patterns
    """
    def __init__(self, parent=None):
        """Initialize analyze screen"""
        super().__init__(parent)
        self.main_window = parent
        self.state_manager = StateManager.get_instance()
        self.theme_manager = ThemeManager.get_instance()
        self.file_manager = FileManager(self)
        self.progress_tracker = ProgressTracker(self)
        
        # State variables
        self.current_file_path = ""
        self.pawprint_data = None
        self.is_analyzing = False
        
        # Set up UI
        self.setup_ui()
        
        # Connect signals
        self.connect_signals()
        
        logger.info("Analyze screen initialized")
    
    def setup_ui(self):
        """Set up the analyze screen UI components"""
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 10, 20, 10)  # Reduced margins
        layout.setSpacing(8)  # Reduced spacing
        
        # Navigation bar at top
        nav_layout = QHBoxLayout()
        nav_layout.setContentsMargins(0, 0, 0, 5)
        
        self.nav_back_button = QPushButton("◀ Back", self)
        self.nav_back_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db; /* Neon blue */
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 5px 10px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.nav_back_button.clicked.connect(self.on_back_clicked)
        nav_layout.addWidget(self.nav_back_button)
        
        # Title - centered
        title_label = QLabel("Analyze Pawprint", self)
        title_label.setStyleSheet("font-size: 22px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFixedHeight(35)  # Fixed height for title
        nav_layout.addWidget(title_label, 1)  # Give title stretch factor for centering
        
        # Home button
        self.nav_home_button = QPushButton("Home", self)
        self.nav_home_button.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71; /* Green */
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 5px 10px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        self.nav_home_button.clicked.connect(self.on_back_clicked)  # Uses same handler
        nav_layout.addWidget(self.nav_home_button)
        
        layout.addLayout(nav_layout)
        
        # File selection
        file_group = QGroupBox("Pawprint File", self)
        file_layout = QHBoxLayout(file_group)
        file_layout.setContentsMargins(10, 8, 10, 8)  # Reduced internal margins
        
        self.file_input = QLineEdit(self)
        self.file_input.setReadOnly(True)
        self.file_input.setPlaceholderText("Select pawprint file...")
        file_layout.addWidget(self.file_input)
        
        self.browse_button = QPushButton("Browse", self)
        self.browse_button.clicked.connect(self.on_browse_clicked)
        file_layout.addWidget(self.browse_button)
        
        layout.addWidget(file_group)
        
        # Main content area with tabs
        self.tab_widget = QTabWidget(self)
        
        # Visualization tab
        self.visualizer = PawprintVisualizerWidget(self)
        self.tab_widget.addTab(self.visualizer, "Visualization")
        
        # Raw Data tab
        self.json_viewer = JsonViewerWidget(self)
        self.tab_widget.addTab(self.json_viewer, "Raw Data")
        
        # Console tab
        self.console = ConsoleWidget(self)
        self.tab_widget.addTab(self.console, "Console")
        
        layout.addWidget(self.tab_widget)
        
        # Status bar
        status_layout = QHBoxLayout()
        
        self.status_label = QLabel("Ready", self)
        status_layout.addWidget(self.status_label)
        
        status_layout.addStretch(1)
        
        self.analyze_button = QPushButton("Analyze", self)
        self.analyze_button.setEnabled(False)
        self.analyze_button.clicked.connect(self.on_analyze_clicked)
        status_layout.addWidget(self.analyze_button)
        
        layout.addLayout(status_layout)
        
        # Button section - make buttons more visible and add neon blue Back button at bottom
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(5, 0, 5, 0)  # Minimal margins
        
        # Create a prominent Back button with neon blue styling
        self.back_button = QPushButton("Back", self)
        self.back_button.setMinimumWidth(120)
        self.back_button.setMinimumHeight(40)
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db; /* Neon blue */
                color: white;
                font-weight: bold;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1c6ea4;
            }
        """)
        self.back_button.clicked.connect(self.on_back_clicked)
        button_layout.addWidget(self.back_button)
        
        # Add permanent Compare button that's always visible
        self.compare_button = QPushButton("🔍 Compare Pawprints", self)
        self.compare_button.setMinimumWidth(180)
        self.compare_button.setMinimumHeight(40)
        self.compare_button.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6; /* Purple */
                color: white;
                font-weight: bold;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
            QPushButton:pressed {
                background-color: #7d3c98;
            }
        """)
        self.compare_button.clicked.connect(self.select_files_for_comparison)
        button_layout.addWidget(self.compare_button)
        
        button_layout.addStretch(1)
        
        self.export_button = QPushButton("Export Results", self)
        self.export_button.setEnabled(False)
        self.export_button.clicked.connect(self.on_export_clicked)
        button_layout.addWidget(self.export_button)
        
        layout.addLayout(button_layout)
    
    def connect_signals(self):
        """Connect signals to slots"""
        # Connect progress tracker signals
        self.progress_tracker.progress_updated.connect(self.on_progress_updated)
        self.progress_tracker.operation_completed.connect(self.on_operation_completed)
    
    def on_browse_clicked(self):
        """Handle browse button click"""
        # Get last used directory from state
        last_dir = self.state_manager.get_value("last_session.last_directory", "")
        
        # Use QFileDialog directly for better handling of file selection
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Pawprint File",
            last_dir,
            "Pawprint Files (*.json *.pawprint);;All Files (*)"
        )
        
        if file_path:
            # Update state with selected file's directory
            self.state_manager.set_value("last_session.last_directory", os.path.dirname(file_path))
            self.state_manager.add_recent_file(file_path)
            
            # Update UI
            self.current_file_path = file_path
            self.file_input.setText(file_path)
            self.analyze_button.setEnabled(True)
            
            # Load the file automatically
            self.load_pawprint_file(file_path)
            
            # Log selection
            logger.info(f"Selected pawprint file: {file_path}")
            NotificationManager.show_info(f"Selected file: {os.path.basename(file_path)}")
    
    def load_pawprint_file(self, file_path):
        """
        Load pawprint file
        
        Args:
            file_path: Path to pawprint file
        """
        try:
            self.console.info(f"Loading pawprint file: {file_path}")
            self.status_label.setText(f"Loading {os.path.basename(file_path)}...")
            
            # Load JSON data
            with open(file_path, 'r') as f:
                self.pawprint_data = json.load(f)
            
            # Log data structure for debugging
            self.console.info(f"Loaded data structure: {type(self.pawprint_data)}")
            if isinstance(self.pawprint_data, dict):
                self.console.info(f"Keys in data: {', '.join(self.pawprint_data.keys())}")
            
            # Ensure we have valid data before proceeding
            if not self.pawprint_data:
                raise ValueError("Empty pawprint data")
                
            # Update JSON viewer with raw data
            self.console.info("Updating JSON viewer with raw data...")
            self.json_viewer.set_data(self.pawprint_data)
            # self.json_viewer.format_json() # This call is likely redundant as set_data handles formatting/highlighting.
        
            # Update visualizer with data for charts
            self.console.info("Updating visualizer with data...")
            self.visualizer.set_data(self.pawprint_data)
            
            # Explicitly trigger a visualization update
            self.visualizer.update_plot()
            
            # Enable analyze button
            self.analyze_button.setEnabled(True)
            
            # Provide feedback on success
            self.console.info(f"Loaded pawprint file successfully")
            self.status_label.setText(f"Loaded {os.path.basename(file_path)}")
            
            # Switch to Raw Data tab first to ensure it's visible
            self.tab_widget.setCurrentIndex(1)  # Index 1 should be the Raw Data tab
        
            # After a brief delay, switch to Visualization tab
            # QTimer.singleShot(1000, lambda: self.tab_widget.setCurrentIndex(0)) # Temporarily disabled for debugging
            
        except Exception as e:
            logger.error(f"Error loading pawprint file: {e}")
            self.console.error(f"Error loading file: {e}")
            NotificationManager.show_error(f"Error loading file: {e}")
            self.status_label.setText("Error loading file")
    
    def on_analyze_clicked(self):
        """Handle analyze button click"""
        if not self.pawprint_data:
            NotificationManager.show_error("No pawprint data loaded")
            return
        
        # Start analysis
        self.start_analysis()
    
    def start_analysis(self):
        """Start pawprint analysis"""
        # Update UI
        self.is_analyzing = True
        self.analyze_button.setEnabled(False)
        self.browse_button.setEnabled(False)
        
        # Update status
        self.status_label.setText("Analyzing pawprint data...")
        
        # Start progress tracker
        self.progress_tracker.start(100, "Pawprint Analysis")
        
        # Log start
        self.console.info("Starting pawprint analysis...")
        
        # Simulate analysis for now
        # In a real app, this would call actual analysis code
        QTimer.singleShot(500, self.simulate_analysis)
    
    def simulate_analysis(self):
        """Simulate pawprint analysis (for testing UI)"""
        # This would be replaced with actual analysis code
        total_steps = 100
        
        # Start simulation
        for i in range(1, total_steps + 1):
            # Simulate processing step
            if i < 20:
                message = "Loading pawprint structure..."
            elif i < 40:
                message = "Analyzing patterns..."
            elif i < 60:
                message = "Calculating metrics..."
            elif i < 80:
                message = "Generating visualizations..."
            else:
                message = "Finalizing analysis..."
            
            # Update progress
            self.progress_tracker.update(i, message)
            
            # Update console
            if i % 10 == 0:
                self.console.info(f"{message} - {i}% complete")
            
            # Process events to keep UI responsive
            QApplication.processEvents()
            
            # Add delay for simulation
            QTimer.singleShot(30, lambda: None)
        
        # Complete analysis
        self.progress_tracker.complete(True, "Pawprint analysis completed successfully")
        
        # Generate random data for visualization demo
        self.visualizer.update_plot()
        
        # Enable export button
        self.export_button.setEnabled(True)
    
    def on_back_clicked(self):
        """Handle back button click"""
        if self.is_analyzing:
            # Ask for confirmation if currently analyzing
            confirm = NotificationManager.show_dialog(
                "Cancel Analysis",
                "An analysis is in progress. Are you sure you want to cancel and go back?",
                "question"
            )
            
            if not confirm:
                return
        
        # Go back to dashboard
        if hasattr(self.main_window, "show_dashboard_screen") and callable(self.main_window.show_dashboard_screen):
            self.main_window.show_dashboard_screen()
    
    def on_export_clicked(self):
        """Handle export results button click"""
        if not self.pawprint_data:
            NotificationManager.show_error("No analysis results to export")
            return
        
        # Get default export directory
        last_export_dir = self.state_manager.get_value("last_session.last_export_directory", "")
        if not last_export_dir:
            last_export_dir = os.path.dirname(self.current_file_path) if self.current_file_path else ""
        
        # Generate default filename
        default_name = "analysis_results.html"
        if self.current_file_path:
            base_name = os.path.splitext(os.path.basename(self.current_file_path))[0]
            default_name = f"{base_name}_analysis.html"
        
        default_path = os.path.join(last_export_dir, default_name) if last_export_dir else default_name
        
        # Show save dialog
        export_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Analysis Results",
            default_path,
            "HTML Files (*.html);;PDF Files (*.pdf);;CSV Files (*.csv);;All Files (*)"
        )
        
        if not export_path:
            return
        
        # Update state with selected directory
        export_dir = os.path.dirname(export_path)
        self.state_manager.set_value("last_session.last_export_directory", export_dir)
        
        # Export results
        try:
            # For demonstration, we'll just create a simple HTML file
            with open(export_path, 'w') as f:
                f.write(f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Pawprint Analysis Results</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; margin: 20px; }}
                        h1 {{ color: #2c3e50; }}
                        .section {{ margin-bottom: 20px; padding: 10px; border: 1px solid #ddd; }}
                    </style>
                </head>
                <body>
                    <h1>Pawprint Analysis Results</h1>
                    <div class="section">
                        <h2>Analysis Summary</h2>
                        <p>Analysis performed on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                        <p>File: {self.current_file_path}</p>
                    </div>
                    <div class="section">
                        <h2>Metrics</h2>
                        <ul>
                            <li>Complexity Score: 0.87</li>
                            <li>Pattern Matching: 92%</li>
                            <li>Uniqueness Factor: High</li>
                        </ul>
                    </div>
                    <div class="section">
                        <h2>Raw Data</h2>
                        <pre>{json.dumps(self.pawprint_data, indent=2)}</pre>
                    </div>
                </body>
                </html>
                """)
            
            self.console.info(f"Exported analysis results to {export_path}")
            NotificationManager.show_success(f"Results exported to {export_path}")
            
            # Ask if user wants to open the exported file
            confirm = NotificationManager.show_dialog(
                "Export Complete",
                f"Results exported to {export_path}. Do you want to open this file?",
                "question"
            )
            
            if confirm:
                # Open the file with the default application
                if sys.platform == "win32":
                    os.startfile(export_path)
                elif sys.platform == "darwin":  # macOS
                    os.system(f"open \"{export_path}\"")
                else:  # Linux
                    os.system(f"xdg-open \"{export_path}\"")
                
        except Exception as e:
            logger.error(f"Error exporting results: {e}")
            self.console.error(f"Error exporting results: {e}")
            NotificationManager.show_error(f"Error exporting results: {e}")
    
    def on_progress_updated(self, percentage, message):
        """
        Handle progress updates from the progress tracker
        
        Args:
            percentage: Progress percentage (0-100)
            message: Status message
        """
        self.status_label.setText(message)
    
    def on_operation_completed(self, success, message):
        """
        Handle operation completion from the progress tracker
        
        Args:
            success: Whether the operation was successful
            message: Completion message
        """
        # Update UI
        self.is_analyzing = False
        self.analyze_button.setEnabled(True)
        self.browse_button.setEnabled(True)
        
        # Update status
        self.status_label.setText(message)
        
        # Show notification
        if success:
            NotificationManager.show_success("Analysis completed successfully")
            self.console.info("Analysis completed successfully")
        else:
            NotificationManager.show_error("Error during analysis: " + message)
            self.console.error("Error during analysis: " + message)
    
    def load_file(self, file_path):
        """Public method to load a file from external call
        
        Args:
            file_path: Path to pawprint file to load
        """
        if file_path and os.path.exists(file_path):
            self.current_file_path = file_path
            self.file_input.setText(file_path)
            self.load_pawprint_file(file_path)
            return True
        return False
        
    def compare_files(self, file_paths):
        """Compare multiple pawprint files
        
        Args:
            file_paths: List of paths to pawprint files to compare
            
        Returns:
            bool: True if comparison was set up successfully, False otherwise
        """
        if not file_paths or len(file_paths) < 2:
            NotificationManager.show_warning("At least two files are required for comparison")
            return False
            
        # Try to load all pawprint files
        comparison_data = []
        file_names = []
        metadata_origins = []
        
        for file_path in file_paths:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    comparison_data.append(data)
                    file_names.append(os.path.basename(file_path))
                    
                    # Extract origin metadata if available
                    if 'metadata' in data and 'origin' in data['metadata']:
                        metadata_origins.append(data['metadata']['origin'])
                    else:
                        metadata_origins.append('Unknown')
            except Exception as e:
                logger.error(f"Error loading pawprint file {file_path}: {str(e)}")
                NotificationManager.show_error(f"Error loading pawprint file: {str(e)}")
                return False
        
        # Group files by origin for easier comparison
        origin_groups = {}
        for i, origin in enumerate(metadata_origins):
            if origin not in origin_groups:
                origin_groups[origin] = []
            origin_groups[origin].append((file_names[i], file_paths[i], comparison_data[i]))
                
        # Set up comparison view
        self._setup_comparison_view(file_names, comparison_data, origin_groups)
        return True
    
    def _setup_comparison_view(self, file_names, comparison_data, origin_groups=None):
        """Set up the comparison view UI with tabs for overview, individual files, and differences
        
        Args:
            file_names: List of file names being compared
            comparison_data: List of pawprint data dictionaries to compare
            origin_groups: Dictionary of files grouped by origin metadata
        """
        # Clear current view
        self.clear_ui()
        
        # Store the comparison data for export
        self.current_comparison = {
            "file_names": file_names,
            "data": comparison_data,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Create comparison container
        self.comparison_container = QWidget()
        comparison_layout = QVBoxLayout(self.comparison_container)
        
        # Create tab widget for comparison
        self.comparison_tabs = QTabWidget()
        self.layout().addWidget(self.comparison_tabs)
        
        # Overview tab
        overview_widget = QWidget()
        overview_layout = QVBoxLayout(overview_widget)
        
        # Add title
        title = QLabel(f"Comparing {len(file_names)} Pawprint Files", overview_widget)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        overview_layout.addWidget(title)
        
        # Origin group section (if available)
        if origin_groups and len(origin_groups) > 1:
            origin_group_box = QGroupBox("Files by Origin", overview_widget)
            origin_group_layout = QVBoxLayout(origin_group_box)
            
            origin_label = QLabel("Select pawprints from the same origin to compare:")
            origin_label.setStyleSheet("font-weight: bold;")
            origin_group_layout.addWidget(origin_label)
            
            # Create group list
            for origin, files in origin_groups.items():
                if len(files) >= 2:  # Only show origins with multiple files
                    origin_button = QPushButton(f"{origin} ({len(files)} files)")
                    origin_button.setStyleSheet("""
                        QPushButton {
                            background-color: #9b59b6; /* Purple */
                            color: white;
                            font-weight: bold;
                            border-radius: 5px;
                            padding: 8px;
                            text-align: left;
                        }
                        QPushButton:hover {
                            background-color: #8e44ad;
                        }
                    """)
                    # Use lambda with default argument to capture the current origin value
                    origin_button.clicked.connect(lambda checked=False, o=origin: self._show_origin_comparison(o, origin_groups[o]))
                    origin_group_layout.addWidget(origin_button)
                    
            if origin_group_layout.count() > 1:  # Only add if we have origins with multiple files
                overview_layout.addWidget(origin_group_box)
        
        # All files list
        files_group = QGroupBox("All Files Being Compared", overview_widget)
        files_layout = QVBoxLayout(files_group)
        
        files_list = QListWidget()
        for name in file_names:
            files_list.addItem(name)
        files_list.setMaximumHeight(150)
        files_layout.addWidget(files_list)
        overview_layout.addWidget(files_group)
        
        # Calculate comparison metrics
        metrics = self._calculate_comparison_metrics(comparison_data)
        
        # Display overall similarity score
        similarity_label = QLabel(f"<h3>Overall Similarity Score: {metrics['overall_similarity']:.2f}%</h3>")
        similarity_label.setTextFormat(Qt.TextFormat.RichText)
        overview_layout.addWidget(similarity_label)
        
        # Create a summary table of metrics
        metrics_html = "<table border='1' cellpadding='5' style='border-collapse: collapse'>\n"
        metrics_html += "<tr><th>Metric</th><th>Value</th></tr>\n"
        metrics_html += f"<tr><td>Total attributes compared</td><td>{metrics['total_attributes']}</td></tr>\n"
        metrics_html += f"<tr><td>Identical attributes</td><td>{metrics['identical_attributes']} ({metrics['identical_percent']:.2f}%)</td></tr>\n"
        metrics_html += f"<tr><td>Different attributes</td><td>{metrics['different_attributes']} ({metrics['different_percent']:.2f}%)</td></tr>\n"
        metrics_html += f"<tr><td>Unique attributes</td><td>{metrics['unique_attributes']} ({metrics['unique_percent']:.2f}%)</td></tr>\n"
        metrics_html += "</table>"
        
        metrics_text = QLabel(metrics_html)
        metrics_text.setTextFormat(Qt.TextFormat.RichText)
        overview_layout.addWidget(metrics_text)
        
        # Add export button
        export_btn = QPushButton("Export Comparison Report")
        export_btn.clicked.connect(self.export_comparison_report)
        overview_layout.addWidget(export_btn)
        
        # Add a back button to exit comparison mode
        back_btn = QPushButton("Exit comparison mode")
        back_btn.clicked.connect(self.exit_comparison_mode)
        overview_layout.addWidget(back_btn)
        
        # Add overview tab
        tab_widget.addTab(overview_tab, "Overview")
        
        # Log what we're comparing
        logger.info(f"Setting up comparison view for {len(file_names)} files: {', '.join(file_names)}")
        
        # Set window title to indicate comparison mode
        if hasattr(self.main_window, "setWindowTitle"):
            self.main_window.setWindowTitle(f"Pawprint Analyzer - Comparing {len(file_names)} Files")
            
        # Create a tabbed interface for comparing files if it doesn't exist
        if not hasattr(self, 'comparison_tabs'):
            # Store original visualizer and json viewer for later restoration
            self.original_visualizer = self.visualizer
            self.original_json_viewer = self.json_viewer
            
            # Create a tab widget for comparison
            self.comparison_tabs = QTabWidget()
            
            # Replace the content area with the tab widget
            self.content_layout.removeWidget(self.content_splitter)
            self.content_splitter.hide()
            self.content_layout.addWidget(self.comparison_tabs)
        else:
            # Clear existing tabs
            while self.comparison_tabs.count() > 0:
                self.comparison_tabs.removeTab(0)
        
        # Add overview tab
        overview_widget = QWidget()
        overview_layout = QVBoxLayout(overview_widget)
        
        # Add back button at the top
        back_button = QPushButton("← Back to Normal View")
        back_button.setToolTip("Exit comparison mode and return to normal view")
        back_button.clicked.connect(self.exit_comparison_mode)
        overview_layout.addWidget(back_button)
        
        # Add title and description
        title = QLabel(f"Comparing {len(file_names)} Pawprint Files")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        overview_layout.addWidget(title)
        
        description = QLabel("Select tabs to view individual files or comparison results")
        overview_layout.addWidget(description)
        
        # Add file list
        files_group = QGroupBox("Files Being Compared")
        files_layout = QVBoxLayout(files_group)
        
        for i, name in enumerate(file_names):
            file_label = QLabel(f"{i+1}. {name}")
            files_layout.addWidget(file_label)
            
        overview_layout.addWidget(files_group)
        
        # Add comparison metrics section
        metrics_group = QGroupBox("Comparison Metrics")
        metrics_layout = QGridLayout(metrics_group)
        
        # Calculate basic difference metrics
        # This is a simplified example - in a real app, we'd do more advanced comparison
        similar_keys = self._find_common_keys(comparison_data)
        different_keys = self._find_different_keys(comparison_data, similar_keys)
        
        metrics_layout.addWidget(QLabel("Similar attributes:"), 0, 0)
        metrics_layout.addWidget(QLabel(str(len(similar_keys))), 0, 1)
        
        metrics_layout.addWidget(QLabel("Different attributes:"), 1, 0)
        metrics_layout.addWidget(QLabel(str(len(different_keys))), 1, 1)
        
        metrics_layout.addWidget(QLabel("Total files:"), 2, 0)
        metrics_layout.addWidget(QLabel(str(len(file_names))), 2, 1)
        
        overview_layout.addWidget(metrics_group)
        overview_layout.addStretch(1)
        
        # Add overview tab
        self.comparison_tabs.addTab(overview_widget, "Overview")
        
        # Add individual file tabs
        for i, (name, data) in enumerate(zip(file_names, comparison_data)):
            file_widget = QWidget()
            file_layout = QVBoxLayout(file_widget)
            
            # Create visualizer and json viewer for this file
            splitter = QSplitter(Qt.Orientation.Vertical)
            
            # Create visualizer
            viz = PawprintVisualizerWidget()
            viz.set_data(data)
            viz.update_plot()
            
            # Create JSON viewer
            json_view = JsonViewerWidget()
            json_view.set_data(data)
            
            # Add to splitter
            splitter.addWidget(viz)
            splitter.addWidget(json_view)
            splitter.setStretchFactor(0, 2)  # Visualizer gets more space
            splitter.setStretchFactor(1, 1)
            
            file_layout.addWidget(splitter)
            
            # Add tab
            self.comparison_tabs.addTab(file_widget, f"File {i+1}: {name}")
            
        # Add difference tab
        diff_widget = QWidget()
        diff_layout = QVBoxLayout(diff_widget)
        
        diff_table = QTextEdit()
        diff_table.setReadOnly(True)
        diff_table.setStyleSheet("font-family: monospace;")
        
        # Generate a simple HTML difference report
        diff_html = self._generate_diff_html(file_names, comparison_data, similar_keys, different_keys)
        diff_table.setHtml(diff_html)
        
        diff_layout.addWidget(diff_table)
        
        # Add to tabs
        self.comparison_tabs.addTab(diff_widget, "Differences")
        
        # Connect signals
        self.comparison_tabs.currentChanged.connect(self._on_comparison_tab_changed)
        
        # Show the first tab
        self.comparison_tabs.setCurrentIndex(0)
        
    def _find_common_keys(self, data_list):
        """Find keys that have the same value across all pawprints"""
        if not data_list or len(data_list) < 2:
            return []
            
        # Start with all keys from first file
        common_keys = set()
        for key, value in self._flatten_dict(data_list[0]).items():
            is_common = True
            for other_data in data_list[1:]:
                flat_other = self._flatten_dict(other_data)
                if key not in flat_other or flat_other[key] != value:
                    is_common = False
                    break
            if is_common:
                common_keys.add(key)
                
        return list(common_keys)
        
    def _find_different_keys(self, data_list, common_keys):
        """Find keys that have different values across pawprints"""
        if not data_list or len(data_list) < 2:
            return []
            
        # Get all keys from all files
        all_keys = set()
        for data in data_list:
            all_keys.update(self._flatten_dict(data).keys())
            
        # Remove common keys
        different_keys = all_keys - set(common_keys)
        return list(different_keys)
        
    def _flatten_dict(self, d, parent_key=''):
        """Flatten a nested dictionary"""
        items = {}
        for k, v in d.items():
            new_key = f"{parent_key}.{k}" if parent_key else k
            if isinstance(v, dict):
                items.update(self._flatten_dict(v, new_key))
            else:
                items[new_key] = v
        return items
        
    def _generate_diff_html(self, file_names, data_list, similar_keys, different_keys):
        """Generate HTML to display differences between files"""
        html = """<html>
        <head>
            <style>
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #4CAF50; color: white; }
                tr:nth-child(even) { background-color: #f2f2f2; }
                .different { background-color: #ffcccc; }
                .similar { background-color: #ccffcc; }
            </style>
        </head>
        <body>
            <h2>Pawprint Comparison Results</h2>
        """
        
        # Generate table for different keys
        html += "<h3>Different Attributes</h3>"
        html += "<table><tr><th>Attribute</th>"
        for name in file_names:
            html += f"<th>{name}</th>"
        html += "</tr>"
        
        # Add rows for different keys
        for key in sorted(different_keys):
            html += f"<tr class='different'><td>{key}</td>"
            for data in data_list:
                flat_data = self._flatten_dict(data)
                value = flat_data.get(key, "N/A")
                # Convert to string and escape HTML
                value_str = str(value).replace("<", "&lt;").replace(">", "&gt;")
                html += f"<td>{value_str}</td>"
            html += "</tr>"
        html += "</table>"
        
        # Generate table for similar keys
        html += "<h3>Similar Attributes</h3>"
        html += "<table><tr><th>Attribute</th><th>Value</th></tr>"
        
        # Add rows for similar keys
        for key in sorted(similar_keys):
            flat_data = self._flatten_dict(data_list[0])
            value = flat_data.get(key, "N/A")
            # Convert to string and escape HTML
            value_str = str(value).replace("<", "&lt;").replace(">", "&gt;")
            html += f"<tr class='similar'><td>{key}</td><td>{value_str}</td></tr>"
        html += "</table>"
        
        html += "</body></html>"
        return html
        
    def _on_comparison_tab_changed(self, index):
        """Handle comparison tab changes"""
        tab_name = self.comparison_tabs.tabText(index)
        logger.info(f"Switched to comparison tab: {tab_name}")
    
    def _calculate_comparison_metrics(self, comparison_data):
        """Calculate metrics for comparing multiple pawprint files
        
        Args:
            comparison_data: List of pawprint data dictionaries to compare
            
        Returns:
            Dictionary with comparison metrics
        """
        if not comparison_data or len(comparison_data) < 2:
            return {
                "total_attributes": 0,
                "identical_attributes": 0,
                "different_attributes": 0,
                "unique_attributes": 0,
                "identical_percent": 0,
                "different_percent": 0,
                "unique_percent": 0,
                "overall_similarity": 0
            }
            
        # Create flattened versions of each data structure
        flat_data = []
        for data in comparison_data:
            flat_data.append(self._flatten_dict(data))
            
        # Find all unique keys across all pawprints
        all_keys = set()
        for data in flat_data:
            all_keys.update(data.keys())
        # Count identical, different, and unique attributes
        total_attributes = len(all_keys)
        identical_attributes = 0
        different_attributes = 0
        unique_attributes = 0
        
        for key in all_keys:
            # Check how many pawprints have this key
            pawprints_with_key = sum(1 for data in flat_data if key in data)
            
            if pawprints_with_key == len(comparison_data):
                # This key exists in all pawprints
                # Check if all values are the same
                values = [str(data.get(key)) for data in flat_data if key in data]
                if len(set(values)) == 1:
                    identical_attributes += 1
                else:
                    different_attributes += 1
            else:
                # This key is unique to some pawprints
                unique_attributes += 1
        
        # Calculate percentages
        identical_percent = (identical_attributes / total_attributes * 100) if total_attributes > 0 else 0
        different_percent = (different_attributes / total_attributes * 100) if total_attributes > 0 else 0
        unique_percent = (unique_attributes / total_attributes * 100) if total_attributes > 0 else 0
        
        # Calculate overall similarity score (weighted more towards identical attributes)
        overall_similarity = (
            identical_percent * 1.0 +
            (100 - different_percent) * 0.5 +
            (100 - unique_percent) * 0.3
        ) / 1.8
        
        return {
            "total_attributes": total_attributes,
            "identical_attributes": identical_attributes,
            "different_attributes": different_attributes,
            "unique_attributes": unique_attributes,
            "identical_percent": identical_percent,
            "different_percent": different_percent,
            "unique_percent": unique_percent,
            "overall_similarity": overall_similarity
        }
    
    def export_comparison_report(self):
        """Export the current comparison data as an HTML report"""
        if not hasattr(self, "current_comparison"):
            NotificationManager.show_warning("No comparison data available to export")
            return
            
        # Get export path
        export_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Comparison Report",
            os.path.join(os.path.expanduser("~"), "Documents", "pawprint_comparison.html"),
            "HTML Files (*.html);;"
        )
            
        if not export_path:
            return
                
        try:
            # Generate HTML report
            metrics = self._calculate_comparison_metrics(self.current_comparison["data"])
            report_html = self._generate_comparison_report_html(
                self.current_comparison["file_names"],
                self.current_comparison["data"],
                metrics
            )
                
            # Write to file
            with open(export_path, "w") as f:
                f.write(report_html)
                    
            # Log and notify
            logger.info(f"Exported comparison report to {export_path}")
            NotificationManager.show_success(f"Comparison report exported to: {export_path}")
                
            # Try to open the file
            if sys.platform == "darwin":  # macOS
                os.system(f"open {export_path}")
            elif sys.platform == "win32":  # Windows
                os.system(f"start {export_path}")
            elif sys.platform == "linux":  # Linux
                os.system(f"xdg-open {export_path}")
                    
        except Exception as e:
            logger.error(f"Error exporting comparison report: {e}")
            NotificationManager.show_error(f"Error exporting comparison report: {str(e)}")
    
    def _generate_comparison_report_html(self, file_names, comparison_data, metrics):
        """Generate HTML report for comparison
            
        Args:
            file_names: List of file names being compared
            comparison_data: List of pawprint data dictionaries
            metrics: Comparison metrics dictionary
                
        Returns:
            HTML string for report
        """
        # Create flattened versions of each data structure
        flat_data = []
        for data in comparison_data:
            flat_data.append(self._flatten_dict(data))
            
        # Find all unique keys across all pawprints
        all_keys = set()
        for data in flat_data:
            all_keys.update(data.keys())
                
        # Generate HTML
        html = """<!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Pawprint Comparison Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h1, h2, h3 { color: #333; }
                table { border-collapse: collapse; width: 100%; margin: 20px 0; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
                tr:nth-child(even) { background-color: #f9f9f9; }
                .identical { background-color: #dff0d8; }
                .different { background-color: #fcf8e3; }
                .unique { background-color: #f2dede; }
                .logo { text-align: center; margin: 20px 0; }
                .footer { margin-top: 30px; text-align: center; font-size: 0.8em; color: #666; }
            </style>
        </head>
        <body>
            <div class="logo">
                <h1>AIMF LLC Digital Forensics</h1>
                <h2>Pawprint Comparison Report</h2>
            </div>
                
            <h3>Files Compared</h3>
            <ul>
        """
        
        # Add file names
        for name in file_names:
            html += f"<li>{name}</li>\n"
                
        html += """</ul>
                
            <h3>Comparison Summary</h3>
            <table>
                <tr><th>Metric</th><th>Value</th></tr>
        """
        
        # Add metrics
        html += f"<tr><td>Overall Similarity Score</td><td>{metrics['overall_similarity']:.2f}%</td></tr>\n"
        html += f"<tr><td>Total Attributes Compared</td><td>{metrics['total_attributes']}</td></tr>\n"
        html += f"<tr><td>Identical Attributes</td><td>{metrics['identical_attributes']} ({metrics['identical_percent']:.2f}%)</td></tr>\n"
        html += f"<tr><td>Different Attributes</td><td>{metrics['different_attributes']} ({metrics['different_percent']:.2f}%)</td></tr>\n"
        html += f"<tr><td>Unique Attributes</td><td>{metrics['unique_attributes']} ({metrics['unique_percent']:.2f}%)</td></tr>\n"
            
        html += """</table>
                
            <h3>Detailed Comparison</h3>
            <table>
                <tr>
                    <th>Attribute</th>
        """
        
        # Add file name headers
        for name in file_names:
            html += f"<th>{name}</th>\n"
                
        html += "<th>Status</th></tr>\n"
            
        # Sort keys for consistent output
        sorted_keys = sorted(list(all_keys))
        
        # Add rows for each attribute
        for key in sorted_keys:
            values = []
            for i, data in enumerate(flat_data):
                values.append(data.get(key, "<em>Not present</em>"))
                    
            # Determine status
            all_present = all(key in data for data in flat_data)
            if all_present:
                if len(set(str(v) for v in values)) == 1:
                    status = "identical"
                    status_text = "Identical"
                else:
                    status = "different"
                    status_text = "Different"
            else:
                status = "unique"
                status_text = "Unique"
                    
            # Create table row
            html += f"<tr class='{status}'><td><code>{key}</code></td>\n"
            for value in values:
                html += f"<td>{value}</td>\n"
            html += f"<td>{status_text}</td></tr>\n"
                
        # Complete HTML
        html += """</table>
                
            <div class="footer">
                <p>Generated by Pawprinting Tool v2.0 on {}</p>
                <p>AIMF LLC Digital Forensics &copy; 2025</p>
            </div>
        </body>
        </html>
        """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            
        return html
    
    def _show_origin_comparison(self, origin, files):
        """Show comparison view for files from the same origin
        
        Args:
            origin: The origin metadata value
            files: List of (filename, filepath, data) tuples for files with the same origin
        """
        # Create a new dialog for this comparison
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Pawprint Comparison - {origin}")
        dialog.setMinimumSize(900, 700)
        
        # Set up dialog layout
        layout = QVBoxLayout(dialog)
        
        # Add header
        header = QLabel(f"Comparing {len(files)} Pawprints from Origin: {origin}")
        header.setStyleSheet("font-size: 18px; font-weight: bold;")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        # Create tab widget for the different files
        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)
        
        # Overview tab showing differences
        overview_tab = QWidget()
        overview_layout = QVBoxLayout(overview_tab)
        
        # Extract just the data and file names
        comparison_file_names = [f[0] for f in files]
        comparison_data = [f[2] for f in files]
        
        # Find common and different keys
        common_keys = self._find_common_keys(comparison_data)
        different_keys = self._find_different_keys(comparison_data, common_keys)
        
        # Create HTML diff view
        diff_html = self._generate_diff_html(comparison_file_names, comparison_data, common_keys, different_keys)
        
        diff_view = QTextEdit()
        diff_view.setReadOnly(True)
        diff_view.setHtml(diff_html)
        overview_layout.addWidget(diff_view)
        
        # Add overview tab
        tab_widget.addTab(overview_tab, "Differences")
        
        # Add individual file tabs
        for i, (filename, filepath, data) in enumerate(files):
            file_tab = QWidget()
            file_layout = QVBoxLayout(file_tab)
            
            # Add file info
            file_info = QLabel(f"File: {filepath}")
            file_info.setWordWrap(True)
            file_layout.addWidget(file_info)
            
            # Create JSON viewer
            json_viewer = JsonViewerWidget()
            json_viewer.set_data(data)
            file_layout.addWidget(json_viewer)
            
            tab_widget.addTab(file_tab, filename)
        
        # Add export button
        export_button = QPushButton("Export Comparison Report")
        export_button.setMinimumHeight(40)
        export_button.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        export_button.clicked.connect(lambda: self._export_origin_comparison(origin, comparison_file_names, comparison_data))
        layout.addWidget(export_button)
        
        dialog.exec()
    
    def _export_origin_comparison(self, origin, file_names, comparison_data):
        """Export comparison report for files with the same origin
        
        Args:
            origin: The origin metadata value
            file_names: List of file names being compared
            comparison_data: List of pawprint data dictionaries
        """
        # Calculate metrics
        metrics = self._calculate_comparison_metrics(comparison_data)
        
        # Generate HTML report
        html_report = self._generate_comparison_report_html(file_names, comparison_data, metrics)
        
        # Save dialog
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Comparison Report",
            f"Pawprint_Comparison_{origin}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
            "HTML Files (*.html);;All Files (*)",
            options=options
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write(html_report)
                NotificationManager.show_info(f"Report saved to {file_path}")
            except Exception as e:
                logger.error(f"Error saving comparison report: {str(e)}")
                NotificationManager.show_error(f"Error saving report: {str(e)}")
    
    def exit_comparison_mode(self):
        """Exit comparison mode and restore the original UI"""
        # Clear comparison data
        self.current_comparison = None
        
        # Restore original view
        self.clear_ui()
        self.setup_ui()
        
        # If a file was previously loaded, reload it
        if self.current_file_path:
            self.load_pawprint_file(self.current_file_path)
            self.main_window.setWindowTitle("Pawprinting - Analyze")
                
        logger.info("Exited comparison mode")
        return True
        
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
