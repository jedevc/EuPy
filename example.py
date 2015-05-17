import euphoria

class HiComponent(euphoria.chat_component.ChatComponent):
    def __init__(self, owner):
        super().__init__(owner)

    def handle_chat(self, message):
        if "hi" in message["content"].lower():
            self.send_chat("Hi there!", message["id"])

def main():
    hi = euphoria.room.Room("test")
    hi.add_component("ping", euphoria.ping_component.PingComponent(hi))
    hi.add_component("hi", HiComponent(hi))
    
    hi.run("HiBot")

if __name__ == "__main__":
    main()