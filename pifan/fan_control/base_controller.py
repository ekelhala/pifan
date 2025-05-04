
class BaseController():
    """
    Base class for fan controllers
    """

    def __init__(self, options: dict):
        self.options = options

    def get_speed(self, system_temperature: float) -> float:
        """
        Calculate current fan speed based on given temperature and options
        """