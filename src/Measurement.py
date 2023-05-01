from typing import Any, Callable

import numpy as np
import pandas as pd
from vector3d.vector import Vector

from PrinterPath import Square, PrinterPath


class Measurement:
    def __init__(
            self,
            pass_height: float = None,
            antenna_offset: Vector = None,
            scanned_area: Square = None,
            measurement_radius: float = None,
            printer_bed_size: Vector = None,
            data: pd.DataFrame = None
    ):
        if data is None:
            self.printer_path = PrinterPath(pass_height, antenna_offset, scanned_area, measurement_radius,
                                            printer_bed_size)
            x_labels = np.unique([pos.x for pos in self.printer_path.get_antenna_path()])
            y_labels = np.unique([pos.y for pos in self.printer_path.get_antenna_path()])

            self.x_axis_length = len(x_labels)
            self.y_axis_length = len(y_labels)

            scan_data = np.empty((self.x_axis_length, self.y_axis_length), float)
            scan_data.fill(None)
            self.data = pd.DataFrame(scan_data)

            self.data.columns = x_labels
            self.data.index = y_labels

        else:
            self.printer_path = None
            self.data = data

        self._current_index = 0

    @staticmethod
    def from_pd_dataframe(data: pd.DataFrame):
        return Measurement(data=data)

    def to_pd_dataframe(self) -> pd.DataFrame:
        return self.data

    def add_measurement(self, x, y, value):
        # TODO this should be improved
        #   scan_data should be indexed using x and y positions of measurement

        self.data[x][y] = value

    def __iter__(self):
        return self

    def __next__(self) -> tuple[Vector, Vector, Callable[[Any], None]]:
        if self._current_index < len(self.printer_path.extruder_path):
            curr_index = self._current_index
            self._current_index += 1
            return (
                self.printer_path.extruder_path[curr_index],
                self.printer_path.antenna_path[curr_index],
                lambda val: self.add_measurement(self.printer_path.antenna_path[curr_index].y,
                                                 self.printer_path.antenna_path[curr_index].x, val),
            )
        raise StopIteration
