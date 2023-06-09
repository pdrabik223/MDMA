import re
from typing import Tuple

from PyQt6.QtCore import QRegularExpression, Qt
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import (
    QLineEdit,
    QComboBox,
    QHBoxLayout,
    QWidget,
)

HZ = "Hz"
KHZ = "KHz"
MHZ = "MHz"
GHZ = "GHz"


class FreqLineEdit(QWidget):
    def __init__(self, default_value: str = "1.32", default_speed: str = GHZ):
        super().__init__()
        self.freq_box_regex = r"^[+-]?([0-9]*[.])?[0-9]+$"
        validator = QRegularExpressionValidator(QRegularExpression(self.freq_box_regex))
        self.input_box = QLineEdit(default_value)
        self.input_box.setMaximumWidth(80)
        self.input_box.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.input_box.setValidator(validator)
        self.input_box.editingFinished.connect(lambda: print(self.get_frequency_in_hz(), "Hz"))

        self.unit_dropdown = QComboBox()
        self.unit_dropdown.addItem(HZ)
        self.unit_dropdown.addItem(KHZ)
        self.unit_dropdown.addItem(MHZ)
        self.unit_dropdown.addItem(GHZ)
        self.unit_dropdown.setCurrentText(default_speed)

        self.unit_dropdown.currentTextChanged.connect(lambda: print(self.get_frequency_in_hz(), "Hz"))
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        main_layout.addWidget(self.input_box)
        main_layout.addWidget(self.unit_dropdown)

    def parse(self) -> Tuple[float, str]:
        if re.match(self.freq_box_regex, self.input_box.text()):
            return float(self.input_box.text()), self.unit_dropdown.currentText()

        raise ValueError(f"Invalid input: {self.input_box.text()}")

    def set_frequency_in_hz(self, new_frequency: float) -> None:
        if new_frequency / 1e3 < 1:
            self.input_box.setText(f"{new_frequency}")
            self.unit_dropdown.setCurrentText(HZ)
        elif new_frequency / 1e6 < 1:
            self.input_box.setText(f"{new_frequency / 1e3}")
            self.unit_dropdown.setCurrentText(KHZ)
        elif new_frequency / 1e9 < 1:
            self.input_box.setText(f"{new_frequency / 1e6}")
            self.unit_dropdown.setCurrentText(MHZ)
        elif new_frequency / 1e12 < 1:
            self.input_box.setText(f"{new_frequency / 1e9}")
            self.unit_dropdown.setCurrentText(GHZ)

    def get_frequency_in_hz(self):
        value, unit = self.parse()
        if unit == HZ:
            return value
        elif unit == KHZ:
            return value * 1e3
        elif unit == MHZ:
            return value * 1e6
        elif unit == GHZ:
            return value * 1e9
        else:
            raise ValueError(f"Invalid unit: {unit}")
