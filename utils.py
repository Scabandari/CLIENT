from random import randint
import json
import socket

REGISTER = 'REGISTER'
REGISTERED = 'REGISTERED'
REQUEST_NUMBER = 1
GUI_MSG_NUMBER = 1
current_item = 0

# https://www.digitalocean.com/community/tutorials/how-to-handle-plain-text-files-in-python-3
# https://www.tutorialspoint.com/python3/python_files_io.htm


def req_number():
    global REQUEST_NUMBER
    num = REQUEST_NUMBER
    REQUEST_NUMBER += 1
    return num


def get_registration(my_tcp_port):
    # name = input("Enter your unique name identifier: ")
    # ip_address = input("Enter the ip address of the computer you'll be bidding from: ")
    # port = input("Enter the port number your computer will be listening on: ")
    name = 'ryan'
    ip_address = '192.168.0.107'
    port = 5000

    send_msg = {
        'request': req_number(),
        'type': REGISTER,
        'name': name,
        'ip': ip_address,
        'port': my_tcp_port
    }
    return send_msg


def get_unregistration():
    # name = input("Enter the client name to de-register: ")
    # ip = input("Enter the corresponding IP address for de-registration: ")
    name = 'ryan'
    ip = '192.168.0.107'
    send_msg = {
        'request': req_number(),
        'type': 'DE-REGISTER',
        'name': name,
        'ip': ip
    }
    return send_msg


def get_offer():
    # name = input("Enter your unique name identifier: ")
    # ip_address = input("Enter the ip address of your computer: ")
    # description = input("Enter a description of the item on offer: ")
    # min_bid = input("Enter the minimum bid: ")
    name = 'ryan'
    # ip_address = '192.168.0.107'
    ip_address = '192.168.0.101'
    description = 'bat'
    min_bid = 10
    send_msg = {
        'type': 'OFFER',
        'request': req_number(),
        'name': name,
        'ip': ip_address,
        'description': description,
        'minimum bid': min_bid
    }
    return send_msg


def dict_to_bytes(dict_):
    json_str = json.dumps(dict_)
    bytes_ = json_str.encode('utf-8')  # todo: was ascii
    return bytes_


def update_txt(items):
    """
    This function updates the text file that passes msg's to the gui. Mainly the state of items for bid
    :param items:
    :return:
    """
    global GUI_MSG_NUMBER
    gui_tup = (GUI_MSG_NUMBER, items)
    GUI_MSG_NUMBER += 1
    with open('toGui.txt', 'a') as f:
        f.write(str(gui_tup))

def getShowAllMessages():
    send_msg = {'type': 'SHOW_ITEMS'}
    return send_msg

#I don't see the item 
def get_port():
    bid_item = input("Enter the Item Number that you wish to bid on: ")
    global current_item
    current_item = bid_item 
    send_msg = {
        'type': 'GETPORT',
        'item': bid_item 
    }
    return send_msg

def establishTcpConnection(HOST, portNumber):
    print("Connecting to TCP connection for the item")
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((HOST, 5050))
    data = tcp_socket.recv(1024)
    print(data)

def get_bid(Host, bidport):
    port = bidport #connect to this port for bid over TCP
    print(port)
    global current_item
    
    establishTcpConnection(Host, bidport)
    
    bid = input("Enter the bid amount: ")
    send_msg = {
        'type': 'BID',
        'request': req_number(),
        'item': current_item,
        'amount': bid
    }
    return send_msg

