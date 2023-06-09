from typing import Callable

from PyQt6.QtWidgets import (
    QPushButton,
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
