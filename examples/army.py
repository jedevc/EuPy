import euphoria as eu

class SoldierBot(eu.ping_room.PingRoom, eu.chat_room.ChatRoom):
    def __init__(self, roomname, password=None):
        super().__init__(roomname, password, attempts=2)

        self.nickname = "SoldierBot"

    def handle_chat(self, m):
        if m["content"] == "!attack":
            self.send_chat("ATTACK!!!", m["id"])

class ArmyBot(eu.ping_room.PingRoom, eu.chat_room.ChatRoom):
    def __init__(self, group, roomname, password=None):
        super().__init__(roomname, password, attempts=2)

        self.nickname = "ArmyBot"

        self.group = group

    def handle_chat(self, message):
        if message["content"] == "!ping":
            self.send_chat("Pong!", message["id"])
        elif message["content"] == "!spawn":
            self.group.add(SoldierBot(self.roomname, self.password))

def main():
    bot = eu.execgroup.ExecGroup()
    bot.add(ArmyBot(bot, "testing"))

    eu.executable.start(bot)

if __name__ == "__main__":
    main()
