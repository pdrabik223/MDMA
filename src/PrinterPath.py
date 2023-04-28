from typing import List, Optional, Tuple

import numpy as np
from vector3d.vector import Vector


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
    def __init__(
        self,
        pass_height: float,
        antenna_offset: Vector,
        scanned_area: Square,
        measurement_radius: float,
        printer_bed_size: Vector,
        **kwargs
    ):
        self.pass_height = pass_height
        self.antenna_offset = antenna_offset
        self.scanned_area = scanned_area
        self.measurement_radius = measurement_radius
        self.printer_bed_size = printer_bed_size

        self.antenna_path: Optional[List[Vector]] = None
        self.extruder_path: Optional[List[Vector]] = None
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
            Vector(
                x + self.scanned_area.position_x,
                y + self.scanned_area.position_y,
                self.pass_height + self.antenna_offset.z,
            )
            for x, y in path
        ]

        self.extruder_path: List[Vector] = [
            Vector(
                position.x + self.antenna_offset.x,
                position.y + self.antenna_offset.y,
                position.z,
            )
            for position in self.antenna_path
        ]

        for extruder_position, antenna_position in zip(self.extruder_path, self.antenna_path):
            if (
                extruder_position.x < 0
                or extruder_position.x > self.printer_bed_size.x
                or extruder_position.y < 0
                or extruder_position.y > self.printer_bed_size.y
                or antenna_position.x < 0
                or antenna_position.x > self.printer_bed_size.x
                or antenna_position.y < 0
                or antenna_position.y > self.printer_bed_size.y
            ):
                self.extruder_path.remove(extruder_position)
                self.antenna_path.remove(antenna_position)

    def get_extruder_path(self) -> List[Vector]:
        return self.extruder_path

    def get_antenna_path(self) -> List[Vector]:
        return self.antenna_path

    @property
    def no_measurements(self) -> int:
        return len(self.antenna_path)

    def get_antenna_bounding_box(self) -> List[Tuple[float, float]]:
        max_x = np.max([point.x for point in self.antenna_path])
        max_y = np.max([point.y for point in self.antenna_path])

        min_x = np.min([point.x for point in self.antenna_path])
        min_y = np.min([point.y for point in self.antenna_path])

        x_antenna_bounding_box = (min_x, min_x, max_x, max_x, min_x)
        y_antenna_bounding_box = (min_y, max_y, max_y, min_y, min_y)
        return [(x, y) for x, y in zip(x_antenna_bounding_box, y_antenna_bounding_box)]

    def get_antenna_min_x_val(self):
        return np.min([point.x for point in self.antenna_path])

    def get_antenna_max_x_val(self):
        return np.max([point.x for point in self.antenna_path])

    def get_antenna_min_y_val(self):
        return np.min([point.y for point in self.antenna_path])

    def get_antenna_max_y_val(self):
        return np.max([point.y for point in self.antenna_path])

    def get_extruder_bounding_box(self) -> List[Tuple[float, float]]:
        max_x = np.max([point.x for point in self.extruder_path])
        max_y = np.max([point.y for point in self.extruder_path])

        min_x = np.min([point.x for point in self.extruder_path])
        min_y = np.min([point.y for point in self.extruder_path])

        x_extruder_bounding_box = (min_x, min_x, max_x, max_x, min_x)
        y_extruder_bounding_box = (min_y, max_y, max_y, min_y, min_y)
        return [(x, y) for x, y in zip(x_extruder_bounding_box, y_extruder_bounding_box)]

    def get_no_scan_points(self) -> int:
        return len(self.extruder_path)

    def total_scan_time_in_seconds(self) -> int:
        # TODO this one should be calculated by printer handle,
        #   and Spectrum analyzer device
        return len(self.extruder_path) * 4 + 60
