"""Telescopes tab manager for the observation log application."""

from PyQt6.QtWidgets import QWidget, QMessageBox, QTableWidgetItem
from PyQt6 import uic

from dialogs import EditTelescopeDialog


class TelescopesTabManager:
    """Manages the Telescopes tab functionality."""
    
    def __init__(self, parent, db, tab_widget, statusbar):
        """
        Initialize the Telescopes tab manager.
        
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
        """Setup the Telescopes tab."""
        telescope_widget = QWidget()
        uic.loadUi('telescope_tab.ui', telescope_widget)
        self.tab_widget.addTab(telescope_widget, "Telescopes")
        
        # Store references
        self.telescopes_table = telescope_widget.findChild(QWidget, "telescopesTable")
        self.telescope_name_line_edit = telescope_widget.findChild(QWidget, "nameLineEdit")
        self.aperture_spin_box = telescope_widget.findChild(QWidget, "apertureSpinBox")
        self.f_ratio_spin_box = telescope_widget.findChild(QWidget, "fRatioSpinBox")
        self.focal_length_spin_box = telescope_widget.findChild(QWidget, "focalLengthSpinBox")
        self.add_telescope_button = telescope_widget.findChild(QWidget, "addTelescopeButton")
        self.edit_telescope_button = telescope_widget.findChild(QWidget, "editTelescopeButton")
        self.delete_telescope_button = telescope_widget.findChild(QWidget, "deleteTelescopeButton")
        
        # Connect signals
        self.add_telescope_button.clicked.connect(self.add_telescope)
        self.edit_telescope_button.clicked.connect(self.edit_telescope)
        self.delete_telescope_button.clicked.connect(self.delete_telescope)
        self.telescope_name_line_edit.returnPressed.connect(self.add_telescope)

        # Connect value change signals for automatic F-ratio calculation
        self.aperture_spin_box.valueChanged.connect(self.calculate_f_ratio)
        self.focal_length_spin_box.valueChanged.connect(self.calculate_f_ratio)
        
        # Hide ID column
        self.telescopes_table.setColumnHidden(0, True)
        self.telescopes_table.setColumnWidth(1, 200)
        self.telescopes_table.setColumnWidth(2, 120)
        self.telescopes_table.setColumnWidth(3, 120)
        self.telescopes_table.setColumnWidth(4, 140)
        
        self.load_telescopes()
    
    def load_telescopes(self):
        """Load all telescopes from database and display in table."""
        try:
            telescopes = self.db.get_all_telescopes()
            self.telescopes_table.setRowCount(len(telescopes))
            
            for row, telescope in enumerate(telescopes):
                self.telescopes_table.setItem(row, 0, QTableWidgetItem(str(telescope['id'])))
                self.telescopes_table.setItem(row, 1, QTableWidgetItem(telescope['name']))
                self.telescopes_table.setItem(row, 2, QTableWidgetItem(str(telescope['aperture'])))
                self.telescopes_table.setItem(row, 3, QTableWidgetItem(str(telescope['f_ratio'])))
                self.telescopes_table.setItem(row, 4, QTableWidgetItem(str(telescope['focal_length'])))
            
            self.statusbar.showMessage(f'Loaded {len(telescopes)} telescope(s)')
        except Exception as e:
            QMessageBox.critical(self.parent, 'Error', f'Failed to load telescopes: {str(e)}')
    
    def add_telescope(self):
        """Add a new telescope to the database."""
        name = self.telescope_name_line_edit.text().strip()
        aperture = self.aperture_spin_box.value()
        f_ratio = self.f_ratio_spin_box.value()
        focal_length = self.focal_length_spin_box.value()

        if not name:
            QMessageBox.warning(self.parent, 'Warning', 'Please enter a telescope name.')
            return

        if aperture == 0 or f_ratio == 0 or focal_length == 0:
            QMessageBox.warning(
                self.parent, 'Warning',
                'Please enter valid aperture, f-ratio, and focal length.'
            )
            return

        # Check for duplicate telescope name
        if self.db.telescope_name_exists(name):
            QMessageBox.warning(self.parent, 'Warning', f'Telescope name "{name}" already exists. Please choose a unique telescope name.')
            return

        try:
            self.db.add_telescope(name, aperture, f_ratio, focal_length)
            self.telescope_name_line_edit.clear()
            self.aperture_spin_box.setValue(0)
            self.f_ratio_spin_box.setValue(0)
            self.focal_length_spin_box.setValue(0)
            self.load_telescopes()
            self.statusbar.showMessage(f'Added telescope: {name}')
        except Exception as e:
            QMessageBox.critical(self.parent, 'Error', f'Failed to add telescope: {str(e)}')
    
    def edit_telescope(self):
        """Edit the selected telescope."""
        selected_rows = self.telescopes_table.selectedItems()

        if not selected_rows:
            QMessageBox.warning(self.parent, 'Warning', 'Please select a telescope to edit.')
            return

        row = self.telescopes_table.currentRow()
        telescope_id = int(self.telescopes_table.item(row, 0).text())
        current_name = self.telescopes_table.item(row, 1).text()
        current_aperture = int(self.telescopes_table.item(row, 2).text())
        current_f_ratio = float(self.telescopes_table.item(row, 3).text())
        current_focal_length = int(self.telescopes_table.item(row, 4).text())

        dialog = EditTelescopeDialog(
            current_name, current_aperture, current_f_ratio,
            current_focal_length, self.parent
        )
        if dialog.exec():
            name, aperture, f_ratio, focal_length = dialog.get_values()

            # Check for duplicate telescope name, excluding the current telescope
            if self.db.telescope_name_exists(name, exclude_id=telescope_id):
                QMessageBox.warning(self.parent, 'Warning', f'Telescope name "{name}" already exists. Please choose a unique telescope name.')
                return

            try:
                self.db.update_telescope(telescope_id, name, aperture, f_ratio, focal_length)
                self.load_telescopes()
                self.statusbar.showMessage(f'Updated telescope ID {telescope_id}')
            except Exception as e:
                QMessageBox.critical(self.parent, 'Error', f'Failed to update telescope: {str(e)}')
    
    def delete_telescope(self):
        """Delete the selected telescope."""
        selected_rows = self.telescopes_table.selectedItems()
        
        if not selected_rows:
            QMessageBox.warning(self.parent, 'Warning', 'Please select a telescope to delete.')
            return
        
        row = self.telescopes_table.currentRow()
        telescope_id = int(self.telescopes_table.item(row, 0).text())
        telescope_name = self.telescopes_table.item(row, 1).text()
        
        reply = QMessageBox.question(
            self.parent, 'Confirm Deletion',
            f'Are you sure you want to delete telescope "{telescope_name}"?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.db.delete_telescope(telescope_id)
                self.load_telescopes()
                self.statusbar.showMessage(f'Deleted telescope: {telescope_name}')
            except Exception as e:
                QMessageBox.critical(self.parent, 'Error', f'Failed to delete telescope: {str(e)}')

    def calculate_f_ratio(self):
        """Automatically calculate and fill F-ratio when aperture and focal length are entered."""
        aperture = self.aperture_spin_box.value()
        focal_length = self.focal_length_spin_box.value()

        # Only calculate if both values are greater than 0
        if aperture > 0 and focal_length > 0:
            f_ratio = focal_length / aperture
            # Round to one decimal place as requested
            rounded_f_ratio = round(f_ratio, 1)
            self.f_ratio_spin_box.setValue(rounded_f_ratio)