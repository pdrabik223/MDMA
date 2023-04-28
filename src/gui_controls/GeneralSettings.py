from typing import Callable

from PyQt5.QtCore import Qt
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

START_MEASUREMENT = "Start Measurement"
STOP_MEASUREMENT = "Stop Measurement"


class StartButton(QPushButton):
    def __init__(self, label: str = START_MEASUREMENT):
        super().__init__()
        assert label in (START_MEASUREMENT, STOP_MEASUREMENT)
        self.setText(label)
        self.setStyleSheet("color: forestgreen")
        self.clicked.connect(self.change_start_button_state)

    def set_state(self, new_state: str):
        if new_state == START_MEASUREMENT:
            self.setText(START_MEASUREMENT)
            self.setStyleSheet("color: forestgreen")
        elif new_state == STOP_MEASUREMENT:
            self.setText(STOP_MEASUREMENT)
            self.setStyleSheet("color: lightcoral")
        else:
            assert False

    def change_start_button_state(self):
        if self.text() == START_MEASUREMENT:
            self.set_state(STOP_MEASUREMENT)
        else:
            self.set_state(START_MEASUREMENT)

    def on_start(self, function: Callable):
        if self.text() == STOP_MEASUREMENT:
            function()

    def on_stop(self, function: Callable):
        if self.text() == START_MEASUREMENT:
            function()


class GeneralSettings(QWidget):
    def __init__(self):
        super().__init__()
        self.export_scan = QPushButton("Export Scan")
        self.import_scan = QPushButton("Import Scan")
        self.export_settings = QPushButton("Export Settings")
        self.import_settings = QPushButton("Import Settings")
        self.start_measurement = StartButton()

        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        general_settings_label = QLabel("General Settings")
        general_settings_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(general_settings_label)

        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        main_layout.addWidget(frame)

        frame_layout = QVBoxLayout()
        frame.setLayout(frame_layout)
        self._init_frame(frame_layout)

    def _init_frame(self, frame_layout: QVBoxLayout):
        frame_layout.addWidget(self.export_scan)
        frame_layout.addWidget(self.import_scan)
        frame_layout.addWidget(self.export_settings)
        frame_layout.addWidget(self.import_settings)
        frame_layout.addWidget(self.start_measurement)

    def on_export_scan_button_press(self, function: Callable) -> None:
        self.export_scan.clicked.connect(function)

    def on_import_scan_button_press(self, function: Callable) -> None:
        self.import_scan.clicked.connect(function)

    def on_export_settings_button_press(self, function: Callable) -> None:
        self.export_settings.clicked.connect(function)

    def on_import_settings_button_press(self, function: Callable) -> None:
        self.import_settings.clicked.connect(function)

    def on_start_measurement_button_press(self, function: Callable):
        self.start_measurement.clicked.connect(
            lambda: self.start_measurement.on_start(function)
        )

    def on_stop_measurement_button_press(self, function: Callable):
        self.start_measurement.clicked.connect(
            lambda: self.start_measurement.on_stop(function)
        )

    def set_disabled(self, is_disabled: bool = False):
        self.export_scan.setDisabled(is_disabled)
        self.import_scan.setDisabled(is_disabled)
        self.export_settings.setDisabled(is_disabled)
        self.import_settings.setDisabled(is_disabled)
