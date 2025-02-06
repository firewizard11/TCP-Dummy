import argparse
import tcp_client
import tcp_server


def main():
    parser = argparse.ArgumentParser(usage='python3 tcp_dummy.py [command] [options]')
    
    parser.add_argument('command', choices=['server', 'client', 'close'])

    args = parser.parse_args()

    command: str = args.command

    print(f'Command: {command}')

    match(command.lower()):
        case 'server':
            device = tcp_server.TCPServer()
        case 'client':
            device = tcp_client.TCPClient()
        case 'close':
            if isinstance(device, tcp_server.TCPServer):
                device.close_server()
                return
            if isinstance(device, tcp_client.TCPClient):
                device.close_connection()
                return
        
        


if __name__ == '__main__':
    main()