import os
from typing import Union, Optional

import numpy as np
from PyQt6 import QtGui
from dotenv import load_dotenv
from PyQt6.QtCore import QThread, Qt
from PyQt6.QtWidgets import QGridLayout, QMainWindow, QWidget, QVBoxLayout, QScrollArea
from serial import SerialException
from vector3d.vector import Vector

from src.gui_controls.ConfigurationInformationWidget import (
    ConfigurationInformationWidget,
)
from gui_controls.custom_input_fiedls.DeviceConnectionStateLabel import (
    CONNECTED,
    CONNECTING,
    DEVICE_NOT_FOUND,
)
from gui_controls.custom_input_fiedls.StartStopButton import START_MEASUREMENT
from src.gui_controls.GeneralSettings import GeneralSettings
from functionalities.MeasurementWorker import MeasurementWorker, Measurement
from src.gui_controls.PrinterControllerWidget import (
    CONNECTION_STATE,
    PRINTER_LENGTH_IN_MM,
    PRINTER_WIDTH_IN_MM,
    PrinterControllerWidget,
    STEP_SIZE_IN_MM,
    MOVEMENT_SPEED,
)
from src.gui_controls.ScanPathSettingsWidget import (
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
from src.gui_controls.SpectrumAnalyzerControllerWidget import (
    FREQUENCY_IN_HZ,
    SpectrumAnalyzerControllerWidget,
    MEASUREMENT_TIME,
    SCAN_MODE,
    HAMEG_HMS_3010,
    POCKET_VNA,
)
from functionalities.export_import_functions import export_project, save_config, load_project, load_config
from src.plot_widgets.Heatmap2DWidget import Heatmap2DWidget
from src.plot_widgets.PrinterPathWidget2D import PrinterPathWidget2D
from src.printer_device.MarlinDevice import MarlinDevice
from src.printer_device.PrinterDevice import Direction
from src.printer_device.PrinterDeviceMock import PrinterDeviceMock

from functionalities.PrinterPath import PrinterPath, Square

from src.spectrum_analyzer_device.hameg3010.HamegHMS3010DeviceMock import (
    HamegHMS3010DeviceMock,
)
from src.spectrum_analyzer_device.hameg3010.HamegHMS3010SerialDevice import HamegHMS3010DeviceSerial
from src.spectrum_analyzer_device.pocket_vna_device.PocketVNADevice import PocketVnaDevice
from src.spectrum_analyzer_device.pocket_vna_device.PocketVnaDeviceMock import PocketVnaDeviceMock

load_dotenv()
VERSION = os.environ.get("VERSION")
PRINTED_MODE = os.environ.get("PRINTED_MODE", "real_device")
ANALYZER_MODE = os.environ.get("ANALYZER_MODE", "real_device")


class MainWindow(QMainWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # this will be set in _init_ui based on default values in settings
        self.plots = []
        self.current_scan_path: Optional[PrinterPath] = None
        self.analyzer_device = None
        self.spectrum_analyzer_controller = SpectrumAnalyzerControllerWidget()
        self.printer_controller = PrinterControllerWidget()
        self.scan_path_settings = ScanPathSettingsWidget()
        self.general_settings = GeneralSettings()
        self.configuration_information = ConfigurationInformationWidget()

        self.measurement_thread = QThread()
        self.measurement_worker = MeasurementWorker()
        self._init_ui()

        self.try_to_set_up_analyzer_device()
        self.try_to_set_up_printer_device()

        self.init_measurement_thread()
        self.connect_functions()
        self.measurement_data = Measurement.empty_measurement()

    def update_measurement_data(self, new_measurement: np.ndarray):
        self.measurement_data = new_measurement

    def closeEvent(self, event):
        print("User has clicked the red x on the main window")
        self.measurement_thread.quit()
        event.accept()

    def display_plots(self):
        for plot in self.plots:
            self.main_layout.removeWidget(plot["widget"])
            plot["widget"].deleteLater()
            plot["widget"] = None

        if self.spectrum_analyzer_controller.get_state()[SCAN_MODE] == HAMEG_HMS_3010:
            self.plots = [
                {
                    "widget": Heatmap2DWidget(title="Signal Amplitude [dB]"),
                    "position": (0, 2),
                    "shape": (2, 1),
                    "title": "Signal Amplitude [dB]",
                }
            ]

        elif self.spectrum_analyzer_controller.get_state()[SCAN_MODE] == POCKET_VNA:
            self.plots = [
                {
                    "widget": Heatmap2DWidget(title="Real part"),
                    "position": (0, 2),
                    "shape": (1, 1),
                    "title": "Real part",
                },
                {
                    "widget": Heatmap2DWidget(title="Imaginary part"),
                    "position": (1, 2),
                    "shape": (1, 1),
                    "title": "Imaginary part",
                },
            ]

        for plot in self.plots:
            self.main_layout.addWidget(plot["widget"], *plot["position"], *plot["shape"])

    def update_plot_from_scan(self, measurement):
        if self.spectrum_analyzer_controller.get_state()[SCAN_MODE] == HAMEG_HMS_3010:
            self.plots[0]["widget"].update_from_scan(measurement)
        elif self.spectrum_analyzer_controller.get_state()[SCAN_MODE] == POCKET_VNA:
            self.plots[0]["widget"].update_from_vna_scan(measurement, "real")
            self.plots[1]["widget"].update_from_vna_scan(measurement, "imag")

    def init_measurement_thread(self):
        self.measurement_worker.moveToThread(self.measurement_thread)
        self.measurement_thread.started.connect(self.measurement_worker.start_measurement_cycle)

        self.measurement_worker.finished.connect(self.update_ui_after_measurement)
        self.measurement_worker.finished.connect(self.measurement_thread.quit)

        # self.measurement_worker.finished.connect(self.measurement_worker.deleteLater)
        self.measurement_worker.progress.connect(self.configuration_information.set_current_scanned_point)
        self.measurement_worker.post_last_measurement.connect(self.spectrum_analyzer_controller.set_last_measurement)
        self.measurement_worker.post_scan_meshgrid.connect(self.update_plot_from_scan)

        # self.measurement_thread.finished.connect(self.measurement_thread.deleteLater)

        self.measurement_thread.finished.connect(self.update_ui_after_measurement)
        self.measurement_worker.finished.connect(self.update_measurement_data)

    def try_to_set_up_analyzer_device(self) -> None:
        self.spectrum_analyzer_controller.set_connection_label_text(CONNECTING)

        if self.analyzer_device is not None:
            self.analyzer_device.close()

        scan_mode = self.spectrum_analyzer_controller.get_state()[SCAN_MODE]

        if "mock_hameg" in ANALYZER_MODE and scan_mode == HAMEG_HMS_3010:
            self.analyzer_device = HamegHMS3010DeviceMock.automatically_connect()
            self.spectrum_analyzer_controller.set_connection_label_text(CONNECTED)
            return
        elif "mock_pocket_vna" in ANALYZER_MODE and scan_mode == POCKET_VNA:
            self.analyzer_device = PocketVnaDeviceMock.automatically_connect()
            self.spectrum_analyzer_controller.set_connection_label_text(CONNECTED)
            return
        try:
            if scan_mode == HAMEG_HMS_3010:
                self.analyzer_device = HamegHMS3010DeviceSerial.automatically_connect()

            elif scan_mode == POCKET_VNA:
                self.analyzer_device = PocketVnaDevice.automatically_connect()

            self.spectrum_analyzer_controller.set_connection_label_text(CONNECTED)

        except Exception as ex:
            print(str(ex))
            self.spectrum_analyzer_controller.set_connection_label_text(DEVICE_NOT_FOUND)
            self.analyzer_device = None

    def try_to_set_up_printer_device(self) -> None:
        self.printer_controller.set_connection_label_text(CONNECTING)
        if PRINTED_MODE == "mock_printer":
            self.printer_controller.set_connection_label_text(CONNECTED)
            self.printer_device = PrinterDeviceMock.connect()
            return
        try:
            self.printer_controller.set_connection_label_text(CONNECTED)
            self.printer_device = MarlinDevice.connect()

        except SerialException:
            self.printer_controller.set_connection_label_text(DEVICE_NOT_FOUND)
            self.printer_device = None

    def _init_ui(self):
        self.setWindowTitle(f"MDMA v{VERSION}")
        self.setWindowIcon(QtGui.QIcon("assets\\3d_fill_color.png"))

        self.setGeometry(100, 100, 1460, 600)

        self.main_layout = QGridLayout()
        self.settings_layout = QVBoxLayout()
        self.scroll_area = QScrollArea()
        self.main_layout.addWidget(self.scroll_area, *(0, 0), *(2, 1))
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(False)

        # settings section
        self.settings_layout.addWidget(self.spectrum_analyzer_controller)
        self.settings_layout.addWidget(self.printer_controller)
        self.settings_layout.addWidget(self.scan_path_settings)
        self.settings_layout.addWidget(self.configuration_information)
        self.settings_layout.addWidget(self.general_settings)

        self.settings_widget = QWidget()

        self.settings_widget.setLayout(self.settings_layout)
        self.scroll_area.setWidget(self.settings_widget)

        self.update_current_scan_path_from_scan_path_settings()

        self.printer_path_plot = PrinterPathWidget2D.from_printer_path(self.current_scan_path)
        self.main_layout.addWidget(self.printer_path_plot, *(0, 1), *(2, 1))
        self.recalculate_path()

        self.display_plots()

        widget = QWidget()
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)

    def home_all_axis(self):
        self.printer_device.home_all_axis()
        self.printer_controller.update_extruder_position(self.printer_device.current_position)

    def center_extruder(self):
        self.printer_device.center_extruder(self.printer_controller.get_state()[MOVEMENT_SPEED])
        self.printer_controller.update_extruder_position(self.printer_device.current_position)

    def step(self, direction: Direction):
        self.printer_device.step(
            direction,
            self.printer_controller.get_state()[STEP_SIZE_IN_MM],
            self.printer_controller.get_state()[MOVEMENT_SPEED],
        )
        self.printer_controller.update_extruder_position(self.printer_device.current_position)

    def connect_functions(self):
        self.scan_path_settings.on_recalculate_path_button_press(self.recalculate_path)
        self.general_settings.on_start_measurement_button_press(self.start_measurement)
        self.general_settings.on_stop_measurement_button_press(self.measurement_worker.stop_thread_execution)
        self.spectrum_analyzer_controller.on_refresh_connection_button_press(self.try_to_set_up_analyzer_device)
        self.spectrum_analyzer_controller.on_scan_mode_box_change(self.try_to_set_up_analyzer_device)
        self.spectrum_analyzer_controller.on_scan_mode_box_change(self.display_plots)

        self.printer_controller.on_refresh_connection_button_press(self.try_to_set_up_printer_device)

        self.printer_controller.on_h_button_press(self.home_all_axis)

        self.printer_controller.on_center_extruder_button_press(self.center_extruder)

        self.printer_controller.on_py_button_press(lambda x: self.step(Direction.PY))
        self.printer_controller.on_ny_button_press(lambda x: self.step(Direction.NY))

        self.printer_controller.on_pz_button_press(lambda x: self.step(Direction.PZ))
        self.printer_controller.on_nz_button_press(lambda x: self.step(Direction.NZ))

        self.printer_controller.on_px_button_press(lambda x: self.step(Direction.PX))
        self.printer_controller.on_nx_button_press(lambda x: self.step(Direction.NX))

        self.spectrum_analyzer_controller.on_update_last_measurement_button_press(self.update_last_measurement)
        self.general_settings.on_export_scan_button_press(lambda x: export_project(self))
        self.general_settings.on_export_settings_button_press(lambda x: save_config(self))
        self.general_settings.on_import_scan_button_press(lambda x: load_project(self))
        self.general_settings.on_import_settings_button_press(lambda x: load_config(self))

    def update_last_measurement(self):
        # TODO make it async
        self.spectrum_analyzer_controller.set_last_measurement(
            self.analyzer_device.get_level(
                self.spectrum_analyzer_controller.get_state()[FREQUENCY_IN_HZ],
                self.spectrum_analyzer_controller.get_state()[MEASUREMENT_TIME],
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
            no_current_measurement=0,
            total_scan_time_in_seconds=self.current_scan_path.total_scan_time_in_seconds(),
        )
        self.printer_path_plot.update_from_printer_path(self.current_scan_path)
        self.printer_path_plot.show()

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
        for plot in self.plots:
            plot["widget"].default_view()
            plot["widget"].show()
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
        self.general_settings.activate_export_buttons()

    def start_measurement(self):
        if self.printer_device is None:
            raise ValueError("printer_handle is None")

        if self.analyzer_device is None:
            raise ValueError("analyzer_handle is None")

        self.recalculate_path()
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
