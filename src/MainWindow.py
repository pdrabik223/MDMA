from PyQt5.QtWidgets import QMainWindow

from vector3d.vector import Vector

from src.PrinterPath import Square
from src.plot_widgets.PrinterPathWidget2D import PrinterPathWidget2D
from src.plot_widgets.PrinterPathWidget3D import PrinterPathWidget3D


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Window")
        self.setGeometry(100, 100, 800, 600)

        self.setCentralWidget(
            PrinterPathWidget2D.from_settings(
                pass_height=5,
                antenna_offset=Vector(1, 56, 0),
                scanned_area=Square(30, 30, 50, 50),
                measurement_radius=3,
            )
        )
