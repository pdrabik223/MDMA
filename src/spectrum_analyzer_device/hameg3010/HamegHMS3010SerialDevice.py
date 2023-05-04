import logging
from time import sleep
from typing import Tuple

import logging
import time
from typing import Optional, Tuple

import serial.tools.list_ports
from serial import Serial, SerialException


class HamegHMS3010DeviceSerial:
    def __init__(self, device: Serial) -> None:
        self.device_handle = device
        # self.device_handle.set_configuration()

    @staticmethod
    def automatically_connect():

        baudrate: int = 250000
        timeout: int = 1
        device: Optional[Serial] = None
        available_ports = serial.tools.list_ports.comports()

        for port, desc, hwid in sorted(available_ports):
            print(f"Connected connecting to:\n\t port: '{port}', desc: '{desc}', hwid: '{hwid}")

            if 'HAMEG HO720 USB Serial Port (VCP)' in desc:
                try:
                    device: Serial = Serial(port=str(port), baudrate=baudrate, timeout=timeout)
                    print("Serial port is Open'")
                    resp: bytes = device.readline()
                    print(f"Answer: '{resp}'")

                    print(f"Connected on port: '{port}', desc: '{desc}', hwid: '{hwid}")
                    logging.info(f"Connected on port: '{port}', desc: '{desc}', hwid: '{hwid}")
                    break

                except SerialException:
                    device = None
                    continue

        if device is None:
            raise SerialException("Device not found")

        return HamegHMS3010DeviceSerial(device)

    def get_level(
            self,
            frequency: int,
            measurement_time: int = 1,
    ) -> float:
        self.send_await_resp(f"rmode:mtime {measurement_time}")
        self.send_await_resp(f"rmode:frequency {frequency}")
        self.send_await_resp(f"trigger:software")

        sleep(measurement_time + 0.4)

        _, level_raw = self.send_await_resp("rmode:level?")

        level_raw = level_raw[2:-1]  # TODO this line might be unnecessary

        level = level_raw[level_raw.find(",") + 1:]

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
            self.device_handle.write(bytearray(command, "ascii"))
        except Exception:
            logging.error("error occurred while writing to device", exc_info=True)
            raise

    def _await_resp(self):
        for _ in range(10):
            resp: bytes = self.device_handle.readline()
            if len(resp) != 2:
                print(resp)
                return resp, bytearray(resp).decode("utf-8")
        return None, None

    def send_await_resp(self, cmd: str) -> tuple[bytes, str] | tuple[None, None]:
        self._send_str(command=cmd)
        return self._await_resp()

    def is_set_up(self):
        raise NotImplementedError()

    def close(self):
        # this should be closed but idunno
        pass
