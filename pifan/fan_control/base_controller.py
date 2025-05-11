
class ControllerOptions:
    """
    Represents the controller configuration
    """

    def __init__(self, temp_high: float, temp_low: float):
        self.temp_low = temp_low
        self.temp_high = temp_high

class BaseController():
    """
    Base class for fan controllers
    """

    def __init__(self, options: ControllerOptions):
        """
        Create a new fan controller with the given options.
        """
        self.options = options

    def get_speed(self, system_temperature: float) -> float:
        """
        Calculate current fan speed based on given temperature and options
        """

    def get_name(self) -> str:
        """
        Return controller name as string
        """
