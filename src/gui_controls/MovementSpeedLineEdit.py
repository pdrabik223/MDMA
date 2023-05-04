import re
from typing import Tuple

from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import QLineEdit


class MovementSpeedLineEdit(QLineEdit):
    def __init__(self, default_value: str = "1000 mm/s"):
        super().__init__()
        # TODO add 0 mm/s validator
        self.speed_regex = r"^\d+(?:\.\d)?\s?(mm/s|mm/min|cm/s|cm/min)$"
        validator = QRegularExpressionValidator(QRegularExpression(self.speed_regex))
        self.setValidator(validator)
        self.setText(default_value)
        self.editingFinished.connect(lambda: print(self.parse()))

    def parse(self) -> Tuple[float, str]:
        if re.match(self.speed_regex, self.text()):
            value, unit = re.findall(r"(\d+(?:\.\d{1,2})?)\s?([^\d\s]+)", self.text())[0]
            return float(value), unit
        raise ValueError(f"Invalid input: {self.text()}")

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
