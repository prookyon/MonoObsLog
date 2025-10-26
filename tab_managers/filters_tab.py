"""Filters tab manager for the observation log application."""

from PyQt6.QtWidgets import QWidget, QMessageBox, QTableWidgetItem
from PyQt6 import uic

from dialogs import EditFilterDialog


class FiltersTabManager:
    """Manages the Filters tab functionality."""
    
    def __init__(self, parent, db, tab_widget, statusbar):
        """
        Initialize the Filters tab manager.
        
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
        """Setup the Filters tab."""
        filter_widget = QWidget()
        uic.loadUi('filter_tab.ui', filter_widget)
        self.tab_widget.addTab(filter_widget, "Filters")
        
        # Store references
        self.filters_table = filter_widget.findChild(QWidget, "filtersTable")
        self.filter_name_line_edit = filter_widget.findChild(QWidget, "nameLineEdit")
        self.filter_type_combo_box = filter_widget.findChild(QWidget, "typeComboBox")
        self.add_filter_button = filter_widget.findChild(QWidget, "addFilterButton")
        self.edit_filter_button = filter_widget.findChild(QWidget, "editFilterButton")
        self.delete_filter_button = filter_widget.findChild(QWidget, "deleteFilterButton")
        
        # Connect signals
        self.add_filter_button.clicked.connect(self.add_filter)
        self.edit_filter_button.clicked.connect(self.edit_filter)
        self.delete_filter_button.clicked.connect(self.delete_filter)
        self.filter_name_line_edit.returnPressed.connect(self.add_filter)
        
        # Hide ID column
        self.filters_table.setColumnHidden(0, True)
        self.filters_table.setColumnWidth(1, 350)
        self.filters_table.setColumnWidth(2, 350)
        
        self.load_filters()
        self.update_filter_type_combo()
    
    def update_filter_type_combo(self):
        """Update the filter type combo box with current filter types."""
        try:
            filter_types = self.db.get_all_filter_types()
            self.filter_type_combo_box.clear()
            for ft in filter_types:
                self.filter_type_combo_box.addItem(ft['name'])
        except Exception as e:
            QMessageBox.critical(self.parent, 'Error', f'Failed to update filter types: {str(e)}')
    
    def load_filters(self):
        """Load all filters from database and display in table."""
        try:
            filters = self.db.get_all_filters()
            self.filters_table.setRowCount(len(filters))
            
            for row, filt in enumerate(filters):
                self.filters_table.setItem(row, 0, QTableWidgetItem(str(filt['id'])))
                self.filters_table.setItem(row, 1, QTableWidgetItem(filt['name']))
                self.filters_table.setItem(row, 2, QTableWidgetItem(filt['type']))
            
            self.statusbar.showMessage(f'Loaded {len(filters)} filter(s)')
        except Exception as e:
            QMessageBox.critical(self.parent, 'Error', f'Failed to load filters: {str(e)}')
    
    def add_filter(self):
        """Add a new filter to the database."""
        name = self.filter_name_line_edit.text().strip()
        filter_type = self.filter_type_combo_box.currentText()
        
        if not name:
            QMessageBox.warning(self.parent, 'Warning', 'Please enter a filter name.')
            return
        
        if not filter_type:
            QMessageBox.warning(self.parent, 'Warning', 'Please select a filter type.')
            return
        
        try:
            self.db.add_filter(name, filter_type)
            self.filter_name_line_edit.clear()
            self.load_filters()
            self.statusbar.showMessage(f'Added filter: {name}')
        except Exception as e:
            QMessageBox.critical(self.parent, 'Error', f'Failed to add filter: {str(e)}')
    
    def edit_filter(self):
        """Edit the selected filter."""
        selected_rows = self.filters_table.selectedItems()
        
        if not selected_rows:
            QMessageBox.warning(self.parent, 'Warning', 'Please select a filter to edit.')
            return
        
        row = self.filters_table.currentRow()
        filter_id = int(self.filters_table.item(row, 0).text())
        current_name = self.filters_table.item(row, 1).text()
        current_type = self.filters_table.item(row, 2).text()
        
        # Get available filter types
        filter_types = [ft['name'] for ft in self.db.get_all_filter_types()]
        
        dialog = EditFilterDialog(current_name, current_type, filter_types, self.parent)
        if dialog.exec():
            name, filter_type = dialog.get_values()
            try:
                self.db.update_filter(filter_id, name, filter_type)
                self.load_filters()
                self.statusbar.showMessage(f'Updated filter ID {filter_id}')
            except Exception as e:
                QMessageBox.critical(self.parent, 'Error', f'Failed to update filter: {str(e)}')
    
    def delete_filter(self):
        """Delete the selected filter."""
        selected_rows = self.filters_table.selectedItems()
        
        if not selected_rows:
            QMessageBox.warning(self.parent, 'Warning', 'Please select a filter to delete.')
            return
        
        row = self.filters_table.currentRow()
        filter_id = int(self.filters_table.item(row, 0).text())
        filter_name = self.filters_table.item(row, 1).text()
        
        reply = QMessageBox.question(
            self.parent, 'Confirm Deletion',
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
                QMessageBox.critical(self.parent, 'Error', f'Failed to delete filter: {str(e)}')