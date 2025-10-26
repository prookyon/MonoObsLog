"""Dialog classes for editing various entities in the observation log application."""

from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QDateEdit, QDoubleSpinBox,
    QSpinBox, QComboBox, QDialogButtonBox
)
from PyQt6.QtCore import QDate


class EditSessionDialog(QDialog):
    """Dialog for editing session data."""
    
    def __init__(self, session_id, start_date, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Session")
        
        layout = QFormLayout()
        
        self.session_id_edit = QLineEdit(session_id)
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDate(QDate.fromString(start_date, "yyyy-MM-dd"))
        
        layout.addRow("Session ID:", self.session_id_edit)
        layout.addRow("Start Date:", self.start_date_edit)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
        
        self.setLayout(layout)
    
    def get_values(self):
        """Return the edited values."""
        return self.session_id_edit.text(), self.start_date_edit.date().toString("yyyy-MM-dd")


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
    
    def __init__(self, name, filter_type, filter_types, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Filter")
        
        layout = QFormLayout()
        
        self.name_edit = QLineEdit(name)
        self.type_combo = QComboBox()
        self.type_combo.addItems(filter_types)
        self.type_combo.setCurrentText(filter_type)
        
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
        """Return the edited values."""
        return self.name_edit.text(), self.type_combo.currentText()


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
    
    def __init__(self, session_id, object_name, camera_name, telescope_name,
                 filter_name, image_count, exposure_length, comments,
                 sessions, objects, cameras, telescopes, filters, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Observation")
        
        layout = QFormLayout()
        
        self.session_combo = QComboBox()
        self.session_combo.addItems(sessions)
        self.session_combo.setCurrentText(session_id)
        
        self.object_combo = QComboBox()
        self.object_combo.addItems(objects)
        self.object_combo.setCurrentText(object_name)
        
        self.camera_combo = QComboBox()
        self.camera_combo.addItems(cameras)
        self.camera_combo.setCurrentText(camera_name)
        
        self.telescope_combo = QComboBox()
        self.telescope_combo.addItems(telescopes)
        self.telescope_combo.setCurrentText(telescope_name)
        
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(filters)
        self.filter_combo.setCurrentText(filter_name)
        
        self.image_count_spin = QSpinBox()
        self.image_count_spin.setMaximum(99999)
        self.image_count_spin.setValue(image_count)
        
        self.exposure_spin = QSpinBox()
        self.exposure_spin.setMaximum(99999)
        self.exposure_spin.setValue(exposure_length)
        
        self.comments_edit = QLineEdit(comments)
        
        layout.addRow("Session ID:", self.session_combo)
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
        """Return the edited values."""
        return (
            self.session_combo.currentText(),
            self.object_combo.currentText(),
            self.camera_combo.currentText(),
            self.telescope_combo.currentText(),
            self.filter_combo.currentText(),
            self.image_count_spin.value(),
            self.exposure_spin.value(),
            self.comments_edit.text()
        )