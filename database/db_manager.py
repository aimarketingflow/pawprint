#!/usr/bin/env python3
"""
Database Manager for Pawprinting PyQt6

Provides SQLite-based storage and retrieval for pawprint generations and configurations,
enabling historical records and analysis of pawprint signatures.

Author: AIMF LLC
Date: June 3, 2025
"""

import json
import logging
import os
import sqlite3
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Union

# Import config paths
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config_paths import BASE_DIR, RESULTS_DIR

# Set up logging
logger = logging.getLogger(__name__)

class PawprintDatabase:
    """
    Manages database operations for the Pawprinting application.
    
    This class handles the creation, connection, and query operations
    for the SQLite database storing pawprint generation history.
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
        
        # Initialize database
        self._initialize_database()
        
        logger.info(f"PawprintDatabase initialized at {self.db_path}")
    
    def _initialize_database(self) -> None:
        """Initialize the database schema if it doesn't exist."""
        try:
            # Connect to database (creates file if it doesn't exist)
            conn = sqlite3.connect(self.db_path)
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
                cursor.execute('INSERT INTO db_info (key, value) VALUES (?, ?)', ('version', str(self.DB_VERSION)))
                
                conn.commit()
                logger.info("Database schema created successfully")
            else:
                logger.debug("Database already exists")
            
            conn.close()
        except sqlite3.Error as e:
            logger.error(f"Database initialization error: {e}")
            raise
    
    def import_existing_configs(self) -> Tuple[int, int]:
        """
        Import existing JSON configuration files into the database.
        
        Returns:
            Tuple of (number of files processed, number of files imported)
        """
        config_dir = os.path.join(BASE_DIR, 'config')
        results_dir = RESULTS_DIR
        
        imported = 0
        total = 0
        
        try:
            # Connect to database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create a set of already imported file paths
            cursor.execute('SELECT file_path FROM pawprints WHERE file_path IS NOT NULL')
            existing_files = set(row[0] for row in cursor.fetchall())
            
            # Import from config directory
            if os.path.exists(config_dir):
                for filename in os.listdir(config_dir):
                    if filename.endswith('.json'):
                        file_path = os.path.join(config_dir, filename)
                        total += 1
                        
                        if file_path in existing_files:
                            logger.debug(f"Skipping already imported file: {file_path}")
                            continue
                            
                        try:
                            with open(file_path, 'r') as f:
                                config = json.load(f)
                                
                            # Extract key information
                            name = config.get('name', filename.replace('.json', ''))
                            created_at = config.get('created_at', datetime.now().isoformat())
                            signature = config.get('pawprint_signature', '')
                            text_input = config.get('text_input', '')
                            text_entropy = config.get('text_entropy', 0.0)
                            json_config = json.dumps(config)
                            
                            # Insert into database
                            cursor.execute('''
                            INSERT INTO pawprints (name, created_at, signature, text_input, json_config, file_path, text_entropy)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                            ''', (name, created_at, signature, text_input, json_config, file_path, text_entropy))
                            
                            imported += 1
                            logger.info(f"Imported configuration: {name}")
                        except Exception as e:
                            logger.error(f"Error importing {file_path}: {e}")
            
            conn.commit()
            conn.close()
            
            logger.info(f"Import complete. Processed {total} files, imported {imported} new configurations.")
            return (total, imported)
        
        except sqlite3.Error as e:
            logger.error(f"Database error during import: {e}")
            raise
    
    def add_pawprint(self, params: Dict[str, Any], file_path: Optional[str] = None) -> int:
        """
        Add a new pawprint generation to the database.
        
        Args:
            params: Parameter dictionary containing the generation config
            file_path: Optional path to the JSON file if saved separately
            
        Returns:
            ID of the newly created pawprint record
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Extract key information
            name = params.get('name', f"pawprint_{int(time.time())}")
            created_at = params.get('created_at', datetime.now().isoformat())
            signature = params.get('pawprint_signature', '')
            text_input = params.get('text_input', '')
            text_entropy = params.get('text_entropy', 0.0)
            json_config = json.dumps(params)
            
            # Insert into database
            cursor.execute('''
            INSERT INTO pawprints (name, created_at, signature, text_input, json_config, file_path, text_entropy)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (name, created_at, signature, text_input, json_config, file_path, text_entropy))
            
            pawprint_id = cursor.lastrowid
            
            # Add a run record
            cursor.execute('''
            INSERT INTO runs (pawprint_id, run_timestamp, notes)
            VALUES (?, ?, ?)
            ''', (pawprint_id, datetime.now().isoformat(), "Initial generation"))
            
            conn.commit()
            
            logger.info(f"Added new pawprint: {name} (ID: {pawprint_id})")
            
            conn.close()
            return pawprint_id
        
        except sqlite3.Error as e:
            logger.error(f"Database error adding pawprint: {e}")
            raise
    
    def get_recent_pawprints(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get most recent pawprint generations.
        
        Args:
            limit: Maximum number of records to return
            
        Returns:
            List of pawprint records as dictionaries
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Return rows as dictionaries
            cursor = conn.cursor()
            
            cursor.execute('''
            SELECT id, name, created_at, signature, text_entropy, file_path
            FROM pawprints
            ORDER BY created_at DESC
            LIMIT ?
            ''', (limit,))
            
            results = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            return results
        
        except sqlite3.Error as e:
            logger.error(f"Database error retrieving recent pawprints: {e}")
            raise
    
    def get_pawprint_by_id(self, pawprint_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific pawprint by its ID.
        
        Args:
            pawprint_id: The ID of the pawprint to retrieve
            
        Returns:
            Pawprint record as a dictionary, or None if not found
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
            SELECT id, name, created_at, signature, text_input, json_config, file_path, text_entropy
            FROM pawprints
            WHERE id = ?
            ''', (pawprint_id,))
            
            row = cursor.fetchone()
            result = dict(row) if row else None
            
            if result and 'json_config' in result:
                # Parse the JSON config
                result['params'] = json.loads(result['json_config'])
            
            conn.close()
            return result
        
        except sqlite3.Error as e:
            logger.error(f"Database error retrieving pawprint {pawprint_id}: {e}")
            raise
    
    def search_pawprints(self, 
                        query: Optional[str] = None, 
                        signature: Optional[str] = None,
                        min_entropy: Optional[float] = None,
                        max_entropy: Optional[float] = None,
                        start_date: Optional[str] = None,
                        end_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Search for pawprints based on various criteria.
        
        Args:
            query: Text to search in name or text_input
            signature: Full or partial signature to match
            min_entropy: Minimum entropy value
            max_entropy: Maximum entropy value
            start_date: Start date in ISO format
            end_date: End date in ISO format
            
        Returns:
            List of matching pawprint records
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            conditions = []
            params = []
            
            if query:
                conditions.append("(name LIKE ? OR text_input LIKE ?)")
                params.extend([f"%{query}%", f"%{query}%"])
            
            if signature:
                conditions.append("signature LIKE ?")
                params.append(f"%{signature}%")
            
            if min_entropy is not None:
                conditions.append("text_entropy >= ?")
                params.append(min_entropy)
            
            if max_entropy is not None:
                conditions.append("text_entropy <= ?")
                params.append(max_entropy)
            
            if start_date:
                conditions.append("created_at >= ?")
                params.append(start_date)
            
            if end_date:
                conditions.append("created_at <= ?")
                params.append(end_date)
            
            query_string = '''
            SELECT id, name, created_at, signature, text_entropy, file_path
            FROM pawprints
            '''
            
            if conditions:
                query_string += " WHERE " + " AND ".join(conditions)
            
            query_string += " ORDER BY created_at DESC"
            
            cursor.execute(query_string, params)
            results = [dict(row) for row in cursor.fetchall()]
            
            conn.close()
            return results
        
        except sqlite3.Error as e:
            logger.error(f"Database error searching pawprints: {e}")
            raise
    
    def log_run(self, pawprint_id: int, notes: Optional[str] = None) -> int:
        """
        Log a run of an existing pawprint.
        
        Args:
            pawprint_id: ID of the pawprint that was run
            notes: Optional notes about this run
            
        Returns:
            ID of the newly created run record
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
            INSERT INTO runs (pawprint_id, run_timestamp, notes)
            VALUES (?, ?, ?)
            ''', (pawprint_id, datetime.now().isoformat(), notes or ""))
            
            run_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            logger.info(f"Logged run for pawprint {pawprint_id}")
            return run_id
        
        except sqlite3.Error as e:
            logger.error(f"Database error logging run: {e}")
            raise
    
    def get_run_history(self, pawprint_id: int) -> List[Dict[str, Any]]:
        """
        Get the run history for a specific pawprint.
        
        Args:
            pawprint_id: ID of the pawprint
            
        Returns:
            List of run records
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
            SELECT id, run_timestamp, notes
            FROM runs
            WHERE pawprint_id = ?
            ORDER BY run_timestamp DESC
            ''', (pawprint_id,))
            
            results = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            return results
        
        except sqlite3.Error as e:
            logger.error(f"Database error retrieving run history: {e}")
            raise
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get database statistics.
        
        Returns:
            Dictionary with statistics about the database
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            stats = {}
            
            # Total pawprints
            cursor.execute("SELECT COUNT(*) FROM pawprints")
            stats['total_pawprints'] = cursor.fetchone()[0]
            
            # Total runs
            cursor.execute("SELECT COUNT(*) FROM runs")
            stats['total_runs'] = cursor.fetchone()[0]
            
            # Average entropy
            cursor.execute("SELECT AVG(text_entropy) FROM pawprints")
            stats['avg_entropy'] = cursor.fetchone()[0] or 0.0
            
            # Date of first and last pawprint
            cursor.execute("SELECT MIN(created_at), MAX(created_at) FROM pawprints")
            first, last = cursor.fetchone()
            stats['first_pawprint_date'] = first
            stats['last_pawprint_date'] = last
            
            conn.close()
            return stats
        
        except sqlite3.Error as e:
            logger.error(f"Database error getting stats: {e}")
            raise

# Function to get a global database instance
_db_instance = None

def get_database() -> PawprintDatabase:
    """Get or create the global database instance."""
    global _db_instance
    if _db_instance is None:
        _db_instance = PawprintDatabase()
    return _db_instance
