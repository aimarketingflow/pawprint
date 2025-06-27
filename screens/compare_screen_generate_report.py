#!/usr/bin/env python3
"""
Compare Screen - Generate Report

Main report generation function that integrates all report modules.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)

def generate_comparison_report(self, chart_data, before_file, after_file, export_path):
    """Generate full HTML comparison report by integrating all report modules
    
    Args:
        chart_data: Chart data dictionary
        before_file: Before comparison file
        after_file: After comparison file
        export_path: Path to save the report
        
    Returns:
        tuple: (success, file_path)
    """
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        logger.info("Generating comparison report...")
        
        # Start with HTML header
        html_content = self.create_report_header("Pawprinting Comparison Report", timestamp)
        
        # Add summary section
        positive_changes, negative_changes, neutral_changes = self.get_report_summary_section(chart_data, before_file, after_file)
        total_patterns = len(chart_data.get('patterns', []))
        
        # Format summary with file info
        before_filename = os.path.basename(before_file) if before_file != "Unknown" else "Unknown"
        after_filename = os.path.basename(after_file) if after_file != "Unknown" else "Unknown"
        
        html_content += self.format_file_info_html(before_filename, after_filename)
        
        # Add statistics tables with styling
        pos_percent = (positive_changes / total_patterns * 100) if total_patterns > 0 else 0
        neg_percent = (negative_changes / total_patterns * 100) if total_patterns > 0 else 0
        neu_percent = (neutral_changes / total_patterns * 100) if total_patterns > 0 else 0
        
        html_content += self.create_stats_table(pos_percent, neg_percent, neu_percent, 
                                               positive_changes, negative_changes, 
                                               neutral_changes, total_patterns)
        
        html_content += self.format_stats_rows(pos_percent, neg_percent, neu_percent,
                                              positive_changes, negative_changes,
                                              neutral_changes, total_patterns)
        
        html_content += self.format_table_footer()
        
        # Add charts section if matplotlib available
        if self.MATPLOTLIB_AVAILABLE:
            html_content += self.format_charts_section_html(chart_data)
            
            # Add all chart types if available
            chart_types = ["Bar Chart", "Radar Chart", "Pie Chart"]
            for chart_type in chart_types:
                self.draw_chart(chart_data, chart_type)
                encoded_chart = self.encode_chart_to_base64(io.BytesIO())
                if encoded_chart:
                    html_content += self.create_chart_image_html(encoded_chart, chart_type)
            
            html_content += self.create_charts_section_footer()
        
        # Add patterns detail section
        html_content += self.create_patterns_section_html(chart_data)
        html_content += self.create_patterns_table_header()
        
        # Add individual pattern rows
        for pattern in chart_data.get('patterns', []):
            name = pattern.get('name', 'Unknown')
            category = pattern.get('category', 'Unknown')
            before = pattern.get('before_score', 0.0)
            after = pattern.get('after_score', 0.0)
            change = pattern.get('change', 0.0)
            percent = pattern.get('percent_change', 0.0)
            
            # Determine row color based on change
            if change > 0.05:
                change_color = "#03dac6"  # Teal for positive
            elif change < -0.05:
                change_color = "#cf6679"  # Red for negative
            else:
                change_color = "#bbbbbb"  # Gray for neutral
                
            html_content += self.create_pattern_row_html(name, category, before, after, 
                                                       change, percent, change_color)
        
        html_content += self.create_patterns_table_footer()
        
        # Add report footer
        html_content += self.create_report_footer(timestamp)
        
        # Save report to file
        file_path = os.path.join(export_path, f"pawprinting_comparison_report_{timestamp}.html")
        success = self.write_report_file(file_path, html_content)
        
        return success, file_path
        
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        return False, None
