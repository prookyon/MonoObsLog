"""Filter Types tab manager for the observation log application."""

import os
from PyQt6.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QInputDialog
from PyQt6 import uic


class FilterTypesTabManager:
    """Manages the Filter Types tab functionality."""
    
    def __init__(self, parent, db, tab_widget, statusbar):
        """
        Initialize the Filter Types tab manager.
        
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
        """Setup the Filter Types tab."""
        filter_type_widget = QWidget()
        base_dir = os.path.dirname(os.path.dirname(__file__))
        ui_path = os.path.join(base_dir, 'uifiles', 'filter_type_tab.ui')
        uic.loadUi(ui_path, filter_type_widget)
        self.tab_widget.addTab(filter_type_widget, "Filter Types")
        
        # Store references
        self.filter_types_table = filter_type_widget.findChild(QWidget, "filterTypesTable")
        self.filter_type_name_line_edit = filter_type_widget.findChild(QWidget, "nameLineEdit")
        self.add_filter_type_button = filter_type_widget.findChild(QWidget, "addFilterTypeButton")
        self.edit_filter_type_button = filter_type_widget.findChild(QWidget, "editFilterTypeButton")
        self.delete_filter_type_button = filter_type_widget.findChild(QWidget, "deleteFilterTypeButton")
        
        # Connect signals
        self.add_filter_type_button.clicked.connect(self.add_filter_type)
        self.edit_filter_type_button.clicked.connect(self.edit_filter_type)
        self.delete_filter_type_button.clicked.connect(self.delete_filter_type)
        self.filter_type_name_line_edit.returnPressed.connect(self.add_filter_type)
        
        # Hide ID column
        self.filter_types_table.setColumnHidden(0, True)
        self.filter_types_table.setColumnWidth(1, 600)
        
        self.load_filter_types()
    
    def load_filter_types(self):
        """Load all filter types from database and display in table."""
        try:
            filter_types = self.db.get_all_filter_types()
            self.filter_types_table.setRowCount(len(filter_types))
            
            for row, ft in enumerate(filter_types):
                self.filter_types_table.setItem(row, 0, QTableWidgetItem(str(ft['id'])))
                self.filter_types_table.setItem(row, 1, QTableWidgetItem(ft['name']))
            
            self.statusbar.showMessage(f'Loaded {len(filter_types)} filter type(s)')
        except Exception as e:
            QMessageBox.critical(self.parent, 'Error', f'Failed to load filter types: {str(e)}')
    
    def add_filter_type(self):
        """Add a new filter type to the database."""
        name = self.filter_type_name_line_edit.text().strip()

        if not name:
            QMessageBox.warning(self.parent, 'Warning', 'Please enter a filter type name.')
            return

        # Check for duplicate filter type name
        if self.db.filter_type_name_exists(name):
            QMessageBox.warning(self.parent, 'Warning', f'Filter type name "{name}" already exists. Please choose a unique filter type name.')
            return

        try:
            self.db.add_filter_type(name)
            self.filter_type_name_line_edit.clear()
            self.load_filter_types()
            self.statusbar.showMessage(f'Added filter type: {name}')
        except Exception as e:
            QMessageBox.critical(self.parent, 'Error', f'Failed to add filter type: {str(e)}')
    
    def edit_filter_type(self):
        """Edit the selected filter type."""
        selected_rows = self.filter_types_table.selectedItems()

        if not selected_rows:
            QMessageBox.warning(self.parent, 'Warning', 'Please select a filter type to edit.')
            return

        row = self.filter_types_table.currentRow()
        filter_type_id = int(self.filter_types_table.item(row, 0).text())
        current_name = self.filter_types_table.item(row, 1).text()

        new_name, ok = QInputDialog.getText(
            self.parent, 'Edit Filter Type', 'Enter new name:', text=current_name
        )

        if ok and new_name.strip():
            new_name = new_name.strip()
            # Check for duplicate filter type name, excluding the current filter type
            if self.db.filter_type_name_exists(new_name, exclude_id=filter_type_id):
                QMessageBox.warning(self.parent, 'Warning', f'Filter type name "{new_name}" already exists. Please choose a unique filter type name.')
                return

            try:
                self.db.update_filter_type(filter_type_id, new_name)
                self.load_filter_types()
                self.statusbar.showMessage(f'Updated filter type ID {filter_type_id}')
            except Exception as e:
                QMessageBox.critical(self.parent, 'Error', f'Failed to update filter type: {str(e)}')
    
    def delete_filter_type(self):
        """Delete the selected filter type."""
        selected_rows = self.filter_types_table.selectedItems()
        
        if not selected_rows:
            QMessageBox.warning(self.parent, 'Warning', 'Please select a filter type to delete.')
            return
        
        row = self.filter_types_table.currentRow()
        filter_type_id = int(self.filter_types_table.item(row, 0).text())
        filter_type_name = self.filter_types_table.item(row, 1).text()
        
        reply = QMessageBox.question(
            self.parent, 'Confirm Deletion',
            f'Are you sure you want to delete filter type "{filter_type_name}"?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.db.delete_filter_type(filter_type_id)
                self.load_filter_types()
                self.statusbar.showMessage(f'Deleted filter type: {filter_type_name}')
            except Exception as e:
                QMessageBox.critical(self.parent, 'Error', f'Failed to delete filter type: {str(e)}')