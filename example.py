import euphoria as eu

class HiBot(eu.ping_room.PingRoom, eu.chat_room.ChatRoom):
    def __init__(self, roomname, password=None):
        super().__init__(roomname, password)
    
        self.nickname = "HiBot"

    def handle_chat(self, message):
        if "hi" in message["content"].lower():
            self.send_chat("Hi there!", message["id"])

def main():
    hi = HiBot("test")
    hi.run()

if __name__ == "__main__":
    main()