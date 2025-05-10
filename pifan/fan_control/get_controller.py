from fan_control.base_controller import BaseController, ControllerOptions
from fan_control.linear_interpolator_controller import LinearInterpolatorController
from fan_control.max_speed_controller import MaxSpeedController

def get_controller(controller_type: str,
                   controller_options: ControllerOptions) -> BaseController:
    
    match controller_type:
        case "linear_interpolator":
            controller = LinearInterpolatorController(controller_options)
        case _:
            controller = MaxSpeedController(controller_options)
    return controller