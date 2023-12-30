"""
Printer handling class for purposes of investigation, later this will be merged with ui 
"""

from ast import Tuple
import time
import comm
import serial.tools.list_ports
from serial import Serial, SerialException
from typing import Optional

from pydantic import ValidationError, validate_call


def list_ports() -> list:
    print("List all available ports:")
    for port, desc, hwid in sorted(serial.tools.list_ports.comports()):
        print(f"\t port: '{port}', desc: '{desc}', hwid: '{hwid}")
    return sorted(serial.tools.list_ports.comports())


class GCodeCommands:
    @staticmethod
    def G28() -> str:
        return "G28\n"

    @staticmethod
    @validate_call
    def G1(
        x: Optional[float] = None, y: Optional[float] = None, z: Optional[float] = None, f: Optional[float] = None
    ) -> str:
        if not any([x is None, y is None, z is None]):
            print("Invalid G code command, none parameters were provided")

        command = "G1"
        if x is not None:
            command += f"X{x}"

        if y is not None:
            command += f"Y{y}"

        if z is not None:
            command += f"Z{z}"

        return command + "\n"

    @staticmethod
    def M400():
        return "M400\n"


class AnycubicPrinter:
    def __init__(self, device: Serial):
        self._line_counter = 0
        self._serial_device = device

    def __del__(self):
        self._serial_device.close()

    @staticmethod
    def _checksum(line: str) -> int:
        cs = 0
        for i in range(0, len(line)):
            cs ^= ord(line[i]) & 0xFF
        cs &= 0xFF
        return cs

    @staticmethod
    def _cs_line(line: str) -> str:
        return line + "*" + str(AnycubicPrinter._checksum(line))

    def _no_line(self, line: str) -> str:
        self._line_counter += 1
        return f"N{self._line_counter} " + line + f" N{self._line_counter}"

    @staticmethod
    def connect(port: str, baudrate: int = 250000, timeout: int = 1) -> "AnycubicPrinter":
        device: Serial = Serial(port=str(port), baudrate=baudrate, timeout=timeout)

        resp = "start"

        while resp != "":
            resp = device.readline().decode("utf-8")
            if resp != "":
                print(resp.strip())
            else:
                break
            time.sleep(0.5)

        return AnycubicPrinter(device)

    @staticmethod
    def auto_connect() -> "AnycubicPrinter":
        list_of_available_ports = sorted(serial.tools.list_ports.comports())

        # anycubic printers have a specific device description
        # something like:
        #   'Silicon Labs CP210x USB to UART Bridge (COM5)'
        # for now we will live with assumption that it never changes
        print(list_of_available_ports)
        anycubic_printers = [device for device in list_of_available_ports if "Silicon Labs" in device[1]]
        if len(anycubic_printers) == 0:
            raise RuntimeError("No printer is currently connected")

        first_printer = anycubic_printers[0]

        return AnycubicPrinter.connect(first_printer[0])

    def send(self, command: str, timeout: float = 60.0) -> tuple:
        
        command = command.strip()
        command = self._no_line(command)
        command = AnycubicPrinter._cs_line(command)

        print("_line_counter: ", self._line_counter)

        if command[-1] != "\n":
            command += "\n"

        print(f"req:\t'{command}'")
        self._serial_device.write(bytearray(command, "ascii"))

        # wait for 'ok' response

        resp = []
        for i in range(int(timeout // 0.2)):
            time.sleep(0.2)
            resp.append(self._serial_device.readline().decode("utf-8").strip())

            if len(resp) != 0:
                print(f"\t{i} resp:\t'{resp[-1]}'")

            if resp[-1] == "ok":
                return True, resp

        return (False, [])

    def send_and_await(self, command: str, timeout: float = 60.0):
        response = self.send(command, timeout)
        self.send(GCodeCommands.M400())
        return response


if __name__ == "__main__":
    printer = AnycubicPrinter.auto_connect()
    printer.send_and_await(GCodeCommands.G28())
