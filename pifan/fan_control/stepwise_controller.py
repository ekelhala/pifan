from pifan.fan_control.base_controller import BaseController

class StepwiseController(BaseController):
    """
    This controller adjusts the speed of the fan in steps when it is between temp_low and temp_high
    The steps used:
    lower than temp_low or < 29% of temp_high-temp_low -> 0% speed
    30-59% of temp_high-temp_low -> 30% speed
    60-90% of temp_high-temp_low -> 60% speed
    over 90% temp_high-temp_low -> 100% speed
    """

    def get_speed(self, system_temperature):
        if system_temperature <= self.options.temp_low:
            return 0.0
        temp_pct = round((system_temperature - self.options.temp_low) / (self.options.temp_high - self.options.temp_low), 2)
        if temp_pct < 0.3:
            return 0.0
        elif temp_pct < 0.6:
            return 0.3
        elif temp_pct < 0.9:
            return 0.6
        return 1.0

    def get_name(self):
        return "stepwise"
