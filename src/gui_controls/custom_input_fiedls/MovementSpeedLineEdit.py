import re
from typing import Tuple

from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import QLineEdit, QComboBox
from vector3d.vector import Vector

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
)

MM_PER_SEC = "mm/s"
MM_PER_MIN = "mm/min"
CM_PER_SEC = "cm/s"
CM_PER_MIN = "cm/min"


class MovementSpeedLineEdit(QWidget):
    def __init__(self, default_value: str = "1000 mm/s"):
        super().__init__()
        # TODO add 0 mm/s validator
        self.speed_regex = r"^[+-]?([0-9]*[.])?[0-9]+$"
        validator = QRegularExpressionValidator(QRegularExpression(self.speed_regex))
        self.input_box = QLineEdit(default_value)
        self.input_box.setValidator(validator)
        self.input_box.editingFinished.connect(lambda: print(self.parse()))

        self.unit_dropdown = QComboBox()
        self.unit_dropdown.addItem(MM_PER_SEC)
        self.unit_dropdown.addItem(MM_PER_MIN)
        self.unit_dropdown.addItem(CM_PER_SEC)
        self.unit_dropdown.addItem(CM_PER_MIN)

        self.unit_dropdown.editingFinished.connect(lambda: print(self.parse()))

    def init_ui(self):
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        main_layout.addWidget(self.input_box)
        main_layout.addLayout(self.unit_dropdown)

    def parse(self) -> Tuple[float, str]:
        if re.match(self.speed_regex, self.input_box.text()):
            return float(self.input_box.text())

        raise ValueError(f"Invalid input: {self.input_box.text()}")

    def set_value_in_mm_per_second(self, value: float) -> None:
        # TODO finish the value ladder
        # if value / 10 < 1:
        self.setText(f"{value} mm/s")
        # elif value / 60 < 1:
        #     self.setText(f"{value / 10} cm/s")
        #
        # elif value / 100 < 1:
        #     self.setText(f"{value / 60} cm/s")
        #
        # elif value / 60 * 100 < 1:
        #     self.setText(f"{value / 10} cm/s")

    def get_value_in_mm_per_second(self) -> float:
        value, unit = self.parse()
        if unit == "mm/s":
            return value
        elif unit == "mm/min":
            return value / 60
        elif unit == "cm/s":
            return value * 10
        elif unit == "cm/min":
            return value / 6
        else:
            raise ValueError(f"Invalid unit: {unit}")
