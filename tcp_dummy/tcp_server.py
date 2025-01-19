""" This Module Defines a TCPServer Class """

import socket
from typing import List

MAX_PORTS = 65535
CLOSED = 0


class TCPServer():
    """ Represents a TCP Server """

    def __init__(self, server_ip: str = '', timeout: int = 10, backlog: int = 5):
        self.open_ports: List[int | socket.socket] = [CLOSED] * MAX_PORTS
        self.server_ip = server_ip
        self.timeout = timeout
        self.backlog = backlog

        print(f'[*] Created Server [IP: {self.server_ip}, Timeout {self.timeout}, Backlog: {self.backlog}]')

    # === getters & setters
    def get_server_ip(self) -> str:
        return self.server_ip

    def set_server_ip(self, new_ip: str) -> None:
        self.server_ip = new_ip
        print(f'[*] New Server IP: {self.server_ip}')

    def get_timeout(self) -> int:
        return self.timeout

    def set_timeout(self, new_timeout: int) -> None:
        self.timeout = new_timeout
        print(f'[*] New Timeout: {self.timeout}')

    def get_backlog(self) -> int:
        return self.backlog
    
    def set_backlog(self, new_backlog: int) -> None:
        self.backlog = new_backlog
        print(f'[*] New Backlog: {self.backlog}')

    # === methods ===
    def is_open(self, port: int) -> bool:
        if self.open_ports[port - 1] is CLOSED:
            return False
        else:
            return True
        
    def open_port(self, port: int) -> None:
        if self.is_open(port):
            raise Exception(f'Port {port} is Already Open')
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)

        sock.bind((self.server_ip, port))
        sock.listen(self.backlog)

        self.open_ports[port - 1] = sock

    def close_port(self, port: int) -> None:
        if not self.is_open(port):
            raise Exception(f'Port {port} is Already Closed')
        
        self.open_ports[port - 1].close()
        self.open_ports[port - 1] = CLOSED

    def close_server(self) -> None:
        for port in self.open_ports:
            if port is not CLOSED:
                port.close()

    def accept_connection(self, port: int) -> None:
        if not self.is_open(port):
            raise Exception(f'Port {port} is not Open')
        
        connection, address = self.open_ports[port - 1].accept()





if __name__ == '__main__':
    test_server = TCPServer()

    print(f'Start (OPEN?): {test_server.is_open(50)} | {test_server.is_open(4444)}')

    for _ in range(10):        
        test_server.open_port(50)
        test_server.open_port(4444)

        print(f'Open: {test_server.is_open(50)} | {test_server.is_open(4444)}')

        test_server.close_port(50)
        test_server.close_port(4444)

        print(f'Closed: {not test_server.is_open(50)} | {not test_server.is_open(4444)}')

    test_server.close_server()