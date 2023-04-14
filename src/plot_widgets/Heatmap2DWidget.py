import sys
from typing import List, Optional

import pandas as pd
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow, QHBoxLayout

import numpy as np
from vector3d.vector import Vector

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from src.plot_widgets.PlotWidget import PlotWidget, PlotType


class Heatmap2DWidget(PlotWidget):
    def __init__(self):
        super().__init__(plot_type=PlotType.Heatmap2D)

        # create the color bar for the heatmap
        # self.color_bar_widget = pg.GradientWidget(orientation="right")

        # create the layout for the widget

        self.axes.set_xlabel("X [mm]")
        self.axes.set_ylabel("Y [mm]")
        self.axes.set_title("Measurement")

        dx, dy = 0.015, 0.05
        y, x = np.mgrid[slice(-4, 4 + dy, dy), slice(-4, 4 + dx, dx)]
        z = (1 - x / 3.0 + x ** 5 + y ** 5) * np.exp(-(x ** 2) - y ** 2)
        z = z[:-1, :-1]
        z_min, z_max = -np.abs(z).max(), np.abs(z).max()

        self.axes.set_xlim([x.min(), x.max()])
        self.axes.set_ylim([y.min(), y.max()])

        self.axes.imshow(
            z,
            cmap="Wistia",
            vmin=z_min,
            vmax=z_max,
            extent=[x.min(), x.max(), y.min(), y.max()],
            interpolation="none",
            origin="lower",
        )

        # set the data for the heatmap
        # self.setData(data)

    @staticmethod
    def from_dataframe(dataframe: pd.DataFrame = None):
        pass
