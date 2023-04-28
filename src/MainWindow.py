import json
import os
from typing import Optional, Union

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog, QGridLayout, QMainWindow, QWidget
from serial import SerialException
from vector3d.vector import Vector

from gui_controls.ConfigurationInformationWidget import (
    ConfigurationInformationWidget,
)
from gui_controls.DeviceConnectionStateLabel import (
    CONNECTED,
    CONNECTING,
    DEVICE_NOT_FOUND,
)
from gui_controls.GeneralSettings import START_MEASUREMENT, GeneralSettings
from gui_controls.MeasurementWorker import MeasurementWorker
from gui_controls.PrinterControllerWidget import (
    CONNECTION_STATE,
    PRINTER_LENGTH_IN_MM,
    PRINTER_WIDTH_IN_MM,
    PrinterControllerWidget,
)
from gui_controls.ScanPathSettingsWidget import (
    ANTENNA_X_OFFSET_IN_MM,
    ANTENNA_Y_OFFSET_IN_MM,
    MEASUREMENT_RADIUS_IN_MM,
    SAMPLE_LENGTH_IN_MM,
    SAMPLE_WIDTH_IN_MM,
    SAMPLE_X_POSITION_IN_MM,
    SAMPLE_Y_POSITION_IN_MM,
    SCAN_HEIGHT_IN_MM,
    ScanPathSettingsWidget,
)
from gui_controls.SpectrumAnalyzerControllerWidget import (
    FREQUENCY_IN_HZ,
    SpectrumAnalyzerControllerWidget,
)
from plot_widgets.Heatmap2DWidget import Heatmap2DWidget
from plot_widgets.PrinterPathWidget2D import PrinterPathWidget2D
from printer_device.MarlinDevice import MarlinDevice
from printer_device.PrinterDevice import PrinterDevice
from printer_device.PrinterDeviceMock import PrinterDeviceMock

from PrinterPath import PrinterPath, Square
from spectrum_analyzer_device.hameg3010.hameg3010device import Hameg3010Device
from spectrum_analyzer_device.hameg3010.HamegHMS3010DeviceMock import (
    HamegHMS3010DeviceMock,
)

load_dotenv()
VERSION = os.environ.get("VERSION")
PRINTED_MODE = os.environ.get("PRINTED_MODE", False)
ANALYZER_MODE = os.environ.get("ANALYZER_MODE", False)


class MainWindow(QMainWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stop_scan = False

        # this will be set in _init_ui based on default values in settings
        self.current_scan_path = None

        self.spectrum_analyzer_controller = SpectrumAnalyzerControllerWidget()
        self.printer_controller = PrinterControllerWidget()
        self.scan_path_settings = ScanPathSettingsWidget()
        self.general_settings = GeneralSettings()
        self.configuration_information = ConfigurationInformationWidget()

        self.measurement_thread = QThread()
        self.measurement_worker = MeasurementWorker()
        self._init_ui()

        self.analyzer_device = self.try_to_set_up_analyzer_device()
        self.printer_device = self.try_to_set_up_printer_device()

        self.init_measurement_thread()
        self.connect_functions()
        self.measurement_data = None

    def export_project(self):
        measurement = pd.DataFrame(self.measurement_data)
        print(measurement.head())

        file_name = QFileDialog.getSaveFileName(
            self,
            "Export Project",
            os.getcwd(),
            "MDMA project(*.mdma)",
        )

        if file_name != "":
            directory_path, extention = file_name
            root_directory_path = directory_path.split(".")
            root_directory_path = ".".join(root_directory_path[:-1])

            os.mkdir(root_directory_path)
            data_path = os.path.join(root_directory_path, "data.mdma")
            config_path = os.path.join(root_directory_path, "config.json")
            config_dict = {}
            config_dict.update({"spectrum_analyzer_controller": self.spectrum_analyzer_controller.get_state()})
            config_dict.update({"printer_controller": self.printer_controller.get_state()})
            config_dict.update({"scan_path_settings": self.scan_path_settings.get_state()})
            config_dict.update({"configuration_information": self.configuration_information.get_state()})

            with open(config_path, "w") as outfile:
                json.dump(config_dict, outfile)
            measurement.to_csv(data_path)

            printer_path_fig_path = os.path.join(root_directory_path, "printer_path.png")
            self.printer_path_widget.save_fig(printer_path_fig_path)

    def load_project(self):
        raise NotImplementedError()

    def save_config(self):
        raise NotImplementedError()

    def load_config(self):
        raise NotImplementedError()

    def update_measurement_data(self, new_measurement: np.ndarray):
        self.measurement_data = new_measurement

    def closeEvent(self, event):
        print("User has clicked the red x on the main window")
        self.measurement_thread.quit()
        event.accept()

    def init_measurement_thread(self):
        self.measurement_worker.moveToThread(self.measurement_thread)
        self.measurement_thread.started.connect(self.measurement_worker.start_measurement_cycle)

        self.measurement_worker.finished.connect(self.update_ui_after_measurement)
        self.measurement_worker.finished.connect(self.measurement_thread.quit)

        # self.measurement_worker.finished.connect(self.measurement_worker.deleteLater)
        self.measurement_worker.progress.connect(self.configuration_information.set_current_scanned_point)
        self.measurement_worker.post_last_measurement.connect(self.spectrum_analyzer_controller.set_last_measurement)
        self.measurement_worker.post_scan_meshgrid.connect(self.heatmap_widget.update_from_scan)

        # self.measurement_thread.finished.connect(self.measurement_thread.deleteLater)

        self.measurement_thread.finished.connect(self.update_ui_after_measurement)
        self.measurement_worker.finished.connect(self.update_measurement_data)

    def try_to_set_up_analyzer_device(self) -> Optional[Hameg3010Device]:
        self.spectrum_analyzer_controller.set_connection_label_text(CONNECTING)
        try:
            self.spectrum_analyzer_controller.set_connection_label_text(CONNECTED)

            if ANALYZER_MODE == "mock_hameg":
                return HamegHMS3010DeviceMock.automatically_connect()
            else:
                return Hameg3010Device.automatically_connect()

        except ValueError:
            self.spectrum_analyzer_controller.set_connection_label_text(DEVICE_NOT_FOUND)
            return None

    def try_to_set_up_printer_device(self) -> Optional[PrinterDevice]:
        self.printer_controller.set_connection_label_text(CONNECTING)
        try:
            self.printer_controller.set_connection_label_text(CONNECTED)
            if PRINTED_MODE == "mock_printer":
                return PrinterDeviceMock.connect()
            else:
                return MarlinDevice.connect()

        except SerialException:
            self.printer_controller.set_connection_label_text(DEVICE_NOT_FOUND)
            print("could not connect")
            return None

    def _init_ui(self):
        self.setWindowTitle(f"MDMA v{VERSION}")
        self.setWindowIcon(QIcon("assets/sensor.png"))

        self.setGeometry(100, 100, 1600, 600)

        self.main_layout = QGridLayout()

        # settings section
        self.main_layout.addWidget(self.spectrum_analyzer_controller, *(0, 0))
        self.main_layout.addWidget(self.printer_controller, *(1, 0))
        self.main_layout.addWidget(self.scan_path_settings, *(2, 0))
        self.main_layout.addWidget(self.configuration_information, *(3, 0))
        self.main_layout.addWidget(self.general_settings, *(4, 0))

        self.update_current_scan_path_from_scan_path_settings()

        self.printer_path_widget = PrinterPathWidget2D.from_printer_path(self.current_scan_path)

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
        self.general_settings.on_stop_measurement_button_press(self.measurement_worker.stop_thread_execution)
        self.spectrum_analyzer_controller.on_refresh_connection_button_press(self.try_to_set_up_analyzer_device)
        self.printer_controller.on_refresh_connection_button_press(self.try_to_set_up_printer_device)
        self.spectrum_analyzer_controller.on_update_last_measurement_button_press(
            lambda: self.analyzer_device.get_level(self.spectrum_analyzer_controller.get_state()[FREQUENCY_IN_HZ])
        )
        self.spectrum_analyzer_controller.on_update_last_measurement_button_press(self.update_last_measurement)
        self.general_settings.on_export_scan_button_press(self.export_project)

    def update_last_measurement(self):
        # TODO make it async
        self.spectrum_analyzer_controller.set_last_measurement(
            self.analyzer_device.get_level(self.spectrum_analyzer_controller.get_state()[FREQUENCY_IN_HZ])
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
            no_current_measurement=0,
            total_scan_time_in_seconds=self.current_scan_path.total_scan_time_in_seconds(),
        )
        self.printer_path_widget.update_from_printer_path(self.current_scan_path)
        self.printer_path_widget.show()

    def re_compute_path(self):
        raise NotImplementedError()

    def update_ui(self):
        raise NotImplementedError()

    def run_outline(self):
        raise NotImplementedError()

    def perform_measurement(self):
        raise NotImplementedError()

    def scan_can_be_performed(self) -> Union[bool, str]:
        if self.current_scan_path.get_no_scan_points() <= 0:
            raise ValueError("Scan path is of length 0")

        printer_settings = self.printer_controller.get_state()
        if printer_settings[CONNECTION_STATE] != CONNECTED:
            raise ValueError("Printer device connection failed")

        analyzer = self.spectrum_analyzer_controller.get_state()
        if analyzer[CONNECTION_STATE] != CONNECTED:
            raise ValueError("Analyzer device connection failed")

        return True

    def update_ui_before_measurement(self):
        self.spectrum_analyzer_controller.set_disabled(True)
        self.printer_controller.set_disabled(True)
        self.scan_path_settings.set_disabled(True)
        self.general_settings.set_disabled(True)
        self.configuration_information.start_elapsed_timer()

    def update_ui_after_measurement(self):
        self.spectrum_analyzer_controller.set_disabled(False)
        self.printer_controller.set_disabled(False)
        self.scan_path_settings.set_disabled(False)
        self.general_settings.set_disabled(False)
        self.general_settings.start_measurement.set_state(START_MEASUREMENT)
        self.configuration_information.stop_elapsed_timer()

    def start_measurement(self):
        if self.printer_device is None:
            raise ValueError("printer_handle is None")
        if self.analyzer_device is None:
            raise ValueError("analyzer_handle is None")
        self.update_ui_before_measurement()
        self.measurement_worker.init(
            spectrum_analyzer_controller_state=self.spectrum_analyzer_controller.get_state(),
            printer_controller_state=self.printer_controller.get_state(),
            scan_path_settings_state=self.scan_path_settings.get_state(),
            scan_configuration_state=self.configuration_information.get_state(),
            printer_handle=self.printer_device,
            analyzer_handle=self.analyzer_device,
        )
        self.measurement_thread.start()
