#!/usr/bin/env python3
"""
Compare Screen - Draw Pie Chart

Draws pie chart for pattern comparison visualization.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
import numpy as np

logger = logging.getLogger(__name__)

def _draw_pie_chart(self, pattern_names, before_counts, after_counts):
    """Draw pie chart for pattern comparison
    
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
            logger.warning("No pattern names for pie chart")
            return False
            
        # Create subplots for before and after
        ax1 = self.chart_figure.add_subplot(121)
        ax2 = self.chart_figure.add_subplot(122)
        
        # Limit number of patterns for pie chart
        max_patterns = 6
        if len(pattern_names) > max_patterns:
            # Group others for clarity
            sorted_before = sorted(zip(pattern_names, before_counts), 
                                 key=lambda x: x[1], reverse=True)
            sorted_after = sorted(zip(pattern_names, after_counts), 
                                key=lambda x: x[1], reverse=True)
                                
            top_before_names = [item[0] for item in sorted_before[:max_patterns-1]]
            top_before_counts = [item[1] for item in sorted_before[:max_patterns-1]]
            top_before_names.append('Others')
            top_before_counts.append(sum(item[1] for item in sorted_before[max_patterns-1:]))
            
            top_after_names = [item[0] for item in sorted_after[:max_patterns-1]]
            top_after_counts = [item[1] for item in sorted_after[:max_patterns-1]]
            top_after_names.append('Others')
            top_after_counts.append(sum(item[1] for item in sorted_after[max_patterns-1:]))
            
            pattern_names_before = top_before_names
            before_counts = top_before_counts
            pattern_names_after = top_after_names
            after_counts = top_after_counts
        else:
            pattern_names_before = pattern_names
            pattern_names_after = pattern_names
        
        # Color palette
        colors = ['#bb86fc', '#03dac6', '#cf6679', '#4caf50', '#2196f3', '#ff9800']
        if len(pattern_names_before) > len(colors):
            # Extend color palette if needed
            colors = colors * (len(pattern_names_before) // len(colors) + 1)
            
        # Plot before pie chart
        wedges1, texts1, autotexts1 = ax1.pie(
            before_counts, 
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            wedgeprops={'edgecolor': '#121212', 'linewidth': 1}
        )
        
        # Plot after pie chart
        wedges2, texts2, autotexts2 = ax2.pie(
            after_counts, 
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            wedgeprops={'edgecolor': '#121212', 'linewidth': 1}
        )
        
        # Make text readable
        for text in autotexts1 + autotexts2:
            text.set_color('black')
            text.set_fontsize(8)
            text.set_fontweight('bold')
        
        # Add titles
        ax1.set_title('Before', color='#bb86fc')
        ax2.set_title('After', color='#03dac6')
        
        # Add legends outside the pie
        ax1.legend(
            wedges1, pattern_names_before,
            loc="center left",
            bbox_to_anchor=(-0.1, 0, 0.5, 1),
            fontsize=8,
            frameon=False
        )
        
        ax2.legend(
            wedges2, pattern_names_after,
            loc="center right",
            bbox_to_anchor=(1.1, 0, 0.5, 1),
            fontsize=8,
            frameon=False
        )
        
        # Style the chart background
        self.chart_figure.patch.set_facecolor('#1e1e1e')
        
        # Equal aspect ratio for pie charts
        ax1.set_aspect('equal')
        ax2.set_aspect('equal')
        
        # Adjust layout to fit legends
        self.chart_figure.tight_layout()
        
        logger.debug("Pie chart created successfully")
        return True
    except Exception as e:
        logger.error(f"Error creating pie chart: {str(e)}")
        return False
