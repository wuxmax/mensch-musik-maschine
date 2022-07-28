import socket
from time import sleep

from utils import load_config

class PDConnector:
    def __init__(self, config: dict) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(('localhost', config['socket_port']))

    # def send(self, msg: str = ""):
    #     fudi_msg = msg + ' ;'  # pure data uses the FUDI protocol (messages terminate with ';')
    #     self.socket.send(fudi_msg.encode('ascii'))

    def send(self, msg: str = ""):
        self.socket.send(msg.encode('ascii'))

    def send_int(self, int_: int):
        try:
            assert int_ in range(0, 128)
        except AssertionError:
            print(f"Number must be in ASCII range (0, 128), but is: {int_}")

        self.send(chr(int_))

    def send_ints(self, ints: list[int]):
        for int_ in ints:
            self.send_int(int_)

if __name__ == "__main__":
    config = load_config()['pd_connector']
    connector = PDConnector(config)
    
    while True:
        connector.send_ints([1, 5])
        print("sent")
        sleep(1)
        