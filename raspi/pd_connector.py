import socket

from utils import load_config

config = load_config()['pd_connector']


class PDConnector:
    def __init__(self, config: dict) -> None:
        # self.socket_port = config['socket_port']
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(('localhost', 2342))

    def send(self):
        message = "hallo"
        self.socket.send(message.encode('utf-8'))

if __name__ == "__main__":
    connector = PDConnector(config)
    connector.send()