#!/usr/bin/env python3
"""
Pawprinting Database Operations Module

Provides core database operations for pawprint management
including adding, retrieving, and searching pawprints.

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

from .db_core import get_database

# Set up logging
logger = logging.getLogger(__name__)

def add_pawprint(params: Dict[str, Any], file_path: Optional[str] = None) -> int:
    """
    Add a new pawprint generation to the database.
    
    Args:
        params: Parameter dictionary containing the generation config
        file_path: Optional path to the JSON file if saved separately
        
    Returns:
        ID of the newly created pawprint record
    """
    try:
        db = get_database()
        conn = db.get_connection()
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
        conn.close()
        
        logger.info(f"Added new pawprint: {name} (ID: {pawprint_id})")
        return pawprint_id
    
    except sqlite3.Error as e:
        logger.error(f"Database error adding pawprint: {e}")
        raise

def get_pawprint_by_id(pawprint_id: int) -> Optional[Dict[str, Any]]:
    """
    Get a specific pawprint by its ID.
    
    Args:
        pawprint_id: The ID of the pawprint to retrieve
        
    Returns:
        Pawprint record as a dictionary, or None if not found
    """
    try:
        db = get_database()
        conn = db.get_connection()
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

def get_recent_pawprints(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get most recent pawprint generations.
    
    Args:
        limit: Maximum number of records to return
        
    Returns:
        List of pawprint records as dictionaries
    """
    try:
        db = get_database()
        conn = db.get_connection()
        conn.row_factory = sqlite3.Row
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

def search_pawprints(
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
        db = get_database()
        conn = db.get_connection()
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

def update_pawprint(pawprint_id: int, params: Dict[str, Any]) -> bool:
    """
    Update an existing pawprint record.
    
    Args:
        pawprint_id: ID of the pawprint to update
        params: New parameter values
        
    Returns:
        True if update was successful
    """
    try:
        db = get_database()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Check if record exists
        cursor.execute("SELECT id FROM pawprints WHERE id = ?", (pawprint_id,))
        if not cursor.fetchone():
            logger.warning(f"Pawprint ID {pawprint_id} not found for update")
            return False
        
        # Fields that can be updated
        updateable_fields = [
            'name', 'signature', 'text_entropy', 'file_path', 'tags'
        ]
        
        # Build update query
        set_clauses = []
        values = []
        
        for field in updateable_fields:
            if field in params:
                set_clauses.append(f"{field} = ?")
                values.append(params[field])
        
        # Handle special case for json_config
        if any(k for k in params.keys() if k not in updateable_fields):
            # Need to update the full JSON config
            cursor.execute("SELECT json_config FROM pawprints WHERE id = ?", (pawprint_id,))
            row = cursor.fetchone()
            if row:
                current_config = json.loads(row[0])
                current_config.update(params)
                set_clauses.append("json_config = ?")
                values.append(json.dumps(current_config))
        
        if not set_clauses:
            logger.warning("No fields to update")
            return False
        
        # Execute update
        query = f"UPDATE pawprints SET {', '.join(set_clauses)} WHERE id = ?"
        values.append(pawprint_id)
        cursor.execute(query, values)
        
        conn.commit()
        conn.close()
        
        logger.info(f"Updated pawprint ID: {pawprint_id}")
        return True
    
    except sqlite3.Error as e:
        logger.error(f"Database error updating pawprint: {e}")
        raise

def delete_pawprint(pawprint_id: int) -> bool:
    """
    Delete a pawprint and its associated runs.
    
    Args:
        pawprint_id: ID of the pawprint to delete
        
    Returns:
        True if deletion was successful
    """
    try:
        db = get_database()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # First delete associated runs
        cursor.execute("DELETE FROM runs WHERE pawprint_id = ?", (pawprint_id,))
        
        # Then delete the pawprint
        cursor.execute("DELETE FROM pawprints WHERE id = ?", (pawprint_id,))
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        if deleted_count > 0:
            logger.info(f"Deleted pawprint ID: {pawprint_id}")
            return True
        else:
            logger.warning(f"No pawprint found with ID: {pawprint_id}")
            return False
    
    except sqlite3.Error as e:
        logger.error(f"Database error deleting pawprint: {e}")
        raise

def import_existing_configs() -> Tuple[int, int]:
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
        db = get_database()
        conn = db.get_connection()
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
