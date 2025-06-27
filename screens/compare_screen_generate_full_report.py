#!/usr/bin/env python3
"""
Compare Screen - Generate Full Report

Generates complete HTML comparison report by combining all sections.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)

def generate_comparison_report(self, chart_data, before_file, after_file, export_path):
    """Generate complete HTML comparison report
    
    Args:
        chart_data: Dictionary containing pattern comparison data
        before_file: Path to before comparison file
        after_file: Path to after comparison file
        export_path: Directory to save the report
        
    Returns:
        tuple: (Success status, report file path)
    """
    try:
        from .compare_screen_custom_report_css import get_custom_report_css
        from .compare_screen_report_header_html import generate_report_header_html
        from .compare_screen_report_summary_html import generate_report_summary_html
        from .compare_screen_report_chart_html import generate_report_chart_html
        from .compare_screen_report_patterns_table_html import generate_report_patterns_table_html
        from .compare_screen_report_footer_html import generate_report_footer_html
        from .compare_screen_generate_report_filename import generate_report_filename
        from .compare_screen_embed_chart_image import embed_chart_image
        
        logger.info("Starting HTML report generation")
        
        # Get chart image for report if available
        chart_image_data = None
        if self.MATPLOTLIB_AVAILABLE and hasattr(self, 'chart_figure'):
            # Generate chart image
            current_chart_type = self.chart_selector.currentText() if hasattr(self, 'chart_selector') else "Bar Chart"
            success = self.draw_chart(chart_data, current_chart_type)
            if success:
                chart_image_data = self.embed_chart_image()
        
        # Generate the report filename with timestamp
        report_filename = self.generate_report_filename(before_file, after_file)
        report_file_path = os.path.join(export_path, report_filename)
        
        # Generate HTML content for each section
        header_html = self.generate_report_header_html(before_file, after_file)
        summary_html = self.generate_report_summary_html(chart_data)
        chart_html = self.generate_report_chart_html(chart_image_data) if chart_image_data else ""
        patterns_table_html = self.generate_report_patterns_table_html(chart_data)
        footer_html = self.generate_report_footer_html()
        
        # Get CSS styling
        css = get_custom_report_css()
        
        # Combine all sections into full HTML
        header_with_css = header_html.replace("/* CSS will be inserted here */", css)
        full_html = header_with_css + summary_html + chart_html + patterns_table_html + footer_html
        
        # Make sure export directory exists
        os.makedirs(export_path, exist_ok=True)
        
        # Write HTML to file
        with open(report_file_path, 'w') as f:
            f.write(full_html)
            
        logger.info(f"HTML report generated: {report_file_path}")
        return True, report_file_path
    except Exception as e:
        logger.error(f"Error generating HTML report: {str(e)}")
        return False, None
