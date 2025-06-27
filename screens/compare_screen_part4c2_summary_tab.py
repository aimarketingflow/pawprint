#!/usr/bin/env python3
"""
Compare Screen for Pawprinting PyQt6 Application - Part 4c-2: Summary Tab

Implements the Summary tab for the Compare Screen.

Author: AIMF LLC
Date: June 6, 2025
"""

# This file contains methods for the summary tab that would be included in the CompareScreen class

def setup_summary_tab(self):
    """Set up the summary tab for comparison overview"""
    self.summary_tab = QWidget()
    summary_layout = QVBoxLayout(self.summary_tab)
    
    # Create comparison metadata section
    self.setup_comparison_metadata()
    
    # Create key findings section
    self.setup_key_findings()
    
    # Create statistics section
    self.setup_statistics_section()
    
    # Add components to layout
    summary_layout.addWidget(self.comparison_metadata)
    summary_layout.addWidget(self.key_findings)
    summary_layout.addWidget(self.statistics_section, 1)
    
    # Add to tab widget
    self.tab_widget.addTab(self.summary_tab, "Summary")

def setup_comparison_metadata(self):
    """Set up the comparison metadata section"""
    self.comparison_metadata = QGroupBox("Comparison Information")
    metadata_layout = QFormLayout(self.comparison_metadata)
    
    # Create metadata fields
    self.date_time_label = QLabel("--")
    self.num_files_label = QLabel("--")
    self.origin_label = QLabel("--")
    self.pawprint_types_label = QLabel("--")
    
    # Add fields to form layout
    metadata_layout.addRow("Comparison Date:", self.date_time_label)
    metadata_layout.addRow("Number of Files:", self.num_files_label)
    metadata_layout.addRow("Origin:", self.origin_label)
    metadata_layout.addRow("Pawprint Types:", self.pawprint_types_label)

def setup_key_findings(self):
    """Set up the key findings section"""
    self.key_findings = QGroupBox("Key Findings")
    findings_layout = QVBoxLayout(self.key_findings)
    
    # Create scrollable area for findings
    findings_scroll = QScrollArea()
    findings_scroll.setWidgetResizable(True)
    findings_content = QWidget()
    findings_scroll_layout = QVBoxLayout(findings_content)
    findings_scroll_layout.setContentsMargins(0, 0, 0, 0)
    
    # Create findings list
    self.findings_list = QTextEdit()
    self.findings_list.setReadOnly(True)
    self.findings_list.setObjectName("findingsList")
    
    # Add to layout
    findings_scroll_layout.addWidget(self.findings_list)
    findings_scroll.setWidget(findings_content)
    findings_layout.addWidget(findings_scroll)
    
    # Export button
    self.export_findings_button = QPushButton("Export Findings Report")
    findings_layout.addWidget(self.export_findings_button)
    
    # Connect signals
    self.export_findings_button.clicked.connect(self.on_export_findings_clicked)

def setup_statistics_section(self):
    """Set up the statistics section"""
    self.statistics_section = QGroupBox("Comparison Statistics")
    stats_layout = QHBoxLayout(self.statistics_section)
    
    # Left column - File Changes
    file_changes = QGroupBox("File Changes")
    file_changes_layout = QFormLayout(file_changes)
    
    self.total_files_label = QLabel("--")
    self.added_files_label = QLabel("--")
    self.modified_files_label = QLabel("--")
    self.deleted_files_label = QLabel("--")
    self.unchanged_files_label = QLabel("--")
    
    file_changes_layout.addRow("Total Files:", self.total_files_label)
    file_changes_layout.addRow("Added:", self.added_files_label)
    file_changes_layout.addRow("Modified:", self.modified_files_label)
    file_changes_layout.addRow("Deleted:", self.deleted_files_label)
    file_changes_layout.addRow("Unchanged:", self.unchanged_files_label)
    
    # Middle column - Pattern Changes
    pattern_changes = QGroupBox("Pattern Score Changes")
    pattern_changes_layout = QFormLayout(pattern_changes)
    
    self.patterns_improved_label = QLabel("--")
    self.patterns_declined_label = QLabel("--")
    self.patterns_unchanged_label = QLabel("--")
    self.average_change_label = QLabel("--")
    self.largest_change_label = QLabel("--")
    
    pattern_changes_layout.addRow("Improved:", self.patterns_improved_label)
    pattern_changes_layout.addRow("Declined:", self.patterns_declined_label)
    pattern_changes_layout.addRow("Unchanged:", self.patterns_unchanged_label)
    pattern_changes_layout.addRow("Avg. Change:", self.average_change_label)
    pattern_changes_layout.addRow("Largest Change:", self.largest_change_label)
    
    # Right column - Visualization
    stats_viz = QGroupBox("Visualization")
    stats_viz_layout = QVBoxLayout(stats_viz)
    
    if MATPLOTLIB_AVAILABLE:
        # Create small chart
        self.summary_figure = Figure(figsize=(4, 4), dpi=100, tight_layout=True)
        self.summary_canvas = FigureCanvas(self.summary_figure)
        
        stats_viz_layout.addWidget(self.summary_canvas)
    else:
        # Fallback if matplotlib is not available
        no_mpl_label = QLabel("Matplotlib is required for visualization")
        no_mpl_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stats_viz_layout.addWidget(no_mpl_label)
    
    # Add view details button
    self.view_stats_details_button = QPushButton("View Detailed Statistics")
    stats_viz_layout.addWidget(self.view_stats_details_button)
    
    # Add columns to main layout
    stats_layout.addWidget(file_changes)
    stats_layout.addWidget(pattern_changes)
    stats_layout.addWidget(stats_viz)
    
    # Connect signals
    self.view_stats_details_button.clicked.connect(self.on_view_stats_details_clicked)

def update_summary_tab(self):
    """Update the summary tab with current comparison data"""
    # Update comparison metadata
    self.update_comparison_metadata()
    
    # Update key findings
    self.update_key_findings()
    
    # Update statistics
    self.update_statistics()

def update_comparison_metadata(self):
    """Update the comparison metadata section"""
    # In a real implementation, we would extract this from the comparison data
    # For now, use example values
    
    # Current date and time
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    self.date_time_label.setText(current_datetime)
    
    # Number of files
    num_files = len(self.comparison_files) if hasattr(self, 'comparison_files') else 0
    self.num_files_label.setText(str(num_files))
    
    # Origin
    self.origin_label.setText("Multiple" if num_files > 1 else "Unknown")
    
    # Pawprint types
    self.pawprint_types_label.setText("System Pawprints")

def update_key_findings(self):
    """Update the key findings section"""
    # In a real implementation, we would extract this from the comparison data
    # For now, use example findings
    
    findings_html = """
    <h3>Key Findings Summary</h3>
    <ul>
        <li><b style="color:#00cc00">Improved:</b> Directory Structure patterns show improvement (+0.07)</li>
        <li><b style="color:#cc0000">Regression:</b> File Permissions show decreased scores (-0.06)</li>
        <li><b style="color:#cc6600">Warning:</b> New network ports detected that weren't in the baseline</li>
        <li><b style="color:#00cc00">Improved:</b> Process Tree structure matches expected patterns better (+0.14)</li>
        <li><b style="color:#cc6600">Warning:</b> 3 files modified that are part of critical system components</li>
        <li><b style="color:#cc0000">Regression:</b> User permission changes detected that diverge from baseline (-0.09)</li>
    </ul>
    <p>Overall comparison shows a mixed pattern with both improvements and regressions.
    The process tree improvements are significant but are offset by permission changes.</p>
    <h4>Recommendations:</h4>
    <ol>
        <li>Review file permission changes in detail</li>
        <li>Investigate new network ports for potential security issues</li>
        <li>Monitor user permission changes for unauthorized access patterns</li>
    </ol>
    """
    
    self.findings_list.setHtml(findings_html)

def update_statistics(self):
    """Update the statistics section"""
    # File change statistics (example values)
    self.total_files_label.setText("124")
    self.added_files_label.setText("8 (6.5%)")
    self.modified_files_label.setText("17 (13.7%)")
    self.deleted_files_label.setText("3 (2.4%)")
    self.unchanged_files_label.setText("96 (77.4%)")
    
    # Pattern change statistics (example values)
    self.patterns_improved_label.setText("12 (48%)")
    self.patterns_declined_label.setText("7 (28%)")
    self.patterns_unchanged_label.setText("6 (24%)")
    self.average_change_label.setText("+0.03")
    self.largest_change_label.setText("+0.14 (Process Tree)")
    
    # Update summary chart
    self.update_summary_chart()

def update_summary_chart(self):
    """Update the summary chart in the statistics section"""
    if not MATPLOTLIB_AVAILABLE:
        return
    
    # Clear previous figure
    self.summary_figure.clear()
    
    # Create simple pie chart showing file change distribution
    ax = self.summary_figure.add_subplot(111)
    
    # Example data
    labels = ['Added', 'Modified', 'Deleted', 'Unchanged']
    sizes = [8, 17, 3, 96]
    colors = ['#4CAF50', '#FFC107', '#F44336', '#2196F3']
    explode = (0.1, 0.1, 0.1, 0)  # explode the first three slices
    
    ax.pie(sizes, explode=explode, labels=labels, colors=colors,
           autopct='%1.1f%%', shadow=True, startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    
    # Add title
    ax.set_title("File Change Distribution")
    
    # Draw the updated chart
    self.summary_canvas.draw()

def on_export_findings_clicked(self):
    """Handle export findings button click"""
    # In a real implementation, this would export the findings to a file
    file_name, _ = QFileDialog.getSaveFileName(
        self, "Export Findings", "", "HTML Files (*.html);;Text Files (*.txt)"
    )
    
    if file_name:
        try:
            # Get findings content based on format
            if file_name.endswith(".html"):
                content = self.findings_list.toHtml()
            else:
                content = self.findings_list.toPlainText()
            
            # Write to file
            with open(file_name, 'w') as f:
                f.write(content)
            
            logger.info(f"Findings exported to {file_name}")
            NotificationManager.show_info(f"Findings exported to {file_name}")
        except Exception as e:
            logger.error(f"Error exporting findings: {e}")
            NotificationManager.show_error(f"Error exporting findings: {e}")

def on_view_stats_details_clicked(self):
    """Handle view statistics details button click"""
    # Switch to charts tab
    self.tab_widget.setCurrentIndex(1)  # Assumes charts tab is index 1
