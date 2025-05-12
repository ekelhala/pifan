import socket
from threading import Event
import json

from pifan.socket_server.logger import log_message
from pifan.socket_server.command_handler import CommandHandler
from pifan.daemon import Daemon

class ConnectionHandler:

    def __init__(self, server_socket: socket.socket, stop_event: Event, daemon: Daemon):
        self.server_socket = server_socket
        self.stop_event = stop_event
        self.command_handler = CommandHandler(daemon)

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
                    response = self.command_handler.handle_command(request)
                    connection.sendall(json.dumps(response).encode("utf-8"))
                except json.JSONDecodeError:
                    log_message("error decoding client message")
                    connection.sendall(json.dumps({"status":"error", "message": "JSON decode error"}).encode("utf-8"))                    
                except Exception:
                    connection.sendall(json.dumps({"status":"error", "message": "unknown error"}).encode("utf-8"))
        connection.close()
