from . import connection as cn

from . import component

import time

class PingComponent(component.Component):
    """
    A ping component is added to a room to maintain a connection.
    """

    def __init__(self, owner):
        super().__init__(owner)

        self.owner.connection.add_callback(cn.PTYPE["EVENT"]["PING"],
                                    self.handle_ping)

    def handle_ping(self, packet):
        """
        handle_ping(packet) -> None

        The method sends a ping packet off to the server to maintain the
        connection.
        """

        self.owner.connection.send_packet(cn.PTYPE["CLIENT"]["PING"],
                                    cn.build_json(time=int(time.time())))