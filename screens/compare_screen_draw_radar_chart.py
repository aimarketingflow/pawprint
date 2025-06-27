#!/usr/bin/env python3
"""
Compare Screen - Draw Radar Chart

Draws radar (spider) chart for pattern comparison visualization.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
import numpy as np

logger = logging.getLogger(__name__)

def _draw_radar_chart(self, pattern_names, before_counts, after_counts):
    """Draw radar (spider) chart for pattern comparison
    
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
            logger.warning("No pattern names for radar chart")
            return False
            
        # For radar chart, we need at least 3 patterns 
        if len(pattern_names) < 3:
            logger.warning("Need at least 3 patterns for radar chart")
            # Pad with empty patterns if needed
            while len(pattern_names) < 3:
                pattern_names.append("")
                before_counts.append(0)
                after_counts.append(0)
                
        # Limit to top 8 patterns for clarity
        if len(pattern_names) > 8:
            # Sort by the sum of before and after counts
            total_counts = [b + a for b, a in zip(before_counts, after_counts)]
            sorted_data = sorted(
                zip(pattern_names, before_counts, after_counts, total_counts),
                key=lambda x: x[3],
                reverse=True
            )
            sorted_data = sorted_data[:8]
            pattern_names = [item[0] for item in sorted_data]
            before_counts = [item[1] for item in sorted_data]
            after_counts = [item[2] for item in sorted_data]
        
        # Get axis for plotting
        ax = self.chart_figure.add_subplot(111, polar=True)
        
        # Set up angles for radar chart
        angles = np.linspace(0, 2*np.pi, len(pattern_names), endpoint=False).tolist()
        
        # Close the polygon by appending first point to end
        before_values = before_counts + [before_counts[0]]
        after_values = after_counts + [after_counts[0]]
        angles = angles + [angles[0]]
        
        # Pattern labels need to be repeated too for labels
        labels = pattern_names + [pattern_names[0]]
        
        # Plot radar chart
        ax.plot(angles, before_values, 'o-', linewidth=2, color='#bb86fc', label='Before')
        ax.fill(angles, before_values, alpha=0.25, color='#bb86fc')
        
        ax.plot(angles, after_values, 's-', linewidth=2, color='#03dac6', label='After')
        ax.fill(angles, after_values, alpha=0.25, color='#03dac6')
        
        # Set pattern labels
        ax.set_xticks(angles[:-1])
        
        # Truncate long pattern names
        truncated_names = [name[:10] + '...' if len(name) > 12 else name 
                         for name in pattern_names]
        ax.set_xticklabels(truncated_names, color='white')
        
        # Add value labels at points
        for i, (angle, before, after) in enumerate(zip(angles[:-1], before_counts, after_counts)):
            # Add before value
            ax.annotate(
                f"{before}", 
                xy=(angle, before),
                xytext=(0, 10),
                textcoords='offset points',
                ha='center',
                va='bottom',
                color='white',
                fontsize=8
            )
            
            # Add after value
            ax.annotate(
                f"{after}", 
                xy=(angle, after),
                xytext=(0, -15),
                textcoords='offset points',
                ha='center',
                va='top',
                color='white',
                fontsize=8
            )
        
        # Add legend
        ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
        
        # Style the chart
        ax.set_facecolor('#121212')  # Dark background
        self.chart_figure.patch.set_facecolor('#1e1e1e')  # Dark background
        
        # Configure grid and spokes
        ax.grid(True, color="gray", alpha=0.3)
        ax.spines['polar'].set_visible(False)
        
        # Add title
        ax.set_title('Pattern Comparison: Before vs After', color='#bb86fc')
        
        # Adjust layout
        self.chart_figure.tight_layout()
        
        logger.debug("Radar chart created successfully")
        return True
    except Exception as e:
        logger.error(f"Error creating radar chart: {str(e)}")
        return False
