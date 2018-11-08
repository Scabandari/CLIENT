from random import randint
import json
REGISTER = 'REGISTER'
REGISTERED = 'REGISTERED'
REQUEST_NUMBER = 1

# https://www.digitalocean.com/community/tutorials/how-to-handle-plain-text-files-in-python-3
# https://www.tutorialspoint.com/python3/python_files_io.htm


def req_number():
    global REQUEST_NUMBER
    num = REQUEST_NUMBER
    REQUEST_NUMBER += 1
    return num


def get_registration(my_tcp_port, user):
    # name = input("Enter your unique name identifier: ")
    # ip_address = input("Enter the ip address of the computer you'll be bidding from: ")
    # port = input("Enter the port number your computer will be listening on: ")
    length = len(user)
    name = user[length-1]['name']
    ip_address = user[length-1]['ip']
    port = user[length-1]['port']

    send_msg = {
        'request': req_number(),
        'type': REGISTER,
        'name': name,
        'ip': ip_address,
        'port': port
    }
    return send_msg


def get_unregistration():
    # name = input("Enter the client name to de-register: ")
    # ip = input("Enter the corresponding IP address for de-registration: ")
    name = 'ryan'
    ip = '172.30.65.196'
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
    ip_address = '172.30.65.196'
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

def not_sold():
    notifyNS = 'Not-Sold'
    item_num = 100
    reason = 'No Valid Bid'
    send_msg = {
        'type': notifyNS,
        'item_number': item_num,
        'reason': reason
    }
    return send_msg

def sold_to():
    notifyS = 'SoldTo'
    item_num = 90
    name = 'ryan'
    ip_address = '172.30.65.196'
    port = 5000
    amount = 1000
    send_msg = {
        'type': notifyS,
        'item_number': item_num,
        'name': name,
        'ip': ip_address,
        'port': port,
        'amount': amount
    }
    return send_msg

def bid_over():
    notifyBO = 'Bid-Over'
    item_num = 95
    amount = 100
    send_msg = {
        'type': notifyBO,
        'item': item_num,
        'amount': amount
    }
    return send_msg


def dict_to_bytes(dict_):
    json_str = json.dumps(dict_)
    bytes_ = json_str.encode('utf-8')  # todo: was ascii
    return bytes_






