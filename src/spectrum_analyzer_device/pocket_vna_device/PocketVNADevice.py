import random

from spectrum_analyzer_device.pocket_vna_device.pocketvnaAPI.pocketvna import pocketvna


# from pocket_vna_device.pocketvnaAPI.pocketvna import *


def close():
    pocketvna.close_api()


class PocketVnaDevice:
    def __init__(self):
        print(f"pocketvnaAPI Version: {pocketvna.driver_version()}")
        self.driver = pocketvna.Driver()
        print("")
        print("List all available self.drivers:")
        for i in range(0, self.driver.count()):
            print("Device {}".format(i))
            print("\t {}".format(self.driver.info_at(i)))

        self.driver.connect_to_first(pocketvna.ConnectionInterfaceCode.CIface_HID)
        print("")
        print(f"Connected to Pocket VNA: {self.driver.valid()}")
        if not self.driver.valid():
            raise Exception("Device not found")

    def get_level(
            self,
            frequency=int(1.32 * 10 ** 9),
            aggregate_samples=200,
            params=pocketvna.NetworkParams.ALL,
    ):
        return self.driver.single_scan(frequency, aggregate_samples, params)[0]

    def __del__(self):
        close()
