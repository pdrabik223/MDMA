import numpy as np
from vector3d.vector import Vector

from plot_widgets.PlotWidget import PlotType, PlotWidget
from PrinterPath import PrinterPath, Square


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

        self.axes.set_xlim3d(left=0, right=210)
        self.axes.set_ylim3d(bottom=0, top=210)
        self.axes.set_zlim3d(bottom=0, top=210)

        x = np.linspace(0, 210, 4)
        y = np.linspace(0, 210, 4)
        x, y = np.meshgrid(x, y)
        eq = x * 0 + y * 0

        self.axes.plot_surface(x, y, eq)

    @staticmethod
    def from_settings(
        pass_height: float,
        antenna_offset: Vector,
        scanned_area: Square,
        measurement_radius: float,
    ):
        return PrinterPathWidget3D(PrinterPath(pass_height, antenna_offset, scanned_area, measurement_radius))
