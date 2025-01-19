import socket
from typing import Dict


class TCPServer():

    def __init__(self, server_ip: str = ''):
        self.listening_ports: Dict[int, socket.socket | None] = {}
        self.server_ip = server_ip
        print(f'[*] Created Server [IP: {self.server_ip}]')

    def get_server_ip(self) -> str:
        return self.server_ip
    
    def set_server_ip(self, new_ip: str) -> None:
        self.server_ip = new_ip
        print(f'[*] New Server IP: {self.server_ip}')

    def is_listening(self, port_number: int) -> bool:
        if self.listening_ports[port_number] is None:
            return False
        else:
            return True
        
    def start_listener(self, port_number: int) -> None:
        if self.is_listening(port_number):
            return None
        
        self.listening_ports[port_number] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.listening_ports[port_number].bind((self.server_ip, port_number))

        self.listening_ports[port_number].listen(0)

        print(f'[*] Listening on {self.server_ip}:{port_number}')

    def stop_listener(self, port_number: int) -> None:
        if not self.is_listening(port_number):
            return None
        
        self.listening_ports[port_number].close()
        self.listening_ports[port_number] = None
        print(f'[*] Port Closed: {port_number}')