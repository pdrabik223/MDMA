import json
import os

import pandas as pd
from PyQt5.QtWidgets import QFileDialog

from Measurement import Measurement


def export_project(main_window_object):
    file_name = QFileDialog.getSaveFileName(
        main_window_object,
        "Export Project",
        os.getcwd(),
        "MDMA project(*.mdma)",
    )

    if file_name != "":
        directory_path, extention = file_name
        root_directory_path = directory_path.split(".")
        root_directory_path = ".".join(root_directory_path[:-1])

        os.mkdir(root_directory_path)

        data_path = os.path.join(root_directory_path, "data.mdma")
        main_window_object.measurement_data.to_pd_dataframe().to_csv(data_path)

        for plot in main_window_object.plots:
            fig_path = os.path.join(root_directory_path, plot["widget"].get_title() + ".png")
            plot["widget"].save_fig(fig_path)

        config_path = os.path.join(root_directory_path, "config.json")
        export_config_to_file(main_window_object, config_path)


def export_config_to_file(main_window_object, config_path):
    config_dict = {}
    config_dict.update({"spectrum_analyzer_controller": main_window_object.spectrum_analyzer_controller.get_state()})
    config_dict.update({"printer_controller": main_window_object.printer_controller.get_state()})
    config_dict.update({"scan_path_settings": main_window_object.scan_path_settings.get_state()})
    config_dict.update({"configuration_information": main_window_object.configuration_information.get_state()})

    with open(config_path, "w") as outfile:
        json.dump(config_dict, outfile)


def save_config(main_window_object):
    file_name = QFileDialog.getSaveFileName(
        main_window_object,
        "Save config",
        os.getcwd(),
        "JSON (*.json)",
    )
    if file_name[0] == "":
        return
    config_path = file_name[0]
    export_config_to_file(main_window_object, config_path)


def load_project(main_window_object):
    file_name = QFileDialog.getExistingDirectory(main_window_object, "Select directory")
    print(file_name)
    if file_name != "":
        directory_path = file_name
        data_path = os.path.join(directory_path, "data.mdma")
        config_path = os.path.join(directory_path, "config.json")
        try:
            data = pd.read_csv(data_path, index_col=0)

            main_window_object.measurement_data = Measurement.from_pd_dataframe(data)
            print(
                main_window_object.measurement_data.x_min(),
                main_window_object.measurement_data.x_max(),
                main_window_object.measurement_data.y_min(),
                main_window_object.measurement_data.y_max(),
            )

            main_window_object.plots[1]["widget"].update_from_scan(
                main_window_object.measurement_data.x_min(),
                main_window_object.measurement_data.x_max(),
                main_window_object.measurement_data.y_min(),
                main_window_object.measurement_data.y_max(),
                main_window_object.measurement_data,
            )
            main_window_object.plots[1]["widget"].show()

        except Exception as ex:
            print(str(ex))

        try:
            with open(config_path, "r") as outfile:
                config_dict = json.load(outfile)

                main_window_object.spectrum_analyzer_controller.set_state(config_dict["spectrum_analyzer_controller"])
                main_window_object.printer_controller.set_state(config_dict["printer_controller"])
                main_window_object.scan_path_settings.set_state(config_dict["scan_path_settings"])


        except Exception as ex:
            print(str(ex))

        main_window_object.recalculate_path()


def load_config(main_window_object):
    file_name = QFileDialog.getOpenFileName(
        main_window_object,
        "Load config",
        os.getcwd(),
        "JSON (*.json)",
    )
    if file_name[0] == "":
        return

    try:
        with open(file_name[0], "r") as outfile:
            config_dict = json.load(outfile)

            main_window_object.spectrum_analyzer_controller.set_state(config_dict["spectrum_analyzer_controller"])
            main_window_object.printer_controller.set_state(config_dict["printer_controller"])
            main_window_object.scan_path_settings.set_state(config_dict["scan_path_settings"])
            main_window_object.recalculate_path()

    except Exception as ex:
        print(str(ex))
