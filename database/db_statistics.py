#!/usr/bin/env python3
"""
Pawprinting Database Statistics Module

Provides analytics and statistical functions for pawprint data.

Author: AIMF LLC
Date: June 3, 2025
"""

import logging
import sqlite3
from typing import Dict, Any, List, Tuple, Optional

from .db_core import get_database

# Set up logging
logger = logging.getLogger(__name__)

def get_database_stats() -> Dict[str, Any]:
    """
    Get database statistics.
    
    Returns:
        Dictionary with statistics about the database
    """
    try:
        db = get_database()
        conn = db.get_connection()
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
        avg_entropy = cursor.fetchone()[0]
        stats['avg_entropy'] = round(float(avg_entropy), 3) if avg_entropy else 0.0
        
        # Date of first and last pawprint
        cursor.execute("SELECT MIN(created_at), MAX(created_at) FROM pawprints")
        first, last = cursor.fetchone() or (None, None)
        stats['first_pawprint_date'] = first
        stats['last_pawprint_date'] = last
        
        # Count by entropy ranges
        cursor.execute("""
        SELECT 
            SUM(CASE WHEN text_entropy < 0.3 THEN 1 ELSE 0 END) as low_entropy,
            SUM(CASE WHEN text_entropy >= 0.3 AND text_entropy < 0.7 THEN 1 ELSE 0 END) as medium_entropy,
            SUM(CASE WHEN text_entropy >= 0.7 THEN 1 ELSE 0 END) as high_entropy
        FROM pawprints
        """)
        entropy_counts = cursor.fetchone()
        if entropy_counts:
            stats['low_entropy_count'] = entropy_counts[0] or 0
            stats['medium_entropy_count'] = entropy_counts[1] or 0
            stats['high_entropy_count'] = entropy_counts[2] or 0
        
        conn.close()
        return stats
    
    except sqlite3.Error as e:
        logger.error(f"Database error getting stats: {e}")
        raise

def get_run_history(pawprint_id: int) -> List[Dict[str, Any]]:
    """
    Get the run history for a specific pawprint.
    
    Args:
        pawprint_id: ID of the pawprint
        
    Returns:
        List of run records
    """
    try:
        db = get_database()
        conn = db.get_connection()
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

def log_run(pawprint_id: int, notes: Optional[str] = None) -> int:
    """
    Log a run of an existing pawprint.
    
    Args:
        pawprint_id: ID of the pawprint that was run
        notes: Optional notes about this run
        
    Returns:
        ID of the newly created run record
    """
    try:
        db = get_database()
        conn = db.get_connection()
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

def get_entropy_distribution() -> List[Tuple[float, int]]:
    """
    Get distribution of entropy values for visualization.
    
    Returns:
        List of tuples (entropy_value, count)
    """
    try:
        db = get_database()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Round entropy to 1 decimal place for binning
        cursor.execute("""
        SELECT ROUND(text_entropy, 1) as entropy_bin, COUNT(*) as count
        FROM pawprints
        GROUP BY entropy_bin
        ORDER BY entropy_bin ASC
        """)
        
        results = cursor.fetchall()
        conn.close()
        
        return results
    
    except sqlite3.Error as e:
        logger.error(f"Database error getting entropy distribution: {e}")
        raise

def get_time_series_data(interval: str = 'day') -> List[Tuple[str, int]]:
    """
    Get time series data of pawprint creations.
    
    Args:
        interval: Time grouping interval ('hour', 'day', 'week', 'month')
    
    Returns:
        List of tuples (time_period, count)
    """
    try:
        db = get_database()
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Format string based on interval
        if interval == 'hour':
            time_format = '%Y-%m-%dT%H'
        elif interval == 'day':
            time_format = '%Y-%m-%d'
        elif interval == 'week':
            time_format = '%Y-W%W'
        elif interval == 'month':
            time_format = '%Y-%m'
        else:
            time_format = '%Y-%m-%d'  # Default to day
        
        # SQLite strftime for time grouping
        cursor.execute(f"""
        SELECT strftime('{time_format}', created_at) as time_period, COUNT(*) as count
        FROM pawprints
        GROUP BY time_period
        ORDER BY time_period ASC
        """)
        
        results = cursor.fetchall()
        conn.close()
        
        return results
    
    except sqlite3.Error as e:
        logger.error(f"Database error getting time series data: {e}")
        raise
