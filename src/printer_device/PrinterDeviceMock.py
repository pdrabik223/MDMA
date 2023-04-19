import time

from printer_device.PrinterDevice import PrinterDevice


class PrinterDeviceMock(PrinterDevice):
    def send_and_await(self, command: str) -> str:
        if "F" not in command:
            command += f" F {self.speed}"

        if command[-1] != "\n":
            command += "\n"

        if "G1" in command:
            self.set_current_position_from_string(command)
            time.sleep(0.5)

        elif "G28" in command:
            self.current_position.from_tuple((0, 0, 0))
            time.sleep(1)

        return "this is mock"

    @staticmethod
    def connect_on_port(
        port: str, baudrate: int = 250000, timeout: int = 5
    ) -> "PrinterDeviceMock":
        print("Connected on port: 'mock', desc: 'table', hwid: 'kazooooo")
        return PrinterDeviceMock()

    @staticmethod
    def connect() -> "PrinterDeviceMock":
        print("Connected on port: 'mock', desc: 'table', hwid: 'kazooooo")
        return PrinterDeviceMock()

    def startup_procedure(self) -> None:
        pass
