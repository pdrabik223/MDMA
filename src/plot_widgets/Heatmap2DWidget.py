import numpy as np
import pyqtgraph as pg

from functionalities.Measurement import Measurement
from src.plot_widgets.PlotWidget import PlotType, PlotWidget
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

            self.axes.imshow(
                z,
                cmap="Wistia",
                extent=[0, 50, 0, 50],
                interpolation="none",
                origin="upper",
            )

            self.axes.set_xlim([0, 50])
            self.axes.set_ylim([0, 50])

    def default_view(self):
        self.axes.cla()
        self.add_labels_and_axes_styling()

        self.axes.imshow(
            np.asarray(Image.open("assets\\3d_fill_color.png")),
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

    def update_from_scan(self, z: Measurement):
        self.axes.cla()
        self.add_labels_and_axes_styling()
        # Compute the mean of the non-None elements

        local_z = np.array(z.data.to_numpy(), copy=True)

        if not np.isnan(local_z).all():
            z_mean = np.mean(local_z[~np.isnan(local_z)])
            local_z[np.isnan(local_z)] = z_mean

        self.axes.imshow(
            local_z,
            cmap="Wistia",
            vmin=np.min(local_z),
            vmax=np.max(local_z),
            extent=[z.x_min, z.x_max, z.y_min, z.y_max],
            interpolation="none",
            origin="lower",
        )

        self.axes.set_xlim([z.x_min, z.x_max])
        self.axes.set_ylim([z.y_min, z.y_max])

        self.show()
        # self.axes.legend(loc="upper right", fancybox=True)

    def update_from_vna_scan(self, z, part):
        self.axes.cla()
        self.add_labels_and_axes_styling()
        # Compute the mean of the non-None elements
        if part == "real":
            local_z = np.array(z.data.to_numpy().real, copy=True)
        elif part == "imag":
            local_z = np.array(z.data.to_numpy().imag, copy=True)
        else:
            raise ValueError(f"part should be one of: [real, imag], not:'{part}'")

        if not np.isnan(local_z).all():
            z_mean = np.mean(local_z[~np.isnan(local_z)])
            local_z[np.isnan(local_z)] = z_mean

        self.axes.imshow(
            local_z,
            cmap="Wistia",
            vmin=np.min(local_z),
            vmax=np.max(local_z),
            extent=[z.x_min, z.x_max, z.y_min, z.y_max],
            interpolation="none",
            origin="lower",
        )

        self.axes.set_xlim([z.x_min, z.x_max])
        self.axes.set_ylim([z.y_min, z.y_max])

        self.show()
        # self.axes.legend(loc="upper right", fancybox=True)

    def update_from_numpy_array(self, z):
        self.axes.cla()
        self.add_labels_and_axes_styling()
        # Compute the mean of the non-None elements

        local_z = np.array(z, copy=True)

        if not np.isnan(local_z).all():
            z_mean = np.mean(local_z[~np.isnan(local_z)])
            local_z[np.isnan(local_z)] = z_mean

        x_min = 0
        y_min = 0
        x_max = 50
        y_max = 50

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
