"""
Controller that prioritizes silent operation - runs the fan at full speed when 
the temperature is within 10% of the 'high'-temperature
"""
from pifan.fan_control.base_controller import BaseController

class SilentController(BaseController):

    def get_speed(self, system_temperature):
        if system_temperature > self.options.temp_high * 0.9:
            return 1.0
        return 0.0