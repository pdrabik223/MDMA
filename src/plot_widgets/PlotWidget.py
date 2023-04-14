import enum
import sys
from typing import List, Optional

import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow, QHBoxLayout

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class PlotType(enum.Enum):
    Path2D = 0
    Path3D = 1
    Heatmap2D = 2


class PlotWidget(QWidget):
    def __init__(self, plot_type: PlotType):
        super().__init__()

        self.fig = Figure(figsize=(10, 5), dpi=90)
        self.fig.tight_layout()

        if plot_type == PlotType.Path3D:
            self.axes = self.fig.add_subplot(111, projection="3d")
            self.axes.set_xlabel("Untitled")
            self.axes.set_ylabel("Untitled")
            self.axes.set_zlabel("Untitled")

        elif plot_type == PlotType.Path2D:
            self.axes = self.fig.add_subplot(111)
            self.axes.set_xlabel("Untitled")
            self.axes.set_ylabel("Untitled")

        elif plot_type == PlotType.Heatmap2D:
            self.axes = self.fig.add_subplot(111)


        self.axes.set_title("Untitled")
        self.axes.axis("square")
        self.axes.grid()

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.figure_canvas = FigureCanvas(self.fig)
        self.main_layout.addWidget(NavigationToolbar(self.figure_canvas, self))
        self.main_layout.addWidget(self.figure_canvas)

    def show(self):
        self.fig.draw()
