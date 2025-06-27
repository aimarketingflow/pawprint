#!/usr/bin/env python3
"""
Compare Screen - Embed Charts

Embeds chart images in HTML reports.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
import base64
import io

logger = logging.getLogger(__name__)

def embed_chart_images(self, chart_type='Bar Chart'):
    """Create embedded chart images for HTML report
    
    Args:
        chart_type: Type of chart to embed
        
    Returns:
        str: HTML with embedded chart images
    """
    try:
        # Check if matplotlib is available
        if not self.MATPLOTLIB_AVAILABLE:
            logger.warning("Cannot embed charts - matplotlib not available")
            return "<p>Charts could not be generated - matplotlib not available.</p>"
            
        # Create buffer for image
        buf = io.BytesIO()
        
        # Save current figure to buffer
        self.chart_figure.savefig(
            buf, 
            format='png', 
            dpi=100, 
            bbox_inches='tight',
            facecolor=self.chart_figure.get_facecolor()
        )
