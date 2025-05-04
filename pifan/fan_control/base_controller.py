
class BaseController():
    """
    Base class for fan controllers
    """

    def __init__(self, options: dict):
        """
        Create a new fan controller with the given options.
        The options-dictionary MUST contain the following contents:
        
        ```
        {
           "temp_high": float,
           "temp_low": float
        }
        ```
        """
        self.options = options

    def get_speed(self, system_temperature: float) -> float:
        """
        Calculate current fan speed based on given temperature and options
        """