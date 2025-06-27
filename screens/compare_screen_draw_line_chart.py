#!/usr/bin/env python3
"""
Compare Screen - Draw Line Chart

Draws line chart for pattern comparison visualization.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
import numpy as np

logger = logging.getLogger(__name__)

def _draw_line_chart(self, pattern_names, before_counts, after_counts):
    """Draw line chart for pattern comparison
    
    Args:
        pattern_names: List of pattern names
        before_counts: List of counts from before file
        after_counts: List of counts from after file
        
    Returns:
        bool: Success status
    """
    try:
        # Check if we have data to plot
        if not pattern_names or len(pattern_names) == 0:
            logger.warning("No pattern names for line chart")
            return False
            
        # Get axis for plotting
        ax = self.chart_figure.add_subplot(111)
        
        # Set up x positions
        x = np.arange(len(pattern_names))
        
        # Plot lines
        ax.plot(x, before_counts, marker='o', linestyle='-', linewidth=2, 
               color='#bb86fc', label='Before')
        ax.plot(x, after_counts, marker='s', linestyle='-', linewidth=2, 
               color='#03dac6', label='After')
        
        # Add fills for better visualization
        ax.fill_between(x, before_counts, alpha=0.3, color='#bb86fc')
        ax.fill_between(x, after_counts, alpha=0.3, color='#03dac6')
        
        # Add grid
        ax.grid(True, linestyle='--', alpha=0.3)
        
        # Add labels and title
        ax.set_xlabel('Patterns')
        ax.set_ylabel('Count')
        ax.set_title('Pattern Comparison: Before vs After')
        
        # Customize x-ticks
        if len(pattern_names) > 5:
            # If many patterns, rotate labels and show limited names
            truncated_names = [name[:12] + '...' if len(name) > 15 else name 
                             for name in pattern_names]
            ax.set_xticks(x)
            ax.set_xticklabels(truncated_names, rotation=45, ha='right')
        else:
            ax.set_xticks(x)
            ax.set_xticklabels(pattern_names)
            
        # Add value labels on data points
        for i, (before, after) in enumerate(zip(before_counts, after_counts)):
            ax.annotate(f'{before}', (i, before), textcoords="offset points", 
                       xytext=(0, 10), ha='center', fontsize=8, color='white')
            ax.annotate(f'{after}', (i, after), textcoords="offset points", 
                       xytext=(0, -15), ha='center', fontsize=8, color='white')
            
        # Add legend
        ax.legend(loc='best')
        
        # Style the chart
        ax.set_facecolor('#121212')  # Dark background
        self.chart_figure.patch.set_facecolor('#1e1e1e')  # Dark background
        
        # Style the text colors
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.title.set_color('#bb86fc')  # Neon purple
        ax.tick_params(colors='white')
        
        # Add a zero line for reference
        ax.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
        
        # Adjust layout to fit labels
        self.chart_figure.tight_layout()
        
        logger.debug("Line chart created successfully")
        return True
    except Exception as e:
        logger.error(f"Error creating line chart: {str(e)}")
        return False
