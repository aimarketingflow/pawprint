#!/usr/bin/env python3
"""
Compare Screen for Pawprinting PyQt6 Application - Part 4a: Charts Tab Setup

Implements the basic setup for the charts tab in the Compare Screen.

Author: AIMF LLC
Date: June 6, 2025
"""

# This file contains methods for the charts tab setup that would be included in the CompareScreen class

def setup_charts_tab(self):
    """Set up the charts tab for visualizing pattern score changes"""
    self.charts_tab = QWidget()
    charts_layout = QVBoxLayout(self.charts_tab)
    
    # Create controls area for chart options
    self.setup_chart_controls()
    
    # Create chart display area
    self.setup_chart_display()
    
    # Add components to layout
    charts_layout.addWidget(self.chart_controls)
    charts_layout.addWidget(self.chart_display_container, 1)
    
    # Add to tab widget
    self.tab_widget.addTab(self.charts_tab, "Charts")

def setup_chart_controls(self):
    """Set up chart control options"""
    self.chart_controls = QGroupBox("Chart Options")
    controls_layout = QHBoxLayout(self.chart_controls)
    
    # Chart type selection
    type_layout = QHBoxLayout()
    type_label = QLabel("Chart Type:")
    self.chart_type_combo = QComboBox()
    self.chart_type_combo.addItems([
        "Radar Chart", 
        "Bar Chart", 
        "Pie Chart", 
        "Line Chart",
        "Heatmap"
    ])
    type_layout.addWidget(type_label)
    type_layout.addWidget(self.chart_type_combo)
    
    # Pattern category selection
    category_layout = QHBoxLayout()
    category_label = QLabel("Pattern Category:")
    self.category_combo = QComboBox()
    self.category_combo.addItems([
        "All Categories",
        "File System",
        "Registry",
        "Network",
        "Processes",
        "Users & Groups",
        "Services"
    ])
    category_layout.addWidget(category_label)
    category_layout.addWidget(self.category_combo)
    
    # Score threshold
    threshold_layout = QHBoxLayout()
    threshold_label = QLabel("Min. Score Difference:")
    self.threshold_combo = QComboBox()
    self.threshold_combo.addItems([
        "Any Change",
        "> 0.01",
        "> 0.05",
        "> 0.10",
        "> 0.25"
    ])
    threshold_layout.addWidget(threshold_label)
    threshold_layout.addWidget(self.threshold_combo)
    
    # Update button
    self.update_chart_button = QPushButton("Update Chart")
    self.update_chart_button.setObjectName("primaryButton")
    
    # Add all controls to main layout
    controls_layout.addLayout(type_layout)
    controls_layout.addLayout(category_layout)
    controls_layout.addLayout(threshold_layout)
    controls_layout.addStretch()
    controls_layout.addWidget(self.update_chart_button)
    
    # Connect signals
    self.chart_type_combo.currentIndexChanged.connect(self.on_chart_type_changed)
    self.category_combo.currentIndexChanged.connect(self.on_chart_category_changed)
    self.threshold_combo.currentIndexChanged.connect(self.on_chart_threshold_changed)
    self.update_chart_button.clicked.connect(self.on_update_chart_clicked)

def setup_chart_display(self):
    """Set up chart display area"""
    self.chart_display_container = QSplitter(Qt.Orientation.Vertical)
    
    # Chart canvas area
    self.chart_widget = QWidget()
    chart_layout = QVBoxLayout(self.chart_widget)
    chart_layout.setContentsMargins(0, 0, 0, 0)
    
    if MATPLOTLIB_AVAILABLE:
        # Create matplotlib figure and canvas
        self.chart_figure = Figure(figsize=(8, 6), dpi=100, tight_layout=True)
        self.chart_canvas = FigureCanvas(self.chart_figure)
        self.chart_toolbar = NavigationToolbar(self.chart_canvas, self)
        
        chart_layout.addWidget(self.chart_canvas)
        chart_layout.addWidget(self.chart_toolbar)
    else:
        # Fallback if matplotlib is not available
        no_mpl_label = QLabel("Matplotlib is required for chart visualization")
        no_mpl_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        chart_layout.addWidget(no_mpl_label)
    
    # Chart description and insights area
    self.chart_insights = QGroupBox("Chart Insights")
    insights_layout = QVBoxLayout(self.chart_insights)
    
    self.chart_description = QTextEdit()
    self.chart_description.setReadOnly(True)
    self.chart_description.setObjectName("chartDescription")
    
    insights_layout.addWidget(self.chart_description)
    
    # Add components to splitter
    self.chart_display_container.addWidget(self.chart_widget)
    self.chart_display_container.addWidget(self.chart_insights)
    
    # Set initial stretch factors
    self.chart_display_container.setStretchFactor(0, 3)  # Chart gets more space
    self.chart_display_container.setStretchFactor(1, 1)  # Description gets less space

def on_chart_type_changed(self, index):
    """Handle chart type selection change
    
    Args:
        index: Selected index in chart type combo
    """
    # Update chart display based on selected type
    chart_type = self.chart_type_combo.currentText()
    self.update_chart(chart_type)

def on_chart_category_changed(self, index):
    """Handle chart category selection change
    
    Args:
        index: Selected index in category combo
    """
    # Update chart to filter by selected category
    category = self.category_combo.currentText()
    self.filter_chart_by_category(category)

def on_chart_threshold_changed(self, index):
    """Handle chart threshold selection change
    
    Args:
        index: Selected index in threshold combo
    """
    # Update chart to filter by selected threshold
    threshold_text = self.threshold_combo.currentText()
    
    # Parse threshold value
    if threshold_text == "Any Change":
        threshold = 0.0
    else:
        # Extract number from text like "> 0.05"
        threshold = float(threshold_text.split(" ")[1])
    
    self.filter_chart_by_threshold(threshold)

def on_update_chart_clicked(self):
    """Handle update chart button click"""
    # Get current settings
    chart_type = self.chart_type_combo.currentText()
    category = self.category_combo.currentText()
    threshold_text = self.threshold_combo.currentText()
    
    # Parse threshold value
    if threshold_text == "Any Change":
        threshold = 0.0
    else:
        # Extract number from text like "> 0.05"
        threshold = float(threshold_text.split(" ")[1])
    
    # Update chart with all settings
    self.update_chart(chart_type, category, threshold)
