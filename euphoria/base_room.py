from . import connection as cn

import time

class BaseRoom:
    """
    A room object that simply connects to a room and handles pings from the
    server.
    """

    def __init__(self, roomname, password=None):
        self.connection = cn.Connection()

        self.roomname = roomname
        self.password = password
    
        self.nickname = None

        self.connection.add_callback(cn.PTYPE["EVENT"]["PING"],
                                    self.handle_ping)

    def handle_ping(self, packet):
        """
        handle_ping(packet) -> None

        This method is added as a callback to handling pings. It should not
        be called directly.

        The method sends a ping packet off to the server to maintain the
        connection.
        """

        self.connection.send_packet(cn.PTYPE["CLIENT"]["PING"],
                                    cn.build_json(time=int(time.time())))

    def join(self, nick):
        """
        join(nick) -> None

        Connects to the room and submits the password if there is one.
        It then sends its nick over.
        """

        self.nickname = nick

        self.connection.connect(self.roomname)
        self.connection.send_packet(cn.PTYPE["CLIENT"]["AUTH"],
                                    cn.build_json(passcode=self.password))

        self.connection.send_packet(cn.PTYPE["CLIENT"]["NICK"],
                                    cn.build_json(name=nick))

    def ready(self):
        """
        ready() -> None
        
        Do last minute setup.
        """
        
        pass

    def run(self):
        """
        run() -> None

        Run the room.
        """
        while 1:
            self.connection.receive_data()
            time.sleep(0.2)