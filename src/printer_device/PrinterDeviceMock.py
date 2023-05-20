import time

from src.printer_device.PrinterDevice import PrinterDevice


class PrinterDeviceMock(PrinterDevice):
    def send_and_await(self, command: str) -> str:
        if "F" not in command:
            command += f" F {self.speed}"

        if "G1" in command:
            new_position = PrinterDevice.parse_move_command_to_position(command)
            if new_position is not None:
                if new_position[0] < 0 or new_position[0] > self.x_size:
                    return "error"
                if new_position[1] < 0 or new_position[1] > self.y_size:
                    return "error"
                if new_position[2] < 0 or new_position[2] > self.z_size:
                    return "error"

        if command[-1] != "\n":
            command += "\n"

        if "G1" in command:
            self.set_current_position_from_string(command)
            print(f"Move to new position: {command}")
            time.sleep(0.5)

        elif "G28" in command:
            self.current_position.x = 0
            self.current_position.y = 0
            self.current_position.z = 0
            print("Home all Axis")
            time.sleep(1)

        return "this is mock"

    @staticmethod
    def connect_on_port(port: str, baudrate: int = 250000, timeout: int = 5) -> "PrinterDeviceMock":
        print("Connected on port: 'mock', desc: 'table', hwid: 'kazooooo")
        return PrinterDeviceMock()

    @staticmethod
    def connect() -> "PrinterDeviceMock":
        print("Connected on port: 'mock', desc: 'table', hwid: 'kazooooo")
        return PrinterDeviceMock()

    def startup_procedure(self) -> None:
        raise NotImplementedError()
