from random import randint
import json
CHOICES = ['r']
REGISTER = 'REGISTER'
REGISTERED = 'REGISTERED'

# todo https://www.digitalocean.com/community/tutorials/how-to-handle-plain-text-files-in-python-3
# https://www.tutorialspoint.com/python3/python_files_io.htm


def send_udp(msg, socket_, server):  # todo needs socket param?
    msg = str.encode(msg)
    socket_.sendto(msg, server)
    response, addr = socket_.recvfrom(1024)
    response = response.decode('utf-8')
    print(response)


# todo this possibly returns None, maybe change this
def get_user_command(state=None ):
    """This function gives the user their options of different actions they can take
        and either returns None if their choice doesn't exist or the msg to be send
         over UDP to the server"""
    choice = input("Enter 'r' if you would like to register: ")
    if choice is CHOICES[0]:
        name = input("Enter your unique name identifier: ")
        ip_address = input("Enter the ip address of the computer you'll be bidding from: ")
        port = input("Enter the port number your computer will be listening on: ")
        request_number = randint(0, 100000)
        send_msg = {'request': request_number,
                    'type': REGISTER,
                    'name': name,
                    'ip': ip_address,
                    'port': port}
        send_bytes = dict_to_bytes(send_msg)
    else:
        print("That option isn't available")
        return None
    return send_bytes


def dict_to_bytes(dict_):
    json_str = json.dumps(dict_)
    bytes_ = json_str.encode('utf-8')  # todo: was ascii
    return bytes_