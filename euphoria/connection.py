import websocket
import json

import threading

from . import exception

def build_json(**data):
    """
    build_json(**data) -> dict

    Build a dictionary out of arguments.
    """

    return data

#Different things that you or the server can send.
PTYPE = {"CLIENT": {"PING": "ping-reply", "NICK": "nick", "WHO": "who",
                    "LOG": "log", "SEND": "send", "AUTH": "auth"},
        "SERVER":  {"NICK": "nick-reply", "WHO": "who-reply",
                    "LOG": "log-reply", "SEND": "send-reply"},
        "EVENT":   {"PING": "ping-event", "NICK": "nick-event",
                    "SEND": "send-event", "SNAPSHOT": "snapshot-event",
                    "JOIN": "join-event", "PART": "part-event"}
        }

class Connection:
    """
    A basic object that provides a simple interface of callbacks for sending and
    receiving packets.
    """

    def __init__(self):
        self.socket = None
        self.room = ""
        
        self.lock = threading.RLock()
        
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

        self.room = room

        url = "wss://euphoria.io/room/" + room + "/ws"
        
        try:
            self.socket = websocket.create_connection(url)
        except (websocket.WebSocketException, IOError):
            raise exception.EuphoriaConnectionLost()

    def close(self):
        """
        close() -> None

        Close the connection to the room off nicely.
        """

        if self.socket is not None:
            self.socket.close()
            self.socket = None

    def send_json(self, data):
        """
        send_json(data) -> None

        Send json data into the stream.
        """

        if self.socket is None:
            raise exception.EuphoriaNoConnection

        try:
            self.socket.send(json.dumps(data))
        except websocket.WebSocketException:
            raise exception.EuphoriaConnectionLost()

    def receive_data(self):
        """
        reveive_data() -> None

        Reveive a packet and send it to handle_packet() for proccessing.
        """

        if self.socket is None:
            raise exception.EuphoriaNoConnection
            
        try:
            raw = self.socket.recv()
            self.handle_packet(json.loads(raw))
        except websocket.WebSocketException:
            raise exception.EuphoriaConnectionLost()

    def send_packet(self, ptype, data, callback=None):
        """
        send_packet(data, ptype, callback=None) -> None

        Creates a packet of type ptype, and sends the data. Also creates a
        callback entry for when a reply is received.
        """

        with self.lock:
            pid = self.idcounter
            self.idcounter += 1

            packet = {"id": str(pid),
                    "type": ptype,
                    "data": data}

            self.send_json(packet)

            if callback is not None:
                self.id_callbacks[str(pid)] = callback

    def handle_packet(self, packet):
        """
        handle_packet(packet) -> None

        Process a packet and send it off to the appropriate callback.
        """

        pid = packet.get("id")
        ptype = packet.get("type")
        
        if pid in self.id_callbacks:
            callback = self.id_callbacks.pop(pid)
            if callable(callback):
                callback(packet)

        if ptype in self.type_callbacks:
            for i in self.type_callbacks[ptype]:
                i(packet)
