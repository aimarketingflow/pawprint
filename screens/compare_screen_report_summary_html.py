#!/usr/bin/env python3
"""
Compare Screen - Report Summary HTML

Generates HTML summary section for comparison reports.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def generate_report_summary_html(self, chart_data):
    """Generate HTML summary section for comparison report
    
    Args:
        chart_data: Dictionary containing pattern comparison data
        
    Returns:
        str: HTML summary section
    """
    try:
        # Extract summary counts
        patterns = chart_data.get('patterns', {})
        if not patterns:
            logger.warning("No pattern data for summary section")
            return "<div class='summary-section'><h2>Summary</h2><p>No comparison data available.</p></div>"
            
        # Count pattern changes
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        
        for name, data in patterns.items():
            before = data.get('before', 0)
            after = data.get('after', 0)
            
            if after > before:
                positive_count += 1
            elif after < before:
                negative_count += 1
            else:
                neutral_count += 1
                
        total_count = positive_count + negative_count + neutral_count
        
        # Calculate percentages
        pos_percent = (positive_count / total_count * 100) if total_count > 0 else 0
        neg_percent = (negative_count / total_count * 100) if total_count > 0 else 0
        neu_percent = (neutral_count / total_count * 100) if total_count > 0 else 0
        
        # Generate summary HTML
        html = f"""
        <section class="summary-section">
            <h2>Summary</h2>
            <p>This report compares patterns between two pawprint files. A total of <strong>{total_count}</strong> patterns were analyzed.</p>
            
            <h3>Pattern Changes</h3>
            <p>
                <span class="positive">{positive_count} patterns increased</span> ({pos_percent:.1f}%)<br>
                <span class="negative">{negative_count} patterns decreased</span> ({neg_percent:.1f}%)<br>
                <span class="neutral">{neutral_count} patterns unchanged</span> ({neu_percent:.1f}%)
            </p>
            
            <p>Detailed analysis of each pattern is provided below.</p>
        </section>
        """
        
        logger.debug("Report summary HTML generated")
        return html
    except Exception as e:
        logger.error(f"Error generating report summary HTML: {str(e)}")
        return "<div class='summary-section'><h2>Summary</h2><p>Error generating summary.</p></div>"
