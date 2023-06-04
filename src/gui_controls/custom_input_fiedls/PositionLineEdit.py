from typing import Tuple

from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import (
    QLineEdit,
    QComboBox,
    QWidget,
    QHBoxLayout,
)
import re

MM = "mm"
CM = "cm"


class PositionLineEdit(QWidget):
    def __init__(self, default_value: str = "50", default_unit: str = MM):
        super().__init__()
        self.speed_regex = r"^[+-]?([0-9]*[.])?[0-9]+$"
        validator = QRegularExpressionValidator(QRegularExpression(self.speed_regex))
        self.input_box = QLineEdit(default_value)
        self.input_box.setValidator(validator)
        self.input_box.setText(default_value)
        self.input_box.editingFinished.connect(lambda: print(self.parse()))

        self.unit_dropdown = QComboBox()
        self.unit_dropdown.addItem(MM)
        self.unit_dropdown.addItem(CM)
        self.unit_dropdown.setCurrentText(default_unit)

        self.unit_dropdown.currentTextChanged.connect(lambda: print(self.get_value_in_mm()))
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        main_layout.addWidget(self.input_box)
        main_layout.addWidget(self.unit_dropdown)

    def parse(self) -> Tuple[float, str]:
        if re.match(self.speed_regex, self.input_box.text()):
            return float(self.input_box.text()), self.unit_dropdown.currentText()

        raise ValueError(f"Invalid input: '{self.input_box.text()}'")

    def set_value_in_mm(self, new_value: float) -> None:
        if new_value / 10 < 1:
            self.input_box.setText(f"{new_value}")
            self.unit_dropdown.setCurrentText(MM)
        elif new_value / (10 * 10) < 1:
            self.input_box.setText(f"{new_value / 10}")
            self.unit_dropdown.setCurrentText(CM)

    def get_value_in_mm(self) -> float:
        value, unit = self.parse()
        if unit == MM:
            return value
        elif unit == CM:
            return value * 10
        raise ValueError(f"Invalid unit: {unit}")
