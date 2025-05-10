"""
A server component for the daemon that listens for incoming connections on Unix socket.
Useful for querying information and making configuration changes on the fly.
"""
import os
import socket
import threading

class SocketServer:

    def __init__(self, daemon, socket_path: str = "/run/pifan.sock"):
        self.socket_path = socket_path
        self.daemon = daemon

    def _log_message(self, message):
        print(f"[socket_server] {message}")

    def _handle_connections(self):
        """
        Handle client connection on the socket
        """
        while True:
            connection, _ = self.server.accept()
            with connection:
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
        self._log_message(f"started, listening on socket {self.socket_path}")

    def stop(self):
        """
        Stop socket server
        """
        if self.thread:
            self.thread.join()
            self._log_message("socket server exiting now")
