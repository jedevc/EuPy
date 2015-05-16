from . import connection as cn

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
        self.connection.add_callback(cn.PTYPE["EVENT"]["NICK"],
                                     self.handle_user)
        
        self.people = dict()

    def handle_message(self, data):
        """
        handle_message(data) -> None

        Simply extracts the message data and passes it on to handle_chat()
        """

        self.handle_chat(data["data"])
        
    def handle_user(self, data):
        """
        handle_user(data) -> None
        
        Add and remove users from self.people.
        """
        
        info = data["data"]
        
        if info["from"] in self.people:
            self.people.pop(info["from"])
            
        self.people[info["to"]] = None
        
    def handle_who(self, data):
        """
        handle_who(data) -> None
        
        Update the list of who is in the room.
        """
        
        self.people = dict()
        
        for user in data["data"]["listing"]:
            self.people[user["name"]] = None

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
                                    cn.build_json(content=message, parent=parent))
        
    def ready(self):
        self.connection.send_packet(cn.PTYPE["CLIENT"]["WHO"], "",
                                    self.handle_who)