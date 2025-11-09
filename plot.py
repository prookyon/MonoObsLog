from datetime import datetime

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication

class ObjectsPlot:

    def __init__(self, parent, latitude: float, longitude: float, marker_coords: list[float, float, str]):
        self.parent = parent
        self.latitude = latitude
        self.longitude = longitude
        self.marker_coords = marker_coords
        self.plot = PlotWindow(self.parent)
        self.plot.show()
        QApplication.instance().processEvents()

    def _generate_plot(self):
        from starplot import Observer as SPObserver, _
        from starplot.styles import PlotStyle, extensions, PolygonStyle
        from starplot import ZenithPlot

        dt = datetime.now().astimezone()
        observer = SPObserver(
            dt=dt,
            lat=self.latitude,
            lon=self.longitude
        )
        
        p = ZenithPlot(
            observer=observer,
            style=PlotStyle().extend(
                extensions.BLUE_NIGHT,
            ),
            resolution=2000,
            scale=0.35,
        )

        for coords in self.marker_coords:
            object_name = coords[2]
            object_ra = coords[0]
            object_dec = coords[1]
            if object_ra is None or object_dec is None:
                continue
            p.marker(
                ra=object_ra * 15,
                dec=object_dec,
                style={
                    "marker": {
                        "size": 6,
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
                        "font_size": 22,
                        "font_weight": "bold",
                        "font_color": "hsl(44, 70%, 75%)",
                        "font_alpha": 1,
                        "offset_x": "auto",
                        "offset_y": "auto",
                        "anchor_point": "top right",
                    },
                },
                label=object_name,
            )

        p.sun()
        p.moon(show_phase=True)
        p.planets()
        p.zenith()
        p.constellations()
        p.stars(where=[_.magnitude < 4], where_labels=[False])
        p.celestial_equator()
        p.milky_way()
        p.ellipse([observer.lst+90.0, 0.0],180,180, PolygonStyle(edge_width=1,edge_color='red'))
        p.horizon()
        p.constellation_labels(style__font_alpha=0.4, auto_adjust=False)

        return p


    def display_plot(self):
        from starplot import ZenithPlot
        p: ZenithPlot = self._generate_plot()
        canvas = FigureCanvas(p.fig)
        self.plot.layout().removeWidget(self.plot.label)
        self.plot.setMinimumSize(640,480)
        self.plot.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, False)
        self.plot.showMaximized()
        self.plot.layout().addWidget(canvas)



    


class PlotWindow(QWidget):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowType.Window, True)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        self.setWindowTitle("Plot")
        layout = QVBoxLayout()
        self.label = QLabel()
        self.label.setText("Generating ...")
        layout.addWidget(self.label)
        self.setLayout(layout)