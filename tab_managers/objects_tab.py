"""Objects tab manager for the observation log application."""

import os
from datetime import datetime, timedelta, UTC
from PyQt6.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QTableWidget, QPushButton
from PyQt6 import uic
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import astropy.units as u
from astroplan import FixedTarget, Observer
from astroplan.plots import plot_airmass
from astropy.coordinates import EarthLocation, SkyCoord


from dialogs import EditObjectDialog
from utilities.NumericTableWidgetItem import NumericTableWidgetItem
from utilities.MplCanvas import MplCanvas
from calculations import calculate_transit_time
import settings
from plot import ObjectsPlot


class CalculateTransitWorker(QThread):
    """Worker thread for calculating transit times without blocking UI."""
    
    finished = pyqtSignal(list)  # Emits the list of objects with transit times when done
    error = pyqtSignal(str)  # Emits error message if something goes wrong
    
    def __init__(self, objects, latitude, longitude):
        super().__init__()
        self.objects = objects
        self.latitude = latitude
        self.longitude = longitude
    
    def run(self):
        """Calculate transit times in background thread."""
        try:
            # Pre-calculate transit times in background
            for obj in self.objects:
                if obj['ra'] is not None and obj['dec'] is not None:
                    transit_time = calculate_transit_time(
                        obj['ra'], obj['dec'],
                        self.latitude, self.longitude
                    )
                    obj['transit_time'] = transit_time.replace(tzinfo=UTC).astimezone().strftime('%H:%M')
                else:
                    obj['transit_time'] = None
            
            self.finished.emit(self.objects)
        except Exception as e:
            self.error.emit(str(e))


class ObjectsTabManager:
    """Manages the Objects tab functionality."""
    
    def __init__(self, parent, db, tab_widget, statusbar):
        """
        Initialize the Objects tab manager.
        
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
        self.worker = None  # Keep reference to worker thread
        self.setup_tab()
    
    def setup_tab(self):
        """Setup the Objects tab."""
        object_widget = QWidget()
        base_dir = os.path.dirname(os.path.dirname(__file__))
        ui_path = os.path.join(base_dir, 'uifiles', 'object_tab.ui')
        uic.loadUi(ui_path, object_widget)
        self.tab_widget.addTab(object_widget, "Objects")

        # Add matplotlib canvas
        self.canvas = MplCanvas(self, width=6, height=3, dpi=100)
        layout = object_widget.layout()
        layout.addWidget(self.canvas)


        # Store references
        self.objects_table = object_widget.findChild(QTableWidget, "objectsTable")
        self.name_line_edit = object_widget.findChild(QWidget, "nameLineEdit")
        self.add_button = object_widget.findChild(QWidget, "addButton")
        self.edit_button = object_widget.findChild(QWidget, "editButton")
        self.delete_button = object_widget.findChild(QWidget, "deleteButton")
        self.plot_button = object_widget.findChild(QPushButton, "plotButton")

        # Connect signals
        self.add_button.clicked.connect(self.add_object)
        self.edit_button.clicked.connect(self.edit_object)
        self.delete_button.clicked.connect(self.delete_object)
        self.name_line_edit.returnPressed.connect(self.add_object)
        self.objects_table.itemSelectionChanged.connect(self.selection_changed)
        self.plot_button.clicked.connect(self.display_plot)

        # Hide ID column
        self.objects_table.setColumnHidden(0, True)
        self.objects_table.setColumnWidth(1, 300)
        self.objects_table.setColumnWidth(2, 150)
        self.objects_table.setColumnWidth(3, 150)

        self.load_objects()
    
    def load_objects(self):
        """Load all objects from database and display in table (non-blocking)."""
        # Show loading message
        self.statusbar.showMessage('Loading objects...')
        
        try:
            # Get objects from database (fast, done in main thread)
            objects = self.db.get_all_objects()
            
            # Stop any existing worker
            if self.worker and self.worker.isRunning():
                self.worker.quit()
                self.worker.wait()
            
            # Create and start worker thread for transit time calculations
            self.worker = CalculateTransitWorker(objects, settings.get_latitude(), settings.get_longitude())
            self.worker.finished.connect(self._on_objects_loaded)
            self.worker.error.connect(self._on_load_error)
            self.worker.start()
        except Exception as e:
            self.statusbar.clearMessage()
            QMessageBox.critical(self.parent, 'Error', f'Failed to load objects: {str(e)}')
    
    def _on_objects_loaded(self, objects):
        """Handle loaded objects data and update UI (runs on main thread)."""
        try:
            self.objects_table.setRowCount(len(objects))
            
            for row, obj in enumerate(objects):
                self.objects_table.setItem(row, 0, QTableWidgetItem(str(obj['id'])))
                self.objects_table.setItem(row, 1, QTableWidgetItem(obj['name']))
                
                # Display RA coordinate in hours (or empty if None)
                ra_text = f"{obj['ra']:.6f}h" if obj['ra'] is not None else ""
                self.objects_table.setItem(row, 2, NumericTableWidgetItem(ra_text))
                self.objects_table.item(row,2).setData(Qt.ItemDataRole.UserRole, obj['ra'])
                
                # Display Dec coordinate (or empty if None)
                dec_text = f"{obj['dec']:.6f}°" if obj['dec'] is not None else ""
                self.objects_table.setItem(row, 3, NumericTableWidgetItem(dec_text))
                self.objects_table.item(row,3).setData(Qt.ItemDataRole.UserRole, obj['dec'])

                # Display pre-calculated transit time
                if obj.get('transit_time'):
                    self.objects_table.setItem(row, 4, QTableWidgetItem(obj['transit_time']))
            
            self.objects_table.resizeColumnsToContents()
            self.statusbar.showMessage(f'Loaded {len(objects)} object(s)')
        except Exception as e:
            QMessageBox.critical(self.parent, 'Error', f'Failed to display objects: {str(e)}')
    
    def _on_load_error(self, error_msg):
        """Handle error from worker thread (runs on main thread)."""
        self.statusbar.clearMessage()
        QMessageBox.critical(self.parent, 'Error', f'Failed to load objects: {error_msg}')
    
    def add_object(self):
        """Add a new object to the database."""
        name = self.name_line_edit.text().strip()

        if not name:
            QMessageBox.warning(self.parent, 'Warning', 'Please enter an object name.')
            return

        # Check for duplicate object name
        if self.db.object_name_exists(name):
            QMessageBox.warning(self.parent, 'Warning', f'Object name "{name}" already exists. Please choose a unique object name.')
            return

        try:
            # Open dialog for optional coordinate entry
            dialog = EditObjectDialog(name, parent=self.parent)
            if dialog.exec() == EditObjectDialog.DialogCode.Accepted:
                obj_name, ra, dec = dialog.get_values()
                self.db.add_object(obj_name, ra, dec)
                self.name_line_edit.clear()
                self.load_objects()
                self.statusbar.showMessage(f'Added object: {obj_name}')
        except Exception as e:
            QMessageBox.critical(self.parent, 'Error', f'Failed to add object: {str(e)}')
    
    def edit_object(self):
        """Edit the selected object."""
        selected_rows = self.objects_table.selectedItems()

        if not selected_rows:
            QMessageBox.warning(self.parent, 'Warning', 'Please select an object to edit.')
            return

        row = self.objects_table.currentRow()
        object_id = int(self.objects_table.item(row, 0).text())
        current_name = self.objects_table.item(row, 1).text()
        current_ra = self.objects_table.item(row, 2).text()
        current_dec = self.objects_table.item(row, 3).text()
        
        # Convert empty strings to None for coordinates, strip units
        ra = float(current_ra.rstrip('h')) if current_ra else None
        dec = float(current_dec.rstrip('°')) if current_dec else None

        dialog = EditObjectDialog(current_name, ra, dec, parent=self.parent)
        if dialog.exec() == EditObjectDialog.DialogCode.Accepted:
            new_name, new_ra, new_dec = dialog.get_values()
            new_name = new_name.strip()
            
            # Check for duplicate object name, excluding the current object
            if new_name != current_name and self.db.object_name_exists(new_name, exclude_id=object_id):
                QMessageBox.warning(self.parent, 'Warning', f'Object name "{new_name}" already exists. Please choose a unique object name.')
                return

            try:
                self.db.update_object(object_id, new_name, new_ra, new_dec)
                self.load_objects()
                self.statusbar.showMessage(f'Updated object ID {object_id}')
            except Exception as e:
                QMessageBox.critical(self.parent, 'Error', f'Failed to update object: {str(e)}')
    
    def delete_object(self):
        """Delete the selected object."""
        selected_rows = self.objects_table.selectedItems()
        
        if not selected_rows:
            QMessageBox.warning(self.parent, 'Warning', 'Please select an object to delete.')
            return
        
        row = self.objects_table.currentRow()
        object_id = int(self.objects_table.item(row, 0).text())
        object_name = self.objects_table.item(row, 1).text()
        
        reply = QMessageBox.question(
            self.parent, 'Confirm Deletion',
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
                QMessageBox.critical(self.parent, 'Error', f'Failed to delete object: {str(e)}')
    
    def selection_changed(self):
        """Handle selection change in the objects table."""
        self.canvas.fig.clear()
        selected_rows = self.objects_table.selectedItems()
        if selected_rows:
            row = self.objects_table.currentRow()
            object_name = self.objects_table.item(row, 1).text()
            object_ra = self.objects_table.item(row, 2).data(Qt.ItemDataRole.UserRole)
            object_dec = self.objects_table.item(row, 3).data(Qt.ItemDataRole.UserRole)
            if object_ra is None or object_dec is None:
                return
            
            time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
            target = FixedTarget(coord=SkyCoord(ra=object_ra*15*u.deg, dec=object_dec*u.deg), name=object_name)
            obs = Observer(EarthLocation(lat=settings.get_latitude()*u.deg,
                            lon=settings.get_longitude()*u.deg,
                            height=0*u.m))
            plot_airmass(target, obs, time.astimezone(),
                         self.canvas.fig.add_subplot(111),
                         brightness_shading=True,altitude_yaxis=True, use_local_tz=True)
            
    def display_plot(self):
        marker_coords: list[float,float,str] = []

        for row in range(0, self.objects_table.rowCount()):
            object_name = self.objects_table.item(row, 1).text()
            object_ra = self.objects_table.item(row, 2).data(Qt.ItemDataRole.UserRole)
            object_dec = self.objects_table.item(row, 3).data(Qt.ItemDataRole.UserRole)
            if object_ra is None or object_dec is None:
                continue
            marker_coords.append([object_ra,object_dec,object_name])

        plot = ObjectsPlot(self.parent,settings.get_latitude(),settings.get_longitude(), marker_coords)
        plot.display_plot()

            
   
