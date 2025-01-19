import socket
from typing import Dict


class TCPServer():

    def __init__(self, server_ip: str = '', timeout: int = 5):
        self.listening_ports: Dict[int, socket.socket | None] = {}
        self.server_ip = server_ip
        self.timeout = timeout
        print(f'[*] Created Server [IP: {self.server_ip}]')

    def get_server_ip(self) -> str:
        return self.server_ip

    def set_server_ip(self, new_ip: str) -> None:
        self.server_ip = new_ip
        print(f'[*] New Server IP: {self.server_ip}')

    def get_timeout(self) -> int:
        return self.timeout

    def set_timeout(self, new_timeout: int) -> None:
        self.timeout = new_timeout

    def is_listening(self, port_number: int) -> bool:
        if port_number not in self.listening_ports.keys():
            self.listening_ports[port_number] = None

        if self.listening_ports[port_number] is None:
            return False
        else:
            return True

    def start_listener(self, port_number: int) -> None:
        if self.is_listening(port_number):
            return None

        self.listening_ports[port_number] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listening_ports[port_number].settimeout(self.timeout)

        self.listening_ports[port_number].bind((self.server_ip, port_number))
        self.listening_ports[port_number].listen(0)

        print(f'[*] Listening on {self.server_ip}:{port_number}')

    def stop_listener(self, port_number: int) -> None:
        if not self.is_listening(port_number):
            return None
        
        self.listening_ports[port_number].close()
        self.listening_ports[port_number] = None
        print(f'[*] Port Closed: {port_number}')

    def accept_connection(self, port_number: int) -> None:
        if not self.is_listening(port_number):
            return None
        
        try:
            conn, addr = self.listening_ports[port_number].accept()
        except TimeoutError:
            print(f'[!] Connection Timeout [{port_number}]')
            return None

        print(f'[*] Connection Established on {port_number} from {addr[0]}:{addr[1]}')

        while True:
            try:
                data = conn.recv(4096)
            except TimeoutError:
                print('[!] Connection Timedout')
                break
            except ConnectionAbortedError:
                print('[!] Connection Aborted')
                break

            print(f'Incoming Message: {data.decode('utf-8')}')

            conn.sendall(b'Message Received')
            print('[*] Reply Sent')

            if not data:
                break

if __name__ == '__main__':
    print('=== Create Server ===')
    test_server = TCPServer('127.0.0.1', 20)

    print('=== Port 1234 ===')
    test_server.start_listener(1234)
    print(f'Is Listening: {test_server.is_listening(1234)}')
    test_server.stop_listener(1234)
    print(f'Is Listening: {test_server.is_listening(1234)}')

    print('=== Port 4444 ===')
    test_server.start_listener(4444)
    print(f'Is Listening: {test_server.is_listening(4444)}')
    test_server.accept_connection(4444)
    print(f'Is Listening: {test_server.is_listening(4444)}')
    test_server.accept_connection(4444)
    test_server.stop_listener(4444)
    print(f'Is Listening: {test_server.is_listening(4444)}')