"""Dialog classes for editing various entities in the observation log application."""

from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QDateEdit, QDoubleSpinBox,
    QSpinBox, QComboBox, QDialogButtonBox
)
from PyQt6.QtCore import QDate


class EditSessionDialog(QDialog):
    """Dialog for editing session data."""
    
    def __init__(self, name, start_date, comments, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Session")
        
        layout = QFormLayout()
        
        self.name_edit = QLineEdit(name)
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDate(QDate.fromString(start_date, "yyyy-MM-dd"))
        self.comments_edit = QLineEdit(comments)
        
        layout.addRow("Session Name:", self.name_edit)
        layout.addRow("Start Date:", self.start_date_edit)
        layout.addRow("Comments:", self.comments_edit)
        self.comments_edit.setMinimumWidth(300)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
        
        self.setLayout(layout)
    
    def get_values(self):
        """Return the edited values."""
        return self.name_edit.text(), self.start_date_edit.date().toString("yyyy-MM-dd"), self.comments_edit.text()


class EditCameraDialog(QDialog):
    """Dialog for editing camera data."""
    
    def __init__(self, name, sensor, pixel_size, width, height, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Camera")
        
        layout = QFormLayout()
        
        self.name_edit = QLineEdit(name)
        self.sensor_edit = QLineEdit(sensor)
        self.pixel_size_spin = QDoubleSpinBox()
        self.pixel_size_spin.setDecimals(2)
        self.pixel_size_spin.setMaximum(100.0)
        self.pixel_size_spin.setValue(pixel_size)
        self.width_spin = QSpinBox()
        self.width_spin.setMaximum(99999)
        self.width_spin.setValue(width)
        self.height_spin = QSpinBox()
        self.height_spin.setMaximum(99999)
        self.height_spin.setValue(height)
        
        layout.addRow("Name:", self.name_edit)
        layout.addRow("Sensor:", self.sensor_edit)
        layout.addRow("Pixel Size (μm):", self.pixel_size_spin)
        layout.addRow("Width (px):", self.width_spin)
        layout.addRow("Height (px):", self.height_spin)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
        
        self.setLayout(layout)
    
    def get_values(self):
        """Return the edited values."""
        return (
            self.name_edit.text(),
            self.sensor_edit.text(),
            self.pixel_size_spin.value(),
            self.width_spin.value(),
            self.height_spin.value()
        )


class EditFilterDialog(QDialog):
    """Dialog for editing filter data."""
    
    def __init__(self, name, filter_type_id, filter_types_dict, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Filter")
        
        layout = QFormLayout()
        
        self.name_edit = QLineEdit(name)
        self.type_combo = QComboBox()
        
        # Populate combo box with filter type names and store IDs
        for ft in filter_types_dict:
            self.type_combo.addItem(ft['name'], ft['id'])
        
        # Set current selection by ID
        if filter_type_id is not None:
            index = self.type_combo.findData(filter_type_id)
            if index >= 0:
                self.type_combo.setCurrentIndex(index)
        
        layout.addRow("Name:", self.name_edit)
        layout.addRow("Type:", self.type_combo)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
        
        self.setLayout(layout)
    
    def get_values(self):
        """Return the edited values (name and filter_type_id)."""
        return self.name_edit.text(), self.type_combo.currentData()


class EditTelescopeDialog(QDialog):
    """Dialog for editing telescope data."""
    
    def __init__(self, name, aperture, f_ratio, focal_length, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Telescope")
        
        layout = QFormLayout()
        
        self.name_edit = QLineEdit(name)
        self.aperture_spin = QSpinBox()
        self.aperture_spin.setMaximum(99999)
        self.aperture_spin.setValue(aperture)
        self.f_ratio_spin = QDoubleSpinBox()
        self.f_ratio_spin.setDecimals(2)
        self.f_ratio_spin.setMaximum(100.0)
        self.f_ratio_spin.setValue(f_ratio)
        self.focal_length_spin = QSpinBox()
        self.focal_length_spin.setMaximum(99999)
        self.focal_length_spin.setValue(focal_length)
        
        layout.addRow("Name:", self.name_edit)
        layout.addRow("Aperture (mm):", self.aperture_spin)
        layout.addRow("F-ratio:", self.f_ratio_spin)
        layout.addRow("Focal Length (mm):", self.focal_length_spin)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
        
        self.setLayout(layout)
    
    def get_values(self):
        """Return the edited values."""
        return (
            self.name_edit.text(),
            self.aperture_spin.value(),
            self.f_ratio_spin.value(),
            self.focal_length_spin.value()
        )


class EditObservationDialog(QDialog):
    """Dialog for editing observation data."""
    
    def __init__(self, session_id, object_id, camera_id, telescope_id,
                 filter_id, image_count, exposure_length, comments,
                 sessions, objects, cameras, telescopes, filters, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Observation")
        
        layout = QFormLayout()
        
        # Session combo - store IDs
        self.session_combo = QComboBox()
        for session in sessions:
            self.session_combo.addItem(session['name'], session['id'])
        if session_id is not None:
            index = self.session_combo.findData(session_id)
            if index >= 0:
                self.session_combo.setCurrentIndex(index)
        
        # Object combo - store IDs
        self.object_combo = QComboBox()
        for obj in objects:
            self.object_combo.addItem(obj['name'], obj['id'])
        if object_id is not None:
            index = self.object_combo.findData(object_id)
            if index >= 0:
                self.object_combo.setCurrentIndex(index)
        
        # Camera combo - store IDs
        self.camera_combo = QComboBox()
        for camera in cameras:
            self.camera_combo.addItem(camera['name'], camera['id'])
        if camera_id is not None:
            index = self.camera_combo.findData(camera_id)
            if index >= 0:
                self.camera_combo.setCurrentIndex(index)
        
        # Telescope combo - store IDs
        self.telescope_combo = QComboBox()
        for telescope in telescopes:
            self.telescope_combo.addItem(telescope['name'], telescope['id'])
        if telescope_id is not None:
            index = self.telescope_combo.findData(telescope_id)
            if index >= 0:
                self.telescope_combo.setCurrentIndex(index)
        
        # Filter combo - store IDs
        self.filter_combo = QComboBox()
        for filt in filters:
            self.filter_combo.addItem(filt['name'], filt['id'])
        if filter_id is not None:
            index = self.filter_combo.findData(filter_id)
            if index >= 0:
                self.filter_combo.setCurrentIndex(index)
        
        self.image_count_spin = QSpinBox()
        self.image_count_spin.setMaximum(99999)
        self.image_count_spin.setValue(image_count)
        
        self.exposure_spin = QSpinBox()
        self.exposure_spin.setMaximum(99999)
        self.exposure_spin.setValue(exposure_length)
        
        self.comments_edit = QLineEdit(comments)
        
        layout.addRow("Session:", self.session_combo)
        layout.addRow("Object:", self.object_combo)
        layout.addRow("Camera:", self.camera_combo)
        layout.addRow("Telescope:", self.telescope_combo)
        layout.addRow("Filter:", self.filter_combo)
        layout.addRow("Image Count:", self.image_count_spin)
        layout.addRow("Exposure Length (s):", self.exposure_spin)
        layout.addRow("Comments:", self.comments_edit)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
        
        self.setLayout(layout)
    
    def get_values(self):
        """Return the edited values (all as IDs)."""
        return (
            self.session_combo.currentData(),
            self.object_combo.currentData(),
            self.camera_combo.currentData(),
            self.telescope_combo.currentData(),
            self.filter_combo.currentData(),
            self.image_count_spin.value(),
            self.exposure_spin.value(),
            self.comments_edit.text()
        )


class EditObjectDialog(QDialog):
    """Dialog for editing object data with coordinate lookup capability."""
    
    def __init__(self, name, ra=None, dec=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Object")
        self.ra_value = ra
        self.dec_value = dec
        
        layout = QFormLayout()
        
        self.name_edit = QLineEdit(name)
        self.ra_spin = QDoubleSpinBox()
        self.ra_spin.setDecimals(6)
        self.ra_spin.setMinimum(0.0)
        self.ra_spin.setMaximum(24.0)
        self.ra_spin.setValue(ra if ra is not None else 0.0)
        
        self.dec_spin = QDoubleSpinBox()
        self.dec_spin.setDecimals(6)
        self.dec_spin.setMinimum(-90.0)
        self.dec_spin.setMaximum(90.0)
        self.dec_spin.setValue(dec if dec is not None else 0.0)
        
        layout.addRow("Object Name:", self.name_edit)
        layout.addRow("RA (hours, 0-24):", self.ra_spin)
        layout.addRow("Dec (degrees, -90 to +90):", self.dec_spin)
        
        # Add lookup button
        from PyQt6.QtWidgets import QPushButton, QHBoxLayout
        lookup_button = QPushButton("Lookup Coordinates")
        lookup_button.clicked.connect(self.lookup_coordinates)
        layout.addRow("Online Lookup:", lookup_button)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
        
        self.setLayout(layout)
    
    def lookup_coordinates(self):
        """Look up coordinates using astropy."""
        from calculations import lookup_object_coordinates
        
        object_name = self.name_edit.text().strip()
        if not object_name:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, 'Warning', 'Please enter an object name to look up.')
            return
        
        try:
            ra_degrees, dec = lookup_object_coordinates(object_name)
            # Convert RA from degrees to hours (1 hour = 15 degrees)
            ra_hours = ra_degrees / 15.0
            self.ra_spin.setValue(ra_hours)
            self.dec_spin.setValue(dec)
            from PyQt6.QtWidgets import QMessageBox
            # QMessageBox.information(self, 'Success', f'Found coordinates for {object_name}:\nRA: {ra_hours:.6f}h\nDec: {dec:.6f}°')
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self, 'Lookup Error', str(e))
    
    def get_values(self):
        """Return the edited values."""
        return (
            self.name_edit.text(),
            self.ra_spin.value() if self.ra_spin.value() > 0 else None,
            self.dec_spin.value() if self.dec_spin.value() != 0 else None
        )
