#!/usr/bin/env python3
"""
Compare Screen - Pattern Table Footer

Creates HTML footer for pattern details table.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def create_pattern_table_footer():
    """Create HTML footer for pattern details table
    
    Returns:
        str: HTML content for pattern table footer
    """
    try:
        # Close HTML table structure
        table_footer_html = """
            </tbody>
        </table>
        <div class="table-notes">
            <p>* Impact is determined by the percentage change and direction.</p>
        </div>
        """
        
        logger.debug("Pattern table footer HTML created")
        return table_footer_html
    except Exception as e:
        logger.error(f"Error creating pattern table footer: {str(e)}")
        return "</tbody></table>"
