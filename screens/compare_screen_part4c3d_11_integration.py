#!/usr/bin/env python3
"""
Compare Screen - Part 4c-3d-11: Main Integration Module

Integrates all chart components into the CompareScreen class.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
from datetime import datetime

# Import required chart modules
from .compare_screen_part4c3d_1_chart_data_extraction import extract_chart_data
from .compare_screen_part4c3d_2_radar_chart import format_radar_chart_data, draw_radar_chart, generate_radar_html_description
from .compare_screen_part4c3d_3_bar_chart import format_bar_chart_data, draw_bar_chart, generate_bar_html_description
from .compare_screen_part4c3d_4_line_chart import format_line_chart_data, draw_line_chart, generate_line_html_description
from .compare_screen_part4c3d_5_pie_chart import format_pie_chart_data, draw_pie_chart, toggle_pie_chart_view, generate_pie_html_description
from .compare_screen_part4c3d_6_heatmap_chart import format_heatmap_chart_data, draw_heatmap_chart, toggle_heatmap_chart_view, generate_heatmap_html_description
from .compare_screen_part4c3d_7a_base_insights import generate_base_chart_insights
from .compare_screen_part4c3d_7b_advanced_insights import generate_advanced_chart_insights

# Import export modules
from .compare_screen_part4c3d_8a_chart_image_export import export_chart_image
from .compare_screen_part4c3d_8b_chart_data_csv_export import export_chart_csv_data
from .compare_screen_part4c3d_8c_summary_export import export_comparison_summary
from .compare_screen_part4c3d_8d_text_summary import _generate_text_summary
from .compare_screen_part4c3d_8e_html_report import export_html_report
from .compare_screen_part4c3d_8f_html_template import _generate_html_report
from .compare_screen_part4c3d_8g_html_sections import _get_html_files_section, _get_html_summary_section
from .compare_screen_part4c3d_8h_json_export import export_json_data
from .compare_screen_part4c3d_8i_json_data import _prepare_json_export_data

# Import UI components and handlers
from .compare_screen_part4c3d_9a_chart_widget import setup_chart_widget
from .compare_screen_part4c3d_9b_chart_theme import configure_chart_theme
from .compare_screen_part4c3d_9c_chart_display import display_chart
from .compare_screen_part4c3d_9d_chart_interaction import setup_chart_interactions, setup_view_toggle_buttons, show_chart_view_options
from .compare_screen_part4c3d_10a_charts_tab_ui import setup_charts_tab_ui
from .compare_screen_part4c3d_10b_charts_tab_buttons import setup_chart_buttons
from .compare_screen_part4c3d_10c_export_buttons import setup_export_buttons
from .compare_screen_part4c3d_10d_chart_controls import setup_chart_controls
from .compare_screen_part4c3d_10e_tab_layout import assemble_charts_tab_layout
from .compare_screen_part4c3d_10f_signals import connect_chart_signals, _handle_severity_change, _handle_category_filter_change, _handle_normalize_toggle
from .compare_screen_part4c3d_10g_export_dialogs import show_export_image_dialog
from .compare_screen_part4c3d_10h_csv_export_dialog import show_export_csv_dialog, _handle_report_export
from .compare_screen_part4c3d_10i_charts_tab_init import initialize_charts_tab

def integrate_charts_tab_into_compare_screen(CompareScreenClass):
    """Add all charts tab functionality to CompareScreen class
    
    Args:
        CompareScreenClass: The CompareScreen class to extend
    """
    # Add chart methods to CompareScreen class
    CompareScreenClass.extract_chart_data = extract_chart_data
    
    # Add chart type-specific methods
    CompareScreenClass.format_radar_chart_data = format_radar_chart_data
    CompareScreenClass.draw_radar_chart = draw_radar_chart
    CompareScreenClass.generate_radar_html_description = generate_radar_html_description
    
    CompareScreenClass.format_bar_chart_data = format_bar_chart_data
    CompareScreenClass.draw_bar_chart = draw_bar_chart
    CompareScreenClass.generate_bar_html_description = generate_bar_html_description
    
    CompareScreenClass.format_line_chart_data = format_line_chart_data
    CompareScreenClass.draw_line_chart = draw_line_chart
    CompareScreenClass.generate_line_html_description = generate_line_html_description
    
    CompareScreenClass.format_pie_chart_data = format_pie_chart_data
    CompareScreenClass.draw_pie_chart = draw_pie_chart
    CompareScreenClass.toggle_pie_chart_view = toggle_pie_chart_view
    CompareScreenClass.generate_pie_html_description = generate_pie_html_description
    
    CompareScreenClass.format_heatmap_chart_data = format_heatmap_chart_data
    CompareScreenClass.draw_heatmap_chart = draw_heatmap_chart
    CompareScreenClass.toggle_heatmap_chart_view = toggle_heatmap_chart_view
    CompareScreenClass.generate_heatmap_html_description = generate_heatmap_html_description
    
    # Add insights methods
    CompareScreenClass.generate_base_chart_insights = generate_base_chart_insights
    CompareScreenClass.generate_advanced_chart_insights = generate_advanced_chart_insights
    
    # Add export methods
    CompareScreenClass.export_chart_image = export_chart_image
    CompareScreenClass.export_chart_csv_data = export_chart_csv_data
    CompareScreenClass.export_comparison_summary = export_comparison_summary
    CompareScreenClass._generate_text_summary = _generate_text_summary
    CompareScreenClass.export_html_report = export_html_report
    CompareScreenClass._generate_html_report = _generate_html_report
    CompareScreenClass._get_html_files_section = _get_html_files_section
    CompareScreenClass._get_html_summary_section = _get_html_summary_section
    CompareScreenClass.export_json_data = export_json_data
    CompareScreenClass._prepare_json_export_data = _prepare_json_export_data
    
    # Add UI component methods
    CompareScreenClass.setup_chart_widget = setup_chart_widget
    CompareScreenClass.configure_chart_theme = configure_chart_theme
    CompareScreenClass.display_chart = display_chart
    CompareScreenClass.setup_chart_interactions = setup_chart_interactions
    CompareScreenClass.setup_view_toggle_buttons = setup_view_toggle_buttons
    CompareScreenClass.show_chart_view_options = show_chart_view_options
    CompareScreenClass.setup_charts_tab_ui = setup_charts_tab_ui
    CompareScreenClass.setup_chart_buttons = setup_chart_buttons
    CompareScreenClass.setup_export_buttons = setup_export_buttons
    CompareScreenClass.setup_chart_controls = setup_chart_controls
    CompareScreenClass.assemble_charts_tab_layout = assemble_charts_tab_layout
    CompareScreenClass.connect_chart_signals = connect_chart_signals
    CompareScreenClass._handle_severity_change = _handle_severity_change
    CompareScreenClass._handle_category_filter_change = _handle_category_filter_change
    CompareScreenClass._handle_normalize_toggle = _handle_normalize_toggle
    CompareScreenClass.show_export_image_dialog = show_export_image_dialog
    CompareScreenClass.show_export_csv_dialog = show_export_csv_dialog
    CompareScreenClass._handle_report_export = _handle_report_export
    
    # Add main initialization method
    CompareScreenClass.initialize_charts_tab = initialize_charts_tab
    
    # Log integration completion
    logging.info(f"Successfully integrated charts tab functionality into CompareScreen class: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
