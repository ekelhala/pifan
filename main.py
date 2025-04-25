import time
from gpiozero import GPIODevice

PWM_PIN = "GPIO12"
TEMP_SENSOR_PATH = "/sys/class/thermal/thermal_zone0/temp"
UPDATE_INTERVAL = 5

fan = GPIODevice(PWM_PIN)

def get_cpu_temp():
    """
    Reads the CPU temperature from the provided TEMP_SENSOR_PATH
    """
    with open(TEMP_SENSOR_PATH, "r") as sensor:
        temp_str = sensor.read()
    return int(temp_str) / 1000

def run():
    # just a demo, start from 0, increment and decrement
    value = True
    while True:
        print(f"current temp:", get_cpu_temp())
        fan.value = value
        value = not value
        time.sleep(UPDATE_INTERVAL)

if __name__=="__main__":
    try:
        run()
    except KeyboardInterrupt:
        fan.value = 0