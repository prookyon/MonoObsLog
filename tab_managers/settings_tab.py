"""Settings tab manager for the observation log application."""

import os
from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6 import uic
import settings

class SettingsTabManager:
    """Manages the Settings tab functionality."""

    def __init__(self, parent, db, tab_widget, statusbar):
        """
        Initialize the Settings tab manager.

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
        self.main_window = parent  # Reference to main window for refreshing other tabs
        self.setup_tab()

    def setup_tab(self):
        """Setup the Settings tab."""
        settings_widget = QWidget()
        base_dir = os.path.dirname(os.path.dirname(__file__))
        ui_path = os.path.join(base_dir, 'settings_tab.ui')
        uic.loadUi(ui_path, settings_widget)
        self.tab_widget.addTab(settings_widget, "Settings")

        # Store references
        self.moon_phase_spin_box = settings_widget.findChild(QWidget, "moonPhaseSpinBox")
        self.moon_separation_spin_box = settings_widget.findChild(QWidget, "moonSeparationSpinBox")
        self.save_button = settings_widget.findChild(QWidget, "saveButton")

        # Connect signals
        self.save_button.clicked.connect(self.save_settings)

        # Load current settings
        self.load_settings()

    def load_settings(self):
        """Load settings and populate UI."""
        try:
            moon_phase = settings.get_moon_phase_warning()
            moon_separation = settings.get_moon_angular_separation_warning()

            self.moon_phase_spin_box.setValue(moon_phase)
            self.moon_separation_spin_box.setValue(moon_separation)

            self.statusbar.showMessage('Settings loaded')
        except Exception as e:
            QMessageBox.critical(self.parent, 'Error', f'Failed to load settings: {str(e)}')

    def save_settings(self):
        """Save settings from UI."""
        try:
            moon_phase = self.moon_phase_spin_box.value()
            moon_separation = self.moon_separation_spin_box.value()

            settings.set_moon_phase_warning(moon_phase)
            settings.set_moon_angular_separation_warning(moon_separation)

            # Refresh observations tab to apply new settings
            if hasattr(self.main_window, 'observations_tab'):
                current_filter = self.main_window.observations_tab.get_current_filter()
                self.main_window.observations_tab.load_observations(current_filter)

            self.statusbar.showMessage('Settings saved')
        except Exception as e:
            QMessageBox.critical(self.parent, 'Error', f'Failed to save settings: {str(e)}')