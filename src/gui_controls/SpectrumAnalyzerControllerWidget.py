from typing import Callable

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QComboBox,
    QFrame,
    QGridLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from gui_controls.DeviceConnectionStateLabel import (
    CONNECTED,
    CONNECTING,
    DEVICE_NOT_FOUND,
    DeviceConnectionStateLabel,
)
from gui_controls.FreqLineEdit import FreqLineEdit
from gui_controls.MeasurementTimeLineEdit import MeasurementTimeLineEdit

CONNECTION_STATE = "connection_state"
SCAN_MODE = "scan_mode_box"
FREQUENCY_IN_HZ = "frequency_in_hz"
LAST_MEASUREMENT_IN_HZ = "last_measurement_in_hz"
MEASUREMENT_TIME = "measurement_time"

SPECTRUM_ANALYZER_STATE_PARAMS = [
    CONNECTION_STATE,
    SCAN_MODE,
    FREQUENCY_IN_HZ,
    LAST_MEASUREMENT_IN_HZ,
    MEASUREMENT_TIME,
]
HAMEG_HMS_3010 = "HamegHMS3010"
POCKET_VNA = "Pocket VNA"


class SpectrumAnalyzerControllerWidget(QWidget):
    def __init__(
            self,
    ):
        super().__init__()

        self.connection_label = DeviceConnectionStateLabel()

        self.refresh_connection = QPushButton("Refresh connection")

        self.scan_mode_box = QComboBox()
        self.scan_mode_box.addItem(HAMEG_HMS_3010)
        self.scan_mode_box.addItem(POCKET_VNA)

        self.last_measured_value = QLabel("-")

        self.update_last_measurement = QPushButton("Refresh Measurement")

        self.freq_box = FreqLineEdit()
        self.scan_measurement_time = MeasurementTimeLineEdit()

        self._init_ui()
        self.set_connection_label_text(DEVICE_NOT_FOUND)

    def set_connection_label_text(self, state: str):
        if state == DEVICE_NOT_FOUND:
            self.update_last_measurement.setDisabled(True)
        elif state == CONNECTING:
            self.update_last_measurement.setDisabled(True)
        elif state == CONNECTED:
            self.update_last_measurement.setDisabled(False)
        else:
            assert False
        self.connection_label.set_text(state)
    def on_scan_mode_box_change(self, function):
        self.scan_mode_box.currentTextChanged.connect(function)
    def on_refresh_connection_button_press(self, function: Callable):
        self.refresh_connection.clicked.connect(function)

    def on_update_last_measurement_button_press(self, function: Callable):
        self.update_last_measurement.clicked.connect(function)

    def get_state(self) -> dict:
        return {
            CONNECTION_STATE: self.connection_label.text(),
            SCAN_MODE: self.scan_mode_box.currentText(),
            FREQUENCY_IN_HZ: self.freq_box.get_frequency_in_hz(),
            LAST_MEASUREMENT_IN_HZ: self.last_measured_value.text(),
            MEASUREMENT_TIME: self.scan_measurement_time.get_value_in_seconds(),
        }

    def set_state(self, data: dict) -> None:
        # self.scan_mode_box.set_text(data[SCAN_MODE])
        self.freq_box.set_frequency_in_hz(data[FREQUENCY_IN_HZ])
        self.scan_measurement_time.set_value_from_seconds(data[MEASUREMENT_TIME])

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

        settings_layout.addWidget(self.update_last_measurement, *(0, 0), *(1, 2))

        # Operating Frequency Input Box
        freq_label = QLabel("Operating Frequency:")
        freq_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        settings_layout.addWidget(freq_label, *(1, 0))
        settings_layout.addWidget(self.freq_box, *(1, 1))

        scan_measurement_time = QLabel("Measurement Time:")
        scan_measurement_time.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        settings_layout.addWidget(scan_measurement_time, *(2, 0))
        settings_layout.addWidget(self.scan_measurement_time, *(2, 1))

        last_measurement_label = QLabel("Last measurement:")
        last_measurement_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        settings_layout.addWidget(last_measurement_label, *(3, 0))
        settings_layout.addWidget(self.last_measured_value, *(3, 1))

        # Operating Mode Selector
        mode_label = QLabel("Operating Mode:")
        mode_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        settings_layout.addWidget(mode_label, *(4, 0))
        settings_layout.addWidget(self.scan_mode_box, *(4, 1))

    def set_last_measurement(self, new_value: float):
        self.last_measured_value.setText(str(new_value))

    def set_disabled(self, is_disabled: bool = False):
        self.connection_label.setDisabled(is_disabled)
        self.scan_mode_box.setDisabled(is_disabled)
        self.freq_box.setDisabled(is_disabled)
        self.refresh_connection.setDisabled(is_disabled)
        self.scan_measurement_time.setDisabled(is_disabled)
        self.update_last_measurement.setDisabled(is_disabled)
