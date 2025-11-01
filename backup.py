"""
Database Backup Utility

Handles automatic weekly backups of the SQLite database file.
Backups are stored in the 'ObsLogBackup' subfolder of the database location,
zipped, and named with the backup date.
"""

import os
import zipfile
from datetime import datetime, timedelta
from typing import Optional, Tuple


BACKUP_FOLDER_NAME = "ObsLogBackup"
BACKUP_INTERVAL_DAYS = 7


def get_backup_folder(db_path: str) -> str:
    """Get the path to the backup folder for the given database.
    
    Args:
        db_path: Path to the database file
        
    Returns:
        Path to the backup folder
    """
    db_dir = os.path.dirname(db_path)
    return os.path.join(db_dir, BACKUP_FOLDER_NAME)


def ensure_backup_folder_exists(db_path: str) -> str:
    """Ensure the backup folder exists, creating it if necessary.
    
    Args:
        db_path: Path to the database file
        
    Returns:
        Path to the backup folder
    """
    backup_folder = get_backup_folder(db_path)
    os.makedirs(backup_folder, exist_ok=True)
    return backup_folder


def get_backup_filename(date: datetime) -> str:
    """Generate a backup filename based on the given date.
    
    Args:
        date: The date for the backup
        
    Returns:
        Backup filename in format: observations_backup_YYYY-MM-DD.zip
    """
    db_name = "observations"  # Base name without extension
    date_str = date.strftime("%Y-%m-%d")
    return f"{db_name}_backup_{date_str}.zip"


def parse_backup_date(filename: str) -> Optional[datetime]:
    """Parse the date from a backup filename.
    
    Args:
        filename: The backup filename
        
    Returns:
        Datetime object if the filename is valid, None otherwise
    """
    # Expected format: observations_backup_YYYY-MM-DD.zip
    try:
        if not filename.endswith('.zip'):
            return None
        
        # Remove .zip extension
        name_without_ext = filename[:-4]
        
        # Split by underscore
        parts = name_without_ext.split('_')
        
        # Should be: ['observations', 'backup', 'YYYY-MM-DD']
        if len(parts) != 3 or parts[0] != 'observations' or parts[1] != 'backup':
            return None
        
        # Parse the date
        date_str = parts[2]
        return datetime.strptime(date_str, "%Y-%m-%d")
    except (ValueError, IndexError):
        return None


def get_latest_backup_info(db_path: str) -> Tuple[Optional[str], Optional[datetime]]:
    """Get information about the latest backup.
    
    Args:
        db_path: Path to the database file
        
    Returns:
        Tuple of (backup_filename, backup_date) or (None, None) if no backups exist
    """
    backup_folder = get_backup_folder(db_path)
    
    # Check if backup folder exists
    if not os.path.exists(backup_folder):
        return None, None
    
    # Get all backup files
    backup_files = []
    try:
        for filename in os.listdir(backup_folder):
            if filename.endswith('.zip'):
                backup_date = parse_backup_date(filename)
                if backup_date:
                    backup_files.append((filename, backup_date))
    except OSError:
        return None, None
    
    # If no valid backups found
    if not backup_files:
        return None, None
    
    # Sort by date (most recent first)
    backup_files.sort(key=lambda x: x[1], reverse=True)
    
    return backup_files[0]


def is_backup_needed(db_path: str) -> bool:
    """Check if a backup is needed based on the latest backup date.
    
    A backup is needed if:
    - No backups exist, OR
    - The latest backup is more than BACKUP_INTERVAL_DAYS old
    
    Args:
        db_path: Path to the database file
        
    Returns:
        True if a backup is needed, False otherwise
    """
    _, latest_backup_date = get_latest_backup_info(db_path)
    
    # No backups exist
    if latest_backup_date is None:
        return True
    
    # Check if latest backup is older than the interval
    days_since_backup = (datetime.now() - latest_backup_date).days
    return days_since_backup >= BACKUP_INTERVAL_DAYS


def create_backup(db_path: str) -> Tuple[bool, str]:
    """Create a backup of the database.
    
    Args:
        db_path: Path to the database file
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        # Check if database file exists
        if not os.path.exists(db_path):
            return False, f"Database file not found: {db_path}"
        
        # Ensure backup folder exists
        backup_folder = ensure_backup_folder_exists(db_path)
        
        # Generate backup filename
        backup_filename = get_backup_filename(datetime.now())
        backup_path = os.path.join(backup_folder, backup_filename)
        
        # Create a zip file containing the database
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add the database file to the zip
            # Use only the basename in the archive to avoid full path
            zipf.write(db_path, os.path.basename(db_path))
        
        return True, f"Backup created successfully: {backup_filename}"
    
    except Exception as e:
        return False, f"Failed to create backup: {str(e)}"


def check_and_create_backup(db_path: str) -> Tuple[bool, str]:
    """Check if a backup is needed and create one if necessary.
    
    This is the main function to be called on application startup.
    
    Args:
        db_path: Path to the database file
        
    Returns:
        Tuple of (backup_created: bool, message: str)
    """
    try:
        # Check if backup is needed
        if not is_backup_needed(db_path):
            _, latest_backup_date = get_latest_backup_info(db_path)
            if latest_backup_date:
                days_since_backup = (datetime.now() - latest_backup_date).days
                return False, f"Backup not needed (last backup was {days_since_backup} days ago)"
            return False, "Backup not needed"
        
        # Create backup
        success, message = create_backup(db_path)
        return success, message
    
    except Exception as e:
        return False, f"Error checking backup status: {str(e)}"