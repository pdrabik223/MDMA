from PyQt6.QtWidgets import QLabel

CONNECTING = "Connecting"
DEVICE_NOT_FOUND = "Device not found"
CONNECTED = "Connected"


class DeviceConnectionStateLabel(QLabel):
    def __init__(self, label: str = DEVICE_NOT_FOUND):
        super().__init__()
        self.set_text(label)

    def update_style(self):
        if self.text() == DEVICE_NOT_FOUND:
            self.setStyleSheet("QLabel {color: red;}")
        elif self.text() == CONNECTING:
            self.setStyleSheet("QLabel {color: yellow;}")
        elif self.text() == CONNECTED:
            self.setStyleSheet("QLabel {color: green;}")
        else:
            assert False

    def set_text(self, label: str):
        assert label in (CONNECTING, DEVICE_NOT_FOUND, CONNECTED)
        self.setText(label)
        self.update_style()
