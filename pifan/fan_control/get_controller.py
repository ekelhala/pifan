from pifan.fan_control.base_controller import BaseController, ControllerOptions
from pifan.fan_control.linear_interpolator_controller import LinearInterpolatorController
from pifan.fan_control.max_speed_controller import MaxSpeedController
from pifan.fan_control.silent_controller import SilentController
from pifan.fan_control.stepwise_controller import StepwiseController

def get_controller(controller_type: str,
                   controller_options: ControllerOptions) -> BaseController:

    match controller_type:
        case "linear_interpolator":
            controller = LinearInterpolatorController(controller_options)
        case "silent":
            controller = SilentController(controller_options)
        case "max_speed":
            controller = MaxSpeedController(controller_options)
        case "stepwise":
            controller = StepwiseController(controller_options)
        case _:
            controller = None
    return controller
