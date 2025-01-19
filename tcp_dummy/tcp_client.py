import socket


class TCPClient():

    def __init__(self, timeout: int = 5):
        self.current_connection: socket.socket | None = None
        self.timeout = timeout

    # Getters and Setters
    def get_timeout(self) -> int:
        return self.timeout
    
    def set_timeout(self, new_timeout: int) -> None:
        self.timeout = new_timeout
    
    # Methods
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
        self.current_connection.settimeout(self.timeout)

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