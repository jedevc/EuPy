from . import connection as cn

from . import component

class ChatComponent(component.Component):
    """
    A chat component allows you to talk and process chats from the room.
    """

    def __init__(self, owner):
        super().__init__(owner)

        self.owner.connection.add_callback(cn.PTYPE["EVENT"]["SEND"],
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

        self.owner.connection.send_packet(cn.PTYPE["CLIENT"]["SEND"],
                                cn.build_json(content=message, parent=parent))