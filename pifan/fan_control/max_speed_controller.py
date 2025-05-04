"""
A controller that drives the fan at max speed at all times
"""
from pifan.fan_control.base_controller import BaseController

class MaxSpeedController(BaseController):
    
    def get_speed(self, _system_temperature: float) -> float:
        return 1.0