from vector3d.vector import Vector

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
)


class PrinterPositionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.current_position_x = QLabel("x: - mm")
        self.current_position_y = QLabel("y: - mm")
        self.current_position_z = QLabel("z: - mm")
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        printer_controller_label = QLabel("Current Extruder Position")
        printer_controller_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(printer_controller_label)
        coordinate_layout = QHBoxLayout()
        main_layout.addLayout(coordinate_layout)
        coordinate_layout.addWidget(self.current_position_x)
        coordinate_layout.addWidget(self.current_position_y)
        coordinate_layout.addWidget(self.current_position_z)

    def set_position(self, new_position: Vector) -> None:
        self.current_position_x.setText(f"x: {new_position.x} mm")
        self.current_position_y.setText(f"y: {new_position.y} mm")
        self.current_position_z.setText(f"z: {new_position.z} mm")

    def get_position(self) -> Vector:
        x = float(self.current_position_x.text()[3:-3]) if self.current_position_x.text() != "x: - mm" else None
        y = float(self.current_position_y.text()[3:-3]) if self.current_position_y.text() != "y: - mm" else None
        z = float(self.current_position_z.text()[3:-3]) if self.current_position_z.text() != "z: - mm" else None
        return Vector(x, y, z)

    # TODO Pocket measures temeprature of itself. figure out how to display that
