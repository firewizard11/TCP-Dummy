import argparse
import tcp_client
import tcp_server


def main():
    """ Example Flow
    1. Start Server/Client, with relevant options
    2. Ctrl+C to Close the Program
    """

    parser = argparse.ArgumentParser(
        prog="tcp_dummy.py"
    )

    parser.add_argument("command", choices=["server", "client"])
    parser.add_argument("-H", "--Host")
    parser.add_argument("-P", "--Ports")

    args = parser.parse_args()

    print(args)

    command = args.command
    host = args.Host
    ports = args.Ports
    device = None

    match (command):
        case "server":
            device = tcp_server.TCPServer(host)

        case "client":
            device = tcp_client.TCPClient()

if __name__ == '__main__':
    main()