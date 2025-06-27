#!/usr/bin/env python3
"""
Compare Screen for Pawprinting PyQt6 Application - Part 2: UI Setup

Implements the UI setup methods for the Compare Screen.

Author: AIMF LLC
Date: June 6, 2025
"""

# This file contains UI setup methods that would be included in the CompareScreen class

def setup_ui(self):
    """Set up the Compare Screen UI components"""
    logger.info("Setting up Compare Screen UI")
    
    # Create main layout with splitter for sidebar and content
    self.main_layout = QVBoxLayout(self)
    self.main_layout.setContentsMargins(0, 0, 0, 0)
    self.main_layout.setSpacing(0)
    
    # Create back button and header
    self.setup_header()
    
    # Create main splitter
    self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
    
    # Create sidebar for file selection and management
    self.setup_sidebar()
    
    # Create content area with tab widget
    self.setup_content_area()
    
    # Add splitter to main layout
    self.main_layout.addWidget(self.main_splitter, 1)
    
    # Set up initial styles
    self.apply_styles()
    
    logger.info("Compare Screen UI setup complete")

def setup_header(self):
    """Set up the header with back button and title"""
    header_container = QWidget()
    header_layout = QHBoxLayout(header_container)
    
    # Back button
    self.back_button = QPushButton("← Back")
    self.back_button.setObjectName("backButton")
    self.back_button.setFixedHeight(36)
    
    # Title label
    self.title_label = QLabel("Compare Pawprints")
    self.title_label.setObjectName("screenTitle")
    
    # Add to layout with spacer
    header_layout.addWidget(self.back_button)
    header_layout.addWidget(self.title_label)
    header_layout.addStretch()
    
    # Add header to main layout
    self.main_layout.addWidget(header_container)
    
    # Add separator line
    separator = QFrame()
    separator.setFrameShape(QFrame.Shape.HLine)
    separator.setFrameShadow(QFrame.Shadow.Sunken)
    separator.setObjectName("separator")
    self.main_layout.addWidget(separator)

def setup_sidebar(self):
    """Set up the sidebar for file selection and management"""
    self.sidebar = QWidget()
    self.sidebar.setObjectName("compareSidebar")
    self.sidebar.setMinimumWidth(250)
    self.sidebar.setMaximumWidth(350)
    
    sidebar_layout = QVBoxLayout(self.sidebar)
    
    # Files section
    files_group = QGroupBox("Files to Compare")
    files_layout = QVBoxLayout(files_group)
    
    # File list
    self.file_list = QTreeWidget()
    self.file_list.setHeaderLabels(["Files"])
    self.file_list.setObjectName("filesList")
    
    # Add/remove file buttons
    file_buttons_layout = QHBoxLayout()
    self.add_file_button = QPushButton("Add File")
    self.remove_file_button = QPushButton("Remove")
    self.clear_files_button = QPushButton("Clear All")
    
    file_buttons_layout.addWidget(self.add_file_button)
    file_buttons_layout.addWidget(self.remove_file_button)
    file_buttons_layout.addWidget(self.clear_files_button)
    
    files_layout.addWidget(self.file_list)
    files_layout.addLayout(file_buttons_layout)
    
    # Options section
    options_group = QGroupBox("Comparison Options")
    options_layout = QVBoxLayout(options_group)
    
    # Group by origin checkbox
    self.group_by_origin = QCheckBox("Group by Origin")
    self.group_by_origin.setChecked(True)
    
    # Compare button
    self.compare_button = QPushButton("Compare Files")
    self.compare_button.setObjectName("primaryButton")
    self.compare_button.setEnabled(False)  # Disabled until files are selected
    
    options_layout.addWidget(self.group_by_origin)
    options_layout.addWidget(self.compare_button)
    
    # Add all sections to sidebar layout
    sidebar_layout.addWidget(files_group)
    sidebar_layout.addWidget(options_group)
    sidebar_layout.addStretch()
    
    # Export section
    export_group = QGroupBox("Export")
    export_layout = QVBoxLayout(export_group)
    
    # Export options
    self.export_button = QPushButton("Export Results...")
    self.export_button.setEnabled(False)  # Disabled until comparison is done
    
    export_layout.addWidget(self.export_button)
    
    sidebar_layout.addWidget(export_group)
    
    # Add sidebar to splitter
    self.main_splitter.addWidget(self.sidebar)

def setup_content_area(self):
    """Set up the content area with tab widget"""
    self.content_area = QWidget()
    content_layout = QVBoxLayout(self.content_area)
    content_layout.setContentsMargins(0, 0, 0, 0)
    
    # Create tab widget for different views
    self.tab_widget = QTabWidget()
    self.tab_widget.setObjectName("compareTabWidget")
    
    # Create tabs for different views
    self.setup_comparison_tab()
    self.setup_charts_tab()
    self.setup_raw_data_tab()
    self.setup_summary_tab()
    
    # Add tab widget to layout
    content_layout.addWidget(self.tab_widget)
    
    # Add content area to splitter
    self.main_splitter.addWidget(self.content_area)
    
    # Set stretch factors (content area should take more space)
    self.main_splitter.setStretchFactor(0, 0)  # Sidebar doesn't stretch
    self.main_splitter.setStretchFactor(1, 1)  # Content area stretches

def apply_styles(self):
    """Apply theme styles to the Compare Screen components"""
    # Get primary accent color from theme manager
    accent_color = self.theme_manager.get_accent_color()
    dark_bg_color = self.theme_manager.get_background_color()
    text_color = self.theme_manager.get_text_color()
    
    # Set styles for main components
    self.setStyleSheet(f"""
        #backButton {{
            background-color: transparent;
            border: 1px solid {accent_color};
            border-radius: 4px;
            color: {text_color};
            font-weight: bold;
            padding: 5px 10px;
        }}
        #backButton:hover {{
            background-color: {accent_color};
            color: #FFFFFF;
        }}
        #screenTitle {{
            font-size: 18px;
            font-weight: bold;
            color: {accent_color};
        }}
        #separator {{
            color: {accent_color};
            height: 2px;
        }}
        #filesList {{
            background-color: {dark_bg_color};
            border: 1px solid #444;
            border-radius: 4px;
        }}
        #compareTabWidget::pane {{
            border: 1px solid #444;
            border-top: 2px solid {accent_color};
        }}
        #compareTabWidget::tab-bar {{
            alignment: left;
        }}
        #compareTabWidget QTabBar::tab {{
            background-color: {dark_bg_color};
            color: {text_color};
            min-width: 100px;
            padding: 8px 12px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }}
        #compareTabWidget QTabBar::tab:selected {{
            background-color: {accent_color};
            color: white;
        }}
        #primaryButton {{
            background-color: {accent_color};
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 12px;
            font-weight: bold;
        }}
        #primaryButton:disabled {{
            background-color: #555;
            color: #999;
        }}
    """)

def connect_signals(self):
    """Connect signals to slots"""
    # Back button
    self.back_button.clicked.connect(self.on_back_clicked)
    
    # File management
    self.add_file_button.clicked.connect(self.on_add_file_clicked)
    self.remove_file_button.clicked.connect(self.on_remove_file_clicked)
    self.clear_files_button.clicked.connect(self.on_clear_files_clicked)
    self.file_list.itemSelectionChanged.connect(self.on_file_selection_changed)
    
    # Compare button
    self.compare_button.clicked.connect(self.on_compare_clicked)
    
    # Tab widget
    self.tab_widget.currentChanged.connect(self.on_tab_changed)
    
    # Export button
    self.export_button.clicked.connect(self.on_export_clicked)
