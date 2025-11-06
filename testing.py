from datetime import datetime
import PyQt6.QtCore

from starplot import ZenithPlot, Observer as SPObserver, _
from starplot.styles import PlotStyle, extensions

def test_plot():
    observer = SPObserver(
        dt=datetime.now().astimezone(),
        lat=59.4458,
        lon=24.8847,
    )

    p = ZenithPlot(
        observer=observer,
        style=PlotStyle().extend(
            extensions.BLUE_MEDIUM,
        ),
        resolution=2000,
        autoscale=True,
    )
    p.horizon()
    p.constellations()
    p.stars(where=[_.magnitude < 4.6], where_labels=[_.magnitude < 2.4])
    p.constellation_labels()

    p.export("star_chart_basic.png", transparent=True, padding=0.1)

if __name__ == "__main__":
    test_plot()