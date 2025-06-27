#!/usr/bin/env python3
"""
Compare Screen - Registry Category Handler

Handles registry-specific pattern categorization.

Author: AIMF LLC
Date: June 6, 2025
"""

def get_registry_category(self, pattern_name):
    """Determine if pattern falls into Registry category
    
    Args:
        pattern_name: Name of the pattern
        
    Returns:
        bool: True if pattern is registry-related
    """
    registry_terms = ['_registry_', '_reg_', '_key_', '_hkey_', '_regedit_']
    
    for term in registry_terms:
        if term in pattern_name.lower():
            return True
            
    # Check for registry hive prefixes
    hive_prefixes = ['hkcr', 'hkcu', 'hklm', 'hku', 'hkcc']
    
    for prefix in hive_prefixes:
        if pattern_name.lower().startswith(prefix):
            return True
            
    return False
