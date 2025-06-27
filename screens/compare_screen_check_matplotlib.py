#!/usr/bin/env python3
"""
Compare Screen - Check Matplotlib

Checks if matplotlib is available for chart functionality.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def check_matplotlib_availability(self):
    """Check if matplotlib is available
    
    Sets MATPLOTLIB_AVAILABLE flag on self
    
    Returns:
        bool: True if matplotlib is available, False otherwise
    """
    try:
        import matplotlib
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
        
        # Set flag for availability
        self.MATPLOTLIB_AVAILABLE = True
        logger.info("Matplotlib available - chart functionality enabled")
        return True
    except ImportError as e:
        # Set flag for unavailability
        self.MATPLOTLIB_AVAILABLE = False
        logger.warning(f"Matplotlib not available - chart functionality disabled: {e}")
        return False
    except Exception as e:
        # Set flag for unavailability due to unexpected error
        self.MATPLOTLIB_AVAILABLE = False
        logger.error(f"Unexpected error checking matplotlib availability: {e}")
        return False
