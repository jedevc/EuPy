from . import connection as cn

from . import room

class UserRoom(room.Room):
    """
    A user room contains a list of all the current users in the room.
    """

    def __init__(self, roomname, password=None, attempts=None):
        super().__init__(roomname, password, attempts)

        self.connection.add_callback("nick-event", self.handle_change)
        self.connection.add_callback("join-event", self.handle_join)
        self.connection.add_callback("part-event", self.handle_part)
        self.connection.add_callback("snapshot-event", self.handle_snapshot)

        self.users = []

    def get_users(self, prefix):
        return [x[1] for x in self.users if x[0].split(':')[0] == prefix]

    def handle_change(self, data):
        """
        handle_user(data) -> None

        Change a user's name.
        """

        if (data["data"]["id"], data["data"]["from"]) in self.users:
            self.users.remove((data["data"]["id"], data["data"]["from"]))

        self.users.append((data["data"]["id"], data["data"]["to"]))

    def handle_join(self, data):
        """
        handle_join(data) -> None

        Add a new user when they join.
        """

        self.users.append((data["data"]["id"], data["data"]["name"]))

    def handle_part(self, data):
        """
        handle_part(data) -> None

        Remove a user when they leave.
        """

        if (data["data"]["id"], data["data"]["name"]) in self.users:
            self.users.remove((data["data"]["id"], data["data"]["name"]))

    def handle_snapshot(self, data):
        """
        handle_who(data) -> None

        Get a complete list of who is in the room.
        """

        self.users.clear()

        for user in data["data"]["listing"]:
            self.users.append((user["id"], user["name"]))
