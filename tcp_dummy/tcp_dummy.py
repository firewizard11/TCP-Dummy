import argparse
import tcp_client
import tcp_server


def main():
    parser = argparse.ArgumentParser(usage='python3 tcp_dummy.py [command] [options]')
    
    parser.add_argument('command', choices=['server', 'client'])

    parser.add_argument('-h --host')


    

if __name__ == '__main__':
    main()