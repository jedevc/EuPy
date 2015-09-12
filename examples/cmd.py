import euphoria as eu

class CmdBot(eu.ping_room.PingRoom, eu.chat_room.ChatRoom):
    def __init__(self, roomname, password=None):
        super().__init__(roomname, password, attempts=2)

    def handle_chat(self, message):
        c = eu.command.Command(message["content"])
        c.parse()
        print("command: %s\nflags: %s\nargs: %s\n%s" % (c.command, str(c.flags), c.args, '*'*10))

def main():
    cmdbot = CmdBot("testing")
    eu.executable.start(cmdbot)

if __name__ == "__main__":
    main()
