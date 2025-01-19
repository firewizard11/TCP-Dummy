import socket


class TCPServer():

    def __init__(self, server_ip: str = ''):
        self.listening_ports = {}
        self.server_ip = server_ip

    def get_server_ip(self) -> str:
        return self.server_ip
    
    def set_server_ip(self, new_ip: str) -> None:
        self.server_ip = new_ip