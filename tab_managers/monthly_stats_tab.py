"""Monthly Stats tab manager for the observation log application."""

import os
from PyQt6.QtWidgets import QWidget, QMessageBox, QVBoxLayout
from PyQt6 import uic
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class MonthlyStatsTabManager:
    """Manages the Monthly Stats tab functionality."""
    
    def __init__(self, parent, db, tab_widget, statusbar):
        """
        Initialize the Monthly Stats tab manager.
        
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
        """Setup the Monthly Stats tab."""
        stats_widget = QWidget()
        base_dir = os.path.dirname(os.path.dirname(__file__))
        ui_path = os.path.join(base_dir, 'monthly_stats_tab.ui')
        uic.loadUi(ui_path, stats_widget)
        self.tab_widget.addTab(stats_widget, "Monthly Stats")
        
        # Get reference to chart widget container
        self.chart_widget = stats_widget.findChild(QWidget, "chartWidget")
        
        # Create matplotlib figure and canvas
        self.figure = Figure(figsize=(10, 6))
        self.canvas = FigureCanvas(self.figure)
        
        # Add canvas to the chart widget
        layout = QVBoxLayout(self.chart_widget)
        layout.addWidget(self.canvas)
        self.chart_widget.setLayout(layout)
        
        # Load initial data
        self.load_stats()
    
    def load_stats(self):
        """Load monthly statistics from database and display in bar chart."""
        try:
            # Get monthly stats data
            stats_data = self.db.get_monthly_stats()
            
            if not stats_data:
                # No data to display
                self.figure.clear()
                ax = self.figure.add_subplot(111)
                ax.text(0.5, 0.5, 'No observation data available', 
                       ha='center', va='center', fontsize=14)
                ax.axis('off')
                self.canvas.draw()
                self.statusbar.showMessage('No observation data available')
                return
            
            # Extract months and exposures
            months = [row['year_month'] for row in stats_data]
            exposures = [row['total_exposure'] for row in stats_data]
            
            # Clear previous plot
            self.figure.clear()
            
            # Create bar chart
            ax = self.figure.add_subplot(111)
            bars = ax.bar(range(len(months)), exposures, color='steelblue', alpha=0.7)
            
            # Customize the chart
            ax.set_xlabel('Month', fontsize=12, fontweight='bold')
            ax.set_ylabel('Total Exposure (hours)', fontsize=12, fontweight='bold')
            ax.set_title('Monthly Cumulative Exposure Statistics', fontsize=14, fontweight='bold', pad=20)
            
            # Set x-axis labels
            ax.set_xticks(range(len(months)))
            ax.set_xticklabels(months, rotation=45, ha='right')
            
            # Add grid for better readability
            ax.grid(True, axis='y', alpha=0.3, linestyle='--')
            ax.set_axisbelow(True)
            
            # Add value labels on top of bars
            for i, (bar, value) in enumerate(zip(bars, exposures)):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{value:.1f}h',
                       ha='center', va='bottom', fontsize=9)
            
            # Adjust layout to prevent label cutoff
            self.figure.tight_layout()
            
            # Refresh canvas
            self.canvas.draw()
            
            self.statusbar.showMessage(f'Loaded stats for {len(months)} month(s)')
            
        except Exception as e:
            QMessageBox.critical(self.parent, 'Error', f'Failed to load monthly stats: {str(e)}')