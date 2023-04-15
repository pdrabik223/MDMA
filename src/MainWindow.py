import os

import pandas as pd
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QGridLayout, QMainWindow, QWidget
from vector3d.vector import Vector

from src.gui_controls.GeneralSettings import GeneralSettings
from src.gui_controls.PrinterControllerWidget import PrinterControllerWidget
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
from src.PrinterPath import Square


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"MDMA v{os.environ.get('VERSION')}")
        self.setWindowIcon(QIcon("./assets/sensor.png"))

        self.setGeometry(100, 100, 1600, 600)

        self.main_layout = QGridLayout()

        self.spectrum_analyzer_controller = SpectrumAnalyzerControllerWidget()
        self.printer_controller = PrinterControllerWidget()
        self.scann_path_settings = ScannPathSettingsWidget()
        self.general_settings = GeneralSettings()

        # settings section
        self.main_layout.addWidget(self.spectrum_analyzer_controller, *(0, 0))
        self.main_layout.addWidget(self.printer_controller, *(1, 0))
        self.main_layout.addWidget(self.scann_path_settings, *(2, 0))
        self.main_layout.addWidget(self.general_settings, *(3, 0))

        # plots section
        path_settings = self.scann_path_settings.get_state()
        self.main_layout.addWidget(
            PrinterPathWidget2D.from_settings(
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
            ),
            *(0, 1),
            *(4, 1),
        )
        self.main_layout.addWidget(Heatmap2DWidget(), *(0, 2), *(4, 1))

        widget = QWidget()
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)

        self.stop_scan = False

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
