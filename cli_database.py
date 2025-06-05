#!/usr/bin/env python3
"""
CLI Database Interface for Pawprinting PyQt6 V2

Command-line interface for working with the pawprint database.
Allows importing, exporting, searching, and managing pawprints.

Author: AIMF LLC
Date: June 3, 2025
"""

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime
from typing import Dict, Any, List, Optional

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import database modules
from database import (
    get_database, get_recent_pawprints, search_pawprints,
    get_pawprint_by_id, add_pawprint, delete_pawprint,
    import_existing_configs, get_database_stats
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def setup_parser():
    """Set up argument parser for CLI"""
    parser = argparse.ArgumentParser(description='Pawprinting Database CLI Tool')
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Import command
    import_parser = subparsers.add_parser('import', help='Import existing JSON configs into database')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List recent pawprints')
    list_parser.add_argument('--limit', type=int, default=10, help='Number of entries to display')
    list_parser.add_argument('--format', choices=['table', 'json'], default='table', help='Output format')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search for pawprints')
    search_parser.add_argument('--query', type=str, help='Text search query')
    search_parser.add_argument('--signature', type=str, help='Partial or full signature to match')
    search_parser.add_argument('--min-entropy', type=float, help='Minimum entropy value')
    search_parser.add_argument('--max-entropy', type=float, help='Maximum entropy value')
    search_parser.add_argument('--start-date', type=str, help='Start date in ISO format (YYYY-MM-DD)')
    search_parser.add_argument('--end-date', type=str, help='End date in ISO format (YYYY-MM-DD)')
    search_parser.add_argument('--format', choices=['table', 'json'], default='table', help='Output format')
    
    # View command
    view_parser = subparsers.add_parser('view', help='View details of a specific pawprint')
    view_parser.add_argument('id', type=int, help='Pawprint ID to view')
    view_parser.add_argument('--format', choices=['pretty', 'json'], default='pretty', help='Output format')
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a pawprint')
    delete_parser.add_argument('id', type=int, help='Pawprint ID to delete')
    delete_parser.add_argument('--force', action='store_true', help='Skip confirmation prompt')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export pawprints to JSON files')
    export_parser.add_argument('--id', type=int, help='Specific pawprint ID to export')
    export_parser.add_argument('--output-dir', type=str, default='./exports', help='Directory for exported files')
    export_parser.add_argument('--all', action='store_true', help='Export all pawprints')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show database statistics')
    
    return parser

def format_table(data: List[Dict[str, Any]], columns: List[str]) -> str:
    """
    Format data as an ASCII table.
    
    Args:
        data: List of dictionaries containing the data
        columns: List of column keys to display
    
    Returns:
        Formatted table as string
    """
    if not data:
        return "No data to display."
    
    # Determine column widths
    col_widths = {}
    for col in columns:
        # Start with the header width
        col_widths[col] = len(col)
        
        # Check each row
        for row in data:
            if col in row:
                col_widths[col] = max(col_widths[col], len(str(row[col])))
    
    # Create header
    header = " | ".join(f"{col:<{col_widths[col]}}" for col in columns)
    separator = "-" * len(header)
    
    # Create rows
    rows = []
    for row in data:
        rows.append(" | ".join(
            f"{str(row.get(col, '')):<{col_widths[col]}}"
            for col in columns
        ))
    
    # Combine all parts
    return "\n".join([header, separator] + rows)

def handle_import_command(args):
    """Handle import command"""
    logger.info("Importing existing configurations...")
    total, imported = import_existing_configs()
    logger.info(f"Import complete. Processed {total} files, imported {imported} new configurations.")

def handle_list_command(args):
    """Handle list command"""
    limit = args.limit
    logger.info(f"Listing {limit} most recent pawprints...")
    
    pawprints = get_recent_pawprints(limit=limit)
    
    if args.format == 'json':
        print(json.dumps(pawprints, indent=2))
    else:
        columns = ['id', 'name', 'created_at', 'signature', 'text_entropy']
        print(format_table(pawprints, columns))

def handle_search_command(args):
    """Handle search command"""
    logger.info("Searching for pawprints...")
    
    # Parse dates if provided
    start_date = None
    if args.start_date:
        start_date = f"{args.start_date}T00:00:00"
    
    end_date = None
    if args.end_date:
        end_date = f"{args.end_date}T23:59:59"
    
    results = search_pawprints(
        query=args.query,
        signature=args.signature,
        min_entropy=args.min_entropy,
        max_entropy=args.max_entropy,
        start_date=start_date,
        end_date=end_date
    )
    
    if args.format == 'json':
        print(json.dumps(results, indent=2))
    else:
        columns = ['id', 'name', 'created_at', 'signature', 'text_entropy']
        print(format_table(results, columns))
    
    logger.info(f"Found {len(results)} matching pawprints")

def handle_view_command(args):
    """Handle view command"""
    pawprint_id = args.id
    logger.info(f"Retrieving pawprint {pawprint_id}...")
    
    pawprint = get_pawprint_by_id(pawprint_id)
    
    if not pawprint:
        logger.error(f"Pawprint {pawprint_id} not found")
        sys.exit(1)
    
    if args.format == 'json':
        print(json.dumps(pawprint, indent=2))
    else:
        # Pretty print
        print(f"Pawprint ID: {pawprint['id']}")
        print(f"Name: {pawprint['name']}")
        print(f"Created: {pawprint['created_at']}")
        print(f"Signature: {pawprint['signature']}")
        print(f"Text Entropy: {pawprint['text_entropy']}")
        print(f"File Path: {pawprint['file_path'] or 'N/A'}")
        
        if 'params' in pawprint:
            print("\nParameters:")
            for key, value in pawprint['params'].items():
                if key not in ['json_config', 'text_input'] and not isinstance(value, dict):
                    print(f"  {key}: {value}")

def handle_delete_command(args):
    """Handle delete command"""
    pawprint_id = args.id
    
    # Get pawprint info first
    pawprint = get_pawprint_by_id(pawprint_id)
    if not pawprint:
        logger.error(f"Pawprint {pawprint_id} not found")
        sys.exit(1)
    
    # Confirm deletion unless --force flag used
    if not args.force:
        confirm = input(f"Are you sure you want to delete pawprint '{pawprint['name']}' (ID: {pawprint_id})? [y/N]: ")
        if confirm.lower() != 'y':
            logger.info("Delete operation cancelled")
            return
    
    logger.info(f"Deleting pawprint {pawprint_id}...")
    success = delete_pawprint(pawprint_id)
    
    if success:
        logger.info(f"Pawprint {pawprint_id} deleted successfully")
    else:
        logger.error(f"Failed to delete pawprint {pawprint_id}")
        sys.exit(1)

def handle_export_command(args):
    """Handle export command"""
    output_dir = args.output_dir
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logger.info(f"Created output directory: {output_dir}")
    
    if args.id:
        # Export single pawprint
        pawprint_id = args.id
        pawprint = get_pawprint_by_id(pawprint_id)
        
        if not pawprint:
            logger.error(f"Pawprint {pawprint_id} not found")
            sys.exit(1)
        
        # Export to file
        output_file = os.path.join(output_dir, f"pawprint_{pawprint_id}.json")
        with open(output_file, 'w') as f:
            json.dump(pawprint['params'], f, indent=2)
        
        logger.info(f"Exported pawprint {pawprint_id} to {output_file}")
    
    elif args.all:
        # Export all pawprints
        pawprints = search_pawprints()
        exported_count = 0
        
        for pawprint_summary in pawprints:
            try:
                pawprint_id = pawprint_summary['id']
                full_pawprint = get_pawprint_by_id(pawprint_id)
                
                if full_pawprint and 'params' in full_pawprint:
                    # Export to file
                    output_file = os.path.join(output_dir, f"pawprint_{pawprint_id}.json")
                    with open(output_file, 'w') as f:
                        json.dump(full_pawprint['params'], f, indent=2)
                    
                    exported_count += 1
            except Exception as e:
                logger.error(f"Error exporting pawprint {pawprint_id}: {e}")
        
        logger.info(f"Exported {exported_count} pawprints to {output_dir}")
    
    else:
        logger.error("You must specify either --id or --all")
        sys.exit(1)

def handle_stats_command(args):
    """Handle stats command"""
    logger.info("Retrieving database statistics...")
    
    stats = get_database_stats()
    
    print("\nPawprint Database Statistics")
    print("===========================")
    print(f"Total Pawprints: {stats['total_pawprints']}")
    print(f"Total Runs: {stats['total_runs']}")
    print(f"Average Entropy: {stats['avg_entropy']:.3f}")
    
    print("\nEntropy Distribution:")
    print(f"  Low (<0.3): {stats.get('low_entropy_count', 0)}")
    print(f"  Medium (0.3-0.7): {stats.get('medium_entropy_count', 0)}")
    print(f"  High (>0.7): {stats.get('high_entropy_count', 0)}")
    
    if stats['first_pawprint_date'] and stats['last_pawprint_date']:
        try:
            first_date = datetime.fromisoformat(stats['first_pawprint_date']).strftime('%Y-%m-%d')
            last_date = datetime.fromisoformat(stats['last_pawprint_date']).strftime('%Y-%m-%d')
            print(f"\nFirst Pawprint: {first_date}")
            print(f"Latest Pawprint: {last_date}")
        except Exception:
            pass

def main():
    """Main entry point"""
    parser = setup_parser()
    args = parser.parse_args()
    
    # Initialize database
    try:
        db = get_database()
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        sys.exit(1)
    
    # Time the operation
    start_time = time.time()
    
    try:
        if args.command == 'import':
            handle_import_command(args)
        elif args.command == 'list':
            handle_list_command(args)
        elif args.command == 'search':
            handle_search_command(args)
        elif args.command == 'view':
            handle_view_command(args)
        elif args.command == 'delete':
            handle_delete_command(args)
        elif args.command == 'export':
            handle_export_command(args)
        elif args.command == 'stats':
            handle_stats_command(args)
        else:
            parser.print_help()
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)
    
    # Print execution time
    execution_time = time.time() - start_time
    logger.info(f"Command completed in {execution_time:.2f} seconds")

if __name__ == '__main__':
    main()
