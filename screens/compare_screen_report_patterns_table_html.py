#!/usr/bin/env python3
"""
Compare Screen - Report Patterns Table HTML

Generates HTML table of patterns for comparison reports.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def generate_report_patterns_table_html(self, chart_data):
    """Generate HTML table of pattern details for comparison report
    
    Args:
        chart_data: Dictionary containing pattern comparison data
        
    Returns:
        str: HTML patterns table section
    """
    try:
        patterns = chart_data.get('patterns', {})
        if not patterns:
            logger.warning("No pattern data for patterns table")
            return "<section class='patterns-section'><h2>Pattern Details</h2><p>No pattern data available.</p></section>"
            
        # Start patterns table HTML
        html = """
        <section class="patterns-section">
            <h2>Pattern Details</h2>
            <table class="patterns-table">
                <thead>
                    <tr>
                        <th>Pattern</th>
                        <th>Before</th>
                        <th>After</th>
                        <th>Change</th>
                        <th>% Change</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        # Process pattern rows sorted by percent change (descending)
        pattern_rows = []
        for name, data in patterns.items():
            before = data.get('before', 0)
            after = data.get('after', 0)
            
            # Calculate change and percent change
            change = after - before
            
            if before == 0:
                if after == 0:
                    percent_change = 0  # No change (both zero)
                else:
                    percent_change = 100  # New pattern
            else:
                percent_change = (change / before) * 100
                
            # Create row entry
            pattern_rows.append({
                'name': name,
                'before': before,
                'after': after,
                'change': change,
                'percent_change': percent_change
            })
            
        # Sort by absolute percent change (largest changes first)
        pattern_rows.sort(key=lambda x: abs(x['percent_change']), reverse=True)
        
        # Generate rows
        for row in pattern_rows:
            # Determine styling class based on change
            if row['change'] > 0:
                change_class = "positive"
                arrow = "▲"
            elif row['change'] < 0:
                change_class = "negative"
                arrow = "▼"
            else:
                change_class = "neutral"
                arrow = "●"
                
            # Generate row HTML
            html += f"""
                <tr>
                    <td class="pattern-name">{row['name']}</td>
                    <td>{row['before']}</td>
                    <td>{row['after']}</td>
                    <td class="{change_class}">{arrow} {row['change']}</td>
                    <td class="{change_class} percentage">{row['percent_change']:.1f}%</td>
                </tr>
            """
            
        # Close table
        html += """
                </tbody>
            </table>
        </section>
        """
        
        logger.debug("Report patterns table HTML generated")
        return html
    except Exception as e:
        logger.error(f"Error generating patterns table HTML: {str(e)}")
        return "<section class='patterns-section'><h2>Pattern Details</h2><p>Error generating pattern details.</p></section>"
