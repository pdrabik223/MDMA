import random
import time
from typing import Any


class HamegHMS3010DeviceMock:
    def __init__(self) -> None:
        self.current_frequency = 1_000_000
        self.receiver_mode = "RMODE"

    @staticmethod
    def connect_using_vid_pid(id_vendor: int, id_product: int):
        print(f"Connected to mock device with pid: {id_product}, vid: {id_vendor}")
        return HamegHMS3010DeviceMock()

    @staticmethod
    def automatically_connect():
        return HamegHMS3010DeviceMock()

    def get_level(
            self,
            frequency: int,
            measurement_time: int = 1,
    ) -> float:
        time.sleep(0.5)
        measurement_value = -20 + (2 * ((random.random() * 2) - 1))
        return float(measurement_value)

    def send_await_resp(self, cmd: str) -> Any:
        cmd = cmd.casefold()
        if cmd == "*idn?":
            return (
                "1'HAMEG IDN 123324.1231",
                "1'Hameg 12.11 I need some C2H6O stat \n",
            )
        elif cmd == "system:software?":
            return "1'idk like 12", "1'idk like 12 i'm not good with numbers\n"
        elif cmd == "system:hardware?":
            return "1'idk like 12", "1'idk like 11 this thinking is killing me\n"
        elif cmd == "system:mode?":
            return f"1'{self.receiver_mode}", f"1'{self.receiver_mode}\n"
        elif cmd == "rmode:frequency?":
            return f"1'{self.current_frequency}", f"1'{self.current_frequency}\n"
        elif cmd == "rmode:level?":
            measurement_value = -20 + (2 * ((random.random() * 2) - 1))
            return (
                f"1'{self.current_frequency},{measurement_value}",
                f"1'{self.current_frequency},{measurement_value}\n",
            )
        elif "rmode:frequency" in cmd:
            self.current_frequency = float(cmd[15:])
        elif "system:mode" in cmd:
            self.receiver_mode = cmd[11:]
        return ("1'", "")

    def close(self):
        # this is mock device, it doesn't need to be deleted
        pass
