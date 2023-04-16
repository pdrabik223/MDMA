import re
from typing import Tuple, Callable

from PyQt5.QtCore import QRegularExpression, Qt
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
)

from src.gui_controls.PositionLineEdit import PositionLineEdit

SCAN_MODE = "scan_mode"
SAMPLE_X_POSITION_IN_MM = "sample_x_position_in_mm"
SAMPLE_Y_POSITION_IN_MM = "sample_y_position_in_mm"
ANTENNA_X_OFFSET_IN_MM = "antenna_x_offset_in_mm"
ANTENNA_Y_OFFSET_IN_MM = "antenna_y_offset_in_mm"
SAMPLE_LENGTH_IN_MM = "sample_length_in_mm"
SAMPLE_WIDTH_IN_MM = "sample_width_in_mm"
SCAN_HEIGHT_IN_MM = "scann_height_in_mm"
MEASUREMENT_RADIUS_IN_MM = "measurement_radius_in_mm"


class ScannPathSettingsWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.scan_mode_box = QComboBox()
        self.scan_mode_box.addItem("Constant Z height")
        self.scan_mode_box.addItem("Variable Z height")

        self.sample_x_position = PositionLineEdit()
        self.sample_y_position = PositionLineEdit()

        self.antenna_x_offset = PositionLineEdit()
        self.antenna_y_offset = PositionLineEdit()

        self.sample_length = PositionLineEdit()
        self.sample_width = PositionLineEdit()

        self.measurement_radius = PositionLineEdit(default_value="3 mm")
        self.scann_height = PositionLineEdit(default_value="4 mm")

        self.recalculate_path_button = QPushButton("Recalculate path")

        self._init_ui()

    def on_recalculate_path_button_press(self, function: Callable) -> None:
        self.recalculate_path_button.clicked.connect(function)

    def get_state(self) -> dict:
        return {
            SCAN_MODE: self.scan_mode_box.currentText(),
            SAMPLE_X_POSITION_IN_MM: self.sample_x_position.get_value_in_mm(),
            SAMPLE_Y_POSITION_IN_MM: self.sample_y_position.get_value_in_mm(),
            ANTENNA_X_OFFSET_IN_MM: self.antenna_x_offset.get_value_in_mm(),
            ANTENNA_Y_OFFSET_IN_MM: self.antenna_y_offset.get_value_in_mm(),
            SAMPLE_LENGTH_IN_MM: self.sample_length.get_value_in_mm(),
            SAMPLE_WIDTH_IN_MM: self.sample_width.get_value_in_mm(),
            MEASUREMENT_RADIUS_IN_MM: self.measurement_radius.get_value_in_mm(),
            SCAN_HEIGHT_IN_MM: self.scann_height.get_value_in_mm(),
        }

    def _init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        scann_path_settings = QLabel("Scann Path Settings")
        scann_path_settings.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(scann_path_settings)

        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        main_layout.addWidget(frame)

        frame_layout = QVBoxLayout()
        frame.setLayout(frame_layout)
        self._init_frame(frame_layout)

    def _init_frame(self, frame_layout: QVBoxLayout):
        settings_layout = QGridLayout()
        frame_layout.addLayout(settings_layout)

        def add_setting(
            label: str, position: int, target_layout: QGridLayout, input_type
        ):
            input_label = QLabel(label)
            input_label.setAlignment(Qt.AlignLeft)

            target_layout.addWidget(input_label, *(position, 0))
            target_layout.addWidget(input_type, *(position, 1))

        add_setting("Movement Mode:", 0, settings_layout, self.scan_mode_box)

        add_setting("Sample X position:", 1, settings_layout, self.sample_x_position)
        add_setting("Sample Y position:", 2, settings_layout, self.sample_y_position)

        add_setting("Antenna X offset:", 3, settings_layout, self.antenna_x_offset)
        add_setting("Antenna Y offset:", 4, settings_layout, self.antenna_y_offset)

        add_setting("Sample Width:", 5, settings_layout, self.sample_width)
        add_setting("Sample Length:", 6, settings_layout, self.sample_length)
        add_setting("Measurement Radius:", 7, settings_layout, self.measurement_radius)
        add_setting("Scann Height:", 8, settings_layout, self.scann_height)

        settings_layout.addWidget(self.recalculate_path_button, *(9, 0), *(1, 2))
