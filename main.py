import time
from gpiozero import PWMOutputDevice

PWM_PIN = "GPIO12"
TEMP_SENSOR_PATH = "/sys/class/thermal/thermal_zone0/temp"
UPDATE_INTERVAL = 5
OPTIONS = {
    "temp_low": 45.0,
    "temp_high": 80.0,
    "gpio_pin": "GPIO12"
}

fan = PWMOutputDevice(OPTIONS["gpio_pin"])

def get_cpu_temp() -> float:
    """
    Reads the CPU temperature from the provided TEMP_SENSOR_PATH
    """
    with open(TEMP_SENSOR_PATH, "r") as sensor:
        temp_str = sensor.read()
    return int(temp_str) / 1000

def calculate_speed(cpu_temp: float) -> float:
    """
    Calculates the speed for the fan, given the current CPU temperature
    """
    if cpu_temp < OPTIONS["temp_low"]:
        return 0.0
    else:
        # return a value between 0.3 and 1.0 based on linear interpolation
        return 0.3 + (cpu_temp - OPTIONS["temp_low"]) * (1.0 - 0.3) / (OPTIONS["temp_high"] - OPTIONS["temp_low"])

def run():
    # just a demo, start from 0.0, increment and decrement
    # values between 0.0 and 0.3 don't do anything to the fan
    while True:
        cpu_temp = get_cpu_temp()
        value = calculate_speed(cpu_temp)
        print(f"current temp:", get_cpu_temp())
        print(f"current speed {value}")
        fan.value = value
        time.sleep(UPDATE_INTERVAL)

if __name__=="__main__":
    try:
        run()
    except KeyboardInterrupt:
        fan.value = 0.0