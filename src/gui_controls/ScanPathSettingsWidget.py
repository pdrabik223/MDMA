from typing import Callable

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QFrame,
    QGridLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from gui_controls.custom_input_fiedls.PositionLineEdit import PositionLineEdit

SCAN_MODE = "scan_mode"
SAMPLE_X_POSITION_IN_MM = "sample_x_position_in_mm"
SAMPLE_Y_POSITION_IN_MM = "sample_y_position_in_mm"
ANTENNA_X_OFFSET_IN_MM = "antenna_x_offset_in_mm"
ANTENNA_Y_OFFSET_IN_MM = "antenna_y_offset_in_mm"
SAMPLE_LENGTH_IN_MM = "sample_length_in_mm"
SAMPLE_WIDTH_IN_MM = "sample_width_in_mm"
SCAN_HEIGHT_IN_MM = "scan_height_in_mm"
MEASUREMENT_RADIUS_IN_MM = "measurement_radius_in_mm"

SCAN_PATH_STATE_PARAMS = [
    SCAN_MODE,
    SAMPLE_X_POSITION_IN_MM,
    SAMPLE_Y_POSITION_IN_MM,
    ANTENNA_X_OFFSET_IN_MM,
    ANTENNA_Y_OFFSET_IN_MM,
    SAMPLE_LENGTH_IN_MM,
    SAMPLE_WIDTH_IN_MM,
    SCAN_HEIGHT_IN_MM,
    MEASUREMENT_RADIUS_IN_MM,
]


class ScanPathSettingsWidget(QWidget):
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

        self.measurement_radius = PositionLineEdit(default_value="3")
        self.scan_height = PositionLineEdit(default_value="4")
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
            SAMPLE_WIDTH_IN_MM: self.sample_width.get_value_in_mm(),
            SAMPLE_LENGTH_IN_MM: self.sample_length.get_value_in_mm(),
            MEASUREMENT_RADIUS_IN_MM: self.measurement_radius.get_value_in_mm(),
            SCAN_HEIGHT_IN_MM: self.scan_height.get_value_in_mm(),
        }

    def set_state(self, data: dict) -> None:
        # self.scan_mode_box.setText(str(data[SCAN_MODE]))
        try:
            self.sample_x_position.set_value_in_mm(data[SAMPLE_X_POSITION_IN_MM])
        except KeyError:
            pass
        try:
            self.sample_y_position.set_value_in_mm(data[SAMPLE_Y_POSITION_IN_MM])
        except KeyError:
            pass
        try:
            self.antenna_x_offset.set_value_in_mm(data[ANTENNA_X_OFFSET_IN_MM])
        except KeyError:
            pass
        try:
            self.antenna_y_offset.set_value_in_mm(data[ANTENNA_Y_OFFSET_IN_MM])
        except KeyError:
            pass
        try:
            self.sample_width.set_value_in_mm(data[SAMPLE_WIDTH_IN_MM])
        except KeyError:
            pass
        try:
            self.sample_length.set_value_in_mm(data[SAMPLE_LENGTH_IN_MM])
        except KeyError:
            pass
        try:
            self.measurement_radius.set_value_in_mm(data[MEASUREMENT_RADIUS_IN_MM])
        except KeyError:
            pass
        try:
            self.scan_height.set_value_in_mm(data[SCAN_HEIGHT_IN_MM])
        except KeyError:
            pass

    def _init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        scan_path_settings = QLabel("Scan Path Settings")
        scan_path_settings.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(scan_path_settings)

        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        main_layout.addWidget(frame)

        frame_layout = QVBoxLayout()
        frame.setLayout(frame_layout)
        self._init_frame(frame_layout)

    def _init_frame(self, frame_layout: QVBoxLayout):
        settings_layout = QGridLayout()
        frame_layout.addLayout(settings_layout)

        def add_setting(label: str, position: int, target_layout: QGridLayout, input_type):
            input_label = QLabel(label)
            input_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

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
        add_setting("Scan Height:", 8, settings_layout, self.scan_height)

        settings_layout.addWidget(self.recalculate_path_button, *(9, 0), *(1, 2))

    def set_disabled(self, is_disabled: bool = False):
        self.scan_mode_box.setDisabled(is_disabled)

        self.sample_x_position.setDisabled(is_disabled)
        self.sample_y_position.setDisabled(is_disabled)

        self.antenna_x_offset.setDisabled(is_disabled)
        self.antenna_y_offset.setDisabled(is_disabled)

        self.sample_length.setDisabled(is_disabled)
        self.sample_width.setDisabled(is_disabled)

        self.measurement_radius.setDisabled(is_disabled)
        self.scan_height.setDisabled(is_disabled)
        self.recalculate_path_button.setDisabled(is_disabled)
