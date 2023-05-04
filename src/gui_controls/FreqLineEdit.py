import re
from typing import Tuple

from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import (
    QLineEdit,
)


class FreqLineEdit(QLineEdit):
    def __init__(self, default_value: str = "1.32 GHz"):
        super().__init__()
        self.freq_box_regex = r"^\d+(?:\.\d{1,2})?\s?(Hz|kHz|MHz|GHz)$"
        validator = QRegularExpressionValidator(QRegularExpression(self.freq_box_regex))
        self.setValidator(validator)
        self.setText(default_value)
        self.editingFinished.connect(lambda: print(self.parse()))

    def parse(self) -> Tuple[float, str]:
        if re.match(self.freq_box_regex, self.text()):
            value, unit = re.findall(r"(\d+(?:\.\d{1,2})?)\s?([^\d\s]+)", self.text())[0]
            return float(value), unit

        raise ValueError(f"Invalid input: {self.text()}")

    def set_frequency_in_hz(self, new_frequency: float) -> None:
        if new_frequency / 1e3 < 1:
            self.setText(f"{new_frequency} Hz")
        elif new_frequency / 1e6 < 1:
            self.setText(f"{new_frequency / 1e3} KHz")
        elif new_frequency / 1e9 < 1:
            self.setText(f"{new_frequency / 1e6} MHz")
        elif new_frequency / 1e12 < 1:
            self.setText(f"{new_frequency / 1e9} GHz")

    def get_frequency_in_hz(self):
        value, unit = self.parse()
        if unit == "Hz":
            return value
        elif unit == "kHz":
            return value * 1e3
        elif unit == "MHz":
            return value * 1e6
        elif unit == "GHz":
            return value * 1e9
        else:
            raise ValueError(f"Invalid unit: {unit}")
