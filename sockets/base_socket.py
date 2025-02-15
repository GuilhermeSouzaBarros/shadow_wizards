from socket import *
import multiprocessing
from abc import ABC, abstractmethod

class BaseSocket(ABC):
    def __init__(self):
        self.ip = gethostbyname(gethostname())
        self.socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        
        self.send_queue = multiprocessing.Queue(256)
        self.get_queue = multiprocessing.Queue(256)

        self.process_send = None
        self.process_get = None

    @abstractmethod
    def get_data(self, loop:bool=False) -> None:
        raise NotImplementedError

    @abstractmethod
    def send_data(self, loop:bool=False) -> None:
        raise NotImplementedError

    def update_get(self, loop:bool=False) -> None:
        if not self.process_get or (self.process_get and not self.process_get.is_alive()):
            self.process_get = multiprocessing.Process(target=self.get_data, args=(loop,), daemon=True)
            self.process_get.start()

    def update_send(self, loop:bool=False) -> None:
        if not self.process_send or (self.process_send and not self.process_send.is_alive()):
            self.process_send = multiprocessing.Process(target=self.send_data, args=(loop,), daemon=True)
            self.process_send.start()

    def update(self, loop:bool=False) -> None:
        self.update_get(loop)
        self.update_send(loop)

    def close(self) -> None:
        if self.process_get and self.process_get.is_alive():
            self.process_get.kill()
        if self.process_send and self.process_send.is_alive():
            self.process_send.kill()
        self.socket.close()
        