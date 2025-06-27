#!/usr/bin/env python3
"""
Compare Screen - Refresh Chart

Handles chart refresh when comparison data changes.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def refresh_chart_on_data_change(self, before_file=None, after_file=None):
    """Refresh chart when comparison data changes
    
    Args:
        before_file: Optional path to before comparison file
        after_file: Optional path to after comparison file
        
    Returns:
        None
    """
    try:
        # Update file references if provided
        if before_file:
            self.before_file = before_file
        if after_file:
            self.after_file = after_file
            
        # Update chart display with new data
        success = self.update_chart_display()
        
        if not success:
            logger.warning("Failed to refresh chart with new comparison data")
            if hasattr(self, 'chart_widget'):
                self.chart_widget.setHidden(True)
        else:
            if hasattr(self, 'chart_widget'):
                self.chart_widget.setHidden(False)
                
        logger.debug("Chart refresh completed")
    except Exception as e:
        logger.error(f"Error refreshing chart: {str(e)}")
