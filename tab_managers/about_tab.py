"""About tab manager for the observation log application."""

import os
from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import QUrl
from PyQt6 import uic

class AboutTabManager:
    """Manages the About tab functionality."""

    def __init__(self, parent, db, tab_widget, statusbar):
        """
        Initialize the About tab manager.

        Args:
            parent: Parent window
            db: Database instance
            tab_widget: Main tab widget
            statusbar: Status bar for messages
        """
        self.parent = parent
        self.db = db
        self.tab_widget = tab_widget
        self.statusbar = statusbar
        self.setup_tab()

    def setup_tab(self):
        """Setup the About tab."""
        about_widget = QWidget()
        base_dir = os.path.dirname(os.path.dirname(__file__))
        ui_path = os.path.join(base_dir, 'about_tab.ui')
        uic.loadUi(ui_path, about_widget)
        self.tab_widget.addTab(about_widget, "About")

        # Store references if needed for future functionality
        self.icon_label = about_widget.findChild(QWidget, "iconLabel")
        self.version_label = about_widget.findChild(QWidget, "versionLabel")
        self.link_label = about_widget.findChild(QLabel, "linkLabel")
        
        # Set up the link with proper HTML formatting
        self.link_label.setText('<a href="https://github.com/prookyon/MonoObsLog">GitHub Repository</a>')
        self.link_label.setOpenExternalLinks(True)
        self.link_label.setToolTip("https://github.com/prookyon/MonoObsLog")
        
        # Connect link activation to open URL
        self.link_label.linkActivated.connect(self.open_github_link)

        # Set status bar message
        self.statusbar.showMessage('About tab loaded')
        
    def open_github_link(self):
        """Open the GitHub repository link in the default browser."""
        QDesktopServices.openUrl(QUrl("https://github.com/prookyon/MonoObsLog"))
        self.statusbar.showMessage('Opening GitHub repository...')