import websocket
import json

def build_json(**data):
    """
    build_json(**data) -> dict

    Build a dictionary out of arguments.
    """

    return data

#Different things that you or the server can send.
PTYPE = {"CLIENT": {"PING": "ping-reply", "NICK": "nick", "WHO": "who",
                    "LOG": "log", "SEND": "send", "AUTH": "auth"},
         "SERVER": {"NICK": "nick-reply", "WHO": "who-reply",
                    "LOG": "log-reply", "SEND": "send-reply"},
         "EVENT":  {"PING": "ping-event", "NICK": "nick-event",
                    "SEND": "send-event", "SNAPSHOT": "snapshot-event",
                    "JOIN": "join-event", "PART": "part"}
        }

class DictFields:
    def __init__(self, dictionary):
        for k, v in dictionary:
            setattr(self, k, v)

class Connection:
    """
    A basic object that provides a simple interface of callbacks for sending and
    receiving packets.
    """

    def __init__(self):
        self.socket = None
        self.idcounter = 0

        self.type_callbacks = dict()
        self.id_callbacks = dict()

    def add_callback(self, ptype, callback):
        """
        add_callback(ptype, callback) -> None

        Add a callback so that when a packet of type ptype arrives, it will be
        proccessed by the callback.
        """

        if ptype not in self.type_callbacks:
            self.type_callbacks[ptype] = []
        self.type_callbacks[ptype].append(callback)

    def connect(self, room):
        """
        connect(room) -> None

        Connect to the given room. Cannot send messages without first
        connecting.
        """

        url = "wss://euphoria.io/room/" + room + "/ws"
        self.socket = websocket.create_connection(url)

    def close(self):
        """
        close() -> None

        Close the connection to the room off nicely.
        """

        self.socket.close()
        self.socket = None

    def send_json(self, data):
        """
        send_json(data) -> None

        Send json data into the stream.
        """

        if self.socket is not None:
            self.socket.send(json.dumps(data))

    def receive_data(self):
        """
        reveive_data() -> None

        Reveive a packet and send it to handle_packet() for proccessing.
        """

        raw = self.socket.recv()
        self.handle_packet(json.loads(raw))

    def send_packet(self, ptype, data, callback=None):
        """
        send_packet(data, ptype, callback=None) -> None

        Creates a packet of type ptype, and sends the data. Also creates a
        callback entry for when a reply is received.
        """

        pid = self.idcounter
        self.idcounter += 1

        packet = {"id": str(pid),

                  "type": ptype,
                  "data": data}

        self.send_json(packet)

        if callback is not None:
            self.id_callbacks[pid] = callback

    def handle_packet(self, packet):
        """
        handle_packet(packet) -> None

        Process a packet and send it off to the appropriate callback.
        """

        pid = packet.get("id")
        if pid in self.id_callbacks:
            self.id_callbacks[pid](packet)
            self.id_callbacks.pop(pid, None)

        ptype = packet.get("type")
        if ptype in self.type_callbacks:
            for i in self.type_callbacks[ptype]:
                i(packet)
