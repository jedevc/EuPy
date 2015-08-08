import euphoria as eu

class HiBot(eu.ping_room.PingRoom, eu.standard_room.StandardRoom):
    def __init__(self, roomname, password=None):
        super().__init__(roomname, password, attempts=2)

        self.nickname = "HiBot"
        self.short_help_text = "Say hello to @HiBot!"
        self.help_text = self.short_help_text + 2 * '\n' + "Just a quick demo bot."

    def handle_chat(self, message):
        if "hi" in message["content"].lower():
            self.send_chat("Hi there!", message["id"])

    def ready(self):
        self.send_chat("/me Hello!")

    def cleanup(self):
        self.send_chat("/me Goodbye...")

def main():
    hi = HiBot("testing")
    eu.executable.start(hi)

if __name__ == "__main__":
    main()
