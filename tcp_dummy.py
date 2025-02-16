import argparse
import tcp_client
import tcp_server
from helper import format_ports, validate_host, validate_port


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        usage='python3 tcp_dummy.py command options'
    )

    parser.add_argument('command', choices=['server', 'client'])

    args = parser.parse_args()

    command = args.command

    match (command):
        case 'server':
            device = tcp_server.TCPServer()

        case 'client':
            device = tcp_client.TCPClient()
