from socket import *
from time import sleep
import multiprocessing

from sockets.address import set_address

class Server:
    def __init__(self):
        self.ip = gethostbyname(gethostname())
        self.socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
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
        self.send_queue = multiprocessing.Queue(10)
        self.get_queue = multiprocessing.Queue(10)

        self.process_get = None
        self.process_send = None

    def get_data(self):
        data, addr = self.socket.recvfrom(1024)
        if addr in self.clients_addresses or len(self.clients_addresses) < 4:
            self.get_queue.put([addr, data])

    def send_data(self):
        while True:
            try:
                data = self.send_queue.get_nowait()
                for addr in self.clients_addresses:
                    self.socket.sendto(data, addr)
            except:
                break

    def update(self):
        if not self.process_get or (self.process_get and not self.process_get.is_alive()):
            self.process_get = multiprocessing.Process(target=self.get_data, daemon=True)
            self.process_get.start()

        if not self.process_send or (self.process_send and not self.process_send.is_alive()):
            self.process_send = multiprocessing.Process(target=self.send_data, daemon=True)
            self.process_send.start()
