from . import connection

from . import room

import time

class PingRoom(room.Room):
    """
    A ping room maintains a connection with the server.
    """

    def __init__(self, roomname, password=None, attempts=None):
        super().__init__(roomname, password, attempts)

        self.connection.add_callback("ping-event", self.handle_ping)

    def handle_ping(self, packet):
        """
        handle_ping(packet) -> None

        The method sends a ping packet off to the server to maintain the
        connection.
        """

        self.connection.send_packet("ping-reply", connection.build_json(time=int(time.time())))
