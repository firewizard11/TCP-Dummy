import socket


class TCPClient():

    def __init__(self):
        self.current_connection: socket.socket | None = None

    def is_connected(self) -> bool:
        if self.current_connection is not None:
            return True
        else:
            return False
        
    def close_connection(self) -> None:
        self.current_connection.close()
        self.current_connection = None
        print('[*] Connection Closed')

    def create_connection(self, host_ip: str, port: int) -> None:
        if self.is_connected():
            self.close_connection()

        self.current_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.current_connection.settimeout(5)

        try:
            self.current_connection.connect((host_ip, port))
            print(f'[*] Connection Established {host_ip}:{port}')
        except TimeoutError:
            print('[!] Connection Timed Out')
            self.close_connection()

    def send_message(self, message: str) -> None:
        if not self.is_connected():
            print('[!] No Connection Active')
            return
        
        self.current_connection.sendall(bytes(message, encoding='utf-8'))
        print(f'[*] Outgoing Message: {message}')

    def receive_message(self) -> None:
        if not self.is_connected():
            print('[!] No Connection Active')

        while True:
            data = self.current_connection.recv(4096)

            if not data:
                break

            print(f'[*] Incoming Message: {data}')