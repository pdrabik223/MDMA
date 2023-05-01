from typing import Callable, Tuple

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
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
from gui_controls.MovementSpeedLineEdit import MovementSpeedLineEdit
from gui_controls.PositionLineEdit import PositionLineEdit

CONNECTION_STATE = "connection_state"
MOVEMENT_SPEED = "movement_speed"
PRINTER_WIDTH_IN_MM = "printer_bed_width"
PRINTER_LENGTH_IN_MM = "printer_bed_length"

PRINTER_STATE_PARAMS = [
    CONNECTION_STATE,
    MOVEMENT_SPEED,
    PRINTER_WIDTH_IN_MM,
    PRINTER_LENGTH_IN_MM,
]


class PrinterControllerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.connection_label = DeviceConnectionStateLabel()
        self.refresh_connection = QPushButton("Refresh connection")
        self.movement_speed_box = MovementSpeedLineEdit()
        self.printer_bed_width = PositionLineEdit(default_value="210 mm")
        self.printer_bed_length = PositionLineEdit(default_value="210 mm")
        self.current_position = QLabel("-")  # this I think should be input box, or three
        self.center_extruder = QPushButton("Center Extruder")
        self.extruder_move_buttons = [
            {
                "label": "y+",
                "style": "QPushButton {color: blue;}",
                "q_button": QPushButton(),
            },
            {
                "label": "z+",
                "style": "QPushButton {color: green;}",
                "q_button": QPushButton(),
            },
            {
                "label": "x-",
                "style": "QPushButton {color: red;}",
                "q_button": QPushButton(),
            },
            {
                "label": "H",
                "style": "QPushButton {color: black;}",
                "q_button": QPushButton(),
            },
            {
                "label": "x+",
                "style": "QPushButton {color: red;}",
                "q_button": QPushButton(),
            },
            {
                "label": "y-",
                "style": "QPushButton {color: blue;}",
                "q_button": QPushButton(),
            },
            {
                "label": "z-",
                "style": "QPushButton {color: green;}",
                "q_button": QPushButton(),
            },
        ]
        self._init_ui()

    def set_connection_label_text(self, state: str):
        if state in (DEVICE_NOT_FOUND, CONNECTING):
            self.center_extruder.setDisabled(True)
            for button_info in self.extruder_move_buttons:
                button_info["q_button"].setDisabled(True)

        elif state == CONNECTED:
            self.center_extruder.setDisabled(False)
            for button_info in self.extruder_move_buttons:
                button_info["q_button"].setDisabled(False)

        else:
            assert False

        self.connection_label.set_text(state)

    def set_current_position_label(self, x: int, y: int, z: int):
        self.current_position.setText(f"x: {str(x)}mm, y: {str(y)}mm, z: {str(z)}mm ")

    def on_refresh_connection_button_press(self, function: Callable):
        self.refresh_connection.clicked.connect(function)

    def get_state(self) -> dict:
        return {
            CONNECTION_STATE: self.connection_label.text(),
            MOVEMENT_SPEED: self.movement_speed_box.get_value_in_mm_per_second(),
            PRINTER_WIDTH_IN_MM: self.printer_bed_width.get_value_in_mm(),
            PRINTER_LENGTH_IN_MM: self.printer_bed_length.get_value_in_mm(),
        }

    def set_state(self, data: dict) -> None:

        self.connection_label.set_text(data[CONNECTION_STATE])
        self.movement_speed_box.setText(data[MOVEMENT_SPEED])
        self.printer_bed_width.setText(data[PRINTER_WIDTH_IN_MM])
        self.printer_bed_length.setText(data[PRINTER_LENGTH_IN_MM])

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

        frame_layout.addWidget(self.connection_label)

        frame_layout.addWidget(self.refresh_connection)

        movement_layout = QGridLayout()
        frame_layout.addLayout(movement_layout)

        def add_move_btn(
                label: str,
                position: Tuple[int, int],
                target_layout: QGridLayout,
                style: str,
                q_button: QPushButton,
        ):
            q_button.setText(label)
            q_button.setStyleSheet(style)
            target_layout.addWidget(q_button, *position)

        # TOOD those unicode's could be swapped for png's, from flaticon

        add_move_btn(
            self.extruder_move_buttons[0]["label"],
            (0, 1),
            movement_layout,
            self.extruder_move_buttons[0]["style"],
            self.extruder_move_buttons[0]["q_button"],
        )
        add_move_btn(
            self.extruder_move_buttons[1]["label"],
            (0, 2),
            movement_layout,
            self.extruder_move_buttons[1]["style"],
            self.extruder_move_buttons[1]["q_button"],
        )
        add_move_btn(
            self.extruder_move_buttons[2]["label"],
            (1, 0),
            movement_layout,
            self.extruder_move_buttons[2]["style"],
            self.extruder_move_buttons[2]["q_button"],
        )
        add_move_btn(
            self.extruder_move_buttons[3]["label"],
            (1, 1),
            movement_layout,
            self.extruder_move_buttons[3]["style"],
            self.extruder_move_buttons[3]["q_button"],
        )
        add_move_btn(
            self.extruder_move_buttons[4]["label"],
            (1, 2),
            movement_layout,
            self.extruder_move_buttons[4]["style"],
            self.extruder_move_buttons[4]["q_button"],
        )
        add_move_btn(
            self.extruder_move_buttons[5]["label"],
            (2, 1),
            movement_layout,
            self.extruder_move_buttons[5]["style"],
            self.extruder_move_buttons[5]["q_button"],
        )
        add_move_btn(
            self.extruder_move_buttons[6]["label"],
            (2, 2),
            movement_layout,
            self.extruder_move_buttons[6]["style"],
            self.extruder_move_buttons[6]["q_button"],
        )

        frame_layout.addWidget(self.center_extruder)

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

    def set_disabled(self, is_disabled: bool = False):
        self.connection_label.setDisabled(is_disabled)
        self.movement_speed_box.setDisabled(is_disabled)
        self.printer_bed_width.setDisabled(is_disabled)
        self.printer_bed_length.setDisabled(is_disabled)
        self.refresh_connection.setDisabled(is_disabled)

        self.center_extruder.setDisabled(is_disabled)
        for button_info in self.extruder_move_buttons:
            button_info["q_button"].setDisabled(is_disabled)
