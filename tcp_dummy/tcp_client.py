import socket


class TCPClient():

    def __init__(self, timeout: int = 10):
        self.current_connection: socket.socket | None = None
        self.timeout = timeout

    # Getters and Setters
    def get_timeout(self) -> int:
        return self.timeout
    
    def set_timeout(self, new_timeout: int) -> None:
        self.timeout = new_timeout
    
    # Methods
    def is_connected(self) -> bool:
        return self.current_connection is not None
        
    def close_connection(self) -> None:
        self.current_connection.close()
        self.current_connection = None
        print('[*] Connection Closed')

    def create_connection(self, host_ip: str, port: int) -> None:
        if self.is_connected():
            print('[*] Closing Current Connection')
            self.close_connection()

        new_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        new_sock.settimeout(self.timeout)

        try:
            new_sock.connect((host_ip, port))
        except TimeoutError:
            print(f'[!] Connection Timeout with {host_ip}:{port}')
            new_sock.close()
            return None
        
        self.current_connection = new_sock
        print(f'[*] Connection Established with {host_ip}:{port}')

    def send_message(self, message: str) -> None:
        if not self.is_connected():
            print('[!] No Connection Active')
            return None
        
        try:
            self.current_connection.sendall(bytes(message, encoding='utf-8'))
        except TimeoutError:
            print('[!] Connection Timeout: Message Didn\'t Send')
            return None
        
        print(f'[*] Outgoing Message: {message}')

    def receive_message(self) -> None:
        if not self.is_connected():
            print('[!] No Connection Active')
            return None

        while True:

            try:
                data = self.current_connection.recv(4096)
            except TimeoutError:
                print('[*] No Response From Server')
                break

            if not data:
                break

            print(f'[*] Incoming Message: {data.decode('utf-8')}')

if __name__ == '__main__':
    test_client = TCPClient(1)

    print(test_client.is_connected(), 'timeout:', test_client.get_timeout())

    test_client.create_connection('127.0.0.1', 4444)

    test_client.send_message('Hello, Server\n')

    test_client.receive_message()

    test_client.send_message('No Reply?\n')

    test_client.close_connection()