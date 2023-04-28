import logging
from time import sleep
from typing import Tuple

import usb.core
import usb.util


class Hameg3010Device:
    def __init__(self, device_handle: usb.core.Device) -> None:
        self.device_handle: usb.core.Device = device_handle
        self.device_handle.set_configuration()

    @staticmethod
    def connect_using_vid_pid(id_vendor: int, id_product: int) -> "Hameg3010Device":
        print(f"connecting do device with pid: {id_product}, vid: {id_vendor}")

        device = usb.core.find(idVendor=id_vendor, idProduct=id_product)

        if device is None:
            raise ValueError(f"Device is not found vid: {hex(id_vendor)} pid: {hex(id_product)}")

        logging.debug(f"connected do device with vid: {hex(id_vendor)} pid: {hex(id_product)}")
        return Hameg3010Device(device)

    @staticmethod
    def automatically_connect():
        # TODO this does nothing
        dev = usb.core.find(find_all=True)

        no_devices_found = 0
        for cfg in dev:
            no_devices_found += 1
            print(f"Decimal VendorID= {cfg.idVendor} ProductID= {cfg.idProduct}")
            print(f"Hexadecimal VendorID= {hex(cfg.idVendor)} ProductID= {hex(cfg.idProduct)}")
        print(f"no devices found: {no_devices_found}")
        return Hameg3010Device.connect_using_vid_pid(id_vendor=0x403, id_product=0xED72)

    def get_level(
        self,
        frequency: int,
        measurement_time: int = 1,
    ) -> float:
        self.send_await_resp(f"rmode:mtime {measurement_time}")
        self.send_await_resp(f"rmode:frequency {frequency}")

        sleep(measurement_time)

        _, level_raw = self.send_await_resp("rmode:level?")

        level_raw = level_raw[2:-1]  # TODO this line might be unnecessary

        level = level_raw[level_raw.find(",") + 1 :]

        return float(level)

    def _send_str(self, command: str):
        if not isinstance(command, str):
            raise TypeError(f"expected cmd to be str, received {type(command)}")

        if command is None or len(command) == 0:
            raise ValueError(f"cmd has to be not empty string, received: {command}")

        # commands send to device must end with terminal character
        if command[-1] != "\n":
            command += "\n"

        try:
            self.device_handle.write(0x2, command)
        except Exception:
            logging.error("error occurred while writing to device", exc_info=True)
            raise

    def _await_resp(self):
        # Following lines are hack
        # problem seems to be that after sending message multiple readout are required to get response
        # the delay between readouts is not important, can be as short as 0.1 s
        # seems like a problem with buffer somewhere, following while statement waits for non-empty readout
        # thus avoiding the issue, this will come back tho
        # TODO find the source of this problem

        for _ in range(10):
            resp = self.device_handle.read(0x81, 1_000_000, 1_000)
            if len(resp) != 2:
                print(resp)
                return resp, bytearray(resp).decode("utf-8")
        return None, None

    def send_await_resp(self, cmd: str) -> Tuple[bytearray, str]:
        self._send_str(command=cmd)
        return self._await_resp()

    def is_set_up(self):
        raise NotImplementedError()
