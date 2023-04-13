import sys
from typing import List, Optional

import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow, QHBoxLayout

import numpy as np
from vector3d.vector import Vector

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class Heatmap2D(QWidget):
    def __init__(self, data):
        super().__init__()

        # create the ImageItem for the heatmap
        self.image_item = pg.ImageItem()

        # create the PlotWidget to display the heatmap
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.addItem(self.image_item)

        # set the axis labels and title for the heatmap
        self.plot_widget.setLabel("bottom", "X Axis")
        self.plot_widget.setLabel("left", "Y Axis")
        self.plot_widget.setTitle("2D Heatmap")

        # create the color bar for the heatmap
        self.color_bar_widget = pg.GradientWidget(orientation="right")

        # create the layout for the widget
        self.central_layout = QHBoxLayout()
        self.central_layout.addWidget(self.plot_widget)
        self.central_layout.addWidget(self.color_bar_widget)
        self.setLayout(self.central_layout)

        # set the data for the heatmap
        self.setData(data)

    def setData(self, data):
        # set the data for the heatmap and update the color bar
        self.image_item.setImage(data)
        # self.color_bar_widget.setGradient(self.image_item.getLookupTable())
