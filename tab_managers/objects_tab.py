"""Objects tab manager for the observation log application."""

import os, tempfile
from datetime import datetime, timedelta, UTC
from PyQt6.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QInputDialog, QTableWidget, QPushButton, QDialog, QVBoxLayout, QLabel
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import astropy.units as u
from astroplan import FixedTarget, Observer
from astroplan.plots import plot_airmass, plot_altitude
from astropy.coordinates import EarthLocation, SkyCoord
from starplot import ZenithPlot, Observer as SPObserver, _
from starplot.styles import PlotStyle, extensions

from dialogs import EditObjectDialog
from utilities import NumericTableWidgetItem
from calculations import calculate_transit_time
import settings
import image_viewer


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
        self.setup_tab()
    
    def setup_tab(self):
        """Setup the Objects tab."""
        object_widget = QWidget()
        base_dir = os.path.dirname(os.path.dirname(__file__))
        ui_path = os.path.join(base_dir, 'object_tab.ui')
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
        """Load all objects from database and display in table."""
        try:
            objects = self.db.get_all_objects()
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

                # Display transit time if both RA and Dec are available
                if obj['ra'] is not None and obj['dec'] is not None:
                    transit_time = calculate_transit_time(obj['ra'], obj['dec'], settings.get_latitude(), settings.get_longitude())
                    self.objects_table.setItem(row, 4, QTableWidgetItem(transit_time.replace(tzinfo=UTC).astimezone().strftime('%H:%M')))
            
            self.objects_table.resizeColumnsToContents()
            self.statusbar.showMessage(f'Loaded {len(objects)} object(s)')
        except Exception as e:
            QMessageBox.critical(self.parent, 'Error', f'Failed to load objects: {str(e)}')
    
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
        dt = datetime.now().astimezone()
        observer = SPObserver(
            dt=dt,
            lat=settings.get_latitude(),
            lon=settings.get_longitude()
        )
        
        p = ZenithPlot(
            observer=observer,
            style=PlotStyle().extend(
                extensions.BLUE_MEDIUM,
            ),
            resolution=3600,
            autoscale=True,
        )
        p.horizon()

        for row in range(0, self.objects_table.rowCount()):
            object_name = self.objects_table.item(row, 1).text()
            object_ra = self.objects_table.item(row, 2).data(Qt.ItemDataRole.UserRole)
            object_dec = self.objects_table.item(row, 3).data(Qt.ItemDataRole.UserRole)
            if object_ra is None or object_dec is None:
                continue
            p.marker(
                ra=object_ra * 15,
                dec=object_dec,
                style={
                    "marker": {
                        "size": 5,
                        "symbol": "diamond",
                        "fill": "full",
                        "color": "#F00",
                        "edge_color": "hsl(44, 70%, 73%)",
                        "edge_width": 2,
                        "line_style": "solid",
                        "alpha": 1,
                        "zorder": 2000,
                    },
                    "label": {
                        "zorder": 2000,
                        "font_size": 16,
                        "font_weight": "bold",
                        "font_color": "hsl(44, 70%, 64%)",
                        "font_alpha": 1,
                        "offset_x": "auto",
                        "offset_y": "auto",
                        "anchor_point": "top right",
                    },
                },
                label=object_name,
            )

        p.constellations()
        p.stars(where=[_.magnitude < 4.6], where_labels=[_.magnitude < 1.5])
        p.constellation_labels()

        # create file in temp folder
        temp_file_path = os.path.join(tempfile.gettempdir(), 'zenith_plot.png')
        p.export(temp_file_path, transparent=True, padding=0.1)

        viewer = image_viewer.ImageViewer(temp_file_path)
        viewer.show()

        #cleanup temp image
        os.remove(temp_file_path)

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)