"""
A server component for the daemon that listens for incoming connections on Unix socket.
Useful for querying information and making configuration changes on the fly.
"""
import os
import socket
import threading
import json

from pifan.daemon import Daemon

class SocketServer:

    def __init__(self, daemon: Daemon, socket_path: str = "/tmp/pifan.sock"):
        self.socket_path = socket_path
        self.daemon = daemon
        self.stop_event = threading.Event()

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

    def _handle_connections(self):
        """
        Handle client connection on the socket
        """
        while not self.stop_event.is_set():
            connection, _ = self.server.accept()
            with connection:
                try:
                    data = connection.recv(1024).decode()
                    request = json.loads(data)

                    match request["command"]:
                        case "get_speed":
                            response = self._ok_response({"fan_speed": self.daemon.fan_speed})
                        case "get_status":
                            response = self._ok_response({"status": self.daemon.get_status()})
                        case "get_config":
                            response = self._ok_response({"config": self.daemon.get_config()})
                        case _:
                            response = self._error_response("unknown command")

                    connection.sendall(json.dumps(response).encode("utf-8"))
                except json.JSONDecodeError:
                    self._log_message("error decoding client message")
                    connection.sendall(json.dumps({"status":"error", "message": "JSON decode error"}).encode("utf-8"))                    
                except Exception:
                    connection.sendall(json.dumps({"status":"error", "message": "unknown error"}).encode("utf-8"))
        connection.close()

    def start(self):
        """
        Start the socket server
        """
        if os.path.exists(self.socket_path):
            os.remove(self.socket_path)
        self.server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.server.bind(self.socket_path)
        self.server.listen(1)
        self.thread = threading.Thread(target=self._handle_connections, daemon=True)
        self.thread.start()
        self._log_message(f"server started, listening on socket {self.socket_path}")

    def stop(self):
        """
        Stop socket server
        """
        if self.thread:
            self.stop_event.set()
            if os.path.exists(self.socket_path):
                os.remove(self.socket_path)
            self._log_message("socket server exiting now")
