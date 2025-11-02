#!/usr/bin/env python3
"""
Console utilities for the Observation Log Application

This module provides command-line utilities for managing astronomical observation data,
including moon illumination calculations and database maintenance operations.

Usage:
    python utilities.py --calc-moon [--database DATABASE_FILE]
    
Options:
    --calc-moon          Recalculate moon illumination and location data for all sessions
    --database FILE      Specify database file path (default: objects.db)
    --help, -h           Show this help message
"""

import argparse
import sys
import os
from datetime import datetime
from pathlib import Path

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(__file__))

from calculations import calculate_moon_data
from database import Database


def calculate_moon_data_for_all_sessions(db_path: str = "objects.db") -> dict:
    """
    Recalculate moon illumination and location data for all sessions in the database.
    
    Parameters:
    -----------
    db_path : str
        Path to the SQLite database file
        
    Returns:
    --------
    dict
        Dictionary containing statistics about the operation:
        - 'total_sessions': Total number of sessions processed
        - 'updated_sessions': Number of sessions successfully updated
        - 'errors': List of error messages encountered
        - 'results': List of results for each session processed
    """
    print(f"Connecting to database: {db_path}")
    
    # Check if database file exists
    if not os.path.exists(db_path):
        error_msg = f"Database file not found: {db_path}"
        print(f"Error: {error_msg}", file=sys.stderr)
        return {
            'total_sessions': 0,
            'updated_sessions': 0,
            'errors': [error_msg],
            'results': []
        }
    
    try:
        # Initialize database connection
        db = Database(db_path)
        
        # Get all sessions
        print("Retrieving all sessions from database...")
        sessions = db.get_all_sessions()
        
        if not sessions:
            print("No sessions found in database.")
            return {
                'total_sessions': 0,
                'updated_sessions': 0,
                'errors': [],
                'results': []
            }
        
        print(f"Found {len(sessions)} sessions to process.")
        print("-" * 60)
        
        # Statistics
        stats = {
            'total_sessions': len(sessions),
            'updated_sessions': 0,
            'errors': [],
            'results': []
        }
        
        # Process each session
        for i, session in enumerate(sessions, 1):
            session_id = session['session_id']
            start_date = session['start_date']
            
            print(f"[{i}/{len(sessions)}] Processing session '{session_id}' (date: {start_date})")
            
            try:
                # Calculate new moon data
                moon_illumination, moon_ra, moon_dec = calculate_moon_data(start_date)
                
                # Update session in database
                db.update_session(
                    session_id=session['id'],
                    new_session_id=session_id,
                    start_date=start_date,
                    moon_illumination=moon_illumination,
                    moon_ra=moon_ra,
                    moon_dec=moon_dec
                )
                
                result = {
                    'session_id': session_id,
                    'start_date': start_date,
                    'moon_illumination': round(moon_illumination, 2),
                    'moon_ra': round(moon_ra, 4),
                    'moon_dec': round(moon_dec, 4),
                    'status': 'success'
                }
                stats['results'].append(result)
                stats['updated_sessions'] += 1
                
                print(f"  [OK] Updated - illumination: {moon_illumination:.2f}%, RA: {moon_ra:.4f}°, Dec: {moon_dec:.4f}°")
                
            except Exception as e:
                error_msg = f"Error processing session '{session_id}': {str(e)}"
                stats['errors'].append(error_msg)
                stats['results'].append({
                    'session_id': session_id,
                    'start_date': start_date,
                    'status': 'error',
                    'error': str(e)
                })
                print(f"  [ERROR] - {error_msg}", file=sys.stderr)
        
        # Close database connection
        db.close()
        
        print("-" * 60)
        print("Processing complete!")
        print(f"Total sessions: {stats['total_sessions']}")
        print(f"Successfully updated: {stats['updated_sessions']}")
        
        if stats['errors']:
            print(f"Errors encountered: {len(stats['errors'])}")
            for error in stats['errors']:
                print(f"  - {error}", file=sys.stderr)
        else:
            print("No errors encountered.")
        
        return stats
        
    except Exception as e:
        error_msg = f"Database error: {str(e)}"
        print(f"Error: {error_msg}", file=sys.stderr)
        return {
            'total_sessions': 0,
            'updated_sessions': 0,
            'errors': [error_msg],
            'results': []
        }


def main():
    """Main entry point for the utilities console application."""
    parser = argparse.ArgumentParser(
        description='Console utilities for Observation Log Application',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python utilities.py --calc-moon
  python utilities.py --calc-moon --database /path/to/custom.db
  
This command will:
1. Connect to the specified database
2. Retrieve all observation sessions
3. Recalculate moon illumination and coordinates for each session
4. Update the database with the new calculations
5. Display progress and summary statistics
        """
    )
    
    parser.add_argument(
        '--calc-moon',
        action='store_true',
        help='Recalculate moon illumination and location data for all sessions in the database'
    )
    
    parser.add_argument(
        '--database',
        default='objects.db',
        help='Path to the SQLite database file (default: objects.db)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )
    
    args = parser.parse_args()
    
    # Check if no arguments provided
    if not any(vars(args).values()):
        parser.print_help()
        return 1
    
    # Handle --calc-moon command
    if args.calc_moon:
        # Resolve database path
        db_path = os.path.abspath(args.database)
        
        print("Observation Log - Moon Data Calculator")
        print("=" * 40)
        print(f"Database: {db_path}")
        print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Execute moon calculation for all sessions
        result = calculate_moon_data_for_all_sessions(db_path)
        
        # Return appropriate exit code
        if result['errors']:
            return 1
        else:
            return 0
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)