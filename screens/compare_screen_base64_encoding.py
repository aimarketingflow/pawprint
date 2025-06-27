#!/usr/bin/env python3
"""
Compare Screen - Base64 Encoding

Handles base64 encoding for chart image embedding in HTML reports.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
import base64

logger = logging.getLogger(__name__)

def encode_chart_to_base64(self, buf):
    """Encode chart image buffer to base64 for HTML embedding
    
    Args:
        buf: BytesIO buffer containing chart image
        
    Returns:
        str: Base64 encoded chart image
    """
    try:
        # Get buffer value and encode as base64
        buf.seek(0)
        img_bytes = buf.getvalue()
        encoded = base64.b64encode(img_bytes).decode('utf-8')
        
        return encoded
    except Exception as e:
        logger.error(f"Error encoding chart image: {str(e)}")
        return ""
