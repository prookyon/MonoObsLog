"""
Observation Log Application

A PyQt6-based application for managing astronomical observation sessions,
including objects, cameras, telescopes, filters, and observations.
"""

import sys
import os
from PyQt6.QtWidgets import QApplication, QFileDialog, QMessageBox

from main_window import MainWindow
import settings
import backup
from testing import test_plot


def main():
    test_plot()
    """Main entry point for the application."""
    app = QApplication(sys.argv)
    
    # Check if database path is configured
    db_path = settings.get_database_path()
    
    if db_path is None:
        # Show file selection dialog to let user select or create database
        db_path, _ = QFileDialog.getSaveFileName(
            None,
            "Select Database Location",
            os.path.join(os.path.expanduser("~"), "observations.db"),
            "Database Files (*.db);;All Files (*)"
        )
        
        # If user cancelled the dialog, exit the application
        if not db_path:
            QMessageBox.warning(
                None,
                "Database Required",
                "A database location must be selected to run the application."
            )
            sys.exit(0)
        
        # Save the selected database path to settings
        settings.set_database_path(db_path)
    
    # Verify the database path exists or can be created
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        try:
            os.makedirs(db_dir, exist_ok=True)
        except Exception as e:
            QMessageBox.critical(
                None,
                "Error",
                f"Failed to create database directory: {str(e)}"
            )
            sys.exit(1)
    
    # Check and create backup if needed
    try:
        backup_created, backup_message = backup.check_and_create_backup(db_path)
        if backup_created:
            print(f"Database backup: {backup_message}")
    except Exception as e:
        # Don't prevent app startup if backup fails, just log it
        print(f"Warning: Backup check failed: {str(e)}")
    
    # Create and show main window with the database path
    window = MainWindow(db_path)
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()