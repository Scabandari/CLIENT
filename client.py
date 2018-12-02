import socket
import ast
from utils import (get_registration, get_unregistration, dict_to_bytes, get_offer,
                   update_txt, show_all_messages, get_port, get_bid, sendTCPMessage,
                   tcp_socket, req_number, msg_to_queue)
import threading
from time import sleep

"""Here I'm thinking we need 2 threads in addition to the main thread. One that constantly checks 
    a list to see if there are user msg's to be sent over UDP and then another thread doing same 
    for TCP. We now have a 3rd thread checking for incoming UDP messages. When user decides from main 
    thread to answer at terminal they want to register they'll give some info and we create a msg 
    and put into the list the UDP thread keeps checking."""
SERVER_CRASHED = 'SERVER-CRASHED'
REGISTER = 'REGISTER'
UNREGISTERED = 'UNREGISTERED'
BID = 'BID'
CLIENT_MSG_NUMBER = 0  # next number of incoming msg from gui to client
RETURN_MSG = 'RETURN-MSG'
UPDATE_STATE = 'UPDATE-STATE'
UPDATE_CLIENTS = 'UPDATE-CLIENTS'
ITEMPORT = 'ITEMPORT' 
current_port = 0
current_item = 0

resend_register = True
latest_registration = {}
latest_registration_lock = threading.Lock()
port_lock = threading.Lock()

udp_messages = []
udp_msg_lock = threading.Lock()
tcp_messages = []
tcp_msg_lock = threading.Lock()

general_lock = threading.Lock()

tcp_messages_returned = []  # tcp msg's returned from server, todo need this?
tcp_ret_lock = threading.Lock()
terminal_lock = threading.Lock()
#HOST = "192.168.1.184"  # this would normally be different and particular to the host machine ie client
#HOST = "172.31.121.120"
#HOST = '192.168.0.106'
HOST = '172.31.19.215'
UDP_PORT = 5075  # Clients UDP port they are listening on
#SERVER_IP = "172.31.121.120"
#SERVER_IP = '192.168.0.106'
SERVER_IP = '172.31.19.215'
SERVER_UDP_PORT = 5024
SERVER = (SERVER_IP, SERVER_UDP_PORT)
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
udp_socket.bind((HOST, UDP_PORT))

start_receiving_tcp_messages = False

tcp_ip = HOST  # won't usually, get tcp servers machines local ip address on LAN
tcp_server_port = 5002
MY_TCP_PORT = 5010  # For listening, the server needs to know which port we're listening on
# when sending msg's to all clients over TCP
#tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# TCP_CLIENT_PORT = 5071  # the port the client is listening for responses on
# If we wanted to set the port the client would listen for responses on we'd bind it like so
# tcp_socket.bind((HOST, TCP_CLIENT_PORT))
#tcp_socket.connect((tcp_ip, tcp_server_port))


# we need to check the

def tcp_incoming():
    while True:
        if start_receiving_tcp_messages: # this condition will be true after conn to item is made
            with tcp_msg_lock:
                # print('hello, im in tcp_incoming')
                message, addr = tcp_socket.recvfrom(1024)
                message = message.decode('utf-8')
                msg_dict = ast.literal_eval(message)
                print("message received over tcp: ")
                print(msg_dict)
                '''
                try:
                    if msg['set port']:
                        current 
                '''


def tcp_outgoing():
    while True:
        if tcp_messages:
            with tcp_msg_lock:
                msg = tcp_messages.pop(0)
                sendTCPMessage(msg)

# def tcp_incoming():
#     global MY_TCP_PORT
#     while True:
#         msg_received = tcp_socket.recv(1024).decode('utf-8')
#         msg = ast.literal_eval(msg_received)
#         with terminal_lock:
#             print("Received tcp msg: " + str(msg))
#         try:
#             if msg['set port']:
#                 MY_TCP_PORT = msg['port']
#         except KeyError:
#             pass
#
#
# def tcp_outgoing():
#     while True:
#         if tcp_messages:  # msg's to send
#             with tcp_msg_lock:
#                 msg = tcp_messages.pop(0)
#             tcp_socket.send(msg)
#             return_msg = tcp_socket.recv(1024).decode('utf-8')
#             with terminal_lock:
#                 print("Received back tcp response: " + return_msg)


def gui_msg(udp_messages_, udp_msg_lock_, CLIENT_MSG_NUMBER_):
    # global CLIENT_MSG_NUMBER
    # global udp_msg_lock
    # global udp_messages
    global latest_registration
    global latest_registration_lock
    global port_lock
    #global resend_register
    path = 'C:\\Users\\Adamd\\OneDrive\\School\\COEN445\\project\\server\\SERVER\\state.txt'
    item_list = open(path, 'r')
    cport = 0
    global REGISTER
    """ Read the next last line of text from toClient.txt and if """
    # todo read the next line in toClient.txt and put the msg in the correct queue
    while True:
        with open('toClient.txt', 'r') as f:
            for line in f:  # line ===> (number, state_dict)
                try:
                    line = ast.literal_eval(line)
                    if int(line[0]) >= CLIENT_MSG_NUMBER_:
                        print("reading toClient.txt")
                        CLIENT_MSG_NUMBER_ += 1
                        msg_for_server = line[2]
                        if line[1] == REGISTER:
                            with latest_registration_lock:
                                latest_registration = line[2]
                        msg_for_server['request'] = req_number()
                        send_bytes = dict_to_bytes(line[2])
                        if line[1] == BID:  # BID is the only kind of msg to be sent over TCP? I think so
                            item = line[2]['item #']
                            amount = line[2]['amount']
                            name = line[2]['name']
                            item_read = item_list.read()
                            item_dict = ast.literal_eval(item_read)
                            items = item_dict['items']
                            print(items)
                            for element in range (0, len(items)):
                                if int(items[element]['item #']) == int(item):
                                    print('got here')
                                    cport = items[element]['port #']

                                send_msg = get_bid(HOST, cport, amount, name, item)

                                global start_receiving_tcp_messages
                                start_receiving_tcp_messages = True
                                try:
                                    send_bytes = dict_to_bytes(send_msg)
                                    with tcp_msg_lock:
                                        tcp_messages.append(send_bytes)
                                except UnboundLocalError:
                                    pass

                        else:  # else if not a bid we send over UDP
                            with udp_msg_lock_:
                                udp_messages_.append(send_bytes)
                        # try:
                        #     send_bytes = dict_to_bytes(line[2])
                        #     with udp_msg_lock:
                        #         udp_messages.append(send_bytes)
                        # except UnboundLocalError:
                        #     pass
                        # msg_to_queue(udp_messages, udp_msg_lock, line[2])
                except SyntaxError:
                    print("Could not read line in toClient.txt")
                    pass


def udp_incoming():
    global latest_registration_lock
    global latest_registration
    global resend_register
    # there are times when the UDP server will send all connected clients a msg such as NEW-ITEM msg's
    while True:
        message, addr = udp_socket.recvfrom(1024)
        message = message.decode('utf-8')
        msg_dict = ast.literal_eval(message)
        if msg_dict['type'] == UNREGISTERED and resend_register is True:
            with latest_registration_lock:
                reg = latest_registration
            resend_register = False
            send_bytes = dict_to_bytes(reg)
            with udp_msg_lock:
                udp_messages.append(send_bytes)
        elif msg_dict['type'] == UNREGISTERED and resend_register is False:
            resend_register = True

        if msg_dict['type'] == UPDATE_CLIENTS:
            update_txt(UPDATE_STATE, msg_dict['items'])
            continue
        elif msg_dict['type'] == SERVER_CRASHED:
            update_txt(SERVER_CRASHED, msg_dict['description'])
            continue
        # elif msg_dict['type'] == ITEMPORT:  #
        #     global current_port
        #     current_port = msg_dict['port']
        #     print(current_port)
        print("Received udp message: " + message)
        update_txt(RETURN_MSG, message)


def udp_outgoing():
    while True:
        if udp_messages:  # msg's to send
            with udp_msg_lock:
                msg = udp_messages.pop(0)
            udp_socket.sendto(msg, SERVER)
            # response, addr = udp_socket.recvfrom(1024)
            # response = response.decode('utf-8')
            # print("Receive back udp response: " + response)


gui_msg_reader = threading.Thread(target=gui_msg, args=(udp_messages, udp_msg_lock, CLIENT_MSG_NUMBER))
gui_msg_reader.start()

udp_incoming_thread = threading.Thread(target=udp_incoming)
udp_incoming_thread.start()

udp_outgoing_thread = threading.Thread(target=udp_outgoing)
udp_outgoing_thread.start()

tcp_incoming_thread = threading.Thread(target=tcp_incoming)
tcp_incoming_thread.start()

tcp_outgoing_thread = threading.Thread(target=tcp_outgoing)
tcp_outgoing_thread.start()


def get_user_command():  # should be set on start up, include when sending TCP msg's
    """This function gives the user their options of different actions they can take
        and either returns None if their choice doesn't exist or the msg to be send
         over UDP to the server"""

    # todo the server should keep track of the request numbers so if the client initiates the contact how does it know
    # todo which request numbers are already taken or not???

    """
        Get a command from the user, determine if TCP or UDP msg will be sent and form msg
        then put in respective queue for dispatch by either TCP or UDP thread in client.py
    """
    choice = input("Enter a command: \n" +
                   "'r' ==> Registration and offers\n" +
                   "'b' ==> Bidding etc.\n" +
                   "'c' ==> Cancel, will free up terminal to display any responses from server\n::")
    if choice is 'r':
        selection = input("Enter a command: \n" +
                          "'r' ==> Registrations \n" +
                          "'of' ==> Offers:: \n")
        if selection == 'r':
            register_unregister = input("Enter a command: \n" +
                                        "'r' ==> Register to be able to offer or bid\n" +
                                        "'d' ==> De-register if you are already registered\n::")
            if register_unregister == 'r':
                send_msg = get_registration(MY_TCP_PORT)
            elif register_unregister == 'd':
                send_msg = get_unregistration()
            else:
                print("That option isn't available")
                return None
        elif selection == 'of':
            send_msg = get_offer()

        try:
            send_bytes = dict_to_bytes(send_msg)
            with udp_msg_lock:
                udp_messages.append(send_bytes)
        except UnboundLocalError:
            pass

    elif choice is 'b':
        """Before bidding for a given item, a registered client has to establish a TCP connection to
            the TCP socket associated with the item of interest at the server side. After this
            connection, a client can bid on the item by sending a BID message."""
        print("These are the items available:")
        # message to show all items
        send_msg = show_all_messages()
        # need to differentiate these two messages
        
        try:
            send_bytes = dict_to_bytes(send_msg)
            with udp_msg_lock:
                udp_messages.append(send_bytes)
        except UnboundLocalError:
            pass
        sleep(0.5)  # temp fix for display to allow udp incoming thread to run before the rest of the code runs



        #send_msg = get_port()
        try:
            send_bytes = dict_to_bytes(send_msg)
            with udp_msg_lock:
                udp_messages.append(send_bytes)
        except UnboundLocalError:
            pass
        sleep(2)  # need to fix this

        if current_port != 0:
            #send_msg = get_bid(HOST, current_port)

            global start_receiving_tcp_messages
            start_receiving_tcp_messages = True

            try:
                send_bytes = dict_to_bytes(send_msg)
                with tcp_msg_lock:
                    tcp_messages.append(send_bytes)
            except UnboundLocalError:
                pass
        else:
            print("This item does not exit")
    elif choice is 'c':
        return
    else:
        print("That option isn't available")
        return None

"""
#########################################################################################
## FOR NOW YOU GUYS ARE USING THIS
#while True:
 #   get_user_command()
##########################################################################################


########################################################################################
## ONCE GUI IS FINISHED WE USE THIS
udp_incoming_thread.join()

udp_outgoing_thread.join()

# tcp_incoming_thread.join()

tcp_outgoing_thread.join()

gui_msg_reader.join()
########################################################################################
"""