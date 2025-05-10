from pifan.socket_server import SocketServer
from pifan.daemon import Daemon

def start():
    daemon = Daemon()
    server = SocketServer(daemon)
    server.start()
    daemon.run()
