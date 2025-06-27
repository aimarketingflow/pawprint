#!/usr/bin/env python3
"""
Compare Screen - Draw Bar Chart

Draws bar chart for pattern comparison visualization.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
import numpy as np

logger = logging.getLogger(__name__)

def _draw_bar_chart(self, pattern_names, before_counts, after_counts):
    """Draw bar chart for pattern comparison
    
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
            logger.warning("No pattern names for bar chart")
            return False
            
        # Get axis for plotting
        ax = self.chart_figure.add_subplot(111)
        
        # Set up bar positions and width
        x = np.arange(len(pattern_names))
        width = 0.35
        
        # Plot bars
        before_bars = ax.bar(x - width/2, before_counts, width, label='Before', color='#bb86fc')
        after_bars = ax.bar(x + width/2, after_counts, width, label='After', color='#03dac6')
        
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
            
        # Add legend
        ax.legend()
        
        # Add value labels on top of bars
        def add_labels(bars):
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'{height}',
                          xy=(bar.get_x() + bar.get_width() / 2, height),
                          xytext=(0, 3),
                          textcoords="offset points",
                          ha='center', va='bottom',
                          color='white', fontsize=8)
                          
        add_labels(before_bars)
        add_labels(after_bars)
        
        # Style the chart
        ax.set_facecolor('#121212')  # Dark background
        self.chart_figure.patch.set_facecolor('#1e1e1e')  # Dark background
        
        # Style the grid
        ax.grid(True, linestyle='--', alpha=0.3)
        
        # Style the text colors
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.title.set_color('#bb86fc')  # Neon purple
        ax.tick_params(colors='white')
        
        # Adjust layout to fit labels
        self.chart_figure.tight_layout()
        
        logger.debug("Bar chart created successfully")
        return True
    except Exception as e:
        logger.error(f"Error creating bar chart: {str(e)}")
        return False
