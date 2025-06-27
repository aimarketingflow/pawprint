#!/usr/bin/env python3
"""
Compare Screen - Part 4c-3d-8g: HTML Report Sections

Generates individual HTML sections for reports.

Author: AIMF LLC
Date: June 6, 2025
"""

def _get_html_files_section(self):
    """Generate HTML for files section
    
    Returns:
        str: HTML section content
    """
    html = """
    <div class="section">
        <h2>Files Compared</h2>
    """
    
    # Add file information
    if hasattr(self, 'file_groups') and self.file_groups:
        for origin, files in self.file_groups.items():
            html += f"<h3>{origin}</h3><ul>"
            for file_info in files:
                filename = file_info.get("filename", "Unknown")
                path = file_info.get("path", "Unknown path")
                html += f"<li>{filename} <small>({path})</small></li>"
            html += "</ul>"
    else:
        html += "<p>No files selected for comparison.</p>"
    
    html += "</div>"
    return html

def _get_html_summary_section(self):
    """Generate HTML for summary section
    
    Returns:
        str: HTML section content
    """
    html = """
    <div class="section">
        <h2>Comparison Summary</h2>
    """
    
    # Pattern changes summary
    if hasattr(self, 'diff_cache') and self.diff_cache:
        diff = self.diff_cache.get('current_diff', {})
        added = diff.get('added', [])
        removed = diff.get('removed', [])
        changed = diff.get('changed', {})
        
        # Summary counts
        html += "<div class='summary-counts'>"
        html += f"<p><strong>Added Patterns:</strong> {len(added)}</p>"
        html += f"<p><strong>Removed Patterns:</strong> {len(removed)}</p>"
        html += f"<p><strong>Changed Patterns:</strong> {len(changed)}</p>"
        html += "</div>"
        
        # Top changes
        if hasattr(self, 'top_findings'):
            html += "<h3>Key Findings</h3>"
            html += "<ul>"
            
            for finding in self.top_findings.get('improvements', [])[:3]:
                html += f"<li class='improved'>{finding}</li>"
                
            for finding in self.top_findings.get('regressions', [])[:3]:
                html += f"<li class='regressed'>{finding}</li>"
                
            html += "</ul>"
    else:
        html += "<p>No comparison data available.</p>"
    
    html += "</div>"
    return html
