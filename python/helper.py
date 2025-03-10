def validate_port(port: int) -> bool:
    return (1 <= port <= 65535)


def validate_host(host: str) -> bool:
    if '.' not in host or host.count('.') != 3:
        return False
    
    octets = host.split('.')

    if len(octets) != 4:
        return False
    
    for octet in octets:
        if not octet.isdecimal():
            return False

        if not (0 <= int(octet) <= 255):
            return False
        
        if int(octet) < 10 and len(octet) > 1:
            return False
        
        if int(octet) < 100 and len(octet) > 2:
            return False
        
        if int(octet) < 1000 and len(octet) > 3:
            return False
        
        if int(octet) < 10000 and len(octet) > 4:
            return False

    return True


def format_ports(ports: str) -> list[int]:
    """ Formats various forms of port inputs into a list of port numbers 
    
    Supported Formats:
    - Single Port (e.g. "40" or "40000")
    - Range of Ports (Inclusive) (e.g. "40-2000")
    - List of Ports (e.g. 21,22,80,139,443,445)
    """
    # List of Ports 
    if ',' in ports:
        temp = ports.split(',')

        for elem in temp:
            if not elem.isdecimal():
                raise ValueError(f'Please Enter a list of valid ports: {elem}')
             
            if not validate_port(int(elem)):
                raise ValueError(f'Error: Invalid Port in List {elem}')
            
        return [int(port) for port in temp]
    
    # Range of Ports
    if '-' in ports:
        temp = ports.split('-')

        if len(temp) != 2:
            raise ValueError(f'Error: Incorrect Number of Ports in Range of Ports: {ports}')
        
        for elem in temp:
            if not elem.isdecimal():
                raise ValueError(f'Please Enter a Range of valid ports: {elem}')
            
            if not validate_port(int(elem)):
                raise ValueError(f'Error: Invalid Port in Range {elem}')
            
        start = int(temp[0])
        stop = int(temp[1]) + 1

        if start > stop:
            raise ValueError(f'{start} Should be smaller than {stop}')

        return list(range(start, stop))

    # Single Ports
    if not ports.isdecimal():
        raise ValueError(f'Use a Supported Port Format: {ports}')
    
    if not validate_port(int(ports)):
        raise ValueError(f'Enter a valid port: {ports}')
    
    return [int(ports)]

