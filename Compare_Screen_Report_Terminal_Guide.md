# Pawprinting PyQt6 V2 Compare Screen Report Terminal Guide

## Overview

This guide documents the modular report generation components in the Compare Screen. These modules provide functionality for generating detailed HTML comparison reports, chart visualizations, data exports, and user notifications.

## Module Structure

The Compare Screen report functionality is organized into the following modules:

### Report Generation
- `compare_screen_generate_full_report.py` - Main function to generate complete HTML report
- `compare_screen_report_header_html.py` - HTML header with document structure
- `compare_screen_report_summary_html.py` - Summary section with overall pattern changes
- `compare_screen_report_chart_html.py` - Chart visualization section 
- `compare_screen_report_patterns_table_html.py` - Detailed pattern comparison table
- `compare_screen_report_footer_html.py` - Report footer with timestamp and copyright
- `compare_screen_custom_report_css.py` - CSS styling for dark theme reports
- `compare_screen_generate_report_filename.py` - Timestamped filename generation

### Chart Visualization
- `compare_screen_check_matplotlib.py` - Availability check for matplotlib
- `compare_screen_draw_chart.py` - Main chart drawing dispatcher
- `compare_screen_draw_bar_chart.py` - Bar chart implementation
- `compare_screen_draw_pie_chart.py` - Pie chart implementation  
- `compare_screen_draw_line_chart.py` - Line chart implementation
- `compare_screen_draw_radar_chart.py` - Radar chart implementation
- `compare_screen_embed_chart_image.py` - Encoding chart for HTML embedding
- `compare_screen_save_chart_image.py` - Save chart as PNG file

### UI Components
- `compare_screen_create_chart_selector.py` - Chart type dropdown
- `compare_screen_create_chart_display.py` - Chart display widget
- `compare_screen_create_report_button.py` - Report generation button
- `compare_screen_create_export_button.py` - Data export button
- `compare_screen_create_save_chart_button.py` - Chart image save button

### Event Handling
- `compare_screen_connect_report_button.py` - Connect report button events
- `compare_screen_connect_export_button.py` - Connect export button events  
- `compare_screen_connect_save_chart_button.py` - Connect save button events
- `compare_screen_report_button_handler.py` - Report button click handler
- `compare_screen_export_data_handler.py` - Export data button click handler
- `compare_screen_charts_unavailable.py` - Fallback UI when matplotlib missing

### User Interaction
- `compare_screen_open_report.py` - Open report in browser
- `compare_screen_report_success_notification.py` - Success notification dialog
- `compare_screen_handle_report_completion.py` - Post-report actions
- `compare_screen_data_export_notification.py` - Data export notification
- `compare_screen_error_dialog.py` - Error dialogs with dark styling

### File Operations  
- `compare_screen_write_json_data.py` - Write JSON data export
- `compare_screen_export_path_manager.py` - Manage export paths/directories

### Integration
- `compare_screen_report_integration.py` - Main integration point
- `compare_screen_action_buttons_layout.py` - Button layout arrangement
- `compare_screen_chart_panel_layout.py` - Chart panel layout
- `compare_screen_chart_panel_widget.py` - Chart panel widget

## Example Usage

To run the report generation functionality:

```python
# In Compare Screen class:

# Initialize report functionality
self.integrate_report_functionality()

# On report button click:
def on_report_button_clicked(self):
    chart_data = self.extract_chart_data() 
    export_path = self.get_export_path("report")
    success, file_path = self.generate_comparison_report(
        chart_data, self.before_file, self.after_file, export_path
    )
    self.handle_report_completion(success, file_path)
```

## Dependencies

- `PyQt6` - UI components and dialogs
- `matplotlib` - Chart generation (with runtime availability check)
- `os`, `datetime`, `logging` - Standard libraries
- `base64` - Image embedding in HTML reports

## Export Paths

Reports and data are organized in the user's Documents folder:

- `~/Documents/Pawprinting_Exports/reports/` - HTML comparison reports
- `~/Documents/Pawprinting_Exports/data/` - JSON data exports
- `~/Documents/Pawprinting_Exports/images/` - PNG chart images

## Error Handling

All modules implement comprehensive error handling and logging:

- Graceful fallbacks when matplotlib is unavailable
- File operation error detection
- User-friendly error notifications with dark styling
- Detailed logging of operations and failures
