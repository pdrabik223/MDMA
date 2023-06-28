import math

import numpy as np
import pyqtgraph as pg

from mpl_toolkits.axes_grid1 import make_axes_locatable
from functionalities.Measurement import Measurement
from src.plot_widgets.PlotWidget import PlotType, PlotWidget
from PIL import Image


def phase(imag, real):
    math.atan(imag / real)


class Heatmap2DPhaseWidget(PlotWidget):
    def __init__(self, printer_path=None, title: str = None):
        super().__init__(plot_type=PlotType.Heatmap2D)
        self.title = title
        # create the color bar for the heatmap
        self.color_bar_widget = pg.GradientWidget(orientation="right")
        self.cax = None
        self.default_view()

    def default_view(self):
        self.axes.cla()
        self.add_labels_and_axes_styling()
        try:
            self.axes.imshow(
                np.asarray(Image.open("assets\\3d_fill_color.png")),
                cmap="Wistia",
                extent=[0, 512, 0, 512],
                interpolation="none",
                origin="upper",
            )

            self.axes.set_xlim([-10, 522])
            self.axes.set_ylim([-10, 522])
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

    def add_labels_and_axes_styling(self):
        self.axes_styling("Extruder path")
        self.axes.set_xlabel("X [mm]")
        self.axes.set_ylabel("Y [mm]")
        self.axes.set_title(self.title)

    def update_from_vna_scan(self, z):
        self.axes.cla()
        self.add_labels_and_axes_styling()
        # Compute the mean of the non-None elements

        real_part = np.array(z.data.to_numpy().real)
        imag_part = np.array(z.data.to_numpy().imag)



        # TODO: Make sure which function to use
        phase = np.arctan(real_part / imag_part)

        # if not np.isnan(phase).all():
        #     z_mean = np.mean(real_part[~np.isnan(real_part)])
        #     real_part[np.isnan(real_part)] = z_mean

        self.im = self.axes.imshow(
            phase,
            cmap="Wistia",
            vmin=np.min(phase),
            vmax=np.max(phase),
            extent=[z.x_min, z.x_max, z.y_min, z.y_max],
            interpolation="none",
            origin="lower",
        )

        if self.cax is not None:
            self.cax.remove()

        self.divider = make_axes_locatable(self.axes)
        self.cax = self.divider.append_axes("right", size="5%", pad=0.05)
        self.color_bar = self.fig.colorbar(self.im, cax=self.cax, orientation="vertical")

        self.axes.set_xlim([z.x_min, z.x_max])
        self.axes.set_ylim([z.y_min, z.y_max])

        self.show()
        # self.axes.legend(loc="upper right", fancybox=True)
