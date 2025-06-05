#!/usr/bin/env python3
"""
Pawprinting Database Module

Provides database management functionality for storing and retrieving
pawprint generations and user configurations.

This module consists of multiple components broken down into individual files
for better organization and maintenance.

Author: AIMF LLC
Date: June 3, 2025
"""

from .db_core import get_database, PawprintDatabase
from .db_schema import create_database_schema
from .db_operations import (
    import_existing_configs,
    add_pawprint,
    get_recent_pawprints,
    search_pawprints,
    get_pawprint_by_id,
    delete_pawprint,
    update_pawprint
)
from .db_statistics import get_database_stats, get_run_history
