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
    PRINTER_STATE_PARAMS,
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
)
from PrinterPath import Square, PrinterPath
from time import sleep


class MeasurementWorker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(float)

    def init(self, spectrum_analyzer_controller_state: dict,
             printer_controller_state: dict,
             scan_path_settings_state: dict,
             scan_configuration_state: dict,
             ):
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
        self.scan_configuration_state[NO_CURRENT_MEASUREMENT] = 0

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

    def start_measurement_cycle(self):
        """main measurement loop"""
        print("""HOME ALL AXIS""")

        print("""DRAW BOUNDING_BOX""")
        for bounding_box_points in self.printer_path.get_extruder_bounding_box():
            print(bounding_box_points)

        for no_current_measurement, measurement_positions in enumerate(
                zip(self.printer_path.get_extruder_path(), self.printer_path.get_antenna_path())):
            print(f'no_current_measurement: {no_current_measurement}')
            print(f"no_measurements: {self.printer_path.no_measurements}")
            self.progress.emit(no_current_measurement)
            print("""MOVE TO THE NEXT MEASUREMENT SPOT""")
            sleep(0.5)
            print("""REQUEST SCAN""")
            print("""UPDATE PLOTS""")

        self.finished.emit()
