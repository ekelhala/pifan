"""
A server component for the daemon that listens for incoming connections on Unix socket.
Useful for querying information and making configuration changes on the fly.
"""
import os
import socket
import threading

from pifan.daemon import Daemon
from pifan.socket_server.connection_handler import ConnectionHandler

class SocketServer:

    def __init__(self, daemon: Daemon, socket_path: str = "/run/pifan.sock"):
        self.socket_path = socket_path
        self.daemon = daemon
        self.stop_event = threading.Event()

    def _log_message(self, message):
        print(f"[socket_server] {message}")

    def start(self):
        """
        Start the socket server
        """
        if os.path.exists(self.socket_path):
            os.remove(self.socket_path)
        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server.bind(self.socket_path)
        server.listen(1)
        connection_handler = ConnectionHandler(server, self.stop_event)
        self.thread = threading.Thread(target=connection_handler.handle_connection, daemon=True)
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
