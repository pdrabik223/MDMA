import re
from typing import Tuple

from PyQt5.QtCore import QRegularExpression, Qt
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
                             QHBoxLayout, QLabel, QLineEdit, QMainWindow,
                             QVBoxLayout, QWidget)

from src.gui_controls.PositionLineEdit import PositionLineEdit


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

        self.sample_height = PositionLineEdit()
        self.sample_width = PositionLineEdit()

        self.scann_height = PositionLineEdit(default_value='4 mm')

        self._init_ui()

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
        add_setting("Sample Length:", 6, settings_layout, self.sample_height)

        add_setting("Scann Height:", 7, settings_layout, self.scann_height)
