"""Cameras tab manager for the observation log application."""

import os
from PyQt6.QtWidgets import QWidget, QMessageBox, QTableWidgetItem
from PyQt6 import uic

from dialogs import EditCameraDialog
from utilities.NumericTableWidgetItem import NumericTableWidgetItem


class CamerasTabManager:
    """Manages the Cameras tab functionality."""
    
    def __init__(self, parent, db, tab_widget, statusbar):
        """
        Initialize the Cameras tab manager.
        
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
        """Setup the Cameras tab."""
        camera_widget = QWidget()
        base_dir = os.path.dirname(os.path.dirname(__file__))
        ui_path = os.path.join(base_dir, 'camera_tab.ui')
        uic.loadUi(ui_path, camera_widget)
        self.tab_widget.addTab(camera_widget, "Cameras")
        
        # Store references
        self.cameras_table = camera_widget.findChild(QWidget, "camerasTable")
        self.camera_name_line_edit = camera_widget.findChild(QWidget, "nameLineEdit")
        self.sensor_line_edit = camera_widget.findChild(QWidget, "sensorLineEdit")
        self.pixel_size_spin_box = camera_widget.findChild(QWidget, "pixelSizeSpinBox")
        self.width_spin_box = camera_widget.findChild(QWidget, "widthSpinBox")
        self.height_spin_box = camera_widget.findChild(QWidget, "heightSpinBox")
        self.add_camera_button = camera_widget.findChild(QWidget, "addCameraButton")
        self.edit_camera_button = camera_widget.findChild(QWidget, "editCameraButton")
        self.delete_camera_button = camera_widget.findChild(QWidget, "deleteCameraButton")
        
        # Connect signals
        self.add_camera_button.clicked.connect(self.add_camera)
        self.edit_camera_button.clicked.connect(self.edit_camera)
        self.delete_camera_button.clicked.connect(self.delete_camera)
        self.camera_name_line_edit.returnPressed.connect(self.add_camera)
        
        # Hide ID column
        self.cameras_table.setColumnHidden(0, True)
        self.cameras_table.setColumnWidth(1, 180)
        self.cameras_table.setColumnWidth(2, 180)
        self.cameras_table.setColumnWidth(3, 100)
        self.cameras_table.setColumnWidth(4, 100)
        self.cameras_table.setColumnWidth(5, 100)
        
        self.load_cameras()
    
    def load_cameras(self):
        """Load all cameras from database and display in table."""
        try:
            cameras = self.db.get_all_cameras()
            self.cameras_table.setRowCount(len(cameras))
            
            for row, camera in enumerate(cameras):
                self.cameras_table.setItem(row, 0, QTableWidgetItem(str(camera['id'])))
                self.cameras_table.setItem(row, 1, QTableWidgetItem(camera['name']))
                self.cameras_table.setItem(row, 2, QTableWidgetItem(camera['sensor']))
                self.cameras_table.setItem(row, 3, NumericTableWidgetItem(camera['pixel_size']))
                self.cameras_table.setItem(row, 4, NumericTableWidgetItem(camera['width']))
                self.cameras_table.setItem(row, 5, NumericTableWidgetItem(camera['height']))
            
            self.statusbar.showMessage(f'Loaded {len(cameras)} camera(s)')
        except Exception as e:
            QMessageBox.critical(self.parent, 'Error', f'Failed to load cameras: {str(e)}')
    
    def add_camera(self):
        """Add a new camera to the database."""
        name = self.camera_name_line_edit.text().strip()
        sensor = self.sensor_line_edit.text().strip()
        pixel_size = self.pixel_size_spin_box.value()
        width = self.width_spin_box.value()
        height = self.height_spin_box.value()

        if not name or not sensor:
            QMessageBox.warning(self.parent, 'Warning', 'Please enter camera name and sensor.')
            return

        if pixel_size == 0 or width == 0 or height == 0:
            QMessageBox.warning(
                self.parent, 'Warning',
                'Please enter valid pixel size, width, and height.'
            )
            return

        # Check for duplicate camera name
        if self.db.camera_name_exists(name):
            QMessageBox.warning(self.parent, 'Warning', f'Camera name "{name}" already exists. Please choose a unique camera name.')
            return

        try:
            self.db.add_camera(name, sensor, pixel_size, width, height)
            self.camera_name_line_edit.clear()
            self.sensor_line_edit.clear()
            self.pixel_size_spin_box.setValue(0)
            self.width_spin_box.setValue(0)
            self.height_spin_box.setValue(0)
            self.load_cameras()
            self.statusbar.showMessage(f'Added camera: {name}')
        except Exception as e:
            QMessageBox.critical(self.parent, 'Error', f'Failed to add camera: {str(e)}')
    
    def edit_camera(self):
        """Edit the selected camera."""
        selected_rows = self.cameras_table.selectedItems()

        if not selected_rows:
            QMessageBox.warning(self.parent, 'Warning', 'Please select a camera to edit.')
            return

        row = self.cameras_table.currentRow()
        camera_id = int(self.cameras_table.item(row, 0).text())
        current_name = self.cameras_table.item(row, 1).text()
        current_sensor = self.cameras_table.item(row, 2).text()
        current_pixel_size = float(self.cameras_table.item(row, 3).text())
        current_width = int(self.cameras_table.item(row, 4).text())
        current_height = int(self.cameras_table.item(row, 5).text())

        dialog = EditCameraDialog(
            current_name, current_sensor, current_pixel_size,
            current_width, current_height, self.parent
        )
        if dialog.exec():
            name, sensor, pixel_size, width, height = dialog.get_values()

            # Check for duplicate camera name, excluding the current camera
            if self.db.camera_name_exists(name, exclude_id=camera_id):
                QMessageBox.warning(self.parent, 'Warning', f'Camera name "{name}" already exists. Please choose a unique camera name.')
                return

            try:
                self.db.update_camera(camera_id, name, sensor, pixel_size, width, height)
                self.load_cameras()
                self.statusbar.showMessage(f'Updated camera ID {camera_id}')
            except Exception as e:
                QMessageBox.critical(self.parent, 'Error', f'Failed to update camera: {str(e)}')
    
    def delete_camera(self):
        """Delete the selected camera."""
        selected_rows = self.cameras_table.selectedItems()
        
        if not selected_rows:
            QMessageBox.warning(self.parent, 'Warning', 'Please select a camera to delete.')
            return
        
        row = self.cameras_table.currentRow()
        camera_id = int(self.cameras_table.item(row, 0).text())
        camera_name = self.cameras_table.item(row, 1).text()
        
        reply = QMessageBox.question(
            self.parent, 'Confirm Deletion',
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
                QMessageBox.critical(self.parent, 'Error', f'Failed to delete camera: {str(e)}')