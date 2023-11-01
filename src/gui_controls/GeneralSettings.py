from typing import Callable

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QComboBox, QFrame, QLabel, QPushButton, QVBoxLayout, QWidget

from gui_controls.custom_input_fiedls.StartStopButton import StartButton

SINGLE_PASS_SCAN = "Single Pass Scan"
BACKGROUND_FILTERING = "Background Filter"


class GeneralSettings(QWidget):
    def __init__(self):
        super().__init__()
        self.scan_mode_box = QComboBox()
        self.scan_mode_box.addItem(SINGLE_PASS_SCAN)
        self.scan_mode_box.addItem(BACKGROUND_FILTERING)
        self.scan_mode_box.model().item(1).setEnabled(False)
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
        general_settings_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(general_settings_label)

        self.scan_mode_box.setEditable(True)
        self.scan_mode_box.lineEdit().setReadOnly(True)
        self.scan_mode_box.lineEdit().setAlignment(Qt.AlignmentFlag.AlignCenter)

        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        main_layout.addWidget(frame)

        frame_layout = QVBoxLayout()
        frame.setLayout(frame_layout)
        self._init_frame(frame_layout)

    def _init_frame(self, frame_layout: QVBoxLayout):
        frame_layout.addWidget(self.scan_mode_box)
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
        self.start_measurement.clicked.connect(lambda: self.start_measurement.on_start(function))

    def on_stop_measurement_button_press(self, function: Callable):
        self.start_measurement.clicked.connect(lambda: self.start_measurement.on_stop(function))

    def activate_export_buttons(self):
        self.export_settings.setDisabled(False)

    def set_disabled(self, is_disabled: bool = False):
        self.scan_mode_box.setDisabled(is_disabled)
        self.export_scan.setDisabled(is_disabled)
        self.import_scan.setDisabled(is_disabled)
        self.export_settings.setDisabled(is_disabled)
        self.import_settings.setDisabled(is_disabled)
