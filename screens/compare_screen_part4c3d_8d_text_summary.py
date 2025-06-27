#!/usr/bin/env python3
"""
Compare Screen - Part 4c-3d-8d: Text Summary Generator

Generates text summaries for comparison results.

Author: AIMF LLC
Date: June 6, 2025
"""

from datetime import datetime

def _generate_text_summary(self):
    """Generate plain text summary of comparison
    
    Returns:
        str: Formatted text summary
    """
    summary = []
    summary.append("PAWPRINTING COMPARISON SUMMARY")
    summary.append("=" * 30)
    summary.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Files info
    if hasattr(self, 'file_groups') and self.file_groups:
        summary.append("FILES COMPARED:")
        for origin, files in self.file_groups.items():
            summary.append(f"  {origin}: {len(files)} file(s)")
    
    # Pattern changes
    if hasattr(self, 'diff_cache') and self.diff_cache:
        diff = self.diff_cache.get('current_diff', {})
        added = len(diff.get('added', []))
        removed = len(diff.get('removed', []))
        changed = len(diff.get('changed', []))
        unchanged = len(diff.get('unchanged', []))
        
        summary.append("\nPATTERN CHANGES:")
        summary.append(f"  Added: {added}")
        summary.append(f"  Removed: {removed}")
        summary.append(f"  Changed: {changed}")
        summary.append(f"  Unchanged: {unchanged}")
    
    return "\n".join(summary)
