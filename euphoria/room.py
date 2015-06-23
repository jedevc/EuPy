from . import connection as cn
from . import executable

import time

class Room(executable.Executable):
    """
    A base room object that simply holds a connection and simple methods for
    interfacing with the room.
    """

    def __init__(self, roomname, password=None, attempts=None):
        super().__init__()

        self.connection = cn.Connection()

        self.roomname = roomname
        self.password = password

        self.nickname = None

        self.attempts = attempts

    def join(self):
        """
        join() -> None

        Connects to the room and sends the passcode.
        """

        if self.connection is not None:
            self.connection.connect(self.roomname)

            if self.password is not None:
                self.connection.send_packet(cn.PTYPE["COMMAND"]["AUTH"],
                                            cn.build_json(passcode=self.password))

    def identify(self):
        """
        identify() -> None

        Identifies with the server according to the nickname.
        """

        if self.connection is not None:
            if self.nickname is not None:
                self.connection.send_packet(cn.PTYPE["COMMAND"]["NICK"],
                                            cn.build_json(name=self.nickname))

    def quit(self):
        """
        quit() -> None

        Performs neccessary cleanup for the connection.
        """

        self.cleanup()

        if self.connection is not None:
            self.connection.close()

        super().quit()

    def ready(self):
        """
        ready() -> None

        Overrideable function that is called every time the room is ready for
        transmitting information.
        """

        pass

    def cleanup(self):
        """
        cleanup() -> None

        Overrideable cleanup function that is called when the room is closing.
        """

        pass

    def run(self):
        """
        run() -> None

        Run the room.
        """

        super().run()

        first = True
        attempts = 0

        while self.running:
            #Check for multiple failures in a row
            if self.attempts is not None and attempts >= self.attempts:
                self.quit()
                break

            #Check if quit
            if not self.running:
                break

            #Receive data and handle connection errors
            try:
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
            except OSError:  #Catching some exception that occurs in single threading bots
                break
