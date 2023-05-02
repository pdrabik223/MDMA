from typing import Union

from PyQt5.QtCore import QObject, pyqtSignal
from vector3d.vector import Vector

from Measurement import Measurement
from gui_controls.ConfigurationInformationWidget import (
    CONFIGURATION_INFORMATION_STATE_PARAMS,
    NO_CURRENT_MEASUREMENT,
)
from gui_controls.PrinterControllerWidget import (
    PRINTER_WIDTH_IN_MM,
    PRINTER_LENGTH_IN_MM,
    PRINTER_STATE_PARAMS,
    MOVEMENT_SPEED,
)
from gui_controls.ScanPathSettingsWidget import (
    SAMPLE_X_POSITION_IN_MM,
    SAMPLE_Y_POSITION_IN_MM,
    ANTENNA_X_OFFSET_IN_MM,
    ANTENNA_Y_OFFSET_IN_MM,
    SAMPLE_LENGTH_IN_MM,
    SAMPLE_WIDTH_IN_MM,
    SCAN_HEIGHT_IN_MM,
    MEASUREMENT_RADIUS_IN_MM,
    SCAN_PATH_STATE_PARAMS,
)
from gui_controls.SpectrumAnalyzerControllerWidget import (
    SPECTRUM_ANALYZER_STATE_PARAMS,
    FREQUENCY_IN_HZ,
    MEASUREMENT_TIME,
)
from PrinterPath import Square
from printer_device.PrinterDevice import PrinterDevice
from spectrum_analyzer_device.hameg3010.HamegHMS3010DeviceMock import HamegHMS3010DeviceMock
from spectrum_analyzer_device.hameg3010.hameg3010device import Hameg3010Device


class MeasurementWorker(QObject):
    finished: pyqtSignal = pyqtSignal(Measurement)
    progress: pyqtSignal = pyqtSignal(float)
    post_last_measurement: pyqtSignal = pyqtSignal(float)
    post_scan_meshgrid: pyqtSignal = pyqtSignal(Measurement)
    stop_thread: bool = True

    def __init__(self):
        super().__init__()

    def init(
        self,
        spectrum_analyzer_controller_state: dict,
        printer_controller_state: dict,
        scan_path_settings_state: dict,
        scan_configuration_state: dict,
        printer_handle: PrinterDevice,
        analyzer_handle: Union[Hameg3010Device, HamegHMS3010DeviceMock],
    ):
        self.printer_handle = printer_handle
        self.analyzer_handle = analyzer_handle
        self.spectrum_analyzer_controller_state = spectrum_analyzer_controller_state
        self.printer_controller_state = printer_controller_state
        self.scan_path_settings_state = scan_path_settings_state
        self.scan_configuration_state = scan_configuration_state
        self.measurement_data = Measurement(
            pass_height=self.scan_path_settings_state[SCAN_HEIGHT_IN_MM],
            antenna_offset=Vector(
                self.scan_path_settings_state[ANTENNA_X_OFFSET_IN_MM],
                self.scan_path_settings_state[ANTENNA_Y_OFFSET_IN_MM],
                0,
            ),
            scanned_area=Square(
                self.scan_path_settings_state[SAMPLE_X_POSITION_IN_MM],
                self.scan_path_settings_state[SAMPLE_Y_POSITION_IN_MM],
                self.scan_path_settings_state[SAMPLE_WIDTH_IN_MM],
                self.scan_path_settings_state[SAMPLE_LENGTH_IN_MM],
            ),
            measurement_radius=self.scan_path_settings_state[MEASUREMENT_RADIUS_IN_MM],
            printer_bed_size=Vector(
                self.printer_controller_state[PRINTER_WIDTH_IN_MM],
                self.printer_controller_state[PRINTER_LENGTH_IN_MM],
                210,
            ),
        )
        self.validate_inputs()
        self.stop_thread: bool = False
        self.scan_configuration_state[NO_CURRENT_MEASUREMENT] = 0

    def validate_inputs(self):
        assert not len([False for param in PRINTER_STATE_PARAMS if param not in self.printer_controller_state])

        assert not len(
            [False for param in SPECTRUM_ANALYZER_STATE_PARAMS if param not in self.spectrum_analyzer_controller_state]
        )

        assert not len([False for param in SCAN_PATH_STATE_PARAMS if param not in self.scan_path_settings_state])

        assert not len(
            [False for param in CONFIGURATION_INFORMATION_STATE_PARAMS if param not in self.scan_configuration_state]
        )

        assert self.measurement_data.printer_path.no_measurements > 0

    def stop_thread_execution(self):
        self.stop_thread = True
        print("stopping thread")

    def start_measurement_cycle(self):
        """main measurement loop"""
        min_x = self.measurement_data.printer_path.get_antenna_min_x_val()
        max_x = self.measurement_data.printer_path.get_antenna_max_x_val()
        min_y = self.measurement_data.printer_path.get_antenna_min_y_val()
        max_y = self.measurement_data.printer_path.get_antenna_max_y_val()

        if self.stop_thread:
            self.finished.emit(self.measurement_data)
            return

        self.progress.emit(0)

        self.printer_handle.send_and_await("G28")

        for bounding_box_points in self.measurement_data.printer_path.get_extruder_bounding_box():
            if self.stop_thread:
                self.finished.emit(self.measurement_data)
                return

            self.printer_handle.send_and_await(
                f"G1 X{bounding_box_points[0]} "
                f"Y{bounding_box_points[1]} "
                f"Z{self.scan_path_settings_state[SCAN_HEIGHT_IN_MM]} "
                f"F{self.printer_controller_state[MOVEMENT_SPEED]}"
            )

        for no_current_measurement, data in enumerate(self.measurement_data):
            self.progress.emit(no_current_measurement + 1)

            if self.stop_thread:
                self.finished.emit(self.measurement_data)
                return

            self.printer_handle.send_and_await(
                f"G1 X{data[0].x} "
                f"Y{data[0].y} "
                f"Z{self.scan_path_settings_state[SCAN_HEIGHT_IN_MM]} "
                f"F{self.printer_controller_state[MOVEMENT_SPEED]}"
            )

            if self.stop_thread:
                self.finished.emit(self.measurement_data)
                return

            measurement = self.analyzer_handle.get_level(
                self.spectrum_analyzer_controller_state[FREQUENCY_IN_HZ],
                self.spectrum_analyzer_controller_state[MEASUREMENT_TIME],
            )
            data[2](measurement)

            self.post_last_measurement.emit(measurement)

            self.post_scan_meshgrid.emit(self.measurement_data)

        self.finished.emit(self.measurement_data)
