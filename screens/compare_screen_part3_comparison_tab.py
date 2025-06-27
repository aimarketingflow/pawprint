#!/usr/bin/env python3
"""
Compare Screen for Pawprinting PyQt6 Application - Part 3: Comparison Tab

Implements the main comparison tab for the Compare Screen.

Author: AIMF LLC
Date: June 6, 2025
"""

# This file contains methods for the comparison tab that would be included in the CompareScreen class

def setup_comparison_tab(self):
    """Set up the main comparison tab for visualizing differences"""
    self.comparison_tab = QWidget()
    comparison_layout = QVBoxLayout(self.comparison_tab)
    
    # Create a splitter for file explorer and comparison view
    self.comparison_splitter = QSplitter(Qt.Orientation.Horizontal)
    
    # Setup file explorer (left side)
    self.setup_file_explorer()
    
    # Setup comparison view (right side)
    self.setup_comparison_view()
    
    # Add components to splitter
    self.comparison_splitter.addWidget(self.file_explorer)
    self.comparison_splitter.addWidget(self.comparison_view_container)
    
    # Set stretch factors (content area should take more space)
    self.comparison_splitter.setStretchFactor(0, 0)  # File explorer doesn't stretch as much
    self.comparison_splitter.setStretchFactor(1, 1)  # Comparison view stretches more
    
    # Add splitter to layout
    comparison_layout.addWidget(self.comparison_splitter)
    
    # Add to tab widget
    self.tab_widget.addTab(self.comparison_tab, "Comparison")

def setup_file_explorer(self):
    """Set up the file explorer component"""
    self.file_explorer = QWidget()
    self.file_explorer.setObjectName("fileExplorer")
    self.file_explorer.setMinimumWidth(250)
    
    explorer_layout = QVBoxLayout(self.file_explorer)
    
    # Search bar
    search_layout = QHBoxLayout()
    self.explorer_search = QLineEdit()
    self.explorer_search.setPlaceholderText("Search files...")
    search_button = QPushButton(QIcon("icons/search.png"), "")
    search_layout.addWidget(self.explorer_search)
    search_layout.addWidget(search_button)
    
    # Filter tabs
    self.filter_tabs = QTabWidget()
    self.filter_tabs.setObjectName("filterTabs")
    
    # All changes tab
    self.all_changes_tab = QWidget()
    self.all_changes_list = QListWidget()
    all_changes_layout = QVBoxLayout(self.all_changes_tab)
    all_changes_layout.addWidget(self.all_changes_list)
    
    # Added files tab
    self.added_files_tab = QWidget()
    self.added_files_list = QListWidget()
    added_files_layout = QVBoxLayout(self.added_files_tab)
    added_files_layout.addWidget(self.added_files_list)
    
    # Deleted files tab
    self.deleted_files_tab = QWidget()
    self.deleted_files_list = QListWidget()
    deleted_files_layout = QVBoxLayout(self.deleted_files_tab)
    deleted_files_layout.addWidget(self.deleted_files_list)
    
    # Modified files tab
    self.modified_files_tab = QWidget()
    self.modified_files_list = QListWidget()
    modified_files_layout = QVBoxLayout(self.modified_files_tab)
    modified_files_layout.addWidget(self.modified_files_list)
    
    # Add tabs to filter tabs widget
    self.filter_tabs.addTab(self.all_changes_tab, "All Changes")
    self.filter_tabs.addTab(self.added_files_tab, "Added")
    self.filter_tabs.addTab(self.deleted_files_tab, "Deleted")
    self.filter_tabs.addTab(self.modified_files_tab, "Modified")
    
    # Group options
    group_layout = QHBoxLayout()
    self.group_label = QLabel("Group by:")
    self.group_combo = QComboBox()
    self.group_combo.addItems(["Origin", "Type", "Path", "None"])
    
    group_layout.addWidget(self.group_label)
    group_layout.addWidget(self.group_combo, 1)
    
    # Add components to explorer layout
    explorer_layout.addLayout(search_layout)
    explorer_layout.addWidget(self.filter_tabs, 1)
    explorer_layout.addLayout(group_layout)
    
    # Connect signals for file explorer
    self.explorer_search.textChanged.connect(self.on_file_search_changed)
    self.filter_tabs.currentChanged.connect(self.on_filter_tab_changed)
    self.all_changes_list.itemClicked.connect(self.on_file_item_clicked)
    self.added_files_list.itemClicked.connect(self.on_file_item_clicked)
    self.deleted_files_list.itemClicked.connect(self.on_file_item_clicked)
    self.modified_files_list.itemClicked.connect(self.on_file_item_clicked)
    self.group_combo.currentIndexChanged.connect(self.on_group_option_changed)

def setup_comparison_view(self):
    """Set up the comparison view component"""
    self.comparison_view_container = QWidget()
    comparison_view_layout = QVBoxLayout(self.comparison_view_container)
    
    # Pattern explanations section
    self.setup_pattern_explanations()
    
    # Diff view section
    self.setup_diff_view()
    
    # Add components to layout
    comparison_view_layout.addWidget(self.pattern_explanations, 1)
    comparison_view_layout.addWidget(self.diff_view_container, 2)

def setup_pattern_explanations(self):
    """Set up the pattern explanations component"""
    self.pattern_explanations = QGroupBox("Pattern Changes")
    explanations_layout = QVBoxLayout(self.pattern_explanations)
    
    # Create scrollable area for pattern explanations
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_content = QWidget()
    scroll_layout = QVBoxLayout(scroll_content)
    
    # Pattern score overview
    scores_container = QWidget()
    scores_layout = QHBoxLayout(scores_container)
    scores_layout.setContentsMargins(0, 0, 0, 0)
    
    # Add 4 example pattern score cards
    for i, pattern in enumerate(["Directory Structure", "File Permissions", "Startup Processes", "Network Services"]):
        score_card = self.create_pattern_score_card(pattern, 0.75 + i*0.05, 0.02 if i % 2 == 0 else -0.03)
        scores_layout.addWidget(score_card)
    
    # Main pattern explanation content
    self.pattern_content = QTextEdit()
    self.pattern_content.setReadOnly(True)
    self.pattern_content.setObjectName("patternContent")
    
    # Add components to scroll layout
    scroll_layout.addWidget(scores_container)
    scroll_layout.addWidget(self.pattern_content)
    
    # Set scroll content
    scroll_area.setWidget(scroll_content)
    explanations_layout.addWidget(scroll_area)
    
    # Action buttons
    buttons_layout = QHBoxLayout()
    self.view_charts_button = QPushButton("View Charts")
    self.expand_button = QPushButton("Expand All")
    
    buttons_layout.addWidget(self.view_charts_button)
    buttons_layout.addWidget(self.expand_button)
    buttons_layout.addStretch()
    
    explanations_layout.addLayout(buttons_layout)
    
    # Connect signals
    self.view_charts_button.clicked.connect(self.on_view_charts_clicked)
    self.expand_button.clicked.connect(self.on_expand_explanations_clicked)

def create_pattern_score_card(self, name, score, change):
    """Create a pattern score card for the explanations section
    
    Args:
        name: Pattern name
        score: Current pattern score (0-1)
        change: Score change from previous value (-1 to 1)
        
    Returns:
        QFrame containing the score card
    """
    card = QFrame()
    card.setFrameShape(QFrame.Shape.StyledPanel)
    card.setObjectName("scoreCard")
    
    card_layout = QVBoxLayout(card)
    
    # Pattern name
    name_label = QLabel(name)
    name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    name_label.setWordWrap(True)
    
    # Score display
    score_label = QLabel(f"{score:.2f}")
    score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    score_label.setObjectName("scoreValue")
    
    # Change indicator
    if change > 0:
        change_text = f"+{change:.2f} ↑"
        change_class = "scoreUp"
    elif change < 0:
        change_text = f"{change:.2f} ↓"
        change_class = "scoreDown"
    else:
        change_text = "No change"
        change_class = "scoreNeutral"
    
    change_label = QLabel(change_text)
    change_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    change_label.setObjectName(change_class)
    
    # Add to layout
    card_layout.addWidget(name_label)
    card_layout.addWidget(score_label)
    card_layout.addWidget(change_label)
    
    # Set styles based on score
    if score >= 0.8:
        card.setProperty("scoreType", "high")
    elif score >= 0.6:
        card.setProperty("scoreType", "medium")
    else:
        card.setProperty("scoreType", "low")
    
    # Apply style
    card.style().unpolish(card)
    card.style().polish(card)
    
    return card

def setup_diff_view(self):
    """Set up the diff view component"""
    self.diff_view_container = QGroupBox("File Changes")
    diff_layout = QVBoxLayout(self.diff_view_container)
    
    # Diff options
    options_layout = QHBoxLayout()
    
    # Diff type selection
    self.diff_type_group = QButtonGroup(self)
    
    self.line_diff_radio = QRadioButton("Line Diff")
    self.json_tree_radio = QRadioButton("JSON Tree")
    self.side_by_side_radio = QRadioButton("Side by Side")
    
    self.diff_type_group.addButton(self.line_diff_radio, 0)
    self.diff_type_group.addButton(self.json_tree_radio, 1)
    self.diff_type_group.addButton(self.side_by_side_radio, 2)
    
    self.line_diff_radio.setChecked(True)
    
    options_layout.addWidget(self.line_diff_radio)
    options_layout.addWidget(self.json_tree_radio)
    options_layout.addWidget(self.side_by_side_radio)
    options_layout.addStretch()
    
    # Diff actions
    self.expand_all_button = QPushButton("Expand All")
    self.copy_button = QPushButton("Copy")
    
    options_layout.addWidget(self.expand_all_button)
    options_layout.addWidget(self.copy_button)
    
    # Stacked widget for different diff views
    self.diff_stack = QStackedWidget()
    
    # Simple line diff view
    self.line_diff_view = QTextEdit()
    self.line_diff_view.setReadOnly(True)
    self.line_diff_view.setObjectName("lineDiffView")
    self.line_diff_view.setFont(QFont("Monospace", 10))
    
    # JSON tree diff view
    self.json_tree_view = QTreeWidget()
    self.json_tree_view.setHeaderLabels(["Key", "Value", "Change"])
    self.json_tree_view.setObjectName("jsonTreeView")
    
    # Side by side diff view
    self.side_by_side_view = QSplitter(Qt.Orientation.Horizontal)
    
    self.before_view = QTextEdit()
    self.before_view.setReadOnly(True)
    self.before_view.setObjectName("beforeView")
    self.before_view.setFont(QFont("Monospace", 10))
    
    self.after_view = QTextEdit()
    self.after_view.setReadOnly(True)
    self.after_view.setObjectName("afterView")
    self.after_view.setFont(QFont("Monospace", 10))
    
    self.side_by_side_view.addWidget(self.before_view)
    self.side_by_side_view.addWidget(self.after_view)
    
    # Add views to stack
    self.diff_stack.addWidget(self.line_diff_view)
    self.diff_stack.addWidget(self.json_tree_view)
    self.diff_stack.addWidget(self.side_by_side_view)
    
    # Add components to diff layout
    diff_layout.addLayout(options_layout)
    diff_layout.addWidget(self.diff_stack, 1)
    
    # Connect signals
    self.diff_type_group.idClicked.connect(self.on_diff_type_changed)
    self.expand_all_button.clicked.connect(self.on_expand_all_clicked)
    self.copy_button.clicked.connect(self.on_copy_diff_clicked)

def on_file_search_changed(self, text):
    """Handle search text changes in file explorer
    
    Args:
        text: Current search text
    """
    # Implement file filtering based on search text
    self.filter_files(text)

def on_filter_tab_changed(self, index):
    """Handle filter tab changes
    
    Args:
        index: Selected tab index
    """
    # Update displayed files based on selected filter tab
    self.update_file_lists(self.current_filter_type())

def on_file_item_clicked(self, item):
    """Handle file item selection
    
    Args:
        item: Selected QListWidgetItem
    """
    # Get file path from item data
    file_path = item.data(Qt.ItemDataRole.UserRole)
    
    # Update diff view to show this file
    self.show_file_diff(file_path)
    
    # Update pattern explanations for this file
    self.update_pattern_explanations(file_path)

def on_diff_type_changed(self, id):
    """Handle diff type selection change
    
    Args:
        id: Button ID of selected radio button
    """
    # Switch to corresponding diff view
    self.diff_stack.setCurrentIndex(id)
    
    # Update diff view content based on new type
    self.refresh_diff_view()

def show_file_diff(self, file_path):
    """Show diff for a specific file
    
    Args:
        file_path: Path of the file to show diff for
    """
    # This would contain logic to generate and display the diff
    # between versions of the specified file
    pass

def update_pattern_explanations(self, file_path):
    """Update pattern explanations based on selected file
    
    Args:
        file_path: Path of the selected file
    """
    # This would contain logic to update the pattern explanation
    # text based on the selected file
    pass

def current_filter_type(self):
    """Get the current filter type based on selected tab
    
    Returns:
        String representing the current filter type
    """
    index = self.filter_tabs.currentIndex()
    
    if index == 0:
        return "all"
    elif index == 1:
        return "added"
    elif index == 2:
        return "deleted"
    elif index == 3:
        return "modified"
    
    return "all"
