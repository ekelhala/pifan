import sys

from pifan.socket_server.server import SocketServer
from pifan.daemon import Daemon

def start():
    daemon = Daemon()
    server = SocketServer(daemon)
    server.start()
    daemon.run()
    # if we get here, it means that daemon has stopped
    server.stop()
    sys.exit(0)
