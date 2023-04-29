
import numpy as np
from vector3d.vector import Vector

from PrinterPath import Square, PrinterPath


class Measurement(PrinterPath):
    def __init__(
        self,
        pass_height: float,
        antenna_offset: Vector,
        scanned_area: Square,
        measurement_radius: float,
        printer_bed_size: Vector,
    ):
        super().__init__(pass_height, antenna_offset, scanned_area, measurement_radius, printer_bed_size)

        self.x_axis_length = len(np.unique([pos.x for pos in self.get_antenna_path()]))
        self.y_axis_length = len(np.unique([pos.y for pos in self.get_antenna_path()]))

        self.scan_data = np.empty((self.x_axis_length, self.y_axis_length), float)
        self.scan_data.fill(None)

    def __iter__(self):
        return MeasurementIter(self)

    def add_measurement(self, pos, value):
        # TODO this should be improved
        #   scan_data should be indexed using x and y positions of measurement
        self.scan_data[pos // self.x_axis_length][pos % self.x_axis_length] = value


class MeasurementIter:
    def __init__(self, measurement: Measurement):
        self._extruder_path = measurement.extruder_path
        self._antenna_path = measurement.antenna_path
        self._scan_data: np.array = measurement.scan_data
        self._x_axis_length = measurement.x_axis_length
        self._class_size = len(self._extruder_path)
        self._current_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._current_index < self._class_size:
            member = (
                self._extruder_path[self._current_index],
                self._antenna_path[self._current_index],
                self._scan_data[self._current_index // self._x_axis_length][self._current_index % self._x_axis_length],
            )
            self._current_index += 1
            return member
        raise StopIteration
