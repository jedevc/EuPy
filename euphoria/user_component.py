from . import connection as cn

from . import component

class UserComponent(component.Component):
    """
    A user component contains a list of all the current users in the room.
    """

    def __init__(self, owner):
        super().__init__(owner)

        self.owner.connection.add_callback(cn.PTYPE["EVENT"]["NICK"],
                                     self.handle_user)
        
        self.people = dict()

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

    def ready(self):
        self.owner.connection.send_packet(cn.PTYPE["CLIENT"]["WHO"], "",
                                    self.handle_who)