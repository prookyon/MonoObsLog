"""Objects tab manager for the observation log application."""

from PyQt6.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QInputDialog
from PyQt6 import uic


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
        uic.loadUi('object_tab.ui', object_widget)
        self.tab_widget.addTab(object_widget, "Objects")

        # Store references
        self.objects_table = object_widget.findChild(QWidget, "objectsTable")
        self.name_line_edit = object_widget.findChild(QWidget, "nameLineEdit")
        self.add_button = object_widget.findChild(QWidget, "addButton")
        self.edit_button = object_widget.findChild(QWidget, "editButton")
        self.delete_button = object_widget.findChild(QWidget, "deleteButton")

        # Connect signals
        self.add_button.clicked.connect(self.add_object)
        self.edit_button.clicked.connect(self.edit_object)
        self.delete_button.clicked.connect(self.delete_object)
        self.name_line_edit.returnPressed.connect(self.add_object)

        # Hide ID column
        self.objects_table.setColumnHidden(0, True)
        self.objects_table.setColumnWidth(1, 600)

        self.load_objects()
    
    def load_objects(self):
        """Load all objects from database and display in table."""
        try:
            objects = self.db.get_all_objects()
            self.objects_table.setRowCount(len(objects))
            
            for row, obj in enumerate(objects):
                self.objects_table.setItem(row, 0, QTableWidgetItem(str(obj['id'])))
                self.objects_table.setItem(row, 1, QTableWidgetItem(obj['name']))
            
            self.statusbar.showMessage(f'Loaded {len(objects)} object(s)')
        except Exception as e:
            QMessageBox.critical(self.parent, 'Error', f'Failed to load objects: {str(e)}')
    
    def add_object(self):
        """Add a new object to the database."""
        name = self.name_line_edit.text().strip()
        
        if not name:
            QMessageBox.warning(self.parent, 'Warning', 'Please enter an object name.')
            return
        
        try:
            self.db.add_object(name)
            self.name_line_edit.clear()
            self.load_objects()
            self.statusbar.showMessage(f'Added object: {name}')
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
        
        new_name, ok = QInputDialog.getText(
            self.parent, 'Edit Object', 'Enter new name:', text=current_name
        )
        
        if ok and new_name.strip():
            try:
                self.db.update_object(object_id, new_name.strip())
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