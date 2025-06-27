#!/usr/bin/env python3
"""
Compare Screen for Pawprinting PyQt6 Application - Part 4c-3c: Pattern Analysis Methods

Implements the pattern analysis and explanation methods for the Compare Screen.

Author: AIMF LLC
Date: June 6, 2025
"""

# This file contains methods for pattern analysis that would be included in the CompareScreen class

def get_pattern_categories(self):
    """Get all unique pattern categories from comparison data
    
    Returns:
        list: List of unique pattern categories
    """
    categories = set()
    
    # Extract categories from all pattern changes
    for diff_key, diff_data in self.diff_cache.items():
        pattern_changes = diff_data.get("pattern_changes", [])
        for pattern in pattern_changes:
            categories.add(pattern.get("category", "Unknown"))
    
    # Convert to sorted list
    return sorted(list(categories))

def get_pattern_changes_by_category(self, category=None, threshold=0.0):
    """Get pattern changes filtered by category and threshold
    
    Args:
        category: Pattern category to filter by (None for all)
        threshold: Minimum absolute change threshold
        
    Returns:
        list: Filtered list of pattern changes
    """
    all_patterns = []
    
    # Extract patterns from all diff data
    for diff_key, diff_data in self.diff_cache.items():
        pattern_changes = diff_data.get("pattern_changes", [])
        all_patterns.extend(pattern_changes)
    
    # Remove duplicates by pattern key
    unique_patterns = {}
    for pattern in all_patterns:
        if pattern["key"] not in unique_patterns:
            unique_patterns[pattern["key"]] = pattern
    
    # Filter by category and threshold
    filtered_patterns = []
    for pattern in unique_patterns.values():
        # Apply category filter if provided
        if category and pattern.get("category") != category and category != "All":
            continue
            
        # Apply threshold filter
        if abs(pattern.get("change", 0.0)) < threshold:
            continue
            
        filtered_patterns.append(pattern)
    
    # Sort by absolute change magnitude (largest first)
    filtered_patterns.sort(key=lambda x: abs(x.get("change", 0.0)), reverse=True)
    
    return filtered_patterns

def generate_pattern_explanation(self, pattern_key):
    """Generate an explanation for a specific pattern's changes
    
    Args:
        pattern_key: Pattern identifier key
        
    Returns:
        dict: Pattern explanation details
    """
    # Find pattern in diff data
    pattern_data = None
    related_changes = []
    
    # Search all diffs for this pattern
    for diff_key, diff_data in self.diff_cache.items():
        pattern_changes = diff_data.get("pattern_changes", [])
        for pattern in pattern_changes:
            if pattern.get("key") == pattern_key:
                pattern_data = pattern
                break
                
        # Find related changes
        added = diff_data.get("added", {})
        removed = diff_data.get("removed", {})
        changed = diff_data.get("changed", {})
        
        # Look for keys that match pattern name
        pattern_name = pattern_key.split(".")[-1]
        for key in added:
            if pattern_name.lower() in key.lower():
                related_changes.append({
                    "key": key,
                    "change_type": "added",
                    "value": added[key]
                })
        
        for key in removed:
            if pattern_name.lower() in key.lower():
                related_changes.append({
                    "key": key,
                    "change_type": "removed",
                    "value": removed[key]
                })
                
        for key, value_dict in changed.items():
            if pattern_name.lower() in key.lower():
                related_changes.append({
                    "key": key,
                    "change_type": "changed",
                    "before": value_dict.get("before"),
                    "after": value_dict.get("after")
                })
                
        # Limit to top related changes
        if len(related_changes) > 10:
            break
    
    if not pattern_data:
        return {
            "name": pattern_key,
            "explanation": "Pattern details not found",
            "score_before": 0.0,
            "score_after": 0.0,
            "change": 0.0,
            "category": "Unknown",
            "description": "",
            "severity": "neutral",
            "related_changes": []
        }
    
    # Calculate severity level
    severity = "neutral"
    change = pattern_data.get("change", 0.0)
    if change > 0.1:
        severity = "major_improvement"
    elif change > 0.05:
        severity = "improvement"
    elif change > 0:
        severity = "minor_improvement"
    elif change < -0.1:
        severity = "major_regression"
    elif change < -0.05:
        severity = "regression"
    elif change < 0:
        severity = "minor_regression"
    
    # Generate explanation
    explanation = self._generate_pattern_change_explanation(pattern_data, related_changes)
    
    return {
        "name": pattern_data.get("name", pattern_key),
        "explanation": explanation,
        "score_before": pattern_data.get("before_score", 0.0),
        "score_after": pattern_data.get("after_score", 0.0),
        "change": pattern_data.get("change", 0.0),
        "percent_change": pattern_data.get("percent_change", 0.0),
        "category": pattern_data.get("category", "Unknown"),
        "description": pattern_data.get("description", ""),
        "severity": severity,
        "related_changes": related_changes[:10]  # Limit to top 10 related changes
    }

def _generate_pattern_change_explanation(self, pattern_data, related_changes):
    """Generate a natural language explanation for a pattern change
    
    Args:
        pattern_data: Pattern data dictionary
        related_changes: List of related changes
        
    Returns:
        str: Natural language explanation
    """
    name = pattern_data.get("name", "Unknown pattern")
    change = pattern_data.get("change", 0.0)
    percent_change = pattern_data.get("percent_change", 0.0)
    before_score = pattern_data.get("before_score", 0.0)
    after_score = pattern_data.get("after_score", 0.0)
    
    # Base explanation
    if change > 0:
        explanation = f"The <b>{name}</b> pattern shows an <span style='color:green'>improvement</span> "
        explanation += f"of <b>{change:.2f}</b> points "
        if before_score > 0:
            explanation += f"(<b>{percent_change:.1f}%</b> increase) "
        explanation += f"from {before_score:.2f} to {after_score:.2f}. "
    elif change < 0:
        explanation = f"The <b>{name}</b> pattern shows a <span style='color:red'>regression</span> "
        explanation += f"of <b>{abs(change):.2f}</b> points "
        if before_score > 0:
            explanation += f"(<b>{abs(percent_change):.1f}%</b> decrease) "
        explanation += f"from {before_score:.2f} to {after_score:.2f}. "
    else:
        explanation = f"The <b>{name}</b> pattern shows <span style='color:blue'>no change</span> "
        explanation += f"with a score of {before_score:.2f}. "
    
    # Add description if available
    description = pattern_data.get("description", "")
    if description:
        explanation += f"<p><b>Pattern Description:</b> {description}</p>"
    
    # Add information about related changes
    if related_changes:
        explanation += "<p><b>Related Changes:</b></p><ul>"
        for change in related_changes[:5]:  # Limit to top 5 for brevity
            change_type = change.get("change_type", "")
            key = change.get("key", "")
            
            if change_type == "added":
                explanation += f"<li><span style='color:green'>Added:</span> {key}</li>"
            elif change_type == "removed":
                explanation += f"<li><span style='color:red'>Removed:</span> {key}</li>"
            elif change_type == "changed":
                before = change.get("before", "")
                after = change.get("after", "")
                explanation += f"<li><span style='color:orange'>Changed:</span> {key}"
                if len(str(before)) < 50 and len(str(after)) < 50:
                    explanation += f" from '{before}' to '{after}'</li>"
                else:
                    explanation += " (value changed)</li>"
        
        if len(related_changes) > 5:
            explanation += f"<li>...and {len(related_changes) - 5} more related changes</li>"
            
        explanation += "</ul>"
        
    return explanation

def get_severity_color(self, severity):
    """Get color for severity level
    
    Args:
        severity: Severity level string
        
    Returns:
        str: Hex color code
    """
    severity_colors = {
        "major_improvement": "#00cc00",  # Bright green
        "improvement": "#66cc33",        # Green
        "minor_improvement": "#99cc66",  # Light green
        "neutral": "#808080",            # Gray
        "minor_regression": "#cc9966",   # Light red
        "regression": "#cc6633",         # Red
        "major_regression": "#cc0000"    # Bright red
    }
    
    return severity_colors.get(severity, "#808080")

def get_severity_icon(self, severity):
    """Get icon for severity level
    
    Args:
        severity: Severity level string
        
    Returns:
        str: Path to icon file
    """
    severity_icons = {
        "major_improvement": "icons/arrow_up_double.png",
        "improvement": "icons/arrow_up.png",
        "minor_improvement": "icons/arrow_up_small.png",
        "neutral": "icons/neutral.png",
        "minor_regression": "icons/arrow_down_small.png",
        "regression": "icons/arrow_down.png",
        "major_regression": "icons/arrow_down_double.png"
    }
    
    return severity_icons.get(severity, "icons/neutral.png")

def generate_top_findings(self):
    """Generate top findings from pattern changes
    
    Returns:
        list: List of top findings dictionaries
    """
    findings = []
    
    # Get all pattern changes across all diffs
    all_patterns = []
    for diff_key, diff_data in self.diff_cache.items():
        pattern_changes = diff_data.get("pattern_changes", [])
        all_patterns.extend(pattern_changes)
    
    # Remove duplicates by pattern key
    unique_patterns = {}
    for pattern in all_patterns:
        if pattern["key"] not in unique_patterns:
            unique_patterns[pattern["key"]] = pattern
    
    # Sort by absolute change (largest first)
    sorted_patterns = sorted(
        unique_patterns.values(),
        key=lambda x: abs(x.get("change", 0.0)),
        reverse=True
    )
    
    # Get top improvements
    top_improvements = [p for p in sorted_patterns if p.get("change", 0.0) > 0.05][:3]
    
    # Get top regressions
    top_regressions = [p for p in sorted_patterns if p.get("change", 0.0) < -0.05][:3]
    
    # Create findings
    for pattern in top_improvements:
        severity = "improvement"
        if pattern.get("change", 0.0) > 0.1:
            severity = "major_improvement"
            
        findings.append({
            "key": pattern.get("key", ""),
            "name": pattern.get("name", "Unknown"),
            "category": pattern.get("category", "Unknown"),
            "change": pattern.get("change", 0.0),
            "severity": severity,
            "type": "improvement",
            "description": f"{pattern.get('name', 'Pattern')} shows improvement of {pattern.get('change', 0.0):.2f}"
        })
    
    for pattern in top_regressions:
        severity = "regression"
        if pattern.get("change", 0.0) < -0.1:
            severity = "major_regression"
            
        findings.append({
            "key": pattern.get("key", ""),
            "name": pattern.get("name", "Unknown"),
            "category": pattern.get("category", "Unknown"),
            "change": pattern.get("change", 0.0),
            "severity": severity,
            "type": "regression",
            "description": f"{pattern.get('name', 'Pattern')} shows regression of {abs(pattern.get('change', 0.0)):.2f}"
        })
    
    # Add overall finding
    avg_change = sum(p.get("change", 0.0) for p in unique_patterns.values()) / max(1, len(unique_patterns))
    
    if avg_change > 0.03:
        findings.append({
            "key": "overall",
            "name": "Overall Comparison",
            "category": "Summary",
            "change": avg_change,
            "severity": "improvement",
            "type": "summary",
            "description": f"Overall positive change of {avg_change:.2f} across all patterns"
        })
    elif avg_change < -0.03:
        findings.append({
            "key": "overall",
            "name": "Overall Comparison",
            "category": "Summary",
            "change": avg_change,
            "severity": "regression",
            "type": "summary",
            "description": f"Overall negative change of {abs(avg_change):.2f} across all patterns"
        })
    else:
        findings.append({
            "key": "overall",
            "name": "Overall Comparison",
            "category": "Summary",
            "change": avg_change,
            "severity": "neutral",
            "type": "summary",
            "description": f"Minimal overall change of {abs(avg_change):.2f} across all patterns"
        })
    
    return findings
