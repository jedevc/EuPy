from . import connection as cn
from . import exception

import time

class Room:
    """
    A room object that simply holds components and a connection.
    """

    def __init__(self, roomname, password=None):
        self.connection = cn.Connection()

        self.roomname = roomname
        self.password = password
    
        self.nickname = "Default"

        self.components = []
        
    def add_component(self, comp):
        """
        add_component(comp) -> None
        
        Add a component to the list of components.
        """
        
        self.components.append(comp)

    def join(self, nick=None):
        """
        join(nick) -> None

        Connects to the room and submits the password if there is one.
        It then sends its nick over.
        """

        if nick is not None:
            self.nickname = nick

        self.connection.connect(self.roomname)
        
        self.connection.send_packet(cn.PTYPE["CLIENT"]["AUTH"],
                                    cn.build_json(passcode=self.password))

        self.connection.send_packet(cn.PTYPE["CLIENT"]["NICK"],
                                    cn.build_json(name=self.nickname))

    def ready(self):
        """
        ready() -> None
        
        Do last minute setup for the room.
        """
        
        for i in self.components:
            i.ready()

    def run(self, nick=None):
        """
        run() -> None

        Run the room.
        """
        
        if nick is not None:
            self.nickname = nick
        
        while 1:
            try:
                self.connection.receive_data()
            except exception.EuphoriaNoConnection:
                #No connection previously initialized
                self.join()
                self.ready()
            except exception.EuphoriaConnectionLost:
                #An error from something
                time.sleep(5)
                self.join()
                self.ready()
            except KeyboardInterrupt:
                #User halt
                self.connection.close()
                break