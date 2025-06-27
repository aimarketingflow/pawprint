#!/usr/bin/env python3
"""
Compare Screen - Report Chart HTML

Generates HTML chart section for comparison reports.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def generate_report_chart_html(self, chart_image_data):
    """Generate HTML chart section for comparison report
    
    Args:
        chart_image_data: Base64 encoded chart image data
        
    Returns:
        str: HTML chart section
    """
    try:
        if not chart_image_data:
            logger.warning("No chart image data for chart section")
            return "<section class='chart-section'><h2>Visualization</h2><p>No chart data available.</p></section>"
            
        # Generate chart section HTML with embedded image
        html = f"""
        <section class="chart-section">
            <h2>Visualization</h2>
            <p>The following chart visualizes the comparison between patterns in the before and after files:</p>
            <div class="chart-container">
                <img src="{chart_image_data}" alt="Pattern Comparison Chart" class="chart-image">
            </div>
        </section>
        """
        
        logger.debug("Report chart HTML generated")
        return html
    except Exception as e:
        logger.error(f"Error generating report chart HTML: {str(e)}")
        return "<section class='chart-section'><h2>Visualization</h2><p>Error generating chart visualization.</p></section>"
