import re
from typing import Tuple

from PyQt5.QtCore import QRegularExpression, Qt, QTimer
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
    QProgressBar,
)

from src.gui_controls.FreqLineEdit import FreqLineEdit


class ConfigurationInformationWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.no_points = QLabel("-")
        self.total_scan_time = QLabel("-")
        self.scan_time_left = QLabel("-")
        self.elapsed_scan_time = QLabel("-")

        self.progress = QProgressBar()
        self.progress.setGeometry(200, 80, 250, 20)
        self.progress.setAlignment(Qt.AlignCenter)
        self._init_ui()

        self.enable_elapsed_scan_timer = False
        self.elapsed_seconds_count = 0

        timer = QTimer()
        timer.timeout.connect(self.update_elapsed_scan_time)
        timer.start(1000)

    def update_widget(
        self,
        no_points: int,
        total_scan_time_in_seconds: int,
        current_progress_in_percentages: float,
    ):
        self.no_points.setText(str(no_points))
        self.total_scan_time.setText(
            ConfigurationInformationWidget.convert_time(total_scan_time_in_seconds)
        )
        scan_time_left_in_seconds = (
            total_scan_time_in_seconds * (100 - current_progress_in_percentages) / 100
        )

        self.scan_time_left.setText(
            ConfigurationInformationWidget.convert_time(scan_time_left_in_seconds)
        )
        self.progress.setValue(current_progress_in_percentages)

    def start_elapsed_timer(self):
        self.enable_elapsed_scan_timer = True
        self.elapsed_seconds_count = 0

    def stop_elapsed_timer(self):
        self.enable_elapsed_scan_timer = False

    def update_elapsed_scan_time(self):
        if self.enable_elapsed_scan_timer:
            self.elapsed_seconds_count += 1
            self.elapsed_scan_time.setText(
                ConfigurationInformationWidget.convert_time(self.elapsed_seconds_count)
            )

    @staticmethod
    def convert_time(seconds: float):
        if seconds < 60:
            return f"{int(seconds)} s"
        elif seconds < 3600:
            minutes = seconds // 60
            seconds = seconds % 60
            return f"{int(minutes)} min, {int(seconds)} s"
        else:
            hours = seconds // 3600
            seconds = seconds % 3600
            minutes = seconds // 60
            seconds = seconds % 60
            return f"{int(hours)} h, {int(minutes)} min, {int(seconds)} s"

    def _init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        configuration_information_label = QLabel("Scan Summary")
        configuration_information_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(configuration_information_label)

        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        main_layout.addWidget(frame)

        frame_layout = QVBoxLayout()
        frame.setLayout(frame_layout)
        self._init_frame(frame_layout)

    def _init_frame(self, frame_layout: QVBoxLayout):
        # Connection Indicator
        settings_layout = QGridLayout()
        frame_layout.addLayout(settings_layout)

        def add_element(
            label: str, position: int, target_layout: QGridLayout, input_type
        ):
            q_label = QLabel(label)
            q_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            target_layout.addWidget(q_label, *(position, 0))

            input_type.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            target_layout.addWidget(input_type, *(position, 1))

        add_element("Number of measurements:", 0, settings_layout, self.no_points)
        add_element(
            "Estimated Total scan time:", 1, settings_layout, self.total_scan_time
        )
        add_element(
            "Estimated Scan time left:", 2, settings_layout, self.scan_time_left
        )
        add_element(
            "Elapsed Scan time left:", 3, settings_layout, self.elapsed_scan_time
        )

        scann_progress_label = QLabel("Current scan progress")
        scann_progress_label.setAlignment(Qt.AlignCenter)
        settings_layout.addWidget(scann_progress_label, *(4, 0), *(1, 2))
        settings_layout.addWidget(self.progress, *(5, 0), *(1, 2))