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
    QVBoxLayout,
    QWidget,
    QPushButton,
)

from src.gui_controls.DeviceConnectionStateLabel import DeviceConnectionStateLabel

from src.gui_controls.FreqLineEdit import FreqLineEdit

CONNECTION_STATE = "connection_state"
SCAN_MODE = "scan_mode_box"
FREQUENCY_IN_HZ = "frequency_in_hz"


class SpectrumAnalyzerControllerWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.connection_label = DeviceConnectionStateLabel()

        self.refresh_connection = QPushButton("Refresh connection")

        self.scan_mode_box = QComboBox()
        self.scan_mode_box.addItem("Mode 1")
        self.scan_mode_box.addItem("Mode 2")
        self.scan_mode_box.addItem("Mode 3")
        # TODO add last measurement value indicator
        self.freq_box = FreqLineEdit()

        self._init_ui()

    def get_state(self) -> dict:
        return {
            CONNECTION_STATE: self.connection_label.text(),
            SCAN_MODE: self.scan_mode_box.currentText(),
            FREQUENCY_IN_HZ: self.freq_box.get_frequency_in_hz(),
        }

    def _init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        spectrum_analyzer_settings_label = QLabel("Spectrum Analyzer Settings")
        spectrum_analyzer_settings_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(spectrum_analyzer_settings_label)

        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        main_layout.addWidget(frame)

        frame_layout = QVBoxLayout()
        frame.setLayout(frame_layout)
        self._init_frame(frame_layout)

    def _init_frame(self, frame_layout: QVBoxLayout):
        # Connection Indicator

        self.connection_label.setAlignment(Qt.AlignCenter)
        self.connection_label.setStyleSheet("QLabel {color: red;}")

        frame_layout.addWidget(self.connection_label)
        frame_layout.addWidget(self.refresh_connection)

        settings_layout = QGridLayout()
        frame_layout.addLayout(settings_layout)

        # Operating Frequency Input Box
        freq_label = QLabel("Operating Frequency:")
        freq_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        settings_layout.addWidget(freq_label, *(0, 0))
        settings_layout.addWidget(self.freq_box, *(0, 1))

        # Operating Mode Selector
        mode_label = QLabel("Operating Mode:")
        mode_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        settings_layout.addWidget(mode_label, *(1, 0))
        settings_layout.addWidget(self.scan_mode_box, *(1, 1))

    def set_disabled(self, is_disabled: bool = False):
        self.connection_label.setDisabled(is_disabled)
        self.scan_mode_box.setDisabled(is_disabled)
        self.freq_box.setDisabled(is_disabled)
        self.refresh_connection.setDisabled(is_disabled)
