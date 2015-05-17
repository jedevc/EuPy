from . import connection as cn

from . import component

class UserComponent(component.Component):
    """
    A user component contains a list of all the current users in the room.
    """

    def __init__(self, owner):
        super().__init__(owner)

        self.owner.connection.add_callback(cn.PTYPE["EVENT"]["NICK"],
                                        self.handle_change)
        self.owner.connection.add_callback(cn.PTYPE["EVENT"]["JOIN"],
                                        self.handle_join)
        self.owner.connection.add_callback(cn.PTYPE["EVENT"]["PART"],
                                        self.handle_part)
        
        self.people = dict()

    def handle_change(self, data):
        """
        handle_user(data) -> None
        
        Add and remove users from self.people.
        """
        
        info = data["data"]
        
        if info["from"] in self.people:
            self.people.pop(info["from"])
            
        self.people[info["to"]] = None
    
    def handle_join(self, data):
        self.people[data["data"]["name"]] = None
    
    def handle_part(self, data):
        if data["data"]["name"] in self.people:
            self.people.pop(data["data"]["name"])
        
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