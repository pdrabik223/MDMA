import numpy as np
import pandas as pd
from PyQt5.QtCore import QObject, pyqtSignal
from vector3d.vector import Vector

from gui_controls.ConfigurationInformationWidget import (
    CONFIGURATION_INFORMATION_STATE_PARAMS,
    NO_CURRENT_MEASUREMENT,
    NO_MEASUREMENTS,
)
from gui_controls.PrinterControllerWidget import (
    PRINTER_WIDTH_IN_MM,
    PRINTER_LENGTH_IN_MM,
    PRINTER_STATE_PARAMS, MOVEMENT_SPEED,
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
    SPECTRUM_ANALYZER_STATE_PARAMS, FREQUENCY_IN_HZ,
)
from PrinterPath import Square, PrinterPath
from time import sleep


class MeasurementWorker(QObject):
    finished = pyqtSignal(np.ndarray)
    progress = pyqtSignal(float)
    post_last_measurement = pyqtSignal(float)
    post_scan_meshgrid = pyqtSignal(float, float, float, float, np.ndarray)
    stop_thread: bool = True

    def __init__(self):
        super().__init__()

    def init(self, spectrum_analyzer_controller_state: dict,
             printer_controller_state: dict,
             scan_path_settings_state: dict,
             scan_configuration_state: dict,
             printer_handle,
             analyzer_handle):

        self.printer_handle = printer_handle
        self.analyzer_handle = analyzer_handle
        self.spectrum_analyzer_controller_state = spectrum_analyzer_controller_state
        self.printer_controller_state = printer_controller_state
        self.scan_path_settings_state = scan_path_settings_state
        self.scan_configuration_state = scan_configuration_state
        self.printer_path = PrinterPath(
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

        self.min_x = self.printer_path.get_antenna_min_x_val()
        self.max_x = self.printer_path.get_antenna_max_x_val()
        self.min_y = self.printer_path.get_antenna_min_y_val()
        self.max_y = self.printer_path.get_antenna_max_y_val()

        self.x_axis_length = len(np.unique([pos.x for pos in self.printer_path.get_antenna_path()]))
        self.y_axis_length = len(np.unique([pos.y for pos in self.printer_path.get_antenna_path()]))

        self.scan_data = np.zeros((self.x_axis_length, self.y_axis_length), float)

    def validate_inputs(self):
        assert (
            not len(
                [
                    False
                    for param in PRINTER_STATE_PARAMS
                    if param not in self.printer_controller_state
                ]
            )
        )

        assert (
            not len(
                [
                    False
                    for param in SPECTRUM_ANALYZER_STATE_PARAMS
                    if param not in self.spectrum_analyzer_controller_state
                ]
            )

        )

        assert (
            not len(
                [
                    False
                    for param in SCAN_PATH_STATE_PARAMS
                    if param not in self.scan_path_settings_state
                ]
            )

        )

        assert (
            not len(
                [
                    False
                    for param in CONFIGURATION_INFORMATION_STATE_PARAMS
                    if param not in self.scan_configuration_state
                ]
            )

        )

        assert self.printer_path.no_measurements > 0

    def stop_thread_execution(self):
        self.stop_thread = True
        print("stopping thread")

    def start_measurement_cycle(self):
        """main measurement loop"""

        if self.stop_thread:
            self.finished.emit(self.scan_data)
            return
        self.progress.emit(0)

        self.printer_handle.send_and_await("G28")

        for bounding_box_points in self.printer_path.get_extruder_bounding_box():
            if self.stop_thread:
                self.finished.emit(self.scan_data)
                return
            self.printer_handle.send_and_await(f"G1 X{bounding_box_points[0]} "
                                               f"Y{bounding_box_points[1]} "
                                               f"Z{self.scan_path_settings_state[SCAN_HEIGHT_IN_MM]} "
                                               f"F{self.printer_controller_state[MOVEMENT_SPEED]}")

        for no_current_measurement, measurement_positions in enumerate(
                zip(self.printer_path.get_extruder_path(), self.printer_path.get_antenna_path())):

            if self.stop_thread:
                self.finished.emit(self.scan_data)
                return
            self.progress.emit(no_current_measurement + 1)
            extruder_position, antenna_position = measurement_positions
            self.printer_handle.send_and_await(f"G1 X{extruder_position.x} "
                                               f"Y{extruder_position.y} "
                                               f"Z{self.scan_path_settings_state[SCAN_HEIGHT_IN_MM]} "
                                               f"F{self.printer_controller_state[MOVEMENT_SPEED]}")

            if self.stop_thread:
                self.finished.emit(self.scan_data)
                return

            new_measurement = self.analyzer_handle.get_level(self.spectrum_analyzer_controller_state[FREQUENCY_IN_HZ],
                                                             1)  # TODO this measurement time should be read from ui
            self.post_last_measurement.emit(new_measurement)
            self.scan_data[
                no_current_measurement // self.x_axis_length][
                no_current_measurement % self.x_axis_length] = new_measurement

            self.post_scan_meshgrid.emit(self.min_x,
                                         self.max_x,
                                         self.min_y,
                                         self.max_y,
                                         self.scan_data)

            if self.stop_thread:
                self.finished.emit(self.scan_data)
                return

            print("""UPDATE PLOTS""")

        self.finished.emit(self.scan_data)
