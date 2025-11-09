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
        ui_path = os.path.join(base_dir, 'uifiles', 'settings_tab.ui')
        uic.loadUi(ui_path, settings_widget)
        self.tab_widget.addTab(settings_widget, "Settings")

        # Store references
        self.moon_illumination_spin_box = settings_widget.findChild(QWidget, "moonIlluminationSpinBox")
        self.moon_separation_spin_box = settings_widget.findChild(QWidget, "moonSeparationSpinBox")
        self.latitude_spin_box = settings_widget.findChild(QWidget, "latitudeSpinBox")
        self.longitude_spin_box = settings_widget.findChild(QWidget, "longitudeSpinBox")
        self.save_button = settings_widget.findChild(QWidget, "saveButton")

        # Connect signals
        self.save_button.clicked.connect(self.save_settings)

        # Load current settings
        self.load_settings()

    def load_settings(self):
        """Load settings and populate UI."""
        try:
            moon_illumination = settings.get_moon_illumination_warning()
            moon_separation = settings.get_moon_angular_separation_warning()
            latitude = settings.get_latitude()
            longitude = settings.get_longitude()

            self.moon_illumination_spin_box.setValue(moon_illumination)
            self.moon_separation_spin_box.setValue(moon_separation)
            self.latitude_spin_box.setValue(latitude)
            self.longitude_spin_box.setValue(longitude)

            self.statusbar.showMessage('Settings loaded')
        except Exception as e:
            QMessageBox.critical(self.parent, 'Error', f'Failed to load settings: {str(e)}')

    def save_settings(self):
        """Save settings from UI."""
        try:
            moon_illumination = self.moon_illumination_spin_box.value()
            moon_separation = self.moon_separation_spin_box.value()
            latitude = self.latitude_spin_box.value()
            longitude = self.longitude_spin_box.value()

            settings.set_moon_illumination_warning(moon_illumination)
            settings.set_moon_angular_separation_warning(moon_separation)
            settings.set_latitude(latitude)
            settings.set_longitude(longitude)

            # Refresh observations tab to apply new settings
            if hasattr(self.main_window, 'observations_tab'):
                current_filter = self.main_window.observations_tab.get_current_filter()
                self.main_window.observations_tab.load_observations(current_filter)

            self.statusbar.showMessage('Settings saved')
        except Exception as e:
            QMessageBox.critical(self.parent, 'Error', f'Failed to save settings: {str(e)}')