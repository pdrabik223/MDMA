import numpy as np
import pyqtgraph as pg

from Measurement import Measurement
from plot_widgets.PlotWidget import PlotType, PlotWidget
from PIL import Image


class Heatmap2DWidget(PlotWidget):
    def __init__(self, printer_path=None):
        super().__init__(plot_type=PlotType.Heatmap2D)

        # create the color bar for the heatmap
        self.color_bar_widget = pg.GradientWidget(orientation="right")

        try:
            self.default_view()

        except Exception as ex:
            print(f"failed to load logo: {str(ex)}")
            z = np.empty((50, 50), float)
            self.update_from_scan(0, 50, 0, 50, z)

    def default_view(self):

        self.axes.cla()
        self.add_labels_and_axes_styling()

        self.axes.imshow(
            np.asarray(Image.open('C:\\D\\MDMA\\assets\\3d.png')),
            cmap="Wistia",
            extent=[0, 512, 0, 512],
            interpolation="none",
            origin="upper",
        )

        self.axes.set_xlim([-10, 522])
        self.axes.set_ylim([-10, 522])

    def add_labels_and_axes_styling(self):
        self.axes_styling("Extruder path")
        self.axes.set_xlabel("X [mm]")
        self.axes.set_ylabel("Y [mm]")
        self.axes.set_title("Measurement")

    def update_from_scan(self, x_min, x_max, y_min, y_max, z):
        self.axes.cla()
        self.add_labels_and_axes_styling()
        # Compute the mean of the non-None elements

        if isinstance(z, Measurement):
            local_z = np.array(z.scan_data, copy=True)
        else:
            local_z = np.array(z, copy=True)

        if not np.isnan(local_z).all():
            z_mean = np.mean(local_z[~np.isnan(local_z)])
            local_z[np.isnan(local_z)] = z_mean

        # Replace the None elements with the mean value

        self.axes.imshow(
            local_z.T,
            cmap="Wistia",
            vmin=np.min(local_z),
            vmax=np.max(local_z),
            extent=[x_min, x_max, y_min, y_max],
            interpolation="none",
            origin="lower",
        )

        self.axes.set_xlim([x_min, x_max])
        self.axes.set_ylim([y_min, y_max])

        self.show()
        # self.axes.legend(loc="upper right", fancybox=True)
