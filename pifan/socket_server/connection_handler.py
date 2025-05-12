import socket
from threading import Event
import json

class ConnectionHandler:

    def __init__(self, server_socket: socket.socket, stop_event: Event):
        self.server_socket = server_socket
        self.stop_event = stop_event

    def _log_message(self, message):
        print(f"[socket_server] {message}")

    def _ok_response(self, data: dict):
        return {
            "status": "ok",
            "data": data
        }
    
    def _error_response(self, message: str):
        return {
            "status": "error",
            "message": message
        }

    def handle_connection(self):
        """
        Handle connections to server_socket
        """
        while not self.stop_event.is_set():
            connection, _ = self.server_socket.accept()
            with connection:
                try:
                    data = connection.recv(1024).decode()
                    request = json.loads(data)

                    match request["command"]:
                        case "get_speed":
                            response = self._ok_response({"fan_speed": self.daemon.fan_speed})
                        case "get_status":
                            response = self._ok_response(self.daemon.get_status())
                        case "get_config":
                            response = self._ok_response(self.daemon.get_config())
                        case "set_controller":
                            if self.daemon.set_controller(request["controller_name"]):
                                response = self._ok_response({"message": "controller set"})
                            else:
                                response = self._error_response(f"invalid controller {request['controller_name']}")
                        case _:
                            response = self._error_response("unknown command")

                    connection.sendall(json.dumps(response).encode("utf-8"))
                except json.JSONDecodeError:
                    self._log_message("error decoding client message")
                    connection.sendall(json.dumps({"status":"error", "message": "JSON decode error"}).encode("utf-8"))                    
                except Exception:
                    connection.sendall(json.dumps({"status":"error", "message": "unknown error"}).encode("utf-8"))
        connection.close()
