import socket
import threading
from typing import Callable, Optional
from .inetwork import INetwork, receive_packet
from .packet import Packet
from .packets import C2SHello


class Client(INetwork):
    socket = None

    def __init__(self, host: str, port: int):
        self.thread = None
        self.handlers = []
        self.host = host
        self.port = port

    def create(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.thread = threading.Thread(target=self.receive_loop)

    def send_packet(self, packet: Packet):
        self.socket.send(packet.pack())

    def run(self, callback: Callable[[Optional[Exception]], None]) -> None:
        try:
            self.socket.connect((self.host, self.port))
            self.send_packet(C2SHello())
            self.thread.start()
            callback(None)
        except Exception as e:
            callback(e)

    def add_packet_handler(self, handler: Callable[[Packet], None]):
        self.handlers.append(handler)

    def receive_loop(self):
        while True:
            packet = receive_packet(self.socket)
            if packet is not None:
                for handler in self.handlers:
                    handler(packet)
