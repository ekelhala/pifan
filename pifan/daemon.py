import time
import signal
from gpiozero import PWMOutputDevice

from pifan.fan_control.get_controller import get_controller
from pifan.fan_control.base_controller import ControllerOptions

from pifan.config import config_loader

class Daemon:

    def __init__(self):
        self.temp_sensor_path = "/sys/class/thermal/thermal_zone0/temp"
        self.fan_speed = 0.0

    def _log_message(self, message: str):
        print(f"[daemon] {message}")

    def get_temp(self) -> float:
        """
        Reads the temperature from the provided TEMP_SENSOR_PATH
        """
        with open(self.temp_sensor_path, "r") as sensor:
            temp_str = sensor.read()
        return int(temp_str) / 1000

    def _handle_sigterm(self, _signum, _frame):
        self._exit()

    def _exit(self):
        self._log_message("stopping daemon...")
        self.fan.value = 0.0

    def run(self):
        config = config_loader.load_config()
        controller_options = ControllerOptions(config["fan"]["temp_high"], config["fan"]["temp_low"])
        controller = get_controller(config["fan"]["controller"], controller_options)
        self.fan = PWMOutputDevice(pin=config["fan"]["gpio_pin"], 
                            frequency=config["fan"]["frequency"])
        signal.signal(signal.SIGTERM, self._handle_sigterm)
        self._log_message("fan daemon started")
        while True:
            try:
                temp = self.get_temp()
                self.fan_speed = round(controller.get_speed(temp), 2)
                self.fan.value = self.fan_speed
                time.sleep(config["daemon"]["update_interval"])
            except KeyboardInterrupt:
                self._exit()
                break
