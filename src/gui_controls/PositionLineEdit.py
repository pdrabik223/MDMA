import re
from typing import Tuple

from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator, QValidator
from PyQt6.QtWidgets import (
    QLineEdit,
)


class ValidStringLength(QValidator):
    def __init__(self, parent):
        QValidator.__init__(self, parent)

        self.min = min
        self.max = max

    def validate(self, s, pos):

        if self.max > -1 and len(s) > self.max:
            return (QValidator.Invalid, pos)

        return (QValidator.Acceptable, pos)

    def fixup(self, s):
        pass


class PositionLineEdit(QLineEdit):
    def __init__(self, default_value: str = "50 mm"):
        super().__init__()
        self.speed_regex = r"^\d+(?:\.\d)?\s?(mm|cm)$"
        validator = QRegularExpressionValidator(QRegularExpression(self.speed_regex))
        self.setValidator(validator)
        self.setText(default_value)
        self.editingFinished.connect(lambda: print(self.parse()))

    def parse(self) -> Tuple[float, str]:
        if re.match(self.speed_regex, self.text()):
            value, unit = re.findall(r"(\d+(?:\.\d{1,2})?)\s?([^\d\s]+)", self.text())[0]
            return float(value), unit
        raise ValueError(f"Invalid input: {self.text()}")

    def set_value_in_mm(self, new_value: float) -> None:
        if new_value / 10 < 1:
            self.setText(f"{new_value} mm")
        elif new_value / (10 * 10) < 1:
            self.setText(f"{new_value / 10} cm")

    def get_value_in_mm(self) -> float:
        value, unit = self.parse()
        if unit == "mm":
            return value
        elif unit == "cm":
            return value * 10
        raise ValueError(f"Invalid unit: {unit}")
