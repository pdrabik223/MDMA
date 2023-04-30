from typing import Any, Callable

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
        self._current_index = 0

    def add_measurement(self, pos, value):
        # TODO this should be improved
        #   scan_data should be indexed using x and y positions of measurement
        x = pos // self.x_axis_length
        y = pos % self.x_axis_length
        if x % 2 != 0:
            y = self.y_axis_length - y - 1

        self.scan_data[x][y] = value

    def __iter__(self):
        return self

    def __next__(self) -> tuple[Vector, Vector, Callable[[Any], None]]:
        if self._current_index < len(self.extruder_path):
            curr_index = self._current_index
            self._current_index += 1
            return (
                self.extruder_path[curr_index],
                self.antenna_path[curr_index],
                lambda val: self.add_measurement(curr_index, val),
            )
        raise StopIteration
