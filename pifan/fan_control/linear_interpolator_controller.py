from pifan.fan_control.base_controller import BaseController

class LinearInterpolatorController(BaseController):

    def get_speed(self, system_temperature: float) -> float:
        if system_temperature <= self.options["temp_low"]:
            return 0.0
        elif system_temperature >= self.options["temp_high"]:
            return 1.0
        else:
        # return a value between 0.3 and 1.0 based on linear interpolation
            return 0.3 + (system_temperature - self.options["temp_low"]) * (1.0 - 0.3) / (self.options["temp_high"] - self.options["temp_low"])

