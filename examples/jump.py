import euphoria as eu

class JumpBot(eu.ping_room.PingRoom, eu.chat_room.ChatRoom):
    def __init__(self, roomname, password=None):
        super().__init__(roomname, password, attempts=2)

        self.nickname = "JumpBot"

    def handle_chat(self, message):
        c = eu.command.Command(message["content"])
        c.parse()

        if c.command == "jump" and len(c.args) == 1:
            self.send_chat("/me jumps to " + c.args[0] + ".", message["id"])
            self.jump(c.args[0])

def main():
    bot = JumpBot("testing")
    eu.executable.start(bot)

if __name__ == "__main__":
    main()
