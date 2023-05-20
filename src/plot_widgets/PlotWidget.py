import enum

import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.figure import Figure
from PyQt6.QtWidgets import QVBoxLayout, QWidget

matplotlib.use("Qt5Agg")


class PlotType(enum.Enum):
    Path2D = 0
    Path3D = 1
    Heatmap2D = 2


class PlotWidget(QWidget):
    def __init__(self, plot_type: PlotType):
        super().__init__()

        self.fig = Figure(figsize=(6, 6), dpi=90)
        self.fig.tight_layout()

        if plot_type == PlotType.Path3D:
            self.axes = self.fig.add_subplot(111, projection="3d")
            self.axes.set_xlabel("Untitled")
            self.axes.set_ylabel("Untitled")
            self.axes.set_zlabel("Untitled")
            self.axes.grid()

        elif plot_type == PlotType.Path2D:
            self.axes = self.fig.add_subplot(111)
            self.axes.set_xlabel("Untitled")
            self.axes.set_ylabel("Untitled")
            self.axes.grid()

        elif plot_type == PlotType.Heatmap2D:
            self.axes = self.fig.add_subplot(111)

        self.axes_styling()

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.figure_canvas = FigureCanvas(self.fig)
        try:
            self.main_layout.addWidget(NavigationToolbar2QT(self.figure_canvas, self))
            self.main_layout.addWidget(self.figure_canvas)
        except Exception:
            pass

    def axes_styling(self, window_title="Untitled"):
        self.axes.set_title(window_title)
        self.axes.axis("square")

    def show(self):
        self.figure_canvas.draw()

    def save_fig(self, path):
        self.fig.savefig(path)

    def get_title(self):
        return self.fig.axes[0].get_title()
