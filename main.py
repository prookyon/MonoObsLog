"""
Observation Log Application

A PyQt6-based application for managing astronomical observation sessions,
including objects, cameras, telescopes, filters, and observations.
"""

import sys
from PyQt6.QtWidgets import QApplication

from main_window import MainWindow


def main():
    """Main entry point for the application."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()