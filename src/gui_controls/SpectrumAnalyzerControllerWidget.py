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

from src.gui_controls.FreqLineEdit import FreqLineEdit


class SpectrumAnalyzerControllerWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.connection_label = QLabel("Device not found")

        self.scan_mode_box = QComboBox()
        self.scan_mode_box.addItem("Mode 1")
        self.scan_mode_box.addItem("Mode 2")
        self.scan_mode_box.addItem("Mode 3")

        self.freq_box = FreqLineEdit()

        self._init_ui()

    def get_state(self) -> dict:
        return {
            "connection_label": self.connection_label.text(),
            "scan_mode_box": self.scan_mode_box.currentText(),
            "frequency_in_hz": self.freq_box.get_frequency_in_hz(),
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

        refresh_connection = QPushButton("Refresh connection")
        frame_layout.addWidget(refresh_connection)

        frame_layout.addWidget(self.connection_label)

        settings_layout = QGridLayout()
        frame_layout.addLayout(settings_layout)

        # Operating Frequency Input Box
        freq_label = QLabel("Operating Frequency:")
        freq_label.setAlignment(Qt.AlignLeft)

        settings_layout.addWidget(freq_label, *(0, 0))
        settings_layout.addWidget(self.freq_box, *(0, 1))

        # Operating Mode Selector
        mode_label = QLabel("Operating Mode:")
        mode_label.setAlignment(Qt.AlignLeft)

        settings_layout.addWidget(mode_label, *(1, 0))
        settings_layout.addWidget(self.scan_mode_box, *(1, 1))
