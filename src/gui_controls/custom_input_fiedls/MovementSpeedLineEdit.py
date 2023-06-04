import re
from typing import Tuple

from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import QLineEdit, QComboBox

from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
)

MM_PER_SEC = "mm/s"
MM_PER_MIN = "mm/min"
CM_PER_SEC = "cm/s"
CM_PER_MIN = "cm/min"


class MovementSpeedLineEdit(QWidget):
    def __init__(self, default_value: str = "1000", default_speed: str = MM_PER_SEC):
        super().__init__()
        # TODO add 0 mm/s validator
        self.speed_regex = r"^[+-]?([0-9]*[.])?[0-9]+$"
        validator = QRegularExpressionValidator(QRegularExpression(self.speed_regex))
        self.input_box = QLineEdit(default_value)
        self.input_box.setValidator(validator)
        self.input_box.editingFinished.connect(lambda: print(self.get_value_in_mm_per_second()))

        self.unit_dropdown = QComboBox()
        self.unit_dropdown.addItem(MM_PER_SEC)
        self.unit_dropdown.addItem(MM_PER_MIN)
        self.unit_dropdown.addItem(CM_PER_SEC)
        self.unit_dropdown.addItem(CM_PER_MIN)
        self.unit_dropdown.setCurrentText(default_speed)

        self.unit_dropdown.currentTextChanged.connect(lambda: print(self.get_value_in_mm_per_second()))
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

    def set_value_in_mm_per_second(self, value: float) -> None:
        self.input_box.setText(f"{value}")
        self.unit_dropdown.setCurrentText(MM_PER_SEC)

    def get_value_in_mm_per_second(self) -> float:
        value, unit = self.parse()
        if unit == MM_PER_SEC:
            return value
        elif unit == MM_PER_MIN:
            return value / 60
        elif unit == CM_PER_SEC:
            return value * 10
        elif unit == CM_PER_MIN:
            return value / 6
        else:
            raise ValueError(f"Invalid unit: {unit}")
