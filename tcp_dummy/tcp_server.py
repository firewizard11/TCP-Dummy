import socket
from typing import Dict


class TCPServer():

    def __init__(self, server_ip: str = '', timeout: int = 10, backlog: int = 0):
        self.listening_ports: Dict[int, socket.socket | None] = {}
        self.server_ip = server_ip
        self.timeout = timeout
        self.backlog = backlog

        print(f'[*] Created Server [IP: {self.server_ip}, Timeout {self.timeout}, Backlog: {self.backlog}]')

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

    def is_listening(self, port_number: int) -> bool:
        if port_number not in self.listening_ports.keys():
            self.listening_ports[port_number] = None
            return False

        if self.listening_ports[port_number] is None:
            return False
        
        return True

    def start_listening(self, port_number: int) -> None:
        print(f'[*] Starting Listener on {port_number}...')

        if self.is_listening(port_number):
            print(f'[!] Port {port_number} is Already Listening')
            return None

        new_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        new_sock.settimeout(self.timeout)

        new_sock.bind((self.server_ip, port_number))
        new_sock.listen(self.backlog)

        self.listening_ports[port_number] = new_sock

        print(f'[*] Started Listener on Port {port_number}')

    def stop_listening(self, port_number: int) -> None:
        print(f'[*] Stopping Listener {port_number}...')

        if not self.is_listening(port_number):
            return None
        
        self.listening_ports[port_number].close()
        self.listening_ports[port_number] = None
        print(f'[*] Port {port_number} Closed')

    def accept_connection(self, port_number: int) -> None:
        print(f'[*] Waiting for Connection on {port_number}...')

        if not self.is_listening(port_number):
            print(f'[!] Port {port_number} is not Listening')
            return None
        
        current_sock = self.listening_ports[port_number]

        while True:
            try:
                conn, addr = current_sock.accept()
                break
            except TimeoutError:
                print(f'[!] Timeout: No Incoming Connections [Port: {port_number}]')
                continue
        
        print(f'[*] Connection Established on {port_number} from {addr}')

        print('[*] Waiting for data...')

        while True:
            
            try:
                data = conn.recv(4096)
            except TimeoutError:
                print('[!] Timeout: No Message Received')
                break
            except ConnectionAbortedError:
                print(f'[*] Connection Closed by {addr[0]}')
                return None
            except ConnectionResetError:
                print(f'[*] Connection Cosed by {addr[0]}')
                return None

            print(f'[*] Incoming Message: {data.decode('utf-8')}')

            try:
                conn.sendall(b'Message Received')
            except TimeoutError:
                print('[!] Timeout: Reply Failed to Send')
                continue

        conn.close()

if __name__ == '__main__':
    test_server = TCPServer()
    test_server.start_listening(4444)
    test_server.start_listening(1234)
    test_server.accept_connection(4444)