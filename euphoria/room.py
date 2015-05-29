from . import connection as cn

import time
import signal
import sys

class Room:
    """
    A base room object that simply holds components and a connection.
    """

    def __init__(self, roomname, password=None):
        self.connection = cn.Connection()

        self.roomname = roomname
        self.password = password
    
        self.nickname = None

    def join(self):
        """
        join() -> None
        
        Connects to the room and sends the passcode.
        """
        
        self.connection.connect(self.roomname)
        
        if self.password is not None:
            self.connection.send_packet(cn.PTYPE["CLIENT"]["AUTH"],
                                        cn.build_json(passcode=self.password))

    def identify(self):
        """
        identify() -> None

        Identifies with the server according to the nickname.
        """

        if self.nickname is not None:
            self.connection.send_packet(cn.PTYPE["CLIENT"]["NICK"],
                                        cn.build_json(name=self.nickname))

    def ready(self):
        """
        ready() -> None
        
        Do last minute setup for the room.
        """
        
        pass
            
    def quit(self):
        """
        quit() -> None
        
        Performs neccessary cleanup.
        """
            
        self.connection.close()
        
    def __sigterm_handler(self, signal, frame):
        """
        sigterm_handler(signal, frame) -> None
        
        Use to quit properly when there is a SIGTERM. NOT to be called directly.
        """

        self.quit()
        sys.exit()

    def run(self):
        """
        run() -> None

        Run the room.
        """
        
        first = True
        attempts = 0
        
        #Handle process kills.
        signal.signal(signal.SIGTERM, self.__sigterm_handler)
        
        while 1:
            try:
                #Check for multiple failures in a row
                if attempts >= 2:
                    self.quit()
                    return
                
                if self.connection.receive_data():
                    attempts = 0
                else:
                    #No connection initialized
                    if first:
                        first = False
                    else:
                        time.sleep(5)
                        attempts += 1
                        
                    self.join()
                    self.identify()
                    self.ready()
            except KeyboardInterrupt:
                #User halt
                self.quit()
                return