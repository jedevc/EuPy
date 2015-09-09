import websocket
import json

import time
import threading

def build_json(**data):
    """
    build_json(**data) -> dict

    Build a dictionary out of arguments.
    """

    return data

class Connection:
    """
    A basic object that provides a simple interface of callbacks for sending and
    receiving packets.
    """

    def __init__(self, limit=0):
        self.socket = None
        self.room = ""

        self.idcounter = 0

        self.limit = limit
        self.last_packet = time.time()

        #Different types of callbacks
        self.type_callbacks = dict()
        self.id_callbacks = dict()

        #Thread stuff
        self.lock = threading.RLock()

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
            self.socket = websocket.create_connection(url, enable_multithread=True, timeout=40)
        except (websocket.WebSocketException, IOError):
            self.socket = None

    def close(self):
        """
        close() -> None

        Close the connection to the room off nicely.
        """

        with self.lock:
            if self.socket is not None:
                try:
                    self.socket.abort()
                    self.socket.close()
                except OSError:
                    pass
                self.socket = None

    def send_json(self, data):
        """
        send_json(data) -> Bool

        Send json data into the stream. Returns false on message fail.
        """

        now = time.time()
        if self.limit != 0 and now - self.last_packet < self.limit:
            time.sleep(self.limit - (now - self.last_packet))

        try:
            self.socket.send(json.dumps(data))
        except (AttributeError, websocket.WebSocketException):
            with self.lock:
                self.socket = None
            return False

        self.last_packet = time.time()

        return True

    def receive_data(self):
        """
        reveive_data() -> Bool

        Reveive a packet and send it to handle_packet() for proccessing.
        Returns false on message fail.
        """

        if self.socket is None:
            return False

        try:
            raw = self.socket.recv()
            self.handle_packet(json.loads(raw))
        except websocket.WebSocketException:
            with self.lock:
                self.socket = None

        return True

    def send_packet(self, ptype, data, callback=None):
        """
        send_packet(data, ptype, callback=None) -> None

        Creates a packet of type ptype, and sends the data. Also creates a
        callback entry for when a reply is received.
        """

        #This is locked to prevent multiple threads from accessing the message
        with self.lock:
            pid = self.idcounter
            self.idcounter += 1

            packet = {"id": str(pid), "type": ptype, "data": data}

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
