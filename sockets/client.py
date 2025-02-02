from socket import *
import multiprocessing
from sockets.address import get_address

class Client:
    def __init__(self):
        self.ip = gethostbyname(gethostname())
        self.socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        self.socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.server_addr = get_address()
        self.server_addr_queue = multiprocessing.Queue(1)
        self.process_get = None
        self.process_send = None
        self.get_queue = multiprocessing.Queue(10)
        self.send_queue = multiprocessing.Queue(10)
        self.server_handshake = False

    def get_data(self):
        data, addr = self.socket.recvfrom(1024)
        while addr != self.server_addr:
            data, addr = self.socket.recvfrom(1024)
        self.get_queue.put(data)

    def send_data(self):
        while True:
            try:
                data = self.send_queue.get_nowait()
                self.socket.sendto(data, self.server_addr)

            except:
                break

    def update(self): 
        if not self.process_get or (self.process_get and not self.process_get.is_alive()):
            self.process_get = multiprocessing.Process(target=self.get_data, daemon=True)
            self.process_get.start()

        if not self.process_send or (self.process_send and not self.process_send.is_alive()):
            self.process_send = multiprocessing.Process(target=self.send_data, daemon=True)
            self.process_send.start()
