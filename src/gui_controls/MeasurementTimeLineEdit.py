import re
from typing import Tuple

from PyQt5.QtCore import QRegularExpression
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtWidgets import QLineEdit


class MeasurementTimeLineEdit(QLineEdit):
    def __init__(self, default_value: str = "1 s"):
        super().__init__()
        # TODO add 0 mm/s validator
        self.speed_regex = r"^\d+(?:\.\d)?\s?(s|min)$"
        validator = QRegularExpressionValidator(QRegularExpression(self.speed_regex))
        self.setValidator(validator)
        self.setText(default_value)
        self.editingFinished.connect(lambda: print(self.parse()))

    def parse(self) -> Tuple[float, str]:
        if re.match(self.speed_regex, self.text()):
            value, unit = re.findall(r"(\d+(?:\.\d{1,2})?)\s?([^\d\s]+)", self.text())[0]
            return float(value), unit
        raise ValueError(f"Invalid input: {self.text()}")

    def set_value_from_seconds(self, new_value: float) -> None:
        if new_value / 60 < 1:
            self.setText(f"{new_value} s")
        elif new_value / (60**2) < 1:
            self.setText(f"{new_value / 60} min")

    def get_value_in_seconds(self) -> float:
        value, unit = self.parse()
        if unit == "s":
            return value
        elif unit == "min":
            return value / 60
        raise ValueError(f"Invalid unit: {unit}")
