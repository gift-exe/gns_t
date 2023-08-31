'''

    As the file name implies ...
    Utility files for cooking the main beans : )
    This text isn't necessary in anyway
    you can carry along hehehe

'''

import re
from gns3fy import Node
import telnetlib



def extract_ip(data):        
    pattern = r'(\d+.\d+.\d+.\d+/\d+)'
    match = re.search(pattern, data.decode("utf-8"))
    if match:
        return match.group(1)
    raise KeyError()


def get_ip(node: Node) -> None:
    """
    The function `get_ip` retrieves the IP address of a node by connecting to its console using Telnet
    and extracting the IP address from the console output.
    
    :param node: The `node` parameter is an instance of the `Node` class. It represents a network node
    and contains information such as its name and console port
    :type node: Node
    :return: the IP address of the given node.
    """
    
    console = telnetlib.Telnet('127.0.0.1', node.console, timeout=5)
    console.write(b'show ip\n')
    data = console.read_until(b'EOF\n', timeout=0.1)
    console.close()
    try:
        ip = extract_ip(data)
    except KeyError:
        print(f'ip not found for node {node.name} with port: {node.console}')

    return ip
    

def set_ip(node, ip_addr, gateway_addr) -> None:
    """
    The function `set_ip` sets the IP address and gateway address of a node using a telnet connection.
    
    :param node: The `node` parameter represents the node or device on which you want to set the IP
    address and gateway address
    :param ip_addr: The `ip_addr` parameter is the IP address that you want to set for the node. It
    should be a string representing a valid IP address, such as "192.168.0.1"
    :param gateway_addr: The `gateway_addr` parameter is the IP address of the gateway that the node
    will use to access other networks. It is the IP address of the router or network device that
    connects the node's network to other networks
    """

    console = telnetlib.Telnet('127.0.0.1', node.console, timeout=5)
    cmd = f'ip {ip_addr} {gateway_addr}\n'
    console.write(cmd.encode('utf-8'))
    console.close()
