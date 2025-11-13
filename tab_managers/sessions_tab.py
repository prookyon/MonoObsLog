"""Sessions tab manager for the observation log application."""

import os
import datetime
from PyQt6.QtWidgets import QWidget, QMessageBox, QTableWidgetItem, QTableWidget
from PyQt6.QtCore import QDate
from PyQt6 import uic

from database import Database
from dialogs import EditSessionDialog
from calculations import calculate_moon_data
from utilities.NumericTableWidgetItem import NumericTableWidgetItem


class SessionsTabManager:
    """Manages the Sessions tab functionality."""
    
    def __init__(self, parent, db: Database, tab_widget, statusbar):
        """
        Initialize the Sessions tab manager.
        
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
        """Setup the Sessions tab."""
        session_widget = QWidget()
        base_dir = os.path.dirname(os.path.dirname(__file__))
        ui_path = os.path.join(base_dir, 'uifiles', 'sessions_tab.ui')
        uic.loadUi(ui_path, session_widget)
        self.tab_widget.addTab(session_widget, "Sessions")
        
        # Store references
        self.sessions_table = session_widget.findChild(QTableWidget, "sessionsTable")
        self.session_name_line_edit = session_widget.findChild(QWidget, "sessionNameLineEdit")
        self.start_date_edit = session_widget.findChild(QWidget, "startDateEdit")
        self.comments_line_edit = session_widget.findChild(QWidget, "sessionCommentsLineEdit")
        self.add_session_button = session_widget.findChild(QWidget, "addSessionButton")
        self.edit_session_button = session_widget.findChild(QWidget, "editSessionButton")
        self.delete_session_button = session_widget.findChild(QWidget, "deleteSessionButton")
        
        # Set current date
        self.start_date_edit.setDate(QDate.currentDate())
        
        # Connect signals
        self.add_session_button.clicked.connect(self.add_session)
        self.edit_session_button.clicked.connect(self.edit_session)
        self.delete_session_button.clicked.connect(self.delete_session)
        self.session_name_line_edit.returnPressed.connect(self.add_session)
        
        # Hide ID column
        self.sessions_table.setColumnHidden(0, True)
        self.sessions_table.setColumnWidth(1, 200)
        self.sessions_table.setColumnWidth(2, 150)
        self.sessions_table.setColumnWidth(3, 100)
        self.sessions_table.setColumnWidth(4, 100)
        self.sessions_table.setColumnWidth(5, 100)
        
        self.load_sessions()
    
    def load_sessions(self):
        """Load all sessions from database and display in table."""
        try:
            sessions = self.db.get_all_sessions_with_totals()
            self.sessions_table.setRowCount(len(sessions))

            for row, session in enumerate(sessions):
                self.sessions_table.setItem(row, 0, QTableWidgetItem(str(session['id'])))
                # Display 'name' field instead of 'session_id'
                self.sessions_table.setItem(row, 1, QTableWidgetItem(session['name']))
                self.sessions_table.setItem(row, 2, QTableWidgetItem(session['start_date']))
                self.sessions_table.setItem(row, 3, NumericTableWidgetItem(f"{session['moon_illumination']:.0f}%" if session['moon_illumination'] is not None else ""))
                self.sessions_table.setItem(row, 4, NumericTableWidgetItem(f"{session['moon_ra']:.2f}°" if session['moon_ra'] is not None else ""))
                self.sessions_table.setItem(row, 5, NumericTableWidgetItem(f"{session['moon_dec']:.2f}°" if session['moon_dec'] is not None else ""))
                self.sessions_table.setItem(row, 6, NumericTableWidgetItem(f"{session['total']:.1f}" if session['total'] is not None else ""))
                self.sessions_table.setItem(row, 7, QTableWidgetItem(session['comments'] if session['comments'] is not None else ""))
            
            self.sessions_table.resizeColumnsToContents()
            self.statusbar.showMessage(f'Loaded {len(sessions)} session(s)')
        except Exception as e:
            QMessageBox.critical(self.parent, 'Error', f'Failed to load sessions: {str(e)}')
    
    def add_session(self):
        """Add a new session to the database."""
        name = self.session_name_line_edit.text().strip()
        start_date = self.start_date_edit.date().toString("yyyy-MM-dd")
        comments = self.comments_line_edit.text().strip()

        if not name:
            QMessageBox.warning(self.parent, 'Warning', 'Please enter a session name.')
            return

        # Check for duplicate session name
        if self.db.session_name_exists(name):
            QMessageBox.warning(self.parent, 'Warning', f'Session name "{name}" already exists. Please choose a unique session name.')
            return

        try:
            # Calculate moon data for the midnight following the start date
            start_date_plus_one = datetime.datetime.strptime(start_date, "%Y-%m-%d") + datetime.timedelta(days=1)
            moon_illumination, moon_ra, moon_dec = calculate_moon_data(start_date_plus_one.isoformat())

            self.db.add_session(name, start_date,comments, moon_illumination, moon_ra, moon_dec)
            self.session_name_line_edit.clear()
            self.comments_line_edit.clear()
            self.start_date_edit.setDate(QDate.currentDate())
            self.load_sessions()
            self.statusbar.showMessage(f'Added session: {name}')
        except Exception as e:
            QMessageBox.critical(self.parent, 'Error', f'Failed to add session: {str(e)}')
    
    def edit_session(self):
        """Edit the selected session."""
        selected_rows = self.sessions_table.selectedItems()

        if not selected_rows:
            QMessageBox.warning(self.parent, 'Warning', 'Please select a session to edit.')
            return

        row = self.sessions_table.currentRow()
        session_id = int(self.sessions_table.item(row, 0).text())
        current_name = self.sessions_table.item(row, 1).text()
        current_start_date = self.sessions_table.item(row, 2).text()
        current_comments = self.sessions_table.item(row, 7).text()

        dialog = EditSessionDialog(current_name, current_start_date,current_comments, self.parent)
        if dialog.exec():
            new_name, new_start_date, new_comments = dialog.get_values()

            # Check for duplicate session name, excluding the current session
            if self.db.session_name_exists(new_name, exclude_id=session_id):
                QMessageBox.warning(self.parent, 'Warning', f'Session name "{new_name}" already exists. Please choose a unique session name.')
                return

            try:
                # Calculate moon data for the new date
                new_start_date_plus_one = datetime.datetime.strptime(new_start_date, "%Y-%m-%d") + datetime.timedelta(days=1)
                moon_illumination, moon_ra, moon_dec = calculate_moon_data(new_start_date_plus_one.isoformat())

                self.db.update_session(session_id, new_name, new_start_date, new_comments, moon_illumination, moon_ra, moon_dec)
                self.load_sessions()
                self.statusbar.showMessage(f'Updated session ID {session_id}')
            except Exception as e:
                QMessageBox.critical(self.parent, 'Error', f'Failed to update session: {str(e)}')
    
    def delete_session(self):
        """Delete the selected session."""
        selected_rows = self.sessions_table.selectedItems()
        
        if not selected_rows:
            QMessageBox.warning(self.parent, 'Warning', 'Please select a session to delete.')
            return
        
        row = self.sessions_table.currentRow()
        session_id = int(self.sessions_table.item(row, 0).text())
        session_name = self.sessions_table.item(row, 1).text()
        
        reply = QMessageBox.question(
            self.parent, 'Confirm Deletion',
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
                QMessageBox.critical(self.parent, 'Error', f'Failed to delete session: {str(e)}')
