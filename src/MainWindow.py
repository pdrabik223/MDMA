import os

import pandas as pd
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QGridLayout, QMainWindow, QWidget
from vector3d.vector import Vector

from src.gui_controls.GeneralSettings import GeneralSettings
from src.gui_controls.PrinterControllerWidget import PrinterControllerWidget
from src.gui_controls.ScannPathSettingsWidget import ScannPathSettingsWidget
from src.gui_controls.SpectrumAnalyzerControllerWidget import \
    SpectrumAnalyzerControllerWidget
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

        self.main_layout.addWidget(
            PrinterPathWidget2D.from_settings(
                pass_height=5,
                antenna_offset=Vector(1, 56, 0),
                scanned_area=Square(30, 30, 50, 50),
                measurement_radius=3,
            ),
            *(0, 1),
            4,
            1,
        )

        self.main_layout.addWidget(Heatmap2DWidget(), *(0, 2), 4, 1)

        self.main_layout.addWidget(SpectrumAnalyzerControllerWidget(), *(0, 3))
        self.main_layout.addWidget(PrinterControllerWidget(), *(1, 3))

        self.main_layout.addWidget(ScannPathSettingsWidget(), *(2, 3))
        self.main_layout.addWidget(GeneralSettings(), *(3, 3))

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
