import os

import pandas as pd
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QGridLayout, QMainWindow, QWidget
from vector3d.vector import Vector

from src.gui_controls.ConfigurationInformationWidget import (
    ConfigurationInformationWidget,
)
from src.gui_controls.GeneralSettings import GeneralSettings
from src.gui_controls.PrinterControllerWidget import (
    PrinterControllerWidget,
    PRINTER_WIDTH_IN_MM,
    PRINTER_LENGTH_IN_MM,
)
from src.gui_controls.ScannPathSettingsWidget import (
    ScannPathSettingsWidget,
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
from src.gui_controls.SpectrumAnalyzerControllerWidget import (
    SpectrumAnalyzerControllerWidget,
)
from src.plot_widgets.Heatmap2DWidget import Heatmap2DWidget
from src.plot_widgets.PrinterPathWidget2D import PrinterPathWidget2D
from src.plot_widgets.PrinterPathWidget3D import PrinterPathWidget3D
from src.PrinterPath import Square, PrinterPath


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.stop_scan = False

        # this will be set in _init_ui based on default values in settings
        self.current_scan_path = None

        self._init_ui()
        self.connect_functions()

    def _init_ui(self):
        self.setWindowTitle(f"MDMA v{os.environ.get('VERSION')}")
        self.setWindowIcon(QIcon("assets/sensor.png"))

        self.setGeometry(100, 100, 1600, 600)

        self.main_layout = QGridLayout()

        self.spectrum_analyzer_controller = SpectrumAnalyzerControllerWidget()
        self.printer_controller = PrinterControllerWidget()
        self.scann_path_settings = ScannPathSettingsWidget()
        self.general_settings = GeneralSettings()
        self.configuration_information = ConfigurationInformationWidget()

        # settings section
        self.main_layout.addWidget(self.spectrum_analyzer_controller, *(0, 0))
        self.main_layout.addWidget(self.printer_controller, *(1, 0))
        self.main_layout.addWidget(self.scann_path_settings, *(2, 0))
        self.main_layout.addWidget(self.configuration_information, *(3, 0))
        self.main_layout.addWidget(self.general_settings, *(4, 0))

        self.update_current_scan_path_from_scann_path_settings()

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
        self.scann_path_settings.on_recalculate_path_button_press(self.recalculate_path)

    def update_current_scan_path_from_scann_path_settings(self):
        printer_settings = self.printer_controller.get_state()
        path_settings = self.scann_path_settings.get_state()

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
        print([f"x:{point.x}, y:{point.y}" for point in self.current_scan_path.get_antenna_path()])

    def recalculate_path(self):
        self.update_current_scan_path_from_scann_path_settings()

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

    def perform_measurement(self):
        while not self.stop_scan:
            # compute path
            # update ui
            # run printer start up procedure
            # run outline
            #

            pass
