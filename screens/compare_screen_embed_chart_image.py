#!/usr/bin/env python3
"""
Compare Screen - Embed Chart Image

Encodes chart image for embedding in HTML reports.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
import io
import base64

logger = logging.getLogger(__name__)

def embed_chart_image(self):
    """Convert current chart to base64 for HTML embedding
    
    Returns:
        str: Base64 encoded image data or None on error
    """
    try:
        # Check if matplotlib is available
        if not hasattr(self, 'MATPLOTLIB_AVAILABLE'):
            self.check_matplotlib_availability()
            
        if not self.MATPLOTLIB_AVAILABLE or not hasattr(self, 'chart_figure'):
            logger.warning("Cannot embed chart - matplotlib not available or chart not created")
            return None
            
        # Save figure to in-memory buffer
        buf = io.BytesIO()
        self.chart_figure.savefig(buf, format='png', dpi=100, 
                                bbox_inches='tight', facecolor=self.chart_figure.get_facecolor())
        buf.seek(0)
        
        # Encode as base64
        img_str = base64.b64encode(buf.read()).decode('utf-8')
        
        # Create data URL for embedding in HTML
        img_data_url = f"data:image/png;base64,{img_str}"
        
        logger.debug("Chart image encoded for HTML embedding")
        return img_data_url
    except Exception as e:
        logger.error(f"Error embedding chart image: {str(e)}")
        return None
