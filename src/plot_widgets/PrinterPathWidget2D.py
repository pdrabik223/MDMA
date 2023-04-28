from vector3d.vector import Vector

from plot_widgets.PlotWidget import PlotType, PlotWidget
from PrinterPath import PrinterPath, Square


class PrinterPathWidget2D(PlotWidget):
    """
    Widget displaying path that printer takes while scanning the sample
    """

    def __init__(self, printer_path: PrinterPath, **kwargs):
        super().__init__(plot_type=PlotType.Path2D)
        self.printer_path = None
        self.update_from_printer_path(printer_path)

    def add_labels_and_axes_styling(self):
        self.axes_styling("Extruder path")
        self.axes.set_xlabel("X [mm]")
        self.axes.set_ylabel("Y [mm]")

    def _zoom_to_show_data(self):
        # TODO this fails sometimes for sample x position = 10 mm
        #   plot is not zoomed correctly
        antenna_x, antenna_y = zip(*self.printer_path.get_antenna_bounding_box())
        extruder_x, extruder_y = zip(*self.printer_path.get_extruder_bounding_box())

        global_x_min = min(antenna_x + extruder_x)
        global_y_min = min(antenna_y + extruder_y)

        global_x_max = max(antenna_x + extruder_x)
        global_y_max = max(antenna_y + extruder_y)

        if global_x_max - global_x_min > global_y_max - global_y_min:
            data_range = [global_x_min - 5, global_x_max + 5]
        else:
            data_range = [global_y_min - 5, global_y_max + 5]

        self.axes.set_xlim(data_range)
        self.axes.set_ylim(data_range)

    def add_scan_bounding_box(self):
        bounding_box_points = self.printer_path.get_extruder_bounding_box()
        bounding_box_points.append(bounding_box_points[0])

        self.axes.plot(
            *zip(*bounding_box_points),
            color="darkred",
            label="Printer extruder movement path boundaries",
        )

    def add_extruder_path(self):
        path = [(point.x, point.y) for point in self.printer_path.get_extruder_path()]

        self.axes.plot(
            *zip(*path),
            color="royalblue",
            label="Extruder path",
        )

        self.axes.scatter(
            *zip(*path),
            color="red",
            label="Measurement extruder points",
        )

    def add_antenna_path(self):
        path = [(point.x, point.y) for point in self.printer_path.get_antenna_path()]
        # TODO this should be circles not scatter
        self.axes.scatter(
            *zip(*path),
            color="gold",
            label="Measurement points",
        )

    @staticmethod
    def from_settings(
        pass_height: float,
        antenna_offset: Vector,
        scanned_area: Square,
        measurement_radius: float,
    ):
        return PrinterPathWidget2D(PrinterPath(pass_height, antenna_offset, scanned_area, measurement_radius))

    @staticmethod
    def from_printer_path(printer_path: PrinterPath):
        return PrinterPathWidget2D(printer_path)

    def update_from_printer_path(self, printer_path: PrinterPath):
        self.printer_path = printer_path
        self.axes.cla()
        self.add_labels_and_axes_styling()

        self._zoom_to_show_data()
        self.add_scan_bounding_box()
        self.add_extruder_path()
        self.add_antenna_path()
        self.axes.legend(loc="upper right", fancybox=True)
