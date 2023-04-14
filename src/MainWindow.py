import pandas as pd
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget

from vector3d.vector import Vector

from src.PrinterPath import Square
from src.plot_widgets.Heatmap2DWidget import Heatmap2DWidget
from src.plot_widgets.PrinterPathWidget2D import PrinterPathWidget2D
from src.plot_widgets.PrinterPathWidget3D import PrinterPathWidget3D


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MDMA v2")
        self.setGeometry(100, 100, 1200, 600)

        self.main_layout = QGridLayout()

        self.main_layout.addWidget(
            PrinterPathWidget2D.from_settings(
                pass_height=5,
                antenna_offset=Vector(1, 56, 0),
                scanned_area=Square(30, 30, 50, 50),
                measurement_radius=3,
            ),
            *(0, 1)
        )

        self.main_layout.addWidget(Heatmap2DWidget(), *(0, 2))

        widget = QWidget()
        widget.setLayout(self.main_layout)
        self.setCentralWidget(widget)
