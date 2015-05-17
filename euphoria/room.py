from . import connection as cn

import time

class Room:
    """
    A room object that simply holds components and a connection.
    """

    def __init__(self, roomname, password=None):
        self.connection = cn.Connection()

        self.roomname = roomname
        self.password = password
    
        self.nickname = None

        self.components = dict()
        
    def add_component(self, name, comp):
        self.components[name] = comp

    def join(self, nick):
        """
        join(nick) -> Bool

        Connects to the room and submits the password if there is one.
        It then sends its nick over.
        """

        self.nickname = nick

        if not self.connection.connect(self.roomname):
            return False
        
        self.connection.send_packet(cn.PTYPE["CLIENT"]["AUTH"],
                                    cn.build_json(passcode=self.password))

        self.connection.send_packet(cn.PTYPE["CLIENT"]["NICK"],
                                    cn.build_json(name=nick))
        
        return True

    def ready(self):
        """
        ready() -> None
        
        Do last minute setup for the room.
        """
        
        for i in self.components:
            self.components[i].ready()

    def run(self):
        """
        run() -> None

        Run the room.
        """
        try:
            while 1:
                self.connection.receive_data()
        except KeyboardInterrupt:
            self.connection.close()