import argparse
import tcp_client
import tcp_server
from helper import format_ports, validate_host, validate_port


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        usage='python3 tcp_dummy.py command options'
    )

    parser.add_argument('command', choices=['server', 'client'])
    parser.add_argument('-H', '--Host')
    parser.add_argument('-P', '--Ports')
    parser.add_argument('-T', '--Timeout', type=int)
    parser.add_argument('-B', '--Backlog', type=int)

    args = parser.parse_args()

    print(args)

    command = args.command

    if args.Host is None:
        host = ''
    elif validate_host(args.Host):
        host = args.Host
    else:
        print('Error: Host is Invalid')
        exit()

    try:
        ports = format_ports(args.Ports)
    except ValueError as e:
        print(f'Error: {e}')
        exit()
    
    if args.Timeout is None:
        timeout = 10
    elif args.Timeout >= 0:
        timeout = args.Timeout
    else:
        print('Error: Timeout must be greater than 0')
        exit()

    if args.Backlog is None:
        backlog = 5
    elif 0 < args.Backlog <= 5:
        backlog = args.Backlog
    else:
        print('Error: Backlog must be between 0 and 5')
        exit()

    match (command):
        case 'server':
            device = tcp_server.TCPServer(host, timeout, backlog)

            try:
                for port in ports:
                    device.open_port(port)
            except OSError as e:
                print(f'Error: {e}')
                exit()

            if len(ports) == 1:
                device.accept_connection(ports[0])
            else:
                device.accept_multiple_connections(ports)

            device.close_server()
        case 'client':
            device = tcp_client.TCPClient()

            if len(ports) > 1:
                print('Error: Too Many Ports')
                exit()
            
            device.create_connection(host, ports[0])
