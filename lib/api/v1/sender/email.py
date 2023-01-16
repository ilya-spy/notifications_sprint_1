from abc import ABC, abstractmethod


class IEmail(ABC):
    @abstractmethod
    def connect(self, host: str, port: int):
        pass

    @abstractmethod
    def send(self, address: str, body: str, subject: str = None, sender: str = None):
        pass

    @abstractmethod
    def close(self):
        pass
