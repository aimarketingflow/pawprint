#!/usr/bin/env python3
"""
Pawprinting Database Schema Module

Handles creating and updating the database schema including
tables, indices, and constraints.

Author: AIMF LLC
Date: June 3, 2025
"""

import logging
import os
import sqlite3
from typing import Optional

# Set up logging
logger = logging.getLogger(__name__)

def create_database_schema(db_path: str, db_version: int) -> None:
    """
    Initialize or update the database schema.
    
    Args:
        db_path: Path to the SQLite database file
        db_version: Current schema version number
    """
    try:
        # Connect to database (creates file if it doesn't exist)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if the database already has the necessary tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='pawprints'")
        tables = cursor.fetchall()
        
        if not tables:
            logger.info("Creating database schema...")
            
            # Create tables with appropriate schema
            cursor.execute('''
            CREATE TABLE db_info (
                key TEXT PRIMARY KEY,
                value TEXT
            )
            ''')
            
            cursor.execute('''
            CREATE TABLE pawprints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                created_at TEXT NOT NULL,
                signature TEXT NOT NULL,
                text_input TEXT,
                json_config TEXT NOT NULL,
                file_path TEXT,
                text_entropy REAL,
                tags TEXT
            )
            ''')
            
            cursor.execute('''
            CREATE TABLE runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pawprint_id INTEGER NOT NULL,
                run_timestamp TEXT NOT NULL,
                notes TEXT,
                FOREIGN KEY (pawprint_id) REFERENCES pawprints (id)
            )
            ''')
            
            # Create indices for faster lookups
            cursor.execute('CREATE INDEX idx_pawprints_signature ON pawprints(signature)')
            cursor.execute('CREATE INDEX idx_pawprints_created_at ON pawprints(created_at)')
            
            # Store database version
            cursor.execute('INSERT INTO db_info (key, value) VALUES (?, ?)', ('version', str(db_version)))
            
            conn.commit()
            logger.info("Database schema created successfully")
        else:
            # Check if we need to perform schema migrations
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='db_info'")
            has_db_info = cursor.fetchall()
            
            current_version = 0
            if has_db_info:
                cursor.execute("SELECT value FROM db_info WHERE key='version'")
                version_row = cursor.fetchone()
                if version_row:
                    current_version = int(version_row[0])
            
            if current_version < db_version:
                # Perform migrations here when needed in future updates
                logger.info(f"Migrating database from version {current_version} to {db_version}")
                
                # Update version number
                if has_db_info:
                    cursor.execute("UPDATE db_info SET value = ? WHERE key = 'version'", (str(db_version),))
                else:
                    cursor.execute("CREATE TABLE db_info (key TEXT PRIMARY KEY, value TEXT)")
                    cursor.execute("INSERT INTO db_info (key, value) VALUES (?, ?)", ('version', str(db_version)))
                
                conn.commit()
                logger.info("Database migration completed successfully")
            else:
                logger.debug("Database schema is up to date")
        
        conn.close()
    except sqlite3.Error as e:
        logger.error(f"Database schema creation error: {e}")
        raise

def reset_database(db_path: str) -> None:
    """
    Reset the database by deleting all data and recreating schema.
    
    CAUTION: This will delete all data in the database!
    
    Args:
        db_path: Path to the SQLite database file
    """
    try:
        if os.path.exists(db_path):
            logger.warning(f"Removing existing database: {db_path}")
            os.remove(db_path)
        
        # Create new schema
        create_database_schema(db_path, 1)
        logger.info("Database reset completed")
    except Exception as e:
        logger.error(f"Error resetting database: {e}")
        raise
