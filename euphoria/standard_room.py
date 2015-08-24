from . import connection as cn

from . import chat_room

from . import utils

import datetime

class StandardRoom(chat_room.ChatRoom):
    """
    A room with basic utilities already implemented as instructed by
    https://github.com/jedevc/botrulez
    """

    def __init__(self, roomname, password=None, attempts=None):
        super().__init__(roomname, password, attempts)

        self.ping_text = "Pong!"
        self.short_help_text = None
        self.help_text = None

    def handle_message(self, data):  #TODO: This is quite hacky.
        content = data["data"]["content"]
        reply = data["data"]["id"]

        if content == "!ping":
            self.send_chat(self.ping_text, reply)
        elif content == "!ping @" + self.nickname:
            self.send_chat(self.ping_text, reply)

        elif content == "!help":
            if self.short_help_text is not None:
                self.send_chat(self.short_help_text, reply)
        elif content == "!help @" + self.nickname:
            if self.help_text is not None:
                self.send_chat(self.help_text, reply)

        elif content == "!uptime @" + self.nickname:
            u = datetime.datetime.strftime(self.start_utc, "%Y-%m-%d %H:%M:%S")
            t = utils.extract_time(self.uptime())

            self.send_chat("/me has been up since " + u + " UTC (" + t + ")", reply)
        else:
            super().handle_message(data)
