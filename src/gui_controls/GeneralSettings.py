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


class GeneralSettings(QWidget):
    def __init__(self):
        super().__init__()
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
        button = QPushButton("Export Scan")
        frame_layout.addWidget(button)

        button = QPushButton("Import Scan")
        frame_layout.addWidget(button)

        button = QPushButton("Export Settings")
        frame_layout.addWidget(button)

        button = QPushButton("Import Settings")
        frame_layout.addWidget(button)

        button = QPushButton("Start Measurement")
        frame_layout.addWidget(button)
