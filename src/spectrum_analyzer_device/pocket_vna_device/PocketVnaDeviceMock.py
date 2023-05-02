import random

from spectrum_analyzer_device.pocket_vna_device.pocketvnaAPI.pocketvna import pocketvna


class PocketVnaDeviceMock:
    def __init__(self):
        print(f"pocketvnaAPI Version: (12 but I dont care, 3.141592653589793)")
        print("List all available self.drivers:\n\tmock driver")

        print("")
        print(f"Connected to Pocket VNA: Mock device")

    def get_level(
            self,
            frequency=2_280_000_000,
            aggregate_samples=100,
            params: pocketvna.NetworkParams = pocketvna.NetworkParams.ALL,
    ):
        import random
        # randomly generate the real part
        x = random.random()
        # randomly generate the imaginary part
        y = random.random()
        # resulting complex number
        return complex(x, y)
