import json
import socket

class Client:

    def __init__(self, socket_path: str = "/run/pifan.sock"):
        """
        Initialize and connect the client
        """
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.socket.connect(socket_path)

    def _print_error(self, message: str):
        print(f"[client] Error: {message}")

    def send_command(self, command: str) -> dict|None:
        try:
            self.socket.sendall(json.dumps({"command": command}).encode("utf-8"))
            response = self.socket.recv(4096).decode("utf-8")
            response_dict = json.loads(response)
            if response_dict["status"] == "error":
                self._print_error(response_dict)
                return None
            return response_dict
        except Exception as e:
            self._print_error(f"Error when processing command: {e}")
            return None
    
    def destroy(self):
        self.socket.shutdown()
        self.socket.close()