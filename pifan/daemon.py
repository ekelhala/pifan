import time
from gpiozero import PWMOutputDevice

from pifan.fan_control.max_speed_controller import MaxSpeedController
from pifan.config import config_loader

TEMP_SENSOR_PATH = "/sys/class/thermal/thermal_zone0/temp"

OPTIONS = {
    "temp_low": 45.0,
    "temp_high": 80.0,
    "gpio_pin": "GPIO12",
    "update_interval": 5
}

fan = PWMOutputDevice(OPTIONS["gpio_pin"])

def get_temp() -> float:
    """
    Reads the temperature from the provided TEMP_SENSOR_PATH
    """
    with open(TEMP_SENSOR_PATH, "r") as sensor:
        temp_str = sensor.read()
    return int(temp_str) / 1000

def run():
    config = config_loader.load_config()
    controller = MaxSpeedController({
                                    "temp_high": config["fan"]["temp_high"],
                                    "temp_low": config["fan"]["temp_low"]
                                    })
    while True:
        temp = get_temp()
        value = controller.get_speed(temp)
        print(f"current temp:", temp)
        print(f"current speed {value}")
        fan.value = value
        time.sleep(config["daemon"]["update_interval"])

if __name__=="__main__":
    try:
        run()
    except KeyboardInterrupt:
        fan.value = 0.0