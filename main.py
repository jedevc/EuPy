import euphoria

def main():
    test_room = euphoria.chat_room.ChatRoom("test")
    test_room.join("TestNick")

    test_room.run()

if __name__ == "__main__":
    main()