import socket
from time import sleep

from utils import load_config

config = load_config()['pd_connector']


class PDConnector:
    def __init__(self, config: dict) -> None:
        # self.socket_port = config['socket_port']
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(('localhost', 2342))

    def send(self, msg: str = ""):
        fudi_msg = msg + ' ;'  # pure data uses the FUDI protocol (messages terminate with ';')
        self.socket.send(fudi_msg.encode('ascii'))

    def send_ints(self, ints: list[int]):
        try:
            assert all(int_ in range(0, 128) for int_ in ints)
        except AssertionError:
            print(f"Number must be in ASCII range (0, 128)!")

        msg = " ".join(chr(int_) for int_ in ints)
        self.send(msg)

if __name__ == "__main__":
    connector = PDConnector(config)
    
    while True:
        connector.send_ints([1, 5])
        # connector.send("python")
        print("sent")
        sleep(1)