import sys
from typing import List, Optional

import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow, QHBoxLayout

import numpy as np
from vector3d.vector import Vector

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class Square:
    def __init__(self, x: float, y: float, width: float, height: float):
        self.position_x = x
        self.position_y = y
        self.width = width
        self.height = height


def f_range(
        start: float = 0,
        end: float = 1,
        step: float = 1,
        include_start=True,
        include_end=False,
):
    range = []

    temp_value = start

    if include_start:
        range.append(temp_value)

    temp_value += step
    while temp_value < end:
        range.append(temp_value)
        temp_value += step

    if include_end:
        range.append(temp_value)

    return range


class PrinterPath:
    def __init__(self,
                 pass_height: float,
                 antenna_offset: Vector,
                 scanned_area: Square,
                 measurement_radius: float, **kwargs):

        self.pass_height = pass_height
        self.antenna_offset = antenna_offset
        self.scanned_area = scanned_area
        self.measurement_radius = measurement_radius

        self.antenna_path: Optional[List[Vector]] = None
        self.measurement_path: Optional[List[Vector]] = None
        self.generate_path()

    def generate_path(self):
        x_measurements_coords = [
            x
            for x in f_range(
                self.measurement_radius / 2,
                self.scanned_area.position_x,
                self.measurement_radius,
                include_end=True,
            )
        ]
        y_measurements_coords = [
            y
            for y in f_range(
                self.measurement_radius / 2,
                self.scanned_area.position_y,
                self.measurement_radius,
                include_end=True,
            )
        ]

        path = []
        flip = False
        for x in x_measurements_coords:
            flip = not flip
            if flip:
                for id in range(0, len(y_measurements_coords), 1):
                    path.append((x, y_measurements_coords[id]))
            else:
                for id in range(len(y_measurements_coords) - 1, -1, -1):
                    path.append((x, y_measurements_coords[id]))

        self.antenna_path = [
            Vector(x + self.scanned_area.position_x,
                   y + self.scanned_area.position_y,
                   self.pass_height + self.antenna_offset.z)
            for x, y in path
        ]

        self.measurement_path = [
            Vector(position.x + self.antenna_offset.x, position.y + self.antenna_offset.y, position.z)
            for position in self.antenna_path
        ]

    def get_measurement_path(self):
        return self.measurement_path

    def get_antenna_path(self):
        return self.antenna_path


class PrinterPathWidget(QWidget):
    """
    Widget displaying path that printer takes while scanning the sample
    """

    def __init__(self, printer_path, **kwargs):
        super().__init__()
        self.printer_path = printer_path

        self.fig = Figure(figsize=(9, 5), dpi=90)
        self.fig.tight_layout()

        self.axes = self.fig.add_subplot(111, projection='3d')

        self.axes.axis("square")
        self.axes.grid()
        self.axes.set_xlabel("X [mm]")
        self.axes.set_ylabel("Y [mm]")
        self.axes.set_zlabel("Z [mm]")
        self.axes.set_title("Extruder path")
        self.axes.legend()

        self.add_scan_bounding_box()
        self.main_layout = QVBoxLayout()
        self.figure_canvas = FigureCanvas(self.fig)
        # toolbar = NavigationToolbar(self.fig, self.figure_canvas)

        # self.main_layout.addWidget(toolbar)
        self.main_layout.addWidget(self.figure_canvas)
        self.setLayout(self.main_layout)

    def add_scan_bounding_box(self):
        max_x = np.max([point.x for point in self.printer_path.measurement_path])
        max_y = np.max([point.x for point in self.printer_path.measurement_path])
        min_x = np.min([point.x for point in self.printer_path.measurement_path])
        min_y = np.min([point.x for point in self.printer_path.measurement_path])

        x_printer_boundaries = (min_x, min_x, max_x, max_x, min_x)
        y_printer_boundaries = (min_y, max_y, max_y, min_y, min_y)
        z_printer_boundaries = [self.printer_path.pass_height for _ in range(len(y_printer_boundaries))]

        self.axes.plot(
            x_printer_boundaries, y_printer_boundaries, z_printer_boundaries, color="black", alpha=0.6,
            label="Printer extruder movement path boundaries")

    def show(self):
        self.fig.draw()

    @staticmethod
    def from_settings(pass_height: float,
                      antenna_offset: Vector,
                      scanned_area: Square,
                      measurement_radius: float):
        return PrinterPathWidget(PrinterPath(pass_height,
                                             antenna_offset,
                                             scanned_area,
                                             measurement_radius))

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
            self.color_bar_widget = pg.GradientWidget(orientation='right')

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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Window")
        self.setGeometry(100, 100, 800, 600)

        # create a vertical layout for the window
        # self.main_layout = QVBoxLayout(self)
        self.setCentralWidget(PrinterPathWidget.from_settings(pass_height=5,
                                                              antenna_offset=Vector(1, 3, 4),
                                                              scanned_area=Square(1, 1, 20, 20),
                                                              measurement_radius=3))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
