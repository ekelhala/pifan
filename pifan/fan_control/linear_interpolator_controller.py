from pifan.fan_control.base_controller import BaseController

class LinearInterpolatorController(BaseController):

    def get_speed(self, system_temperature):
        return super().get_speed(system_temperature)
