import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QTableWidgetItem, 
    QInputDialog, QWidget, QDialog, QVBoxLayout, QFormLayout,
    QLineEdit, QDateEdit, QDoubleSpinBox, QSpinBox, QComboBox,
    QDialogButtonBox
)
from PyQt6.QtCore import QDate
from PyQt6 import uic
from database import Database


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
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
        
        self.setLayout(layout)
    
    def get_values(self):
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
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
        
        self.setLayout(layout)
    
    def get_values(self):
        return (self.name_edit.text(), self.sensor_edit.text(), 
                self.pixel_size_spin.value(), self.width_spin.value(), 
                self.height_spin.value())


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
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
        
        self.setLayout(layout)
    
    def get_values(self):
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
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
        
        self.setLayout(layout)
    
    def get_values(self):
        return (self.name_edit.text(), self.aperture_spin.value(), 
                self.f_ratio_spin.value(), self.focal_length_spin.value())

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
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
        
        self.setLayout(layout)
    
    def get_values(self):
        return (self.session_combo.currentText(), self.object_combo.currentText(),
                self.camera_combo.currentText(), self.telescope_combo.currentText(),
                self.filter_combo.currentText(), self.image_count_spin.value(),
                self.exposure_spin.value(), self.comments_edit.text())



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Load the main UI file
        uic.loadUi('mainwindow.ui', self)
        
        # Initialize database
        self.db = Database()
        
        # Load and setup tabs
        self.setup_objects_tab()
        self.setup_sessions_tab()
        self.setup_cameras_tab()
        self.setup_filter_types_tab()
        self.setup_filters_tab()
        self.setup_telescopes_tab()
        self.setup_observations_tab()

        # Connect tab change signal to update observation combos when switching to Observations tab
        self.tabWidget.currentChanged.connect(self.on_tab_changed)

        # Set status bar message
        self.statusbar.showMessage('Ready')
    
    def setup_objects_tab(self):
        """Setup the Objects tab."""
        object_widget = QWidget()
        uic.loadUi('object_tab.ui', object_widget)
        self.tabWidget.addTab(object_widget, "Objects")

        # Store references
        self.objectsTable = object_widget.findChild(QWidget, "objectsTable")
        self.nameLineEdit = object_widget.findChild(QWidget, "nameLineEdit")
        self.addButton = object_widget.findChild(QWidget, "addButton")
        self.editButton = object_widget.findChild(QWidget, "editButton")
        self.deleteButton = object_widget.findChild(QWidget, "deleteButton")

        # Connect signals
        self.addButton.clicked.connect(self.add_object)
        self.editButton.clicked.connect(self.edit_object)
        self.deleteButton.clicked.connect(self.delete_object)
        self.nameLineEdit.returnPressed.connect(self.add_object)

        # Hide ID column
        self.objectsTable.setColumnHidden(0, True)
        self.objectsTable.setColumnWidth(1, 600)

        self.load_objects()
    
    def setup_sessions_tab(self):
        """Setup the Sessions tab."""
        session_widget = QWidget()
        uic.loadUi('session_tab.ui', session_widget)
        self.tabWidget.addTab(session_widget, "Sessions")
        
        # Store references
        self.sessionsTable = session_widget.findChild(QWidget, "sessionsTable")
        self.sessionIdLineEdit = session_widget.findChild(QWidget, "sessionIdLineEdit")
        self.startDateEdit = session_widget.findChild(QWidget, "startDateEdit")
        self.addSessionButton = session_widget.findChild(QWidget, "addSessionButton")
        self.editSessionButton = session_widget.findChild(QWidget, "editSessionButton")
        self.deleteSessionButton = session_widget.findChild(QWidget, "deleteSessionButton")
        
        # Set current date
        self.startDateEdit.setDate(QDate.currentDate())
        
        # Connect signals
        self.addSessionButton.clicked.connect(self.add_session)
        self.editSessionButton.clicked.connect(self.edit_session)
        self.deleteSessionButton.clicked.connect(self.delete_session)
        self.sessionIdLineEdit.returnPressed.connect(self.add_session)
        
        # Hide ID column
        self.sessionsTable.setColumnHidden(0, True)
        self.sessionsTable.setColumnWidth(1, 300)
        self.sessionsTable.setColumnWidth(2, 300)
        
        self.load_sessions()
    
    def setup_cameras_tab(self):
        """Setup the Cameras tab."""
        camera_widget = QWidget()
        uic.loadUi('camera_tab.ui', camera_widget)
        self.tabWidget.addTab(camera_widget, "Cameras")
        
        # Store references
        self.camerasTable = camera_widget.findChild(QWidget, "camerasTable")
        self.cameraNameLineEdit = camera_widget.findChild(QWidget, "nameLineEdit")
        self.sensorLineEdit = camera_widget.findChild(QWidget, "sensorLineEdit")
        self.pixelSizeSpinBox = camera_widget.findChild(QWidget, "pixelSizeSpinBox")
        self.widthSpinBox = camera_widget.findChild(QWidget, "widthSpinBox")
        self.heightSpinBox = camera_widget.findChild(QWidget, "heightSpinBox")
        self.addCameraButton = camera_widget.findChild(QWidget, "addCameraButton")
        self.editCameraButton = camera_widget.findChild(QWidget, "editCameraButton")
        self.deleteCameraButton = camera_widget.findChild(QWidget, "deleteCameraButton")
        
        # Connect signals
        self.addCameraButton.clicked.connect(self.add_camera)
        self.editCameraButton.clicked.connect(self.edit_camera)
        self.deleteCameraButton.clicked.connect(self.delete_camera)
        self.cameraNameLineEdit.returnPressed.connect(self.add_camera)
        
        # Hide ID column
        self.camerasTable.setColumnHidden(0, True)
        self.camerasTable.setColumnWidth(1, 180)
        self.camerasTable.setColumnWidth(2, 180)
        self.camerasTable.setColumnWidth(3, 100)
        self.camerasTable.setColumnWidth(4, 100)
        self.camerasTable.setColumnWidth(5, 100)
        
        self.load_cameras()
    
    def setup_filter_types_tab(self):
        """Setup the Filter Types tab."""
        filter_type_widget = QWidget()
        uic.loadUi('filter_type_tab.ui', filter_type_widget)
        self.tabWidget.addTab(filter_type_widget, "Filter Types")
        
        # Store references
        self.filterTypesTable = filter_type_widget.findChild(QWidget, "filterTypesTable")
        self.filterTypeNameLineEdit = filter_type_widget.findChild(QWidget, "nameLineEdit")
        self.addFilterTypeButton = filter_type_widget.findChild(QWidget, "addFilterTypeButton")
        self.editFilterTypeButton = filter_type_widget.findChild(QWidget, "editFilterTypeButton")
        self.deleteFilterTypeButton = filter_type_widget.findChild(QWidget, "deleteFilterTypeButton")
        
        # Connect signals
        self.addFilterTypeButton.clicked.connect(self.add_filter_type)
        self.editFilterTypeButton.clicked.connect(self.edit_filter_type)
        self.deleteFilterTypeButton.clicked.connect(self.delete_filter_type)
        self.filterTypeNameLineEdit.returnPressed.connect(self.add_filter_type)
        
        # Hide ID column
        self.filterTypesTable.setColumnHidden(0, True)
        self.filterTypesTable.setColumnWidth(1, 600)
        
        self.load_filter_types()
    
    def setup_filters_tab(self):
        """Setup the Filters tab."""
        filter_widget = QWidget()
        uic.loadUi('filter_tab.ui', filter_widget)
        self.tabWidget.addTab(filter_widget, "Filters")
        
        # Store references
        self.filtersTable = filter_widget.findChild(QWidget, "filtersTable")
        self.filterNameLineEdit = filter_widget.findChild(QWidget, "nameLineEdit")
        self.filterTypeComboBox = filter_widget.findChild(QWidget, "typeComboBox")
        self.addFilterButton = filter_widget.findChild(QWidget, "addFilterButton")
        self.editFilterButton = filter_widget.findChild(QWidget, "editFilterButton")
        self.deleteFilterButton = filter_widget.findChild(QWidget, "deleteFilterButton")
        
        # Connect signals
        self.addFilterButton.clicked.connect(self.add_filter)
        self.editFilterButton.clicked.connect(self.edit_filter)
        self.deleteFilterButton.clicked.connect(self.delete_filter)
        self.filterNameLineEdit.returnPressed.connect(self.add_filter)
        
        # Hide ID column
        self.filtersTable.setColumnHidden(0, True)
        self.filtersTable.setColumnWidth(1, 350)
        self.filtersTable.setColumnWidth(2, 350)
        
        self.load_filters()
        self.update_filter_type_combo()
    
    def setup_telescopes_tab(self):
        """Setup the Telescopes tab."""
        telescope_widget = QWidget()
        uic.loadUi('telescope_tab.ui', telescope_widget)
        self.tabWidget.addTab(telescope_widget, "Telescopes")
        
        # Store references
        self.telescopesTable = telescope_widget.findChild(QWidget, "telescopesTable")
        self.telescopeNameLineEdit = telescope_widget.findChild(QWidget, "nameLineEdit")
        self.apertureSpinBox = telescope_widget.findChild(QWidget, "apertureSpinBox")
        self.fRatioSpinBox = telescope_widget.findChild(QWidget, "fRatioSpinBox")
        self.focalLengthSpinBox = telescope_widget.findChild(QWidget, "focalLengthSpinBox")
        self.addTelescopeButton = telescope_widget.findChild(QWidget, "addTelescopeButton")
        self.editTelescopeButton = telescope_widget.findChild(QWidget, "editTelescopeButton")
        self.deleteTelescopeButton = telescope_widget.findChild(QWidget, "deleteTelescopeButton")
        
        # Connect signals
        self.addTelescopeButton.clicked.connect(self.add_telescope)
        self.editTelescopeButton.clicked.connect(self.edit_telescope)
        self.deleteTelescopeButton.clicked.connect(self.delete_telescope)
        self.telescopeNameLineEdit.returnPressed.connect(self.add_telescope)

        # Connect value change signals for automatic F-ratio calculation
        self.apertureSpinBox.valueChanged.connect(self.calculate_f_ratio)
        self.focalLengthSpinBox.valueChanged.connect(self.calculate_f_ratio)
        
        # Hide ID column
        self.telescopesTable.setColumnHidden(0, True)
        self.telescopesTable.setColumnWidth(1, 200)
        self.telescopesTable.setColumnWidth(2, 120)
        self.telescopesTable.setColumnWidth(3, 120)
        self.telescopesTable.setColumnWidth(4, 140)
        
        self.load_telescopes()
    
    # ==================== Object Methods ====================
    
    
    def setup_observations_tab(self):
        """Setup the Observations tab."""
        observation_widget = QWidget()
        uic.loadUi('observation_tab.ui', observation_widget)
        self.tabWidget.addTab(observation_widget, "Observations")
        
        # Store references
        self.observationsTable = observation_widget.findChild(QWidget, "observationsTable")
        self.sessionIdComboBox = observation_widget.findChild(QWidget, "sessionIdComboBox")
        self.objectComboBox = observation_widget.findChild(QWidget, "objectComboBox")
        self.cameraComboBox = observation_widget.findChild(QWidget, "cameraComboBox")
        self.telescopeComboBox = observation_widget.findChild(QWidget, "telescopeComboBox")
        self.filterComboBox = observation_widget.findChild(QWidget, "filterComboBox")
        self.imageCountSpinBox = observation_widget.findChild(QWidget, "imageCountSpinBox")
        self.exposureLengthSpinBox = observation_widget.findChild(QWidget, "exposureLengthSpinBox")
        self.commentsLineEdit = observation_widget.findChild(QWidget, "commentsLineEdit")
        self.addObservationButton = observation_widget.findChild(QWidget, "addObservationButton")
        self.editObservationButton = observation_widget.findChild(QWidget, "editObservationButton")
        self.deleteObservationButton = observation_widget.findChild(QWidget, "deleteObservationButton")
        
        # Connect signals
        self.addObservationButton.clicked.connect(self.add_observation)
        self.editObservationButton.clicked.connect(self.edit_observation)
        self.deleteObservationButton.clicked.connect(self.delete_observation)
        
        # Hide ID column
        self.observationsTable.setColumnHidden(0, True)
        self.observationsTable.setColumnWidth(1, 100)  # Session ID
        self.observationsTable.setColumnWidth(2, 100)  # Object
        self.observationsTable.setColumnWidth(3, 100)  # Camera
        self.observationsTable.setColumnWidth(4, 100)  # Telescope
        self.observationsTable.setColumnWidth(5, 80)   # Filter
        self.observationsTable.setColumnWidth(6, 60)   # Images
        self.observationsTable.setColumnWidth(7, 80)   # Exposure
        self.observationsTable.setColumnWidth(8, 100)  # Total Exposure
        self.observationsTable.setColumnWidth(9, 200)  # Comments
        
        self.load_observations()
        self.update_observation_combos()
    def load_objects(self):
        """Load all objects from database and display in table."""
        try:
            objects = self.db.get_all_objects()
            self.objectsTable.setRowCount(len(objects))
            
            for row, obj in enumerate(objects):
                self.objectsTable.setItem(row, 0, QTableWidgetItem(str(obj['id'])))
                self.objectsTable.setItem(row, 1, QTableWidgetItem(obj['name']))
            
            self.statusbar.showMessage(f'Loaded {len(objects)} object(s)')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load objects: {str(e)}')
    
    def add_object(self):
        """Add a new object to the database."""
        name = self.nameLineEdit.text().strip()
        
        if not name:
            QMessageBox.warning(self, 'Warning', 'Please enter an object name.')
            return
        
        try:
            self.db.add_object(name)
            self.nameLineEdit.clear()
            self.load_objects()
            self.statusbar.showMessage(f'Added object: {name}')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to add object: {str(e)}')
    
    def edit_object(self):
        """Edit the selected object."""
        selected_rows = self.objectsTable.selectedItems()
        
        if not selected_rows:
            QMessageBox.warning(self, 'Warning', 'Please select an object to edit.')
            return
        
        row = self.objectsTable.currentRow()
        object_id = int(self.objectsTable.item(row, 0).text())
        current_name = self.objectsTable.item(row, 1).text()
        
        new_name, ok = QInputDialog.getText(self, 'Edit Object', 'Enter new name:', text=current_name)
        
        if ok and new_name.strip():
            try:
                self.db.update_object(object_id, new_name.strip())
                self.load_objects()
                self.statusbar.showMessage(f'Updated object ID {object_id}')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to update object: {str(e)}')
    
    def delete_object(self):
        """Delete the selected object."""
        selected_rows = self.objectsTable.selectedItems()
        
        if not selected_rows:
            QMessageBox.warning(self, 'Warning', 'Please select an object to delete.')
            return
        
        row = self.objectsTable.currentRow()
        object_id = int(self.objectsTable.item(row, 0).text())
        object_name = self.objectsTable.item(row, 1).text()
        
        reply = QMessageBox.question(
            self, 'Confirm Deletion',
            f'Are you sure you want to delete "{object_name}"?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.db.delete_object(object_id)
                self.load_objects()
                self.statusbar.showMessage(f'Deleted object: {object_name}')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to delete object: {str(e)}')
    
    # ==================== Session Methods ====================
    
    def load_sessions(self):
        """Load all sessions from database and display in table."""
        try:
            sessions = self.db.get_all_sessions()
            self.sessionsTable.setRowCount(len(sessions))
            
            for row, session in enumerate(sessions):
                self.sessionsTable.setItem(row, 0, QTableWidgetItem(str(session['id'])))
                self.sessionsTable.setItem(row, 1, QTableWidgetItem(session['session_id']))
                self.sessionsTable.setItem(row, 2, QTableWidgetItem(session['start_date']))
            
            self.statusbar.showMessage(f'Loaded {len(sessions)} session(s)')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load sessions: {str(e)}')
    
    def add_session(self):
        """Add a new session to the database."""
        session_id = self.sessionIdLineEdit.text().strip()
        start_date = self.startDateEdit.date().toString("yyyy-MM-dd")
        
        if not session_id:
            QMessageBox.warning(self, 'Warning', 'Please enter a session ID.')
            return
        
        try:
            self.db.add_session(session_id, start_date)
            self.sessionIdLineEdit.clear()
            self.startDateEdit.setDate(QDate.currentDate())
            self.load_sessions()
            self.statusbar.showMessage(f'Added session: {session_id}')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to add session: {str(e)}')
    
    def edit_session(self):
        """Edit the selected session."""
        selected_rows = self.sessionsTable.selectedItems()
        
        if not selected_rows:
            QMessageBox.warning(self, 'Warning', 'Please select a session to edit.')
            return
        
        row = self.sessionsTable.currentRow()
        session_id = int(self.sessionsTable.item(row, 0).text())
        current_session_id = self.sessionsTable.item(row, 1).text()
        current_start_date = self.sessionsTable.item(row, 2).text()
        
        dialog = EditSessionDialog(current_session_id, current_start_date, self)
        if dialog.exec():
            new_session_id, new_start_date = dialog.get_values()
            try:
                self.db.update_session(session_id, new_session_id, new_start_date)
                self.load_sessions()
                self.statusbar.showMessage(f'Updated session ID {session_id}')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to update session: {str(e)}')
    
    def delete_session(self):
        """Delete the selected session."""
        selected_rows = self.sessionsTable.selectedItems()
        
        if not selected_rows:
            QMessageBox.warning(self, 'Warning', 'Please select a session to delete.')
            return
        
        row = self.sessionsTable.currentRow()
        session_id = int(self.sessionsTable.item(row, 0).text())
        session_name = self.sessionsTable.item(row, 1).text()
        
        reply = QMessageBox.question(
            self, 'Confirm Deletion',
            f'Are you sure you want to delete session "{session_name}"?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.db.delete_session(session_id)
                self.load_sessions()
                self.statusbar.showMessage(f'Deleted session: {session_name}')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to delete session: {str(e)}')
    
    # ==================== Camera Methods ====================
    
    def load_cameras(self):
        """Load all cameras from database and display in table."""
        try:
            cameras = self.db.get_all_cameras()
            self.camerasTable.setRowCount(len(cameras))
            
            for row, camera in enumerate(cameras):
                self.camerasTable.setItem(row, 0, QTableWidgetItem(str(camera['id'])))
                self.camerasTable.setItem(row, 1, QTableWidgetItem(camera['name']))
                self.camerasTable.setItem(row, 2, QTableWidgetItem(camera['sensor']))
                self.camerasTable.setItem(row, 3, QTableWidgetItem(str(camera['pixel_size'])))
                self.camerasTable.setItem(row, 4, QTableWidgetItem(str(camera['width'])))
                self.camerasTable.setItem(row, 5, QTableWidgetItem(str(camera['height'])))
            
            self.statusbar.showMessage(f'Loaded {len(cameras)} camera(s)')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load cameras: {str(e)}')
    
    def add_camera(self):
        """Add a new camera to the database."""
        name = self.cameraNameLineEdit.text().strip()
        sensor = self.sensorLineEdit.text().strip()
        pixel_size = self.pixelSizeSpinBox.value()
        width = self.widthSpinBox.value()
        height = self.heightSpinBox.value()
        
        if not name or not sensor:
            QMessageBox.warning(self, 'Warning', 'Please enter camera name and sensor.')
            return
        
        if pixel_size == 0 or width == 0 or height == 0:
            QMessageBox.warning(self, 'Warning', 'Please enter valid pixel size, width, and height.')
            return
        
        try:
            self.db.add_camera(name, sensor, pixel_size, width, height)
            self.cameraNameLineEdit.clear()
            self.sensorLineEdit.clear()
            self.pixelSizeSpinBox.setValue(0)
            self.widthSpinBox.setValue(0)
            self.heightSpinBox.setValue(0)
            self.load_cameras()
            self.statusbar.showMessage(f'Added camera: {name}')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to add camera: {str(e)}')
    
    def edit_camera(self):
        """Edit the selected camera."""
        selected_rows = self.camerasTable.selectedItems()
        
        if not selected_rows:
            QMessageBox.warning(self, 'Warning', 'Please select a camera to edit.')
            return
        
        row = self.camerasTable.currentRow()
        camera_id = int(self.camerasTable.item(row, 0).text())
        current_name = self.camerasTable.item(row, 1).text()
        current_sensor = self.camerasTable.item(row, 2).text()
        current_pixel_size = float(self.camerasTable.item(row, 3).text())
        current_width = int(self.camerasTable.item(row, 4).text())
        current_height = int(self.camerasTable.item(row, 5).text())
        
        dialog = EditCameraDialog(current_name, current_sensor, current_pixel_size, 
                                  current_width, current_height, self)
        if dialog.exec():
            name, sensor, pixel_size, width, height = dialog.get_values()
            try:
                self.db.update_camera(camera_id, name, sensor, pixel_size, width, height)
                self.load_cameras()
                self.statusbar.showMessage(f'Updated camera ID {camera_id}')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to update camera: {str(e)}')
    
    def delete_camera(self):
        """Delete the selected camera."""
        selected_rows = self.camerasTable.selectedItems()
        
        if not selected_rows:
            QMessageBox.warning(self, 'Warning', 'Please select a camera to delete.')
            return
        
        row = self.camerasTable.currentRow()
        camera_id = int(self.camerasTable.item(row, 0).text())
        camera_name = self.camerasTable.item(row, 1).text()
        
        reply = QMessageBox.question(
            self, 'Confirm Deletion',
            f'Are you sure you want to delete camera "{camera_name}"?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.db.delete_camera(camera_id)
                self.load_cameras()
                self.statusbar.showMessage(f'Deleted camera: {camera_name}')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to delete camera: {str(e)}')
    
    # ==================== Filter Type Methods ====================
    
    def load_filter_types(self):
        """Load all filter types from database and display in table."""
        try:
            filter_types = self.db.get_all_filter_types()
            self.filterTypesTable.setRowCount(len(filter_types))
            
            for row, ft in enumerate(filter_types):
                self.filterTypesTable.setItem(row, 0, QTableWidgetItem(str(ft['id'])))
                self.filterTypesTable.setItem(row, 1, QTableWidgetItem(ft['name']))
            
            self.statusbar.showMessage(f'Loaded {len(filter_types)} filter type(s)')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load filter types: {str(e)}')
    
    def add_filter_type(self):
        """Add a new filter type to the database."""
        name = self.filterTypeNameLineEdit.text().strip()
        
        if not name:
            QMessageBox.warning(self, 'Warning', 'Please enter a filter type name.')
            return
        
        try:
            self.db.add_filter_type(name)
            self.filterTypeNameLineEdit.clear()
            self.load_filter_types()
            self.update_filter_type_combo()
            self.statusbar.showMessage(f'Added filter type: {name}')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to add filter type: {str(e)}')
    
    def edit_filter_type(self):
        """Edit the selected filter type."""
        selected_rows = self.filterTypesTable.selectedItems()
        
        if not selected_rows:
            QMessageBox.warning(self, 'Warning', 'Please select a filter type to edit.')
            return
        
        row = self.filterTypesTable.currentRow()
        filter_type_id = int(self.filterTypesTable.item(row, 0).text())
        current_name = self.filterTypesTable.item(row, 1).text()
        
        new_name, ok = QInputDialog.getText(self, 'Edit Filter Type', 'Enter new name:', text=current_name)
        
        if ok and new_name.strip():
            try:
                self.db.update_filter_type(filter_type_id, new_name.strip())
                self.load_filter_types()
                self.update_filter_type_combo()
                self.statusbar.showMessage(f'Updated filter type ID {filter_type_id}')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to update filter type: {str(e)}')
    
    def delete_filter_type(self):
        """Delete the selected filter type."""
        selected_rows = self.filterTypesTable.selectedItems()
        
        if not selected_rows:
            QMessageBox.warning(self, 'Warning', 'Please select a filter type to delete.')
            return
        
        row = self.filterTypesTable.currentRow()
        filter_type_id = int(self.filterTypesTable.item(row, 0).text())
        filter_type_name = self.filterTypesTable.item(row, 1).text()
        
        reply = QMessageBox.question(
            self, 'Confirm Deletion',
            f'Are you sure you want to delete filter type "{filter_type_name}"?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.db.delete_filter_type(filter_type_id)
                self.load_filter_types()
                self.update_filter_type_combo()
                self.statusbar.showMessage(f'Deleted filter type: {filter_type_name}')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to delete filter type: {str(e)}')
    
    # ==================== Filter Methods ====================
    
    def update_filter_type_combo(self):
        """Update the filter type combo box with current filter types."""
        try:
            filter_types = self.db.get_all_filter_types()
            self.filterTypeComboBox.clear()
            for ft in filter_types:
                self.filterTypeComboBox.addItem(ft['name'])
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to update filter types: {str(e)}')
    
    def load_filters(self):
        """Load all filters from database and display in table."""
        try:
            filters = self.db.get_all_filters()
            self.filtersTable.setRowCount(len(filters))
            
            for row, filt in enumerate(filters):
                self.filtersTable.setItem(row, 0, QTableWidgetItem(str(filt['id'])))
                self.filtersTable.setItem(row, 1, QTableWidgetItem(filt['name']))
                self.filtersTable.setItem(row, 2, QTableWidgetItem(filt['type']))
            
            self.statusbar.showMessage(f'Loaded {len(filters)} filter(s)')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load filters: {str(e)}')
    
    def add_filter(self):
        """Add a new filter to the database."""
        name = self.filterNameLineEdit.text().strip()
        filter_type = self.filterTypeComboBox.currentText()
        
        if not name:
            QMessageBox.warning(self, 'Warning', 'Please enter a filter name.')
            return
        
        if not filter_type:
            QMessageBox.warning(self, 'Warning', 'Please select a filter type.')
            return
        
        try:
            self.db.add_filter(name, filter_type)
            self.filterNameLineEdit.clear()
            self.load_filters()
            self.statusbar.showMessage(f'Added filter: {name}')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to add filter: {str(e)}')
    
    def edit_filter(self):
        """Edit the selected filter."""
        selected_rows = self.filtersTable.selectedItems()
        
        if not selected_rows:
            QMessageBox.warning(self, 'Warning', 'Please select a filter to edit.')
            return
        
        row = self.filtersTable.currentRow()
        filter_id = int(self.filtersTable.item(row, 0).text())
        current_name = self.filtersTable.item(row, 1).text()
        current_type = self.filtersTable.item(row, 2).text()
        
        # Get available filter types
        filter_types = [ft['name'] for ft in self.db.get_all_filter_types()]
        
        dialog = EditFilterDialog(current_name, current_type, filter_types, self)
        if dialog.exec():
            name, filter_type = dialog.get_values()
            try:
                self.db.update_filter(filter_id, name, filter_type)
                self.load_filters()
                self.statusbar.showMessage(f'Updated filter ID {filter_id}')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to update filter: {str(e)}')
    
    def delete_filter(self):
        """Delete the selected filter."""
        selected_rows = self.filtersTable.selectedItems()
        
        if not selected_rows:
            QMessageBox.warning(self, 'Warning', 'Please select a filter to delete.')
            return
        
        row = self.filtersTable.currentRow()
        filter_id = int(self.filtersTable.item(row, 0).text())
        filter_name = self.filtersTable.item(row, 1).text()
        
        reply = QMessageBox.question(
            self, 'Confirm Deletion',
            f'Are you sure you want to delete filter "{filter_name}"?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.db.delete_filter(filter_id)
                self.load_filters()
                self.statusbar.showMessage(f'Deleted filter: {filter_name}')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to delete filter: {str(e)}')
    
    # ==================== Telescope Methods ====================
    
    def load_telescopes(self):
        """Load all telescopes from database and display in table."""
        try:
            telescopes = self.db.get_all_telescopes()
            self.telescopesTable.setRowCount(len(telescopes))
            
            for row, telescope in enumerate(telescopes):
                self.telescopesTable.setItem(row, 0, QTableWidgetItem(str(telescope['id'])))
                self.telescopesTable.setItem(row, 1, QTableWidgetItem(telescope['name']))
                self.telescopesTable.setItem(row, 2, QTableWidgetItem(str(telescope['aperture'])))
                self.telescopesTable.setItem(row, 3, QTableWidgetItem(str(telescope['f_ratio'])))
                self.telescopesTable.setItem(row, 4, QTableWidgetItem(str(telescope['focal_length'])))
            
            self.statusbar.showMessage(f'Loaded {len(telescopes)} telescope(s)')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load telescopes: {str(e)}')
    
    def add_telescope(self):
        """Add a new telescope to the database."""
        name = self.telescopeNameLineEdit.text().strip()
        aperture = self.apertureSpinBox.value()
        f_ratio = self.fRatioSpinBox.value()
        focal_length = self.focalLengthSpinBox.value()
        
        if not name:
            QMessageBox.warning(self, 'Warning', 'Please enter a telescope name.')
            return
        
        if aperture == 0 or f_ratio == 0 or focal_length == 0:
            QMessageBox.warning(self, 'Warning', 'Please enter valid aperture, f-ratio, and focal length.')
            return
        
        try:
            self.db.add_telescope(name, aperture, f_ratio, focal_length)
            self.telescopeNameLineEdit.clear()
            self.apertureSpinBox.setValue(0)
            self.fRatioSpinBox.setValue(0)
            self.focalLengthSpinBox.setValue(0)
            self.load_telescopes()
            self.statusbar.showMessage(f'Added telescope: {name}')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to add telescope: {str(e)}')
    
    def edit_telescope(self):
        """Edit the selected telescope."""
        selected_rows = self.telescopesTable.selectedItems()
        
        if not selected_rows:
            QMessageBox.warning(self, 'Warning', 'Please select a telescope to edit.')
            return
        
        row = self.telescopesTable.currentRow()
        telescope_id = int(self.telescopesTable.item(row, 0).text())
        current_name = self.telescopesTable.item(row, 1).text()
        current_aperture = int(self.telescopesTable.item(row, 2).text())
        current_f_ratio = float(self.telescopesTable.item(row, 3).text())
        current_focal_length = int(self.telescopesTable.item(row, 4).text())
        
        dialog = EditTelescopeDialog(current_name, current_aperture, current_f_ratio, 
                                     current_focal_length, self)
        if dialog.exec():
            name, aperture, f_ratio, focal_length = dialog.get_values()
            try:
                self.db.update_telescope(telescope_id, name, aperture, f_ratio, focal_length)
                self.load_telescopes()
                self.statusbar.showMessage(f'Updated telescope ID {telescope_id}')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to update telescope: {str(e)}')
    
    def delete_telescope(self):
        """Delete the selected telescope."""
        selected_rows = self.telescopesTable.selectedItems()
        
        if not selected_rows:
            QMessageBox.warning(self, 'Warning', 'Please select a telescope to delete.')
            return
        
        row = self.telescopesTable.currentRow()
        telescope_id = int(self.telescopesTable.item(row, 0).text())
        telescope_name = self.telescopesTable.item(row, 1).text()
        
        reply = QMessageBox.question(
            self, 'Confirm Deletion',
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
                QMessageBox.critical(self, 'Error', f'Failed to delete telescope: {str(e)}')

    def calculate_f_ratio(self):
        """Automatically calculate and fill F-ratio when aperture and focal length are entered."""
        aperture = self.apertureSpinBox.value()
        focal_length = self.focalLengthSpinBox.value()

        # Only calculate if both values are greater than 0
        if aperture > 0 and focal_length > 0:
            f_ratio = focal_length / aperture
            # Round to one decimal place as requested
            rounded_f_ratio = round(f_ratio, 1)
            self.fRatioSpinBox.setValue(rounded_f_ratio)

    # ==================== Observation Methods ====================
    
    def update_observation_combos(self):
        """Update all combo boxes in the observations tab."""
        try:
            # Update Session ID combo
            sessions = self.db.get_all_sessions()
            self.sessionIdComboBox.clear()
            for session in sessions:
                self.sessionIdComboBox.addItem(session['session_id'])
            
            # Update Object combo
            objects = self.db.get_all_objects()
            self.objectComboBox.clear()
            for obj in objects:
                self.objectComboBox.addItem(obj['name'])
            
            # Update Camera combo
            cameras = self.db.get_all_cameras()
            self.cameraComboBox.clear()
            for camera in cameras:
                self.cameraComboBox.addItem(camera['name'])
            
            # Update Telescope combo
            telescopes = self.db.get_all_telescopes()
            self.telescopeComboBox.clear()
            for telescope in telescopes:
                self.telescopeComboBox.addItem(telescope['name'])
            
            # Update Filter combo
            filters = self.db.get_all_filters()
            self.filterComboBox.clear()
            for filt in filters:
                self.filterComboBox.addItem(filt['name'])
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to update observation combos: {str(e)}')
    
    def load_observations(self):
        """Load all observations from database and display in table."""
        try:
            observations = self.db.get_all_observations()
            self.observationsTable.setRowCount(len(observations))
            
            for row, obs in enumerate(observations):
                self.observationsTable.setItem(row, 0, QTableWidgetItem(str(obs['id'])))
                self.observationsTable.setItem(row, 1, QTableWidgetItem(obs['session_id']))
                self.observationsTable.setItem(row, 2, QTableWidgetItem(obs['object_name']))
                self.observationsTable.setItem(row, 3, QTableWidgetItem(obs['camera_name']))
                self.observationsTable.setItem(row, 4, QTableWidgetItem(obs['telescope_name']))
                self.observationsTable.setItem(row, 5, QTableWidgetItem(obs['filter_name']))
                self.observationsTable.setItem(row, 6, QTableWidgetItem(str(obs['image_count'])))
                self.observationsTable.setItem(row, 7, QTableWidgetItem(str(obs['exposure_length'])))
                self.observationsTable.setItem(row, 8, QTableWidgetItem(str(obs['total_exposure'])))
                self.observationsTable.setItem(row, 9, QTableWidgetItem(obs['comments'] or ''))
            
            self.statusbar.showMessage(f'Loaded {len(observations)} observation(s)')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load observations: {str(e)}')
    
    def add_observation(self):
        """Add a new observation to the database."""
        session_id = self.sessionIdComboBox.currentText()
        object_name = self.objectComboBox.currentText()
        camera_name = self.cameraComboBox.currentText()
        telescope_name = self.telescopeComboBox.currentText()
        filter_name = self.filterComboBox.currentText()
        image_count = self.imageCountSpinBox.value()
        exposure_length = self.exposureLengthSpinBox.value()
        comments = self.commentsLineEdit.text().strip()
        
        if not all([session_id, object_name, camera_name, telescope_name, filter_name]):
            QMessageBox.warning(self, 'Warning', 'Please select all required fields.')
            return
        
        if image_count == 0 or exposure_length == 0:
            QMessageBox.warning(self, 'Warning', 'Please enter valid image count and exposure length.')
            return
        
        try:
            self.db.add_observation(session_id, object_name, camera_name, telescope_name,
                                   filter_name, image_count, exposure_length, comments)
            self.imageCountSpinBox.setValue(0)
            self.exposureLengthSpinBox.setValue(0)
            self.commentsLineEdit.clear()
            self.load_observations()
            self.statusbar.showMessage(f'Added observation for {object_name}')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to add observation: {str(e)}')
    
    def edit_observation(self):
        """Edit the selected observation."""
        selected_rows = self.observationsTable.selectedItems()
        
        if not selected_rows:
            QMessageBox.warning(self, 'Warning', 'Please select an observation to edit.')
            return
        
        row = self.observationsTable.currentRow()
        observation_id = int(self.observationsTable.item(row, 0).text())
        current_session_id = self.observationsTable.item(row, 1).text()
        current_object = self.observationsTable.item(row, 2).text()
        current_camera = self.observationsTable.item(row, 3).text()
        current_telescope = self.observationsTable.item(row, 4).text()
        current_filter = self.observationsTable.item(row, 5).text()
        current_image_count = int(self.observationsTable.item(row, 6).text())
        current_exposure = int(self.observationsTable.item(row, 7).text())
        current_comments = self.observationsTable.item(row, 9).text()
        
        # Get available options
        sessions = [s['session_id'] for s in self.db.get_all_sessions()]
        objects = [o['name'] for o in self.db.get_all_objects()]
        cameras = [c['name'] for c in self.db.get_all_cameras()]
        telescopes = [t['name'] for t in self.db.get_all_telescopes()]
        filters = [f['name'] for f in self.db.get_all_filters()]
        
        dialog = EditObservationDialog(
            current_session_id, current_object, current_camera, current_telescope,
            current_filter, current_image_count, current_exposure, current_comments,
            sessions, objects, cameras, telescopes, filters, self
        )
        
        if dialog.exec():
            session_id, object_name, camera_name, telescope_name, filter_name, \
                image_count, exposure_length, comments = dialog.get_values()
            try:
                self.db.update_observation(observation_id, session_id, object_name,
                                          camera_name, telescope_name, filter_name,
                                          image_count, exposure_length, comments)
                self.load_observations()
                self.statusbar.showMessage(f'Updated observation ID {observation_id}')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to update observation: {str(e)}')
    
    def delete_observation(self):
        """Delete the selected observation."""
        selected_rows = self.observationsTable.selectedItems()
        
        if not selected_rows:
            QMessageBox.warning(self, 'Warning', 'Please select an observation to delete.')
            return
        
        row = self.observationsTable.currentRow()
        observation_id = int(self.observationsTable.item(row, 0).text())
        object_name = self.observationsTable.item(row, 2).text()
        
        reply = QMessageBox.question(
            self, 'Confirm Deletion',
            f'Are you sure you want to delete observation for "{object_name}"?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.db.delete_observation(observation_id)
                self.load_observations()
                self.statusbar.showMessage(f'Deleted observation for {object_name}')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to delete observation: {str(e)}')

    def on_tab_changed(self, index):
        """Handle tab change events."""
        # Get the tab text to identify which tab was selected
        tab_text = self.tabWidget.tabText(index)
        if tab_text == "Observations":
            # Update the observation combo boxes when switching to the Observations tab
            self.update_observation_combos()

    def closeEvent(self, event):
        """Handle window close event."""
        self.db.close()
        event.accept()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
    