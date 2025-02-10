from socket import *

from sockets.address import set_address
from sockets.base_socket import BaseSocket

class Server(BaseSocket):
    def __init__(self):
        super().__init__()
        self.port = 0
        for i in range(65534, 0, -1):
            try:
                self.socket.bind((self.ip, i))
                self.port = i
                break
            except:
                continue
        set_address(self.ip, self.port)
        print("Server addr:", (self.ip, self.port))
        self.clients_addresses = []

    def get_data(self, loop:bool) -> None:
        while True:
            data, addr = self.socket.recvfrom(128)
            if addr in self.clients_addresses or len(self.clients_addresses) < 4:
                self.get_queue.put([addr, data])
            if not loop: break

    def send_data(self, loop:bool) -> None:
        while True:
            data = self.send_queue.get()
            for addr in self.clients_addresses:
                self.socket.sendto(data, addr)
            if not loop: break
