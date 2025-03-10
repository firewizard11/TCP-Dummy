# TCP Dummy

## Description

TCP Dummy is a tool I developed to help me test TCP Networking tools

### Warning

Usable but not free of bugs/errors and definitely not polished

## How to Use

### Create local TCP Server listening on Ports 80,443

python3 tcp_dummy.py server -H 127.0.0.1 -P 80,443

### Create local TCP Server listening on Ports 50000 to 50200 which will listen for 200s

python3 tcp_dummy.py server -H 127.0.0.1 -P 50000-50200 -T 200

### Send data to target server on a certain port (Will wait for response until Timeout)

python3 tcp_dummy.py client -H 127.0.0.1 -P 1234 -D "Hello, World!" -T 5
