"""Main window class for the observation log application."""

import os
from PyQt6.QtWidgets import QMainWindow
from PyQt6 import uic

from database import Database
from tab_managers import (
    ObjectsTabManager,
    SessionsTabManager,
    CamerasTabManager,
    FilterTypesTabManager,
    FiltersTabManager,
    TelescopesTabManager,
    ObservationsTabManager,
    ObjectStatsTabManager,
    MonthlyStatsTabManager,
    SettingsTabManager,
    AboutTabManager,
)


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self, db_path: str):
        super().__init__()
        
        # Load the main UI file
        base_dir = os.path.dirname(__file__)
        ui_path = os.path.join(base_dir, 'mainwindow.ui')
        uic.loadUi(ui_path, self)
        
        # Initialize database with the specified path
        self.db = Database(db_path)
        
        # Initialize tab managers
        self.objects_tab = ObjectsTabManager(self, self.db, self.tabWidget, self.statusbar)
        self.sessions_tab = SessionsTabManager(self, self.db, self.tabWidget, self.statusbar)
        self.cameras_tab = CamerasTabManager(self, self.db, self.tabWidget, self.statusbar)
        self.filter_types_tab = FilterTypesTabManager(self, self.db, self.tabWidget, self.statusbar)
        self.filters_tab = FiltersTabManager(self, self.db, self.tabWidget, self.statusbar)
        self.telescopes_tab = TelescopesTabManager(self, self.db, self.tabWidget, self.statusbar)
        self.observations_tab = ObservationsTabManager(self, self.db, self.tabWidget, self.statusbar)
        self.object_stats_tab = ObjectStatsTabManager(self, self.db, self.tabWidget, self.statusbar)
        self.monthly_stats_tab = MonthlyStatsTabManager(self, self.db, self.tabWidget, self.statusbar)
        self.settings_tab = SettingsTabManager(self, self.db, self.tabWidget, self.statusbar)
        self.about_tab = AboutTabManager(self, self.db, self.tabWidget, self.statusbar)

        # Connect tab change signal to update observation combos when switching to Observations tab
        self.tabWidget.currentChanged.connect(self.on_tab_changed)

        # Set status bar message
        self.statusbar.showMessage('Ready')
    
    def on_tab_changed(self, index):
        """Handle tab change events."""
        # Get the tab text to identify which tab was selected
        tab_text = self.tabWidget.tabText(index)
        if tab_text == "Observations":
            # Update the observation combo boxes when switching to the Observations tab
            self.observations_tab.update_observation_combos()
        elif tab_text == "Filters":
            # Update filter type combo when switching to Filters tab
            self.filters_tab.update_filter_type_combo()
        elif tab_text == "Object Stats":
            # Reload stats when switching to Object Stats tab
            self.object_stats_tab.load_stats()
        elif tab_text == "Monthly Stats":
            # Reload stats when switching to Monthly Stats tab
            self.monthly_stats_tab.load_stats()

    def closeEvent(self, event):
        """Handle window close event."""
        self.db.close()
        event.accept()