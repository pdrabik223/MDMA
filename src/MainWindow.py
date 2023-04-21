import os
from typing import Union, Optional

import pandas as pd
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QGridLayout, QMainWindow, QWidget
from serial import SerialException
from vector3d.vector import Vector

from gui_controls.ConfigurationInformationWidget import (
    ConfigurationInformationWidget,
)
from gui_controls.DeviceConnectionStateLabel import (
    CONNECTING,
    CONNECTED,
    DEVICE_NOT_FOUND,
)
from gui_controls.GeneralSettings import GeneralSettings
from gui_controls.PrinterControllerWidget import (
    PrinterControllerWidget,
    PRINTER_WIDTH_IN_MM,
    PRINTER_LENGTH_IN_MM,
    CONNECTION_STATE,
)
from gui_controls.ScanPathSettingsWidget import (
    ScanPathSettingsWidget,
    SCAN_MODE,
    SAMPLE_X_POSITION_IN_MM,
    SAMPLE_Y_POSITION_IN_MM,
    ANTENNA_X_OFFSET_IN_MM,
    ANTENNA_Y_OFFSET_IN_MM,
    SAMPLE_LENGTH_IN_MM,
    SAMPLE_WIDTH_IN_MM,
    SCAN_HEIGHT_IN_MM,
    MEASUREMENT_RADIUS_IN_MM,
)
from gui_controls.SpectrumAnalyzerControllerWidget import (
    SpectrumAnalyzerControllerWidget,
    FREQUENCY_IN_HZ,
)
from plot_widgets.Heatmap2DWidget import Heatmap2DWidget
from plot_widgets.PrinterPathWidget2D import PrinterPathWidget2D
from plot_widgets.PrinterPathWidget3D import PrinterPathWidget3D
from PrinterPath import Square, PrinterPath
from printer_device.PrinterDevice import PrinterDevice
from spectrum_analyzer_device.hameg3010.hameg3010device import Hameg3010Device
from printer_device.MarlinDevice import MarlinDevice
from dotenv import load_dotenv
import os

load_dotenv()
VERSION = os.environ.get('VERSION')


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.stop_scan = False

        # this will be set in _init_ui based on default values in settings
        self.current_scan_path = None

        self._init_ui()
        self.connect_functions()
        self.analyzer_device = self.try_to_set_up_analyzer_device()
        self.printer_device = self.try_to_set_up_printer_device()

    def try_to_set_up_analyzer_device(self) -> Optional[Hameg3010Device]:
        self.spectrum_analyzer_controller.set_connection_label_text(CONNECTING)
        try:
            self.spectrum_analyzer_controller.set_connection_label_text(CONNECTED)
            return Hameg3010Device.automatically_connect()
        except ValueError:
            self.spectrum_analyzer_controller.set_connection_label_text(
                DEVICE_NOT_FOUND
            )
            return None

    def try_to_set_up_printer_device(self) -> Optional[PrinterDevice]:
        self.printer_controller.set_connection_label_text(CONNECTING)
        try:
            self.printer_controller.set_connection_label_text(CONNECTED)
            return MarlinDevice.connect()

        except SerialException:
            self.printer_controller.set_connection_label_text(DEVICE_NOT_FOUND)
            return None

    def _init_ui(self):
        self.setWindowTitle(f"MDMA v{VERSION}")
        self.setWindowIcon(QIcon("assets/sensor.png"))

        self.setGeometry(100, 100, 1600, 600)

        self.main_layout = QGridLayout()

        self.spectrum_analyzer_controller = SpectrumAnalyzerControllerWidget()
        self.printer_controller = PrinterControllerWidget()
        self.scan_path_settings = ScanPathSettingsWidget()
        self.general_settings = GeneralSettings()
        self.configuration_information = ConfigurationInformationWidget()

        # settings section
        self.main_layout.addWidget(self.spectrum_analyzer_controller, *(0, 0))
        self.main_layout.addWidget(self.printer_controller, *(1, 0))
        self.main_layout.addWidget(self.scan_path_settings, *(2, 0))
        self.main_layout.addWidget(self.configuration_information, *(3, 0))
        self.main_layout.addWidget(self.general_settings, *(4, 0))

        self.update_current_scan_path_from_scan_path_settings()

        self.printer_path_widget = PrinterPathWidget2D.from_printer_path(
            self.current_scan_path
        )

        self.heatmap_widget = Heatmap2DWidget()

        self.recalculate_path()

        # plots section
        self.main_layout.addWidget(self.printer_path_widget, *(0, 1), *(5, 1))
        self.main_layout.addWidget(self.heatmap_widget, *(0, 2), *(5, 1))

        widget = QWidget()
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)

    def connect_functions(self):
        self.scan_path_settings.on_recalculate_path_button_press(self.recalculate_path)
        self.general_settings.on_start_measurement_button_press(self.start_measurement)
        self.spectrum_analyzer_controller.on_refresh_connection_button_press(
            self.try_to_set_up_analyzer_device
        )
        self.spectrum_analyzer_controller.on_update_last_measurement_button_press(
            lambda: self.analyzer_device.get_level(
                self.spectrum_analyzer_controller.get_state()[FREQUENCY_IN_HZ]
            )
        )
        self.spectrum_analyzer_controller.on_update_last_measurement_button_press(
            self.update_last_measurement
        )

    def update_last_measurement(self):
        # TODO make it async
        self.spectrum_analyzer_controller.set_last_measurement(
            self.analyzer_device.get_level(
                self.spectrum_analyzer_controller.get_state()[FREQUENCY_IN_HZ]
            )
        )

    def update_current_scan_path_from_scan_path_settings(self):
        printer_settings = self.printer_controller.get_state()
        path_settings = self.scan_path_settings.get_state()

        self.current_scan_path = PrinterPath(
            pass_height=path_settings[SCAN_HEIGHT_IN_MM],
            antenna_offset=Vector(
                path_settings[ANTENNA_X_OFFSET_IN_MM],
                path_settings[ANTENNA_Y_OFFSET_IN_MM],
                0,
            ),
            scanned_area=Square(
                path_settings[SAMPLE_X_POSITION_IN_MM],
                path_settings[SAMPLE_Y_POSITION_IN_MM],
                path_settings[SAMPLE_WIDTH_IN_MM],
                path_settings[SAMPLE_LENGTH_IN_MM],
            ),
            measurement_radius=path_settings[MEASUREMENT_RADIUS_IN_MM],
            printer_bed_size=Vector(
                printer_settings[PRINTER_WIDTH_IN_MM],
                printer_settings[PRINTER_LENGTH_IN_MM],
                210,
            ),
        )

    def recalculate_path(self):
        self.update_current_scan_path_from_scan_path_settings()

        self.configuration_information.update_widget(
            no_points=self.current_scan_path.get_no_scan_points(),
            total_scan_time_in_seconds=self.current_scan_path.total_scan_time_in_seconds(),
            current_progress_in_percentages=0,
        )
        self.printer_path_widget.update_from_printer_path(self.current_scan_path)
        self.printer_path_widget.show()

    def re_compute_path(self):
        pass

    def update_ui(self):
        pass

    def run_outline(self):
        pass

    def perform_measurement(self):
        pass

    def scan_can_be_performed(self) -> Union[bool, str]:
        if self.current_scan_path.get_no_scan_points() <= 0:
            return "Scan path is of length 0"

        printer_settings = self.printer_controller.get_state()
        if printer_settings[CONNECTION_STATE] != "Connected":
            return "Printer device connection failed"

        analyzer = self.spectrum_analyzer_controller.get_state()
        if analyzer[CONNECTION_STATE] != "Connected":
            return "Analyzer device connection failed"

    def start_measurement(self):
        self.update_current_scan_path_from_scan_path_settings()
        if not self.scan_can_be_performed():
            return

        self.spectrum_analyzer_controller.set_disabled(True)
        self.printer_controller.set_disabled(True)
        self.scan_path_settings.set_disabled(True)
        self.general_settings.set_disabled(True)

        self.configuration_information.start_elapsed_timer()
        # while not self.stop_scan:
        #         pass
