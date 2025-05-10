from pifan.fan_control.base_controller import BaseController, ControllerOptions
from pifan.fan_control.linear_interpolator_controller import LinearInterpolatorController
from pifan.fan_control.max_speed_controller import MaxSpeedController
from pifan.fan_control.silent_controller import SilentController

def get_controller(controller_type: str,
                   controller_options: ControllerOptions) -> BaseController:
    
    match controller_type:
        case "linear_interpolator":
            controller = LinearInterpolatorController(controller_options)
        case "silent":
            controller = SilentController(controller_options)
        case _:
            controller = MaxSpeedController(controller_options)
    return controller