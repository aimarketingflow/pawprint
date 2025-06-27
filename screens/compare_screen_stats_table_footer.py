#!/usr/bin/env python3
"""
Compare Screen - Stats Table Footer

Creates HTML table footer for statistics section.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def format_table_footer(self):
    """Format HTML statistics table footer
    
    Returns:
        str: HTML statistics table footer
    """
    # Create table footer
    html = """
                    </tbody>
                </table>
            </div>
        </section>
    """
    return html
