#!/usr/bin/env python3
"""
Compare Screen for Pawprinting PyQt6 Application - Part 4c-1: Raw Data Tab

Implements the Raw Data tab for the Compare Screen.

Author: AIMF LLC
Date: June 6, 2025
"""

# This file contains methods for the raw data tab that would be included in the CompareScreen class

def setup_raw_data_tab(self):
    """Set up the raw data tab for viewing comparison JSON data"""
    self.raw_data_tab = QWidget()
    raw_data_layout = QVBoxLayout(self.raw_data_tab)
    
    # Create file selection area
    self.setup_raw_data_file_selector()
    
    # Create JSON viewer
    self.setup_raw_data_viewer()
    
    # Add components to layout
    raw_data_layout.addWidget(self.raw_data_file_selector)
    raw_data_layout.addWidget(self.raw_data_viewer_container, 1)
    
    # Add to tab widget
    self.tab_widget.addTab(self.raw_data_tab, "Raw Data")

def setup_raw_data_file_selector(self):
    """Set up file selection area for raw data tab"""
    self.raw_data_file_selector = QGroupBox("File Selection")
    selector_layout = QHBoxLayout(self.raw_data_file_selector)
    
    # File dropdown
    file_label = QLabel("Select File:")
    self.raw_data_file_combo = QComboBox()
    
    # View options
    self.raw_data_view_combo = QComboBox()
    self.raw_data_view_combo.addItems(["Before", "After", "Side by Side", "Differences Only"])
    
    # Add to layout
    selector_layout.addWidget(file_label)
    selector_layout.addWidget(self.raw_data_file_combo, 1)
    selector_layout.addWidget(QLabel("View:"))
    selector_layout.addWidget(self.raw_data_view_combo)
    
    # Format options
    format_label = QLabel("Format:")
    self.raw_data_format_combo = QComboBox()
    self.raw_data_format_combo.addItems(["JSON", "Text", "Key-Value"])
    
    # Add to layout
    selector_layout.addWidget(format_label)
    selector_layout.addWidget(self.raw_data_format_combo)
    
    # Search box
    search_label = QLabel("Search:")
    self.raw_data_search = QLineEdit()
    self.raw_data_search.setPlaceholderText("Search raw data...")
    
    # Add to layout
    selector_layout.addWidget(search_label)
    selector_layout.addWidget(self.raw_data_search)
    
    # Connect signals
    self.raw_data_file_combo.currentIndexChanged.connect(self.on_raw_data_file_changed)
    self.raw_data_view_combo.currentIndexChanged.connect(self.on_raw_data_view_changed)
    self.raw_data_format_combo.currentIndexChanged.connect(self.on_raw_data_format_changed)
    self.raw_data_search.textChanged.connect(self.on_raw_data_search_changed)

def setup_raw_data_viewer(self):
    """Set up the raw data viewer component"""
    self.raw_data_viewer_container = QWidget()
    viewer_layout = QVBoxLayout(self.raw_data_viewer_container)
    viewer_layout.setContentsMargins(0, 0, 0, 0)
    
    # Create stacked widget for different view types
    self.raw_data_stack = QStackedWidget()
    
    # Single view (for Before or After)
    self.raw_data_single_view = QTextEdit()
    self.raw_data_single_view.setReadOnly(True)
    self.raw_data_single_view.setFont(QFont("Monospace", 10))
    self.raw_data_single_view.setObjectName("rawDataSingleView")
    
    # Side by side view
    self.raw_data_side_by_side = QSplitter(Qt.Orientation.Horizontal)
    
    self.raw_data_before_view = QTextEdit()
    self.raw_data_before_view.setReadOnly(True)
    self.raw_data_before_view.setFont(QFont("Monospace", 10))
    self.raw_data_before_view.setObjectName("rawDataBeforeView")
    
    self.raw_data_after_view = QTextEdit()
    self.raw_data_after_view.setReadOnly(True)
    self.raw_data_after_view.setFont(QFont("Monospace", 10))
    self.raw_data_after_view.setObjectName("rawDataAfterView")
    
    self.raw_data_side_by_side.addWidget(self.raw_data_before_view)
    self.raw_data_side_by_side.addWidget(self.raw_data_after_view)
    
    # Diff-only view
    self.raw_data_diff_view = QTextEdit()
    self.raw_data_diff_view.setReadOnly(True)
    self.raw_data_diff_view.setFont(QFont("Monospace", 10))
    self.raw_data_diff_view.setObjectName("rawDataDiffView")
    
    # Add views to stack
    self.raw_data_stack.addWidget(self.raw_data_single_view)
    self.raw_data_stack.addWidget(self.raw_data_side_by_side)
    self.raw_data_stack.addWidget(self.raw_data_diff_view)
    
    # Add toolbar with actions
    toolbar_layout = QHBoxLayout()
    
    self.raw_data_refresh_button = QPushButton("Refresh")
    self.raw_data_copy_button = QPushButton("Copy")
    self.raw_data_expand_button = QPushButton("Expand All")
    self.raw_data_collapse_button = QPushButton("Collapse All")
    self.raw_data_export_button = QPushButton("Export Data")
    
    toolbar_layout.addWidget(self.raw_data_refresh_button)
    toolbar_layout.addWidget(self.raw_data_copy_button)
    toolbar_layout.addWidget(self.raw_data_expand_button)
    toolbar_layout.addWidget(self.raw_data_collapse_button)
    toolbar_layout.addStretch()
    toolbar_layout.addWidget(self.raw_data_export_button)
    
    # Add components to layout
    viewer_layout.addLayout(toolbar_layout)
    viewer_layout.addWidget(self.raw_data_stack, 1)
    
    # Connect signals
    self.raw_data_refresh_button.clicked.connect(self.on_raw_data_refresh_clicked)
    self.raw_data_copy_button.clicked.connect(self.on_raw_data_copy_clicked)
    self.raw_data_expand_button.clicked.connect(self.on_raw_data_expand_clicked)
    self.raw_data_collapse_button.clicked.connect(self.on_raw_data_collapse_clicked)
    self.raw_data_export_button.clicked.connect(self.on_raw_data_export_clicked)

def on_raw_data_file_changed(self, index):
    """Handle raw data file selection change
    
    Args:
        index: Selected index in file combo
    """
    file_name = self.raw_data_file_combo.currentText()
    
    # Update raw data views based on selected file
    self.update_raw_data_views(file_name)

def on_raw_data_view_changed(self, index):
    """Handle raw data view type change
    
    Args:
        index: Selected index in view combo
    """
    view_type = self.raw_data_view_combo.currentText()
    
    # Switch to appropriate view
    if view_type == "Before" or view_type == "After":
        self.raw_data_stack.setCurrentIndex(0)  # Single view
    elif view_type == "Side by Side":
        self.raw_data_stack.setCurrentIndex(1)  # Side by side view
    elif view_type == "Differences Only":
        self.raw_data_stack.setCurrentIndex(2)  # Diff view
    
    # Update content
    self.update_raw_data_content()

def on_raw_data_format_changed(self, index):
    """Handle raw data format change
    
    Args:
        index: Selected index in format combo
    """
    # Update display format
    self.update_raw_data_content()

def on_raw_data_search_changed(self, text):
    """Handle search text change
    
    Args:
        text: Current search text
    """
    # Highlight search matches in raw data views
    self.highlight_raw_data_search(text)

def update_raw_data_views(self, file_name):
    """Update raw data views for the selected file
    
    Args:
        file_name: Name of the selected file
    """
    # Find the file data in comparison_data
    # For now, we'll use example data
    before_data = {"example": "before data", "nested": {"value": 123}}
    after_data = {"example": "after data", "nested": {"value": 456}, "new": "field"}
    
    # Update the views based on current format
    format_type = self.raw_data_format_combo.currentText()
    view_type = self.raw_data_view_combo.currentText()
    
    # Format the data
    before_content = self.format_raw_data(before_data, format_type)
    after_content = self.format_raw_data(after_data, format_type)
    diff_content = self.generate_raw_data_diff(before_data, after_data, format_type)
    
    # Update the appropriate views
    if view_type == "Before":
        self.raw_data_single_view.setText(before_content)
    elif view_type == "After":
        self.raw_data_single_view.setText(after_content)
    elif view_type == "Side by Side":
        self.raw_data_before_view.setText(before_content)
        self.raw_data_after_view.setText(after_content)
    elif view_type == "Differences Only":
        self.raw_data_diff_view.setText(diff_content)
    
    # Apply search highlighting if needed
    search_text = self.raw_data_search.text()
    if search_text:
        self.highlight_raw_data_search(search_text)

def format_raw_data(self, data, format_type):
    """Format raw data according to selected format
    
    Args:
        data: Raw data dictionary
        format_type: Selected format type
        
    Returns:
        Formatted string representation of the data
    """
    if format_type == "JSON":
        return json.dumps(data, indent=2, sort_keys=True)
    elif format_type == "Text":
        return str(data)
    elif format_type == "Key-Value":
        # Flatten and format as key-value pairs
        flat_data = self._flatten_dict(data)
        return "\n".join([f"{k}: {v}" for k, v in flat_data.items()])
    
    return str(data)

def generate_raw_data_diff(self, before_data, after_data, format_type):
    """Generate diff content showing changes between before and after data
    
    Args:
        before_data: Data before changes
        after_data: Data after changes
        format_type: Selected format type
        
    Returns:
        Formatted string showing differences
    """
    # Simple diff implementation for now
    diff_text = ""
    
    # Format both datasets
    before_text = self.format_raw_data(before_data, format_type)
    after_text = self.format_raw_data(after_data, format_type)
    
    # Process line by line
    before_lines = before_text.splitlines()
    after_lines = after_text.splitlines()
    
    # This is a very basic diff algorithm for demonstration
    # In a real implementation, you would use a proper diff library
    for line in before_lines:
        if line not in after_lines:
            diff_text += f"- {line}\n"
    
    for line in after_lines:
        if line not in before_lines:
            diff_text += f"+ {line}\n"
    
    return diff_text

def highlight_raw_data_search(self, search_text):
    """Highlight search matches in raw data views
    
    Args:
        search_text: Text to search for
    """
    if not search_text:
        return
    
    # Define format for highlights
    highlight_format = QTextCharFormat()
    highlight_format.setBackground(QColor(255, 255, 0, 100))  # Light yellow
    highlight_format.setForeground(QColor(0, 0, 0))  # Black text
    
    # Apply highlight to all text views
    view_type = self.raw_data_view_combo.currentText()
    
    if view_type == "Before" or view_type == "After":
        self._highlight_text_in_editor(self.raw_data_single_view, search_text, highlight_format)
    elif view_type == "Side by Side":
        self._highlight_text_in_editor(self.raw_data_before_view, search_text, highlight_format)
        self._highlight_text_in_editor(self.raw_data_after_view, search_text, highlight_format)
    elif view_type == "Differences Only":
        self._highlight_text_in_editor(self.raw_data_diff_view, search_text, highlight_format)

def _highlight_text_in_editor(self, editor, search_text, format):
    """Apply text highlighting to a QTextEdit widget
    
    Args:
        editor: QTextEdit widget to apply highlighting
        search_text: Text to search for
        format: QTextCharFormat to apply to matches
    """
    # Reset previous highlighting
    cursor = editor.textCursor()
    cursor.select(QTextCursor.SelectionType.Document)
    cursor.setCharFormat(QTextCharFormat())  # Default format
    cursor.clearSelection()
    editor.setTextCursor(cursor)
    
    # Apply new highlighting
    if not search_text:
        return
    
    # Create cursor for search
    cursor = editor.textCursor()
    cursor.movePosition(QTextCursor.MoveOperation.Start)
    
    # Regular cursor for search
    while True:
        cursor = editor.document().find(search_text, cursor)
        if cursor.isNull():
            break
        
        # Apply format
        cursor.mergeCharFormat(format)
