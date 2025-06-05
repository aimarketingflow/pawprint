#!/usr/bin/env python3
"""
Pawprinting Database Core Module

Provides the core database connection and management functionality.

Author: AIMF LLC
Date: June 3, 2025
"""

import logging
import os
import sqlite3
from typing import Optional

# Import config paths
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config_paths import BASE_DIR

# Set up logging
logger = logging.getLogger(__name__)

class PawprintDatabase:
    """
    Manages database operations for the Pawprinting application.
    
    This class handles the core database connection and initialization.
    Specific operations are broken out into separate modules for maintainability.
    """
    
    DB_VERSION = 1  # For future schema migrations
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize the database manager.
        
        Args:
            db_path: Optional custom path to the database file
        """
        if db_path is None:
            db_path = os.path.join(BASE_DIR, 'database', 'pawprints.db')
        
        self.db_path = db_path
        self.db_dir = os.path.dirname(db_path)
        
        # Ensure database directory exists
        os.makedirs(self.db_dir, exist_ok=True)
        
        from .db_schema import create_database_schema
        create_database_schema(self.db_path, self.DB_VERSION)
        
        logger.info(f"PawprintDatabase initialized at {self.db_path}")
    
    def get_connection(self):
        """
        Get a connection to the SQLite database.
        
        Returns:
            sqlite3.Connection: A connection to the database
        """
        try:
            conn = sqlite3.connect(self.db_path)
            return conn
        except sqlite3.Error as e:
            logger.error(f"Error connecting to database: {e}")
            raise

# Singleton pattern for database access
_db_instance = None

def get_database() -> PawprintDatabase:
    """
    Get or create the global database instance.
    
    Returns:
        PawprintDatabase: The database instance
    """
    global _db_instance
    if _db_instance is None:
        _db_instance = PawprintDatabase()
    return _db_instance
