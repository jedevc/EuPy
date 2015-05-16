import euphoria

class HiBot(euphoria.chat_room.ChatRoom):
    def __init__(self, room, password=None):
        super().__init__(room, password)

    def handle_chat(self, message):
        if "hi" in message["content"].lower():
            self.send_chat("Hi there!", message["id"])

def main():
    hi = HiBot("test")
    hi.join("HiBot")

    hi.run()

if __name__ == "__main__":
    main()