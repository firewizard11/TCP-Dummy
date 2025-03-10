"""This Module Defines a TCPServer Class."""

import socket
import threading
from typing import List

MAX_PORTS = 65535
CLOSED = 0


class TCPServer():
    """Represents a TCP Server."""

    def __init__(self, server_ip: str = '', timeout: int = 10, backlog: int = 5):
        self.open_ports: List[int | socket.socket] = [CLOSED] * MAX_PORTS
        self.server_ip = server_ip
        self.timeout = timeout
        self.backlog = backlog

        print(f'[*] Created Server [IP: "{self.server_ip}", Timeout {self.timeout}, Backlog: {self.backlog}]')

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
        """Checks if a port is open or closed."""

        if self.open_ports[port - 1] is CLOSED:
            return False
        else:
            return True

    def open_port(self, port: int) -> None:
        """This method will open a port on the server"""

        print(f'[*] Opening Port [{port}]...')

        if self.is_open(port):
            raise Exception(f'Port {port} is Already Open')

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)

        sock.bind((self.server_ip, port))
        sock.listen(self.backlog)

        self.open_ports[port - 1] = sock

        print(f'[*] Opened Port [{port}]')

    def close_port(self, port: int) -> None:
        """This method will close an open port."""

        print(f'[*] Closing Port [{port}]...')

        if not self.is_open(port):
            raise Exception(f'Port {port} is Already Closed')

        self.open_ports[port - 1].close()
        self.open_ports[port - 1] = CLOSED

        print(f'[*] Closed Port [{port}]')

    def close_server(self) -> None:
        """This Method will loop through each port and close it."""

        print('[*] Closing Server...')
        for port in self.open_ports:
            if port is not CLOSED:
                port.close()
        print('[*] Closed Server')

    def accept_connection(self, port: int) -> None:
        """Will wait for incoming connections (until timeout).
           When a connection establishes it will wait for data until the connection is closed.
        """

        if not self.is_open(port):
            raise Exception(f'Port {port} is not Open')

        try:
            connection, address = self.open_ports[port - 1].accept()
        except TimeoutError:
            print(f'[!] No Incoming Connections [{port}]')
            return None

        print(f'[*] Connection Established {port} <- {address[0]}:{address[1]}')

        while True:

            data = connection.recv(4096)

            print(data.decode('utf-8'))

            if len(data) == 0:
                print(f'[*] Closing Connection {address[0]} [{port}]')
                connection.close()
                break

    def accept_multiple_connections(self, ports: List[int]) -> None:
        """Will accept and process a connection on it's own thread.
           Use if you want to accept connections on multiple ports at the same time.
        """
        threads = []

        for port in ports:
            new_thread = threading.Thread(target=self.accept_connection, args=(port,))
            threads.append(new_thread)
            new_thread.start()

        for thread in threads:
            thread.join()
