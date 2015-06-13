import euphoria as eu

class HiBot(eu.ping_room.PingRoom, eu.chat_room.ChatRoom):
    def __init__(self, roomname, password=None):
        super().__init__(roomname, password)

        self.nickname = "HiBot"

    def handle_chat(self, message):
        if message["content"] == "!ping":
            self.send_chat("Pong!", message["id"])
        elif "hi" in message["content"].lower():
            self.send_chat("Hi there!", message["id"])

    def setup(self):
        print("Appearing...")

    def cleanup(self):
        print("Leaving...")

def main():
    hi = HiBot("test")
    eu.executable.start(hi)

if __name__ == "__main__":
    main()
