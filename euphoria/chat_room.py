import euphoria.connection as cn

from euphoria.base_room import BaseRoom

class ChatRoom(BaseRoom):
    """
    A room object that inherits from BaseRoom. It can handle and send chats
    to other people.
    """

    def __init__(self, roomname, password=None):
        super().__init__(roomname, password)

        self.connection.add_callback(cn.PTYPE["EVENT"]["SEND"],
                                    self.handle_message)

    def handle_message(self, data):
        """
        handle_message(data) -> None

        Simply extracts the message data and passes it on to handle_chat()
        """

        self.handle_chat(data["data"])

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

        self.connection.send_packet(cn.PTYPE["CLIENT"]["SEND"],
                                    {"content": message, "parent": parent})