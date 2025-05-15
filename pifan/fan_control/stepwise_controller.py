from pifan.fan_control.base_controller import BaseController

class StepwiseController(BaseController):
    """
    This controller adjusts the speed of the fan in increasing steps based on temp_high
    The steps used:
    lower than temp_low or <= 29% of temp_high -> 0% speed
    30-59% of temp_high -> 30% speed
    60-90% of temp_high -> 60% speed
    over 90% temp_high -> 100% speed
    """

    def get_speed(self, system_temperature):
        temp_high_fraction = round(system_temperature / self.options.temp_high, 2)
        if system_temperature < self.options.temp_low or temp_high_fraction <= 0.29:
            return 0.0
        elif temp_high_fraction <= 0.59:
            return 0.3
        elif temp_high_fraction <= 0.90:
            return 0.6
        return 1.0

    def get_name(self):
        return "stepwise"
