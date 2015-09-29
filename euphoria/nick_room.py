from . import connection

from . import room

class NickRoom(room.Room):
    """
    A nick room allows a user to quickly change names.
    """

    def __init__(self, roomname, password=None, attempts=None):
        super().__init__(roomname, password, attempts)

    def change_nick(self, nick):
        """
        change_nick(nick) -> None

        Change your username to a different one.
        """

        self.connection.send_packet("nick", connection.build_json(name=nick), self.handle_nickreply)

    def handle_nickreply(self, data):
        """
        handle_nickreply(data) -> None

        Handle a callback so that the nickname is only changed once you have
        received confirmation from the server.
        """

        if data["data"] is not None:
            self.nickname = data["data"]["to"]
