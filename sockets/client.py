from socket import *

from sockets.address import get_address
from sockets.base_socket import BaseSocket

class Client(BaseSocket):
    def __init__(self):
        super().__init__()
        self.socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.server_addr = get_address()
        
        self.server_handshake = False

    def get_data(self, loop:bool) -> None:
        while True:
            data, addr = self.socket.recvfrom(1024)
            while addr != self.server_addr:
                data, addr = self.socket.recvfrom(1024)
            self.get_queue.put(data)
            if not loop: break

    def send_data(self, loop:bool) -> None:
        while True:
            data = self.send_queue.get()
            self.socket.sendto(data, self.server_addr)
            if not loop: break
