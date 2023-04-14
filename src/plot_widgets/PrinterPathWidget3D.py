import sys
from typing import List, Optional

import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow, QHBoxLayout

import numpy as np
from vector3d.vector import Vector

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from src.PrinterPath import PrinterPath, Square
from src.plot_widgets.PlotWidget import PlotWidget, PlotType


class PrinterPathWidget3D(PlotWidget):
    """
    Widget displaying path that printer takes while scanning the sample
    """

    def __init__(self, printer_path: PrinterPath, **kwargs):
        super().__init__(plot_type=PlotType.Path3D)
        self.printer_path = printer_path
        self.add_scan_bounding_box()

        self.axes.set_xlabel("X [mm]")
        self.axes.set_ylabel("Y [mm]")
        self.axes.set_zlabel("Z [mm]")
        self.axes.set_title("Extruder path")

        self.axes.set_xlim([0, 210])
        self.axes.set_ylim([0, 210])
        self.axes.set_zlim([0, 210])

        self.axes.legend(loc="upper right", fancybox=True)

    def add_scan_bounding_box(self):
        bounding_box_points = self.printer_path.get_antenna_bounding_box()
        bounding_box_points += bounding_box_points[0]

        z_printer_boundaries = [
            self.printer_path.pass_height for _ in range(len(bounding_box_points))
        ]

        self.axes.set_xlim3d(left=0, right=210)
        self.axes.set_ylim3d(bottom=0, top=210)
        self.axes.set_zlim3d(bottom=0, top=210)

        x = np.linspace(0, 210, 4)
        y = np.linspace(0, 210, 4)
        x, y = np.meshgrid(x, y)
        eq = x * 0 + y * 0

        self.axes.plot_surface(x, y, eq)

        # def data_for_cylinder_along_z(center_x, center_y, radius, height_z):
        #     z = np.linspace(0, height_z, 10)
        #     theta = np.linspace(0, 2 * np.pi, 10)
        #     theta_grid, z_grid = np.meshgrid(theta, z)
        #     x_grid = radius * np.cos(theta_grid) + center_x
        #     y_grid = radius * np.sin(theta_grid) + center_y
        #     return x_grid, y_grid, z_grid
        #
        # Xc, Yc, Zc = data_for_cylinder_along_z(100, 100, 20, 0)
        # self.axes.plot_surface(Xc, Yc, Zc)

        # axes = [55, 55, 2]
        # data = np.ones(axes)
        # self.axes.voxels(data)

        # self.axes.plot(
        #     x_printer_boundaries, y_printer_boundaries, z_printer_boundaries, color="black", alpha=0.6,
        #     label="Printer extruder movement path boundaries")

    @staticmethod
    def from_settings(
        pass_height: float,
        antenna_offset: Vector,
        scanned_area: Square,
        measurement_radius: float,
    ):
        return PrinterPathWidget3D(
            PrinterPath(pass_height, antenna_offset, scanned_area, measurement_radius)
        )
