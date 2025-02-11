import argparse
import tcp_client
import tcp_server


def main():
    """ Example Flow
    1. Start Server/Client, with relevant options
    2. Close Server/Client that was opened by previous command
    """

    parser = argparse.ArgumentParser(
        prog="tcp_dummy.py"
    )

    parser.add_argument("command", choices=["server", "client", "close"])
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

        case "close":
            if device is None:
                print("[!] No Device On")
                return None
            
            if type(device) is tcp_server.TCPServer:
                print("[*] Closing Server...")

                device.close_server()

                print("[*] Server Closed")
                return None
            
            if type(device) is tcp_client.TCPClient:
                print("[*] Closing Client...")

                device.close_connection()

                print("[*] Client Closed")
                return None

if __name__ == '__main__':
    main()