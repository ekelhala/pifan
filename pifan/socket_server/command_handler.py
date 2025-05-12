from pifan.daemon import Daemon
from pifan.socket_server.responses import ok_response, error_response

class CommandHandler:

    def __init__(self, daemon: Daemon):
        self.daemon = daemon

    def handle_command(self, request: dict[str, str]) -> dict[str]:
        match request["command"]:
            case "get_speed":
                return ok_response({"fan_speed": self.daemon.fan_speed})
            case "get_status":
                return self._ok_response(self.daemon.get_status())
            case "get_config":
                return self._ok_response(self.daemon.get_config())
            case "set_controller":
                if self.daemon.set_controller(request["controller_name"]):
                    return self._ok_response({"message": "controller set"})
                else:
                    return self._error_response(f"invalid controller {request['controller_name']}")
            case _:
                return self._error_response("unknown command")
