from . import connection

from . import room

class ChatRoom(room.Room):
    """
    A chat room allows you to talk and process chats from the room.
    """

    def __init__(self, roomname, password=None, attempts=None):
        super().__init__(roomname, password, attempts)

        self.connection.add_callback("send-event", self.handle_message)

    def handle_message(self, message):
        """
        handle_message(message) -> None

        Pipes the message onto handle_chat()
        """

        self.handle_chat(message["data"])

    def handle_chat(self, message):
        """
        handle_chat(message) -> None

        Override this method to handle chats.
        """

        pass

    def send_chat(self, message, parent=""):
        """
        send_chat(message, parent="") -> None

        Send a message out to the world!
        """

        if message is not None:
            self.connection.send_packet("send",
                        connection.build_json(content=message, parent=parent))
