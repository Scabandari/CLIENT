from random import randint
import json
import ast
import socket
import os
import ast

#UPDATE_STATE = 'UPDATE-STATE'
REGISTER = 'REGISTER'
REGISTERED = 'REGISTERED'
DE_REGISTER = 'DE-REGISTER'
REQUEST_NUMBER = 1
GUI_MSG_NUMBER = 1  # GUI is receiver here, todo should be 0 ?
# CLIENT_MSG_NUMBER = 1
list_of_connections = [()] # each () consists of socket, and port number for each tcp item
# https://www.digitalocean.com/community/tutorials/how-to-handle-plain-text-files-in-python-3
# https://www.tutorialspoint.com/python3/python_files_io.htm


def get_client_msg_num(file_name):
    lines = []
    msg_num = 1
    if os.path.getsize(file_name) > 0:
        with open(file_name, 'r') as f:
            for line in f:
                lines.append(line)
    if len(lines) > 0:
        last_line = ast.literal_eval(lines[-1])
        msg_num = int(last_line[0]) + 1
    return msg_num


def attempt_recovery():
    global GUI_MSG_NUMBER
    GUI_MSG_NUMBER = get_client_msg_num('toGui.txt')


def msg_to_queue(udp_queue, queue_lock, msg):
    """
         This function takes a msg and a queue and binarizes it then adds to the queue
    """
    msg = dict_to_bytes(msg)
    with queue_lock:
        udp_queue.append(msg)


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
        'port': my_tcp_port  #todo should be using port from user import here?
    }
    return send_msg


def get_unregistration():
    # name = input("Enter the client name to de-register: ")
    # ip = input("Enter the corresponding IP address for de-registration: ")
    name = 'ryan'
    ip = '192.168.0.107'
    send_msg = {
        'request': req_number(),
        'type': DE_REGISTER,
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


def update_txt(msg_type, items, gui_msg_number=None):
    """
    This function updates the text file that passes msg's to the gui. Mainly the state of items for bid
    :param items:
    :return:
    """
    global GUI_MSG_NUMBER
    gui_tup = (GUI_MSG_NUMBER, msg_type, items)
    #gui_tup = (gui_msg_number, msg_type, items)
    GUI_MSG_NUMBER += 1
    #gui_msg_number += 1
    with open('toGui.txt', 'a') as f:
        f.write(str(gui_tup))
        f.write("\n")


def show_all_messages():
    send_msg = {'type': 'SHOW_ITEMS'}
    return send_msg


def get_port(item):  # bid_item=None here but pass it from what we get from gui
    #global current_item
    #current_item = item
    send_msg = {
        'type': 'GETPORT',
        'item': item 
    }
    return send_msg


def establishTcpConnection(HOST, portNumber):
    for a_socket in list_of_connections:
        if a_socket:
            if a_socket[1] == portNumber:  # there is already a socket for that item
                return
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Connecting to TCP connection for the item")
    tcp_socket.connect((HOST, portNumber))
    initial_data = tcp_socket.recv(1024)
    print(initial_data)
    entry = (tcp_socket, portNumber)
    list_of_connections.append(entry)


def sendTCPMessage(msg):
    msg = msg.decode("utf-8")
    dict_msg = ast.literal_eval(msg)
    for a_socket in list_of_connections:
        if a_socket:
            if a_socket[1] == dict_msg['port #']:
                send_bytes = dict_to_bytes(msg)
                a_socket[0].send(send_bytes)


def get_bid(Host, bidport, bid_param, name, current_item):
    #global current_item
    # establishTcpConnection(Host, bidport)
    bid = bid_param
    send_msg = {
        'type': 'BID',
        'request': req_number(),
        'item': itemNum,
        'amount': bid,
        'name': name,
        'port #': bidport
    }
    return send_msg

