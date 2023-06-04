import re
from typing import Tuple

from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import QLineEdit, QComboBox, QHBoxLayout, QWidget

S = "s"
MIN = "min"


class MeasurementTimeLineEdit(QWidget):
    def __init__(self, default_value: str = "1", default_speed: str = S):
        super().__init__()
        # TODO add 0 mm/s validator
        self.speed_regex = r"^[+-]?([0-9]*[.])?[0-9]+$"
        validator = QRegularExpressionValidator(QRegularExpression(self.speed_regex))
        self.input_box = QLineEdit(default_value)
        self.input_box.setValidator(validator)
        self.input_box.editingFinished.connect(lambda: print(self.get_value_in_seconds(), "s"))

        self.unit_dropdown = QComboBox()
        self.unit_dropdown.addItem(S)
        self.unit_dropdown.addItem(MIN)
        self.unit_dropdown.setCurrentText(default_speed)

        self.unit_dropdown.currentTextChanged.connect(lambda: print(self.get_value_in_seconds(), "s"))
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        main_layout.addWidget(self.input_box)
        main_layout.addWidget(self.unit_dropdown)

    def parse(self) -> Tuple[float, str]:
        if re.match(self.speed_regex, self.input_box.text()):
            return float(self.input_box.text()), self.unit_dropdown.currentText()

        raise ValueError(f"Invalid input: {self.input_box.text()}")

    def set_value_from_seconds(self, new_value: float) -> None:
        if new_value / 60 < 1:
            self.input_box.setText(f"{new_value}")
            self.unit_dropdown.setCurrentText(S)
        elif new_value / (60**2) < 1:
            self.input_box.setText(f"{new_value / 60}")
            self.unit_dropdown.setCurrentText(MIN)

    def get_value_in_seconds(self) -> float:
        value, unit = self.parse()
        if unit == S:
            return value
        elif unit == MIN:
            return value / 60
        raise ValueError(f"Invalid unit: {unit}")
