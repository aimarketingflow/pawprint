#!/usr/bin/env python3
"""
Compare Screen - Patterns Table Footer

Creates HTML footer for patterns table in reports.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def create_patterns_table_footer(self):
    """Create HTML footer for patterns table
    
    Returns:
        str: HTML patterns table footer
    """
    # Create table footer with dark theme styling
    html = """
                    </tbody>
                </table>
            </div>
        </section>
    """
    return html
