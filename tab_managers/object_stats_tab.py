"""Object Stats tab manager for the observation log application."""

from PyQt6.QtWidgets import QWidget, QMessageBox, QTableWidgetItem
from PyQt6 import uic


class ObjectStatsTabManager:
    """Manages the Object Stats tab functionality."""
    
    def __init__(self, parent, db, tab_widget, statusbar):
        """
        Initialize the Object Stats tab manager.
        
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
        """Setup the Object Stats tab."""
        stats_widget = QWidget()
        uic.loadUi('object_stats_tab.ui', stats_widget)
        self.tab_widget.addTab(stats_widget, "Object Stats")
        
        # Store reference to table
        self.stats_table = stats_widget.findChild(QWidget, "objectStatsTable")
        
        # Load initial data
        self.load_stats()
    
    def load_stats(self):
        """Load object statistics from database and display in table."""
        try:
            # Get raw stats data
            stats_data = self.db.get_object_stats()
            
            if not stats_data:
                # No data to display
                self.stats_table.setRowCount(0)
                self.stats_table.setColumnCount(0)
                self.statusbar.showMessage('No observation data available')
                return
            
            # Get unique object names and filter types
            object_names = sorted(set(row['object_name'] for row in stats_data))
            filter_types = sorted(set(row['filter_type'] for row in stats_data))
            
            # Create a dictionary to store stats: {object_name: {filter_type: total_exposure}}
            stats_dict = {}
            for row in stats_data:
                obj_name = row['object_name']
                filter_type = row['filter_type']
                total_exp = row['total_exposure']
                
                if obj_name not in stats_dict:
                    stats_dict[obj_name] = {}
                stats_dict[obj_name][filter_type] = total_exp
            
            # Setup table columns: Object Name + filter types + Total
            column_count = 1 + len(filter_types) + 1  # Object Name + filter types + Total
            self.stats_table.setColumnCount(column_count)
            
            # Set column headers
            headers = ['Object Name'] + filter_types + ['Total']
            self.stats_table.setHorizontalHeaderLabels(headers)
            
            # Setup table rows
            self.stats_table.setRowCount(len(object_names))
            
            # Populate table
            for row_idx, obj_name in enumerate(object_names):
                # Object name column
                self.stats_table.setItem(row_idx, 0, QTableWidgetItem(obj_name))
                
                # Calculate total for this object
                row_total = 0
                
                # Filter type columns
                for col_idx, filter_type in enumerate(filter_types):
                    exposure = stats_dict[obj_name].get(filter_type, 0)
                    row_total += exposure
                    self.stats_table.setItem(
                        row_idx, 
                        col_idx + 1, 
                        QTableWidgetItem(str(exposure))
                    )
                
                # Total column
                self.stats_table.setItem(
                    row_idx, 
                    len(filter_types) + 1, 
                    QTableWidgetItem(str(row_total))
                )
            
            # Adjust column widths
            self.stats_table.setColumnWidth(0, 150)  # Object Name
            for i in range(1, column_count):
                self.stats_table.setColumnWidth(i, 100)
            
            self.statusbar.showMessage(f'Loaded stats for {len(object_names)} object(s)')
            
        except Exception as e:
            QMessageBox.critical(self.parent, 'Error', f'Failed to load object stats: {str(e)}')