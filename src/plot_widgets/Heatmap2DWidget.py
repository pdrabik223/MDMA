import numpy as np
import pyqtgraph as pg

from plot_widgets.PlotWidget import PlotType, PlotWidget


class Heatmap2DWidget(PlotWidget):
    def __init__(self, printer_path=None):
        super().__init__(plot_type=PlotType.Heatmap2D)

        # create the color bar for the heatmap
        self.color_bar_widget = pg.GradientWidget(orientation="right")

        z = np.zeros((50, 50), float)

        for id_x, x in enumerate(z):
            for id_y, y in enumerate(x):
                z[id_x][id_y] = (id_x / 50) + (id_y / 50)

        self.update_from_scan(0, 50, 0, 50, z)

    def add_labels_and_axes_styling(self):
        self.axes_styling("Extruder path")
        self.axes.set_xlabel("X [mm]")
        self.axes.set_ylabel("Y [mm]")
        self.axes.set_title("Measurement")

    def update_from_scan(self, x_min, x_max, y_min, y_max, z):
        self.axes.cla()
        self.add_labels_and_axes_styling()
        self.axes.imshow(
            z.T,
            cmap="Wistia",
            vmin=np.min(z),
            vmax=np.max(z),
            extent=[x_min, x_max, y_min, y_max],
            interpolation="none",
            origin="lower",
        )
        self.show()
        # self.axes.legend(loc="upper right", fancybox=True)
