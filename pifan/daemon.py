import time
from gpiozero import PWMOutputDevice

from pifan.fan_control.get_controller import get_controller
from pifan.fan_control.base_controller import ControllerOptions

from pifan.config import config_loader

TEMP_SENSOR_PATH = "/sys/class/thermal/thermal_zone0/temp"

def get_temp() -> float:
    """
    Reads the temperature from the provided TEMP_SENSOR_PATH
    """
    with open(TEMP_SENSOR_PATH, "r") as sensor:
        temp_str = sensor.read()
    return int(temp_str) / 1000

def run():
    config = config_loader.load_config()
    controller_options = ControllerOptions(config["fan"]["temp_high"], config["fan"]["temp_low"])
    controller = get_controller(config["fan"]["controller"], controller_options)
    fan = PWMOutputDevice(config["fan"]["gpio_pin"])
    while True:
        try:
            temp = get_temp()
            value = controller.get_speed(temp)
            print(f"current temp:", temp)
            print(f"current speed {value}")
            fan.value = value
            time.sleep(config["daemon"]["update_interval"])
        except KeyboardInterrupt:
            print("stopping pifan daemon...")
            fan.value = 0.0
            break


if __name__=="__main__":
    run()