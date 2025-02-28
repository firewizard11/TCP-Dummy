import socket


class TCPClient():

    def __init__(self, timeout: int = 10):
        """ TCP Client Constructor
        
        :Parameters:
        - timeout (int): How long to wait for connection or response (Default=10s)
        """
        self.current_connection: socket.socket | None = None
        self.timeout = timeout
        print('[*] Client Created')

    # Getters and Setters
    def get_timeout(self) -> int:
        return self.timeout
    
    def set_timeout(self, new_timeout: int) -> None:
        self.timeout = new_timeout

    # Methods
    def is_connected(self) -> bool:
        """ Check if Client has an active connection 
        
        :Returns:
        - True: If connection active
        - False: If connection is not active
        """
        if self.current_connection is None:
            return False
        else:
            return True

    def create_connection(self, server_ip: str, port: int) -> None:
        """ Attempt to establish connection with chosen server:port

        :Parameters:
        - server_ip (str): An IPv4 address to connect to
        - port (int): An port number to connect to
        """
        print(f'[*] Creating Connection with {server_ip}:{port}...')

        if self.is_connected():
            print('[*] Closing Previous Connection...')
            self.close_connection()

        new_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        new_sock.settimeout(self.timeout)

        try:
            new_sock.connect((server_ip, port))
        except TimeoutError:
            print(f'[!] Connection Timeout with {server_ip}:{port}')
            new_sock.close()
            return None
        except ConnectionRefusedError:
            print(f'[!] Connection Refused by {server_ip}:{port}')
            new_sock.close()
            return None
        
        self.current_connection = new_sock
        print(f'[*] Connection Established with {server_ip}:{port}') 

    def close_connection(self) -> None:
        """ Will close any active connection
        If no connection is active will end early
        """
        if not self.is_connected():
            return None

        print('[*] Closing Connection...')
        self.current_connection.close()
        self.current_connection = None
        print('[*] Connection Closed')

    def send_data(self, data: str) -> None:
        """ Will try to send a message to connected server until timeout
        Terminates early if no active connection

        :Parameter:
        - data (str): The data to be sent        
        """

        if not self.is_connected():
            return None
        
        try:
            self.current_connection.sendall(bytes(data, encoding='utf-8'))
        except TimeoutError:
            print('[!] Connection Timeout: Data Didn\'t Send')
            return None
        
        print(f'[*] Outgoing Data: {data}')

    def receive_data(self) -> None:
        """ Will wait for data to arrive from server until timeout
        Finish early if no active connection
        """
        if not self.is_connected():
            return None

        while True:

            try:
                data = self.current_connection.recv(4096)
            except TimeoutError:
                print('[!] Timeout: No Response From Server')
                break

            if not data:
                break

            print(f'[*] Incoming Data: {data.decode('utf-8')}')

if __name__ == '__main__':
    test_client = TCPClient()
    test_client.create_connection('127.0.0.1', 4444)
    test_client.send_data('Data Test 1!!!!')
    test_client.create_connection('192.168.60.129', 1234)
    test_client.send_data('Data Test 2 :::::)_)_)_()()()()')
    test_client.receive_data()
    test_client.close_connection()