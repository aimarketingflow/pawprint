#!/usr/bin/env python3
"""
Compare Screen - Draw Chart

Draws different chart types for pattern comparison visualization.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def draw_chart(self, chart_data, chart_type="Bar Chart"):
    """Draw chart visualization based on chart type
    
    Args:
        chart_data: Dictionary containing pattern comparison data
        chart_type: Type of chart to draw
        
    Returns:
        bool: Success status
    """
    try:
        # Check matplotlib availability
        if not hasattr(self, 'MATPLOTLIB_AVAILABLE'):
            self.check_matplotlib_availability()
            
        if not self.MATPLOTLIB_AVAILABLE:
            logger.warning("Cannot draw chart - matplotlib not available")
            return False
            
        # Check if we have chart figure and canvas
        if not hasattr(self, 'chart_figure') or not hasattr(self, 'canvas'):
            logger.warning("Chart figure or canvas not initialized")
            return False
            
        # Clear previous chart
        self.chart_figure.clear()
        
        # Get patterns data
        patterns = chart_data.get('patterns', {})
        if not patterns:
            logger.warning("No pattern data available for chart")
            return False
            
        # Process data for visualization
        pattern_names = []
        before_counts = []
        after_counts = []
        
        for name, data in patterns.items():
            pattern_names.append(name)
            before_counts.append(data.get('before', 0))
            after_counts.append(data.get('after', 0))
            
        # Limit number of patterns to display if too many
        max_patterns = 10
        if len(pattern_names) > max_patterns:
            pattern_names = pattern_names[:max_patterns]
            before_counts = before_counts[:max_patterns]
            after_counts = after_counts[:max_patterns]
            
        # Draw the selected chart type
        if chart_type == "Bar Chart":
            success = self._draw_bar_chart(pattern_names, before_counts, after_counts)
        elif chart_type == "Pie Chart":
            success = self._draw_pie_chart(pattern_names, before_counts, after_counts)
        elif chart_type == "Line Chart":
            success = self._draw_line_chart(pattern_names, before_counts, after_counts)
        elif chart_type == "Radar Chart":
            success = self._draw_radar_chart(pattern_names, before_counts, after_counts)
        else:
            # Default to bar chart
            success = self._draw_bar_chart(pattern_names, before_counts, after_counts)
            
        # Refresh canvas
        if success:
            self.canvas.draw()
            logger.info(f"Chart drawn successfully: {chart_type}")
            
        return success
    except Exception as e:
        logger.error(f"Error drawing chart: {str(e)}")
        return False
