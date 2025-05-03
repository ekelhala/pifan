import time
from gpiozero import PWMOutputDevice

PWM_PIN = "GPIO12"
TEMP_SENSOR_PATH = "/sys/class/thermal/thermal_zone0/temp"
UPDATE_INTERVAL = 5

fan = PWMOutputDevice(PWM_PIN)

def get_cpu_temp():
    """
    Reads the CPU temperature from the provided TEMP_SENSOR_PATH
    """
    with open(TEMP_SENSOR_PATH, "r") as sensor:
        temp_str = sensor.read()
    return int(temp_str) / 1000

def run():
    # just a demo, start from 0.0, increment and decrement
    # values between 0.0 and 0.2 don't do anything to the fan
    value = 0.0
    while True:
        print(f"current temp:", get_cpu_temp())
        fan.value = value
        print(f"current speed {value}")
        if value < 1:
            value += 0.2
        else:
            value = 0.0
        time.sleep(UPDATE_INTERVAL)

if __name__=="__main__":
    try:
        run()
    except Exception:
        fan.value = 0.0