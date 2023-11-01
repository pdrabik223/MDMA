from spectrum_analyzer_device.pocket_vna_device.pocketvnaAPI.pocketvna import (
    ConnectionInterfaceCode,
    Driver,
    NetworkParams,
    driver_version,
)


class PocketVnaDevice:
    def __init__(self):
        print(f"pocketvnaAPI Version: {driver_version()}")
        self.driver = Driver()
        self.driver.connect_to_first(ConnectionInterfaceCode.CIface_HID)
        
        if not self.driver.valid():
            raise Exception("Device not found")

    def close(self):
        self.driver.close()

    def get_level(
        self,
        frequency=int(1.32 * 10**9),
        aggregate_samples=200,
        params=NetworkParams.S11,
    ):
        frequency = int(frequency)
        aggregate_samples = int(aggregate_samples)
        return self.driver.single_scan(frequency, aggregate_samples, params)[0]

    @staticmethod
    def automatically_connect():
        return PocketVnaDevice()
