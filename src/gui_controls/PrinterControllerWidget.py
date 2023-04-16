import re
from typing import Tuple

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
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.gui_controls.MovementSpeedLineEdit import MovementSpeedLineEdit
from src.gui_controls.PositionLineEdit import PositionLineEdit

CONNECTION_STATE = 'connection_state'
MOVEMENT_SPEED = "movement_speed"
PRINTER_WIDTH_IN_MM = "printer_bed_width"
PRINTER_LENGTH_IN_MM = "printer_bed_length"


class PrinterControllerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.connection_label = QLabel("Device not found")
        self.movement_speed_box = MovementSpeedLineEdit()
        self.printer_bed_width = PositionLineEdit(default_value="210 mm")
        self.printer_bed_length = PositionLineEdit(default_value="210 mm")

        self._init_ui()

    def get_state(self) -> dict:
        return {
            CONNECTION_STATE: self.connection_label.text(),
            MOVEMENT_SPEED: self.movement_speed_box.get_value_in_mm_per_second(),
            PRINTER_WIDTH_IN_MM: self.printer_bed_width.get_value_in_mm(),
            PRINTER_LENGTH_IN_MM: self.printer_bed_length.get_value_in_mm(),
        }

    def _init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        printer_controller_label = QLabel("Printer Controller")
        printer_controller_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(printer_controller_label)

        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        main_layout.addWidget(frame)

        frame_layout = QVBoxLayout()
        frame.setLayout(frame_layout)
        self._init_frame(frame_layout)

    def _init_frame(self, frame_layout):
        self.connection_label.setAlignment(Qt.AlignCenter)
        self.connection_label.setStyleSheet("QLabel {color: red;}")

        frame_layout.addWidget(self.connection_label)

        refresh_connection = QPushButton("Refresh connection")
        frame_layout.addWidget(refresh_connection)

        movement_layout = QGridLayout()
        frame_layout.addLayout(movement_layout)

        def add_move_btn(
                label: str,
                position: Tuple[int, int],
                target_layout: QGridLayout,
                style: str,
        ):
            button = QPushButton(label)
            button.setStyleSheet(style)
            target_layout.addWidget(button, *position)

        # TOOD those unicodes could be swapped for png's, from flaticon
        add_move_btn("🢁", (0, 1), movement_layout, "QPushButton {color: blue;}")
        add_move_btn("🢁", (0, 2), movement_layout, "QPushButton {color: green;}")
        add_move_btn("🢀", (1, 0), movement_layout, "QPushButton {color: red;}")
        add_move_btn("H", (1, 1), movement_layout, "QPushButton {color: black;}")
        add_move_btn("🢂", (1, 2), movement_layout, "QPushButton {color: red;}")
        add_move_btn("🢃", (2, 1), movement_layout, "QPushButton {color: blue;}")
        add_move_btn("🢃", (2, 2), movement_layout, "QPushButton {color: green;}")

        center_extruder = QPushButton("Center Extruder")
        frame_layout.addWidget(center_extruder)

        settings_layout = QGridLayout()
        frame_layout.addLayout(settings_layout)

        freq_label = QLabel("Movement Speed:")
        freq_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        settings_layout.addWidget(freq_label, *(0, 0))
        settings_layout.addWidget(self.movement_speed_box, *(0, 1))

        freq_label = QLabel("Printer Bed Width:")
        freq_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        settings_layout.addWidget(freq_label, *(1, 0))
        settings_layout.addWidget(self.printer_bed_width, *(1, 1))

        freq_label = QLabel("Printer Bed Length:")
        freq_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        settings_layout.addWidget(freq_label, *(2, 0))
        settings_layout.addWidget(self.printer_bed_length, *(2, 1))
